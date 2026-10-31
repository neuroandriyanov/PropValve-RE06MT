"""Data-only reader for NRBF project files. Never loads .NET types or executes code.

Records retain byte spans, allowing narrowly scoped edits without reserializing
the application's object graph. Unrecognized record types fail closed.
"""
import json
import math
import struct
import sys
from pathlib import Path


class Reader:
    def __init__(self, data):
        self.data, self.pos = data, 0
        self.objects, self.metadata, self.spans = {}, {}, {}
        self.libraries = {}

    def take(self, n):
        if n < 0 or self.pos + n > len(self.data):
            raise ValueError('Truncated record')
        result = self.data[self.pos:self.pos + n]
        self.pos += n
        return result

    def number(self, fmt):
        return struct.unpack('<' + fmt, self.take(struct.calcsize('<' + fmt)))[0]

    def string(self):
        length, shift = 0, 0
        while True:
            byte = self.number('B')
            length |= (byte & 127) << shift
            if not byte & 128:
                break
            shift += 7
            if shift > 28:
                raise ValueError('Invalid string length')
        return self.take(length).decode('utf-8')

    def primitive(self, kind):
        formats = {1: '?', 2: 'B', 6: 'd', 7: 'h', 8: 'i', 9: 'q',
                   10: 'b', 11: 'f', 12: 'q', 13: 'Q', 14: 'H', 15: 'I', 16: 'Q'}
        if kind in formats:
            return self.number(formats[kind])
        if kind in (5, 18):
            return self.string()
        if kind == 17:
            return None
        raise ValueError(f'Unsupported primitive {kind} at {self.pos}')

    def type_info(self, kind):
        if kind in (0, 7):
            return self.number('B')
        if kind == 3:
            return self.string()
        if kind == 4:
            return (self.string(), self.number('i'))
        if kind in (1, 2, 5, 6):
            return None
        raise ValueError(f'Unsupported binary type {kind}')

    def members(self, objid, metadata):
        name, names, types, info = metadata
        obj = {'$id': objid, '$type': name, 'fields': {}}
        self.objects[objid] = obj
        for member, kind, extra in zip(names, types, info):
            start = self.pos
            obj['fields'][member] = self.primitive(extra) if kind == 0 else self.value()
            self.spans[(objid, member)] = (start, self.pos, kind, extra)
        return obj

    def array_values(self, count, primitive=None, objid=None):
        if count < 0 or count > 1000000:
            raise ValueError('Invalid array size')
        values = []
        while len(values) < count:
            start = self.pos
            value = self.primitive(primitive) if primitive is not None else self.value()
            if isinstance(value, dict) and '$nulls' in value:
                values.extend([None] * value['$nulls'])
            else:
                self.spans[(objid, len(values))] = (start, self.pos, 0 if primitive is not None else 2, primitive)
                values.append(value)
        if len(values) != count:
            raise ValueError('Null run exceeds array')
        return values

    def value(self):
        start = self.pos
        record = self.number('B')
        if record == 0:
            self.header = [self.number('i') for _ in range(4)]
            return {'$header': self.header}
        if record == 12:
            lib = self.number('i')
            self.libraries[lib] = self.string()
            return self.value()  # library records may appear before a member value
        if record in (4, 5):
            objid, name, count = self.number('i'), self.string(), self.number('i')
            names = [self.string() for _ in range(count)]
            types = [self.number('B') for _ in range(count)]
            info = [self.type_info(kind) for kind in types]
            if record == 5:
                self.number('i')
            metadata = name, names, types, info
            self.metadata[objid] = metadata
            return self.members(objid, metadata)
        if record == 1:
            objid, metadata_id = self.number('i'), self.number('i')
            return self.members(objid, self.metadata[metadata_id])
        if record == 6:
            objid = self.number('i')
            offset = self.pos
            obj = {'$id': objid, '$string': self.string()}
            self.objects[objid] = obj
            self.spans[(objid, '$string')] = (offset, self.pos, 'string', None)
            return obj
        if record == 9:
            return {'$ref': self.number('i')}
        if record == 10:
            return None
        if record == 11:
            return {'$end': True}
        if record == 8:
            kind = self.number('B')
            offset = self.pos
            result = self.primitive(kind)
            return {'$primitive': kind, 'value': result, '$offset': offset, '$end_offset': self.pos}
        if record in (13, 14):
            return {'$nulls': self.number('B' if record == 13 else 'i')}
        if record in (15, 16, 17):
            objid, count = self.number('i'), self.number('i')
            primitive = self.number('B') if record == 15 else None
            obj = {'$id': objid, '$array': [], '$primitive_type': primitive}
            self.objects[objid] = obj
            obj['$array'] = self.array_values(count, primitive, objid)
            return obj
        if record == 7:
            objid, arraytype, rank = self.number('i'), self.number('B'), self.number('i')
            lengths = [self.number('i') for _ in range(rank)]
            lower = [self.number('i') for _ in range(rank)] if arraytype in (3, 4, 5) else None
            kind = self.number('B')
            extra = self.type_info(kind)
            obj = {'$id': objid, '$array': [], '$shape': lengths, '$lower': lower,
                   '$binary_type': kind, '$extra': extra}
            self.objects[objid] = obj
            obj['$array'] = self.array_values(math.prod(lengths), extra if kind == 0 else None, objid)
            return obj
        raise ValueError(f'Unsupported NRBF record {record} at {start}')

    def read(self):
        while self.pos < len(self.data):
            value = self.value()
            if isinstance(value, dict) and value.get('$end'):
                break
        if self.pos != len(self.data):
            raise ValueError('Trailing data')
        return self

    def resolve(self, value):
        while isinstance(value, dict) and '$ref' in value:
            value = self.objects[value['$ref']]
        if isinstance(value, dict) and '$string' in value:
            return value['$string']
        if isinstance(value, dict) and '$primitive' in value:
            return value['value']
        return value


if __name__ == '__main__':
    reader = Reader(Path(sys.argv[1]).read_bytes()).read()
    for obj in reader.objects.values():
        name = obj.get('$type', '')
        if name in ('ADICtrls.DCHex', 'ADICtrls.LinearInterpolator', 'Analog.Data.UIData'):
            print(json.dumps({'id': obj['$id'], 'type': name,
                              'fields': {k: reader.resolve(v) for k, v in obj['fields'].items()}}, ensure_ascii=True))

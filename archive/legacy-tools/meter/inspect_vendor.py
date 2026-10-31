"""Read-only inspection of the meter's PE binaries; no vendor code is loaded."""
import hashlib
import json
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / 'программа_мультиметра' / 'UT61D+'


def inspect(path):
    data = path.read_bytes()
    pe = struct.unpack_from('<I', data, 0x3c)[0]
    machine, nsections = struct.unpack_from('<HH', data, pe + 4)
    optsize = struct.unpack_from('<H', data, pe + 20)[0]
    opt = pe + 24
    magic = struct.unpack_from('<H', data, opt)[0]
    directories = opt + (96 if magic == 0x10b else 112)
    sections = []
    for i in range(nsections):
        offset = opt + optsize + i * 40
        virtual_size, rva, raw_size, raw = struct.unpack_from('<IIII', data, offset + 8)
        sections.append((rva, max(virtual_size, raw_size), raw))

    def at(rva):
        for start, size, raw in sections:
            if start <= rva < start + size:
                return raw + rva - start
        raise ValueError(f'Unmapped RVA {rva:x}')

    def string(offset):
        return data[offset:data.index(b'\0', offset)].decode('ascii', errors='replace')

    imports = {}
    import_rva = struct.unpack_from('<I', data, directories + 8)[0]
    if import_rva:
        off = at(import_rva)
        while True:
            original, _, _, name, first = struct.unpack_from('<IIIII', data, off)
            if not name:
                break
            names = []
            pointer = at(original or first)
            width = 4 if magic == 0x10b else 8
            while True:
                thunk = int.from_bytes(data[pointer:pointer + width], 'little')
                if not thunk:
                    break
                names.append(f'ordinal:{thunk & 0xffff}' if thunk >> (width * 8 - 1) else string(at(thunk) + 2))
                pointer += width
            imports[string(at(name))] = names
            off += 20
    ascii_strings = [m.decode('ascii') for m in re.findall(rb'[ -~]{5,}', data)]
    pattern = re.compile(r'HidUart|HidDevice|CP211|Serial|Command|Dmm|Read|Write|9600|UT61|\.dll|\.csv|\.db', re.I)
    return {'file': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(data).hexdigest(),
            'machine': hex(machine), 'imports': imports,
            'relevant_strings': sorted(set(s for s in ascii_strings if pattern.search(s)))}


if __name__ == '__main__':
    for name in ['DMM.exe', 'Lib/CustomDmm.dll', 'Lib/CP2110.dll', 'MyCore.dll']:
        print(json.dumps(inspect(ROOT / name), ensure_ascii=True))

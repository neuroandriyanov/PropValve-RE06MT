"""Patch only existing double coefficients in a SigmaStudio project copy."""
import argparse
import struct
from pathlib import Path
from nrbf_project import Reader


def patch(source, destination, coefficients):
    original = source.read_bytes()
    reader = Reader(original).read()
    cells = [o for o in reader.objects.values() if o.get('$type') == 'ADICtrls.LinearInterpolator']
    if len(cells) != 1:
        raise ValueError('Expected exactly one linear interpolator')
    cell = cells[0]
    values = reader.resolve(cell['fields']['values'])
    if values.get('$primitive_type') != 6 or len(values['$array']) != len(coefficients):
        raise ValueError('Coefficient array shape mismatch')
    updated = bytearray(original)
    for index, coefficient in enumerate(coefficients):
        if not -1 <= coefficient <= 1:
            raise ValueError('Calibration DAC coefficients must be within -1..1')
        start, end, kind, primitive = reader.spans[(values['$id'], index)]
        if (end - start, kind, primitive) != (8, 0, 6):
            raise ValueError('Unexpected serialized coefficient format')
        updated[start:end] = struct.pack('<d', coefficient)
    verified = Reader(bytes(updated)).read()
    actual = verified.objects[values['$id']]['$array']
    if actual != coefficients or len(updated) != len(original):
        raise ValueError('Project validation failed')
    allowed = set()
    for index in range(len(coefficients)):
        start, end, _, _ = reader.spans[(values['$id'], index)]
        allowed.update(range(start, end))
    if any(a != b and i not in allowed for i, (a, b) in enumerate(zip(original, updated))):
        raise ValueError('Unexpected changes outside the coefficient array')
    destination.write_bytes(updated)
    print({'project': str(destination), 'coefficients': actual,
           'min': reader.resolve(cell['fields']['Min']), 'max': reader.resolve(cell['fields']['Max'])})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--coefficients', required=True, help='Comma-separated existing table values')
    args = parser.parse_args()
    patch(args.source, args.destination, [float(v) for v in args.coefficients.split(',')])

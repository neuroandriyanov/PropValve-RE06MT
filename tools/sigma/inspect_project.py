"""Read a saved SigmaStudio project as data only; no GUI, USB, or .NET calls."""
import argparse
import hashlib
import json
from pathlib import Path
from nrbf_project import Reader

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PROJECT = ROOT / 'проект_сигма/Design1_parker_v0.dspproj'


def inspect(path):
    data = Path(path).read_bytes()
    reader = Reader(data).read()
    cells, tables, constants = [], {}, {}
    for obj in reader.objects.values():
        fields = obj.get('fields', {})
        kind = obj.get('$type', '')
        if 'nid' not in fields or 'name' not in fields or 'Pin' in kind:
            continue
        name = reader.resolve(fields['name'])
        if not name:
            continue
        cells.append({'name': name, 'nid': reader.resolve(fields['nid']), 'type': kind})
        if kind == 'ADICtrls.LinearInterpolator':
            tables[name] = {'min': float(reader.resolve(fields['Min'])),
                            'max': float(reader.resolve(fields['Max'])),
                            'coefficients': reader.resolve(fields['values'])['$array']}
        elif kind == 'ADICtrls.DCHex':
            constants[name] = reader.resolve(fields['textvalue'])
    return {'project': Path(path).name, 'sha256': hashlib.sha256(data).hexdigest(),
            'cell_count': len(cells), 'cells': cells, 'tables': tables, 'constants': constants}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', nargs='?', type=Path, default=DEFAULT_PROJECT)
    args = parser.parse_args()
    print(json.dumps(inspect(args.project), ensure_ascii=True, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()

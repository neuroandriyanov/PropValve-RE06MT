"""Check the delivered package and saved calibration without accessing hardware."""
import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools/sigma'))
from inspect_project import inspect


def sha256(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    errors = []
    manifest = json.loads((ROOT / 'docs/manifest.json').read_text(encoding='utf-8'))
    for entry in manifest['files']:
        path = (ROOT / entry['path']).resolve()
        if not path.is_relative_to(ROOT):
            errors.append('Manifest path escapes package: ' + entry['path'])
        elif not path.is_file():
            errors.append('Missing: ' + entry['path'])
        elif sha256(path) != entry['sha256']:
            errors.append('Changed since packaging: ' + entry['path'])
    folder = ROOT / 'проект_сигма'
    project = inspect(folder / 'Design1_parker_v0.dspproj')
    tables = project['tables']
    settings = json.loads((folder / 'current_calibration_settings.json').read_text())
    vin = json.loads((folder / 'voltage_input_settings.json').read_text())
    expected = {'CURRENT_0_3A': settings['command'], 'I_FEEDBACK_0_1': settings['feedback'],
                'VIN_TABLE_0_10V': vin['table']}
    for name, table in expected.items():
        actual = tables.get(name)
        if actual is None or any(actual[k] != float(table[k]) for k in ('min', 'max')) or actual['coefficients'] != table['coefficients']:
            errors.append('Saved project/settings mismatch: ' + name)
    exports = {'CURRENT_0_3A': 'current_command_0_3A.txt',
               'I_FEEDBACK_0_1': 'current_feedback_0_3A.txt',
               'VIN_TABLE_0_10V': 'voltage_input_0_10V.txt',
               'Interpolator1': 'linintdacout_calibrated.txt'}
    for name, filename in exports.items():
        values = [float(v) for v in (folder / filename).read_text().split()]
        actual = tables.get(name, {}).get('coefficients', [])
        if len(values) != len(actual) or not all(math.isclose(a, b, rel_tol=0, abs_tol=1e-9) for a, b in zip(values, actual)):
            errors.append('Saved project/TXT mismatch: ' + filename)
    constants = {'ZERO_CONSTANT': 0, 'DC2_3': 0, 'FB_MIN_CONST': -.78,
                 'FB_MAX_CONST': .70, 'VIN_ZERO': 0, 'VIN_ONE': 1}
    for name, value in constants.items():
        if project['constants'].get(name) != value:
            errors.append('Unexpected baseline constant: ' + name)
    names = {cell['name'] for cell in project['cells']}
    for name in ['ZERO_OFF', 'Inv1', 'VIN_LPF_20Hz', 'CURRENT_LPF_20Hz',
                 'VIN_LIMIT_MIN', 'VIN_LIMIT_MAX', 'FB_LIMIT_MIN', 'FB_LIMIT_MAX',
                 'VIN_MEAS_0_1', 'I_MEAS_0_1']:
        if name not in names:
            errors.append('Missing baseline block: ' + name)
    if names & {'CURRENT_INPUT_0_1', 'DC2_4'}:
        errors.append('Historical manual sources found in the working project')
    if project['sha256'] != sha256(folder / 'Design1_parker_transfer_2026-10-27.dspproj'):
        errors.append('Working project differs from the transfer snapshot')
    for path in folder.glob('*.dspproj'):
        inspect(path)
    print(json.dumps({'ok': not errors, 'manifest_files_checked': len(manifest['files']),
                      'projects_parsed': len(list(folder.glob('*.dspproj'))),
                      'tables_checked': len(exports), 'hardware_accessed': False,
                      'errors': errors}, indent=2, ensure_ascii=True))
    return 1 if errors else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({'ok': False, 'hardware_accessed': False, 'error': str(error)}, ensure_ascii=True))
        sys.exit(2)

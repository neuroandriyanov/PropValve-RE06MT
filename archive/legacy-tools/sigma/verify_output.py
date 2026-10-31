"""Measure the explicitly authorized 0..1 -> 0..10 V calibration.

Only operates the already-identified DC2_4 EDIT under its known parent.
Returns its input to zero on completion or failure. Never writes EEPROM.
"""
import argparse
import ctypes as C
import json
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from win32_sigma import U, focus, info, keys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'meter'))
from read_meter import Meter, find_devices


def set_input(hwnd, expected_parent, value):
    if not 0 <= value <= 1:
        raise ValueError('Only normalized input 0..1 is allowed')
    before = info(hwnd)
    if before['parent'] != expected_parent or '.EDIT.' not in before['class']:
        raise RuntimeError('DC2_4 control identity changed; aborting')
    focus(hwnd)
    text = C.create_unicode_buffer(format(value, '.9g'))
    U.SendMessageW(hwnd, 0x000c, 0, C.addressof(text))
    keys([0x0d])
    time.sleep(.15)
    actual = info(hwnd)['text']
    if abs(float(actual) - value) > 1e-8:
        raise RuntimeError(f'Input did not match requested value: {actual!r}')


def samples(meter, count=3):
    readings = []
    for index in range(count):
        value = meter.query()
        if not value['calibration_usable']:
            raise RuntimeError(f'Meter is not usable for DC voltage calibration: {value}')
        if value['volts'] is None or not -.05 <= value['volts'] <= 10.2:
            raise RuntimeError(f'Unexpected voltage: {value}')
        readings.append(value)
        if index + 1 < count:
            time.sleep(.4)
    return readings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hwnd', required=True, type=int)
    parser.add_argument('--parent', required=True, type=int)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    devices = find_devices()
    if len(devices) != 1:
        raise RuntimeError('Expected exactly one meter adapter')
    meter = Meter(*devices[0])
    report = {'started_utc': datetime.now(timezone.utc).isoformat(),
              'input_control': info(args.hwnd), 'points': [], 'completed': False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        for value in [0, .1, .125, .25, .375, .5, .625, .75, .875, 1]:
            set_input(args.hwnd, args.parent, value)
            time.sleep(1.2)
            readings = samples(meter)
            volts = [r['volts'] for r in readings]
            result = {'input': value, 'target_volts': value * 10,
                      'median_volts': statistics.median(volts), 'readings_volts': volts,
                      'error_volts': statistics.median(volts) - value * 10,
                      'raw_readings': readings}
            report['points'].append(result)
            args.output.write_text(json.dumps(report, indent=2), encoding='utf-8')
            print(json.dumps({k: v for k, v in result.items() if k != 'raw_readings'}), flush=True)
        report['completed'] = True
    finally:
        try:
            set_input(args.hwnd, args.parent, 0)
            time.sleep(1.2)
            report['restored_zero'] = samples(meter)
        finally:
            meter.close()
            report['finished_utc'] = datetime.now(timezone.utc).isoformat()
            args.output.write_text(json.dumps(report, indent=2), encoding='utf-8')
    report['max_abs_error_volts'] = max(abs(p['error_volts']) for p in report['points'])
    args.output.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'completed': True, 'max_abs_error_volts': report['max_abs_error_volts'],
                      'restored_zero_volts': [r['volts'] for r in report['restored_zero']]}), flush=True)


if __name__ == '__main__':
    main()

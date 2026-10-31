"""Read the connected UNI-T UT61D+ over USB HID, independently of its GUI.

Standard-library only. Does not install drivers, patch vendor software,
change meter range/mode, or alter its nonvolatile memory.
"""
import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from protocol import Framer, command, decode, uart_payload

SUPPORTED = {'vid_1a86&pid_e429': 'ch9329', 'vid_10c4&pid_ea80': 'cp2110'}


def find_devices():
    from win_hid import enumerate_paths
    return [(p, kind) for p in enumerate_paths() for token, kind in SUPPORTED.items() if token in p.lower()]


class Meter:
    def __init__(self, path, transport, passive=False):
        from win_hid import Hid
        self.hid = Hid(path, read_only=passive)
        self.transport, self.framer = transport, Framer()
        self.passive = passive
        try:
            if transport == 'cp2110' and not passive:
                # Volatile UART settings only. No FIFO purge and no reset.
                self.hid.feature(bytes.fromhex('41 01'))
                self.hid.feature(bytes.fromhex('50 00 00 25 80 00 00 03 00 00'))
        except BaseException:
            self.close()
            raise

    def close(self):
        self.hid.close()

    def query(self, timeout=2):
        if not self.passive:
            # Drain this handle's queued input reports, not the adapter FIFO.
            # Otherwise an open vendor app could leave old replies queued here.
            for _ in range(512):
                if not self.hid.io(timeout_ms=1):
                    break
            else:
                raise TimeoutError('Input queue is continuously busy; stop competing polling before calibration.')
        # Clear incomplete local framing left by a timed-out previous request.
        self.framer.buffer.clear()
        if not self.passive:
            request = command(0x5e)
            prefix = b'\0' if self.transport == 'ch9329' else b''
            report = prefix + bytes([len(request)]) + request
            self.hid.io(report.ljust(self.hid.caps.output_length, b'\0'))
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            remaining = max(1, int((deadline - time.monotonic()) * 1000))
            report = self.hid.io(timeout_ms=min(remaining, 500))
            if not report:
                continue
            for frame in self.framer.feed(uart_payload(report, self.transport)):
                if len(frame) != 19 or frame[2] != 16:
                    continue  # ACK/model replies are not measurements.
                reading = decode(frame)
                reading.update(timestamp_utc=datetime.now(timezone.utc).isoformat(timespec='milliseconds'),
                               received_unix=time.time(), transport=self.transport,
                               model='UT61D+ (user identified)', checksum_errors=self.framer.checksum_errors)
                return reading
        raise TimeoutError('No valid measurement received. Check USB/IR mode and competing polling apps.')


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    temporary.replace(path)


def publish(args, result, error=False):
    print(json.dumps(result, ensure_ascii=True, allow_nan=False),
          file=sys.stderr if error else sys.stdout, flush=True)
    if args.latest:
        atomic_json(args.latest, result)
    if args.log:
        args.log.parent.mkdir(parents=True, exist_ok=True)
        with args.log.open('a', encoding='utf-8') as log:
            log.write(json.dumps(result, ensure_ascii=False, allow_nan=False) + '\n')


def error_reading(error):
    return {'ok': False, 'error': str(error), 'calibration_usable': False,
            'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'received_unix': time.time()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='List compatible USB HID paths only')
    parser.add_argument('--path', help='Exact HID path when more than one compatible adapter is present')
    parser.add_argument('--count', type=int, default=1, help='Number of readings; 0 streams until Ctrl+C')
    parser.add_argument('--interval', type=float, default=1.0)
    parser.add_argument('--timeout', type=float, default=2.0)
    parser.add_argument('--passive', action='store_true', help='Listen only; do not issue measurement requests')
    parser.add_argument('--latest', type=Path, help='Atomically update latest JSON, including errors')
    parser.add_argument('--log', type=Path, help='Append every reading/error as JSON lines')
    args = parser.parse_args()
    if sys.platform != 'win32':
        parser.error('Native HID transport requires Windows')
    if args.count < 0 or args.interval < 0.1 or args.timeout <= 0:
        parser.error('count >= 0, interval >= 0.1, timeout > 0 required')
    try:
        devices = find_devices()
        if args.list:
            print(json.dumps([{'path': p, 'transport': t} for p, t in devices], indent=2))
            return 0
        if args.path:
            devices = [(p, t) for p, t in devices if p == args.path]
        if len(devices) != 1:
            raise RuntimeError(f'Expected one compatible meter adapter, found {len(devices)}. Use --list / --path.')
        path, transport = devices[0]
        meter = Meter(path, transport, passive=args.passive)
    except (OSError, ValueError, RuntimeError) as error:
        publish(args, error_reading(error), error=True)
        return 2
    failures = 0
    try:
        for index in iter(range(1 << 62)):
            if args.count and index >= args.count:
                break
            start = time.monotonic()
            try:
                result = meter.query(args.timeout)
                result.update(ok=True, sequence=index + 1)
            except (OSError, ValueError, TimeoutError) as error:
                failures += 1
                result = error_reading(error)
            publish(args, result)
            if not args.count or index + 1 < args.count:
                time.sleep(max(0, args.interval - (time.monotonic() - start)))
    except KeyboardInterrupt:
        pass
    finally:
        meter.close()
    return 1 if failures else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, RuntimeError) as error:
        print(json.dumps({'ok': False, 'error': str(error)}), file=sys.stderr)
        sys.exit(2)

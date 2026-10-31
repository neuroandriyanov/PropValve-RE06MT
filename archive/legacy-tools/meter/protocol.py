"""UNI-T UT61+ framing and strict voltage/current decoding.

Interoperability references (wire format, not copied source):
https://github.com/ljakob/unit_ut61eplus
https://github.com/mbraune/ut161b
"""
from decimal import Decimal, InvalidOperation


def command(code):
    # Restrict this reader to querying the display and model. No mode changes.
    if code not in (0x5e, 0x5f):
        raise ValueError('Only read-measurement and read-model queries are allowed')
    prefix = bytes([0xab, 0xcd, 3, code])
    return prefix + sum(prefix).to_bytes(2, 'big')


class Framer:
    def __init__(self):
        self.buffer = bytearray()
        self.checksum_errors = 0

    def feed(self, data):
        self.buffer.extend(data)
        frames = []
        while True:
            index = self.buffer.find(b'\xab\xcd')
            if index < 0:
                self.buffer[:] = self.buffer[-1:] if self.buffer[-1:] == b'\xab' else b''
                break
            del self.buffer[:index]
            if len(self.buffer) < 3:
                break
            length = self.buffer[2]
            if not 3 <= length <= 128:
                del self.buffer[0]
                continue
            total = 3 + length
            if len(self.buffer) < total:
                break
            frame = bytes(self.buffer[:total])
            if sum(frame[:-2]) & 0xffff != int.from_bytes(frame[-2:], 'big'):
                self.checksum_errors += 1
                del self.buffer[0]
                continue
            frames.append(frame)
            del self.buffer[:total]
        return frames


def uart_payload(report, transport):
    if transport == 'ch9329':
        # Windows includes the zero report ID; byte 1 is the UART byte count.
        if len(report) < 2 or report[0] != 0:
            raise ValueError('Invalid CH9329 report ID')
        length, offset = report[1], 2
        maximum = 63
    elif transport == 'cp2110':
        if not report:
            return b''
        length, offset, maximum = report[0], 1, 63
    else:
        raise ValueError('Unsupported transport')
    if length > maximum or offset + length > len(report):
        raise ValueError('Invalid HID payload length')
    # The remainder is HID padding and may contain arbitrary bytes.
    return report[offset:offset + length]


def decode(frame):
    if len(frame) != 19 or frame[:3] != b'\xab\xcd\x10':
        raise ValueError('Not a UT61+ measurement frame')
    if sum(frame[:-2]) & 0xffff != int.from_bytes(frame[-2:], 'big'):
        raise ValueError('Invalid checksum')
    payload = frame[3:-2]
    mode_code, range_code = payload[0], payload[1]
    if not 0x30 <= range_code <= 0x39:
        raise ValueError('Invalid range code')
    display = payload[2:9].decode('ascii').strip()
    mode = {0: 'ACV', 1: 'ACmV', 2: 'DCV', 3: 'DCmV', 4: 'Hz',
            5: 'Duty', 6: 'Resistance', 7: 'Continuity', 8: 'Diode',
            9: 'Capacitance', 10: 'Celsius', 11: 'Fahrenheit',
            12: 'DCuA', 13: 'ACuA', 14: 'DCmA', 15: 'ACmA',
            16: 'DCA', 17: 'ACA'}.get(mode_code, f'UNKNOWN_{mode_code:02X}')
    flags = {
        'max': bool(payload[11] & 8), 'min': bool(payload[11] & 4),
        'hold': bool(payload[11] & 2), 'rel': bool(payload[11] & 1),
        'auto_range': not bool(payload[12] & 4),
        'low_battery': bool(payload[12] & 2), 'hv_warning': bool(payload[12] & 1),
        'peak_max': bool(payload[13] & 4), 'peak_min': bool(payload[13] & 2),
    }
    overload = 'OL' in display.replace('.', '').upper()
    value = None
    if not overload:
        try:
            parsed = Decimal(display.replace(' ', ''))
        except InvalidOperation as exc:
            raise ValueError(f'Invalid numeric display: {display!r}') from exc
        if not parsed.is_finite():
            raise ValueError('Nonfinite numeric display')
        value = float(parsed)
    unit = {0: 'V', 1: 'mV', 2: 'V', 3: 'mV', 8: 'V',
            12: 'uA', 13: 'uA', 14: 'mA', 15: 'mA', 16: 'A', 17: 'A'}.get(mode_code)
    volts = value / 1000 if unit == 'mV' and value is not None else (value if unit == 'V' else None)
    amps = value / {'uA': 1000000, 'mA': 1000, 'A': 1}[unit] if unit in ('uA', 'mA', 'A') and value is not None else None
    quantity = 'voltage' if mode_code in (0, 1, 2, 3, 8) else ('current' if mode_code in range(12, 18) else None)
    usable = mode_code in (2, 3, 12, 14, 16) and value is not None and not any(
        flags[f] for f in ('hold', 'rel', 'max', 'min', 'peak_max', 'peak_min', 'low_battery'))
    return {'display': display, 'value': value, 'unit': unit, 'volts': volts, 'amps': amps, 'quantity': quantity,
            'mode': mode, 'mode_code': mode_code, 'range_code': chr(range_code),
            'overload': overload, 'flags': flags, 'calibration_usable': usable,
            'checksum_valid': True, 'frame_hex': frame.hex(' ')}

import unittest
from protocol import Framer, command, decode, uart_payload


def frame(payload):
    data = b'\xab\xcd' + bytes([len(payload) + 2]) + payload
    return data + (sum(data) & 0xffff).to_bytes(2, 'big')


class ProtocolTests(unittest.TestCase):
    def test_real_hardware_capture(self):
        raw = bytes.fromhex('00 13 ab cd 10 02 31 20 20 20 36 2e 32 35 00 03 30 30 30 03 79') + b'\xff' * 44
        frames = Framer().feed(uart_payload(raw, 'ch9329'))
        self.assertEqual(len(frames), 1)
        result = decode(frames[0])
        self.assertEqual(result['volts'], 6.25)
        self.assertTrue(result['calibration_usable'])

    def test_fragmented_and_back_to_back(self):
        raw = frame(bytes.fromhex('02 31') + b'  3.240' + bytes.fromhex('00 00 30 30 30'))
        stream = Framer()
        self.assertEqual(stream.feed(b'noise' + raw[:1]), [])
        self.assertEqual(stream.feed(raw[1:5]), [])
        self.assertEqual(stream.feed(raw[5:] + raw), [raw, raw])

    def test_bad_checksum_is_never_a_reading(self):
        raw = frame(bytes.fromhex('02 31') + b'  3.240' + bytes.fromhex('00 00 30 30 30'))
        broken = bytearray(raw)
        broken[8] ^= 1
        stream = Framer()
        self.assertEqual(stream.feed(broken + raw), [raw])
        self.assertEqual(stream.checksum_errors, 1)
        with self.assertRaises(ValueError):
            decode(broken)

    def test_millivolts_hold_rel_overload_and_unknown_units(self):
        raw = frame(bytes.fromhex('03 30') + b' -12.34' + bytes.fromhex('00 00 33 30 30'))
        result = decode(raw)
        self.assertAlmostEqual(result['volts'], -.01234)
        self.assertTrue(result['flags']['hold'])
        self.assertTrue(result['flags']['rel'])
        self.assertFalse(result['calibration_usable'])
        result = decode(frame(bytes.fromhex('02 31') + b'  OL.  ' + bytes.fromhex('00 00 30 30 30')))
        self.assertTrue(result['overload'])
        self.assertIsNone(result['volts'])
        result = decode(frame(bytes.fromhex('06 31') + b'  3.240' + bytes.fromhex('00 00 30 30 30')))
        self.assertIsNone(result['unit'])
        self.assertIsNone(result['volts'])
        self.assertFalse(result['calibration_usable'])

    def test_queries_are_read_only(self):
        self.assertEqual(command(0x5e).hex(), 'abcd035e01d9')
        with self.assertRaises(ValueError):
            command(0x4a)  # HOLD change is deliberately prohibited.

    def test_current_units_and_polarity(self):
        for mode, display, expected, unit in [
                (12, b'  123.4', .0001234, 'uA'),
                (14, b' -12.34', -.01234, 'mA'),
                (16, b'  1.234', 1.234, 'A')]:
            result = decode(frame(bytes([mode, 0x30]) + display + bytes.fromhex('00 00 30 30 30')))
            self.assertAlmostEqual(result['amps'], expected)
            self.assertEqual(result['unit'], unit)
            self.assertEqual(result['quantity'], 'current')
            self.assertIsNone(result['volts'])
            self.assertTrue(result['calibration_usable'])

    def test_ac_and_held_current_rejected_for_dc_calibration(self):
        ac = decode(frame(bytes.fromhex('11 30') + b'  1.234' + bytes.fromhex('00 00 30 30 30')))
        held = decode(frame(bytes.fromhex('10 30') + b'  1.234' + bytes.fromhex('00 00 32 30 30')))
        overload = decode(frame(bytes.fromhex('10 30') + b'  OL.  ' + bytes.fromhex('00 00 30 30 30')))
        self.assertAlmostEqual(ac['amps'], 1.234)
        self.assertFalse(ac['calibration_usable'])
        self.assertTrue(held['flags']['hold'])
        self.assertFalse(held['calibration_usable'])
        self.assertIsNone(overload['amps'])
        self.assertFalse(overload['calibration_usable'])


if __name__ == '__main__':
    unittest.main()

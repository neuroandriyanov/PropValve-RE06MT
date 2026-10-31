"""Small Windows HID transport using the operating system API, no drivers installed."""
import ctypes as C
from ctypes import wintypes as W

K = C.WinDLL('kernel32', use_last_error=True)
S = C.WinDLL('setupapi', use_last_error=True)
H = C.WinDLL('hid', use_last_error=True)


class GUID(C.Structure):
    _fields_ = [('a', W.DWORD), ('b', W.WORD), ('c', W.WORD), ('d', C.c_ubyte * 8)]


class INTERFACE(C.Structure):
    _fields_ = [('size', W.DWORD), ('guid', GUID), ('flags', W.DWORD), ('reserved', C.c_void_p)]


class CAPS(C.Structure):
    _fields_ = [(name, W.USHORT) for name in ['usage', 'page', 'input_length', 'output_length', 'feature_length']] + [
        ('reserved', W.USHORT * 17), ('counts', W.USHORT * 10)]


class OVERLAPPED(C.Structure):
    _fields_ = [('internal', C.c_size_t), ('internal_high', C.c_size_t),
                ('offset', W.DWORD), ('offset_high', W.DWORD), ('event', W.HANDLE)]


def signature(lib, name, result, *args):
    fn = getattr(lib, name)
    fn.restype, fn.argtypes = result, list(args)
    return fn


signature(H, 'HidD_GetHidGuid', None, C.POINTER(GUID))
signature(S, 'SetupDiGetClassDevsW', W.HANDLE, C.POINTER(GUID), W.LPCWSTR, W.HWND, W.DWORD)
signature(S, 'SetupDiEnumDeviceInterfaces', W.BOOL, W.HANDLE, C.c_void_p, C.POINTER(GUID), W.DWORD, C.POINTER(INTERFACE))
signature(S, 'SetupDiGetDeviceInterfaceDetailW', W.BOOL, W.HANDLE, C.POINTER(INTERFACE), C.c_void_p, W.DWORD, C.POINTER(W.DWORD), C.c_void_p)
signature(S, 'SetupDiDestroyDeviceInfoList', W.BOOL, W.HANDLE)
signature(K, 'CreateFileW', W.HANDLE, W.LPCWSTR, W.DWORD, W.DWORD, C.c_void_p, W.DWORD, W.DWORD, W.HANDLE)
signature(K, 'CloseHandle', W.BOOL, W.HANDLE)
signature(H, 'HidD_GetPreparsedData', W.BOOL, W.HANDLE, C.POINTER(C.c_void_p))
signature(H, 'HidD_FreePreparsedData', W.BOOL, C.c_void_p)
signature(H, 'HidP_GetCaps', C.c_long, C.c_void_p, C.POINTER(CAPS))
signature(H, 'HidD_SetFeature', W.BOOL, W.HANDLE, C.c_void_p, W.ULONG)
signature(H, 'HidD_GetFeature', W.BOOL, W.HANDLE, C.c_void_p, W.ULONG)
signature(K, 'CreateEventW', W.HANDLE, C.c_void_p, W.BOOL, W.BOOL, W.LPCWSTR)
signature(K, 'ReadFile', W.BOOL, W.HANDLE, C.c_void_p, W.DWORD, C.POINTER(W.DWORD), C.POINTER(OVERLAPPED))
signature(K, 'WriteFile', W.BOOL, W.HANDLE, C.c_void_p, W.DWORD, C.POINTER(W.DWORD), C.POINTER(OVERLAPPED))
signature(K, 'WaitForSingleObject', W.DWORD, W.HANDLE, W.DWORD)
signature(K, 'CancelIoEx', W.BOOL, W.HANDLE, C.POINTER(OVERLAPPED))
signature(K, 'GetOverlappedResult', W.BOOL, W.HANDLE, C.POINTER(OVERLAPPED), C.POINTER(W.DWORD), W.BOOL)

INVALID = C.c_void_p(-1).value


def enumerate_paths():
    guid = GUID()
    H.HidD_GetHidGuid(C.byref(guid))
    devices = S.SetupDiGetClassDevsW(C.byref(guid), None, None, 0x12)
    if devices == INVALID:
        raise C.WinError(C.get_last_error())
    try:
        index = 0
        while True:
            interface = INTERFACE()
            interface.size = C.sizeof(interface)
            if not S.SetupDiEnumDeviceInterfaces(devices, None, C.byref(guid), index, C.byref(interface)):
                error = C.get_last_error()
                if error == 259:
                    break
                raise C.WinError(error)
            required = W.DWORD()
            S.SetupDiGetDeviceInterfaceDetailW(devices, C.byref(interface), None, 0, C.byref(required), None)
            buf = C.create_string_buffer(required.value)
            C.cast(buf, C.POINTER(W.DWORD))[0] = 8 if C.sizeof(C.c_void_p) == 8 else 6
            if not S.SetupDiGetDeviceInterfaceDetailW(devices, C.byref(interface), buf, required, None, None):
                raise C.WinError(C.get_last_error())
            yield C.wstring_at(C.addressof(buf) + 4)
            index += 1
    finally:
        S.SetupDiDestroyDeviceInfoList(devices)


class Hid:
    def __init__(self, path, read_only=False):
        self.handle = K.CreateFileW(path, 0x80000000 if read_only else 0xC0000000, 3, None, 3, 0x40000000, None)
        if self.handle == INVALID:
            raise C.WinError(C.get_last_error())
        preparsed = C.c_void_p()
        try:
            if not H.HidD_GetPreparsedData(self.handle, C.byref(preparsed)):
                raise C.WinError(C.get_last_error())
            self.caps = CAPS()
            if H.HidP_GetCaps(preparsed, C.byref(self.caps)) != 0x110000:
                raise RuntimeError('HidP_GetCaps failed')
        except BaseException:
            self.close()
            raise
        finally:
            if preparsed:
                H.HidD_FreePreparsedData(preparsed)

    def close(self):
        if self.handle != INVALID:
            K.CloseHandle(self.handle)
            self.handle = INVALID

    def feature(self, data):
        buf = C.create_string_buffer(bytes(data))
        if not H.HidD_SetFeature(self.handle, buf, len(data)):
            raise C.WinError(C.get_last_error())

    def get_feature(self, report_id, length):
        buf = C.create_string_buffer(length)
        buf[0] = report_id
        if not H.HidD_GetFeature(self.handle, buf, length):
            raise C.WinError(C.get_last_error())
        return bytes(buf)

    def io(self, data=None, timeout_ms=1000):
        reading = data is None
        buf = C.create_string_buffer(self.caps.input_length) if reading else C.create_string_buffer(data, len(data))
        size = C.sizeof(buf)
        event = K.CreateEventW(None, True, False, None)
        if not event:
            raise C.WinError(C.get_last_error())
        ov = OVERLAPPED()
        ov.event = event
        transferred = W.DWORD()
        fn = K.ReadFile if reading else K.WriteFile
        try:
            if not fn(self.handle, buf, size, C.byref(transferred), C.byref(ov)):
                error = C.get_last_error()
                if error != 997:
                    raise C.WinError(error)
                result = K.WaitForSingleObject(event, timeout_ms)
                if result != 0:
                    K.CancelIoEx(self.handle, C.byref(ov))
                    K.GetOverlappedResult(self.handle, C.byref(ov), C.byref(transferred), True)
                    if result == 258:
                        return b''
                    raise C.WinError(C.get_last_error())
                if not K.GetOverlappedResult(self.handle, C.byref(ov), C.byref(transferred), False):
                    raise C.WinError(C.get_last_error())
            return bytes(buf[:transferred.value])
        finally:
            K.CloseHandle(event)

    def write_uart(self, data):
        if not 1 <= len(data) <= 63:
            raise ValueError('UART report payload must be 1..63 bytes')
        packet = bytes([len(data)]) + data
        self.io(packet.ljust(self.caps.output_length, b'\0'))

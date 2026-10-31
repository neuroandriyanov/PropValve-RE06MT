"""Explicitly user-authorized Win32 control, restricted to SigmaStudio windows."""
import argparse
import ctypes as C
from ctypes import wintypes as W
import json
import time
from pathlib import Path

U = C.WinDLL('user32', use_last_error=True)
K = C.WinDLL('kernel32', use_last_error=True)


def sig(lib, name, result, *args):
    f = getattr(lib, name)
    f.restype, f.argtypes = result, list(args)
    return f


sig(U, 'IsWindow', W.BOOL, W.HWND)
sig(U, 'GetWindowThreadProcessId', W.DWORD, W.HWND, C.POINTER(W.DWORD))
sig(U, 'GetAncestor', W.HWND, W.HWND, W.UINT)
sig(U, 'GetParent', W.HWND, W.HWND)
sig(U, 'GetWindowTextW', C.c_int, W.HWND, W.LPWSTR, C.c_int)
sig(U, 'GetClassNameW', C.c_int, W.HWND, W.LPWSTR, C.c_int)
sig(U, 'SendMessageW', C.c_ssize_t, W.HWND, W.UINT, C.c_size_t, C.c_ssize_t)
sig(U, 'SetForegroundWindow', W.BOOL, W.HWND)
sig(U, 'SetActiveWindow', W.HWND, W.HWND)
sig(U, 'SetFocus', W.HWND, W.HWND)
sig(U, 'GetFocus', W.HWND)
sig(U, 'AttachThreadInput', W.BOOL, W.DWORD, W.DWORD, W.BOOL)
sig(U, 'BringWindowToTop', W.BOOL, W.HWND)
sig(U, 'OpenClipboard', W.BOOL, W.HWND)
sig(U, 'EmptyClipboard', W.BOOL)
sig(U, 'SetClipboardData', W.HANDLE, W.UINT, W.HANDLE)
sig(U, 'CloseClipboard', W.BOOL)
sig(K, 'GetCurrentThreadId', W.DWORD)
sig(K, 'OpenProcess', W.HANDLE, W.DWORD, W.BOOL, W.DWORD)
sig(K, 'QueryFullProcessImageNameW', W.BOOL, W.HANDLE, W.DWORD, W.LPWSTR, C.POINTER(W.DWORD))
sig(K, 'CloseHandle', W.BOOL, W.HANDLE)
sig(K, 'GlobalAlloc', W.HANDLE, W.UINT, C.c_size_t)
sig(K, 'GlobalLock', C.c_void_p, W.HANDLE)
sig(K, 'GlobalUnlock', W.BOOL, W.HANDLE)
sig(K, 'GlobalFree', W.HANDLE, W.HANDLE)


class KEYBOARD(C.Structure):
    _fields_ = [('vk', W.WORD), ('scan', W.WORD), ('flags', W.DWORD),
                ('time', W.DWORD), ('extra', C.c_size_t)]


class MOUSE(C.Structure):
    _fields_ = [('x', W.LONG), ('y', W.LONG), ('data', W.DWORD),
                ('flags', W.DWORD), ('time', W.DWORD), ('extra', C.c_size_t)]


class INPUT_UNION(C.Union):
    _fields_ = [('keyboard', KEYBOARD), ('mouse', MOUSE)]


class INPUT(C.Structure):
    _fields_ = [('type', W.DWORD), ('value', INPUT_UNION)]


sig(U, 'SendInput', W.UINT, W.UINT, C.POINTER(INPUT), C.c_int)


def info(hwnd):
    if not U.IsWindow(hwnd):
        raise ValueError(f'Window no longer exists: {hwnd}')
    pid = W.DWORD()
    thread = U.GetWindowThreadProcessId(hwnd, C.byref(pid))
    process = K.OpenProcess(0x1000, False, pid)
    if not process:
        raise C.WinError(C.get_last_error())
    try:
        path, length = C.create_unicode_buffer(4096), W.DWORD(4096)
        if not K.QueryFullProcessImageNameW(process, 0, path, C.byref(length)):
            raise C.WinError(C.get_last_error())
        if path.value.lower().split('\\')[-1] != 'sstudio.exe':
            raise ValueError('Only SigmaStudio controls are permitted')
    finally:
        K.CloseHandle(process)
    text, classname = C.create_unicode_buffer(8192), C.create_unicode_buffer(256)
    U.GetWindowTextW(hwnd, text, len(text))
    caption = text.value
    # GetWindowText reads the remote window's cached caption, not necessarily
    # an EDIT's current content. WM_GETTEXT asks the actual control.
    U.SendMessageW(hwnd, 0x000d, len(text), C.addressof(text))
    U.GetClassNameW(hwnd, classname, len(classname))
    return {'handle': hwnd, 'pid': pid.value, 'thread': thread,
            'parent': U.GetParent(hwnd), 'text': text.value, 'cached_caption': caption,
            'class': classname.value}


def focus(hwnd):
    target = info(hwnd)
    root = U.GetAncestor(hwnd, 2)
    current_thread = K.GetCurrentThreadId()
    attached = current_thread != target['thread']
    if attached and not U.AttachThreadInput(current_thread, target['thread'], True):
        raise C.WinError(C.get_last_error())
    try:
        U.SetForegroundWindow(root)
        U.BringWindowToTop(root)
        U.SetActiveWindow(root)
        U.SetFocus(hwnd)
        if U.GetFocus() != hwnd:
            raise RuntimeError('Could not focus the exact SigmaStudio control')
    finally:
        if attached:
            U.AttachThreadInput(current_thread, target['thread'], False)


def keys(vks):
    events = []
    for vk in vks:
        events.append(INPUT(type=1, value=INPUT_UNION(keyboard=KEYBOARD(vk=vk))))
    for vk in reversed(vks):
        events.append(INPUT(type=1, value=INPUT_UNION(keyboard=KEYBOARD(vk=vk, flags=2))))
    packed = (INPUT * len(events))(*events)
    if U.SendInput(len(events), packed, C.sizeof(INPUT)) != len(events):
        raise C.WinError(C.get_last_error())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['inspect', 'focus', 'commit', 'text', 'paste', 'paste-clipboard', 'click', 'save', 'download', 'enable-readbacks', 'disable-readbacks'])
    parser.add_argument('hwnd', type=int)
    parser.add_argument('--text')
    parser.add_argument('--text-file', type=Path)
    args = parser.parse_args()
    if args.text_file:
        args.text = args.text_file.read_text(encoding='utf-8-sig').rstrip('\r\n')
    before = info(args.hwnd)
    if args.action == 'inspect':
        print(json.dumps(before))
        return
    focus(args.hwnd)
    if args.action == 'commit':
        if '.EDIT.' not in before['class']:
            raise ValueError('commit action requires a native EDIT control')
        keys([0x0d])
    elif args.action == 'text':
        if '.EDIT.' not in before['class'] and before['class'].lower() != 'edit':
            raise ValueError('text action requires a native EDIT control')
        text = C.create_unicode_buffer(args.text)
        U.SendMessageW(args.hwnd, 0x000c, 0, C.addressof(text))
        keys([0x0d])
    elif args.action == 'paste-clipboard':
        raw = (args.text.replace('\r\n', '\n').replace('\n', '\r\n') + '\0').encode('utf-16-le')
        block = K.GlobalAlloc(2, len(raw))
        pointer = K.GlobalLock(block)
        if not pointer:
            raise C.WinError(C.get_last_error())
        C.memmove(pointer, raw, len(raw))
        K.GlobalUnlock(block)
        if not U.OpenClipboard(args.hwnd):
            K.GlobalFree(block)
            raise C.WinError(C.get_last_error())
        try:
            U.EmptyClipboard()
            if not U.SetClipboardData(13, block):
                K.GlobalFree(block)
                raise C.WinError(C.get_last_error())
        finally:
            U.CloseClipboard()
        keys([0x11, 0x41])
        time.sleep(.15)
        keys([0x11, 0x56])
    elif args.action == 'paste':
        # Unicode keystrokes, preserving the clipboard. Used for the observed
        # custom table editor after selecting its complete text.
        keys([0x11, 0x41])
        time.sleep(.1)
        events = []
        raw = args.text.replace('\n', '\r').encode('utf-16-le')
        for offset in range(0, len(raw), 2):
            unit = int.from_bytes(raw[offset:offset + 2], 'little')
            events.extend([INPUT(type=1, value=INPUT_UNION(keyboard=KEYBOARD(scan=unit, flags=4))),
                           INPUT(type=1, value=INPUT_UNION(keyboard=KEYBOARD(scan=unit, flags=6)))])
        packed = (INPUT * len(events))(*events)
        if U.SendInput(len(events), packed, C.sizeof(INPUT)) != len(events):
            raise C.WinError(C.get_last_error())
        time.sleep(.1)
        if '.EDIT.' in before['class']:
            keys([0x0d])
    elif args.action == 'click':
        if '.BUTTON.' not in before['class']:
            raise ValueError('click action requires a native BUTTON control')
        U.SendMessageW(args.hwnd, 0xf5, 0, 0)  # BM_CLICK
    elif args.action == 'save':
        keys([0x11, 0x53])
    elif args.action == 'download':
        keys([0x76])  # F7: Link Compile Download
    elif args.action == 'enable-readbacks':
        keys([0x11,0x7a])  # Ctrl+F11, observed Action menu
    elif args.action == 'disable-readbacks':
        keys([0x11,0x7b])  # Ctrl+F12, observed Action menu
    time.sleep(.2)
    print(json.dumps({'before': before, 'after': info(args.hwnd)}, ensure_ascii=True))


if __name__ == '__main__':
    main()

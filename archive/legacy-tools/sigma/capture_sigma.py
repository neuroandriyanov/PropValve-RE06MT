"""User-authorized Win32/GDI screenshot of only the SigmaStudio window."""
import argparse
import ctypes as C
from ctypes import wintypes as W
from pathlib import Path
import time
import json
from PIL import ImageGrab
from win32_sigma import U, info, sig

sig(U, 'GetWindowRect', W.BOOL, W.HWND, C.POINTER(W.RECT))
sig(U, 'ShowWindow', W.BOOL, W.HWND, C.c_int)
sig(U, 'IsIconic', W.BOOL, W.HWND)
sig(U, 'SetProcessDPIAware', W.BOOL)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('hwnd', type=int)
    parser.add_argument('path', type=Path)
    parser.add_argument('--width', type=int, default=1600)
    args = parser.parse_args()
    print(info(args.hwnd))
    U.SetProcessDPIAware()
    if U.IsIconic(args.hwnd):
        U.ShowWindow(args.hwnd, 9)
    U.SetForegroundWindow(args.hwnd)
    time.sleep(.3)
    rect = W.RECT()
    if not U.GetWindowRect(args.hwnd, C.byref(rect)):
        raise C.WinError(C.get_last_error())
    args.path.parent.mkdir(parents=True, exist_ok=True)
    image = ImageGrab.grab(bbox=(rect.left, rect.top, rect.right, rect.bottom), all_screens=True)
    if image.width > args.width:
        image = image.resize((args.width, round(image.height * args.width / image.width)))
    image.save(args.path)
    metadata = {'bounds': [rect.left, rect.top, rect.right, rect.bottom], 'path': str(args.path),
                'width': image.width, 'height': image.height, 'hwnd': args.hwnd, 'pid': info(args.hwnd)['pid'],
                'time': time.time()}
    args.path.with_suffix('.json').write_text(json.dumps(metadata), encoding='utf-8')
    print(metadata)

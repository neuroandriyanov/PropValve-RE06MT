"""Screenshot-bound, user-authorized native input, restricted to SigmaStudio."""
import argparse
import ctypes as C
from ctypes import wintypes as W
import json
from pathlib import Path
import time
from win32_sigma import U, INPUT, INPUT_UNION, MOUSE, info, sig, keys

sig(U, 'SetProcessDPIAware', W.BOOL)
sig(U, 'GetWindowRect', W.BOOL, W.HWND, C.POINTER(W.RECT))
sig(U, 'SetCursorPos', W.BOOL, C.c_int, C.c_int)
sig(U, 'WindowFromPoint', W.HWND, W.POINT)


def mouse_event(flags):
    value = INPUT(type=0, value=INPUT_UNION(mouse=MOUSE(flags=flags)))
    if U.SendInput(1, C.byref(value), C.sizeof(value)) != 1:
        raise C.WinError(C.get_last_error())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['click', 'double', 'right', 'drag'])
    parser.add_argument('snapshot', type=Path)
    parser.add_argument('x', type=float)
    parser.add_argument('y', type=float)
    parser.add_argument('--to-x', type=float)
    parser.add_argument('--to-y', type=float)
    parser.add_argument('--key', choices=['ctrl', 'shift'])
    args = parser.parse_args()
    metadata = json.loads(args.snapshot.with_suffix('.json').read_text())
    if time.time() - metadata['time'] > 120:
        raise RuntimeError('Screenshot expired; capture and inspect again')
    U.SetProcessDPIAware()
    target = info(metadata['hwnd'])
    if target['pid'] != metadata['pid']:
        raise RuntimeError('SigmaStudio process changed')
    rect = W.RECT()
    U.GetWindowRect(metadata['hwnd'], C.byref(rect))
    if [rect.left, rect.top, rect.right, rect.bottom] != metadata['bounds']:
        raise RuntimeError('Window geometry changed; capture again')

    def position(x, y):
        if not 0 <= x < metadata['width'] or not 0 <= y < metadata['height']:
            raise ValueError('Point outside observed screenshot')
        point = W.POINT(rect.left + round(x * (rect.right - rect.left) / metadata['width']),
                        rect.top + round(y * (rect.bottom - rect.top) / metadata['height']))
        hit = U.WindowFromPoint(point)
        if info(hit)['pid'] != target['pid']:
            raise RuntimeError('Point is not over SigmaStudio')
        U.SetCursorPos(point.x, point.y)

    U.SetForegroundWindow(metadata['hwnd'])
    time.sleep(.15)
    position(args.x, args.y)
    modifier = {'ctrl': 0x11, 'shift': 0x10}.get(args.key)
    if modifier:
        from win32_sigma import KEYBOARD
        value = INPUT(type=1, value=INPUT_UNION(keyboard=KEYBOARD(vk=modifier)))
        U.SendInput(1, C.byref(value), C.sizeof(value))
    try:
        if args.action == 'drag':
            mouse_event(2)
            try:
                for i in range(1, 21):
                    position(args.x + (args.to_x - args.x) * i / 20,
                             args.y + (args.to_y - args.y) * i / 20)
                    time.sleep(.025)
            finally:
                mouse_event(4)
        else:
            for i in range(2 if args.action == 'double' else 1):
                mouse_event(8 if args.action == 'right' else 2)
                time.sleep(.08)
                mouse_event(16 if args.action == 'right' else 4)
                if args.action == 'double':
                    time.sleep(.08)
    finally:
        if modifier:
            from win32_sigma import KEYBOARD
            value = INPUT(type=1, value=INPUT_UNION(keyboard=KEYBOARD(vk=modifier, flags=2)))
            U.SendInput(1, C.byref(value), C.sizeof(value))
    print(json.dumps({'action': args.action, 'point': [args.x, args.y], 'target': target['text']}))


if __name__ == '__main__':
    main()

"""Read native SigmaStudio control identity and bounds."""
import ctypes as C
from ctypes import wintypes as W
import json
from win32_sigma import U, info, sig
sig(U,'SetProcessDPIAware',W.BOOL)
sig(U,'GetWindowRect',W.BOOL,W.HWND,C.POINTER(W.RECT))
U.SetProcessDPIAware()
callback=C.WINFUNCTYPE(W.BOOL,W.HWND,W.LPARAM)
def visit(hwnd,param):
    try:
        v=info(hwnd)
        if '.EDIT.' in v['class'] or '.BUTTON.' in v['class']:
            r=W.RECT();U.GetWindowRect(hwnd,C.byref(r))
            v['bounds']=[r.left,r.top,r.right,r.bottom]
            print(json.dumps(v))
    except ValueError: pass
    return True
U.EnumChildWindows(855898,callback(visit),0)

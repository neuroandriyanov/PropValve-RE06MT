"""Client for the installed vendor API. Calls may write hardware or project state."""
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BRIDGE = Path(os.environ.get('PROPVALVE_SIGMA_BRIDGE', ROOT / 'tools/bin/SigmaBridge2.exe'))
COMPILED_DIR = Path(os.environ.get(
    'PROPVALVE_COMPILED_DIR', ROOT / 'проект_сигма/IC 1_Design1_parker_v0/net_list_out2'))


def require_bridge():
    if not BRIDGE.is_file():
        raise FileNotFoundError('Build tools/sigma/build_bridge.ps1 first; see docs/SETUP.md')
    return str(BRIDGE)


def call(method, args):
    bridge = require_bridge()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', encoding='utf-8', delete=False) as handle:
        path = Path(handle.name)
        json.dump(args, handle)
    try:
        output = subprocess.check_output(
            [bridge, 'call', method, str(path)], text=True, timeout=15)
        return json.loads(output.splitlines()[-1])['result']
    finally:
        path.unlink(missing_ok=True)


def adc1():
    """Select and read ADC1; caller must verify the map matches DSP RAM."""
    trap = (COMPILED_DIR / 'trap.dat').read_text()
    match = re.search(r'ADC1_RAW_ReadBackAlg1 trap value (\d+)', trap)
    if not match:
        raise ValueError('ADC1_RAW trap not found; compile the intended project first')
    pc = int(match[1])
    if not call('REGISTER_WRITE', ['IC 1', 2074, 2, (pc << 2) | 2]):
        raise RuntimeError('Capture setup failed')
    raw = bytes(call('REGISTER_READ_ARRAY', ['IC 1', 2074, 3]))
    if len(raw) != 3:
        raise ValueError('Expected a 3-byte readback')
    return int.from_bytes(raw, 'big', signed=True) / 524288

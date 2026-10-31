"""Select a DSP node and read it; disable GUI continuous readback first.

Selection writes register 2074. The caller must verify that trap.dat matches
the project loaded in DSP RAM. This is not an offline file reader.
"""
import json
import re
import statistics
import subprocess
from sigma_api import COMPILED_DIR, call, require_bridge


def sample_node(name, count=32):
    if not isinstance(count, int) or not 2 <= count <= 512:
        raise ValueError('Sample count must be an integer from 2 to 512')
    bridge = require_bridge()
    trap = (COMPILED_DIR / 'trap.dat').read_text()
    match = re.search(r'Signal ' + re.escape(name) + r'_\S+ trap value (\d+) register MAC_out', trap)
    if not match:
        raise ValueError('Missing MAC_out trap for ' + name)
    pc = int(match[1])
    if not call('REGISTER_WRITE', ['IC 1', 2074, 2, (pc << 2) | 2]):
        raise RuntimeError('Capture setup failed')
    output = subprocess.check_output([bridge, 'sample', str(count), '2074'], text=True, timeout=30)
    data = json.loads(output.splitlines()[-1])
    if len(data) != count:
        raise ValueError('Unexpected sample count from SigmaStudio bridge')
    return {'mean': statistics.mean(data), 'std': statistics.stdev(data),
            'min': min(data), 'max': max(data), 'samples': data}

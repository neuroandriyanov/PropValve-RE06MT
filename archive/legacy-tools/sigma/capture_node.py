"""Read a compiled DSP node; disable GUI continuous Readback before batch capture."""
import re,json,subprocess,statistics
from sigma_api import ROOT,call
def sample_node(name,count=32):
    trap=(ROOT/'проект_сигма/IC 1_Design1_parker_v0/net_list_out2/trap.dat').read_text()
    match=re.search(r'Signal '+re.escape(name)+r'_\S+ trap value (\d+) register MAC_out',trap)
    if not match:raise ValueError('Missing MAC_out trap for '+name)
    pc=int(match[1]);assert call('REGISTER_WRITE',['IC 1',2074,2,(pc<<2)|2])
    out=subprocess.check_output([str(ROOT/'tools/sigma/SigmaBridge2.exe'),'sample',str(count),'2074'],text=True,timeout=30)
    data=json.loads(out.splitlines()[-1])
    return {'mean':statistics.mean(data),'std':statistics.stdev(data),'min':min(data),'max':max(data),'samples':data}

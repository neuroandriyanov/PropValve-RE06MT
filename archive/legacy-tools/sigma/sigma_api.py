"""Client for the installed vendor .NET automation interface."""
import json,subprocess,tempfile,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def call(method,args):
    with tempfile.NamedTemporaryFile(mode='w',suffix='.json',encoding='utf-8',delete=False) as f:
        json.dump(args,f);path=Path(f.name)
    try:
        output=subprocess.check_output([str(ROOT/'tools/sigma/SigmaBridge2.exe'),'call',method,str(path)],text=True,timeout=15)
        response=json.loads(output.splitlines()[-1])
        return response['result']
    finally:path.unlink(missing_ok=True)
def adc1():
    trap=(ROOT/'проект_сигма/IC 1_Design1_parker_v0/net_list_out2/trap.dat').read_text()
    pc=int(re.search(r'ADC1_RAW_ReadBackAlg1 trap value (\d+)',trap)[1])
    if not call('REGISTER_WRITE',['IC 1',2074,2,(pc<<2)|2]):raise RuntimeError('Capture setup failed')
    raw=call('REGISTER_READ_ARRAY',['IC 1',2074,3])
    value=int.from_bytes(bytes(raw),'big',signed=True)
    return value/524288

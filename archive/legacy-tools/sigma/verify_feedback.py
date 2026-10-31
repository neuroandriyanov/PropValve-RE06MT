"""Validate the final normalized measurement against the independent meter."""
import sys,time,json,statistics,subprocess,re
from pathlib import Path
from verify_output import set_input
from sigma_api import ROOT,call
sys.path.insert(0,str(ROOT/'tools/meter'))
from read_meter import Meter,find_devices
meter=Meter(*find_devices()[0]);results=[]
try:
    for level in [0,.125,.25,.5,.75,1,0]:
        set_input(134730,134722,level);samples=[];start=time.monotonic()
        while True:
            time.sleep(.65);r=meter.query()
            if not r['calibration_usable'] or r['quantity']!='current':raise RuntimeError(str(r))
            amps=r['amps'];samples.append(amps)
            if not -.02<=amps<=3.02:raise RuntimeError('Current limit '+str(amps))
            if time.monotonic()-start>6 and max(samples[-5:])-min(samples[-5:])<=.004:break
            if time.monotonic()-start>30:break
        trap=(ROOT/'проект_сигма/IC 1_Design1_parker_v0/net_list_out2/trap.dat').read_text()
        pc=int(re.search(r'I_MEAS_0_1_ReadBackAlg2 trap value (\d+)',trap)[1])
        assert call('REGISTER_WRITE',['IC 1',2074,2,(pc<<2)|2])
        output=subprocess.check_output([str(ROOT/'tools/sigma/SigmaBridge2.exe'),'sample','128'],text=True,timeout=20)
        normalized=json.loads(output.splitlines()[-1]);r=meter.query()
        if not r['calibration_usable'] or r['quantity']!='current' or not -.02<=r['amps']<=3.02:raise RuntimeError(str(r))
        actual=statistics.mean([statistics.median(samples[-5:]),r['amps']]);measured=statistics.mean(normalized)
        p={'input':level,'target_amps':level*3,'meter_amps':actual,'feedback_norm':measured,'feedback_amps':measured*3,'feedback_error_amps':measured*3-actual,'command_error_amps':actual-level*3,'feedback_std_amps':statistics.stdev(normalized)*3,'meter_samples':samples}
        results.append(p);Path('output/meter/feedback_final_verification.json').write_text(json.dumps(results,indent=2))
        print(json.dumps({k:v for k,v in p.items() if k!='meter_samples'}),flush=True)
finally:set_input(134730,134722,0);meter.close()

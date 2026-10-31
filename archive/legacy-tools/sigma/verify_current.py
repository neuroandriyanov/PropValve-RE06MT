"""Verify command table against the independent meter; always return zero."""
import sys,time,json,statistics
from pathlib import Path
from verify_output import set_input
from sigma_api import adc1
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'meter'))
from read_meter import Meter,find_devices
meter=Meter(*find_devices()[0]);results=[]
try:
    for value in ([float(x) for x in sys.argv[1:]] or [0,.1,.25,.375,.5,.625,.75,.875,1,0]):
        set_input(134730,134722,value);samples=[];start=time.monotonic()
        while True:
            time.sleep(.65);r=meter.query()
            if not r['calibration_usable'] or r['quantity']!='current':raise RuntimeError(str(r))
            a=r['amps'];samples.append(a)
            if not -.02<=a<=3.02:raise RuntimeError('Current bound '+str(a))
            if time.monotonic()-start>6 and max(samples[-5:])-min(samples[-5:])<=.004:break
            if time.monotonic()-start>30:break
        amps=statistics.median(samples[-5:]);raw=adc1()
        p={'input':value,'target_amps':value*3,'amps':amps,'error_amps':amps-value*3,'adc1_raw':raw,'samples':samples}
        results.append(p);Path('output/meter/current_verification.json').write_text(json.dumps(results,indent=2))
        print(json.dumps(p),flush=True)
finally:set_input(134730,134722,0);meter.close()

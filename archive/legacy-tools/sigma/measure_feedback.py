"""Measure ADC1 versus independent coil current after R43 replacement."""
import sys,time,json,statistics,subprocess,re
from pathlib import Path
from verify_output import set_input
from sigma_api import adc1,ROOT,call
sys.path.insert(0,str(ROOT/'tools/meter'))
from read_meter import Meter,find_devices
meter=Meter(*find_devices()[0]);results=[]
filtered='--filtered' in sys.argv
try:
    for level in ([0,.25,.5,.75,1,0] if filtered else [0,.125,.25,.375,.5,.625,.75,.875,1,0]):
        set_input(134730,134722,level);amps=[];start=time.monotonic()
        while True:
            time.sleep(.65);r=meter.query()
            if not r['calibration_usable'] or r['quantity']!='current':raise RuntimeError(str(r))
            a=r['amps'];amps.append(a)
            if not -.02<=a<=3.02:raise RuntimeError('Current bound '+str(a))
            if time.monotonic()-start>6 and max(amps[-5:])-min(amps[-5:])<=.004:break
            if time.monotonic()-start>30:break
        if filtered:
            trap=(ROOT/'проект_сигма/IC 1_Design1_parker_v0/net_list_out2/trap.dat').read_text()
            pc=int(re.search(r'FB_NOT_CALIBRATED_ReadBackAlg2 trap value (\d+)',trap)[1])
            assert call('REGISTER_WRITE',['IC 1',2074,2,(pc<<2)|2])
        else: adc1()
        output=subprocess.check_output([str(ROOT/'tools/sigma/SigmaBridge2.exe'),'sample','128'],text=True,timeout=20)
        raw=json.loads(output.splitlines()[-1])
        after=meter.query()
        if not after['calibration_usable'] or after['quantity']!='current' or not -.02<=after['amps']<=3.02:raise RuntimeError(str(after))
        p={'input':level,'amps':statistics.mean([statistics.median(amps[-5:]),after['amps']]),
           'adc_mean':statistics.mean(raw),'adc_std':statistics.stdev(raw),'adc_min':min(raw),'adc_max':max(raw),'adc_samples':raw,'meter_samples':amps,'meter_after':after['amps']}
        filename='feedback_r43_10k_filtered.json' if filtered else 'feedback_r43_10k_measurements.json'
        results.append(p);Path('output/meter/'+filename).write_text(json.dumps(results,indent=2))
        print(json.dumps({k:v for k,v in p.items() if k not in ('adc_samples','meter_samples')}),flush=True)
        if max(raw)>=.99999 or min(raw)<=-1:raise RuntimeError('ADC saturation')
finally:set_input(134730,134722,0);meter.close()

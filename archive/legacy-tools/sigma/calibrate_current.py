"""Empirical five-point command calibration with a 3 A bound and zero reset."""
import sys,time,json,statistics
from pathlib import Path
from verify_output import set_input
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'meter'))
from read_meter import Meter,find_devices
meter=Meter(*find_devices()[0]); report=[]
resume='--resume' in sys.argv
if resume: report=json.loads(Path('output/meter/current_calibration_points.json').read_text())
def measure(code):
    if not 0<=code<=.57: raise ValueError(code)
    set_input(134730,134722,code/.6)
    values=[];start=time.monotonic()
    while True:
        time.sleep(.65);r=meter.query()
        if not r['calibration_usable'] or r['quantity']!='current': raise RuntimeError(str(r))
        a=r['amps'];values.append(a)
        if not -.02<=a<=3.02: raise RuntimeError('Current bound: '+str(a))
        if time.monotonic()-start>=6 and len(values)>=6 and max(values[-6:])-min(values[-6:])<=.003: break
        if time.monotonic()-start>45: raise RuntimeError('Current did not settle '+str(values))
    return statistics.median(values[-6:]),values
try:
    # Find the upper edge of the measured zero-current region, then leave margin.
    lo=0;hi=.05
    for _ in range(0 if resume else 6):
        code=(lo+hi)/2;a,values=measure(code)
        if a<=.001: lo=code
        else: hi=code
        print(json.dumps({'zero_search_code':code,'amps':a}),flush=True)
    zero=max(0,lo-.001)
    if not resume:
        a,values=measure(zero)
        report.append({'input':0,'target':0,'code':zero,'amps':a,'samples':values})
    for target in ([3.0] if resume else [.75,1.5,2.25,3.0]):
        code=.53 if target==3 else min(.55,(target+.17)/5.8)
        for iteration in range(8):
            a,values=measure(code)
            print(json.dumps({'target':target,'code':code,'amps':a,'iteration':iteration}),flush=True)
            if abs(target-a)<=.003:break
            code+=max(-.01,min(.01,(target-a-.001)/5.8*.85))
        else: raise RuntimeError('Target did not converge')
        report.append({'input':target/3,'target':target,'code':code,'amps':a,'samples':values})
        Path('output/meter/current_calibration_points.json').write_text(json.dumps(report,indent=2))
finally:
    set_input(134730,134722,0);meter.close()

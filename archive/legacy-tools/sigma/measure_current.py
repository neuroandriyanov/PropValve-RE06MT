"""Bounded, user-authorized coil calibration; restore zero on every exit."""
import sys,time,json,statistics
from pathlib import Path
from verify_output import set_input
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'meter'))
from read_meter import Meter,find_devices
levels=[float(x) for x in sys.argv[1:]] or [0,.1,.25,.5,.75,1]
meter=Meter(*find_devices()[0]);results=[]
try:
    for level in levels:
        set_input(134730,134722,level)
        samples=[];started=time.monotonic()
        while True:
            time.sleep(.7)
            r=meter.query()
            if not r['calibration_usable'] or r['quantity']!='current': raise RuntimeError(str(r))
            amps=r['amps']
            if abs(amps)>3.02: raise RuntimeError('Current limit exceeded: '+str(amps))
            samples.append(amps)
            if time.monotonic()-started>6 and len(samples)>=6 and max(samples[-6:])-min(samples[-6:])<=.003: break
            if time.monotonic()-started>30: raise RuntimeError('No stable reading: '+str(samples))
        point={'input':level,'amps':statistics.median(samples[-6:]),'samples':samples}
        results.append(point)
        Path('output/meter/current_initial.json').write_text(json.dumps(results,indent=2))
        print(json.dumps(point),flush=True)
finally:
    set_input(134730,134722,0)
    meter.close()

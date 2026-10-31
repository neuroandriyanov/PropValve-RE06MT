"""Fit a five-node table on the safe full ADC domain, constrained at measured 0 V and 10 V."""
import json,statistics
from pathlib import Path
from sigma_api import call
rows=json.loads(Path('output/meter/voltage_input_filtered.json').read_text())
assert all(r['reference_source']=='multimeter' for r in rows)
x0=statistics.mean(r['adc']['mean'] for r in rows if abs(r['reference_volts'])<.001)
top=max(rows,key=lambda r:r['reference_volts']);xt=top['adc']['mean'];yt=top['reference_volts']/10
assert -.5<x0<0 and .5<xt<1
k=(1+2*x0)/(-2*x0);at=2-2*xt;bt=2*xt-1
def weights(x):
    if x<0:return (1+2*x+2*x*k,0,0)
    if x<=.5:return (1-2*x,2*x,0)
    return (0,2-2*x-(2*x-1)*at/bt,(2*x-1)*yt/bt)
aa=ab=bb=va=vb=0
for r in rows:
    a,b,d=weights(r['adc']['mean']);target=r['reference_volts']/10-d
    aa+=a*a;ab+=a*b;bb+=b*b;va+=a*target;vb+=b*target
det=aa*bb-ab*ab;p=(va*bb-vb*ab)/det;q=(vb*aa-va*ab)/det
cm=-k*p;ct=(yt-at*q)/bt
coeff=[2*cm-p,cm,p,q,ct]
def predicted(x):
    a,b,d=weights(x);return a*p+b*q+d
errors=[10*predicted(r['adc']['mean'])-r['reference_volts'] for r in rows]
report={'R42_ohms':10000,'sample_rate_hz':96000,'lowpass_hz':20,'min':-1,'max':1,'coefficients':coeff,
        'zero_adc':x0,'top_adc':xt,'fit_max_error_volts':max(map(abs,errors)),'fit_errors_volts':errors,'output_limits':[0,1]}
Path('output/meter/voltage_input_calibration.json').write_text(json.dumps(report,indent=2))
assert call('SET_OBJECT_PROPERTY',['setControlValue','VIN_TABLE_0_10V',[0,0,'Coefficients',coeff]])
assert call('COMPILE_PROJECT',[])
print(json.dumps(report))

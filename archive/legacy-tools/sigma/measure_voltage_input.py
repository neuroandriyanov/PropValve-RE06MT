"""Calibrate ADC0 from the previously calibrated 0..10 V output; restore both commands to zero."""
import sys,time,json
from pathlib import Path
from verify_output import set_input
from capture_node import sample_node
from sigma_api import ROOT
sys.path.insert(0,str(ROOT/'tools/meter'))
from read_meter import Meter,find_devices
stage=sys.argv[1] if len(sys.argv)>1 else 'raw'
node={'raw':'ADC0_RAW','filtered':'VIN_FILTERED','verify':'VIN_MEAS_0_1'}[stage]
levels=[0,.1,.5,1,0] if stage=='raw' else [0,.1,.125,.25,.375,.5,.625,.75,.875,1,0]
meter=Meter(*find_devices()[0]);results=[]
try:
    set_input(134730,134722,0)
    for value in levels:
        set_input(460422,199202,value);time.sleep(1.3)
        stats=sample_node(node,32)
        m=meter.query()
        volts=m.get('volts') if m.get('calibration_usable') and m.get('quantity')=='voltage' else None
        if volts is not None and abs(volts-value*10)>.15:raise RuntimeError('Meter voltage differs from calibrated output: '+str(m))
        if m.get('quantity')=='current' and m.get('calibration_usable') and abs(m['amps'])>.05:raise RuntimeError('Unexpected coil current '+str(m))
        if stage!='verify' and (stats['min']<=-1 or stats['max']>=.99999):raise RuntimeError('ADC saturation '+str(stats))
        reference=volts if volts is not None else value*10
        p={'output_input':value,'reference_volts':reference,'reference_source':'multimeter' if volts is not None else 'previously_calibrated_output','adc':stats,'meter':m}
        if stage=='verify':p.update(input_norm=stats['mean'],input_volts=stats['mean']*10,error_volts=stats['mean']*10-reference)
        results.append(p);Path('output/meter/voltage_input_'+stage+'.json').write_text(json.dumps(results,indent=2))
        print(json.dumps({k:v for k,v in p.items() if k not in ('adc','meter')}|{'dsp_mean':stats['mean'],'std':stats['std'],'min':stats['min'],'max':stats['max']}),flush=True)
finally:
    set_input(460422,199202,0);set_input(134730,134722,0);meter.close()

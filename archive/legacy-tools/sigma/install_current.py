import json
from pathlib import Path
from sigma_api import call
points=json.loads(Path('output/meter/current_calibration_points.json').read_text())
coeff=[p['code'] for p in points]
assert len(coeff)==5 and all(0<=v<=.57 for v in coeff)
def checked(method,args):
    if call(method,args) is not True:raise RuntimeError((method,args))
checked('SET_OBJECT_PROPERTY',['setControlValue','Interpolator2',[0,0,'Coefficients',coeff]])
Path('проект_сигма/current_command_0_3A.txt').write_text(''.join(f'{v:.9f}\n' for v in coeff))
checked('DISCONNECT_OBJECT',['Input1',1,'ReadBack1',0])
for args in [['Input1',1,'T2',0],['T2',0,'ReadBack1',0],['T2',0,'Interpolator3',0],['Interpolator3',0,'ReadBack2',0]]:
    checked('CONNECT_OBJECT',args)
checked('SET_OBJECT_PROPERTY',['setControlValue','Interpolator3',[0,0,'Coefficients',[-1,-.5,0,.5,1]]])
for old,new in [('Interpolator2','CURRENT_0_3A'),('Interpolator3','ADC1_RAW_PENDING_R43'),('ReadBack1','ADC1_RAW'),('ReadBack2','FB_NOT_CALIBRATED')]:
    checked('SET_OBJECT_PROPERTY',['setName',old,[new]])
print(json.dumps({'command_coefficients':coeff,'feedback':'raw identity; calibration pending R43 change'}))

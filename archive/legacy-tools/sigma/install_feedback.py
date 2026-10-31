import json
from pathlib import Path
from sigma_api import call
p=json.loads(Path('output/meter/feedback_calibration.json').read_text())
def checked(method,args):
    if call(method,args) is not True:raise RuntimeError((method,args))
checked('SET_OBJECT_PROPERTY',['setControlValue','ADC1_RAW_PENDING_R43',[0,0,'Coefficients',p['coefficients']]])
checked('SET_OBJECT_PROPERTY',['setControlValue','CURRENT_0_3A',[0,0,'Coefficients',p['command_coefficients']]])
checked('SET_OBJECT_PROPERTY',['setName','ADC1_RAW_PENDING_R43',['I_FEEDBACK_0_1']])
checked('SET_OBJECT_PROPERTY',['setName','FB_NOT_CALIBRATED',['I_MEAS_0_1']])
print('Feedback interpolation and corrected command table installed.')

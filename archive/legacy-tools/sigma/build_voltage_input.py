from sigma_api import call
def run(method,args):
    if call(method,args) is not True:raise RuntimeError((method,args))
def add(kind,x,y,old,new):
    run('INSERT_OBJECT_POINT',[kind,x,y]);run('SET_OBJECT_PROPERTY',['setName',old,[new]])
add('General (1st order)',100,850,'Gen 1st Order1','VIN_LPF_20Hz')
add('Linear Interpolator',260,850,'Interpolator2','VIN_TABLE_0_10V')
add('AB in/out Condition',420,850,'AB 1','VIN_LIMIT_MIN')
add('AB in/out Condition',540,850,'AB 1','VIN_LIMIT_MAX')
add('DC Input Entry',420,950,'DC1','VIN_ZERO')
add('DC Input Entry',540,950,'DC1','VIN_ONE')
add('DSP Readback',690,850,'ReadBack1','VIN_FILTERED')
add('T Connection',100,700,'T5','VIN_ADC_SPLIT')
run('DISCONNECT_OBJECT',['Input1',0,'ADC0_RAW',0])
for args in [['Input1',0,'VIN_ADC_SPLIT',0],['VIN_ADC_SPLIT',0,'ADC0_RAW',0],['VIN_ADC_SPLIT',0,'VIN_LPF_20Hz',0],
             ['VIN_LPF_20Hz',0,'VIN_TABLE_0_10V',0],['VIN_TABLE_0_10V',0,'VIN_FILTERED',0]]:
    run('CONNECT_OBJECT',args)
# Output limiters are wired after the filtered calibration series.
print('Voltage input processing created; parameter setup and upper comparison pending.')

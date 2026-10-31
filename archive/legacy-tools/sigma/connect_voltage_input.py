from sigma_api import call
def run(method,args):
    if call(method,args) is not True:raise RuntimeError((method,args))
run('INSERT_OBJECT_POINT',['T Connection',190,850])
run('SET_OBJECT_PROPERTY',['setName','T5',['VIN_FILTER_SPLIT']])
run('INSERT_OBJECT_POINT',['DSP Readback',690,1000])
run('SET_OBJECT_PROPERTY',['setName','ReadBack1',['VIN_MEAS_0_1']])
for args in [['VIN_LPF_20Hz',0,'VIN_TABLE_0_10V',0],['VIN_TABLE_0_10V',0,'VIN_FILTERED',0]]:run('DISCONNECT_OBJECT',args)
for args in [
    ['VIN_LPF_20Hz',0,'VIN_FILTER_SPLIT',0],['VIN_FILTER_SPLIT',0,'VIN_FILTERED',0],['VIN_FILTER_SPLIT',0,'VIN_TABLE_0_10V',0],
    ['VIN_TABLE_0_10V',0,'VIN_LIMIT_MIN',0],['VIN_ZERO',0,'VIN_LIMIT_MIN',1],['VIN_LIMIT_MIN',0,'VIN_LIMIT_MAX',0],['VIN_ONE',0,'VIN_LIMIT_MAX',1],['VIN_LIMIT_MAX',0,'VIN_MEAS_0_1',0]]:run('CONNECT_OBJECT',args)
run('SET_OBJECT_PROPERTY',['setControlValue','VIN_TABLE_0_10V',[0,0,'Coefficients',[-1,-.5,0,.5,1]]])
run('COMPILE_PROJECT',[])
print('All voltage input modules connected and downloaded; identity table pending calibration.')

from sigma_api import call
def run(method,args):
    if call(method,args) is not True:raise RuntimeError((method,args))
for args in [['T Connection',180,250],['T Connection',180,450]]:run('INSERT_OBJECT_POINT',args)
for args in [['DC2_2',0,'CURRENT_0_3A',0],['CURRENT_0_3A',0,'T1',0]]:run('DISCONNECT_OBJECT',args)
for args in [
    ['DC2_2',0,'T3',0],['T3',0,'CURRENT_0_3A',0],['T3',0,'ABCD1',0],
    ['DC2',0,'T4',0],['T4',0,'ABCD1',1],['T4',0,'ABCD1',3],
    ['CURRENT_0_3A',0,'ABCD1',2],['ABCD1',0,'T1',0]]:
    run('CONNECT_OBJECT',args)
run('SET_OBJECT_PROPERTY',['setName','ABCD1',['ZERO_OFF']])
print('Gate installed: input > 0 passes current table, otherwise both DAC commands are zero.')

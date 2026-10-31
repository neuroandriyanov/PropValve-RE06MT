from sigma_api import call
for args in [['T3',0,'ABCD 1',0],['DC2',0,'T4',0],['T4',0,'ABCD 1',1],['T4',0,'ABCD 1',3],['CURRENT_0_3A',0,'ABCD 1',2],['ABCD 1',0,'T1',0]]:
    if call('CONNECT_OBJECT',args) is not True: raise RuntimeError(args)
assert call('SET_OBJECT_PROPERTY',['setName','ABCD 1',['ZERO_OFF']])
assert call('COMPILE_PROJECT',[])
print('Compiled and downloaded zero gate.')

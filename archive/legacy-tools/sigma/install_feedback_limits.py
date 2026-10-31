from sigma_api import call
def checked(method,args):
    if call(method,args) is not True:raise RuntimeError((method,args))
checked('DISCONNECT_OBJECT',['CURRENT_LPF_20Hz',0,'I_FEEDBACK_0_1',0])
for p in [['CURRENT_LPF_20Hz',0,'AB 1',0],['DC1',0,'AB 1',1],['AB 1',0,'AB 2',0],['DC2',0,'AB 2',1],['AB 2',0,'I_FEEDBACK_0_1',0]]:
    checked('CONNECT_OBJECT',p)
for a,b in [('AB 1','FB_LIMIT_MIN'),('AB 2','FB_LIMIT_MAX'),('DC1','FB_MIN_CONST'),('DC2','FB_MAX_CONST')]:
    checked('SET_OBJECT_PROPERTY',['setName',a,[b]])
checked('COMPILE_PROJECT',[])
print('Explicit input clipping installed before feedback interpolation.')

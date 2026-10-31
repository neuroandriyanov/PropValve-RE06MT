import json,shutil
from pathlib import Path
from sigma_api import call
report=json.loads(Path('output/meter/feedback_calibration.json').read_text())
old=report['coefficients'];minimum=-.79;maximum=.71
rows=json.loads(Path('output/meter/feedback_final_verification.json').read_text())
def lerp(x,points):
    for i in range(len(points)-1):
        if x<=points[i+1][0]:break
    else:i=len(points)-2
    a,b=points[i],points[i+1]
    return a[1]+(x-a[0])*(b[1]-a[1])/(b[0]-a[0])
# Reconstruct the measured filtered ADC value from the known monotone table.
inverse=[(c,minimum+(maximum-minimum)*i/4) for i,c in enumerate(old)]
points=[(-.78,0)]+[(lerp(r['feedback_norm'],inverse),r['meter_amps']) for r in rows if r['meter_amps']>0]
new_min=-.78;new_max=.70
coeff=[lerp(new_min+(new_max-new_min)*i/4,points)/3 for i in range(5)]
coeff[0]=0;coeff[-1]=1
report.update(min=new_min,max=new_max,coefficients=coeff,refinement_points=points)
Path('output/meter/feedback_calibration.json').write_text(json.dumps(report,indent=2))
shutil.copy2('output/meter/feedback_final_verification.json','output/meter/feedback_verification_before_refinement.json')
assert call('SET_OBJECT_PROPERTY',['setControlValue','I_FEEDBACK_0_1',[0,0,'Coefficients',coeff]])
print(json.dumps({'min':new_min,'max':new_max,'coefficients':coeff}))

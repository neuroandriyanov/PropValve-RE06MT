import json
from pathlib import Path
pts=json.loads(Path('output/meter/feedback_r43_10k_filtered.json').read_text())
samples=sorted([(p['adc_mean'],p['amps']) for p in pts if p['amps']>0])
minimum=pts[-1]['adc_mean']
samples.insert(0,(minimum,0))
def linear(x,points):
    for i in range(len(points)-1):
        if x<=points[i+1][0]:break
    else:i=len(points)-2
    a,b=points[i],points[i+1]
    return a[1]+(x-a[0])*(b[1]-a[1])/(b[0]-a[0])
maximum=linear(3,[(a,x) for x,a in samples])
coeff=[linear(minimum+(maximum-minimum)*i/4,samples)/3 for i in range(5)]
coeff[0]=0;coeff[-1]=1
old=[float(v) for v in Path('проект_сигма/current_command_0_3A.txt').read_text().split()]
command_pairs=[(0,old[0])]+[(p['amps'],old[round(p['input']*4)]) for p in pts if p['amps']>0]
command=[old[0]]+[linear(i*.75,command_pairs) for i in range(1,5)]
report={'min':minimum,'max':maximum,'coefficients':coeff,'command_coefficients':command,
        'zero_drift_raw':pts[-1]['adc_mean']-pts[0]['adc_mean'],
        'approx_zero_drift_amps':(pts[-1]['adc_mean']-pts[0]['adc_mean'])*3/(maximum-minimum)}
Path('output/meter/feedback_calibration.json').write_text(json.dumps(report,indent=2))
Path('tmp/sigma/fb_min.txt').write_text(f'{minimum:.9f}')
Path('tmp/sigma/fb_max.txt').write_text(f'{maximum:.9f}')
print(json.dumps(report))

from nrbf_project import Reader
from pathlib import Path
import json
r=Reader(Path('проект_сигма/Design1_parker_v0.dspproj').read_bytes()).read()
for v in r.objects.values():
    f=v.get('fields',{})
    if 'nid' in f and 'name' in f:
        print(json.dumps({'type':v['$type'],'nid':r.resolve(f['nid']),'name':r.resolve(f['name'])}))

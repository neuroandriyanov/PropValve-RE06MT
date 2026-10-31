import sys,json
from pathlib import Path
from nrbf_project import Reader
r=Reader(Path('проект_сигма/Design1_parker_v0.dspproj').read_bytes()).read()
for o in r.objects.values():
    if o.get('$type') in sys.argv[1:]:
        print(json.dumps({'type':o['$type'],'fields':{k:r.resolve(v) for k,v in o['fields'].items()}},ensure_ascii=False))

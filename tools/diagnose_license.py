from pathlib import Path
import re,sys
s=Path(sys.argv[1]).read_text(encoding='utf-8',errors='replace')
terms=['load_cached_license()','WM_AUTO_LICENSE','fn license_monitor','fn accept_capture','fn parse_binding','WH_MOUSE_LL','WM_LBUTTONDOWN','WM_RBUTTONDOWN','fn main','run_key_gate']
for term in terms:
    print('===',term,'===')
    start=0; n=0
    while True:
        i=s.find(term,start)
        if i<0: break
        n+=1
        a=max(0,i-700); b=min(len(s),i+1800)
        print(f'-- occurrence {n} at {i} --')
        print(s[a:b].replace('\\n',' ').replace('\\r',' '))
        start=i+len(term)

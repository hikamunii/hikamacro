from pathlib import Path
import re,sys
s=Path(sys.argv[1]).read_text(encoding='utf-8',errors='replace')
terms=['cached_license','load_cached','save_cached','clear_cached','license_monitor','run_key_gate','WM_AUTO_LICENSE','mouse_hook','WH_MOUSE_LL','WM_XBUTTONDOWN','WM_LBUTTONDOWN','WM_RBUTTONDOWN','MSLLHOOKSTRUCT','parse_binding']
for term in terms:
    print('===',term,'===')
    start=0; count=0
    while count<8:
        i=s.lower().find(term.lower(),start)
        if i<0: break
        a=max(0,i-1200); b=min(len(s),i+3000)
        chunk=s[a:b].replace('\\n',' ').replace('\\r',' ')
        chunk=re.sub(r'https?://[^"\\s]+','<URL>',chunk)
        print(chunk); print('---')
        start=i+len(term); count+=1

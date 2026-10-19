from pathlib import Path
import re,sys
s=Path(sys.argv[1]).read_text(encoding='utf-8',errors='replace')
terms=['license','Connection error','Retry','ureq','validate','saved','BindKind','mouse_button','XBUTTON','LBUTTON','RBUTTON','WM_LBUTTON','WM_RBUTTON']
seen=[]
for term in terms:
    print('===',term,'===')
    start=0; count=0
    while count<12:
        i=s.lower().find(term.lower(),start)
        if i<0: break
        a=max(0,i-700); b=min(len(s),i+1400)
        chunk=s[a:b].replace('\\n',' ').replace('\\r',' ')
        chunk=re.sub(r'https?://[^"\\s]+','<URL>',chunk)
        print(chunk)
        print('---')
        start=i+len(term); count+=1

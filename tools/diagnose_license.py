from pathlib import Path
import re, sys
p=Path(sys.argv[1]); lines=p.read_text(encoding='utf-8',errors='replace').splitlines()
terms=('license','Connection error','Retry','ureq','validate','key','429','rate')
for i,line in enumerate(lines,1):
    if any(t.lower() in line.lower() for t in terms):
        s=line
        s=re.sub(r'https?://[^"\\s]+','<URL>',s)
        s=re.sub(r'([A-Za-z0-9_]*(?:secret|token|api_key|apikey)[A-Za-z0-9_]*)\\s*[:=]\\s*[^,;)]+',r'\\1=<REDACTED>',s,flags=re.I)
        print(f'{i:04d}: {s[:500]}')

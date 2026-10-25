import re,glob,statistics as st,collections
R='reviews/capture-panel/split-experiments'
def gates(arm,model):
    out={}
    for p in glob.glob(f'{R}/dates-{arm}/{model}/dag/romance-graduate/gate-ch*.md'):
        n=int(re.search(r'ch(\d+)',p).group(1))
        if n<25: continue
        t=open(p).read().split('\n',1)[1]
        g=lambda k: (re.search(rf'^\**{k}:\**\s*(.+)$',t,re.M) or [None,None])[1]
        out[n]=dict(cap=float(g('CAPTURE') or 'nan'),dec=g('DECISION'),alm=g('ALMOST-STOPPED'),text=t)
    return out
models=sorted(p.split('/')[-1] for p in glob.glob(f'{R}/dates-dated/*'))
spans={'25-42 pre-Thanksgiving':(25,42),'43-71 Thanksgiving-Gesso+':(43,71),'72-75 tail':(72,75),'25-75 all':(25,75)}
TIME=re.compile(r"\b(how long|how much time|timeline|time ?jump|weeks? (later|passed|have passed)|months? (later|passed)|what day|which day|lost track|chronolog|disorient|confus\w* about (when|time))",re.I)
DATE=re.compile(r"\b(date line|datelines?|the dates?|header|heading|timestamp|(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),? (January|February|March|April|May|June|July|August|September|October|November|December) \d+)",re.I)
print(f"{'model':18}"+''.join(f"{k[:22]:>24}" for k in spans))
agg={a:collections.defaultdict(list) for a in('undated','dated')}
for m in models:
    G={a:gates(a,m) for a in('undated','dated')}
    row=f"{m:18}"
    for k,(lo,hi) in spans.items():
        cell=[]
        for a in('undated','dated'):
            v=[G[a][n]['cap'] for n in range(lo,hi+1) if n in G[a]]
            agg[a][k]+=v
            cell.append(f"{st.mean(v):.2f}" if v else ' -- ')
        row+=f"{cell[0]+'→'+cell[1]:>24}"
    print(row)
    for a in('undated','dated'):
        g=G[a];stops=[n for n,x in g.items() if x['dec'] and 'STOP' in x['dec'].upper()]
        alm=sum(1 for x in g.values() if x['alm'] and x['alm'].strip().lower() not in('none','no','—','-'))
        tq=sum(len(TIME.findall(x['text'])) for x in g.values()); dq=sum(len(DATE.findall(x['text'])) for x in g.values())
        print(f"   {a:8} n={len(g):2} max=ch{max(g)} stops={stops} almost={alm} time-confusion-terms={tq} date-mentions={dq}")
print('ALL', ''.join(f"{st.mean(agg['undated'][k]):.2f}→{st.mean(agg['dated'][k]):.2f}  " for k in spans))

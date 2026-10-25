import json,glob,re,collections
B='/tmp/dates-blind-spring'; key=json.load(open(f'{B}/KEY.json'))
def load(prefix):
    agg={}
    for f in sorted(glob.glob(f'{B}/out-{prefix}*.json')):
        for lane,v in json.load(open(f))['result'].items():
            lane=lane.strip()
            if lane not in key: continue
            a=agg.setdefault(lane,collections.Counter()); errs=agg.setdefault(lane+'#e',[])
            for k,x in v.items():
                if isinstance(x,(int,float)): a[k]+=x
            errs+= [(f.split('out-')[1][:-5],e) for e in v.get('errors',[])]
            agg.setdefault(lane+'#u',[]).extend(v.get('unsure_quotes',[])); agg.setdefault(lane+'#m',[]).extend(v.get('meta',[]))
    return agg
for prefix,fields in (('gates',('correct','wrong','vague','unsure','not_temporal')),('mints',('correct','wrong','vague','unsure','precise_dates'))):
    agg=load(prefix); print(f'\n=== {prefix} ==='); print(f"{'model':18}{'arm':9}"+''.join(f'{x:>13}' for x in fields)+'   err%')
    tot={'dated':collections.Counter(),'undated':collections.Counter()}
    for lane in sorted((l for l in agg if '#' not in l), key=lambda l:(key[l]['model'],key[l]['arm'])):
        c=agg[lane]; arm=key[lane]['arm']; tot[arm]+=c
        ev=c['correct']+c['wrong']; print(f"{key[lane]['model']:18}{arm:9}"+''.join(f'{c[x]:>13}' for x in fields)+f"   {100*c['wrong']/ev if ev else 0:.0f}%")
    for arm,c in tot.items():
        ev=c['correct']+c['wrong']; print(f"{'TOTAL':18}{arm:9}"+''.join(f'{c[x]:>13}' for x in fields)+f"   {100*c['wrong']/ev if ev else 0:.1f}%")
    if prefix=='gates':
        # Thanksgiving-Gesso stretch: error items by chapter
        for arm in ('undated','dated'):
            e=[x for l in agg if l.endswith('#e') and key[l[:-2]]['arm']==arm for x in agg[l]]
            k=[x for x in e if (m:=re.match(r'\s*ch0?(\d+)',x[1])) and 43<=int(m.group(1))<=71]
            u=[x for l in agg if l.endswith('#u') and key[l[:-2]]['arm']==arm for x in agg[l]]
            print(f'{arm}: wrong={len(e)} (ch43-71: {len(k)}), unsure={len(u)}, meta={sum(len(agg[l]) for l in agg if l.endswith("#m") and key[l[:-2]]["arm"]==arm)}')
    json.dump({l:v for l,v in agg.items()},open(f'{B}/agg-{prefix}.json','w'),indent=1,default=list)

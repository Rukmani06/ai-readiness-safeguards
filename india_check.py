import pandas as pd, numpy as np
exec(open('fig_results.py').read().split('# ---------- Figure 3')[0])
def run(df,lab):
    for nm,kw,d in [('within regime',{'g':'v2x_regime'},df),('democracies',{},df[df.v2x_regime>=2]),('autocracies',{},df[df.v2x_regime<2])]:
        e,B=boot(d,**kw); l,h=np.percentile(B[:,2],[2.5,97.5]); print(lab,nm,len(d),np.round(e,2),round(l,2),round(h,2))
run(s,'as coded')
t=s.copy(); t.loc[t.iso3=='IND','v2x_regime']=2; run(t,'India=electoral democracy')
# India's regime history since 2015 needs the full V-Dem v16 file (not included; download from https://v-dem.net).
import os
FULL='vdem/V-Dem-CY-Full+Others-v16.csv'
if os.path.exists(FULL):
    v=pd.read_csv(FULL,usecols=['country_text_id','year','v2x_regime','v2x_polyarchy'])
    print(v[(v.country_text_id=='IND')&(v.year>=2015)])
else:
    print(f'{FULL} not found, so showing 2025 only (from vdem_regime_polyarchy_2025.csv):')
    print(pd.read_csv('vdem_regime_polyarchy_2025.csv').query("iso3=='IND'"))

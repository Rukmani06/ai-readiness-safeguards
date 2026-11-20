import pandas as pd, numpy as np
ox=pd.read_csv('pdf/oxford2025_pillars_iso.csv'); gi=pd.read_csv('pdf/girai2026_scores_iso.csv')
v=pd.read_csv('vdem_subset.csv')
P5=['v2xcl_acjst','v2smgovsmmon_osp','v2cltrnslw_osp','v2clrspct_osp','v2clsocgrp_osp']
v25=v[v.year==2025][['country_text_id']+P5]
v23=v[v.year==2023][['country_text_id','v2peapsecon_osp']]
print('peapsecon non-null 2025:', v[v.year==2025].v2peapsecon_osp.notna().sum(), '2024:', v[v.year==2024].v2peapsecon_osp.notna().sum())
d=gi[['iso3','country','girai','aipolicy','cso','enabling']].rename(columns={'country':'country_girai'})
d=d.merge(ox[['iso3','country','rank','infra','devdiff']].rename(columns={'country':'country_oxford','rank':'oxford_rank'}),on='iso3',how='left')
d=d.merge(v25.rename(columns={'country_text_id':'iso3'}),on='iso3',how='left').merge(v23.rename(columns={'country_text_id':'iso3'}),on='iso3',how='left')
need=['infra','devdiff','aipolicy']+P5+['v2peapsecon_osp']
excl=d[d[need].isna().any(axis=1)]
for _,r in excl.iterrows(): print('excluded:',r.country_girai,'missing',[c for c in need if pd.isna(r[c])])
s=d.dropna(subset=need).copy(); print('n =',len(s))
s['technical']=(s.infra+s.devdiff)/2
PR=['v2xcl_acjst','v2smgovsmmon_osp','v2cltrnslw_osp','v2peapsecon_osp','v2clrspct_osp','v2clsocgrp_osp']
for c in PR: s['z_'+c]=(s[c]-s[c].mean())/s[c].std(ddof=1)
s['practice']=s[['z_'+c for c in PR]].mean(axis=1)
for k in ['technical','aipolicy','practice']:
    s['pos_'+k]=s[k].rank(method='average'); s['pct_'+k]=s['pos_'+k]/len(s)*100
s.to_pickle('s.pkl')

import pandas as pd, numpy as np
s=pd.read_pickle('s.pkl'); n=len(s)
C=['technical','aipolicy','practice']
print('Pearson\n',s[C].corr().round(3)); print('Spearman\n',s[C].corr(method='spearman').round(3))
PR=['v2xcl_acjst','v2smgovsmmon_osp','v2cltrnslw_osp','v2peapsecon_osp','v2clrspct_osp','v2clsocgrp_osp']
rng=np.random.default_rng(20261113); diffs=[]
A=s[['technical','aipolicy']+PR].to_numpy()
for _ in range(5000):
    b=A[rng.integers(0,n,n)]
    z=(b[:,2:]-b[:,2:].mean(0))/b[:,2:].std(0,ddof=1); pr=z.mean(1)
    diffs.append(np.corrcoef(b[:,0],b[:,1])[0,1]-np.corrcoef(b[:,0],pr)[0,1])
d=s.technical.corr(s.aipolicy)-s.technical.corr(s.practice)
print('diff',round(d,3),'95% CI',np.round(np.percentile(diffs,[2.5,97.5]),3))
print('practice SD',round(s.practice.std(),3))
print(s[['infra','devdiff','technical','aipolicy']].mean().round(1))
t=s.set_index('iso3')
for i in ['NLD','IND','USA']:
    r=t.loc[i]; print(i, r[['infra','devdiff','technical','aipolicy','practice']].round(2).tolist(), r[['pct_technical','pct_aipolicy','pct_practice']].round(0).tolist(), [round(r['z_'+c],2) for c in PR])
q=lambda k:s['pct_'+k]
print('top quarter all three:',((q('technical')>75)&(q('aipolicy')>75)&(q('practice')>75)).sum())
nine=s[(q('technical')>75)&(q('practice')<=50)]; print('top-q tech & bottom-half practice:',len(nine),sorted(nine.country_girai))
s['gap']=q('technical')-q('practice')
print(s.sort_values('gap',ascending=False).head(10)[['country_girai','pct_technical','pct_aipolicy','pct_practice','gap']].round(0).to_string(index=False))

import pandas as pd, numpy as np
inc=dict(x.split('|') for x in open('wb_income.txt').read().split())
s=pd.read_pickle('s.pkl'); s['inc']=s.iso3.map(inc); assert s.inc.notna().all()
s['grp']=s.inc.replace({'LIC':'Low/lower-middle','LMC':'Low/lower-middle','UMC':'Upper-middle','HIC':'High'})
PR=['v2xcl_acjst','v2smgovsmmon_osp','v2cltrnslw_osp','v2peapsecon_osp','v2clrspct_osp','v2clsocgrp_osp']
def prac(df): z=(df[PR]-df[PR].mean())/df[PR].std(); return z.mean(axis=1)
def diff(df):
    p=prac(df); a=df.technical.corr(df.aipolicy); b=df.technical.corr(p); return a,b,a-b
def within(df):
    df=df.assign(prac=prac(df)); r=df[['technical','aipolicy','prac']]-df.groupby('grp')[['technical','aipolicy','prac']].transform('mean')
    a=r.technical.corr(r.aipolicy); b=r.technical.corr(r.prac); return a,b,a-b
def ci(f,df):
    rng=np.random.default_rng(20261113); n=len(df); v=[f(df.iloc[rng.integers(0,n,n)])[2] for _ in range(5000)]; return np.percentile(v,[2.5,97.5])
print(s.grp.value_counts().to_dict())
a,b,d=diff(s); lo,hi=ci(diff,s); print(f'All 128: {a:.3f} {b:.3f} diff {d:.3f} CI {lo:.3f}-{hi:.3f}')
a,b,d=within(s); lo,hi=ci(within,s); print(f'Within income groups: {a:.2f} {b:.2f} diff {d:.2f} CI {lo:.2f}-{hi:.2f}')
for g,df in s.groupby('grp'):
    a,b,d=diff(df); lo,hi=ci(diff,df); print(f'{g}: n={len(df)} {a:.2f} {b:.2f} diff {d:.2f} CI {lo:.2f}-{hi:.2f}')
s[['iso3','country_girai','inc','grp']].to_csv('income_groups.csv',index=False)

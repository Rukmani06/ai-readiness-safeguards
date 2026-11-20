"""Sensitivity checks that change the AI-policy side of the comparison (README table, Figure 6).
Recreated 18 Nov 2026; the original script did not survive. Reads s.pkl (run build.py first)
and pdf/girai2026_scores_iso.csv. Same bootstrap as check.py: 5,000 resamples, seed 20261113.

1. AI Policy plus Civil Society Engagement: the GIRAI AI Policy pillar and the Civil Society
   Engagement pillar, each standardised across the 128 countries, then averaged.
2. Four GIRAI dimensions, excluding Labour & Skills: the mean of the other four dimension scores.
"""
import pandas as pd, numpy as np

s = pd.read_pickle('s.pkl')
gi = pd.read_csv('pdf/girai2026_scores_iso.csv')
s = s.merge(gi[['iso3', 'inclusion', 'ethics', 'labour', 'trust', 'aips']], on='iso3')
assert len(s) == 128
PR = ['v2xcl_acjst', 'v2smgovsmmon_osp', 'v2cltrnslw_osp', 'v2peapsecon_osp', 'v2clrspct_osp', 'v2clsocgrp_osp']
z = lambda d, c: (d[c] - d[c].mean()) / d[c].std()

def stats(df, policy):
    zp = (df[PR] - df[PR].mean()) / df[PR].std(); practice = zp.mean(axis=1)
    a = df.technical.corr(policy(df)); b = df.technical.corr(practice); return a, b, a - b

def report(label, policy):
    a, b, d = stats(s, policy); rng = np.random.default_rng(20261113); n = len(s)
    B = [stats(s.iloc[rng.integers(0, n, n)], policy)[2] for _ in range(5000)]
    lo, hi = np.percentile(B, [2.5, 97.5])
    print(f'{label:<48} {a:.2f}  {b:.2f}  difference {d:.2f} ({lo:.2f} to {hi:.2f})')

print(f'{"Version":<48} TR~policy  TR~practice')
report('Main (GIRAI AI Policy pillar)', lambda d: d.aipolicy)
report('AI Policy plus Civil Society Engagement', lambda d: (z(d, 'aipolicy') + z(d, 'cso')) / 2)
report('Four GIRAI dimensions, excl. Labour & Skills', lambda d: d[['inclusion', 'ethics', 'trust', 'aips']].mean(axis=1))

"""Within-group checks (Section 4.2, Appendix A).
Inputs (all in the replication package):
  unripe_base_128_countries.csv      - the three national measures and six V-Dem indicators, 128 countries
  income_groups.csv                  - World Bank income group per country (read 13 Nov 2026)
  vdem_regime_polyarchy_2025.csv     - V-Dem v16, 2025: Regimes of the World (v2x_regime) and electoral democracy index (v2x_polyarchy)
Method: practice = mean of the six indicators, each standardised across the 128 countries.
Within-group: subtract each group's mean from each measure, then correlate. Difference = r(TR, AI policy) - r(TR, practice).
95% intervals: 5,000 bootstrap resamples of countries (seed 20261113), 2.5th-97.5th percentile.
"""
import pandas as pd, numpy as np
from scipy.stats import pearsonr, spearmanr
# Row order follows income_groups.csv, the order used for the published bootstrap intervals.
d = pd.read_csv('income_groups.csv')[['iso3', 'grp']].merge(pd.read_csv('unripe_base_128_countries.csv'), on='iso3') \
     .merge(pd.read_csv('vdem_regime_polyarchy_2025.csv')[['iso3', 'v2x_regime', 'v2x_polyarchy']], on='iso3')
assert len(d) == 128
IND = ['vdem_access_to_justice_2025', 'vdem_social_media_monitoring_2025', 'vdem_transparent_laws_2025',
       'vdem_access_services_income_2023', 'vdem_impartial_admin_2025', 'vdem_equal_liberties_groups_2025']
d = d.rename(columns={'technical_readiness_score': 'tr', 'girai_ai_policy_score': 'pol'})

def stats(df, g=None):
    z = (df[IND] - df[IND].mean()) / df[IND].std(); df = df.assign(prac=z.mean(axis=1))
    c = ['tr', 'pol', 'prac']; r = df[c] - df.groupby(g)[c].transform('mean') if g else df[c]
    a, b = r.tr.corr(r.pol), r.tr.corr(r.prac); return a, b, a - b

def ci(df, g=None):
    rng = np.random.default_rng(20261113); n = len(df)
    v = [stats(df.iloc[rng.integers(0, n, n)], g)[2] for _ in range(5000)]; return np.percentile(v, [2.5, 97.5])

def row(label, df, g=None):
    a, b, x = stats(df, g); lo, hi = ci(df, g)
    print(f'{label:<38} n={len(df):>3}  TR~policy {a:.2f}  TR~practice {b:.2f}  difference {x:.2f} ({lo:.2f} to {hi:.2f})')

d['dem'] = np.where(d.v2x_regime >= 2, 'Democracy', 'Autocracy')
row('All 128 countries', d)
row('Within income groups (pooled)', d, 'grp')
for g in ['High', 'Upper-middle', 'Low/lower-middle']: row(f'  {g} income only', d[d.grp == g])
row('Within regime types (pooled)', d, 'v2x_regime')
row('  Democracies only', d[d.dem == 'Democracy'])
row('  Autocracies only', d[d.dem == 'Autocracy'])
# India recoded as an electoral democracy
e = d.copy(); e.loc[e.iso3 == 'IND', 'v2x_regime'] = 2; e['dem'] = np.where(e.v2x_regime >= 2, 'Democracy', 'Autocracy')
row('India recoded: within regime types', e, 'v2x_regime')
row('India recoded: democracies only', e[e.dem == 'Democracy'])
row('India recoded: autocracies only', e[e.dem == 'Autocracy'])
# Practice and democracy
z = (d[IND] - d[IND].mean()) / d[IND].std(); d['prac'] = z.mean(axis=1)
print(f"Practice ~ electoral democracy index: Pearson {pearsonr(d.prac, d.v2x_polyarchy)[0]:.2f}, Spearman {spearmanr(d.prac, d.v2x_polyarchy)[0]:.2f}")
for c in IND: print(f'  {c:<36} {z[c].corr(d.v2x_polyarchy):.2f}')
print(d.grp.value_counts().to_dict(), d.v2x_regime.value_counts().sort_index().to_dict())

import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.stats import spearmanr

BLUE, ORANGE, INK, MUTED, GRID = '#2a78d6', '#eb6834', '#0b0b0b', '#52514e', '#e1e0d9'
plt.rcParams.update({'font.size': 8.5, 'axes.spines.top': False, 'axes.spines.right': False})

s = pd.read_pickle('s.pkl').merge(pd.read_csv('income_groups.csv')[['iso3', 'grp']], on='iso3') \
    .merge(pd.read_csv('regime_groups.csv')[['iso3', 'v2x_regime']], on='iso3')
assert len(s) == 128
PR = ['v2xcl_acjst', 'v2smgovsmmon_osp', 'v2cltrnslw_osp', 'v2peapsecon_osp', 'v2clrspct_osp', 'v2clsocgrp_osp']
PR4 = ['v2xcl_acjst', 'v2peapsecon_osp', 'v2clrspct_osp', 'v2clsocgrp_osp']
NOT23 = [p for p in PR if p != 'v2peapsecon_osp']
NAMES = {'v2xcl_acjst': 'Access to justice', 'v2smgovsmmon_osp': 'Social media monitoring (restraint)',
         'v2cltrnslw_osp': 'Transparent laws, predictable enforcement', 'v2peapsecon_osp': 'Access to public services (2023)',
         'v2clrspct_osp': 'Impartial public administration', 'v2clsocgrp_osp': 'Equal civil liberties across groups'}

def stats(df, g=None, ind=PR, rank=False):
    z = (df[ind] - df[ind].mean()) / df[ind].std(); df = df.assign(prac=z.mean(axis=1)); c = ['technical', 'aipolicy', 'prac']
    r = df[c] - df.groupby(g)[c].transform('mean') if g else df[c]
    if rank:
        a = spearmanr(r.technical, r.aipolicy)[0]; b = spearmanr(r.technical, r.prac)[0]
    else:
        a = r.technical.corr(r.aipolicy); b = r.technical.corr(r.prac)
    return a, b, a - b

def boot(df, **kw):
    est = stats(df, **kw); rng = np.random.default_rng(20261113); n = len(df)
    B = np.array([stats(df.iloc[rng.integers(0, n, n)], **kw) for _ in range(5000)])
    return est, B

z = (s[PR] - s[PR].mean()) / s[PR].std(); s['prac'] = z.mean(axis=1)
s['dem'] = np.where(s.v2x_regime >= 2, 'Democracy', 'Autocracy')

#: case countries' percentiles + quadrant ----------
fig, (ax, bx) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=200, gridspec_kw={'width_ratios': [0.9, 1.1]})
meas = [('pct_technical', 'Technical\nreadiness'), ('pct_aipolicy', 'AI-policy\nmeasure'), ('pct_practice', 'Institutional\npractice')]
cases = [('NLD', 'Netherlands', BLUE, 'o'), ('IND', 'India', ORANGE, 's'), ('USA', 'United States', MUTED, '^')]
for iso, nm, c, m in cases:
    v = [float(s.loc[s.iso3 == iso, k].iloc[0]) for k, _ in meas]
    print(nm, [round(x) for x in v])
    ax.plot(range(3), v, color=c, lw=1.6, marker=m, ms=7, label=nm)
    for i, x in enumerate(v): ax.text(i + 0.08, x, f'{x:.0f}', fontsize=7.5, color=c, va='center')
ax.axhspan(75, 100, color=BLUE, alpha=0.06); ax.axhline(50, color=GRID, lw=1)
ax.text(2.35, 76.5, 'Top quarter', fontsize=7.5, color=MUTED, ha='right', va='bottom'); ax.text(2.35, 45, 'Median', fontsize=7.5, color=MUTED, ha='right')
ax.set_xticks(range(3)); ax.set_xticklabels([m[1] for m in meas]); ax.set_xlim(-0.3, 2.45)
ax.set_ylim(0, 103); ax.set_ylabel('Percentile rank among 128 countries')
ax.legend(frameon=False, fontsize=8, loc='lower left'); ax.set_title('(a) The case countries', fontsize=9, loc='left')
top = s.pct_technical > 75; low = s.pct_practice <= 50
nine = s[top & low]; print('nine', sorted(nine.country_oxford)); print('all three >75', ((s.pct_technical > 75) & (s.pct_aipolicy > 75) & (s.pct_practice > 75)).sum())
bx.axvspan(75, 101, ymin=0, ymax=50/102, color=ORANGE, alpha=0.10)
bx.scatter(s.pct_technical, s.pct_practice, s=14, color='#b9b8b0', zorder=2)
bx.scatter(nine.pct_technical, nine.pct_practice, s=22, color=ORANGE, zorder=3)
short = {'United Arab Emirates': 'UAE', 'Saudi Arabia': 'Saudi Arabia', 'Viet Nam': 'Viet Nam'}
OFF = {'Malaysia': (-6, 4), 'UAE': (-6, 4), 'Indonesia': (-40, 14), 'India': (6, 6), 'Thailand': (8, -2),
       'Viet Nam': (-40, 4), 'Bahrain': (-40, -8), 'China': (-4, 12), 'Saudi Arabia': (-40, -6)}
for _, r in nine.iterrows():
    nm = short.get(r.country_oxford, r.country_oxford); dx, dy = OFF.get(nm, (-4, 0))
    bx.annotate(nm, (r.pct_technical, r.pct_practice), xytext=(dx, dy), textcoords='offset points',
                ha='left' if dx > 0 else 'right', va='center', fontsize=6.8, color=INK,
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.5) if abs(dx) > 10 else None)
nl = s[s.iso3 == 'NLD'].iloc[0]; bx.scatter(nl.pct_technical, nl.pct_practice, s=26, color=BLUE, zorder=4)
bx.annotate('Netherlands', (nl.pct_technical, nl.pct_practice), xytext=(-4, 0), textcoords='offset points', ha='right', va='center', fontsize=6.8, color=BLUE)
bx.axvline(75, color=MUTED, lw=.8, ls='--'); bx.axhline(50, color=MUTED, lw=.8, ls='--')

bx.set_xlim(0, 101); bx.set_ylim(0, 102)
bx.set_xlabel('Technical readiness, percentile rank'); bx.set_ylabel('Institutional practice, percentile rank')
bx.set_title('(b) All 128 countries', fontsize=9, loc='left')
plt.tight_layout(); plt.savefig('fig8_case_positions.png'); plt.close()
print('done')

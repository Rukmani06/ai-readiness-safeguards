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

# ---------- Figure 3: bootstrap distribution of the difference ----------
est, B = boot(s)
d = B[:, 2]; lo, hi = np.percentile(d, [2.5, 97.5])
print('main', np.round(est, 3), 'CI', round(lo, 3), round(hi, 3), 'share>0', (d > 0).mean(), 'min', d.min().round(3))
fig, ax = plt.subplots(figsize=(7, 3.2), dpi=200)
ax.hist(d, bins=np.arange(-0.05, 0.62, 0.02), color=BLUE, edgecolor='white', linewidth=0.6, zorder=2)
ax.axvspan(lo, hi, color=BLUE, alpha=0.08, zorder=1)
ax.axvline(est[2], color=INK, lw=1.2, zorder=3); ax.axvline(0, color=ORANGE, lw=1.2, ls='--', zorder=3)
ymax = ax.get_ylim()[1]
ax.text(est[2] + 0.008, ymax * 0.93, f'Observed difference {est[2]:.2f}', fontsize=8, color=INK)
ax.text(0.005, ymax * 0.93, 'No difference (0)', fontsize=8, color=ORANGE)
ax.text(hi + 0.01, ymax * 0.6, f'Shaded: 95% interval\n{lo:.2f} to {hi:.2f}', ha='left', fontsize=8, color=MUTED)
ax.set_xlabel('Difference: r(technical, AI policy) − r(technical, practice)')
ax.set_ylabel('Number of resamples'); ax.set_xlim(-0.06, 0.6)
ax.grid(axis='y', color=GRID, lw=.6); ax.set_axisbelow(True)
plt.tight_layout(); plt.savefig('fig3_bootstrap.png'); plt.close()

# ---------- Figure 4: means by income group ----------
order = ['Low & lower-middle', 'Upper-middle', 'High']
xl = ['Low &\nlower-middle', 'Upper-\nmiddle', 'High']
gm = s.groupby('grp')[['technical', 'aipolicy', 'prac']].mean(); print(gm.round(2)); print(s.grp.value_counts())
gm = gm.rename(index=lambda x: {'Low/lower-middle': 'Low & lower-middle'}.get(x, x))
print(gm.index.tolist())
gm = gm.reindex(order)
cnt = s.grp.map({'Low/lower-middle': 'Low & lower-middle'}).fillna(s.grp).value_counts().reindex(order)
shades = ['#a9c9ef', '#5c9be3', '#1b5fae']
fig, axs = plt.subplots(1, 3, figsize=(8, 2.9), dpi=200)
panels = [('technical', 'Technical readiness (0–100)', '{:.0f}'), ('aipolicy', 'AI-policy measure (0–100)', '{:.0f}'),
          ('prac', 'Institutional practice (0 = sample average)', '{:+.2f}')]
for ax, (col, title, fmt) in zip(axs, panels):
    v = gm[col].values
    ax.bar(range(3), v, 0.62, color=shades, zorder=2)
    for i, x in enumerate(v):
        ax.text(i, x + (1.2 if col != 'prac' else (0.04 if x >= 0 else -0.04)), fmt.format(x), ha='center',
                va='bottom' if x >= 0 else 'top', fontsize=8, color=INK)
    ax.set_title(title, fontsize=8.5, color=INK); ax.axhline(0, color='#c3c2b7', lw=.8)
    ax.set_xticks(range(3)); ax.set_xticklabels([f'{o}\n(n = {c})' for o, c in zip(xl, cnt)], fontsize=7)
    ax.grid(axis='y', color=GRID, lw=.6); ax.set_axisbelow(True)
axs[0].set_ylim(0, 65); axs[1].set_ylim(0, 65); axs[2].set_ylim(-0.7, 0.9)
plt.tight_layout(); plt.savefig('fig4_income_means.png'); plt.close()

# ---------- Figure 5 (two panels): correlations + differences by subgroup ----------
groups = [('All 128 countries', s, {}), ('Within income groups', s, {'g': 'grp'}), ('Within regime types', s, {'g': 'v2x_regime'})]
res = {n: boot(df, **kw) for n, df, kw in groups}
sub = [('High income', s[s.grp == 'High']), ('Upper-middle income', s[s.grp == 'Upper-middle']), ('Low & lower-middle income', s[s.grp == 'Low/lower-middle']),
       ('Democracies', s[s.dem == 'Democracy']), ('Autocracies', s[s.dem == 'Autocracy'])]
for n, df in sub: res[n] = boot(df)
for n, (e, Bx) in res.items():
    l, h = np.percentile(Bx[:, 2], [2.5, 97.5]); print(f'{n}: {np.round(e,2)} diff CI {l:.2f} {h:.2f}')
fig, (ax, bx) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=200, gridspec_kw={'width_ratios': [1.15, 1]})
labs = [g[0] for g in groups]; x = np.arange(3); w = 0.36
for j, (c, l, k) in enumerate([(BLUE, 'With the AI-policy measure', 0), (ORANGE, 'With institutional practice', 1)]):
    e = np.array([res[n][0][k] for n in labs]); lo_ = np.array([np.percentile(res[n][1][:, k], 2.5) for n in labs])
    hi_ = np.array([np.percentile(res[n][1][:, k], 97.5) for n in labs]); pos = x + (j - 0.5) * w
    ax.bar(pos, e, w * 0.92, color=c, label=l, zorder=2)
    ax.errorbar(pos, e, yerr=[e - lo_, hi_ - e], fmt='none', ecolor='#444441', elinewidth=1, capsize=3, zorder=3)
    for p, v, h in zip(pos, e, hi_): ax.text(p, h + 0.02, f'{v:.2f}', ha='center', va='bottom', fontsize=8, color=INK)
ax.axhline(0, color='#c3c2b7', lw=.8); ax.set_xticks(x); ax.set_xticklabels(labs, fontsize=8)
ax.set_ylim(-0.1, 1.05); ax.set_ylabel('Correlation with technical readiness (r)')
ax.grid(axis='y', color=GRID, lw=.6); ax.set_axisbelow(True); ax.legend(frameon=False, fontsize=8, loc='upper right')
ax.set_title('(a) Correlations with technical readiness', fontsize=9, loc='left')
fl = labs + [n for n, _ in sub]
ns = [128, 128, 128] + [len(df) for _, df in sub]
y = np.arange(len(fl))[::-1]
for yi, n, nn in zip(y, fl, ns):
    e = res[n][0][2]; l, h = np.percentile(res[n][1][:, 2], [2.5, 97.5])
    col = BLUE if l > 0 else MUTED
    bx.plot([l, h], [yi, yi], color=col, lw=1.6, zorder=2); bx.plot(e, yi, 'o', ms=6, color=col, zorder=3)
    bx.text(1.22, yi, f'{e:.2f} ({l:.2f} to {h:.2f})', va='center', fontsize=7.5, color=INK)
bx.axvline(0, color=ORANGE, lw=1, ls='--'); bx.axhline(4.5, color=GRID, lw=.8)
bx.set_yticks(y); bx.set_yticklabels([f'{n} (n = {k})' for n, k in zip(fl, ns)], fontsize=7.5)
bx.set_xlim(-0.2, 1.2); bx.set_xlabel('Difference between the two correlations, 95% interval')
bx.set_title('(b) The difference, pooled and by subgroup', fontsize=9, loc='left')
bx.grid(axis='x', color=GRID, lw=.6); bx.set_axisbelow(True)
plt.tight_layout(); plt.savefig('fig5_wealth_regime_2panel.png'); plt.close()

# ---------- Figure 6: robustness forest ----------
rows = []
def add(name, e, Bx): l, h = np.percentile(Bx[:, 2], [2.5, 97.5]); rows.append((name, e[2], l, h))
add('Main analysis', *boot(s))
add('Rank correlations (Spearman)', *boot(s, rank=True))
add('Within World Bank income groups', *boot(s, g='grp'))
add('Within regime types', *boot(s, g='v2x_regime'))
rows.append(('V-Dem model estimates', 0.26, 0.13, 0.41))            # README sensitivity table (check.py run)
add('Without the 2023 indicator', *boot(s, ind=NOT23))
rows.append(('AI Policy plus Civil Society Engagement', 0.28, 0.16, 0.43))   # README
rows.append(('Four GIRAI dimensions, excl. Labour & Skills', 0.32, 0.20, 0.46))  # README
add('Four practice indicators (two distant proxies dropped)', *boot(s, ind=PR4))
for r in rows: print('robust', r[0], [round(v, 2) for v in r[1:]])
fig, ax = plt.subplots(figsize=(8, 3.8), dpi=200)
y = np.arange(len(rows))[::-1]
for yi, (n, e, l, h) in zip(y, rows):
    c = INK if n == 'Main analysis' else BLUE
    ax.plot([l, h], [yi, yi], color=c, lw=1.6); ax.plot(e, yi, 'o', ms=6, color=c)
    ax.text(0.83, yi, f'{e:.2f} ({l:.2f} to {h:.2f})', va='center', fontsize=7.5, color=INK)
ax.axvline(0, color=ORANGE, lw=1, ls='--'); ax.axvline(rows[0][1], color=GRID, lw=1)
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=7.8)
ax.set_xlim(-0.1, 1.05); ax.set_xlabel('Difference between the two correlations, with 95% bootstrap interval')
ax.grid(axis='x', color=GRID, lw=.6); ax.set_axisbelow(True)
plt.tight_layout(); plt.savefig('fig6_robustness.png'); plt.close()

# ---------- Figure 7: each practice indicator vs technical readiness ----------
ic = {p: s.technical.corr(s[p]) for p in PR}; ic = dict(sorted(ic.items(), key=lambda kv: kv[1]))
print({NAMES[k]: round(v, 2) for k, v in ic.items()})
fig, ax = plt.subplots(figsize=(7, 2.9), dpi=200)
yy = np.arange(len(ic))
cols = [ORANGE if k == 'v2peapsecon_osp' else '#8fb6e8' for k in ic]
ax.barh(yy, list(ic.values()), 0.6, color=cols, zorder=2)
for yi, v in zip(yy, ic.values()): ax.text(v + 0.01, yi, f'{v:.2f}', va='center', fontsize=8, color=INK, bbox=dict(fc='white', ec='none', pad=0.5))
ax.axvline(est[1], color=INK, lw=1, ls=':'); ax.text(est[1] + 0.01, len(ic) - 0.45, f'Six-indicator composite {est[1]:.2f}', fontsize=7.5, color=INK)
ax.set_yticks(yy); ax.set_yticklabels([NAMES[k] for k in ic], fontsize=8); ax.set_xlim(0, 0.8)
ax.set_xlabel('Correlation with technical readiness (r), 128 countries')
ax.grid(axis='x', color=GRID, lw=.6); ax.set_axisbelow(True)
plt.tight_layout(); plt.savefig('fig7_indicators.png'); plt.close()

# ---------- Figure 8: case countries' percentiles + quadrant ----------
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

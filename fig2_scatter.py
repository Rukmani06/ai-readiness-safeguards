"""Figure 2: technical readiness against the AI-policy measure (left) and institutional practice (right).
Recreated 18 Nov 2026; the original script for this figure did not survive. Reads s.pkl (run build.py first).
Writes figure2_scatter_usa.png.
"""
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt

BLUE, ORANGE, GREEN, INK, GRID = '#2a78d6', '#eb6834', '#1fae7e', '#0b0b0b', '#e1e0d9'
plt.rcParams.update({'font.size': 8.5, 'axes.spines.top': False, 'axes.spines.right': False})

s = pd.read_pickle('s.pkl'); assert len(s) == 128
CASES = [('NLD', 'Netherlands', BLUE, 'o', (8, 8)), ('IND', 'India', ORANGE, 's', (6, -14)),
         ('USA', 'United States', GREEN, 'D', (-60, 14))]
PANELS = [('aipolicy', 'AI-policy frameworks and initiatives (0–100)'),
          ('practice', 'Institutional practice (0 = sample average)')]

fig, axs = plt.subplots(1, 2, figsize=(10, 4.6), dpi=200)
for ax, (col, ylab) in zip(axs, PANELS):
    x, y = s.technical, s[col]
    ax.scatter(x, y, s=14, color='#a3a29b', zorder=2)
    b, a = np.polyfit(x, y, 1); xs = np.array([x.min(), x.max()])
    ax.plot(xs, a + b * xs, color='#444441', lw=1.1, ls='--', zorder=1)
    for iso, name, c, m, off in CASES:
        r = s[s.iso3 == iso].iloc[0]
        ax.scatter(r.technical, r[col], s=50, color=c, marker=m, zorder=4)
        ax.annotate(name, (r.technical, r[col]), xytext=off, textcoords='offset points', fontsize=9, color=INK)
    ax.set_title(f'r = {x.corr(y):.2f}', loc='left', fontsize=10)
    ax.set_xlabel('Technical readiness (0–100)'); ax.set_ylabel(ylab)
    ax.grid(axis='y', color=GRID, lw=.6); ax.set_axisbelow(True)
plt.tight_layout(); plt.savefig('figure2_scatter_usa.png'); plt.close()
print('done')

import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
s=pd.read_pickle('s.pkl'); assert len(s)==128
bins=np.arange(0,101,5)
fig,axs=plt.subplots(2,1,figsize=(7.5,5.0),dpi=200,sharex=True)
for ax,(k,lab,c) in zip(axs,[('technical','Technical readiness','#2a78d6'),('aipolicy','AI-policy measure','#eb6834')]):
    v=s[k]
    if k=='aipolicy':
        ax.axvspan(0,30,color='#eb6834',alpha=0.08,zorder=0)
        n30=(v<30).sum()
        ax.text(6.5,21,f'{n30} of 128 countries\n(just over half)\nscore below 30',ha='left',va='top',fontsize=8,color='#52514e')
    ax.hist(v,bins=bins,color=c,edgecolor='white',linewidth=1.5,zorder=2)
    m=v.mean(); ax.axvline(m,color='#0b0b0b',lw=1,ls='--',zorder=3)
    ax.text(m+1,29.5,f'mean {m:.1f} (SD {v.std():.1f})',fontsize=8,va='top',color='#0b0b0b')
    ax.set_title(lab,fontsize=9,loc='left'); ax.set_ylabel('Countries',fontsize=8.5)
    ax.set_ylim(0,30); ax.set_yticks(range(0,31,5))
    for sp in ['top','right']: ax.spines[sp].set_visible(False)
    ax.grid(axis='y',color='#e1e0d9',lw=.6); ax.set_axisbelow(True); ax.tick_params(labelsize=8)
z=(s.aipolicy==0).sum(); n5=(s.aipolicy<5).sum()
axs[1].annotate(f'{z} countries score exactly 0',xy=(5,24.5),xytext=(55,25.5),fontsize=8,color='#0b0b0b',
                arrowprops=dict(arrowstyle='->',color='#52514e',lw=0.8))
axs[1].set_xlabel('Score (0–100), 5-point intervals',fontsize=8.5); axs[1].set_xlim(0,100)
plt.tight_layout(); plt.savefig('figure_distributions_v2.png'); print(n5,z,(s.aipolicy<30).sum())

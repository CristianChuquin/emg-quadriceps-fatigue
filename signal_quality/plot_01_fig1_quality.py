import pandas as pd, numpy as np, matplotlib as mpl, matplotlib.pyplot as plt
from scipy.signal import welch
PALETTE={"primary":"#4A235A","secondary":"#1A5276","line":"#BDC3C7","panel":"#F2F3F4","text":"#1C1C1C"}
mpl.rcParams.update({"font.family":"sans-serif","font.sans-serif":["DejaVu Sans"],"font.size":9,"axes.titlesize":10,"axes.titleweight":"bold",
 "axes.edgecolor":PALETTE["line"],"axes.grid":True,"grid.color":PALETTE["panel"],"savefig.dpi":300,"savefig.bbox":"tight"})
import glob, os
# Participant folders are anonymised as S01-S15 in alphabetical order of the dataset folders.
S14=sorted(glob.glob('emg/raw/*/'))[13]
def trial(t,leg): return os.path.relpath(glob.glob(os.path.join(S14,f'{t}_{leg}_*.csv'))[0],'emg/raw')
sel=[(trial('R2','dr'),'Accepted: S14, right leg, R2'),(trial('R3','dr'),'Rejected (E5): S14, right leg, R3')]
fig,ax=plt.subplots(2,2,figsize=(7.2,4.4),gridspec_kw={'width_ratios':[2.2,1]})
for i,(f,t) in enumerate(sel):
    d=pd.read_csv('emg/raw/'+f); x=d.Voltage_mV.values-d.Voltage_mV.mean(); tt=d.Relative_Time_s.values
    c=PALETTE['secondary'] if i==0 else PALETTE['primary']
    m=(tt>=2)&(tt<=17); ax[i,0].plot(tt[m],x[m],lw=0.4,color=c); ax[i,0].set_title(t,loc='left'); ax[i,0].set_ylabel('mV')
    fr,P=welch(x,fs=1000,nperseg=2048); lfp=100*P[(fr>=1)&(fr<20)].sum()/P[(fr>=1)&(fr<=450)].sum()
    ax[i,1].semilogy(fr,P,color=c,lw=0.8); ax[i,1].axvspan(1,20,color=PALETTE['line'],alpha=0.5); ax[i,1].set_xlim(0,250)
    ax[i,1].set_title(f'1-20 Hz share: {lfp:.0f} %',loc='left'); ax[i,1].set_ylabel('PSD (mV$^2$/Hz)')
ax[1,0].set_xlabel('Time (s)'); ax[1,1].set_xlabel('Frequency (Hz)')
fig.tight_layout(); fig.savefig('signal_quality/fig_01_quality.png')

import pandas as pd, numpy as np, glob, os, re
from scipy.signal import welch
df=pd.read_csv('signal_quality/quality_per_trial.csv')
lf=[]
for f in sorted(glob.glob('emg/raw/**/*.csv',recursive=True)):
    x=pd.read_csv(f)['Voltage_mV'].values; x=x-x.mean()
    fr,P=welch(x,fs=1000,nperseg=2048)
    lf.append(100*P[(fr>=1)&(fr<20)].sum()/P[(fr>=1)&(fr<=450)].sum())
df['lf_pct']=lf; df.to_csv('signal_quality/quality_per_trial.csv',index=False)
print(df.lf_pct.describe().round(1))
print(df.sort_values('lf_pct',ascending=False).head(10)[['subject','leg','trial','lf_pct','mdf_hz','snr_db']].round(1).to_string())

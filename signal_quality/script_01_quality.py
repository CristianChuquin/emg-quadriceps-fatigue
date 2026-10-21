import glob, os, re, numpy as np, pandas as pd
from scipy.signal import butter, filtfilt, welch, find_peaks
FS=1000
rows=[]
for f in sorted(glob.glob('emg/raw/**/*.csv', recursive=True)):
    d=pd.read_csv(f); x=d['Voltage_mV'].values.astype(float); adc=d['ADC_Value'].values
    name=os.path.basename(f); subj=os.path.basename(os.path.dirname(f))
    m=re.match(r'(R\d(?:_1)?)_(dr|iz)_',name); trial,leg=m.group(1),m.group(2)
    dt=np.median(np.diff(d['Relative_Time_s'].values))
    b,a=butter(4,[20,450],btype='band',fs=FS); y=filtfilt(b,a,x-np.mean(x))
    f_,P=welch(x-np.mean(x),fs=FS,nperseg=2048)
    band=(f_>=20)&(f_<=450); pl=(f_>=58)&(f_<=62)
    pl_ratio=P[pl].sum()/P[band].sum()
    mdf_total=f_[band][np.searchsorted(np.cumsum(P[band]),P[band].sum()/2)]
    w=FS; rms=np.array([np.sqrt(np.mean(y[i:i+w]**2)) for i in range(0,len(y)-w,w//2)])
    snr=20*np.log10(np.sqrt(np.mean(y**2))/rms.min())
    env=filtfilt(*butter(2,3,fs=FS),np.abs(y))
    pk,_=find_peaks(env,height=0.3*np.percentile(env,99),distance=int(0.8*FS),prominence=0.15*np.percentile(env,99))
    clip=np.mean((adc<=0)|(adc>=4095))
    rows.append(dict(subject=subj,leg=leg,trial=trial,dur_s=len(x)*dt,fs=round(1/dt),adc_min=adc.min(),adc_max=adc.max(),
        clip_pct=100*clip,pl_pct=100*pl_ratio,snr_db=snr,mdf_hz=mdf_total,reps=len(pk)))
df=pd.DataFrame(rows); df.to_csv('signal_quality/quality_per_trial.csv',index=False)
pd.set_option('display.width',200)
print(df.describe().round(2).to_string())
print(df.groupby('trial').size())
print(df.sort_values('snr_db').head(8).round(2).to_string())
print(df.sort_values('pl_pct',ascending=False).head(6).round(2).to_string())
print('adc max overall',df.adc_max.max(),'min',df.adc_min.min())

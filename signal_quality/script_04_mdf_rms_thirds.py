import glob,os,re,numpy as np,pandas as pd
from scipy.signal import butter,filtfilt,welch
FS=1000; b,a=butter(4,[20,450],btype='band',fs=FS); rows=[]
for f in sorted(glob.glob('emg/raw/**/*.csv',recursive=True)):
    name=os.path.basename(f); m=re.match(r'(R\d(?:_1)?)_(dr|iz)_',name)
    x=pd.read_csv(f)['Voltage_mV'].values.astype(float); y=filtfilt(b,a,x-x.mean())
    n=len(y)//3; seg=[y[:n],y[n:2*n],y[2*n:3*n]]; mdf=[];rms=[]
    for s in seg:
        fr,P=welch(s,fs=FS,nperseg=2048); bd=(fr>=20)&(fr<=450); c=np.cumsum(P[bd])
        mdf.append(fr[bd][np.searchsorted(c,c[-1]/2)]); rms.append(np.sqrt(np.mean(s**2)))
    rows.append(dict(subj=os.path.basename(os.path.dirname(f)),trial=m.group(1),leg=m.group(2),mdf1=mdf[0],mdf3=mdf[2],rms1=rms[0],rms3=rms[2]))
d=pd.DataFrame(rows); d['dmdf']=100*(d.mdf3/d.mdf1-1); d['drms']=100*(d.rms3/d.rms1-1)
k=d[~d.trial.str.startswith('R0')]; print(len(d),len(k))
print('MDF down',(k.dmdf<0).sum(),'median',k.dmdf.median().round(1)); print('RMS up',(k.drms>0).sum(),'median',k.drms.median().round(1))
d.to_csv('signal_quality/mdf_rms_thirds.csv',index=False)

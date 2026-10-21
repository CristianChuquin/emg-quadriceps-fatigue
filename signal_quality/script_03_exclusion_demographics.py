import pandas as pd, numpy as np
df=pd.read_csv('signal_quality/quality_per_trial.csv')
df['excl']=''
df.loc[~df.trial.isin(['R1','R2','R3','R4','R5']),'excl']='E1 not part of R1-R5'
m=(df.excl=='')
df.loc[m&(df.snr_db<15),'excl']='E2 SNR<15dB'
df.loc[(df.excl=='')&(df.pl_pct>15),'excl']='E3 powerline>15%'
df.loc[(df.excl=='')&(df.sat_pct>1),'excl']='E4 saturation>1%'
df.loc[(df.excl=='')&(df.lf_pct>25),'excl']='E5 motion artefact LF>25%'
df.to_csv('signal_quality/quality_per_trial.csv',index=False)
print(df.excl.value_counts())
print(df[df.excl!=''][['subject','leg','trial','snr_db','pl_pct','lf_pct','excl']].round(1).to_string())
k=df[df.excl=='']
print('kept trials',len(k),'subjects',k.subject.nunique())
print(k.groupby('leg').size())
for leg in ['dr','iz']:
    r=k[k.leg==leg].reps; print(leg,'reps mean %.1f sd %.1f range %d-%d n=%d'%(r.mean(),r.std(),r.min(),r.max(),len(r)))
    r1=k[(k.leg==leg)&(k.trial=='R1')].reps; print(leg,'R1 reps mean %.1f sd %.1f range %d-%d n=%d'%(r1.mean(),r1.std(),r1.min(),r1.max(),len(r1)))
print('dur by trial', k.groupby('trial').dur_s.mean().round(1).to_dict())
print('SNR kept median %.1f IQR %.1f-%.1f'%(k.snr_db.median(),k.snr_db.quantile(.25),k.snr_db.quantile(.75)))
print('PL kept median %.1f max %.1f'%(k.pl_pct.median(),k.pl_pct.max()))
print('subjects per leg', k.groupby('leg').subject.nunique().to_dict())
print(k.groupby(['subject','leg']).size().unstack().fillna(0).astype(int).to_string())

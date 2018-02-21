import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as sm
from sklearn.isotonic import IsotonicRegression

params={
    'IgnAdvCYL1':True,
    'AirTempC':True,
    'MAP_PSI':True,
    'LC1.AFR':True,
    'InjPulse(ms)':True,
    'KnkVolt':True,
    'KnkNoiseLev':True,
    'KnockRetard':True,
    'AirMasskg/h':True}

df = pd.read_csv('/Users/canf/Documents/miniport/log0117.csv')
df = pd.read_csv('/Users/canf/Documents/miniport/log0117.csv')
df = pd.read_csv('/Users/canf/Documents/miniport/old/log0006.csv')
df_3_wot = df.loc[(df['GearPosition'] == 3) & (df['PedalAng%']>90) & (df['RPM']<7550)]



df2 = pd.read_csv('/Users/canf/Documents/miniport/log0061.csv')
df2 = pd.read_csv('/Users/canf/Documents/miniport/tune4/log0025_3rd_gear_wot_tune4.csv')
if(not df2.empty):
    df_3_wot_2 = df2.loc[(df2['GearPosition'] == 3) & (df2['PedalAng%']>90) & (df2['RPM']<7550)]
'''
df = df.append(df2)
'''
print list(df)
print df_3_wot_2['AirTempC'], df_3_wot_2['KnockRetard']

'''Regression on noise'''
fit= sm.ols(formula="KnkNoiseLev ~ RPM", data=df_3_wot).fit()
exog = df_3_wot['RPM']
noise_ols = fit.predict(exog = exog)

ir = IsotonicRegression()
noise_ols = ir.fit_transform(df_3_wot['RPM'], df_3_wot['KnkNoiseLev'])

fit= sm.ols(formula="KnkNoiseLev ~ RPM", data=df_3_wot_2).fit()
exog = df_3_wot_2['RPM']
noise_ols_2 = fit.predict(exog = exog)

noise_ols_2 = ir.fit_transform(df_3_wot_2['RPM'], df_3_wot_2['KnkNoiseLev'])

X_RANGE =np.arange(1000,7800, 200)
Y_RANGE =np.arange(-100,+100, 0.5)
fig, ax1 = plt.subplots()
ax1.set_xlabel('RPM')
ax1.xaxis.set_ticks(X_RANGE)
ax1.yaxis.set_ticks(Y_RANGE)

plt.grid()

if params['LC1.AFR']==True: ax1.plot([df_3_wot['RPM'].min(),df_3_wot['RPM'].max()], ['14.6', '14.6'], 'k-')
if params['LC1.AFR']==True: ax1.plot([df_3_wot['RPM'].min(),df_3_wot['RPM'].max()], ['11.6', '11.6'], 'k-')
if params['LC1.AFR']==True: ax1.plot(df_3_wot['RPM'], df_3_wot['LC1.AFR'], 'b-', label="AFR")
if params['IgnAdvCYL1']==True: ax1.plot(df_3_wot['RPM'], df_3_wot['IgnAdvCYL1'], 'y-', label="IgnAdvCYL1")
if params['KnockRetard']==True: ax1.plot(df_3_wot['RPM'], df_3_wot['KnockRetard'], 'g-', label="KR")
if params['MAP_PSI']==True: ax1.plot(df_3_wot['RPM'], df_3_wot['MAP_PSI'], 'k-', label="MAP_PSI")
if params['KnkVolt']==True: ax1.plot(df_3_wot['RPM'], df_3_wot['KnkVolt'], color='navy', linestyle='-', linewidth=1, label="KnkVolt")
if params['InjPulse(ms)']==True: ax1.plot(df_3_wot['RPM'], df_3_wot['InjPulse(ms)'], 'm-', label="InjPulse" )
ax1.legend(loc="upper left")

if(not df_3_wot_2.empty):
    if params['IgnAdvCYL1']==True: ax1.plot(df_3_wot_2['RPM'], df_3_wot_2['IgnAdvCYL1'], 'y--', label="IgnAdvCYL1")
    if params['LC1.AFR']==True: ax1.plot(df_3_wot_2['RPM'], df_3_wot_2['LC1.AFR'], 'b--', label="AFR")
    if params['KnockRetard']==True: ax1.plot(df_3_wot_2['RPM'], df_3_wot_2['KnockRetard'], 'g--', label="KR")
    if params['MAP_PSI']==True: ax1.plot(df_3_wot_2['RPM'], df_3_wot_2['MAP_PSI'], 'k--', label="MAP_PSI")
    if params['KnkVolt']==True: ax1.plot(df_3_wot_2['RPM'], df_3_wot_2['KnkVolt'], color='navy', linestyle='--',  linewidth=1, label="KnkVolt")
    if params['InjPulse(ms)']==True: ax1.plot(df_3_wot_2['RPM'], df_3_wot_2['InjPulse(ms)'], 'm--', label="InjPulse" )

    '''ax3.legend(loc="lower right")'''

ax2 = ax1.twinx()
if params['AirTempC']==True: ax2.plot(df_3_wot['RPM'], df_3_wot['AirTempC'],  'r-', label="AirTempC")
if params['KnkNoiseLev']==True: ax2.plot(df_3_wot['RPM'], df_3_wot['KnkNoiseLev'], 'go', label="KnkNoiseLev")
if params['KnkNoiseLev']==True: ax2.plot(df_3_wot['RPM'], noise_ols, color='peru', linestyle="-", label="noise_ols")
if params['AirMasskg/h']==True: ax2.plot(df_3_wot['RPM'], df_3_wot['AirMasskg/h'] / 10, 'c-',label="AirMass kg/h / 10")

ax2.legend(loc="lower left")

if(not df_3_wot_2.empty):
    if params['AirTempC']==True: ax2.plot(df_3_wot_2['RPM'], df_3_wot_2['AirTempC'], 'r--', label="AirTempC")
    if params['KnkNoiseLev']==True: ax2.plot(df_3_wot_2['RPM'], df_3_wot_2['KnkNoiseLev'], 'gx', label="KnkNoiseLev")
    if params['KnkNoiseLev']==True: ax2.plot(df_3_wot_2['RPM'], noise_ols_2, color='peru',  linestyle="--", label="noise_ols")
    if params['AirMasskg/h']==True: ax2.plot(df_3_wot_2['RPM'], df_3_wot_2['AirMasskg/h'] / 10, 'c--', label="AirMass kg/h / 10")



'''plt.grid()'''
plt.show()

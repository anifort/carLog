from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as sm
from calculator import Calculator
from sklearn.isotonic import IsotonicRegression

pd.set_option('precision',2)

calc = Calculator()

df0 = pd.read_csv('/Users/canf/Documents/miniport/tune8/log0013_3rd_WOT_1_tune8.csv')
df1 = pd.read_csv('/Users/canf/Documents/miniport/tune8/log0016_6th_cruise_tune7.csv')

df = df0.append(df1)
df['bhp'] = calc.airmassKghToBhp(df['AirMasskg/h'], df['LC1.AFR'])
df['AirMassG/s'] = calc.kghToGs(df['AirMasskg/h'])
df['AirMassLb/h'] = calc.kghToLbh(df['AirMasskg/h'])
df['fuel/s'] = calc.kghToGs(df['AirMasskg/h'])
df['afrToFuelRateLb/h'] = calc.flowRateLbH(df['AirMassLb/h'], df['LC1.AFR'])
df['pulseToFuelRateLb/h'] = calc.pulseFlowRate(df['InjPulse(ms)'],df['RPM'])

rpm_range = [600,750,1000,1200,1600,2000,2600,2800,3400,3800,4000,4200,4400,5000,5200,5400,5800,6000,6500,7550]
load_range = [0,35.69, 57.11,92.80,178.44,221.27,267.67,314.07,361.18,407.58,454.69,521.05,578.16,1000]



rpms = pd.cut(df['RPM'], rpm_range)
load = pd.cut(df['AirMasskg/h'], load_range)
print  df.pivot_table('InjPulse(ms)', [rpms], [load], aggfunc=np.mean).to_string()+"\n\n"
print  df.pivot_table('KnockRetard', [rpms], [load], aggfunc=np.mean).to_string()+"\n\n"



print  df.pivot_table('bhp', [rpms], [load], aggfunc=np.max).to_string()+"\n\n"

print  df.pivot_table('AirMasskg/h', [rpms], [load], aggfunc=np.min).to_string()+"\n\n"

print "PULSE ms \n\n"
print  df.pivot_table('InjPulse(ms)', [rpms], [load], aggfunc=np.median).to_string()+"\n\n"

print  df.pivot_table('IgnAdvCYL1', [rpms], [load], aggfunc=np.min).to_string()+"\n\n"


print  df.pivot_table('LC1.AFR', [rpms], [load], aggfunc=np.mean).to_string()+"\n\n"
print  df.pivot_table('AirMassLb/h', [rpms], [load], aggfunc=np.mean).to_string()+"\n\n"
print  df.pivot_table('afrToFuelRateLb/h', [rpms], [load], aggfunc=np.mean).to_string()+"\n\n"
print  df.pivot_table('pulseToFuelRateLb/h', [rpms], [load], aggfunc=np.mean).to_string()+"\n\n"

print "PULSE ms \n\n"
print  df.pivot_table('InjPulse(ms)', [rpms], [load], aggfunc=np.median).to_string()+"\n\n"

import matplotlib
matplotlib.use('tkAgg')

import numpy as np
import matplotlib.pyplot as plt
from configuration import *

t = 17000//4
fres_q1 = qubit_IF_q1
fres_q2 = qubit_IF_q2
dfs = np.arange(- 40e6, + 30e6, 0.30e6)
dcs = np.arange(-0.03, 0.21, 0.002)
n_avg = 100000
LO = qubit_LO/u.MHz
IF_q1 = -qubit_IF_q1/u.MHz
IF_q2 = -qubit_IF_q2/u.MHz

x = np.load("9_multi_qubit_spec_vs_flux_02.npz")
I1 = x.f.I1
Q1 = x.f.Q1
I2 = x.f.I2
Q2 = x.f.Q2

s1 = I1 + 1j * Q1
plt.title("q1 amp (LO: %s)" %(LO))
plt.xlabel("flux-1")
plt.ylabel("q1_ifreq")
plt.pcolor(dcs, LO + IF_q1 - dfs/u.MHz, np.abs(s1))
pts_to_fit = plt.ginput(3, timeout=-1)
print(pts_to_fit)
x = np.array(list(zip(*pts_to_fit))[0])
y = np.array(list(zip(*pts_to_fit))[1])
print(x)
print(y)
fit_params = np.polyfit(x, y, 2)
fit = np.polyval(fit_params, dcs)
plt.plot(x, y, '*', color="red")
plt.plot(dcs, fit, color='red')
plt.show()
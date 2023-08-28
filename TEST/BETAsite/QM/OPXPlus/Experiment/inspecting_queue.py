from qm.QuantumMachinesManager import QuantumMachinesManager, QmJob
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.units import unit
from configuration import config, qop_ip, save_dir
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import numpy as np

qmm = QuantumMachinesManager(host=qop_ip, port=80)
print("QM-version: %s" %qmm.version())
qm_list =  qmm.list_open_quantum_machines()
qm = qmm.get_qm(qm_list[0])
print("QM-ID: %s" %qm.id)
job = qm.get_running_job()
print("JOB-ID: %s" %job.id())
job = QmJob(qmm, job.id())

ts = np.arange(4, 200, 1)
amps = np.arange(-0.098, -0.118, -0.0005)
n_avg = 1300000

results = fetching_tool(job, ["n", "I1", "Q1", "I2", "Q2"], mode="live")
n, I1, Q1, I2, Q2 = results.fetch_all()
progress_counter(n, 130000)
print("Completed %s shots" %n)

fig, ax = plt.subplots(2,2)

u = unit()
ax[0,0].cla()
ax[0,0].pcolor(amps,4*ts, I1)
ax[0,0].set_title('q1 - I , n={}'.format(n))
ax[0,0].set_xlabel("Z1 (V)")
ax[0,0].set_ylabel("Exchange time (ns)")

ax[1,0].cla()
ax[1,0].pcolor(amps,4*ts, Q1)
ax[1,0].set_title('q1 - Q , n={}'.format(n))
ax[1,0].set_xlabel("Z1 (V)")
ax[1,0].set_ylabel("Exchange time (ns)")

ax[0,1].cla()
ax[0,1].pcolor(amps,4*ts, I2)
ax[0,1].set_title('q2 - I , n={}'.format(n))
ax[0,1].set_xlabel("Z1 (V)")
ax[0,1].set_ylabel("Exchange time (ns)")

ax[1,1].cla()
ax[1,1].pcolor(amps,4*ts, Q2)
ax[1,1].set_title('q2 - Q , n={}'.format(n))
ax[1,1].set_xlabel("Z1 (V)")
ax[1,1].set_ylabel("Exchange time (ns)")

plt.show()
np.savez(save_dir/'cz', I1=I1, Q1=Q1, I2=I2, Q2=Q2, ts=ts, amps=amps)

fig, ax = plt.subplots(1,2)
fsize = 18

ax[0].cla()
ax[0].pcolor(amps,4*ts, Q1)
ax[0].set_title('Q1 1-2 Exchange', fontsize=fsize)
ax[0].tick_params(axis='both', which='major', labelsize=fsize)
ax[0].set_xlabel("Z1 (V)", fontsize=fsize)
ax[0].set_ylabel("Exchange time (ns)", fontsize=fsize)

ax[1].cla()
ax[1].pcolor(amps,4*ts, Q2)
ax[1].set_title('Q2 1-0 Exchange', fontsize=fsize)
ax[1].tick_params(axis='both', which='major', labelsize=fsize)
ax[1].set_xlabel("Z1 (V)", fontsize=fsize)
ax[1].set_ylabel("Exchange time (ns)", fontsize=fsize)

plt.show()


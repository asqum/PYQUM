from qm.QuantumMachinesManager import QuantumMachinesManager, QmJob
from qm import SimulationConfig
from configuration import config, qop_ip, save_dir

from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.plot import interrupt_on_close
from qualang_tools.units import unit

import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import os, fnmatch

from Macros import cz_gate
from cosine import Cosine

# from E12_single_qubit_T1 import *
from qua_code import *

filename = 'Test_'
modelist = ['sim', 'prev', 'load', 'new']
mode = modelist[int(input("1. simulate, 2. previous job, 3. load data, 4. new run (1-4)?"))-1]
print("mode: %s" %mode)
data_dict = dict()

# Prepare Figures
###########################################
row,col = 2,2
fig, ax = plt.subplots(row,col)
def data_present(live=True, data=[]):
    fig.suptitle('Tuning CZ on: %s'%filename, fontsize=20, fontweight='bold', color='blue')

    if len(data)==0:
        results = fetching_tool(job, SCOPE, mode="live")
        for i, dataz in enumerate(results.fetch_all()): data_dict[SCOPE[i]] = dataz
        
        
    # else: n, I1g, Q1g, I2g, Q2g, I1e, Q1e, I2e, Q2e = \
    #         data.f.n, data.f.I1g, data.f.Q1g, data.f.I2g, data.f.Q2g, data.f.I1e, data.f.Q1e, data.f.I2e, data.f.Q2e
    progress_counter(data_dict["n"], n_avg)

    u = unit()
    ax[0,0].cla()
    ax[0,0].plot(Phi, I1g, 'b', Phi, I1e, 'r')
    ax[0,0].set_title('q1 - I , n={}'.format(n))
    ax[1,0].cla()
    ax[1,0].plot(Phi, Q1g, 'b', Phi, Q1e, 'r')
    ax[1,0].set_title('q1 - Q , n={}'.format(n))
    ax[0,1].cla()
    ax[0,1].plot(Phi, I2g, 'b', Phi, I2e, 'r')
    ax[0,1].set_title('q2 - I , n={}'.format(n))
    ax[1,1].cla()

    try:
        fit = Cosine(Phi, Q2g, plot=False)
        phase_g = fit.out.get('phase')[0]
        ax[1, 1].plot(fit.x_data, fit.fit_type(fit.x, fit.popt) * fit.y_normal, '-b', alpha=0.5)
        fit = Cosine(Phi, Q2e, plot=False)
        phase_e = fit.out.get('phase')[0]
        ax[1, 1].plot(fit.x_data, fit.fit_type(fit.x, fit.popt) * fit.y_normal, '-r', alpha=0.5)
            
    except Exception as e:
        print(e)
        
    ax[1,1].plot(Phi, Q2g, '.b', Phi, Q2e, '.r')
    ax[1,1].set_title('q2 - Q , n={}, pha_diff={}'.format(n, phase_g-phase_e))

    if live: 
        plt.pause(4.0)
    else: 
        plt.show()
        if not len(data):
            np.savez(save_dir/filename, n=n, Phi=Phi, I1g=I1g, Q1g=Q1g, I2g=I2g, Q2g=Q2g, I1e=I1e, Q1e=Q1e, I2e=I2e, Q2e=Q2e)
            print("Data saved as %s.npz" %filename)
        plt.close()

    return
##################################################

# open communication with opx
qmm = QuantumMachinesManager(host=qop_ip, port=80)
print("QUA version: %s" %qmm.version())

if mode=="sim": # simulate the qua program
    job = qmm.simulate(config, qua_program, SimulationConfig(15000))
    job.get_simulated_samples().con1.plot()

if mode=="prev": # check any running previous job
    qm_list =  qmm.list_open_quantum_machines()
    qm = qmm.get_qm(qm_list[0])
    print("QM-ID: %s, Queue: %s" %(qm.id,qm.queue.count))
    job = qm.get_running_job()
    try: 
        print("JOB-ID: %s" %job.id())
        while int(input("Continue collecting data (1/0)?")):
            job = QmJob(qmm, job.id())
            data_present(False)
            fig, ax = plt.subplots(row,col)
    except Exception as e: 
        print(e)
        qm.close()
    
if mode=="load": # load data
    flist = fnmatch.filter(os.listdir(save_dir), 'cz_ops*')
    keyword = input("Enter Keyword if any: ")
    flist = list(filter(lambda x: keyword in x, flist))
    print("Saved data with keyword '%s':\n" %keyword)
    for i, f in enumerate(flist): print("%s. %s" %(i+1,f))
    f_location = int(input("enter 1-%s: " %len(flist)))
    filename = flist[f_location-1]
    data = np.load(save_dir/(filename))
    data_present(False, data)
    
if mode=="new": # new run
    qm = qmm.open_qm(config)
    job = qm.execute(qua_program)
    data_present(True)
    interrupt = int(input("Stop execution on closing figure (1/0)?"))
    if interrupt: 
        interrupt_on_close(fig, job)
    else:
        print("kill the thread to exit..")
    while job.result_handles.is_processing(): 
        data_present(True)
    if interrupt: qm.close()
        
            
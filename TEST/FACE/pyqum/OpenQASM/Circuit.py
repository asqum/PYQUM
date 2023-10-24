from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from pyqum.OpenQASM.configuration import *
from pyqum.OpenQASM.macros import multiplexed_readout, cz_gate

from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.plot import interrupt_on_close
from qualang_tools.units import unit
from oqc import *
import grpclib

import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd


cz_type = "square"
n_avg = 1024
h_loop = 1

def simple_circuit():
    with program() as cz_ops:

        I_g = [declare(fixed) for i in range(2)]
        Q_g = [declare(fixed) for i in range(2)] 
        I_st_g = [declare_stream() for i in range(2)]
        Q_st_g = [declare_stream() for i in range(2)]
        n = declare(int)
        n_st = declare_stream()
        t = declare(int)
        a = declare(fixed)
        phi = declare(fixed)

        with for_(n, 0, n < n_avg, n+1):
            save(n, n_st)
            
            wait(thermalization_time * u.ns)
            align()
            
            # Circuit 1:
            # play("x90", "q1_xy")
            # play("x90", "q2_xy")
            # align()
            # cz_gate(cz_type)
            # align()
            # play("x90", "q2_xy")
            # align()
            # cz_gate(cz_type)
            # align()
            # play("x180", "q2_xy")
            # align()
            # cz_gate(cz_type)

            # Circuit 2: Bell-state
            # play("y180", "q2_xy")
            align()

            # play("y90", "q1_xy")
            # play("x180", "q1_xy")

            # align()
            # play("y90", "q2_xy")
            # play("x180", "q2_xy")
            # align()

            # play("x180", "q1_xy")
            # play("x180", "q2_xy")
            # play("x180", "q1_xy")
            # play("x180", "q2_xy")
            # align()

            # cz_gate(cz_type)
            # frame_rotation_2pi(0.42, "q2_xy")

            # align()
            # play("y180", "q1_xy")
            # play("y180", "q2_xy")
            # play("y180", "q1_xy")
            # play("y180", "q2_xy")
            # align()

            # play("y90", "q2_xy")
            # play("x180", "q2_xy")
            # align()

            # Circuit 3: Hadamard-test
            play("y90", "q1_xy")
            play("x180", "q1_xy")
            play("y90", "q2_xy")
            play("x180", "q2_xy")
            # align()
            # play("y90", "q1_xy")
            # play("x180", "q1_xy")
            # play("y90", "q2_xy")
            # play("x180", "q2_xy")
        
        
            multiplexed_readout(I_g, I_st_g, Q_g, Q_st_g, resonators=[1, 2], weights="rotated_")
            
        with stream_processing():

            I_st_g[0].save_all(f"I_g_1")
            Q_st_g[0].save_all(f"Q_g_1")
            I_st_g[1].save_all(f"I_g_2")
            Q_st_g[1].save_all(f"Q_g_2")

    # open communication with qm-cluster:
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

    # while server in sleep mode, qmm requires 3 wake-up calls:
    wakeup_call = 0
    while (wakeup_call>=0) & (wakeup_call<10):
        try: 
            qm = qmm.open_qm(config)
            wakeup_call = -1
        except(grpclib.exceptions.StreamTerminatedError): 
            wakeup_call += 1
            print(Fore.BLUE + "WAKE-UPPPPPPPPP: %s" %wakeup_call)
            pass
    
    job = qm.execute(cz_ops)
    job.result_handles.wait_for_all_values()
    results = fetching_tool(job, ["I_g_1", "I_g_2"])
    qm.close()

    q1_states = [str(int(x)) for x in np.array(results.fetch_all()[0])>ge_threshold_q1]
    q2_states = [str(int(x)) for x in np.array(results.fetch_all()[1])>ge_threshold_q2]
    dummy_states = [str(int(x)) for x in np.zeros(n_avg)]

    print("q1-states: %s" %Counter(q1_states))
    print("q2-states: %s" %Counter(q2_states))

    bitstrings = sorted([''.join(x) for x in zip(dummy_states,dummy_states,dummy_states,       q2_states,q1_states)])
    print(Counter(bitstrings))

    return Counter(bitstrings)

# n, bins, patches = plt.hist(x=bitstrings, bins='auto', color='#0504aa', alpha=0.7, rwidth=0.85)
# plt.grid(axis='y', alpha=0.75)
# plt.xlabel('Bitstrings')
# plt.ylabel('Occurance')
# plt.title('State Population')
# plt.text(23, 45, r'$\mu=15, b=3$')
# maxfreq = n.max()
# Set a clean upper y-axis limit.
# plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
# plt.show()

# fig, ax = plt.subplots()

# print(Counter(bitstrings).keys())

# CBits = [x for x in Counter(bitstrings).keys()]
# percentage = [x/n_avg*100 for x in Counter(bitstrings).values()]
# bar_colors = ['tab:blue', 'tab:green', 'tab:orange', 'tab:red']
# ax.bar(CBits, percentage)#, color=bar_colors)
# ax.set_ylabel('Population (%)')
# ax.set_title('Quantum Circuit\'s Outcome')
# ax.legend(title='Fruit color')
# plt.show()

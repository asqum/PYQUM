from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from pyqum.OpenQASM.configuration import *
from pyqum.OpenQASM.protocols import *

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
h_loop = 1
multiplexed = [1,2,3,4,5]

# open communication with qm-cluster:
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

def simple_circuit(shots, script, qmm=qmm):
    shots = int(shots)

    script = script.split(";\n")
    print(Fore.GREEN + "QASM type: %s" %(script[0]))

    with program() as quantum_circuit:

        I_g = [declare(fixed) for i in range(len(multiplexed))]
        Q_g = [declare(fixed) for i in range(len(multiplexed))] 
        I_st_g = [declare_stream() for i in range(len(multiplexed))]
        Q_st_g = [declare_stream() for i in range(len(multiplexed))]
        n = declare(int)
        n_st = declare_stream()

        with for_(n, 0, n < shots, n+1):
            save(n, n_st)
            
            wait(thermalization_time * u.ns)
            align()
                
            for line in script[4:-1]:
                if "measure" not in line:
                    operation = line.split(" ")[0]
                    # 2q gate:
                    if "," in line:
                        control = int(line.split(" ")[1].split(",")[0].split("q[")[1].split("]")[0]) + 1
                        target = int(line.split(" ")[1].split(",")[1].split("q[")[1].split("]")[0]) + 1
                        try: eval("%s_gate(%s,%s)" %(operation,control,target))
                        except Exception as e: print(Fore.RED + "error: %s" %e)
                        print(Fore.YELLOW + "%s_gate(%s,%s)" %(operation,control,target))
                    # sq gate:
                    else:
                        qubit = int(line.split(" ")[1].split("q[")[1].split("]")[0]) + 1
                        try: eval("%s_gate(%s)" %(operation,qubit))
                        except Exception as e: print(Fore.RED + "error: %s" %e)
                        print(Fore.YELLOW + "%s_gate(%s)" %(operation,qubit))
            

            align()
            play("y90", "q4_xy")
            play("x180", "q4_xy")

            align()
            play("y90", "q5_xy")
            play("x180", "q5_xy")
            align()

            cz_gate(4, 5)
            frame_rotation_2pi(0.5, "q5_xy")

            align()
            play("y90", "q5_xy")
            play("x180", "q5_xy")

            
            align()
            multiplexed_readout(I_g, I_st_g, Q_g, Q_st_g, resonators=multiplexed, weights="rotated_")
            
        with stream_processing():
            for i in range(len(multiplexed)):
                I_st_g[i].save_all(f"I_g_{i+1}")
                Q_st_g[i].save_all(f"Q_g_{i+1}")

    
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
    
    job = qm.execute(quantum_circuit)
    job.result_handles.wait_for_all_values()
    results = fetching_tool(job, [f"I_g_{x}" for x in multiplexed])
    qm.close()

    q1_states = [str(int(x)) for x in np.array(results.fetch_all()[0])>ge_threshold_q1]
    q2_states = [str(int(x)) for x in np.array(results.fetch_all()[1])>ge_threshold_q2]
    q3_states = [str(int(x)) for x in np.array(results.fetch_all()[2])>ge_threshold_q3]
    q4_states = [str(int(x)) for x in np.array(results.fetch_all()[3])>ge_threshold_q4]
    q5_states = [str(int(x)) for x in np.array(results.fetch_all()[4])>ge_threshold_q5]
    dummy_states = [str(int(x)) for x in np.zeros(shots)]

    print("q1-states: %s" %Counter(q1_states))
    print("q2-states: %s" %Counter(q2_states))
    print("q3-states: %s" %Counter(q3_states))
    print("q4-states: %s" %Counter(q4_states))
    print("q5-states: %s" %Counter(q5_states))

    bitstrings = sorted([''.join(x) for x in zip(q5_states,q4_states,q3_states,q2_states,q1_states)])
    print(Counter(bitstrings))


    # fig, ax = plt.subplots()
    # print(Counter(bitstrings).keys())
    # CBits = [x for x in Counter(bitstrings).keys()]
    # percentage = [x/shots*100 for x in Counter(bitstrings).values()]
    # ax.bar(CBits, percentage)#, color=bar_colors)
    # ax.set_ylabel('Population (%)')
    # ax.set_title('Quantum Circuit\'s Outcome')
    # plt.show()

    return Counter(bitstrings)


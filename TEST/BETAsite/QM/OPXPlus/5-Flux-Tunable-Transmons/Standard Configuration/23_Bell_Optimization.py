from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from configuration import *

from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.plot import interrupt_on_close
from qualang_tools.units import unit
from qualang_tools.analysis import two_state_discriminator
# from oqc import *

import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd

from macros import multiplexed_readout, cz_gate, Dynamical_Decoupling

simulate = False
cz_type = "const_wf"
shots = 2048
h_loop = 1
multiplexed = [1,2,3,4,5]
bitstrings = ['00', '01', '10', '11']

qubit_to_flux_tune, qubit_to_meet_with = 1, 2
cx_control, cx_target = 1, 2  # switch order in turn to compensate both channel consecutively
th_control, th_target = eval(f"ge_threshold_q{cx_control}"), eval(f"ge_threshold_q{cx_target}")
phis_corr = np.linspace(-0.9, 0.9, 180)

with program() as cz_ops:

    I = [declare(fixed) for i in range(len(multiplexed))]
    Q = [declare(fixed) for i in range(len(multiplexed))] 
    I_st = [declare_stream() for i in range(len(multiplexed))]
    Q_st = [declare_stream() for i in range(len(multiplexed))]
    state = [declare(bool) for _ in range(len(bitstrings))]
    state_st = [declare_stream() for _ in range(len(bitstrings))]
    n = declare(int)
    n_st = declare_stream()
    a = declare(fixed)
    phi_corr = declare(fixed)
    global_phase_correction = declare(fixed, value=eval(f"cz{qubit_to_flux_tune}_{qubit_to_meet_with}_2pi_dev"))

    with for_(n, 0, n < shots, n+1):
        save(n, n_st)
        
        with for_(*from_array(phi_corr, phis_corr)):
            if not simulate: wait(thermalization_time * u.ns)

            align()
            play("y90", f"q{cx_control}_xy")
            play("-y90", f"q{cx_target}_xy")
            
            align()
            # Dynamical_Decoupling(2,2)
            cz_gate(qubit_to_meet_with, qubit_to_flux_tune, cz_type)
            # frame_rotation_2pi(global_phase_correction+phi_corr, f"q{cx_target}_xy")

            # for 3-4, 4-5 upper: FT = target
            if (qubit_to_flux_tune==4 and qubit_to_meet_with==3) or (qubit_to_flux_tune==5 and qubit_to_meet_with==4):
                frame_rotation_2pi(eval(f"cz{cx_target}_{cx_control}_2pi_dev")+phi_corr, f"q{cx_target}_xy")  # <---------
                frame_rotation_2pi(eval(f"cz{cx_control}_{cx_target}_2pi_dev")+phi_corr, f"q{cx_control}_xy") # from flux-crosstalk
            # for 1-2, 2-3 upper: FT = control
            if (qubit_to_flux_tune==1 and qubit_to_meet_with==2) or (qubit_to_flux_tune==2 and qubit_to_meet_with==3):
                frame_rotation_2pi(eval(f"cz{cx_control}_{cx_target}_2pi_dev")+phi_corr, f"q{cx_target}_xy")  # <---------
                frame_rotation_2pi(eval(f"cz{cx_target}_{cx_control}_2pi_dev")+phi_corr, f"q{cx_control}_xy") # from flux-crosstalk
            
            align()
            play("y90", f"q{cx_target}_xy") # the channel that we're calibrating

            # align()
            # play("x180"*amp(phi_corr), f"q{cx_control}_xy")
            # play("x180"*amp(phi_corr), f"q{cx_target}_xy")

            align()
            multiplexed_readout(I, I_st, Q, Q_st, resonators=multiplexed, weights="rotated_")

            assign(state[0], ((I[multiplexed.index(cx_control)]<th_control) & (I[multiplexed.index(cx_target)]<th_target)))
            assign(state[1], ((I[multiplexed.index(cx_control)]<th_control) & (I[multiplexed.index(cx_target)]>th_target)))
            assign(state[2], ((I[multiplexed.index(cx_control)]>th_control) & (I[multiplexed.index(cx_target)]<th_target)))
            assign(state[3], ((I[multiplexed.index(cx_control)]>th_control) & (I[multiplexed.index(cx_target)]>th_target)))

            for i in range(len(bitstrings)): save(state[i], state_st[i])
        
        save(n, n_st)
    with stream_processing():
        # for the progress counter
        n_st.save("n")
        for i in range(len(multiplexed)):
            I_st[i].buffer(len(phis_corr)).save_all(f"I_{i+1}")
        for i in range(len(bitstrings)):
            state_st[i].boolean_to_int().buffer(len(phis_corr)).average().save(f"state_{bitstrings[i]}")
        

# open communication with opx
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

if not simulate:
    qm = qmm.open_qm(config)
    job = qm.execute(cz_ops)
    # job.result_handles.wait_for_all_values()
    # Get results from QUA program
    results = fetching_tool(job, ["n"] + [f"state_{x}" for x in bitstrings] + [f"I_{x}" for x in multiplexed], mode="live")
    # Live plotting
    fig = plt.figure()
    interrupt_on_close(fig, job)  #  Interrupts the job when closing the figure
    while results.is_processing():
        # Fetch results
        n, state00, state01, state10, state11, I1, I2, I3, I4, I5 = results.fetch_all()
        # Progress bar
        progress_counter(n, shots, start_time=results.start_time)

        Bell_SNR = (state00+state11)/(state01+state10)

        plt.suptitle(f"Optimizing Phase compensation for CZ ({n}/{shots})")
        plt.subplot(121)
        plt.cla()
        plt.plot(phis_corr, state00, '.b', phis_corr, state11, '.r')
        plt.xlabel("Phase adjustment (2pi)")
        plt.ylabel("I quadrature [V]")
        plt.legend(("00", "11"), loc="upper right")
        plt.subplot(122)
        plt.cla()
        plt.plot(phis_corr, Bell_SNR)
        plt.xlabel("Phase adjustment (2pi)")
        plt.ylabel("Bell SNR")
        plt.title(f"The Best Phi-Adjust: {phis_corr[list(Bell_SNR).index(max(Bell_SNR))]:.3f}")

        plt.tight_layout()
        plt.pause(0.3)

    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    plt.show()
    

    collected_shots = len(I1[:,0])
    for j in [0, list(Bell_SNR).index(max(Bell_SNR)), -1]:
        q_states = [] #np.zeros((len(multiplexed),collected_shots))
        for i,x in enumerate(multiplexed): 
            q_states += [[str(int(a)) for a in np.array(eval(f"I{x}")[:,j])>eval(f"ge_threshold_q{x}")]]
            print(f"q{x}-states: %s" %Counter(q_states[i]))
        
        bitstrings = sorted([''.join(x) for x in zip(q_states[multiplexed.index(cx_target)], q_states[multiplexed.index(cx_control)])])
        print(Counter(bitstrings))

        fig, ax = plt.subplots()
        print(Counter(bitstrings).keys())
        CBits = [x for x in Counter(bitstrings).keys()]
        percentage = [x/collected_shots*100 for x in Counter(bitstrings).values()]
        ax.bar(CBits, percentage)#, color=bar_colors)
        ax.set_ylabel('Population (%)')
        ax.set_title(f'Bell/GHZ state fidelity: {(percentage[0]+percentage[-1]):.3}%')
        plt.show()

    print("=====================================")
    print(f"The Best Phi-Adjust: {phis_corr[list(Bell_SNR).index(max(Bell_SNR))]:.3f}")

    

else:
    # Simulates the QUA program for the specified duration
    simulation_config = SimulationConfig(duration=3_000)  # In clock cycles = 4ns
    # Simulate blocks python until the simulation is done
    job = qmm.simulate(config, cz_ops, simulation_config)
    # Plot the simulated samples
    job.get_simulated_samples().con1.plot()
    job.get_simulated_samples().con2.plot()
    plt.show()

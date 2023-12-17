"""
        CZ CHEVRON - 4ns granularity
The goal of this protocol is to find the parameters of the CZ gate between two flux-tunable qubits.
The protocol consists in flux tuning one qubit to bring the |11> state on resonance with |20>.
The two qubits must start in their excited states so that, when |11> and |20> are on resonance, the state |11> will
start acquiring a global phase when varying the flux pulse duration.

By scanning the flux pulse amplitude and duration, the CZ chevron can be obtained and post-processed to extract the
CZ gate parameters corresponding to a single oscillation period such that |11> pick up an overall phase of pi (flux
pulse amplitude and interation time).

This version sweeps the flux pulse duration using real-time QUA, which means that the flux pulse can be arbitrarily long
but the step must be larger than 1 clock cycle (4ns) and the minimum pulse duration is 4 clock cycles (16ns).

Prerequisites:
    - Having found the resonance frequency of the resonator coupled to the qubit under study (resonator_spectroscopy).
    - Having found the qubits maximum frequency point (qubit_spectroscopy_vs_flux).
    - Having calibrated qubit gates (x180) by running qubit spectroscopy, rabi_chevron, power_rabi, Ramsey and updated the configuration.
    - (Optional) having corrected the flux line distortions by running the Cryoscope protocol and updating the filter taps in the configuration.

Next steps before going to the next node:
    - Update the CZ gate parameters in the configuration.
"""

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from configuration import *
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
import numpy as np
from macros import qua_declaration, multiplexed_readout
import warnings
from scipy.optimize import curve_fit

warnings.filterwarnings("ignore")

from cosine import Cosine

####################
# Define variables #
####################
simulate = True

# Qubit to flux-tune to reach some distance of Ec with another qubit, Qubit to meet with:
qubit_to_flux_tune, qubit_to_meet_with = 2, 3
cz = 1

# qubit to flux-tune is target
# qubit to meet with is control 

multiplexed = [1,2,3,4,5]
points_per_cycle = 20
cz_corr = float(eval(f"cz{qubit_to_flux_tune}_{qubit_to_meet_with}_2pi_dev"))

n_avg = 100000  # The number of averages
phis = np.arange(0, 3, 1/points_per_cycle)
amps = np.linspace(0.9, 1.1, 25)
amps = np.linspace(0.95,1.05,25)
# amps = np.linspace(0.9995,1.0005,25)

###################
# The QUA program #
###################

with program() as cz_pi_cal:
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=len(multiplexed))
    phi = declare(fixed)  # QUA variable angle of the second pi/2 wrt to the first pi/2
    a = declare(fixed)  # QUA variable for the flux pulse amplitude pre-factor.
    flag = declare(bool)
    global_phase_correction = declare(fixed, value=cz_corr)

    with for_(n, 0, n < n_avg, n + 1):
        # Save the averaging iteration to get the progress bar
        save(n, n_st)

        with for_(*from_array(phi, phis)):
            with for_(*from_array(a, amps)):
                with for_each_(flag, [True, False]):
                    
                    # control qubit
                    play("x180", f"q{qubit_to_meet_with}_xy", condition=flag)
                    
                    # ramsey first pi/2
                    align()
                    play("x90", f"q{qubit_to_flux_tune}_xy")

                    # play("y180", f"q{qubit_to_flux_tune}_xy")
                    # play("y180", f"q{qubit_to_flux_tune}_xy")
                    
                    # cz
                    if cz:
                        wait(flux_settle_time * u.ns, f"q{qubit_to_flux_tune}_z")
                        align()
                        play(f"cz_{qubit_to_meet_with}c{qubit_to_flux_tune}t" * amp(a), f"q{qubit_to_flux_tune}_z")
                        # frame_rotation_2pi(global_phase_correction, f"q{qubit_to_flux_tune}_xy")
                        # frame_rotation_2pi(global_phase_correction, f"q{qubit_to_flux_tune}_xy")
                        align()
                        wait(flux_settle_time * u.ns, f"q{qubit_to_flux_tune}_z")
                    
                    # ramsey second pi/2
                    align()
                    frame_rotation_2pi(phi, f"q{qubit_to_flux_tune}_xy")
                    play("x90", f"q{qubit_to_flux_tune}_xy")
                    align()
                    
                    # Measure the state of the resonators
                    wait(4)
                    multiplexed_readout(I, I_st, Q, Q_st, resonators=multiplexed, weights="rotated_")
                    
                    # Wait for the qubit to decay to the ground state
                    if simulate: wait(7)
                    else: wait(thermalization_time * u.ns)
                    

    with stream_processing():
        # for the progress counter
        n_st.save("n")
        
        # Target:
        I_st[multiplexed.index(qubit_to_flux_tune)].buffer(len(phis), len(amps), 2).average().save("I1")
        Q_st[multiplexed.index(qubit_to_flux_tune)].buffer(len(phis), len(amps), 2).average().save("Q1")
        
        # Control:
        I_st[multiplexed.index(qubit_to_meet_with)].buffer(len(phis), len(amps), 2).average().save("I2")
        I_st[multiplexed.index(qubit_to_meet_with)].buffer(len(phis), len(amps), 2).average().save("Q2")
        

#####################################
#  Open Communication with the QOP  #
#####################################

qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

###########################
# Run or Simulate Program #
###########################

if simulate:
    # Simulates the QUA program for the specified duration
    simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
    job = qmm.simulate(config, cz_pi_cal, simulation_config)
    job.get_simulated_samples().con1.plot()
    job.get_simulated_samples().con2.plot()
    plt.show()
else:
    # Open the quantum machine
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(cz_pi_cal)
    
    
    # import time
    # time.sleep(300)
    # I1 =job.result_handles.I1.fetch_all()
    # print(f"len of amps {len(amps)}")
    # print(f"len of phis {len(phis)}")


    # fig = plt.figure()
    fig, ax = plt.subplots(len(amps)//5, 5)
    # fig2, ax2 = plt.subplots(len(amps)//5, 5)
    interrupt_on_close(fig, job)
    results = fetching_tool(job, ["n", "I1", "Q1", "I2", "Q2"], mode="live")
    # Live plotting
    while results.is_processing():
        # Fetch results
        n, I1, Q1, I2, Q2 = results.fetch_all()
        # Progress bar
        progress_counter(n, n_avg, start_time=results.start_time)
        
        plt.suptitle(f"q{qubit_to_flux_tune}->q{qubit_to_meet_with}: amp_scale, pha_diff_deg ({n}/{n_avg})")
        # CZ_sign = np.zeros([len(amps),len(phis)])
        for i in range(len(amps)):
            ax[int(i//5), int(i%5)].cla()
            
            # Fitting for phase
            I_control_g = I1[:,i,1]
            I_control_e = I1[:,i,0]
            try:
                fit = Cosine(phis, I_control_g, plot=False)
                phase_g = fit.out.get('phase')[0]
                ax[int(i//5), int(i%5)].plot(fit.x_data, fit.fit_type(fit.x, fit.popt) * fit.y_normal, '-b', alpha=0.5)
                fit = Cosine(phis, I_control_e, plot=False)
                phase_e = fit.out.get('phase')[0]
                ax[int(i//5), int(i%5)].plot(fit.x_data, fit.fit_type(fit.x, fit.popt) * fit.y_normal, '-r', alpha=0.5)
                dphase = (phase_g-phase_e)/np.pi*180     
            except Exception as e: print(e)
            ax[int(i//5), int(i%5)].plot(phis, I_control_e, '.r', phis, I_control_g, '.b')
            ax[int(i//5), int(i%5)].set_title("%.7f, %.1f" %(amps[i], dphase))
            
            # I10 = I1[:,i,0]
            # I10 /= np.max(I10)
            # I11 = I1[:,i,1]
            # I11 /= np.max(I11)
            # ax[i,1].cla()
            # ax[i,1].plot(I10)
            # ax[i,1].plot(I11)
            
            # CZ_sign[i,:] = I10 - I11
            # ax2[int(i//5), int(i%5)].cla()
            # ax2[int(i//5), int(i%5)].plot(I11, I10, '.')
            # ax2[int(i//5), int(i%5)].set_aspect('equal')
            # ax2[int(i//5), int(i%5)].set_title(f"amp scale: {amps[i]}")

        plt.tight_layout()
        plt.pause(3)
            
    plt.show()   

    # plt.plot(amps, [np.max(CZ_sign[x,:]) for x in range(len(amps))] )
    # plt.show()
    
    # def cosine_function(t, A, f, phi, C):
    #     return A * np.cos(2 * np.pi * f * (t - phi)) + C

    # for i in range(len(amps)):
    #     # Initial guess for parameters
    #     initial_guess = [np.abs(np.max(I1[:,i,0])-np.min(I1[:,i,0]))/2, 1/15, 0.0, np.mean(I1[:,i,0])]
    #     # initial_guess = [1,1,1,1]
    #     params, covariance = curve_fit(cosine_function, phis, I1[:,i,0], p0=initial_guess)
    #     print(params)
    #     plt.plot(cosine_function(phis, params[0], params[1], params[2], params[3]))
    # plt.show()
     
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    # plt.show()

    filename = f"CZ_Pi_Cal_c{qubit_to_meet_with}_t{qubit_to_flux_tune}"
    save = False
    if save:
        np.savez(save_dir/filename, I1=I1)
        print("Data saved as %s.npz" %filename)

    # np.savez(save_dir/'cz', I1=I1, Q1=Q1, I2=I2, Q2=Q2, ts=ts, amps=amps)

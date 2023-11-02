"""
        POWER RABI WITH ERROR AMPLIFICATION
This sequence involves repeatedly executing the qubit pulse (such as x180, square_pi, or similar) 'N' times and
measuring the state of the resonator across different qubit pulse amplitudes and number of pulses.
By doing so, the effect of amplitude inaccuracies is amplified, enabling a more precise measurement of the pi pulse
amplitude. The results are then analyzed to determine the qubit pulse amplitude suitable for the selected duration.

Prerequisites:
    - Having found the resonance frequency of the resonator coupled to the qubit under study (resonator_spectroscopy).
    - Having calibrated the IQ mixer connected to the qubit drive line (external mixer or Octave port)
    - Having found the rough qubit frequency and pi pulse duration (rabi_chevron_duration or time_rabi).
    - Having found the pi pulse amplitude (power_rabi).
    - Set the qubit frequency, desired pi pulse duration and rough pi pulse amplitude in the configuration.
    - Set the desired flux bias

Next steps before going to the next node:
    - Update the qubit pulse amplitude (pi_amp_q) in the configuration.
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
from macros import qua_declaration, multiplexed_readout
import warnings

warnings.filterwarnings("ignore")

###################
# The QUA program #
###################
n_avg = 100000  # The number of averages
test_qubits = [1,2,3,4,5]

# Pulse amplitude sweep (as a pre-factor of the qubit pulse amplitude) - must be within [-2; 2)
amps = np.arange(0.1, 1.9, 0.01)

# Number of applied Rabi pulses sweep
# max_nb_of_pulses = 2 # 1D-sweep
max_nb_of_pulses = 24  # 2D-sweep: Maximum number of qubit pulses
nb_of_pulses = np.arange(1, max_nb_of_pulses, 1)  # Always play an odd/even number of pulses to end up in the same state

with program() as rabi:
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=5)
    a = declare(fixed)  # QUA variable for the qubit drive amplitude pre-factor
    npi = declare(int)  # QUA variable for the number of qubit pulses
    count = declare(int)  # QUA variable for counting the qubit pulses

    with for_(n, 0, n < n_avg, n + 1):
        with for_(*from_array(npi, nb_of_pulses)):
            with for_(*from_array(a, amps)):
                # Loop for error amplification (perform many qubit pulses)
                with for_(count, 0, count < npi, count + 1):
                    if 1 in test_qubits: play("x180" * amp(a), "q1_xy")
                    if 2 in test_qubits: play("x180" * amp(a), "q2_xy")
                    if 3 in test_qubits: play("x180" * amp(a), "q3_xy")
                    if 4 in test_qubits: play("x180" * amp(a), "q4_xy")
                    if 5 in test_qubits: play("x180" * amp(a), "q5_xy")
                # Align the elements to measure after playing the qubit pulses.
                align()
                # Start using Rotated integration weights (cf. IQ_blobs.py)
                multiplexed_readout(I, I_st, Q, Q_st, resonators=[1, 2, 3, 4, 5], weights="rotated_", amplitude=1)
                # Wait for the qubit to decay to the ground state
                wait(thermalization_time * u.ns)
        # Save the averaging iteration to get the progress bar
        save(n, n_st)

    with stream_processing():
        n_st.save("n")
        # resonator 1
        I_st[0].buffer(len(amps)).buffer(len(nb_of_pulses)).average().save("I1")
        Q_st[0].buffer(len(amps)).buffer(len(nb_of_pulses)).average().save("Q1")
        # resonator 2
        I_st[1].buffer(len(amps)).buffer(len(nb_of_pulses)).average().save("I2")
        Q_st[1].buffer(len(amps)).buffer(len(nb_of_pulses)).average().save("Q2")
        # resonator 3
        I_st[2].buffer(len(amps)).buffer(len(nb_of_pulses)).average().save("I3")
        Q_st[2].buffer(len(amps)).buffer(len(nb_of_pulses)).average().save("Q3")
        # resonator 4
        I_st[3].buffer(len(amps)).buffer(len(nb_of_pulses)).average().save("I4")
        Q_st[3].buffer(len(amps)).buffer(len(nb_of_pulses)).average().save("Q4")
        # resonator 5
        I_st[4].buffer(len(amps)).buffer(len(nb_of_pulses)).average().save("I5")
        Q_st[4].buffer(len(amps)).buffer(len(nb_of_pulses)).average().save("Q5")

#####################################
#  Open Communication with the QOP  #
#####################################
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

###########################
# Run or Simulate Program #
###########################

simulate = False

if simulate:
    # Simulates the QUA program for the specified duration
    simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
    job = qmm.simulate(config, rabi, simulation_config)
    job.get_simulated_samples().con1.plot()

else:
    # Open the quantum machine
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(rabi)
    # Prepare the figure for live plotting
    fig = plt.figure()
    interrupt_on_close(fig, job)
    # Tool to easily fetch results from the OPX (results_handle used in it)
    results = fetching_tool(job, ["n", "I1", "Q1", "I2", "Q2", "I3", "Q3", "I4", "Q4", "I5", "Q5"], mode="live")
    # Live plotting
    while results.is_processing():
        # Fetch results
        n, I1, Q1, I2, Q2, I3, Q3, I4, Q4, I5, Q5 = results.fetch_all()
        # Progress bar
        progress_counter(n, n_avg, start_time=results.start_time)
        # Convert the results into Volts
        I1, Q1 = u.demod2volts(I1, readout_len), u.demod2volts(Q1, readout_len)
        I2, Q2 = u.demod2volts(I2, readout_len), u.demod2volts(Q2, readout_len)
        I3, Q3 = u.demod2volts(I3, readout_len), u.demod2volts(Q3, readout_len)
        I4, Q4 = u.demod2volts(I4, readout_len), u.demod2volts(Q4, readout_len)
        I5, Q5 = u.demod2volts(I5, readout_len), u.demod2volts(Q5, readout_len)
        # Plots
        if I1.shape[0] > 1:
            # Power Rabi with error amplification
            # q1:
            plt.subplot(2,5,1)
            plt.cla()
            plt.pcolor(amps * pi_amp_q1, nb_of_pulses, I1)
            plt.axvline(pi_amp_q1, color="k", linewidth=0.37)
            plt.title("I1")
            plt.ylabel("# of Rabi pulses")
            plt.subplot(2,5,6)
            plt.cla()
            plt.pcolor(amps * pi_amp_q1, nb_of_pulses, Q1)
            plt.title("Q1")
            plt.xlabel("qubit pulse amplitude [V]")
            plt.ylabel("# of Rabi pulses")
            # q2:
            plt.subplot(2,5,2)
            plt.cla()
            plt.pcolor(amps * pi_amp_q2, nb_of_pulses, I2)
            plt.axvline(pi_amp_q2, color="k", linewidth=0.37)
            plt.title("I2")
            plt.subplot(2,5,7)
            plt.cla()
            plt.pcolor(amps * pi_amp_q2, nb_of_pulses, Q2)
            plt.title("Q2")
            plt.xlabel("Qubit pulse amplitude [V]")
            # q3:
            plt.subplot(2,5,3)
            plt.cla()
            plt.pcolor(amps * pi_amp_q3, nb_of_pulses, I3)
            plt.axvline(pi_amp_q3, color="k", linewidth=0.37)
            plt.title("I3")
            plt.subplot(2,5,8)
            plt.cla()
            plt.pcolor(amps * pi_amp_q3, nb_of_pulses, Q3)
            plt.title("Q3")
            plt.xlabel("Qubit pulse amplitude [V]")
            # q4:
            plt.subplot(2,5,4)
            plt.cla()
            plt.pcolor(amps * pi_amp_q4, nb_of_pulses, I4)
            plt.axvline(pi_amp_q4, color="k", linewidth=0.37)
            plt.title("I4")
            plt.subplot(2,5,9)
            plt.cla()
            plt.pcolor(amps * pi_amp_q4, nb_of_pulses, Q4)
            plt.title("Q4")
            plt.xlabel("Qubit pulse amplitude [V]")
            # q5:
            plt.subplot(2,5,5)
            plt.cla()
            plt.pcolor(amps * pi_amp_q5, nb_of_pulses, I5)
            plt.axvline(pi_amp_q5, color="k", linewidth=0.37)
            plt.title("I5")
            plt.subplot(2,5,10)
            plt.cla()
            plt.pcolor(amps * pi_amp_q5, nb_of_pulses, Q5)
            plt.title("Q5")
            plt.xlabel("Qubit pulse amplitude [V]")
        else:
            # 1D power Rabi
            plt.suptitle("Power Rabi")
            # q1:
            plt.subplot(2,5,1)
            plt.cla()
            plt.plot(amps * pi_amp_q1, I1[0])
            plt.ylabel("I quadrature")
            plt.title("Qubit 1")
            plt.subplot(2,5,6)
            plt.cla()
            plt.plot(amps * pi_amp_q1, Q1[0])
            plt.ylabel("Q quadrature")
            plt.xlabel("Qubit pulse amplitude [V]")
            # q2:
            plt.subplot(2,5,2)
            plt.cla()
            plt.plot(amps * pi_amp_q2, I2[0])
            plt.title("Qubit 2")
            plt.subplot(2,5,7)
            plt.cla()
            plt.plot(amps * pi_amp_q2, Q2[0])
            plt.xlabel("Qubit pulse amplitude [V]")
            # q3:
            plt.subplot(2,5,3)
            plt.cla()
            plt.plot(amps * pi_amp_q3, I3[0])
            plt.title("Qubit 3")
            plt.subplot(2,5,8)
            plt.cla()
            plt.plot(amps * pi_amp_q3, Q3[0])
            plt.xlabel("Qubit pulse amplitude [V]")
            # q4:
            plt.subplot(2,5,4)
            plt.cla()
            plt.plot(amps * pi_amp_q4, I4[0])
            plt.title("Qubit 4")
            plt.subplot(2,5,9)
            plt.cla()
            plt.plot(amps * pi_amp_q4, Q4[0])
            plt.xlabel("Qubit pulse amplitude [V]")
            # q5:
            plt.subplot(2,5,5)
            plt.cla()
            plt.plot(amps * pi_amp_q5, I5[0])
            plt.title("Qubit 5")
            plt.subplot(2,5,10)
            plt.cla()
            plt.plot(amps * pi_amp_q5, Q5[0])
            plt.xlabel("Qubit pulse amplitude [V]")
        
        plt.tight_layout()
        plt.pause(1.0)
    
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()

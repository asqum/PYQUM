"""
        QUBIT SPECTROSCOPY
This sequence involves sending a saturation pulse to the qubit, placing it in a mixed state,
and then measuring the state of the resonator across various qubit drive intermediate dfs.
In order to facilitate the qubit search, the qubit pulse duration and amplitude can be changed manually in the QUA
program directly without having to modify the configuration.

The data is post-processed to determine the qubit resonance frequency, which can then be used to adjust
the qubit intermediate frequency in the configuration under "qubit_IF".

Note that it can happen that the qubit is excited by the image sideband or LO leakage instead of the desired sideband.
This is why calibrating the qubit mixer is highly recommended.

This step can be repeated using the "x180" operation to adjust the pulse parameters (amplitude, duration, frequency)
before performing the next calibration steps.

Prerequisites:
    - Identification of the resonator's resonance frequency when coupled to the qubit in question (referred to as "resonator_spectroscopy_multiplexed").
    - Calibration of the IQ mixer connected to the qubit drive line (whether it's an external mixer or an Octave port).
    - Set the flux bias to the maximum frequency point, labeled as "max_frequency_point", in the configuration.
    - Configuration of the cw pulse amplitude (const_amp) and duration (const_len) to transition the qubit into a mixed state.
    - Specification of the expected qubits T1 in the configuration.

Before proceeding to the next node:
    - Update the qubit frequency, labeled as "qubit_IF_q", in the configuration.
"""

from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from configuration import *
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.loops import from_array
from macros import qua_declaration, multiplexed_readout
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")


###################
# The QUA program #
###################
focus = False
n_avg = 100000  # The number of averages
qubit_num = 5
test_qubits = [3]

# Adjust the pulse duration and amplitude to drive the qubit into a mixed state
saturation_len = 20 * u.us  # In ns (should be < FFT of df)
if focus: saturation_amp = 0.0001  # pre-factor to the value defined in the config - restricted to [-2; 2)
else: saturation_amp = 0.07  # pre-factor to the value defined in the config - restricted to [-2; 2)

# Qubit detuning sweep with respect to qubit_IF
if focus:
    # 1. Hitting the spot:
    span = 0.4 * u.MHz
    df = 1 * u.kHz
else:
    # 2. Wide-scan, Find 02/2:
    span = 480 * u.MHz
    df = 480 * u.kHz
dfs = np.arange(-span, +span + 0.1, df)


with program() as multi_qubit_spec:
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=qubit_num)
    df = declare(int)  # QUA variable for the readout frequency
    
    with for_(n, 0, n < n_avg, n + 1):
        with for_(*from_array(df, dfs)):
            update_frequency("q1_xy", df + qubit_IF_q1)
            update_frequency("q2_xy", df + qubit_IF_q2)
            update_frequency("q3_xy", df + qubit_IF_q3)
            update_frequency("q4_xy", df + qubit_IF_q4)
            update_frequency("q5_xy", df + qubit_IF_q5)
            
            # Play the saturation pulse to put the qubit in a mixed state - Can adjust the amplitude on the fly [-2; 2)
            # qubit 1
            if 1 in test_qubits: play("saturation" * amp(saturation_amp), "q1_xy", duration=saturation_len * u.ns)
            align("q1_xy", "rr1")
            # qubit 2
            if 2 in test_qubits: play("saturation" * amp(saturation_amp), "q2_xy", duration=saturation_len * u.ns)
            align("q2_xy", "rr2")
            # qubit 3
            if 3 in test_qubits: play("saturation" * amp(saturation_amp), "q3_xy", duration=saturation_len * u.ns)
            align("q3_xy", "rr3")
            # qubit 4
            if 4 in test_qubits: play("saturation" * amp(saturation_amp), "q4_xy", duration=saturation_len * u.ns)
            align("q4_xy", "rr4")
            # qubit 5
            if 5 in test_qubits: play("saturation" * amp(saturation_amp), "q5_xy", duration=saturation_len * u.ns)
            align("q5_xy", "rr5")

            # Multiplexed readout, also saves the measurement outcomes
            multiplexed_readout(I, I_st, Q, Q_st, resonators=[1, 2, 3, 4, 5], amplitude=0.99)
            # Wait for the qubit to decay to the ground state
            wait(thermalization_time * u.ns)
        # Save the averaging iteration to get the progress bar
        save(n, n_st)

    with stream_processing():
        n_st.save("n")
        # resonator 1
        I_st[0].buffer(len(dfs)).average().save("I1")
        Q_st[0].buffer(len(dfs)).average().save("Q1")
        # resonator 2
        I_st[1].buffer(len(dfs)).average().save("I2")
        Q_st[1].buffer(len(dfs)).average().save("Q2")
        # resonator 3
        I_st[2].buffer(len(dfs)).average().save("I3")
        Q_st[2].buffer(len(dfs)).average().save("Q3")
        # resonator 4
        I_st[3].buffer(len(dfs)).average().save("I4")
        Q_st[3].buffer(len(dfs)).average().save("Q4")
        # resonator 5
        I_st[4].buffer(len(dfs)).average().save("I5")
        Q_st[4].buffer(len(dfs)).average().save("Q5")

#####################################
#  Open Communication with the QOP  #
#####################################
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
print("Running QUA version: %s" %(qmm.version()))

###########################
# Run or Simulate Program #
###########################

simulate = False

if simulate:
    # Simulates the QUA program for the specified duration
    simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
    job = qmm.simulate(config, multi_qubit_spec, simulation_config)
    job.get_simulated_samples().con1.plot()
    plt.show()
else:
    # Open a quantum machine to execute the QUA program
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(multi_qubit_spec)
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
        # Data analysis
        S1 = u.demod2volts(I1 + 1j * Q1, readout_len)
        S2 = u.demod2volts(I2 + 1j * Q2, readout_len)
        S3 = u.demod2volts(I3 + 1j * Q3, readout_len)
        S4 = u.demod2volts(I4 + 1j * Q4, readout_len)
        S5 = u.demod2volts(I5 + 1j * Q5, readout_len)
        R1 = np.abs(S1)
        phase1 = np.angle(S1)
        R2 = np.abs(S2)
        phase2 = np.angle(S2)
        R3 = np.abs(S3)
        phase3 = np.angle(S3)
        R4 = np.abs(S4)
        phase4 = np.angle(S4)
        R5 = np.abs(S5)
        phase5 = np.angle(S5)
        # Plots
        plt.suptitle("Qubit spectroscopy")
        # q1:
        plt.subplot(2, qubit_num, 1)
        plt.cla()
        plt.plot((dfs + qubit_IF_q1) / u.MHz, R1)
        plt.ylabel(r"$R=\sqrt{I^2 + Q^2}$ [V]")
        plt.title(f"Qubit 1 - LO = {qubit_LO_q1 / u.GHz} GHz)")
        plt.subplot(2, qubit_num, 6)
        plt.cla()
        plt.plot((dfs + qubit_IF_q1) / u.MHz, np.unwrap(phase1))
        plt.ylabel("Phase [rad]")
        plt.xlabel("Qubit intermediate frequency [MHz]")
        # q2:
        plt.subplot(2, qubit_num, 2)
        plt.cla()
        plt.plot((dfs + qubit_IF_q2) / u.MHz, np.abs(R2))
        plt.title(f"Qubit 2 - LO = {qubit_LO_q2 / u.GHz} GHz)")
        plt.subplot(2, qubit_num, 7)
        plt.cla()
        plt.plot((dfs + qubit_IF_q2) / u.MHz, np.unwrap(phase2))
        plt.xlabel("Qubit intermediate frequency [MHz]")
        # q3:
        plt.subplot(2, qubit_num, 3)
        plt.cla()
        plt.plot((dfs + qubit_IF_q3) / u.MHz, np.abs(R3))
        plt.title(f"Qubit 3 - LO = {qubit_LO_q3 / u.GHz} GHz)")
        plt.subplot(2, qubit_num, 8)
        plt.cla()
        plt.plot((dfs + qubit_IF_q3) / u.MHz, np.unwrap(phase3))
        plt.xlabel("Qubit intermediate frequency [MHz]")
        # q4:
        plt.subplot(2, qubit_num, 4)
        plt.cla()
        plt.plot((dfs + qubit_IF_q4) / u.MHz, np.abs(R4))
        plt.title(f"Qubit 4 - LO = {qubit_LO_q4 / u.GHz} GHz)")
        plt.subplot(2, qubit_num, 9)
        plt.cla()
        plt.plot((dfs + qubit_IF_q4) / u.MHz, np.unwrap(phase4))
        plt.xlabel("Qubit intermediate frequency [MHz]")
        # q5:
        plt.subplot(2, qubit_num, 5)
        plt.cla()
        plt.plot((dfs + qubit_IF_q5) / u.MHz, np.abs(R5))
        plt.title(f"Qubit 5 - LO = {qubit_LO_q5 / u.GHz} GHz)")
        plt.subplot(2, qubit_num, 10)
        plt.cla()
        plt.plot((dfs + qubit_IF_q5) / u.MHz, np.unwrap(phase5))
        plt.xlabel("Qubit intermediate frequency [MHz]")

        plt.tight_layout()
        plt.pause(0.1)

    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()

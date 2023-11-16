"""
        RESONATOR SPECTROSCOPY VERSUS READOUT AMPLITUDE
This sequence involves measuring the resonator by sending a readout pulse and demodulating the signals to
extract the 'I' and 'Q' quadratures.
This is done across various readout intermediate frequencies and amplitudes.
Based on the results, one can determine if a qubit is coupled to the resonator by noting the resonator frequency
splitting. This information can then be used to adjust the readout amplitude, choosing a readout amplitude value
just before the observed frequency splitting.

Prerequisites:
    - Calibration of the time of flight, offsets, and gains (referenced as "time_of_flight").
    - Calibration of the IQ mixer connected to the readout line (be it an external mixer or an Octave port).
    - Identification of the resonator's resonance frequency (referred to as "resonator_spectroscopy_multiplexed").
    - Configuration of the readout pulse amplitude (the pulse processor will sweep up to twice this value) and duration.
    - Specification of the expected resonator depletion time in the configuration.

Before proceeding to the next node:
    - Update the readout frequency, labeled as "resonator_IF_q", in the configuration.
    - Adjust the readout amplitude, labeled as "readout_amp_q", in the configuration.
"""

from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from configuration import *
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.loops import from_array
from macros import qua_declaration
import matplotlib.pyplot as plt
from scipy import signal
import warnings

warnings.filterwarnings("ignore")


###################
# The QUA program #
###################
qubit_num = 5
n_avg = 10000  # The number of averages
# The frequency sweep around the resonators' frequency "resonator_IF_q"
dfs = np.arange(-1.2e6, +1.2e6, 0.1e6)
# The readout amplitude sweep (as a pre-factor of the readout amplitude) - must be within [-2; 2)
amplitudes = np.arange(0.0, 1.98, 0.01)  # The amplitude vector +da/2 to add a_max to the scan

print("plotting %s X %s points" %(qubit_num,len(dfs)*len(amplitudes)))

with program() as multi_res_spec_vs_amp:
    # QUA macro to declare the measurement variables and their corresponding streams for a given number of resonators
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=qubit_num)
    df = declare(int)  # QUA variable for sweeping the readout frequency detuning around the resonance
    a = declare(fixed)  # QUA variable for sweeping the readout amplitude pre-factor

    with for_(n, 0, n < n_avg, n + 1):  # QUA for_ loop for averaging
        with for_(*from_array(df, dfs)):  # QUA for_ loop for sweeping the frequency
            update_frequency("rr1", df + resonator_IF_q1)
            update_frequency("rr2", df + resonator_IF_q2)
            update_frequency("rr3", df + resonator_IF_q3)
            update_frequency("rr4", df + resonator_IF_q4)
            update_frequency("rr5", df + resonator_IF_q5)

            with for_(*from_array(a, amplitudes)):  # QUA for_ loop for sweeping the readout amplitude
                # resonator 1
                wait(depletion_time * u.ns, "rr1")  # wait for the resonator to relax
                measure(
                    "readout" * amp(a),
                    "rr1",
                    None,
                    dual_demod.full("cos", "out1", "sin", "out2", I[0]),
                    dual_demod.full("minus_sin", "out1", "cos", "out2", Q[0]),
                )
                # Save the 'I' & 'Q' quadratures for rr1 to their respective streams
                save(I[0], I_st[0])
                save(Q[0], Q_st[0])

                # align("rr1", "rr2")  # Uncomment to measure sequentially
                # resonator 2
                wait(depletion_time * u.ns, "rr2")  # wait for the resonator to relax
                measure(
                    "readout" * amp(a),
                    "rr2",
                    None,
                    dual_demod.full("cos", "out1", "sin", "out2", I[1]),
                    dual_demod.full("minus_sin", "out1", "cos", "out2", Q[1]),
                )
                # Save the 'I' & 'Q' quadratures for rr2 to their respective streams
                save(I[1], I_st[1])
                save(Q[1], Q_st[1])

                # align("rr2, "rr3")  # Uncomment to measure sequentially
                # resonator 3
                wait(depletion_time * u.ns, "rr3")  # wait for the resonator to relax
                measure(
                    "readout" * amp(a),
                    "rr3",
                    None,
                    dual_demod.full("cos", "out1", "sin", "out2", I[2]),
                    dual_demod.full("minus_sin", "out1", "cos", "out2", Q[2]),
                )
                # Save the 'I' & 'Q' quadratures for rr2 to their respective streams
                save(I[2], I_st[2])
                save(Q[2], Q_st[2])

                # align("rr3, "rr4")  # Uncomment to measure sequentially
                # resonator 4
                wait(depletion_time * u.ns, "rr4")  # wait for the resonator to relax
                measure(
                    "readout" * amp(a),
                    "rr4",
                    None,
                    dual_demod.full("cos", "out1", "sin", "out2", I[3]),
                    dual_demod.full("minus_sin", "out1", "cos", "out2", Q[3]),
                )
                # Save the 'I' & 'Q' quadratures for rr2 to their respective streams
                save(I[3], I_st[3])
                save(Q[3], Q_st[3])

                # align("rr4, "rr5")  # Uncomment to measure sequentially
                # resonator 5
                wait(depletion_time * u.ns, "rr5")  # wait for the resonator to relax
                measure(
                    "readout" * amp(a),
                    "rr5",
                    None,
                    dual_demod.full("cos", "out1", "sin", "out2", I[4]),
                    dual_demod.full("minus_sin", "out1", "cos", "out2", Q[4]),
                )
                # Save the 'I' & 'Q' quadratures for rr2 to their respective streams
                save(I[4], I_st[4])
                save(Q[4], Q_st[4])

        # Save the averaging iteration to get the progress bar
        save(n, n_st)

    with stream_processing():
        n_st.save("n")
        # Cast the data into a 2D matrix, average the 2D matrices together and store the results on the OPX processor
        # NOTE that the buffering goes from the most inner loop (left) to the most outer one (right)
        # resonator 1
        I_st[0].buffer(len(amplitudes)).buffer(len(dfs)).average().save("I1")
        Q_st[0].buffer(len(amplitudes)).buffer(len(dfs)).average().save("Q1")
        # resonator 2
        I_st[1].buffer(len(amplitudes)).buffer(len(dfs)).average().save("I2")
        Q_st[1].buffer(len(amplitudes)).buffer(len(dfs)).average().save("Q2")
        # resonator 3
        I_st[2].buffer(len(amplitudes)).buffer(len(dfs)).average().save("I3")
        Q_st[2].buffer(len(amplitudes)).buffer(len(dfs)).average().save("Q3")
        # resonator 4
        I_st[3].buffer(len(amplitudes)).buffer(len(dfs)).average().save("I4")
        Q_st[3].buffer(len(amplitudes)).buffer(len(dfs)).average().save("Q4")
        # resonator 5
        I_st[4].buffer(len(amplitudes)).buffer(len(dfs)).average().save("I5")
        Q_st[4].buffer(len(amplitudes)).buffer(len(dfs)).average().save("Q5")

#####################################
#  Open Communication with the QOP  #
#####################################
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
print("Running QUA version: %s" %(qmm.version()))

#######################
# Simulate or execute #
#######################
simulate = False

if simulate:
    # Simulates the QUA program for the specified duration
    simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
    job = qmm.simulate(config, multi_res_spec_vs_amp, simulation_config)
    job.get_simulated_samples().con1.plot()

else:
    # Open a quantum machine to execute the QUA program
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(multi_res_spec_vs_amp)
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
        # Normalize data
        row_sums = R1.sum(axis=0)
        R1 /= row_sums[np.newaxis, :]
        row_sums = R2.sum(axis=0)
        R2 /= row_sums[np.newaxis, :]
        row_sums = R3.sum(axis=0)
        R3 /= row_sums[np.newaxis, :]
        row_sums = R4.sum(axis=0)
        R4 /= row_sums[np.newaxis, :]
        row_sums = R5.sum(axis=0)
        R5 /= row_sums[np.newaxis, :]
        # Plot
        plt.suptitle("Power dep. Resonator spectroscopy (%s/%s)" %(n,n_avg))
        # rr1:
        plt.subplot(2, qubit_num, 1)
        plt.cla()
        plt.pcolor(amplitudes, (dfs + resonator_IF_q1) / u.MHz, R1)
        plt.ylabel("Readout IF [MHz]")
        plt.title(f"Resonator 1 - LO: {resonator_LO / u.GHz} GHz")
        plt.axhline(resonator_IF_q1 / u.MHz, color="k", linewidth=0.37)
        plt.axvline(1, color="k", linewidth=0.37)
        plt.subplot(2, qubit_num, 6)
        plt.cla()
        plt.pcolor(amplitudes, (dfs + resonator_IF_q1) / u.MHz, signal.detrend(np.unwrap(phase1)))
        plt.xlabel("Readout amplitude [%sV]" %readout_amp_q1)
        plt.ylabel("Readout IF [MHz]")
        plt.axhline(resonator_IF_q1 / u.MHz, color="k", linewidth=0.37)
        # rr2:
        plt.subplot(2, qubit_num, 2)
        plt.cla()
        plt.pcolor(amplitudes, (dfs + resonator_IF_q2) / u.MHz, R2)
        plt.title(f"Resonator 2 - LO: {resonator_LO / u.GHz} GHz")
        plt.axhline(resonator_IF_q2 / u.MHz, color="k", linewidth=0.37)
        plt.axvline(1, color="k", linewidth=0.37)
        plt.subplot(2, qubit_num, 7)
        plt.cla()
        plt.pcolor(amplitudes, (dfs + resonator_IF_q2) / u.MHz, signal.detrend(np.unwrap(phase2)))
        plt.xlabel("Readout amplitude [%sV]" %readout_amp_q2)
        plt.axhline(resonator_IF_q2 / u.MHz, color="k", linewidth=0.37)
        # rr3:
        plt.subplot(2, qubit_num, 3)
        plt.cla()
        plt.pcolor(amplitudes, (dfs + resonator_IF_q3) / u.MHz, R3)
        plt.title(f"Resonator 3 - LO: {resonator_LO / u.GHz} GHz")
        plt.axhline(resonator_IF_q3 / u.MHz, color="k", linewidth=0.37)
        plt.axvline(1, color="k", linewidth=0.37)
        plt.subplot(2, qubit_num, 8)
        plt.cla()
        plt.pcolor(amplitudes, (dfs + resonator_IF_q3) / u.MHz, signal.detrend(np.unwrap(phase3)))
        plt.xlabel("Readout amplitude [%sV]" %readout_amp_q3)
        plt.axhline(resonator_IF_q3 / u.MHz, color="k", linewidth=0.37)
        # rr4:
        plt.subplot(2, qubit_num, 4)
        plt.cla()
        plt.pcolor(amplitudes, (dfs + resonator_IF_q4) / u.MHz, R4)
        plt.title(f"Resonator 4 - LO: {resonator_LO / u.GHz} GHz")
        plt.axhline(resonator_IF_q4 / u.MHz, color="k", linewidth=0.37)
        plt.axvline(1, color="k", linewidth=0.37)
        plt.subplot(2, qubit_num, 9)
        plt.cla()
        plt.pcolor(amplitudes, (dfs + resonator_IF_q4) / u.MHz, signal.detrend(np.unwrap(phase4)))
        plt.xlabel("Readout amplitude [%sV]" %readout_amp_q4)
        plt.axhline(resonator_IF_q4 / u.MHz, color="k", linewidth=0.37)
        # rr5:
        plt.subplot(2, qubit_num, 5)
        plt.cla()
        plt.pcolor(amplitudes, (dfs + resonator_IF_q5) / u.MHz, R5)
        plt.title(f"Resonator 5 - LO: {resonator_LO / u.GHz} GHz")
        plt.axhline(resonator_IF_q5 / u.MHz, color="k", linewidth=0.37)
        plt.axvline(1, color="k", linewidth=0.37)
        plt.subplot(2, qubit_num, 10)
        plt.cla()
        plt.pcolor(amplitudes, (dfs + resonator_IF_q5) / u.MHz, signal.detrend(np.unwrap(phase5)))
        plt.xlabel("Readout amplitude [%sV]" %readout_amp_q5)
        plt.axhline(resonator_IF_q5 / u.MHz, color="k", linewidth=0.37)

        plt.tight_layout()
        plt.show()
        plt.pause(0.1)

    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    
    
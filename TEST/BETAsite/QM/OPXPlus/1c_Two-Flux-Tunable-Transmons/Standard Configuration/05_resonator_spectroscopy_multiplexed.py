"""
        RESONATOR SPECTROSCOPY MULTIPLEXED
This sequence involves measuring the resonator by sending a readout pulse and demodulating the signals to extract the
'I' and 'Q' quadratures across varying readout intermediate frequencies for the two resonators simultaneously.
The data is then post-processed to determine the resonators' resonance frequency.
This frequency can be used to update the readout intermediate frequency in the configuration.

Prerequisites:
    - Ensure calibration of the time of flight, offsets, and gains (referenced as "time_of_flight").
    - Calibrate the IQ mixer connected to the readout line (whether it's an external mixer or an Octave port).
    - Having found each resonator resonant frequency and updated the configuration (resonator_spectroscopy).
    - Specify the expected resonator depletion time in the configuration.

Before proceeding to the next node:
    - Update the readout frequency, labeled as "resonator_IF_q1" and "resonator_IF_q2", in the configuration.
"""

from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from configuration import *
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.loops import from_array
import matplotlib.pyplot as plt
from scipy import signal
import warnings

warnings.filterwarnings("ignore")

###################
# The QUA program #
###################
qubit_num = 3
n_avg = 2000  # The number of averages
# The frequency sweep parameters (for both resonators)
span = 3 * u.MHz  # the span around the resonant frequencies
step = 100 * u.kHz
dfs = np.arange(-span, span, step)

with program() as multi_res_spec:
    n = declare(int)  # QUA variable for the averaging loop
    df = declare(int)  # QUA variable for the readout frequency detuning around the resonance
    n_st = declare_stream()  # Stream for the averaging iteration 'n'
    # Here we define one 'I', 'Q', 'I_st' & 'Q_st' for each resonator via a python list
    I = [declare(fixed) for _ in range(qubit_num)]
    Q = [declare(fixed) for _ in range(qubit_num)]
    I_st = [declare_stream() for _ in range(qubit_num)]
    Q_st = [declare_stream() for _ in range(qubit_num)]

    with for_(n, 0, n < n_avg, n + 1):  # QUA for_ loop for averaging
        with for_(*from_array(df, dfs)):  # QUA for_ loop for sweeping the frequency
            # wait for the resonators to deplete
            wait(depletion_time * u.ns, "rr1", "rr2")

            # resonator 1
            update_frequency("rr1", df + resonator_IF_q1)
            # Measure the resonator (send a readout pulse and demodulate the signals to get the 'I' & 'Q' quadratures)
            measure(
                "readout",
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
            update_frequency("rr2", df + resonator_IF_q2)
            measure(
                "readout",
                "rr2",
                None,
                dual_demod.full("cos", "out1", "sin", "out2", I[1]),
                dual_demod.full("minus_sin", "out1", "cos", "out2", Q[1]),
            )
            # Save the 'I' & 'Q' quadratures for rr2 to their respective streams
            save(I[1], I_st[1])
            save(Q[1], Q_st[1])

            # align("rr2", "rr3")  # Uncomment to measure sequentially
            # resonator 3
            update_frequency("rr3", df + resonator_IF_q3)
            measure(
                "readout",
                "rr3",
                None,
                dual_demod.full("cos", "out1", "sin", "out2", I[2]),
                dual_demod.full("minus_sin", "out1", "cos", "out2", Q[2]),
            )
            # Save the 'I' & 'Q' quadratures for rr2 to their respective streams
            save(I[2], I_st[2])
            save(Q[2], Q_st[2])

        # Save the averaging iteration to get the progress bar
        save(n, n_st)

    with stream_processing():
        n_st.save("iteration")
        # resonator 1
        I_st[0].buffer(len(dfs)).average().save("I1")
        Q_st[0].buffer(len(dfs)).average().save("Q1")

        # resonator 2
        I_st[1].buffer(len(dfs)).average().save("I2")
        Q_st[1].buffer(len(dfs)).average().save("Q2")

        # resonator 2
        I_st[2].buffer(len(dfs)).average().save("I3")
        Q_st[2].buffer(len(dfs)).average().save("Q3")

#####################################
#  Open Communication with the QOP  #
#####################################
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

#######################
# Simulate or execute #
#######################
simulate = False

if simulate:
    # Simulates the QUA program for the specified duration
    simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
    job = qmm.simulate(config, multi_res_spec, simulation_config)
    job.get_simulated_samples().con1.plot()

else:
    # Open a quantum machine to execute the QUA program
    qm = qmm.open_qm(config)
    # Execute the QUA program
    job = qm.execute(multi_res_spec)
    # Tool to easily fetch results from the OPX (results_handle used in it)
    results = fetching_tool(job, ["I1", "Q1", "I2", "Q2", "I3", "Q3", "iteration"], mode="live")
    # Live plotting
    fig = plt.figure()
    interrupt_on_close(fig, job)  # Interrupts the job when closing the figure
    while results.is_processing():
        # Fetch results
        I1, Q1, I2, Q2, I3, Q3, iteration = results.fetch_all()
        # Progress bar
        progress_counter(iteration, n_avg, start_time=results.get_start_time())
        # Data analysis
        S1 = u.demod2volts(I1 + 1j * Q1, readout_len)
        S2 = u.demod2volts(I2 + 1j * Q2, readout_len)
        S3 = u.demod2volts(I3 + 1j * Q3, readout_len)
        R1 = np.abs(S1)
        phase1 = np.angle(S1)
        R2 = np.abs(S2)
        phase2 = np.angle(S2)
        R3 = np.abs(S3)
        phase3 = np.angle(S3)
        # Plot
        plt.suptitle("Multiplexed resonator spectroscopy")

        plt.subplot(200 + qubit_num*10 + 1)
        plt.cla()
        plt.plot((resonator_IF_q1 + dfs) / u.MHz, R1)
        plt.title(f"Resonator 1 - LO: {resonator_LO / u.GHz} GHz")
        plt.ylabel(r"R=$\sqrt{I^2 + Q^2}$ [V]")
        plt.subplot(200 + qubit_num*10 + 2)
        plt.cla()
        plt.plot((resonator_IF_q2 + dfs) / u.MHz, R2)
        plt.title(f"Resonator 2 - LO: {resonator_LO / u.GHz} GHz")
        plt.subplot(200 + qubit_num*10 + 3)
        plt.cla()
        plt.plot((resonator_IF_q3 + dfs) / u.MHz, R3)
        plt.title(f"Resonator 3 - LO: {resonator_LO / u.GHz} GHz")

        plt.subplot(200 + qubit_num*10 + 4)
        plt.cla()
        plt.plot((resonator_IF_q1 + dfs) / u.MHz, signal.detrend(np.unwrap(phase1)))
        plt.xlabel("Readout IF [MHz]")
        plt.ylabel("Phase [rad]")
        plt.subplot(200 + qubit_num*10 + 5)
        plt.cla()
        plt.plot((resonator_IF_q2 + dfs) / u.MHz, signal.detrend(np.unwrap(phase2)))
        plt.xlabel("Readout IF [MHz]")
        plt.subplot(200 + qubit_num*10 + 6)
        plt.cla()
        plt.plot((resonator_IF_q3 + dfs) / u.MHz, signal.detrend(np.unwrap(phase3)))
        plt.xlabel("Readout IF [MHz]")
        
        plt.tight_layout()
        plt.show()
        plt.pause(0.1)

    try:
        from qualang_tools.plot.fitting import Fit

        fit = Fit()
        plt.figure()
        plt.suptitle("Fitting resonator spectroscopy")
        
        plt.subplot(131)
        fit.reflection_resonator_spectroscopy((resonator_IF_q1 + dfs) / u.MHz, R1, plot=True)
        plt.xlabel("rr1 IF [MHz]")
        plt.ylabel("Amplitude [V]")
        plt.subplot(132)
        fit.reflection_resonator_spectroscopy((resonator_IF_q2 + dfs) / u.MHz, R2, plot=True)
        plt.xlabel("rr2 IF [MHz]")
        plt.subplot(133)
        fit.reflection_resonator_spectroscopy((resonator_IF_q3 + dfs) / u.MHz, R3, plot=True)
        plt.xlabel("rr3 IF [MHz]")

        plt.tight_layout()
        plt.show()
    except (Exception,):
        pass
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()

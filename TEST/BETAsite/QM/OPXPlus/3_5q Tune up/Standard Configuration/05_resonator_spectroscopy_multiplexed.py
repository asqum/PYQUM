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
qubit_num = 5
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
            wait(depletion_time * u.ns, ["rr%s"%(i+1) for i in range(qubit_num)])

            sequential = False # to measure sequentially
            for i in range(qubit_num):
                update_frequency("rr%s"%(i+1), df + resonator_IF[i])
                measure("readout", "rr%s"%(i+1), None,
                    dual_demod.full("cos", "out1", "sin", "out2", I[i]),
                    dual_demod.full("minus_sin", "out1", "cos", "out2", Q[i]),
                )
                save(I[i], I_st[i])
                save(Q[i], Q_st[i])
                if sequential and i<qubit_num-1: align("rr%s"%(i+1), "rr%s"%(i+2))

        save(n, n_st) # Save the averaging iteration to get the progress bar

    with stream_processing():
        n_st.save("iteration")
        for i in range(qubit_num):
            I_st[i].buffer(len(dfs)).average().save("I%s" %(i+1))
            Q_st[i].buffer(len(dfs)).average().save("Q%s" %(i+1))

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
    I_list, Q_list = ["I%s"%(i+1) for i in range(qubit_num)], ["Q%s"%(i+1) for i in range(qubit_num)]
    results = fetching_tool(job, I_list + Q_list + ["iteration"], mode="live")
    # Live plotting
    fig = plt.figure()
    interrupt_on_close(fig, job)  # Interrupts the job when closing the figure
    while results.is_processing():
        # Fetch results
        all_results = results.fetch_all()
        iteration = all_results[-1]
        I, Q = all_results[0:qubit_num], all_results[qubit_num:qubit_num*2]
        # Progress bar
        progress_counter(iteration, n_avg, start_time=results.get_start_time())
        plt.suptitle("Multiplexed resonator spectroscopy")
        R = np.zeros((qubit_num, len(dfs)))
        for i in range(qubit_num):
            # Data analysis
            S = u.demod2volts(I[i] + 1j * Q[i], readout_len)
            R[i] = np.abs(S)
            phase = np.angle(S)
            # Plot R:
            plt.subplot(2, qubit_num, i+1)
            plt.cla()
            plt.plot((resonator_IF[i] + dfs) / u.MHz, R[i])
            plt.title("Resonator %s - LO: %s GHz" %(i+1, resonator_LO / u.GHz))
            if i ==0: plt.ylabel(r"R=$\sqrt{I^2 + Q^2}$ [V]")
            # Plot phase:
            plt.subplot(2, qubit_num, qubit_num+i+1)
            plt.cla()
            plt.plot((resonator_IF[i] + dfs) / u.MHz, signal.detrend(np.unwrap(phase)))
            plt.xlabel("Readout IF [MHz]")
            if i==0: plt.ylabel("Phase [rad]")
        
        plt.tight_layout()
        plt.show()
        plt.pause(0.1)

    try:
        from qualang_tools.plot.fitting import Fit

        fit = Fit()
        plt.figure()
        plt.suptitle("Fitting resonator spectroscopy")
        
        for i in range(qubit_num):
            plt.subplot(int(np.ceil(qubit_num/3))*100 + (3)*10 + i+1)
            fit.reflection_resonator_spectroscopy((resonator_IF[i] + dfs) / u.MHz, R[i], plot=True)
            plt.xlabel("rr%s IF [MHz]" %(i+1))
            if i%3==0: plt.ylabel("Amplitude [V]")
        
        plt.tight_layout(pad=1, h_pad=0, w_pad=0)
        plt.show()
    except (Exception,):
        pass
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()

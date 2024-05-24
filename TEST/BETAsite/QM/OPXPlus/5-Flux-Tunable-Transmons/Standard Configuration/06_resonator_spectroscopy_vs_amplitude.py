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
from macros import qua_declaration, multiplexed_readout, live_plotting, serialize
import matplotlib.pyplot as plt
from scipy import signal
import warnings

warnings.filterwarnings("ignore")


###################
# The QUA program #
###################
test_qubit = [1,2,3,4,5]
n_avg = 13700 #6400  # The number of averages (NOTE: max allocation per core ~ 152832000 ~ 4GBit?)
# The frequency sweep around the resonators' frequency "resonator_IF_q"
dfs = np.arange(-4e6, +4e6, 0.2e6)
# The readout amplitude sweep (as a pre-factor of the readout amplitude) - must be within [-2; 2)
amplitudes = np.arange(0.0, 1.99, 0.01)  # The amplitude vector +da/2 to add a_max to the scan

print("plotting %s X %s X %s = %s allocation" %(n_avg, len(test_qubit), len(dfs)*len(amplitudes), n_avg*len(test_qubit)*len(dfs)*len(amplitudes)))

with program() as multi_res_spec_vs_amp:
    # QUA macro to declare the measurement variables and their corresponding streams for a given number of resonators
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=len(test_qubit))
    df = declare(int)  # QUA variable for sweeping the readout frequency detuning around the resonance
    a = declare(fixed)  # QUA variable for sweeping the readout amplitude pre-factor

    with for_(n, 0, n < n_avg, n + 1):  # QUA for_ loop for averaging
        with for_(*from_array(df, dfs)):  # QUA for_ loop for sweeping the frequency
            for q in test_qubit: 
                update_frequency("rr%s"%q, df + eval("resonator_IF_q%s"%q))

            with for_(*from_array(a, amplitudes)):  # QUA for_ loop for sweeping the readout amplitude
                # Macro to perform multiplexed readout on the specified resonators
                # It also save the 'I' and 'Q' quadratures into their respective streams
                multiplexed_readout(I, I_st, Q, Q_st, resonators=test_qubit, weights="rotated_", amplitude=a)
                # wait for the resonators to relax
                # wait(depletion_time * u.ns, "rr1", "rr2", "rr3", "rr4", "rr5")
                wait(depletion_time * u.ns)
                # wait(1000)

        # Save the averaging iteration to get the progress bar
        save(n, n_st)

    with stream_processing():
        n_st.save("n")
        # Cast the data into a 2D matrix, average the 2D matrices together and store the results on the OPX processor
        # NOTE that the buffering goes from the most inner loop (left) to the most outer one (right)
        for i in range(len(test_qubit)):
            I_st[i].buffer(len(amplitudes)).buffer(len(dfs)).average().save("I%s"%(test_qubit[i]))
            Q_st[i].buffer(len(amplitudes)).buffer(len(dfs)).average().save("Q%s"%(test_qubit[i]))

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

    q_id = [x-1 for x in test_qubit]
    live_plotting(n_avg, q_id, job, amplitudes, dfs, "Power dep. Resonator spectroscopy", False, "~", stage="6a")

    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    print(job.execution_report())
    qm.close()
    
    
serialize(multi_res_spec_vs_amp, config, "respect_amplitude")
    
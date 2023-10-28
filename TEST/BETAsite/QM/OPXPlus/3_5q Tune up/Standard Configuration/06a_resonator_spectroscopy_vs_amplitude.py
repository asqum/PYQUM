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
from qualang_tools.loops import from_array
from macros import qua_declaration, live_plotting
import warnings

warnings.filterwarnings("ignore")

###################
#   Data Saving   #
###################
from datetime import datetime
import sys

save_data = True  # Default = False in configuration file
save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
save_time = str(datetime.now().strftime("%Y%m%d-%H%M%S"))
save_path = f"{save_dir}\{save_time}_{save_progam_name}"


###################
# The QUA program #
###################
q_id = [0,1,2,3,4]
n_avg = 1000  # The number of averages
# The frequency sweep around the resonators' frequency "resonator_IF_q"
span = 5 * u.MHz
df = 100 * u.kHz
dfs = np.arange(-span, +span + 0.1, df)
# The readout amplitude sweep (as a pre-factor of the readout amplitude) - must be within [-2; 2)
a_min = 0.01
a_max = 1.99
da = 0.01
amplitudes = np.arange(a_min, a_max + da / 2, da)  # The amplitude vector +da/2 to add a_max to the scan

with program() as multi_res_spec_vs_amp:
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=len(q_id))
    df = declare(int)
    a = declare(fixed)

    with for_(n, 0, n < n_avg, n + 1):
        with for_(*from_array(df, dfs)):
            for i in q_id:
                update_frequency("rr%s"%(i+1), df + resonator_IF[i])
            
            with for_(*from_array(a, amplitudes)):
                wait(depletion_time * u.ns, ["rr%s"%(i+1) for i in q_id])
                sequential = False # to measure sequentially
                for i in q_id:
                    measure(
                        "readout" * amp(a),
                        "rr%s"%(i+1),
                        None,
                        dual_demod.full("cos", "out1", "sin", "out2", I[q_id.index(i)]),
                        dual_demod.full("minus_sin", "out1", "cos", "out2", Q[q_id.index(i)]),
                    )
                    save(I[q_id.index(i)], I_st[q_id.index(i)])
                    save(Q[q_id.index(i)], Q_st[q_id.index(i)])
                    if sequential and i!=q_id[-1]: align("rr%s"%(i+1), "rr%s"%(i+2))
                
        save(n, n_st)

    with stream_processing():
        n_st.save("n")
        # Cast the data into a 2D matrix, average the 2D matrices together and store the results on the OPX processor
        # NOTE that the buffering goes from the most inner loop (left) to the most outer one (right)
        for i in q_id:
            I_st[q_id.index(i)].buffer(len(amplitudes)).buffer(len(dfs)).average().save("I%s"%(i+1))
            Q_st[q_id.index(i)].buffer(len(amplitudes)).buffer(len(dfs)).average().save("Q%s"%(i+1))
        
#####################################
#  Open Communication with the QOP  #
#####################################
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

#######################
# Simulate or execute #
#######################
simulate = False

if simulate:
    simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
    job = qmm.simulate(config, multi_res_spec_vs_amp, simulation_config)
    job.get_simulated_samples().con1.plot()

else:
    qm = qmm.open_qm(config)
    job = qm.execute(multi_res_spec_vs_amp)
    
    live_plotting(n_avg, q_id, job, amplitudes, dfs, "Power dep. Resonator spectroscopy", save_data, save_path, stage="6a")

    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
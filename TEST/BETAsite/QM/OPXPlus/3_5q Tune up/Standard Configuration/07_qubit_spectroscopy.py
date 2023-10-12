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
from qualang_tools.loops import from_array
from macros import qua_declaration, multiplexed_readout, live_plotting
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")


###################
# The QUA program #
###################
q_id = [1,2]
focus = False
n_avg = 100000  # The number of averages

# Adjust the pulse duration and amplitude to drive the qubit into a mixed state
saturation_len = 20 * u.us  # In ns (should be < FFT of df)
if focus: saturation_amp = 0.0007  # pre-factor to the value defined in the config - restricted to [-2; 2)
else: saturation_amp = 0.15  # pre-factor to the value defined in the config - restricted to [-2; 2)

# Qubit detuning sweep with respect to qubit_IF
if focus:
    # 1. Hitting the spot:
    span = 0.4 * u.MHz
    df = 1 * u.kHz
else:
    # 2. Wide-scan, Find 02/2:
    span = 490 * u.MHz
    df = 300 * u.kHz
dfs = np.arange(-span, +span + 0.1, df)


with program() as multi_qubit_spec:
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=len(q_id))
    df = declare(int)  # QUA variable for the readout frequency

    with for_(n, 0, n < n_avg, n + 1):
        with for_(*from_array(df, dfs)):
            for i in q_id:
                update_frequency("q%s_xy"%(i+1), df + qubit_IF[i])
            for i in q_id:
                if i==2: play("saturation" * amp(saturation_amp), "q%s_xy"%(i+1), duration=saturation_len * u.ns)  
                align("q%s_xy"%(i+1), "rr%s"%(i+1))
            multiplexed_readout(I, I_st, Q, Q_st, resonators=[x+1 for x in q_id], amplitude=0.99)
            wait(thermalization_time * u.ns)
        save(n, n_st)

    with stream_processing():
        n_st.save("n")
        for i in q_id:
            I_st[q_id.index(i)].buffer(len(dfs)).average().save("I%s"%(i+1))
            Q_st[q_id.index(i)].buffer(len(dfs)).average().save("Q%s"%(i+1))
        

#####################################
#  Open Communication with the QOP  #
#####################################
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

###########################
# Run or Simulate Program #
###########################

simulate = False

if simulate:
    simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
    job = qmm.simulate(config, multi_qubit_spec, simulation_config)
    job.get_simulated_samples().con1.plot()
    plt.show()
else:
    qm = qmm.open_qm(config)
    job = qm.execute(multi_qubit_spec)

    live_plotting(n_avg, q_id, job, dfs, [], 
                     "Qubit spectroscopy", stage="7", normalize=False, dimension=1)

    qm.close()

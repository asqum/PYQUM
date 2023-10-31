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
from QM_macros_jacky import multiRO_declare, multiRO_measurement, multiRO_pre_save
import warnings

warnings.filterwarnings("ignore")

###################
#   Data Saving   #
###################
from datetime import datetime
import sys


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
def mRO_power_dep_resonator( ro_element, freq_IF, amp_ratio, qmm:QuantumMachinesManager):
    """
    frequency shape (M)
    N is RO multiplex channel number
    M is frequency array number
    """
    ro_channel_num = len(ro_element)
    freq_len = np.arange(freq_IF.shape[-1])
    amp_ratio_len = amp_ratio.shape[-1]
    with program() as multi_res_spec_vs_amp:
        
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)
        n_st = declare_stream()
        idx_f = declare(int)
        a = declare(fixed)

        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(a, amplitudes)):
                with for_(*from_array(idx_f, freq_len)):
                    mRO_freq_IF = []
                    for i in range(ro_channel_num):
                        mRO_freq_IF.append(freq_IF[i][idx_f])    

                    multiRO_measurement( iqdata_stream, ro_element, mRO_freq_IF )

                    wait(depletion_time * u.ns, ["rr%s"%(i+1) for i in q_id])

            save(n, n_st)

        with stream_processing():
            n_st.save("n")
            # Cast the data into a 2D matrix, average the 2D matrices together and store the results on the OPX processor
            # NOTE that the buffering goes from the most inner loop (left) to the most outer one (right)
            multiRO_pre_save( iqdata_stream, ro_element, [freq_len, amp_ratio_len])
    #######################
    # Simulate or execute #
    #######################

    qm = qmm.open_qm(config)
    job = qm.execute(multi_res_spec_vs_amp) 

    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
"""
        QUBIT SPECTROSCOPY VERSUS FLUX
This sequence involves doing a qubit spectroscopy for several flux biases in order to exhibit the qubit frequency
versus flux response.

Prerequisites:
    - Identification of the resonator's resonance frequency when coupled to the qubit in question (referred to as "resonator_spectroscopy").
    - Calibration of the IQ mixer connected to the qubit drive line (whether it's an external mixer or an Octave port).
    - Having calibrated the resonator frequency versus flux fit parameters (amplitude_fit, frequency_fit, phase_fit, offset_fit) in the configuration
    - Identification of the approximate qubit frequency ("qubit_spectroscopy").

Before proceeding to the next node:
    - Update the qubit frequency, labeled as "qubit_IF_q", in the configuration.
    - Update the relevant flux points in the configuration.
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


# Get the resonator frequency vs flux trend from the node 05_resonator_spec_vs_flux.py in order to always measure on
# resonance while sweeping the flux
def cosine_func(x, amplitude, frequency, phase, offset):
    return amplitude * np.cos(2 * np.pi * frequency * x + phase) + offset


###################
# The QUA program #
###################
n_avg = 20000  # The number of averages
qubit_pair = [1,5]
q1_xy, q1_z, q1_IF, q1_LO = "q%s_xy"%(qubit_pair[0]), "q%s_z"%(qubit_pair[0]), eval("qubit_IF_q%s"%(qubit_pair[0])), eval("qubit_LO_q%s"%(qubit_pair[0]))
q2_xy, q2_z, q2_IF, q2_LO = "q%s_xy"%(qubit_pair[1]), "q%s_z"%(qubit_pair[1]), eval("qubit_IF_q%s"%(qubit_pair[1])), eval("qubit_LO_q%s"%(qubit_pair[1]))

# Adjust the pulse duration and amplitude to drive the qubit into a mixed state
saturation_len = 20 * u.us  # In ns
saturation_amp = 0.057  # pre-factor to the value defined in the config - restricted to [-2; 2)
# Qubit detuning sweep with respect to qubit_IF
dfs = np.arange(-450e6, +450e6, 1e6)
# Flux sweep
dcs = np.arange(-0.2, 0.2, 0.002)
flux_offset_1 = 0
flux_offset_2 = 0

# The fit parameters are take from the config
fitted_curve1 = (cosine_func(dcs, amplitude_fit1, frequency_fit1, phase_fit1, offset_fit1)).astype(int)
fitted_curve2 = (cosine_func(dcs, amplitude_fit2, frequency_fit2, phase_fit2, offset_fit2)).astype(int)


with program() as multi_qubit_spec_vs_flux:
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=2)
    df = declare(int)  # QUA variable for the qubit detuning
    dc = declare(fixed)  # QUA variable for the flux bias
    resonator_freq1 = declare(int, value=fitted_curve1.tolist())  # res freq vs flux table
    resonator_freq2 = declare(int, value=fitted_curve2.tolist())  # res freq vs flux table
    index = declare(int, value=0)  # index to get the right resonator freq for a given flux

    with for_(n, 0, n < n_avg, n + 1):
        with for_(*from_array(df, dfs)):
            # Update the frequency of the two qubit elements
            update_frequency(q1_xy, df + q1_IF)
            update_frequency(q2_xy, df + q2_IF)
            assign(index, 0)
            with for_(*from_array(dc, dcs)):
                # Flux sweeping
                set_dc_offset(q1_z, "single", dc + flux_offset_1)
                set_dc_offset(q2_z, "single", dc + flux_offset_2)
                wait(flux_settle_time * u.ns)  # Wait for the flux to settle
                # Update the resonator frequency to always measure on resonance
                # update_frequency("rr1", resonator_freq1[index] + resonator_IF_q1)
                # update_frequency("rr2", resonator_freq2[index] + resonator_IF_q2)

                # Saturate qubit
                play("saturation" * amp(saturation_amp), q1_xy, duration=saturation_len * u.ns)
                play("saturation" * amp(saturation_amp), q2_xy, duration=saturation_len * u.ns)

                # Multiplexed readout, also saves the measurement outcomes
                multiplexed_readout(I, I_st, Q, Q_st, resonators=qubit_pair, amplitude=0.9)
                # Wait for the qubit to decay to the ground state
                # wait(thermalization_time * u.ns)
                # Update the resonator frequency vs flux index
                assign(index, index + 1)
        # Save the averaging iteration to get the progress bar
        save(n, n_st)

    with stream_processing():
        n_st.save("n")
        # resonator 1
        I_st[0].buffer(len(dcs)).buffer(len(dfs)).average().save("I1")
        Q_st[0].buffer(len(dcs)).buffer(len(dfs)).average().save("Q1")
        # resonator 2
        I_st[1].buffer(len(dcs)).buffer(len(dfs)).average().save("I2")
        Q_st[1].buffer(len(dcs)).buffer(len(dfs)).average().save("Q2")

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
    job = qmm.simulate(config, multi_qubit_spec_vs_flux, simulation_config)
    job.get_simulated_samples().con1.plot()
    plt.show()
else:
    # Open a quantum machine to execute the QUA program
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(multi_qubit_spec_vs_flux)
    # Prepare the figure for live plotting
    fig = plt.figure()
    interrupt_on_close(fig, job)
    # Tool to easily fetch results from the OPX (results_handle used in it)
    results = fetching_tool(job, ["n", "I1", "Q1", "I2", "Q2"], mode="live")
    # Live plotting
    while results.is_processing():
        # Fetch results
        n, I1, Q1, I2, Q2 = results.fetch_all()
        # Progress bar
        progress_counter(n, n_avg, start_time=results.start_time)
        # Data analysis
        S1 = u.demod2volts(I1 + 1j * Q1, readout_len)
        S2 = u.demod2volts(I2 + 1j * Q2, readout_len)
        R1 = np.abs(S1)
        phase1 = np.angle(S1)
        R2 = np.abs(S2)
        phase2 = np.angle(S2)
        # Plots
        plt.suptitle("Qubit spectroscopy (%s/%s)" %(n,n_avg))
        plt.subplot(221)
        plt.cla()
        plt.pcolor(dcs, (q1_IF + dfs) / u.MHz, R1)
        plt.xlabel("Flux bias [V]")
        plt.ylabel("q%s IF [MHz]"%(qubit_pair[0]))
        plt.title(f"q{qubit_pair[0]} (LO: {(q1_LO) / u.MHz} MHz)")
        plt.subplot(223)
        plt.cla()
        plt.pcolor(dcs, (q1_IF + dfs) / u.MHz, phase1)
        plt.xlabel("Flux bias [V]")
        plt.ylabel("q%s IF [MHz]"%(qubit_pair[0]))
        plt.subplot(222)
        plt.cla()
        plt.pcolor(dcs, (q2_IF + dfs) / u.MHz, R2)
        plt.xlabel("Flux bias [V]")
        plt.ylabel("q%s IF [MHz]"%(qubit_pair[1]))
        plt.title(f"q{qubit_pair[1]} (LO: {(q2_LO) / u.MHz} MHz)")
        plt.subplot(224)
        plt.cla()
        plt.pcolor(dcs, (q2_IF + dfs) / u.MHz, phase2)
        plt.xlabel("Flux bias [V]")
        plt.ylabel("q%s IF [MHz]"%(qubit_pair[1]))
        plt.tight_layout()
        plt.pause(0.1)
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()

"""
        RESONATOR SPECTROSCOPY VERSUS FLUX
This sequence involves measuring the resonator by sending a readout pulse and demodulating the signals to
extract the 'I' and 'Q' quadratures. This is done across various readout intermediate frequencies and flux biases.
The resonator frequency as a function of flux bias is then extracted and fitted so that the parameters can be stored in the configuration.

This information can then be used to adjust the readout frequency for the maximum frequency point.

Prerequisites:
    - Calibration of the time of flight, offsets, and gains (referenced as "time_of_flight").
    - Calibration of the IQ mixer connected to the readout line (be it an external mixer or an Octave port).
    - Identification of the resonator's resonance frequency (referred to as "resonator_spectroscopy_multiplexed").
    - Configuration of the readout pulse amplitude and duration.
    - Specification of the expected resonator depletion time in the configuration.

Before proceeding to the next node:
    - Update the readout frequency, labeled as "resonator_IF", in the configuration.
    - Adjust the flux bias to the maximum frequency point, labeled as "max_frequency_point", in the configuration.
    - Update the resonator frequency versus flux fit parameters (amplitude_fit, frequency_fit, phase_fit, offset_fit) in the configuration
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
from scipy import signal
from scipy.optimize import curve_fit
import warnings

warnings.filterwarnings("ignore")


###################
# The QUA program #
###################
qubit_num = 3
n_avg = 200000
# The frequency sweep around the resonators' frequency "resonator_IF_q"
span = 1.5 * u.MHz
df = 100 * u.kHz
dfs = np.arange(-span, +span + 0.1, df)
# Flux bias sweep in V
flux_min = -0.2
flux_max = 0.2
step = 0.01
flux = np.arange(flux_min, flux_max + step / 2, step)

with program() as multi_res_spec_vs_flux:
    # QUA macro to declare the measurement variables and their corresponding streams for a given number of resonators
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=qubit_num)
    df = declare(int)  # QUA variable for sweeping the readout frequency detuning around the resonance
    dc = declare(fixed)  # QUA variable for sweeping the flux bias

    with for_(n, 0, n < n_avg, n + 1):
        with for_(*from_array(df, dfs)):
            # Update the frequency of the two resonator elements
            update_frequency("rr1", df + resonator_IF_q1)
            update_frequency("rr2", df + resonator_IF_q2)
            update_frequency("rr3", df + resonator_IF_q3)

            with for_(*from_array(dc, flux)):
                # Flux sweeping
                set_dc_offset("q1_z", "single", dc)
                set_dc_offset("q2_z", "single", dc)
                set_dc_offset("q3_z", "single", dc)
                wait(flux_settle_time * u.ns)  # Wait for the flux to settle
                # Macro to perform multiplexed readout on the specified resonators
                # It also save the 'I' and 'Q' quadratures into their respective streams
                multiplexed_readout(I, I_st, Q, Q_st, resonators=[1, 2, 3], sequential=False)
                # wait for the resonators to relax
                wait(depletion_time * u.ns, "rr1", "rr2", "rr3")
        save(n, n_st)

    # set_dc_offset("q1_z", "single", 0)
    # set_dc_offset("q2_z", "single", 0)
    # set_dc_offset("q3_z", "single", 0)

    with stream_processing():
        n_st.save("n")
        # resonator 1
        I_st[0].buffer(len(flux)).buffer(len(dfs)).average().save("I1")
        Q_st[0].buffer(len(flux)).buffer(len(dfs)).average().save("Q1")
        # resonator 2
        I_st[1].buffer(len(flux)).buffer(len(dfs)).average().save("I2")
        Q_st[1].buffer(len(flux)).buffer(len(dfs)).average().save("Q2")
        # resonator 3
        I_st[2].buffer(len(flux)).buffer(len(dfs)).average().save("I3")
        Q_st[2].buffer(len(flux)).buffer(len(dfs)).average().save("Q3")

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
    job = qmm.simulate(config, multi_res_spec_vs_flux, simulation_config)
    job.get_simulated_samples().con1.plot()
    plt.show()
else:
    # Open a quantum machine to execute the QUA program
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(multi_res_spec_vs_flux)
    # Prepare the figure for live plotting
    fig = plt.figure()
    interrupt_on_close(fig, job)
    # Tool to easily fetch results from the OPX (results_handle used in it)
    results = fetching_tool(job, ["n", "I1", "Q1", "I2", "Q2", "I3", "Q3"], mode="live")
    # Live plotting
    while results.is_processing():
        # Fetch results
        n, I1, Q1, I2, Q2, I3, Q3 = results.fetch_all()
        # Progress bar
        progress_counter(n, n_avg, start_time=results.start_time)
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
        # Plots
        plt.suptitle("Flux dep. Resonator spectroscopy")

        plt.subplot(200 + qubit_num*10 + 1)
        plt.cla()
        plt.title(f"Resonator 1 - LO: {resonator_LO / u.GHz} GHz")
        plt.ylabel("Readout IF [MHz]")
        plt.pcolor(flux, (dfs + resonator_IF_q1) / u.MHz, R1)
        plt.axhline(resonator_IF_q1 / u.MHz, color="k")
        plt.subplot(200 + qubit_num*10 + 2)
        plt.cla()
        plt.title(f"Resonator 2 - LO: {resonator_LO / u.GHz} GHz")
        plt.pcolor(flux, (dfs + resonator_IF_q2) / u.MHz, R2)
        plt.axhline(resonator_IF_q2 / u.MHz, color="k")
        plt.subplot(200 + qubit_num*10 + 3)
        plt.cla()
        plt.title(f"Resonator 3 - LO: {resonator_LO / u.GHz} GHz")
        plt.pcolor(flux, (dfs + resonator_IF_q3) / u.MHz, R3)
        plt.axhline(resonator_IF_q3 / u.MHz, color="k")
        
        plt.subplot(200 + qubit_num*10 + 4)
        plt.cla()
        plt.xlabel("Flux bias [V]")
        plt.ylabel("Readout IF [MHz]")
        plt.pcolor(flux, (dfs + resonator_IF_q1) / u.MHz, signal.detrend(np.unwrap(phase1)))
        plt.axhline(resonator_IF_q1 / u.MHz, color="k")
        plt.subplot(200 + qubit_num*10 + 5)
        plt.cla()
        plt.xlabel("Flux bias [V]")
        plt.pcolor(flux, (dfs + resonator_IF_q2) / u.MHz, signal.detrend(np.unwrap(phase2)))
        plt.axhline(resonator_IF_q2 / u.MHz, color="k")
        plt.subplot(200 + qubit_num*10 + 6)
        plt.cla()
        plt.xlabel("Flux bias [V]")
        plt.pcolor(flux, (dfs + resonator_IF_q3) / u.MHz, signal.detrend(np.unwrap(phase3)))
        plt.axhline(resonator_IF_q3 / u.MHz, color="k")

        plt.tight_layout()
        plt.pause(0.1)
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()

    # Fitting to cosine resonator frequency response
    def cosine_func(x, amplitude, frequency, phase, offset):
        return amplitude * np.cos(2 * np.pi * frequency * x + phase) + offset

    # Array for the flux minima
    minima = np.zeros(len(flux))
    # Frequency range for the 3 resonators
    frequencies = [dfs + resonator_IF_q1, dfs + resonator_IF_q2, dfs + resonator_IF_q3]
    # Amplitude for the 3 resonators
    R = [R1, R2, R3]
    plt.figure()
    for rr in range(3):
        print(f"Resonator rr{rr+1}")
        # Find the resonator frequency vs flux minima
        for i in range(len(flux)):
            minima[i] = frequencies[rr][np.argmin(R[rr].T[i])]

        # Cosine fit
        initial_guess = [1, 0.5, 0, 0]  # Initial guess for the parameters
        fit_params, _ = curve_fit(cosine_func, flux, minima, p0=initial_guess)

        # Get the fitted values
        amplitude_fit, frequency_fit, phase_fit, offset_fit = fit_params
        print("fitting parameters", fit_params)

        # Generate the fitted curve using the fitted parameters
        fitted_curve = cosine_func(flux, amplitude_fit, frequency_fit, phase_fit, offset_fit)
        plt.subplot(3, 1, rr + 1)
        plt.pcolor(flux, frequencies[rr] / u.MHz, R1)
        plt.plot(flux, minima / u.MHz, "x-", color="red", label="Flux minima")
        plt.plot(flux, fitted_curve / u.MHz, label="Fitted Cosine", color="orange")
        plt.xlabel("Flux bias [V]")
        plt.ylabel("Readout IF [MHz]")
        plt.title(f"Resonator rr{rr+1}")
        plt.legend()
        plt.tight_layout()
        plt.show()

        print(
            f"DC flux value corresponding to the maximum frequency point for resonator {rr}: {flux[np.argmax(fitted_curve)]}"
        )

# from qm import generate_qua_script
# sourceFile = open('debug.py', 'w')
# print(generate_qua_script(multi_res_spec_vs_flux, config), file=sourceFile)
# sourceFile.close()
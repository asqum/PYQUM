"""
        CRYOSCOPE - 4ns
The goal of this protocol is to measure the step response of the flux line and design proper FIR and IIR filters
(implemented on the OPX) to pre-distort the flux pulses and improve the two-qubit gates fidelity.
Since the flux line ends on the qubit chip, it is not possible to measure the flux pulse after propagation through the
fridge. The idea is to exploit the flux dependency of the qubit frequency, measured with a modified Ramsey sequence, to
estimate the flux amplitude received by the qubit as a function of time.

The sequence consists of a Ramsey sequence ("x90" - idle time - "x90" or "y90") with a fixed dephasing time.
A flux pulse with varying duration is played during the idle time. The Sx and Sy components of the Bloch vector are
measured by alternatively closing the Ramsey sequence with a "x90" or "y90" gate in order to extract the qubit dephasing
 as a function of the flux pulse duration.

The results are then post-processed to retrieve the step function of the flux line which is fitted with an exponential
function. The corresponding exponential parameters are then used to derive the FIR and IIR filter taps that will
compensate for the distortions introduced by the flux line (wiring, bias-tee...).
Such digital filters are then implemented on the OPX. Note that these filters will introduce a global delay on all the
output channels that may rotate the IQ blobs so that you may need to recalibrate them for state discrimination or
active reset protocols for instance. You can read more about these filters here:
https://docs.quantum-machines.co/0.1/qm-qua-sdk/docs/Guides/output_filter/?h=filter#hardware-implementation

The protocol is inspired from https://doi.org/10.1063/1.5133894, which contains more details about the sequence and
the post-processing of the data.

This version sweeps the flux pulse duration using real-time QUA, which means that the flux pulse can be arbitrarily long
but the step must be larger than 1 clock cycle (4ns) and the minimum pulse duration must be 4 clock cycles (16ns).

Prerequisites:
    - Having found the resonance frequency of the resonator coupled to the qubit under study (resonator_spectroscopy).
    - Having calibrated qubit gates (x90 and y90) by running qubit spectroscopy, rabi_chevron, power_rabi, Ramsey and updated the configuration.

Next steps before going to the next node:
    - Update the FIR and IIR filter taps in the configuration (config/controllers/con1/analog_outputs/"filter": {"feedforward": fir, "feedback": iir}).
"""

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from configuration import *
from scipy import signal, optimize
import matplotlib.pyplot as plt
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.plot import interrupt_on_close
import numpy as np
from macros import qua_declaration, multiplexed_readout
from qualang_tools.loops import from_array
import warnings

warnings.filterwarnings("ignore")


####################
# Helper functions #
####################
def exponential_decay(x, a, t):
    """Exponential decay defined as 1 + a * np.exp(-x / t).

    :param x: numpy array for the time vector in ns
    :param a: float for the exponential amplitude
    :param t: float for the exponential decay time in ns
    :return: numpy array for the exponential decay
    """
    return 1 + a * np.exp(-x / t)


def exponential_correction(A, tau, Ts=1e-9):
    """Derive FIR and IIR filter taps based on the exponential coefficients A and tau from 1 + a * np.exp(-x / t).

    :param A: amplitude of the exponential decay.
    :param tau: decay time of the exponential decay
    :param Ts: sampling period. Default is 1e-9
    :return: FIR and IIR taps
    """
    tau = tau * Ts
    k1 = Ts + 2 * tau * (A + 1)
    k2 = Ts - 2 * tau * (A + 1)
    c1 = Ts + 2 * tau
    c2 = Ts - 2 * tau
    feedback_tap = k2 / k1
    feedforward_taps = np.array([c1, c2]) / k1
    return feedforward_taps, feedback_tap


def filter_calc(exponential):
    """Derive FIR and IIR filter taps based on a list of exponential coefficients.

    :param exponential: exponential coefficients defined as [(A1, tau1), (A2, tau2)]
    :return: FIR and IIR taps as [fir], [iir]
    """
    # Initialization based on the number of exponential coefficients
    b = np.zeros((2, len(exponential)))
    feedback_taps = np.zeros(len(exponential))
    # Derive feedback tap for each set of exponential coefficients
    for i, (A, tau) in enumerate(exponential):
        b[:, i], feedback_taps[i] = exponential_correction(A, tau)
    # Derive feedback tap for each set of exponential coefficients
    feedforward_taps = b[:, 0]
    for i in range(len(exponential) - 1):
        feedforward_taps = np.convolve(feedforward_taps, b[:, i + 1])
    # feedforward taps are bounded to +/- 2
    if np.abs(max(feedforward_taps)) >= 2:
        feedforward_taps = 2 * feedforward_taps / max(feedforward_taps)

    return feedforward_taps, feedback_taps


###################
# The QUA program #
###################
# Index of the qubit to measure
qubit = 4
multiplexed = [1,2,3,4,5]
wait_z = 450
wait_xy = 400

n_avg = 6_000  # Number of averages
# Flux pulse durations in clock cycles (4ns) - must be > 4 or the pulse won't be played.
durations = np.arange(3, const_flux_len // 4, 1)  # Starts at 3 clock-cycles to have the first point without pulse.
# flux_waveform = np.array([const_flux_amp] * max(durations))
xplot = durations * 4  # x-axis for plotting and deriving the filter taps - must be in ns.
step_response_th = [1.0] * len(xplot)  # Perfect step response (square)


with program() as cryoscope:
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=5)
    t = declare(int)  # QUA variable for the flux pulse duration
    flag = declare(bool)  # QUA boolean to switch between x90 and y90
    state = [declare(bool) for _ in range(5)]
    state_st = [declare_stream() for _ in range(5)]

    # Outer loop for averaging
    with for_(n, 0, n < n_avg, n + 1):
        # Loop over the truncated flux pulse
        with for_(*from_array(t, durations)):
            # Alternate between X/2 and Y/2 pulses
            with for_each_(flag, [True, False]):
                # Play first X/2
                play("x90", f"q{qubit}_xy")
                # Play truncated flux pulse
                align()
                # Wait some time to ensure that the flux pulse will arrive after the x90 pulse
                wait(wait_z * u.ns)
                # Play the flux pulse only if t is larger than the minimum of 4 clock cycles (16ns)
                with if_(t > 3):
                    play("const", f"q{qubit}_z", duration=t)
                
                # Wait for the idle time set slightly above the maximum flux pulse duration to ensure that the 2nd x90
                # pulse arrives after the longest flux pulse
                wait((const_flux_len + wait_xy) * u.ns, f"q{qubit}_xy")
                # NOTE: Keep the phase consistent

                # Play second X/2 or Y/2
                with if_(flag):
                    play("x90", f"q{qubit}_xy")
                with else_():
                    play("y90", f"q{qubit}_xy")
                # Measure resonator state after the sequence
                align()
                multiplexed_readout(I, I_st, Q, Q_st, resonators=multiplexed, weights="rotated_")
                # State discrimination
                assign(state[0], I[0] > ge_threshold_q4)
                assign(state[1], I[1] > ge_threshold_q5)
                assign(state[2], I[2] > ge_threshold_q3)
                assign(state[3], I[3] > ge_threshold_q4)
                assign(state[4], I[4] > ge_threshold_q5)
                save(state[0], state_st[0])
                save(state[1], state_st[1])
                save(state[2], state_st[2])
                save(state[3], state_st[3])
                save(state[4], state_st[4])
                # Wait cooldown time and save the results
                wait(thermalization_time * u.ns)
        save(n, n_st)

    with stream_processing():
        # for the progress counter
        n_st.save("n")
        for i,x in enumerate(multiplexed):
            I_st[i].buffer(2).buffer(len(durations)).average().save(f"I{x}")
            # Q_st[i].buffer(2).buffer(len(durations)).average().save(f"Q{x}")
            state_st[i].boolean_to_int().buffer(2).buffer(len(durations)).average().save(f"state{x}")
        

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
    simulation_config = SimulationConfig(duration=20_000)  # In clock cycles = 4ns
    job = qmm.simulate(config, cryoscope, simulation_config)
    job.get_simulated_samples().con1.plot()
    job.get_simulated_samples().con2.plot()
    plt.show()
    
else:
    # Open the quantum machine
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(cryoscope)
    # Get results from QUA program
    results = fetching_tool(job, ["n"]+[f"I{x}" for x in multiplexed]+[f"state{x}" for x in multiplexed], mode="live")
    # Live plotting
    fig = plt.figure()
    interrupt_on_close(fig, job)  #  Interrupts the job when closing the figure
    while results.is_processing():
        # Fetch results
        n, I1, I2, I3, I4, I5, state1, state2, state3, state4, state5 = results.fetch_all()
        # Convert the results into Volts
        I1, I2, I3, I4, I5 = u.demod2volts(I1, readout_len), u.demod2volts(I2, readout_len), u.demod2volts(I3, readout_len), u.demod2volts(I4, readout_len), u.demod2volts(I5, readout_len)
        
        # Progress bar
        progress_counter(n, n_avg, start_time=results.start_time)
        
        # Bloch vector Sx + iSy
        eigenvalue_X = eval(f"state{qubit}")[:, 0]
        Sxx = (eigenvalue_X-min(eigenvalue_X))
        Sxx = Sxx/max(Sxx) * 2 - 1
        
        eigenvalue_Y = eval(f"state{qubit}")[:, 1]
        Syy = (eigenvalue_Y-min(eigenvalue_Y))
        Syy = Syy/max(Syy) * 2 - 1
        
        S = Sxx + 1j * Syy

        # print("max: %s "%max(eigenvalue_Y))
        # print("S: %s" %(S))

        # Accumulated phase: angle between Sx and Sy
        phase = np.unwrap(np.angle(S))
        phase = phase - phase[-1]
        # Filtering and derivative of the phase to get the averaged frequency
        detuning = signal.savgol_filter(phase / 2 / np.pi, 21, 2, deriv=1, delta=0.001)
        # Flux line step response in freq domain and voltage domain
        step_response_freq = detuning / np.average(detuning[-int(const_flux_len / 2) :])
        step_response_volt = np.sqrt(step_response_freq)
        # Plots
        plt.suptitle(f"Cryoscope for qubit {qubit}")
        plt.subplot(241)
        plt.cla()
        plt.plot(xplot, eval(f"I{qubit}"))
        plt.xlabel("Pulse duration [ns]")
        plt.ylabel(f"q{qubit}-I [V]")
        plt.legend(("X", "Y"), loc="lower right")
        plt.subplot(242)
        plt.cla()
        plt.plot(xplot, phase)
        plt.xlabel("Pulse duration [ns]")
        plt.ylabel("phase")
        plt.subplot(243)
        plt.cla()
        plt.plot(xplot, detuning)
        plt.xlabel("Pulse duration [ns]")
        plt.ylabel("detuning")
        plt.subplot(244)
        plt.cla()
        plt.plot(xplot, step_response_freq, label="Frequency")
        plt.xlabel("Pulse duration [ns]")
        plt.ylabel("Step response frequency")
        plt.title(f"Qubit {qubit}")
        plt.legend()

        plt.subplot(245)
        plt.cla()
        plt.plot(xplot, eval(f"state{qubit}"))
        plt.xlabel("Pulse duration [ns]")
        plt.ylabel(f"q{qubit} |1> population")
        plt.legend(("X", "Y"), loc="lower right")
        plt.subplot(246)
        plt.cla()
        plt.plot(xplot, Sxx, 'b', xplot, Syy, 'r')
        plt.xlabel("Pulse duration [ns]")
        plt.ylabel("State amplitude")
        plt.legend(("Sx", "Sy"), loc="lower right")
        plt.subplot(247)
        plt.cla()
        for x in multiplexed:
            if x != qubit:
                plt.plot(xplot, eval(f"state{x}"))
                plt.legend((f"X{x}", f"Y{x}"), loc="lower right")
        plt.xlabel("Pulse duration [ns]")
        plt.ylabel("neighbors' |1> population")
        
        plt.subplot(248)
        plt.cla()
        plt.plot(xplot, step_response_volt, label=r"Voltage ($\sqrt{freq}$)")
        plt.xlabel("Pulse duration [ns]")
        plt.ylabel("Step response")
        plt.legend()
        plt.title(f"Qubit {qubit}")

        plt.tight_layout()
        plt.pause(0.1)

    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()

    filename = "Cryoscope4ns_q%s_%s" %(qubit,const_flux_len)
    save = False
    if save:
        np.savez(save_dir/filename, I1=I1, I2=I2, Q1=Q1, Q2=Q2, S=S, xplot=xplot, step_response_volt=step_response_volt)
        print("Data saved as %s.npz" %filename)


    ## Fit step response with exponential
    [A, tau], _ = optimize.curve_fit(
        exponential_decay,
        xplot[3::],
        step_response_volt[3::],
    )
    print(f"A: {A}\ntau: {tau}")

    ## Derive IIR and FIR corrections
    fir, iir = filter_calc(exponential=[(A, tau)])
    print(f"FIR: {fir}\nIIR: {iir}")

    ## Derive responses and plots
    # Response without filter
    no_filter = exponential_decay(xplot, A, tau)
    # Response with filters
    with_filter = no_filter * signal.lfilter(fir, [1, iir[0]], step_response_th)  # Output filter , DAC Output

    # Plot all data
    plt.rcParams.update({"font.size": 13})
    plt.figure()
    plt.suptitle("Cryoscope with filter implementation")
    plt.plot(xplot, step_response_volt, "o-", label="Experimental data")
    plt.plot(xplot, no_filter, label="Fitted response without filter")
    plt.plot(xplot, with_filter, label="Fitted response with filter")
    plt.plot(xplot, step_response_th, label="Ideal WF")  # pulse
    plt.text(
        max(xplot) // 2,
        max(step_response_volt) / 2,
        f"IIR = {iir}\nFIR = {fir}",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )
    plt.text(
        max(xplot) // 4,
        max(step_response_volt) / 2,
        f"A = {A:.2f}\ntau = {tau:.2f}",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )
    plt.xlabel("Flux pulse duration [ns]")
    plt.ylabel("Step response")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()
    

"""
This file contains useful QUA macros meant to simplify and ease QUA programs.
All the macros below have been written and tested with the basic configuration. If you modify this configuration
(elements, operations, integration weights...) these macros will need to be modified accordingly.
"""

from qm.qua import *
from qualang_tools.addons.variables import assign_variables_to_element
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.plot import interrupt_on_close
from configuration import *

import matplotlib.pyplot as plt
from scipy import signal
from scipy.optimize import curve_fit

##############
# QUA macros #
##############


def cz_gate(type="square"):
    if type == "square":
        wait(5)  # for flux pulse to relax back completely
        set_dc_offset("q2_z", "single", 0.14519591) # 10cc: 0.1452099
        wait(48 // 4, "q2_z")
        align()
        set_dc_offset("q2_z", "single", idle_q2)
        wait(5)  # for flux pulse to relax back completely
    elif type == "ft_gaussian":
        play("cz_1_2"*amp((0.150-max_frequency_point2)/(cz_point_1_2_q2-idle_q2)), "q2_z", duration=80//4)
    elif type == "gaussian":
        play("cz_1_2"*amp(1.4), "q2_z", duration=32//4)


def multiplexed_readout(I, I_st, Q, Q_st, resonators, sequential=False, amplitude=1.0, weights=""):
    """Perform multiplexed readout on two resonators"""
    if type(resonators) is not list:
        resonators = [resonators]

    for ind, res in enumerate(resonators):
        measure(
            "readout" * amp(amplitude),
            f"rr{res}",
            None,
            dual_demod.full(weights + "cos", "out1", weights + "sin", "out2", I[ind]),
            dual_demod.full(weights + "minus_sin", "out1", weights + "cos", "out2", Q[ind]),
        )

        if I_st is not None:
            save(I[ind], I_st[ind])
        if Q_st is not None:
            save(Q[ind], Q_st[ind])

        if sequential and ind < len(resonators) - 1:
            align(f"rr{res}", f"rr{res+1}")


def qua_declaration(nb_of_qubits):
    """
    Macro to declare the necessary QUA variables

    :param nb_of_qubits: Number of qubits used in this experiment
    :return:
    """
    n = declare(int)
    n_st = declare_stream()
    I = [declare(fixed) for _ in range(nb_of_qubits)]
    Q = [declare(fixed) for _ in range(nb_of_qubits)]
    I_st = [declare_stream() for _ in range(nb_of_qubits)]
    Q_st = [declare_stream() for _ in range(nb_of_qubits)]
    # Workaround to manually assign the results variables to the readout elements
    for i in range(nb_of_qubits):
        assign_variables_to_element(f"rr{i + 1}", I[i], Q[i])
    return I, I_st, Q, Q_st, n, n_st


def reset_qubit(method: str, qubit: str, resonator: str, **kwargs):
    """
    Macro to reset the qubit state.

    If method is 'cooldown', then the variable cooldown_time (in clock cycles) must be provided as a python integer > 4.

    **Example**: reset_qubit('cooldown', cooldown_times=500)

    If method is 'active', then 3 parameters are available as listed below.

    **Example**: reset_qubit('active', threshold=-0.003, max_tries=3)

    :param method: Method the reset the qubit state. Can be either 'cooldown' or 'active'.
    :param qubit: The qubit element. Must be defined in the config.
    :param resonator: The resonator element. Must be defined in the config.
    :key cooldown_time: qubit relaxation time in clock cycle, needed if method is 'cooldown'. Must be an integer > 4.
    :key threshold: threshold to discriminate between the ground and excited state, needed if method is 'active'.
    :key max_tries: python integer for the maximum number of tries used to perform active reset,
        needed if method is 'active'. Must be an integer > 0 and default value is 1.
    :key Ig: A QUA variable for the information in the `I` quadrature used for active reset. If not given, a new
        variable will be created. Must be of type `Fixed`.
    :return:
    """
    if method == "cooldown":
        # Check cooldown_time
        cooldown_time = kwargs.get("cooldown_time", None)
        if (cooldown_time is None) or (cooldown_time < 4):
            raise Exception("'cooldown_time' must be an integer > 4 clock cycles")
        # Reset qubit state
        wait(cooldown_time, qubit)
    elif method == "active":
        # Check threshold
        threshold = kwargs.get("threshold", None)
        if threshold is None:
            raise Exception("'threshold' must be specified for active reset.")
        # Check max_tries
        max_tries = kwargs.get("max_tries", 1)
        if (max_tries is None) or (not float(max_tries).is_integer()) or (max_tries < 1):
            raise Exception("'max_tries' must be an integer > 0.")
        # Check Ig
        Ig = kwargs.get("Ig", None)
        # Reset qubit state
        return active_reset(threshold, qubit, resonator, max_tries=max_tries, Ig=Ig)


# Macro for performing active reset until successful for a given number of tries.
def active_reset(threshold: float, qubit: str, resonator: str, max_tries=1, Ig=None):
    """Macro for performing active reset until successful for a given number of tries.

    :param threshold: threshold for the 'I' quadrature discriminating between ground and excited state.
    :param qubit: The qubit element. Must be defined in the config.
    :param resonator: The resonator element. Must be defined in the config.
    :param max_tries: python integer for the maximum number of tries used to perform active reset. Must >= 1.
    :param Ig: A QUA variable for the information in the `I` quadrature. Should be of type `Fixed`. If not given, a new
        variable will be created
    :return: A QUA variable for the information in the `I` quadrature and the number of tries after success.
    """
    if Ig is None:
        Ig = declare(fixed)
    if (max_tries < 1) or (not float(max_tries).is_integer()):
        raise Exception("max_count must be an integer >= 1.")
    # Initialize Ig to be > threshold
    assign(Ig, threshold + 2**-28)
    # Number of tries for active reset
    counter = declare(int)
    # Reset the number of tries
    assign(counter, 0)

    # Perform active feedback
    align(qubit, resonator)
    # Use a while loop and counter for other protocols and tests
    with while_((Ig > threshold) & (counter < max_tries)):
        # Measure the resonator
        measure(
            "readout",
            resonator,
            None,
            dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", Ig),
        )
        # Play a pi pulse to get back to the ground state
        play("x180", qubit, condition=(Ig > threshold))
        # Increment the number of tries
        assign(counter, counter + 1)
    return Ig, counter


# Exponential decay
def expdecay(x, a, t):
    """Exponential decay defined as 1 + a * np.exp(-x / t).

    :param x: numpy array for the time vector in ns
    :param a: float for the exponential amplitude
    :param t: float for the exponential decay time in ns
    :return: numpy array for the exponential decay
    """
    return 1 + a * np.exp(-x / t)


# Theoretical IIR and FIR taps based on exponential decay coefficients
def exponential_correction(A, tau, Ts=1e-9):
    """Derive FIR and IIR filter taps based on a the exponential coefficients A and tau from 1 + a * np.exp(-x / t).

    :param A: amplitude of the exponential decay
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


# FIR and IIR taps calculation
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
    # Derive feddback tap for each set of exponential coefficients
    feedforward_taps = b[:, 0]
    for i in range(len(exponential) - 1):
        feedforward_taps = np.convolve(feedforward_taps, b[:, i + 1])
    # feedforward taps are bounded to +/- 2
    if np.abs(max(feedforward_taps)) >= 2:
        feedforward_taps = 2 * feedforward_taps / max(feedforward_taps)

    return feedforward_taps, feedback_taps


# Plotting
def live_plotting(n_avg, q_id, job, x_range, y_range, title, save_data, save_path, stage="", normalize=True, dimension=2):
    # extracting data
    I_list, Q_list = ["I%s"%(i+1) for i in q_id], ["Q%s"%(i+1) for i in q_id]
    results = fetching_tool(job, I_list + Q_list + ["n"], mode="live")
    
    # Live plotting
    fig = plt.figure()
    interrupt_on_close(fig, job)
    while results.is_processing():
        # Fetch results
        all_results = results.fetch_all()
        n = all_results[-1]
        I, Q = all_results[0:len(q_id)], all_results[len(q_id):len(q_id)*2]

        ###################
        #   .npz Saving   #
        ###################
        # NOTE: stage dependency:
        if stage == "6a":
            ReadoutAmplitude = np.zeros((len(q_id), len(x_range)))
            Frequency = np.zeros((len(q_id), len(y_range)))
            Amplitude = np.zeros((len(q_id), len(y_range), len(x_range)))
            Phase = np.zeros((len(q_id), len(y_range), len(x_range)))
        
        # Progress bar
        progress_counter(n, n_avg, start_time=results.start_time)
        # output results for fitting later
        map_top = R = np.zeros((len(q_id), len(x_range), len(y_range)))
        map_bottom = R = np.zeros((len(q_id), len(x_range), len(y_range)))
        plt.suptitle(title + " (%s/%s)" %(n,n_avg))
        for i in q_id:
            # Data analysis
            S = u.demod2volts(I[q_id.index(i)] + 1j * Q[q_id.index(i)], readout_len)
            R = np.abs(S)
            phase = np.angle(S)
            if normalize:
                row_sums = R.sum(axis=0)
                R /= row_sums[np.newaxis, :]

            # NOTE: stage dependency:
            if stage == "6a":
                x_var = x_range * readout_amp[i]
                y_var = (y_range + resonator_IF[i]) / u.MHz
                x_label = "Readout amplitude [V]"
                y_label = "Readout IF [MHz]"
                map_top = R
                map_bottom = signal.detrend(np.unwrap(phase))
                axh, axv = True, False
                h_center = resonator_IF[i] / u.MHz
                # .npz saving
                ReadoutAmplitude[i] = x_var
                Frequency[i] = y_range + resonator_IF[i] + resonator_LO
                Amplitude[i] = R
                Phase[i] = signal.detrend(np.unwrap(phase))
            elif stage == "6b":
                x_var = x_range
                y_var = (y_range + resonator_IF[i]) / u.MHz
                x_label = "Flux bias [V]"
                y_label = "Readout IF [MHz]"
                map_top = R
                map_bottom = signal.detrend(np.unwrap(phase))
                axh, axv = True, False
                h_center = resonator_IF[i] / u.MHz
            elif stage == "7":
                x_var = (x_range + qubit_IF[i]) / u.MHz
                y_var = y_range
                x_label = "Qubit intermediate frequency [MHz]"
                y_label = r"$R=\sqrt{I^2 + Q^2}$ [V]"
                y_label_bottom = "Phase [rad]"
                map_top = R
                map_bottom = signal.detrend(np.unwrap(phase))
                axh, axv = False, True
                v_center = qubit_IF[i] / u.MHz

            else:
                title = ""
                x_var = x_range
                y_var = y_range
                x_label = ""
                y_label = ""
                map_top = I[q_id.index(i)]
                map_bottom = Q[q_id.index(i)]
                axh, axv = 0, 0
            
            # Plot Top
            plt.subplot(2, len(q_id), q_id.index(i)+1)
            plt.cla()
            plt.title("q%s:"%(i+1))
            if q_id.index(i)==0: 
                plt.ylabel(y_label)
            if dimension==1: 
                plt.plot(x_var, map_top)
            elif dimension==2: 
                plt.pcolor(x_var, y_var, map_top)
            if axh:
                plt.axhline(h_center, color="k", linewidth=0.37)
            if axv:
                plt.axvline(v_center, color="k", linewidth=0.37)
            
            # Plot Bottom
            plt.subplot(2, len(q_id), len(q_id)+q_id.index(i)+1)
            plt.cla()
            plt.xlabel(x_label)
            if q_id.index(i)==0: 
                if dimension==1: plt.ylabel(y_label_bottom)
                else: plt.ylabel(y_label)
            if dimension==1: 
                plt.plot(x_var, map_bottom)
            elif dimension==2: 
                plt.pcolor(x_var, y_var, map_bottom)
            if axh:
                plt.axhline(h_center, color="k", linewidth=0.37)
            if axv:
                plt.axvline(v_center, color="k", linewidth=0.37)
        
        plt.tight_layout()
        plt.pause(0.1)

    if save_data == True:
        ###################
        #  Figure Saving  #
        ################### 
        figure = plt.gcf() # get current figure
        figure.set_size_inches(16, 8)
        plt.tight_layout()
        plt.savefig(f"{save_path}.png", dpi = 500)

        ###################
        #   .npz Saving   #
        ###################
        # NOTE: stage dependency:
        if stage == "6a":
            np.savez(save_path, I=I, Q=Q, ReadoutAmplitude=ReadoutAmplitude, F=Frequency, R=Amplitude, P=Phase)
    
    plt.show()

    

    return map_top, map_bottom


# Fitting:

# Fitting to cosine resonator frequency response
def cosine_func(x, amplitude, frequency, phase, offset):
    return amplitude * np.cos(2 * np.pi * frequency * x + phase) + offset

def fit_plotting(x_range, y_range, q_id, stage):
    if stage=="6b":
        minima = np.zeros(len(x_range)) # Array for the flux minima
        # Frequency range for the 3 resonators
        frequencies = [(y_range + resonator_IF[i]) for i in q_id]
        # Amplitude for the 3 resonators
        R = [R1, R2, R3]
        plt.figure()
        for rr in q_id:
            print(f"Resonator rr{rr+1}")
            # Find the resonator frequency vs flux minima
            for i in range(len(x_range)):
                minima[i] = frequencies[q_id.index(rr)][np.argmin(R[rr].T[i])]

            # Cosine fit
            initial_guess = [1, 0.5, 0, 0]  # Initial guess for the parameters
            fit_params, _ = curve_fit(cosine_func, x_range, minima, p0=initial_guess)

            # Get the fitted values
            amplitude_fit, frequency_fit, phase_fit, offset_fit = fit_params
            print("fitting parameters", fit_params)

            # Generate the fitted curve using the fitted parameters
            fitted_curve = cosine_func(x_range, amplitude_fit, frequency_fit, phase_fit, offset_fit)
            plt.subplot(3, 1, rr + 1)
            plt.pcolor(x_range, frequencies[rr] / u.MHz, R1)
            plt.plot(x_range, minima / u.MHz, "x-", color="red", label="Flux minima")
            plt.plot(x_range, fitted_curve / u.MHz, label="Fitted Cosine", color="orange")
            plt.xlabel("Flux bias [V]")
            plt.ylabel("Readout IF [MHz]")
            plt.title(f"Resonator rr{rr+1}")
            plt.legend()
            plt.tight_layout()
            plt.show()

            print(
                f"DC flux value corresponding to the maximum frequency point for resonator {rr}: {x_range[np.argmax(fitted_curve)]}"
            )
    


"""
        DRAG PULSE CALIBRATION (YALE METHOD)
The sequence consists in applying successively x180-y90 and y180-x90 to the qubit while varying the DRAG
coefficient alpha. The qubit is reset to the ground state between each sequence and its state is measured and stored.
Each sequence will bring the qubit to the same state only when the DRAG coefficient is set to its correct value.

This protocol is described in Reed's thesis (Fig. 5.8) https://rsl.yale.edu/sites/default/files/files/RSL_Theses/reed.pdf
This protocol was also cited in: https://doi.org/10.1103/PRXQuantum.2.040202

Prerequisites:
    - Having found the resonance frequency of the resonator coupled to the qubit under study (resonator_spectroscopy).
    - Having calibrated qubit pi pulse (x180) by running qubit, spectroscopy, rabi_chevron, power_rabi and updated the config.
    - (optional) Having calibrated the readout (readout_frequency, amplitude, duration_optimization IQ_blobs) for better SNR.
    - Set the DRAG coefficient to a non-zero value in the config: such as drag_coef = 1
    - Set the desired flux bias.

Next steps before going to the next node:
    - Update the DRAG coefficient (drag_coef) in the configuration.
"""

from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from configuration import *
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.loops import from_array
from macros import readout_macro
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

###################
# The QUA program #
###################


def DRAG_calibration_Yale( q_name, ro_element, multiplexed, config, qmm:QuantumMachinesManager, sequence_repeat:int=1, n_avg=100 ):
    a_min = 0
    a_max = 1.9
    da = 0.01
    amps = np.arange(a_min, a_max + da / 2, da)  # + da/2 to add a_max to amplitudes
    with program() as drag:
        n = declare(int)  # QUA variable for the averaging loop
        a = declare(fixed)  # QUA variable for the DRAG coefficient pre-factor
        I = declare(fixed)  # QUA variable for the measured 'I' quadrature
        Q = declare(fixed)  # QUA variable for the measured 'Q' quadrature
        state = declare(bool)  # QUA variable for the qubit state
        I1_st = declare_stream()  # Stream for the 'I' quadrature for the 1st sequence x180-y90
        Q1_st = declare_stream()  # Stream for the 'Q' quadrature for the 1st sequence x180-y90
        I2_st = declare_stream()  # Stream for the 'Q' quadrature for the 2nd sequence y180-x90
        Q2_st = declare_stream()  # Stream for the 'Q' quadrature for the 2nd sequence y180-x90
        state1_st = declare_stream()  # Stream for the qubit state for the 1st sequence x180-y90
        state2_st = declare_stream()  # Stream for the qubit state for the 2nd sequence y180-x90
        n_st = declare_stream()  # Stream for the averaging iteration 'n'
        
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(a, amps)):
                # Play the 1st sequence with varying DRAG coefficient
                for _ in range(sequence_repeat):
                    play("x180" * amp(1, 0, 0, a), q_name)
                    play("y90" * amp(a, 0, 0, 1), q_name)
                # Align the two elements to measure after playing the qubit pulses.
                align(q_name, ro_element)
                # Measure the resonator and extract the qubit state
                state, I, Q = readout_macro(ro_element, multiplexed, threshold=ge_threshold, state=state, I=I, Q=Q)
                # Wait for the qubit to decay to the ground state
                wait(thermalization_time * u.ns, ro_element)
                # Save the 'I' & 'Q' quadratures to their respective streams
                save(I, I1_st)
                save(Q, Q1_st)
                save(state, state1_st)

                align()  # Global align between the two sequences

                # Play the 2nd sequence with varying DRAG coefficient
                for _ in range(sequence_repeat):
                    play("y180" * amp(a, 0, 0, 1), q_name)
                    play("x90" * amp(1, 0, 0, a), q_name)
                # Align the two elements to measure after playing the qubit pulses.
                align(q_name, ro_element)
                # Measure the resonator and extract the qubit state
                state, I, Q = readout_macro(ro_element, multiplexed, threshold=ge_threshold, state=state, I=I, Q=Q)
                # Wait for the qubit to decay to the ground state
                wait(thermalization_time * u.ns, ro_element)
                # Save the 'I' & 'Q' quadratures to their respective streams
                save(I, I2_st)
                save(Q, Q2_st)
                save(state, state2_st)
            save(n, n_st)

        with stream_processing():
            # Cast the data into a 1D vector, average the 1D vectors together and store the results on the OPX processor
            I1_st.buffer(len(amps)).average().save("I1")
            Q1_st.buffer(len(amps)).average().save("Q1")
            I2_st.buffer(len(amps)).average().save("I2")
            Q2_st.buffer(len(amps)).average().save("Q2")
            state1_st.boolean_to_int().buffer(len(amps)).average().save("state1")
            state2_st.boolean_to_int().buffer(len(amps)).average().save("state2")
            n_st.save("iteration")

    ###########################
    # Run or Simulate Program #
    ###########################
    simulate = False

    if simulate:
        # Simulates the QUA program for the specified duration
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, drag, simulation_config)
        job.get_simulated_samples().con1.plot()

    else:
        # Open the quantum machine
        qm = qmm.open_qm(config)
        # Send the QUA program to the OPX, which compiles and executes it
        job = qm.execute(drag)
        # Get results from QUA program
        results = fetching_tool(job, data_list=["I1", "I2", "Q1", "Q2", "state1", "state2", "iteration"], mode="live")
        # Live plotting
        fig = plt.figure()
        interrupt_on_close(fig, job)  # Interrupts the job when closing the figure

        while results.is_processing():
            # Fetch results
            I1, I2, Q1, Q2, state1, state2, iteration = results.fetch_all()
            # Convert the results into Volts
            I1, Q1 = u.demod2volts(I1, readout_len), u.demod2volts(Q1, readout_len)
            I2, Q2 = u.demod2volts(I2, readout_len), u.demod2volts(Q2, readout_len)
            # Progress bar
            progress_counter(iteration, n_avg, start_time=results.get_start_time())
            # Find optimal points:
            drag_coef_opt = amps[np.argmin(np.abs(state1-state2))] * drag_coef
            # Plot results
            plt.suptitle(f"DRAG coefficient calibration (Yale): {drag_coef_opt:.4f}")
            plt.subplot(221)
            plt.cla()
            plt.plot(amps * drag_coef, I1, label="x180y90")
            plt.plot(amps * drag_coef, I2, label="y180x90")
            plt.ylabel("I [V]")
            plt.legend()
            plt.axvline(drag_coef, color='r', linewidth=0.37)
            plt.subplot(222)
            plt.cla()
            plt.plot(amps * drag_coef, Q1, label="x180y90")
            plt.plot(amps * drag_coef, Q2, label="y180x90")
            plt.ylabel("Q [V]")
            plt.legend()
            plt.subplot(223)
            plt.cla()
            plt.plot(amps * drag_coef, state1, label="x180y90")
            plt.plot(amps * drag_coef, state2, label="y180x90")
            plt.xlabel("Drag coefficient")
            plt.ylabel("g-e transition probability")
            plt.legend()
            plt.axvline(drag_coef, color='r', linewidth=0.37)
            plt.subplot(224)
            plt.cla()
            plt.plot(amps * drag_coef, np.abs(state1-state2), label="|x180y90-y180x90|", color='black')
            plt.xlabel("Drag coefficient")
            plt.ylabel("Find the lowest probability")
            plt.legend()
            plt.axvline(drag_coef, color='r', linewidth=0.57)
            plt.axvline(drag_coef_opt, color='b', linewidth=0.57)

            plt.tight_layout()
            plt.pause(0.1)

        # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
        qm.close()

def amp_calibration( amp_modify_range, q_name, ro_element, multiplexed, config, qmm:QuantumMachinesManager, sequence_repeat:int=1, n_avg=100 ):
    a_min = 1-amp_modify_range
    a_max = 1+amp_modify_range
    da = amp_modify_range/20
    n_pi = sequence_repeat *2
    n_90 = sequence_repeat *4
    amps = np.arange(a_min, a_max + da / 2, da)  # + da/2 to add a_max to amplitudes
    with program() as drag:
        n = declare(int)  # QUA variable for the averaging loop
        a = declare(fixed)  # QUA variable for the DRAG coefficient pre-factor
        I = declare(fixed)  # QUA variable for the measured 'I' quadrature
        Q = declare(fixed)  # QUA variable for the measured 'Q' quadrature
        state = declare(bool)  # QUA variable for the qubit state
        I1_st = declare_stream()  # Stream for the 'I' quadrature for the 1st sequence x180-y90
        Q1_st = declare_stream()  # Stream for the 'Q' quadrature for the 1st sequence x180-y90
        I2_st = declare_stream()  # Stream for the 'Q' quadrature for the 2nd sequence y180-x90
        Q2_st = declare_stream()  # Stream for the 'Q' quadrature for the 2nd sequence y180-x90
        state1_st = declare_stream()  # Stream for the qubit state for the 1st sequence x180-y90
        state2_st = declare_stream()  # Stream for the qubit state for the 2nd sequence y180-x90
        n_st = declare_stream()  # Stream for the averaging iteration 'n'
        
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(a, amps)):
                # Play the 1st sequence with varying DRAG coefficient
                for _ in range(n_90):
                    play("x90" * amp(a), q_name)
                # Align the two elements to measure after playing the qubit pulses.
                align(q_name, ro_element)
                # Measure the resonator and extract the qubit state
                state, I, Q = readout_macro(ro_element, multiplexed, threshold=ge_threshold, state=state, I=I, Q=Q)
                # Wait for the qubit to decay to the ground state
                wait(thermalization_time * u.ns, ro_element)
                # Save the 'I' & 'Q' quadratures to their respective streams
                save(I, I1_st)
                save(Q, Q1_st)
                save(state, state1_st)

                align()  # Global align between the two sequences

                # Play the 2nd sequence with varying DRAG coefficient
                for _ in range(n_pi):
                    play("x180" * amp(a), q_name)
                # Align the two elements to measure after playing the qubit pulses.
                align(q_name, ro_element)
                # Measure the resonator and extract the qubit state
                state, I, Q = readout_macro(ro_element, multiplexed, threshold=ge_threshold, state=state, I=I, Q=Q)
                # Wait for the qubit to decay to the ground state
                wait(thermalization_time * u.ns, ro_element)
                # Save the 'I' & 'Q' quadratures to their respective streams
                save(I, I2_st)
                save(Q, Q2_st)
                save(state, state2_st)
                
            save(n, n_st)

        with stream_processing():
            # Cast the data into a 1D vector, average the 1D vectors together and store the results on the OPX processor
            I1_st.buffer(len(amps)).average().save("I1")
            Q1_st.buffer(len(amps)).average().save("Q1")
            I2_st.buffer(len(amps)).average().save("I2")
            Q2_st.buffer(len(amps)).average().save("Q2")
            state1_st.boolean_to_int().buffer(len(amps)).average().save("state1")
            state2_st.boolean_to_int().buffer(len(amps)).average().save("state2")
            n_st.save("iteration")

    ###########################
    # Run or Simulate Program #
    ###########################
    simulate = False

    if simulate:
        # Simulates the QUA program for the specified duration
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, drag, simulation_config)
        job.get_simulated_samples().con1.plot()
        job.get_simulated_samples().con1.plot()
        plt.show()

    else:
        # Open the quantum machine
        qm = qmm.open_qm(config)
        # Send the QUA program to the OPX, which compiles and executes it
        job = qm.execute(drag)
        # Get results from QUA program
        results = fetching_tool(job, data_list=["I1", "I2", "Q1", "Q2", "state1", "state2", "iteration"], mode="live")
        # Live plotting
        fig = plt.figure()
        interrupt_on_close(fig, job)  # Interrupts the job when closing the figure

        while results.is_processing():
            # Fetch results
            I1, I2, Q1, Q2, state1, state2, iteration = results.fetch_all()
            # Convert the results into Volts
            I1, Q1 = u.demod2volts(I1, readout_len), u.demod2volts(Q1, readout_len)
            I2, Q2 = u.demod2volts(I2, readout_len), u.demod2volts(Q2, readout_len)
            # Progress bar
            progress_counter(iteration, n_avg, start_time=results.get_start_time())
            # Find optimal points:
            x90_opt = amps[np.argmin(I1)]
            x180_opt = amps[np.argmin(I2)]
            # Plot results
            plt.suptitle("Amp pre factor calibration (AS)")
            plt.subplot(311)
            plt.cla()
            plt.plot(amps, I1, label="x90x90")
            plt.plot(amps, I2, label="x180x180")
            plt.axvline(x90_opt, color='b', linewidth=0.371)
            plt.axvline(x180_opt, color='r', linewidth=0.371)
            plt.title(f"x180_opt: {x180_opt:.5f}, x90_opt: {x90_opt:.5f}")
            plt.ylabel("I [V]")
            plt.legend()

            plt.subplot(312)
            plt.cla()
            plt.plot(amps, Q1, label="x90x90")
            plt.plot(amps, Q2, label="x180x180")
            plt.ylabel("Q [V]")
            plt.legend()

            plt.subplot(313)
            plt.cla()
            plt.plot(amps, state1, label="x90x90")
            plt.plot(amps, state2, label="x180x180")
            # plt.plot(amps * drag_coef, state2, label="y180x90")
            plt.xlabel("amp pre factor")
            plt.ylabel("g-e transition probability")
            plt.legend()
            plt.tight_layout()
            plt.pause(1)

        # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
        qm.close()
if __name__ == '__main__':
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
    n_avg = 20000
    qubit = 2
    multiplexed = [1,2,3,4,5]
    mode = "amp"

    # Scan the DRAG coefficient pre-factor

    drag_coef = eval(f"drag_coef_q{qubit}")
    ge_threshold = eval(f"ge_threshold_q{qubit}")
    # Check that the DRAG coefficient is not 0
    assert drag_coef != 0, "The DRAG coefficient 'drag_coef' must be different from 0 in the config."
    sequence_repeat = 35 # 5, 15, 25, 35
    prefactor_range = 0.7/sequence_repeat
    match mode.lower():
        case "drag":
            DRAG_calibration_Yale( f"q{qubit}_xy", f"rr{qubit}", multiplexed, config, qmm, n_avg=n_avg)
        case "amp":
            amp_calibration( prefactor_range, f"q{qubit}_xy", f"rr{qubit}", multiplexed, config, qmm, n_avg=n_avg, sequence_repeat=sequence_repeat)
    plt.show()
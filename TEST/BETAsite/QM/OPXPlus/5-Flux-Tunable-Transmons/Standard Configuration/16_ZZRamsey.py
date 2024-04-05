"""
        RAMSEY WITH VIRTUAL Z ROTATIONS
The program consists in playing a Ramsey sequence (x90 - idle_time - x90 - measurement) for different idle times.
Instead of detuning the qubit gates, the frame of the second x90 pulse is rotated (de-phased) to mimic an accumulated
phase acquired for a given detuning after the idle time.
This method has the advantage of playing resonant gates.

From the results, one can fit the Ramsey oscillations and precisely measure the qubit resonance frequency and T2*.

Prerequisites:
    - Having found the resonance frequency of the resonator coupled to the qubit under study (resonator_spectroscopy).
    - Having calibrated qubit pi pulse (x180) by running qubit, spectroscopy, rabi_chevron, power_rabi and updated the config.
    - (optional) Having calibrated the readout (readout_frequency, amplitude, duration_optimization IQ_blobs) for better SNR.
    - Set the desired flux bias.

Next steps before going to the next node:
    - Update the qubit frequency (qubit_IF_q) in the configuration.
"""

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from configuration import *
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.plot import interrupt_on_close
from macros import qua_declaration, multiplexed_readout
from qualang_tools.plot.fitting import Fit
import warnings

warnings.filterwarnings("ignore")


###################
# The QUA program #
###################
n_avg = 100000  # Number of averages
X = False
control, target = 1,2

detuning = -2.00e6 # "Virtual" detuning in Hz
multiplexed = [1,2,3,4,5]
the_rest = [x for x in multiplexed if x not in [control,target]]

DD_even = False # for circuit implementation
DD_cycle = 0 # push T2, avoid zz-coupling

# Idle time sweep in clock cycles (Needs to be a list of integers)
if X: idle_times = np.arange(4, 1000, 1)
else: 
    if DD_even: idle_times = np.arange(0, 2000*DD_cycle, 3**(DD_cycle + 0))
    else: idle_times = np.arange(0, 1000, 2**(DD_cycle + 1))
    print(f"First 3 idle-times: {idle_times[0:3]} clock cycles")


with program() as ramsey:
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=len(multiplexed))
    t = declare(int)  # QUA variable for the idle time
    phi = declare(fixed)  # Phase to apply the virtual Z-rotation

    with for_(n, 0, n < n_avg, n + 1):
        with for_(*from_array(t, idle_times)):
            # Rotate the frame of the second x90 gate to implement a virtual Z-rotation
            # 4*tau because tau was in clock cycles and 1e-9 because tau is ns
            assign(phi, Cast.mul_fixed_by_int(detuning * 1e-9, 4 * t))
            align()

            # Qubit a
            if X:
                play("x180", "q%s_xy"%control)  # Conditional x180 gate
                align()

            # Qubit b
            play("x90", "q%s_xy"%target)  # 1st x90 gate

            if DD_even: # even Pi: circuit implementation 
                wait(t/(3**DD_cycle), "q%s_xy"%target)
                for i in range(3**DD_cycle-1):
                    play("y180", "q%s_xy"%target)  # DD sequence
                    wait(t/(3**DD_cycle), "q%s_xy"%target)
                    # print("Between echo: %s clock cycles" %(t/(3**DD_cycle)))

            else: # odd Pi: usual echo
                wait(t/(2**DD_cycle), "q%s_xy"%target)
                for i in range(2**DD_cycle-1):
                    play("y180", "q%s_xy"%target)  # DD sequence
                    wait(t/(2**DD_cycle), "q%s_xy"%target)

            frame_rotation_2pi(phi, "q%s_xy"%target)  # Virtual Z-rotation
            play("x90", "q%s_xy"%target)  # 2nd x90 gate

            # Align the elements to measure after having waited a time "tau" after the qubit pulses.
            align()
            # Measure the state of the resonators
            multiplexed_readout(I, I_st, Q, Q_st, resonators=multiplexed, weights="rotated_")
            # Reset the frame of the qubit in order not to accumulate rotations
            reset_frame("q%s_xy"%control)
            reset_frame("q%s_xy"%target)

            wait(thermalization_time * u.ns)

        # Save the averaging iteration to get the progress bar
        save(n, n_st)

    with stream_processing():
        n_st.save("n")
        # control:
        I_st[multiplexed.index(control)].buffer(len(idle_times)).average().save("I1")
        Q_st[multiplexed.index(control)].buffer(len(idle_times)).average().save("Q1")
        # target:
        I_st[multiplexed.index(target)].buffer(len(idle_times)).average().save("I2")
        Q_st[multiplexed.index(target)].buffer(len(idle_times)).average().save("Q2")
        # the rest:
        for i,k in enumerate(the_rest):
            I_st[multiplexed.index(k)].buffer(len(idle_times)).average().save(f"I{3+i}")
            Q_st[multiplexed.index(k)].buffer(len(idle_times)).average().save(f"Q{3+i}")

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
    job = qmm.simulate(config, ramsey, simulation_config)
    job.get_simulated_samples().con1.plot()
    job.get_simulated_samples().con2.plot()
    plt.show()

else:
    # Open the quantum machine
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(ramsey)
    # Prepare the figure for live plotting
    fig = plt.figure()
    interrupt_on_close(fig, job)
    # Tool to easily fetch results from the OPX (results_handle used in it)
    results = fetching_tool(job, ["n", "I1", "Q1", "I2", "Q2", "I3", "Q3", "I4", "Q4", "I5", "Q5"], mode="live")
    # Live plotting
    while results.is_processing():
        # Fetch results
        n, I1, Q1, I2, Q2, I3, Q3, I4, Q4, I5, Q5 = results.fetch_all()
        # Convert the results into Volts
        I1, Q1 = u.demod2volts(I1, readout_len), u.demod2volts(Q1, readout_len)
        I2, Q2 = u.demod2volts(I2, readout_len), u.demod2volts(Q2, readout_len)
        I3, Q3 = u.demod2volts(I3, readout_len), u.demod2volts(Q3, readout_len)
        I4, Q4 = u.demod2volts(I4, readout_len), u.demod2volts(Q4, readout_len)
        I5, Q5 = u.demod2volts(I5, readout_len), u.demod2volts(Q5, readout_len)
        # Progress bar
        progress_counter(n, n_avg, start_time=results.start_time)
        # Plot
        plt.subplot(2,3,1)
        plt.cla()
        plt.plot(4 * idle_times, I1)
        plt.ylabel("I quadrature [V]")
        plt.title("Control: q%s (X=%s)" %(control,int(X)))
        plt.subplot(2,3,4)
        plt.cla()
        plt.plot(4 * idle_times, Q1)
        plt.ylabel("Q quadrature [V]")
        plt.xlabel("Idle times [ns]")
        plt.subplot(2,3,2)
        plt.cla()
        plt.plot(4 * idle_times, I2)
        plt.title("Target: q%s" %target)
        plt.subplot(2,3,5)
        plt.cla()
        plt.plot(4 * idle_times, Q2)
        plt.title("Target-Q")
        plt.xlabel("Idle times [ns]")

        plt.subplot(2,3,3)
        plt.cla()
        plt.plot(4 * idle_times, I3, 'b')
        plt.plot(4 * idle_times, I4, 'r')
        plt.plot(4 * idle_times, I5, 'g')
        plt.title("Others: q%s,%s,%s" %(the_rest[0],the_rest[1],the_rest[2]))
        plt.subplot(2,3,6)
        plt.cla()
        plt.plot(4 * idle_times, Q3, 'b')
        plt.plot(4 * idle_times, Q4, 'r')
        plt.plot(4 * idle_times, Q5, 'g')
        plt.title(f"q{the_rest[0],the_rest[1],the_rest[2]}-Q")
        plt.xlabel("Idle times [ns]")
        
        plt.tight_layout()
        plt.pause(0.1)
    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    try:
        fit = Fit()
        plt.figure()
        plt.suptitle(f"ZZ-Ramsey measurement with detuning={detuning} Hz")
        
        # plt.subplot(2,2,1)
        # fit.ramsey(4 * idle_times, I1, plot=True)
        # plt.xlabel("Idle times [ns]")
        # plt.ylabel("I quadrature [V]")
        # plt.title("Control-I")
        # plt.subplot(2,2,3)
        # fit.ramsey(4 * idle_times, Q1, plot=True)
        # plt.xlabel("Idle times [ns]")
        # plt.ylabel("I quadrature [V]")
        # plt.title("Control-Q")

        plt.subplot(1,1,1)
        fitting_results = fit.ramsey(4 * idle_times, I2, plot=True)
        plt.xlabel("Idle times [ns]")
        plt.ylabel("I quadrature [V]")

        # plt.subplot(2,2,4)
        # fit.ramsey(4 * idle_times, Q2, plot=True)
        # plt.xlabel("Idle times [ns]")
        # plt.ylabel("I quadrature [V]")

        plt.tight_layout()
        plt.show()
        if detuning > 0:
            print("f01-correction: %.3f MHz" %((detuning - fitting_results['f'][0]*1e9)/u.MHz) )
        elif detuning < 0:
            print("f01-correction: %.3f MHz" %((detuning + fitting_results['f'][0]*1e9)/u.MHz) )
    except (Exception,) as e:
        print(e)

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
from RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
from qualang_tools.plot.fitting import Fit
import warnings

warnings.filterwarnings("ignore")
from qualang_tools.units import unit


#######################
# AUXILIARY FUNCTIONS #
#######################
u = unit(coerce_to_integer=True)

###################
# The QUA program #
###################

def Ramsey_freq_calibration( virtial_detune_freq, q_name:list, ro_element:list, config, qmm:QuantumMachinesManager, n_avg:int=100, simulate=False, xscale:int=1 ):
    """
    Use positive and nagative detuning refence to freq in config to get measured ramsey oscillation frequency.
    evo_time unit is tick (4ns)
    virtial_detune_freq unit in MHz can't larger than 2
    """
    point_per_period = 20
    Ramsey_period = (1e3/virtial_detune_freq)* u.ns
    tick_resolution = (Ramsey_period//(4*point_per_period))
    evo_time_tick_max = tick_resolution *point_per_period *5 *xscale
    evo_time_tick = np.arange( 4, evo_time_tick_max, tick_resolution)
    evo_time = evo_time_tick*4
    time_len = len(evo_time)
    with program() as ramsey:
        iqdata_stream = multiRO_declare( ro_element )
        n = declare(int)
        n_st = declare_stream()
        t = declare(int)  # QUA variable for the idle time
        phi = declare(fixed)  # Phase to apply the virtual Z-rotation
        phi_idx = declare(int)
        with for_(n, 0, n < n_avg, n + 1):
            with for_each_( phi_idx, [-1, 1]):
                with for_(*from_array(t, evo_time_tick)):

                    # Rotate the frame of the second x90 gate to implement a virtual Z-rotation
                    # 4*tau because tau was in clock cycles and 1e-9 because tau is ns
                    
                    # Init
                    if not simulate: wait(thermalization_time * u.ns)

                    align()
                    # Operation
                    with switch_(phi_idx, unsafe=True):
                        with case_(1):
                            assign(phi, Cast.mul_fixed_by_int(virtial_detune_freq * 1e-3, 4 * t))
                        with case_(-1):
                            assign(phi, Cast.mul_fixed_by_int(-virtial_detune_freq * 1e-3, 4 * t))

                    for q in q_name:
                        play("x90", q)  # 1st x90 gate

                    for q in q_name:
                        wait(t, q)

                    for q in q_name:
                        frame_rotation_2pi(phi, q)  # Virtual Z-rotation
                        play("x90", q)  # 2st x90 gate

                    # Align after playing the qubit pulses.
                    align()
                    # Readout
                    multiRO_measurement(iqdata_stream, ro_element, weights="rotated_")         
                

            # Save the averaging iteration to get the progress bar
            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            multiRO_pre_save(iqdata_stream, ro_element, (2,time_len) )

    ###########################
    # Run or Simulate Program #
    ###########################


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
        # Get results from QUA program
        ro_ch_name = []
        for r_name in ro_element:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")
        data_list = ro_ch_name + ["iteration"]   
        results = fetching_tool(job, data_list=data_list, mode="live")
        # Live plotting

        fig, ax = plt.subplots(2, len(ro_element))
        interrupt_on_close(fig, job)  # Interrupts the job when closing the figure

        # Live plotting
        while results.is_processing():
            # Fetch results
            fetch_data = results.fetch_all()
            fig.suptitle(f"Frequency calibration ({fetch_data[-1]}/{n_avg})")
            output_data = {}
            for r_idx, r_name in enumerate(ro_element):
                ax[0][r_idx].cla()
                ax[1][r_idx].cla()
                output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])
                
                # Plot I
                ax[0][r_idx].set_ylabel("I quadrature [V]")
                plot_dual_Ramsey_oscillation(evo_time, output_data[r_name][0], ax[0][r_idx])
                # Plot Q
                ax[1][r_idx].set_ylabel("Q quadrature [V]")
                plot_dual_Ramsey_oscillation(evo_time, output_data[r_name][1], ax[1][r_idx])

    
            # Progress bar
            iteration = fetch_data[-1]
            progress_counter(iteration, n_avg, start_time=results.start_time)
            # Plot
            plt.tight_layout()
            plt.pause(0.1)
        # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
        qm.close()
        return output_data, evo_time
        # try:
        #     fit = Fit()
        #     plt.figure()
        #     plt.suptitle(f"ZZ-Ramsey measurement with detuning={detuning} Hz")
        #     plt.subplot(221)
        #     fit.ramsey(evo_time, I1, plot=True)
        #     plt.xlabel("Idle times [ns]")
        #     plt.ylabel("I quadrature [V]")
        #     plt.title("Control-I")
        #     plt.subplot(223)
        #     fit.ramsey(evo_time, Q1, plot=True)
        #     plt.xlabel("Idle times [ns]")
        #     plt.ylabel("I quadrature [V]")
        #     plt.title("Control-Q")
        #     plt.subplot(222)
        #     fitting_results = fit.ramsey(evo_time, I2, plot=True)
        #     plt.xlabel("Idle times [ns]")
        #     plt.ylabel("I quadrature [V]")
        #     plt.subplot(224)
        #     fit.ramsey(4 * idle_times, Q2, plot=True)
        #     plt.xlabel("Idle times [ns]")
        #     plt.ylabel("I quadrature [V]")
        #     plt.tight_layout()
        #     print("Detuned: %s" %(fitting_results['f'][0]*1e9*u.MHz - detuning))
        # except (Exception,) as e:
        #     print(e)
        
        # if save_data == True:
        #     ###################
        #     #  Figure Saving  #
        #     ################### 
        #     figure = plt.gcf() # get current figure
        #     figure.set_size_inches(16, 8)
        #     plt.tight_layout()
        #     plt.pause(0.1)
        #     plt.savefig(f"{save_path}.png", dpi = 500)
        # plt.show()
def plot_dual_Ramsey_oscillation( x, y, ax=None ):
    """
    y in shape (2,N)
    2 is postive and negative
    N is evo_time_point
    """
    if ax == None:
        fig, ax = plt.subplots()
    ax.plot(x, y[0], "-",label="positive")
    ax.plot(x, y[1], "-",label="negative")
    ax.set_xlabel("Free Evolution Times [ns]")
    ax.legend()

    if ax == None:
        return fig
    
def plot_ana_result( evo_time, data, detuning, ax=None ):
    """
    data in shape (2,N)
    2 is postive and negative
    N is evo_time_point
    """
    if ax == None:
        fig, ax = plt.subplots()
    fit = Fit()
    plot_dual_Ramsey_oscillation(evo_time, data, ax)
    ax.set_title(f"ZZ-Ramsey measurement with virtual detuning {detuning} MHz")

    ana_dict_pos = fit.ramsey(evo_time, data[0], plot=False)
    ana_dict_neg = fit.ramsey(evo_time, data[1], plot=False)

    ax.set_xlabel("Idle times [ns]")

    freq_pos = ana_dict_pos['f'][0]*1e3
    freq_neg = ana_dict_neg['f'][0]*1e3
    ax.plot(evo_time, ana_dict_pos["fit_func"](evo_time), label=f"Positive freq: {freq_pos:.3f} MHz")
    ax.plot(evo_time, ana_dict_neg["fit_func"](evo_time), label=f"Negative freq: {freq_neg:.3f} MHz")
    ax.text(0.07, 0.9, f"Real Detuning freq : {(freq_pos-freq_neg)/2:.3f}", fontsize=10, transform=ax.transAxes)

    ax.legend()
    plt.tight_layout()

if __name__ == '__main__':
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
    n_avg = 2000  # Number of averages

    qubit_select = [5]
    ro_element = ["rr1","rr2","rr3","rr4","rr5"]
    q_name =  [f"q{x}_xy" for x in qubit_select]
    virtual_detune = 2 # Unit in MHz
    output_data, evo_time = Ramsey_freq_calibration( virtual_detune, q_name, ro_element, config, qmm, n_avg=n_avg, simulate=False, xscale=1)
    #   Data Saving   # 
    save_data = False
    if save_data == True:
        from save_data import save_npz
        import sys
        save_progam_name = sys.argv[0].split('\\')[-1].split('.')[0]  # get the name of current running .py program
        save_npz(save_dir, save_progam_name, output_data)

    # for r in ro_element:
    plot_ana_result(evo_time,output_data[f"rr{qubit_select[0]}"][0],virtual_detune)
    # # Plot
    plt.show()
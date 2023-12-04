"""
        TIME RABI
The sequence consists in playing the qubit pulse and measuring the state of the resonator
for different qubit pulse durations.
The results are then post-processed to find the qubit pulse duration for the chosen amplitude.

Prerequisites:
    - Having found the resonance frequency of the resonator coupled to the qubit under study (resonator_spectroscopy).
    - Having calibrated the IQ mixer connected to the qubit drive line (external mixer or Octave port)
    - Having found the rough qubit frequency and pi pulse amplitude (rabi_chevron_amplitude or power_rabi).
    - Set the qubit frequency and desired pi pulse amplitude (pi_amp_q) in the configuration.
    - Set the desired flux bias

Next steps before going to the next node:
    - Update the qubit pulse duration (pi_len_q) in the configuration.
"""

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
import sys
import pathlib
QM_script_root = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(QM_script_root)
from configuration import *
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
from macros import cz_gate
from RO_macros import state_tomo_singleRO_declare, tomo_pre_save_singleShot, state_tomo_measurement, tomo_NQ_proj
import warnings

warnings.filterwarnings("ignore")

###################
# The QUA program #
###################


def state_tomography( q_name, ro_element, prepare_state, n_avg, config, qmm:QuantumMachinesManager, simulate:bool=True):
    """
    1Q only
    """    
    with program() as tomo:
        iqdata_stream = state_tomo_singleRO_declare( ro_element )
        n = declare(int)  # QUA variable for the qubit pulse duration
        n_st = declare_stream()

        with for_(n, 0, n < n_avg, n + 1):

            state_tomo_measurement( iqdata_stream, prepare_state, q_name, ro_element, weights="rotated_", thermalization_time= 200)

            # Wait for the qubit to decay to the ground state
            # Save the averaging iteration to get the progress bar
            save(n, n_st)

        with stream_processing():
            n_st.save("n")
            tomo_pre_save_singleShot( iqdata_stream, q_name, ro_element )

    ###########################
    # Run or Simulate Program #
    ###########################
    if simulate:
        # Simulates the QUA program for the specified duration
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, tomo, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()

    else:
        # Open the quantum machine
        qm = qmm.open_qm(config)
        # Send the QUA program to the OPX, which compiles and executes it
        job = qm.execute(tomo)

        data_list = []
        projection_type = ["x", "y", "z"]

        for r in ro_element:
            data_list.append(f"{r}_I")
            data_list.append(f"{r}_Q")

        # Tool to easily fetch results from the OPX (results_handle used in it)
        results = fetching_tool(job, data_list, mode="wait_for_all")
        fetch_data = results.fetch_all()
        output_data = {}
        for r_idx, r_name in enumerate(ro_element):
            # output_data[r_name] = np.array(
            #     [[fetch_data[0][r_idx*3], fetch_data[0][r_idx*3+1],fetch_data[0][r_idx*3+2]],
            #      [fetch_data[1][r_idx*3], fetch_data[1][r_idx*3+1],fetch_data[1][r_idx*3+2]]])
            output_data[r_name] = np.array(fetch_data)
        # Live plotting
    
        # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
        qm.close()
        return output_data


def state_tomography_NQ( q_name, ro_element, prepare_state, n_avg, config, qmm:QuantumMachinesManager, simulate:bool=True):
    """
    For N-Q
    """ 
    with program() as tomo:
        iqdata_stream = state_tomo_singleRO_declare( ro_element )
        n = declare(int)  # QUA variable for the qubit pulse duration
        n_st = declare_stream()

        with for_(n, 0, n < n_avg, n + 1):

            tomo_NQ_proj( iqdata_stream, prepare_state, q_name, ro_element, weights="rotated_", thermalization_time=thermalization_time)

            # Wait for the qubit to decay to the ground state
            # Save the averaging iteration to get the progress bar
            save(n, n_st)

        with stream_processing():
            n_st.save("n")
            tomo_pre_save_singleShot( iqdata_stream, q_name, ro_element )

    ###########################
    # Run or Simulate Program #
    ###########################
    if simulate:
        # Simulates the QUA program for the specified duration
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, tomo, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()

    else:
        # Open the quantum machine
        qm = qmm.open_qm(config)
        # Send the QUA program to the OPX, which compiles and executes it
        job = qm.execute(tomo)

        data_list = []
        projection_type = ["x", "y", "z"]

        for r in ro_element:
            data_list.append(f"{r}_I")
            data_list.append(f"{r}_Q")

        # Tool to easily fetch results from the OPX (results_handle used in it)
        results = fetching_tool(job, data_list, mode="wait_for_all")
        fetch_data = results.fetch_all()
        output_data = {}
        for r_idx, r_name in enumerate(ro_element):
            # output_data[r_name] = np.array(
            #     [[fetch_data[0][r_idx*3], fetch_data[0][r_idx*3+1],fetch_data[0][r_idx*3+2]],
            #      [fetch_data[1][r_idx*3], fetch_data[1][r_idx*3+1],fetch_data[1][r_idx*3+2]]])
            output_data[r_name] = np.array(fetch_data)
        # Live plotting
    
        # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
        qm.close()
        return output_data

def calculate_block_vector( data, threshold ):
    vect_dis = []
    dirction = ["z", "x", "y"]
    total_count = data.shape[-1]
    for idx, dir in enumerate(dirction):
        count_0 = np.count_nonzero(data[idx] < threshold)
        pop_0 = count_0/total_count
        print(f"{dir} g count {total_count}, {pop_0}")

        pop_1 = 1-pop_0
        vect_dis.append(pop_0-pop_1)
    vect_dis = [vect_dis[1],vect_dis[2],vect_dis[0]]
    return vect_dis

def plot_block_vector( vect_dis, fig=None ):
    from qutip import Bloch
    if fig == None:
        fig = Bloch()
    fig.add_vectors(vect_dis)
    return fig

if __name__ == '__main__':
    ro_element = ["rr1","rr2","rr3","rr4","rr5"] #"rr1","rr2","rr3",
    n_avg = 1000
    q_name = ["q3_xy","q4_xy","q5_xy"]
    threshold = ge_threshold_q1

    #####################################
    #  Open Communication with the QOP  #
    #####################################e4
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

    def prepare_state():

        # play("x180", "q4_xy" )
        # play("x180", "q5_xy" )

        align()
        play("y90", "q3_xy")

        # CX(3,4)
        play("-y90", "q4_xy")
        align()
        cz_gate(3, 4)
        frame_rotation_2pi(eval(f"cz{4}_{3}_2pi_dev"), "q4_xy")
        align()
        play("y90", "q4_xy")

        # CX(4,5)
        play("-y90", "q5_xy")
        align()
        cz_gate(4, 5)
        frame_rotation_2pi(eval(f"cz{5}_{4}_2pi_dev"), "q5_xy")
        align()
        play("y90", "q5_xy")

        align()
        # pass

    # data = state_tomography(q_name, ro_element, prepare_state, n_avg, config, qmm, False)
    # print(data)

    data = state_tomography_NQ(q_name, ro_element, prepare_state, n_avg, config, qmm, False)
    print(type(data),data.keys())

    np.savez("5Q_GHZ_5_4_3.npz",**data)
    data = np.load("5Q_GHZ_5_4_3.npz")
    for label in data.keys():
        print(data[label].shape)
    # Plot Bloch Sphere

    # data = data[ro_element[0]]
    # print(data.shape)

    # total_count = n_avg
    # print(f"total count {total_count}")
    # dirction = ["x","y","z"]
    # data_i = data[ro_element[0]][0].transpose()
    # data_q = data[ro_element[0]][1].transpose()
    # # plt.plot(data_i[0],data_q[0],'o')

    # vect_dis = calculate_block_vector(data_i, threshold)
    # block_plot = plot_block_vector(vect_dis)
    # block_plot.show()
    # plt.show()
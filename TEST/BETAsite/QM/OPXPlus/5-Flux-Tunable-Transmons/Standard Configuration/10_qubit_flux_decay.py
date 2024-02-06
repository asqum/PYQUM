
from qualang_tools.units import unit
u = unit(coerce_to_integer=True)
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
from qualang_tools.plot.fitting import Fit
from scipy.optimize import curve_fit
import warnings
from RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import config_par as gc
warnings.filterwarnings("ignore")

# Qi = 1 stands for Q1

def qubit_flux_decay(dfs,t_delay, q_name:list, ro_element:list, z_name:list,dc,config, qmm:QuantumMachinesManager, n_avg=100,initializer=None,simulate=False):
    """
    Return ductionary with value 2*N array
    N is t_delay length
    """
    ref_z_offset = {}
    for z in z_name:
        ref_z_offset[z] = gc.get_offset(z, config)
    ref_xy_IF = {}
    for xy in q_name:
        ref_xy_IF[xy] = gc.get_IF(xy, config)
    evo_time_len = t_delay.shape[-1]
    freq_len = len(dfs)
    # QUA program
    with program() as decay_time:

        iqdata_stream = multiRO_declare( ro_element )
        t = declare(int)  
        n = declare(int)
        df = declare(int)
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(df, dfs)):
                with for_(*from_array(t, t_delay)):
                    # Init
                    if initializer is None:
                        wait(100*u.us)
                        #wait(thermalization_time * u.ns)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            print("Initializer didn't work!")
                            wait(100*u.us)
                    for q in q_name:
                        update_frequency(q, ref_xy_IF[q]+df)
                    # Operation
                    for z in z_name:
                        wait(50,z)
                    for q in q_name:
                        wait(t,q)
                        play("x180", q)
                    for z in z_name:
                        set_dc_offset(z, "single", ref_z_offset[z]+dc)
                    wait(125)
                    #align()
                    for z in z_name:
                        set_dc_offset(z, "single", ref_z_offset[z])
                        wait(50,z)
                    align()
                    
                    
                    # Readout
                    multiRO_measurement( iqdata_stream,  resonators=ro_element, weights="rotated_")
                
            # Save the averaging iteration to get the progress bar
            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            multiRO_pre_save(iqdata_stream, ro_element, (freq_len,evo_time_len) )
    if simulate:
        simulation_config = SimulationConfig(duration=150000)  # In clock cycles = 4ns
        job = qmm.simulate(config, decay_time, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(decay_time)
        
        fig, ax = plt.subplots(2, len(ro_element))
        if len(ro_element) == 1:
            ax = [[ax[0]],[ax[1]]]
        interrupt_on_close(fig, job)
        ro_ch_name = []
        for r_name in ro_element:
            ro_ch_name.append(f"{r_name}_I")
            ro_ch_name.append(f"{r_name}_Q")

        data_list = ro_ch_name + ["iteration"]   

        results = fetching_tool(job, data_list=data_list, mode="live")
        output_data = {}
        while results.is_processing():
            fetch_data = results.fetch_all()
            for r_idx, r_name in enumerate(ro_element):
                ax[0][r_idx].cla()
                ax[1][r_idx].cla()
                output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])
                plot_qubit_flux_decay(output_data[r_name], dfs, t_delay, [ax[0][r_idx],ax[1][r_idx]])
            iteration = fetch_data[-1]
            # Progress bar
            progress_counter(iteration, n_avg, start_time=results.get_start_time()) 

            plt.pause(1)

        fetch_data = results.fetch_all()
        output_data = {}
        for r_idx, r_name in enumerate(ro_element):
            output_data[r_name] = np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]])

        qm.close()
        return output_data

def plot_qubit_flux_decay( data, time, dfs, ax=None ):
    """
    data shape ( 2, N, M )
    2 is I,Q
    N is freq
    M is flux
    """
    idata = data[0]
    qdata = data[1]
    zdata = idata +1j*qdata
    s21 = zdata

    if type(ax)==None:
        fig, ax = plt.subplots()
        ax.set_title('pcolormesh')
        fig.show()
    ax[0].pcolormesh( dfs, time, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    ax[1].pcolormesh( dfs, time, np.angle(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)

def plot_ana_qubit_flux_decay( data, dfs, time, freq_LO, freq_IF, ax=None ):
    """
    data shape ( 2, N, M )
    2 is I,Q
    N is freq
    M is time
    """
    idata = data[0]
    qdata = data[1]
    zdata = idata +1j*qdata
    s21 = zdata

    abs_freq = freq_LO+freq_IF+dfs
    if type(ax)==None:
        fig, ax = plt.subplots()
        ax.set_title('pcolormesh')
        fig.show()
    ax[0].pcolormesh( time, abs_freq, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    # ax[0].axvline(x=freq_LO+freq_IF, color='b', linestyle='--', label='ref IF')
    # ax[0].axvline(x=freq_LO, color='r', linestyle='--', label='LO')
    ax[0].axhline(y=freq_LO+freq_IF, color='black', linestyle='--', label='ref IF')

    ax[0].legend()
    ax[1].pcolormesh( time, abs_freq, np.angle(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    ax[1].axhline(y=freq_LO+freq_IF, color='black', linestyle='--', label='ref IF')

    ax[1].legend()

if __name__ == '__main__':
    # from OnMachine.Octave_Config.QM_config_dynamic import Circuit_info, QM_config, initializer
    # from OnMachine.MeasFlow.ConfigBuildUp import spec_loca, config_loca, qubit_num
    # spec = Circuit_info(qubit_num)
    # config = QM_config()
    # spec.import_spec(spec_loca)
    # config.import_config(config_loca)
    # q_num = 5
    from configuration import *
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

    target_q = 'q3'

    # qmm, _ = spec.buildup_qmm()
    # init_macro = initializer((spec.give_WaitTime_with_q(target_q,5),),'wait')

    n_avg = 100
    tau_min = 16 // 4 # in clock cycles
    tau_max = 860 // 4  # in clock cycles
    d_tau = 4 // 4  # in clock cycles
    t_delay = np.arange(tau_min, tau_max + 0.1, d_tau)  # Linear sweep
    dfs = np.arange(-250e6, 100e6, 0.35e6)

    q_name = [f"{target_q}_xy"]
    ro_element = ["rr3"]
    z_name = [f"{target_q}_z"]
    dc=0.035
    output = qubit_flux_decay(dfs,t_delay,q_name,ro_element,z_name,dc,config,qmm,n_avg,initializer=None,simulate=False)
    plt.show()
    #Data Saving   #
    
    save_data = True
    if save_data:
        from save_data import save_npz
        import sys
        filename = f"qb_flux_decay_dr2a_q3"
        save_npz(save_dir, filename, output)
    


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
import warnings
from RO_macros import multiRO_declare, multiRO_measurement, multiRO_pre_save
import config_par as gc
warnings.filterwarnings("ignore")
import xarray as xr

# Qi = 1 stands for Q1

def qubit_flux_decay( flux_amp, freq_span:Union[tuple, float], switch_time:tuple, freq_resolution:float, 
                     q_name:list, ro_element:list, z_name:list, config, qmm:QuantumMachinesManager,time_resolution=1, 
                     n_avg=100,initializer=False,simulate=False, pi_pulse_scaling=5):
    """
    freq_span unit in MHz \n
    for asymetric span, in put a tuple ( begin, end )\n
    switch_time is a tuple include three element unit in us \n
    (switch_delay, switch_on, switch_off) \n
    total record time = switch_delay  +switch_on +switch_off\n
    time_resolution unit in clock cycle (4ns), defalut is 1\n

    """
    # Adjust the pulse duration and amplitude to drive the qubit into a mixed state
    saturation_len = pi_len * pi_pulse_scaling
    saturation_amp = pi_amp_q5 / pi_pulse_scaling  # pre-factor to the value defined in the config - restricted to [-2; 2)

    s_delay_qua = switch_time[0]/4 *u.us +4
    s_on_qua = switch_time[1]/4 *u.us
    s_off_qua = switch_time[2]/4 *u.us

    pi_delay_qua = np.arange(4, s_delay_qua+s_on_qua+s_off_qua, 1)  # Linear sweep

    freq_resolution_qua = freq_resolution *u.MHz
    if isinstance(freq_span, float):
        freqs_qua = np.arange( -freq_span/2 *u.MHz, +freq_span/2 *u.MHz, freq_resolution_qua)
    else:
        freqs_qua = np.arange( freq_span[0] *u.MHz, freq_span[1] *u.MHz, freq_resolution_qua)

    freqs_mhz = freqs_qua/1e6 # Convert Hz to MHz
    pi_delay_ns = pi_delay_qua*4  # Convert clock cycle to ns

    ref_z_offset = {}
    for z in z_name:
        ref_z_offset[z] = gc.get_offset(z, config)
    ref_xy_IF = {}
    for xy in q_name:
        ref_xy_IF[xy] = gc.get_IF(xy, config)

    time_len = pi_delay_qua.shape[-1]
    freq_len = len(freqs_qua)
    # QUA program
    with program() as decay_time:

        iqdata_stream = multiRO_declare( ro_element )
        t = declare(int)  
        n = declare(int)
        df = declare(int)
        n_st = declare_stream()
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(df, freqs_qua)):
                with for_(*from_array(t, pi_delay_qua)):
                    # Init
                    if initializer:
                        # wait(100*u.us)
                        wait(thermalization_time * u.ns)
                    else:
                        try:
                            initializer[0](*initializer[1])
                        except:
                            print("Initializer didn't work!")
                            wait(100*u.us)
                    for q in q_name:
                        update_frequency(q, ref_xy_IF[q]+df)
                    # Operation
                    for q in q_name:
                        wait(t,q)
                        # play("x180", q)
                        play("saturation" * amp(saturation_amp), q, duration=saturation_len * u.ns)


                    for z in z_name:
                        wait(s_delay_qua,z)
                        set_dc_offset(z, "single", ref_z_offset[z]+flux_amp)
                    wait(s_on_qua)
                    #align()
                    for z in z_name:
                        set_dc_offset(z, "single", ref_z_offset[z])
                        wait(s_off_qua,z)
                    align()
                    
                    
                    # Readout
                    multiRO_measurement( iqdata_stream,  resonators=ro_element, weights="rotated_")
                
            # Save the averaging iteration to get the progress bar
            save(n, n_st)

        with stream_processing():
            n_st.save("iteration")
            multiRO_pre_save(iqdata_stream, ro_element, (freq_len, time_len) )

    continue_from_previous = 1
    if simulate:
        simulation_config = SimulationConfig(duration=150000)  # In clock cycles = 4ns
        job = qmm.simulate(config, decay_time, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        if continue_from_previous:
            qm_list =  qmm.list_open_quantum_machines()
            qm = qmm.get_qm(qm_list[0])
            print("QM-ID: %s, Queue: %s, Version: %s" %(qm.id,qm.queue.count,qmm.version()))
            job = qm.get_running_job()
            print("The Cluster is currently running JOB-ID: %s" %job.id())
            job = qm.get_job(job.id)
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
                plot_qubit_flux_decay(output_data[r_name], freqs_mhz, pi_delay_ns, [ax[0][r_idx],ax[1][r_idx]])
            iteration = fetch_data[-1]
            # Progress bar
            progress_counter(iteration, n_avg, start_time=results.get_start_time()) 

            plt.pause(1)

        fetch_data = results.fetch_all()
        output_data = {}
        for r_idx, r_name in enumerate(ro_element):
            output_data[r_name] = ( ["mixer","frequency","time"],
                                np.array([fetch_data[r_idx*2], fetch_data[r_idx*2+1]]) )

        qm.close()
        dataset = xr.Dataset(
            output_data,
            coords={ "mixer":np.array(["I","Q"]), "frequency": freqs_mhz, "time": pi_delay_ns }
        )
        return dataset

def plot_qubit_flux_decay( data, time, freqs_qua, ax=None ):
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
    ax[0].pcolormesh( freqs_qua, time, np.abs(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)
    ax[1].pcolormesh( freqs_qua, time, np.angle(s21), cmap='RdBu')# , vmin=z_min, vmax=z_max)

def plot_ana_qubit_flux_decay( data, freqs_qua, time, freq_LO, freq_IF, ax=None ):
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

    abs_freq = freq_LO+freq_IF+freqs_qua
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
    from configuration import *
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)
    target_q = 'q5'
  
    # qmm, _ = spec.buildup_qmm()
    # init_macro = initializer((spec.give_WaitTime_with_q(target_q,5),),'wait')
  
    pi_pulse_scaling = 2
    n_avg = 100_000
    q_name = [f"{target_q}_xy"]
    ro_element = ["rr5"]
    z_name = [f"{target_q}_z"]
    flux_amp=0.04
    output = qubit_flux_decay(flux_amp,(-60., 20.),(0.3,0.3,0.1),0.2,q_name,ro_element,z_name,config,qmm,n_avg=n_avg,initializer=True,simulate=False, pi_pulse_scaling=pi_pulse_scaling)
    plt.show()
    #Data Saving   #
    
    save_data = True
    if save_data:
        from save_data import *
        import sys
        filename = f"qb_flux_decay_dr2a_{target_q}_({pi_pulse_scaling}Xpi)"
        save_xr(save_dir, filename, output, False)
        # output.to_netcdf(save_dir/filename)

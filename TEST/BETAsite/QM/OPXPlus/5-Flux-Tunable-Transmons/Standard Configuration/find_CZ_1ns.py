from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from configuration import *
import matplotlib.pyplot as plt
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter
# from common_fitting_func import *
import numpy as np
# from common_fitting_func import *
from macros import qua_declaration, multiplexed_readout
from qualang_tools.bakery import baking
import warnings
from qm import generate_qua_script

warnings.filterwarnings("ignore")

def baked_waveform(waveform, pulse_duration, flux_qubit):
    pulse_segments = []  
    for i in range(0, pulse_duration + 1):
        with baking(config, padding_method="right") as b:
            if i == 0:  # Otherwise, the baking will be empty and will not be created
                wf = [0.0] * 16
            else:
                wf = waveform[:i].tolist()
            b.add_op("flux_pulse", f"q{flux_qubit}_z", wf)
            b.play("flux_pulse", f"q{flux_qubit}_z")
        pulse_segments.append(b)
    return pulse_segments

def CZ_1ns(q_id,Qi_list,flux_Qi,amps,const_flux_len,simulate,qmm):
    # res_IF = []
    # resonator_freq = [[] for _ in q_id]
    with program() as cz:
        I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=len(q_id))
        a = declare(fixed)  
        segment = declare(int)  
        # for i in q_id:
        #     res_F = cosine_func(idle_flux_point[i], *g1[i])
        #     res_F = (res_F - resonator_LO)/1e6
        #     res_IF.append(int(res_F * u.MHz))
        #     resonator_freq[q_id.index(i)] = declare(int, value=res_IF[q_id.index(i)])
        #     set_dc_offset(f"q{i+1}_z", "single", idle_flux_point[i])
        #     update_frequency(f"rr{i+1}", resonator_freq[q_id.index(i)])
        wait(flux_settle_time * u.ns)
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(a, amps)):
                with for_(segment, 0, segment <= const_flux_len, segment + 1):
                    wait(thermalization_time * u.ns)
                    if excited_Qi_list != []: 
                        for excited_Qi in excited_Qi_list:
                            play("x180", f"q{excited_Qi}_xy")
                    align()
                    wait(5)
                    with switch_(segment):
                        for j in range(0, const_flux_len + 1):
                            with case_(j):
                                square_pulse_segments[j].run(amp_array=[(f"q{flux_Qi}_z", a)])
                    align()
                    wait(5)
                    align()
                    multiplexed_readout(I, I_st, Q, Q_st, resonators=[x+1 for x in q_id], weights="rotated_")
            save(n, n_st)
        with stream_processing():
            n_st.save("n")
            for i in q_id:
                I_st[q_id.index(i)].buffer( len(amps),const_flux_len+1 ).average().save(f"I{i+1}")
                Q_st[q_id.index(i)].buffer( len(amps),const_flux_len+1 ).average().save(f"Q{i+1}")
    if simulate:
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, cz, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(cz)
        fig = plt.figure()
        interrupt_on_close(fig, job)
        I_list, Q_list = [f"I{i+1}" for i in q_id], [f"Q{i+1}" for i in q_id]
        results = fetching_tool(job, I_list + Q_list + ["n"], mode="live")
        while results.is_processing():
            all_results = results.fetch_all()
            n = all_results[-1]
            I, Q = all_results[0:len(q_id)], all_results[len(q_id):len(q_id)*2]
            for i in q_id:
                I[q_id.index(i)] = u.demod2volts(I[q_id.index(i)], readout_len)
                Q[q_id.index(i)] = u.demod2volts(Q[q_id.index(i)], readout_len)
            progress_counter(n, n_avg, start_time=results.start_time)
            live_plotting(I,Q,Qi_list)
        qm.close()
        plt.show()
        return I, Q
    

def live_plotting(I,Q,Qi_list):
    plt.suptitle(f"CZ chevron sweeping the flux on qubit {flux_Qi}")
    for Qi in Qi_list:
        for i in q_id: 
            if i == Qi-1: plot_index = q_id.index(i)
        plt.subplot(2,2,Qi_list.index(Qi)+1)
        plt.cla()
        plt.pcolor(amps * scale_reference, ts, I[plot_index].transpose())
        plt.title(f"q{Qi} - I [V]")
        plt.ylabel("Interaction time (ns)")
        plt.subplot(2,2,Qi_list.index(Qi)+3)
        plt.cla()
        plt.pcolor(amps * scale_reference, ts, Q[plot_index].transpose())
        plt.title(f"q{Qi} - Q [V]")
        plt.ylabel("Interaction time (ns)")
        plt.xlabel("Flux amplitude (V)")       
        plt.tight_layout()
        plt.pause(0.1)

flux_Qi = 2  
scale_reference = const_flux_amp 
Qi_list = [2,3]
excited_Qi_list = [2,3]
n_avg = 500  
amps = np.arange(0.32, 0.38, 0.001) 
const_flux_len = 50
flux_waveform = np.array([const_flux_amp] * const_flux_len)
square_pulse_segments = baked_waveform(flux_waveform, const_flux_len, flux_Qi)
# for list in square_pulse_segments:
#     print('-'*20)
#     print(list.get_waveforms_dict())

simulate = False
q_id = [1,2,3,4]
ts = np.arange(0,const_flux_len+0.1,1)
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)      
I,Q = CZ_1ns(q_id,Qi_list,flux_Qi,amps,const_flux_len,simulate,qmm)


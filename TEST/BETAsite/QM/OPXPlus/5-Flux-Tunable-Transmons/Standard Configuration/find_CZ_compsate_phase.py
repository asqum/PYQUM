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
from cosine import Cosine

warnings.filterwarnings("ignore")

def cz_gate(type, idle_flux_point, flux_Qi, const_flux_len, a):
    # with baking(config,padding_method="symmetric_l") as b:
    #     q1_z_element = f"q{flux_Qi}_z"
    #     b.add_op("cz",q1_z_element,cz_wf)
    #     b.wait(20) # The unit is 1 ns.
    #     b.align()
    #     b.play("cz", q1_z_element)
    #     b.align(q1_z_element)
    #     b.wait(23,q1_z_element)
    #     b.align()
    #     b.run()

    if type == "square":
        square_pulse_segments = baked_waveform(flux_waveform, const_flux_len, flux_Qi, type)
        wait(5)  
        square_pulse_segments[const_flux_len].run(amp_array=[(f"q{flux_Qi}_z", a)])    
        align()
        set_dc_offset(f"q{flux_Qi}_z", "single", idle_flux_point[flux_Qi-1])
        wait(5)
    # elif type == 'eerp':
    #     eerp_pulse_segments = baked_waveform(waveform, pulse_duration, flux_qubit, type, paras = None)


def baked_waveform(waveform, pulse_duration, flux_qubit, type, paras = None):
    pulse_segments = []
    if type == 'square':  
        for i in range(0, pulse_duration + 1):
            with baking(config, padding_method="symmetric_l") as b:
                if i == 0:  # Otherwise, the baking will be empty and will not be created
                    wf = [0.0] * 16
                else:
                    wf = waveform[:i].tolist()
                b.add_op("flux_pulse", f"q{flux_qubit}_z", wf)
                b.play("flux_pulse", f"q{flux_qubit}_z")
            pulse_segments.append(b)

    elif type == 'eerp':
        duration = np.linspace(0,pulse_duration-1,pulse_duration)
        p = ( paras[0], paras[1]/2, paras[1]/paras[2], 2*paras[1], 5 ) # This 5 can make the pulse edge smooth in the begining.
        eerp_up_wf = np.array(EERP(duration,*p)[:(paras[1]+5)]) 
        eerp_dn_wf = eerp_up_wf[::-1]
        for i in range(0, pulse_duration + 1):
            with baking(config, padding_method="symmetric_l") as b:
                if i == 0: 
                    wf = np.concatenate((eerp_up_wf, eerp_dn_wf)).tolist()
                else:
                    wf = np.concatenate((eerp_up_wf, waveform[:i], eerp_dn_wf)).tolist()
                b.add_op("flux_pulse", f"q{flux_qubit}_z", wf)
                b.play("flux_pulse", f"q{flux_qubit}_z")
            pulse_segments.append(b)
    return pulse_segments


def CZ_phase_compensate(q_id,flux_Qi,ramsey_Qi,Phi,const_flux_len,simulate,qmm):
    res_IF = []
    resonator_freq = [[] for _ in q_id]
    with program() as cz_phase_compensate:
        ## _c means comparation
        I = [declare(fixed) for i in range(len(q_id))]
        Q = [declare(fixed) for i in range(len(q_id))] 
        I_c = [declare(fixed) for i in range(len(q_id))]
        Q_c = [declare(fixed) for i in range(len(q_id))] 
        I_st = [declare_stream() for i in range(len(q_id))]
        Q_st = [declare_stream() for i in range(len(q_id))]
        I_st_c = [declare_stream() for i in range(len(q_id))]
        Q_st_c = [declare_stream() for i in range(len(q_id))]  
        n = declare(int)
        n_st = declare_stream()      
        phi = declare(fixed)
        # for i in q_id:
        #     res_F = cosine_func(idle_flux_point[i], *g1[i])
        #     res_F = (res_F - resonator_LO)/1e6
        #     res_IF.append(int(res_F * u.MHz))
        #     resonator_freq[q_id.index(i)] = declare(int, value=res_IF[q_id.index(i)])
        #     set_dc_offset(f"q{i+1}_z", "single", idle_flux_point[i])
        #     update_frequency(f"rr{i+1}", resonator_freq[q_id.index(i)])
        wait(flux_settle_time * u.ns)
        with for_(n, 0, n < n_avg, n + 1):
            with for_(*from_array(phi, Phi)):
                ###  With CZ flux
                if not simulate: wait(thermalization_time * u.ns)
                play("x90", f"q{ramsey_Qi}_xy")
                align()
                ## This +1 is inserted because of making const_flux_len equal to actual pulse duration 
                cz_gate(type, idle_flux_point, flux_Qi, const_flux_len+1, a) 
                align()
                frame_rotation_2pi(phi, f"q{ramsey_Qi}_xy")
                play("x90", f"q{ramsey_Qi}_xy")
                wait(flux_settle_time * u.ns)
                align()
                multiplexed_readout(I, I_st, Q, Q_st, resonators=[x+1 for x in q_id], weights="rotated_")

                ###  Without CZ flux
                if not simulate: wait(thermalization_time * u.ns)
                play("x90", f"q{ramsey_Qi}_xy")
                align()
                cz_gate(type, idle_flux_point, flux_Qi, const_flux_len+1, a=0)
                align()
                frame_rotation_2pi(phi, f"q{ramsey_Qi}_xy")
                play("x90", f"q{ramsey_Qi}_xy")
                wait(flux_settle_time * u.ns)
                align()
                multiplexed_readout(I_c, I_st_c, Q_c, Q_st_c, resonators=[x+1 for x in q_id], weights="rotated_")
            save(n, n_st)
        with stream_processing():
            n_st.save("n")
            for i in q_id:
                I_st[q_id.index(i)].buffer(len(Phi)).average().save(f"I{i+1}")
                Q_st[q_id.index(i)].buffer(len(Phi)).average().save(f"Q{i+1}")
                I_st_c[q_id.index(i)].buffer(len(Phi)).average().save(f"I_c{i+1}")
                Q_st_c[q_id.index(i)].buffer(len(Phi)).average().save(f"Q_c{i+1}")
    if simulate:
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, cz_phase_compensate, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(cz_phase_compensate)
        fig = plt.figure()
        interrupt_on_close(fig, job)
        I_list, Q_list, I_c_list, Q_c_list = [f"I{i+1}" for i in q_id], [f"Q{i+1}" for i in q_id], [f"I_c{i+1}" for i in q_id], [f"Q_c{i+1}" for i in q_id]
        results = fetching_tool(job, I_list + Q_list + I_c_list + Q_c_list + ["n"], mode="live")
        while results.is_processing():
            all_results = results.fetch_all()
            n = all_results[-1]
            I, Q, I_c, Q_c = all_results[0:len(q_id)], all_results[len(q_id):len(q_id)*2], all_results[len(q_id)*2:len(q_id)*3], all_results[len(q_id)*3:len(q_id)*4]
            for i in q_id:
                I[q_id.index(i)] = u.demod2volts(I[q_id.index(i)], readout_len)
                Q[q_id.index(i)] = u.demod2volts(Q[q_id.index(i)], readout_len)
                I_c[q_id.index(i)] = u.demod2volts(I_c[q_id.index(i)], readout_len)
                Q_c[q_id.index(i)] = u.demod2volts(Q_c[q_id.index(i)], readout_len)
            progress_counter(n, n_avg, start_time=results.start_time)
            match signal_mode:
                case 'I':
                    signal = I
                    signal_c = I_c
                case 'Q':
                    signal = Q
                    signal_c = Q_c
            live_plotting(signal,signal_c,ramsey_Qi)
        qm.close()
        plt.show()
        return I, Q, I_c, Q_c
    

def live_plotting(signal,signal_c,ramsey_Qi):
    
    for i in q_id: 
        if i == ramsey_Qi-1: plot_index = q_id.index(i)
    plt.cla()
    plt.plot(Phi, signal[plot_index], '.b', Phi, signal_c[plot_index], '.r')
    try:
        fit = Cosine(Phi, signal[plot_index], plot=False)
        phase = fit.out.get('phase')[0]
        plt.plot(fit.x_data, fit.fit_type(fit.x, fit.popt) * fit.y_normal, '-b', alpha=0.5, label='with CZ pulse')
        fit = Cosine(Phi, signal_c[plot_index], plot=False)
        phase_c = fit.out.get('phase')[0]
        plt.plot(fit.x_data, fit.fit_type(fit.x, fit.popt) * fit.y_normal, '-r', alpha=0.5, label='without CZ pulse')
        dphase = (phase-phase_c)/np.pi*180     
    except Exception as e: print(e) 
    plt.title(f"CZ phase difference at q{ramsey_Qi}, phase diff: {dphase:.3f}")  
    plt.legend()
    plt.tight_layout()
    plt.pause(0.1)

flux_Qi = 5  
ramsey_Qi = 5
cz_sqr_amp, cz_sqr_len = cz5_4_amp, cz5_4_len
a = cz_sqr_amp/const_flux_amp
type = 'square'
signal_mode = 'I'
scale_reference = const_flux_amp 
n_avg = 2000  
const_flux_len = cz5_4_len
flux_waveform = np.array([const_flux_amp] * (const_flux_len+1))
Phi = np.arange(0, 5, 0.05) # 5 rotations
idle_flux_point = [idle_q1,idle_q2,idle_q3,idle_q4,idle_q5]

cz_wf = np.array([cz_sqr_amp]*(cz_sqr_len+1)) # cz_len+1 is the exactly time of z pulse.
cz_wf = cz_wf.tolist()


###
# square_pulse_segments = baked_waveform(flux_waveform, const_flux_len, flux_Qi)
# for segment in square_pulse_segments:
#     print(segment.get_waveforms_dict())

simulate = False
q_id = [1,2,3,4]
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)      
I, Q, I_c, Q_c = CZ_phase_compensate(q_id,flux_Qi,ramsey_Qi,Phi,const_flux_len,simulate,qmm)
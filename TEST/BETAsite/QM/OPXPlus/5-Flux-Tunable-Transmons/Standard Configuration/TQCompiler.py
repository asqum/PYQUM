from qutip_qip.operations import Gate #Measurement in 0.3.X qutip_qip
from qutip_qip.circuit import QubitCircuit
from qutip_qip.compiler import GateCompiler
from tqdm import tqdm
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from configuration import *
import matplotlib.pyplot as plt
import numpy as np
from qualang_tools.bakery import baking
from macros import multiplexed_readout


x180_wf, y180_wf, x90_wf, y90_wf, minus_x90_wf, minus_y90_wf  = [], [], [], [], [], []
for i in range(5):
    ### x180_wf[0] stands for q1_x180's waveforms
    x180_wf.append( [config["waveforms"][f"x180_I_wf_q{i+1}"]["samples"],config["waveforms"][f"x180_Q_wf_q{i+1}"]["samples"]] )
    y180_wf.append( [config["waveforms"][f"y180_I_wf_q{i+1}"]["samples"],config["waveforms"][f"y180_Q_wf_q{i+1}"]["samples"]] )
    x90_wf.append( [config["waveforms"][f"x90_I_wf_q{i+1}"]["samples"],config["waveforms"][f"x90_Q_wf_q{i+1}"]["samples"]] )
    y90_wf.append( [config["waveforms"][f"y90_I_wf_q{i+1}"]["samples"],config["waveforms"][f"y90_Q_wf_q{i+1}"]["samples"]] )
    minus_x90_wf.append( [config["waveforms"][f"minus_x90_I_wf_q{i+1}"]["samples"],config["waveforms"][f"minus_x90_Q_wf_q{i+1}"]["samples"]] )
    minus_y90_wf.append( [config["waveforms"][f"minus_y90_I_wf_q{i+1}"]["samples"],config["waveforms"][f"minus_y90_Q_wf_q{i+1}"]["samples"]] )
cz_sqr_wf = np.array([cz5_4_amp]*(cz5_4_len+1)) # cz_sqr_len+1 is the exactly time of z pulse.
cz_sqr_wf = cz_sqr_wf.tolist()

# edge = 10
# sFactor = 4
# duration = np.linspace(0,49,50)
# paras = [cz_eerp_amp, edge, sFactor]
# p = ( paras[0], paras[1]/2, paras[1]/paras[2], 2*paras[1], 5 ) # This 5 can make the pulse edge smooth in the begining.
# eerp_up_wf = np.array(EERP(duration,*p)[:(paras[1]+5)]) 
# eerp_dn_wf = eerp_up_wf[::-1]
# waveform = np.array([cz_eerp_amp]*(cz_eerp_len+1))
# eerp_wf = np.concatenate((eerp_up_wf, waveform, eerp_dn_wf))
# eerp_wf = eerp_wf.tolist()

q4_x180 = Gate("RX", 4, arg_value=np.pi)
q5_x180 = Gate("RX", 5, arg_value=np.pi)
q4_x90 = Gate("RX", 4, arg_value=np.pi/2)
q5_x90 = Gate("RX", 5, arg_value=np.pi/2)
q4_y180 = Gate("RY", 4, arg_value=np.pi)
q4_y90 = Gate("RY", 4, arg_value=np.pi/2)
q5_y90 = Gate("RY", 5, arg_value=np.pi/2)
q5_y180 = Gate("RY", 5, arg_value=np.pi)
idle_gate = Gate("IDLE", 2)
### Crucially Important!! The controls of CZ gate is the first element, which we apply flux. That is the higher freq. one.
cz = Gate("CZ", controls=5, targets=4)

def meas():
    threshold1 = ge_threshold_q4 # threshold for state discrimination 0 <-> 1 using the I quadrature
    threshold2 = ge_threshold_q5  # threshold for state discrimination 0 <-> 1 using the I quadrature
    I1 = declare(fixed)
    I2 = declare(fixed)
    Q1 = declare(fixed)
    Q2 = declare(fixed)
    I3 = declare(fixed)
    I4 = declare(fixed)
    Q3 = declare(fixed)
    Q4 = declare(fixed)
    I5 = declare(fixed)
    Q5 = declare(fixed)
    state1 = declare(bool)
    state2 = declare(bool)
    multiplexed_readout(
        [I1, I2, I3, I4, I5], None, [Q1, Q2, Q3, Q4, Q5], None, resonators=[ 4, 5, 1, 2, 3 ], weights="rotated_"
    )  # readout macro for multiplexed readout
    assign(state1, I1 > threshold1)  # assume that all information is in I
    assign(state2, I2 > threshold2)  # assume that all information is in I
    return state1, state2

class TQCompile(GateCompiler):
    """Custom compiler for generating pulses from gates using the base class 
    GateCompiler.

    Args:
        num_qubits (int): The number of qubits in the processor
        params (dict): A dictionary of parameters for gate pulses such as
                       the pulse amplitude.
    """

    def __init__(self, num_qubits, q1_frame_update, q2_frame_update, params, cz_type = 'square'):
        super().__init__(num_qubits, params=params)
        self.params = params
        self.cz_type = cz_type
        self.gate_compiler = {
            "RX": self.rxy_compiler,
            "RY": self.rxy_compiler,
            "CZ": self.cz_compiler,
            "IDLE": self.idle_compiler,

        }
        self.q1_frame_update = q1_frame_update
        self.q2_frame_update = q2_frame_update
        if cz_type == 'square':
            cz_wf = cz_sqr_wf
        elif cz_type == 'eerp':
            cz_wf = eerp_wf
        self.cz_wf = cz_wf

    def rxy_compiler(self, gate, args):
        """Compiles single-qubit gates to pulses.
        
        Args:
            gate (qutip_qip.circuit.Gate): A qutip Gate object.
        
        """
        if gate.name == "RX":
            if int(round(gate.arg_value/np.pi*180)) == 90: self.x90_compiler(gate,args)
            elif int(round(gate.arg_value/np.pi*180)) == 180: self.x180_compiler(gate,args)
            elif int(round(gate.arg_value/np.pi*180)) == -90: self.minus_x90_compiler(gate,args)
            else: print('NO RX why?')

        elif gate.name == "RY":
            if int(round(gate.arg_value/np.pi*180)) == 90: self.y90_compiler(gate,args)
            elif int(round(gate.arg_value/np.pi*180)) ==  180: self.y180_compiler(gate,args)
            elif int(round(gate.arg_value/np.pi*180)) == -90: self.minus_y90_compiler(gate,args)
            else: print('NO RY why?')

    def x180_compiler(self,gate,args):
        with baking(config,padding_method="symmetric_l") as b: 
            b.add_op("x180", f"q{gate.targets[0]}_xy", x180_wf[gate.targets[0]-1])
            b.play("x180", f"q{gate.targets[0]}_xy")
            b.run()
            # return b

    def y180_compiler(self,gate,args):
        with baking(config,padding_method="symmetric_l") as b: 
            b.add_op("y180", f"q{gate.targets[0]}_xy", y180_wf[gate.targets[0]-1])
            b.play("y180", f"q{gate.targets[0]}_xy")
            b.run()
            # return b

    def x90_compiler(self,gate,args):
        with baking(config,padding_method="symmetric_l") as b: 
            b.add_op("x90", f"q{gate.targets[0]}_xy", x90_wf[gate.targets[0]-1])
            b.play("x90", f"q{gate.targets[0]}_xy")
            b.run()
            # return b

    def y90_compiler(self,gate,args):
        with baking(config,padding_method="symmetric_l") as b: 
            b.add_op("y90", f"q{gate.targets[0]}_xy", y90_wf[gate.targets[0]-1])
            b.play("y90", f"q{gate.targets[0]}_xy")
            b.run()
            # return b

    def minus_x90_compiler(self,gate,args):
        with baking(config,padding_method="symmetric_l") as b: 
            b.add_op("minus_x90", f"q{gate.targets[0]}_xy", minus_x90_wf[gate.targets[0]-1])
            b.play("minus_x90", f"q{gate.targets[0]}_xy")  
            b.run()
            # return b

    def minus_y90_compiler(self,gate,args):
        with baking(config,padding_method="symmetric_l") as b: 
            b.add_op("minus_y90", f"q{gate.targets[0]}_xy", minus_y90_wf[gate.targets[0]-1])
            b.play("minus_y90", f"q{gate.targets[0]}_xy")  
            b.run()
            # return b

    def idle_compiler(self,gate,args):
        with baking(config,padding_method="symmetric_l") as b:
            b.wait(pi_len, f"q{gate.targets[0]}_xy")
            b.run()
            # return b

    def cz_compiler(self,gate,args):
        ### Crucially Important!! The control of CZ gate is the first element, which we apply flux. That is the higher freq. one.
        with baking(config,padding_method="symmetric_l") as b:
            q1_xy_element = f"q{gate.controls[0]}_xy"  
            q2_xy_element = f"q{gate.targets[0]}_xy"
            q1_z_element = f"q{gate.controls[0]}_z"
            b.add_op("cz",q1_z_element,self.cz_wf)
            b.wait(20,q1_xy_element,q2_xy_element,q1_z_element) # The unit is 1 ns.
            b.align(q1_xy_element,q2_xy_element,q1_z_element)
            b.play("cz", q1_z_element)
            b.align(q1_xy_element,q2_xy_element,q1_z_element)
            b.wait(23,q1_xy_element,q2_xy_element,q1_z_element)
            b.frame_rotation_2pi(self.q1_frame_update, q1_xy_element)
            b.frame_rotation_2pi(self.q2_frame_update, q2_xy_element)
            b.align(q1_xy_element,q2_xy_element,q1_z_element)
            b.run()

if __name__ == '__main__':
    from TQRB.TQClifford import m_random_Clifford_circuit, get_TQcircuit_random_clifford
    from TQRB.RBResult import RBResult
    mycompiler = TQCompile( 2, q1_frame_update= -258.128 / 360, q2_frame_update= -18.345 / 360, params={}, cz_type='eerp' )
    ### TEST GATE
    q2_x180 = Gate("RX", 2, arg_value=np.pi)
    q3_x180 = Gate("RX", 3, arg_value=np.pi)
    q2_x90 = Gate("RX", 2, arg_value=np.pi/2)
    q3_x90 = Gate("RX", 3, arg_value=np.pi/2)
    # rg_y1 = Gate("RY", 2, arg_value=-np.pi/2)
    idle_gate = Gate("IDLE", 2)
    # idle_gate_1 = Gate("IDLE", 3)
    # ### Crucially Important!! The controls of CZ gate is the first element, which we apply flux. That is the higher freq. one.
    cz = Gate("CZ", controls=2, targets=3)
    gate_seq = [
       cz
    ]
    circuit = QubitCircuit(2)
    for gate in gate_seq:
        circuit.add_gate(gate)

    ### TEST TQRB
    # circuit_depths = [0]
    # circuit_repeats = 1
    n_avg = 2000
    # circuit = [[[] for _ in range(circuit_repeats)] for _ in range(len(circuit_depths))]
    # for i in circuit_depths:
    #     for j in tqdm(range(circuit_repeats), desc="Processing", unit="step"):
    #         circuit[i][j] = get_TQcircuit_random_clifford(control=2, target=3, num_gates=i, mode='ONE') 
    print('Entering QUA program')
    with program() as prog:
        n = declare(int)
        n_st = declare_stream()  
        state = declare(int)
        state_os = declare_stream()

        ####  TEST GATE
        with for_(n, 0, n < n_avg, n + 1):  
            # wait(thermalization_time)
            compiled_data = mycompiler.compile(circuit,schedule_mode='ASAP')
            align()
            wait(flux_settle_time * u.ns)
            out1, out2 = meas()
            assign(state, (Cast.to_int(out2) << 1) + Cast.to_int(out1))
            save(state, state_os)
            save(n, n_st)

        ####  TEST TQRB
        # for i in circuit_depths:
        #     for j in tqdm(range(circuit_repeats), desc="Processing", unit="step"):
        #         with for_(n, 0, n < n_avg, n + 1):   
        #             wait(thermalization_time)
        #             compiled_data = mycompiler.compile(circuit,schedule_mode='ASAP')
        #             align()
        #             wait(flux_settle_time * u.ns)
        #             out1, out2 = meas()
        #             assign(state, (Cast.to_int(out2) << 1) + Cast.to_int(out1))
        #             save(state, state_os)
        #             save(n, n_st)
        # with stream_processing():
        #     n_st.save("n")
        #     state_os.buffer(len(circuit_depths), circuit_repeats, n_avg).save("state")

    simulate = True
    qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config) 
    if simulate:
        simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
        job = qmm.simulate(config, prog, simulation_config)
        job.get_simulated_samples().con1.plot()
        plt.show()
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(prog)
        full_progress = len(circuit_depths)
        job.result_handles.wait_for_all_values()
        rbresult = RBResult(
            circuit_depths=circuit_depths,
            num_repeats=circuit_repeats,
            num_averages=n_avg,
            state=job.result_handles.get("state").fetch_all(),
        )
        rbresult.plot_hist()
        plt.show()

        # rbresult.plot_fidelity()
        # plt.show()


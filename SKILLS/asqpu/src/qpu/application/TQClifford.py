from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from argparse import Action
from typing import List
#from pulse_generator.pulse import Pulse
import numpy as np
from qutip import sigmax, sigmay, sigmaz, basis, qeye, Qobj
from qutip_qip.circuit import QubitCircuit
from qutip_qip.operations import Gate #Measurement in 0.3.X qutip_qip
from typing import List
from pulse_signal.common_Mathfunc import ErfAmplifier
from qutip.tensor import tensor
from qpu.backend.circuit.TQRB.TQCompiler import TQCompile
from qpu.backend.circuit.backendcircuit import BackendCircuit
from collections import Counter


## Basic
## Pi
def rg_i(target): # idle gate
    return Gate("RX", target, arg_value= 0)
def rg_x(target):   
    return Gate("RX", target, arg_value= np.pi)
def rg_y(target):
    return Gate("RY", target, arg_value= np.pi)

## Pi/2
def rg_px2(target):
    return Gate("RX", target, arg_value= +np.pi/2)
def rg_py2(target):
    return Gate("RY", target, arg_value= +np.pi/2)
def rg_nx2(target):
    return Gate("RX", target, arg_value= -np.pi/2)
def rg_ny2(target):
    return Gate("RY", target, arg_value= -np.pi/2)

## CZ gate
def cz(target,control):
    return Gate("CZ", target, control)

# The followings are the 4 components of C2 clifford group  
def c1_gates(target:int)->List:
    """
    Get a gate in Clifford group for single qubit
    """
## Decompose
## Pi
    g_z = [rg_y(target), rg_x(target)]
## Pi/2
    g_phz = [rg_nx2(target),rg_py2(target),rg_px2(target)]
    g_nhz = [rg_nx2(target),rg_ny2(target),rg_px2(target)]
## Had
    g_hpxz = [rg_x(target),rg_ny2(target)]
    g_hnxz = [rg_x(target),rg_py2(target)]
    g_hpyz = [rg_y(target),rg_px2(target)]
    g_hnyz = [rg_y(target),rg_nx2(target)]
    g_hpxy = [rg_px2(target),rg_py2(target),rg_px2(target)]
    g_hnxy = [rg_nx2(target),rg_py2(target),rg_nx2(target)]
## 2pi/3 
    g_pc1 = [rg_py2(target),rg_px2(target)]
    g_pc2 = [rg_py2(target),rg_nx2(target)]
    g_pc4 = [rg_ny2(target),rg_px2(target)]
    g_pc3 = [rg_ny2(target),rg_nx2(target)]

    g_nc1 = [rg_nx2(target),rg_py2(target)]
    g_nc2 = [rg_px2(target),rg_py2(target)]
    g_nc4 = [rg_nx2(target),rg_ny2(target)]
    g_nc3 = [rg_px2(target),rg_ny2(target)]

    gates_set = [
        [rg_i(target)],[rg_x(target)],[rg_y(target)],[rg_px2(target)],[rg_nx2(target)],
        [rg_py2(target)],[rg_ny2(target)],
    ## Pi
        g_z,
    ## Pi/2
        g_phz,g_nhz,
    ## Had
        g_hpxz,g_hnxz,g_hpyz,g_hnyz,g_hpxy,g_hnxy,
    ## 2pi/3 
        g_pc1,g_pc2,g_pc4,g_pc3,
        g_nc1,g_nc2,g_nc4,g_nc3
    ]
    return gates_set

def s1_gates(target)->List:
    s_11 = [rg_i(target)]
    s_12 = [rg_py2(target),rg_px2(target)]
    s_13 = [rg_nx2(target),rg_ny2(target)]
    gates_set = [s_11,s_12,s_13]

    return gates_set
    
def s1_x_gates(target)->List:
    s_21 = [rg_px2(target)]
    s_22 = [rg_px2(target),rg_py2(target),rg_px2(target)]
    s_23 = [rg_ny2(target)]
    gates_set = [s_21,s_22,s_23]

    return gates_set
    
def s1_y_gates(target)->List:
    s_31 = [rg_py2(target)]
    s_32 = [rg_y(target),rg_px2(target)]
    s_33 = [rg_nx2(target),rg_ny2(target),rg_px2(target)]
    gates_set = [s_31,s_32,s_33]

    return gates_set

def single_qubit_class(target, control)->List:
    '''
    Total 576 C2 clifford gates
    '''
    sequence = [gate_c + gate_t for gate_c in c1_gates(control) for gate_t in c1_gates(target)]

    return sequence 

def cnot_like_class(target, control)->List:
    '''
    Total 5184 C2 clifford gates
    '''    
    sequence = [c1_gate + [cz(target, control)] for c1_gate in single_qubit_class(target, control)]
    sequence = [
        gate_seq + s1_gate + s1y_gate for s1_gate in s1_gates(control) for s1y_gate in s1_y_gates(target) for gate_seq in sequence
    ]

    return sequence

def iswap_like_class(target,control)->List:
    '''
    Total 5184 C2 clifford gates
    '''    
    sequence = [
        c1_gate + [cz(target, control)] + [rg_py2(control)] + [rg_nx2(target)] + [cz(target, control)] 
        for c1_gate in single_qubit_class(target, control)
    ]
    sequence = [
        gate_seq + s1y_gate + s1x_gate for s1y_gate in s1_y_gates(control) 
        for s1x_gate in s1_x_gates(target) for gate_seq in sequence
    ]

    return sequence

def swap_like_class(target, control)->List:
    '''
    Total 576 C2 clifford gates
    '''
    sequence = [
        c1_gate + [cz(target, control)] + [rg_ny2(control)] + [rg_py2(target)] + [cz(target, control)] +
        [rg_py2(control)] + [rg_ny2(target)] + [cz(target, control)] + [rg_py2(target)]        
        for c1_gate in single_qubit_class(target, control)
    ]

    return sequence

def c2_clifford_gates(target, control)->List:
    '''
    Combine four classes. 
    '''
    sequence = single_qubit_class(target, control) + cnot_like_class(target, control) + iswap_like_class(target, control) + swap_like_class(target, control)

    return sequence

def get_random_c2_gate(target, control)->List:
    return np.random.choice(c2_clifford_gates(target, control))

def m_random_Clifford_circuit( m, target, control )->QubitCircuit:
    sequence = []
    circuit = QubitCircuit(2)
    for i in range(m):
        clifford_gate = get_random_c2_gate(target, control)
        for gate in clifford_gate:
            sequence.append(gate)
    
    for gate in sequence:
        circuit.add_gate(gate)

    return circuit

def decomposition(gates:List[Gate])->Qobj:
    """
    Give a list of gate then return the represent matrix (Qobj). This matrix do not involve target 
    and control, hence the order of target and control should be determined first.
    The elements in tensor product are not commutable, since they denote the different Hilbert spaces.
    Make sure the first element denote the control qubit Hilbert space, and the second denote the 
    target qubit Hilbert space.

    Args:
        List : A list of qutip Gate object (qutip_qip.circuit.Gate). 
    
    Returns:
        Qobj (qutip.Qobj): 
    """

    operation = qeye([2,2])

    for gate in gates:
        if gate.name != 'CZ':
            gate_qobj = gate.get_compact_qobj() 

            if str(gate.targets) == '[0]':
                gate_qobj = tensor(gate_qobj, qeye(2))

            elif str(gate.targets) == '[1]':
                gate_qobj = tensor(qeye(2), gate_qobj)

            operation = gate_qobj * operation

        elif gate.name == 'CZ':
            gate_qobj = gate.get_compact_qobj()

            operation = gate_qobj * operation

    return operation

def find_inv_gate(gates:List[Gate], target=1, control=0):
    '''
    Give the list of gates of C2 Clifford, then return the inverse of it from C2 Clifford group.

    Args:
        gates: list  A list of (qutip_qip.circuit.Gate) gate.
    
    Returns:
        list : A list of (qutip_qip.circuit.Gate) gate.  
    '''
    c2_gate_inv = None
    operation = decomposition(gates)
    c2_gate_set = c2_clifford_gates(target, control)
    for c2_gate in c2_gate_set:
        compare_operation = decomposition(c2_gate)
        operation_inv = operation.inv()
        for phase in [
            1,1j,-1,-1j,(1+1j)/np.sqrt(2),(1-1j)/np.sqrt(2),(-1+1j)/np.sqrt(2),(-1-1j)/np.sqrt(2)
                ]:
            if phase * operation_inv == compare_operation:
                c2_gate_inv = c2_gate
                break
                
    if c2_gate_inv == None:
        print(f'operation matrix: {operation}')
        print(f'operation matrix inv: {operation.inv()}')

    return c2_gate_inv

def get_TQcircuit_random_clifford(target, control, num_gates)->QubitCircuit:
    '''
    Give the number, target and control of C2 Clifford, then return 
    the random gate operation combined with inverse of this operation.

    Args:
        target: int
        control: int
        num_gates: int  A number of C2 Clifford group.
    
    Returns:
        circuit_RB : Qubitcircuit  Combine all the gate and inverse operation.
    '''
    circuit_RB = m_random_Clifford_circuit( num_gates, target, control )
    c2_gate_inv = find_inv_gate( circuit_RB.gates )
    circuit_RB.add_gates(c2_gate_inv)

    return circuit_RB

def get_TQRB_device_setting(backendcircuit:BackendCircuit, num_gates, target=1, control=0, withRO:bool=False):

    d_setting = []
    circuit_RB = get_TQcircuit_random_clifford(target, control, num_gates)
    if withRO:
        rg_ro = Gate("RO", [control,target] )
        circuit_RB.add_gate(rg_ro)
    mycompiler = TQCompile(2, params={})
    q1_name = backendcircuit.q_reg["qubit"][0]
    q1_info = backendcircuit.get_qComp(q1_name)
    backendcircuit.total_time = q1_info.tempPars["total_time"]
    q2_name = backendcircuit.q_reg["qubit"][1]
    q2_info = backendcircuit.get_qComp(q2_name)
    print(f"{q1_name}, {q2_name} get RB sequence." )
    print(f"dt={backendcircuit.dt}")
    qubit_info = [q1_info,q2_info]

    # Give parameters to TQCompiler
    for qi in range(2):
        mycompiler.params[str(qi)] = {}
        mycompiler.params[str(qi)]["rxy"] = {}
        mycompiler.params[str(qi)]["rxy"]["dt"] = backendcircuit.dt
        mycompiler.params[str(qi)]["rxy"]["pulse_length"] = qubit_info[qi].tempPars["XYW"]
        mycompiler.params[str(qi)]["anharmonicity"] = float(qubit_info[qi].tempPars["anharmonicity"])*2*np.pi
        mycompiler.params[str(qi)]["cz"] = {}
        mycompiler.params[str(qi)]["cz"]["dt"] = backendcircuit.dt
        mycompiler.params[str(qi)]["cz"]["pulse_length"] = qubit_info[qi].tempPars["CZ"]["ZW"]
        mycompiler.params[str(qi)]["cz"]["dz"] = qubit_info[qi].tempPars["CZ"]["dZ"]
        mycompiler.params[str(qi)]["cz"]["c_Z"] = qubit_info[qi].tempPars["CZ"]["c_Z"]    
        mycompiler.params[str(qi)]["cz"]["c_ZW"] = qubit_info[qi].tempPars["CZ"]["c_ZW"]

        mycompiler.params[str(qi)]["cz"]["type"] = qubit_info[qi].tempPars["CZ"]["type"] 
        mycompiler.params[str(qi)]["cz"]["xyr"] = qubit_info[qi].tempPars["CZ"]["XYR"] 
        # if "waveform&alpha&sigma" in list(qubit_info[qi].tempPars.keys()):
        #     mycompiler.params["waveform"] = qubit_info[qi].tempPars["waveform&alpha&sigma"]
        # else:
        #     mycompiler.params["waveform"] = ["NaN",0,4]  #[waveform,a_weight,S-Factor]
        '''Ratis debug: '''
        mycompiler.params[str(qi)]["iswap"] = {}
        mycompiler.params[str(qi)]["iswap"]["type"] = qubit_info[qi].tempPars["ISWAP"]["type"] 
        mycompiler.params[str(qi)]["iswap"]["xyr"] = qubit_info[qi].tempPars["ISWAP"]["XYR"]
        if "waveform&edge&sigma" in list(qubit_info[qi].tempPars["CZ"].keys()):
            mycompiler.params[str(qi)]["cz"]["waveform"] = qubit_info[qi].tempPars["CZ"]["waveform&edge&sigma"]
        else:
            mycompiler.params[str(qi)]["cz"]["waveform"] = ["NaN"]
        if "waveform&edge&sigma" in list(qubit_info[qi].tempPars["CZ"].keys()):   
            mycompiler.params[str(qi)]["cz"]["c_waveform"] = qubit_info[qi].tempPars["CZ"]["c_waveform&edge&sigma"]
        else:
            mycompiler.params[str(qi)]["cz"]["c_waveform"] = [""]
        if "waveform&alpha&sigma" in list(qubit_info[qi].tempPars.keys()):
            mycompiler.params[str(qi)]["waveform"] = qubit_info[qi].tempPars["waveform&alpha&sigma"]
        else:
            mycompiler.params[str(qi)]["waveform"] = ["NaN",0,4]  #[waveform,a_weight,S-Factor]


    # The readout pulse length for 2 qubits should be the same.    
    mycompiler.params["ro"] = {}
    mycompiler.params["ro"]["pulse_length"] = q1_info.tempPars["ROW"]
    mycompiler.params["ro"]["dt"] = backendcircuit.dt
    mycompiler.params["a_weight"] = 0    
    mycompiler.params["img_ratio"] = 0.5
    # print(Back.WHITE + Fore.RED + "** Now use %s with a_weight = %.2f, S-Factor = %d and Anharmonicity = %.5f (GHz) **"%(mycompiler.params["waveform"][0],mycompiler.params["waveform"][1],mycompiler.params["waveform"][2],mycompiler.params["anharmonicity"]))

    waveform_channel = mycompiler.to_waveform(circuit_RB)
    d_setting = backendcircuit.devices_setting(waveform_channel)
    d_setting["total_time"] = backendcircuit.total_time
    return d_setting


def test_c2_clifford_compact(target,control,group:str):

    # The following part is to test the compactness of the C2 clifford group
    i = 0
    found = False
    match group:
        case 'single':
            test1 = single_qubit_class(target,control)
            test2 = single_qubit_class(target,control)
        case 'cnot':
            test1 = cnot_like_class(target,control)
            test2 = cnot_like_class(target,control)
        case 'iswap':
            test1 = iswap_like_class(target,control)
            test2 = iswap_like_class(target,control)
        case 'swap':
            test1 = swap_like_class(target,control)
            test2 = swap_like_class(target,control)
        case _:
            raise NameError('No such group')

    for seq1 in test1:
        x = decomposition(seq1)
        match_seq = None
        for seq2 in test2:
            y = decomposition(seq2)
            for phase in [1,1j,-1,-1j]:
                if phase * y == x.inv():
                    match_seq = seq2
                    i += 1
                    found = True
                    print(i)
                    break
            if found:
                break
        if match_seq == None:
            print(f'operation matrix:{x}')
            print(f'operation matrix inv:{x.inv()}')
            break
        found = False
        if match_seq is not None:
            test2.remove(match_seq)  
    print(i)
    print(test2)

# if __name__ == '__main__':
#     test_c2_clifford_compact(1,0,'cnot')
   
                    


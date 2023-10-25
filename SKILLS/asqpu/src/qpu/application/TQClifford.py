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
import ast
# gate file path
num_pairs_path = r'C:\Users\Administrator\Documents\GitHub\PYQUM\SKILLS\asqpu\src\qpu\application\c2_num_pairs.txt'
inv_pairs_path = r'C:\Users\Administrator\Documents\GitHub\PYQUM\SKILLS\asqpu\src\qpu\application\c2_inv_pairs.txt'

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

def name_c1_gates(target:int)->List:
    """
    Get a gate name in Clifford group for single qubit
    """
## Decompose
## Pi
    g_z = [f"rg_y({target})", f"rg_x({target})"]   
## Pi/2
    g_phz = [f"rg_nx2({target})",f"rg_py2({target})",f"rg_px2({target})"]
    g_nhz = [f"rg_nx2({target})",f"rg_ny2({target})",f"rg_px2({target})"]     
## Had
    g_hpxz = [f"rg_x({target})",f"rg_ny2({target})"]
    g_hnxz = [f"rg_x({target})",f"rg_py2({target})"]
    g_hpyz = [f"rg_y({target})",f"rg_px2({target})"]
    g_hnyz = [f"rg_y({target})",f"rg_nx2({target})"]
    g_hpxy = [f"rg_px2({target})",f"rg_py2({target})",f"rg_px2({target})"]
    g_hnxy = [f"rg_nx2({target})",f"rg_py2({target})",f"rg_nx2({target})"]
## 2pi/3 
    g_pc1 = [f"rg_py2({target})",f"rg_px2({target})"]
    g_pc2 = [f"rg_py2({target})",f"rg_nx2({target})"]
    g_pc4 = [f"rg_ny2({target})",f"rg_px2({target})"]
    g_pc3 = [f"rg_ny2({target})",f"rg_nx2({target})"]

    g_nc1 = [f"rg_nx2({target})",f"rg_py2({target})"]
    g_nc2 = [f"rg_px2({target})",f"rg_py2({target})"]
    g_nc4 = [f"rg_nx2({target})",f"rg_ny2({target})"]
    g_nc3 = [f"rg_px2({target})",f"rg_ny2({target})"]

    gates_set = [
        [f"rg_i({target})"],[f"rg_x({target})"],[f"rg_y({target})"],[f"rg_px2({target})"],[f"rg_nx2({target})"],
        [f"rg_py2({target})"],[f"rg_ny2({target})"],
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

def name_s1_gates(target)->List:
    s_11 = [f"rg_i({target})"]
    s_12 = [f"rg_py2({target})",f"rg_px2({target})"]
    s_13 = [f"rg_nx2({target})",f"rg_ny2({target})"]
    gates_set = [s_11,s_12,s_13]

    return gates_set

def name_s1_x_gates(target)->List:
    s_21 = [f"rg_px2({target})"]
    s_22 = [f"rg_px2({target})",f"rg_py2({target})",f"rg_px2({target})"]
    s_23 = [f"rg_ny2({target})"]
    gates_set = [s_21,s_22,s_23]

    return gates_set

def name_s1_y_gates(target)->List:
    s_31 = [f"rg_py2({target})"]
    s_32 = [f"rg_y({target})",f"rg_px2({target})"]
    s_33 = [f"rg_nx2({target})",f"rg_ny2({target})",f"rg_px2({target})"]
    gates_set = [s_31,s_32,s_33]

    return gates_set

def name_single_qubit_class(target, control)->List:
    '''
    Total 576 C2 clifford gates
    '''
    sequence = [gate_c + gate_t for gate_c in name_c1_gates(control) for gate_t in name_c1_gates(target)]

    return sequence 

def name_cnot_like_class(target, control)->List:
    '''
    Total 5184 C2 clifford gates
    '''    
    sequence = [c1_gate + [f"cz({target}, {control})"] for c1_gate in name_single_qubit_class(target, control)]
    sequence = [
        gate_seq + s1_gate + s1y_gate for s1_gate in name_s1_gates(control) for s1y_gate in name_s1_y_gates(target) for gate_seq in sequence
    ]

    return sequence

def name_iswap_like_class(target,control)->List:
    '''
    Total 5184 C2 clifford gates
    '''    
    sequence = [
        c1_gate + [f"cz({target}, {control})"] + [f"rg_py2({control})"] + [f"rg_nx2({target})"] + [f"cz({target}, {control})"]
        for c1_gate in name_single_qubit_class(target, control)
    ]
    sequence = [
        gate_seq + s1y_gate + s1x_gate for s1y_gate in name_s1_y_gates(control) 
        for s1x_gate in name_s1_x_gates(target) for gate_seq in sequence
    ]

    return sequence

def name_swap_like_class(target, control)->List:
    '''
    Total 576 C2 clifford gates
    '''
    sequence = [
        c1_gate + [f"cz({target}, {control})"] + [f"rg_ny2({control})"] + [f"rg_py2({target})"] + [f"cz({target}, {control})"] +
        [f"rg_py2({control})"] + [f"rg_ny2({target})"] + [f"cz({target}, {control})"] + [f"rg_py2({target})"]        
        for c1_gate in name_single_qubit_class(target, control)
    ]

    return sequence

def name_c2_clifford_gates(target, control)->List:
    '''
    Combine four classes. Total 11520 gates.
    '''
    sequence = name_single_qubit_class(target, control) + name_cnot_like_class(target, control) + name_iswap_like_class(target, control) + name_swap_like_class(target, control)

    return sequence


def get_random_c2_gate(target, control)->List:
    i = np.random.choice(11520)
    clifford_gate = c2_clifford_gates(target,control)[i]
    return i, clifford_gate

def m_random_Clifford_circuit( m, target, control )->QubitCircuit:
    # sequence is comprised of gates: sequence = [[gate],[gate],...]
    # num_seq is comprised of index of these clifford_gates.
    sequence = []
    num_seq = []
    circuit = QubitCircuit(2)
    if m == 0 :
        for gate in c2_clifford_gates(target,control)[0]:
            circuit.add_gate(gate) # Add identity gate
        num_seq.append(str(0))
    else:
        for i in range(m):
            j, clifford_gate = get_random_c2_gate(target, control) # j is the index of this clifford gate
            for gate in clifford_gate:
                sequence.append(gate)
            num_seq.append(str(j))
        for gate in sequence:
            circuit.add_gate(gate)

    return circuit, num_seq

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

def c2_inv_gate(target=1, control=0):
    '''
    Give the list of gates of C2 Clifford, then return the inverse of it from C2 Clifford group.

    Args:
        gates: list  A list of (qutip_qip.circuit.Gate) gate.
    
    Returns:
        list : A list of (qutip_qip.circuit.Gate) gate.  
    '''

    c2_gate_set = c2_clifford_gates(target, control)
    c2_gate_set2 = c2_clifford_gates(target, control)
    name_c2_gate_set = name_c2_clifford_gates(target, control)
    c2_inv_dict = {}
    count = 0
    error_num = 0
    matrix_tuple_list = [tuple(row) for row in name_c2_gate_set]
    inv_matrix_tuple_list = [tuple(row) for row in name_c2_gate_set]

    for i, c2_gate in enumerate(c2_gate_set):
        matrix = decomposition(c2_gate)
        matrix_inv = matrix.inv()
        match_seq = None
        for j, c2_gate_inv in enumerate(c2_gate_set2):
            comparison = decomposition(c2_gate_inv)
            for phase in [
                1,1j,-1,-1j,(1+1j)/np.sqrt(2),(1-1j)/np.sqrt(2),(-1+1j)/np.sqrt(2),(-1-1j)/np.sqrt(2)
                ]:
                if phase * matrix_inv == comparison:
                    match_seq = True
                    count += 1
                    c2_inv_dict[matrix_tuple_list[i]] = inv_matrix_tuple_list[j]
                    print(f'finished c2 gate: {count}')
                    break 
            if match_seq is not None: break
        if match_seq == None:
            error_num += 1
            print(f'error num: {error_num}')
            print(f'operation matrix: {matrix}')
            print(f'operation matrix inv: {matrix_inv}')
        if match_seq is not None: 
            c2_gate_set2.remove(c2_gate_inv)
            inv_matrix_tuple_list.remove(inv_matrix_tuple_list[j])
            

    with open(inv_pairs_path, 'w') as file:
        file.write(f'{c2_inv_dict}')
    print(f'finished c2 gate: {count}')
    print(f'error num: {error_num}')

def c2_inv_pairs_to_num_pairs():
    dict = {}
    with open(inv_pairs_path, 'r') as file:
        content = file.read()
        data_list = ast.literal_eval(content)
        for i, name_gate in enumerate(list(data_list.values())):
            for j, name_inv_clifford_gate in enumerate(name_c2_clifford_gates(target=1, control=0)):
                if list(name_gate) == name_inv_clifford_gate: 
                    dict[str(i)] = str(j)
                    break
            print(f'finish {i}')
    with open(num_pairs_path, 'w') as file:
        file.write(f'{dict}')
    

def get_TQcircuit_random_clifford(target, control, num_gates, mode = 'ONE')->QubitCircuit:
    '''
    Give the number, target and control of C2 Clifford, then return 
    the random gate operation combined with inverse of this operation.

    Args:
        target: int
        control: int
        num_gates: int  A number of C2 Clifford group.
        mode: 'MR' or 'ONE'. 
        'MR' means the inverse gate will be inverse of each Clifford without combination. 
        'ONE' means the inverse gate will be combination of all Clifford gates.

    Returns:
        circuit_RB : Qubitcircuit  Combine all the gate and inverse operation.
    '''
    circuit_RB, num_seq = m_random_Clifford_circuit( num_gates, target, control )
    if mode == 'ONE':   
        c2_gate_inv = find_inv_gate( circuit_RB.gates )
        circuit_RB.add_gates(c2_gate_inv)
    elif mode == 'MR':  
        with open(num_pairs_path, 'r') as file:
            content = file.read()
            data_list = ast.literal_eval(content)
            
        c2_gates = c2_clifford_gates(target, control)
        
        for num in list(reversed(num_seq)): # The order of inversed gate should be reversed to clifford gates
            inv_num = data_list[str(num)]
            c2_gate_inv = c2_gates[int(inv_num)]
            circuit_RB.add_gates(c2_gate_inv)

    return circuit_RB

def test_TQcircuit_random_clifford(target, control, num_gates, mode = 'MR'):
    circuit_RB, num_seq = m_random_Clifford_circuit( num_gates, target, control )
    if mode == 'ONE':
        c2_gate_inv = find_inv_gate( circuit_RB.gates )
        circuit_RB.add_gates(c2_gate_inv)           
        operation = decomposition(circuit_RB.gates)         
        for phase in [
            1,1j,-1,-1j,(1+1j)/np.sqrt(2),(1-1j)/np.sqrt(2),(-1+1j)/np.sqrt(2),(-1-1j)/np.sqrt(2)
                ]:
            if phase * operation == tensor(qeye(2), qeye(2)):
                print('successfully find inverse gate ')
                break   
    elif mode == 'MR':
        with open(r'.\SKILLS\asqpu\src\qpu\application\c2_num_pairs.txt', 'r') as file:
            content = file.read()
            data_list = ast.literal_eval(content)        
        c2_gates = c2_clifford_gates(target, control)
        for num in reversed(num_seq): # The order of inversed gate should be reversed to clifford gates
            inv_num = data_list[str(num)]
            c2_gate_inv = c2_gates[int(inv_num)]
            circuit_RB.add_gates(c2_gate_inv)
        operation = decomposition(circuit_RB.gates)   
        for phase in [
            1,1j,-1,-1j,(1+1j)/np.sqrt(2),(1-1j)/np.sqrt(2),(-1+1j)/np.sqrt(2),(-1-1j)/np.sqrt(2)
                ]:
            if phase * operation == tensor(qeye(2), qeye(2)):
                print('successfully find inverse gate ')
                break           

def get_TQRB_device_setting(backendcircuit:BackendCircuit, num_gates, target=1, control=0, mode='ONE', withRO:bool=False):

    d_setting = []
    circuit_RB = get_TQcircuit_random_clifford(target, control, num_gates, mode)
    
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

'''
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
'''
# if __name__ == '__main__':
    # x = test_TQcircuit_random_clifford(target=1, control=0, num_gates=100, mode = 'MR')
    # target = 1
    # control = 0
    # num_gates = 5
    # mode = 'MR'
    # x = get_TQcircuit_random_clifford(target=1, control=0, num_gates=1, mode='MR' )
    # x = c2_inv_pairs_to_num_pairs()



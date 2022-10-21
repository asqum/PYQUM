
from argparse import Action
from typing import List
import numpy as np
from qutip import sigmax, sigmay, sigmaz, basis, qeye, Qobj
from qutip_qip.circuit import QubitCircuit, Gate
from typing import List

from qpu.backend.circuit.compiler import SQCompiler
from qpu.backend.circuit.backendcircuit import BackendCircuit

def clifford_gates( target:int )->List:
    """
    Get a gate in Clifford group for target qubit
    """
## Basic
## Pi
    rg_i = Gate("RX", target, arg_value= 0)
    rg_x = Gate("RX", target, arg_value= np.pi)
    rg_y = Gate("RY", target, arg_value= np.pi)
    ## Pi/2
    rg_px2 = Gate("RX", target, arg_value= +np.pi/2)
    rg_py2 = Gate("RY", target, arg_value= +np.pi/2)
    rg_nx2 = Gate("RX", target, arg_value= -np.pi/2)
    rg_ny2 = Gate("RY", target, arg_value= -np.pi/2)

    ## Decompose
    ## Pi
    g_z = [rg_y,rg_x]
    ## Pi/2
    g_phz = [rg_nx2,rg_py2,rg_px2]
    g_nhz = [rg_nx2,rg_ny2,rg_px2]
    ## Had
    g_hpxz = [rg_x,rg_ny2]
    g_hnxz = [rg_x,rg_py2]
    g_hpyz = [rg_y,rg_px2]
    g_hnyz = [rg_y,rg_nx2]
    g_hpxy = [rg_px2,rg_py2,rg_px2]
    g_hnxy = [rg_nx2,rg_py2,rg_nx2]
    ## 2pi/3 
    g_pc1 = [rg_py2,rg_px2]
    g_pc2 = [rg_py2,rg_nx2]
    g_pc4 = [rg_ny2,rg_px2]
    g_pc3 = [rg_ny2,rg_nx2]

    g_nc1 = [rg_nx2,rg_py2]
    g_nc2 = [rg_px2,rg_py2]
    g_nc4 = [rg_nx2,rg_ny2]
    g_nc3 = [rg_px2,rg_ny2]

    gates_set = [
        [rg_i],[rg_x],[rg_y],[rg_px2],[rg_nx2],[rg_py2],[rg_ny2],
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




def decomposition( gates:List[Gate] )->Qobj:
    """
        
    Args:
        List : A list of qutip Gate object (qutip_qip.circuit.Gate). 
    
    Returns:
        Qobj (qutip.Qobj): An .
    """
    circuit = QubitCircuit(1)
    eff_op = qeye(2)
    name_seq = []
    for g in gates:
        circuit.add_gate(g)
        name_seq.append(g.name)
        g_qobj = g.get_compact_qobj()
        eff_op = g_qobj *eff_op
        # eff_op = circuit.run(qeye(2))
    return eff_op

def get_random_clifford( num_gates:int )->QubitCircuit:
    
    circuit = QubitCircuit(1)
    single_qubit = basis(2)
    total_op = qeye(2)
    gates_set = clifford_gates(0)

    for ind in np.random.randint(0, len(gates_set), num_gates):
        random_gate = gates_set[ind]
        eff_op = decomposition(random_gate)
        circuit.add_gates(random_gate)
        #print(random_gate.name, random_gate.arg_value/np.pi)
        #print( eff_op )
        single_qubit = eff_op*single_qubit
        total_op = eff_op*total_op
            #print( total_op )
    return circuit

def find_inv_gate( gates:List[Gate] ):
    """get inversed gate from input gates in clifford group.    
    Args:
        gates: list  A list of (qutip_qip.circuit.Gate) gate.
    
    Returns:
        list : A list of (qutip_qip.circuit.Gate) gate.
    """
    operation_eff = decomposition(gates)
    gate_inv = None
    gates_set = clifford_gates(0)
    for gate in gates_set:
        rev_op = operation_eff.inv()
        compared_op = decomposition(gate)
        for g_phase in [1,1j,-1,-1j]:
            if g_phase*rev_op == compared_op:
                gate_inv = gate
    return gate_inv

def find_inv_gate_state( state:List[Gate] ):
    """get inversed gate from input gates in clifford group.    
    Args:
        gates: list  A list of (qutip_qip.circuit.Gate) gate.
    
    Returns:
        list : A list of (qutip_qip.circuit.Gate) gate.
    """
    gate_inv = None
    gates_set = clifford_gates(0)

    for gate in gates_set:
        compared_op = decomposition(gate)
        final_state = compared_op*state
        if abs(abs(final_state[0][0][0])-1)<0.01:
            gate_inv = gate
    return gate_inv


def get_SQcircuit_random_clifford( target:int, num_gates:int ):

    circuit_RB = get_random_clifford( num_gates ) 

    inv_gate = find_inv_gate( circuit_RB.gates )

    circuit_RB.add_gates(inv_gate)
    for g in circuit_RB.gates:
        g.targets = [target]
    return circuit_RB


def get_SQRB_device_setting( backendcircuit:BackendCircuit, num_gates, target:int=0, withRO:bool=False  ):

    d_setting = []
    circuit_RB = get_SQcircuit_random_clifford( target, num_gates )
    if withRO:
        rg_ro = Gate("RO", target )
        circuit_RB.add_gate(rg_ro)


    mycompiler = SQCompiler(1, params={})


    q_name = backendcircuit.q_reg["qubit"][target]
    print(f"{q_name} get RB sequence." )
    q_info = backendcircuit.get_qComp(q_name)
    backendcircuit.total_time = q_info.tempPars["total_time"]

    mycompiler.params["rxy"] = {}
    mycompiler.params["rxy"]["dt"] = backendcircuit.dt
    mycompiler.params["rxy"]["pulse_length"] = q_info.tempPars["XYW"]

    mycompiler.params["ro"] = {}
    mycompiler.params["ro"]["dt"] = backendcircuit.dt
    mycompiler.params["ro"]["pulse_length"] = q_info.tempPars["ROW"]


    waveform_channel = mycompiler.to_waveform(circuit_RB)
    
    d_setting = backendcircuit.devices_setting(waveform_channel)
    d_setting['total_time'] = q_info.tempPars["total_time"]

    return d_setting


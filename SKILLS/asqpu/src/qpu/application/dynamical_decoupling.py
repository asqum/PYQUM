
from argparse import Action
from typing import List
#from pulse_generator.pulse import Pulse
import numpy as np
from qutip import sigmax, sigmay, sigmaz, basis, qeye, Qobj
from qutip_qip.circuit import QubitCircuit, Gate
from typing import List

from qpu.backend.circuit.compiler import SQCompiler
from qpu.backend.circuit.backendcircuit import BackendCircuit

def CPMG( echo_times, free_evo_time ):

    t = free_evo_time/echo_times
    qc = QubitCircuit(1)
    qc.add_gate("RX", 0, arg_value=np.pi/2)
    qc.add_gate("IDLE", 0, arg_value=t/2)
    qc.add_gate("RY", 0, arg_value=np.pi)
    for i in range(echo_times-1):
        qc.add_gate("IDLE", 0, arg_value=t)
        qc.add_gate("RY", 0, arg_value=np.pi)
        
    qc.add_gate("IDLE", 0, arg_value=t/2)
    qc.add_gate("RX", 0, arg_value=np.pi/2)

    return qc

def ramsey( free_evo_time ):

    t = free_evo_time
    qc = QubitCircuit(1)
    qc.add_gate("RX", 0, arg_value=np.pi/2)
    qc.add_gate("IDLE", 0, arg_value=t)
    qc.add_gate("RX", 0, arg_value=np.pi/2)

    return qc

def get_SQDD( target:int, echo_times, free_evo_time ):

    if echo_times == 0:
        qc = ramsey( free_evo_time )
    else:
        qc = CPMG( echo_times, free_evo_time ) 

    for g in qc.gates:
        g.targets = [target]

    return qc


def get_SQDD_device_setting( backendcircuit:BackendCircuit, echo_times, free_evo_time, target:int=0, withRO:bool=False  ):

    d_setting = []
    qc = get_SQDD( target, echo_times, free_evo_time  )
    print(target)
    if withRO:
        rg_ro = Gate("RO", target )
        qc.add_gate(rg_ro)
    mycompiler = SQCompiler(1, params={})
    q_name = backendcircuit.q_reg["qubit"][target]
    print(f"{q_name} get CPMG sequence." )
    q_info = backendcircuit.get_qComp(q_name)
    backendcircuit.total_time = q_info.tempPars["total_time"]
    mycompiler.params["rxy"] = {}
    mycompiler.params["rxy"]["dt"] = backendcircuit.dt
    mycompiler.params["rxy"]["pulse_length"] = q_info.tempPars["XYW"]
    mycompiler.params["anharmonicity"] = q_info.tempPars["anharmonicity"]
    mycompiler.params["a_weight"] = q_info.tempPars["a_weight"]

    mycompiler.params["ro"] = {}
    mycompiler.params["ro"]["dt"] = backendcircuit.dt
    mycompiler.params["ro"]["pulse_length"] = q_info.tempPars["ROW"]


    waveform_channel = mycompiler.to_waveform(qc)
    d_setting = backendcircuit.devices_setting(waveform_channel)
    d_setting["total_time"] = backendcircuit.total_time
    return d_setting


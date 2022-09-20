from math import e
import qpu.backend.phychannel as pch
from qutip import sigmax, sigmay, sigmaz, basis, qeye, tensor, Qobj
from qutip_qip.operations import Gate #Measurement in 0.3.X qutip_qip
from qutip_qip.circuit import QubitCircuit
from qutip_qip.compiler import GateCompiler, Instruction
import numpy as np
import qpu.backend.circuit.backendcircuit as bec
import qpu.backend.component as qcp
from pandas import DataFrame
import pulse_signal.common_Mathfunc as ps 
import qpu.backend.circuit.compiler as becc
def read_phych():
    fo = open("./tests/wiring.txt", "r")
    spec = fo.read()
    fo.close()
    #print(spec)
    dict_list = eval(spec)
    channels = []
    for ch in dict_list:
        #print(ch)
        channels.append( pch.from_dict( ch ) )
    return channels


def read_qComp():
    fo = open("./tests/spec.txt", "r")
    spec = fo.read()
    fo.close()
    #print(spec)
    dict_list = eval(spec)
    qComps = []
    for qc in dict_list:
        #print(ch)
        qComps.append( qcp.from_dict( qc ) )
    return qComps

def read_ChQcomp():
    fo = open("./tests/ChQComp_relation.txt", "r")
    spec = fo.read()
    fo.close()
    #print(spec)
    read_dict = eval(spec)
    
    return DataFrame.from_dict(read_dict)

def read_QReg():
    fo = open("./tests/qRegister.txt", "r")
    spec = fo.read()
    fo.close()
    #print(spec)
    read_dict = eval(spec)
    
    return read_dict

def get_test_bec()->bec.BackendCircuit:
    mybec = bec.BackendCircuit()
    mybec._channels = read_phych()
    mybec._qComps = read_qComp()
    mybec.qc_relation = read_ChQcomp()
    mybec.q_reg = read_QReg()
    return mybec

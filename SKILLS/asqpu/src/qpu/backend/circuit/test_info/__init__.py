from math import e
import qpu.backend.phychannel as pch
import numpy as np
import qpu.backend.circuit.backendcircuit as bec
import qpu.backend.component as qcp
from pandas import DataFrame

# import sys
# sys.path.append(".")
from pathlib import Path

path = Path(__file__).parent

def read_phych():
    fo = open(f"{path}\wiring.txt", "r")
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
    fo = open(f"{path}\spec.txt", "r")
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
    fo = open(f"{path}\ChQComp_relation.txt", "r")
    spec = fo.read()
    fo.close()
    #print(spec)
    read_dict = eval(spec)
    
    return DataFrame.from_dict(read_dict)

def read_QReg():
    fo = open(f"{path}\qRegister.txt", "r")
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
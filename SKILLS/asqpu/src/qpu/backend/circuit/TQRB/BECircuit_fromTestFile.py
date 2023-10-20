from math import e
import qpu.backend.phychannel as pch
import numpy as np
import qpu.backend.circuit.backendcircuit as bec
import qpu.backend.component as qcp
from pandas import DataFrame
import os
ROOT_DIR = os.path.dirname(os.path.abspath(r".\SKILLS\asqpu\src\qpu\backend\circuit\TQRB\BECircuit_test_2Q.py"))

def read_location( location_path ):
    # location.txt contains three parts: 
    # real physical channel (_channels),
    # channels' id and corresponding qubits (qc_relation),
    # ubits type and id (q_reg)
    
    fo = open(location_path, "r")
    locstr = fo.read()
    fo.close() 
    locstr = locstr.split("===")
    return read_phych(locstr[0]), read_ChQcomp(locstr[1]), read_QReg(locstr[2])

def read_qComp( spec_path ):
    fo = open(spec_path, "r")
    infostr = fo.read()
    fo.close()
    #print(spec)
    dict_list = eval(infostr)
    qComps = []
    for qc in dict_list:
        #print(ch)
        qComps.append( qcp.from_dict( qc ) )
    return qComps

def read_phych( infostr ):
    dict_list = eval(infostr)
    channels = []
    for ch in dict_list:
        #print(ch)
        channels.append( pch.from_dict( ch ) )
    return channels

def read_ChQcomp( infostr ):
    read_dict = eval(infostr)
    return DataFrame.from_dict(read_dict)

def read_QReg( infostr ):
    read_dict = eval(infostr)
    
    return read_dict

def get_test_bec()->bec.BackendCircuit:
    location_path = os.path.join(ROOT_DIR, "location.txt")
    spec_path = os.path.join(ROOT_DIR, "spec.txt")
    mybec = bec.BackendCircuit()
    mybec._channels, mybec.qc_relation, mybec.q_reg = read_location(location_path)
    mybec._qComps = read_qComp(spec_path)

    return mybec
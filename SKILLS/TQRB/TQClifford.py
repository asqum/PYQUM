from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from argparse import Action
from typing import List
#from pulse_generator.pulse import Pulse
import numpy as np
from qutip import sigmax, sigmay, sigmaz, basis, qeye, Qobj
from qutip_qip.circuit import QubitCircuit, Gate
from typing import List
from pulse_signal.common_Mathfunc import ErfAmplifier

from qpu.backend.circuit.compiler import SQCompiler
from qpu.backend.circuit.backendcircuit import BackendCircuit

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

def c1_gates(target:int)->List:
    """
    Get a gate in Clifford group for single qubit
    """
## Decompose
## Pi
    g_z = [rg_x(target), rg_y(target)]
## Pi/2
    g_phz = [rg_px2(target),rg_py2(target),rg_nx2(target)]
    g_nhz = [rg_px2(target),rg_ny2(target),rg_nx2(target)]
## Had
    g_hpxz = [rg_ny2(target),rg_x(target)]
    g_hnxz = [rg_py2(target),rg_x(target)]
    g_hpyz = [rg_px2(target),rg_y(target)]
    g_hnyz = [rg_nx2(target),rg_y(target)]
    g_hpxy = [rg_px2(target),rg_py2(target),rg_px2(target)]
    g_hnxy = [rg_nx2(target),rg_py2(target),rg_nx2(target)]
## 2pi/3 
    g_pc1 = [rg_px2(target),rg_py2(target)]
    g_pc2 = [rg_nx2(target),rg_py2(target)]
    g_pc4 = [rg_px2(target),rg_ny2(target)]
    g_pc3 = [rg_nx2(target),rg_ny2(target)]

    g_nc1 = [rg_py2(target),rg_nx2(target)]
    g_nc2 = [rg_py2(target),rg_px2(target)]
    g_nc4 = [rg_ny2(target),rg_nx2(target)]
    g_nc3 = [rg_ny2(target),rg_px2(target)]

    gates_set = [
        [rg_i(target)],[rg_x(target)],[rg_y(target)],[rg_px2(target)],[rg_nx2(target)]
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
    s_12 = [rg_px2(target),rg_py2(target)]
    s_13 = [rg_ny2(target),rg_nx2(target)]
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
    s_32 = [rg_px2(target),rg_y(target)]
    s_33 = [rg_px2(target),rg_ny2(target),rg_nx2(target)]
    gates_set = [s_31,s_32,s_33]

    return gates_set

def get_random_c1( target )->Gate:
    # Assign a target qubit a random C1 clifford gate 

    return None
    
x = c1_gates(target=0)
print(np.random.choice(c1_gates(0)))

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

def c1_gates( target:int )->List:
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

def s1_gates( target:int )->List:



def s1_x_gates( target:int )->List:
def s1_y_gates( target:int )->List:
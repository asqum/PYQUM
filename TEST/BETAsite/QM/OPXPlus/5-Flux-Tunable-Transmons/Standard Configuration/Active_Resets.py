
from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from configuration import *
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.plot import interrupt_on_close
from qualang_tools.loops import from_array
import matplotlib.pyplot as plt
from scipy import signal
import warnings




with program() as active_reset:
    I = declare(fixed)
    th = declare(fixed, value=0)
    measure('readout', 'resonator', None, demod.full('cos', I))
    play('pi', 'qubit', condition=I>th)


with program() as active_reset_RUS:
    I = declare(fixed)
    th1 = declare(fixed, value=0.2)
    th2 = declare(fixed, value=0.1)    
    with while_(I>th1):
        measure('readout', 'resonator', None, demod.full('cos', I))
        play('pi', 'qubit', condition=I>th2)

def update_threshold(n, state):
    assign(th, ...)

with program() as active_reset_dynamic_th:
    n = declare(int)
    N = declare(int, value=8)   # Number of iterations to reset the qubit
    I = declare(fixed)
    th = declare(fixed, value=0)
    state = declare(bool, size=N)
    lookup_table = declare(fixed, value=python_loopup_table)
    with for_(n, 0, n<N, n+1):
        measure('readout', 'resonator', None, demod.full('cos', I))
        assign(state[n], I>th)
        play('pi', 'qubit', condition=state[n])
        update_threshold(n, state[n])

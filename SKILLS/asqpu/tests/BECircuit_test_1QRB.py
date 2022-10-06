from math import e
import qpu.backend.phychannel as pch
from qutip import sigmax, sigmay, sigmaz, basis, qeye, tensor, Qobj
from qutip_qip.operations import Gate #Measurement in 0.3.X qutip_qip
from qutip_qip.circuit import QubitCircuit
import numpy as np
import qpu.application as qapp

import qpu.backend.circuit 
import pulse_signal.common_Mathfunc as ps 
import qpu.backend.circuit.compiler as becc
import sys
sys.path.append("..")
from BECircuit_fromTestFile import get_test_bec
import matplotlib.pyplot as plt



mybec = get_test_bec()

for i in range(1):
    d_setting = qapp.get_SQRB_device_setting( mybec, 5, 0, True  )


    #print(mybec.load_coeff(coeffs))


    dac_wf = d_setting["DAC"]
    for dcategory in d_setting.keys():
        print(dcategory, d_setting[dcategory].keys())
    # Plot setting
    fig, ax = plt.subplots(1,1,sharex=True)

    # Compare signal and envelope
    for instr_name, settings in dac_wf.items():
        for i, s in enumerate(settings):
            if type(s) != type(None):
                ax.plot( s, label=f"{instr_name}-{i+1}" )
    ax.legend()

    plt.show()


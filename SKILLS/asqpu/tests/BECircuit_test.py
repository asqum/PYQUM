from math import e
import qpu.backend.phychannel as pch
from qutip import sigmax, sigmay, sigmaz, basis, qeye, tensor, Qobj
from qutip_qip.operations import Gate #Measurement in 0.3.X qutip_qip
from qutip_qip.circuit import QubitCircuit
import numpy as np
import qpu.backend.circuit.backendcircuit as bec

import pulse_signal.common_Mathfunc as ps 
import qpu.backend.circuit.compiler as becc
import sys
sys.path.append("..")
from BECircuit_fromTestFile import get_test_bec

rg_ro0 = Gate("RO", 0 )
rg_x0 = Gate("RX", 0, arg_value= np.pi)
rg_y0 = Gate("RY", 0, arg_value= np.pi)
rg_z0 = Gate("RZ", 0, arg_value= 500)

rg_ro1 = Gate("RO", 1 )
rg_x1 = Gate("RX", 1, arg_value= np.pi)
rg_y1 = Gate("RY", 1, arg_value= np.pi)
rg_z1 = Gate("RZ", 1, arg_value= 500)

gate_seq = [
    rg_x1, rg_x1, rg_y1, rg_y1, rg_x1, rg_z1, rg_ro1
]
circuit = QubitCircuit(1)

single_qubit = basis(2, 0)
for gate in gate_seq:
    circuit.add_gate(gate)
    #g_qobj = gate.get_compact_qobj()
    #print( g_qobj )
    #total_op *= g_qobj
#print( "Result" )
#print( total_op )

mycompiler = becc.SQCompiler(1, params={})
#print(mycompiler.gate_compiler)

# raw circuit
for gate in circuit.gates:
    print(f"{gate.name} for {gate.targets}")

#     print(gate.name, gate.get_compact_qobj())

# After transpile
# total_op = qeye(2)
# trans_QC = myprocessor.transpile(circuit)
# for gate in trans_QC.gates:
#     total_op *= gate.get_compact_qobj()
# print(total_op)

compiled_data = mycompiler.compile(circuit, schedule_mode=False)

tlist = compiled_data[0]
coeffs = compiled_data[1]
print(coeffs.keys())

# plt.plot(tlist["sx0"],coeffs["sx0"], label="sx0")
# plt.plot(tlist["sy0"],coeffs["sy0"], label="sy0")
# plt.legend()
# plt.show()


mybec = get_test_bec()

#print(mybec.load_coeff(coeffs))

ch_wf = mybec.translate_channel_output(coeffs)
d_setting = mybec.devices_setting(coeffs)
dac_wf = d_setting["DAC"]

import json
with open('d_setting.txt', 'w') as file:
    file.write(str(d_setting)) # use `json.loads` to do the reverse


for dcategory in d_setting.keys():
    print(dcategory, d_setting[dcategory].keys())
# Plot setting
import matplotlib.pyplot as plt
fig, ax = plt.subplots(3,1,sharex=True)

# Compare signal and envelope
for cl in coeffs.keys():
    ax[0].plot( coeffs[cl], label=cl )
ax[0].legend()

# Compare signal and envelope
for ch_name in ch_wf.keys():
    print(ch_name)
    if type(ch_wf[ch_name][0]) != type(None):
        ax[1].plot( ch_wf[ch_name][0].real, label=f"{ch_name}.real" )
        ax[1].plot( ch_wf[ch_name][0].imag, label=f"{ch_name}.imag" )
ax[1].legend()

# Compare signal and envelope
for dacname in dac_wf.keys():
    if type(dac_wf[dacname]) != type(None):
        ax[2].plot( dac_wf[dacname], label=dacname )
ax[2].legend()

plt.show()


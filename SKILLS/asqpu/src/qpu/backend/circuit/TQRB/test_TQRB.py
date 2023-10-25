from math import e
import qpu.backend.phychannel as pch
from qutip import sigmax, sigmay, sigmaz, basis, qeye, tensor, bell_state, Qobj
from qutip_qip.operations import Gate, Measurement #Measurement in 0.3.X qutip_qip
from qutip_qip.circuit import QubitCircuit
import numpy as np
from qutip_qip.operations.gates import expand_operator
import pulse_signal.common_Mathfunc as ps 
from qpu.application.TQClifford import m_random_Clifford_circuit, get_TQcircuit_random_clifford
from TQCompiler import TQCompile
import sys
sys.path.append("..")
from BECircuit_fromTestFile import get_test_bec

mybec = get_test_bec()

# sampling rate: 0.5 ns/#
mybec.dt = 0.5

rg_ro = Gate("RO", [1,0] )

circuit = get_TQcircuit_random_clifford(target=1, control=0, num_gates=0, mode='MR')
circuit.add_gate(rg_ro)

mycompiler = TQCompile(2, params={})
q1_name = mybec.q_reg["qubit"][0]
q1_info = mybec.get_qComp(q1_name)
mybec.total_time = q1_info.tempPars["total_time"]
q2_name = mybec.q_reg["qubit"][1]
q2_info = mybec.get_qComp(q2_name)
qubit_info = [q1_info,q2_info]

# Give parameters to TQCompiler
for qi in range(2):
    mycompiler.params[str(qi)] = {}
    mycompiler.params[str(qi)]["rxy"] = {}
    mycompiler.params[str(qi)]["rxy"]["dt"] = mybec.dt
    mycompiler.params[str(qi)]["rxy"]["pulse_length"] = q1_info.tempPars["XYW"]
    mycompiler.params[str(qi)]["anharmonicity"] = q1_info.tempPars["anharmonicity"]
    mycompiler.params[str(qi)]["cz"] = {}
    mycompiler.params[str(qi)]["cz"]["type"] = qubit_info[qi].tempPars["CZ"]["type"]    
    mycompiler.params[str(qi)]["cz"]["dt"] = mybec.dt
    mycompiler.params[str(qi)]["cz"]["pulse_length"] = qubit_info[qi].tempPars["CZ"]["ZW"]
    mycompiler.params[str(qi)]["cz"]["dz"] = qubit_info[qi].tempPars["CZ"]["dZ"]
    mycompiler.params[str(qi)]["cz"]["c_Z"] = qubit_info[qi].tempPars["CZ"]["c_Z"]    
    mycompiler.params[str(qi)]["cz"]["c_ZW"] = qubit_info[qi].tempPars["CZ"]["c_ZW"]
    mycompiler.params[str(qi)]["cz"]["xyr"] = qubit_info[qi].tempPars["CZ"]["XYR"]   
    mycompiler.params[str(qi)]["cz"]["waveform"] = qubit_info[qi].tempPars["CZ"]["waveform&edge&sigma"]
    mycompiler.params[str(qi)]["cz"]["c_waveform"] = qubit_info[qi].tempPars["CZ"]["c_waveform&edge&sigma"]    
    mycompiler.params[str(qi)]["iswap"] = {}
    mycompiler.params[str(qi)]["iswap"]["type"] = qubit_info[qi].tempPars["ISWAP"]["type"]  
    mycompiler.params[str(qi)]["iswap"]["dt"] = mybec.dt
    mycompiler.params[str(qi)]["iswap"]["pulse_length"] = qubit_info[qi].tempPars["ISWAP"]["ZW"]
    mycompiler.params[str(qi)]["iswap"]["dz"] = qubit_info[qi].tempPars["ISWAP"]["dZ"]
    mycompiler.params[str(qi)]["iswap"]["c_Z"] = qubit_info[qi].tempPars["ISWAP"]["c_Z"]
    mycompiler.params[str(qi)]["iswap"]["c_ZW"] = qubit_info[qi].tempPars["ISWAP"]["c_ZW"]
    mycompiler.params[str(qi)]["iswap"]["xyr"] = qubit_info[qi].tempPars["ISWAP"]["XYR"]  
    mycompiler.params[str(qi)]["iswap"]["waveform"] = qubit_info[qi].tempPars["ISWAP"]["waveform&edge&sigma"]
    mycompiler.params[str(qi)]["iswap"]["c_waveform"] = qubit_info[qi].tempPars["ISWAP"]["c_waveform&edge&sigma"]
    mycompiler.params[str(qi)]["waveform"] = qubit_info[qi].tempPars["waveform&alpha&sigma"]    
mycompiler.params["ro"] = {}
mycompiler.params["ro"]["pulse_length"] = q1_info.tempPars["ROW"]
mycompiler.params["ro"]["dt"] = mybec.dt
mycompiler.params["a_weight"] = 0    
mycompiler.params["img_ratio"] = 0.5

with open(r'.\SKILLS\asqpu\src\qpu\backend\circuit\TQRB\TQRBmycompiler_params.txt', 'w') as file:
    file.write(str(mycompiler.params)) # use `json.loads` to do the reverse

# # raw circuit
# for gate in circuit.gates:
#     print(f"{gate.name} for {gate.targets}")

compiled_data = mycompiler.compile(circuit,schedule_mode='ASAP')
tlist = compiled_data[0]
coeffs = compiled_data[1]

ch_wf = mybec.translate_channel_output(mycompiler.to_waveform(circuit,schedule_mode='ASAP'))
d_setting = mybec.devices_setting(mycompiler.to_waveform(circuit,schedule_mode='ASAP'))
dac_wf = d_setting["DAC"]

with open('d_setting.txt', 'w') as file:
    file.write(str(d_setting)) # use `json.loads` to do the reverse


for dcategory in d_setting.keys():
    print(dcategory, d_setting[dcategory].keys())
# Plot setting
import matplotlib.pyplot as plt
fig, ax = plt.subplots(3,1,sharex=True)

# Compare signal and envelope
for cl in coeffs.keys():
    ax[0].plot(coeffs[cl],label=cl )
ax[0].set_xlim([0, 40000])
ax[0].legend(fontsize="5")

# Compare signal and envelope
for ch_name in ch_wf.keys():
    print(ch_name)
    if type(ch_wf[ch_name][0]) != type(None):
        ax[1].plot( ch_wf[ch_name][0][0].real, label=f"{ch_name}.real" )
        ax[1].plot( ch_wf[ch_name][0][0].imag, label=f"{ch_name}.imag" )
ax[1].set_xlim([0, 40000])
ax[1].legend(fontsize="5")

# Compare signal and envelope
for instr_name, settings in dac_wf.items():
    # print(instr_name)
    for i, s in enumerate(settings):
        if type(s) != type(None):
            ax[2].plot( s, label=f"{instr_name}-{i+1}" )
ax[2].set_xlim([0, 40000])
ax[2].legend(fontsize="5")

plt.show()


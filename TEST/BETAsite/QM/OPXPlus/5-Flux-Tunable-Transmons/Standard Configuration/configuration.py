from pathlib import Path

import sys
print("Absolute Path: " + str(Path().absolute()))
sys.path.append(str(Path().absolute()/"TEST"/"BETAsite"/"QM"/"OPXPlus"/"Configurations"))
# sys.path.append(str(Path().absolute()/"PYQUM"/"TEST"/"BETAsite"/"QM"/"OPXPlus"/"Configurations"))
from configuration_AS_5q4c_dr2a_new_qua import *

QPU = {
    "q1": {
        "readout": {
            "frequency": resonator_LO + resonator_IF_q1,
            "length": readout_len
        },
        "control": {
            "frequency": qubit_LO_q1 + qubit_IF_q1,
            "T1": qubit1_T1
        },
    },
    "q2": {
        "readout": {
            "frequency": resonator_LO + resonator_IF_q2,
            "length": readout_len
        },
        "control": {
            "frequency": qubit_LO_q2 + qubit_IF_q2,
            "T1": qubit2_T1
        },
    },
    "q3": {
        "readout": {
            "frequency": resonator_LO + resonator_IF_q3,
            "length": readout_len
        },
        "control": {
            "frequency": qubit_LO_q3 + qubit_IF_q3,
            "T1": qubit3_T1
        },
    },
    "q4": {
        "readout": {
            "frequency": resonator_LO + resonator_IF_q4,
            "length": readout_len
        },
        "control": {
            "frequency": qubit_LO_q4 + qubit_IF_q4,
            "T1": qubit4_T1
        },
    },
    "q5": {
        "readout": {
            "frequency": resonator_LO + resonator_IF_q5,
            "length": readout_len
        },
        "control": {
            "frequency": qubit_LO_q5 + qubit_IF_q5,
            "T1": qubit5_T1
        },
    },
}

# print("QPU q1 readout frequency: %s Hz" %(QPU["q1"]["readout"]["frequency"]))
print("QPU q1 control frequency: %s Hz" %(QPU["q1"]["control"]["frequency"]))
# print("QPU q2 readout frequency: %s Hz" %(QPU["q2"]["readout"]["frequency"]))
print("QPU q2 control frequency: %s Hz" %(QPU["q2"]["control"]["frequency"]))
# print("QPU q3 readout frequency: %s Hz" %(QPU["q3"]["readout"]["frequency"]))
print("QPU q3 control frequency: %s Hz" %(QPU["q3"]["control"]["frequency"]))
# print("QPU q4 readout frequency: %s Hz" %(QPU["q4"]["readout"]["frequency"]))
print("QPU q4 control frequency: %s Hz" %(QPU["q4"]["control"]["frequency"]))
# print("QPU q5 readout frequency: %s Hz" %(QPU["q5"]["readout"]["frequency"]))
print("QPU q5 control frequency: %s Hz" %(QPU["q5"]["control"]["frequency"]))

# Flux offset (at idle-point) 
# for i in range(5):
#     flux_offset = config["controllers"]["con2"]["analog_outputs"][
#         config["elements"][f"q{i+1}_z"]["singleInput"]["port"][1]
#     ]["offset"]
#     print("flux_offset for q%s: %s" %(i+1, flux_offset))

print("running local experiments.. ")  
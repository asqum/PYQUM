from pathlib import Path

import sys
print("Absolute Path: " + str(Path().absolute()))
# sys.path.append(str(Path().absolute()/"TEST"/"BETAsite"/"QM"/"OPXPlus"/"Configurations"))
sys.path.append(str(Path().absolute()/"PYQUM"/"TEST"/"BETAsite"/"QM"/"OPXPlus"/"Configurations"))
from configuration_2q_flux_transmon import *

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
    }
}

print("QPU q1 readout frequency: %s Hz" %(QPU["q1"]["readout"]["frequency"]))
print("QPU q1 control frequency: %s Hz" %(QPU["q1"]["control"]["frequency"]))
print("QPU q2 readout frequency: %s Hz" %(QPU["q2"]["readout"]["frequency"]))
print("QPU q2 control frequency: %s Hz" %(QPU["q2"]["control"]["frequency"]))
# print("QPU q3 readout frequency: %s Hz" %(QPU["q3"]["readout"]["frequency"]))
# print("QPU q3 control frequency: %s Hz" %(QPU["q3"]["control"]["frequency"]))


from pathlib import Path

import sys
sys.path.append(str(Path().absolute()/"PYQUM"/"TEST"/"BETAsite"/"QM"/"OPXPlus"/"Configurations"))
from configuration_qctrl import *

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
            "frequency": qubit_LO_q1 + qubit_IF_q1,
            "T1": qubit1_T1
        },
    }
}

print("QPU q1 readout frequency: %s" %(QPU["q1"]["readout"]["frequency"]))


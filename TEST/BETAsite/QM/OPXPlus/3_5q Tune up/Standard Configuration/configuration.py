from pathlib import Path

import sys
sys.path.append(str(Path().absolute()/"TEST"/"BETAsite"/"QM"/"OPXPlus"/"Configurations"))
# sys.path.append(str(Path().absolute()/"PYQUM"/"TEST"/"BETAsite"/"QM"/"OPXPlus"/"Configurations"))
from configuration_5q_dr2b import *

qubit_num = 5

# Initialization:
QPU = {}
for i in range(qubit_num):
    QPU["q%s"%(i+1)] = {}
    QPU["q%s"%(i+1)]["readout"] = {}
    QPU["q%s"%(i+1)]["control"] = {}
    QPU["q%s"%(i+1)]["readout"]["length"]= readout_len

for i in range(qubit_num):
    QPU["q%s"%(i+1)]["readout"]["frequency"] = resonator_LO + resonator_IF[i]
    QPU["q%s"%(i+1)]["control"]["frequency"] = eval("qubit_LO_q%s"%(i+1)) + qubit_IF[i]

    if i==0:
        print("QPU q%s readout frequency: %s GHz" %(i+1, int(QPU["q%s"%(i+1)]["readout"]["frequency"])*1e-9))
        print("QPU q%s readout frequency: %s GHz" %(i+1, int(QPU["q%s"%(i+1)]["control"]["frequency"])*1e-9))


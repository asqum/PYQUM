from pathlib import Path

import sys
print("Absolute Path: " + str(Path().absolute()))

# For running PYQUM:
sys.path.append(str(Path().absolute().parent/"BETAsite"/"QM"/"OPXPlus"/"Configurations"))
# For VS-Code workspace:
sys.path.append(str(Path().absolute()/"TEST"/"BETAsite"/"QM"/"OPXPlus"/"Configurations"))

from configuration_AS_5q4c_dr2a_new_qua import *

print("resonator_IF_q1: %s" %resonator_IF_q1)

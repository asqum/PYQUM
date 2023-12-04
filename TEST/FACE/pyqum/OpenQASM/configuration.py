from pathlib import Path

import sys
print("Absolute Path: " + str(Path().absolute()))

# For running PYQUM:
sys.path.append(str(Path().absolute().parent/"BETAsite"/"QM"/"OPXPlus"/"Configurations"))
# For VS-Code workspace:
sys.path.append(str(Path().absolute()/"TEST"/"BETAsite"/"QM"/"OPXPlus"/"Configurations"))

from configuration_2q_flux_transmon import *


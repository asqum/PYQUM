"""
This file is used to configure the Octave ports (gain, switch_mode, down-conversion) and calibrate the up-conversion mixers.
You need to run this file in order to update the Octaves with the new parameters.
"""
from set_octave import ElementsSettings, octave_settings
from qm.QuantumMachinesManager import QuantumMachinesManager
from configuration import *

# Configure the Octave parameters for each element
# LO 1-1:
rr1 = ElementsSettings("rr1", gain=10, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
rr2 = ElementsSettings("rr2", gain=10, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
rr3 = ElementsSettings("rr3", gain=10, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
rr4 = ElementsSettings("rr4", gain=10, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
rr5 = ElementsSettings("rr5", gain=10, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
# LO 1-2:
q1_xy = ElementsSettings("q1_xy", gain=15)
q3_xy = ElementsSettings("q3_xy", gain=15)
# LO 1-3:
q2_xy = ElementsSettings("q2_xy", gain=20)
q4_xy = ElementsSettings("q4_xy", gain=20)
# LO 2-1:
q5_xy = ElementsSettings("q5_xy", gain=20)

# Add the "octave" elements
q1, q2, q3, q4, q5 = [rr1, q1_xy], [rr2, q2_xy], [rr3, q3_xy], [rr4, q4_xy], [rr5, q5_xy]
elements_settings = q1 + q2 + q3 + q4 + q5
# elements_settings = q2 + q4
# elements_settings = q5

###################
# Octave settings #
###################
# Configure the Octave according to the elements settings and calibrate
qmm = QuantumMachinesManager(
    host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config, log_level="ERROR"
)
print("Running QUA version: %s" %(qmm.version()))

octave_settings(
    qmm=qmm,
    config=config,
    octaves=octaves,
    elements_settings=elements_settings,
    calibration=True,
)
qmm.close()

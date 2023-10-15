"""
This file is used to configure the Octave ports (gain, switch_mode, down-conversion) and calibrate the up-conversion mixers.
You need to run this file in order to update the Octaves with the new parameters.
"""
from set_octave import ElementsSettings, octave_settings
from qm.QuantumMachinesManager import QuantumMachinesManager
from configuration import *

# Configure the Octave parameters for each element
rr1 = ElementsSettings("rr1", gain=10, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
rr2 = ElementsSettings("rr2", gain=10, rf_in_port=["octave1", 1], down_convert_LO_source="Internal")
q1_xy = ElementsSettings("q1_xy", gain=6)
q2_xy = ElementsSettings("q2_xy", gain=6)
# Add the "octave" elements
elements_settings = [rr1, rr2]

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

from qpu.backend.component.q_component import QComponent
from qpu.backend.component.qubit.transmon import Transmon


def from_dict( info:dict )->QComponent:
    if info["type"] == "qubit":
        qubitObj = Transmon(info["id"])
        qubitObj.tempPars = info
        # qubitObj.transition_freq = info["freq_xy"]
        # qubitObj.sensitivity_RF = info["coupling_xy"]
        # qubitObj.sensitivity_flux = info["coupling_z"]
        # qubitObj.readout_freq = info["freq_ro"]
        # qubitObj.readout_power = info["power_ro"]
        # qubitObj.Ec = info["Ec"]
    else:
        qubitObj = QComponent(info["id"])
    return qubitObj
from qpu.backend.instruments.api import device_from_dict
from qpu.backend.phychannel.api import channel_from_dict
from qpu.backend.action.api import action_from_dict

from qpu.backend.component.api import qComponent_from_dict
from qpu.backend.circuit.backendcircuit import PhysicalCircuit
from pandas import DataFrame
from typing import List


def base_circuit_from_str( specification:str )->PhysicalCircuit:

    specification_list = specification.split("===")


    baseCir = PhysicalCircuit()
    q_component_list = eval(specification_list[2])
    for q in q_component_list:
        baseCir.register_qubit( qComponent_from_dict( q ) )

    device_list = eval(specification_list[4])
    for device in device_list:
        for deviceObj in device_from_dict(device):
            baseCir.register_device( deviceObj )

    channel_list = eval(specification_list[6])
    for ch_dict in channel_list:
        PChObj = channel_from_dict( ch_dict )
        for device_type in ch_dict["devices"].keys():
            devices = ch_dict["devices"][device_type]
            for devices_id in devices:
                if devices_id in baseCir.get_IDs_devices():
                    PChObj.register_device(baseCir.get_device(devices_id))
        PChObj.port = ch_dict["port"]
        baseCir.register_channel(PChObj)

    action_list = eval(specification_list[8])
    for a_dict in action_list:
        actionObj = action_from_dict(a_dict)
        baseCir.register_action(actionObj)

    qa_relation_dict = eval(specification_list[10])
    baseCir.qa_relation = DataFrame.from_dict(qa_relation_dict)


    qc_relation_dict = eval(specification_list[12])
    baseCir.qc_relation = DataFrame.from_dict(qc_relation_dict)
    return baseCir

def to_deviceManager( location:str, typeList: List ):
    """
    Output the dictionary for CHAR or QPC
    """
    # Initialize dict with keys from typeList, with empty list value
    device_dict = dict.fromkeys(typeList,[])
    for t in device_dict.keys():
        device_dict[t] = []

    # To dict {"device type":"device name (str array)"}
    device_list = eval(location)
    for device in device_list:
        for deviceType in typeList:
            if device["type"] == deviceType:
                device_dict[deviceType].append(device["id"])


    DM_dict = {
        "ROLE":f"{}"
    }
    for t in device_dict.keys():
        DM_dict[t] = ",".join(DM_dict[t])
                
    return DM_dict
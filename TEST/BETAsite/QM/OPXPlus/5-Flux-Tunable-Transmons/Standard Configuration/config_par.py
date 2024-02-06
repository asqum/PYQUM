


def get_offset( element, config ):
    port_info = config["elements"][element]["singleInput"]["port"]
    con_name = port_info[0]
    port_name = port_info[1]

    offset = config["controllers"][con_name]["analog_outputs"][port_name]["offset"]
    return offset

def get_IF( element, config ):
    return config["elements"][element]["intermediate_frequency"]

def get_LO( element, config ):
    return config["elements"][element]["mixInputs"]["lo_frequency"]

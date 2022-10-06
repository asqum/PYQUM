from qpu.backend.phychannel.physical_channel import PhysicalChannel, UpConversionChannel, DACChannel, DownConversionChannel, PumpingLine


def from_dict( channel:dict )->PhysicalChannel:
    category = channel["type"]
    name = channel["id"]
    #print("api", name, category)
    
    match category:
        case "up":    
            PChObj = UpConversionChannel(name)
            PChObj.devices = channel["devices"]
            PChObj.comps = channel["comps"]
            PChObj.freqIF = channel["freqIF"] 

        case "dir":    
            PChObj = DACChannel(name)
            PChObj.devices = channel["devices"]
        case "down":    
            PChObj = DownConversionChannel(name)
            PChObj.devices = channel["devices"]
        case "pump":    
            PChObj = PumpingLine(name)
            PChObj.devices = channel["devices"]
        case _:
            print("channel category not defined")
            return None
    PChObj.port = channel["port"]

    print(f"api name: {PChObj.name} port:{PChObj.port} class: {type(PChObj)}")

    return PChObj

    

from qpu.backend.phychannel.physical_channel import PhysicalChannel, UpConversionChannel, DACChannel, DownConversionChannel, PumpingLine


def from_dict( channel:dict )->PhysicalChannel:
    category = channel["type"]
    name = channel["name"]
    #print("api", name, category)
    
    match category:
        case "up":    
            PChObj = UpConversionChannel(name)
        case "dir":    
            PChObj = DACChannel(name)
        case "down":    
            PChObj = DownConversionChannel(name)
        case "pump":    
            PChObj = PumpingLine(name)

        case _:
            print("channel category not defined")
            return None
    PChObj.devices = channel["devices"]
    PChObj.paras = channel["paras"] 
    PChObj.port = channel["port"]

    print(f"api name: {PChObj.name} port:{PChObj.port} class: {type(PChObj)}")

    return PChObj

    

from qpu.backend.action.basic_action import PhysicalAction, RXYOperation, RZOperation, Measurement


def action_from_dict( a_dict:dict ):
    if a_dict["type"]=="RXYOperation": 
        actionObj = RXYOperation(a_dict["id"])
    if a_dict["type"]=="RZOperation": 
        actionObj = RZOperation(a_dict["id"])
    if a_dict["type"]=="Measurement": 
        actionObj = Measurement(a_dict["id"])
        
    actionObj.duration = float(a_dict["duration"])
    return actionObj


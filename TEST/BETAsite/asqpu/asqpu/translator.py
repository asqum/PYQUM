from asqpu.hardware_information import *
from ast import literal_eval


# API
def delete_char_in_string( string:str, delChar:list ):
    """
    Remove all char in 'delChar' from the 'string'
    """
    for c in delChar:
        string.replace(c, "")
    return string

def create_QPU_by_route( qpuid:str, routeString:str ):
    """
    'qpuid' is the id for the QPU\n
    'routeString' example:\n
    Q1,Q2/RO1/I1+Q1:DAC=SDAWG_6-1+SDAWG_6-2,SG=DDSLO_4,ADC=SDDIG_2;Q1/XY1/X1+Y1:DAC=SDAWG_4-1+SDAWG_4-2,SG=DDSLO_3;Q1/Z1:DAC=SDAWG_4-3;
    """
    routeString=delete_char_in_string(routeString, [" ","\n"])
    newQPU = QuantumProcessUnit(qpuid)
    phyChannels = []
    for singleString in routeString.split(";"):
        if singleString == "": break
        qCh = singleString.split(":")[0].split("/")

        phyChID = qCh[1]
        phyCh = PhysicalChannel(phyChID)

        if len(qCh) == 2: phyCh.coupled = [phyChID]
        else: phyCh.coupled = qCh[2].split("+")
 
        devices = singleString.split(":")[1].split(",")
        
        for d in devices:
            deviceType = d.split("=")[0]
            deviceID = d.split("=")[1].split("+")
            phyCh.register_device(deviceID,deviceType)
        phyChannels.append(phyCh)
        newQPU.register_PhysicalChannel(phyCh)
        phyQIDs = qCh[0].split(",")
        for qid in phyQIDs:
            if newQPU.isExist_PhysicalQubit(qid):
                newQPU.assign_channelToQubit( qid, [phyCh.id] )
            else:    
                newQPU.register_PhysicalQubit( qid, [phyCh.id] )
            

    return newQPU

def get_QPCinstrument( qpu:QuantumProcessUnit, instrumentList:list )->dict:
    QPC_list = instrumentList
    instrumentDict = dict.fromkeys(QPC_list,"")

    for devicesType in QPC_list:
        devicesList = []

        for chid in qpu.get_IDList_PhysicalChannel():
            pch = qpu.get_PhysicalChannel_byID(chid)
            if devicesType in pch.device.keys():
                deviceIDs = pch.device[devicesType] 

                for did in deviceIDs:
                    moduleID=did.split("-")[0]
                    if moduleID not in devicesList: 
                        devicesList.append(moduleID)
        instrumentDict[devicesType] = devicesList

    return instrumentDict

def get_QPUwiring( qpu:QuantumProcessUnit ) -> dict:
    """
    Translate the information in QPU to the format of the QPC
    """
    QPC_list = ["DAC","ADC","SG","DC"]
    instr_organized = dict.fromkeys(QPC_list,"")
    # Get the instrument used in this QPC 
    # The keys in dictionary are the devices type in 'QPC_list'
    instrumentDict = get_QPCinstrument(qpu, QPC_list)

    # Get CH and ROLE of the physical channel
    # Initialize
    instr_organized["CH"] = {} 
    instr_organized["ROLE"] = {}
    # Get the instrument with devices type 'devicesType' in all physical channel
    for devicesType in instrumentDict.keys():
        instrumentList = instrumentDict[devicesType]
        # Initialize the list of device type 'devicesType'
        CHList = []
        ROLEList = []
        for instrument in instrumentList:
            # Initialize the list of channel in instrument and its role
            instrChList = []
            rList = []
            # Searching in all physical channel
            for chid in qpu.get_IDList_PhysicalChannel():
                # Get the physical channel object
                pch = qpu.get_PhysicalChannel_byID(chid)

                # Check 'devicesType' is exist in pch
                if devicesType in pch.device.keys():
                    deviceIDs = pch.device[devicesType] 
                    # Extract used 
                    for i, did in enumerate(deviceIDs):
                        deviceInfo = did.split("-")
                        if deviceInfo[0] == instrument and shape(deviceInfo)[-1]>1:
                            channelID = did.split("-")[1]
                            instrChList.append(channelID)
                            rList.append(pch.coupled[i])
            if shape(instrChList)[-1]>0:
                CHList.append(instrChList)
                ROLEList.append(rList)
        instr_organized["CH"][devicesType] = CHList
        instr_organized["ROLE"][devicesType] = ROLEList
        instr_organized[devicesType] = ",".join(instrumentList)

    return instr_organized




def convert_spec_to_QubitOperation( specString:str )->dict:
    """
    The string format example:\n
    {\n
    'Q1':{\n
        'fluxBias':0.1,\n
        'qubit_frequency':4.0,\n
        'readout_frequency':6.0,\n
        'state_determination':None,\n
        'x_gate':'drag/4/-0.8/0,30,0.2',\n
        'readout_pulse':'drag/4/-0.8/0,100,0.2'},\n
    'Q2':{...}\n
    }
    """
    operation = literal_eval(specString)
    return operation

if __name__ == "__main__":

    testQPU = create_QPU_by_route("testQPU","Q1,Q2/RO1/I1+Q1:DAC=SDAWG_6-1+SDAWG_6-2,SG=DDSLO_4,ADC=SDDIG_2;Q1/XY1/X1+Y1:DAC=SDAWG_4-1+SDAWG_4-2,SG=DDSLO_3;Q1/Z1:DAC=SDAWG_4-3;")

    opdict = convert_spec_to_QubitOperation("{'Q1':{'fluxBias':0.1,'qubit_frequency':4.0,'readout_frequency':6.0,'state_determination':None,'x_gate':'drag/4/-0.8/0,30,0.2','readout_pulse':'drag/4/-0.8/0,100,0.2'}}")
    print(opdict['Q1'])
    # testQPU.set_qubitSpec(opdict)

    print(get_QPUwiring(testQPU))

    # for qid in testQPU.get_IDList_PhysicalQubit():
    #     print(f"Qubit ID: {qid}")
    #     print(f"Spec: {testQPU.QubitSet[qid].operationCondition}")
    #     for pchid in list(testQPU.QubitSet[qid].phyCh):
    #         pch = testQPU.QubitSet[qid].phyCh[pchid]
    #         print(f"channel ID: {pch.id} coupled: {pch.coupled} devices: {pch.device}")
# Numpy
# 
from calendar import c
from numpy import linspace, arange
# Numpy common math function
from numpy import exp
# Numpy constant
from numpy import pi

class QuantumProcessUnit:
    def __init__ ( self, id ):
        self.id = id
        self.QubitSet = {}
        self.ChannelSet = {}
        self.OperationCondition = []

    def get_IDList_PhysicalChannel( self ):
        return list(self.ChannelSet.keys())

    def isExist_PhysicalChannel( self, channelID ):
        if channelID in self.get_IDList_PhysicalChannel():
            return True
        else:
            #print(f"Warning: The channel {channelID} didn't register in QPU {self.id}.")
            return False

    def get_IDList_PhysicalQubit( self ):
        return list(self.QubitSet.keys())

    def isExist_PhysicalQubit( self, QubitID ):
        if QubitID in self.get_IDList_PhysicalQubit():
            return True
        else:
            #print(f"Warning: The Qubit {QubitID} didn't register in QPU {self.id}.")
            return False
    def register_PhysicalChannel( self, phyChList ):
        for phyCh in phyChList:
            if not self.isExist_PhysicalChannel(phyCh.id):
                print(f"Register physical channel {phyCh.id} in QPU {self.id} successfully.")
                self.ChannelSet.update({phyCh.id:phyCh})
            else:
                print(f"Physical channel {phyCh.id} is already in QPU {self.id}.")

    def register_PhysicalQubit( self, qubitID, channelIDList=None ):

        if not self.isExist_PhysicalQubit(qubitID):
            #print(f"Create Qubit {qubitID}.")
            newQubit = PhyQubit(qubitID)
            self.QubitSet[qubitID]=newQubit
            print(f"Register Qubit {qubitID} in QPU {self.id}.")
            if channelIDList != None:
                self.assign_channelToQubit(qubitID,channelIDList)

        else:
            print(f"Qubit {qubitID} is registered.")
        return self.QubitSet[qubitID]

    def assign_channelToQubit( self, qubitID, channelIDList ):
        qubitChannel = {}
        if self.isExist_PhysicalQubit(qubitID):
            for channelID in channelIDList:
                #print(f"Assigning {channelID}...")
                if self.isExist_PhysicalChannel(channelID):
                    qubitChannel[channelID]=self.ChannelSet[channelID]
                    print(f"Assign {channelID} to {qubitID}.")
                else:
                    print(f"Warning: The channel {channelID} didn't register in QPU {self.id}.")

            self.QubitSet[qubitID].register_PhysicalChannel(qubitChannel)
        else:
            print(f"Warning: The Qubit {qubitID} didn't register in QPU {self.id}, can't assign.")





class PhyQubit():
    def __init__ ( self, qid, PhysicalChannel={} ):

        self.id = qid
        self.PhysicalChannel = PhysicalChannel
        self.init_intrinsicProperties()
        self.operationCondition = []

    def get_IDList_PhysicalChannel( self ):
        return list(self.PhysicalChannel.keys())

    def isExist_PhysicalChannel( self, channelID ):
        if channelID in self.get_IDList_PhysicalChannel():
            return True
        else:
            #print(f"Warning: The channel {channelID} didn't register in QPU {self.id}.")
            return False

    def register_PhysicalChannel( self, phyChDict ):
        for phyCh in phyChDict.keys():
            if not self.isExist_PhysicalChannel(phyCh):
                print(f"Assign physical channel {phyCh} to Qubit {self.id} successfully.")
                self.PhysicalChannel.update({phyCh:phyChDict[phyCh]})
            else:
                print(f"Physical channel {phyCh} is already in QPU {self.id}.")

    def set_intrinsicProperties( self, properties ):
        self.intrinsicProperties.update(properties)

    def init_intrinsicProperties( self ):
        self.intrinsicProperties = {
            "qubit":{
                "flux_period": None,
                "frequency": None, # GHz
                "anharmonicity": None, #MHz w12 -w01
            },
            "dressed_resonator":{
                "RT_power":None,
                "frequency": (None,None), # GHz
                "Q_load": (None,None),
                "Q_couple": (None,None),
                "phase": (None,None),
            },
            "bare_resonator":{
                "RT_power": None,
                "frequency": (None,None), # GHz
                "Q_load": (None,None),
                "Q_couple": (None,None),
                "phase": (None,None),
            },
        }

    def set_operationCondition( self, conditionName, paras ):
        notExist = True
        for opc in self.operationCondition:
            if conditionName == opc.name:
                notExist = False
                opc.update(paras)
                break
        if notExist:
            opc = {
                "fluxBias": 0,
                "qubit_frequency":0, #GHz
                "readout_frequency": 0, #GHz
                "readout_power": -40, #dBm
                "state_determination": {},
            }
            opc.update(paras)
            self.operationCondition.append(opc)


class PhysicalChannel():
    
    #channelTypes = ["PulseRO","PulseCtrl","CWRO","CWCtrl"]
    deviceTypes = ["DAC","ADC","SG","VNA","SA","IQMixer","DRWiring"]
    roles = ["Control","Readout"]

    def __init__( self, id, role="Readout" ):
        self.id = id
        self.role = role
        self.coupled = []
        self.device = {}

    def add_device( self, deviceIDs, deviceType ):
        print(f"Add devices {deviceIDs} with type {deviceType} to physical channel {self.id}.")
        if deviceType in PhysicalChannel.deviceTypes:
            if deviceType not in self.device.keys():
                self.device[deviceType]=[]
                print(f"Device type {deviceType} didn't exist, creating now.")

            for dID in deviceIDs:
                if dID not in self.device[deviceType]:
                    self.device[deviceType].append(dID)
                    print(f"Device {dID} is added successfully.")
                else:
                    print(f"Device {dID} is already registered.")
        else: 
            print(f"Can't recognize device type {deviceType}.")


# API
def delete_char_in_string( string, delChar ):
    for c in delChar:
        string.replace(c, "")
    return string

def create_QPU_by_route( qpuid, routeString ):
    routeString=delete_char_in_string(routeString, [" ","\n"])
    newQPU = QuantumProcessUnit(qpuid)
    phyChannels = []
    for singleString in routeString.split(";"):
        if singleString == "": break
        qCh = singleString.split(":")[0].split("/")

        phyChID = qCh[1]
        phyCh = PhysicalChannel(phyChID)

        if len(qCh) == 2: phyCh.coupled = ["None"]
        else: phyCh.coupled = qCh[2].split("+")
 
        devices = singleString.split(":")[1].split(",")
        
        for d in devices:
            deviceType = d.split("=")[0]
            deviceID = d.split("=")[1].split("+")
            phyCh.add_device(deviceID,deviceType)
        phyChannels.append(phyCh)
        newQPU.register_PhysicalChannel([phyCh])
        phyQIDs = qCh[0].split(",")
        for qid in phyQIDs:
            if newQPU.isExist_PhysicalQubit(qid):
                newQPU.assign_channelToQubit( qid, [phyCh.id] )
            else:    
                newQPU.register_PhysicalQubit( qid, [phyCh.id] )
            

    return newQPU


if __name__ == "__main__":


    print(PhysicalChannel.deviceTypes)
    testQPU = create_QPU_by_route("testQPU","Q1,Q2/RO1/I+Q:DAC=SDAWG_6-1+SDAWG_6-2,SG=DDSLO_4,ADC=SDDIG_2;Q1/XY1/I+Q:DAC=SDAWG_4-1+SDAWG_4-2,SG=DDSLO_3;Q1/Z1:DAC=SDAWG_4-3;")

    # availableCh = testQPU.get_IDList_PhysicalChannel()
    # print(f"Avalable channel in QPU {testQPU.id}: {availableCh}")
    # availableQ = testQPU.get_IDList_PhysicalQubit()
    # print(f"Register Qubit in QPU {testQPU.id}: {availableQ}")
    # q1 = testQPU.QubitSet[availableQ[0]]
    # print(f"Qubit {availableQ[0]}")
    for qid in testQPU.get_IDList_PhysicalQubit():
        print(f"Qubit ID: {qid}")

        for pchid in list(testQPU.QubitSet[qid].PhysicalChannel):
            pch = testQPU.QubitSet[qid].PhysicalChannel[pchid]
            print(f"channel ID: {pch.id} Role: {pch.role} coupled: {pch.coupled} devices: {pch.device}")









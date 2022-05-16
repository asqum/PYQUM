# Numpy
# 
# from calendar import c
# from sys import modules
# from tokenize import String
from numpy import linspace, arange, shape
# Numpy common math function
from numpy import exp
# Numpy constant
from numpy import pi

from hardware_information import PhysicalChannel
"""
Hardware level:
instrument > device

Software level:
QPU > { PhysicalChannel, PhysicalQubit }

"""
PhysicalCHList = List[PhysicalChannel]

class PhysicalChannel():
    
    #channelTypes = ["PulseRO","PulseCtrl","CWRO","CWCtrl"]
    deviceTypes = ["DAC","ADC","SG","DC","VNA","SA","IQMixer","DRWiring"]
    roles = ["Control","Readout"]

    def __init__( self, id ):
        self.id = id
        #self.role = role
        self.coupled = []
        self.device = {}

    def register_device( self, deviceIDs:str, deviceType:str ):
        """
        Register the devise 'deviceIDs' with type 'deviceType' in to this physicalChannel\n
        'deviceType' arg = "DAC","ADC","SG","DC","VNA","SA","IQMixer","DRWiring"
        """
        #print(f"Add devices {deviceIDs} with type {deviceType} to physical channel {self.id}.")
        if deviceType in PhysicalChannel.deviceTypes:
            if deviceType not in self.device.keys():
                self.device[deviceType]=[]
                print(f"Device type {deviceType} didn't exist, creating now.")

            for dID in deviceIDs:
                if dID not in self.device[deviceType]:
                    self.device[deviceType].append(dID)
                    #print(f"Device {dID} is added successfully.")
                else:
                    print(f"Device {dID} is already registered.")
        else: 
            print(f"Can't recognize device type {deviceType}.")

class PhysicalSingleTransmon():
    """
    This class is used for record information of a Qubit-Cavity coupling system.
    """
    def __init__ ( self, qid:str):

        self.id = qid
        self.phyChIDList = []
        self.control = PhysicalChannel()
        self.control_IF = PhysicalChannel()
        self.operationCondition = {}

        self.init_intrinsicProperties()

    def isExist_PhysicalChannel( self, channelID:str ):
        if channelID in self.phyChIDList:
            return True
        else:
            #print(f"Warning: The channel {channelID} didn't register in QPU {self.id}.")
            return False

    def register_PhysicalChannel( self, phyChDict ):
        for phyCh in phyChDict.keys():
            if not self.isExist_PhysicalChannel(phyCh):
                #print(f"Assign physical channel {phyCh} to Qubit {self.id} successfully.")
                self.phyChIDList.append(phyCh)
            else:
                print(f"Physical channel {phyCh} is already in Qubit {self.id}.")

    def set_intrinsicProperties( self, properties ):
        self.intrinsicProperties.update(properties)

    def init_intrinsicProperties( self ):
        self.intrinsicProperties = {
            "qubit":{
                "flux_period": None,
                "max_frequency": None, # GHz
                "anharmonicity": None, #MHz w12 -w01
                "max_T1": None,
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

    def set_operationCondition( self, paras:dict ):
        opcTemp = {
            "fluxBias": None,
            "qubit_frequency": None, #GHz
            "readout_frequency": None, #GHz
            "state_determination": None,
            "readout_pulse":None,
            "x_gate":None,
        }
        opcTemp.update(paras)
        self.operationCondition = opcTemp








class QuantumProcessUnit:
    """
    This class include the all imformation of the qubit and physical channel. 
    """
    def __init__ ( self, id ):
        """
        Create QPU object with the id as same as the 'id' in argument.
        Default value is a empty QubitSet and ChannelSet
        """
        self.id = id
        self.QubitSet = {}
        self.ChannelSet = {}
        self.OperationCondition = []

    def get_IDList_PhysicalChannel( self ) -> list:
        """
        Get all registed IDs of PhysicalChannel.
        """
        return list(self.ChannelSet.keys())

    def get_PhysicalChannel_byID( self, channelID:str ) -> PhysicalChannel:
        """
        Get PhysicalChannel object in QPU by ID 'channelID'.
        """
        if self.isExist_PhysicalChannel( channelID ):
            return self.ChannelSet[channelID]
        else:
            return None

    def isExist_PhysicalChannel( self, channelID:str ) -> bool:
        """
        Search ID 'channelID' of PhysicalChannel in QPU.
        Return 'True' means exist.  
        """
        if channelID in self.get_IDList_PhysicalChannel():
            return True
        else:
            #print(f"Warning: The channel {channelID} didn't register in QPU {self.id}.")
            return False

    def get_IDList_PhysicalQubit( self ) -> list:
        """
        Get all registed IDs of PhysicalQubit.
        """
        return list(self.QubitSet.keys())

    def isExist_PhysicalQubit( self, QubitID:str ) -> bool:
        """
        Search the ID 'QubitID' of PhysicalQubit whether in this QPU.\n
        Return 'True' means exist.  
        """
        if QubitID in self.get_IDList_PhysicalQubit():
            return True
        else:
            #print(f"Warning: The Qubit {QubitID} didn't register in QPU {self.id}.")
            return False

    def get_PhysicalQubit_byID( self, QubitID:str ) -> PhysicalQubit:
        """
        Get PhysicalQubit object in QPU by ID 'QubitID'.
        """
        if self.isExist_PhysicalQubit( QubitID ):
            return self.QubitSet[QubitID]
        else:
            return None

    def register_PhysicalChannel( self, phyCh:PhysicalChannel ):
        """
        Create PhysicalChannel object and store in QuantumProcessUnit.ChannelSet .
        """
        # If the phyCh haven't register yet, put it to the ChannelSet
        if not self.isExist_PhysicalChannel(phyCh.id):
            #print(f"Register physical channel {phyCh.id} in QPU {self.id} successfully.")
            self.ChannelSet.update({phyCh.id:phyCh})
        else:
            print(f"Physical channel {phyCh.id} is already in QPU {self.id}.")
        


    def register_PhysicalQubit( self, qubitID:str, channelIDList=None ):
        """
        Create PhysicalQubit object and store in QuantumProcessUnit.QubitSet .
        """
        if not self.isExist_PhysicalQubit(qubitID):
            #print(f"Create Qubit {qubitID}.")
            newQubit = PhysicalQubit(qubitID)
            self.QubitSet[qubitID] = newQubit
            #print(f"Register Qubit {qubitID} in QPU {self.id}.")
            if channelIDList != None:
                self.assign_channelToQubit(qubitID,channelIDList)

        else:
            print(f"Qubit {qubitID} is registered.")

    def assign_channelToQubit( self, qubitID:str, channelIDList:list ):
        """
        Make PhysicalQubit object record used IDs of channel 'channelIDList' that.
        """
        qubitChannel = {}
        if self.isExist_PhysicalQubit(qubitID):
            for channelID in channelIDList:
                #print(f"Assigning {channelID}...")
                if self.isExist_PhysicalChannel(channelID):
                    qubitChannel[channelID]=self.ChannelSet[channelID]
                else:
                    print(f"Warning: The channel {channelID} didn't register in QPU {self.id}.")

            self.QubitSet[qubitID].register_PhysicalChannel(qubitChannel)
        else:
            print(f"Warning: The Qubit {qubitID} didn't register in QPU {self.id}, can't assign.")

    def set_qubitSpec( self, spec:dict ):
        """
        Set qubit specification from dictionary structure\n
        structure example:\n
        { qid1:{spec1},qid2:{spec2},... }
        """
        for qubitID in spec.keys():
            if self.isExist_PhysicalQubit(qubitID):
                    self.QubitSet[qubitID].set_operationCondition(spec[qubitID])
            else:
                print(f"Warning: The Qubit {qubitID} didn't register in QPU {self.id}, can't assign.")




if __name__ == "__main__":

    
    testQPU = QuantumProcessUnit("testQPU")

    # availableCh = testQPU.get_IDList_PhysicalChannel()
    # print(f"Avalable channel in QPU {testQPU.id}: {availableCh}")
    # availableQ = testQPU.get_IDList_PhysicalQubit()
    # print(f"Register Qubit in QPU {testQPU.id}: {availableQ}")
    # q1 = testQPU.QubitSet[availableQ[0]]
    # print(f"Qubit {availableQ[0]}")






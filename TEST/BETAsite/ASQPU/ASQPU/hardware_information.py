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
"""
Hardware levels:

instrument > device

"""


class PhysicalChannel():
    
    #channelTypes = ["PulseRO","PulseCtrl","CWRO","CWCtrl"]
    deviceTypes = ["DAC","ADC","SG","DC","VNA","SA","IQMixer","DRWiring"]
    roles = ["Control","Readout"]

    def __init__( self, id ):
        self.id = id
        #self.role = role
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

class PhyQubit():
    def __init__ ( self, qid:str):

        self.id = qid
        self.phyCh = {}
        self.init_intrinsicProperties()
        self.operationCondition = {}

    def get_IDList_PhysicalChannel( self ):
        return list(self.phyCh.keys())

    def isExist_PhysicalChannel( self, channelID:str ):
        if channelID in self.get_IDList_PhysicalChannel():
            return True
        else:
            #print(f"Warning: The channel {channelID} didn't register in QPU {self.id}.")
            return False

    def register_PhysicalChannel( self, phyChDict ):
        for phyCh in phyChDict.keys():
            if not self.isExist_PhysicalChannel(phyCh):
                print(f"Assign physical channel {phyCh} to Qubit {self.id} successfully.")
                self.phyCh.update({phyCh:phyChDict[phyCh]})
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
        notExist = True

        opcTemp = {
            "fluxBias": None,
            "qubit_frequency": None, #GHz
            "readout_frequency": None, #GHz
            "state_determination": None,
            "pulse_string": {
                "readout":None,
                "x":None,
                "y":None,
                "+x/2":None,
                "+y/2":None,
                "-x/2":None,
                "-y/2":None,
                "I":None,
            }
        }
        opcTemp.update(paras)
        self.operationCondition=opcTemp




class QuantumProcessUnit:
    def __init__ ( self, id ):
        self.id = id
        self.QubitSet = {}
        self.ChannelSet = {}
        self.OperationCondition = []

    def get_IDList_PhysicalChannel( self ) -> list:
        return list(self.ChannelSet.keys())

    def get_PhysicalChannel_byID( self, channelID ) -> PhysicalChannel:
        if self.isExist_PhysicalChannel( channelID ):
            return self.ChannelSet[channelID]
        else:
            return None

    def isExist_PhysicalChannel( self, channelID ) -> bool:
        if channelID in self.get_IDList_PhysicalChannel():
            return True
        else:
            #print(f"Warning: The channel {channelID} didn't register in QPU {self.id}.")
            return False

    def get_IDList_PhysicalQubit( self ) -> list:
        return list(self.QubitSet.keys())

    def isExist_PhysicalQubit( self, QubitID ) -> bool:
        if QubitID in self.get_IDList_PhysicalQubit():
            return True
        else:
            #print(f"Warning: The Qubit {QubitID} didn't register in QPU {self.id}.")
            return False
    def get_PhysicalQubit_byID( self, QubitID ) -> PhyQubit:
        if self.isExist_PhysicalQubit( QubitID ):
            return self.QubitSet[QubitID]
        else:
            return None

    def register_PhysicalChannel( self, phyChList ):
        for phyCh in phyChList:
            if not self.isExist_PhysicalChannel(phyCh.id):
                print(f"Register physical channel {phyCh.id} in QPU {self.id} successfully.")
                self.ChannelSet.update({phyCh.id:phyCh})
            else:
                print(f"Physical channel {phyCh.id} is already in QPU {self.id}.")
        


    def register_PhysicalQubit( self, qubitID:str, channelIDList=None ):

        if not self.isExist_PhysicalQubit(qubitID):
            #print(f"Create Qubit {qubitID}.")
            newQubit = PhyQubit(qubitID)
            self.QubitSet[qubitID] = newQubit

            print(f"Register Qubit {qubitID} in QPU {self.id}.")
            if channelIDList != None:
                self.assign_channelToQubit(qubitID,channelIDList)

        else:
            print(f"Qubit {qubitID} is registered.")

    def assign_channelToQubit( self, qubitID:str, channelIDList:list ):
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
        Set qubit specification from dictionary structure
        """

        qubitChannel = {}
        for qubitID in spec.keys():
            if self.isExist_PhysicalQubit(qubitID):
                    self.QubitSet[qubitID].set_operationCondition(spec[qubitID])
            else:
                print(f"Warning: The Qubit {qubitID} didn't register in QPU {self.id}, can't assign.")



# API
def delete_char_in_string( string:str, delChar:list ):
    for c in delChar:
        string.replace(c, "")
    return string

def create_QPU_by_route( qpuid:str, routeString:str ):
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


def convert_spec_to_QubitOperation( specString:str ):
    """
    Convert string to dictionary that can send to PhysicalQubit class
    """
    # oi = operation information
    def set_fluxbias ( bias:str ):
        biasValue = float(bias)
        infoDict ={"fluxBias":biasValue}
        return "fluxBias", infoDict
    def set_qubitFrequency ( freq:str ):
        freqValue = float(freq)
        infoDict = {"qubit_frequency":freqValue}
        return "qubit_frequency", infoDict
    def set_readoutFrequency ( freq:str ):
        freqValue = float(freq)
        infoDict = {"readout_frequency":freqValue}
        return "readout_frequency", infoDict
    def set_stateDetermination ( clusterCenter:str ):
        IQComplex = [complex(k) for k in centerString.split(",")]
        state = {
            "g":IQComplex[0],
            "e":IQComplex[1],
        }
        infoDict = {"state_determination":state}
        return "state_determination", infoDict
    def set_roPulseString ( waveformString:str ):
        infoDict = {
            "pulse_string":{"readout":waveformString}
            }
        return "pulse_string", infoDict
    def set_ctrlPulseString ( waveformString:str  ):
        waveformType = waveformString.split('/')[0]
        basicParas = []
        for p in waveformString.split(',')[1:]:
            if p == '' :
                basicParas.append( nan )
            else:
                basicParas.append( float(p) )  
        pulsewidth = float(basicParas[0])
        pulseheight = float(basicParas[1])
        waveformParas = []
        for p in waveformString.split(',')[0].split('/')[1:]:
            if p == '':
                waveformParas.append( nan )
            else:
                waveformParas.append( float(p) )
        infoDict = {
            "pulse_string":{
                "I":f"FLAT/,{pulsewidth},{pulseheight}",
                "x":f"{waveformType}/{p}/{p}/0,{pulsewidth},{pulseheight}",
                "y":f"{waveformType}/{p}/{p}/90,{pulsewidth},{pulseheight}",
                "+x/2":f"{waveformType}/{p}/{p}/0,{pulsewidth},{pulseheight/2}",
                "+y/2":f"{waveformType}/{p}/{p}/90,{pulsewidth},{pulseheight/2}",
                "-x/2":f"{waveformType}/{p}/{p}/-180,{pulsewidth},{pulseheight/2}",
                "-y/2":f"{waveformType}/{p}/{p}/-90,{pulsewidth},{pulseheight/2}",
            }
        }
        return "pulse_string", infoDict
    specString=delete_char_in_string(specString, [" ","\n"])
    oiDict = {}
    oiType = {
        'bias': set_fluxbias,
        'fq': set_qubitFrequency,
        'fro': set_readoutFrequency,
        'ctrl': set_ctrlPulseString,
        'ro':set_roPulseString,
        'state': set_stateDetermination,
    }
    for singleString in specString.split(";"):
        qubitName = specString.split(":")[0]
        oiDict[qubitName] = {}
        operationInfoList = specString.split(":")[1].split("&")
        for oi in operationInfoList:
            keywordStr = oi.split("=")[0]
            ioKey, partialOI = oiType[keywordStr](oi.split("=")[1])
            print(ioKey, partialOI, oiDict[qubitName].keys())

            if ioKey not in oiDict[qubitName].keys():
                oiDict[qubitName].update(partialOI)
            else:
                oiDict[qubitName][ioKey].update(partialOI[ioKey])
    return oiDict


def get_QPUinstrument( qpu:QuantumProcessUnit ):
    QPC_list = ["DAC","ADC","SG","DC"]

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

def get_QPUwiring( qpu:QuantumProcessUnit ):
    """
    Translate the information in QPU to the format of the QPC
    """
    QPC_list = ["DAC","ADC","SG","DC"]
    instr_organized = dict.fromkeys(QPC_list,"")

    instrumentDict = get_QPUinstrument(qpu)
    instr_organized["CH"] = ""
    instr_organized["ROLE"] = ""

    for devicesType in instrumentDict.keys():
        instrumentList = instrumentDict[devicesType]
        CHstringList = []
        ROLEstringList = []
        for instrument in instrumentList:
            channelList = []
            ROLElist = []
            for chid in qpu.get_IDList_PhysicalChannel():
                pch = qpu.get_PhysicalChannel_byID(chid)

                if devicesType in pch.device.keys():
                    deviceIDs = pch.device[devicesType] 
                    for i, did in enumerate(deviceIDs):
                        deviceInfo = did.split("-")
                        if deviceInfo[0] == instrument and shape(deviceInfo)[-1]>1:
                            channelID = did.split("-")[1]
                            channelList.append(channelID)
                            ROLElist.append(pch.coupled[i])
            if shape(channelList)[-1]>0:
                CHstringList.append("/".join(channelList))
                ROLEstringList.append("/".join(ROLElist))
            
        if shape(CHstringList)[-1]>0:
            CHstring = f"{devicesType}:{','.join(CHstringList)}"
            ROLEstring = f"{devicesType}:{','.join(ROLEstringList)}"
        instr_organized[devicesType] = ",".join(instrumentList)
    instr_organized["CH"] = CHstring
    instr_organized["ROLE"] = ROLEstring

    return instr_organized



if __name__ == "__main__":


    testQPU = create_QPU_by_route("testQPU","Q1,Q2/RO1/I1+Q1:DAC=SDAWG_6-1+SDAWG_6-2,SG=DDSLO_4,ADC=SDDIG_2;Q1/XY1/X1+Y1:DAC=SDAWG_4-1+SDAWG_4-2,SG=DDSLO_3;Q1/Z1:DAC=SDAWG_4-3;")

    # availableCh = testQPU.get_IDList_PhysicalChannel()
    # print(f"Avalable channel in QPU {testQPU.id}: {availableCh}")
    # availableQ = testQPU.get_IDList_PhysicalQubit()
    # print(f"Register Qubit in QPU {testQPU.id}: {availableQ}")
    # q1 = testQPU.QubitSet[availableQ[0]]
    # print(f"Qubit {availableQ[0]}")

    

    opdict = convert_spec_to_QubitOperation("Q1:bias=0.1&fq=4.0&fro=6.0&ctrl=drag/4/-0.8/0,30,0.2&ro=drag/4/-0.8/0,100,0.2")
    #print(opdict)
    testQPU.set_qubitSpec(opdict)

    print(get_QPUwiring(testQPU))

    for qid in testQPU.get_IDList_PhysicalQubit():
        print(f"Qubit ID: {qid}")
        print(f"Spec: {testQPU.QubitSet[qid].operationCondition}")
        for pchid in list(testQPU.QubitSet[qid].phyCh):
            pch = testQPU.QubitSet[qid].phyCh[pchid]
            print(f"channel ID: {pch.id} coupled: {pch.coupled} devices: {pch.device}")






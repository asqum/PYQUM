# Numpy
# 
from numpy import linspace, arange
# Numpy common math function
from numpy import exp
# Numpy constant
from numpy import pi




class PhyQubit():
    def __init__ ( self, PhysicalChannel ):
        self.name = "Q1"
        self.PhysicalChannel = PhysicalChannel
        self.init_intrinsicProperties()
        self.operationCondition = []

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
                "readout_power": -40, # dBm
            }
            opc.update(paras)
            self.operationCondition.append(opc)


class PhysicalChannel():
    def __init__( self, AWGChannel, iQMixerChannel):
        self.name = "XY"

        self.IQMixerChannel = iQMixerChannel
        self.AWGChannel = AWGChannel


class DRChannel():
        def __init__ ( self ):
            self.instrmentID = ["I1"]
            self.gain = []

        def add_attenuator( self, temperature, attenuation ):
            info={
                "T":temperature,
                "A":-attenuation,
            }
            self.gain.append(info)

        def add_amplifier( self, temperature, gain ):
            info={
                "T":temperature,
                "A":gain,
            }
            self.gain.append(info)

class IQMixerChannel():
    def __init__ ( self ):
        self.instrmentID = "U3022AH37 5-9 GHz/CH1"
        self.ifFreq = 91. # MHz
        self.ampBalance = 1. # I/Q amp ratio compensation for SSB
        self.offset = (0.,0.)
        self.phaseBalance = -90 # I/Q Quadrature phase difference compensation for SSB

class AWGChannel():
    def __init__ ( self ):
        self.instrmentID = ["1-1","1-2"]
        self.timeResolution = 1. # ns/sample
# Numpy
# 
from numpy import linspace, arange
# Numpy common math function
from numpy import exp
# Numpy constant
from numpy import pi

class HardwareInfo():
    def __init__( self, Qubit, InputPort, IQMixerChannel ):

        self.timeResolution = 1. # ns/sample
        self.Qubit = Qubit
        self.InputPort = InputPort
        self.IQMixerChannel = IQMixerChannel

    def print_json( self ):
        data = {
            "qubit": self.qubit

        }
        return data

class InputPort():
    
    def __init__ (self):
        self.couplingStrength = 10

class Qubit():
    
    def __init__ (self):
        self.fluxBias = 0
        self.qubitFreq = 5 # GHz
        self.couplingStrength = 10
        self.anharmonicity = -100 #MHz w12 -w01

class IQMixerChannel():

    def __init__ (self):
        self.ID = "CH1"
        self.ifFreq = 100 # MHz
        self.ampBalance = 1 # I/Q amp ratio compensation for SSB
        self.offset = (0,0)
        self.phaseBalance = 90 # I/Q Quadrature phase difference compensation for SSB
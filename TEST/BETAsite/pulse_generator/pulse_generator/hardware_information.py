# Numpy
# 
from numpy import linspace, arange
# Numpy common math function
from numpy import exp
# Numpy constant
from numpy import pi


class HardwareInfo():
    def __init__( self, qubit, inputPort, iQMixerChannel ):

        self.timeResolution = .1 # ns/sample
        self.Qubit = qubit
        self.InputPort = inputPort
        self.IQMixerChannel = iQMixerChannel

    def print_json( self ):
        data = {
            "qubit": self.qubit

        }
        return data

class InputPort():
    
    def __init__ (self):
        self.couplingStrength = 1.

class Qubit():
    
    def __init__ (self):
        self.fluxBias = 0
        self.qubitFreq = 4.0 # GHz
        self.anharmonicity = -200 #MHz w12 -w01

class IQMixerChannel():

    def __init__ (self):
        self.ID = {
            "I":"CH1",
            "Q":"CH2",
            }
        self.ifFreq = 91. # MHz
        self.ampBalance = 1. # I/Q amp ratio compensation for SSB
        self.offset = (0.,0.)
        self.phaseBalance = -90 # I/Q Quadrature phase difference compensation for SSB
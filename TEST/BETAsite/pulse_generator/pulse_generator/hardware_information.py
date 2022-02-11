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
        self.fluxBias = 0
        self.qubitFreq = 4.0 # GHz
        self.anharmonicity = -200 #MHz w12 -w01

class PhysicalChannel():
    def __init__( self ,AWGChannel ,iQMixerChannel):
        self.name = "XY_I"
        self.timeResolution = .1 # ns/sample
        self.IQMixerChannel = iQMixerChannel
        self.AWGChannel = AWGChannel


class IQMixerChannel():

    def __init__ ( self ):
        self.instrmentID = "U3022AH37 5-9 GHz/CH1"
        self.ifFreq = 91. # MHz
        self.ampBalance = 1. # I/Q amp ratio compensation for SSB
        self.offset = (0.,0.)
        self.phaseBalance = -90 # I/Q Quadrature phase difference compensation for SSB

class AWGChannel():
    def __init__ ( self ):
        self.instrmentID = ["1-1"]
        self.timeResolution = 1. # ns/sample
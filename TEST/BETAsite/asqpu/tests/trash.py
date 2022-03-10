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

# class IQMixerChannel():
#     def __init__ ( self ):
#         self.instrmentID = "U3022AH37 5-9 GHz/CH1"
#         self.ifFreq = 91. # MHz
#         self.ampBalance = 1. # I/Q amp ratio compensation for SSB
#         self.offset = (0.,0.)
#         self.phaseBalance = -90 # I/Q Quadrature phase difference compensation for SSB

class AWGChannel():
    def __init__ ( self ):
        self.instrmentID = ["1-1","1-2"]
        self.channelID = "1"
        self.timeResolution = 1. # ns/sample

class LOChannel():
    def __init__ ( self ):
        self.instrmentID = ["1-1","1-2"]
        self.timeResolution = 1. # ns/sample

class ADCChannel():
    def __init__ ( self ):
        self.instrmentID = ["1-1","1-2"]
        self.timeResolution = 1. # ns/sample
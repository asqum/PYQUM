'''Basic QuBit Characterizations'''

__author__ = "Teik-Hui Lee"
__copyright__ = "Copyright 2019, The Pyqum Project"
__credits__ = ["Chii-Dong Chen", "Yu-Cheng Chang"]
__license__ = "GPL"
__version__ = "beta3"
__email__ = "teikhui@phys.sinica.edu.tw"
__status__ = "development"



class basics:
    '''TEST
    '''

    def __init__(self, params, instrs, spans):
        self.params = params
        self.instrs = instrs
        self.spans = spans
    
    def unitvector(self, cycle):
        from numpy import sin, cos, pi
        y = sin(cycle*2*pi)
        x = cos(cycle*2*pi)
        return x, y


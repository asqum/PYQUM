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



class TransmonModel():
    """
    Properties of ideal Transmon
    Dictionary like structure
    """
    def __init__( self ):
        print(f"init IsolatedTransmon")
        self._transitionFrequency = None
        self._anharmonicity = None
    
    @property
    def transitionFrequency( self )->float:
        """
        Get the transition frequency of the transmon 0->1 transition frequency in unit of GHz
        """
        return self._transitionFrequency

    @transitionFrequency.setter
    def transitionFrequency( self, transitionFrequency:float ):
        self._transitionFrequency = transitionFrequency

    @property
    def anharmonicity( self )->float:
        """
        The anharmonicity in unit of MHz
        Anharmonicity difinition is transition frequency f_12 - f_01 
        """
        return self._anharmonicity

    @anharmonicity.setter
    def anharmonicity( self, anharmonicity:float ):
        self._anharmonicity = anharmonicity

    @property
    def Ec( self ) -> float:
        """
        Ec in unit of MHz
        Calculated from anharmonicity
        """
        return -self._anharmonicity

class SQUIDTransmonModel(TransmonModel):
    """
    Properties of ideal tunable Transmon 
    Dictionary like structure
    """
    def __init__( self ):
        super().__init__()
        self.flux = None

    @property
    def flux ( self )->float:
        """Magnetic flux in SQUID, unit in magnetic flux quantum, Dimensionless"""
        return self._flux
    @flux.setter
    def flux ( self, value:float):
        self._flux = value

class Resonator():
    """
    Properties of resonator
    Dictionary like structure

    """
    def __init__( self ):
        print(f"init IsolatedResonator")
        self._f_r = None
        self._Q_internal = None
        self._Q_coupling = None
        self._Q_load = None

    @property
    def f_r ( self )->float:
        """ The resonant frequency of the resonator, unit in GHz """
        return self._f_r
    @f_r.setter
    def f_r ( self, value:float ):
        self._f_r = value

    @property
    def Q_internal ( self )->float:
        """ The resonant frequency of the resonator, unit in GHz """
        return self._Q_internal

    @Q_internal.setter
    def Q_internal ( self, value:float ):
        self.Q_internal = value

    @property
    def Q_coupling ( self )->float:
        """Coupling quality factor between cavity and transmission line. Dimensionless"""
        return self._Q_coupling
    @Q_coupling.setter
    def Q_coupling ( self, value:float ):
        self._Q_coupling = value

    @property
    def Q_load ( self )->float:
        """Loaded quality factor of cavity. Dimensionless"""
        return self._Q_load
    @Q_load.setter
    def Q_coupling ( self, value:float ):
        self._Q_load = value
class TransmissionLine():
    """
    Properties of Transmission Line
    """
    def __init__( self ):
        self.s21 = None

if __name__ == '__main__':
    a = SQUIDTransmonModel()
    print(a.anharmonicity)
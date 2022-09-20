# Numpy Series
# Numpy array
#from numpy import linspace, arange, shape
# Numpy common math function
#from numpy import exp
# Numpy constant
#from numpy import pi


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



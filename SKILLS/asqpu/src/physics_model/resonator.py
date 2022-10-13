
# Numpy Series
# Numpy array
#from numpy import linspace, arange, shape
# Numpy common math function
#from numpy import exp
# Numpy constant
#from numpy import pi



class Resonator():
    """
    Properties of resonator
    Dictionary like structure

    """
    def __init__( self ):
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
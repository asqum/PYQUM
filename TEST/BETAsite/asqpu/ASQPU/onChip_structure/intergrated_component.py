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

# Dependency in the same package
from single_component import IsolatedTransmon, IsolatedResonator



class SingleTransmon():
    """
    This class is used for record information of a Qubit-Cavity coupling system.
    Dictionary like structure
    property
    g_qc : Unit in MHz
    flux : Unit in magnetic flux quantum
    zSensitivity : Unit in magnetic flux quantum per mA 
    """
    def __init__( self ):

        self.qubit = IsolatedTransmon()
        self.dressed_cavity = IsolatedResonator()
        self._g_qc = None
        self._Q_coupling = None
        self._Q_load = None
        self._flux = 0 # Unit in magnetic flux quantum
        self._sensitivity_z = None
        self._sensitivity_RF = None


    @property
    def g_qc ( self )->float :
        """Coupling strength between cavity and qubit, unit in MHz."""
        return self._g_qc
    @g_qc.setter
    def g_qc ( self, value : float ):
        self._g_qc = value

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

    @property
    def flux ( self )->float:
        """Magnetic flux in SQUID, unit in magnetic flux quantum, Dimensionless"""
        return self._flux
    @flux.setter
    def flux ( self, value:float):
        self._flux = value

    @property
    def sensitivity_z ( self )->float:
        """Unit in magnetic flux quantum per mA"""
        return self._sensitivity_z
    @sensitivity_z.setter
    def sensitivity_z ( self, value:float ):
        self._sensitivity_z = value

    @property
    def sensitivity_RF ( self )->float:
        """Intergation of V(t) per pi pulse, unit in V/ns"""
        return self.sensitivity_RF
    @sensitivity_RF.setter
    def sensitivity_RF ( self, value:float ):
        self.sensitivity_RF = value

if __name__ == '__main__':
    a = SingleTransmon()
    a.qubit.anharmonicity = -10.
    a.g_qc = 70
    a.Q_coupling = 1e6

    print(a.g_qc)
    print(a.qubit.anharmonicity)
    print(a.qubit.Ec)

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
from independent_system import SQUIDTransmonModel, Resonator



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

        self.qubit = SQUIDTransmonModel()
        self.dressed_cavity = Resonator()
        self.bare_cavity = Resonator()
        self._g_qc = None



    @property
    def g_qc ( self )->float :
        """Coupling strength between cavity and qubit, unit in MHz."""
        return self._g_qc
    @g_qc.setter
    def g_qc ( self, value : float ):
        self._g_qc = value




if __name__ == '__main__':
    a = SingleTransmon()
    a.qubit.anharmonicity = -10.
    a.g_qc = 70

    print(a.g_qc)
    print(a.qubit.anharmonicity)
    print(a.qubit.Ec)

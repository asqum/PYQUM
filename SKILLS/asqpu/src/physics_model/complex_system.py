# Numpy


# Dependency in the same package
from physics_model.qubit_model import SQUIDTransmonModel
from physics_model.resonator import Resonator


class SingleReadableTransmon():
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
    a = SingleReadableTransmon()
    a.qubit.anharmonicity = -10.
    a.g_qc = 70

    print(a.g_qc)
    print(a.qubit.anharmonicity)
    print(a.qubit.Ec)

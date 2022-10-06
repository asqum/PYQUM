from physics_model.complex_system import SingleReadableTransmon
from qpu.backend.phychannel.physical_channel import PhysicalChannel
from typing import List
from qpu.backend.component.q_component import QComponent


  

class Transmon( QComponent ):
    """
    This class is used for record information of a Qubit-Cavity coupling system and operation method.
    """
    def __init__ ( self, qid:str ):
        super().__init__( qid )
        #self._ports = []
        self.readout_power = None
        self.readout_freq = None
        self._sensitivity_flux = None
        self._sensitivity_RF = None
        self._transition_freq = None
        self.Ec = None
        
    def __eq__( self, other )->str:
        if isinstance(other, Transmon):
            return self.name == other.name
        if isinstance(other, str):
            return self.name == other
        return False

    @property
    def sensitivity_flux ( self )->float:
        """Unit in magnetic flux quantum per mA"""
        return self._sensitivity_flux
    @sensitivity_flux.setter
    def sensitivity_flux ( self, value:float ):
        self._sensitivity_flux = value

    @property
    def sensitivity_RF ( self )->float:
        """Intergation of V(t) per pi pulse, unit in V/ns"""
        return self._sensitivity_RF
    @sensitivity_RF.setter
    def sensitivity_RF ( self, value:float ):
        self._sensitivity_RF = value

    @property
    def transition_freq ( self )->float:
        """Intergation of V(t) per pi pulse, unit in V/ns"""
        return self._transition_freq
    @transition_freq.setter
    def transition_freq ( self, value:float ):
        self._transition_freq = value


    # @property
    # def properties( self )->SingleReadableTransmon:
    #     """A object store the specification of qubit"""
    #     return self._properties
    # @properties.setter
    # def properties( self, value:SingleReadableTransmon):
    #     self._properties = value









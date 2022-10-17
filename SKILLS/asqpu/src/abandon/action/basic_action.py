from abc import ABC, abstractmethod
from typing import Union, List
from qpu.backend.component.qubit.transmon import Transmon
from numpy import pi
from pulse_signal.common_Mathfunc import DRAGFunc, constFunc, rectPulseFunc, GERPFunc
from pulse_signal.pulse import Pulse

class PhysicalAction():
    """
    Any physical interaction with the qubit
    """
    def __init__( self, id:str ):
        self._id = id
        #self._port = port
        self._t0 = 0

        self._duration = 10
        self._duration_unit = "dt"

    @property
    def id( self )->str:
        return self._id
    @id.setter    
    def id( self, value:str ):
        self._id = value

    @property
    def t0( self )->Union[float,int]:
        return self._t0
    @t0.setter    
    def t0( self, value:Union[float,int] ):
        self._t0 = value

    @property
    def duration( self )->Union[float,int]:
        return self._duration
    @duration.setter    
    def duration( self, value:Union[float,int] ):
        self._duration = value

    def to_pulse( self )->Pulse:
        pass

    def __eq__( self, other )->str:
        if isinstance(other, PhysicalAction):
            return self.id == other.id
        if isinstance(other, str):
            return self.id == other
        return False

class Operation( ABC, PhysicalAction ):
    """
    The action which can control qubit
    """
    @abstractmethod
    def __init__( self, id:str ):
        self._id = id
        #self._port = port

    @property
    @abstractmethod
    def pars( self ):
        return self._pars

    @pars.setter
    @abstractmethod
    def pars( self, value ):
        self._pars = value


class RXYOperation( Operation ):
    """
    Rotation along cos(phi)x+sin(phi)y axis.
    """
    def __init__( self, id:str ):
        """
        
        args:
            id: the ID of the operation.
            qubit: store the information to build pulse
            pars: a list of parameters to build pulse
                pars[0] = theta
                pars[1] = phi

        """
        super().__init__( id )
        self._t0 = 0

    @property
    def pars( self )->List[float]:
        """
        pars[0] = theta\n
        pars[1] = phi\n     
        """

        return self._pars

    @pars.setter
    def pars( self, value:List[float] ):
        self._pars = value

    
    def to_pulse( self, qubit:Transmon )->Pulse:
        theta = self.pars[0]
        phi = self.pars[1]

        s = qubit.sensitivity_RF
        duration = self.duration
        center = self.t0+duration/2
        amp = (theta/pi)/s/duration
        derivative_ratio = 1/qubit.Ec

        pulse = Pulse()
        pulse.carrierFrequency = qubit.transition_freq
        pulse.carrierPhase = phi
        pulse.duration = self.duration
        pulse.parameters = (amp, duration/4, center, derivative_ratio)
        pulse.envelopeFunc = DRAGFunc
        return pulse

class RZOperation( Operation ):
    """
    Rotation along z axis.
    """
    def __init__( self, id:str ):
        """
        
        args:
            id: the ID of the operation.
            qubit: store the information to build pulse
            pars: a list of parameters to build pulse
                pars[0] = phi

        """
        super().__init__( id )

    @property
    def pars( self )->List[float]:
        """
        pars[0] = phi\n     
        """

        return self._pars

    @pars.setter
    def pars( self, value:List[float] ):
        self._pars = value

    
    def to_pulse( self, qubit:Transmon )->Pulse:
        amp = 1/qubit.sensitivity_flux
        phi = self.pars[0]
        duration = self.duration
        width = phi/pi*duration

        pulse = Pulse()
        pulse.carrierFrequency = 0
        pulse.carrierPhase = 0
        pulse.duration = self.duration
        pulse.parameters = (amp, width, self.t0)
        pulse.envelopeFunc = rectPulseFunc
        return pulse

class Measurement( PhysicalAction ):

    def __init__( self, id:str ):
        """
        
        args:
            id: the ID of the operation.
            qubit: store the information to build pulse
            pars: a list of parameters to build pulse
                pars[0] = length
                pars[1] = s factor
                pars[2] = edge length

        """
        super().__init__( id )

    @property
    def pars( self )->List[float]:
        """
        pars[0] = theta\n
        pars[1] = phi\n     
        """

        return self._pars

    @pars.setter
    def pars( self, value:List[float] ):
        self._pars = value

    
    def to_pulse( self, qubit:Transmon )->Pulse:

        duration = self.duration
        amp = qubit.readout_power
        pulse = Pulse()
        pulse.carrierFrequency = qubit.readout_freq
        pulse.carrierPhase = 0
        pulse.duration = self.duration
        pulse.parameters = (amp, duration, self.t0, 30, 30/2 )
        pulse.envelopeFunc = GERPFunc
        return pulse

class Idle( Operation ):
    """
    The output when the circuit is idle.
    """
    def __init__( self, id:str, pars:List[float] ):
        """
        The output when the circuit is idle.
            id: the ID of the operation.
            qubit: store the information to build pulse
            pars: a list of parameters to build pulse
                pars[0] = constant voltage
        """
        super().__init__( id )
        
        self._pars = pars

    @property
    def pars( self )->List[float]:
        """
        pars[0] = constant voltage   
        """

        return self._pars

    @pars.setter
    def pars( self, value:List[float] ):
        self._pars = value

    
    def to_pulse( self ):
        pulse = Pulse()
        pulse.carrierFrequency = 0
        pulse.carrierPhase = 0
        pulse.duration = self.duration
        pulse.parameters = [self.pars[0]]
        pulse.envelopeFunc = constFunc
        return pulse


#if __name__ == '__main__':

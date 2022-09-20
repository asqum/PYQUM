# import sys
# sys.path.insert(0, r'../')
# Numpy Series
# Typing
from numpy import ndarray, complex128, issubdtype
# Array
from numpy import array, linspace, empty, append
# Math
from numpy import cos, sin, exp, arctan2, radians, sign
# const
from numpy import pi

from typing import Tuple
from .common_Mathfunc import gaussianFunc, DRAGFunc
from .waveform import Waveform
from .digital_mixer import upConversion_IQ

class QAM():
    """
    Quadrature amplitude modulation (QAM)

    """
    def __init__ ( self ):
        self.carrierFrequency = None
        self.envelope = array([[None],[None]])



    @property
    def inphase ( self )->ndarray:
        """ In-phase component I(t)."""
        return self.envelope[0]
    @inphase.setter
    def inphase ( self, value:ndarray ):
        self.envelope[0] = value

    @property
    def quadrature ( self )->ndarray:
        """ Quadrature component Q(t)."""
        return self.envelope[1]
    @quadrature.setter
    def duration ( self, value:ndarray ):
        self.envelope[1] = value


    def SSB( self, freqIF:float, IQMixer:tuple=(1,90,0,0) )->Tuple[ndarray,ndarray,float]:
        """
        For the pulse is generate by IQMixer
        For a given dt and t0, calculate the I/Q for IQmixer. \n

        IFFreq: The Intermediate frequency of I/Q ( Unit in dt ) \n
        IQMixer: The parametrs for calibrate IQmixer\n
            p1: I/Q Amplitude Balance ( dimensionless ratio )\n
            p2: Phase Balance ( unit in angle )\n
            p3: I offset\n
            p4: Q offset\n
        The LO frequency should be RF-IF (RF is carrier frequency)
        """
        signal_I, signal_Q = upConversion_IQ( self.envelope, freqIF, IQMixer)
        freq_LO = self.carrierFrequency - freqIF
        return signal_I, signal_Q, freq_LO


class Pulse():
    """ Store the necessary information for waveform """
    def __init__ ( self ):

        self._duration = None
        self._carrierFrequency = None
        self._carrierPhase = None
        self._envelopeFunc = None
        self._parameters = None

    @property
    def carrierFrequency ( self )->float:
        """ The carrier frequency of the signal, unit depended on dt."""
        return self._carrierFrequency
    @carrierFrequency.setter
    def carrierFrequency ( self, value:float ):
        self._carrierFrequency = value

    @property
    def carrierPhase ( self )->float:
        """ The carrier phase of the signal, unit depended on dt."""
        return self._carrierPhase
    @carrierPhase.setter
    def carrierPhase ( self, value:float ):
        self._carrierPhase = value

    @property
    def duration ( self )->float:
        """ The duration time of the pulse, unit depended on dt."""
        return self._duration
    @duration.setter
    def duration ( self, value:float ):
        self._duration = value

    @property
    def envelopeFunc ( self ):
        """ The function to form the envelope."""
        return self._envelopeFunc
    @envelopeFunc.setter
    def envelopeFunc ( self, value ):
        self._envelopeFunc = value

    @property
    def parameters ( self )->tuple:
        """ The parameters for the function to form the envelope."""
        return self._parameters
    @parameters.setter
    def parameters ( self, value:tuple ):
        self._parameters = value

    def generate_envelope( self, t0:float, dt:float )->Waveform:
        """ For a given dt and t0, calculate the envelop waveform"""
        points = int( -(self.duration //-dt) )
        envelope = Waveform(t0, dt, empty(points))

        time = envelope.get_xAxis()
        envelope.Y = self.envelopeFunc( time, *self.parameters )
        
        return envelope

    def generate_signal( self, t0:float, dt:float )->Waveform:
        """ For a given dt and t0, calculate the signal waveform"""

        envelope = self.generate_envelope( t0, dt )
        signal = Waveform(envelope.x0, envelope.dx, empty(envelope.Y.shape[-1]))
        time = envelope.get_xAxis()
        if issubdtype(envelope.Y.dtype,complex):
            phase_I = 2.*pi*self.carrierFrequency*time +self.carrierPhase
            phase_Q = phase_I +pi/2
            LO_I = cos( phase_I )
            LO_Q = cos( phase_Q )
            signal.Y = envelope.Y.real*LO_I +envelope.Y.imag*LO_Q
        else:
            signal.Y = envelope.Y*cos( 2.*pi*self.carrierFrequency*time +self.carrierPhase)

        return signal

    def generate_IQSignal( self, t0:float, dt:float, IFFreq:float, IQMixer:tuple=(1,90,0,0) )->Tuple[Waveform,Waveform,float]:
        """
        For the pulse is generate by IQMixer
        For a given dt and t0, calculate the I/Q for IQmixer. \n

        IFFreq: The Intermediate frequency of I/Q ( Unit in dt ) \n
        IQMixer: The parametrs for calibrate IQmixer\n
            p1: I/Q Amplitude Balance ( dimensionless ratio )\n
            p2: Phase Balance ( unit in angle )\n
            p3: I offset\n
            p4: Q offset\n
        The LO frequency should be RF-IF (RF is carrier frequency)
        """
        envelope = self.generate_envelope( t0, dt )
        data_I, data_Q = upConversion_IQ( envelope.Y, IFFreq*dt, IQMixer)
        signal_I = Waveform(t0, dt, data_I)
        signal_Q = Waveform(t0, dt, data_Q)
        freq_LO = self.carrierFrequency - IFFreq
        return signal_I, signal_Q, freq_LO




# API
def get_Pulse_gauss ( duration:float, parameters:tuple, carrierFrequency:float=0, carrierPhase:float=0  ):
    """ 
    Get a Pulse Object
    p0: Amplitude 
    p1: sigma
    p2: Peak Position
    """
    newPulse = Pulse()
    newPulse.carrierFrequency = carrierFrequency
    newPulse.carrierPhase = carrierPhase
    newPulse.duration = duration
    newPulse.envelopeFunc = gaussianFunc
    newPulse.parameters = parameters

    return newPulse


def get_Pulse_DRAG ( duration:float, parameters:tuple, carrierFrequency:float=0, carrierPhase:float=0  ):
    """ 
    Get a Pulse Object \n
    p0: Amplitude \n
    p1: sigma \n
    p2: Peak Position \n
    p3: derivative Gaussian amplitude ratio \n
    """
    newPulse = Pulse()
    newPulse.carrierFrequency = carrierFrequency
    newPulse.carrierPhase = carrierPhase
    newPulse.duration = duration
    newPulse.envelopeFunc = DRAGFunc
    newPulse.parameters = parameters

    return newPulse





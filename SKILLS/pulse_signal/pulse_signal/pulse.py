# import sys
# sys.path.insert(0, r'../')
# Numpy Series
# Typing
from numpy import ndarray, complex128, issubdtype
# Array
from numpy import array, linspace, empty, append
# Math
from numpy import cos, sin, exp, arctan2, radians, sign, sqrt
# const
from numpy import pi

from typing import List, Tuple
from .common_Mathfunc import gaussianFunc, DRAGFunc
from .waveform import Waveform
from .digital_mixer import upConversion_IQ, upConversion_RF



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
        envelope.Y = exp(1j*self.carrierPhase) *envelope.Y
        return envelope

    def generate_signal( self, t0:float, dt:float )->Waveform:
        """ For a given dt and t0, calculate the signal waveform"""

        envelope = self.generate_envelope( t0, dt )
        signal = Waveform(envelope.x0, envelope.dx, empty(envelope.Y.shape[-1]))
        time = envelope.get_xAxis()
        if issubdtype(envelope.Y.dtype,complex):
            signal.Y = upConversion_RF( envelope.Y.real, envelope.Y.imag, self.carrierFrequency*dt )
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

class QAM():
    """
    Quadrature amplitude modulation (QAM)
    In-phase component I(t) is real part of envelope.
    Quadrature component Q(t) is imag part of envelope
    """
    def __init__ ( self, dt:float = 1 ):
        self.carrierFrequency = None
        self.envelope = array([[]])
        self.dt = dt

    @property
    def amplitude ( self )->ndarray:
        """ Quadrature component Q(t)."""
        return sqrt(self.envelope[0]**2+self.envelope[1]**2)

    def import_pulseSequence( self, pulses:List[Pulse], dt:float = None ):

        if dt == None: dt = self.dt
        envelope_RF = array([])
        for pulse in pulses:
            self.carrierFrequency = pulse.carrierFrequency
            new_envelope = pulse.generate_envelope( 0, dt ).Y
            envelope_RF = append( envelope_RF, new_envelope, axis=0 )
        self.envelope = envelope_RF
        return envelope_RF
        
    def SSB( self, freqIF:float, envelope_RF:ndarray = None, dt:float = None, IQMixer:tuple=(1,90,0,0) )->Tuple[ndarray,ndarray,float]:
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
        if dt == None: dt = self.dt
        if envelope_RF == None: envelope_RF = self.envelope
        signal_I, signal_Q = upConversion_IQ( envelope_RF, freqIF*dt, IQMixer=IQMixer )
        if self.carrierFrequency != None:
            freq_LO = self.carrierFrequency - freqIF
            return signal_I, signal_Q, freq_LO
        else: # Do not care carrier frequency
            return signal_I, signal_Q



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





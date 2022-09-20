# Numpy
# Typing
from numpy import ndarray
# Array
from numpy import array, empty
# Numpy common math function
from numpy import arctan2, cos, sin, angle, radians, sign
# const
from numpy import pi
from typing import Tuple
from .waveform import Waveform


def leakage_suppress( signal_I, signal_Q, IQMixer:Tuple=(1,90,0,0) ):
    """
    add offset in IF signal for suppress LO leakage.
    """
    offsetI = IQMixer[2]
    offsetQ = IQMixer[3]
    signal_I -= offsetI
    signal_Q -= offsetQ

    return signal_I, signal_Q


def upconversion_LO( freq_carrier:float, freq_IF:float):
    return freq_carrier-freq_IF

def upConversion_IQ( envelope_RF:ndarray, freq_IF:float, IQMixer:Tuple=(1,90,0,0), suppress_leakage = True )->Tuple[ndarray,ndarray]:
    """
    IFFreq unit is 1/dt of envelope_RF
    """
    ampBalance = IQMixer[0]
    phaseBalance = IQMixer[1]
    offsetI = IQMixer[2]
    offsetQ = IQMixer[3]

    time = array(range(len(envelope_RF)))

    LOShiftSign = sign(sin(radians(phaseBalance)))
    
    envelopeIQ = abs( envelope_RF )
    envelopeI = envelopeIQ /cos(radians(abs(phaseBalance)-90))
    envelopeQ = envelopeI /ampBalance
    phi_envelope = arctan2( envelope_RF.imag, envelope_RF.real )
    phi_Q = phi_envelope -LOShiftSign*pi/2
    phi_I = phi_Q -radians(phaseBalance) +pi

    signal_I = envelopeI *cos( 2. *pi *freq_IF *time +phi_I) -offsetI
    signal_Q = envelopeQ *cos( 2. *pi *freq_IF *time +phi_Q) -offsetQ
    if suppress_leakage:
        signal_I, signal_Q = leakage_suppress(signal_I,signal_Q,IQMixer)

    return signal_I, signal_Q


def upConversion_RF ( I:ndarray, Q:ndarray, LOFreq:float, IQMixer:tuple=(1,90,0,0))->ndarray:
    """
    IFFreq unit is 1/dt of envelope_RF
    """
    time = array(range(len(I)))
    ampBalance = IQMixer[0]
    phaseBalance = IQMixer[1]
    offsetI = IQMixer[2]
    offsetQ = IQMixer[3]
    mixed_I = (I+offsetI)*cos( 2.*pi*LOFreq*time )
    mixed_Q = (Q+offsetQ)*ampBalance*cos( 2.*pi*LOFreq*time +radians(phaseBalance)) 
    signal_RF = mixed_I+mixed_Q
    return signal_RF

# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 10:34:47 2020

@author: shiau
"""
import numpy as np
import scipy.fft as spfft
from scipy.interpolate import interp1d

class Signal_sampling(object):
    
    def __init__( self, t0, dt, signal, *args,**kwargs ):
        
        # Time sequence
        self._row_number = signal.shape[1]
        self._t0 = t0
        self._dt = dt
        
        # Waveform
        self._time = np.linspace( self._t0, self._t0 +self._dt*self._row_number, self._row_number )
        self._signal = signal

    @property    
    def row_number ( self ):
        return int(self._row_number)
    @property
    def t0 ( self ):
        return float(self._t0)
    @property
    def dt ( self ):
        return float(self._dt)    

    @property
    def signal ( self ):
        return np.array(self._signal)
    @signal.setter
    def signal ( self, signal ):
        self._signal = signal
    
    @property    
    def time ( self ):
        return np.array(self._time)

   
        
    def get_FftAnalysis ( self, channel, fft_region ):
        
        
        if fft_region[0] < self.time[1]:
            fft_region[0] = self.time[1]       
        if fft_region[1] > self.time[self.row_number-1]:
            fft_region[1] = self.time[self.row_number-1]
            
        region_index = (int((fft_region[0]-self.t0)/self.dt), int((fft_region[1]-self.t0)/self.dt))

        data_points = region_index[1]-region_index[0]
        f_points = data_points//2
        faxis = spfft.fftfreq(data_points,self.dt)[0:f_points]

        vector = spfft(self.signal[channel][region_index[0]:region_index[1]])[0:f_points]/self.row_number
        power = abs(vector)
        phase = np.angle(vector)
        return faxis, power, phase

class HybridCoupler90():
    def __init__( self, err_amp=1, err_phase=0, *args, **kwargs ):
        super().__init__(  *args, **kwargs )
         # Hybrid Coupler
        self._quadrature_err_amp = err_amp # I/Q imbalance error
        self._quadrature_err_phase = err_phase # I/Q imbalance error    
        
    @property    
    def quadrature_err_amp ( self ):
        return self._quadrature_err_amp    
    @quadrature_err_amp.setter    
    def quadrature_err_amp ( self, amp ):
        self._quadrature_err_amp = amp   
        
    @property    
    def quadrature_err_phase ( self ):
        return self._quadrature_err_phase    
    @quadrature_err_phase.setter 
    def quadrature_err_phase ( self, phase ):
        self._quadrature_err_phase = phase     

class Mixer():
    def __init__( self, bias=(0,0), *args, **kwargs ):
        super().__init__(  *args, **kwargs )
        # Mixer property
        self._bias_err = bias # I/Q bias error
    @property    
    def bias_err ( self ):
        return self._bias_err    
    @bias_err.setter 
    def bias_err ( self, bias ):
        self._bias_err = bias         
        
class IQMixer():   
    def __init__( self, err_amp=1, err_phase=0, bias=(0,0) ):
        # IQ mixer property
        super().__init__( )
        self._mixer = Mixer(bias)
        self._hybridCoupler = HybridCoupler90(err_amp,err_phase)

    @property    
    def mixer ( self ):
        return self._mixer   
    @mixer.setter    
    def mixer ( self, mixer ):
        self._mixer = mixer
    @property    
    def hybridCoupler ( self ):
        return self._hybridCoupler
    @hybridCoupler.setter    
    def hybridCoupler ( self, hybridCoupler ):
        self._hybridCoupler = hybridCoupler                 
        
class SingleTone():
    def __init__( self, amp, freq, phase, offset, *args,**kwargs ):
        # Tone property
        self._amp = amp # I/Q imbalance error
        self._freq = freq
        self._phase = phase
        self._offset = offset # I/Q bias error   
    
    @property    
    def amp ( self ):
        return self._amp    
    @amp.setter    
    def amp ( self, amp ):
        self._amp = amp   
    
    @property    
    def freq ( self ):
        return self._freq    
    @freq.setter    
    def freq ( self, freq ):
        self._freq = freq 
        
    @property    
    def phase ( self ):
        return self._phase
    @phase.setter 
    def phase ( self, phase ):
        self._phase = phase  
    
    @property    
    def offset ( self ):
        return self._offset
    @offset.setter 
    def offset ( self, offset ):
        self._offset = offset  

class TransmissionLine():
    def __init__( self, delay ):
        # Tone property
        self._delay = delay # I/Q imbalance error
    @property    
    def delay ( self ):
        return self._delay
    def transmission_parameter( self, freq ):
        s21 = np.exp(-2*np.pi*1j*freq*self.delay)       
        return s21
    
class Resonator():
    def __init__( self, resonator_freq, resonator_phase, Ql, Qc ):
        # Tone property
        self._resonator_freq = resonator_freq
        self._resonator_phase = resonator_phase
        self._loaded_quality = Ql
        self._coupling_quality = Qc
    @property    
    def resonator_freq ( self ):
        return self._resonator_freq
    @property    
    def resonator_phase ( self ):
        return self._resonator_phase
    @property    
    def loaded_quality ( self ):
        return self._loaded_quality
    @property    
    def coupling_quality ( self ):
        return self._coupling_quality  
     
    def transmission_parameter( self, freq ):
        d = (self.loaded_quality/abs(self.coupling_quality))
        resonator_s21 = 1-d*np.exp(1j*self.resonator_phase)/(1+2j*self.loaded_quality*(freq/self.resonator_freq-1))
        return resonator_s21

# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 16:51:04 2020

@author: shiau
"""

import numpy as np
import qspp.core as sa_core
import qspp.waveform as wf
import scipy.signal as sp_sig
from scipy.interpolate import interp1d




class Simulation_circuit(sa_core.Signal_sampling):
    
    def __init__( self, t0, dt, row_number, col_Number ):    
        super().__init__(t0, dt, np.empty((col_Number,row_number)))
        
    
    
    def process_generateSingleTone ( self, input_tone = sa_core.SingleTone, output_channel = 0 ):
        self._signal[output_channel] = wf.get_sinewaveSummation( self.time, [input_tone.amp], [input_tone.freq], [input_tone.phase] )
        return self._signal[output_channel]
    
    def process_HybridCoupler90 ( self, input_tone = sa_core.SingleTone, HybridCoupler= sa_core.HybridCoupler90, output_channel=(0,1) ):
        
        amp = input_tone.amp    
        omega = 2*np.pi*input_tone.freq
        phi = input_tone.phase
        offset = input_tone.offset
        t = self.time
        sig_LO_I = amp*np.cos(omega*t+phi)+offset
        sig_LO_Q = amp*np.cos(omega*t+phi-np.pi/2)+offset 
        if output_channel != None:
            ind_LO_I = output_channel[0]
            ind_LO_Q = output_channel[1]
            self._signal[ind_LO_I] = sig_LO_I
            self._signal[ind_LO_Q] = sig_LO_Q      
        return np.array([sig_LO_I, sig_LO_Q])
    
    def process_AmplitudeModulation ( self, envelope = None, input_channel=0, output_channel = 0 ):
        
        self._signal[output_channel] = envelope*self._signal[input_channel]
        
        
        
    def process_LowPass ( self, order, cutoff, input_channel = 0, output_channel = 0 ):        
        sos = sp_sig.butter(order, cutoff, 'low', analog=False, output='sos')
        self._signal[output_channel] = sp_sig.sosfilt(sos, self.signal[input_channel])

    def process_Mixer_upConversion ( self, input_LO_channel=0 ,input_IF_channel=1, output_RF_channel =None ): 
        ind_LO = int(input_LO_channel)
        ind_IF = int(input_IF_channel)
        mix_sig_RF = self.signal[ind_LO] *self.signal[ind_IF]
        if output_RF_channel != None:
            ind_RF = int(output_RF_channel)   
            self._signal[ind_RF] = mix_sig_RF
            
        return mix_sig_RF
    
    def process_Mixer_downConversion ( self, input_RF_channel =0, input_LO_channel=1, output_IF_channel=None ):
        ind_RF = int(input_RF_channel)
        ind_LO = int(input_LO_channel)
        output_IF = self.signal[ind_RF] * self.signal[ind_LO]
        if output_IF_channel != None:
            ind_IF = int(output_IF_channel) 
            self._signal[ind_IF] = output_IF
            
        return output_IF

    def process_IQMixer_upConversion ( self, LO_tone = sa_core.SingleTone, IQMixer =sa_core.IQMixer, output_LO_channels=(0,1), input_IF_channels=(2,3), output_RF_channel =None ):
        
        self.process_HybridCoupler90(LO_tone, IQMixer.hybridCoupler, output_LO_channels)
        mix_sig_I = self.process_Mixer_upConversion(output_LO_channels[0],input_IF_channels[0])
        mix_sig_Q = self.process_Mixer_upConversion(output_LO_channels[1],input_IF_channels[1])
        output_RF = mix_sig_I+mix_sig_Q
        if output_RF_channel != None:   
            self._signal[output_RF_channel] = output_RF
        return output_RF
    
    def process_IQMixer_downConversion ( self, LO_tone = sa_core.SingleTone, IQMixer =sa_core.IQMixer, output_LO_channels=(0,1), input_RF_channel=2, output_IF_channels =None ):

        ind_LO_I = int(output_LO_channels[0])
        ind_LO_Q = int(output_LO_channels[1])

        self.process_HybridCoupler90(LO_tone, IQMixer.hybridCoupler, output_LO_channels)
        mix_sig_I = self.process_Mixer_downConversion(input_RF_channel, ind_LO_I, None)
        mix_sig_Q = self.process_Mixer_downConversion(input_RF_channel, ind_LO_Q, None)
            
        if output_IF_channels != None: 
            ind_IF_I = int(output_IF_channels[0])
            ind_IF_Q = int(output_IF_channels[1])
            self._signal[ind_IF_I] = mix_sig_I
            self._signal[ind_IF_Q] = mix_sig_Q
        return np.array([mix_sig_I,mix_sig_Q])    
    
    def process_Resonator ( self, operate_frequency, resonator=sa_core.Resonator, input_channel=0, output_channel=1 ):
        
        s21 = resonator.transmission_parameter(operate_frequency)
        self._signal[input_channel] = self.signal[output_channel]*s21.real    
        
    def process_sampling ( self, t0, dt ):       
        f = interp1d(self.time, self.signal)
        
        new_row_number = int(self.dt*self.row_number/dt)
        
        new_signal = sa_core.Signal_sampling( t0, dt, np.empty((self.signal.shape[0],new_row_number)) )
        new_signal._signal = f(new_signal.time)
        print( 'Time sequence is reset as t0 = ', t0,',dt = ', dt, ' for ', self.row_number, 'points')

        return new_signal
        
        
        
    
 
        
        
        
        
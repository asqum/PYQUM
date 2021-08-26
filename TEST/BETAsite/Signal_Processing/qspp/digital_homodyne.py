# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 11:01:54 2020

@author: shiau
"""

import qspp.core as sa_core
from numpy import array, mean, sin, cos, pi, empty, linspace, argmax, cumsum, concatenate, zeros, ones
import scipy.signal as sp_sig
class DigitalHomodyne(sa_core.Signal_sampling):

    def __init__ ( self, t0, dt, processed_signal ):
        super().__init__( t0, dt, processed_signal )
        self._statistic_region = array([0,self.row_number], dtype='int')
        self._downconversion_freq = 0    

    @property
    def region_statistic( self ):
        return self._region_statistic
    @region_statistic.setter
    def region_statistic( self, region ):
        self._region_statistic = region

    
    @property
    def downconversion_freq ( self ):
        return self._downconversion_freq
    @downconversion_freq.setter
    def downconversion_freq ( self, freq ):
        self._downconversion_freq = freq    

    def get_average ( self, statistic_region ):
        
        region_index = ((statistic_region-self.t0)/self.dt).astype('int') 
        return mean( self.signal[:,region_index[0]:region_index[1]], axis=1 )    

    def process_LowPass ( self, order, cutoff ):        
        sos = sp_sig.butter(order, cutoff, 'low', analog=False, output='sos')
        self._signal = array([sp_sig.sosfilt(sos, self.signal[i]) for i in range(2)])
        # self._signal[1] = sp_sig.sosfilt(sos, self.signal[1])

    def get_MaxFreq ( self, fft_region):

        freq_axis, power, phase = self.get_FftAnalysis ( 0, fft_region )
        freq_I = freq_axis[argmax(power[1:])]
        # print("freq_I: %s" %freq_I)
        return freq_I




class DualChannel(DigitalHomodyne):

    def __init__ ( self, t0, dt, processed_signal ):
        super().__init__( t0, dt, processed_signal )
        self._iq_mixer = sa_core.IQMixer

    @property
    def iq_mixer( self ):
        return self._iq_mixer

    def get_RotationMatrix ( self, t ):
        omega = 2*pi*self.downconversion_freq # relative IF omega = freq(LO) - freq(RF)
        corr_amp = self.iq_mixer.hybridCoupler.quadrature_err_amp
        corr_phase = self.iq_mixer.hybridCoupler.quadrature_err_phase
        R = array([  
                    [cos(omega*t+corr_phase)/corr_amp, sin(omega*t)],
                    [-sin(omega*t+corr_phase)/corr_amp, cos(omega*t)]
                    ])        
        return R.transpose(2,0,1)

    def process_DownConversion ( self, freq, iq_mixer=sa_core.IQMixer()  ):        
        self.downconversion_freq = freq
        self._iq_mixer = iq_mixer
        bias = mean(self.signal,axis=1)
        #print("native signal offset by average: %s" %bias)
        self.iq_mixer.mixer.bias = (bias[0],bias[1])
        IQ_vect = self.signal.transpose().reshape((len(self.time),2,1))
        # ROTATION BY VECTORIZATION:
        IQ_vect = self.get_RotationMatrix(self.time) @ ( IQ_vect - (bias.reshape((2,1))*ones(len(self.time))).transpose().reshape((len(self.time),2,1)) )
        self._signal = IQ_vect.reshape(len(self.time),2).transpose()
        # print("shape: %s,%s" %(self._signal.shape, self.time.shape))

    # OLD SLOW FOR-LOOP METHOD:
    # def get_RotationMatrix ( self, t ):
    #     omega = 2*pi*self.downconversion_freq # relative IF omega = freq(LO) - freq(RF)
    #     corr_amp = self.iq_mixer.hybridCoupler.quadrature_err_amp
    #     corr_phase = self.iq_mixer.hybridCoupler.quadrature_err_phase
    #     R = array([  
    #                 [cos(omega*t+corr_phase)/corr_amp,sin(omega*t)],
    #                 [-sin(omega*t+corr_phase)/corr_amp,cos(omega*t)]
    #                 ])        
    #     return R

    # def process_DownConversion ( self, freq, iq_mixer=sa_core.IQMixer()  ):        
    #     self.downconversion_freq = freq
    #     self._iq_mixer = iq_mixer
    #     bias = mean(self.signal,axis=1)
    #     print("native signal offset by average: %s" %bias)
    #     self.iq_mixer.mixer.bias = (bias[0],bias[1])
    #     IQ_vect = self.signal.transpose()
    #     for step in range(self.row_number):
    #         IQ_vect[step] = self.get_RotationMatrix( self.time[step] )@(IQ_vect[step]-bias)
    #     self._signal = IQ_vect.transpose()

    
    
class SingleChannel(DigitalHomodyne):

    def __init__ ( self, t0, dt, processed_signal ):
        
        
        super().__init__( t0, dt, processed_signal )

    def process_DownConversion ( self, freq, iq_mixer=sa_core.IQMixer() ):
        self._downconversion_freq = freq
        omega = freq *2 *pi
        origin_sig = array([self.signal[0],self.signal[0]])
        conversion_vector = array([cos(self.time[0]*omega), sin(self.time[0]*omega)])
        integ_sig = empty((2,self.row_number))
        integ_sig[:,0] = origin_sig[:,0] *conversion_vector*self.dt
        # INTEGRATE BY VECTORIZE:
        conversion_vector = array([cos(self.time*omega), sin(self.time*omega)])
        integ_sig = cumsum(origin_sig*conversion_vector*self.dt, axis=1)
        # Segmented differentiation per IF-period:
        period_datapoints = abs( int(1/freq/self.dt) )
        integ_sig = concatenate((zeros((2,period_datapoints)), integ_sig), axis=1) # pre-compensation
        integ_sig_t1 = integ_sig[:,:-period_datapoints]
        integ_sig_t2 = integ_sig[:,period_datapoints:]
        self._signal = (integ_sig_t2-integ_sig_t1)*2*freq # differentiate then renormalization
        self._signal[1] = -self._signal[1]
        # print("Original: %s, Integrated: %s" %(origin_sig.shape, self._signal.shape))
        
        # self._t0 = self.t0 +self.dt*period_datapoints/2
        # self._row_number = self.row_number-period_datapoints
        # self._time = linspace(self.t0, self.t0+self.dt*self.row_number,self.row_number)


        
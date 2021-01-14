# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 01:22:55 2021

@author: shiau
"""

import sys 
sys.path.append("..") 

import qspp.signal_simulation as sa_sig
import qspp.waveform as sa_wf
import qspp.digital_homodyne as sa_dh
import qspp.core as sa_core
import matplotlib.pyplot as plt
import numpy as np

simulation_points = 220000
simulation_dt = 0.005 #ns

sampling_dt = 1
sampling_points = int((simulation_points*simulation_dt)/sampling_dt)

t0 = 0 #ns

rising_time = 10 #ns
readout_time = 1000 #ns
start_readout_time = 50 #ns


fft_region = np.array([start_readout_time, start_readout_time+readout_time]) #ns



# Simulation Signal
freq_LO = 5 #GHz
freq_IF = 0.02 #GHz
simulation_signal = sa_sig.Simulation_circuit(  t0, simulation_dt, simulation_points, 12 )

'''
Channel list
Origin LO: 0
up-converter IF I: 1
up-converter IF Q: 2
up-converter LO I: 3
up-converter LO Q: 4
up-converter RF: 5
'''
# Up conversion simulation
## Set LO properties for up conversion
up_LO_tone = sa_core.SingleTone(1,freq_LO,0,0)
simulation_signal.process_generateSingleTone( up_LO_tone, 0 )

## Set IF properties for up conversion
data_IF_envelope = sa_wf.get_gaussianEdgeStepPulse( simulation_signal.time, start_readout_time, readout_time, 1, rising_time)
up_IF_I_tone = sa_core.SingleTone(1,freq_IF,0,0)
up_IF_Q_tone = sa_core.SingleTone(1,freq_IF,-np.pi/2,0)


simulation_signal.process_generateSingleTone( up_IF_I_tone, 1 )
simulation_signal.process_AmplitudeModulation( data_IF_envelope, 1, 1 )

simulation_signal.process_generateSingleTone( up_IF_Q_tone, 2 )
simulation_signal.process_AmplitudeModulation( data_IF_envelope, 2, 2 )

## Do up conversion
mixer_up = sa_core.IQMixer(1,0,(0,0))
sig_up_RF = simulation_signal.process_IQMixer_upConversion( LO_tone = up_LO_tone, IQMixer=mixer_up, output_LO_channels=(3,4), input_IF_channels=(1,2), output_RF_channel =5 )

# Plot the simulation signal after up conversion
"""
fig1, axs1 = plt.subplots(2)
axs1[0].plot(simulation_signal.time, simulation_signal.signal[5],'-',markersize=0.5)
f_conv, power_conv, phase_conv = simulation_signal.get_FftAnalysis(5,fft_region)
axs1[1].plot(f_conv, power_conv,'-',markersize=0.5)
fig1.show()
"""


# Down conversion simulation
## Set LO properties for down conversion
down_LO_tone = sa_core.SingleTone(1,freq_LO,0,0)
mixer_down = sa_core.IQMixer(1,0,(0,0))
simulation_signal.process_IQMixer_downConversion( LO_tone=down_LO_tone, IQMixer=mixer_down, output_LO_channels=(3,4), input_RF_channel=5, output_IF_channels=(6,7))


# Plot the simulation signal after down conversion
"""
fig2, axs2 = plt.subplots(2)
axs2[0].plot(simulation_signal.time, simulation_signal.signal[6],'-',markersize=0.5)
axs2[0].plot(simulation_signal.time, simulation_signal.signal[7],'-',markersize=0.5)
f_conv, power_conv, phase_conv = simulation_signal.get_FftAnalysis(6,fft_region)
axs2[1].plot(f_conv, power_conv,'-',markersize=0.5)
f_conv, power_conv, phase_conv = simulation_signal.get_FftAnalysis(7,fft_region)
axs2[1].plot(f_conv, power_conv,'-',markersize=0.5)
fig2.show()
"""

# Low pass filter simulation
simulation_signal.process_LowPass( 6, 0.05, 6, 8)
simulation_signal.process_LowPass( 6, 0.05, 7, 9)
# Plot the simulation signal after low pass filter
"""
fig3, axs3 = plt.subplots(2)
axs3[0].plot(simulation_signal.time, simulation_signal.signal[8],'o',markersize=0.5)
axs3[0].plot(simulation_signal.time, simulation_signal.signal[9],'o',markersize=0.5)
f_conv, power_conv, phase_conv = simulation_signal.get_FftAnalysis(8,fft_region)
axs3[1].plot(f_conv, power_conv,'-',markersize=0.5)
f_conv, power_conv, phase_conv = simulation_signal.get_FftAnalysis(9,fft_region)
axs3[1].plot(f_conv, power_conv,'-',markersize=0.5)
fig3.show()
"""

sampling_sig = simulation_signal.process_sampling(t0, sampling_dt)

fig4, axs4 = plt.subplots(2)
axs4[0].plot(sampling_sig.time, sampling_sig.signal[8],'o',markersize=0.5)
axs4[0].plot(sampling_sig.time, sampling_sig.signal[9],'o',markersize=0.5)
f_conv, power_conv, phase_conv = sampling_sig.get_FftAnalysis(8,fft_region)
axs4[1].plot(f_conv, power_conv,'-',markersize=0.5)
f_conv, power_conv, phase_conv = sampling_sig.get_FftAnalysis(9,fft_region)
axs4[1].plot(f_conv, power_conv,'-',markersize=0.5)
fig4.show()
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 01:38:37 2020

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

simulation_time = 500
simulation_dt = 0.005 #ns

simulation_points = int(simulation_time/simulation_dt)

sampling_dt = 1
sampling_points = int((simulation_time)/sampling_dt)

t0 = 0 #ns

rising_time = 0 #ns
readout_time = 500 #ns
start_readout_time = 0 #ns


fft_region = np.array([start_readout_time, start_readout_time+readout_time]) #ns



# Simulation Signal
freq_LO = 5 #GHz
freq_IF = 0.01 #GHz
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
up_IF_Q_tone = sa_core.SingleTone(1,freq_IF,0,0)


simulation_signal.process_generateSingleTone( up_IF_I_tone, 1 )
simulation_signal.process_AmplitudeModulation( data_IF_envelope, 1, 1 )

simulation_signal.process_generateSingleTone( up_IF_Q_tone, 2 )
simulation_signal.process_AmplitudeModulation( data_IF_envelope, 2, 2 )

## Do up conversion
mixer_up = sa_core.IQMixer(1,0,(0,0))
sig_up_RF = simulation_signal.process_IQMixer_upConversion( LO_tone = up_LO_tone, IQMixer=mixer_up, output_LO_channels=(3,4), input_IF_channels=(1,2), output_RF_channel =5 )

# Plot the simulation signal after up conversion

fig1, axs1 = plt.subplots(2)
axs1[0].plot(simulation_signal.time, simulation_signal.signal[5],'-',markersize=0.5)
f_conv, power_conv, phase_conv = simulation_signal.get_FftAnalysis(5,fft_region)
axs1[1].plot(f_conv, power_conv,'-',markersize=0.5)
fig1.show()



# Down conversion simulation
## Set LO properties for down conversion
down_LO_tone = sa_core.SingleTone(1,freq_LO,0,0)
mixer_down = sa_core.IQMixer(1,0,(0,0))
simulation_signal.process_IQMixer_downConversion( LO_tone=down_LO_tone, IQMixer=mixer_down, output_LO_channels=(3,4), input_RF_channel=5, output_IF_channels=(6,7))


# Plot the simulation signal after down conversion

fig2, axs2 = plt.subplots(2)
axs2[0].plot(simulation_signal.time, simulation_signal.signal[6],'-',markersize=0.5)
axs2[0].plot(simulation_signal.time, simulation_signal.signal[7],'-',markersize=0.5)
f_conv, power_conv, phase_conv = simulation_signal.get_FftAnalysis(6,fft_region)
axs2[1].plot(f_conv, power_conv,'-',markersize=0.5)
f_conv, power_conv, phase_conv = simulation_signal.get_FftAnalysis(7,fft_region)
axs2[1].plot(f_conv, power_conv,'-',markersize=0.5)
fig2.show()


# Low pass filter simulation
simulation_signal.process_LowPass( 6, 0.05, 6, 8)
simulation_signal.process_LowPass( 6, 0.05, 7, 9)
# Plot the simulation signal after low pass filter


fig3, axs3 = plt.subplots(2)
axs3[0].plot(simulation_signal.time, simulation_signal.signal[8],'o',markersize=0.5)
axs3[0].plot(simulation_signal.time, simulation_signal.signal[9],'o',markersize=0.5)
f_conv, power_conv, phase_conv = simulation_signal.get_FftAnalysis(8,fft_region)
axs3[1].plot(f_conv, power_conv,'-',markersize=0.5)
f_conv, power_conv, phase_conv = simulation_signal.get_FftAnalysis(9,fft_region)
axs3[1].plot(f_conv, power_conv,'-',markersize=0.5)
fig3.show()

sampling_sig = simulation_signal.process_sampling(t0, sampling_dt)

"""
fig4, axs4 = plt.subplots(2)
axs4[0].plot(sampling_sig.time, sampling_sig.signal[8],'o',markersize=1)
axs4[0].plot(sampling_sig.time, sampling_sig.signal[9],'o',markersize=1)
f_conv, power_conv, phase_conv = sampling_sig.get_FftAnalysis(8,fft_region)
axs4[1].plot(f_conv, power_conv,'-',markersize=0.5)
f_conv, power_conv, phase_conv = sampling_sig.get_FftAnalysis(9,fft_region)
axs4[1].plot(f_conv, power_conv,'-',markersize=0.5)
fig4.show()
"""



# Signal Processing
# Creat 'signal' type object

processing_data = sa_dh.DualChannel( t0, sampling_dt, sampling_sig.signal[8:10,:] ) # IQ channel
Idata, Qdata = processing_data.signal
print("I:\n%s \nQ:\n%s" %(Idata, Qdata))
processing_data_s = sa_dh.SingleChannel( t0, sampling_dt, sampling_sig.signal[8:10,:] ) # Single channel



# Plot the signal for digital down converter

fig4, axs4 = plt.subplots(3)
for i in [0,1]:
    axs4[0].plot(processing_data.time, processing_data.signal[i],'o',markersize=1)
    f_conv, power_conv, phase_conv = processing_data.get_FftAnalysis(i,fft_region)
axs4[1].plot(f_conv, power_conv,'-',markersize=1)
axs4[2].plot(processing_data.signal[0], processing_data.signal[1],'-',markersize=1)
fig4.show()



# Do dual channel digital homodyne
# processing_data.process_DownConversion( freq_IF, mixer_down ) # IQ channel
processing_data.process_DownConversion( freq_IF ) # IQ channel
processing_data_s.process_DownConversion( freq_IF ) # Single channel



# Plot the signal after digital down converter

fig5, axs5 = plt.subplots(2)
for i in [0,1]:   
    axs5[0].plot(processing_data.time, processing_data.signal[i],'o',markersize=1)
    f_conv, power_conv, phase_conv = processing_data.get_FftAnalysis(i,fft_region)
    axs5[1].plot(f_conv, power_conv,'-',markersize=0.5)
    # axs5[2].plot(processing_data_s.time, processing_data_s.signal[i],'o',markersize=1)
    # f_conv, power_conv, phase_conv = processing_data_s.get_FftAnalysis(i,fft_region)
    # axs5[3].plot(f_conv, power_conv,'-',markersize=0.5)
fig5.show()


# Get the average value
ave_point = processing_data.get_average( np.array([start_readout_time, start_readout_time+readout_time]) )
ave_amp = np.sqrt(ave_point[0]**2+ave_point[1]**2)
ave_phase = np.arctan2(ave_point[1],ave_point[0])
print(ave_point, ave_amp, ave_phase)


ave_point_s = processing_data_s.get_average( np.array([start_readout_time, start_readout_time+readout_time]) )
print(ave_point_s, np.arctan2(ave_point_s[1],ave_point_s[0]))


#Plot the time-averaged point on IQ plane

fig6, axs6 = plt.subplots()
axs6.plot(processing_data.signal[0], processing_data.signal[1],'o',markersize=0.5)
# axs6.plot(processing_data_s.signal[0], processing_data_s.signal[1],'o',markersize=0.5)
axs6.plot(ave_point[0], ave_point[1],'o',markersize=5)
# axs6.plot(ave_point_s[0], ave_point_s[1],'o',markersize=5)

fig6.show()
plt.show()




  


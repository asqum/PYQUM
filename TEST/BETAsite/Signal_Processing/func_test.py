# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 20:15:28 2020

@author: shiau
"""

import sys 
sys.path.append("..") 

import qspp.signal_simulation as sig
from scipy import interpolate
import matplotlib.pyplot as plt
import qspp.digital_homodyne as hd
import numpy as np
data_points = 1500
dt = 1 #ns
t0 = 0
rising_time = 20

freq_M = 10.164 #MHz
freq_G = freq_M*1e-3 #GHz
#print(freq)
# Simulation Signal
sig_test = sig.SimulationReadout( t0, dt, data_points )
sig_test.set_carrier( [1,0.0], [freq_G,freq_G*2], [2.4,0.5] )
sig_test.set_envelope( 5*rising_time, 1000, rising_time )
sig_test.set_noise(.1)
sig_test.IQcorr_amp = np.array([1,2], dtype='int' ) 
sig_test.IQcorr_phase = 0.2
sig_test.process_generateSignal()
test_t = sig_test.time 
test_v = sig_test.signal




# Signal Processing
# Creat signal type object
processing_data = hd.dual( t0, dt, sig_test.signal )

processing_data.set_region( np.array([ 0,processing_data.N]) )
f_origin , power_origin, phase_origin = processing_data.get_FftAnalysis() # Get spectrum

# set readout region
#processing_data.set_region( np.array([ int(rising_time)/dt+data_points/4,int(data_points*3/4)]) )
processing_data.set_region( np.array([ 0,processing_data.N]) )

#sig_region = processing_data.signal[:,processing_data.region[0]:processing_data.region[1]]
sig_region = processing_data.signal
time_region = test_t
#time_region = processing_data.time[processing_data.region[0]:processing_data.region[1]]
f_region , power_region, phase_region = processing_data.get_FftAnalysis() # Get spectrum

processing_data.process_MainSignalFreq()
fft_interpolateI = interpolate.CubicSpline(f_region,power_region[0])
f_interpolate = np.linspace(processing_data.downconversion_freq-0.01,processing_data.downconversion_freq+0.01,2000)

fft_interpolateQ = interpolate.CubicSpline(f_region,power_region[1])

print(f_interpolate[np.argmax(fft_interpolateI(f_interpolate))])
print(f_interpolate[np.argmax(fft_interpolateQ(f_interpolate))])

# Do dual channel digital homodyne
processing_data.process_DownConversion(freq_G, sig_test.IQcorr_amp, sig_test.IQcorr_phase)
#processing_data.process_DownConversion(freq_G, [1,1], 0)

#sig_conv = processing_data.signal[:,processing_data.region[0]:processing_data.region[1]]
sig_conv = processing_data.signal
f_conv, power_conv, phase_conv = processing_data.get_FftAnalysis() # Get spectrum


# Do Butterworth low pass filter
processing_data.process_LowPass(2, 0.1)

#sig_filter = processing_data.signal[:,processing_data.region[0]:processing_data.region[1]]
sig_filter = processing_data.signal
f_filter, power_filter, phase_filter = processing_data.get_FftAnalysis() # Get spectrum



# Plot data
fig1, axs1 = plt.subplots(2)
fig2, axs2 = plt.subplots(2)
fig3, axs3 = plt.subplots(2)

for i in [0,1]:    
    axs1[i].plot(test_t, sig_test.signal[i],'-',markersize=0.5)
    
    
    axs1[i].plot(time_region, sig_region[i],'-',markersize=0.5)
    axs1[i].plot(time_region, sig_conv[i],'-',markersize=0.5)
    axs1[i].plot(time_region, sig_filter[i],'-',markersize=0.5)
    
    axs3[i].plot(f_origin, power_origin[i],'-',markersize=0.5)   
    axs3[i].plot(f_region, power_region[i],'-',markersize=0.5)  

    axs3[i].plot(f_conv, power_conv[i],'-',markersize=0.5)
    axs3[i].plot(f_filter, power_filter[i],'-',markersize=0.5)    
    
    
axs3[0].plot(f_interpolate, fft_interpolateI(f_interpolate),'-',markersize=0.5)    
axs3[1].plot(f_interpolate, fft_interpolateQ(f_interpolate),'-',markersize=0.5)    

axs2[0].plot(sig_test.signal[0], sig_test.signal[1],'o',markersize=0.5)
axs2[0].plot(sig_region[0], sig_region[1],'o',markersize=0.5)
axs2[0].plot(sig_conv[0], sig_conv[1],'o',markersize=0.5)   
axs2[0].plot(sig_filter[0], sig_filter[1],'o',markersize=0.5)   

axs2[1].plot(test_t, np.angle(sig_test.signal[0]+1j*sig_test.signal[1]),'-',markersize=0.5)
axs2[1].plot(time_region, np.angle(sig_region[0]+1j*sig_region[1]),'-',markersize=0.5)   
axs2[1].plot(time_region, np.angle(sig_conv[0]+1j*sig_conv[1]),'-',markersize=0.5)   
axs2[1].plot(time_region, np.angle(sig_filter[0]+1j*sig_filter[1]),'-',markersize=0.5)   


fig1.show()
fig2.show()
fig3.show()

  


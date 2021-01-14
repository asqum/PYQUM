# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 01:22:39 2021

@author: shiau
"""


import sys 
sys.path.append("..") 

import qspp.signal_simulation as sig
import qspp.waveform as wf
import qspp.digital_homodyne as hd

from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np

data_points = 10500
dt = 0.01 #ns
t0 = 0 #ns
rising_time = 10 #ns
readout_time = 1000 #ns
start_readout_time = 50 #ns
resonator_freq = 6 #GHz

fft_region = np.array([20,120]) #ns




# Simulation Signal
sig_test = sig.Simulation_IQMixer( t0, dt, data_points )
scan_number = 100
freq_input = np.linspace(5.999,6.001,scan_number) #GHz
freq_IF = 0.2 #GHz
freq_LO = freq_input+freq_IF
output_amps = np.empty(scan_number)

for freq_index in range(scan_number):

    ## Set LO properties 
    sig_test.LO_freq = freq_LO[freq_index]
    sig_test.LO_phase = 0
    sig_test.process_generateLO()
    
    ## Set IF properties for up conversion
    sig_test.IF_freq = [freq_IF,freq_IF]
    sig_test.IF_phase = [0,-np.pi/2]
    sig_test.process_generateIF( wf.get_gaussianEdgeStepPulse(sig_test.time, start_readout_time, readout_time, 1, rising_time) )
    
    ## Do up conversion
    sig_test.process_upConversion()
    
    ## Pass resonator
    sig_test.process_Resonator(freq_input[freq_index], resonator_freq)
    
    # Down conversion simulation
    ## Set LO properties for down conversion
    sig_test.LO_phase = 0.
    sig_test.process_generateLO()
    sig_test.process_downConversion()
    
    
    # Low pass filter simulation
    sig_test.process_LowPass( 2, 4, 0.1 )
    sig_test.process_LowPass( 3, 4, 0.1 )
    
    # Plot the simulation signal after low pass filter
    
    
    # Signal Processing
    # Creat 'signal' type object
    #processing_data = hd.DualChannel( t0, dt, sig_test.waveform_IF ) # IQ channel
    processing_data = hd.SingleChannel( t0, dt, sig_test.waveform_IF ) # Single channel
 

    
    # Do dual channel digital homodyne
    #processing_data.process_DownConversion(freq_IF, sig_test.quadrature_err_amp, sig_test.quadrature_err_phase) # IQ channel
    processing_data.process_DownConversion(freq_IF) # Single channel
    

    
    # Get the average value
    ave_point = processing_data.get_average( np.array([start_readout_time, start_readout_time+readout_time]) )
    ave_amp = np.sqrt(ave_point[0]**2+ave_point[1]**2)
    ave_phase = np.arctan2(ave_point[1],ave_point[0])
    print( 'freq=', freq_input[freq_index], ave_point, 'amp=',ave_amp, 'phi=',ave_phase)
    output_amps[freq_index] = ave_amp
    
#Plot the time-averaged point on IQ plane

fig6, axs6 = plt.subplots()
axs6.plot(freq_input, output_amps,'o',markersize=5)
fig6.show()




  


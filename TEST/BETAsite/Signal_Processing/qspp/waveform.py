# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 17:25:39 2021

@author: shiau
"""

import numpy as np



        
def get_sinewaveSummation ( time, amps, freqs, phases ):
    waveform = np.zeros(time.shape[0])
    for a, f, phi in zip(amps, freqs, phases):
        omega = 2*np.pi*f
        waveform += a*np.cos(omega*time+phi)
    return waveform


def get_gaussianEdgeStepPulse ( time, start, width, height, sigma ):
    
    waveform = np.zeros(time.shape[0])
    if sigma != 0:
        waveform = waveform +get_gaussianEdge( time, start, sigma, height )
        waveform = waveform +get_gaussianEdge( time, start+width, -sigma, height )
    waveform = waveform +get_stepPulse( time, start, width, height )
  
    return waveform

def get_gaussianEdge ( time, center, sigma, height ):
    '''
    positive sigma for rising
    nagtive sigma for falling
    '''
    N = time.shape[0]
    shifted_time = time -center
    waveform = np.empty(N)
    for i in range(N):
        if shifted_time[i]/np.sign(sigma) < 0:
            waveform[i] = height *np.exp(-(shifted_time[i]/sigma)**2/2)
        else:
            waveform[i] =0
    return waveform


def get_stepPulse ( time, start, width, height ):
    
    N = time.shape[0]
    waveform = np.empty(N)
    for i in range(N):
        if time[i] > start and time[i] < start+width:
            waveform[i] =height      
        else:
            waveform[i] =0  
    return waveform
        
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 09:32:06 2022

@author: B00172

20220118-Sinica-ITRI_Pulse techniques.pptx
"""

import numpy as np
import matplotlib.pyplot as plt

class DRAGPulse:
    def __init__(self):
        pass
    
    def genGaussian(self, t, tcenter, twidth, alpha, delta):
        
        I = np.exp(-(t-tcenter)*(t-tcenter)/twidth/twidth)
        Q = -alpha / delta * (-2*(t-tcenter)/twidth/twidth) * I
        
        I_q = I;
        Q_q = Q;
        return I_q, Q_q

    def genDetunedGaussian(self, t, tcenter, twidth, alpha, delta, df):
        
        I = np.exp(-(t-tcenter)*(t-tcenter)/twidth/twidth)
        Q = -alpha / (delta - 2 * np.pi * df) * (-2*(t-tcenter)/twidth/twidth) * I
        cost = np.cos(2 * np.pi * df * t)
        sint = np.sin(2 * np.pi * df * t)
        
        I_q = I * cost - Q * sint;
        Q_q = I * sint + Q * cost;
        return I_q, Q_q


class AWGPulse:
    def __init__(self):
        pass
#        self.test = 1
    
    """
    Mixer_Coeff: [mixer_phase, mixer_IQratio, mixer_Ioffset, mixer_Qoffset]
    """
    def generate(self, t, I_q, Q_q, iffreq, Mixer_Coeff):
        
        mixer_phase, mixer_IQratio, mixer_Ioffset, mixer_Qoffset = Mixer_Coeff

        A = np.sqrt(I_q * I_q + Q_q * Q_q)
        phi = np.arctan2(Q_q, I_q)
        A1 = A / np.cos(mixer_phase)
        A2 = A1 / mixer_IQratio
        I_lo = A1 * np.cos (2 * np.pi * iffreq * t + phi - mixer_phase) - mixer_Ioffset
        Q_lo = A2 * np.sin (2 * np.pi * iffreq * t + phi) - mixer_Qoffset

        return I_lo, Q_lo
    
    """
    Generate the RFsignal from AWG-IQ and non-ideal mixer
    sin(wt), cos(wt + mixer_phase) * mixer_IQratio
    """
    def Mixering(self, t, I_lo, Q_lo, rffreq, Mixer_Coeff):
        
        mixer_phase, mixer_IQratio, mixer_Ioffset, mixer_Qoffset = Mixer_Coeff
        rfwave = (I_lo + mixer_Ioffset) * np.sin(2 * np.pi * rffreq * t) + (Q_lo + mixer_Qoffset) * np.cos(2 * np.pi * rffreq * t + mixer_phase) * mixer_IQratio
        
        return rfwave

    """
    Generate the ideal RF signal into qubit
    """
    def RFWaveGen(self, t, I_q, Q_q, qbfreq):
        
        rfwave = I_q * np.sin(2 * np.pi * qbfreq * t) + Q_q * np.cos(2 * np.pi * qbfreq * t)
        
        return rfwave

#===========================================
#Mixer_Coeff: [mixer_phase, mixer_IQratio, mixer_Ioffset, mixer_Qoffset]
Mixer_Coeff = [0.1,0.90,0,0]
qbfreq = 0.150
iffreq = 0.015
rffreq = qbfreq - iffreq
t = np.linspace(0, 100, 1000)

drag = DRAGPulse()
I_q, Q_q = drag.genDetunedGaussian(t, 50, 5, -0.1*5*5/2, 1, 0.01)

#I_q, Q_q = drag.genGaussian(t, 50, 5, -0.1*5*5/2, 1)

#I_q = np.array(np.exp(-(t-50)*(t-50)/25))
#Q_q = np.array(np.exp(-(t-50)*(t-50)/25)) * (t-50) * (-0.1)

plt.plot(t, I_q, 'r-', t, Q_q, 'b-')
plt.title('I, Q @ qubit frequency')
plt.xlabel('time (ns)')
plt.legend(['I_q','Q_q'])
plt.show()

#===========================================
awg = AWGPulse()
rfwave0 = awg.RFWaveGen(t, I_q, Q_q, qbfreq)

#===========================================
I_lo, Q_lo = awg.generate(t, I_q, Q_q, iffreq, Mixer_Coeff)
plt.plot(t, I_lo, 'r-', t, Q_lo, 'b-')
plt.title('I, Q @ IF frequency')
plt.xlabel('time (ns)')
plt.legend(['I_lo','Q_lo'])
plt.show()

rfwave1 = awg.Mixering(t, I_lo, Q_lo, rffreq, Mixer_Coeff)

#===========================================
plt.plot(t, rfwave0, 'r:', t, rfwave1, 'b-')
plt.title('RF Signal to qubit')
plt.xlabel('time (ns)')
plt.legend(['RFwave0','RFwave1'])
plt.show()

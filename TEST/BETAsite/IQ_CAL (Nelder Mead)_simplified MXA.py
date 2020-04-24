"""
Created on Wed Jan 15 11:17:10 2020
@author: mesch
"""

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

import copy
from pyqum.instrument.benchtop import RSA5 as MXA
from pyqum.instrument.benchtop import PSGA
from pyqum.instrument.modular import AWG
from pyqum.instrument.logger import status_code
from pyqum.instrument.analyzer import curve
from numpy import sin, cos, pi, array, float64, sum, dot

# Initialize instruments:
# PSGA
saga = PSGA.Initiate()
PSGA.rfoutput(saga, action=['Set', 1])
PSGA.frequency(saga, action=['Set', "5.5" + "GHz"])
PSGA.power(saga, action=['Set', "13" + "dBm"])
# SA
mxa = MXA.Initiate()
MXA.frequency(mxa, action=['Set','5.525GHz'])
MXA.fspan(mxa, action=['Set','150MHz'])
MXA.rbw(mxa, action=['Set','1MHz'])
MXA.vbw(mxa, action=['Set','100kHz'])
MXA.trigger_source(mxa, action=['Set','EXTernal1'])
# AWG
awgsess = AWG.InitWithOptions()
AWG.Abort_Gen(awgsess)
AWG.ref_clock_source(awgsess, action=['Set',int(1)]) # External 10MHz clock-reference
AWG.predistortion_enabled(awgsess, action=['Set',True])
AWG.output_mode_adv(awgsess, action=['Set',int(2)]) # Sequence output mode
AWG.arb_sample_rate(awgsess, action=['Set',float(1250000000)]) # maximum sampling rate
AWG.active_marker(awgsess, action=['Set','3']) # master
AWG.marker_delay(awgsess, action=['Set',float(0)])
AWG.marker_pulse_width(awgsess, action=['Set',float(1e-7)])
AWG.marker_source(awgsess, action=['Set',int(7)])
samplingrate = AWG.arb_sample_rate(awgsess)[1]
dt = 1e9/samplingrate # in ns
# PRESET Output:
for ch in range(2):
    channel = str(ch + 1)
    AWG.output_config(awgsess, RepCap=channel, action=["Set", 0]) # Single-ended
    AWG.output_filter_bandwidth(awgsess, RepCap=channel, action=["Set", 0])
    AWG.arb_gain(awgsess, RepCap=channel, action=["Set", 0.5])
    AWG.output_impedance(awgsess, RepCap=channel, action=["Set", 50])
# output settings:
for ch in range(2):
    channel = str(ch + 1)
    AWG.output_enabled(awgsess, RepCap=channel, action=["Set", int(1)])  # ON
    AWG.output_filter_enabled(awgsess, RepCap=channel, action=["Set", True])
    AWG.output_config(awgsess, RepCap=channel, action=["Set", int(2)]) # Amplified 1:2
    AWG.output_filter_bandwidth(awgsess, RepCap=channel, action=["Set", 0])
    AWG.arb_gain(awgsess, RepCap=channel, action=["Set", 0.5])
    AWG.output_impedance(awgsess, RepCap=channel, action=["Set", 50])

def AWG_Sinewave(ifreq,IQparams):
    '''
    ifreq: IF frequency in MHz
    '''

    AWG.Clear_ArbMemory(awgsess)
    WAVE = []

    Ioffset, Qoffset, ampratio, Iphase, Qphase = IQparams

    if (ampratio > -1.0) and (ampratio < 1.0):
        Iamp = 1
        Qamp = Iamp * ampratio
    else:
        Qamp = 1
        Iamp = Qamp/ampratio

    ifvoltag = [min(abs(Qamp),1), min(abs(Iamp),1)] # contain amplitude within 1V
    iffunction = ['sin', 'cos']
    iffreq = [ifreq, ifreq]
    ifoffset = [Qoffset, Ioffset]
    ifphase = [Qphase, Iphase]

    # construct waveform:
    for ch in range(2):
        channel = str(ch + 1)

        Nperiod = int(1000/iffreq[ch]/dt) # of points per period
        Nperiod *= 8
        wavefom = [ifvoltag[ch] * eval(iffunction[ch] + '(x*%s*%s/1000*2*pi + %s/180*pi)' %(dt,iffreq[ch],ifphase[ch])) + ifoffset[ch] for x in range(Nperiod)]

        createdwave = AWG.CreateArbWaveform(awgsess, wavefom)
        WAVE.append(createdwave[1])
    # Building Sequences:
    for ch in range(2):
        channel = str(ch + 1)	
        createdseqhandl = AWG.CreateArbSequence(awgsess, [WAVE[ch]], [1]) # loop# canbe >1 if longer sequence is needed in the future!
        # Channel Assignment:
        AWG.arb_sequence_handle(awgsess, RepCap=channel, action=["Set", createdseqhandl[1]])
    # Trigger Settings:
    for ch in range(2):
        channel = str(ch + 1)
        AWG.operation_mode(awgsess, RepCap=channel, action=["Set", 0])
        AWG.trigger_source_adv(awgsess, RepCap=channel, action=["Set", 0])
    AWG.Init_Gen(awgsess)
    AWG.Send_Pulse(awgsess, 1)

    return

class IQ_Cal:

    def __init__(self, suppression='LO', IQparams=array([0.,0.,1.,0.,0.]), STEP=array([-0.5,-0.5,0.5,12,12]), ratio=1):
        self.IQparams = IQparams
        self.STEP = STEP
        self.suppression = suppression
        if self.suppression == 'LO':
            self.var = copy.copy(self.IQparams[:2])
            self.step = self.STEP[:2]/(10**(ratio+1))
        elif self.suppression == 'MR':
            self.var = copy.copy(self.IQparams[2:])
            self.step = self.STEP[2:]/(2**(ratio+1))

    def nelder_mead(self, no_improve_thr=10e-6, no_improv_break=10, max_iter=0,
                    alpha=1., gamma=2., rho=-0.5, sigma=0.5, time=0):
        '''
        Pure Python/Numpy implementation of the Nelder-Mead algorithm.
        Reference: https://en.wikipedia.org/wiki/Nelder%E2%80%93Mead_method
        '''
        '''
            @param f (function): function to optimize, must return a scalar score
                and operate over a numpy array of the same dimensions as x_start
            @param x_start (numpy array): initial position
            @param step (float): look-around radius in initial step
            @no_improv_thr,  no_improv_break (float, int): break after no_improv_break iterations with
                an improvement lower than no_improv_thr
            @max_iter (int): always break after this number of iterations.
                Set it to 0 to loop indefinitely.
            @alpha, gamma, rho, sigma (floats): parameters of the algorithm
                (see Wikipedia page for reference)
            return: tuple (best parameter array, best score)
        '''

        index = time%2
        dim = len(self.var)
        "tell AWG to apply DC offset(x) on I & Q"
        AWG_Sinewave(25, self.IQparams)
        "read signal amplitude at LO frequency in and assign it as score"
        MXA.preamp(mxa, action=['Set','OFF'])
        # MXA.preamp_band(mxa, action=['Set','FULL'])
        # MXA.attenuation(mxa, action=['Set','14dB'])
        MXA.attenuation_auto(mxa, action=['Set','ON'])
        power = float((MXA.fpower(mxa, str(5.5 - 0.025*index)+'GHz')).split('dBm')[0]) - index*float((MXA.fpower(mxa, str(5.5 + 0.025*index)+'GHz')).split('dBm')[0])
        prev_best = power
        no_improv = 0
        res = [[self.var, prev_best]]

        # while True:
        #     print("LOPower: %s" %power)
        #     if bool(input('hello')): break

        for i in range(dim):
            x = copy.copy(self.var)
            x[i] = x[i] + self.step[i]
            "tell AWG to apply DC offset(x) on I & Q"
            if self.suppression == 'LO': self.IQparams[:2] = x
            elif self.suppression == 'MR': self.IQparams[2:] = x
            
            AWG_Sinewave(25, self.IQparams)
            "read signal amplitude at LO frequency in and assign it as score"
            power = float((MXA.fpower(mxa, str(5.5 - 0.025*index)+'GHz')).split('dBm')[0]) - index*float((MXA.fpower(mxa, str(5.5 + 0.025*index)+'GHz')).split('dBm')[0])
            score = power
            res.append([x, score])

        # simplex iter
        iters = 0
        while 1:
            # order
            res.sort(key=lambda x: x[1])
            if self.suppression == 'LO': self.IQparams[:2] = res[0][0]
            elif self.suppression == 'MR': self.IQparams[2:] = res[0][0]
            # print(Fore.YELLOW + "\rProgress time#%s: %s" %(time, self.IQparams), end='\r', flush=True)
            best = res[0][1]

            # break after max_iter
            if max_iter and iters >= max_iter:
                return res[0]
            iters += 1

            # AWG_Sinewave(25, self.IQparams)
            # if float((RSA5.fpower(rsa, str(5.5)+'GHz')).split('dBm')[0]) < -65. and float((RSA5.fpower(rsa, str(5.475)+'GHz')).split('dBm')[0]) < -65.:
            #     return array([self.IQparams, best, 0.])

            if best < prev_best - no_improve_thr or best == prev_best:
                no_improv = 0
                prev_best = best
            else:
                no_improv += 1

            if no_improv >= no_improv_break:
                AWG_Sinewave(25, self.IQparams)
                print("Rest at Optimized IQ Settings: %s" %self.IQparams)
                return array([self.IQparams, best]) # Optimized parameters

            # centroid
            x0 = [0.] * dim
            for tup in res[:-1]:
                for i, c in enumerate(tup[0]):
                    x0[i] += c / (len(res)-1)

            # reflection
            xr = x0 + alpha*(x0 - res[-1][0])
            if self.suppression == 'LO': self.IQparams[:2] = xr
            elif self.suppression == 'MR': self.IQparams[2:] = xr
            "tell AWG to apply DC offset(x) on I & Q"
            AWG_Sinewave(25, self.IQparams)
            "read signal amplitude at LO frequency in and assign it as score"
            power = float((MXA.fpower(mxa, str(5.5 - 0.025*index)+'GHz')).split('dBm')[0]) - index*float((MXA.fpower(mxa, str(5.5 + 0.025*index)+'GHz')).split('dBm')[0])
            rscore = power
            if res[0][1] <= rscore < res[-2][1]:
                del res[-1]
                res.append([xr, rscore])
                continue

            # expansion
            if rscore < res[0][1]:
                xe = x0 + gamma*(x0 - res[-1][0])
                if self.suppression == 'LO': self.IQparams[:2] = xe
                elif self.suppression == 'MR': self.IQparams[2:] = xe
                "tell AWG to apply DC offset(x) on I & Q"
                AWG_Sinewave(25, self.IQparams)

                "read signal amplitude at LO frequency in and assign it as score"
                power = float((MXA.fpower(mxa, str(5.5 - 0.025*index)+'GHz')).split('dBm')[0]) - index*float((MXA.fpower(mxa, str(5.5 + 0.025*index)+'GHz')).split('dBm')[0])
                escore = power
                if escore < rscore:
                    del res[-1]
                    res.append([xe, escore])
                    continue
                else:
                    del res[-1]
                    res.append([xr, rscore])
                    continue

            # contraction
            xc = x0 + rho*(x0 - res[-1][0])
            if self.suppression == 'LO': self.IQparams[:2] = xc
            elif self.suppression == 'MR': self.IQparams[2:] = xc
            "tell AWG to apply DC offset(x) on I & Q"
            AWG_Sinewave(25, self.IQparams)

            "read signal amplitude at LO frequency in and assign it as score"
            power = float((MXA.fpower(mxa, str(5.5 - 0.025*index)+'GHz')).split('dBm')[0]) - index*float((MXA.fpower(mxa, str(5.5 + 0.025*index)+'GHz')).split('dBm')[0])
            cscore = power
            if cscore < res[-1][1]:
                del res[-1]
                res.append([xc, cscore])
                continue

            # reduction
            x1 = res[0][0]
            nres = []
            for tup in res:
                redx = x1 + sigma*(tup[0] - x1)
                if self.suppression == 'LO': self.IQparams[:2] = redx
                elif self.suppression == 'MR': self.IQparams[2:] = redx
                "tell AWG to apply DC offset(x) on I & Q"
                AWG_Sinewave(25, self.IQparams)

                "read signal amplitude at LO frequency in and assign it as score"
                power = float((MXA.fpower(mxa, str(5.5 - 0.025*index)+'GHz')).split('dBm')[0]) - index*float((MXA.fpower(mxa, str(5.5 + 0.025*index)+'GHz')).split('dBm')[0])
                score = power
                nres.append([redx, score])
            res = nres


if __name__ == "__main__":

    LO_0 = float((MXA.fpower(mxa, str(5.5)+'GHz')).split('dBm')[0])
    Mirror_0 = float((MXA.fpower(mxa, str(5.475)+'GHz')).split('dBm')[0])
    Initial = [0., 0., 1., 0., 0.]
    time = 0
    OPT = IQ_Cal()
    OPT.IQparams = array(Initial,dtype=float64) #overwrite initial values  
    result = OPT.nelder_mead(time = time)
    prev = result[0]
    no_improv, no_improv_thr, no_improv_break = 0, 1e-5, 6
    LO, Mirror, T = [], [], []
    while True:
        time += 1
        if time%2: OPT = IQ_Cal('MR',result[0], ratio = time)
        else: OPT = IQ_Cal('LO',result[0], ratio = time)
        result = OPT.nelder_mead(time = time)
        # if len(result) == 3:
        #     print("Optimized IQ parameters:\n %s" %result)
        #     break
        LO.append(float((MXA.fpower(mxa, str(5.5)+'GHz')).split('dBm')[0]) - LO_0)
        Mirror.append(float((MXA.fpower(mxa, str(5.475)+'GHz')).split('dBm')[0]) - Mirror_0)
        print(Back.BLUE + Fore.WHITE + "Mirror has been suppressed for %s from %s" %(Mirror[-1],Mirror_0))
        T.append(time)
        ssq = sum((result[0] - prev)**2)
        if ssq > no_improv_thr:
            no_improv = 0
            prev = result[0]
        else:
            no_improv += 1

        if no_improv >= no_improv_break:
            AWG_Sinewave(25, OPT.IQparams)
            print(type(OPT.IQparams))
            print("Optimized IQ parameters:\n %s" %result)
            print("Amplitude Imbalance:\n %s" %OPT.IQparams[2])
            if OPT.IQparams[3] > OPT.IQparams[4] and OPT.IQparams[3]-OPT.IQparams[4] < 180:
                print("phase skew I-Q:\n %s" %(OPT.IQparams[3]-OPT.IQparams[4]))
            if OPT.IQparams[3] > OPT.IQparams[4] and OPT.IQparams[3]-OPT.IQparams[4] > 180:
                print("phase skew Q-I:\n %s" %(360-(OPT.IQparams[3]-OPT.IQparams[4])))
            if (OPT.IQparams[4] > OPT.IQparams[3] and OPT.IQparams[4]-OPT.IQparams[3] < 180) or (OPT.IQparams[3] > OPT.IQparams[4] and OPT.IQparams[3]-OPT.IQparams[4] > 180):
                print("phase skew Q-I:\n %s" %(OPT.IQparams[4]-OPT.IQparams[3]))
            
            if (OPT.IQparams[2] > -1.0) and (OPT.IQparams[2] < 1.0):
                Iamp = 1
                Qamp = Iamp * OPT.IQparams[2]
            else:
                Qamp = 1
                Iamp = Qamp/OPT.IQparams[2]
            
            print("Ioffset:\n %s" %OPT.IQparams[0])
            print("Qoffset:\n %s" %OPT.IQparams[1])
            print("Iamp:\n %s" %Iamp)
            print("Qamp:\n %s" %Qamp)
            print("Iphase:\n %s" %OPT.IQparams[3])
            print("Qphase:\n %s" %OPT.IQparams[4])

            break

        
    curve(T,LO,'LO Leakage vs time','T(#)','DLO(dB)')
    curve(T,Mirror,'Mirror Image vs time','T(#)','DMirror(dB)')

# closing instruments:
ans = input("Press any keys to close AWG, PSGA and RSA-5 ")
AWG.Abort_Gen(awgsess)
AWG.close(awgsess)
PSGA.rfoutput(saga, action=['Set', 0])
PSGA.close(saga, False)
MXA.close(mxa,False)



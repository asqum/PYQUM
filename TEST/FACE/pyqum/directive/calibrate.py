"""
Created on Wed Jan 15 11:17:10 2020
@author: mesch
@co-author: LTH
"""

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

import copy
from pyqum.instrument.benchtop import MXA
from pyqum.instrument.benchtop import PSGA
from pyqum.instrument.benchtop import TKAWG as DAC
from pyqum.instrument.logger import status_code, get_status, set_status, clocker
from pyqum.instrument.analyzer import curve
from pyqum.instrument.composer import pulser
from numpy import sin, cos, pi, array, float64, sum, dot  
from time import sleep

# Instrument acting on feedback:
# 1. DAC taking feedback from Optimization loop:
def Update_DAC(daca, ifreq, IQparams, IF_period, mixer_module='xy1', scale=0.1):
    '''
    ifreq: IF frequency in MHz
    mixer_module: name given to each modules in a mixer box.
    '''
    Ioffset, Qoffset, ampratio, Iphase, Qphase = IQparams

    if (ampratio > -1.0) and (ampratio < 1.0): 
        Iamp = 1
        Qamp = Iamp * ampratio
    else: 
        Qamp = 1
        Iamp = Qamp/ampratio

    IF_period, ifreq = int(IF_period), int(ifreq*1000)

    # Saving settings
    mix_dict, SCORE_DEFINED = {}, {}
    mix_dict["xy1i%s" %ifreq] = "%s/%s/%s" %(Iamp,Iphase,Ioffset)
    mix_dict["xy1q%s" %ifreq] = "%s/%s/%s" %(Qamp,Qphase,Qoffset)
    set_status("MIXER", mix_dict)
    # Translate into SCORE:
    SCORE_DEFINED['CH3'] = "ns=%s,mhz=I/%s/%si%s;FLAT/,%s,%s;" %(IF_period,ifreq,mixer_module,ifreq,IF_period,scale)
    SCORE_DEFINED['CH4'] = "ns=%s,mhz=Q/%s/%sq%s;FLAT/,%s,%s;" %(IF_period,ifreq,mixer_module,ifreq,IF_period,scale)
    
    # Update DAC
    for ch in range(2):
        channel = str(ch + 3)
        dt = round(1/float(DAC.clock(daca)[1]['SRATe'])/1e-9, 2)
        pulseq = pulser(dt=dt, clock_multiples=1, score=SCORE_DEFINED['CH%s'%channel])
        pulseq.song()
        DAC.compose_DAC(daca, int(channel), pulseq.music, 1) # route marker from RO-channel-I to trigger digitizer
    DAC.ready(daca)
    sleep(0.73) # wait for trigger to complete MXA measurement

# 2. Prepare MXA accordingly:
def SA_Setup(mxa, center_freq_GHz, fspan_MHz=1e-3, BW_Hz=1000, points=7):
    MXA.sweepoint(mxa, action=['Set', '%s'%points])
    MXA.frequency(mxa, action=['Set','%sGHz' %(center_freq_GHz)])
    MXA.fspan(mxa, action=['Set','%sMHz'%fspan_MHz])
    MXA.rbw(mxa, action=['Set','%sHz'%BW_Hz])
    MXA.vbw(mxa, action=['Set','%sHz'%(BW_Hz/10)])
    power = MXA.fpower(mxa, center_freq_GHz)
    # print("Power at %sGHz is %sdBm" %(center_freq_GHz, power))
    return power


class IQ_Cal:

    def __init__(self, Conv_freq, LO_powa, IF_freq, IF_period, mixer_module):
        '''
        Initialize relevant instruments:
        Conv_freq: Converted frequency in GHz (aka Target frequency)
        LO_freq: LO frequency in GHz
        LO_powa: LO power in dBm
        IF_freq: IF frequency in GHz
        '''

        self.LO_freq, self.LO_powa, self.IF_freq, self.IF_period, self.mixer_module = Conv_freq - IF_freq, LO_powa, IF_freq, IF_period, mixer_module

        # PSGA
        self.saga = PSGA.Initiate(1, mode="TEST")
        PSGA.rfoutput(self.saga, action=['Set', 1])
        PSGA.frequency(self.saga, action=['Set', "%sGHz" %self.LO_freq])
        PSGA.power(self.saga, action=['Set', "%sdBm" %LO_powa])
        # DAC:
        self.daca = DAC.Initiate(which=1, mode="TEST")
        DAC.clock(self.daca, action=['Set', 'EFIXed',2.5e9])
        DAC.clear_waveform(self.daca,'all')
        DAC.alloff(self.daca, action=['Set',1])
        '''Prepare DAC:'''
        dt = round(1/float(DAC.clock(self.daca)[1]['SRATe'])/1e-9, 2)
        pulseq = pulser(dt=dt, clock_multiples=1, score="ns=%s"%IF_period)
        pulseq.song()
        for ch in range(4):
            channel = str(ch + 1)
            DAC.prepare_DAC(self.daca, channel, pulseq.totalpoints)
        for ch in range(4):
            channel = str(ch + 1)
            DAC.compose_DAC(self.daca, channel, pulseq.music) # we don't need marker yet initially
        # Turn on all 4 channels:
        DAC.alloff(self.daca, action=['Set',0])
        DAC.ready(self.daca)
        DAC.play(self.daca)
        # SA
        self.mxa = MXA.Initiate()
        SA_Setup(self.mxa, self.LO_freq, fspan_MHz=self.IF_freq*1000*3, BW_Hz=1e6, points=int(self.IF_freq*1e9*3/1e6*2))
        MXA.trigger_source(self.mxa, action=['Set','EXTernal1'])
        sleep(3)

    def settings(self, suppression='LO', STEP=array([-0.5,-0.5,0.5,12,12]), logratio=1):
        try:
            # load previous half-way calibrated results and resume:
            Iamp, Iphase, Ioffset = [float(x) for x in get_status("MIXER")["%si%s" %(self.mixer_module, int(self.IF_freq*1000))].split("/")]
            Qamp, Qphase, Qoffset = [float(x) for x in get_status("MIXER")["%sq%s" %(self.mixer_module, int(self.IF_freq*1000))].split("/")]
            IQparams = array([Ioffset, Qoffset, Qamp/Iamp, Iphase, Qphase])
        except:
            # defaults:
            IQparams=array([0.,0.,1.,0.,0.])

        self.IQparams = IQparams
        self.STEP = STEP
        self.suppression = suppression
        if self.suppression == 'LO':
            self.var = copy.copy(self.IQparams[:2])
            self.step = self.STEP[:2]/(10**(logratio+1))
        elif self.suppression == 'MR':
            self.var = copy.copy(self.IQparams[2:])
            self.step = self.STEP[2:]/(2**(logratio+1))

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
        Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.mixer_module)
        "read signal amplitude at LO frequency in and assign it as score"
        MXA.preamp(self.mxa, action=['Set','OFF'])
        # MXA.attenuation(mxa, action=['Set','14dB'])
        MXA.attenuation_auto(self.mxa, action=['Set','ON'])
        power = MXA.fpower(self.mxa, self.LO_freq-self.IF_freq*index) - index*MXA.fpower(self.mxa, self.LO_freq+self.IF_freq*index)
        # print("power: %s" %power)
        prev_best = power
        no_improv = 0
        res = [[self.var, prev_best]]

        for i in range(dim):
            x = copy.copy(self.var)
            x[i] = x[i] + self.step[i]
            "tell AWG to apply DC offset(x) on I & Q"
            if self.suppression == 'LO': self.IQparams[:2] = x
            elif self.suppression == 'MR': self.IQparams[2:] = x
            
            Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.mixer_module)
            "read signal amplitude at LO frequency in and assign it as score"
            power = MXA.fpower(self.mxa, self.LO_freq-self.IF_freq*index) - index*MXA.fpower(self.mxa, self.LO_freq+self.IF_freq*index)
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

            if best < prev_best - no_improve_thr or best == prev_best:
                no_improv = 0
                prev_best = best
            else:
                no_improv += 1

            if no_improv >= no_improv_break:
                Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.mixer_module)
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
            Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.mixer_module)
            "read signal amplitude at LO frequency in and assign it as score"
            power = MXA.fpower(self.mxa, self.LO_freq-self.IF_freq*index) - index*MXA.fpower(self.mxa, self.LO_freq+self.IF_freq*index)
            print("reflection cost: %s" %power)
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
                Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.mixer_module)
                "read signal amplitude at LO frequency in and assign it as score"
                power = MXA.fpower(self.mxa, self.LO_freq-self.IF_freq*index) - index*MXA.fpower(self.mxa, self.LO_freq+self.IF_freq*index)
                # print("expansion cost: %s" %power)
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
            Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.mixer_module)
            "read signal amplitude at LO frequency in and assign it as score"
            power = MXA.fpower(self.mxa, self.LO_freq-self.IF_freq*index) - index*MXA.fpower(self.mxa, self.LO_freq+self.IF_freq*index)
            # print("contraction cost: %s" %power)
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
                Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.mixer_module)
                "read signal amplitude at LO frequency in and assign it as score"
                power = MXA.fpower(self.mxa, self.LO_freq-self.IF_freq*index) - index*MXA.fpower(self.mxa, self.LO_freq+self.IF_freq*index)
                print("reduction costs: %s" %power)
                score = power
                nres.append([redx, score])
            res = nres

    # start optimization:
    def run(self):
        self.LO_Initial = MXA.fpower(self.mxa, self.LO_freq)
        self.Mirror_Initial = MXA.fpower(self.mxa, self.LO_freq-self.IF_freq)
        self.settings()
        result = self.nelder_mead()
        prev = result[0]
        no_improv, no_improv_thr, no_improv_break = 0, 1e-5, 6
        time, LO, Mirror, T = 0, [], [], []
        # Check LO & Mirror alternatively:
        while True:
            time += 1
            if time%2: 
                print(Fore.YELLOW + "Minimizing MIRROR LEAKAGE")
                self.settings('MR',result[0], logratio = time)
            else: 
                print(Fore.YELLOW + "Minimizing CARRIER FEEDTHROUGH")
                self.settings('LO',result[0], logratio = time)
            result = self.nelder_mead(time = time)
            
            LO.append(MXA.fpower(self.mxa, self.LO_freq)-self.LO_Initial)
            print(Back.BLUE + Fore.WHITE + "LO has been suppressed for %sdB from %sdBm" %(LO[-1],self.LO_Initial))
            Mirror.append(MXA.fpower(self.mxa, self.LO_freq-self.IF_freq) - self.Mirror_Initial)
            print(Back.BLUE + Fore.WHITE + "Mirror has been suppressed for %sdB from %sdBm" %(Mirror[-1],self.Mirror_Initial))
            # Display different stages' optimization results:
            Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.mixer_module)
            sleep(7)
            
            T.append(time)
            ssq = sum((result[0] - prev)**2)
            if ssq > no_improv_thr:
                no_improv = 0
                prev = result[0]
            else:
                no_improv += 1

            if no_improv >= no_improv_break:
                print("Calibration completed!")

                # display on instruments and save the final optimized parameters:
                Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.mixer_module)
                
                print(type(self.IQparams))
                print("Optimized IQ parameters:\n %s" %result)
                print("Amplitude Imbalance:\n %s" %self.IQparams[2])
                if self.IQparams[3] > self.IQparams[4] and self.IQparams[3]-self.IQparams[4] < 180:
                    print("phase skew I-Q:\n %s" %(self.IQparams[3]-self.IQparams[4]))
                if self.IQparams[3] > self.IQparams[4] and self.IQparams[3]-self.IQparams[4] > 180:
                    print("phase skew Q-I:\n %s" %(360-(self.IQparams[3]-self.IQparams[4])))
                if (self.IQparams[4] > self.IQparams[3] and self.IQparams[4]-self.IQparams[3] < 180) or (self.IQparams[3] > self.IQparams[4] and self.IQparams[3]-self.IQparams[4] > 180):
                    print("phase skew Q-I:\n %s" %(self.IQparams[4]-self.IQparams[3]))
                
                if (self.IQparams[2] > -1.0) and (self.IQparams[2] < 1.0):
                    Iamp = 1
                    Qamp = Iamp * self.IQparams[2]
                else:
                    Qamp = 1
                    Iamp = Qamp/self.IQparams[2]
                
                print("Ioffset:\n %s" %self.IQparams[0])
                print("Qoffset:\n %s" %self.IQparams[1])
                print("Iamp:\n %s" %Iamp)
                print("Qamp:\n %s" %Qamp)
                print("Iphase:\n %s" %self.IQparams[3])
                print("Qphase:\n %s" %self.IQparams[4])

                break

            
        # curve(T,LO,'LO Leakage vs time','T(#)','DLO(dB)')
        # curve(T,Mirror,'Mirror Image vs time','T(#)','DMirror(dB)')

    def close(self):
        '''closing instruments:
        '''
        DAC.alloff(self.daca, action=['Set',1])
        DAC.close(self.daca, which=1, mode="TEST")
        PSGA.rfoutput(self.saga, action=['Set', 0])
        PSGA.close(self.saga, 1, False, mode="TEST")
        MXA.close(self.mxa, False)

def test():
    s, t = clocker("IQ-CAL")
    # ===============================================================
    C = IQ_Cal(4.06, 16, 0.077, 100000, 'xy1')
    C.run()
    # ===============================================================
    clocker("IQ-CAL", s, t)
    ans = input("Press any keys to close AWG, PSGA and RSA-5 ")
    C.close()

test()

"""
Created on Wed Jan 15 11:17:10 2020
@author: mesch
@co-author: LTH
"""

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

import copy
from pyqum.instrument.benchtop import MXA
from pyqum.instrument.benchtop import PSGA as PSG # RO: V, XY: A
from pyqum.instrument.benchtop import TKAWG as DAC
from pyqum.instrument.logger import status_code, get_status, set_status, clocker
from pyqum.instrument.analyzer import curve
from pyqum.instrument.composer import pulser
from numpy import sin, cos, pi, array, float64, sum, dot, log10  
from time import sleep

# Instrument acting on feedback:
# 1. DAC taking feedback from Optimization loop:
def Update_DAC(daca, ifreq, IQparams, IF_period, IF_scale, mixer_module, channels_group):
    '''
    Update DAC on the fly.
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

    IF_period = int(IF_period)
    ifreq = round(ifreq, 1) # allow down to 100kHz of IFB, hence 10us integration-time max.

    # Saving settings
    mix_dict, SCORE_DEFINED = {}, {}
    mix_dict["%si%s" %(mixer_module, ifreq)] = "%s/%s/%s" %(Iamp,Iphase,Ioffset)
    mix_dict["%sq%s" %(mixer_module, ifreq)] = "%s/%s/%s" %(Qamp,Qphase,Qoffset)
    set_status("MIXER", mix_dict)
    # Translate into SCORE:
    SCORE_DEFINED['CH%s' %(channels_group)] = "ns=%s,mhz=I/%s/%si%s;FLAT/,%s,%s;" %(IF_period,abs(ifreq),mixer_module,ifreq,IF_period,IF_scale) # IF carrier should always be +ve
    SCORE_DEFINED['CH%s' %(channels_group+1)] = "ns=%s,mhz=Q/%s/%sq%s;FLAT/,%s,%s;" %(IF_period,abs(ifreq),mixer_module,ifreq,IF_period,IF_scale)
    
    # Update DAC
    for ch in range(2):
        channel = str(ch + channels_group)
        dt = round(1/float(DAC.clock(daca)[1]['SRATe'])/1e-9, 2)
        pulseq = pulser(dt=dt, clock_multiples=1, score=SCORE_DEFINED['CH%s'%channel])
        pulseq.song()
        DAC.compose_DAC(daca, int(channel), pulseq.music, pulseq.envelope, 2) # ODD for PIN-SWITCH, EVEN for TRIGGER; RO-TRIGGER: 1: ALZDG, 2: MXA; XY-TRIGGER: 1: MXA, 2: SCOPE
    DAC.ready(daca)
    sleep(0.73) # wait for trigger to complete MXA measurement

    return (SCORE_DEFINED['CH%s' %(channels_group)], SCORE_DEFINED['CH%s' %(channels_group+1)])

# 2. Prepare MXA accordingly:
def SA_Setup(mxa, center_freq_GHz, fspan_MHz=1e-3, BW_Hz=1000, points=7):
    MXA.sweepoint(mxa, action=['Set', '%s'%points])
    MXA.frequency(mxa, action=['Set','%sGHz' %(center_freq_GHz)])
    MXA.fspan(mxa, action=['Set','%sMHz'%fspan_MHz])
    MXA.rbw(mxa, action=['Set','%sHz'%BW_Hz])
    MXA.vbw(mxa, action=['Set','%sHz'%(BW_Hz/10)])
    power = MXA.fpower(mxa, center_freq_GHz)
    print("Power at %sGHz is %sdBm" %(center_freq_GHz, power))
    return power

# 3. Obtain the cost function for each cases:
def Cost(index, mxa, leakage_freq, Conv_freq):
    '''
    Calculate COST in terms of suppression or isolation
    '''
    if index == 0:
        isolation = MXA.fpower(mxa, leakage_freq[index]) - MXA.fpower(mxa, Conv_freq)
    else:
        isolation = 0
        for i in range(len(leakage_freq[index])):
            isolation += MXA.fpower(mxa, leakage_freq[index][i]) - MXA.fpower(mxa, Conv_freq)
        isolation = isolation / len(leakage_freq[index])

    return isolation


class IQ_Cal:

    def __init__(self, Conv_freq, LO_powa, IF_freq, IF_period, IF_scale, mixer_module):
        '''
        Initialize relevant instruments:
        Conv_freq: Converted frequency in GHz (aka Target frequency)
        LO_freq: LO frequency in GHz
        LO_powa: LO power in dBm
        IF_freq: IF frequency in MHz
        IF_period: IF pulse period in ns
        '''

        # Carrier LO:
        self.LO_freq = Conv_freq - IF_freq/1000
        # Mirror Images: 1st, 2nd, 3rd, 4th
        self.MR_freq = [Conv_freq - 2 * IF_freq/1000, Conv_freq + IF_freq/1000, Conv_freq - 3 * IF_freq/1000, Conv_freq + 2 * IF_freq/1000]
        self.Conv_freq, self.leakage_freq = Conv_freq, [self.LO_freq, self.MR_freq]
        

        
        self.LO_powa, self.IF_freq, self.IF_period, self.IF_scale, self.mixer_module = LO_powa, IF_freq, IF_period, IF_scale, mixer_module

        if "xy" in mixer_module: self.channels_group = 3
        elif "ro" in mixer_module: self.channels_group = 1

        # 1. PSG
        self.saga = PSG.Initiate(2, mode="TEST")
        PSG.rfoutput(self.saga, action=['Set', 1])
        PSG.frequency(self.saga, action=['Set', "%sGHz" %self.LO_freq])
        PSG.power(self.saga, action=['Set', "%sdBm" %LO_powa])
        
        # 2. DAC:
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
        
        # 3. SA
        self.mxa = MXA.Initiate()
        fspan_MHz = abs(self.IF_freq)*7 # SPAN MUST INCLUDE ALL PEAKS
        BW_Hz = fspan_MHz*1e6 / 100
        points = 1000
        SA_Setup(self.mxa, self.LO_freq, fspan_MHz=fspan_MHz, BW_Hz=BW_Hz, points=points)
        MXA.trigger_source(self.mxa, action=['Set','EXTernal1'])
        sleep(3)

    def settings(self, suppression='LO', STEP=array([-0.5,-0.5,0.5,12,12]), logratio=1):
        try:
            # load previous half-way calibrated results and resume:
            Iamp, Iphase, Ioffset = [float(x) for x in get_status("MIXER")["%si%s" %(self.mixer_module, round(self.IF_freq, 1))].split("/")]
            Qamp, Qphase, Qoffset = [float(x) for x in get_status("MIXER")["%sq%s" %(self.mixer_module, round(self.IF_freq, 1))].split("/")]
            IQparams = array([Ioffset, Qoffset, Qamp/Iamp, Iphase, Qphase])
        except:
            # defaults:
            print(Fore.CYAN + "Fresh Calibration: Loading Defaults")
            IQparams=array([0.,0.,1.,0.,0.])

        self.IQparams = IQparams
        self.STEP = STEP
        self.suppression = suppression
        if self.suppression == 'LO':
            self.var = copy.copy(self.IQparams[:2])
            self.step = self.STEP[:2]/(10**(logratio+1))
            print(Fore.CYAN + "Every Step for LO leakage minimization: %s" %self.step)
        elif self.suppression == 'MR':
            self.var = copy.copy(self.IQparams[2:])
            self.step = self.STEP[2:]/(2**(logratio+1))
            print(Fore.CYAN + "Every Step for MR leakage minimization: %s" %self.step)
        
        # Pre-play Pre-Calibrated Modulation:
        pulsettings = Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.IF_scale, self.mixer_module, self.channels_group)
        if logratio==1: print(Fore.BLUE + str(pulsettings))

    def nelder_mead(self, no_improve_thr=1e-4, no_improv_break=3, max_iter=0,
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

        index = time%2 # only 0 & 1
        dim = len(self.var)
        # PENDING: OPTION to PreAmp
        # MXA.preamp(self.mxa, action=['Set','ON'])
        # MXA.attenuation(self.mxa, action=['Set','24dB'])
        # MXA.attenuation_auto(self.mxa, action=['Set','ON'])
        power = MXA.fpower(self.mxa, self.leakage_freq[index]) - MXA.fpower(self.mxa, self.Conv_freq)
        prev_best = power
        no_improv = 0
        res = [[self.var, prev_best]]

        for i in range(dim):
            x = copy.copy(self.var)
            x[i] = x[i] + self.step[i]
            if self.suppression == 'LO': self.IQparams[:2] = x # adjusting IQ offsets
            elif self.suppression == 'MR': self.IQparams[2:] = x # adjusting IQ amplitudes' & phases' balances
            Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.IF_scale, self.mixer_module, self.channels_group)
            score = Cost(index, self.mxa, self.leakage_freq, self.Conv_freq)
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
                Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.IF_scale, self.mixer_module, self.channels_group)
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
            Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.IF_scale, self.mixer_module, self.channels_group)
            rscore = Cost(index, self.mxa, self.leakage_freq, self.Conv_freq)
            if res[0][1] <= rscore < res[-2][1]:
                del res[-1]
                res.append([xr, rscore])
                continue

            # expansion
            if rscore < res[0][1]:
                xe = x0 + gamma*(x0 - res[-1][0])
                if self.suppression == 'LO': self.IQparams[:2] = xe
                elif self.suppression == 'MR': self.IQparams[2:] = xe
                Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.IF_scale, self.mixer_module, self.channels_group)
                escore = Cost(index, self.mxa, self.leakage_freq, self.Conv_freq)
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
            Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.IF_scale, self.mixer_module, self.channels_group)
            cscore = Cost(index, self.mxa, self.leakage_freq, self.Conv_freq)
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
                Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.IF_scale, self.mixer_module, self.channels_group)
                score = Cost(index, self.mxa, self.leakage_freq, self.Conv_freq)
                print("reduction costs: %s" %score)
                nres.append([redx, score])
            res = nres

    # start optimization:
    def run(self, no_improve_thr=1e-3, no_improv_break=2):
        print(Back.WHITE + Fore.RED + "Background LO-leakage: %s\nBackground MR-leakage: %s\n" %(MXA.fpower(self.mxa, self.LO_freq), MXA.fpower(self.mxa, self.MR_freq)))
        input("PROCEED? (y/n) ")

        print(Fore.YELLOW + "Initial LO")
        self.settings('LO')
        self.LO_Initial, self.MR_Initial = MXA.fpower(self.mxa, self.LO_freq), MXA.fpower(self.mxa, self.MR_freq[0])
        print(Back.WHITE + Fore.RED + "Initial LO-leakage: %s\nInitial 1st-MR-leakage: %s\n" %(self.LO_Initial, self.MR_Initial))
        if input("PROCEED? (y/n) ").lower()=='n': return
        result = self.nelder_mead(no_improve_thr=no_improve_thr, no_improv_break=no_improv_break)

        prev = result[0]
        print(Fore.YELLOW + "PREVIOUS STEPS: %s" %prev)
        no_improv, no_improv_thr, no_improv_break = 0, 1e-5, 6
        time, LO, Mirror, T = 0, [], [], []

        # Check LO & Mirror alternatively:
        while True:
            time += 1
            if time == 1:
                print(Fore.YELLOW + "Initial MR")
                self.settings('MR')
            elif time%2: 
                print(Fore.YELLOW + "Minimizing MIRROR LEAKAGE #%s" %time)
                self.settings('MR',result[0], logratio = time)
            else: 
                print(Fore.YELLOW + "Minimizing CARRIER FEEDTHROUGH #%s" %time)
                self.settings('LO',result[0], logratio = time)
            result = self.nelder_mead(no_improve_thr=no_improve_thr, no_improv_break=no_improv_break, time=time)
            
            LO.append(MXA.fpower(self.mxa, self.LO_freq)-self.LO_Initial)
            print(Back.BLUE + Fore.WHITE + "LO has been suppressed for %sdB from %sdBm" %(LO[-1],self.LO_Initial))
            Mirror.append(MXA.fpower(self.mxa, self.MR_freq) - self.MR_Initial)
            print(Back.BLUE + Fore.WHITE + "Mirror has been suppressed for %sdB from %sdBm" %(Mirror[-1],self.MR_Initial))
            # Display different stages' optimization results:
            Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.IF_scale, self.mixer_module, self.channels_group)
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
                Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.IF_scale, self.mixer_module, self.channels_group)
                
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
        PSG.rfoutput(self.saga, action=['Set', 0])
        PSG.close(self.saga, 1, False, mode="TEST")
        MXA.close(self.mxa, False)

def test():
    s, t = clocker(agenda="IQ-CAL")
    # ===============================================================
    C = IQ_Cal(5.6, 19, -75, 120000, 0.6, 'xy1') # Conv_freq (GHz), LO_powa (dBm), IF_freq (MHz), IF_period (ns), IF_scale, mixer_module
    C.run()
    # ===============================================================
    clocker(s, t, agenda="IQ-CAL")
    input("Press any keys to close AWG, PSG and RSA-5 ")
    C.close()

# test()
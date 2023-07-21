"""
Created on Wed Jan 15 11:17:10 2020
@author: mesch
@co-author: LTH
"""

from colorama import init, Fore, Back
from pyqum.instrument.toolbox import waveform
# init(autoreset=True) #to convert termcolor to wins color
from importlib import import_module as im
import copy
#from pyqum.directive.Mixer import calibration
from pyqum.instrument.logger import status_code, get_status, set_status, clocker
# from pyqum.instrument.analyzer import curve
from pyqum.instrument.composer import pulser
from scipy.optimize import curve_fit
from numpy import sin, cos, pi, array, float64, sum, dot, log10, linspace, min, argmin
from time import time, sleep
import matplotlib.pyplot as plt

def target_function(x, a, b, c):
    return a*x**2 + b*x + c

# def find_minimum(x,y):
#     popt, pcov = curve_fit(
#         f=target_function,         # model function
#         xdata=x,    # x data
#         ydata=y,     # y data
#         p0=(1,1,1),    # initial value of the parameters
#     )
#     minimum = -popt[1]/2/popt[0]
#     return minimum

def find_minimum(x,y):
    min_idx = argmin(y)
    if min_idx == 0 or min_idx == len(y)-1:
        minimum = x[argmin(y)]
    else:
        minL_idx = min_idx-1
        minR_idx = min_idx+1
        dyL = y[minL_idx]-y[min_idx]
        dyR = y[minR_idx]-y[min_idx]
        nor_dyL = dyL/(dyL+dyR)
        nor_dyR = dyR/(dyL+dyR)
        dx = (x[minR_idx]-x[minL_idx])/2
        print(f"dx {dx}")
        print(f"Shift {(dx*dyR -dx*dyL)}")
        minimum = x[argmin(y)]+(dx*nor_dyL -dx*nor_dyR)
    return minimum

# Instrument acting on feedback:
# 1. DAC taking feedback from Optimization loop:
def Update_DAC(daca, ifreq, IQparams, IF_period, IF_scale, mixer_module, channels_group, marker):
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
    SCORE_DEFINED['CH%s' %(channels_group)] = "ns=%s,mhz=I/%s/%si%s;FLAT/,%s,%s;" %(IF_period,ifreq,mixer_module,ifreq,IF_period,IF_scale) # PENDING: make IF relative
    SCORE_DEFINED['CH%s' %(channels_group+1)] = "ns=%s,mhz=Q/%s/%sq%s;FLAT/,%s,%s;" %(IF_period,ifreq,mixer_module,ifreq,IF_period,IF_scale)
    
    # Update DAC
    for ch in range(2):
        channel = str(ch + channels_group)
        dt = round(1/float(DAC.clock(daca)[1]['SRATe'])/1e-9, 2)
        pulseq = pulser(dt=dt, clock_multiples=1, score=SCORE_DEFINED['CH%s'%channel])
        pulseq.song()

        DAC.compose_DAC(daca, int(channel), pulseq.music, pulseq.envelope, marker, dict(PINSW=False)) # ODD for PIN-SWITCH, EVEN for TRIGGER; RO-TRIGGER: 1: ALZDG, 2: MXA; XY-TRIGGER: 1: MXA, 2: SCOPE
    DAC.ready(daca)
    sleep(0.73) # wait for trigger to complete MXA measurement

    return (SCORE_DEFINED['CH%s' %(channels_group)], SCORE_DEFINED['CH%s' %(channels_group+1)])

# 2. Prepare MXA accordingly:
def SA_Setup(mxa, center_freq_GHz, fspan_MHz=1e-3, BW_Hz=1000, points=7):
    SA.sweepSA(mxa, action=['Set', '%s'%points])
    SA.fcenter(mxa, action=['Set','%sGHz' %(center_freq_GHz)])
    SA.fspan(mxa, action=['Set','%sMHz'%fspan_MHz])
    SA.rbw(mxa, action=['Set','%sHz'%BW_Hz])
    SA.vbw(mxa, action=['Set','%sHz'%(BW_Hz/10)])
    SA.autoscal(mxa, 0)
    power = SA.mark_power(mxa, center_freq_GHz)[0]
    print("Power at %sGHz is %sdBm" %(center_freq_GHz, power))
    return power

class IQ_Calibrate:

    def __init__(self, Conv_freq, LO_powa, IF_freq, IF_period, IF_scale, mixer_module, iqcal_config=dict(SG='PSGA_1',DA='TKAWG_1',SA='MXA_1'), channels_group=1,\
        range_phai=20, range_a=0.1, range_I=0.2, range_Q=0.2, step_rate=0.6, LOstop=-50, MRstop=-50):
        '''
        The calibration is based on the mixer mechanism.
        Initialize relevant instruments:
        Conv_freq: Converted frequency in GHz (aka Target frequency)
        LO_freq: LO frequency in GHz
        LO_powa: LO power in dBm
        IF_freq: IF frequency in MHz
        IF_period: IF pulse period in ns
        mixer_module = 'xy3' for example
        '''
        global SG, DAC, SA
        self.mode = mixer_module[:2].upper()
        # Wiring configurations:
        if 'SDAWG' in iqcal_config['DA']: iqcal_config.update(dict(XY={'marker':0, 'trigger':1}, RO={'marker':0, 'trigger':2})) # dict(XY={'marker':7, 'trigger':1}, RO={'marker':7, 'trigger':2})
        elif 'TKAWG' in iqcal_config['DA']: iqcal_config.update(dict(XY={'marker':1, 'trigger':1}, RO={'marker':2, 'trigger':2}))
        self.iqcal_config = iqcal_config
        # Carrier LO:
        self.LO_freq = Conv_freq - IF_freq/1000
        self.MR_freq = Conv_freq - 2 * IF_freq/1000 
        self.Conv_freq, self.leakage_freq = Conv_freq, [self.LO_freq, self.MR_freq]
        self.range_phai, self.range_a, self.range_I, self.range_Q = range_phai, range_a, range_I, range_Q
        self.step_rate, self.LOstop, self.MRstop = step_rate, LOstop, MRstop
        self.LO_powa, self.IF_freq, self.IF_period, self.IF_scale, self.mixer_module = LO_powa, IF_freq, IF_period, IF_scale, mixer_module
        self.channels_group = channels_group
        # if "xy" in mixer_module: self.channels_group = 3
        # elif "ro" in mixer_module: self.channels_group = 1

        # 1. PSG (RO:PSGV_1 XY:PSGA_2)
        LO_type, self.LO_label = iqcal_config['SG'].split("_")
        SG = im("pyqum.instrument.machine.%s" %LO_type)
        self.saga = SG.Initiate(which=self.LO_label)
        SG.rfoutput(self.saga, action=['Set', 1])
        SG.frequency(self.saga, action=['Set', "%sGHz" %self.LO_freq])
        SG.power(self.saga, action=['Set', "%sdBm" %LO_powa])
        
        # 2. DAC:
        DA_type, self.DA_label = iqcal_config['DA'].split("_")
        DAC = im("pyqum.instrument.machine.%s" %DA_type)
        self.daca = DAC.Initiate(which=self.DA_label)
        if "TKAWG" in DA_type: CLOCK_HZ = 2.5e9
        elif "SDAWG" in DA_type: CLOCK_HZ = 1e9
        else: pass
        DAC.clock(self.daca, action=['Set', 'EFIXed', CLOCK_HZ])
        DAC.clear_waveform(self.daca,'all')
        DAC.alloff(self.daca, action=['Set',1])
        '''Prepare DAC:'''
        dt = round(1/float(DAC.clock(self.daca)[1]['SRATe'])/1e-9, 2)
        pulseq = pulser(dt=dt, clock_multiples=1, score="ns=%s"%IF_period)
        pulseq.song()
        for ch in range(2):
            channel = int(ch + channels_group)
            DAC.prepare_DAC(self.daca, channel, pulseq.totalpoints, update_settings=dict(Master=True, trigbyPXI=2)) # First-in-line = Master)
        for ch in range(2):
            channel = int(ch + channels_group)
            # PENDING: AVOID HAVING "MARKER=7" TWICE: IT WILL HAVE RESEND ERROR POPPING UP!
            DAC.compose_DAC(self.daca, channel, pulseq.music, pulseq.envelope, self.iqcal_config[self.mode]['marker'], dict(PINSW=False)) # we don't need marker yet initially
        # Turn on all 4 channels:
        DAC.alloff(self.daca, action=['Set',0])
        DAC.ready(self.daca)
        DAC.play(self.daca)
        
        # 3. SA
        SA_type, self.SA_label = iqcal_config['SA'].split("_")
        SA = im("pyqum.instrument.machine.%s" %SA_type)
        self.mxa = SA.Initiate(which=self.SA_label, screenoff=False)
        fspan_MHz = abs(self.IF_freq)*7 # SPAN MUST INCLUDE ALL PEAKS
        BW_Hz = 1e6
        points = fspan_MHz*10 + 1
        SA_Setup(self.mxa, self.LO_freq, fspan_MHz=fspan_MHz, BW_Hz=BW_Hz, points=points)
        SA.averag(self.mxa,action=['Set', '10'])
        self.frequency_range = waveform("%s to %s *%s" %(self.LO_freq-fspan_MHz/2000, self.LO_freq+fspan_MHz/2000, points-1)).data
        # Trigger Number XY:1 RO:2 (for DR-1 case)
        SA.trigger_source(self.mxa, action=['Set','EXTernal%s'%(self.iqcal_config[self.mode]['trigger'])])
        sleep(3)

    def settings(self):
        
        # It will catch the data from C:\Users\ASQUM\HODOR\CONFIG\INSTLOG\MIXER_1_status.pyqum and update to DAC. 
        try:
            # load previous half-way calibrated results and resume:
            Iamp, Iphase, Ioffset = [float(x) for x in get_status("MIXER")["%si%s" %(self.mixer_module, round(self.IF_freq, 1))].split("/")]
            Qamp, Qphase, Qoffset = [float(x) for x in get_status("MIXER")["%sq%s" %(self.mixer_module, round(self.IF_freq, 1))].split("/")]
            IQparams = array([Ioffset, Qoffset, Qamp/Iamp, Iphase, Qphase])
        except:
            # defaults:
            print(Fore.CYAN + "Fresh Calibration: Loading Defaults")
            IQparams=array([0.,0.,1.,0.,90.])
        self.IQparams = IQparams
        
        # Pre-play Pre-Calibrated Modulation:
        pulsettings = Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.IF_scale, self.mixer_module, self.channels_group, self.iqcal_config[self.mode]['marker'])    

    def calibration(self):
        count = 0
        Ioffset, Qoffset = self.IQparams[0], self.IQparams[1]
        phai_IQ = self.IQparams[4] - self.IQparams[3]
        a_IQ = self.IQparams[2]
        print(f'Conv power: {SA.mark_power(self.mxa, self.Conv_freq)[0]} dBm')
        print(f'LO leakage: {SA.mark_power(self.mxa, self.leakage_freq[0])[0]} dBm') 
        print(f'MR leakage: {SA.mark_power(self.mxa, self.leakage_freq[1])[0]} dBm')
        low_phai_bound, high_phai_bound = phai_IQ-self.range_phai, phai_IQ+self.range_phai
        low_a_bound, high_a_bound = a_IQ-self.range_a, a_IQ+self.range_a
        low_offsetI_bound, high_offsetI_bound = Ioffset-self.range_I, Ioffset+self.range_I
        low_offsetQ_bound, high_offsetQ_bound = Qoffset-self.range_Q, Qoffset+self.range_Q
        
        while(1):
            # Press 'stop' then it will stop at here
            if get_status("RELAY")['autoIQCAL'] == 0: break
            print('######################################### Phase calibration #########################################')
            # Choose 5 separate points between the low bound and high bound
            Phai = linspace(low_phai_bound, high_phai_bound, 5)
            print(f'low_phai_bound:{low_phai_bound}, high_phai_bound:{high_phai_bound}')
            mirror = []
            for phai_IQ in Phai:
                self.IQparams = array([Ioffset, Qoffset, a_IQ, 0, phai_IQ])
                pulsettings = Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.IF_scale, self.mixer_module, self.channels_group, self.iqcal_config[self.mode]['marker'])
                signal = SA.mark_power(self.mxa, self.leakage_freq[1])[0]
                mirror.append(signal)
            phai_IQ = find_minimum(Phai,mirror)
            self.IQparams = array([Ioffset, Qoffset, a_IQ, 0, phai_IQ])
            pulsettings = Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.IF_scale, self.mixer_module, self.channels_group, self.iqcal_config[self.mode]['marker'])
            signal = SA.mark_power(self.mxa, self.leakage_freq[1])[0]
            target = SA.mark_power(self.mxa, self.Conv_freq)[0]
            print(f'{Phai}, {mirror}')
            print(f'find min phai_IQ: {phai_IQ}, {signal} dBm')
            # Choose phai_IQ as center and decrease point choose with range 
            low_phai_bound, high_phai_bound = phai_IQ-(high_phai_bound-low_phai_bound)/2*self.step_rate**count, phai_IQ+(high_phai_bound-low_phai_bound)/2*self.step_rate**count
            self.current_spectrum = SA.sdata(self.mxa, mode="")
            set_status("RELAY", dict(autoIQCAL_dur_s=time()-self.t_start, autoIQCAL_frequencies=self.frequency_range, autoIQCAL_spectrum=self.current_spectrum))
            # Criterion of when the loop will stop
            if signal < target+self.MRstop or count >= 5 or signal < -80:
                print(f'RF: {target} dBm, MR leakage: {signal} dBm')
                break
            count += 1

        count = 0
        while(1):    
            # Press 'stop' then it will stop at here
            if get_status("RELAY")['autoIQCAL'] == 0: break
            print('######################################### Amplitude calibration #########################################')
            # Choose 5 separate points between the low bound and high bound
            A_IQ = linspace(low_a_bound, high_a_bound, 5)
            print(f'low_a_bound:{low_a_bound}, high_a_bound:{high_a_bound}')
            
            mirror = []
            for a_IQ in A_IQ:
                self.IQparams = array([Ioffset, Qoffset, a_IQ, 0, phai_IQ])
                pulsettings = Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.IF_scale, self.mixer_module, self.channels_group, self.iqcal_config[self.mode]['marker'])
                signal = SA.mark_power(self.mxa, self.leakage_freq[1])[0]
                mirror.append(signal)
            
            a_IQ = find_minimum(A_IQ,mirror)
            self.IQparams = array([Ioffset, Qoffset, a_IQ, 0, phai_IQ])
            pulsettings = Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.IF_scale, self.mixer_module, self.channels_group, self.iqcal_config[self.mode]['marker'])
            signal = SA.mark_power(self.mxa, self.leakage_freq[1])[0]
            target = SA.mark_power(self.mxa, self.Conv_freq)[0]
            print(f'find min a_IQ: {a_IQ}, {signal}dBm')
            # Decrease bound with the range 
            low_a_bound, high_a_bound = a_IQ-(high_a_bound-low_a_bound)/2*self.step_rate**count, a_IQ+(high_a_bound-low_a_bound)/2*self.step_rate**count
            print(f'AAAAAAAAAAAAAAAAAAAAAAAAAAAAA count: {count} AAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            self.current_spectrum = SA.sdata(self.mxa, mode="")
            set_status("RELAY", dict(autoIQCAL_dur_s=time()-self.t_start, autoIQCAL_frequencies=self.frequency_range, autoIQCAL_spectrum=self.current_spectrum))
            
            # Criterion of when the loop will stop
            if signal < target+self.MRstop or count >= 5 or signal < -80:
                print(f'RF: {SA.mark_power(self.mxa, self.Conv_freq)[0]} dBm, MR leakage: {signal} dBm')
                break
            
            count += 1
        count = 0 
        offset_Q = Qoffset
        while(1):
            # Press 'stop' then it will stop at here
            if get_status("RELAY")['autoIQCAL'] == 0: break
            print('######################################### LO calibration #########################################')
            # Choose 5 separate points between the low bound and high bound
            Offset_I = linspace(low_offsetI_bound, high_offsetI_bound, 5)
            print(f'low offsetI bound: {low_offsetI_bound}, high offsetI bound: {high_offsetI_bound}')
            leakage = []
            for offset_I in Offset_I:
                self.IQparams = array([offset_I, offset_Q, a_IQ, 0, phai_IQ])
                print("I", self.IQparams)
                pulsettings = Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.IF_scale, self.mixer_module, self.channels_group, self.iqcal_config[self.mode]['marker'])
                signal = SA.mark_power(self.mxa, self.leakage_freq[0])[0]
                leakage.append(signal)
            offset_I = find_minimum(Offset_I,leakage)
            # plt.plot(Offset_I,leakage)
            # plt.savefig(r'C:\Users\ASQUM\Desktop\mixer_cal\offsetI_{}.png'.format(count))
            self.IQparams = array([offset_I, offset_Q, a_IQ, 0, phai_IQ])
            pulsettings = Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.IF_scale, self.mixer_module, self.channels_group, self.iqcal_config[self.mode]['marker'])
            signal = SA.mark_power(self.mxa, self.leakage_freq[0])[0]
            target = SA.mark_power(self.mxa, self.Conv_freq)[0]
            print(f'{Offset_I}, {leakage}')
            print(f'find min offsetI: {offset_I}, {signal}dBm')
            # Decrease the range 
            low_offsetI_bound, high_offsetI_bound = offset_I-(high_offsetI_bound-low_offsetI_bound)/2*self.step_rate**count, offset_I+(high_offsetI_bound-low_offsetI_bound)/2*self.step_rate**count

            self.current_spectrum = SA.sdata(self.mxa, mode="")
            set_status("RELAY", dict(autoIQCAL_dur_s=time()-self.t_start, autoIQCAL_frequencies=self.frequency_range, autoIQCAL_spectrum=self.current_spectrum))

            # Criterion of when the loop will stop
            if signal < target+self.LOstop or count >= 5 or signal < -80:
                print(f'RF: {target} dBm, MR leakage: {signal} dBm')
                break
            
            # Choose 5 separate points between the low bound and high bound
            Offset_Q = linspace(low_offsetQ_bound, high_offsetQ_bound, 5)
            print(f'low offsetQ bound: {low_offsetQ_bound}, high offsetQ bound: {high_offsetQ_bound}')
            leakage = []
            for offset_Q in Offset_Q:
                self.IQparams = array([offset_I, offset_Q, a_IQ, 0, phai_IQ])
                print("Q", self.IQparams)
                pulsettings = Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.IF_scale, self.mixer_module, self.channels_group, self.iqcal_config[self.mode]['marker'])
                signal = SA.mark_power(self.mxa, self.leakage_freq[0])[0]
                leakage.append(signal)
            offset_Q = find_minimum(Offset_Q,leakage)
            self.IQparams = array([offset_I, offset_Q, a_IQ, 0, phai_IQ])
            pulsettings = Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.IF_scale, self.mixer_module, self.channels_group, self.iqcal_config[self.mode]['marker'])
            signal = SA.mark_power(self.mxa, self.leakage_freq[0])[0]
            target = SA.mark_power(self.mxa, self.Conv_freq)[0]
            print(f'{Offset_Q}, {leakage}')
            print(f'find min offsetQ: {offset_Q}, {signal}dBm')
            # Decrease the range 
            low_offsetQ_bound, high_offsetQ_bound = offset_Q-(high_offsetQ_bound-low_offsetQ_bound)/2*self.step_rate**count, offset_Q+(high_offsetQ_bound-low_offsetQ_bound)/2*self.step_rate**count
            print(f'AAAAAAAAAAAAAAAAAAAAAAAAAAAAA count: {count} AAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            self.current_spectrum = SA.sdata(self.mxa, mode="")
            set_status("RELAY", dict(autoIQCAL_dur_s=time()-self.t_start, autoIQCAL_frequencies=self.frequency_range, autoIQCAL_spectrum=self.current_spectrum))

            # Criterion of when the loop will stop
            if signal < target+self.LOstop or count >= 5 or signal < -80:
                print(f'RF: {target} dBm, LO leakage: {signal} dBm')
                break
            count += 1
        # Final check
        pulsettings = Update_DAC(self.daca, self.IF_freq, self.IQparams, self.IF_period, self.IF_scale, self.mixer_module, self.channels_group, self.iqcal_config[self.mode]['marker'])
        
        leakage_LO = SA.mark_power(self.mxa, self.leakage_freq[0])[0]
        leakage_MR = SA.mark_power(self.mxa, self.leakage_freq[1])[0]
        target = SA.mark_power(self.mxa, self.Conv_freq)[0]
        print(f"Calibration Paras {self.IQparams}")
        print(f'RF: {target} dBm, MR leakage: {leakage_MR} dBm, LO leakage: {leakage_LO} dBm')

    def run(self):
        set_status("RELAY", dict(autoIQCAL=1))
        # print(Back.WHITE + Fore.RED + "Background LO-leakage: %s\nBackground MR-leakage: %s\n" %(SA.mark_power(self.mxa, self.LO_freq)[0], SA.mark_power(self.mxa, self.MR_freq[0])[0]))
        set_status("RELAY", dict(BackgroundLO=SA.mark_power(self.mxa, self.LO_freq)[0], BackgroundMR=SA.mark_power(self.mxa, self.MR_freq)[0]))
        self.current_spectrum = SA.sdata(self.mxa, mode="")
        set_status("RELAY", dict(autoIQCAL_dur_s="Check Background", autoIQCAL_frequencies=self.frequency_range, autoIQCAL_spectrum=self.current_spectrum))
        sleep(3.17)
        
        print(Fore.YELLOW + "Initial LO")
        self.settings()
        self.LO_Initial, self.MR_Initial = SA.mark_power(self.mxa, self.LO_freq)[0], SA.mark_power(self.mxa, self.MR_freq)[0]
        # print(Back.WHITE + Fore.RED + "Initial LO-leakage: %s\nInitial 1st-MR-leakage: %s\n" %(self.LO_Initial, self.MR_Initial))
        set_status("RELAY", dict(LO_Initial=self.LO_Initial, MR_Initial=self.MR_Initial))
        self.current_spectrum = SA.sdata(self.mxa, mode="")
        set_status("RELAY", dict(autoIQCAL_dur_s="Check Initial LO", autoIQCAL_frequencies=self.frequency_range, autoIQCAL_spectrum=self.current_spectrum))
        sleep(3.17)

        print('RF before calibration : %s' %(SA.mark_power(self.mxa, self.Conv_freq)[0]))
        print('LO leakage before calibration: %s' %(SA.mark_power(self.mxa, self.leakage_freq[0])[0]))
        print('MR leakage before calibration: %s' %(SA.mark_power(self.mxa, self.leakage_freq[1])[0]))
        sleep(3.17)

        self.t_start = time()
        if SA.mark_power(self.mxa, self.leakage_freq[0])[0] > SA.mark_power(self.mxa, self.Conv_freq)[0]-50 or SA.mark_power(self.mxa, self.leakage_freq[1])[0] > SA.mark_power(self.mxa, self.Conv_freq)[0]-50:
            self.calibration()
        self.current_spectrum = SA.sdata(self.mxa, mode="")
        set_status("RELAY", dict(autoIQCAL=0, autoIQCAL_dur_s=time()-self.t_start, autoIQCAL_frequencies=self.frequency_range, autoIQCAL_spectrum=self.current_spectrum))
        sleep(3.17)
        
        print('RF after calibration : %s' %(SA.mark_power(self.mxa, self.Conv_freq)[0]))
        print('LO leakage after calibration: %s' %(SA.mark_power(self.mxa, self.leakage_freq[0])[0]))
        print('MR leakage after calibration: %s' %(SA.mark_power(self.mxa, self.leakage_freq[1])[0]))
    
    def close(self):
        '''closing instruments:
        '''
        DAC.alloff(self.daca, action=['Set',1])
        DAC.close(self.daca, which=self.DA_label)
        SG.rfoutput(self.saga, action=['Set', 0])
        SG.close(self.saga, self.LO_label, False)
        SA.close(self.mxa, False, which=self.SA_label)

def test():
    # ===============================================================
    # Conv_freq (GHz), LO_powa (dBm), IF_freq (MHz), IF_period (ns), IF_scale, mixer_module, wiring-configuration, channels-group (1st channel of dual)
    C = IQ_Calibrate(4.30996, 23, -120, 300000, 0.02, 'xy195v4', dict(SG='PSGA_2',DA='SDAWG_2',SA='MXA_1'), 1) # Conv_freq (GHz), LO_powa (dBm), IF_freq (MHz), IF_period (ns), IF_scale, mixer_module
    C.run()
    # ===============================================================
    C.close()

if __name__ == '__main__' :
    test()

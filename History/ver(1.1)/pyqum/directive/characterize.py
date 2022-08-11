'''Basic QuBit Characterizations'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # instrument-module's name e.g. ENA, PSG, YOKO

from time import time, sleep
from numpy import linspace, sin, pi, prod, array, mean, sqrt, zeros, float64, ceil, power, arctan2, floor
from flask import request, session, current_app, g, Flask

from pyqum.instrument.modular import VSA
from pyqum.instrument.benchtop import TKAWG as AWG
from pyqum.instrument.benchtop import PSGV as PSG0
from pyqum.instrument.benchtop import PSGA as PSG1
from pyqum.instrument.benchtop import ENA, YOKO
from pyqum.instrument.logger import settings, clocker, get_status, set_status, status_code
from pyqum.instrument.analyzer import curve, IQAP, UnwraPhase, IQAParray
from pyqum.instrument.toolbox import cdatasearch, gotocdata, waveform, squarewave

__author__ = "Teik-Hui Lee"
__copyright__ = "Copyright 2019, The Pyqum Project"
__credits__ = ["Chii-Dong Chen"]
__license__ = "GPL"
__version__ = "beta3"
__email__ = "teikhui@phys.sinica.edu.tw"
__status__ = "development"

yoko_choice = 0 # Left: 0 for coil; Right: 1 for Z-Line
            
# **********************************************************************************************************************************************************
# 1. FREQUENCY RESPONSE MEASUREMENT:
@settings(2) # data-density
def F_Response(user, tag="", corder={}, comment='', dayindex='', taskentry=0, resumepoint=0, instr=['YOKO','ENA'], testeach=False):
    '''Characterizing Frequency Response:
    C-Order: Flux-Bias, S-Parameter, IF-Bandwidth, Power, Frequency
    '''
    sample = get_status("MSSN")[session['user_name']]['sample']
    # pushing pre-measurement parameters to settings:
    yield user, sample, tag, instr, corder, comment, dayindex, taskentry, testeach
    set_status("F_Response", dict(active=instr))

    # User-defined Controlling-PARAMETER(s) ======================================================================================
    fluxbias = waveform(corder['Flux-Bias'])
    Sparam = waveform(corder['S-Parameter'])
    ifb = waveform(corder['IF-Bandwidth'])
    powa = waveform(corder['Power'])
    freq = waveform(corder['Frequency'])
    # Total data points:
    datasize = prod([waveform(x).count for x in corder.values()]) * 2 #data density of 2 due to IQ

    # Pre-loop settings:
    # ENA:
    bench = ENA.Initiate(True)
    ENA.dataform(bench, action=['Set', 'REAL'])
    ENA.sweep(bench, action=['Set', 'ON', freq.count])
    fstart, fstop = freq.data[0]*1e9, freq.data[-1]*1e9
    ENA.linfreq(bench, action=['Set', fstart, fstop]) # Linear Freq-sweep-range
    # YOKO:
    if "opt" not in fluxbias.data: # check if it is in optional-state
        yokog = YOKO.Initiate(current=True, which=yoko_choice) # PENDING option: choose between Voltage / Current output
        YOKO.output(yokog, 1)

    # Buffer setting(s) for certain loop(s):
    buffersize_1 = freq.count * 2 #data density of 2 due to IQ
    
    # User-defined Measurement-FLOW ==============================================================================================
    if testeach: # measure-time contribution from each measure-loop
        loopcount, loop_dur = [], []
        stage, prev = clocker(0) # Marking starting point of time
    
    # Registerring parameter(s)-structure
    cstructure = [fluxbias.count,Sparam.count,ifb.count,powa.count]

    # set previous parameters based on resumepoint:
    if resumepoint > 0:
        caddress = cdatasearch(resumepoint//buffersize_1, cstructure)
        # Only those involved in virtual for-loop need to be pre-set here:
        if "opt" not in fluxbias.data: # check if it is in optional-state
            YOKO.sweep(yokog, str(fluxbias.data[caddress[0]]), pulsewidth=77*1e-3, sweeprate=0.0007) # A-mode: sweeprate=0.0007 A/s ; V-mode: sweeprate=0.07 V/s
        ENA.setrace(bench, Mparam=[Sparam.data[caddress[1]]], window='D1')
        ENA.ifbw(bench, action=['Set', ifb.data[caddress[2]]])

    measure_loop_1 = range(resumepoint//buffersize_1,datasize//buffersize_1) # saving chunck by chunck improves speed a lot!
    while True:
        for i in measure_loop_1:

            # Registerring parameter(s)
            caddress = cdatasearch(i, cstructure)

            # setting each c-order (From High to Low level of execution):
            if not i%prod(cstructure[1::]): # virtual for-loop using exact-multiples condition
                if "opt" not in fluxbias.data: # check if it is in optional-state
                    if testeach: # test each measure-loop:
                        loopcount += [fluxbias.count]
                        if fluxbias.count > 1: loop_dur += [abs(fluxbias.data[0]-fluxbias.data[1])/0.2 + 35*1e-3]
                        else: loop_dur += [0]
                        stage, prev = clocker(stage, prev) # Marking time
                    else: YOKO.sweep(yokog, str(fluxbias.data[caddress[0]]), pulsewidth=77*1e-3, sweeprate=0.0007) # A-mode: sweeprate=0.0007 A/s ; V-mode: sweeprate=0.07 V/s
                    
            if not i%prod(cstructure[2::]): # virtual for-loop using exact-multiples condition
                ENA.setrace(bench, Mparam=[Sparam.data[caddress[1]]], window='D1')

            if not i%prod(cstructure[3::]): # virtual for-loop using exact-multiples condition
                ENA.ifbw(bench, action=['Set', ifb.data[caddress[2]]])

            ENA.power(bench, action=['Set', powa.data[caddress[3]]]) # same as the whole measure-loop

            # start sweeping:
            stat = ENA.sweep(bench) #getting the estimated sweeping time
            print("Time-taken for this loop would be: %s (%spts)" %(stat[1]['TIME'], stat[1]['POINTS']))
            print("Operation Complete: %s" %bool(ENA.measure(bench)))
            # adjusting display on ENA:
            ENA.autoscal(bench)
            ENA.selectrace(bench, action=['Set', 'para 1 calc 1'])
            data = ENA.sdata(bench)
            # print(Fore.YELLOW + "\rProgress: %.3f%% [%s]" %((i+1)/datasize*100, data), end='\r', flush=True)
            print(Fore.YELLOW + "\rProgress: %.3f%%" %((i+1)/datasize*buffersize_1*100), end='\r', flush=True)
            
            # test for the last loop if there is
            if testeach: # test each measure-loop:
                loopcount += [len(measure_loop_1)]
                loop_dur += [time() - prev]
                stage, prev = clocker(stage, prev) # Marking time
                ENA.close(bench)
                if "opt" not in fluxbias.data: # check if it is in optional-state
                    YOKO.close(yokog, False)
                yield loopcount, loop_dur
                
            else:
                if get_status("F_Response")['pause']:
                    break
                else:
                    yield data

        if not get_status("F_Response")['repeat']:
            set_status("F_Response", dict(pause=True))
            ENA.close(bench)
            if "opt" not in fluxbias.data: # check if it is in optional-state
                YOKO.close(yokog, False)
            return

# **********************************************************************************************************************************************************
# 2. CONTINUOUS-WAVE SWEEPING:
@settings(2) # data-density
def CW_Sweep(user, tag="", corder={}, comment='', dayindex='', taskentry=0, resumepoint=0, instr=['PSG','YOKO','ENA'], testeach=False):
    '''Continuous Wave Sweeping:
    C-Order: Flux-Bias, XY-Frequency, XY-Power, S-Parameter, IF-Bandwidth, Frequency, Power
    '''
    sample = get_status("MSSN")[session['user_name']]['sample']
    # pushing pre-measurement parameters to settings:
    yield user, sample, tag, instr, corder, comment, dayindex, taskentry, testeach
    set_status("CW_Sweep", dict(active=instr))

    # User-defined Controlling-PARAMETER(s) ======================================================================================
    fluxbias = waveform(corder['Flux-Bias'])
    xyfreq = waveform(corder['XY-Frequency'])
    xypowa = waveform(corder['XY-Power'])
    Sparam = waveform(corder['S-Parameter'])
    ifb = waveform(corder['IF-Bandwidth'])
    freq = waveform(corder['Frequency'])
    # special treatment to power in this CW-Mode Sweeping:
    powa = waveform(corder['Power'])
    powa_repeat = powa.inner_repeat
    print("power sequence: %s, length: %s, inner-repeat-counts: %s" %(powa.command, powa.count, powa_repeat))
    # input("continue?")

    # Total data points:
    datasize = int(prod([waveform(x).count * waveform(x).inner_repeat for x in corder.values()], dtype='uint64')) * 2 #data density of 2 due to IQ
    print("data size: %s" %datasize)
    
    # Pre-loop settings:
    # ENA:
    bench = ENA.Initiate(True)
    ENA.dataform(bench, action=['Set', 'REAL'])
    if powa_repeat == 1: 
        # collect swept power-data every measure-loop
        ENA.sweep(bench, action=['Set', 'ON', powa.count])
        ENA.power(bench, action=['Set', '', powa.data[0], powa.data[-1]]) # for power sweep (set pstart & pstop)
        buffersize_1 = powa.count * 2 # (buffer) data density of 2 due to IQ
    else: 
        # collect repetitive power-data every measure-loop
        ENA.sweep(bench, action=['Set', 'ON', powa_repeat])
        buffersize_1 = powa_repeat * 2 # (buffer) data density of 2 due to IQ

    # YOKO:
    if "opt" not in fluxbias.data: # check if it is in optional-state / serious-state
        yokog = YOKO.Initiate(current=True, which=yoko_choice) # pending option
        YOKO.output(yokog, 1)

    # PSG:
    if "opt" not in xyfreq.data: # check if it is in optional-state / serious-state
        sogo = PSG0.Initiate() # pending option
        PSG0.rfoutput(sogo, action=['Set', 1])

    # User-defined Measurement-FLOW ==============================================================================================
    if testeach: # measure-time contribution from each measure-loop
        loopcount, loop_dur = [], []
        stage, prev = clocker(0) # Marking starting point of time
    
    # Registerring parameter(s)-structure
    if powa_repeat == 1: cstructure = [fluxbias.count, xyfreq.count, xypowa.count, Sparam.count, ifb.count, freq.count, 1] # just single CW
    else: cstructure = [fluxbias.count, xyfreq.count, xypowa.count, Sparam.count, ifb.count, freq.count, powa.count] # take CW average by repeating
    
    # set previous parameters based on resumepoint:
    if resumepoint//buffersize_1 > 0:
        caddress = cdatasearch(resumepoint//buffersize_1, cstructure)
        # Only those involved in virtual for-loop need to be pre-set here:
        # Optionals:
        if "opt" not in fluxbias.data: # check if it is in optional-state / serious-state
            YOKO.sweep(yokog, str(fluxbias.data[caddress[0]]), pulsewidth=77*1e-3, sweeprate=0.0007) # A-mode: sweeprate=0.0007 A/s ; V-mode: sweeprate=0.07 V/s 
        if "opt" not in xyfreq.data: # check if it is in optional-state / serious-state
            PSG0.frequency(sogo, action=['Set', str(xyfreq.data[caddress[1]]) + "GHz"])
            PSG0.power(sogo, action=['Set', str(xypowa.data[caddress[2]]) + "dBm"])
        # Basics:
        ENA.setrace(bench, Mparam=[Sparam.data[caddress[3]]], window='D1')
        ENA.ifbw(bench, action=['Set', ifb.data[caddress[4]]])
        ENA.cwfreq(bench, action=['Set', freq.data[caddress[5]]*1e9])

    measure_loop_1 = range(resumepoint//buffersize_1,datasize//buffersize_1) # saving chunck by chunck improves speed a lot!
    while True:
        for i in measure_loop_1:

            # determining the index-locations for each parameters, i.e. the address at any instance
            caddress = cdatasearch(i, cstructure)

            # setting each c-order (From High to Low level of execution):
            # ***************************************************************
            # Optionals:
            if not i%prod(cstructure[1::]): # virtual for-loop using exact-multiples condition
                if "opt" not in fluxbias.data: # check if it is in optional-state
                    if testeach: # adding instrument transition-time between set-values:
                        loopcount += [fluxbias.count]
                        if fluxbias.count > 1: loop_dur += [abs(fluxbias.data[0]-fluxbias.data[1])/0.2 + 35*1e-3]
                        else: loop_dur += [0]
                        stage, prev = clocker(stage, prev) # Marking time
                    else: YOKO.sweep(yokog, str(fluxbias.data[caddress[0]]), pulsewidth=77*1e-3, sweeprate=0.0007) # A-mode: sweeprate=0.0007 A/s ; V-mode: sweeprate=0.07 V/s
            
            if not i%prod(cstructure[2::]): # virtual for-loop using exact-multiples condition
                if "opt" not in xyfreq.data: # check if it is in optional-state
                    PSG0.frequency(sogo, action=['Set', str(xyfreq.data[caddress[1]]) + "GHz"])

            if not i%prod(cstructure[3::]): # virtual for-loop using exact-multiples condition
                if "opt" not in xypowa.data: # check if it is in optional-state
                    PSG0.power(sogo, action=['Set', str(xypowa.data[caddress[2]]) + "dBm"])

            # Basics:
            if not i%prod(cstructure[4::]): # virtual for-loop using exact-multiples condition
                ENA.setrace(bench, Mparam=[Sparam.data[caddress[3]]], window='D1')

            if not i%prod(cstructure[5::]): # virtual for-loop using exact-multiples condition
                ENA.ifbw(bench, action=['Set', ifb.data[caddress[4]]])

            if not i%prod(cstructure[6::]): # virtual for-loop using exact-multiples condition
                ENA.cwfreq(bench, action=['Set', freq.data[caddress[5]]*1e9])

            if powa_repeat > 1:
                ENA.power(bench, action=['Set', '', powa.data[caddress[6]], powa.data[caddress[6]]]) # same as the whole measure-loop

            # start sweeping:
            stat = ENA.sweep(bench) #getting the estimated sweeping time
            print("Time-taken for this loop would be: %s (%spts)" %(stat[1]['TIME'], stat[1]['POINTS']))
            print("Operation Complete: %s" %bool(ENA.measure(bench)))
            # adjusting display on ENA:
            ENA.autoscal(bench)
            ENA.selectrace(bench, action=['Set', 'para 1 calc 1'])
            data = ENA.sdata(bench)
            print(Fore.YELLOW + "\rProgress: %.3f%%" %((i+1)/datasize*buffersize_1*100), end='\r', flush=True)
            
            # test for the last loop if there is
            if testeach: # test each measure-loop:
                loopcount += [len(measure_loop_1)]
                loop_dur += [time() - prev]
                stage, prev = clocker(stage, prev) # Marking time
                ENA.close(bench)
                if "opt" not in xyfreq.data: # check if it is in optional-state
                    PSG0.close(sogo, False)
                if "opt" not in fluxbias.data: # check if it is in optional-state
                    YOKO.close(yokog, False)
                yield loopcount, loop_dur
                
            else:
                if get_status("CW_Sweep")['pause']:
                    break
                else:
                    yield data


        if not get_status("CW_Sweep")['repeat']:
            set_status("CW_Sweep", dict(pause=True))
            ENA.close(bench)
            if "opt" not in xyfreq.data: # check if it is in optional-state
                PSG0.rfoutput(sogo, action=['Set', 0])
                PSG0.close(sogo, False)
            if "opt" not in fluxbias.data: # check if it is in optional-state
                YOKO.output(yokog, 0)
                YOKO.close(yokog, False)
            return

# **********************************************************************************************************************************************************
# 3. Square-wave Pulse measurement
@settings(2) # data-density
def SQE_Pulse(user, tag="", corder={}, comment='', dayindex='', taskentry=0, resumepoint=0, instr=['YOKO', 'PSGV', 'PSGA', 'AWG', 'VSA'], testeach=False):
    '''Time-domain Square-wave measurement:
    C-Structure: ['Flux-Bias', 
                    'Average', 'Pulse-Period', 'ADC-delay', 
                    'LO-Frequency', 'LO-Power', 'RO-Frequency', 'RO-Power', 'RO-ifLevel', 'RO-Pulse-Delay', 'RO-Pulse-Width', 
                    'XY-Frequency', 'XY-Power', 'XY-ifLevel', 'XY-Pulse-Delay', 'XY-Pulse-Width', 
                    'Sampling-Time'] (IQ-Bandwidth (250MHz or its HALFlings) + Acquisition-Time (dt must be multiples of 2ns))
    '''
    # Loading sample:
    sample = get_status("MSSN")[session['user_name']]['sample']
    # sample = get_status("MSSN")['abc']['sample'] # by-pass HTTP-request before interface is ready

    # pushing pre-measurement parameters to settings:
    yield user, sample, tag, instr, corder, comment, dayindex, taskentry, testeach
    set_status("SQE_Pulse", dict(msg='measurement started', active=instr))

    # ***USER_DEFINED*** Controlling-PARAMETER(s) ======================================================================================
    config = corder['C-Config']
    structure = corder['C-Structure']
    fluxbias = waveform(corder['Flux-Bias'])
    averaging = waveform(corder['Average'])
    pperiod = waveform(corder['Pulse-Period'])
    adcdelay = waveform(corder['ADC-delay'])
    lofreq = waveform(corder['LO-Frequency'])
    lopowa = waveform(corder['LO-Power'])
    rofreq = waveform(corder['RO-Frequency'])
    ropowa = waveform(corder['RO-Power'])
    roiflevel = waveform(corder['RO-ifLevel'])
    ropdelay = waveform(corder['RO-Pulse-Delay'])
    ropwidth = waveform(corder['RO-Pulse-Width'])
    xyfreq = waveform(corder['XY-Frequency'])
    xypowa = waveform(corder['XY-Power'])
    xyiflevel = waveform(corder['XY-ifLevel'])
    xypdelay = waveform(corder['XY-Pulse-Delay'])
    xypwidth = waveform(corder['XY-Pulse-Width'])
    samptime = waveform(corder['Sampling-Time'])

    # Total data points:
    datasize = int(prod([waveform(corder[param]).count for param in structure], dtype='uint64')) * 2 #data density of 2 due to IQ
    print("data size: %s" %datasize)
    
    # Pre-loop settings:
    # Optionals:
    # YOKO:
    if "opt" not in fluxbias.data: # check if it is in optional-state / serious-state
        yokog = YOKO.Initiate(current=True, which=yoko_choice) # pending option
        YOKO.output(yokog, 1)

    # PSGV:
    if "opt" not in xyfreq.data: # check if it is in optional-state / serious-state
        sogo = PSG0.Initiate() # pending option
        PSG0.rfoutput(sogo, action=['Set', 1])

    # Basics:
    # PSGA for LO:
    saga = PSG1.Initiate() # pending option
    PSG1.rfoutput(saga, action=['Set', 1])

    # AWG for Control:
    ifperiod = pperiod.data[0] # PENDING: make pulse-period a peripheral (a constant config every scheduled run)
    awgsess = AWG.Initiate()
    AWG.clock(awgsess, action=['Set', 'EFIXed',2.5e9])
    AWG.clear_waveform(awgsess,'all')
    AWG.alloff(awgsess, action=['Set',1])
    # PRESET Output:
    '''Prepare DAC:'''
    for ch in range(4):
        channel = str(ch + 1)
        AWG.prepare_DAC(awgsess, channel, int(ifperiod*2.5))
    # Turn on all 4 channels:
    AWG.compose_DAC(awgsess, 1, array(squarewave(ifperiod, 0, 0, 1, dt=0.4, clock_multiples=1)))
    AWG.compose_DAC(awgsess, 2, array(squarewave(ifperiod, 0, 0, 1, dt=0.4, clock_multiples=1)))
    AWG.compose_DAC(awgsess, 3, array(squarewave(ifperiod, 0, 0, 1, dt=0.4, clock_multiples=1)))
    AWG.compose_DAC(awgsess, 4, array(squarewave(ifperiod, 0, 0, 1, dt=0.4, clock_multiples=1)))
    AWG.alloff(awgsess, action=['Set',0])
    AWG.ready(awgsess)
    AWG.play(awgsess)
    
    # VSA for Readout
    vsasess = VSA.InitWithOptions()
    
    # Buffer-size for lowest-bound data-collecting instrument:
    buffersize_1 = samptime.count * 2 #data density of 2 due to IQ
    print("Buffer-size: %s" %buffersize_1)

    # User-defined Measurement-FLOW ==============================================================================================
    if testeach: # measure-time contribution from each measure-loop
        loopcount, loop_dur = [], []
        stage, prev = clocker(0) # Marking starting point of time
    
    # Registerring parameter(s)-structure
    cstructure = [waveform(corder[param]).count for param in structure][:-1] # The last one will become a buffer
    print('cstructure: %s' %cstructure)

    measure_loop_1 = range(resumepoint//buffersize_1,datasize//buffersize_1) # saving chunck by chunck improves speed a lot!
    while True:
        for i in measure_loop_1:
            print(Back.BLUE + Fore.WHITE + 'measure %s/%s' %(i,datasize//buffersize_1))
            # determining the index-locations for each parameters, i.e. the address at any instance
            caddress = cdatasearch(i, cstructure)

            # setting each c-order (From High to Low level of execution):
            # ***************************************************************
            for j in range(len(cstructure)-1): # the last one will be run for every i (common sense!)
                if (not i%prod(cstructure[j+1::])) or i==resumepoint//buffersize_1: # virtual for-loop using exact-multiples condition
                    # print("entering %s-stage" %j)
                    # Optionals:
                    # YOKO
                    if structure[j] == 'Flux-Bias':
                        if "opt" not in fluxbias.data: # check if it is in optional-state
                            if testeach: # adding instrument transition-time between set-values:
                                loopcount += [fluxbias.count]
                                if fluxbias.count > 1: loop_dur += [abs(fluxbias.data[0]-fluxbias.data[1])/0.2 + 35*1e-3] # manually calculating time without really setting parameter on the instrument
                                else: loop_dur += [0]
                                stage, prev = clocker(stage, prev) # Marking time
                            else: YOKO.sweep(yokog, str(fluxbias.data[caddress[structure.index('Flux-Bias')]]), pulsewidth=77*1e-3, sweeprate=0.0007) # A-mode: sweeprate=0.0007 A/s ; V-mode: sweeprate=0.07 V/s

                    # PSG
                    if structure[j] == 'XY-Frequency':
                        if "opt" not in xyfreq.data: # check if it is in optional-state
                            PSG0.frequency(sogo, action=['Set', str(xyfreq.data[caddress[structure.index('XY-Frequency')]]) + "GHz"])
                    if structure[j] == 'XY-Power':
                        if "opt" not in xypowa.data: # check if it is in optional-state
                            PSG0.power(sogo, action=['Set', str(xypowa.data[caddress[structure.index('XY-Power')]]) + "dBm"])
                    if structure[j] == 'RO-Frequency':
                        if "opt" not in rofreq.data: # check if it is in optional-state
                            PSG1.frequency(saga, action=['Set', str(rofreq.data[caddress[structure.index('RO-Frequency')]]) + "GHz"])
                    if structure[j] == 'RO-Power':
                        if "opt" not in ropowa.data: # check if it is in optional-state
                            PSG1.power(saga, action=['Set', str(ropowa.data[caddress[structure.index('RO-Power')]]) + "dBm"])

            # Basic
            # AWG (Every-loop)
            # define waveforms' elements:
            ifontime = float(xypwidth.data[caddress[structure.index('XY-Pulse-Width')]]), float(ropwidth.data[caddress[structure.index('RO-Pulse-Width')]])
            if "lockxypwd" in str(ropdelay.data[0]): 
                if '+' in str(ropdelay.data[0]): rooffset = float(ropdelay.data[0].split('+')[1])
                else: rooffset = 0 # default value
                ifdelay = float(xypdelay.data[caddress[structure.index('XY-Pulse-Delay')]]), float(xypwidth.data[caddress[structure.index('XY-Pulse-Width')]]) + rooffset
                print("RO-Pulse Delays behind XY-Pulse for %sns" %(ifdelay[1]-ifdelay[0]))
            else: 
                ifdelay = float(xypdelay.data[caddress[structure.index('XY-Pulse-Delay')]]), float(ropdelay.data[caddress[structure.index('RO-Pulse-Delay')]])
            ifscale = float(xyiflevel.data[caddress[structure.index('XY-ifLevel')]]), float(roiflevel.data[caddress[structure.index('RO-ifLevel')]])
            
            # assigning I-channels for XY and RO:
            AWG.compose_DAC(awgsess, 1, array(squarewave(ifperiod, ifontime[0], ifdelay[0], ifscale[0],  dt=0.4, clock_multiples=1)))
            AWG.compose_DAC(awgsess, 3, array(squarewave(ifperiod, ifontime[1], ifdelay[1], ifscale[1],  dt=0.4, clock_multiples=1)), 1, 200) # put marker on RO channel-I
            print('Waveform is Ready: %s' %str(AWG.ready(awgsess)))
                
            # Basic / Buffer:
            # VSA (Every-loop)
            avenum = int(averaging.data[caddress[structure.index('Average')]])
            if config['lock-period'] == 'yes': 
                recurrence = int(min([floor(256e6/ifperiod), avenum])) 
                avenum = int(ceil(avenum / recurrence))
            else: #default
                recurrence = 1
            VSA.acquisition_time(vsasess, action=['Set',float(recurrence*samptime.count*2e-9)]) # minimum time resolution
            VSA.preselector_enabled(vsasess, action=['Set',False]) # disable preselector to allow the highest bandwidth of 250MHz
            print(Fore.YELLOW + "Recurrence: %s" %recurrence)

            if "lockro" in str(lofreq.data[0]):
                if '+' in str(lofreq.data[0]): lof_offset = float(lofreq.data[0].split('+')[1])
                elif '-' in str(lofreq.data[0]): lof_offset = -float(lofreq.data[0].split('-')[1])
                else: lof_offset = 0 # default value
                VSA.frequency(vsasess, action=['Set',float(rofreq.data[caddress[structure.index('RO-Frequency')]])*1e9+lof_offset]) # freq offset / correction in Hz
                print("Locking on RO at %sGHz" %(VSA.frequency(vsasess)[1]/1e9))
            else:
                VSA.frequency(vsasess, action=['Set',float(lofreq.data[caddress[structure.index('LO-Frequency')]])*1e9])

            VSA.power(vsasess, action=['Set',float(lopowa.data[caddress[structure.index('LO-Power')]])])
            VSA.bandwidth(vsasess, action=['Set',250e6]) # maximum LO bandwidth of 250MHz (500MHz Sampling-rate gives 2ns of time resolution)
            VSA.trigger_source(vsasess, action=['Set',int(1)]) # External Trigger (slave)

            # Delay for Readout
            if "lockxypwd" in str(ropdelay.data[0]):
                # trigger-delay sync with xy-pulse-width for Rabi measurement:
                VSA.trigger_delay(vsasess, action=['Set', float(adcdelay.data[caddress[structure.index('ADC-delay')]]) + \
                    float(xypwidth.data[caddress[structure.index('XY-Pulse-Width')]])*1e-9 + rooffset*1e-9])
                print("ACQ delays with XY-Pulse for %sns" %int(VSA.trigger_delay(vsasess)[1]/1e-9))
            elif "lockropdelay" in str(adcdelay.data[0]):
                # trigger-delay sync with ro-pulse-delay for T1 measurement:
                VSA.trigger_delay(vsasess, action=['Set', float(ropdelay.data[caddress[structure.index('RO-Pulse-Delay')]])*1e-9])
                print("ACQ delays with RO-Pulse for %sns" %int(VSA.trigger_delay(vsasess)[1]/1e-9))
            else:
                VSA.trigger_delay(vsasess, action=['Set', float(adcdelay.data[caddress[structure.index('ADC-delay')]])]) 

            VSA.external_trigger_level(vsasess, action=['Set',float(0.3)])
            VSA.external_trigger_slope(vsasess, action=['Set',int(1)]) # Positive slope
            VSA.trigger_timeout(vsasess, action=['Set',int(1000)]) # 1s of timeout
            stat = VSA.Init_Measure(vsasess) # Initiate Measurement
                        
            # Start Quantum machine:
            # Start Averaging Loop:
            vsasn = VSA.samples_number(vsasess)[1]
            if (vsasn%recurrence) and (recurrence>1):
                errormsg = "Period must be multiples of 2ns"
                set_status("SQE_Pulse", dict(msg=errormsg, pause=True))
                print(Fore.RED + errormsg)
                break
            iqdata = zeros((avenum*recurrence,int(2*vsasn/recurrence)))
            # Max number of points for VSA in the buffer = 128MS
            # BUT: M9202A doesn't support Segment Acquisition, which I'm trying to do as follows:
            for c in range(avenum):
                VSA.Arm_Measure(vsasess)
                gd = VSA.Get_Data(vsasess, 2*vsasn)
                # iqdata[c*recurrence:(c+1)*recurrence,:] = array(gd[1]['ComplexData']).reshape(recurrence,int(2*vsasn/recurrence))
                iqdata[c,:] = mean(array(gd[1]['ComplexData']).reshape(recurrence,int(2*vsasn/recurrence)), axis=0)
            # exporting data for saving
            endata = zeros(int(2*vsasn/recurrence))
            
            if config['data-option'] == 'AP':
                print(Fore.BLUE + "%s mode:" %config)
                idata, qdata = iqdata[:,0::2], iqdata[:,1::2]
                Adata = mean(sqrt(power(idata,2) + power(qdata,2)), axis=0)
                Pdata = mean(arctan2(qdata, idata), axis=0)
                endata[0::2], endata[1::2] = Adata, Pdata
            else: #default
                print(Fore.BLUE + "%s mode:" %config)
                iqdata = mean(iqdata, axis=0)
                endata = iqdata
            print("Operation Complete")
            print(Fore.YELLOW + "\rProgress: %.3f%%" %((i+1)/datasize*buffersize_1*100), end='\r', flush=True)			
            
            # test for the last loop if there is
            if testeach: # test each measure-loop:
                loopcount += [len(measure_loop_1)]
                loop_dur += [time() - prev]
                stage, prev = clocker(stage, prev) # Marking time
                VSA.close(vsasess)
                if "opt" not in pperiod.data: # check if it is in optional-state
                    AWG.close(awgsess)
                if "opt" not in xyfreq.data: # check if it is in optional-state
                    PSG0.close(sogo, False)
                if "opt" not in rofreq.data: # check if it is in optional-state
                    PSG1.close(saga, False)
                if "opt" not in fluxbias.data: # check if it is in optional-state
                    YOKO.close(yokog, False)
                yield loopcount, loop_dur
                
            else:
                if get_status("SQE_Pulse")['pause']:
                    break
                else:
                    yield list(endata)


        if not get_status("SQE_Pulse")['repeat']:
            set_status("SQE_Pulse", dict(msg='measurement concluded', pause=True))
            VSA.close(vsasess)
            if "opt" not in pperiod.data: # check if it is in optional-state
                AWG.alloff(awgsess, action=['Set',1])
                AWG.close(awgsess)
            if "opt" not in xyfreq.data: # check if it is in optional-state
                PSG0.rfoutput(sogo, action=['Set', 0])
                PSG0.close(sogo, False)
            if "opt" not in rofreq.data: # check if it is in optional-state
                PSG1.rfoutput(saga, action=['Set', 0])
                PSG1.close(saga, False)
            if "opt" not in fluxbias.data: # check if it is in optional-state
                YOKO.output(yokog, 0)
                YOKO.close(yokog, False)
            return


def test():
    # New RUN:

    # Ex: CWSWEEP:
    # CORDER = {'Flux-Bias':'1.5 to 3.2 * 70', 'S-Parameter':'S21,', 'IF-Bandwidth':'100', 'Frequency':'5.36 to 5.56 * 250', 'Power':'-25 to 0 * 100 r 1000'}
    # CW_Sweep('abc', corder=CORDER, comment='prototype test', tag='', dayindex=-1, testeach=False)
    
    # Retrieve data:
    # case = CW_Sweep('abc')
    # case.selectday(case.whichday())
    # m = case.whichmoment()
    # case.selectmoment(m)
    # print("File selected: %s" %case.pqfile)
    # case.accesstructure()
    # print(case.comment)
    
    return

# test()


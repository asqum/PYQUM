'''Single-QuBit Manipulations'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # instrument-module's name e.g. ENA, PSG, YOKO

# from time import time, sleep
from copy import copy, deepcopy
from json import loads
from numpy import prod, array, mean, ceil
from flask import session, g

from importlib import import_module as im
from pyqum.instrument.logger import settings, get_status, set_status, jobsinqueue, qout
from pyqum.instrument.toolbox import cdatasearch, waveform
from pyqum.instrument.composer import pulser
from pyqum.instrument.analyzer import pulse_baseband


__author__ = "Teik-Hui Lee"
__copyright__ = "Copyright 2019, The Pyqum Project"
__credits__ = ["Chii-Dong Chen"]
__license__ = "GPL"
__version__ = "beta3"
__email__ = "teikhui@phys.sinica.edu.tw"
__status__ = "development"

# **********************************************************************************************************************************************************
# 1. Single-Qubit Control:
@settings(2) # data-density
def Single_Qubit(owner, tag="", corder={}, comment='', dayindex='', taskentry=0, resumepoint=0, instr={}, perimeter={}):
    '''
    Time-domain Square-wave measurement:\n
    SCORES (SCripted ORchestration of Entanglement & Superposition) is a scripted pulse instruction language for running Quantum Algorithm.\n
    perimeter.keys() = ['XY-LO-Power', 'RO-LO-Power', 'SCORE-NS', 'SCORE-JSON', 'R-JSON', 'RECORD-SUM', 'RECORD_TIME_NS', 'READOUTYPE']\n
    C-Structure = ['Flux-Bias', 'XY-LO-Frequency', 'RO-LO-Frequency'] + [...R-parameter(s)...]\n
    Differ from previous directive, this version onward, our stored data will assume the following form:\n
    DATA = STRUCTURE + BUFFER (Thus ALL part of Structure will now participate in measure-loop)
    '''

    # BYPASS:
    instr['DC'], instr['SG'], instr['DAC'], instr['ADC'] = 'YOKO_2', ['PSGA_2', 'PSGV_1'], 'TKAWG_1', 'ALZDG_1' # bypass instruments UI-selection
    sample = get_status("MSSN")[session['user_name']]['sample']
    queue = get_status("MSSN")[session['user_name']]['queue']

    # pushing pre-measurement parameters to settings:
    yield owner, sample, tag, instr, corder, comment, dayindex, taskentry, perimeter, queue

    # ***USER_DEFINED*** Controlling-PARAMETER(s) ======================================================================================
    # 1a. DSP perimeter(s)
    digital_homodyne = perimeter['DIGIHOME']
    # rotation_compensate_MHz = float(perimeter['IF_MHZ'])
    ifreqcorrection_kHz = float(perimeter['IF_ALIGN_KHZ'])
    # 1b. Basic perimeter(s): # previously: config = corder['C-Config']
    biasmode = bool(int(perimeter['BIASMODE']))
    xypowa = perimeter['XY-LO-Power']
    ropowa = perimeter['RO-LO-Power']
    trigger_delay_ns = int(perimeter['TRIGGER_DELAY_NS'])
    recordsum = int(perimeter['RECORD-SUM'])
    recordtime_ns = int(perimeter['RECORD_TIME_NS']) # min:1280ns, step:128ns
    readoutype = perimeter['READOUTYPE']
    SCORE_TEMPLATE = perimeter['SCORE-JSON'] # already a DICT
    RJSON = loads(perimeter['R-JSON'].replace("'",'"'))
    # 1b. Derived perimeter(s) from above:
    ifperiod = pulser(score=SCORE_TEMPLATE['CH1']).totaltime
    RO_Compensate_MHz = -pulser(score=SCORE_TEMPLATE['CH1']).IF_MHz_rotation # working with RO-MOD (up or down)
    XY_Compensate_MHz = -pulser(score=SCORE_TEMPLATE['CH3']).IF_MHz_rotation # working with XY-MOD (up or down)
    skipoints = 0
    try: 
        if (digital_homodyne=="i_digital_homodyne" or digital_homodyne=="q_digital_homodyne"): skipoints = int(ceil( 1 / abs(RO_Compensate_MHz) * 1000 ))
    except: 
        print(Fore.RED + "WARNING: INFINITE INTEGRATION IS NOT PRACTICAL!")
    # print(Fore.CYAN + "Skipping first %s point(s)" %skipoints)

    # 2a. Basic corder / parameter(s):
    structure = corder['C-Structure'] + [k for k in RJSON.keys()]
    fluxbias = waveform(corder['Flux-Bias'])
    xyfreq = waveform(corder['XY-LO-Frequency'])
    rofreq = waveform(corder['RO-LO-Frequency'])
    for k in RJSON.keys(): corder[k] = RJSON[k] # update corder with R-parameters
    # 2b. Prepare R-waveform object for pulse-instructions
    R_waveform = {}
    for k in RJSON.keys(): R_waveform[k] = waveform(RJSON[k])

    # Buffer-size for lowest-bound data-collecting instrument:
    if readoutype == 'one-shot': # for fidelity measurement
        buffersize = recordsum * 2 # data-density of 2 due to IQ
        print("Buffer-size: %s" %buffersize)
    else: # by default we usually take average
        buffersize = recordtime_ns * 2 # data-density of 2 due to IQ
        print("Buffer-size: %s" %buffersize)

    # Total data points to be saved into file:
    datasize = int(prod([waveform(corder[param]).count for param in structure], dtype='uint64')) * buffersize
    print("data size: %s" %datasize)
    
    # Pre-loop settings:
    # Optionals:
    # DC:
    [DC_type, DC_label] = instr['DC'].split('_')
    DC = im("pyqum.instrument.machine.%s" %DC_type)
    if "opt" not in fluxbias.data: # check if it is in optional-state / serious-state
        dcbench = DC.Initiate(current=biasmode, which=DC_label) # pending option
        DC.output(dcbench, 1)

    # SG for XY:
    SG_label = [None] * len(instr['SG']) # PENDING: LISTIFY ALL INSTR.VALUES()
    [SG_type, SG_label[0]] = instr['SG'][0].split('_')
    SG0 = im("pyqum.instrument.machine.%s" %SG_type)
    if "opt" not in xyfreq.data: # check if it is in optional-state / serious-state
        sogo = SG0.Initiate(which=SG_label[0])
        SG0.power(sogo, action=['Set', str(xypowa) + "dBm"])
        SG0.rfoutput(sogo, action=['Set', 1])

    # Basics:
    # SG for RO:
    [SG_type, SG_label[1]] = instr['SG'][1].split('_')
    SG1 = im("pyqum.instrument.machine.%s" %SG_type)
    if "opt" not in rofreq.data: # check if it is in optional-state / serious-state
        saga = SG1.Initiate(which=SG_label[1])
        SG1.power(saga, action=['Set', str(ropowa) + "dBm"])
        SG1.rfoutput(saga, action=['Set', 1])

    # DAC:
    [DAC_type, DAC_label] = instr['DAC'].split('_')
    DAC = im("pyqum.instrument.machine.%s" %DAC_type)
    daca = DAC.Initiate(which=DAC_label)
    DAC.clock(daca, action=['Set', 'EFIXed',2.5e9])
    DAC.clear_waveform(daca,'all')
    DAC.alloff(daca, action=['Set',1])
    '''Prepare DAC:'''
    dt = round(1/float(DAC.clock(daca)[1]['SRATe'])/1e-9, 2)
    pulseq = pulser(dt=dt, clock_multiples=1, score="ns=%s"%ifperiod)
    pulseq.song()
    for ch in range(4):
        channel = str(ch + 1)
        DAC.prepare_DAC(daca, channel, pulseq.totalpoints)
    for ch in range(4):
        channel = str(ch + 1)
        DAC.compose_DAC(daca, channel, pulseq.music) # we don't need marker yet initially
    # Turn on all 4 channels:
    DAC.alloff(daca, action=['Set',0])
    DAC.ready(daca)
    DAC.play(daca)
    
    # ADC:
    [ADC_type, ADC_label] = instr['ADC'].split('_')
    ADC = im("pyqum.instrument.machine.%s" %ADC_type)
    adca = ADC.Initiate(which=ADC_label)
    '''Prepare ADC:'''
    ADC.ConfigureBoard_NPT(adca, triggerDelay_sec=trigger_delay_ns*1e-9)

    # User-defined Measurement-FLOW ==============================================================================================
    
    # 1. Registerring parameter(s)-structure
    cstructure = [waveform(corder[param]).count for param in structure] # new version: separation between structure & buffer

    # 2. Start measuring:
    JOBID = g.jobidlist[0]
    measure_loop = range(resumepoint//buffersize,datasize//buffersize) # saving chunck by chunck improves speed a lot!
    while True:
        for i in measure_loop:
            print(Back.BLUE + Fore.WHITE + 'measure single-qubit %s/%s' %(i+1,datasize//buffersize))
            # determining the index-locations for each parameters, i.e. the address at any instance
            caddress = cdatasearch(i, cstructure)
            print(Fore.BLACK + Back.WHITE + "i: %s, cstructure: %s, caddress: %s" %(i,cstructure,caddress))

            # setting each c-order (From High to Low level of execution):
            # ***************************************************************
            SCORE_DEFINED = deepcopy(SCORE_TEMPLATE)
            for j in range(len(cstructure)): # new version: all part of structure will participate
                if (not i%prod(cstructure[j+1::])) or i==resumepoint//buffersize: # virtual for-loop using exact-multiples condition
                    # print("entering %s-stage" %j)
                    # Optionals:
                    # DC
                    if structure[j] == 'Flux-Bias':
                        if "opt" not in fluxbias.data: # check if it is in optional-state
                            if biasmode: sweeprate = 0.000713  # A-mode A/s
                            else:  sweeprate = 1.37  # V-mode V/s (~10kOhm resistance)
                            DC.sweep(dcbench, str(fluxbias.data[caddress[j]]), sweeprate=sweeprate)

                    # SG
                    elif structure[j] == 'XY-LO-Frequency':
                        if "opt" not in xyfreq.data: # check if it is in optional-state
                            SG0.frequency(sogo, action=['Set', str(xyfreq.data[caddress[j]] + XY_Compensate_MHz/1e3) + "GHz"])
                    elif structure[j] == 'RO-LO-Frequency':
                        if "opt" not in rofreq.data: # check if it is in optional-state
                            SG1.frequency(saga, action=['Set', str(rofreq.data[caddress[j]] + RO_Compensate_MHz/1e3) + "GHz"])

                # DAC's SCORE-UPDATE:
                if j > 2:
                    for ch in range(4):
                        channel = str(ch + 1)
                        SCORE_DEFINED['CH%s'%channel] = SCORE_DEFINED['CH%s'%channel].replace("{%s}"%structure[j], str(R_waveform[structure[j]].data[caddress[j]]))

            # print(Fore.YELLOW + "DEFINED SCORE-CH1: %s" %(SCORE_DEFINED['CH1']))
            # IN THE FUTURE: HVI-ROUTINE STARTS HERE:
            # Basic Control (Every-loop)
            # DAC
            for ch in range(4):
                channel = str(ch + 1)
                pulseq = pulser(dt=dt, clock_multiples=1, score=SCORE_DEFINED['CH%s'%channel])
                pulseq.song()
                DAC.compose_DAC(daca, int(channel), pulseq.music, pulseq.envelope, 2) # ODD for PIN-SWITCH, EVEN for TRIGGER; RO-TRIGGER: 1: ALZDG, 2: MXA; XY-TRIGGER: 1: MXA, 2: SCOPE
            DAC.ready(daca)
            print('Waveform is Ready!')
                
            # Basic Readout (Buffer Every-loop):
            # ADC 
            DATA = ADC.AcquireData_NPT(adca, recordtime_ns*1e-9, recordsum)[0]
            # POST PROCESSING
            try:
                # TIME EVOLUTION / FIDELITY TEST:
                if readoutype == 'one-shot':
                    DATA = DATA.reshape([recordsum,recordtime_ns*2])
                    if digital_homodyne != "original": 
                        for r in range(recordsum):
                            trace_I, trace_Q = DATA[r,:].reshape((recordtime_ns, 2)).transpose()[0], DATA[r,:].reshape((recordtime_ns, 2)).transpose()[1]
                            trace_I, trace_Q = pulse_baseband(digital_homodyne, trace_I, trace_Q, RO_Compensate_MHz, ifreqcorrection_kHz)
                            DATA[r,:] = array([trace_I, trace_Q]).reshape(2*recordtime_ns) # back to interleaved IQ-Data
                            if not r%1000: print(Fore.YELLOW + "Shooting %s times" %(r+1))
                    DATA = mean(DATA.reshape([recordsum*2,recordtime_ns])[:,skipoints:], axis=1)
                    print(Fore.BLUE + "DATA of size %s is ready to be saved" %len(DATA))
                else: # by default
                    DATA = mean(DATA.reshape([recordsum,recordtime_ns*2]), axis=0)
                    if digital_homodyne != "original": 
                        trace_I, trace_Q = DATA.reshape((recordtime_ns, 2)).transpose()[0], DATA.reshape((recordtime_ns, 2)).transpose()[1]
                        trace_I, trace_Q = pulse_baseband(digital_homodyne, trace_I, trace_Q, RO_Compensate_MHz, ifreqcorrection_kHz)
                        DATA = array([trace_I, trace_Q]).transpose().reshape(recordtime_ns*2) # back to interleaved IQ-Data
            
            except(ValueError):
                # raise # PENDING: UPDATE TIMSUM MISMATCH LIST
                print(Fore.RED + "Check ALZDG OPT_DMA_BUFFER!")
                break # proceed to close all & queue out
            
            # print("Operation Complete")
            print(Fore.YELLOW + "\rProgress: %.3f%%" %((i+1)/datasize*buffersize*100), end='\r', flush=True)			
            
            jobsinqueue(queue)
            if JOBID in g.jobidlist:
                # print(Fore.YELLOW + "Pushing Data into file...")
                yield list(DATA)
            else: break # proceed to close all & queue out

        # PENDING: LISTIFY / DICTIFY THE HANDLE?
        ADC.close(adca, which=ADC_label)
        DAC.alloff(daca, action=['Set',1])
        DAC.close(daca, which=DAC_label)
        if "opt" not in rofreq.data: # check if it is in optional-state
            SG1.rfoutput(saga, action=['Set', 0])
            SG1.close(saga, SG_label[1], False)
        if "opt" not in xyfreq.data: # check if it is in optional-state
            SG0.rfoutput(sogo, action=['Set', 0])
            SG0.close(sogo, SG_label[0], False)
        if "opt" not in fluxbias.data: # check if it is in optional-state
            DC.output(dcbench, 0)
            DC.close(dcbench, True, DC_label, sweeprate=sweeprate)
        if JOBID in g.jobidlist:
            qout(queue, g.jobidlist[0],g.user['username'])
        break

    return

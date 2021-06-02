'''Basic QuBit Characterizations'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # instrument-module's name e.g. ENA, PSG, YOKO

# from time import time, sleep
from numpy import prod
from flask import session, g

from importlib import import_module as im
from pyqum.instrument.logger import settings, clocker, get_status, set_status, status_code, qout, lisqueue
from pyqum.instrument.analyzer import curve, IQAP, UnwraPhase, IQAParray
from pyqum.instrument.toolbox import cdatasearch, gotocdata, waveform

__author__ = "Teik-Hui Lee"
__copyright__ = "Copyright 2019, The Pyqum Project"
__credits__ = ["Chii-Dong Chen"]
__license__ = "GPL"
__version__ = "beta3"
__email__ = "teikhui@phys.sinica.edu.tw"
__status__ = "development"

yoko_choice = 1 # Left: 1 for coil; Right: 2 for Z-Line
            
# **********************************************************************************************************************************************************
# 1. FREQUENCY RESPONSE MEASUREMENT:
@settings(2) # data-density
def F_Response(owner, tag="", corder={}, comment='', dayindex='', taskentry=0, resumepoint=0, instr={}, perimeter={}, queue=''):
    '''Characterizing Frequency Response:
    C-Order: Flux-Bias, S-Parameter, IF-Bandwidth, Power, Frequency
    '''
    instr['DC'], instr['NA'] = 'YOKO_1', 'ENA_1' # bypass instruments UI-selection
    
    sample = get_status("MSSN")[session['user_name']]['sample']
    queue = get_status("MSSN")[session['user_name']]['queue']
    # pushing pre-measurement parameters to settings:
    yield owner, sample, tag, instr, corder, comment, dayindex, taskentry, perimeter, queue
    # set_status("F_Response", dict(active=instr))

    # User-defined Controlling-PARAMETER(s) ======================================================================================
    fluxbias = waveform(corder['Flux-Bias'])
    Sparam = waveform(corder['S-Parameter'])
    ifb = waveform(corder['IF-Bandwidth'])
    powa = waveform(corder['Power'])
    freq = waveform(corder['Frequency'])
    # Total data points:
    datasize = prod([waveform(x).count for x in corder.values()]) * 2 #data density of 2 due to IQ

    # Pre-loop settings:
    # NA:
    [NA_type, NA_label] = instr['NA'].split('_')
    NA = im("pyqum.instrument.benchtop.%s" %NA_type)
    nabench = NA.Initiate(True, which=NA_label)
    NA.dataform(nabench, action=['Set', 'REAL'])
    NA.sweep(nabench, action=['Set', 'ON', freq.count])
    fstart, fstop = freq.data[0]*1e9, freq.data[-1]*1e9
    NA.linfreq(nabench, action=['Set', fstart, fstop]) # Linear Freq-sweep-range
    # DC:
    [DC_type, DC_label] = instr['DC'].split('_')
    DC = im("pyqum.instrument.benchtop.%s" %DC_type)
    if "opt" not in fluxbias.data: # check if it is in optional-state
        dcbench = DC.Initiate(current=True, which=DC_label) # PENDING option: choose between Voltage / Current output
        DC.output(dcbench, 1)

    # Buffer setting(s) for certain loop(s):
    buffersize_1 = freq.count * 2 #data density of 2 due to IQ
    
    # User-defined Measurement-FLOW ==============================================================================================
    
    # 1. Registerring parameter(s)-structure:
    cstructure = [fluxbias.count,Sparam.count,ifb.count,powa.count]

    # 2. Set previous parameters based on resumepoint:
    if resumepoint > 0:
        caddress = cdatasearch(resumepoint//buffersize_1, cstructure)
        # Only those involved in virtual for-loop need to be pre-set here:
        if "opt" not in fluxbias.data: # check if it is in optional-state
            DC.sweep(dcbench, str(fluxbias.data[caddress[0]]), pulsewidth=77*1e-3, sweeprate=0.0007) # A-mode: sweeprate=0.0007 A/s ; V-mode: sweeprate=0.07 V/s
        NA.setrace(nabench, Mparam=[Sparam.data[caddress[1]]])
        NA.ifbw(nabench, action=['Set', ifb.data[caddress[2]]])

    # 3. Start measuring:
    JOBID = g.jobidlist[queue][0]
    measure_loop_1 = range(resumepoint//buffersize_1,datasize//buffersize_1) # saving chunck by chunck improves speed a lot!
    while True:
        for i in measure_loop_1:

            # Registerring parameter(s)
            caddress = cdatasearch(i, cstructure)

            # setting each c-order (From High to Low level of execution):
            if not i%prod(cstructure[1::]): # virtual for-loop using exact-multiples condition
                if "opt" not in fluxbias.data: # check if it is in optional-state
                    DC.sweep(dcbench, str(fluxbias.data[caddress[0]]), pulsewidth=77*1e-3, sweeprate=0.0007) # A-mode: sweeprate=0.0007 A/s ; V-mode: sweeprate=0.07 V/s
                    
            if not i%prod(cstructure[2::]): # virtual for-loop using exact-multiples condition
                NA.setrace(nabench, Mparam=[Sparam.data[caddress[1]]])

            if not i%prod(cstructure[3::]): # virtual for-loop using exact-multiples condition
                NA.ifbw(nabench, action=['Set', ifb.data[caddress[2]]])

            NA.power(nabench, action=['Set', powa.data[caddress[3]]]) # same as the whole measure-loop

            # start sweeping:
            stat = NA.sweep(nabench) #getting the estimated sweeping time
            print("Time-taken for this loop would be: %s (%spts)" %(stat[1]['TIME'], stat[1]['POINTS']))
            print(Fore.GREEN + "Operation Complete: %s" %bool(NA.measure(nabench)))
            # adjusting display on NA:
            NA.autoscal(nabench)
            # NA.selectrace(nabench, action=['Set', 'para 1 calc 1'])
            data = NA.sdata(nabench)
            # print(Fore.YELLOW + "\rProgress: %.3f%% [%s]" %((i+1)/datasize*100, data), end='\r', flush=True)
            # print(Fore.YELLOW + "\rProgress: %.3f%%" %((i+1)/datasize*buffersize_1*100), end='\r', flush=True)
            print(Fore.YELLOW + "Progress: %.3f%%" %((i+1)/datasize*buffersize_1*100))

            lisqueue(queue)
            if JOBID in g.jobidlist[queue]:
                # print(Fore.YELLOW + "Pushing Data into file...")
                yield data
            else: break

        # Closing all instruments and Queueing out:
        NA.close(nabench)
        if "opt" not in fluxbias.data: # check if it is in optional-state
            DC.close(dcbench, True, DC_label)
        if JOBID in g.jobidlist[queue]:
            qout(queue, g.jobidlist[queue][0],g.user['username'])
        break

    return

# **********************************************************************************************************************************************************
# 2. CONTINUOUS-WAVE SWEEPING:
@settings(2) # data-density
def CW_Sweep(owner, tag="", corder={}, comment='', dayindex='', taskentry=0, resumepoint=0, instr={}, perimeter={}, queue=''):
    '''Continuous Wave Sweeping:
    C-Order: Flux-Bias, XY-Frequency, XY-Power, S-Parameter, IF-Bandwidth, Frequency, Power
    '''
    instr['DC'], instr['SG'], instr['NA'] = 'YOKO_1', 'PSGA_1', 'ENA_1' # bypass instruments UI-selection

    sample = get_status("MSSN")[session['user_name']]['sample']
    queue = get_status("MSSN")[session['user_name']]['queue']
    # pushing pre-measurement parameters to settings:
    yield owner, sample, tag, instr, corder, comment, dayindex, taskentry, perimeter, queue
    # set_status("CW_Sweep", dict(active=instr))

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
    # NA:
    [NA_type, NA_label] = instr['NA'].split('_')
    NA = im("pyqum.instrument.benchtop.%s" %NA_type)
    nabench = NA.Initiate(True, which=NA_label)
    NA.dataform(nabench, action=['Set', 'REAL'])
    if powa_repeat == 1: 
        # collect swept power-data every measure-loop
        NA.sweep(nabench, action=['Set', 'ON', powa.count])
        NA.power(nabench, action=['Set', '', powa.data[0], powa.data[-1]]) # for power sweep (set pstart & pstop)
        buffersize_1 = powa.count * 2 # (buffer) data density of 2 due to IQ
    else: 
        # collect repetitive power-data every measure-loop
        NA.sweep(nabench, action=['Set', 'ON', powa_repeat])
        buffersize_1 = powa_repeat * 2 # (buffer) data density of 2 due to IQ

    # DC:
    [DC_type, DC_label] = instr['DC'].split('_')
    DC = im("pyqum.instrument.benchtop.%s" %DC_type)
    if "opt" not in fluxbias.data: # check if it is in optional-state / serious-state
        dcbench = DC.Initiate(current=True, which=DC_label) # pending option
        DC.output(dcbench, 1)

    # SG:
    [SG_type, SG_label] = instr['SG'].split('_')
    SG = im("pyqum.instrument.benchtop.%s" %SG_type)
    if "opt" not in xyfreq.data: # check if it is in optional-state / serious-state
        sgbench = SG.Initiate(which=SG_label)
        SG.rfoutput(sgbench, action=['Set', 1])

    # User-defined Measurement-FLOW ==============================================================================================
    
    # 1. Registerring parameter(s)-structure
    if powa_repeat == 1: cstructure = [fluxbias.count, xyfreq.count, xypowa.count, Sparam.count, ifb.count, freq.count, 1] # just single CW
    else: cstructure = [fluxbias.count, xyfreq.count, xypowa.count, Sparam.count, ifb.count, freq.count, powa.count] # take CW average by repeating
    
    # 2. Set previous parameters based on resumepoint:
    if resumepoint//buffersize_1 > 0:
        caddress = cdatasearch(resumepoint//buffersize_1, cstructure)
        # Only those involved in virtual for-loop need to be pre-set here:
        # Optionals:
        if "opt" not in fluxbias.data: # check if it is in optional-state / serious-state
            DC.sweep(dcbench, str(fluxbias.data[caddress[0]]), pulsewidth=77*1e-3, sweeprate=0.0007) # A-mode: sweeprate=0.0007 A/s ; V-mode: sweeprate=0.07 V/s 
        if "opt" not in xyfreq.data: # check if it is in optional-state / serious-state
            SG.frequency(sgbench, action=['Set', str(xyfreq.data[caddress[1]]) + "GHz"])
            SG.power(sgbench, action=['Set', str(xypowa.data[caddress[2]]) + "dBm"])
        # Basics:
        NA.setrace(nabench, Mparam=[Sparam.data[caddress[3]]])
        NA.ifbw(nabench, action=['Set', ifb.data[caddress[4]]])
        NA.cwfreq(nabench, action=['Set', freq.data[caddress[5]]*1e9])

    # 3. Start measuring:
    JOBID = g.jobidlist[queue][0]
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
                    DC.sweep(dcbench, str(fluxbias.data[caddress[0]]), pulsewidth=77*1e-3, sweeprate=0.0007) # A-mode: sweeprate=0.0007 A/s ; V-mode: sweeprate=0.07 V/s
            
            if not i%prod(cstructure[2::]): # virtual for-loop using exact-multiples condition
                if "opt" not in xyfreq.data: # check if it is in optional-state
                    SG.frequency(sgbench, action=['Set', str(xyfreq.data[caddress[1]]) + "GHz"])

            if not i%prod(cstructure[3::]): # virtual for-loop using exact-multiples condition
                if "opt" not in xypowa.data: # check if it is in optional-state
                    SG.power(sgbench, action=['Set', str(xypowa.data[caddress[2]]) + "dBm"])

            # Basics:
            if not i%prod(cstructure[4::]): # virtual for-loop using exact-multiples condition
                NA.setrace(nabench, Mparam=[Sparam.data[caddress[3]]])

            if not i%prod(cstructure[5::]): # virtual for-loop using exact-multiples condition
                NA.ifbw(nabench, action=['Set', ifb.data[caddress[4]]])

            if not i%prod(cstructure[6::]): # virtual for-loop using exact-multiples condition
                NA.cwfreq(nabench, action=['Set', freq.data[caddress[5]]*1e9])

            if powa_repeat > 1:
                NA.power(nabench, action=['Set', '', powa.data[caddress[6]], powa.data[caddress[6]]]) # same as the whole measure-loop

            # start sweeping:
            stat = NA.sweep(nabench) #getting the estimated sweeping time
            print("Time-taken for this loop would be: %s (%spts)" %(stat[1]['TIME'], stat[1]['POINTS']))
            print("Operation Complete: %s" %bool(NA.measure(nabench)))
            # adjusting display on NA:
            NA.autoscal(nabench)
            # NA.selectrace(nabench, action=['Set', 'para 1 calc 1'])
            data = NA.sdata(nabench)
            print(Fore.YELLOW + "\rProgress: %.3f%%" %((i+1)/datasize*buffersize_1*100), end='\r', flush=True)
            
            lisqueue(queue)
            if JOBID in g.jobidlist[queue]:
                # print(Fore.YELLOW + "Pushing Data into file...")
                yield data
            else: break

        # Closing all instruments and Queueing out:
        NA.close(nabench)
        if "opt" not in xyfreq.data: # check if it is in optional-state
            SG.rfoutput(sgbench, action=['Set', 0])
            SG.close(sgbench, SG_label, False)
        if "opt" not in fluxbias.data: # check if it is in optional-state
            DC.output(dcbench, 0)
            DC.close(dcbench, True, DC_label)
        if JOBID in g.jobidlist[queue]:
            qout(queue, g.jobidlist[queue][0],g.user['username'])
        break

    return

# **********************************************************************************************************************************************************
# 3. Square-wave Pulse measurement
@settings(2) # data-density
def SQE_Pulse(owner, tag="", corder={}, comment='', dayindex='', taskentry=0, resumepoint=0, instr={}, perimeter={}):
    '''!DEPRECATED!
    Square-Pulse Measurement with VSA (retired: IQ-Bandwidth (250MHz or its HALFlings) & Acquisition-Time (dt must be multiples of 2ns) ).
    '''
    sample = get_status("MSSN")[session['user_name']]['sample']
    yield owner, sample, tag, instr, corder, comment, dayindex, taskentry, perimeter, ''


def test():
    # New RUN:

    # Ex: CWSWEEP:
    # CORDER = {'Flux-Bias':'1.5 to 3.2 * 70', 'S-Parameter':'S21,', 'IF-Bandwidth':'100', 'Frequency':'5.36 to 5.56 * 250', 'Power':'-25 to 0 * 100 r 1000'}
    # CW_Sweep('abc', corder=CORDER, comment='prototype test', tag='', dayindex=-1)
    
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


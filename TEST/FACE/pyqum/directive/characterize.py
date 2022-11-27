'''Basic QuBit Characterizations: CHAR_'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from ast import literal_eval # better than json.loads to handle dict w/o any quotation mark.
from numpy import prod
from flask import session, g

from importlib import import_module as im
from pyqum.instrument.logger import settings, get_status, qout, jobsinqueue
from pyqum.instrument.toolbox import cdatasearch, waveform
from pyqum.instrument.reader import inst_order

__author__ = "Teik-Hui Lee"
__copyright__ = "Copyright 2019, The Pyqum Project"
__credits__ = ["Chii-Dong Chen"]
__license__ = "GPL"
__version__ = "beta3"
__email__ = "teikhui@phys.sinica.edu.tw"
__status__ = "development"

            
# **********************************************************************************************************************************************************
# 1. FREQUENCY RESPONSE MEASUREMENT:
@settings(2) # data-density
def F_Response(owner, tag="", corder={}, comment='', dayindex='', taskentry=0, resumepoint=0, instr={}, perimeter={}, queue='', renamed_task=''):
    '''Characterizing Frequency Response:
    C-Order: Flux-Bias, S-Parameter, IF-Bandwidth, Power, Frequency
    MACE: Modular Assembly of Continuous Execution: 
    '''
    # BYPASS SOME SETTINGS (PENDING IMPLEMENTATION INTO QUM AFTER POC)
    # ============================================================================================================================
    
    # User-specific settings in JSON:
    sample = get_status("MSSN")[session['user_name']]['sample']
    queue = get_status("MSSN")[session['user_name']]['queue']

    # Queue-specific instrument-package:
    CH_Wiring = inst_order(queue, 'CH')
    DC_Matrix = CH_Wiring['DC']
    ROLE_Wiring = inst_order(queue, 'ROLE')
    DC_Role = ROLE_Wiring['DC']
    instr['DC']= inst_order(queue, 'DC') # multiple modules allowed
    instr['NA']= inst_order(queue, 'NA')[0]

    # pushing pre-measurement parameters to settings:
    yield owner, sample, tag, instr, corder, comment, dayindex, taskentry, perimeter, queue, renamed_task

    # User-defined Controlling-PARAMETER(s) & -PERIMETER(s) ======================================================================================
    # 1. PERIMETER:
    dcsweepch = perimeter['dcsweepch']
    z_idle = literal_eval(perimeter['z-idle']) # Idle Z-JSON: {"<Module>-<Channel>": "<DC Value>", ... } e.g. {"1-2": "0.03 to 0.06 *LOCK"}
    dc_sweep_config = literal_eval(perimeter['sweep-config']) # DC sweep configurations
    current = dc_sweep_config['current']
    # 2. PARAMETER:
    fluxbias_lock = dict()
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
    NA = im("pyqum.instrument.machine.%s" %NA_type)
    nabench = NA.Initiate(True, which=NA_label)
    NA.dataform(nabench, action=['Set', 'REAL'])
    NA.sweep(nabench, action=['Set', 'ON', freq.count])
    fstart, fstop = freq.data[0]*1e9, freq.data[-1]*1e9
    NA.linfreq(nabench, action=['Set', fstart, fstop]) # Linear Freq-sweep-range
    # DC:
    DC_qty = len(instr['DC'])
    DC_type, DC_label, DC, DC_instance = [None]*DC_qty, [None]*DC_qty, [None]*DC_qty, [None]*DC_qty
    for i, channel_set in enumerate(DC_Matrix):
        [DC_type[i], DC_label[i]] = instr['DC'][i].split('_')
        if "DUMMY" not in DC_type[i].upper(): DC[i] = im("pyqum.instrument.machine.%s" %DC_type[i])
        if "opt" not in fluxbias.data: # check if it is in optional-state
            DC_instance[i] = DC[i].Initiate(current=current, which=DC_label[i]) # PENDING option: choose between Voltage / Current output
            DC[i].output(DC_instance[i], 1, channel=dcsweepch)
            # Pre-setting Z-Idle-Channels:
            for key in z_idle.keys(): 
                if i+1==int(key.split('-')[0]):
                    if "lock" not in str(z_idle[key]).lower(): DC[i].sweep(DC_instance[i], z_idle[key], channel=int(key.split('-')[1]), update_settings=dc_sweep_config) # locked to itself
                    else: fluxbias_lock[key] = waveform(z_idle[key].lower().replace("lock",str(fluxbias.count-1))) # locked to fluxbias

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
            DC[0].sweep(DC_instance[0], str(fluxbias.data[caddress[0]]), channel=dcsweepch, update_settings=dc_sweep_config) # A-mode: sweeprate=0.0007 A/s ; V-mode: sweeprate=0.07 V/s
            # Locking Z-Idle-Channels to Sweeping-Master-Channel:
            for module, channel_set in enumerate(DC_Matrix):
                for key in z_idle.keys():
                    if module+1==int(key.split('-')[0]):
                        if "lock" in str(z_idle[key]).lower(): DC[module].sweep(DC_instance[module], str(fluxbias_lock[key].data[caddress[0]]), channel=int(key.split('-')[1]), update_settings=dc_sweep_config)
        NA.setrace(nabench, Mparam=[Sparam.data[caddress[1]]])
        NA.ifbw(nabench, action=['Set', ifb.data[caddress[2]]])

    # 3. Start measuring:
    JOBID = g.queue_jobid_list[0]
    measure_loop_1 = range(resumepoint//buffersize_1,datasize//buffersize_1) # saving chunck by chunck improves speed a lot!
    while True:
        for i in measure_loop_1:

            # Registerring parameter(s)
            caddress = cdatasearch(i, cstructure)

            # setting each c-order (From High to Low level of execution):
            if not i%prod(cstructure[1::]): # virtual for-loop using exact-multiples condition
                if "opt" not in fluxbias.data: # check if it is in optional-state
                    DC[0].sweep(DC_instance[0], str(fluxbias.data[caddress[0]]), channel=dcsweepch, update_settings=dc_sweep_config) # A-mode: sweeprate=0.0007 A/s ; V-mode: sweeprate=0.07 V/s
                    # Locking Z-Idle-Channels to Sweeping-Master-Channel:
                    for module, channel_set in enumerate(DC_Matrix):
                        for key in z_idle.keys():
                            if module+1==int(key.split('-')[0]):
                                if "lock" in str(z_idle[key]).lower(): DC[module].sweep(DC_instance[module], str(fluxbias_lock[key].data[caddress[0]]), channel=int(key.split('-')[1]), update_settings=dc_sweep_config)
                    
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

            jobsinqueue(queue)
            if JOBID in g.queue_jobid_list:
                # print(Fore.YELLOW + "Pushing Data into file...")
                yield data
            else: break

        # Closing all instruments and Queueing out:
        NA.close(nabench, which=NA_label)
        if "opt" not in fluxbias.data: # check if it is in optional-state
            for i_module, channel_set in enumerate(DC_Matrix):
                DC[i_module].output(DC_instance[i_module], 0)
                DC[i_module].close(DC_instance[i_module], reset=True, which=DC_label[i_module])
        if JOBID in g.queue_jobid_list:
            qout(queue, g.queue_jobid_list[0],g.user['username'])
        break

    return

# **********************************************************************************************************************************************************
# 2. CONTINUOUS-WAVE SWEEPING:
@settings(2) # data-density
def CW_Sweep(owner, tag="", corder={}, comment='', dayindex='', taskentry=0, resumepoint=0, instr={}, perimeter={}, queue='', renamed_task=''):
    '''Continuous Wave Sweeping:
    C-Order: Flux-Bias, XY-Frequency, XY-Power, S-Parameter, IF-Bandwidth, Frequency, Power
    '''
    # BYPASS SOME SETTINGS (PENDING IMPLEMENTATION INTO QUM AFTER POC)
    # ============================================================================================================================
    
    # User-specific settings in JSON:
    sample = get_status("MSSN")[session['user_name']]['sample']
    queue = get_status("MSSN")[session['user_name']]['queue']

    # Queue-specific instrument-package:
    CH_Wiring = inst_order(queue, 'CH')
    DC_Matrix = CH_Wiring['DC']
    ROLE_Wiring = inst_order(queue, 'ROLE')
    DC_Role = ROLE_Wiring['DC']
    instr['DC']= inst_order(queue, 'DC') # multiple modules allowed
    instr['SG']= inst_order(queue, 'SG')[0]
    instr['NA']= inst_order(queue, 'NA')[0]

    # pushing pre-measurement parameters to settings:
    yield owner, sample, tag, instr, corder, comment, dayindex, taskentry, perimeter, queue, renamed_task

    # User-defined Controlling-PARAMETER(s) & -PERIMETER(s) ======================================================================================
    # 1. PERIMETER:
    dcsweepch = perimeter['dcsweepch'] # PENDING: to be deprecated
    z_idle = literal_eval(perimeter['z-idle']) # Idle Z-JSON: {<Channel>: <DC Value>, ... }
    sg_locked = literal_eval(perimeter['sg-locked']) # Locked SG-JSON: {<INSTR>/<ATTR>: <Set LOCK-Waveform>, ... }
    dc_sweep_config = literal_eval(perimeter['sweep-config']) # DC sweep configurations
    current = dc_sweep_config['current']
    # 2. PARAMETER:
    fluxbias, fluxbias_lock = waveform(corder['Flux-Bias']), dict()
    SG_LOCKED, sglocked_bench = dict(), dict()
    xyfreq, xyfreq_lock = waveform(corder['XY-Frequency']), dict()
    xypowa, xypowa_lock = waveform(corder['XY-Power']), dict()
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
    NA = im("pyqum.instrument.machine.%s" %NA_type)
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
    DC_qty = len(instr['DC'])
    DC_type, DC_label, DC, DC_instance = [None]*DC_qty, [None]*DC_qty, [None]*DC_qty, [None]*DC_qty
    for i, channel_set in enumerate(DC_Matrix):
        [DC_type[i], DC_label[i]] = instr['DC'][i].split('_')
        if "DUMMY" not in DC_type[i].upper(): DC[i] = im("pyqum.instrument.machine.%s" %DC_type[i])
        if "opt" not in fluxbias.data: # check if it is in optional-state
            DC_instance[i] = DC[i].Initiate(current=current, which=DC_label[i]) # PENDING option: choose between Voltage / Current output
            DC[i].output(DC_instance[i], 1, channel=dcsweepch)
            # Pre-setting Z-Idle-Channels:
            for key in z_idle.keys(): 
                if i+1==int(key.split('-')[0]):
                    if "lock" not in str(z_idle[key]).lower(): DC[i].sweep(DC_instance[i], z_idle[key], channel=int(key.split('-')[1]), update_settings=dc_sweep_config) # locked to itself
                    else: fluxbias_lock[key] = waveform(z_idle[key].lower().replace("lock",str(fluxbias.count-1))) # locked to fluxbias

    # SG:
    [SG_type, SG_label] = instr['SG'].split('_')
    SG = im("pyqum.instrument.machine.%s" %SG_type)
    if "opt" not in xyfreq.data: # check if it is in optional-state / serious-state
        sgbench = SG.Initiate(which=SG_label)
        SG.rfoutput(sgbench, action=['Set', 1])
        # NOTE: Routine below will only iterate if there's ANY listed locked-SG:
        SGLOCKED_NAME_LIST = [x.split('/')[0] for x in list(sg_locked.keys())[::2]] # /F & /P for every SG
        for SGLOCKED_NAME in SGLOCKED_NAME_LIST:
            [SGLOCKED_type, SGLOCKED_label] = list(sg_locked.keys())[0].split('/')[0].split('_')
            SG_LOCKED[SGLOCKED_NAME] = im("pyqum.instrument.machine.%s" %SGLOCKED_type)
            sglocked_bench[SGLOCKED_NAME] = SG_LOCKED[SGLOCKED_NAME].Initiate(which=SGLOCKED_label)
            SG_LOCKED[SGLOCKED_NAME].rfoutput(sglocked_bench[SGLOCKED_NAME], action=['Set', 1])
            #print("SGLOCKED_NAME "+SGLOCKED_NAME)#Checkpoint
            # 1. PRESET FREQUENCY:
            if "lock" in sg_locked['%s/F'%SGLOCKED_NAME].lower(): xyfreq_lock[SGLOCKED_NAME] = waveform(sg_locked['%s/F'%SGLOCKED_NAME].lower().replace("lock",str(xyfreq.count-1)))
            elif "*" in sg_locked['%s/F'%SGLOCKED_NAME].lower(): print(Fore.WHITE + Back.MAGENTA + "COMING NEW FEATURE of FLEXIBLE C_STRUCTURE ON SG-ATTRIBUTES")
            else: SG_LOCKED[SGLOCKED_NAME].frequency(sglocked_bench[SGLOCKED_NAME], action=['Set', str(sg_locked['%s/F'%SGLOCKED_NAME]) + "GHz"])
            #print("xyfreq_lock[SGLOCKED_NAME]= "+sg_locked['%s/F'%SGLOCKED_NAME].lower().replace("lock",str(xyfreq.count-1)) )#Checkpoint

            # 2. PRESET POWER:
            if "lock" in sg_locked['%s/P'%SGLOCKED_NAME].lower(): xypowa_lock[SGLOCKED_NAME] = waveform(sg_locked['%s/P'%SGLOCKED_NAME].lower().replace("lock",str(xypowa.count-1)))
            elif "*" in sg_locked['%s/P'%SGLOCKED_NAME].lower(): print(Fore.WHITE + Back.MAGENTA + "COMING NEW FEATURE of FLEXIBLE C_STRUCTURE ON SG-ATTRIBUTES")
            else: SG_LOCKED[SGLOCKED_NAME].power(sglocked_bench[SGLOCKED_NAME], action=['Set', str(sg_locked['%s/P'%SGLOCKED_NAME]) + "dBm"])

    # User-defined Measurement-FLOW ==============================================================================================
    
    # 1. Registerring parameter(s)-structure
    if powa_repeat == 1: cstructure = [fluxbias.count, xyfreq.count, xypowa.count, Sparam.count, ifb.count, freq.count, 1] # just single CW
    else: cstructure = [fluxbias.count, xyfreq.count, xypowa.count, Sparam.count, ifb.count, freq.count, powa.count] # take CW average by repeating
    
    # 2. Set previous parameters based on resumepoint: (assimilated into measure-loop for advanced directive onwards, by partially or fully Flexible C-Structure)
    if resumepoint//buffersize_1 > 0:
        caddress = cdatasearch(resumepoint//buffersize_1, cstructure)
        # Only those involved in virtual for-loop need to be pre-set here:
        # Optionals:
        if "opt" not in fluxbias.data: # check if it is in optional-state / serious-state
            DC[0].sweep(DC_instance[0], str(fluxbias.data[caddress[0]]), channel=dcsweepch, update_settings=dc_sweep_config) # A-mode: sweeprate=0.0007 A/s ; V-mode: sweeprate=0.07 V/s 
            # Locking Z-Idle-Channels to Sweeping-Master-Channel:
            for module, channel_set in enumerate(DC_Matrix):
                for key in z_idle.keys():
                    if module+1==int(key.split('-')[0]):
                        if "lock" in str(z_idle[key]).lower(): DC[module].sweep(DC_instance[module], str(fluxbias_lock[key].data[caddress[0]]), channel=int(key.split('-')[1]), update_settings=dc_sweep_config)
        if "opt" not in xyfreq.data: # check if it is in optional-state / serious-state
            SG.frequency(sgbench, action=['Set', str(xyfreq.data[caddress[1]]) + "GHz"])
            SG.power(sgbench, action=['Set', str(xypowa.data[caddress[2]]) + "dBm"])
        # Basics:
        NA.setrace(nabench, Mparam=[Sparam.data[caddress[3]]])
        NA.ifbw(nabench, action=['Set', ifb.data[caddress[4]]])
        NA.cwfreq(nabench, action=['Set', freq.data[caddress[5]]*1e9])

    # 3. Start measuring:
    JOBID = g.queue_jobid_list[0]
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
                    DC[0].sweep(DC_instance[0], str(fluxbias.data[caddress[0]]), channel=dcsweepch, update_settings=dc_sweep_config) # A-mode: sweeprate=0.0007 A/s ; V-mode: sweeprate=0.07 V/s
                    # Locking Z-Idle-Channels to Sweeping-Master-Channel:
                    for module, channel_set in enumerate(DC_Matrix):
                        for key in z_idle.keys():
                            if module+1==int(key.split('-')[0]):
                                if "lock" in str(z_idle[key]).lower(): DC[module].sweep(DC_instance[module], str(fluxbias_lock[key].data[caddress[0]]), channel=int(key.split('-')[1]), update_settings=dc_sweep_config)
            
            if not i%prod(cstructure[2::]): # virtual for-loop using exact-multiples condition
                if "opt" not in xyfreq.data: # check if it is in optional-state
                    SG.frequency(sgbench, action=['Set', str(xyfreq.data[caddress[1]]) + "GHz"])
                    #print("SG.frequency "+str(xyfreq.data[caddress[1]]))#Checkpoint

                    # Lock XY-Frequency to another SG(s) below:
                    for SGLOCKED_NAME in SGLOCKED_NAME_LIST:
                        if "lock" in sg_locked['%s/F'%SGLOCKED_NAME].lower(): SG_LOCKED[SGLOCKED_NAME].frequency(sglocked_bench[SGLOCKED_NAME], action=['Set', str(xyfreq_lock[SGLOCKED_NAME].data[caddress[1]]) + "GHz"])
                        #print(SGLOCKED_NAME +" Lock XY-Frequency " +str(xyfreq_lock[SGLOCKED_NAME].data[caddress[1]]))#Checkpoint

            if not i%prod(cstructure[3::]): # virtual for-loop using exact-multiples condition
                if "opt" not in xypowa.data: # check if it is in optional-state
                    SG.power(sgbench, action=['Set', str(xypowa.data[caddress[2]]) + "dBm"])
                    # Lock XY-Power to another SG(s) below:
                    for SGLOCKED_NAME in SGLOCKED_NAME_LIST:
                        if "lock" in sg_locked['%s/P'%SGLOCKED_NAME].lower(): SG_LOCKED[SGLOCKED_NAME].power(sglocked_bench[SGLOCKED_NAME], action=['Set', str(xypowa_lock[SGLOCKED_NAME].data[caddress[2]]) + "dBm"])

            # Basics:
            if not i%prod(cstructure[4::]): # virtual for-loop using exact-multiples condition
                NA.setrace(nabench, Mparam=[Sparam.data[caddress[3]]])

            if not i%prod(cstructure[5::]): # virtual for-loop using exact-multiples condition
                NA.ifbw(nabench, action=['Set', ifb.data[caddress[4]]])
                # print("set IFB: %s, get IFB: %s" %(ifb.data[caddress[4]],NA.ifbw(nabench)) )

            if not i%prod(cstructure[6::]): # virtual for-loop using exact-multiples condition
                NA.cwfreq(nabench, action=['Set', freq.data[caddress[5]]*1e9])
                # print("set cw-freq: %s, get cw-freq: %s" %(freq.data[caddress[5]]*1e9,NA.cwfreq(nabench)) )

            if powa_repeat > 1:
                NA.power(nabench, action=['Set', '', powa.data[caddress[6]], powa.data[caddress[6]]]) # same as the whole measure-loop
                # print("set power: %s, get power: %s" %(powa.data[caddress[6]],NA.power(nabench)) )

            # start sweeping:
            stat = NA.sweep(nabench) #getting the estimated sweeping time
            #print("Time-taken for this loop would be: %s (%spts)" %(stat[1]['TIME'], stat[1]['POINTS']))
            print("Operation Complete: %s" %bool(NA.measure(nabench)))
            # adjusting display on NA:
            NA.autoscal(nabench)
            # NA.selectrace(nabench, action=['Set', 'para 1 calc 1'])
            data = NA.sdata(nabench)

            # NOTE: Debug anomaly in MXA output data:
            # from pyqum.instrument.analyzer import curve
            # curve(list(range(len(data[0::2]))), data[0::2], '', 'repeat#', 'power (dBm)')

            print(Fore.YELLOW + "\rProgress: %.3f%%" %((i+1)/datasize*buffersize_1*100), end='\r', flush=True)
            jobsinqueue(queue)
            if JOBID in g.queue_jobid_list:
                # print(Fore.YELLOW + "Pushing Data into file...")
                yield data
            else: break

        # Closing all instruments and Queueing out:
        NA.close(nabench, which=NA_label)
        if "opt" not in xyfreq.data: # check if it is in optional-state
            SG.rfoutput(sgbench, action=['Set', 0])
            SG.close(sgbench, SG_label, False)
            for SGLOCKED_NAME in SGLOCKED_NAME_LIST:
                SG_LOCKED[SGLOCKED_NAME].rfoutput(sglocked_bench[SGLOCKED_NAME], action=['Set', 0])
                SG_LOCKED[SGLOCKED_NAME].close(sglocked_bench[SGLOCKED_NAME], SGLOCKED_NAME.split("_")[1], False)
        if "opt" not in fluxbias.data: # check if it is in optional-state
            for i_module, channel_set in enumerate(DC_Matrix):
                DC[i_module].output(DC_instance[i_module], 0)
                DC[i_module].close(DC_instance[i_module], reset=True, which=DC_label[i_module])
        if JOBID in g.queue_jobid_list:
            qout(queue, g.queue_jobid_list[0],g.user['username'])
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


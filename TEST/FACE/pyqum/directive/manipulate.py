'''ALL QuBit Manipulations: Single_Qubit, Qubits, RB, QPU'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # instrument-module's name e.g. ENA, PSG, YOKO

from time import time, sleep
from copy import copy, deepcopy
from json import loads, dumps
from numpy import prod, array, mean, ceil, floor, sin, cos
from numexpr import evaluate as eval
from flask import session, g

from importlib import import_module as im
from pyqum.instrument.logger import settings, get_status, set_status, jobsinqueue, qout, job_update_perimeter
from pyqum.instrument.toolbox import cdatasearch, waveform, find_in_list
from pyqum.instrument.composer import pulser
from pyqum.instrument.analyzer import pulse_baseband
from pyqum.instrument.reader import inst_order, macer

# from asqpu.hardware_information import *

__author__ = "Teik-Hui Lee"
__copyright__ = "Copyright 2019, The Pyqum Project"
__credits__ = ["Chii-Dong Chen"]
__license__ = "GPL"
__version__ = "beta3"
__email__ = "teikhui@phys.sinica.edu.tw"
__status__ = "development"

# Qubit-Control:
# **********************************************************************************************************************************************************
@settings(2) # data-density
def QuCTRL(owner, tag="", corder={}, comment='', dayindex='', taskentry=0, resumepoint=0, instr={}, perimeter={}, renamed_task=''):
    '''
    renamed_task: Single_Qubit, Qubits, RB, QPU
    Time-domain Pulse measurement:\n
    SCORES (SCripted ORchestration of Entanglement & Superposition) is a scripted pulse instruction language for running Quantum Algorithm.\n
    perimeter.keys() = ['XY-LO-Power', 'RO-LO-Power', 'SCORE-NS', 'SCORE-JSON', 'R-JSON', 'RECORD-SUM', 'RECORD_TIME_NS', 'READOUTYPE']\n
    C-Structure = ['Flux-Bias', 'XY-LO-Frequency', 'RO-LO-Frequency'] + [...R-parameter(s)...]\n
    Differ from previous directive, this version onward, our stored data will assume the following form:\n
    DATA = STRUCTURE + BUFFER (Thus ALL part of Structure will now participate in measure-loop)
    '''

    # User-specific settings in JSON:
    sample = get_status("MSSN")[session['user_name']]['sample']
    queue = get_status("MSSN")[session['user_name']]['queue']
    print(Back.GREEN + Fore.BLUE + "User [%s] is measuring sample [%s] on queue [%s]" %(session['user_name'],sample,queue))

    # Check TASK LEVEL:
    Exp = macer()
    Experiments = Exp.experiment_list
    Exp.close()
    if renamed_task in Experiments: TASK_LEVEL = "EXP" # EXPERT
    else: TASK_LEVEL = "MAC" # BASIC / LOW-LEVEL

    # Loading Channel-Settings:
    CH_Matrix = inst_order(queue, 'CH')
    DAC_CH_Matrix = CH_Matrix['DAC']
    SG_CH_Matrix = CH_Matrix['SG']
    DC_CH_Matrix = CH_Matrix['DC']
    ROLE_Matrix = inst_order(queue, 'ROLE')
    DAC_ROLE_Matrix = ROLE_Matrix['DAC']
    SG_ROLE_Matrix = ROLE_Matrix['SG']
    DC_ROLE_Matrix = ROLE_Matrix['DC']
    
    # Find Address in the Listified Multi-dimensional Matrix as <MODule>-<CHannel>
    try: RO_addr = find_in_list(DAC_ROLE_Matrix, 'I1')
    except: RO_addr = 'OPT' # Optionized if not present
    try: XY_addr = find_in_list(DAC_ROLE_Matrix, 'X1')
    except: XY_addr = 'OPT' # Optionized if not present
    print(Fore.YELLOW + "RO_addr: %s, XY_addr: %s" %(RO_addr,XY_addr))

    # Queue-specific instrument-package in list:
    instr['DAC']= inst_order(queue, 'DAC')
    instr['SG']= inst_order(queue, 'SG')
    instr['DC']= inst_order(queue, 'DC')
    instr['ADC']= inst_order(queue, 'ADC')[0] # only 1 instrument allowed (No multiplexing yet)

    # Packing instrument-specific perimeter from database:
    perimeter.update(dict(TIME_RESOLUTION_NS=loads(g.machspecs[instr['ADC']])['TIME_RESOLUTION_NS']))
    perimeter.update(dict(CLOCK_HZ=loads(g.machspecs[instr['DAC'][0]])['CLOCK_HZ']))
    # Packing wiring-specific perimeter from database:
    perimeter.update(dict(CH_Matrix=dumps(CH_Matrix)))
    perimeter.update(dict(ROLE_Matrix=dumps(ROLE_Matrix)))

    # pushing pre-measurement parameters to settings:
    yield owner, sample, tag, instr, corder, comment, dayindex, taskentry, perimeter, queue, renamed_task

    # ***USER_DEFINED*** Controlling-PARAMETER(s) ======================================================================================
    # 1a. Instruments' specs:
    TIME_RESOLUTION_NS = int(perimeter['TIME_RESOLUTION_NS'])
    CLOCK_HZ = float(perimeter['CLOCK_HZ'])
    # 1b. DSP perimeter(s)
    digital_homodyne = perimeter['DIGIHOME']
    ifreqcorrection_kHz = float(perimeter['IF_ALIGN_KHZ'])
    # 1c. Basic perimeter(s): # previously: config = corder['C-Config']
    biasmode = bool(int(perimeter['BIASMODE']))
    xypowa = perimeter['XY-LO-Power']
    ropowa = perimeter['RO-LO-Power']
    trigger_delay_ns = int(perimeter['TRIGGER_DELAY_NS'])
    recordsum = int(perimeter['RECORD-SUM'])
    recordtime_ns = int(perimeter['RECORD_TIME_NS']) # min:1280ns, step:128ns
    readoutype = perimeter['READOUTYPE']
    # 1d. SCORE-, MACE- & R-JSON perimeters:
    SCORE_TEMPLATE = perimeter['SCORE-JSON'] # already a DICT
    MACE_TEMPLATE = perimeter['MACE-JSON'] # already a DICT
    RJSON = loads(perimeter['R-JSON'].replace("'",'"'))
    # 1e. Derived perimeter(s) from above:
    ifperiod = pulser(score=SCORE_TEMPLATE['CH%s'%RO_addr], dt=1).totaltime
    ##JACKY 
    print(Fore.BLUE +f"totaltime(ifperiod) {ifperiod}")
    print(Fore.BLUE +f"SCORE_TEMPLATE {SCORE_TEMPLATE['CH%s'%RO_addr]}")

    RO_Compensate_MHz = -pulser(score=SCORE_TEMPLATE['CH%s'%RO_addr]).IF_MHz_rotation # working with RO-MOD (up or down)
    XY_Compensate_MHz = -pulser(score=SCORE_TEMPLATE['CH%s'%XY_addr]).IF_MHz_rotation # working with XY-MOD (up or down)
    print(Fore.YELLOW + "RO_Compensate_MHz: %s, XY_Compensate_MHz: %s" %(RO_Compensate_MHz,XY_Compensate_MHz))
    skipoints = 0
    try: 
        if (digital_homodyne=="i_digital_homodyne" or digital_homodyne=="q_digital_homodyne"): skipoints = int(ceil( 1 / abs(RO_Compensate_MHz) * 1000 ))
    except: 
        print(Fore.RED + "WARNING: INFINITE INTEGRATION IS NOT PRACTICAL!")
    # print(Fore.CYAN + "Skipping first %s point(s)" %skipoints)

    # 2a. Basic corder / parameter(s):
    structure = corder['C-Structure'] + [k for k in RJSON.keys()]
    # fluxbias = waveform(corder['Flux-Bias']) # idx-0
    # xyfreq = waveform(corder['XY-LO-Frequency']) # idx-1
    # rofreq = waveform(corder['RO-LO-Frequency']) # idx-2
    for k in RJSON.keys(): corder[k] = RJSON[k] # update corder with R-parameters # idx-<3,4,5...>
    # 2b. Prepare R-waveform object for pulse-instructions
    R_waveform = {}
    for k in RJSON.keys(): R_waveform[k] = waveform(RJSON[k])
    
    # Pre-loop settings:
    # DC for PA:
    DC_qty = len(instr['DC'])
    DC_type, DC_label, DC, DC_instance = [None]*DC_qty, [None]*DC_qty, [None]*DC_qty, [None]*DC_qty
    for i, channel_set in enumerate(DC_CH_Matrix):
        [DC_type[i], DC_label[i]] = instr['DC'][i].split('_')
        DC[i] = im("pyqum.instrument.machine.%s" %DC_type[i])
        DC_instance[i] = DC[i].Initiate(which=DC_label[i]) # Only voltage mode (default) available / allowed in QPC
        for channel in channel_set:
            DC[i].sweep(DC_instance[i], str(0), channel=channel)
            DC[i].output(DC_instance[i], 1)

    # SG for [XY, RO]:
    SG_qty = len(instr['SG'])
    SG_type, SG_label, SG, SG_instance = [None]*SG_qty, [None]*SG_qty, [None]*SG_qty, [None]*SG_qty
    for i, channel_set in enumerate(SG_CH_Matrix):
        [SG_type[i], SG_label[i]] = instr['SG'][i].split('_')
        SG[i] = im("pyqum.instrument.machine.%s" %SG_type[i])
        SG_instance[i] = SG[i].Initiate(which=SG_label[i])
        for channel in channel_set:
            SG[i].power(SG_instance[i], action=['Set_%s'%channel, str(-17) + ""]) # UNIT dBm NOT WORKING IN DDSLO
            SG[i].rfoutput(SG_instance[i], action=['Set_%s'%channel, 1])

    # DAC for [RO, XY]:
    DAC_qty = len(instr['DAC'])
    DAC_type, DAC_label, DAC, DAC_instance = [None]*DAC_qty, [None]*DAC_qty, [None]*DAC_qty, [None]*DAC_qty

    for i, channel_set in enumerate(DAC_CH_Matrix):
        [DAC_type[i], DAC_label[i]] = instr['DAC'][i].split('_')
        DAC[i] = im("pyqum.instrument.machine.%s" %DAC_type[i])
        DAC_instance[i] = DAC[i].Initiate(which=DAC_label[i])
        DAC[i].clock(DAC_instance[i], action=['Set', 'EFIXed', CLOCK_HZ])
        DAC[i].clear_waveform(DAC_instance[i],'all')
        DAC[i].alloff(DAC_instance[i], action=['Set',1])
        
        # PENDING: Extract the settings from the machine database instead.
        if i==0: 
            markeroption = 7
            update_settings = dict(Master=True, trigbyPXI=2, markeroption=7) # First-in-line = Master (usually RO giving Trigger through CH-4)
        else: 
            markeroption = 0
            update_settings = dict(Master=False, trigbyPXI=2)
        print(Fore.CYAN + "%s's setting: %s" %(instr['DAC'][i], update_settings))

        '''Prepare DAC:'''
        dt = round(1/float(DAC[i].clock(DAC_instance[i])[1]['SRATe'])/1e-9, 2)
        pulseq = pulser(dt=dt, clock_multiples=1, score="ns=%s"%ifperiod)
        # pulseq = pulser(dt, clock_multiples=1, score="ns=300000;FLAT/,3000,0.01;")
        pulseq.song()
        for channel in channel_set:
            DAC[i].prepare_DAC(DAC_instance[i], int(channel), pulseq.totalpoints, update_settings=update_settings)
            ## JACKY
            print(Fore.BLUE +f"pulseq.totalpoints {pulseq.totalpoints}")
        for channel in channel_set:
            DAC[i].compose_DAC(DAC_instance[i], int(channel), pulseq.music, [], markeroption) # we don't need marker yet initially
            print(Fore.BLUE +f"len(pulseq.music) {len(pulseq.music)}")

        # Turn on all 4 channels:
        DAC[i].alloff(DAC_instance[i], action=['Set',0])
        DAC[i].ready(DAC_instance[i])
        DAC[i].play(DAC_instance[i])
    
    # ADC:
    [ADC_type, ADC_label] = instr['ADC'].split('_')
    ADC = im("pyqum.instrument.machine.%s" %ADC_type)
    adca = ADC.Initiate(which=ADC_label)
    '''Prepare ADC:'''
    TOTAL_POINTS = round(recordtime_ns / TIME_RESOLUTION_NS)
    update_items = dict( triggerDelay_sec=trigger_delay_ns*1e-9, TOTAL_POINTS=TOTAL_POINTS, NUM_CYCLES=recordsum, PXI=-13 ) # HARDWIRED to receive trigger from the front-panel EXT.
    ADC.ConfigureBoard(adca, update_items)
    

    # Buffer-size for lowest-bound data-collecting instrument:
    if readoutype == 'one-shot': # for fidelity measurement
        buffersize = recordsum * 2 # data-density of 2 due to IQ
        print("Buffer-size: %s" %buffersize)
    else: # by default we usually take average
        buffersize = TOTAL_POINTS * 2 # data-density of 2 due to IQ
        print("Buffer-size: %s" %buffersize)
    # Total data points to be saved into file:
    datasize = int(prod([waveform(corder[param]).count for param in structure], dtype='uint64')) * buffersize
    print("data size: %s" %datasize)

    # User-defined Measurement-FLOW ==============================================================================================
    
    # 1. Registerring parameter(s)-structure
    cstructure = [waveform(corder[param]).count for param in structure] # new version: separation between structure & buffer

    # 2. Start measuring:
    JOBID = g.queue_jobid_list[0]
    job_update_perimeter(JOBID, perimeter)
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
            MACE_DEFINED = deepcopy(MACE_TEMPLATE)
            for j in range(len(cstructure)): # new version: all parameters in R-JSON
                
                if TASK_LEVEL == "MAC":
                    # 1. DAC's SCORE-UPDATE by R-JSON:
                    for i_slot_order, channel_set in enumerate(DAC_CH_Matrix):
                        for ch in channel_set:
                            dach_address = "%s-%s" %(i_slot_order+1,ch)
                            if ">" in structure[j]: # for locked variables with customized math expression:
                                math_expression = structure[j].split(">")[1] # Algebraic initially
                                for R_KEY in structure[j].split(">")[0].replace(" ","").split(","):
                                    math_expression = math_expression.replace( R_KEY, str(R_waveform[R_KEY].data[caddress[structure.index(R_KEY)]]) )
                                if not channel_set.index(ch): print(Fore.LIGHTBLUE_EX + "CH-%s: STRUCTURE LOCKED AT IDX-%s: %s -> %s" %(ch, j, structure[j], math_expression))
                                Score_Var_Update = eval(math_expression) # evaluate numpy-supported expression
                            else: # for usual variables
                                Score_Var_Update = R_waveform[structure[j]].data[caddress[j]]
                            SCORE_DEFINED['CH%s'%dach_address] = SCORE_DEFINED['CH%s'%dach_address].replace("{%s}"%structure[j], str(Score_Var_Update))

                    # 2. SG's MACE-UPDATE by R-JSON:


                    # 3. DC's MACE-UPDATE by R-JSON:

                if TASK_LEVEL == "EXP": pass
                    # 3.x EXP's MACE-UPDATE by R-JSON:
                    # NOTE: PUT ASQPU HERE


            # print(Fore.YELLOW + "DEFINED SCORE-CH1: %s" %(SCORE_DEFINED['CH1']))
            # IN THE FUTURE: HVI-ROUTINE STARTS HERE:

            
            # Basic MAC Control (Every-loop)

            # 1. DC


            # 2. SG

            
            # Basic CHANNEL Control (Pulse Injection)
            # DAC
            for i_slot_order, channel_set in enumerate(DAC_CH_Matrix):
                # PENDING: Extract the settings from the machine database instead.
                if i_slot_order==0: update_settings = dict(Master=True, clearQ=int(bool(len(channel_set)==4)) ) # First-in-line = Master
                else: update_settings = dict(Master=False, clearQ=int(bool(len(channel_set)==4)) ) # NOTE: manually write stalking-envelop-SCORE for CH4 to drive PIN-SWITCH

                for ch in channel_set:
                    
                    if TASK_LEVEL == "MAC":
                        dach_address = "%s-%s" %(i_slot_order+1,ch)
                        pulseq = pulser(dt=dt, clock_multiples=1, score=SCORE_DEFINED['CH%s'%dach_address])
                        pulseq.song()
                        CH_Pulse_SEQ = pulseq.music

                    if TASK_LEVEL == "EXP":
                        CH_Pulse_SEQ = ["ASQPU"]

                        
                    '''
                    NOTE: 
                    TKAWG's marker (number(s)) = SDAWG's markeroption
                    1-4 for TKAWG: ODD-Channel for ARRA-PIN-SWITCH, EVEN-Channel for TRIGGER PURPOSE; RO-TRIGGER: MKR-1: ALZDG, MKR-2: MXA; XY-TRIGGER: MKR-1: MXA, MKR-2: SCOPE
                    7 for SDAWG: PIN-Switch on MixerBox
                    0 for BOTH: disabled.
                    '''
                    # PENDING: edittable markeroption instead of just "2":
                    if (i_slot_order==0) and ("SDAWG" in DAC_type[i_slot_order]): marker = 7
                    else: marker = 2 # for compatibility with TKAWG

                    DAC[i_slot_order].compose_DAC(DAC_instance[i_slot_order], int(ch), CH_Pulse_SEQ, pulseq.envelope, marker, update_settings=update_settings) # PENDING: Option to turn ON PINSW for SDAWG (default is OFF)
                    print(Fore.BLUE +f"RUN len(CH_Pulse_SEQ) {len(CH_Pulse_SEQ)}")

                DAC[i_slot_order].ready(DAC_instance[i_slot_order])
                print('Waveform from Slot-%s is Ready!'%(i_slot_order+1))
                
            # Basic Readout (Buffer Every-loop):
            # ADC 
            DATA = ADC.AcquireData(adca, recordtime_ns*1e-9, recordsum)[0]
            # POST PROCESSING
            try:
                # TIME EVOLUTION / FIDELITY TEST:
                if readoutype == 'one-shot':
                    DATA = DATA.reshape([recordsum,TOTAL_POINTS*2])
                    if digital_homodyne != "original": 
                        for r in range(recordsum):
                            trace_I, trace_Q = DATA[r,:].reshape((TOTAL_POINTS, 2)).transpose()[0], DATA[r,:].reshape((TOTAL_POINTS, 2)).transpose()[1]
                            trace_I, trace_Q = pulse_baseband(digital_homodyne, trace_I, trace_Q, RO_Compensate_MHz, ifreqcorrection_kHz, dt=TIME_RESOLUTION_NS)
                            DATA[r,:] = array([trace_I, trace_Q]).reshape(2*TOTAL_POINTS) # back to interleaved IQ-Data
                            if not r%1000: print(Fore.YELLOW + "Shooting %s times" %(r+1))
                    DATA = mean(DATA.reshape([recordsum*2,TOTAL_POINTS])[:,skipoints:], axis=1)
                    print(Fore.BLUE + "DATA of size %s is ready to be saved" %len(DATA))
                else: # by default
                    DATA = mean(DATA.reshape([recordsum,TOTAL_POINTS*2]), axis=0)
                    if digital_homodyne != "original": 
                        trace_I, trace_Q = DATA.reshape((TOTAL_POINTS, 2)).transpose()[0], DATA.reshape((TOTAL_POINTS, 2)).transpose()[1]
                        trace_I, trace_Q = pulse_baseband(digital_homodyne, trace_I, trace_Q, RO_Compensate_MHz, ifreqcorrection_kHz, dt=TIME_RESOLUTION_NS)
                        DATA = array([trace_I, trace_Q]).transpose().reshape(TOTAL_POINTS*2) # back to interleaved IQ-Data
            
            except(ValueError):
                # raise # PENDING: UPDATE TIMSUM MISMATCH LIST
                print(Fore.RED + "Check ALZDG OPT_DMA_BUFFER!")
                break # proceed to close all & queue out
            
            # print("Operation Complete")
            print(Fore.YELLOW + "\rProgress-(%s): %.3f%%" %((i+1), (i+1)/datasize*buffersize*100), end='\r', flush=True)			
            
            jobsinqueue(queue)
            if JOBID in g.queue_jobid_list:
                # print(Fore.YELLOW + "Pushing Data into file...")
                yield list(DATA)
            else: break # proceed to close all & queue out

        # CLOSING ALL MAC:
        ADC.close(adca, which=ADC_label)
        for i_slot_order, channel_set in enumerate(DAC_CH_Matrix):
            DAC[i_slot_order].alloff(DAC_instance[i_slot_order], action=['Set',1])
            DAC[i_slot_order].close(DAC_instance[i_slot_order], which=DAC_label[i_slot_order])
        for i, channel_set in enumerate(SG_CH_Matrix):
            for channel in channel_set: SG[i].rfoutput(SG_instance[i], action=['Set_%s'%channel, 0])
            SG[i].close(SG_instance[i], SG_label[i], False)
        for i, channel_set in enumerate(DC_CH_Matrix): DC[i].close(DC_instance[i], reset=True, which=DC_label[i])

        if JOBID in g.queue_jobid_list:
            qout(queue, g.queue_jobid_list[0],g.user['username'])
        break

    return

# 2. Multiple-Qubits Control: (Updated on 2021-Nov-5)
# **********************************************************************************************************************************************************
@settings(2) # data-density
def Qubits(owner, tag="", corder={}, comment='', dayindex='', taskentry=0, resumepoint=0, instr={}, perimeter={}, renamed_task='Qubits'):
    '''
    For Multiple Qubits:
    '''

    Single_Qubit(owner, tag, corder, comment, dayindex, taskentry, resumepoint, instr, perimeter, renamed_task)

    return

# 3. QPU Operations: (Updated on 2022/09/01, Not online)
# **********************************************************************************************************************************************************
import qpu.backend.circuit as bec
from pandas import DataFrame
import qpu.backend.phychannel as pch
import qpu.backend.component as qcp
from pyqum import get_db, close_db

@settings(2) # data-density
def QPU(owner, tag="", corder={}, comment='', dayindex='', taskentry=0, resumepoint=0, instr={}, perimeter={}, renamed_task='user-defined'):

    '''
    For QPU operations:
    1. Randomized Benchmarking
    '''
    ## TODO get wiring and spec from database
    sname = ""
    db = get_db()
    sample_cv = db.execute(
        'SELECT s.id, author_id, samplename, specifications, location, level, description, registered, co_authors, history'
        ' FROM sample s JOIN user u ON s.author_id = u.id'
        ' WHERE s.samplename = ?',
        (sname,)
    ).fetchone()
    sample_cv = dict(sample_cv) # convert sqlite3.row into dictionary for this select format
    close_db()
    mybec = bec.BackendCircuit()
    loc = sample_cv["location"]
    wiring_info = loc.split("===")
    dict_list = eval(wiring_info[0])
    channels = []
    for ch in dict_list:
        channels.append( pch.from_dict( ch ) )

    mybec._channels = channels

    mybec.qc_relation = DataFrame.from_dict(eval(wiring_info[1]))
    mybec.q_reg = eval(wiring_info[2])
    qpc_dict = mybec.to_qpc()

    specs = sample_cv["specifications"]
    spec_list = eval(specs)
    qComps = []
    for qc in spec_list:
        #print(ch)
        qComps.append( qcp.from_dict( qc ) )
    mybec._qComps = qComps

    import qpu.application as qapp
    d_setting = qapp.get_SQRB_device_setting( mybec, 5, 0, True  ) ## TODO get RB MACER parameters
    print(d_setting)
    for dcategory in d_setting.keys():
        print(dcategory, d_setting[dcategory].keys())

    # Calling QPU -> Dict: {"Category": ["Device-name": ["<parameter>": "<value>"]]}
    QuCTRL(owner, tag, corder, comment, dayindex, taskentry, resumepoint, instr, perimeter, renamed_task)

    return





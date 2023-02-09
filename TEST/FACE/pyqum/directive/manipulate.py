'''ALL QuBit Manipulations: Single_Qubit, Qubits, RB, QPU'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # instrument-module's name e.g. ENA, PSG, YOKO

from traceback import format_exc
from time import time, sleep
from copy import copy, deepcopy
from json import loads, dumps
from numpy import prod, array, mean, ceil, moveaxis, linspace, outer, ones, divide
from numexpr import evaluate
from flask import session, g

from importlib import import_module as im
from pyqum.instrument.logger import settings, get_status, set_status, jobsinqueue, qout, job_update_perimeter
from pyqum.instrument.toolbox import cdatasearch, waveform, find_in_list
from pyqum.instrument.composer import pulser
from pyqum.instrument.analyzer import pulse_baseband
from pyqum.instrument.reader import inst_order, macer
from pyqum import get_db, close_db

import qpu.application as qapp
import qpu.backend.circuit.backendcircuit as bec
from pandas import DataFrame
import qpu.backend.phychannel as pch
import qpu.backend.component as qcp

# from asqpu.hardware_information import *

__author__ = "Teik-Hui Lee"
__copyright__ = "Copyright 2019, The Pyqum Project"
__credits__ = ["Chii-Dong Chen"]
__license__ = "GPL"
__version__ = "beta3"
__email__ = "teikhui@phys.sinica.edu.tw"
__status__ = "development"


def get_plain_SCORE(Var_SCORE_Script, RJSON):
    '''
    Get parameters from the SCORE-header with variables inside.
    Var_SCORE_Script with variables that can be accessed from RJSON, to be cleansed.
    '''

    # Extract Pulse-related Settings ONLY:
    rjson_struct = [k for k in RJSON.keys() if k in Var_SCORE_Script] # 1st SCORE only

    # Prepare R-waveform object for pulse-instructions
    R_Max_value = {}
    for k in rjson_struct: R_Max_value[k] = max(waveform(RJSON[k]).data, key=abs) # PICK THE MAX PARAMETER VALUE!

    # UPDATE EVERY {R}
    for j in range(len(rjson_struct)):
        if ">" in rjson_struct[j]: # For Locked variables with customized math expression:
            math_expression = rjson_struct[j].split(">")[1] # Algebraic initially
            for R_KEY in rjson_struct[j].split(">")[0].replace(" ","").split(","):
                math_expression = math_expression.replace( R_KEY, str(R_Max_value[R_KEY]) )
            Script_Var_Update = evaluate(math_expression) # evaluate numpy-supported expression
            print(Fore.LIGHTBLUE_EX + "STRUCTURE LOCKED AT IDX-%s: %s -> %s -> %s" %(j, rjson_struct[j], math_expression, Script_Var_Update))
        else: # for usual variables
            Script_Var_Update = R_Max_value[rjson_struct[j]]
                    
        Var_SCORE_Script = Var_SCORE_Script.replace("{%s}"%rjson_struct[j], str(Script_Var_Update))

    print(Fore.YELLOW + Back.BLUE + "Plain SCORE_Script: %s" %Var_SCORE_Script)
    return Var_SCORE_Script

def get_Qubit_CV (samplename)->bec.BackendCircuit:
    
    db = get_db()
    sample_cv = db.execute(
        'SELECT s.id, author_id, samplename, specifications, location, level, description, registered, co_authors, history'
        ' FROM sample s JOIN user u ON s.author_id = u.id'
        ' WHERE s.samplename = ?',
        (samplename,)
    ).fetchone()
    sample_cv = dict(sample_cv) # convert sqlite3.row into dictionary for this select format
    close_db()
    mybec = bec.BackendCircuit()
    loc = sample_cv["location"]
    wiring_info = loc.split("===")
    print(wiring_info[0])
    dict_list = eval(wiring_info[0])
    channels = []
    for ch in dict_list: channels.append( pch.from_dict( ch ) )

    mybec._channels = channels
    mybec.qc_relation = DataFrame.from_dict(eval(wiring_info[1]))
    mybec.q_reg = eval(wiring_info[2])
    
    specs = sample_cv["specifications"]
    spec_list = eval(specs)
    qComps = []
    for qc in spec_list:
        #print(ch)
        qComps.append( qcp.from_dict( qc ) )
    mybec._qComps = qComps
    # mybec.
    
    return mybec

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

    Device_Categories = ["DAC", "SG", "DC"] # PENDING: ADC

    # User-specific settings in JSON:
    sample = get_status("MSSN")[session['user_name']]['sample']
    queue = get_status("MSSN")[session['user_name']]['queue']
    print(Back.GREEN + Fore.BLUE + "User [%s] is measuring sample [%s] on queue [%s]" %(session['user_name'],sample,queue))

    # Check TASK LEVEL:
    Exp = macer()
    Experiments = Exp.experiment_list
    Exp.close()
    if renamed_task in Experiments: 
        TASK_LEVEL = "EXP" # EXPERT
        Sample_Backend = get_Qubit_CV(sample) # Extract Qubit-CV
        Sample_Backend.dt = 1
    else: 
        TASK_LEVEL = "MAC" # BASIC / LOW-LEVEL

    # Loading Channel-Settings:
    CH_Matrix = inst_order(queue, 'CH')
    DAC_CH_Matrix = CH_Matrix['DAC']
    SG_CH_Matrix = CH_Matrix['SG']
    try: DC_CH_Matrix = CH_Matrix['DC']
    except: DC_CH_Matrix = [[]]
    ROLE_Matrix = inst_order(queue, 'ROLE')
    DAC_ROLE_Matrix = ROLE_Matrix['DAC']
    SG_ROLE_Matrix = ROLE_Matrix['SG']
    try: DC_ROLE_Matrix = ROLE_Matrix['DC']
    except: DC_ROLE_Matrix = [[]]
    
    # Find Address in the Listified Multi-dimensional Matrix as <MODule>-<CHannel>
    try: RO_addr = find_in_list(DAC_ROLE_Matrix, 'RO')
    except: RO_addr = 'OPT' # Optionized if not present
    try: XY_addr = find_in_list(DAC_ROLE_Matrix, 'XY')
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
    # biasmode = bool(int(perimeter['BIASMODE']))
    # xypowa = perimeter['XY-LO-Power']
    # ropowa = perimeter['RO-LO-Power']
    trigger_delay_ns = int(perimeter['TRIGGER_DELAY_NS'])
    recordsum = int(perimeter['RECORD-SUM'])
    recordtime_ns = int(perimeter['RECORD_TIME_NS']) # min:1280ns, step:128ns
    readoutype = perimeter['READOUTYPE']
    # 1d. SCORE-, MACE- & R-JSON perimeters:
    SCORE_TEMPLATE = perimeter['SCORE-JSON'] # already a DICT
    MACE_TEMPLATE = perimeter['MACE-JSON'] # already a DICT
    RJSON = loads(perimeter['R-JSON'].replace("'",'"'))
    # 1e. Derived perimeter(s) from above:
    if TASK_LEVEL == "MAC":
        ifperiod = pulser(score=get_plain_SCORE(SCORE_TEMPLATE['CH%s'%RO_addr], RJSON), dt=(1e9/CLOCK_HZ)).totaltime
    if TASK_LEVEL == "EXP":
        # for i, qubit_id in enumerate(Sample_Backend.q_reg["qubit"]):
        d_setting = qapp.get_SQRB_device_setting( Sample_Backend, 0, 0, True ) # PENDING: MORE unified function from ASQPU?
        ifperiod = d_setting['total_time']
    ##JACKY 
    print(Fore.BLUE +f"totaltime(ifperiod) {ifperiod}")
    
    if TASK_LEVEL == "MAC":
        RO_Compensate_MHz = -pulser(score=get_plain_SCORE(SCORE_TEMPLATE['CH%s'%RO_addr], RJSON)).IF_MHz_rotation # working with RO-MOD (up or down)
        XY_Compensate_MHz = -pulser(score=get_plain_SCORE(SCORE_TEMPLATE['CH%s'%XY_addr], RJSON)).IF_MHz_rotation # working with XY-MOD (up or down)
        DDC_RO_Compensate_MHz = RO_Compensate_MHz
        print(Fore.YELLOW + "RO_Compensate_MHz: %s, XY_Compensate_MHz: %s" %(RO_Compensate_MHz,XY_Compensate_MHz))
    if TASK_LEVEL == "EXP":
        RO_Compensate_MHz = 0
        XY_Compensate_MHz = 0
        # For Digital Down Conversion:
        q_name = Sample_Backend.q_reg["qubit"][0]
        channel_RO = Sample_Backend.get_channel_qPort( q_name, "ro_in")
        DDC_RO_Compensate_MHz = -channel_RO.paras["freq_IF"] *1000
        # channel_XY = Sample_Backend.get_channel_qPort( q_name, "xy")
        # XY_Compensate_MHz = channel_XY.paras["paras"]["freq_IF"]
    
    skipoints = 0
    if (digital_homodyne=="i_digital_homodyne" or digital_homodyne=="q_digital_homodyne"): 
        try: skipoints = int(ceil( 1 / abs(DDC_RO_Compensate_MHz) * 1000 ))
        except: print(Fore.RED + "WARNING: INFINITE INTEGRATION IS NOT PRACTICAL!")
    print(Fore.CYAN + "Skipping first %s point(s)" %skipoints)

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
    for i_slot, channel_set in enumerate(DC_CH_Matrix):
        [DC_type[i_slot], DC_label[i_slot]] = instr['DC'][i_slot].split('_')
        if "DUMMY" in DC_type[i_slot]: 
            pass
        else:
            DC[i_slot] = im("pyqum.instrument.machine.%s" %DC_type[i_slot])
            DC_instance[i_slot] = DC[i_slot].Initiate(which=DC_label[i_slot]) # Only voltage mode (default) available / allowed in QPC
            for channel in channel_set:
                DC[i_slot].sweep(DC_instance[i_slot], str(0), channel=channel)
                # DC[i_slot].output(DC_instance[i_slot], 1, channel)

    # SG for [XY, RO]:
    SG_qty = len(instr['SG'])
    SG_type, SG_label, SG, SG_instance = [None]*SG_qty, [None]*SG_qty, [None]*SG_qty, [None]*SG_qty
    for i_slot, channel_set in enumerate(SG_CH_Matrix):
        [SG_type[i_slot], SG_label[i_slot]] = instr['SG'][i_slot].split('_')
        SG[i_slot] = im("pyqum.instrument.machine.%s" %SG_type[i_slot])
        SG_instance[i_slot] = SG[i_slot].Initiate(which=SG_label[i_slot])
        for channel in channel_set:
            SG[i_slot].power(SG_instance[i_slot], action=['Set_%s'%channel, str(-17) + ""]) # UNIT dBm NOT WORKING IN DDSLO
            # SG[i_slot].rfoutput(SG_instance[i_slot], action=['Set_%s'%channel, 1])

    # DAC for [RO, XY]:
    DAC_qty = len(instr['DAC'])
    DAC_type, DAC_label, DAC, DAC_instance = [None]*DAC_qty, [None]*DAC_qty, [None]*DAC_qty, [None]*DAC_qty

    for i_slot, channel_set in enumerate(DAC_CH_Matrix):
        [DAC_type[i_slot], DAC_label[i_slot]] = instr['DAC'][i_slot].split('_')
        DAC[i_slot] = im("pyqum.instrument.machine.%s" %DAC_type[i_slot])
        DAC_instance[i_slot] = DAC[i_slot].Initiate(which=DAC_label[i_slot])
        DAC[i_slot].clock(DAC_instance[i_slot], action=['Set', 'EFIXed', CLOCK_HZ])
        DAC[i_slot].clear_waveform(DAC_instance[i_slot],'all')
        DAC[i_slot].alloff(DAC_instance[i_slot], action=['Set',1])
        
        # PENDING: Extract the settings from the machine database instead.
        if i_slot==0: 
            markeroption = 7
            update_settings = dict(Master=True, trigbyPXI=2, markeroption=7) # First-in-line = Master (usually RO giving Trigger through CH-4)
        else: 
            markeroption = 0
            update_settings = dict(Master=False, trigbyPXI=2)
        print(Fore.CYAN + "%s's setting: %s" %(instr['DAC'][i_slot], update_settings))

        '''Prepare DAC:'''
        dt = round(1/float(DAC[i_slot].clock(DAC_instance[i_slot])[1]['SRATe'])/1e-9, 2)
        pulseq = pulser(dt=dt, clock_multiples=1, score="ns=%s"%ifperiod)
        pulseq.song()
        DAC_total_points, DAC_idle_music = pulseq.totalpoints, pulseq.music
        for channel in channel_set:
            DAC[i_slot].prepare_DAC(DAC_instance[i_slot], int(channel), DAC_total_points, update_settings=update_settings)
            ## JACKY
            print(Fore.BLUE +f"DAC_total_points: {DAC_total_points}")
        for channel in channel_set:
            # NOTE: TKAWG: we don't need the right marker yet initially.
            # NOTE: SDAWG: default clearQ doesn't matter much for pre-composition.
            DAC[i_slot].compose_DAC(DAC_instance[i_slot], int(channel), DAC_idle_music, [], markeroption)
            print(Fore.BLUE +f"len(DAC_idle_music) {len(DAC_idle_music)}")

        # Turn on all 4 channels:
        DAC[i_slot].alloff(DAC_instance[i_slot], action=['Set',0])
        DAC[i_slot].ready(DAC_instance[i_slot])
        DAC[i_slot].play(DAC_instance[i_slot])
    
    # ADC:
    [ADC_type, ADC_label] = instr['ADC'].split('_')
    ADC = im("pyqum.instrument.machine.%s" %ADC_type)
    adca = ADC.Initiate(which=ADC_label)

    # Mapping Readout-type to FPGA bitMode***:
    FPGA = adca.bitMode_Keysight # original keysight bitfile
    if readoutype in ["rt-wfm-ave"]: FPGA = adca.bitMode_AVE
    elif readoutype in ['rt-ave-singleddc']: FPGA = adca.bitMode_AVE_SingleDDC
    elif readoutype in ['rt-ave-dualddc']: FPGA = adca.bitMode_AVE_DualDDC
    elif readoutype in ['rt-ave-dualddc-int']: FPGA = adca.bitMode_AVE_DualDDC_Int
    elif readoutype in ['rt-dualddc-int']: FPGA = adca.bitMode_DualDDC_Int


    '''Prepare ADC:'''
    TOTAL_POINTS = round(recordtime_ns / TIME_RESOLUTION_NS)
    update_items = dict( triggerDelay_sec=trigger_delay_ns*1e-9, TOTAL_POINTS=TOTAL_POINTS, NUM_CYCLES=recordsum, PXI=-13, FPGA=FPGA ) # HARDWIRED to receive trigger from the front-panel EXT.
    ADC.ConfigureBoard(adca, update_items)
    
    # Buffer-size for lowest-bound data-collecting instrument:
    if readoutype in ['one-shot']: # along record sum (for fidelity measurement)
        buffersize = recordsum * 2 # data-density of 2 due to IQ
    elif readoutype in ["continuous", "rt-wfm-ave"]: # along record time
        buffersize = TOTAL_POINTS * 2 # data-density of 2 due to IQ

    elif readoutype in ['rt-ave-singleddc']: # along record time
        buffersize = 2 * round(TOTAL_POINTS/5) * 2  # 2 groups of IQ, down-sampled 5X
    elif readoutype in ['rt-ave-dualddc', 'rt-ave-dualddc-int']: # along record time
        buffersize = round(TOTAL_POINTS/5) * 2  # only down-sampled 5X
    elif readoutype in ['rt-dualddc-int']: # along record sum (shots with accumulated readout-time)
        buffersize = round(TOTAL_POINTS/5) * recordsum * 2  # only down-sampled 5X
    
    try: print(Fore.YELLOW + "Buffer-size for %s: %s" %(readoutype, buffersize))
    except: print(Back.WHITE + Fore.RED + "INVALID READOUTYPE!")


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
            print(Back.BLUE + Fore.WHITE + 'Measuring %s %s/%s' %(renamed_task, i+1, datasize//buffersize))
            # determining the index-locations for each parameters, i.e. the address at any instance
            caddress = cdatasearch(i, cstructure)
            print(Fore.BLACK + Back.WHITE + "i: %s, cstructure: %s, caddress: %s" %(i,cstructure,caddress))

            # High level of execution: preparing i-th SCORE & MACE Script
            # ***************************************************************
            SCORE_DEFINED = deepcopy(SCORE_TEMPLATE)
            MACE_DEFINED = deepcopy(MACE_TEMPLATE)
            for j in range(len(cstructure)): # new version: all parameters in R-JSON

                # Reveal R-JSON Parameter-value at j-th:
                if ">" in structure[j]: # For Locked variables with customized math expression:
                    math_expression = structure[j].split(">")[1] # Algebraic initially
                    for R_KEY in structure[j].split(">")[0].replace(" ","").split(","):
                        math_expression = math_expression.replace( R_KEY, str(R_waveform[R_KEY].data[caddress[structure.index(R_KEY)]]) )
                    Script_Var_Update = evaluate(math_expression) # evaluate numpy-supported expression
                    print(Fore.LIGHTBLUE_EX + "STRUCTURE LOCKED AT IDX-%s: %s -> %s -> %s" %(j, structure[j], math_expression, Script_Var_Update))
                else: # for usual variables
                    Script_Var_Update = R_waveform[structure[j]].data[caddress[j]]

                if TASK_LEVEL == "MAC":
                    # DAC-SCORE-, SG-MACE- and DC-MACE-UPDATE by R-JSON:
                    CH_Matrix = [DAC_CH_Matrix, SG_CH_Matrix, DC_CH_Matrix]
                    for dev, ch_matrix in enumerate(CH_Matrix):
                        for i_slot_order, channel_set in enumerate(ch_matrix):
                            for ch in channel_set:
                                dach_address = "%s-%s" %(i_slot_order+1,ch)
                                if dev==0: SCORE_DEFINED['CH%s'%dach_address] = SCORE_DEFINED['CH%s'%dach_address].replace("{%s}"%structure[j], str(Script_Var_Update))
                                else: MACE_DEFINED["%s-%s-%s"%(Device_Categories[dev],i_slot_order+1,ch)] =  MACE_DEFINED["%s-%s-%s"%(Device_Categories[dev],i_slot_order+1,ch)].replace("{%s}"%structure[j], str(Script_Var_Update))

                if TASK_LEVEL == "EXP": 
                    # EXP-MACE-UPDATE by R-JSON:
                    MACE_DEFINED["EXP-" + renamed_task] = MACE_DEFINED["EXP-" + renamed_task].replace("{%s}"%structure[j], str(Script_Var_Update))

            # Low level:
            if TASK_LEVEL == "EXP":    
                # Expert EXP Control (Every-loop)
                Exp = macer(commander=renamed_task)
                Exp.execute(MACE_DEFINED["EXP-" + renamed_task])

                # MATCHING EXP-TASK FOR ASQPU API:
                match renamed_task:
                    case "DD": 
                        '''MACE-Skills: Qubit_ID/0, Echo_times, Free_Evolution_ns'''
                        d_setting = qapp.get_SQDD_device_setting( Sample_Backend, int(float(Exp.VALUES[Exp.KEYS.index("Echo_times")])), float(Exp.VALUES[Exp.KEYS.index("Free_Evolution_ns")]), target=int(float(Exp.VALUES[Exp.KEYS.index("Qubit_ID")])), withRO=True )
                    case "RB": 
                        '''MACE-Skills: Qubit_ID/0, Sequence_length, Repeat_Random'''
                        d_setting = qapp.get_SQRB_device_setting( Sample_Backend, int(float(Exp.VALUES[Exp.KEYS.index("Sequence_length")])), target=int(float(Exp.VALUES[Exp.KEYS.index("Qubit_ID")])), withRO=True )
                    case _: 
                        print(Fore.WHITE + Back.RED + "EXP-TASK DOES NOT MATCH MACE-DATABASE")

                Exp.close()
                # DEBUG (1)
                print(Fore.YELLOW + "d-setting: %s" %d_setting)
                # DEBUG (2)
                for dcategory in d_setting.keys(): 
                    try: print("Category: %s, Names: %s" %(dcategory, [x for x in d_setting[dcategory].keys()]))
                    except(AttributeError): print("Category: %s, Value: %s" %(dcategory, d_setting[dcategory]))

                # 1. Extract MACE-Command for DC:
                for i_slot, channel_set in enumerate(DC_CH_Matrix):
                    for channel in channel_set:
                        MACE_DEFINED['DC-%s-%s'%(i_slot+1,channel)] = "sweep:%s" %(d_setting['DC'][instr['DC'][i_slot]][channel-1]['sweep']) # manually assign power for now

                # 2. Extract MACE-Command for SG:
                for i_slot, channel_set in enumerate(SG_CH_Matrix):
                    for channel in channel_set:
                        MACE_DEFINED['SG-%s-%s'%(i_slot+1,channel)] = "frequency:%s, power:%s" %(d_setting['SG'][instr['SG'][i_slot]][channel-1]['freq'], d_setting['SG'][instr['SG'][i_slot]][channel-1]['power']) # manually assign power for now


            # Basic MAC Control (Every-loop)
            # 1. MAC's Device: DC
            for i_slot, channel_set in enumerate(DC_CH_Matrix):
                if "DUMMY" in DC_type[i_slot]: 
                    pass
                else:
                    for channel in channel_set:
                        Mac = macer()
                        Mac.execute(MACE_DEFINED['DC-%s-%s'%(i_slot+1,channel)])
                        DC[i_slot].sweep(DC_instance[i_slot], str(Mac.VALUES[Mac.KEYS.index("sweep")]), channel=channel)
                        if TASK_LEVEL == "MAC": DC[i_slot].output(DC_instance[i_slot], int(float(Mac.VALUES[Mac.KEYS.index("output")])), channel)
                        if TASK_LEVEL == "EXP": DC[i_slot].output(DC_instance[i_slot], 1, channel)
                        Mac.close()

            # 2. MAC's Device: SG
            for i_slot, channel_set in enumerate(SG_CH_Matrix):
                for channel in channel_set: 
                    if 'XY' in SG_ROLE_Matrix[i_slot][channel-1]: Compensate_MHz = XY_Compensate_MHz
                    elif 'RO' in SG_ROLE_Matrix[i_slot][channel-1]: Compensate_MHz = RO_Compensate_MHz
                    else: Compensate_MHz = 0
                    Mac = macer()
                    Mac.execute(MACE_DEFINED['SG-%s-%s'%(i_slot+1,channel)])
                    SG[i_slot].frequency(SG_instance[i_slot], action=['Set_%s'%(channel), str(float(Mac.VALUES[Mac.KEYS.index("frequency")]) + Compensate_MHz/1e3) + "GHz"])
                    SG[i_slot].power(SG_instance[i_slot], action=['Set_%s'%channel, str(Mac.VALUES[Mac.KEYS.index("power")]) + ""]) # UNIT dBm NOT WORKING IN DDSLO
                    if TASK_LEVEL == "MAC": SG[i_slot].rfoutput(SG_instance[i_slot], action=['Set_%s'%channel, int(float(Mac.VALUES[Mac.KEYS.index("output")]))])
                    if TASK_LEVEL == "EXP": SG[i_slot].rfoutput(SG_instance[i_slot], action=['Set_%s'%channel, 1])
                    Mac.close()

            
            # Basic CHANNEL Control (Pulse Injection)
            # 3. CH's Device: DAC
            for i_slot_order, channel_set in enumerate(DAC_CH_Matrix):
                # PENDING: Extract the settings from the machine database instead.
                if i_slot_order==0: update_settings = dict(Master=True, clearQ=int(bool(len(channel_set)==4)) ) # First-in-line = Master
                else: update_settings = dict(Master=False, clearQ=int(bool(len(channel_set)==4)) ) # NOTE: please manually write stalking-envelop-SCORE for CH4 to drive PIN-SWITCH

                for ch in channel_set:
                    
                    if TASK_LEVEL == "MAC":
                        dach_address = "%s-%s" %(i_slot_order+1,ch)
                        pulseq = pulser(dt=dt, clock_multiples=1, score=SCORE_DEFINED['CH%s'%dach_address])
                        pulseq.song()
                        CH_Pulse_SEQ = pulseq.music

                    if TASK_LEVEL == "EXP":
                        try: CH_Pulse_SEQ = d_setting['DAC'][instr['DAC'][i_slot_order]][ch-1]
                        except(KeyError): 
                            # NOTE: TO BE ADDED IN D-SETTINGS LATER ON
                            CH_Pulse_SEQ = DAC_idle_music # Idle music for channel not used in Q. Circuit but present in QPC-Wiring (for Qubits segregation)

                    '''
                    NOTE: 
                    TKAWG's marker (number(s)) = SDAWG's markeroption
                    1-4 for TKAWG: ODD-Channel for ARRA-PIN-SWITCH, EVEN-Channel for TRIGGER PURPOSE; RO-TRIGGER: MKR-1: ALZDG, MKR-2: MXA; XY-TRIGGER: MKR-1: MXA, MKR-2: SCOPE
                    7 for SDAWG: PIN-Switch on MixerBox
                    0 for BOTH: disabled.
                    '''
                    if (i_slot_order==0) and ("SDAWG" in DAC_type[i_slot_order]): marker = 7 # ONLY 1st DAC outputs marker via CH-4 to trigger ADC for RO
                    else: marker = 2 # for compatibility with TKAWG (outputs 2 markers for each channel)


                    DAC[i_slot_order].compose_DAC(DAC_instance[i_slot_order], int(ch), CH_Pulse_SEQ, [], marker, update_settings=update_settings) # PENDING: Option to turn ON PINSW for SDAWG (default is OFF)
                    print(Fore.BLUE +f"INJECTED {len(CH_Pulse_SEQ)} POINTS OF WAVEFORM INTO {instr['DAC'][i_slot_order]} CHANNEL {ch} {i_slot_order} {channel_set}")

                    # Clear ADC memory after each fist-slot-channel's Waveform RELOAD:
                    if FPGA:
                        if i_slot_order in [0]: # still got very rare jump(s) even after this:
                            ADC.BeforePlay(adca, update_settings={"FPGA": FPGA, "DDC_FREQ": [-(DDC_RO_Compensate_MHz)*1e6, -(DDC_RO_Compensate_MHz)*1e6]})

                    # DAC[i_slot_order].resume_channel(DAC_instance[i_slot_order], int(ch)) #PENDING: align with TEKTRONIX


                DAC[i_slot_order].ready(DAC_instance[i_slot_order])
                print(Fore.GREEN + 'Waveform from DAC-%s (%s) is Ready!'%(i_slot_order+1, instr['DAC'][i_slot_order]))
                # input("STAGE-3 TEST ON RB, PRESS ENTER TO PROCEED: ")
                
            try:

                # Basic ADC Readout (Buffer Every-loop):
                DATA = ADC.AcquireData(adca, recordtime_ns*1e-9, recordsum, update_settings=dict(FPGA=FPGA) )[0]
                # POST PROCESSING
                if readoutype in ['one-shot', 'rt-dualddc-int']:
                    
                    # Managing output data based on FPGA bitMode for one-shot-type***:
                    if FPGA & adca.bitMode_DDC:
                        DATA = DATA.reshape([recordsum,round(TOTAL_POINTS/5),2])
                        DATA = moveaxis(DATA,1,0).reshape([round(TOTAL_POINTS/5)*recordsum*2]) # change into [round(TOTAL_POINTS/5),recordsum,2] shape and then melt it down to a string of data (1D)
                        if FPGA & adca.bitMode_Int:
                            # prepare denominator:
                            record_succession = outer(linspace(1+round(trigger_delay_ns/10), round(TOTAL_POINTS/5)+round(trigger_delay_ns/10), round(TOTAL_POINTS/5)), ones(recordsum*2)).reshape([round(TOTAL_POINTS/5)*recordsum*2])
                            DATA = divide(DATA, record_succession)
                    else:
                        DATA = DATA.reshape([recordsum,TOTAL_POINTS*2])
                        if digital_homodyne != "original": 
                            for r in range(recordsum):
                                trace_I, trace_Q = DATA[r,:].reshape((TOTAL_POINTS, 2)).transpose()[0], DATA[r,:].reshape((TOTAL_POINTS, 2)).transpose()[1]
                                trace_I, trace_Q = pulse_baseband(digital_homodyne, trace_I, trace_Q, DDC_RO_Compensate_MHz, ifreqcorrection_kHz, dt=TIME_RESOLUTION_NS)
                                DATA[r,:] = array([trace_I, trace_Q]).reshape(2*TOTAL_POINTS) 
                                if not r%1000: print(Fore.YELLOW + "Shooting %s times" %(r+1))
                        DATA = mean(DATA.reshape([recordsum*2,TOTAL_POINTS])[:,skipoints:], axis=1) # back to interleaved IQ-Data string
                    
                elif readoutype in ["continuous", "rt-wfm-ave", 'rt-ave-singleddc', 'rt-ave-dualddc', 'rt-ave-dualddc-int']: # by default
                    
                    # Managing output data based on FPGA bitMode for averaged(continuous)-type***:
                    if FPGA == adca.bitMode_Keysight:
                        DATA = mean(DATA.reshape([recordsum,TOTAL_POINTS*2]), axis=0) # average was done on CPU
                    elif FPGA == adca.bitMode_AVE:
                        DATA = ( DATA.reshape([TOTAL_POINTS*2]) ) / recordsum # average was done on FPGA (real-time)
                    elif FPGA in [adca.bitMode_AVE_SingleDDC]:
                        DATA = ( DATA.reshape([round(TOTAL_POINTS/5)*4]) ) # average + single-DDC was done on FPGA (real-time)
                    elif FPGA in [adca.bitMode_AVE_DualDDC]:
                        DATA = ( DATA.reshape([round(TOTAL_POINTS/5)*2]) ) # average + dual-DDC was done on FPGA (real-time)
                    elif FPGA in [adca.bitMode_AVE_DualDDC_Int]:
                        DATA = ( DATA.reshape([round(TOTAL_POINTS/5)*2]) ) # average + dual-DDC was done on FPGA (real-time)
                        # prepare denominator:
                        # record_succession = outer(linspace(1+round(trigger_delay_ns/10), round(TOTAL_POINTS/5)+round(trigger_delay_ns/10), round(TOTAL_POINTS/5)), ones(2)).reshape([round(TOTAL_POINTS/5)*2])
                        # DATA = divide(DATA, record_succession)
                    
                    # DDC on CPU:
                    if (digital_homodyne != "original") and not (FPGA & adca.bitMode_DDC): 
                        trace_I, trace_Q = DATA.reshape((TOTAL_POINTS, 2)).transpose()[0], DATA.reshape((TOTAL_POINTS, 2)).transpose()[1]
                        trace_I, trace_Q = pulse_baseband(digital_homodyne, trace_I, trace_Q, DDC_RO_Compensate_MHz, ifreqcorrection_kHz, dt=TIME_RESOLUTION_NS)
                        DATA = array([trace_I, trace_Q]).transpose().reshape(TOTAL_POINTS*2) # back to interleaved IQ-Data string
                else:
                    print(Back.WHITE + Fore.RED + "INVALID READOUTYPE!")

                print(Fore.BLUE + "DATA of shape %s is ready to be buffered" %(DATA.shape)) # should be a string of data (1D)
            

            except Exception as e:
                print(Fore.RED + "PLS CHECK ADC ERROR:\n%s" %e)
                print(Fore.RED + format_exc())
                break # proceed to close all & queue out if error

            
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
        for i_slot, channel_set in enumerate(SG_CH_Matrix):
            for channel in channel_set: SG[i_slot].rfoutput(SG_instance[i_slot], action=['Set_%s'%channel, 0])
            SG[i_slot].close(SG_instance[i_slot], SG_label[i_slot], False)
        for i_slot, channel_set in enumerate(DC_CH_Matrix): 
            if "DUMMY" in DC_type[i_slot]: 
                pass
            else:
                for channel in channel_set: 
                    DC[i_slot].sweep(DC_instance[i_slot], str(0), channel=channel)
                    DC[i_slot].output(DC_instance[i_slot], 0, channel)
                DC[i_slot].close(DC_instance[i_slot], reset=True, which=DC_label[i_slot])

        if JOBID in g.queue_jobid_list:
            qout(queue, g.queue_jobid_list[0],g.user['username'])
        break

    return


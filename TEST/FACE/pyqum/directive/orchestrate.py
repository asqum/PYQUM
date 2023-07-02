'''ALL QuBit Orchestration: INTEGRATED'''

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

# QPU-Orchestration:
# **********************************************************************************************************************************************************
@settings(2) # data-density
def Qoracle(owner, tag="", corder={}, comment='', dayindex='', taskentry=0, resumepoint=0, instr={}, perimeter={}, renamed_task=''):
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

    # Loading Configuration:
    
    

    # pushing pre-measurement parameters to settings:
    yield owner, sample, tag, instr, corder, comment, dayindex, taskentry, perimeter, queue, renamed_task

    
    
    # 2a. Basic corder / parameter(s):
    


    # Total data points to be saved into file:
    datasize = int(prod([waveform(corder[param]).count for param in structure], dtype='uint64')) * buffersize
    print("data size: %s" %datasize)

    # User-defined Measurement-FLOW ==============================================================================================
    
    # 1. Registerring parameter(s)-structure
    cstructure = [waveform(corder[param]).count for param in structure] # new version: separation between structure & buffer

    # 2. Start measuring:
    JOBID = g.queue_jobid_list[0]
    job_update_perimeter(JOBID, perimeter)
    
    while True:

        # Orchestrating Pulses: (QUA etc.)
        exec(qua_code_string)
        

        for i in measure_loop:
            print(Back.BLUE + Fore.WHITE + 'Measuring %s %s/%s' %(renamed_task, i+1, datasize//buffersize))
            print(Fore.YELLOW + "\rProgress-(%s): %.3f%%" %((i+1), (i+1)/datasize*buffersize*100), end='\r', flush=True)			
            
            jobsinqueue(queue)
            if JOBID in g.queue_jobid_list:
                # print(Fore.YELLOW + "Pushing Data into file...")
                yield list(DATA)
            else: break # proceed to close all & queue out

        # CLOSING ALL MAC:
        

        if JOBID in g.queue_jobid_list:
            qout(queue, g.queue_jobid_list[0],g.user['username'])
        break

    return


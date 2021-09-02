from time import sleep
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
from pyqum.instrument.logger import settings, get_status, set_status, jobsinqueue, qout, job_update_perimeter
from pyqum.instrument.toolbox import cdatasearch, waveform, find_in_list
from pyqum.instrument.composer import pulser
from pyqum.instrument.analyzer import pulse_baseband
from pyqum.instrument.reader import inst_order

instr = {}
instr['DAC']= inst_order('QPC0', 'DAC')
DACH_Matrix = [[1,2,3,4],[1,2,3,4]]

# DAC for [ROXY]:
DAC_qty = len(instr['DAC'])
DAC_label, DAC, DAC_instance = [None]*DAC_qty, [None]*DAC_qty, [None]*DAC_qty
DAC = im("pyqum.instrument.machine.SDAWG")
# DAC.test()

for i, channel_set in enumerate(DACH_Matrix):
    [DAC_type, DAC_label[i]] = instr['DAC'][i].split('_')
    
    DAC_instance[i] = DAC.Initiate(which=DAC_label[i],mode='TEST')
    DAC.clock(DAC_instance[i], action=['Set', 'EFIXed', 1e9])
    DAC.clear_waveform(DAC_instance[i],'all')
    DAC.alloff(DAC_instance[i], action=['Set',1])
    
    # PENDING: Extract the settings from the machine database instead.
    if i==0: update_settings = dict(Master=True, trigbyPXI=2) # First-in-line = Master
    elif i>0: update_settings = dict(Master=False, trigbyPXI=2)
    print(Fore.CYAN + "%s's setting: %s" %(instr['DAC'][i], update_settings))

    '''Prepare DAC:'''
    dt = round(1/float(DAC.clock(DAC_instance[i])[1]['SRATe'])/1e-9, 2)
    # pulseq = pulser(dt=dt, clock_multiples=1, score="ns=%s"%(300000))
    pulseq = pulser(dt, clock_multiples=1, score="ns=300000;FLAT/,1000,0.01;")
    pulseq.song()
    for channel in channel_set:
        DAC.prepare_DAC(DAC_instance[i], int(channel), pulseq.totalpoints, update_settings=update_settings)
    for channel in channel_set:
        DAC.compose_DAC(DAC_instance[i], int(channel), pulseq.music) # we don't need marker yet initially
        # DAC.compose_DAC(DAC_instance[i], int(channel), pulseq.music, pulseq.envelope, 2, update_settings=update_settings)
    # Turn on all 4 channels:
    DAC.alloff(DAC_instance[i], action=['Set',0])
    DAC.ready(DAC_instance[i])
    DAC.play(DAC_instance[i])
    print("PROBE BUG for DAC-%s: %s" %(i+1,sleep(3)))

# Multiple WAVEs:
for waveth,pulse_width in enumerate([1000,1100,1200,1300,1400,1500,1600,1700]):
    # ///////////////////////////////////////////////////////////
    # TEST-BLOCK for DAC:
    for i, channel_set in enumerate(DACH_Matrix):

        # PENDING: Extract the settings from the machine database instead.
        if i==0: update_settings = dict(Master=True, clearQ=int(bool(len(channel_set)==4)) ) # First-in-line = Master
        elif i>0: update_settings = dict(Master=False, clearQ=int(bool(len(channel_set)==4)) )
        print(Fore.CYAN + "%s's setting: %s" %(instr['DAC'][i], update_settings))

        for ch in channel_set:
            # channel = str(ch + 1)
            dach_address = "%s-%s" %(i+1,ch)
            pulseq = pulser(dt=dt, clock_multiples=1, score="ns=300000;FLAT/,%s,0.02;" %pulse_width)
            pulseq.song()
            
            DAC.compose_DAC(DAC_instance[i], int(ch), pulseq.music, pulseq.envelope, 2, update_settings=update_settings) # PENDING: Option to turn ON PINSW for SDAWG (default is OFF)
        DAC.ready(DAC_instance[i])
        print('Waveform from Slot-%s is Ready!'%(i))
    print("PROBE BUG for WAVE-%s: %s" %(waveth+1,sleep(3)))
    # /////////////////////////////////////////////////////////////



for i, channel_set in enumerate(DACH_Matrix):
    DAC.alloff(DAC_instance[i], action=['Set',1])
    DAC.close(DAC_instance[i], which=DAC_label[i],mode='TEST')

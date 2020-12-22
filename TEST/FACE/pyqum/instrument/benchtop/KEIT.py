# Communicating with Benchtop YOKOGAWA dc-power supply
# Communicating with Benchtop PSG
from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # model's name e.g. ESG, PSG, AWG, VSA, ADC
debugger = 'debug' + mdlname

import pyvisa as visa
from functools import wraps
from time import sleep, time
from contextlib import suppress
from pyqum.instrument.logger import address, set_status, status_code
from pyqum.instrument.toolbox import waveform

def debug(state=False):
    exec('%s %s; %s = %s' %('global', debugger, debugger, 'state'), globals(), locals()) # open global and local both-ways channels!
    if state:
        print(Back.RED + '%s: Debugging Mode' %debugger.replace('debug', ''))
    return

debug() # declare the debugger mode here

# INITIALIZATION
def Initiate(reset=False, which=1):
    ad = address()
    rs = ad.lookup(mdlname, which) # Instrument's Address
    rm = visa.ResourceManager()
    try:
        bench = rm.open_resource(rs) #establishing connection using GPIB# with the machine
        if reset:
            stat = bench.write('RC') #Clear buffer memory
        else:
            stat = bench.write(':SYSTem:PRESet')
        bench.read_termination = '\n' #omit termination tag from output 
        bench.timeout = 15000 #set timeout in ms
        set_status(mdlname, dict(state='connected'))
        print(Fore.GREEN + "%s's connection Initialized: %s" % (mdlname, str(stat)))
        ad.update_machine(1, "%s_%s"%(mdlname,which))
    except: 
        # raise
        set_status(mdlname, dict(state='DISCONNECTED'))
        print(Fore.RED + "%s's connection NOT FOUND" % mdlname)
        bench = "disconnected"
    return bench

def single_pulse(bench, width, height):
    '''width in seconds, height in volts
       ON: 20ms, OFF: 50ms
    '''
    # set compliances
    Compliance = 0.200 #0.08
    bench.write(":SENS:CURR:PROT %s"%Compliance)
    bench.write(":SENS:CURR:RANGe %s"%Compliance)

    # set range
    # bench.write(":SENS:VOLT:RANGe %s" %height)
    
    # pulse sequence
    bench.write(":SOUR:LIST:VOLT 0,%s,0" %height)
    bench.write(":TRIG:COUN 3")
    bench.write(":SOUR:DEL %s" %width)

    return_width = float(bench.query("SOUR:DEL?"))
    bench.write(":SOUR:VOLT:MODE LIST")
    bench.write(":OUTPUT ON")

    bench.write(":FORMAT:ELEM VOLT,CURR")
    VI_List = [float(x) for x in bench.query(":READ?").split(',')]
    
    return return_width, VI_List


def close(bench, reset=False, which=1):
    bench.write(":OUTPUT OFF")
    if reset:
        bench.write(':SYSTem:PRESet')
        set_status(mdlname, dict(config='return to zero-off'))
    else: set_status(mdlname, dict(config='previous'))
    try:
        bench.close() #None means Success?
        status = "Success"
        ad = address()
        ad.update_machine(0, "%s_%s"%(mdlname,which))
    except: status = "Error"
    set_status(mdlname, dict(state='disconnected'))
    print(Back.WHITE + Fore.BLACK + "%s's connection Closed" %(mdlname))
    return status
        

# Test Zone
def test(detail=True):
    debug(detail)
    print(Back.WHITE + Fore.MAGENTA + "Debugger mode: %s" %eval(debugger))
    s = Initiate()
    if eval(debugger):
        stat = single_pulse(s, 0.02, 10)
        print("KEITHLEY READ: %s" %stat)
    else: print(Fore.RED + "Basic IO Test")
    close(s, True)
    return

# test()

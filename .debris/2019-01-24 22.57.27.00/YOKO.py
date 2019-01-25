# Communicating with Benchtop YOKOGAWA dc-power supply
# Communicating with Benchtop PSG
from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # model's name e.g. ESG, PSG, AWG, VSA, ADC
debugger = 'debug' + mdlname

import visa
from functools import wraps
from numpy import linspace
from pyqum.instrument.logger import address, set_status, status_code

def debug(state=False):
    exec('%s %s; %s = %s' %('global', debugger, debugger, 'state'), globals(), locals()) # open global and local both-ways channels!
    if state:
        print(Back.RED + '%s: Debugging Mode' %debugger.replace('debug', ''))
    return

debug() # declare the debugger mode here

# INITIALIZATION
def Initiate():
    rs = address(mdlname, reset=eval(debugger)) # Instrument's Address
    rm = visa.ResourceManager()
    try:
        bench = rm.open_resource(rs) #establishing connection using GPIB# with the machine
        # stat = bench.write('RC') #Clear buffer memory
        bench.write('H0;F1;R6') #No header; DC current in V; 30V range
        bench.read_termination = '\n' #omit termination tag from output 
        bench.timeout = 15000 #set timeout in ms
        set_status(mdlname, dict(state='connected'))
        print(Fore.GREEN + "%s's connection Initialized: %s" % (mdlname, str(stat[1])[-7:]))
    except: 
        set_status(mdlname, dict(state='DISCONNECTED'))
        print(Fore.RED + "%s's connection NOT FOUND" % mdlname)
        bench = "disconnected"
    return bench

def output(bench, state=0):
    try: 
        bench.write('O%dE' %int(state)) #OUTPUT ON/OFF
        status = 'Success'
    except: 
        pass
        status = 'Error'
    return status

def mansweep(start, stop, sweeptime):
    GPIBspeed = 62 #pts/s
    points = int(GPIBspeed * sweeptime)
    Vrange = linspace(start, stop, points)
    for V in Vrange:
        if eval(debugger): print(Fore.YELLOW + "V: %.5f" %V)
        try:
            bench.write('S%.5fE'%V) #Set Voltage
        except:
            pass
            print("Error setting V")
    return Vrange

def close(bench, reset=False):
    if reset:
        bench.write('RC') # reset
        set_status(mdlname, dict(config='reset'))
    else: set_status(mdlname, dict(config='previous'))
    try:
        bench.close() #None means Success?
        status = "Success"
    except: status = "Error"
    set_status(mdlname, dict(state='disconnected'))
    print(Back.WHITE + Fore.BLACK + "%s's connection Closed" %(mdlname))
    return status
        

# Test Zone
def test(detail=False):
    debug(detail)
    print(Back.WHITE + Fore.MAGENTA + "Debugger mode: %s" %eval(debugger))
    s = Initiate()
    if eval(debugger):
        output(s, 1)
        mansweep(0, 5, 15)
        mansweep(5, 0, 15)
        output(s, 0)
        
    else: print(Fore.RED + "Basic IO Test")
    close(s)
    return

test(True)


# Communicating with Benchtop YOKOGAWA dc-power supply
# Communicating with Benchtop PSG
from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # model's name e.g. ESG, PSG, AWG, VSA, ADC
debugger = 'debug' + mdlname

import visa
from functools import wraps
from time import sleep, time
from contextlib import suppress
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
        stat = bench.write('RC') #Clear buffer memory
        bench.write('H0;F1;M1') #No header; DC current in V; Single sweep
        bench.read_termination = '\n' #omit termination tag from output 
        bench.timeout = 15000 #set timeout in ms
        set_status(mdlname, dict(state='connected'))
        print(Fore.GREEN + "%s's connection Initialized: %s" % (mdlname, str(stat[1])[-7:]))
    except: 
        set_status(mdlname, dict(state='DISCONNECTED'))
        print(Fore.RED + "%s's connection NOT FOUND" % mdlname)
        bench = "disconnected"
    return bench

def previous(bench):
    prev = bench.query('OD')
    return prev

def output(bench, state=0):
    try: 
        bench.write('O%dE' %int(state)) #OUTPUT ON/OFF
        status = 'Success'
    except: 
        pass
        status = 'Error'
    return status

def sweep(bench, start, stop, datapts=1, sweeprate=0.7, pulsewidth=0.5):
    '''
    sweeprate in V/s
    pulsewidth: waiting/staying/settling/stabilization time in sec
    Voltage Range (AUTO): R2: 10mV; R3: 100mV; R4: 1V; R5: 10V; R6: 30V
    '''
    SweepTime = abs(start - stop) / sweeprate + pulsewidth * datapts
    GPIBspeed = 62 #pts/s
    Vdata = linspace(start, stop, datapts)
    for i,V in enumerate(Vdata):
        v_prev = float(previous(bench))
        if i == 1:
            Startime = time()
        try:
            #smoothen the transition by setting as many points as possible
            SweepRange = linspace(v_prev, V, round(abs(V-v_prev) * GPIBspeed / sweeprate))
            for v in SweepRange:
                bench.write('SA%.5fE'%v) #Set Voltage
                # print("v: %.5f" %v)
            if eval(debugger): 
                print(Fore.YELLOW + "Settling %.5fV..." %V)
                with suppress(NameError):
                    print(Fore.BLUE + "Time remaining: %ss" %(SweepTime - time() + Startime))
            sleep(pulsewidth)
        except:
            pass
            print("Error setting V")
    return Vdata, SweepTime

def close(bench, reset=False):
    if reset:
        sweep(bench, 0, 0) # return to zero
        set_status(mdlname, dict(config='return to zero'))
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
        print("Previous V: %s" %previous(s))
        output(s, 1)
        sweep(s, 0, 17, 371)
        sweep(s, 0, 17, 71)
        output(s, 0) 
    else: print(Fore.RED + "Basic IO Test")
    close(s)
    return

test(True)


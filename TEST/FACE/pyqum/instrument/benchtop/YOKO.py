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
from pyqum.instrument.logger import address, set_status, status_code
from pyqum.instrument.toolbox import waveform

def debug(state=False):
    exec('%s %s; %s = %s' %('global', debugger, debugger, 'state'), globals(), locals()) # open global and local both-ways channels!
    if state:
        print(Back.RED + '%s: Debugging Mode' %debugger.replace('debug', ''))
    return

debug() # declare the debugger mode here

# INITIALIZATION
def Initiate(reset=False, current=False):
    ad = address()
    rs = ad.lookup(mdlname) # Instrument's Address
    rm = visa.ResourceManager()
    try:
        bench = rm.open_resource(rs) #establishing connection using GPIB# with the machine
        if reset:
            bench.write('RC') #Clear buffer memory
        if current:
            stat = bench.write('H0;F5;M1') #No header; DC current in A; Single sweep
        else:
            stat = bench.write('H0;F1;M1') #No header; DC current in V; Single sweep
        bench.read_termination = '\n' #omit termination tag from output 
        bench.timeout = 15000 #set timeout in ms
        set_status(mdlname, dict(state='connected'))
        print(Fore.GREEN + "%s's connection Initialized: %s" % (mdlname, str(stat[1])[-7:]))
    except: 
        # raise
        set_status(mdlname, dict(state='DISCONNECTED'))
        print(Fore.RED + "%s's connection NOT FOUND" % mdlname)
        bench = "disconnected"
    return bench

def previous(bench, log=False):
    prev = bench.query('OD')
    if log:
        set_status(mdlname, dict(voltage=float(prev)))
    return prev

def output(bench, state=0, keeprev=True):
    '''if keeprev is False, value will return to zero!
    '''
    try:
        bench.write('O%dE' %int(state)) #OUTPUT ON/OFF #Apparently this will return value to zero!
        status = 'Success'
    except: 
        pass
        status = 'Error'
    return status

def sweep(bench, wave, pulsewidth=0.3, sweeprate=7):
    '''
    sweeprate in V/s
    pulsewidth: waiting/staying/settling/stabilization time in sec
    Voltage Range (AUTO): R2: 10mV; R3: 100mV; R4: 1V; R5: 10V; R6: 30V
    '''
    GPIBspeed = 62 #pts/s
    Vdata = waveform(wave).data
    SweepTime = abs(waveform(wave).data[0] - waveform(wave).data[-1]) / sweeprate + pulsewidth * waveform(wave).count
    
    for i,V in enumerate(Vdata):
        v_prev = float(previous(bench))
        if i == 0:
            Startime = time()
        try:
            #smoothen the transition by interpolating points as much as possible:
            SweepRange = waveform("%sto%s*%s" %(v_prev, V, int(abs(V-v_prev) * GPIBspeed / sweeprate))).data
            for v in SweepRange:
                bench.write('SA%.5fE'%v) #Set Voltage
            if eval(debugger):
                print(Fore.YELLOW + "Staying %.5fV..." %V)
                with suppress(NameError):
                    print(Fore.BLUE + "Time remaining: %.3fs" %(SweepTime - time() + Startime))
            sleep(pulsewidth)
        except:
            print("Error setting V")
    return Vdata, SweepTime

def close(bench, reset=False):
    if reset:
        previous(bench, True) # log last-applied voltage
        sweep(bench, "0to0*0") # return to zero
        output(bench, 0) # off output
        set_status(mdlname, dict(config='return to zero-off'))
    else: set_status(mdlname, dict(config='previous'))
    try:
        bench.close() #None means Success?
        status = "Success"
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
        output(s, 1)
        # sweep(s, 0, 7, 371)
        # factor = 1
        # V = 8 * factor
        # sweep(s, V, V, pulsewidth=3)
        # V = 10 * factor
        # sweep(s, V, V)
        # V = 12 * factor
        # sweep(s, V, V)
        V_set = 10
        sweep(s, "%sto0*1"%V_set, pulsewidth=10, sweeprate=V_set*60) # max sweep rate
    else: print(Fore.RED + "Basic IO Test")
    close(s, True)
    return

# test()

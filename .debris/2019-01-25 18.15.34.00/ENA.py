#!/usr/bin/env python
'''Communicating with Benchtop E-series Vector Network Analyzer'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # model's name e.g. ESG, PSG, MXG, AWG, VSA, ADC, PNA
debugger = 'debug' + mdlname

# from functools import wraps
import matplotlib.pyplot as plt
from numpy import arange, floor, ceil, linspace

import visa, wrapt
from boltons.funcutils import wraps
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
        stat = bench.write('*RST;*CLS') #Clear buffer memory;
        bench.write("SENS:CORR:EXT:AUTO:RESet") #clear port-extension auto-correction
        bench.read_termination = '\n' #omit termination tag from output 
        bench.timeout = 80000000 #set timeout in ms
        set_status(mdlname, dict(state='connected'))
        print(Fore.GREEN + "%s's connection Initialized: %s" % (mdlname, str(stat[1])[-7:]))
    except: 
        set_status(mdlname, dict(state='DISCONNECTED'))
        print(Fore.RED + "%s's connection NOT FOUND" % mdlname)
        bench = "disconnected"
    return bench

@wraps
def Attribute(Name):
    '''Attributes'''
    @wraps(Name)
    # @wrapt.decorator
    def wrapper(*a, **b):

        global debug
        bench, SCPIcore, action = Name(*a, **b)
        SCPIcore = SCPIcore.split(";")
        headers = SCPIcore[0].split(':')
        parakeys, paravalues, getspecific, command = [headers[-1]] + SCPIcore[1:], [], [], []

        if action[0] == 'Get':
            try:
                for i in range(len(parakeys)):
                    if len(str(action[i+1])) > 0: #special type of query (e.g. commentstate)
                        getspecific.append(" " + str(action[i+1]))
                    else: getspecific.append('')
                    command.append(parakeys[i] + "?" + getspecific[i])

                command = ':'.join(headers[:-1] + [";".join(command)])
                paravalues = bench.query(command).split(';')
                #just in case of the presence of query parameters, which is rare
                paravalues = [paravalues[i] + '(' + str(action[i+1]) + ')' for i in range(len(parakeys))]
                paravalues = [x.replace('()', '') for x in paravalues]

                status = "Success"
            except: # get out of the method with just return-value at exception?
                status = "query unsuccessful"
                ans = None

        if action[0] == 'Set':

            for i in range(len(parakeys)):
                if str(action[i+1]) == '':
                    paravalues.append("NIL") # allow for arbitrary choosing
                else: 
                    paravalues.append(str(action[i+1]))
                    command.append(parakeys[i] + " " + paravalues[i])

            command = ':'.join(headers[:-1] + [";".join(command)])
            status = str(bench.write(command)[1])[-7:]
            
        # formatting return answer
        ans = dict(zip([a.replace('*','') for a in parakeys], paravalues))

        # Logging answer
        if action[0] == 'Get': # No logging for "Set"
            set_status(mdlname, {Name.__name__ : ans})

        # debugging
        if eval(debugger):
            print(Fore.BLUE + "SCPI Command: {%s}" %command)
            if action[0] == 'Get':
                print(Fore.YELLOW + "%s %s's %s: %s <%s>" %(action[0], mdlname, Name.__name__, ans, status))
            if action[0] == 'Set':
                print(Back.YELLOW + Fore.MAGENTA + "%s %s's %s: %s <%s>" %(action[0], mdlname, Name.__name__ , ans, status))

        return status, ans
    return wrapper

@Attribute
def model(bench, action=['Get'] + 10 * ['']):
    SCPIcore = '*IDN'  #inquiring machine identity: "who r u?"
    return bench, SCPIcore, action
@Attribute
def rfports(bench, action=['Get'] + 10 * ['']):
    SCPIcore = 'OUTPut:STATE'  #switch-on/off RF-ports
    return bench, SCPIcore, action
@Attribute
def sweep(bench, action=['Get'] + 10 * ['']):
    '''
    action=['Get/Set', <auto: ON/OFF 100>, <points>]
    1. Sets the time the analyzer takes to complete one sweep.
    2. Sets the number of data points for the measurement.
    '''
    if action[1] in ['ON', 'TRUE', 'True']:
        bench.write('SENSe:SWEep:TIME:AUTO ON')
        action.remove(action[1])
        SCPIcore = 'SENSe:SWEep:POINTS'
    elif action[1].split(' ')[0] in ['OFF', 'FALSE', 'False', '']:
        try:
            action[1] = action[1].split(' ')[1]
            bench.write('SENSe:SWEep:TIME:AUTO OFF')
        except IndexError: pass
        SCPIcore = 'SENSe:SWEep:TIME;POINTS'
    else: print(Fore.RED + "Parameter NOT VALID!")
    return bench, SCPIcore, action
@Attribute
def linfreq(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <start(Hz)>, <stop(Hz)>]'''
    bench.write("SENS:SWE:TYPE LINEAR") #by default: Freq Sweep
    SCPIcore = 'SENS:FREQuency:START;STOP'
    return bench, SCPIcore, action
@Attribute
def ifbw(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <IFB(Hz)>]'''
    SCPIcore = 'SENSe:BANDWIDTH'
    return bench, SCPIcore, action
@Attribute
def power(bench, action=['Get']):
    '''action=['Get/Set', <Level(dBm)>, <Start(dBm)>, <Stop(dBm)>]'''
    SCPIcore = 'SOURce:POWER:LEVEL;START;STOP'
    action += 10 * ['']
    return bench, SCPIcore, action
@Attribute
def cwfreq(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <Fixed(Hz)>]
    Sets the Continuous Wave (or Fixed) frequency. 
    Must also send SENS:SWEEP:TYPE CW to put the analyzer into CW sweep mode.
    '''
    bench.write("SENS:SWE:TYPE POWER") #Power Sweep
    SCPIcore = 'SENSe:FREQuency:CW'
    return bench, SCPIcore, action
@Attribute
def averag(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <points>]
    Sets the number of measurements to combine for an average.
    '''
    bench.write("SENSe:AVER ON") # OFF by default
    bench.write("SENSe:AVER:CLE")
    SCPIcore = 'SENSe:AVER:COUNT'
    return bench, SCPIcore, action
@Attribute
def dataform(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <format: REAL/REAL32/ASCii>]
    Sets the data format for data transfers.
    '''
    SCPIcore = 'FORMat:DATA'
    return bench, SCPIcore, action

# Setting Trace
def setrace(bench, Mparam=['S11','S21','S12','S22'], window='D1'):
    '''window = {D<Tr#...>: {#repeat: linewidth, _:next-line}}
    '''
    bench.write("CALC:PAR:COUN %d" %len(Mparam))
    Mreturn = []
    for iTrace, S in enumerate(Mparam):
        bench.write("CALC:PAR%d:DEF %s" %(iTrace + 1, S)) #setting trace name
        Mreturn.append(bench.query("CALC:PAR%d:DEF?" %(iTrace + 1)))
        bench.write(":DISP:WIND:TRAC%d:Y:AUTO"%(iTrace + 1)) #pre-auto-scale
    bench.write("DISPlay:WINDow:SPLit %s" %window)
    return Mreturn

def autoscal(bench):
    tracenum = int(bench.query("CALC:PAR:COUN?"))
    for i in range(tracenum):
        lastatus = bench.write(":DISP:WIND:TRAC%d:Y:AUTO"%(i+1))
    return lastatus

def measure(bench):
    bench.write(':ABOR;:INIT:CONT ON;:TRIG:SOUR BUS;:TRIG:SING;')
    # when opc return, the sweep is done
    ready = bench.query("*OPC?") # method from labber was inefficient at best, misleading us on purpose perhaps!
    return ready

def sdata(bench, format='REAL,32'):
    if format == 'REAL,32':
        datas = bench.query_binary_values("CALC:DATA? SDATA", datatype='f', is_big_endian=True)
    elif format == 'ASCII,0':
        datas = bench.query_ascii_values("CALC:DATA? SDATA")
    print(Back.GREEN + Fore.WHITE + "transferred from %s: ALL-SData: %s" %(mdlname, len(datas)))
    return datas

def close(bench, reset=True):
    try:
        if reset:
            bench.write('OUTP OFF')
            set_status(mdlname, dict(config='reset-off'))
        else: set_status(mdlname, dict(config='previous'))
        try:
            bench.close() #None means Success?
            status = "Success"
        except: status = "Error"
        set_status(mdlname, dict(state='disconnected'))
        print(Back.WHITE + Fore.BLACK + "%s's connection Closed" %(mdlname))
    except: 
        status = "disconnected per se!!!"
        pass
    return status

# Test Zone
def test(detail=False):
    debug(detail)
    print(Back.WHITE + Fore.MAGENTA + "Debugger mode: %s" %eval(debugger))
    bench = Initiate()
    if bench is "disconnected":
        pass
    else:
        model(bench)
        if eval(debugger):
            print(setrace(bench, window='D12_34'))
            N = 7000
            sweep(bench, action=['Set', 'ON', N])
            f_start, f_stop = 4.4e9, 4.9e9
            linfreq(bench, action=['Set', f_start, f_stop])
            stat = linfreq(bench)
            fstart, fstop = stat[1]['START'], stat[1]['STOP']
            # Building X-axis
            fstart, fstop = float(fstart), float(fstop)
            X = list(linspace(fstart, fstop, N))
            noisefilfac = 100
            IFB = abs(float(fstart) - float(fstop))/N/noisefilfac
            ifbw(bench, action=['Set', IFB])
            ifbw(bench)
            power(bench, action=['Set', -10])
            power(bench)
            # cwfreq(bench, action=['Set', 3e9])
            # cwfreq(bench)
            # power(bench, action=['Set', -10, 30])
            averag(bench, action=['Set', 1]) #optional
            averag(bench)
            stat = sweep(bench)
            print("Time-taken would be: %s (%spts)" %(stat[1]['TIME'], stat[1]['POINTS']))
            print("Ready: %s" %measure(bench)[1])
            autoscal(bench)
            rfports(bench, action=['Set', 'OFF'])
            rfports(bench)
        else: print(Fore.RED + "Basic IO Test")
    close(bench)
    return

test(True)



'''Communicating with Benchtop E-series Vector Network Analyzer'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # instrument-module's name e.g. ENA, PSG, YOKO

import matplotlib.pyplot as plt
from numpy import arange, floor, ceil, linspace

import visa
from pyqum.instrument.logger import address, set_status, status_code, debug
from pyqum.instrument.logger import translate_scpi as Attribute

debugger = debug(mdlname)

# INITIALIZATION
def Initiate():
    ad = address()
    rs = ad.lookup(mdlname) # Instrument's Address
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

@Attribute
def model(bench, action=['Get'] + 10 * ['']):
    SCPIcore = '*IDN'  #inquiring machine identity: "who r u?"
    return mdlname, bench, SCPIcore, action
@Attribute
def rfports(bench, action=['Get'] + 10 * ['']):
    SCPIcore = 'OUTPut:STATE'  #switch-on/off RF-ports
    return mdlname, bench, SCPIcore, action
@Attribute
def sweep(bench, action=['Get'] + 10 * ['']):
    '''CONDITIONAL SWEEP:\n
    action=['Get/Set', <auto: ON/OFF 100>, <points>]
    1. Sets the time the analyzer takes to complete one sweep.
    2. Sets the number of data points for the measurement.
    '''
    print(Fore.GREEN + "action: %s" %action)
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
    return mdlname, bench, SCPIcore, action
@Attribute
def linfreq(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <start(Hz)>, <stop(Hz)>]'''
    bench.write("SENS:SWE:TYPE LINEAR") #by default: Freq Sweep
    SCPIcore = 'SENS:FREQuency:START;STOP'
    return mdlname, bench, SCPIcore, action
@Attribute
def ifbw(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <IFB(Hz)>]'''
    SCPIcore = 'SENSe:BANDWIDTH'
    return mdlname, bench, SCPIcore, action
@Attribute
def power(bench, action=['Get']):
    '''
    action=['Get/Set', <Level(dBm)>, <Start(dBm)>, <Stop(dBm)>]
    dynamic range is limited to 35dB
    '''
    SCPIcore = 'SOURce:POWER:LEVEL;START;STOP'
    action += 10 * ['']
    return mdlname, bench, SCPIcore, action
@Attribute
def cwfreq(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <Fixed(Hz)>]
    Sets the Continuous Wave (or Fixed) frequency. 
    Must also send SENS:SWEEP:TYPE CW to put the analyzer into CW sweep mode.
    '''
    bench.write("SENS:SWE:TYPE POWER") #Power Sweep
    SCPIcore = 'SENSe:FREQuency:CW'
    return mdlname, bench, SCPIcore, action
@Attribute
def averag(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <points>]
    Sets the number of measurements to combine for an average.
    '''
    bench.write("SENSe:AVER ON") # OFF by default
    bench.write("SENSe:AVER:CLE")
    SCPIcore = 'SENSe:AVER:COUNT'
    return mdlname, bench, SCPIcore, action
@Attribute
def dataform(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <format: REAL/REAL32/ASCii>]
    Sets the data format for data transfers.
    Usually only the last two are preferred.
    '''
    SCPIcore = 'FORMat:DATA'
    return mdlname, bench, SCPIcore, action

@Attribute
def selectrace(bench, action=['Set'] + ['par 1']):
    '''
    This command sets/gets the selected trace (Tr) of selected channel (Ch) to the active trace.
    You can set only a trace displayed to the active trace. 
    If this object is used to set a trace not displayed to the active trace, an error occurs when executed and the object is ignored. (No read)
    '''
    SCPIcore = 'CALCulate:PARameter:SELECT'
    action += 10 * ['']
    return mdlname, bench, SCPIcore, action

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
    return Mreturn #same as <Mparam>

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

def sdata(bench):
    '''Collect data from ENA
    This command sets/gets the corrected data array, for the active trace of selected channel (Ch).
    '''
    sdatacore = ":CALC:SEL:DATA:SDAT?"
    stat = dataform(bench)
    if stat[1]['DATA'] == 'REAL32': #PENDING: testing REAL (64bit)
        datas = bench.query_binary_values(sdatacore, datatype='f', is_big_endian=True)
    elif stat[1]['DATA'] == 'ASCii':
        datas = bench.query_ascii_values(sdatacore)
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
def test(detail=True):
    bench = Initiate()
    if bench is "disconnected":
        pass
    else:
        model(bench)
        if debug(mdlname, detail):
            print(setrace(bench, window='D12_34'))
            power(bench, action=['Set', -73.1])
            power(bench)
            N = 7000
            sweep(bench, action=['Set', 'OFF 10', N])
            f_start, f_stop = 4.4e9, 4.9e9
            linfreq(bench, action=['Set', f_start, f_stop]) #F-sweep
            stat = linfreq(bench)
            fstart, fstop = stat[1]['START'], stat[1]['STOP']
            # Building X-axis
            fstart, fstop = float(fstart), float(fstop)
            X = list(linspace(fstart, fstop, N))
            noisefilfac = 100
            IFB = abs(float(fstart) - float(fstop))/N/noisefilfac
            ifbw(bench, action=['Set', IFB])
            ifbw(bench)
            averag(bench, action=['Set', 1]) #optional
            averag(bench)
            stat = sweep(bench)
            print("Time-taken would be: %s (%spts)" %(stat[1]['TIME'], stat[1]['POINTS']))
            print("Ready: %s" %measure(bench)[1])
            autoscal(bench)

            cwfreq(bench, action=['Set', 5.25e9])
            cwfreq(bench)
            power(bench, action=['Set', '', -75.3, -40.3])
            power(bench)
            stat = sweep(bench)
            print("Time-taken would be: %s (%spts)" %(stat[1]['TIME'], stat[1]['POINTS']))
            print("Ready: %s" %measure(bench)[1])
            
            autoscal(bench)
            dataform(bench, action=['Set', 'REAL32'])

            selectrace(bench, action=['Set', 'para 1 calc 1'])
            print(sdata(bench))

            rfports(bench, action=['Set', 'OFF'])
            rfports(bench)
        else: print(Fore.RED + "Basic IO Test")
    close(bench)
    return




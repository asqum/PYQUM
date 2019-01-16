# Communicating with Benchtop P-series Vector Network Analyzer 
from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # model's name e.g. ESG, PSG, MXG, AWG, VSA, ADC, PNA
debugger = 'debug' + mdlname

import visa
from functools import wraps
from pyqum.instrument.logger import address, set_status, status_code

import matplotlib.pyplot as plt
from numpy import arange, floor, ceil

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
        stat = bench.write('*RST;*CLS;SYST:FPReset') #Clear buffer memory; Load preset
        bench.write("CALCulate:PARameter:DELete:ALL") #clear all params (S-params)
        bench.write("SENS:CORR:EXT:AUTO:RESet") #clear port-extension auto-correction
        bench.read_termination = '\n' #omit termination tag from output 
        bench.timeout = 731000 #set timeout in ms
        set_status(mdlname, dict(state='connected'))
        print(Fore.GREEN + "%s's connection Initialized: %s" % (mdlname, str(stat[1])[-7:]))
    except: 
        set_status(mdlname, dict(state='DISCONNECTED'))
        print(Fore.RED + "%s's connection NOT FOUND" % mdlname)
        bench = "disconnected"
    return bench

def Attribute(Name):
    @wraps(Name)
    def wrapper(*a, **b):

        global debug
        bench, SCPIcore, action = Name(*a, **b)
        SCPIcore = SCPIcore.split(";")
        parakeys, paravalues, getspecific, command = [(SCPIcore[0]).split(':')[-1]] + SCPIcore[1:], [], [], []

        if action[0] == 'Get':
            try:
                for i in range(len(parakeys)):
                    if len(str(action[i+1])) > 0: #special type of query (e.g. commentstate)
                        getspecific.append(" " + str(action[i+1]))
                    else: getspecific.append('')
                    command.append(str(SCPIcore[i]) + "?" + getspecific[i])
                command = ";".join(command)

                paravalues = bench.query(command).split(';')
                paravalues = [paravalues[i] + '(' + str(action[i+1]) + ')' for i in range(len(parakeys))]
                paravalues = [x.replace('()', '') for x in paravalues]

                status = "Success"
            except: # get out of the method with just return-value at exception?
                status = "query unsuccessful"
                ans = None

        if action[0] == 'Set':

            for i in range(len(parakeys)):
                paravalues.append(str(action[i+1]))
                command.append(str(SCPIcore[i]) + " " + paravalues[i])

            command = ";".join(command)
            status = str(bench.write(command)[1])[-7:]
            
        # formatting return answer
        if len(SCPIcore) > 1:
            ans = dict(zip(parakeys, paravalues))
        else: ans = paravalues[0]

        # Logging answer
        if action[0] == 'Get': # No logging for "Set"
            set_status(mdlname, {Name.__name__ : str(ans)})

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
def catalog(bench, action=['Get'] + 10 * ['']):
    SCPIcore = 'CALC1:PAR:CAT:EXT'  #inquiring machine: "what do u measure?"
    return bench, SCPIcore, action
@Attribute
def rfports(bench, action=['Get'] + 10 * ['']):
    SCPIcore = 'OUTPut:STATe'  #switch-on/off RF-ports
    return bench, SCPIcore, action
@Attribute
def sweep(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <time: MIN>, <points>]
    1. Sets the time the analyzer takes to complete one sweep.
    2. Sets the number of data points for the measurement.
    '''
    SCPIcore = 'SENSe:SWEep:TIME;POINts'
    return bench, SCPIcore, action
@Attribute
def linfreq(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <start(Hz)>, <stop(Hz)>]'''
    bench.write("SENS:SWE:TYPE LINear") #by default
    SCPIcore = 'SENS:FREQuency:STARt;STOP'
    return bench, SCPIcore, action
@Attribute
def ifbw(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <IFB(Hz)>]'''
    SCPIcore = 'SENSe:BANDwidth'
    return bench, SCPIcore, action
@Attribute
def power(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <Power(dBm)>]'''
    SCPIcore = 'SOURce:POWer'
    return bench, SCPIcore, action
@Attribute
def cwfreq(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <Fixed(Hz)>]
    Sets the Continuous Wave (or Fixed) frequency. 
    Must also send SENS:SWEEP:TYPE CW to put the analyzer into CW sweep mode.
    '''
    bench.write("SENS:SWE:TYPE CW")
    SCPIcore = 'SENSe:FREQuency:CW'
    return bench, SCPIcore, action
@Attribute
def fastcw(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <points>]
    Enables Fast CW sweep and sets the number of data points for the channel. 
    Sweep Type must already be set to CW and FIFO must already be enabled.
    '''
    bench.write("SENS:SWE:TYPE CW")
    bench.write("SYSTem:FIFO:STATe")
    SCPIcore = 'SENSe:SWEep:TYPE:FACW'
    return bench, SCPIcore, action
@Attribute
def averag(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <points>]
    Sets the number of measurements to combine for an average.
    '''
    bench.write("SENSe:AVER ON") # OFF by default
    bench.write("SENSe:AVER:CLE")
    SCPIcore = 'SENSe:AVER:COUN;'
    return bench, SCPIcore, action
@Attribute
def dataform(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <format: REAL,32/ASCII,0>]
    Sets the data format for data transfers.
    '''
    SCPIcore = 'FORMat:DATA'
    return bench, SCPIcore, action

# Setting Trace
def setrace(bench, Mparam=['S11','S21']):
    Mname = []
    for S in Mparam:
        iTrace = Mparam.index(S) + 1
        Mname.append(S)
        bench.write("CALC%d:PAR:EXT '%s','%s'" % (1, Mname[iTrace - 1], S)) #setting measurement name
        bench.write(":DISP:WIND%s:STATe ON" %1)
        bench.write("DISP:WIND%d:TRAC%d:FEED '%s'" % (1, iTrace, Mname[iTrace - 1])) #displaying trace (no set-trace for old-type handling of traces)
        bench.write(":DISP:WIND%d:TRAC%d:Y:AUTO"%(1, iTrace)) #pre-auto-scale
    return Mname

def autoscal(bench, tracenum, window='united'):
    '''
    tracenum = <len(Mparam)>
    '''
    if window == 'united':
        for i in range(tracenum):
            bench.write(":DISP:WIND%d:TRAC%d:Y:AUTO"%(1, i+1))
    else:
        for i in range(tracenum):
            bench.write(":DISP:WIND%d:TRAC%d:Y:AUTO"%(i+1, i+1))

def measure(bench, Ave_num=1):
    bench.write("SENSe:SWE:GRO:COUN %s" %Ave_num)
    bench.write("TRIG:SOUR IMM")
    # when opc return, the sweep is done
    ready = bench.query("SENS:SWE:MODE GRO;*OPC?") # method from labber was inefficient at best, misleading us on purpose perhaps!
    return ready

def sdata(bench, format='REAL,32'):
    if format == 'REAL,32':
        datas = bench.query_binary_values("CALC:DATA? SDATA", datatype='f', is_big_endian=True)
    elif format == 'ASCII,0':
        datas = bench.query_ascii_values("CALC:DATA? SDATA")
    print(Back.GREEN + Fore.WHITE + "transferred from %s: ALL-SData: %s" %(mdlname, len(datas)))
    return datas
    

# Analytics
def IQAP(datas):
    # Slicing datas into IQ-data
    IQdata = datas.reshape(len(datas)/2, 2)
    Idata, Qdata = IQdata[:,0], IQdata[:,1]
    yI, yQ = [float(i) for i in Idata], [float(i) for i in Qdata]
    Amp, Pha = [], []
    for i in zip(yI, yQ):
        Amp.append(20*log10(sqrt(i[0]**2 + i[1]**2)))
        Pha.append(arctan2(i[1], i[0])) # -pi < phase < pi
    return yI, yQ, Amp, Pha


def close(bench, reset=True):
    try:
        if reset:
            bench.write('SYSTem:PRESet') # reset to factory setting (except data-format)
            set_status(mdlname, dict(config='reset'))
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
        if eval(debugger):
            
        else: print(Fore.RED + "Basic IO Test")
    close(bench)
    return

# test(True)



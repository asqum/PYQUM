# Communicating with Benchtop DSA8300 (Tektronix Sampling Scope)
from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # module's name e.g. PSG

import pyvisa as visa
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
        stat = bench.write('*ESR?') #basic query
        bench.read_termination = '\n' #omit termination tag from output 
        bench.timeout = 150000 #set timeout in ms
        set_status(mdlname, dict(state='connected'))
        print(Fore.GREEN + "%s's connection Initialized: %s" % (mdlname, str(stat)))
    except: 
        set_status(mdlname, dict(state='DISCONNECTED'))
        print(Fore.RED + "%s's connection NOT FOUND" % mdlname)
        bench = "disconnected"
    return bench

@Attribute
def model(bench, action=['Get', '']):
    SCPIcore = '*IDN'  #inquiring machine identity: "who r u?"
    return mdlname, bench, SCPIcore, action

@Attribute
def tdr(bench, action=['Get'] + 10 * ['']):
    '''Set TDR\n
        action=['Set', {REF10Mhz:  LOCKExt | LOCKInt}, ]'''
    SCPIcore = 'TDR:REF10Mhz'
    return mdlname, bench, SCPIcore, action

@Attribute
def tdrchannel(bench, channel, action=['Get'] + 10 * ['']):
    '''Set TDR Channel\n
        action=['Set', 
        {UNIts:  Volt | Rho | Ohm},
        {PRESET:  <space>} ]'''
    SCPIcore = 'TDR:CH%s:UNIts;PRESET' %channel
    return mdlname, bench, SCPIcore, action

@Attribute
def tdrstep(bench, channel, action=['Get'] + 10 * ['']):
    '''Set TDR Step\n
        action=['Set', {STATE:  ON | OFF | NR1}, {POLarity: PLUS | MINUS} ]'''
    SCPIcore = 'TDR:CH%s:STEP:STATE;POLarity' %channel
    return mdlname, bench, SCPIcore, action

@Attribute
def trigger(bench, action=['Get'] + 10 * ['']):
    '''Trigger settings\n
        action=['Set', 
        {SOUrce: C1CLKRec | C3CLKRec | CLKPre | EXTDirect | EXTPrescaler | FREerun | INTClk | TDR },
        {INTRate: <NR3:scientific format>},
        {SLOpe: RISe | FALL} ]'''
    SCPIcore = 'TRIGger:SOUrce;INTRate;SLOpe'
    return mdlname, bench, SCPIcore, action

@Attribute
def waveformdb(bench, wfmnumber, action=['Get'] + 10 * ['']):
    '''Waveform database (display)\n
        action=['Set', 
        {SOURce: CH<x> | MATH<x> (, MAIn | MAG1 | MAG2)},
        {ENABle: ON | OFF | NR1 },
        {DISplay: ON | OFF | NR1 }]
        WARNING: will SLOWDOWN the sampling scope!'''
    SCPIcore = 'WFMDB:WFMDB%s:SOURce;ENABle;DISplay' %(wfmnumber)
    return mdlname, bench, SCPIcore, action

@Attribute
def acquire(bench, action=['Get'] + 10 * ['']):
    '''acquisition\n
        action=['Set', 
        {STATE: OFF | ON | RUN | STOP | <NR1> },
        {MODe: SAMple | AVERage | ENVElope }]'''
    SCPIcore = 'ACQuire:STATE;MODe'
    return mdlname, bench, SCPIcore, action

@Attribute
def display(bench, action=['Get'] + 10 * ['']):
    '''display settings\n
        action=['Set', 
        {STYle: NORMal | INFPersist | VARPersist },
        {SHOWVector: ON | OFF | NR1 }]'''
    SCPIcore = 'DISplay:STYle;SHOWVector'
    return mdlname, bench, SCPIcore, action

@Attribute
def displaychannel(bench, channel, action=['Get'] + 10 * ['']):
    '''Set Displayed Channel#\n
        action=['Set', {MAIn: ON | OFF | NR1}, {MAGnify: ON | OFF | NR1}]'''
    SCPIcore = 'DISplay:CH%s:MAIn;MAGnify%s' %(channel,channel)
    return mdlname, bench, SCPIcore, action


def close(bench, reset=False):
    if reset:
        bench.write('*RST') # reset to factory setting
        set_status(mdlname, dict(config='reset'))
    else: set_status(mdlname, dict(config='previous'))
    try:
        acquire(bench, action=['Set','OFF','']) # STOP ACQUISITION
        bench.close() #None means Success?
        status = "Success"
    except: status = "Error"
    set_status(mdlname, dict(state='disconnected'))
    print(Back.WHITE + Fore.BLACK + "%s's connection Closed" %(mdlname))
    return status
        

# Test Zone
def test(detail=True):
    s = Initiate()
    if s == "disconnected":
        pass
    else:
        if debug(mdlname, detail):
            print(Fore.RED + "Detailed Test:")
            model(s)

            tdrchannel(s, 3, action=['Set','Volt',' '])
            tdrstep(s, 3, action=['Set','ON','PLUS'])
            # waveformdb(s, 3, action=['Set',"","","ON"])

            tdrchannel(s, 4, action=['Set','Volt',' '])
            tdrstep(s, 4, action=['Set','ON','PLUS'])
            # waveformdb(s, 4, action=['Set',"","","ON"])
            
            tdr(s, action=['Set','LOCKExt'])
            trigger(s, action=['Set','TDR',25e3,''])

            acquire(s, action=['Set','ON','SAMPLE'])
            display(s, action=['Set','NORMAL','ON'])

            # stat = s.write('ACQuire:DATA:CLEar')
            # print('write status: %s' %stat[0])

        else: print(Fore.RED + "Basic IO Test")
    if not bool(input("Press ENTER (OTHER KEY) to (skip) reset: ")):
        state = True
    else: state = False
    close(s, reset=state)
    return

# test()
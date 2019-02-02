# Communicating with Benchtop PSG
from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # module's name e.g. PSG

import visa
from pyqum.instrument.logger import address, set_status, status_code, debug
from pyqum.instrument.logger import translate_scpi as Attribute

debugger = debug(mdlname)

# INITIALIZATION
def Initiate():
    rs = address(mdlname, reset=debugger) # Instrument's Address
    rm = visa.ResourceManager()
    try:
        bench = rm.open_resource(rs) #establishing connection using GPIB# with the machine
        stat = bench.write('*CLS') #Clear buffer memory; Load preset
        bench.read_termination = '\n' #omit termination tag from output 
        bench.timeout = 150000 #set timeout in ms
        set_status(mdlname, dict(state='connected'))
        print(Fore.GREEN + "%s's connection Initialized: %s" % (mdlname, str(stat[1])[-7:]))
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
def savestate(bench, action):
    """action=['Set', '<reg 0-99>,<seq 0-9>']
    """
    SCPIcore = '*SAV'  #save machine state
    return mdlname, bench, SCPIcore, action
@Attribute
def recallstate(bench, action):
    """action=['Set', '<reg 0-99>,<seq 0-9>']
    """
    SCPIcore = '*RCL'  #save machine state
    return mdlname, bench, SCPIcore, action
@Attribute
def commentstate(bench, action): # query with parameters
    """action=['Set', '<reg 0-99>,<seq 0-9>,comment']
    or action=['Get', '<reg 0-99>,<seq 0-9>']
    """
    SCPIcore = ':MEMory:STATe:COMMENT'  #save machine state
    return mdlname, bench, SCPIcore, action
@Attribute
def memory(bench, action=['Get', '']):
    SCPIcore = ':MEMory:CATalog:ALL'  #inquiring machine memory
    return mdlname, bench, SCPIcore, action
@Attribute
def frequency(bench, action=['Get', '']):
    '''action=['Set','2GHz']'''
    SCPIcore = ':SOUR:FREQ:FIXED'
    return mdlname, bench, SCPIcore, action
@Attribute
def power(bench, action=['Get', '']): 
    '''action=['Set','-7dbm']'''
    SCPIcore = ':SOUR:POW:LEVEL'
    return mdlname, bench, SCPIcore, action
@Attribute
def output(bench, action=['Get', '']):
    SCPIcore = ':OUTP:STATE'
    return mdlname, bench, SCPIcore, action

def close(bench, reset=True):
    if reset:
        bench.write('*RST') # reset to factory setting (including switch-off)
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
def test(detail=True):
    s = Initiate()
    if s is "disconnected":
        pass
    else:
        model(s)
        if debug(mdlname, detail):
            print(Fore.RED + "Detailed Test:")
            # recallstate(s, action=['Set', '1,0'])
            frequency(s)
            p = float(power(s)[1]['LEVEL'])
            print("Power: %s" %p)
            output(s, action=['Set', 'ON'])
            output(s)
            # savestate(s, ['Set','1,0'])
            # commentstate(s, action=['Set', "1,0,'OMG I am ALEXA'"])
            # commentstate(s, action=['Get', '1,0'])
            power(s, action=['Set', '-7.3dbm'])
            power(s)
            frequency(s, action=['Set', '1GHz'])
            frequency(s)
            output(s, action=['Set', 'ON'])
            output(s)
        else: print(Fore.RED + "Basic IO Test")
    if not bool(input("Press ENTER (OTHER KEY) to (skip) reset: ")):
        state = True
    else: state = False
    close(s, reset=state)
    return


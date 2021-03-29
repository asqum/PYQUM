# Communicating with Benchtop PSG (Latest:2019/02)
from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # module's name e.g. PSG

import pyvisa as visa
from pyqum.instrument.logger import address, set_status, status_code, debug
from pyqum.instrument.logger import translate_scpi as Attribute

debugger = debug(mdlname)

# INITIALIZATION
def Initiate(which, mode='DATABASE'):
    ad = address(mode)
    rs = ad.lookup(mdlname, which) # Instrument's Address
    rm = visa.ResourceManager()
    try:
        bench = rm.open_resource(rs) #establishing connection using GPIB# with the machine
        stat = bench.write('*CLS') #Clear buffer memory; Load preset
        bench.read_termination = '\n' #omit termination tag from output 
        bench.timeout = 150000 #set timeout in ms
        set_status(mdlname, dict(state='connected'), which)
        print(Fore.GREEN + "%s-%s's connection Initialized: %s" % (mdlname,which, str(stat)))
        ad.update_machine(1, "%s_%s"%(mdlname,which))
    except: 
        set_status(mdlname, dict(state='DISCONNECTED'), which)
        print(Fore.RED + "%s-%s's connection NOT FOUND" %(mdlname,which))
        bench = "disconnected"
    return bench

@Attribute
def model(bench, action=['Get', '']):
    SCPIcore = '*IDN'  #inquiring machine identity: "who r u?"
    return mdlname, bench, SCPIcore, action

@Attribute
def frequency(bench, action=['Get', '']):
    '''This command sets the signal generator output frequency for the CW frequency mode, or increments or decrements the current RF frequency setting.\n
        action=['Set','2GHz']'''
    SCPIcore = 'SOURce:FREQUENCY:CW'
    return mdlname, bench, SCPIcore, action
@Attribute
def power(bench, action=['Get', '']): 
    '''This command sets the RF output power. 
        action=['Set','-7dbm']'''
    SCPIcore = ':SOURce:POWer:AMPLITUDE'
    return mdlname, bench, SCPIcore, action
@Attribute
def rfoutput(bench, action=['Get', '']):
    '''This command enables or disables the RF output. Although you can configure and engage various modulations, 
    no signal is available at the RF OUTPUT connector until this command is executed.'''
    SCPIcore = ':OUTPut:STATE'
    return mdlname, bench, SCPIcore, action


def close(bench, which, reset=True, mode='DATABASE'):
    if reset:
        bench.write('*RST') # reset to factory setting (including switch-off)
        set_status(mdlname, dict(config='reset'), which)
    else: set_status(mdlname, dict(config='previous'), which)
    try:
        bench.close() #None means Success?
        status = "Success"
        ad = address(mode)
        ad.update_machine(0, "%s_%s"%(mdlname,which))
    except: 
        raise
        status = "Error"
    set_status(mdlname, dict(state='disconnected with %s' %status), which)
    print(Back.WHITE + Fore.BLACK + "%s's connection Closed with %s" %(mdlname,status))
    return status
        

# Test Zone
def test(detail=True):
    S={}
    S['x'] = Initiate(1, 'TEST')
    s = S['x']
    if s == "disconnected":
        pass
    else:
        if debug(mdlname, detail):
            print(Fore.RED + "Detailed Test:")
            # print('SCPI TEST:')
            # s.write("*SAV 00,1")
            model(s)
            
            power(s, action=['Set', '17.3dbm'])
            power(s)
            frequency(s, action=['Set', '4.175GHz'])
            frequency(s)
            rfoutput(s, action=['Set', 'ON'])
            rfoutput(s)
            
        else: print(Fore.RED + "Basic IO Test")
    if not bool(input("Press ENTER (OTHER KEY) to (skip) reset: ")):
        state = True
    else: state = False
    close(s, 1, reset=state, mode='TEST')
    return


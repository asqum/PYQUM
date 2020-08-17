# Communicating with Benchtop GW DC-Source (Latest:2019/02)
from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # module's name e.g. PSG

import visa
from time import sleep
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
def channel_voltage(bench, chanum, action=['Get', '']):
    '''This command sets the voltage of power source.\n
        action=['Set','1']'''
    SCPIcore = 'CHAN%s:VOLT' %chanum
    return mdlname, bench, SCPIcore, action

@Attribute
def channel_current(bench, chanum, action=['Get', '']):
    '''This command sets the current of power source.\n
        action=['Set','0.01']'''
    SCPIcore = 'CHAN%s:CURR' %chanum
    return mdlname, bench, SCPIcore, action

@Attribute
def output(bench, action=['Get', '']):
    '''This command enables or disables the RF output. Although you can configure and engage various modulations, 
    no signal is available at the RF OUTPUT connector until this command is executed.'''
    SCPIcore = ':OUTPut:STATE'
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
    S={}
    S['x'] = Initiate()
    s = S['x']
    if s is "disconnected":
        pass
    else:
        if debug(mdlname, detail):
            print(Fore.RED + "Detailed Test:")
            # print('SCPI TEST:')
            # s.write("*SAV 00,1")
            model(s)
            channel_voltage(s, 1)
            channel_voltage(s, 1, action=['Set', '28'])
            channel_current(s, 1)
            channel_current(s, 1, action=['Set', '0.125'])
            output(s, action=['Set', '1'])
            # sleep(1)
            output(s, action=['Set', '0'])
            
        else: print(Fore.RED + "Basic IO Test")
    if not bool(input("Press ENTER (OTHER KEY) to (skip) reset: ")):
        state = True
    else: state = False
    close(s, reset=state)
    return
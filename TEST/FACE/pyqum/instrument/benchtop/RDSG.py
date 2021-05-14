#!/usr/bin/env python
'''Communicating with Benchtop RIGOL DG5000 Series'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # model's name e.g. ESG, PSG, AWG, VSA, ADC
debugger = 'debug' + mdlname

import pyvisa as visa
from functools import wraps
from pyqum.instrument.logger import address, set_status, status_code

def debug(state=False):
    exec('%s %s; %s = %s' %('global', debugger, debugger, 'state'), globals(), locals()) # open global and local both-ways channels!
    if state:
        print(Back.RED + '%s: Debugging Mode' %debugger.replace('debug', ''))
    return

debug() # declare the debugger mode here

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
        set_status(mdlname, dict(state='connected'))
        print(Fore.GREEN + "%s's connection Initialized: %s" % (mdlname, str(stat)))
    except: 
        set_status(mdlname, dict(state='DISCONNECTED'))
        print(Fore.RED + "%s's connection NOT FOUND" % mdlname)
        # bench = "disconnected"
    return bench

def Attribute(Name):
    @wraps(Name)
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
def model(bench, action=['Get', '']):
    SCPIcore = '*IDN'  #inquiring machine identity: "who r u?"
    return bench, SCPIcore, action
@Attribute
def savestate(bench, action):
    """action=['Set', '<reg 0-99>,<seq 0-9>']
    """
    SCPIcore = '*SAV'  #save machine state
    return bench, SCPIcore, action
@Attribute
def recallstate(bench, action):
    """action=['Set', '<reg 0-99>,<seq 0-9>']
    """
    SCPIcore = '*RCL'  #save machine state
    return bench, SCPIcore, action
@Attribute
def commentstate(bench, action): # query with parameters
    """action=['Set', '<reg 0-99>,<seq 0-9>,comment']
    or action=['Get', '<reg 0-99>,<seq 0-9>']
    """
    SCPIcore = ':MEMory:STATe:COMMENT'  #save machine state
    return bench, SCPIcore, action
@Attribute
def memory(bench, action=['Get', '']):
    SCPIcore = ':MEMory:CATalog:ALL'  #inquiring machine memory
    return bench, SCPIcore, action
@Attribute
def frequency(bench, action=['Get', '']):
    '''action=['Set','2GHz']'''
    SCPIcore = ':SOUR:FREQ:FIXED'
    return bench, SCPIcore, action
@Attribute
def power(bench, action=['Get', '']): 
    '''action=['Set','-7dbm']'''
    SCPIcore = ':SOUR:POW:LEVEL'
    return bench, SCPIcore, action
@Attribute
def output(bench, action=['Get', '']):
    SCPIcore = ':OUTP:STATE'
    return bench, SCPIcore, action

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
    debug(detail)
    print(Back.WHITE + Fore.MAGENTA + "Debugger mode: %s" %eval(debugger))
    s = Initiate(1)
    if eval(debugger):
        print(Fore.RED + "Detailed Test:")
        model(s)
        # recallstate(s, action=['Set', '1,0'])
        frequency(s)
        p = float(power(s))
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


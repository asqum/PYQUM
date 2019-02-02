#!/usr/bin/env python
'''For logging file'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from pathlib import Path
from os import stat, SEEK_END
from os.path import exists, getsize
from time import time, ctime
from contextlib import suppress
import inspect, json, wrapt

__author__ = "Teik-Hui Lee"
__copyright__ = "Copyright 2019, The Pyqum Project"
__credits__ = ["Chii-Dong Chen", "Yu-Cheng Chang"]
__license__ = "GPL"
__version__ = "beta3"
__email__ = "teikhui@phys.sinica.edu.tw"
__status__ = "development"

pyfilename = inspect.getfile(inspect.currentframe()) # current pyscript filename (usually with path)
INSTR_PATH = Path(pyfilename).parents[2] / "INSTLOG" # 2 levels up the path
USR_PATH = Path(pyfilename).parents[2] / "USRLOG"
# print(Path(pyfilename).parts[-1]) # last part of the path

def clocker(stage, prev=0):
    now = time()
    duration = now - prev
    if int(stage) > 0:
        print(Fore.BLUE + Back.WHITE + "It took {:.5f}s to complete {:d}-th stage\n".format(duration, stage))
    stage += 1
    return stage, now

def status_code(status):
    if status == 0:
        return "Success!"
    else: return "error %s" % status

def output_code(output):
    if output == "1":
        return "ON"
    elif output == "0":
        return "OFF"

def loginstr(instr_name):
    '''[Existence, Assigned Path] = loginstr(Instrument's name)
    '''
    pyqumfile = instr_name + "status.pyqum"
    pqfile = Path(INSTR_PATH) / pyqumfile
    existence = exists(pqfile) and stat(pqfile).st_size > 0
    return existence, pqfile

def get_status(instr_name):
    '''Get Instrument Status from LOG
    '''
    instr_log = loginstr(instr_name)
    if instr_log[0] == False:
        instrument = None # No such Instrument
    else:
        with open(instr_log[1]) as jfile:
            instrument = json.load(jfile) # in json format
    return instrument

def set_status(instr_name, info):
    '''Set Instrument Status for LOG
    * <info> must be a DICT'''
    instrument = get_status(instr_name)
    if instrument is None:
        instrument = {}
    instrument.update(info)
    with open(loginstr(instr_name)[1], 'w') as jfile:
        json.dump(instrument, jfile)

def address(instr_name, reset=False):
    '''Use Built-in Params as Default
    Set <reset=False> to directly load from LOG if it contains "address" 
    '''
    rs = dict()
    rs['RDG'] = 'TCPIP0::192.168.1.179::INSTR'
    rs['YOKO'] = "GPIB0::2::INSTR"
    rs['RDS'] = 'TCPIP0::192.168.1.81::INSTR'
    rs["PSGV"] = 'TCPIP0::192.168.1.35::INSTR'
    rs["ENA"] = 'TCPIP0::192.168.1.85::INSTR'
    rs["PNA"] = "TCPIP0::192.168.0.6::hpib7,16::INSTR"
    rs["DSO"] = "GPIB0::7::INSTR" # Oscilloscope Agilent 54621A
    # rs["DSO"] = "visa://qdl-pc/GPIB0::7::INSTR" # Oscilloscope Agilent 54621A
    rs["ESG"] = "GPIB0::27::INSTR" # Interface TYPE + Number :: Address :: INSTR
    # rs["MXG"] = "TCPIP0::169.254.0.1::INSTR"
    rs["MXG"] = "TCPIP0::192.168.0.3::INSTR"
    # rs["VSA"] = "PXI0::22-14.0::INSTR;PXI0::22-12.0::INSTR;PXI0::22-9.0::INSTR;PXI0::22-8.0::INSTR;PXI0::27-0.0::INSTR"
    rs["VSA"] = "PXI22::12::0::INSTR;PXI22::14::0::INSTR;PXI22::8::0::INSTR;PXI22::9::0::INSTR;PXI27::0::0::INSTR"
    rs["AWG"] = "PXI20::14::0::INSTR"
    # rs["AWG"] = "visa://qdl-pc/PXI20::14::0::INSTR"
    rs["TEST"] = "PXISAMAZING"
    if instr_name in rs: # checking database
        instrument = get_status(instr_name)
        if instrument is None or "address" not in instrument or reset:
            set_status(instr_name,dict(address=rs[instr_name]))
            instrument = get_status(instr_name) # get status again after the update
        RS = instrument["address"]
    else: RS = None
    return RS

def loguser(usr_name, sample):
    '''[Existence, Assigned Path] = logfile(User's name)
    '''
    pyqumfile = "%s(%s)data.pyqum" %(usr_name, sample)
    pqfile = Path(USR_PATH) / pyqumfile
    existence = exists(pqfile) and stat(pqfile).st_size > 0 #The beauty of Python: if first item is false, second item will not be evaluated in AND-statement, thus avoiding errors
    return existence, pqfile

def get_data(usr_name, sample='Sample'):
    '''Get User's Data from LOG
    '''
    usr_log = loguser(usr_name, sample)
    if usr_log[0] == False:
        user = None # No such User
    else:
        with open(usr_log[1]) as jfile:
            user = json.load(jfile) # in json format
    return user

# SUPER IMPORTANT!!!
def set_data(usr_name, place, mission, machine, measuredata, sample='Sample'):
    '''LOG USER DATA
    * <measuredata> must be a DICT'''
    usr_bag = json.dumps({ctime(): {place: {mission: {machine: measuredata}}}}) #serialize the json
    user = get_data(usr_name, sample)
    if user is None:
        with open(loguser(usr_name, sample)[1], 'ab+') as jfile:
            jfile.write(bytes(usr_bag, 'ascii'))
    else:
        # pending: checking JSON format
        with open(loguser(usr_name, sample)[1], 'rb+') as ufile: # truncate the last letter from file
                    ufile.seek(-1, SEEK_END)
                    ufile.truncate()
        with open(loguser(usr_name, sample)[1], 'ab+') as jfile: #paste new data
            jfile.write(bytes(", ", 'ascii') + bytes(usr_bag[1:-1], 'ascii') + bytes("}", 'ascii'))
    return

# Debugger settings
def debug(mdlname, state=False):
    debugger = 'debug' + mdlname
    exec('%s %s; %s = %s' %('global', debugger, debugger, 'state'), globals(), locals()) # open global and local both-ways channels!
    if state:
        print(Back.RED + '%s: Debugging Mode' %debugger.replace('debug', ''))
    return eval(debugger)

# SCPI Translator
@wrapt.decorator
def translate_scpi(Name, instance, a, b):
    
    mdlname, bench, SCPIcore, action = Name(*a, **b)
    debugger = 'debug' + mdlname
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
            elif ' ' in str(action[i+1]) and not "'" in str(action[i+1]): #set parameters for each header by certain parakey
                actionwords = str(action[i+1]).split(' ')
                oddwords, evenwords, J = actionwords[1::2], actionwords[0::2], []
                # print("Odd: %s; Even: %s"%(oddwords,evenwords))
                for j,h in enumerate(headers):
                    for w,word in enumerate(oddwords):
                        if evenwords[w].upper() in h.upper(): #only need to type part of the header(core)!
                            headers[j] = h.upper() + word
                            J.append(j)
                statement = ','.join([headers[sel] for sel in J])    
                paravalues.append(statement) #will appear in the <ans>
                command.append(parakeys[i])
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
        print(Fore.CYAN + "SCPI Command: {%s}" %command)
        if action[0] == 'Get':
            print(Fore.YELLOW + "%s %s's %s: %s <%s>" %(action[0], mdlname, Name.__name__, ans, status))
        if action[0] == 'Set':
            print(Back.YELLOW + Fore.MAGENTA + "%s %s's %s: %s <%s>" %(action[0], mdlname, Name.__name__ , ans, status))

    return status, ans


def test():
    pass
    return
    


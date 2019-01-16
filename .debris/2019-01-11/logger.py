'''For logging file'''
from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from pathlib import Path
from os import stat, SEEK_END
from os.path import exists, getsize
import inspect, json
from time import time, ctime

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
    return exists(pqfile), pqfile

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
    rs["ENA"] = 'TCPIP0::169.254.176.142::INSTR'
    rs["PNA"] = "TCPIP0::192.168.0.6::hpib7,16::INSTR"
    # rs["DSO"] = "GPIB0::7::INSTR" # Oscilloscope Agilent 54621A
    rs["DSO"] = "visa://qdl-pc/GPIB0::7::INSTR" # Oscilloscope Agilent 54621A
    rs["ESG"] = "GPIB0::27::INSTR" # Interface TYPE + Number :: Address :: INSTR
    rs["MXG"] = "TCPIP0::169.254.0.1::INSTR"
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

def loguser(usr_name):
    '''[Existence, Assigned Path] = logfile(User's name)
    '''
    pyqumfile = usr_name + "data.pyqum"
    pqfile = Path(USR_PATH) / pyqumfile
    existence = exists(pqfile) and stat(pqfile).st_size > 0 #The beauty of Python: if first item is false, second item will not be evaluated in AND-statement, thus avoiding errors
    return existence, pqfile

def get_data(usr_name):
    '''Get User's Data from LOG
    '''
    usr_log = loguser(usr_name)
    if usr_log[0] == False:
        user = None # No such User
    else:
        with open(usr_log[1]) as jfile:
            user = json.load(jfile) # in json format
    return user

def set_data(usr_name, place, mission, machine, measuredata):
    '''LOG USER DATA
    * <measuredata> must be a DICT'''
    usr_bag = json.dumps({ctime(): {place: {mission: {machine: measuredata}}}}) #serialize the json
    user = get_data(usr_name)
    if user is None:
        with open(loguser(usr_name)[1], 'ab+') as jfile:
            jfile.write(bytes(usr_bag, 'ascii'))
    else:
        # pending: checking JSON format
        with open(loguser(usr_name)[1], 'rb+') as ufile: # truncate the last letter from file
                    ufile.seek(-1, SEEK_END)
                    ufile.truncate()
        with open(loguser(usr_name)[1], 'ab+') as jfile: #paste new data
            jfile.write(bytes(", ", 'ascii') + bytes(usr_bag[1:-1], 'ascii') + bytes("}", 'ascii'))
    return

def search_param(usrdata, param, prepath=()):
    Paths =[]
    for k, v in usrdata.items():
        path = prepath + (k,)
        if v == param:
            # Paths.append(path)
            yield path
        elif hasattr(v, 'items'):
            p = search_param(v, param, path)
            if p is not None:
                # Paths.append(path)
                # print(Paths)
                yield p

def test_logger():

    return
    
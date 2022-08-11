'''For logging file'''

from pathlib import Path
from os.path import exists, getsize
import inspect, json

pyfilename = inspect.getfile(inspect.currentframe()) # current pyscript filename (usually with path)
INSTR_PATH = Path(pyfilename).parents[2] / "INSTLOG" # 2 levels up the path
# print(Path(pyfilename).parts[-1]) # last part of the path

def logfile(instr_name):
    '''[Existence, Assigned Path] = logfile(Instrument's name)
    '''
    pyqumfile = instr_name + "status.pyqum"
    pqfile = Path(INSTR_PATH) / pyqumfile
    return exists(pqfile), pqfile

def get_status(instr_name):
    '''Get Instrument Status from LOG
    '''
    instr_log = logfile(instr_name)
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
    with open(logfile(instr_name)[1], 'w') as jfile:
        json.dump(instrument, jfile)

def address(instr_name, reset=False):
    '''Use Built-in Params as Default
    Set <reset=False> to directly load from LOG if it contains "address" 
    '''
    rs = dict()
    rs["ESG"] = "GPIB2::27::INSTR"
    rs["VSA"] = "PXI24::12::0::INSTR;PXI24::14::0::INSTR;PXI24::8::0::INSTR;PXI24::9::0::INSTR;PXI29::0::0::INSTR"
    rs["AWG"] = "PXI22::14::0::INSTR" # ONLY this format is compatible
    rs["TEST"] = "PXISAMAZING"
    if instr_name in rs: # checking database
        instrument = get_status(instr_name)
        if instrument is None or "address" not in instrument or reset:
            set_status(instr_name,dict(address=rs[instr_name]))
            instrument = get_status(instr_name) # get status again after the update
        RS = instrument["address"]
    else: RS = None
    return RS

# set_status("VSA", dict(session=1))
# print(address("VSA", True)) # use this to reset the address in the LOG


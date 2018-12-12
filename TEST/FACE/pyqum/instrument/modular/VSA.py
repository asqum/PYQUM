# communicating with modulars via dll
from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # modular's name e.g. AWG, VSA, ADC
debugger = 'debug' + mdlname

from functools import wraps
from ctypes import c_int, c_bool, c_char_p, byref, cdll, c_char, c_long, c_double # windll
from ctypes.util import find_library
from pyqum.instrument.logger import address, get_status, set_status, status_code

# dloc = "C:\\Program Files\\IVI Foundation\\IVI\Bin\\AgM9392_64.dll" #64-bit
lib_name = find_library('AgM9392_64.dll')
print(Fore.YELLOW + "%s's driver located: %s" %(mdlname, lib_name))
dll = cdll.LoadLibrary(lib_name) #Python is 64-bit

def debug(state=False):
    exec('%s %s; %s = %s' %('global', debugger, debugger, 'state'), globals(), locals()) # open global and local both-ways channels!
    if state:
        print(Back.RED + '%s: Debugging Mode' %debugger.replace('debug', ''))
    return

debug() # declare the debugger mode here

## The name should be consistent with the functions provided in driver's manual
# 1. Initialize
def InitWithOptions(IdQuery=False, Reset=False, OptionsString=''):
    '''status = InitWithOptions(IdQuery, Reset, OptionsString)
    '''
    rs = address(mdlname, reset=eval(debugger)) # Instrument's Address
    Resource = bytes(rs, 'ascii')
    Option = bytes(OptionsString, 'ascii') # utf-8
    Session = c_long()
    AGM = dll.AgM9392_InitWithOptions # from AgM9392.chm
    AGM.restype = c_int
    status = AGM(c_char_p(Resource), c_bool(IdQuery), c_bool(Reset), c_char_p(Option), byref(Session))
    msession = Session.value
    if status == 0:
        set_status(mdlname, dict(state="Initialized Successfully", session=msession))
    else: 
        set_status(mdlname, dict(state="Error: " + str(status)))
        msession = get_status(mdlname)["session"]
    print(Fore.GREEN + "%s's connection Initialized at session %s: %s" % (mdlname, msession, status_code(status)))
    
    return msession

## WRAPPER
# 2.1 Get/Set Attribute (String, Int32, Real64)
def Attribute(Name):
    @wraps(Name)
    def wrapper(*a, **b):
        
        session, Type, RepCap, AttrID, buffsize, action = Name(*a, **b)
        RepCap = bytes(RepCap, "ascii")
        
        AGM = getattr(dll, 'AgM9392_' + action[0] + 'AttributeVi' + Type)
        AGM.restype = c_int # return status (error)
        
        if action[0] == "Get":
            if Type == 'String':
                action[1] = (c_char*888)() # char array: answer value format (use byref)
                status = AGM(c_long(session), c_char_p(RepCap), c_int(AttrID), c_long(buffsize), byref(action[1]))
                ans = [x.decode("ascii") for x in action[1]] # decoding binary # if x is not b'\x00'
                while '\x00' in ans:
                    ans.remove('\x00')
                ans = "".join(ans) # join char array into string
            elif Type == 'Int32':
                action[1] = c_long()
                status = AGM(c_long(session), c_char_p(RepCap), c_int(AttrID), byref(action[1]))
                ans = action[1].value
            elif Type == 'Real64':
                action[1] = c_double()
                status = AGM(c_long(session), c_char_p(RepCap), c_int(AttrID), byref(action[1]))
                ans = action[1].value
            
            if eval(debugger):
                print(Fore.YELLOW + "%s %s's %s: %s, %s" %(action[0], mdlname, Name.__name__, ans, status_code(status)))
            if status == 0:
                set_status(mdlname, {Name.__name__ : ans}) #logging the name and value of the attribute
            else: set_status(mdlname, {Name.__name__ : "Error: " + str(status)})

        elif action[0] == "Set":
            if Type == 'String':
                ans = action[1]
                action[1] = bytes(action[1], 'ascii')
                status = AGM(c_long(session), c_char_p(RepCap), c_int(AttrID), c_char_p(action[1]))
            elif Type == 'Int32':
                ans = action[1]
                status = AGM(c_long(session), c_char_p(RepCap), c_int(AttrID), c_long(action[1]))
            elif Type == 'Real64':
                ans = action[1]
                status = AGM(c_long(session), c_char_p(RepCap), c_int(AttrID), c_double(action[1]))
            if eval(debugger):
                print(Back.YELLOW + Fore.MAGENTA + "%s %s's %s: %s, %s" %(action[0], mdlname, Name.__name__, ans, status_code(status)))
            # No logging for "Set"

        return status, ans
    return wrapper

@Attribute
#define AGM9392_ATTR_INSTRUMENT_MODEL 1050512
def model(session, Type='String', RepCap='', AttrID=1050512, buffsize=2048, action=['Get', '']):
    """[Model Inquiry]
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM9392_ATTR_IO_RESOURCE_DESCRIPTOR 1050304
def resource_descriptor(session, Type='String', RepCap='', AttrID=1050304, buffsize=2048, action=['Get', '']):
    """[Get Resource Descriptor]
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM9392_ATTR_NUMBER_OF_SAMPLES 1150021
def samples_number(session, Type='Int32', RepCap='', AttrID=1150021, buffsize=0, action=['Get', '']):
    """[Get Number of Samples]
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM9392_ATTR_ACQUISITION_TIME 1150005
def acquisition_time(session, Type='Real64', RepCap='', AttrID=1150005, buffsize=0, action=['Get', '']):
    """[Get/Set Acquisition Time]
    """
    return session, Type, RepCap, AttrID, buffsize, action


# 3. close
def close(session):
    '''status = close(session)
    '''
    
    AGMclose = dll.AgM9392_close
    status = AGMclose(c_long(session))
    if status == 0:
        set_status(mdlname, dict(state="Closed Successfully"))
    else: set_status(mdlname, dict(state="Error: " + str(status)))
    print(Back.WHITE + Fore.BLACK + "%s's connection Closed: %s" %(mdlname, status_code(status)))
    return status


# Test Zone
def test(detail=False):
    debug(detail)
    print(Back.WHITE + Fore.MAGENTA + "Debugger mode: %s" %eval(debugger))
    s = InitWithOptions()
    # s = InitWithOptions()
    # s = int(input("Session: "))
    if eval(debugger):
        print(Fore.RED + "Detailed Test:")
        resource_descriptor(s)
        model(s)
        acquisition_time(s)
    else: print(Fore.RED + "Basic IO Test")
    close(s)
    return

# test(True)

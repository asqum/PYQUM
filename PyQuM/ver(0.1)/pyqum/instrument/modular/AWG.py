'''communicating with modular AWG via dll
'''
from functools import wraps
from ctypes import c_int, c_bool, c_char_p, byref, cdll, c_char, c_long, c_double
from ctypes.util import find_library
from pyqum.instrument.logger import address, get_status, set_status

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

# dloc = "C:\\Program Files\\IVI Foundation\\IVI\Bin\\AgM9392_64.dll" #64-bit
lib_name = find_library('AgM933x_64.dll')
dll = cdll.LoadLibrary(lib_name) #Python is 64-bit
AWGrs = address("AWG")

## The name should be consistent with the functions provided in driver's manual
# 1. Initialize
def InitWithOptions(IdQuery=True, Reset=True, OptionsString='Simulate=false, DriverSetup=DDS=false'):
    '''status = InitWithOptions(IdQuery, Reset, OptionsString)
    '''
    Resource = bytes(AWGrs, 'ascii')
    Option = bytes(OptionsString, 'ascii') # utf-8
    Session = c_long()
    AGM = dll.AgM933x_InitWithOptions # from AgM933x.chm
    AGM.restype = c_int
    status = AGM(c_char_p(Resource), c_bool(IdQuery), c_bool(Reset), c_char_p(Option), byref(Session))
    if status == 0:
        set_status("AWG", dict(state="Initialized", session=Session.value))
    else: set_status("AWG", dict(state="Error: " + str(status), session=Session.value))
    print(Fore.GREEN + "Initialized from AWG module at session %s" %Session.value)
    return status, Session.value

## WRAPPER
# 2. Get/Set Attribute (String, Int32, Real64)
def Attribute(Name):
    @wraps(Name)
    def wrapper(*a, **b):
        
        session, Type, RepCap, AttrID, buffsize, action = Name(*a, **b)
        RepCap = bytes(RepCap, "ascii")
        
        AGMmodel = getattr(dll, 'AgM933x_' + action[0] + 'AttributeVi' + Type)
        AGMmodel.restype = c_int # return status (error)
        
        if action[0] == "Get":
            if Type == 'String':
                action[1] = (c_char*888)() # char array: answer value format (use byref)
                status = AGMmodel(c_long(session), c_char_p(RepCap), c_int(AttrID), c_long(buffsize), byref(action[1]))
                ans = [x.decode("ascii") for x in action[1]] # decoding binary # if x is not b'\x00'
                while '\x00' in ans:
                    ans.remove('\x00')
                ans = "".join(ans) # join char array into string
            elif Type == 'Int32':
                action[1] = c_long()
                status = AGMmodel(c_long(session), c_char_p(RepCap), c_int(AttrID), byref(action[1]))
                ans = action[1].value
            elif Type == 'Real64':
                action[1] = c_double()
                status = AGMmodel(c_long(session), c_char_p(RepCap), c_int(AttrID), byref(action[1]))
                ans = action[1].value
        elif action[0] == "Set":
            if Type == 'String':
                ans = action[1]
                action[1] = bytes(action[1], 'ascii')
                status = AGMmodel(c_long(session), c_char_p(RepCap), c_int(AttrID), c_char_p(action[1]))
            elif Type == 'Int32':
                ans = action[1]
                status = AGMmodel(c_long(session), c_char_p(RepCap), c_int(AttrID), c_long(action[1]))
            elif Type == 'Real64':
                ans = action[1]
                status = AGMmodel(c_long(session), c_char_p(RepCap), c_int(AttrID), c_double(action[1]))
        if status == 0:
            set_status("AWG", {Name.__name__ : ans}) #logging the name and value of the attribute
        else: set_status("AWG", {Name.__name__ : "Error: " + str(status)})
        print(Fore.YELLOW + "[AWG module] %s: %s, error:%s" %(Name.__name__, ans, status))
        return status, ans
    return wrapper

@Attribute
#define AGM933X_ATTR_INSTRUMENT_MODEL 1050512
def model(session, Type='String', RepCap='', AttrID=1050512, buffsize=2048, action=['Get', '']):
    """[Model Inquiry]
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_ACTIVE_MARKER 1150058
def active_marker(session, Type='String', RepCap='', AttrID=1150058, buffsize=2048, action=['Get', '']):
    """[Get/Set Active Marker]
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_LOGICAL_NAME 1050305
def logical_name(session, Type='String', RepCap='', AttrID=1050305, buffsize=2048, action=['Get', '']):
    """[Get/Set Logical Name]
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_IO_RESOURCE_DESCRIPTOR 1050304
def resource_descriptor(session, Type='String', RepCap='', AttrID=1050304, buffsize=2048, action=['Get', '']):
    """[Get/Set Resource Descriptor]
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_MARKER_SOURCE 1150065
def marker_source(session, Type='Int32', RepCap='', AttrID=1150065, buffsize=0, action=['Get', '']):
    """[Get/Set Marker Source]
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_MARKER_DELAY 1150061
def marker_delay(session, Type='Real64', RepCap='', AttrID=1150061, buffsize=0, action=['Get', '']):
    """[Marker Delay]
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_MARKER_PULSE_WIDTH 1150064
def marker_pulse_width(session, Type='Real64', RepCap='', AttrID=1150064, buffsize=0, action=['Get', '']):
    """[Marker Pulse Width]
    """
    return session, Type, RepCap, AttrID, buffsize, action


# 3. close
def close(session):
    '''status = close(session)
    '''
    
    AGMclose = dll.AgM933x_close
    status = AGMclose(c_long(session))
    if status == 0:
        set_status("AWG", dict(state="Closed", session=session))
    else: set_status("AWG", dict(state="Error: " + str(status)))
    print(Back.WHITE + Fore.BLACK + "AWG module closed with error: %s" %status)
    return status



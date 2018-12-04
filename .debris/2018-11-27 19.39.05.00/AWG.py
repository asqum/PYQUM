# communicating with modulars via dll
from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # modular's name e.g. AWG, VSA, ADC
debugger = 'debug' + mdlname

from inspect import stack #extract method's name
from functools import wraps #facilitate wrapper's comments
from ctypes import c_int, c_bool, c_char_p, byref, cdll, c_char, c_long, c_double, c_float
from ctypes.util import find_library
from pyqum.instrument.logger import address, get_status, set_status, status_code

# dloc = "C:\\Program Files\\IVI Foundation\\IVI\Bin\\AgM933x_64.dll" #64-bit
lib_name = find_library('AgM933x_64.dll')
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
def InitWithOptions(IdQuery=False, Reset=False, OptionsString='Simulate=false, DriverSetup=DDS=false'):
    '''status = InitWithOptions(IdQuery, Reset, OptionsString)
    '''
    rs = address(mdlname, reset=eval(debugger)) # Instrument's Address
    Resource = bytes(rs, 'ascii')
    Option = bytes(OptionsString, 'ascii') # utf-8
    Session = c_long()
    
    AGM = dll.AgM933x_InitWithOptions # from AgM933x.chm
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
        
        AGM = getattr(dll, 'AgM933x_' + action[0] + 'AttributeVi' + Type)
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
            elif Type == 'Boolean':
                action[1] = c_bool()
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
            elif Type == 'Boolean':
                ans = action[1]
                status = AGM(c_long(session), c_char_p(RepCap), c_int(AttrID), c_bool(action[1]))
            if eval(debugger):
                print(Back.YELLOW + Fore.MAGENTA + "%s %s's %s: %s, %s" %(action[0], mdlname, Name.__name__, ans, status_code(status)))
            # No logging for "Set"

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
    """[Get Logical Name]
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_IO_RESOURCE_DESCRIPTOR 1050304
def resource_descriptor(session, Type='String', RepCap='', AttrID=1050304, buffsize=2048, action=['Get', '']):
    """[Get Resource Descriptor]
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_MARKER_SOURCE 1150065
def marker_source(session, Type='Int32', RepCap='', AttrID=1150065, buffsize=0, action=['Get', '']):
    """[Get/Set Marker Source]
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_ARB_SEQUENCE_HANDLE 1250211
def Arb_Seq_Handle(session, Type='Int32', RepCap='', AttrID=1250211, buffsize=0, action=['Get', '']):
    """[Get/Set Arbitrary Sequence Handle]
        RepCap=< channel# (1-2) >
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_MARKER_DELAY 1150061
def marker_delay(session, Type='Real64', RepCap='', AttrID=1150061, buffsize=0, action=['Get', '']):
    """[Get/Set Marker Delay]
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_MARKER_PULSE_WIDTH 1150064
def marker_pulse_width(session, Type='Real64', RepCap='', AttrID=1150064, buffsize=0, action=['Get', '']):
    """[Get/Set Marker Pulse Width]
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_PREDISTORTION_ENABLED 1150005
def predistortion_enabled(session, Type='Boolean', RepCap='', AttrID=1150005, buffsize=0, action=['Get', '']):
    """[Get/Set Predistortion Enabled]
    """
    return session, Type, RepCap, AttrID, buffsize, action

# 2.1 Abort Generation
def Abort_Gen(session):
    AGM = dll.AgM933x_AbortGeneration
    AGM.restype = c_int
    status = AGM(c_long(session))
    if eval(debugger):
        print(Back.YELLOW + Fore.MAGENTA + "%s: %s" %(stack()[0][3], status_code(status)))
    return status_code(status)

# 2.2 Output Configure Mode Advanced
def Output_Mode(session, mode=2):
    '''
    mode
        1: AGM933X_VAL_OUTPUT_MODE_ARBITRARY
        2: AGM933X_VAL_OUTPUT_MODE_SEQUENCE
        3: AGM933X_VAL_OUTPUT_MODE_ADVANCED_SEQUENCE
    '''
    AGM = dll.AgM933x_OutputConfigureModeAdvanced
    AGM.restype = c_int
    status = AGM(c_long(session), c_int(mode))
    if eval(debugger):
        print(Back.YELLOW + Fore.MAGENTA + "%s: %s" %(stack()[0][3], status_code(status)))
    return status_code(status)

# 2.3 Create Arbitrary Waveform
def CreateArbWaveform(session, Data):
    '''Data should be 1000 points minimum'''
    AGM = dll.AgM933x_CreateArbWaveform
    AGM.restype = c_int
    handle = c_long()
    Size = len(Data)
    carray = (c_double * Size)(*Data)
    status = AGM(c_long(session), c_int(Size), carray, byref(handle))
    if eval(debugger):
        print(Back.YELLOW + Fore.MAGENTA + "%s: %s (%s)" %(stack()[0][3], handle.value, status_code(status)))
    return status_code(status), handle.value

# 2.4 Create Arbitrary Sequence
def CreateArbSequence(session, sequence):
    '''Create Arbitrary Sequence
        sequence = < { waveform (handle.value from "CreateArbWaveform") : loop# (>0) } >
    '''
    AGM = dll.AgM933x_CreateArbSequence
    AGM.restype = c_int
    handle = c_long()
    Size = len(sequence)
    wfmhandles = (c_int * Size)(*[int(i) for i in sequence.keys()])
    loopcounts = (c_int * Size)(*[i for i in sequence.values()])
    status = AGM(c_long(session), c_int(Size), wfmhandles, loopcounts, byref(handle))
    if eval(debugger):
        print(Back.YELLOW + Fore.MAGENTA + "%s: %s (%s)" %(stack()[0][3], handle.value, status_code(status)))
    return status_code(status), handle.value

# 2.5 Configure Sample Rate
def ConfigSampRate(session, SampRate):
    """Configure Sample Rate
    """
    AGM = dll.AgM933x_ConfigureSampleRate
    AGM.restype = c_int
    status = AGM(c_long(session), c_double(SampRate))
    if eval(debugger):
        print(Back.YELLOW + Fore.MAGENTA + "%s: %s (%s)" %(stack()[0][3], SampRate, status_code(status)))
    return status_code(status)

# 2.6 Configure Output State (Enabled/Disabled)
def ConfigOupState(session, channel, state):
    """Configures whether the signal the function generator produces appears at a channel's output connector.
    """
    AGM = dll.AgM933x_ConfigureOutputEnabled
    AGM.restype = c_int
    channel = bytes(channel, 'ascii')
    status = AGM(c_long(session), c_char_p(channel), c_bool(state))
    if eval(debugger):
        print(Back.YELLOW + Fore.MAGENTA + "%s: channel=%s, state=%s (%s)" %(stack()[0][3], str(channel, 'ascii'), state, status_code(status)))
    return status_code(status)

# 2.7 Output Configuration (Type)
def OupConfig(session, channel, outputmode, filteron, Bandwidth):
    """This function allows you to: specify the kind of electrical output generated by the function generator, 
    select the frequency of the low-pass reconstruction filter, and enable/disable that filter.
    """

    AGM = dll.AgM933x_OutputConfigure
    AGM.restype = c_int
    channel = bytes(channel, 'ascii')


# 3. close
def close(session):
    '''status = close(session)
    '''
    
    AGMclose = dll.AgM933x_close
    status = AGMclose(c_long(session))
    if status == 0:
        set_status(mdlname, dict(state="Closed Successfully"))
    else: set_status(mdlname, dict(state="Error: " + str(status)))
    print(Back.WHITE + Fore.BLACK + "%s's connection Closed: %s" %(mdlname, status_code(status)))
    return status


# Test Zone
def test(detail=False):
    debug(detail)
    print(Fore.RED + "Debugger mode: %s" %eval(debugger))
    s = InitWithOptions()
    # s = InitWithOptions()
    if detail:
        resource_descriptor(s)
        model(s)
        active_marker(s)
        active_marker(s, action=["Set", "3"])
        active_marker(s)
        marker_source(s)
        marker_source(s, action=["Set", 10])
        marker_source(s)
        marker_delay(s)
        marker_delay(s, action=["Set", 5e-7])
        marker_delay(s)
        # Preparing AWGenerator
        Abort_Gen(s)
        Output_Mode(s)
        predistortion_enabled(s, action=["Set", False])
        predistortion_enabled(s)
        # Assigning handles to each different waveform
        stat = CreateArbWaveform(s, ([i*0 for i in range(100)] + [i*1 for i in range(1000)] + [i*0 for i in range(100)]))
        h1 = stat[1]
        stat = CreateArbWaveform(s, list([i*0 for i in range(1200)]))
        h2 = stat[1]
        # Composing different sequences to each channel
        # Channel 1
        Seq = {}
        Seq[str(h1)], Seq[str(h2)] = 1, 5
        stat = CreateArbSequence(s, Seq)
        Arb_Seq_Handle(s, RepCap='1', action=["Set", stat[1]])
        Arb_Seq_Handle(s, RepCap='1')
        # Channel 2
        Seq = {}
        Seq[str(h1)], Seq[str(h2)] = 2, 1
        stat = CreateArbSequence(s, Seq)
        Arb_Seq_Handle(s, RepCap='2', action=["Set", stat[1]])
        Arb_Seq_Handle(s, RepCap='2')
        # Setting Sample Rate
        ConfigSampRate(s, 1250000000)
        # Configure Output
        ConfigOupState(s, '1', True)
        ConfigOupState(s, '2', True)
    else: print(Fore.RED + "Basic IO Test")
    close(s)
    return

# test(True)

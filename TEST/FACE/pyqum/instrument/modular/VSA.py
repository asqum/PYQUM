# communicating with modulars via dll
from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # modular's name e.g. AWG, VSA, ADC
debugger = 'debug' + mdlname

from inspect import stack #extract method's name
from functools import wraps
from ctypes import c_int, c_bool, c_char_p, byref, cdll, c_char, c_long, c_double, c_float
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
# 2.1 Get/Set Attribute (String, Int32, Real64, Boolean)
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
            elif Type == 'Boolean':
                action[1] = c_bool()
                status = AGM(c_long(session), c_char_p(RepCap), c_int(AttrID), byref(action[1]))
                ans = action[1].value
            
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

        # Reformatting Answer if RepCap has something:
        RepCap = RepCap.decode('ascii')
        if RepCap != "":
            hashtag = " #Channel %s" %(RepCap)
        else: hashtag = ""

        # Logging Answer:
        if action[0] == "Get": # No logging for "Set"
            if  status == 0:
                set_status(mdlname, {Name.__name__ + hashtag : ans}) #logging the name and value of the attribute
            else: set_status(mdlname, {Name.__name__ + hashtag : "Error: " + str(status)})

        # Debugging
        if eval(debugger):
            if action[0] == "Get":
                print(Fore.YELLOW + "%s %s's %s: %s, %s" %(action[0], mdlname, Name.__name__ + hashtag, ans, status_code(status)))
            if action[0] == "Set":
                print(Back.YELLOW + Fore.MAGENTA + "%s %s's %s: %s, %s" %(action[0], mdlname, Name.__name__ + hashtag, ans, status_code(status)))

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
    Returns the integer number of complex samples that will be available to Get Data or Get Data Block when the measurement completes.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM9392_ATTR_TRIGGER_SOURCE 1150007
def trigger_source(session, Type='Int32', RepCap='', AttrID=1150007, buffsize=0, action=['Get', '']):
    """[Trigger Source]
    Sets the trigger source to Immediate, External, Video, Video Sync Out, or External Sync Out. Reset value: Immediate. 
    NOTE: This setting has no effect on the hardware until Measurements.Initiate() is called.
    ENUM:
        2. AgM9392TriggerSourceImmediate:       Triggers the measurement immediately after the measurement is armed.
        5. AgM9392TriggerSourceVideo:	        Triggers the measurement when the video signal satisfies the constraints specified by Trigger.Video interface
        1. AgM9392TriggerSourceExternal:        Triggers the measurement when the external trigger signal satisfies the constraints specified by the Trigger.External interface
        3. AgM9392TriggerSourceVideoSyncOut:    Triggers the measurement when the video signal satisfies the constraints specified by Trigger.Video interface on a master digitizer module. 
        4. AgM9392TriggerSourceExternalSyncOut:	Triggers the measurement when the external trigger signal satisfies the constraints specified by Trigger.External interface on a master digitizer module.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM9392_ATTR_EXTERNAL_TRIGGER_SLOPE 1150012
def external_trigger_slope(session, Type='Int32', RepCap='', AttrID=1150012, buffsize=0, action=['Get', '']):
    """[External Trigger Slope]
    The required slope of the input signal as it crosses the trigger level to generate an External trigger. 
    Allowable values are Rising and Falling. The value on reset is: Rising.
    ENUM:
        1. AgM9392ExternalTriggerSlopePositive: When Trigger.Source is External, require a positive slope through the trigger level in order to trigger.
        2. AgM9392ExternalTriggerSlopeNegative:	When Trigger.Source is External, require a negative slope through the trigger level in order to trigger.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM9392_ATTR_TRIGGER_TIMEOUT 1150008
def trigger_timeout(session, Type='Int32', RepCap='', AttrID=1150008, buffsize=0, action=['Get', '']):
    """[Trigger Timeout (ms)]
    Sets trigger timeout to avoid instrument lock up when a trigger has not been received. The timer is started when the VSA is armed. 
    Range of allowable values is 0 to 1100 seconds. Reset value: 1000 ms.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM9392_ATTR_ACQUISITION_TIME 1150005
def acquisition_time(session, Type='Real64', RepCap='', AttrID=1150005, buffsize=0, action=['Get', '']):
    """[Acquisition Time (s)]
    Approximate acquisition time of the measurement, in seconds. The number of samples will be rounded up to slightly exceed the requested time range. 
    The allowable range of values depends on bandwidth and the amount of memory available. Absolute maximum is 1000 seconds. Reset value: 250 us.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM9392_ATTR_BANDWIDTH 1150004
def bandwidth(session, Type='Real64', RepCap='', AttrID=1150004, buffsize=0, action=['Get', '']):
    """[Bandwidth (Hz)]
    The digital IF will be configured to provide at least the bandwidth specified. The allowable range of values depends on hardware configuration. 
    The absolute maximum is 250 MHz. Reset value: 40 MHz.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM9392_ATTR_FREQUENCY 1150002
def frequency(session, Type='Real64', RepCap='', AttrID=1150002, buffsize=0, action=['Get', '']):
    """[Frequency (hertz)]
    The nominal (sometimes called center) frequency, in hertz, of the signal to be measured. 
    The allowable range of values depend on hardware configuration, absolute limits are 50 MHz to 26.5 GHz. Reset value: 8 GHz.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM9392_ATTR_POWER 1150003
def power(session, Type='Real64', RepCap='', AttrID=1150003, buffsize=0, action=['Get', '']):
    """[Power (dBm)]
    Expected RMS power of the input signal, in dBm. Limits depend on hardware configuration. 
    Absolute max is +30 dBm. Reset value: -10 dBm.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM9392_ATTR_EXTERNAL_TRIGGER_LEVEL 1150009
def external_trigger_level(session, Type='Real64', RepCap='', AttrID=1150009, buffsize=0, action=['Get', '']):
    """[External Trigger Level (volts)]
    The external trigger level, in volts, when Trigger.Source is External. Range of allowable values -1.0 V to 1.0 V. Reset value: 1.0 V.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM9392_ATTR_TRIGGER_DELAY 1150006
def trigger_delay(session, Type='Real64', RepCap='', AttrID=1150006, buffsize=0, action=['Get', '']):
    """[Trigger Delay (seconds)]
    Specifies the trigger delay, in seconds. The range of allowable values is -1*acquisition time to +1000 seconds. Reset value: 0 seconds.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM9392_ATTR_SAMPLE_RATE 1150020
def sample_rate(session, Type='Real64', RepCap='', AttrID=1150020, buffsize=0, action=['Get', '']):
    """[Sample Rate (Hz)]
    The sample rate, in Hz, of the time record returned by Get Data or Get Data Block.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM9392_ATTR_PRESELECTOR_ENABLED 1150040
def preselector_enabled(session, Type='Boolean', RepCap='', AttrID=1150040, buffsize=0, action=['Get', '']):
    """[Preselector Enabled <?>]
    For instruments configured with a microwave preselector (M9360), use this setting to indicate that you want the preselector used for the measurement. 
    Reset value: false
    """
    return session, Type, RepCap, AttrID, buffsize, action

# 2.2 Initiate Measurement
def Init_Measure(session):
    """[Initiate the Measurement]
    Initiates a measurement with the settings specified by the Acquisition and Trigger interfaces.
    """
    AGM = dll.AgM9392_Initiate
    AGM.restype = c_int
    status = AGM(c_long(session))
    print(Fore.GREEN + "%s's measurement Initiated: %s" % (mdlname, status_code(status)))
    return status_code(status)

# 2.3 Arm Measurement
def Arm_Measure(session):
    """[Arm the Measurement]
    Arms the measurement started by Initiate().
    """
    AGM = dll.AgM9392_Arm
    AGM.restype = c_int
    status = AGM(c_long(session))
    print(Fore.LIGHTGREEN_EX + "%s's measurement Armed: %s" % (mdlname, status_code(status)))
    return status_code(status)

# 2.5 Get Data
def Get_Data(session, ComplexDataBufferSize):
    """[Extracting Complex Data]
    Gets the I/Q measurement results.
    ComplexData:
        Array to hold the measurement data. Allocated by the caller (for performance). 
        The array size should be >= 2 * Measurements.NumberOfSamples (2* since the array will hold interleaved complex data)
    """
    AGM = dll.AgM9392_GetData
    AGM.restype = c_int
    ComplexData = (c_double*int(ComplexDataBufferSize))()
    ComplexDataActualSize = c_long()
    NumberCopied = c_long()
    status = AGM(c_long(session), c_long(ComplexDataBufferSize), byref(ComplexData), byref(ComplexDataActualSize), byref(NumberCopied))
    # print("Complex Data: %s" %[x for x in ComplexData])
    print("Actual Size: %s; Number Copied: %s" %(ComplexDataActualSize.value, NumberCopied.value))
    print(Fore.LIGHTWHITE_EX + "%s's Data Extracted: %s" % (mdlname, status_code(status)))
    return status


# 3. close
def close(session):
    '''[Close the connection]
    '''
    AGM = dll.AgM9392_close
    AGM.restype = c_int
    status = AGM(c_long(session))
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
    if eval(debugger):
        print(Fore.RED + "Detailed Test:")
        resource_descriptor(s)
        model(s)
        acquisition_time(s)
        preselector_enabled(s)
        frequency(s)
        power(s)
        bandwidth(s)
        # setting trigger
        trigger_source(s)
        trigger_delay(s)
        external_trigger_level(s)
        external_trigger_slope(s)
        trigger_timeout(s)
        # Measure
        Init_Measure(s)
        Arm_Measure(s)
        stat = samples_number(s)
        # Get Sample Rate
        sample_rate(s)
        # Extracting Data
        Get_Data(s, 2*stat[1])

    else: print(Fore.RED + "Basic IO Test")
    close(s)
    return

# test(True)

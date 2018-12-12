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
    '''[Initialize the connection]
    status = InitWithOptions(IdQuery, Reset, OptionsString)
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
#define AGM933X_ATTR_INSTRUMENT_MODEL 1050512
def model(session, Type='String', RepCap='', AttrID=1050512, buffsize=2048, action=['Get', '']):
    """[Model Inquiry <string>]
    The model number or name reported by the physical instrument.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_ACTIVE_MARKER 1150058
def active_marker(session, Type='String', RepCap='', AttrID=1150058, buffsize=2048, action=['Get', '']):
    """[Active Marker <string>]
    Establishes the active marker output connector. Once the output marker is selected, 
    it may be configured by setting one of the four marker attributes which determine the marker's source, delay, pulse width, and polarity.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_LOGICAL_NAME 1050305
def logical_name(session, Type='String', RepCap='', AttrID=1050305, buffsize=2048, action=['Get', '']):
    """[Logical Name <string>]
    Logical Name identifies a driver session in the Configuration Store. If Logical Name is not empty, the driver was initialized from information in the driver session. 
    If it is empty, the driver was initialized without using the Configuration Store.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_IO_RESOURCE_DESCRIPTOR 1050304
def resource_descriptor(session, Type='String', RepCap='', AttrID=1050304, buffsize=2048, action=['Get', '']):
    """[Resource Descriptor <string>]
    The resource descriptor specifies the connection to a physical device. It is either specified in the Configuration Store or passed in the ResourceName parameter of the Initialize function. 
    It is empty if the driver is not initialized.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_MARKER_SOURCE 1150065
def marker_source(session, Type='Int32', RepCap='', AttrID=1150065, buffsize=0, action=['Get', '']):
    """[Get/Set Marker Source <int32>]
    Sets/Gets the marker source. Markers may be output on the four marker output connectors.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_ARB_SEQUENCE_HANDLE 1250211
def arb_sequence_handle(session, Type='Int32', RepCap='', AttrID=1250211, buffsize=0, action=['Get', '']):
    """[Arbitrary Sequence Handle <int32>]
    Identifies which arbitrary sequence the function generator produces. 
    You create arbitrary sequences with the Create Arbitrary Sequence function. 
    This function returns a handle that identifies the particular sequence. 
    To configure the function generator to produce a specific sequence, set this attribute to the sequence's handle.
        Set:
            RepCap: < channel# (1-2) >
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_OUTPUT_MODE_ADVANCED 1150051
def output_mode_adv(session, Type='Int32', RepCap='', AttrID=1150051, buffsize=0, action=['Get', '']):
    """[Advance Output Mode <int32>]
    Sets/Gets the output mode, which may be Arbitrary Waveform, Arbitrary Sequence, or Advanced Sequence. 
    In Arbitrary Waveform mode, the generator outputs a single waveform. 
    In the other two modes, sequences of waveforms are output.
    Attribute value (mode):
        1: AGM933X_VAL_OUTPUT_MODE_ARBITRARY
        2: AGM933X_VAL_OUTPUT_MODE_SEQUENCE
        3: AGM933X_VAL_OUTPUT_MODE_ADVANCED_SEQUENCE
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_OPERATION_MODE 1250005
def operation_mode(session, Type='Int32', RepCap='', AttrID=1250005, buffsize=0, action=['Get', '']):
    """[Operation Mode <int32>]
    Sets/Gets how the function generator produces output. When set to Continuous mode, the waveform will be output continuously. 
    When set to Burst mode, the ConfigureBurstCount function is used to specify how many cycles of the waveform to output.
    RepCap: < channel# (1-2) >
    Attribute value (mode):
        0: AGM933X_VAL_OPERATE_CONTINUOUS	
        1: AGM933X_VAL_OPERATE_BURST	
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_TRIGGER_SOURCE_ADVANCED 1150052
def trigger_source_adv(session, Type='Int32', RepCap='', AttrID=1150052, buffsize=0, action=['Get', '']):
    """[Advanced Trigger Source <int32>]
    Specifies the advanced trigger source, which are can be selected from enums of AgM933XTriggerSourceEnum. 
    These sources may be chosen as individual sources or logically OR'd together to allow one of multiple sources to supply the trigger.
    RepCap: < channel# (1-2) >
    Attribute value (mode):
         0: AgM933xTriggerSourceNoTrigger	
         2: AgM933xTriggerSourceExternal1
         4: AgM933xTriggerSourceExternal2
         8: AgM933xTriggerSourceExternal3
        16:	AgM933xTriggerSourceExternal4
         1: AgM933xTriggerSourceSoftware1
        32: AgM933xTriggerSourceSoftware2
        64: AgM933xTriggerSourceSoftware3
       256: AgM933xTriggerSourceMarker1
       512: AgM933xTriggerSourceMarker2
      1024: AgM933xTriggerSourceMarker3
      2048: AgM933xTriggerSourceMarker4
      4096: AgM933xTriggerSourceAuxPort
      8063: AgM933xTriggerSourceAllSources
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_OUTPUT_CONFIGURATION 1150054
def output_config(session, Type='Int32', RepCap='', AttrID=1150054, buffsize=0, action=['Get', '']):
    """[Output Configuration <int32>]
    Specifies the configuration of the output signal.
    RepCap: < channel# (1-2) >
    Attribute value (mode):
        0: AgM933xOutputConfiguration: SingleEnded	
        1: AgM933xOutputConfiguration: Differential
        2. AgM933xOutputConfiguration: Amplified
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_OUTPUT_FILTER_BANDWIDTH 1150056
def output_filter_bandwidth(session, Type='Int32', RepCap='', AttrID=1150056, buffsize=0, action=['Get', '']):
    """[Output Filter Bandwidth <int32>]
    Specifies the bandwidth of the output channel. 
    This only affects the output signal when output filtering is enabled.
    RepCap: < channel# (1-2) >
    Attribute value (mode):
        0: AgM933xFilterBandwidth250MHz: Sets the bandwidth of the arbitrary waveform generator signal to 250 MHz.	
        1: AgM933xFilterBandwidth500MHz: Sets the bandwidth of the arbitrary waveform generator signal to 500 MHz.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_BURST_COUNT 1250350
def burst_count(session, Type='Int32', RepCap='', AttrID=1250350, buffsize=0, action=['Get', '']):
    """[Burst Count <int32>]
    Sets/Gets the number of waveform cycles that the function generator produces after it receives a trigger. 
    The Burst Count is used when the operation mode is Operate Burst.
    RepCap: < channel# (1-2) >
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_MARKER_DELAY 1150061
def marker_delay(session, Type='Real64', RepCap='', AttrID=1150061, buffsize=0, action=['Get', '']):
    """[Marker Delay <real64>]
    Sets/Gets the delay value, in seconds, for the marker connection identified through the Active Marker attribute. 
    Marker delay may be adjusted positive or negative. The limits may be determined with the GetAttrMinMaxViReal64 function.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_MARKER_PULSE_WIDTH 1150064
def marker_pulse_width(session, Type='Real64', RepCap='', AttrID=1150064, buffsize=0, action=['Get', '']):
    """[Marker Pulse Width <real64>]
    Sets/Gets the pulse width value, in seconds, for the marker connection identified through the Active Marker attribute. 
    Markers are always output as pulses of a programmable width. NOTE: Not available for Waveform markers.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_ARB_GAIN 1250202
def arb_gain(session, Type='Real64', RepCap='', AttrID=1250202, buffsize=0, action=['Get', '']):
    """[Arbitrary Gain <real64>]
    Sets/Gets the Gain for the waveform. Allowable range of values depends upon connection type: 
        Single ended passive mode = 0.170 to 0.250 (best signal fidelity); Single ended amplified = 0.340 to 0.500; 
        Differential = .340 to 0.500.This value is unitless.
        Set:
            RepCap=< channel# (1-2) >
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_ARB_SAMPLE_RATE 1250204
def arb_sample_rate(session, Type='Real64', RepCap='', AttrID=1250204, buffsize=0, action=['Get', '']):
    """[Arbitrary Sample Rate <real64>]
    Sets/Gets the sample rate in samples/sec (Sa/s). Sample rate may be set equal to the sample clock frequency (Output Clock Frequency), or reduced from there by factors of exactly two. 
        With sample clock source of Internal, undivided frequency = 1250 MHz.
        Set:
            RepCap=< channel# (1-2) >
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_OUTPUT_IMPEDANCE 1250004
def output_impedance(session, Type='Real64', RepCap='', AttrID=1250004, buffsize=0, action=['Get', '']):
    """[Output Impedance <real64>]
    Sets/Gets the output impedance on the specified channel. 
    Valid values are 0.0, 50.0 and 75.0 Ohms. A value of 0.0 indicates that the instrument is connected to a high impedance load. 
    Reset value: 50.0 Ohms.
        Set:
            RepCap=< channel# (1-2) >
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_OUTPUT_CLOCK_FREQUENCY 1150004
def output_clock_freq(session, Type='Real64', RepCap='', AttrID=1150004, buffsize=0, action=['Get', '']):
    """[Output Clock Frequency <real64>]
    This READ-ONLY attribute is used to ascertain the current clock frequency. 
    Changes to the clock frequency must be accomplished with the OutputConfigureSampleClock function.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_PREDISTORTION_ENABLED 1150005
def predistortion_enabled(session, Type='Boolean', RepCap='', AttrID=1150005, buffsize=0, action=['Get', '']):
    """[Predistortion Enabled <?>]
    Sets/Gets the Predistortion Enabled attribute. 
    If true (the default), any waveforms that are created are pre-distorted to compensate for amplitude and phase variations in the waveform generator's analog hardware. 
    If disabled, no corrections are made.
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_OUTPUT_ENABLED 1250003
def output_enabled(session, Type='Boolean', RepCap='', AttrID=1250003, buffsize=0, action=['Get', '']):
    """[Output Enabled <?>]
    Sets/Gets the output enabled state. 
    If set to True, the signal the function generator produces appears at the output connector. 
    If set to False, no signal is output.
    Set:
        RepCap=< channel# (1-2) >
    """
    return session, Type, RepCap, AttrID, buffsize, action

@Attribute
#define AGM933X_ATTR_OUTPUT_FILTER_ENABLED 1150055
def output_filter_enabled(session, Type='Boolean', RepCap='', AttrID=1150055, buffsize=0, action=['Get', '']):
    """[Output Filtering Enabled <?>]
    Enables output filtering selected by the FilterBandwidth property.
    Set:
        RepCap=< channel# (1-2) >
    """
    return session, Type, RepCap, AttrID, buffsize, action

# 2.1 Abort Generation
def Abort_Gen(session):
    """[Abort Waveform Generation]
    """
    AGM = dll.AgM933x_AbortGeneration
    AGM.restype = c_int
    status = AGM(c_long(session))
    print(Back.WHITE + Fore.BLACK + "%s's generation Aborted: %s" %(mdlname, status_code(status)))
    return status_code(status)

# 2.2 Create Arbitrary Waveform
def CreateArbWaveform(session, Data):
    '''[Create Arbitrary Waveform]
        *Data: 
            minimum: 1000 points
            maximum: 15000 points
    '''
    AGM = dll.AgM933x_CreateArbWaveform
    AGM.restype = c_int
    handle = c_long()
    Size = len(Data)
    carray = (c_double * Size)(*Data)
    status = AGM(c_long(session), c_int(Size), carray, byref(handle))
    if eval(debugger):
        # print("Data: %s" %Data)
        print(Back.YELLOW + Fore.MAGENTA + "%s: %s (%s)" %(stack()[0][3], handle.value, status_code(status)))
    return status_code(status), handle.value

# 2.3 Create Arbitrary Sequence
def CreateArbSequence(session, sequence, counts):
    '''[Create Arbitrary Sequence]
        sequence = < waveform (handle.value from "CreateArbWaveform") >
        counts = loop# (>0)
    '''
    AGM = dll.AgM933x_CreateArbSequence
    AGM.restype = c_int
    handle = c_long()
    Size = len(sequence)
    wfmhandles = (c_long * Size)(*sequence)
    loopcounts = (c_long * Size)(*counts)
    status = AGM(c_long(session), c_long(Size), wfmhandles, loopcounts, byref(handle))
    if eval(debugger):
        print("Sequence's size: %s" %Size)
        print("Sequence: %s" %sequence)
        print("Sequence's counts: %s" %counts)
        print(Back.YELLOW + Fore.MAGENTA + "%s: %s (%s)" %(stack()[0][3], handle.value, status_code(status)))
    return status_code(status), handle.value

# 2.4 Send Numbered Software Trigger (initiate burst/single pulse)
def Send_Pulse(session, triggernum=1):
    """[Sending Software Trigger to generate single/burst pulse]
    """
    AGM = dll.AgM933x_TriggerSendNumberedSoftwareTrigger
    AGM.restype = c_int
    status = AGM(c_long(session), c_long(triggernum))
    if eval(debugger):
        print(Back.YELLOW + Fore.MAGENTA + "%s: %s" %(stack()[0][3], status_code(status)))
    return status_code(status)

# 2.5 Initiate Generation
def Init_Gen(session):
    """[Initiate Waveform Generation]
    """
    AGM = dll.AgM933x_InitiateGeneration
    AGM.restype = c_int
    status = AGM(c_long(session))
    print(Fore.GREEN + "%s's generation Initialized: %s" % (mdlname, status_code(status)))
    return status_code(status)

# 2.6 Clear Arbitrary Memory
def Clear_ArbMemory(session):
    """Removes all previously created arbitrary waveforms and sequences from the instrument's memory and invalidates all waveform and sequence handles. 
    If either a waveform or sequence is currently being generated, an error will be reported.
    """
    AGM = dll.AgM933x_ClearArbMemory
    AGM.restype = c_int
    status = AGM(c_long(session))
    print(Fore.GREEN + "%s's arbitrary memory ALL Cleared: %s" % (mdlname, status_code(status)))
    return status_code(status)

# 3. close
def close(session):
    '''[Close the connection]
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
    Abort_Gen(s)
    # s = InitWithOptions()
    if detail:
        # basic queries:
        resource_descriptor(s)
        model(s)
        active_marker(s)
        marker_source(s)
        marker_delay(s)
        output_clock_freq(s)

        # Setting Marker:
        active_marker(s, action=["Set", "1"])
        active_marker(s)
        marker_source(s, action=["Set", 10])
        marker_source(s)
        marker_delay(s, action=["Set", 2e-7])
        marker_delay(s)
        marker_pulse_width(s, action=["Set", 2.5e-7])
        marker_pulse_width(s)

        # Preparing AWGenerator
        output_mode_adv(s, action=["Set", 2])
        output_mode_adv(s)
        predistortion_enabled(s, action=["Set", False])
        predistortion_enabled(s)

        # Setting Sample Rate
        arb_sample_rate(s, action=["Set", 1250000000])
        arb_sample_rate(s)
        
        seg0 = 5000
        seg1 = 5000
        seg2 = 5000
        # Create Waveform
        stat = CreateArbWaveform(s, ([1]*seg0))
        h1 = stat[1]
        stat = CreateArbWaveform(s, ([0]*seg1))
        h2 = stat[1]
        stat = CreateArbWaveform(s, ([-1]*seg2))
        h3 = stat[1]
        stat = CreateArbWaveform(s, ([0.5]*5000 + [1]*5000 + [-1]*5000))
        ch1 = stat[1]
        stat = CreateArbWaveform(s, ([0.8]*5000 + [-1]*5000))
        ch2 = stat[1]

        # Composing different sequences to each channel
        # Channel 1
        i = 1
        if i:
            # Seq, counts = [h1, h3], [1, 2] #Seqhandles, loops#
            Seq, counts = [ch1], [1] #unique wfm
            stat = CreateArbSequence(s, Seq, counts)
            print("Sequence handle for CH1: %s" %stat[1])
            arb_sequence_handle(s, RepCap='1', action=["Set", stat[1]])
            arb_sequence_handle(s, RepCap='1')
            output_enabled(s, RepCap='1', action=["Set", True])
            output_enabled(s, RepCap='1')
            output_filter_enabled(s, RepCap='1')
            output_filter_enabled(s, RepCap='1', action=["Set", False])
            output_filter_bandwidth(s, RepCap='1')
            output_filter_bandwidth(s, RepCap='1', action=["Set", 0])
            output_config(s, RepCap='1')
            output_config(s, RepCap='1', action=["Set", 0])
            arb_gain(s, RepCap='1', action=["Set", 0.25])
            arb_gain(s, RepCap='1')
            output_impedance(s, RepCap='1', action=["Set", 50])
            output_impedance(s, RepCap='1')
            # Setting pulse mode (Single or Continuous)
            operation_mode(s, RepCap='1')
            operation_mode(s, RepCap='1', action=["Set", 0])
            trigger_source_adv(s, RepCap='1')
            trigger_source_adv(s, RepCap='1', action=["Set", 0])
            burst_count(s, RepCap='1', action=["Set", 1000001])

        # Channel 2
        i = 1
        if i:
            # Seq, counts = [h2, h3], [1, 1] #Seqhandles, loops#
            Seq, counts = [ch2], [1] #unique wfm
            stat = CreateArbSequence(s, Seq, counts)
            print("Sequence handle for CH2: %s" %stat[1])
            arb_sequence_handle(s, RepCap='2', action=["Set", stat[1]])
            arb_sequence_handle(s, RepCap='2')
            output_enabled(s, RepCap='2', action=["Set", True])
            output_enabled(s, RepCap='2')
            output_filter_enabled(s, RepCap='2')
            output_filter_enabled(s, RepCap='2', action=["Set", False])
            output_filter_bandwidth(s, RepCap='2')
            output_filter_bandwidth(s, RepCap='2', action=["Set", 0])
            output_config(s, RepCap='2')
            output_config(s, RepCap='2', action=["Set", 0])
            arb_gain(s, RepCap='2', action=["Set", 0.25])
            arb_gain(s, RepCap='2')
            output_impedance(s, RepCap='2', action=["Set", 50])
            output_impedance(s, RepCap='2')
            # Setting pulse mode (Single or Continuous)
            operation_mode(s, RepCap='2')
            operation_mode(s, RepCap='2', action=["Set", 0])
            trigger_source_adv(s, RepCap='2')
            trigger_source_adv(s, RepCap='2', action=["Set", 0])
            burst_count(s, RepCap='2', action=["Set", 1000001])
            
        # if not bool(input("Press ENTER (OTHER KEY) to initiated (skip) generation: ")):
        Init_Gen(s)
        Send_Pulse(s, 1)
            
    else: print(Fore.RED + "Basic IO Test")
    close(s)
    return

test(True)

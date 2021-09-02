# SD DIG M3102A
from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # module's name e.g. PSG

from time import time
from numpy import array, zeros, reshape
from si_prefix import si_format, si_parse

from pyqum.instrument.logger import address, set_status
from pyqum.instrument.analyzer import curve

# SD1 Libraries
import sys
sys.path.append('C:\Program Files (x86)\Keysight\SD1\Libraries\Python')
import keysightSD1

# INITIALIZATION
def Initiate(which, mode='DATABASE'):
    ad = address(mode)
    rs = ad.lookup(mdlname, label=int(which)) # Instrument's Address
    try:
        # CREATE AND OPEN MODULE
        module = keysightSD1.SD_AIN()
        moduleID = module.openWithSlot("", int(rs.split('::')[0]), int(rs.split('::')[1])) # PRODUCT, CHASSIS::SLOT
        if moduleID < 0: print(Fore.RED + "Module open error:", moduleID)
        else: print(Fore.GREEN + "%s-%s's connection Initialized >> ID: %s, Name: %s, Chassis: %s, Slot: %s" % (mdlname,which, moduleID, module.getProductName(), module.getChassis(), module.getSlot()))
        
        set_status(mdlname, dict(state='connected'), which)
        ad.update_machine(1, "%s_%s"%(mdlname,which))
    except: 
        set_status(mdlname, dict(state='DISCONNECTED'), which)
        print(Fore.RED + "%s-%s's connection NOT FOUND" %(mdlname,which))
        # module = "disconnected"
    return module

# FUNCTIONS
def model(module):
    return ["model", {"IDN": "%s (%s)" %(module.getProductName(), module.getSerialNumber())}]
def sampling_rate(module):
    '''
    Sampling rate of the Digitizer in "Sampling Per Second"
    '''
    return float(module.clockGetFrequency())

# CONFIGURATION:
def ConfigureBoard(module, update_settings={}):
    '''DAQ CONFIGURATION FOR ALL CHANNELS ALTOGETHER:

    '''
    settings=dict(PXI=2, FULL_SCALE=2, TOTAL_POINTS=200000, NUM_CYCLES=100, triggerDelay_sec=0*1e-9) # default settings
    settings.update(update_settings)
    PXI, FULL_SCALE, TOTAL_POINTS, NUM_CYCLES, triggerDelay_sec = int(settings['PXI']), float(settings['FULL_SCALE']), settings['TOTAL_POINTS'], settings['NUM_CYCLES'], settings['triggerDelay_sec']

    dt_s = 1 / sampling_rate(module)
    for DAQ_CH in range(4):
        DAQ_CH += 1
        module.channelInputConfig(DAQ_CH, fullScale=FULL_SCALE, impedance=1, coupling=0)
        module.DAQconfig(DAQ_CH, pointsPerCycle=TOTAL_POINTS, nCycles=NUM_CYCLES, triggerDelay=round(triggerDelay_sec/dt_s), triggerMode=keysightSD1.SD_TriggerModes.EXTTRIG) 
        module.DAQdigitalTriggerConfig(DAQ_CH, keysightSD1.SD_TriggerExternalSources.TRIGGER_PXI+PXI, keysightSD1.SD_TriggerBehaviors.TRIGGER_FALL)

    samplesPerSec = sampling_rate(module)
    dt_ns = 1 / samplesPerSec / 1e-9 # in nano-second
    print(Fore.CYAN + "Sampling rate: %sSPS" %si_format(samplesPerSec, 0))
    return dt_ns

# ACQUISITION:
def AcquireData(module, recordtime_s, recordsum, update_settings={}):
    '''
    NOTE: The input for ‘nPoints’ must always be an even number. If you enter an odd number as input, the SD1 API returns the following message before continuing operation.
    “Warning: DAQ supports only even number of ‘DAQpointsPerCycle’. The input value is reduced by 1.”
    '''
    settings=dict(FULL_SCALE=2, READ_TIMEOUT=100, IQ_PAIR=[1,2]) # default settings
    settings.update(update_settings)
    FULL_SCALE, READ_TIMEOUT, IQ_PAIR = float(settings['FULL_SCALE']), settings['READ_TIMEOUT'], settings['IQ_PAIR']

    samplesPerSec = sampling_rate(module)
    dt_s = 1 / samplesPerSec # in second
    TOTAL_POINTS = round(recordtime_s/dt_s)
    DATA_V = zeros([2, recordsum*TOTAL_POINTS])

    # START DATA ACQUISITION:
    DAQmask = 0
    for i in IQ_PAIR: DAQmask += 2**(i-1) # Mask to select which DAQ-channels (e.g. 0b0011 where LSB is CH1, bit 1 is CH2 and so on).
    start_acq = time()

    module.DAQflushMultiple(DAQmask)
    module.DAQstartMultiple(DAQmask)
    for index, DAQ_CH in enumerate(IQ_PAIR):
        # DAQ ACQUISITION
        readPoints = module.DAQread(DAQ_CH, recordsum*TOTAL_POINTS, READ_TIMEOUT)
        print(Fore.YELLOW + "Total points read by CH-{}: {}".format(DAQ_CH, readPoints.size))
        # convert binary data to voltage
        DATA_V[index] = FULL_SCALE * ( readPoints / 2**(14+1))
    # STOP DAQ
    module.DAQstopMultiple(DAQmask)

    DATA_V = DATA_V.T.reshape(recordsum, TOTAL_POINTS, 2) # Interleaved IQ-pairs
    transferTime_sec = float(time() - start_acq)
    recordsPerBuffer, buffersPerAcquisition = recordsum, 1

    return DATA_V, transferTime_sec, recordsPerBuffer, buffersPerAcquisition

def close(module, which, mode='DATABASE'):
    try:
        module.close() #None means Success?
        status = "Success"
        ad = address(mode)
        ad.update_machine(0, "%s_%s"%(mdlname,which))
    except: status = "Error"
    set_status(mdlname, dict(state='disconnected: %s' %status), which)
    print(Back.WHITE + Fore.BLACK + "%s's connection Closed: %s" %(mdlname,status))
    return status

def check_timsum(record_time_ns, record_sum, update_settings={}):
    '''
    validate record_time_ns & record_sum
    '''
    bad_times = [] # a blacklist of bad record_time_ns
    return (record_time_ns, record_sum)


def test():
    recordsum = 12800
    recordtime_ns = 2560

    digModule = Initiate(1, mode="TEST")
    dt_ns = ConfigureBoard(digModule, dict(TOTAL_POINTS=round(recordtime_ns/2), NUM_CYCLES=recordsum ))

    while True:
        LOOP = input("Press ENTER (OTHER KEY) to CONTINUE (ESCAPE): ")
        if LOOP: break
        
        DATA_V = AcquireData(digModule, recordtime_ns*1e-9, recordsum)[0]

        # PLOT	
        plot_record = 7
        DATA_V = DATA_V.reshape([recordsum,round(recordtime_ns/dt_ns)*2])
        for r in range(plot_record):
            trace_I, trace_Q = DATA_V[r,:].reshape((round(recordtime_ns/dt_ns), 2)).transpose()[0], DATA_V[r,:].reshape((round(recordtime_ns/dt_ns), 2)).transpose()[1]
            curve([dt_ns*array(range(len(trace_I))),dt_ns*array(range(len(trace_Q)))], [trace_I,trace_Q], 'record-%s'%(r+1), 't (ns)', 'Pulse Response (V)')

    print("Exiting...")
    close(digModule, 1, mode="TEST")


# test()



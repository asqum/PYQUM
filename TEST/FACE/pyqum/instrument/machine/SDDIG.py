# SD DIG M3102A
from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # module's name e.g. PSG

from time import time, sleep
from numpy import array, zeros, reshape
from si_prefix import si_format, si_parse

from pyqum.instrument.logger import address, set_status, clocker
from pyqum.instrument.analyzer import curve
from pyqum.instrument.machine import SD_FPGA


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
        # module = keysightSD1.SD_AIN()
        module = SD_FPGA.SD_FPGA()
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
    FPGA: FPGA LEVEL
    '''
    settings=dict(PXI=2, FULL_SCALE=2, TOTAL_POINTS=200000, NUM_CYCLES=100, triggerDelay_sec=0*1e-9, FPGA=0) # default settings
    settings.update(update_settings)
    PXI, FULL_SCALE, TOTAL_POINTS, NUM_CYCLES, triggerDelay_sec, FPGA = int(settings['PXI']), float(settings['FULL_SCALE']), settings['TOTAL_POINTS'], settings['NUM_CYCLES'], settings['triggerDelay_sec'], int(settings["FPGA"])

    # 1. FPGA: SELECT LEVEL
    module.assignCard("M3102A")
    stage, now = clocker()
   
    module.loadFPGABitFile(FPGA)
    print(Fore.GREEN + "FPGA ENABLED: LEVEL-%s"%FPGA)


    dt_s = 1 / sampling_rate(module)
    for DAQ_CH in range(4):
        DAQ_CH += 1
        module.channelInputConfig(DAQ_CH, fullScale=FULL_SCALE, impedance=1, coupling=0)
        # 2. FPGA: SET REGISTER IF TRUE, NORMAL CONFIGURE IF OTHERWISE 
        module.DAQconfigFPGA(DAQ_CH, pt_per_shot=TOTAL_POINTS, shots=NUM_CYCLES, trig_delay=round(triggerDelay_sec/dt_s), trigger_mode=keysightSD1.SD_TriggerModes.EXTTRIG) # previously: module.DAQconfig 
        stage, now = clocker(stage, now, "DAQconfigAVE")
        if PXI < 0: # EXTERNAL FRONT-PANEL TRIGGER:
            print(Fore.CYAN + "Trigger from front panel EXT:")
            module.DAQdigitalTriggerConfig(DAQ_CH, keysightSD1.SD_TriggerExternalSources.TRIGGER_EXTERN, keysightSD1.SD_TriggerBehaviors.TRIGGER_RISE)
        else: # PXI-Marker from DAC cannot be easily customized to follow the main pulse...
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
    settings=dict(FULL_SCALE=2, READ_TIMEOUT=100, IQ_PAIR=[1,2], FPGA=0) # default settings
    settings.update(update_settings)
    FULL_SCALE, READ_TIMEOUT, IQ_PAIR, FPGA = float(settings['FULL_SCALE']), settings['READ_TIMEOUT'], settings['IQ_PAIR'], int(settings["FPGA"])

    samplesPerSec = sampling_rate(module)
    dt_s = 1 / samplesPerSec # in second
    TOTAL_POINTS = round(recordtime_s/dt_s)

    if FPGA == module.bitMode_Keysight: DATA_V = zeros([2, recordsum*TOTAL_POINTS])
    elif FPGA == module.bitMode_AVE : DATA_V = zeros([2, 1*TOTAL_POINTS])
    elif FPGA == module.bitMode_SingleDDC: DATA_V = zeros([4, recordsum*round(TOTAL_POINTS/5)])
    elif FPGA == module.bitMode_SingleDDC_Int: DATA_V = zeros([4, recordsum*round(TOTAL_POINTS/5)])
    elif FPGA == module.bitMode_SingleDDC_Spt: DATA_V = zeros([4, 1*round(TOTAL_POINTS/5)])
    elif FPGA == module.bitMode_AVE_SingleDDC: DATA_V = zeros([4, 1*round(TOTAL_POINTS/5)])
    elif FPGA == module.bitMode_AVE_SingleDDC_Int: DATA_V = zeros([4, 1*round(TOTAL_POINTS/5)])
    elif FPGA == module.bitMode_DualDDC: DATA_V = zeros([2, recordsum*round(TOTAL_POINTS/5)])
    elif FPGA == module.bitMode_DualDDC_Int: DATA_V = zeros([2, recordsum*round(TOTAL_POINTS/5)])
    elif FPGA == module.bitMode_DualDDC_Spt: DATA_V = zeros([2, 1*round(TOTAL_POINTS/5)])
    elif FPGA == module.bitMode_AVE_DualDDC: DATA_V = zeros([2, 1*round(TOTAL_POINTS/5)])
    elif FPGA == module.bitMode_AVE_DualDDC_Int: DATA_V = zeros([2, 1*round(TOTAL_POINTS/5)])
    else:
        raise ValueError(" fpga mode error")

    # SELECT CHANNELS:
    DAQmask = 0
    for i in IQ_PAIR: DAQmask += 2**(i-1) # Mask to select which DAQ-channels (e.g. 0b0011 where LSB is CH1, bit 1 is CH2 and so on).
    start_acq = time()

    # START DATA ACQUISITION:
    module.DAQflushMultiple(DAQmask)
    module.aveMemoryClear()
    module.DAQstartMultiple(DAQmask)
    
    # 4. FPGA: WAIT FOR REAL-TIME COMPUTATION TO CONCLUDE
    

    for index, DAQ_CH in enumerate(IQ_PAIR):
        # DAQ ACQUISITION
        # check the average process completion
        
        if FPGA == module.bitMode_Keysight: 
            module.checkFinished(DAQ_CH, TOTAL_POINTS, recordsum,timeout_in_s=101)
            readPoints = module.DAQread(DAQ_CH, recordsum*TOTAL_POINTS, READ_TIMEOUT)
            DATA_V[index] = FULL_SCALE * ( readPoints / 2**(14+1)) # DECODING BINARY
        elif FPGA & module.bitMode_SingleDDC:
            if DAQ_CH == 1:
                module.checkFinished(1, TOTAL_POINTS, recordsum,timeout_in_s=101)
                module.checkFinished(2, TOTAL_POINTS, recordsum,timeout_in_s=101)
                DATA_V[1] = FULL_SCALE * (model.DAQreadFPGA(1, READ_TIMEOUT) / 2**(14+1))
                DATA_V[2] = FULL_SCALE * (model.DAQreadFPGA(2, READ_TIMEOUT) / 2**(14+1))
            elif DAQ_CH ==2:
                module.checkFinished(3, TOTAL_POINTS, recordsum,timeout_in_s=101)
                module.checkFinished(4, TOTAL_POINTS, recordsum,timeout_in_s=101)
                DATA_V[3] = FULL_SCALE * (model.DAQreadFPGA(3, READ_TIMEOUT) / 2**(14+1))
                DATA_V[4] = FULL_SCALE * (model.DAQreadFPGA(4, READ_TIMEOUT) / 2**(14+1))
        else:
            module.checkFinished(DAQ_CH, TOTAL_POINTS, recordsum,timeout_in_s=101)
            readPoints = module.DAQreadFPGA(DAQ_CH, READ_TIMEOUT)
            DATA_V[index] = FULL_SCALE * ( readPoints / 2**(14+1)) # DECODING BINARY 
        print(Fore.YELLOW + "Total points read by CH-{}: {}".format(DAQ_CH, readPoints.size))
        # convert binary data to voltage

        
        # DATA_V[index] = readPoints # RAW-DIGITS

    # STOP DAQ
    module.DAQstopMultiple(DAQmask)
    # Interleaved function is not implement !!!
    if FPGA: DATA_V = DATA_V.T.reshape(1, TOTAL_POINTS, 2) # Interleaved IQ-pairs
    else: DATA_V = DATA_V.T.reshape(recordsum, TOTAL_POINTS, 2) # Interleaved IQ-pairs
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


# Test Zone
if __name__ == "__main__":
    recordsum = 8000
    recordtime_ns = 3000
    FPGA = 1

    digModule = Initiate(1, mode="TEST")
    dt_ns = ConfigureBoard(digModule, dict(TOTAL_POINTS=round(recordtime_ns/2), NUM_CYCLES=recordsum, FPGA=FPGA))

    while True:
        LOOP = input("Press ENTER (OTHER KEY) to CONTINUE (ESCAPE): ")
        if LOOP: break
        
        DATA_V = AcquireData(digModule, recordtime_ns*1e-9, recordsum, update_settings=dict(FPGA=FPGA))[0]

        # PLOT	
        if not FPGA: 
            DATA_V = DATA_V.reshape([recordsum,round(recordtime_ns/dt_ns)*2])
            plot_record = 7 # check first few records already taken:
            for r in range(plot_record):
                trace_I, trace_Q = DATA_V[r,:].reshape((round(recordtime_ns/dt_ns), 2)).transpose()[0], DATA_V[r,:].reshape((round(recordtime_ns/dt_ns), 2)).transpose()[1]
                curve([dt_ns*array(range(len(trace_I))),dt_ns*array(range(len(trace_Q)))], [trace_I,trace_Q], 'retrieving record-%s'%(r+1), 't (ns)', 'Pulse Response (V)')
        else: 
            # FPGA-case
            DATA_V = DATA_V.reshape([round(recordtime_ns/dt_ns)*2])
            trace_I, trace_Q = DATA_V.reshape((round(recordtime_ns/dt_ns), 2)).transpose()[0], DATA_V.reshape((round(recordtime_ns/dt_ns), 2)).transpose()[1]
            curve([dt_ns*array(range(len(trace_I))),dt_ns*array(range(len(trace_Q)))], [trace_I,trace_Q], 'Data Processed by FPGA', 't (ns)', 'Pulse Response (V)')
        

    print("Exiting...")
    close(digModule, 1, mode="TEST")

#!/usr/bin/env python
'''Communicating with Benchtop RIGOL Spectrum Analyzer RSA5065-TG
'''

from colorama import init, Fore, Back
from numpy.core.fromnumeric import mean
from numpy import array, zeros, transpose
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # module's name e.g. PSG

from time import sleep

import pyvisa as visa
from pyqum.instrument.logger import address, set_status, status_code, debug
from pyqum.instrument.logger import translate_scpi as Attribute

debugger = debug(mdlname)

# INITIALIZATION
def Initiate(reset=True, which=1, mode='DATABASE'): # PENDING INCLUSION INTO THE DATABASE
    ad = address(mode)
    rs = ad.lookup(mdlname) # Instrument's Address
    rm = visa.ResourceManager()
    try:
        bench = rm.open_resource(rs) #establishing connection using GPIB# with the machine
        if reset:
            bench.write('*CLS') #Clear buffer memory
            bench.write(':SYSTem:PRESet') #Mode preset
            bench.write(":TRACe:TYPE WRITe") #clear/write trace
        bench.read_termination = '\n' #omit termination tag from output 
        bench.timeout = 150000 #set timeout in ms
        stat = bench.write(":INIT:CONT ON") #continuous mode

        bench.write(":DISPlay:ENABle OFF") #Display off

        # sleep(3)
        set_status(mdlname, dict(state='connected'))
        print(Fore.GREEN + "%s's connection Initialized: %s" % (mdlname, str(stat)))
        ad.update_machine(1, "%s_%s"%(mdlname,which))
    except: 
        set_status(mdlname, dict(state='DISCONNECTED'))
        print(Fore.RED + "%s's connection NOT FOUND" % mdlname)
        # bench = "disconnected"
    return bench

@Attribute
def model(bench, action=['Get', '']):
    SCPIcore = '*IDN'  #inquiring machine identity: "who r u?"
    return mdlname, bench, SCPIcore, action
@Attribute
def sweepSA(bench, action=['Get', '']):
    '''Specifies the number of measurement points for one sweep run.\n
        action=['Set','101']'''
    SCPIcore = ':SWEep:POINts'
    return mdlname, bench, SCPIcore, action
    
@Attribute
def averag(bench, action=['Get', '']):
    '''
    Averaging mode.
    COUNT: <integer>
    '''
    bench.write(":TRACe:TYPE AVERage") # Trace[1] Average
    bench.write(":SENSe:AVERage:STATe ON") # OFF by default
    SCPIcore = ':SENSe:AVERage:COUNT'
    return mdlname, bench, SCPIcore, action
@Attribute
def dataform(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <format: REAL,32/REAL,64/ASCii,0>]
    '''
    if action[1] == 'REAL': action[1] = 'REAL,64' # Redefine MXA's REAL (32-Bit) into 64-Bit to align with ENA's REAL (64-Bit).
    bench.write('FORMat:BORDer NORMal')
    SCPIcore = ':FORMat:TRACe:DATA'
    return mdlname, bench, SCPIcore, action
@Attribute
def linfreq(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <start(Hz)>, <stop(Hz)>]'''
    # bench.write("SENS:SWE:TYPE LINEAR") # from ENA
    SCPIcore = 'SENS:FREQuency:START;STOP'
    return mdlname, bench, SCPIcore, action
@Attribute
def cwfreq(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <zero-span-center-frequency(Hz)>]'''
    bench.write("FREQ:SPAN 0 Hz") # ZERO-SPAN
    SCPIcore = ':FREQ:CENT'
    return mdlname, bench, SCPIcore, action
@Attribute
def fcenter(bench, action=['Get', '']):
    '''This command sets the signal generator output frequency for the CW frequency mode, or increments or decrements the current RF frequency setting.\n
        action=['Set','5GHz']'''
    SCPIcore = ':FREQ:CENT'
    return mdlname, bench, SCPIcore, action
@Attribute
def fspan(bench, action=['Get', '']):
    '''This command sets the signal generator output frequency for the CW frequency mode, or increments or decrements the current RF frequency setting.\n
        action=['Set','150MHz']'''
    SCPIcore = ':FREQ:SPAN'
    return mdlname, bench, SCPIcore, action
@Attribute
def rbw(bench, action=['Get', '']):
    '''This command sets the signal generator output frequency for the CW frequency mode, or increments or decrements the current RF frequency setting.\n
        action=['Set','1MHz']'''
    SCPIcore = ':BANDwidth:RESolution'
    return mdlname, bench, SCPIcore, action
@Attribute
def vbw(bench, action=['Get', '']):
    '''This command sets the signal generator output frequency for the CW frequency mode, or increments or decrements the current RF frequency setting.\n
        action=['Set','100kHz']'''
    SCPIcore = ':BANDwidth:VIDeo'
    return mdlname, bench, SCPIcore, action
@Attribute
def trigger_source(bench, action=['Get', '']):
    '''Trigger Source:\n
        EXTernal1| EXTernal2| IMMediate| LEVel| FMT|LINE| FRAMe| RFBurst| PERiod| FMT| VIDeo| IF| TV 
        action=['Set','EXTernal1']'''
    SCPIcore = ':TRIGger:SOURCe'
    return mdlname, bench, SCPIcore, action
@Attribute
def preamp(bench, action=['Get', '']):
    '''Pre-amplifier state.\n
        action=['Set','ON']'''
    SCPIcore = ':POW:GAIN'
    return mdlname, bench, SCPIcore, action
@Attribute
def preamp_band(bench, action=['Get', '']):
    '''Pre-amplifier bandwidth.\n
        action=['Set','FULL']'''
    SCPIcore = ':POW:GAIN:BAND'
    return mdlname, bench, SCPIcore, action
@Attribute
def attenuation(bench, action=['Get', '']):
    '''Attenuation.\n
        action=['Set','0dB']'''
    SCPIcore = ':POW:ATT'
    return mdlname, bench, SCPIcore, action
@Attribute
def attenuation_auto(bench, action=['Get', '']):
    '''Auto Attenuation mode.\n
        action=['Set','ON']'''
    SCPIcore = ':POW:ATT:AUTO'
    return mdlname, bench, SCPIcore, action

def mark_power(bench, freq_GHz):
    '''using marker to extract power. (formerly known as fpower)
    '''
    # Sets the instrument to single sweep. Starts a sweep and waits for its completion:
    bench.write("INIT:CONT OFF")
    bench.write("INIT")
    bench.write("*WAI")
    # Marking frequency position:
    if int(bench.query('*OPC?')):
        bench.write(":CALC:MARKer:MODE POS")
        bench.write(":CALC:MARKer:X %sGHz" %freq_GHz)
    # Extract power reading:
    power = float(bench.query(":CALCulate:MARKer:Y?").split('dBm')[0])
    bench.write("INIT:CONT ON")
    return power

def autoscal(bench):
    preamp(bench, action=['Set','OFF'])
    preamp_band(bench, action=['Set','FULL'])
    attenuation(bench, action=['Set','0dB'])
    status = attenuation_auto(bench, action=['Set','ON'])
    return status

def measure(bench):
    trigger_source(bench, action=['Set','IMMediate']) # Free run
    # Sets the instrument to single sweep. Starts a sweep and waits for its completion:
    bench.write("INIT:CONT OFF")
    bench.write("INIT")
    bench.write("*WAI")
    # Ready?
    ready = bench.query("*OPC?") # when opc return, the sweep is done
    return ready

def sdata(bench, mode="NA"):
    '''Collect data from MXA
    This returns the data from the FIRST TRACE.
    mode: to be analogy with the NA in order to be called in "characterize".
    '''
    bench.query('*OPC?')
    try:
        sdatacore = ":TRACe:DATA? TRACE1"
        datatype = dataform(bench)
        #Temp setting (Jacky)
        # databorder = str(bench.query("FORMat:BORDer?"))
        # print(Fore.CYAN + "Endian (Byte-order): %s" %databorder)
        if datatype[1]['DATA'] == 'REAL,32':
            datas = bench.query_binary_values(sdatacore, datatype='f', is_big_endian=True) # convert the transferred ieee-encoded binaries into list (faster, 32-bit)
        elif datatype[1]['DATA'] == 'REAL,64':
            datas = bench.query_binary_values(sdatacore, datatype='d', is_big_endian=True) # convert the transferred ieee-encoded binaries into list (faster, 64-bit)
        elif 'ASC' in datatype[1]['DATA']:
            datas = bench.query_ascii_values(sdatacore) # convert the transferred ascii-encoded binaries into list (slower)
        if mode=="NA":
            # NOTE: interleaving the data with Q=0 or I=0 depending on which gives a zero phase:
            
            fakeI = array(datas)
            fakeQ = zeros(fakeI.shape[0])
            datas = transpose( array([fakeI,fakeQ]) )
            datas = list(datas.flat)
            #print( type(datas), datas )
    except Exception as err:
        datas = [0]
        print(err)
    return datas

def fpower(bench, frequency_GHz, ave_points=100, resBW_kHz=3, ave_counts=10):
    bench.write("FREQ:SPAN 0 Hz") # ZERO-SPAN
    bench.write(":SENSe:SWEep:POINts %s" %(ave_points))
    bench.write(":BANDwidth:RESolution %skHz" %(resBW_kHz))
    fcenter(bench, action=['Set','%sGHz'%frequency_GHz])
    averag(bench, action=['Set',ave_counts])
    bench.write(":SENSe:SPURious:POWer:RF:RANGe:AUTO ON") # auto-scale?
    # Sets the instrument to single sweep. Starts a sweep and waits for its completion:
    bench.write("INIT:CONT OFF")
    bench.write("INIT")
    bench.write("*WAI")
    # Retrieving Data:
    if int(bench.query('*OPC?')):
        sweep_time_s = float(bench.query(":SENSe:SWEep:TIME?"))
        print(Fore.CYAN + "Sweeping time: %ss" %sweep_time_s)
        dataform(bench, action=['Set', 'REAL'])
        powerlist = sdata(bench, mode="") # data in list
    else: powerlist = [0]*int(ave_points)
    # Average all the collected points:
    power = mean(powerlist)
    bench.write("INIT:CONT ON")
    return power, powerlist

def close(bench, reset=True, which=1, mode='DATABASE'):

    bench.write(":DISPlay:ENABle ON") #Display on

    if reset:
        bench.write('*RST') # reset to factory setting (including switch-off)
        set_status(mdlname, dict(config='reset'))
    else: set_status(mdlname, dict(config='previous'))
    try:
        bench.close() #None means Success?
        status = "Success"
        ad = address(mode)
        ad.update_machine(0, "%s_%s"%(mdlname,which))
    except: status = "Error"
    set_status(mdlname, dict(state='disconnected'))
    print(Back.WHITE + Fore.BLACK + "%s's connection Closed" %(mdlname))
    return status

# Dummies:
def power(bench, action): pass
     
def setrace(nabench, Mparam=""): pass

def sweep(nabench, action=['Get','','']): #Default from NA
    if len(action)==3: action = [ action[0], action[2] ] # omit "TIME:AUTO ON"
    if len(action)==2: pass
    sweepSA(nabench, action)

def ifbw(nabench, action=['Get', '']):
    rbw(nabench, action=action)
    vbw(nabench, action=action)

# Test Zone
def test(detail=True):
    from pyqum.instrument.analyzer import curve
    from pyqum.instrument.toolbox import waveform

    S={}
    S['x'] = Initiate(mode="TEST")
    s = S['x']
    if s == "disconnected":
        pass
    else:
        if debug(mdlname, detail):
            print(Fore.RED + "Detailed Test:")
            # print('SCPI TEST:')
            # s.write("*SAV 00,1")
            
            model(s)
            if int(input("Press 1 (others) to proceed (skip) PHASE-1 (Basic sweep with certain span): "))==1:
                npoints = 371
                sweepSA(s)
                sweepSA(s, action=['Set','%s'%npoints])
                freq = 7
                fcenter(s)
                fcenter(s, action=['Set','%sGHz'%freq])
                span = 60
                fspan(s)
                fspan(s, action=['Set','%sMHz'%span])
                rbw(s, action=['Set','1MHz'])
                vbw(s, action=['Set','100kHz'])
                trigger_source(s, action=['Set','IMMediate'])

                preamp(s, action=['Set','OFF'])
                preamp_band(s, action=['Set','FULL'])
                attenuation(s, action=['Set','0dB'])
                attenuation_auto(s, action=['Set','ON'])

                x = waveform('%s to %s * %s' %(freq-span/1000, freq+span/1000, npoints-1)).data
                marking_power = mark_power(s,freq)
                dataform(s, action=['Set', 'REAL'])
                y = sdata(s, mode="")
                print("data points extracted: %s" %len(y))
                curve(x, y, 'Power at %sGHz: %s' %(freq,marking_power), 'frequency (GHz)', 'power (dBm)')

            elif int(input("Press 1 (others) to proceed (skip) PHASE-2 (Linear frequency for adapting NA architecture): "))==1:
                # dataform, sweep, ...(rbw,linfreq), measure, autoscal, sdata
                dataform(s, action=['Set', 'REAL'])
                npoints = 371
                sweepSA(s, action=['Set','%s'%npoints])
                fstart, fstop = 5, 9
                linfreq(s, action=['Set', '%sGHz'%fstart, '%sGHz'%fstop]) # F-sweep
                rbw(s, action=['Set','1MHz'])
                vbw(s, action=['Set','100kHz'])
                
                measure(s)
                autoscal(s)
                x = waveform('%s to %s * %s' %(fstart, fstop, npoints-1)).data
                y = sdata(s, mode="")
                curve(x, y, 'power spectrum-2', 'frequency (GHz)', 'power (dBm)')

            elif int(input("Press 1 (others) to proceed (skip) PHASE-3 (Zero-span power for IQ-Calibration): "))==1:
                preamp(s, action=['Set','OFF'])
                preamp_band(s, action=['Set','FULL'])
                attenuation(s, action=['Set','0dB'])
                attenuation_auto(s, action=['Set','ON'])
                ave_points, freq_GHz =100, 7
                x = waveform('%s to %s * %s' %(1, ave_points, ave_points-1)).data
                zer0span_power, y = fpower(s, frequency_GHz=freq_GHz, resBW_kHz=1, ave_points=ave_points)
                title = "The zer0-span-power at %sGHz is %sdBm" %(freq_GHz, zer0span_power)
                print("power-list: %s" %y)
                curve(x, y, title, 'frequency (GHz)', 'power (dBm)')

            elif int(input("Press 1 (others) to proceed (skip) PHASE-4 (Power Density): "))==1:
                dataform(s, action=['Set', 'ASC'])
                print("Total power in a Channel: %s" %s.query(":MEASure:CHPower:CHPower?"))
            
            
        else: print(Fore.RED + "Basic IO Test")
    if not bool(input("Press ENTER (OTHER KEY) to (skip) reset: ")):
        state = True
    else: state = False
    close(s, reset=state, mode="TEST")
    return

#test()
'''Communicating with Benchtop E-series Vector Network Analyzer'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # instrument-module's name e.g. ENA, PSG, YOKO

import matplotlib.pyplot as plt
from numpy import arange, floor, ceil, array

import pyvisa as visa
from pyqum.instrument.logger import address, set_status, status_code, debug
from pyqum.instrument.logger import translate_scpi as Attribute

debugger = debug(mdlname)

# INITIALIZATION
def Initiate(reset=False, which=1, MaxChannel=2):
	ad = address()
	rs = ad.lookup(mdlname, which) # Instrument's Address
	rm = visa.ResourceManager()
	try:
		bench = rm.open_resource(rs) #establishing connection using GPIB# with the machine
		if reset:
			stat = bench.write('*RST;*CLS') #Clear buffer memory;
		else:
			bench.write(':ABORt;:INIT:CONT OFF;') #hold the trigger
			stat = bench.write('*CLS') #Clear buffer memory;
			bench.write('OUTPut:STATE ON') #open the port (E5071C only has one Source)
		# Allocating Channels:
		if MaxChannel == 1:
			bench.write(':DISPlay:SPLit D1')
		elif MaxChannel == 2:
			bench.write(':DISPlay:SPLit D1_2')
		bench.write("SENS:CORR:EXT:AUTO:RESet") #clear port-extension auto-correction
		bench.read_termination = '\n' #omit termination tag from output 
		bench.timeout = 80000000 #set timeout in ms
		set_status(mdlname, dict(state='connected'))
		print(Fore.GREEN + "%s's connection Initialized: %s" % (mdlname, str(stat)))
		ad.update_machine(1, "%s_%s"%(mdlname,which))
	except: 
		# raise
		set_status(mdlname, dict(state='DISCONNECTED'))
		print(Fore.RED + "%s's connection NOT FOUND" % mdlname)
		# bench = "disconnected"
	return bench

@Attribute
def model(bench, action=['Get'] + 10 * ['']):
	SCPIcore = '*IDN'  #inquiring machine identity: "who r u?"
	return mdlname, bench, SCPIcore, action
@Attribute
def rfports(bench, action=['Get'] + 10 * ['']):
	SCPIcore = 'OUTPut:STATE'  #switch-on/off RF-ports
	return mdlname, bench, SCPIcore, action
@Attribute
def sweep(bench, action=['Get'] + 10 * ['']):
	'''CONDITIONAL SWEEP:\n
	action=['Get/Set', <auto: ON/OFF 100>, <points>]
	1. Sets the time the analyzer takes to complete one sweep.
	2. Sets the number of data points for the measurement.
	'''
	print(Fore.GREEN + "action: %s" %action)
	if action[1] in ['ON', 'TRUE', 'True']:
		bench.write('SENSe:SWEep:TIME:AUTO ON')
		action.remove(action[1])
		SCPIcore = 'SENSe:SWEep:POINTS'
	elif action[1].split(' ')[0] in ['OFF', 'FALSE', 'False', '']: # Get is here
		try:
			action[1] = action[1].split(' ')[1]
			bench.write('SENSe:SWEep:TIME:AUTO OFF')
		except IndexError: pass
		SCPIcore = 'SENSe:SWEep:TIME;POINTS'
	else: print(Fore.RED + "Parameter NOT VALID!")
	return mdlname, bench, SCPIcore, action
@Attribute
def linfreq(bench, action=['Get'] + 10 * ['']):
	'''action=['Get/Set', <start(Hz)>, <stop(Hz)>]'''
	bench.write("SENS:SWE:TYPE LINEAR") #by default: Freq Sweep
	SCPIcore = 'SENS:FREQuency:START;STOP'
	return mdlname, bench, SCPIcore, action
@Attribute
def ifbw(bench, action=['Get'] + 10 * ['']):
	'''action=['Get/Set', <IFB(Hz)>]'''
	SCPIcore = 'SENSe:BANDWIDTH'
	return mdlname, bench, SCPIcore, action
@Attribute
def power(bench, action=['Get']):
	'''
	action=['Get/Set', <Level(dBm)>, <Start(dBm)>, <Stop(dBm)>]
	dynamic range is limited to 35dB
	'''
	SCPIcore = 'SOURce:POWER:LEVEL;START;STOP'
	action += 10 * ['']
	return mdlname, bench, SCPIcore, action
@Attribute
def cwfreq(bench, action=['Get'] + 10 * ['']):
	'''action=['Get/Set', <Fixed(Hz)>]
	Sets the Continuous Wave (or Fixed) frequency. 
	Must also send SENS:SWEEP:TYPE CW to put the analyzer into CW sweep mode.
	'''
	bench.write("SENS:SWE:TYPE POWER") #Power Sweep
	SCPIcore = 'SENSe:FREQuency:CW'
	return mdlname, bench, SCPIcore, action
@Attribute
def averag(bench, action=['Get'] + 10 * ['']):
	'''action=['Get/Set', <points>]
	Sets the number of measurements to combine for an average.
	'''
	bench.write("SENSe:AVER ON") # OFF by default
	bench.write("SENSe:AVER:CLE")
	SCPIcore = 'SENSe:AVER:COUNT'
	return mdlname, bench, SCPIcore, action
@Attribute
def dataform(bench, action=['Get'] + 10 * ['']):
	'''action=['Get/Set', <format: REAL/REAL32/ASCii>]
	Sets the data format for data transfers.
	Usually only the last two are preferred.
	'''
	SCPIcore = 'FORMat:DATA'
	return mdlname, bench, SCPIcore, action

@Attribute
def selectrace(bench, action=['Set'] + ['par 1']):
	'''
	This command sets/gets the selected trace (Tr) of selected channel (Ch) to the active trace.
	You can set only a trace displayed to the active trace. 
	If this object is used to set a trace not displayed to the active trace, an error occurs when executed and the object is ignored. (No read)
	'''
	SCPIcore = 'CALCulate:PARameter:SELECT'
	action += 10 * ['']
	return mdlname, bench, SCPIcore, action

# Setting Trace
def setrace(bench, channel=1, Mparam=['S11','S21','S12','S22'], window='D1'):
	'''window = {D<Tr#...>: {#repeat: linewidth, _:next-line}}
	'''
	bench.write("CALC:PAR:COUN %d" %len(Mparam))
	Mreturn = []
	for iTrace, S in enumerate(Mparam):
		bench.write("CALC:PAR%d:DEF %s" %(iTrace + 1, S)) #setting trace name
		Mreturn.append(bench.query("CALC:PAR%d:DEF?" %(iTrace + 1)))
		bench.write(":DISP:WIND:TRAC%d:Y:AUTO"%(iTrace + 1)) #pre-auto-scale
	bench.write("DISPlay:WINDow%s:ACT" %channel)
	bench.write("DISPlay:WINDow:SPLit %s" %window)
	return Mreturn #same as <Mparam>

# Getting Trace
def getrace(bench):
	'''getting traces on the screen
	'''
	tracenum = int(bench.query("CALC:PAR:COUN?"))
	Mreturn = []
	for i in range(tracenum):
		Mreturn.append(bench.query("CALC:PAR%d:DEF?" %(i+1)))
		bench.write(":DISP:WIND:TRAC%d:Y:AUTO"%(i+1)) #pre-auto-scale
	return Mreturn

def autoscal(bench):
	tracenum = int(bench.query("CALC:PAR:COUN?"))
	for i in range(tracenum):
		lastatus = bench.write(":DISP:WIND:TRAC%d:Y:AUTO"%(i+1))
	return lastatus

def measure(bench):
	bench.write(':ABOR;:INIT:CONT ON;:TRIG:SOUR BUS;:TRIG:SING;')
	# when opc return, the sweep is done
	# ready = bench.query("*OPC?") # method from labber was inefficient at best, misleading us on purpose perhaps!
	# using SRE
	bench.write(':STAT:OPER:PTR 0')
	bench.write(':STAT:OPER:NTR 16')
	bench.write(':STAT:OPER:ENAB 16')
	bench.write('*SRE 128')
	bench.write('*CLS')
	while True:
		ready = int(bench.query('*STB?'))
		if ready: break
	return ready

def scanning(bench, scan=1):
	if scan:
		stat = bench.write(':ABOR;:INIT:CONT ON;:TRIG:SOUR INT;')
	else:
		stat = bench.write(':ABOR;:INIT:CONT OFF;')
	return stat

def sdata(bench):
	'''Collect data from ENA
	This command sets/gets the corrected data array, for the active trace of selected channel (Ch).
	'''
	sdatacore = ":CALC:SEL:DATA:SDAT?"
	stat = dataform(bench)
	if stat[1]['DATA'] == 'REAL32': #PENDING: testing REAL (64bit)
		#convert the transferred ieee-encoded binaries into list (faster)
		datas = bench.query_binary_values(sdatacore, datatype='f', is_big_endian=True)
	elif stat[1]['DATA'] == 'REAL': #PENDING: testing REAL (64bit)
		#convert the transferred ieee-encoded binaries into list (faster)
		datas = bench.query_binary_values(sdatacore, datatype='d', is_big_endian=True)
	elif stat[1]['DATA'] == 'ASCii':
		#convert the transferred ascii-encoded binaries into list (slower)
		datas = bench.query_ascii_values(sdatacore)
	# print(Back.GREEN + Fore.WHITE + "transferred from %s: ALL-SData: %s" %(mdlname, len(datas)))
	return datas

def preset(bench):
	stat = bench.write(':SYSTem:PRESet')
	return stat

def close(bench, reset=True, which=1):
	if reset:
		bench.write(':OUTPut:STATe OFF')
		set_status(mdlname, dict(config='reset-off'))
	else: set_status(mdlname, dict(config='previous'))
	try:
		bench.close() #None means Success?
		status = "Success"
		ad = address()
		ad.update_machine(0, "%s_%s"%(mdlname,which))
	except: status = "Error"
	set_status(mdlname, dict(state='disconnected'))
	print(Back.WHITE + Fore.BLACK + "%s's connection Closed" %(mdlname))
	return status

# Test Zone
def test(detail=True):
	from pyqum.instrument.analyzer import curve, IQAParray, UnwraPhase
	from pyqum.instrument.toolbox import waveform

	bench = Initiate(False)
	if bench == "disconnected":
		pass
	else:
		model(bench)
		if debug(mdlname, detail):
			# print(setrace(bench, window='D12_34'))
			print(setrace(bench, Mparam=['S21','S43'], window='D1_2'))
			power(bench, action=['Set', -35])
			power(bench)
			N = 3000
			# sweep(bench, action=['Set', 'OFF 10', N])
			sweep(bench, action=['Set', 'ON', N])
			f_start, f_stop = 0.7e9, 18e9
			linfreq(bench, action=['Set', f_start, f_stop]) #F-sweep
			stat = linfreq(bench)
			fstart, fstop = stat[1]['START'], stat[1]['STOP']

			# Building X-axis
			# fstart, fstop = float(fstart), float(fstop)
			
			# noisefilfac = 20000
			IFB = 600 #abs(float(fstart) - float(fstop))/N/noisefilfac
			ifbw(bench, action=['Set', IFB])
			ifbw(bench)
			# averag(bench, action=['Set', 1]) #optional
			# averag(bench)

			# start sweeping
			# stat = sweep(bench)
			# print("Time-taken would be: %s (%spts)" %(stat[1]['TIME'], stat[1]['POINTS']))
			# print("Ready: %s" %measure(bench)[1])
			# autoscal(bench)

			cwfreq(bench, action=['Set', 5.25e9])
			cwfreq(bench)
			# power(bench, action=['Set', '', -75.3, -40.3]) #power sweep
			power(bench, action=['Set', '', -10, -10])
			power(bench)

			# start sweeping
			stat = sweep(bench)
			print("Time-taken would be: %s (%spts)" %(stat[1]['TIME'], stat[1]['POINTS']))
			print("Ready: %s" %bool(measure(bench)))
			autoscal(bench)

			dataform(bench, action=['Set', 'REAL'])
			selectrace(bench, action=['Set', 'para 1 calc 1'])
			data = sdata(bench)
			print("Data [Type: %s, Length: %s]" %(type(data), len(data)))

			rfports(bench, action=['Set', 'OFF'])
			rfports(bench)

			# Plotting trace:
			yI, yQ, Amp, Pha = IQAParray(array(data))
			curve(range(len(data)//2), Amp, 'CW-Amp time-series', 'arb time', 'Amp(dB)')

			# TEST SCPI ZONE:
			# bench.write(':SYSTem:PRESet')
			# scanning(bench) #continuous scan
		else: print(Fore.RED + "Basic IO Test")
	close(bench)
	return


# test()

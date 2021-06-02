'''Communicating with Benchtop ENA E5080B, modified from E5071C version
NOTE: 
1. Simultaneous measurement is not possible, since Trigger is under Channel hierarchically. Period.
2. Byte-order is the opposite of that of E5071C.
'''

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
def Initiate(reset=False, which=1, MaxChannel=2, mode='DATABASE'):
	ad = address(mode)
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
		# bench.write(':DISPlay:SPLit %s' %MaxChannel)
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
	'''action=['Get/Set', <format: REAL,32/REAL,64/ASCii,0>]
	'''
	SCPIcore = 'FORMat:DATA'
	return mdlname, bench, SCPIcore, action
@Attribute
def selectrace(bench, action=['Set'] + ['CH1_S21_1']):
	'''
	This command sets/gets the selected trace (Tr) of selected channel (Ch) to the active trace.
	You can set only a trace displayed to the active trace. 
	If this object is used to set a trace not displayed to the active trace, an error occurs when executed and the object is ignored. (No read)
	'''
	SCPIcore = 'CALCulate:PARameter:SELECT'
	action += 10 * ['']
	return mdlname, bench, SCPIcore, action
@Attribute
def tracenum(bench, action=['Get'] + 10 * ['']):
	'''Sets or gets the number of traces of selected channel.
	'''
	SCPIcore = 'CALC:PAR:COUN'
	return mdlname, bench, SCPIcore, action

# Setting Trace
def setrace(bench, Mparam=['S11','S21','S12','S22']):
	bench.write(":CALCulate:MEASure:DELete:ALL") # Clear ALL measurement(s)
	for iTrace, S in enumerate(Mparam):
		bench.write(':CALCulate:MEASure%s:DEFine "%s"' %(iTrace+1, S)) # create measurement per trace
		bench.write(':DISPlay:WINDow:TRACe%s:FEED "CH1_%s_%s"' %(iTrace+1, S, iTrace+1)) # feed trace per measurement
		selectrace(bench, action=['Set', 'CH1_%s_%s'%(S, iTrace+1)]) # select the last trace by default for data retrieval
	return bench.query(":CALCulate:PARameter:CATalog:EXTended?") # can be separated by comma(s)

# Getting Trace
def getrace(bench):
	'''getting traces displayed on the screen
	'''
	catalog = bench.query("CALCulate:PARameter:CATalog:EXTended?").replace('"','')
	Mreturn = catalog.split(',')[1::2]
	return Mreturn

def autoscal(bench):
	tracenum = int(bench.query("CALC:PAR:COUN?"))
	for i in range(tracenum):
		lastatus = bench.write(":DISP:WIND:TRAC%d:Y:AUTO"%(i+1))
	return lastatus

def measure(bench):
	bench.write(':ABOR;:INIT:IMM;:TRIG:SOUR MAN;') # manually triggered with bus
	ready = bench.query("*OPC?") # when opc return, the sweep is done
	return ready

def scanning(bench, scan=1):
	if scan:
		stat = bench.write(':ABOR;:INIT:CONT ON;:TRIG:SOUR IMMediate;')
	else:
		stat = bench.write(':ABOR;:INIT:CONT OFF;')
	return stat

def sdata(bench):
	'''Collect data from ENA
	This command sets/gets the corrected data array, for the active trace of selected channel (Ch).
	'''
	sdatacore = ":CALCulate:MEASure:DATA:SDATa?"
	datatype = dataform(bench)
	if datatype[1]['DATA'] == 'REAL,32':
		datas = bench.query_binary_values(sdatacore, datatype='f', is_big_endian=True) # convert the transferred ieee-encoded binaries into list (faster, 32-bit)
	elif datatype[1]['DATA'] == 'REAL,64':
		datas = bench.query_binary_values(sdatacore, datatype='d', is_big_endian=True) # convert the transferred ieee-encoded binaries into list (faster, 64-bit)
	elif datatype[1]['DATA'] == 'ASC,0':
		datas = bench.query_ascii_values(sdatacore) # convert the transferred ascii-encoded binaries into list (slower)
	# print(Back.GREEN + Fore.WHITE + "transferred from %s: ALL-SData: %s" %(mdlname, len(datas)))
	return datas

def preset(bench):
	stat = bench.write(':SYSTem:PRESet')
	return stat

def close(bench, reset=True, which=1, mode='DATABASE'):
	if reset:
		bench.write(':OUTPut:STATe OFF')
		set_status(mdlname, dict(config='reset-off'))
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

# Test Zone
def test(detail=True):
	from pyqum.instrument.analyzer import curve, IQAParray, UnwraPhase
	from pyqum.instrument.toolbox import waveform

	bench = Initiate(False, mode="TEST")
	if bench == "disconnected": pass
	else:
		if debug(mdlname, detail):
			model(bench)
			print(setrace(bench, ['S21']))
			sweep(bench, action=['Set', 'ON', 1001])
			ifbw(bench, action=['Set', 100])
			ifbw(bench)

			for i in range(2):
				if i:
					input("Press any key to sweep frequency: ")
					f_start, f_stop = 3e9, 9e9
					linfreq(bench, action=['Set', f_start, f_stop]) #F-sweep
					stat = linfreq(bench)
					fstart, fstop = stat[1]['START'], stat[1]['STOP']
					# Building X-axis
					# fstart, fstop = float(fstart), float(fstop)
					power(bench, action=['Set', -31.7])
					power(bench)
					
				else:
					input('Press any key to sweep power: ')
					cwfreq(bench, action=['Set', 5.257e9])
					cwfreq(bench)
					power(bench, action=['Set', '', -73, -35]) #power sweep
					power(bench)

				# start sweeping
				stat = sweep(bench)
				print("Time-taken would be: %s (%spts)" %(stat[1]['TIME'], stat[1]['POINTS']))
				print("Ready: %s" %bool(measure(bench)))
				autoscal(bench)

				dataform(bench, action=['Set', 'REAL'])
				data = sdata(bench)
				print("Data [Type: %s, Length: %s]" %(type(data), len(data)))

				# Plotting trace:
				yI, yQ, Amp, Pha = IQAParray(array(data))
				curve([range(len(data)//2),range(len(data)//2)], [yI,yQ], 'In-Plane', 'Count', 'I(dB)', style=['-b','r'])
				curve(range(len(data)//2), Amp, 'Amplitude', 'Count', 'Amp(dB)')
				curve(range(len(data)//2), UnwraPhase(range(len(data)//2), Pha), 'UPhase', 'Count', 'UPha(dB)')

			# TEST SCPI ZONE:
			print("There is/are %s trace(s)" %str(tracenum(bench)))
			print("%s trace(s): %s"%(len(getrace(bench)), getrace(bench)))
			# averag(bench, action=['Set', 1]) #optional
			# averag(bench)
			# rfports(bench, action=['Set', 'OFF'])
			# rfports(bench)
			# bench.write(':SYSTem:PRESet')
			print("Endian (Byte-order): %s" %str(bench.query("FORMat:BORDer?")))
			# scanning(bench) #continuous scan

		else: print(Fore.RED + "Basic IO Test")
	
	input("Press any key to close: ")
	close(bench, mode="TEST")
	return


# test()

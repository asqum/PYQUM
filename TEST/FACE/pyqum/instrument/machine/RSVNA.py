"""
-----------------------------------------------------------------------------
2022/06/08, lai
Modified code to R&S VNA, ZNB Model, from the version of ENA E5080B
-----------------------------------------------------------------------------

NOTE: 
1. Simultaneous measurement is not possible, since Trigger is under Channel hierarchically. Period.
2. Byte-order is the opposite of that of E5071C.
"""

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
		if reset: stat = bench.write('*RST;*CLS') #Clear buffer memory;
		else: stat = bench.write('*CLS') # Clear buffer memory;
		bench.write(':ABORt;:INIT:CONT OFF;') # hold the trigger
		bench.write('OUTPut:STATE ON') # Power ON
		bench.write('SOURce:POWER:LEVEL -73') # PENDING: ZNB need to set generator (power) level first!!! 
		# bench.write("SENS:CORR:EXT:AUTO:RESet") #clear port-extension auto-correction

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

def sweepmode():
	'''NOTE: Not applicable for ZNB!
	'''
	return None

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
	'''action=['Get/Set', <format: REAL,32/ASCII,0>]
		<return: REAL,32/ASC,0>
	'''
	if action[1] == 'REAL': action[1] = 'REAL,32' # lai, for R&S VNA-ZNB, ZNB only has 'Real,32' format

	# bench.write('FORMat:BORDer NORMal')
	SCPIcore = 'FORMat:DATA'
	return mdlname, bench, SCPIcore, action

def selectrace(): return "Not compatible with ZNB"

@Attribute
def tracenum(bench, action=['Get'] + 10 * ['']):
	'''Sets or gets the number of traces of selected channel.
	'''
	SCPIcore = 'CALC:PAR:COUN'
	return mdlname, bench, SCPIcore, action

# Clear ALL measurement(s)
def clearallmeas(bench): return bench.write("CALCulate:PARameter:DELete:ALL") # bench.write(":CALCulate:MEASure:DELete:ALL")

# Setting Trace
def setrace(bench, Mparam=['S11','S21','S12','S22']):
	clearallmeas(bench)
	for iTrace, S in enumerate(Mparam):		
		bench.write("CALCulate1:PARameter:SDEFine 'Trc%s','%s'" %(iTrace+1,S)) # lai, for R&S VNA-ZNB, set s-parameter from trace1; hasn't shown to screen
		bench.write("DISPlay:WINDow1:TRACe%s:FEED 'Trc%s'" %(iTrace+1,iTrace+1)) # Feed trace for the measurement
		bench.write("DISPlay:TRACe:Y:SCALe:AUTO ONCE,'Trc%s'" %(iTrace+1)) # lai, for R&S VNA-ZNB, y-axis auto scale
	
	return Mparam

# Getting Trace
def getrace(bench):
	'''getting traces displayed on the screen
	'''	
	catalog = bench.query("CONFigure:TRACe:CATalog?") # lai, for R&S VNA-ZNB
	Mreturn = catalog.split(',')[1::2]
	return Mreturn

def autoscal(bench):
	tracenum = int( bench.query("CONFigure:TRACe:CATalog?").count(',') ) # lai, for R&S VNA-ZNB, count the numbers of ',' symbols to have trace count
	tracenum = int( (tracenum+1)/2 ) # lai, for R&S VNA-ZNB, two ',' for one trace
	
	for i in range(tracenum):			
		bench.write("DISPlay:TRACe:Y:SCALe:AUTO ONCE,'Trc%s'" %(i+1)) # lai, for R&S VNA-ZNB, y-axis auto scale		
		lastatus = 1
	return lastatus

def measure(bench):
	bench.write(":TRIG:SOUR IMM;")
	bench.write(":ABOR;INITiate1:IMMediate") # lai, for R&S VNA-ZNB
	ready = bench.query("*OPC?") # when opc return, the sweep is done
	return ready

def scanning(bench, scan=1):
	if scan:
		bench.write(":TRIG:SOUR IMM;")
		stat = bench.write(':ABOR;:INIT:CONT ON;') # likened to pressing "Continuous" on the panel
	else:
		bench.write(":TRIG:SOUR MAN;")
		stat = bench.write(':ABOR;:INIT:CONT OFF;') # likened to pressing "Hold" on the panel
	return stat

def sdata(bench):
	'''Collect data from ENAB
	This returns the data from the FIRST TRACE.
	'''
	try:		
		sdatacore = "CALCulate1:DATA? SDATa"		
		datatype = dataform(bench)
		# databorder = str(bench.query("FORMat:BORDer?"))
		# print(Fore.CYAN + "Endian (Byte-order): %s" %databorder) # DEFAULT: SWAP
		if datatype[1]['DATA'] == 'REAL,32':
			datas = bench.query_binary_values(sdatacore, datatype='f', is_big_endian=False) # convert the transferred ieee-encoded binaries into list (faster, 32-bit)		
		elif datatype[1]['DATA'] == 'ASC':
			datas = bench.query_ascii_values(sdatacore) # convert the transferred ascii-encoded binaries into list (slower)
		
	except Exception as err:
		datas = [0]
		print(err)
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
	except: 
		# raise
		status = "Error"
	set_status(mdlname, dict(state='disconnected'))
	print(Back.WHITE + Fore.BLACK + "%s's connection Closed" %(mdlname))
	return status

# Test Zone
def test(detail=True):
	from pyqum.instrument.analyzer import curve, IQAParray, UnwraPhase
	from pyqum.instrument.toolbox import waveform

	bench = Initiate(True, mode="TEST")
	if bench == "disconnected": pass
	else:
		if debug(mdlname, detail):
			model(bench)
			print(setrace(bench, ['s43','s11','S31','s21']))
			dataform(bench, action=['Set', 'REAL'])
			sweep(bench, action=['Set', 'ON', 1001])
			ifbw(bench, action=['Set', 1000])
			ifbw(bench)

			for i in range(2):
				if not i:
					input("Press any key to sweep frequency: ")
					f_start, f_stop = 5e9, 7e9
					linfreq(bench, action=['Set', f_start, f_stop]) #F-sweep
					# stat = linfreq(bench)
					# fstart, fstop = stat[1]['START'], stat[1]['STOP']
					# Building X-axis
					# fstart, fstop = float(fstart), float(fstop)
					power(bench, action=['Set', -31.7])
					
				else:
					input('Press any key to sweep power: ')
					cwfreq(bench, action=['Set', 5.257e9])
					# cwfreq(bench)
					power(bench, action=['Set', '', -73, -35]) #power sweep
					# power(bench)

				# start sweeping
				stat = sweep(bench)
				print("Time-taken would be: %s (%spts)" %(stat[1]['TIME'], stat[1]['POINTS']))
				print("Ready: %s" %bool(measure(bench)))
				autoscal(bench)

				data = sdata(bench)
				print("Data [Type: %s, Length: %s]" %(type(data), len(data)))

				# Plotting trace:
				yI, yQ, Amp, Pha = IQAParray(array(data))
				curve([range(len(data)//2),range(len(data)//2)], [yI,yQ], 'In-Plane', 'Count', 'I(dB)', style=['-b','r'])
				curve(range(len(data)//2), Amp, 'Amplitude', 'Count', 'Amp(dB)')
				curve(range(len(data)//2), UnwraPhase(range(len(data)//2), Pha), 'UPhase', 'Count', 'UPha(dB)')

			# TEST SCPI ZONE:
			# bench.write(':SYSTem:PRESet')
			"""
			# // delete all trace
			bench.write('CALCulate:PARameter:DELete:ALL')

			# // set 4 traces as S11, S22, S33, S44 separately
			bench.write("CALCulate1:PARameter:SDEFine 'Trc1','S11'")
			bench.write("DISPlay:TRACe:Y:SCALe:AUTO ONCE,'Trc1'")
			bench.write("CALCulate1:PARameter:SDEFine 'Trc2','S22'")
			bench.write("DISPlay:TRACe:Y:SCALe:AUTO ONCE,'Trc2'")
			bench.write("CALCulate1:PARameter:SDEFine 'Trc3','S33'")
			bench.write("DISPlay:TRACe:Y:SCALe:AUTO ONCE,'Trc3'")
			bench.write("CALCulate1:PARameter:SDEFine 'Trc4','S44'")
			bench.write("DISPlay:TRACe:Y:SCALe:AUTO ONCE,'Trc4'")
		

			# // show the 4 traces
			bench.write("DISPlay:WINDow1:TRACe1:FEED 'Trc1'")
			bench.write("DISPlay:WINDow1:TRACe2:FEED 'Trc2'")
			bench.write("DISPlay:WINDow1:TRACe3:FEED 'Trc3'")
			bench.write("DISPlay:WINDow1:TRACe4:FEED 'Trc4'")

			# // list the avalible trace(s)
			#bench.write("CONFigure:TRACe:CATalog?")
			# -> 1,Trc1,2,Trc2,3,Trc3,4,Trc4

			#// data format of the trace data (Ascii or Real,32)
			bench.write("FORMat:DATA REAL,32")
			#bench.write("FORMat:DATA?")
			#-> REAL,32
			# bench.write("FORMat:DATA ASCII,0")
			bench.write("FORMat:DATA REAL")			
			status = bench.query_ascii_values("FORMat:DATA?")
			print("Foramt = %s" %status)
			#-> ASC,0

			#// to init a measurement
			bench.write(":ABOR;INITiate1:IMMediate")			
			status = bench.query_ascii_values("*OPC?")
			print("status = %s" %status)
			#-> 1

			#// read the data out
			# bench.write("CALCulate1:DATA? FDATa")
			#TestDatas = bench.query_ascii_values("CALCulate1:DATA? SDATa")
			#print("length: %s\n %s" %(len(TestDatas), TestDatas))
			#curve(range(len(TestDatas)//1), TestDatas, '', '', '')


			# TestDatas = bench.query_binary_values("CALCulate1:DATA? SDATa", datatype='f', is_big_endian=True) # convert the transferred ieee-encoded binaries into list (faster, 32-bit)
			TestDatas = bench.query_binary_values("CALCulate1:DATA? SDATa", datatype='f', is_big_endian=False) # convert the transferred ieee-encoded binaries into list (faster, 32-bit)
			# print("length: %s\n %f" %(len(TestDatas), TestDatas))
			yI, yQ, Amp, Pha = IQAParray(array(TestDatas))
			curve([range(len(TestDatas)//2),range(len(TestDatas)//2)], [yI,yQ], 'In-Plane', 'Count', 'I(dB)', style=['-b','r'])
			curve(range(len(TestDatas)//2), Amp, 'Amplitude', 'Count', 'Amp(dB)')
			curve(range(len(TestDatas)//2), UnwraPhase(range(len(TestDatas)//2), Pha), 'UPhase', 'Count', 'UPha(dB)')

			#input("Press any key...")			

			#bench.write("FORMat:DATA ASCII")
			#TestDatasAscii = bench.query_ascii_values("CALCulate1:DATA? SDATa")
			#curve(range(len(TestDatas)//1), TestDatas, '', '', '')
		"""
			

		else: print(Fore.RED + "Basic IO Test")
	
	input("Press any key to close: ")
	
	close(bench, mode="TEST")
	
	return

if __name__ == "__main__":
	test()

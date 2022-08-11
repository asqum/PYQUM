"""
-----------------------------------------------------------------------------
2022/06/08, lai
Modified code to R&S VNA, ZNB Model, from the version of ENA E5080B

< Example SCPI comands of R&S ZNB >
// delete all trace
CALCulate:PARameter:DELete:ALL

// set 4 traces as S11, S22, S33, S44 separately
CALCulate1:PARameter:SDEFine 'Trc1','S11'
DISPlay:TRACe:Y:SCALe:AUTO ONCE,'Trc1'
CALCulate1:PARameter:SDEFine 'Trc2','S22'
DISPlay:TRACe:Y:SCALe:AUTO ONCE,'Trc2'
CALCulate1:PARameter:SDEFine 'Trc3','S33'
DISPlay:TRACe:Y:SCALe:AUTO ONCE,'Trc3'
CALCulate1:PARameter:SDEFine 'Trc4','S44'
DISPlay:TRACe:Y:SCALe:AUTO ONCE,'Trc4'

// show the 4 traces
DISPlay:WINDow1:TRACe1:FEED 'Trc1'
DISPlay:WINDow1:TRACe2:FEED 'Trc2'
DISPlay:WINDow1:TRACe3:FEED 'Trc3'
DISPlay:WINDow1:TRACe4:FEED 'Trc4'

// list the avalible trace(s)
CONFigure:TRACe:CATalog?
-> 1,Trc1,2,Trc2,3,Trc3,4,Trc4

// data format of the trace data (Ascii or Real,32)
FORMat:DATA REAL,32
FORMat:DATA?
-> REAL,32
FORMat:DATA ASCII,0
FORMat:DATA?
-> ASC,0

// to init a measurement
:ABOR;INITiate1:IMMediate;*OPC?
-> 1

// read the data out
CALCulate1:DATA? FDATa
-> -6.973031005,-6.836939785,-6.149741277,-7.389566844,-8.46104721,-9.444263571,-9.949094778,-11.05311342,-12.84518773,-14.25114571,-15.36676631,-17.04070624,-18.2499027,-18.48954998,-18.97414047,-19.43582721,-18.5602934,-17.81930068,-17.8680514,-18.6339508,-18.03959304,-16.50905126,-16.61946345,-17.55423616,-15.76692865,-16.36001767,-15.65569793,-14.32262178,-15.10083336,-13.63613342,-12.59165989,-11.98086938,-10.31864854,-8.560172543,-7.739745031,-7.578688658,-7.20316281,-6.527214949,-6.198927149,-7.33669188,-7.221104287,-8.717435499,-9.81009466,-10.36633687,-11.83411405,-14.64884263,-16.79767272,-19.9684113,-23.27747304,-26.1595054,-26.34167283,-25.49783884,-23.05576388,-21.54966487,-20.24225834,-18.10764348,-18.16680278,-17.19922152,-16.63693042,-16.22388538,-16.04033286,-15.63756324,-14.82609926,-14.93667341,-13.97603355,-14.40225113,-12.94895307,-12.00867816,-11.89927186,-10.2790073,-10.26925036,-9.204857201,-8.46090752,-8.109486276,-6.788932204,-7.818606171,-6.495430585,-7.995841216,-7.625631801,-9.230150106,-10.1903226,-12.06209334,-13.90782291,-14.77480443,-17.24392115,-19.74607305,-22.58388091,-27.26862776,-31.1514772,-29.38936665,-25.59544191,-23.29181876,-20.88876282,-20.03599259,-18.93021741,-18.97971569,-17.6636217,-16.85542867,-17.120454,-16.78032867,-15.23667387,-15.46048219,-15.40104143,-13.73273433,-14.66745229,-12.79457241,-12.94428032,-12.06355618,-9.833842762,-9.818191338,-9.307537934,-7.250273567,-7.699323097,-8.094816153,-7.538926611,-7.709284889,-7.534036009,-7.157109592,-8.552351897,-9.341885628,-8.648301109,-9.557368517,-11.35769598,-11.99660279,-14.24600094,-16.25944642,-16.47471627,-17.22182701,-17.941955,-17.07842107,-16.83639319,-14.97840293,-14.10360402,-13.70554135,-13.30837785,-13.9192233,-12.94676632,-13.96555601,-13.07562393,-13.22973528,-12.98706524,-12.5724458,-13.02128344,-11.97984509,-12.46018869,-11.64703362,-12.53102975,-12.88703058,-11.59302179,-12.62523064,-12.14404645,-12.14034434,-11.94027319,-11.76155359,-12.50039967,-12.02684802,-13.07943426,-12.9484709,-13.02180741,-12.68612838,-12.55645268,-12.21355727,-13.08830587,-12.53573446,-12.84697532,-12.66014368,-13.12923765,-11.85241625,-13.23700504,-11.70072054,-12.03310236,-13.05427921,-12.28876295,-11.99955796,-12.72567053,-12.02273116,-11.89240081,-12.29637545,-12.30104809,-12.88397552,-12.11574494,-12.51450019,-12.21900977,-12.34409299,-13.13998331,-12.39881301,-11.75614156,-12.4028396,-13.19570223,-13.00661492,-12.47158043,-12.54396289,-11.65902101,-11.68721252,-12.77324987,-12.07497908,-11.80925638,-13.21260309,-12.25960488,-11.88222844,-11.60097965
-----------------------------------------------------------------------------
(previous comment below)


Communicating with Benchtop ENA E5080B, modified from E5071C version
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
		if reset:
			stat = bench.write('*RST;*CLS') #Clear buffer memory;
		else:
			bench.write(':ABORt;:INIT:CONT OFF;') # hold the trigger
			stat = bench.write('*CLS') # Clear buffer memory;
			bench.write('OUTPut:STATE ON') # Power ON
		# Allocating Channels:
		# bench.write(':DISPlay:SPLit %s' %MaxChannel)
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
@Attribute
def sweepmode(bench, action=['Get'] + 10 * ['']):
	'''action=['Get/Set', <mode>]
	HOLD - channel will not trigger
	CONTinuous - channel triggers indefinitely
	SINGle - channel accepts ONE trigger, then goes to HOLD.
	GROups - channel accepts the number of triggers specified with the last SENS:SWE:GRO:COUN <num>. This is one of the VNA overlapped commands. Learn more.
	NOTE: To perform simple, single-triggering, use SINGle which requires that TRIG:SOURce remain in the default (internal) setting.
	'''
	SCPIcore = 'SENSe:SWEep:MODE'
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
	# lai, commented out, for R&S VNA-ZNB
	# if action[1] == 'REAL': action[1] = 'REAL,64' # Redefine ENAB's REAL (32-Bit) into 64-Bit to align with ENA's REAL (64-Bit).
	if action[1] == 'REAL': action[1] = 'REAL,32' # lai, for R&S VNA-ZNB, ZNB only has 'Real,32' format
		
	# lai, commented out, for R&S VNA-ZNB
	# bench.write('FORMat:BORDer NORMal')
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

# Clear ALL measurement(s)
def clearallmeas(bench): return bench.write("CALCulate:PARameter:DELete:ALL") # bench.write(":CALCulate:MEASure:DELete:ALL")

# Setting Trace
def setrace(bench, Mparam=['S11','S21','S12','S22']):
	clearallmeas(bench)
	for iTrace, S in enumerate(Mparam):

		""" lai, commented out, for R&S VNA-ZNB
		S = S.upper() # ENAB only recognize capitalized parameter-names
		# bench.write('CALCulate:MEASure%s:DEFine "%s"' %(iTrace+1, S)) # Creates a measurement but does NOT display it, on an existing or new channel: CH<n>_<param>_<trace#>
		bench.write('CALCulate:PARameter:DEFine:EXTended %s,%s' %(S,S)) # Creates a measurement but does NOT display it.
		bench.write('DISPlay:WINDow:TRACe%s:FEED "%s"' %(iTrace+1, S)) # Feed trace for the measurement
		bench.write(":DISP:WIND:TRAC%d:Y:AUTO"%(iTrace+1)) #pre-auto-scale
		selectrace(bench, action=['Set', '%s,fast'%S]) # improve measurement speed (fast)
		"""		
		bench.write("CALCulate1:PARameter:SDEFine 'Trc%s','%s'" %(iTrace+1,S)) # lai, for R&S VNA-ZNB, set s-parameter from trace1; hasn't shown to screen
		bench.write("DISPlay:TRACe:Y:SCALe:AUTO ONCE,'Trc%s'" %(iTrace+1)) # lai, for R&S VNA-ZNB, y-axis auto scale
	
	return Mparam

# Getting Trace
def getrace(bench):
	'''getting traces displayed on the screen
	'''	
	# lai, commented out, for R&S VNA-ZNB
	# catalog = bench.query("CALCulate:PARameter:CATalog:EXTended?").replace('"','')	
	catalog = bench.query("CONFigure:TRACe:CATalog?") # lai, for R&S VNA-ZNB
	Mreturn = catalog.split(',')[1::2]
	return Mreturn

def autoscal(bench):
	# lai, commented out, for R&S VNA-ZNB
	#tracenum = int(bench.query("CALC:PAR:COUN?"))	
	tracenum = int( bench.query("CONFigure:TRACe:CATalog?").count(',') ) # lai, for R&S VNA-ZNB, count the numbers of ',' symbols to have trace count
	tracenum = int( (tracenum+1)/2 ) # lai, for R&S VNA-ZNB, two ',' for one trace
	
	for i in range(tracenum):
		# lai, commented out, for R&S VNA-ZNB
		# lastatus = bench.write(":DISP:WIND:TRAC%d:Y:AUTO"%(i+1))				
		bench.write("DISPlay:TRACe:Y:SCALe:AUTO ONCE,'Trc%s'" %(i+1)) # lai, for R&S VNA-ZNB, y-axis auto scale		
	return lastatus

def measure(bench):
	# lai, commented out, for R&S VNA-ZNB
	# bench.write(':ABOR;:TRIG:SOUR MAN;:INIT:IMM;') # manually trigger with bus (likened to pressing "Manual Trigger" on the panel)
	bench.write(":ABOR;:TRIG:SOUR MAN;INITiate1:IMMediate") # lai, for R&S VNA-ZNB
	ready = bench.query("*OPC?") # when opc return, the sweep is done
	return ready

def scanning(bench, scan=1):
	if scan:
		stat = bench.write(':ABOR;:TRIG:SOUR IMM;:INIT:CONT ON;')
		sweepmode(bench, action=['Set', 'CONT']) # likened to pressing "Continuous" on the panel
	else:
		stat = bench.write(':ABOR;:TRIG:SOUR MAN;:INIT:CONT OFF;')
		sweepmode(bench, action=['Set', 'HOLD']) # likened to pressing "Hold" on the panel
	return stat

def sdata(bench):
	'''Collect data from ENAB
	This returns the data from the FIRST TRACE.
	'''
	try:		
		# sdatacore = ":CALCulate:MEASure:DATA:SDATa?"
		sdatacore = "CALCulate1:DATA? FDATa"
		
		datatype = dataform(bench)
		# databorder = str(bench.query("FORMat:BORDer?"))
		# print(Fore.CYAN + "Endian (Byte-order): %s" %databorder)
		if datatype[1]['DATA'] == 'REAL,32':
			datas = bench.query_binary_values(sdatacore, datatype='f', is_big_endian=True) # convert the transferred ieee-encoded binaries into list (faster, 32-bit)
		elif datatype[1]['DATA'] == 'REAL,64':
			datas = bench.query_binary_values(sdatacore, datatype='d', is_big_endian=True) # convert the transferred ieee-encoded binaries into list (faster, 64-bit)
		elif datatype[1]['DATA'] == 'ASC,0':
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

	bench = Initiate(False, mode="TEST")
	if bench == "disconnected": pass
	else:
		if debug(mdlname, detail):
			model(bench)
			print(setrace(bench, ['s43','s21']))
			# sweep(bench, action=['Set', 'ON', 1001])
			# ifbw(bench, action=['Set', 1000])
			# ifbw(bench)

			# for i in range(1):
				# if not i:
				# 	input("Press any key to sweep frequency: ")
				# 	f_start, f_stop = 5e9, 7e9
				# 	linfreq(bench, action=['Set', f_start, f_stop]) #F-sweep
				# 	stat = linfreq(bench)
				# 	fstart, fstop = stat[1]['START'], stat[1]['STOP']
				# 	# Building X-axis
				# 	# fstart, fstop = float(fstart), float(fstop)
				# 	power(bench, action=['Set', -31.7])
				# 	power(bench)
					
				# else:
				# 	input('Press any key to sweep power: ')
				# 	cwfreq(bench, action=['Set', 5.257e9])
				# 	cwfreq(bench)
				# 	power(bench, action=['Set', '', -73, -35]) #power sweep
				# 	power(bench)

				# # start sweeping
				# stat = sweep(bench)
				# print("Time-taken would be: %s (%spts)" %(stat[1]['TIME'], stat[1]['POINTS']))
				# print("Ready: %s" %bool(measure(bench)))
				# autoscal(bench)

				# dataform(bench, action=['Set', 'REAL'])
				# data = sdata(bench)
				# print("Data [Type: %s, Length: %s]" %(type(data), len(data)))

				# # Plotting trace:
				# yI, yQ, Amp, Pha = IQAParray(array(data))
				# curve([range(len(data)//2),range(len(data)//2)], [yI,yQ], 'In-Plane', 'Count', 'I(dB)', style=['-b','r'])
				# curve(range(len(data)//2), Amp, 'Amplitude', 'Count', 'Amp(dB)')
				# curve(range(len(data)//2), UnwraPhase(range(len(data)//2), Pha), 'UPhase', 'Count', 'UPha(dB)')

			# TEST SCPI ZONE:
			# print("There is/are %s trace(s)" %str(tracenum(bench)))
			# print("%s trace(s): %s"%(len(getrace(bench)), getrace(bench)))
			# averag(bench, action=['Set', 1]) #optional
			# averag(bench)
			# rfports(bench, action=['Set', 'OFF'])
			# rfports(bench)
			# bench.write(':SYSTem:PRESet')
			# print("Endian (Byte-order): %s" %str(bench.query("FORMat:BORDer?")))
			# scanning(bench) #continuous scan

		else: print(Fore.RED + "Basic IO Test")
	
	input("Press any key to close: ")
	close(bench, mode="TEST")
	return

if __name__ == "__main__":
	test()
'''Basic QuBit Characterizations'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # instrument-module's name e.g. ENA, PSG, YOKO

from time import time, sleep
from numpy import linspace, sin, pi, prod, array
from flask import request, session, current_app, g, Flask

from pyqum.instrument.benchtop import PSGV as PSG0
from pyqum.instrument.benchtop import PSGA as PSG1
from pyqum.instrument.benchtop import ENA, YOKO
from pyqum.instrument.logger import settings, clocker, get_status, set_status
from pyqum.instrument.analyzer import curve, IQAP, UnwraPhase
from pyqum.instrument.toolbox import cdatasearch, gotocdata, waveform

__author__ = "Teik-Hui Lee"
__copyright__ = "Copyright 2019, The Pyqum Project"
__credits__ = ["Chii-Dong Chen"]
__license__ = "GPL"
__version__ = "beta3"
__email__ = "teikhui@phys.sinica.edu.tw"
__status__ = "development"
			
# **********************************************************************************************************************************************************
# 1. FREQUENCY RESPONSE MEASUREMENT:
@settings(2) # data-density
def F_Response(user, tag="", corder={}, comment='', dayindex='', taskentry=0, resumepoint=0, instr=['YOKO','ENA'], testeach=False):
	'''Characterizing Frequency Response:
	C-Order: Flux-Bias, S-Parameter, IF-Bandwidth, Power, Frequency
	'''
	sample = get_status("MSSN")['sample']
	# pushing pre-measurement parameters to settings:
	yield user, sample, tag, instr, corder, comment, dayindex, taskentry, testeach

	# User-defined Controlling-PARAMETER(s) ======================================================================================
	fluxbias = waveform(corder['Flux-Bias'])
	Sparam = waveform(corder['S-Parameter'])
	ifb = waveform(corder['IF-Bandwidth'])
	powa = waveform(corder['Power'])
	freq = waveform(corder['Frequency'])
	# Total data points:
	datasize = prod([waveform(x).count for x in corder.values()]) * 2 #data density of 2 due to IQ

	# Pre-loop settings:
	# ENA:
	bench = ENA.Initiate(True)
	ENA.dataform(bench, action=['Set', 'REAL'])
	ENA.sweep(bench, action=['Set', 'ON', freq.count])
	fstart, fstop = freq.data[0]*1e9, freq.data[-1]*1e9
	ENA.linfreq(bench, action=['Set', fstart, fstop]) # Linear Freq-sweep-range
	# YOKO:
	if "opt" not in fluxbias.data: # check if it is in optional-state
		yokog = YOKO.Initiate(current=True) # PENDING option: choose between Voltage / Current output
		YOKO.output(yokog, 1)

	# Buffer setting(s) for certain loop(s):
	buffersize_1 = freq.count * 2 #data density of 2 due to IQ
	
	# User-defined Measurement-FLOW ==============================================================================================
	if testeach: # measure-time contribution from each measure-loop
		loopcount, loop_dur = [], []
		stage, prev = clocker(0) # Marking starting point of time
	
	# Registerring parameter(s)-structure
	cstructure = [fluxbias.count,Sparam.count,ifb.count,powa.count]

	# set previous parameters based on resumepoint:
	if resumepoint > 0:
		caddress = cdatasearch(resumepoint//buffersize_1, cstructure)
		# Only those involved in virtual for-loop need to be pre-set here:
		if "opt" not in fluxbias.data: # check if it is in optional-state
			YOKO.sweep(yokog, str(fluxbias.data[caddress[0]]), pulsewidth=77*1e-3, sweeprate=0.0007) # A-mode: sweeprate=0.0007 A/s ; V-mode: sweeprate=0.07 V/s
		ENA.setrace(bench, Mparam=[Sparam.data[caddress[1]]], window='D1')
		ENA.ifbw(bench, action=['Set', ifb.data[caddress[2]]])

	measure_loop_1 = range(resumepoint//buffersize_1,datasize//buffersize_1) # saving chunck by chunck improves speed a lot!
	while True:
		for i in measure_loop_1:

			# Registerring parameter(s)
			caddress = cdatasearch(i, cstructure)

			# setting each c-order (From High to Low level of execution):
			if not i%prod(cstructure[1::]): # virtual for-loop using exact-multiples condition
				if "opt" not in fluxbias.data: # check if it is in optional-state
					if testeach: # test each measure-loop:
						loopcount += [fluxbias.count]
						if fluxbias.count > 1: loop_dur += [abs(fluxbias.data[0]-fluxbias.data[1])/0.2 + 35*1e-3]
						else: loop_dur += [0]
						stage, prev = clocker(stage, prev) # Marking time
					else: YOKO.sweep(yokog, str(fluxbias.data[caddress[0]]), pulsewidth=77*1e-3, sweeprate=0.0007) # A-mode: sweeprate=0.0007 A/s ; V-mode: sweeprate=0.07 V/s
					
			if not i%prod(cstructure[2::]): # virtual for-loop using exact-multiples condition
				ENA.setrace(bench, Mparam=[Sparam.data[caddress[1]]], window='D1')

			if not i%prod(cstructure[3::]): # virtual for-loop using exact-multiples condition
				ENA.ifbw(bench, action=['Set', ifb.data[caddress[2]]])

			ENA.power(bench, action=['Set', powa.data[caddress[3]]]) # same as the whole measure-loop

			# start sweeping:
			stat = ENA.sweep(bench) #getting the estimated sweeping time
			print("Time-taken for this loop would be: %s (%spts)" %(stat[1]['TIME'], stat[1]['POINTS']))
			print("Operation Complete: %s" %bool(ENA.measure(bench)))
			# adjusting display on ENA:
			ENA.autoscal(bench)
			ENA.selectrace(bench, action=['Set', 'para 1 calc 1'])
			data = ENA.sdata(bench)
			# print(Fore.YELLOW + "\rProgress: %.3f%% [%s]" %((i+1)/datasize*100, data), end='\r', flush=True)
			print(Fore.YELLOW + "\rProgress: %.3f%%" %((i+1)/datasize*buffersize_1*100), end='\r', flush=True)
			
			# test for the last loop if there is
			if testeach: # test each measure-loop:
				loopcount += [len(measure_loop_1)]
				loop_dur += [time() - prev]
				stage, prev = clocker(stage, prev) # Marking time
				ENA.close(bench)
				if "opt" not in fluxbias.data: # check if it is in optional-state
					YOKO.close(yokog, False)
				yield loopcount, loop_dur
				
			else:
				if get_status("F_Response")['pause']:
					break
				else:
					yield data

		if not get_status("F_Response")['repeat']:
			set_status("F_Response", dict(pause=True))
			ENA.close(bench)
			if "opt" not in fluxbias.data: # check if it is in optional-state
				YOKO.close(yokog, True)
			return

# **********************************************************************************************************************************************************
# 2. CONTINUOUS-WAVE SWEEPING:
@settings(2) # data-density
def CW_Sweep(user, tag="", corder={}, comment='', dayindex='', taskentry=0, resumepoint=0, instr=['PSG','YOKO','ENA'], testeach=False):
	'''Continuous Wave Sweeping:
	C-Order: Flux-Bias, XY-Frequency, XY-Power, S-Parameter, IF-Bandwidth, Frequency, Power
	'''
	sample = get_status("MSSN")['sample']
	# pushing pre-measurement parameters to settings:
	yield user, sample, tag, instr, corder, comment, dayindex, taskentry, testeach

	# User-defined Controlling-PARAMETER(s) ======================================================================================
	fluxbias = waveform(corder['Flux-Bias'])
	xyfreq = waveform(corder['XY-Frequency'])
	xypowa = waveform(corder['XY-Power'])
	Sparam = waveform(corder['S-Parameter'])
	ifb = waveform(corder['IF-Bandwidth'])
	freq = waveform(corder['Frequency'])
	# special treatment to power in this CW-Mode Sweeping:
	powa = waveform(corder['Power'])
	powa_repeat = powa.inner_repeat
	print("power sequence: %s, length: %s, inner-repeat-counts: %s" %(powa.command, powa.count, powa_repeat))
	# input("continue?")

	# Total data points:
	datasize = int(prod([waveform(x).count * waveform(x).inner_repeat for x in corder.values()], dtype='uint64')) * 2 #data density of 2 due to IQ
	print("data size: %s" %datasize)
	
	# Pre-loop settings:
	# ENA:
	bench = ENA.Initiate(True)
	ENA.dataform(bench, action=['Set', 'REAL'])
	if powa_repeat == 1: 
		# collect swept power-data every measure-loop
		ENA.sweep(bench, action=['Set', 'ON', powa.count])
		ENA.power(bench, action=['Set', '', powa.data[0], powa.data[-1]]) # for power sweep (set pstart & pstop)
		buffersize_1 = powa.count * 2 # (buffer) data density of 2 due to IQ
	else: 
		# collect repetitive power-data every measure-loop
		ENA.sweep(bench, action=['Set', 'ON', powa_repeat])
		buffersize_1 = powa_repeat * 2 # (buffer) data density of 2 due to IQ

	# YOKO:
	if "opt" not in fluxbias.data: # check if it is in optional-state / serious-state
		yokog = YOKO.Initiate(current=True) # pending option
		YOKO.output(yokog, 1)

	# PSG:
	if "opt" not in xyfreq.data: # check if it is in optional-state / serious-state
		sogo = PSG0.Initiate() # pending option
		PSG0.rfoutput(sogo, action=['Set', 1])

	# User-defined Measurement-FLOW ==============================================================================================
	if testeach: # measure-time contribution from each measure-loop
		loopcount, loop_dur = [], []
		stage, prev = clocker(0) # Marking starting point of time
	
	# Registerring parameter(s)-structure
	if powa_repeat == 1: cstructure = [fluxbias.count, xyfreq.count, xypowa.count, Sparam.count, ifb.count, freq.count, 1] # just single CW
	else: cstructure = [fluxbias.count, xyfreq.count, xypowa.count, Sparam.count, ifb.count, freq.count, powa.count] # take CW average by repeating
	
	# set previous parameters based on resumepoint:
	if resumepoint//buffersize_1 > 0:
		caddress = cdatasearch(resumepoint//buffersize_1, cstructure)
		# Only those involved in virtual for-loop need to be pre-set here:
		# Optionals:
		if "opt" not in fluxbias.data: # check if it is in optional-state / serious-state
			YOKO.sweep(yokog, str(fluxbias.data[caddress[0]]), pulsewidth=77*1e-3, sweeprate=0.0007) # A-mode: sweeprate=0.0007 A/s ; V-mode: sweeprate=0.07 V/s 
		if "opt" not in xyfreq.data: # check if it is in optional-state / serious-state
			PSG0.frequency(sogo, action=['Set', str(xyfreq.data[caddress[1]]) + "GHz"])
			PSG0.power(sogo, action=['Set', str(xypowa.data[caddress[2]]) + "dBm"])
		# Basics:
		ENA.setrace(bench, Mparam=[Sparam.data[caddress[3]]], window='D1')
		ENA.ifbw(bench, action=['Set', ifb.data[caddress[4]]])
		ENA.cwfreq(bench, action=['Set', freq.data[caddress[5]]*1e9])

	measure_loop_1 = range(resumepoint//buffersize_1,datasize//buffersize_1) # saving chunck by chunck improves speed a lot!
	while True:
		for i in measure_loop_1:

			# determining the index-locations for each parameters, i.e. the address at any instance
			caddress = cdatasearch(i, cstructure)

			# setting each c-order (From High to Low level of execution):
			# ***************************************************************
			# Optionals:
			if not i%prod(cstructure[1::]): # virtual for-loop using exact-multiples condition
				if "opt" not in fluxbias.data: # check if it is in optional-state
					if testeach: # adding instrument transition-time between set-values:
						loopcount += [fluxbias.count]
						if fluxbias.count > 1: loop_dur += [abs(fluxbias.data[0]-fluxbias.data[1])/0.2 + 35*1e-3]
						else: loop_dur += [0]
						stage, prev = clocker(stage, prev) # Marking time
					else: YOKO.sweep(yokog, str(fluxbias.data[caddress[0]]), pulsewidth=77*1e-3, sweeprate=0.0007) # A-mode: sweeprate=0.0007 A/s ; V-mode: sweeprate=0.07 V/s
			
			if not i%prod(cstructure[2::]): # virtual for-loop using exact-multiples condition
				if "opt" not in xyfreq.data: # check if it is in optional-state
					PSG0.frequency(sogo, action=['Set', str(xyfreq.data[caddress[1]]) + "GHz"])

			if not i%prod(cstructure[3::]): # virtual for-loop using exact-multiples condition
				if "opt" not in xypowa.data: # check if it is in optional-state
					PSG0.power(sogo, action=['Set', str(xypowa.data[caddress[2]]) + "dBm"])

			# Basics:
			if not i%prod(cstructure[4::]): # virtual for-loop using exact-multiples condition
				ENA.setrace(bench, Mparam=[Sparam.data[caddress[3]]], window='D1')

			if not i%prod(cstructure[5::]): # virtual for-loop using exact-multiples condition
				ENA.ifbw(bench, action=['Set', ifb.data[caddress[4]]])

			if not i%prod(cstructure[6::]): # virtual for-loop using exact-multiples condition
				ENA.cwfreq(bench, action=['Set', freq.data[caddress[5]]*1e9])

			if powa_repeat > 1:
				ENA.power(bench, action=['Set', '', powa.data[caddress[6]], powa.data[caddress[6]]]) # same as the whole measure-loop

			# start sweeping:
			stat = ENA.sweep(bench) #getting the estimated sweeping time
			print("Time-taken for this loop would be: %s (%spts)" %(stat[1]['TIME'], stat[1]['POINTS']))
			print("Operation Complete: %s" %bool(ENA.measure(bench)))
			# adjusting display on ENA:
			ENA.autoscal(bench)
			ENA.selectrace(bench, action=['Set', 'para 1 calc 1'])
			data = ENA.sdata(bench)
			print(Fore.YELLOW + "\rProgress: %.3f%%" %((i+1)/datasize*buffersize_1*100), end='\r', flush=True)
			
			# test for the last loop if there is
			if testeach: # test each measure-loop:
				loopcount += [len(measure_loop_1)]
				loop_dur += [time() - prev]
				stage, prev = clocker(stage, prev) # Marking time
				ENA.close(bench)
				if "opt" not in xyfreq.data: # check if it is in optional-state
					PSG0.close(sogo, False)
				if "opt" not in fluxbias.data: # check if it is in optional-state
					YOKO.close(yokog, False)
				yield loopcount, loop_dur
				
			else:
				if get_status("CW_Sweep")['pause']:
					break
				else:
					yield data


		if not get_status("CW_Sweep")['repeat']:
			set_status("CW_Sweep", dict(pause=True))
			ENA.close(bench)
			if "opt" not in xyfreq.data: # check if it is in optional-state
				PSG0.rfoutput(sogo, action=['Set', 0])
				PSG0.close(sogo, False)
			if "opt" not in fluxbias.data: # check if it is in optional-state
				YOKO.output(yokog, 0)
				YOKO.close(yokog, False)
			return


def test():
	# New RUN:

	# Ex: CWSWEEP:
	# CORDER = {'Flux-Bias':'1.5 to 3.2 * 70', 'S-Parameter':'S21,', 'IF-Bandwidth':'100', 'Frequency':'5.36 to 5.56 * 250', 'Power':'-25 to 0 * 100 r 1000'}
	# CW_Sweep('abc', corder=CORDER, comment='prototype test', tag='', dayindex=-1, testeach=False)
	
	

	# Retrieve data:
	case = CW_Sweep('abc')
	case.selectday(case.whichday())
	m = case.whichmoment()
	case.selectmoment(m)
	print("File selected: %s" %case.pqfile)
	case.accesstructure()
	print(case.comment)
	
	

	

	return

# test()


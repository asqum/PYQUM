'''Basic QuBit Characterizations'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # instrument-module's name e.g. ENA, PSG, YOKO

from time import time
from numpy import linspace, sin, pi, prod, array
from flask import request, session, current_app, g, Flask

from pyqum.instrument.benchtop import ENA, YOKO
from pyqum.instrument.logger import settings, clocker, get_status
from pyqum.instrument.analyzer import curve, IQAP, UnwraPhase
from pyqum.instrument.toolbox import cdatasearch, gotocdata, waveform

__author__ = "Teik-Hui Lee"
__copyright__ = "Copyright 2019, The Pyqum Project"
__credits__ = ["Chii-Dong Chen"]
__license__ = "GPL"
__version__ = "beta3"
__email__ = "teikhui@phys.sinica.edu.tw"
__status__ = "development"

# @settings(session['user_name'], 'Sam')
@settings('ABC', 'Sam')
def TESTC(tag="", datadensity=1, instr=[], corder={}, comment='', dayindex='', taskentry=0, resumepoint=0):
	'''Serve as a template for other real tasks to come
		dayindex: {string:access data, -1:new data 0-:manage data}
		C-Order: C1, C2, C3, C4, Var
	'''
	# pushing pre-measurement parameters to settings:
	yield tag, datadensity, instr, corder, comment, dayindex, taskentry

	# User-defined Controlling-PARAMETER(s) ======================================================================================
	C1 = waveform(corder['C1'])
	C2 = waveform(corder['C2'])
	C3 = waveform(corder['C3'])
	C4 = waveform(corder['C4'])
	Var = waveform(corder['Var'])
	# ============================================================================================================================
	buffersize = Var.count
	datasize = prod([waveform(x).count for x in corder.values()])
	data = []
	for i in range(resumepoint,datasize):
		caddress = cdatasearch(i, [C1.count,C2.count,C3.count,C4.count,Var.count])

		# User-defined Measurement-FLOW ==============================================================================================
		x = C1.data[caddress[0]] + Var.data[caddress[4]]*C2.data[caddress[1]]*sin(pi/2*C3.data[caddress[2]]) + C4.data[caddress[3]]
		x = i + 1 #for debugging
		# ============================================================================================================================

		data.append(x)
		# saving chunck by chunck improves speed a lot!
		if not (i+1)%buffersize or i==datasize-1: #multiples of buffersize / reached the destination
			print(Fore.YELLOW + "\rProgress: %.3f%% [%s]" %((i+1)/datasize*100, data), end='\r', flush=True)
			yield data
			data = []

@settings(2, 'Sam') # data-density, sample-name
def F_Response(user, tag="", corder={}, comment='', dayindex='', taskentry=0, resumepoint=0, instr=['YOKO','ENA'], testeach=False):
	'''Characterizing Frequency Response:
	C-Order: Flux-Bias, S-Parameter, IF-Bandwidth, Power, Frequency
	'''
	# pushing pre-measurement parameters to settings:
	yield user, tag, instr, corder, comment, dayindex, taskentry, testeach

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
		yokog = YOKO.Initiate()
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
		YOKO.sweep(yokog, str(fluxbias.data[caddress[0]]), pulsewidth=77*1e-3, sweeprate=0.07)
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
						loop_dur += [abs(fluxbias.data[0]-fluxbias.data[1])/0.2 + 35*1e-3]
						stage, prev = clocker(stage, prev) # Marking time
					else: YOKO.sweep(yokog, str(fluxbias.data[caddress[0]]), pulsewidth=77*1e-3, sweeprate=0.07)
					
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
				yield data

		if not get_status("F_Response")['repeat']:
			ENA.close(bench)
			if "opt" not in fluxbias.data: # check if it is in optional-state
				YOKO.close(yokog, True)
			return

	# ============================================================================================================================

@settings(2, 'Sam') # data-density, sample-name
def CW_Sweep(user, tag="", corder={}, comment='', dayindex='', taskentry=0, resumepoint=0, instr=['YOKO','ENA'], testeach=False):
	'''Continuous Wave Sweeping:
	C-Order: Flux-Bias, S-Parameter, IF-Bandwidth, Frequency, Power
	'''
	# pushing pre-measurement parameters to settings:
	yield user, tag, instr, corder, comment, dayindex, taskentry, testeach

	# User-defined Controlling-PARAMETER(s) ======================================================================================
	fluxbias = waveform(corder['Flux-Bias'])
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
		ENA.sweep(bench, action=['Set', 'ON', powa.count])
		ENA.power(bench, action=['Set', '', powa.data[0], powa.data[-1]]) # for power sweep (set pstart & pstop)
		buffersize_1 = powa.count * 2 # (buffer) data density of 2 due to IQ
	else: 
		ENA.sweep(bench, action=['Set', 'ON', powa_repeat])
		# need to set anew in every measure loop
		buffersize_1 = powa_repeat * 2 # (buffer) data density of 2 due to IQ
	
	# YOKO:
	if "opt" not in fluxbias.data: # check if it is in optional-state
		yokog = YOKO.Initiate()
		YOKO.output(yokog, 1)

	# User-defined Measurement-FLOW ==============================================================================================
	if testeach: # measure-time contribution from each measure-loop
		loopcount, loop_dur = [], []
		stage, prev = clocker(0) # Marking starting point of time
	
	# Registerring parameter(s)-structure
	if powa_repeat == 1: cstructure = [fluxbias.count,Sparam.count,ifb.count,freq.count,1] # just single CW
	else: cstructure = [fluxbias.count,Sparam.count,ifb.count,freq.count,powa.count] # take CW average by repeating
	
	# set previous parameters based on resumepoint:
	if resumepoint//buffersize_1 > 0:
		caddress = cdatasearch(resumepoint//buffersize_1, cstructure)
		# Only those involved in virtual for-loop need to be pre-set here:
		YOKO.sweep(yokog, str(fluxbias.data[caddress[0]]), pulsewidth=77*1e-3, sweeprate=0.07)
		ENA.setrace(bench, Mparam=[Sparam.data[caddress[1]]], window='D1')
		ENA.ifbw(bench, action=['Set', ifb.data[caddress[2]]])
		ENA.cwfreq(bench, action=['Set', freq.data[caddress[3]]*1e9])

	measure_loop_1 = range(resumepoint//buffersize_1,datasize//buffersize_1) # saving chunck by chunck improves speed a lot!
	while True:
		for i in measure_loop_1:

			# determining the index-locations for each parameters, i.e. the address at any instance
			caddress = cdatasearch(i, cstructure)

			# setting each c-order (From High to Low level of execution):
			if not i%prod(cstructure[1::]): # virtual for-loop using exact-multiples condition
				if "opt" not in fluxbias.data: # check if it is in optional-state
					if testeach: # test each measure-loop:
						loopcount += [fluxbias.count]
						loop_dur += [abs(fluxbias.data[0]-fluxbias.data[1])/0.2 + 35*1e-3]
						stage, prev = clocker(stage, prev) # Marking time
					else: YOKO.sweep(yokog, str(fluxbias.data[caddress[0]]), pulsewidth=77*1e-3, sweeprate=0.07)
					
			if not i%prod(cstructure[2::]): # virtual for-loop using exact-multiples condition
				ENA.setrace(bench, Mparam=[Sparam.data[caddress[1]]], window='D1')

			if not i%prod(cstructure[3::]): # virtual for-loop using exact-multiples condition
				ENA.ifbw(bench, action=['Set', ifb.data[caddress[2]]])

			if not i%prod(cstructure[4::]): # virtual for-loop using exact-multiples condition
				ENA.cwfreq(bench, action=['Set', freq.data[caddress[3]]*1e9])

			if powa_repeat > 1:
				ENA.power(bench, action=['Set', '', powa.data[caddress[4]], powa.data[caddress[4]]]) # same as the whole measure-loop

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
				if "opt" not in fluxbias.data: # check if it is in optional-state
					YOKO.close(yokog, False)
				yield loopcount, loop_dur
				
			else:
				yield data

		if not get_status("CW_Sweep")['repeat']:
			ENA.close(bench)
			if "opt" not in fluxbias.data: # check if it is in optional-state
				YOKO.close(yokog, True)
			return

	# ============================================================================================================================


def test():
	# CORDER = {'Flux-Bias':'1.5 to 3.2 * 70', 'S-Parameter':'S21,', 'IF-Bandwidth':'100', 'Frequency':'5.36 to 5.56 * 250', 'Power':'-25 to 0 * 100 r 1000'}
	# CW_Sweep('abc', corder=CORDER, comment='prototype test', tag='', dayindex=-1, testeach=False)
	case = CW_Sweep('abc')
	case.selectday(case.whichday())
	m = case.whichmoment()
	case.selectmoment(m)
	print("File selected: %s" %case.pqfile)
	print("Make analysis: %s" %case.mkanalysis(m))
	case.accesstructure()
	print(case.comment)
	print("Yuhan in comment: %s" %("yuhan" in case.comment.lower()))
	print(case.corder['Power'])
	AveNum = waveform(case.corder['Power']).inner_repeat
	print("Average#: %s" %AveNum)

	# load data to analyze:
	# case.loadata()
	# datas = case.selectedata
	# CWAveData = array(datas).reshape(len(datas)//2//AveNum, 2*AveNum)
	# case.savanalysis('CWAve', CWAveData)
	
	# read from h5
	data = case.loadanalysis('CWAve')
	print("loaded shape: %s,%s" %array(data).shape)

	return

# test()


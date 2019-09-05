# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name

import requests, json
from flask import Flask, request, render_template, Response, redirect, Blueprint, jsonify, stream_with_context, g, session
from numpy import array, unwrap, mean
from time import sleep
from datetime import timedelta

from pyqum.instrument.logger import address, get_status, set_status, status_code, output_code, set_csv, clocker
from pyqum.instrument.toolbox import cdatasearch, gotocdata, waveform
from pyqum.instrument.analyzer import IQAP, UnwraPhase

from pyqum.directive.characterize import F_Response, CW_Sweep

# Scientific Constants
from scipy import constants as cnst

# subprocess to cmd
from subprocess import Popen, PIPE, STDOUT
import os, signal

__author__ = "Teik-Hui Lee"
__copyright__ = "Copyright 2019, The Pyqum Project"
__credits__ = ["Chii-Dong Chen"]
__license__ = "GPL"
__version__ = "beta3"
__email__ = "teikhui@phys.sinica.edu.tw"
__status__ = "development"

encryp = 'ghhgjad'
bp = Blueprint(myname, __name__, url_prefix='/mssn')

# Main
@bp.route('/')
def show():
	return render_template("blog/msson/mission.html", encryp=encryp)

# ALL
@bp.route('/all', methods=['GET'])
def all(): 
	# Test Bed # All Task # Great Work
	return render_template("blog/msson/all.html")
@bp.route('/all/test', methods=['GET'])
def alltest():
	i = request.args.get('idea')
	print(Back.MAGENTA + 'i: %s'%i)
	return jsonify(i=i)
@bp.route('/all/insertopt', methods=['GET'])
def allinsertopt():
	x = [100, 200, 300, 400, 500, 600, 777]
	return jsonify(x=x)
@bp.route('/all/streamjson', methods=['GET'])
def allstreamjson():
	sj = int(request.args.get('sj'))*2
	sleep(1)
	return jsonify(sj=sj)

# CHAR:
@bp.route('/char', methods=['GET'])
def char(): 
	return render_template("blog/msson/char.html")
@bp.route('/char/loadusers', methods=['GET'])
def char_loadusers(): 
	print("analysis-shared users: %s\n" %g.user["analysis"])
	shared_users = waveform(g.user["analysis"]).data # extract allowed to-be-shared user-list from db
	return jsonify(shared_users=shared_users)
@bp.route('/char/activeuser', methods=['GET'])
def char_activeuser():
	session['people'] = request.args.get('people')
	message = "%s is stalking on %s" %(session['user_name'], session['people'])
	session['run_clearance'] = bool(session['user_name'] == session['people'])
	return jsonify(message=message, run_permission=session['run_clearance'])

# CHAR -> 1. F-Response ============================================================================================================================================
@bp.route('/char/fresp', methods=['GET'])
def char_fresp(): 
	return render_template("blog/msson/char/fresp.html")
# Initialize and list days specific to task
@bp.route('/char/fresp/init', methods=['GET'])
def char_fresp_init(): 
	global M_fresp
	try: print(Fore.GREEN + "Connected M-USER(s): %s" %M_fresp.keys())
	except: M_fresp = {}
	set_status("F_Response", dict(repeat=False))
	M_fresp[session['user_name']] = F_Response(session['people']) # initializing Law Maker -> Executioner
	return jsonify(daylist=M_fresp[session['user_name']].daylist, run_permission=session['run_clearance'])
# list task entries based on day picked
@bp.route('/char/fresp/time', methods=['GET'])
def char_fresp_time():
	wday = int(request.args.get('wday'))
	M_fresp[session['user_name']].selectday(wday)
	return jsonify(taskentries=M_fresp[session['user_name']].taskentries)

# adjust settings input for certain instruments' set
@bp.route('/char/fresp/settings', methods=['GET'])
def char_fresp_settings():
	# under construction...
	return jsonify()

# new measurement setup
@bp.route('/char/fresp/new', methods=['GET'])
def char_fresp_new():
	global Run_fresp
	wday = int(request.args.get('wday'))
	print("wday: %s" %wday)
	fluxbias = request.args.get('fluxbias')
	sparam = request.args.get('sparam')
	ifb = request.args.get('ifb')
	powa = request.args.get('powa')
	freq = request.args.get('freq')
	comment = request.args.get('comment').replace("\"","")
	simulate = bool(int(request.args.get('simulate')))
	CORDER = {'Flux-Bias':fluxbias, 'S-Parameter':sparam, 'IF-Bandwidth':ifb, 'Power':powa, 'Frequency':freq}
	Run_fresp = F_Response(session['people'], corder=CORDER, comment=comment, tag='', dayindex=wday, testeach=simulate)
	return jsonify(testeach=simulate)
# ETA (Estimated Time of Arrival for the WHOLE measurement)
@bp.route('/char/fresp/eta100', methods=['GET'])
def char_fresp_eta100():
	eta_time_100 = sum([a*b for a,b in zip(Run_fresp.loopcount, Run_fresp.loop_dur)])
	print(Fore.RED + "ETA: %s" %str(timedelta(seconds=eta_time_100)))
	eta_time_100 = str(timedelta(seconds=eta_time_100)).split('.')[0]
	return jsonify(eta_time_100=eta_time_100)
# toggle between repeat or not
@bp.route('/char/fresp/repeat', methods=['GET'])
def char_fresp_repeat():
	set_status("F_Response", dict(repeat=bool(int(request.args.get('repeat')))))
	return jsonify(repeat=get_status("F_Response")['repeat'])
# search through logs of data specific to task
@bp.route('/char/fresp/search', methods=['GET'])
def char_fresp_search():
	wday = int(request.args.get('wday'))
	filelist = M_fresp[session['user_name']].searchcomment()
	return jsonify(filelist=str(filelist))
# export to csv
@bp.route('/char/fresp/export/1dcsv', methods=['GET'])
def char_fresp_export_1dcsv():
	ifreq = request.args.get('ifreq') # merely for security reason to block out unsolicited visits by return None from this request
	print("ifreq: %s" %ifreq)
	status = None
	if ifreq is not None:
		set_csv(data_dict, '1Dfresp.csv')
		status = "csv written"
	return jsonify(status=status)
# list set-parameters based on selected task-entry
@bp.route('/char/fresp/access', methods=['GET'])
def char_fresp_access():
	wmoment = int(request.args.get('wmoment'))
	M_fresp[session['user_name']].selectmoment(wmoment)
	M_fresp[session['user_name']].accesstructure()
	data_progress = M_fresp[session['user_name']].data_progress
	try: cfluxbias = waveform(M_fresp[session['user_name']].corder['Flux-Bias'])
	except(KeyError): cfluxbias = waveform('opt,')
	csparam = waveform(M_fresp[session['user_name']].corder['S-Parameter'])
	cifb = waveform(M_fresp[session['user_name']].corder['IF-Bandwidth'])
	cpowa = waveform(M_fresp[session['user_name']].corder['Power'])
	cfreq = waveform(M_fresp[session['user_name']].corder['Frequency'])
	session['c_fresp_structure'] = [cfluxbias.count,csparam.count,cifb.count,cpowa.count,cfreq.count*M_fresp[session['user_name']].datadensity]
	session['c_fresp_address'] = cdatasearch(M_fresp[session['user_name']].resumepoint-1, session['c_fresp_structure'])
	# list each parameter range based on data-progress:
	cfluxbias_data = cfluxbias.data[0:session['c_fresp_address'][0]+1]
	csparam_data = csparam.data[0:session['c_fresp_address'][1]+1]
	cifb_data = cifb.data[0:session['c_fresp_address'][2]+1]
	cpowa_data = cpowa.data[0:session['c_fresp_address'][3]+1]
	cfreq_data = cfreq.data # within buffer
	return jsonify(data_progress=data_progress, corder=M_fresp[session['user_name']].corder, comment=M_fresp[session['user_name']].comment, 
		cfluxbias_data=cfluxbias_data,
		csparam_data=csparam_data, cifb_data=cifb_data, cpowa_data=cpowa_data, cfreq_data=cfreq_data)
# Resume the unfinished measurement
@bp.route('/char/fresp/resume', methods=['GET'])
def char_fresp_resume():
	wday = int(request.args.get('wday'))
	wmoment = int(request.args.get('wmoment'))
	fluxbias = request.args.get('fluxbias')
	sparam = request.args.get('sparam')
	ifb = request.args.get('ifb')
	powa = request.args.get('powa')
	freq = request.args.get('freq')
	CORDER = {'Flux-Bias':fluxbias, 'S-Parameter':sparam, 'IF-Bandwidth':ifb, 'Power':powa, 'Frequency':freq}
	M_fresp[session['user_name']].accesstructure()
	F_Response(session['people'], corder=CORDER, dayindex=wday, taskentry=wmoment, resumepoint=M_fresp[session['user_name']].resumepoint)
	return jsonify(resumepoint=str(M_fresp[session['user_name']].resumepoint), datasize=str(M_fresp[session['user_name']].datasize))
# Chart is supposedly shared by all measurements (under construction for nulti-purpose)
@bp.route('/char/fresp/1ddata', methods=['GET'])
def char_fresp_1ddata():
	print(Fore.GREEN + "User %s is plotting 1D-Data" %session['user_name'])
	M_fresp[session['user_name']].loadata()
	selectedata = M_fresp[session['user_name']].selectedata
	ifluxbias = request.args.get('ifluxbias')
	# if ifluxbias == "o": ifluxbias = '0' # for backward compatibility
	isparam = request.args.get('isparam')
	iifb = request.args.get('iifb')
	ipowa = request.args.get('ipowa')
	ifreq = request.args.get('ifreq')
	if ifluxbias == "x":
		title = "<b>Flux-Bias(V)</b>"
		selected_sweep = M_fresp[session['user_name']].corder['Flux-Bias']
		selected_progress = waveform(selected_sweep).data[0:session['c_fresp_address'][0]+1]
		selected_I = [selectedata[gotocdata([x, int(isparam), int(iifb), int(ipowa), 2*int(ifreq)], session['c_fresp_structure'])] for x in range(session['c_fresp_address'][0]+1)]
		selected_Q = [selectedata[gotocdata([x, int(isparam), int(iifb), int(ipowa), 2*int(ifreq)+1], session['c_fresp_structure'])] for x in range(session['c_fresp_address'][0]+1)]
	elif isparam == "x":
		pass
	elif iifb == "x":
		pass
	elif ipowa == "x":
		title = "<b>Power(dBm)</b>"
		selected_sweep = M_fresp[session['user_name']].corder['Power']
		selected_progress = waveform(selected_sweep).data[0:session['c_fresp_address'][3]+1]
		selected_I = [selectedata[gotocdata([int(ifluxbias), int(isparam), int(iifb), x, 2*int(ifreq)], session['c_fresp_structure'])] for x in range(session['c_fresp_address'][3]+1)]
		selected_Q = [selectedata[gotocdata([int(ifluxbias), int(isparam), int(iifb), x, 2*int(ifreq)+1], session['c_fresp_structure'])] for x in range(session['c_fresp_address'][3]+1)]
	elif ifreq == "x":
		title = "<b>frequency(GHz)</b>"
		selected_sweep = M_fresp[session['user_name']].corder['Frequency']
		selected_progress = waveform(selected_sweep).data # Full sweep
		selected_I = [selectedata[gotocdata([int(ifluxbias), int(isparam), int(iifb), int(ipowa), 2*x], session['c_fresp_structure'])] for x in range(waveform(selected_sweep).count)]
		selected_Q = [selectedata[gotocdata([int(ifluxbias), int(isparam), int(iifb), int(ipowa), 2*x+1], session['c_fresp_structure'])] for x in range(waveform(selected_sweep).count)]
	MagPha = [IQAP(x[0],x[1]) for x in zip(selected_I, selected_Q)]
	Amp, Pha = [], []
	for i,j in MagPha:
		Amp.append(i); Pha.append(j)
	x1, y1, y2 = selected_progress, Amp, list(UnwraPhase(selected_progress, Pha)) #list(unwrap(Pha)) 
	global data_dict
	data_dict = {title: x1, 'Amplitude': y1, 'UPhase': y2, 'I': selected_I, 'Q': selected_Q, "exported by": session['user_name']}
	return jsonify(x1=x1, y1=y1, y2=y2, title=title)
@bp.route('/char/fresp/2ddata', methods=['GET'])
def char_fresp_2ddata():
	# M_fresp[session['user_name']].loadata()
	# selectedata = M_fresp[session['user_name']].selectedata
	ifluxbias = request.args.get('ifluxbias')
	# if ifluxbias == "o": ifluxbias = '0' # for backward compatibility
	isparam = request.args.get('isparam')
	iifb = request.args.get('iifb')
	ipowa = request.args.get('ipowa')
	ifreq = request.args.get('ifreq')
	x, y, ZZ = [], [], []
	dict_for_MPW = {
			"pqfile": str(M_fresp[session['user_name']].pqfile), "datalocation": M_fresp[session['user_name']].datalocation, "writtensize": M_fresp[session['user_name']].writtensize,
			"c_fresp_structure": session['c_fresp_structure'], "ifluxbias": ifluxbias, "isparam": isparam, "iifb": iifb, "ipowa": ipowa, "ifreq": ifreq,
		}
	set_status("MPW", dict_for_MPW)
	if ifluxbias == "x" and ifreq == "y":
		print("X: Flux-Bias, Y: Frequency")
		xtitle, ytitle = "<b>Flux-Bias(V)</b>", "<b>frequency(GHz)</b>"
		x, y = waveform(M_fresp[session['user_name']].corder['Flux-Bias']).data[0:session['c_fresp_address'][0]+1], waveform(M_fresp[session['user_name']].corder['Frequency']).data
		x_count, y_count = session['c_fresp_address'][0]+1, waveform(M_fresp[session['user_name']].corder['Frequency']).count

		stage, prev = clocker(0)
		CMD = ["python", "-c", "from pyqum.directive import MP_fresp as mp; print(mp.worker(%s,%s))"%(y_count,x_count)]
		with Popen(CMD, stdout=PIPE, shell=True) as proc:
			output = json.loads(proc.stdout.read().decode("utf-8").replace("\'", "\""))
			# try: os.kill(os.getppid(), signal.SIGTERM) # terminate parent process
			# except: pass
		stage, prev = clocker(stage, prev) # Marking time

		# slow iteration method:
		# Amp, Pha = [], []
		# for j in range(y_count):
		# 	I = [selectedata[gotocdata([x, int(session['isparam']), int(session['iifb']), int(session['ipowa']), 2*j], session['c_fresp_structure'])] for x in range(x_count)]
		# 	Q = [selectedata[gotocdata([x, int(session['isparam']), int(session['iifb']), int(session['ipowa']), 2*j+1], session['c_fresp_structure'])] for x in range(x_count)]
		# 	amp, pha = [], []
		# 	for i,q in zip(I,Q):
		# 		a,p = IQAP(i,q)
		# 		amp.append(a); pha.append(p)
		# 	Amp += [amp]; Pha += [pha]

		print("x is of length %s and of type %s" %(len(x),type(x)))
		print("y is of length %s and of type %s" %(len(y),type(y)))
		
		Amp = output['rA']
		print("Amp of shape %s" %str(array(Amp).shape))
		ZZ = Amp
		
	elif ipowa == "x" and ifreq == "y":
		print("X: Power, Y: Frequency")
		xtitle, ytitle = "<b>Power(V)</b>", "<b>frequency(GHz)</b>"
		x, y = waveform(M_fresp[session['user_name']].corder['Power']).data[0:session['c_fresp_address'][3]+1], waveform(M_fresp[session['user_name']].corder['Frequency']).data
		x_count, y_count = session['c_fresp_address'][3]+1, waveform(M_fresp[session['user_name']].corder['Frequency']).count

		stage, prev = clocker(0)
		CMD = ["python", "-c", "from pyqum.directive import MP_fresp as mp; print(mp.worker(%s,%s,%s,%s))"%(y_count,x_count,'"freq"','"powa"')]
		with Popen(CMD, stdout=PIPE, shell=True) as proc:
			output = json.loads(proc.stdout.read().decode("utf-8").replace("\'", "\""))
			# try: os.kill(os.getppid(), signal.SIGTERM) # terminate parent process
			# except: pass
		stage, prev = clocker(stage, prev) # Marking time

		print("x is of length %s and of type %s" %(len(x),type(x)))
		print("y is of length %s and of type %s" %(len(y),type(y)))
		
		Amp = output['rA']
		print("Amp of shape %s" %str(array(Amp).shape))
		ZZ = Amp

	elif session['iifb'] == "x":
		pass
	
	# x = list(range(len(x))) # for repetitive data
	return jsonify(x=x, y=y, ZZ=ZZ, xtitle=xtitle, ytitle=ytitle)

# CHAR -> 2. CW-Sweeping =============================================================================================================================================
@bp.route('/char/cwsweep', methods=['GET'])
def char_cwsweep(): 
	return render_template("blog/msson/char/cwsweep.html")
# Initialize and list days specific to task
@bp.route('/char/cwsweep/init', methods=['GET'])
def char_cwsweep_init(): 
	global M_cwsweep
	try: print(Fore.GREEN + "Connected M-USER(s): %s" %M_cwsweep.keys())
	except: M_cwsweep = {}
	set_status("CW_Sweep", dict(repeat=False))
	M_cwsweep[session['user_name']] = CW_Sweep(session['people']) # initializing Law Maker -> Executioner
	return jsonify(daylist=M_cwsweep[session['user_name']].daylist, run_permission=session['run_clearance'])
# list task entries based on day picked
@bp.route('/char/cwsweep/time', methods=['GET'])
def char_cwsweep_time():
	wday = int(request.args.get('wday'))
	M_cwsweep[session['user_name']].selectday(wday)
	return jsonify(taskentries=M_cwsweep[session['user_name']].taskentries)

# adjust settings input for certain instruments' set
@bp.route('/char/cwsweep/settings', methods=['GET'])
def char_cwsweep_settings():
	# under construction ***
	return jsonify()

# new measurement setup
@bp.route('/char/cwsweep/new', methods=['GET'])
def char_cwsweep_new():
	global Run_cwsweep # for ETA calculation as well
	wday = int(request.args.get('wday'))
	print("wday: %s" %wday)
	fluxbias = request.args.get('fluxbias')
	sparam = request.args.get('sparam')
	ifb = request.args.get('ifb')
	freq = request.args.get('freq')
	powa = request.args.get('powa')
	comment = request.args.get('comment').replace("\"","")
	simulate = bool(int(request.args.get('simulate')))
	CORDER = {'Flux-Bias':fluxbias, 'S-Parameter':sparam, 'IF-Bandwidth':ifb, 'Frequency':freq, 'Power':powa}
	Run_cwsweep = CW_Sweep(session['people'], corder=CORDER, comment=comment, tag='', dayindex=wday, testeach=simulate)
	return jsonify(testeach=simulate)
# ETA (Estimated Time of Arrival for the WHOLE measurement)
@bp.route('/char/cwsweep/eta100', methods=['GET'])
def char_cwsweep_eta100():
	eta_time_100 = sum([a*b for a,b in zip(Run_cwsweep.loopcount, Run_cwsweep.loop_dur)])
	print(Fore.RED + "ETA: %s" %str(timedelta(seconds=eta_time_100)))
	eta_time_100 = str(timedelta(seconds=eta_time_100)).split('.')[0]
	return jsonify(eta_time_100=eta_time_100)
# toggle between repeat or not
@bp.route('/char/cwsweep/repeat', methods=['GET'])
def char_cwsweep_repeat():
	set_status("CW_Sweep", dict(repeat=bool(int(request.args.get('repeat')))))
	return jsonify(repeat=get_status("CW_Sweep")['repeat'])
# search through logs of data specific to task
@bp.route('/char/cwsweep/search', methods=['GET'])
def char_cwsweep_search():
	wday = int(request.args.get('wday'))
	filelist = M_cwsweep[session['user_name']].searchcomment()
	return jsonify(filelist=str(filelist))
# export to csv
@bp.route('/char/cwsweep/export/1dcsv', methods=['GET'])
def char_cwsweep_export_1dcsv():
	ifreq = request.args.get('ifreq') # merely for security reason to block out unsolicited visits by return None from this request
	print("ifreq: %s" %ifreq)
	status = None
	if ifreq is not None:
		set_csv(data_dict, '1Dcwsweep.csv')
		status = "csv written"
	return jsonify(status=status)
# list set-parameters based on selected task-entry
@bp.route('/char/cwsweep/access', methods=['GET'])
def char_cwsweep_access():
	wmoment = int(request.args.get('wmoment'))
	M_cwsweep[session['user_name']].selectmoment(wmoment)
	M_cwsweep[session['user_name']].accesstructure()
	data_progress = M_cwsweep[session['user_name']].data_progress
	try: cfluxbias = waveform(M_cwsweep[session['user_name']].corder['Flux-Bias'])
	except(KeyError): cfluxbias = waveform('opt,') # create virtual list for the absence of this in older file
	csparam = waveform(M_cwsweep[session['user_name']].corder['S-Parameter'])
	cifb = waveform(M_cwsweep[session['user_name']].corder['IF-Bandwidth'])
	cfreq = waveform(M_cwsweep[session['user_name']].corder['Frequency'])
	cpowa = waveform(M_cwsweep[session['user_name']].corder['Power'])
	cpowa_repeat = cpowa.inner_repeat
	session['c_cwsweep_structure'] = [cfluxbias.count,csparam.count,cifb.count,cfreq.count,cpowa.count*cpowa_repeat*M_cwsweep[session['user_name']].datadensity]
	session['c_cwsweep_address'] = cdatasearch(M_cwsweep[session['user_name']].resumepoint-1, session['c_cwsweep_structure'])
	# list each parameter range based on data-progress:
	cfluxbias_data = cfluxbias.data[0:session['c_cwsweep_address'][0]+1]
	csparam_data = csparam.data[0:session['c_cwsweep_address'][1]+1]
	cifb_data = cifb.data[0:session['c_cwsweep_address'][2]+1]
	cfreq_data = cfreq.data[0:session['c_cwsweep_address'][3]+1]
	cpowa_data = cpowa.data[0:(session['c_cwsweep_address'][4]+1)//cpowa_repeat]  # (to be adjusted ***)
	return jsonify(data_progress=data_progress, corder=M_cwsweep[session['user_name']].corder, comment=M_cwsweep[session['user_name']].comment, 
		cfluxbias_data=cfluxbias_data,
		csparam_data=csparam_data, cifb_data=cifb_data, cfreq_data=cfreq_data, cpowa_data=cpowa_data)
# Resume the unfinished measurement
@bp.route('/char/cwsweep/resume', methods=['GET'])
def char_cwsweep_resume():
	wday = int(request.args.get('wday'))
	wmoment = int(request.args.get('wmoment'))
	fluxbias = request.args.get('fluxbias')
	sparam = request.args.get('sparam')
	ifb = request.args.get('ifb')
	freq = request.args.get('freq')
	powa = request.args.get('powa')
	CORDER = {'Flux-Bias':fluxbias, 'S-Parameter':sparam, 'IF-Bandwidth':ifb, 'Frequency':freq, 'Power':powa}
	M_cwsweep[session['user_name']].accesstructure()
	CW_Sweep(session['people'], corder=CORDER, dayindex=wday, taskentry=wmoment, resumepoint=M_cwsweep[session['user_name']].resumepoint)
	return jsonify(resumepoint=str(M_cwsweep[session['user_name']].resumepoint), datasize=str(M_cwsweep[session['user_name']].datasize))
# Chart is supposedly shared by all measurements (under construction for nulti-purpose)
@bp.route('/char/cwsweep/1ddata', methods=['GET'])
def char_cwsweep_1ddata():
	print(Fore.GREEN + "User %s is plotting 1D-Data" %session['user_name'])
	M_cwsweep[session['user_name']].loadata()
	selectedata = M_cwsweep[session['user_name']].selectedata
	ifluxbias = request.args.get('ifluxbias')
	isparam = request.args.get('isparam')
	iifb = request.args.get('iifb')
	ifreq = request.args.get('ifreq')
	ipowa = request.args.get('ipowa')
	if "x" in ifluxbias:
		title = "<b>Flux-Bias(V)</b>"
		selected_sweep = M_cwsweep[session['user_name']].corder['Flux-Bias']
		selected_progress = waveform(selected_sweep).data[0:session['c_cwsweep_address'][0]+1]
		# pre-transform ipowa:
		ipowa_repeat = waveform(M_cwsweep[session['user_name']].corder['Power']).inner_repeat
		selected_Ir, selected_Qr = [], []
		for i_repeat in range(ipowa_repeat):
			r_powa = int(ipowa) * ipowa_repeat + i_repeat # from the beginning position of repeating power
			selected_Ir += [selectedata[gotocdata([x, int(isparam), int(iifb), int(ifreq), 2*r_powa], session['c_cwsweep_structure'])] for x in range(session['c_cwsweep_address'][0]+1)]
			selected_Qr += [selectedata[gotocdata([x, int(isparam), int(iifb), int(ifreq), 2*r_powa+1], session['c_cwsweep_structure'])] for x in range(session['c_cwsweep_address'][0]+1)]
		# averaging up those power repeats:
		selected_I = list(mean(array(selected_Ir).reshape(ipowa_repeat, session['c_cwsweep_address'][0]+1), axis=0))
		selected_Q = list(mean(array(selected_Qr).reshape(ipowa_repeat, session['c_cwsweep_address'][0]+1), axis=0))
	elif "x" in isparam:
		pass
	elif "x" in iifb:
		pass
	elif "x" in ifreq:
		title = "<b>frequency(GHz)</b>"
		selected_sweep = M_cwsweep[session['user_name']].corder['Frequency']
		selected_progress = waveform(selected_sweep).data[0:session['c_cwsweep_address'][3]+1]
		# pre-transform ipowa:
		ipowa_repeat = waveform(M_cwsweep[session['user_name']].corder['Power']).inner_repeat
		selected_Ir, selected_Qr = [], []
		for i_repeat in range(ipowa_repeat):
			r_powa = int(ipowa) * ipowa_repeat + i_repeat # from the beginning position of repeating power
			selected_Ir += [selectedata[gotocdata([int(ifluxbias), int(isparam), int(iifb), x, 2*r_powa], session['c_cwsweep_structure'])] for x in range(session['c_cwsweep_address'][3]+1)]
			selected_Qr += [selectedata[gotocdata([int(ifluxbias), int(isparam), int(iifb), x, 2*r_powa+1], session['c_cwsweep_structure'])] for x in range(session['c_cwsweep_address'][3]+1)]
		# averaging up those power repeats:
		selected_I = list(mean(array(selected_Ir).reshape(ipowa_repeat, session['c_cwsweep_address'][3]+1), axis=0))
		selected_Q = list(mean(array(selected_Qr).reshape(ipowa_repeat, session['c_cwsweep_address'][3]+1), axis=0))
	elif "x" in ipowa:
		title = "<b>Power(dBm)</b>"
		selected_sweep = M_cwsweep[session['user_name']].corder['Power']
		xpowa = waveform(selected_sweep)
		xpowa_repeat = xpowa.inner_repeat
		selected_progress = xpowa.data[0:(session['c_cwsweep_address'][4]+1)//xpowa_repeat]
		selected_Ir = [selectedata[gotocdata([int(ifluxbias), int(isparam), int(iifb), int(ifreq), 2*x], session['c_cwsweep_structure'])] for x in range(session['c_cwsweep_address'][4]+1)]
		selected_Qr = [selectedata[gotocdata([int(ifluxbias), int(isparam), int(iifb), int(ifreq), 2*x+1], session['c_cwsweep_structure'])] for x in range(session['c_cwsweep_address'][4]+1)]
		# Average the repeated IQ-pairs:
		selected_I = list(mean(array(selected_Ir).reshape(xpowa.count, xpowa_repeat), axis=1)) #-->
		selected_Q = list(mean(array(selected_Qr).reshape(xpowa.count, xpowa_repeat), axis=1)) #-->

	# assembly amplitude & phase:
	MagPha = [IQAP(x[0],x[1]) for x in zip(selected_I, selected_Q)]
	Amp, Pha = [], []
	for i,j in MagPha:
		Amp.append(i); Pha.append(j)

	# to avoid exception when encountering recursive parameters:
	if "c" in ifluxbias + isparam + iifb + ifreq + ipowa:
		selected_progress = list(range(len(selected_progress)))

	x1, y1, y2 = selected_progress, Amp, list(UnwraPhase(selected_progress, Pha)) #list(unwrap(Pha)) 

	global data_dict
	data_dict = {title: x1, 'Amplitude': y1, 'UPhase': y2, 'I': selected_I, 'Q': selected_Q, "exported by": session['user_name']}
	return jsonify(x1=x1, y1=y1, y2=y2, title=title)
@bp.route('/char/cwsweep/2ddata', methods=['GET'])
def char_cwsweep_2ddata():
	# M_cwsweep[session['user_name']].loadata()
	# selectedata = M_cwsweep[session['user_name']].selectedata
	ifluxbias = request.args.get('ifluxbias')
	# if ifluxbias == "o": ifluxbias = '0' # for backward compatibility
	isparam = request.args.get('isparam')
	iifb = request.args.get('iifb')
	ipowa = request.args.get('ipowa')
	ifreq = request.args.get('ifreq')
	x, y, ZZ = [], [], []
	dict_for_MPW = {
			"pqfile": str(M_cwsweep[session['user_name']].pqfile), "datalocation": M_cwsweep[session['user_name']].datalocation, "writtensize": M_cwsweep[session['user_name']].writtensize,
			"c_cwsweep_structure": session['c_cwsweep_structure'], "ifluxbias": ifluxbias, "isparam": isparam, "iifb": iifb, "ifreq": ifreq, "ipowa": ipowa
		}
	set_status("MPW", dict_for_MPW)
	if ifluxbias == "x" and ifreq == "y":
		print("X: Flux-Bias, Y: Frequency")
		xtitle, ytitle = "<b>Flux-Bias(V)</b>", "<b>frequency(GHz)</b>"
		x, y = waveform(M_cwsweep[session['user_name']].corder['Flux-Bias']).data[0:session['c_cwsweep_address'][0]+1], waveform(M_cwsweep[session['user_name']].corder['Frequency']).data
		x_count, y_count = session['c_cwsweep_address'][0]+1, waveform(M_cwsweep[session['user_name']].corder['Frequency']).count

		stage, prev = clocker(0)
		CMD = ["python", "-c", "from pyqum.directive import multiprocessor as mp; print(mp.worker_cwsweep(%s,%s))"%(y_count,x_count)]
		with Popen(CMD, stdout=PIPE, shell=True) as proc:
			output = json.loads(proc.stdout.read().decode("utf-8").replace("\'", "\""))
			try: os.kill(os.getppid(), signal.SIGTERM) # terminate parent process
			except: pass
		stage, prev = clocker(stage, prev) # Marking time

		# slow iteration method:
		# Amp, Pha = [], []
		# for j in range(y_count):
		# 	I = [selectedata[gotocdata([x, int(session['isparam']), int(session['iifb']), int(session['ipowa']), 2*j], session['c_cwsweep_structure'])] for x in range(x_count)]
		# 	Q = [selectedata[gotocdata([x, int(session['isparam']), int(session['iifb']), int(session['ipowa']), 2*j+1], session['c_cwsweep_structure'])] for x in range(x_count)]
		# 	amp, pha = [], []
		# 	for i,q in zip(I,Q):
		# 		a,p = IQAP(i,q)
		# 		amp.append(a); pha.append(p)
		# 	Amp += [amp]; Pha += [pha]

		print("x is of length %s and of type %s" %(len(x),type(x)))
		print("y is of length %s and of type %s" %(len(y),type(y)))
		
		Amp = output['rA']
		print("Amp of shape %s" %str(array(Amp).shape))
		ZZ = Amp
		
	elif ipowa == "x" and ifreq == "y":
		print("X: Power, Y: Frequency")
		xtitle, ytitle = "<b>Power(V)</b>", "<b>frequency(GHz)</b>"
		x, y = waveform(M_cwsweep[session['user_name']].corder['Power']).data[0:session['c_cwsweep_address'][3]+1], waveform(M_cwsweep[session['user_name']].corder['Frequency']).data
		x_count, y_count = session['c_cwsweep_address'][3]+1, waveform(M_cwsweep[session['user_name']].corder['Frequency']).count

		stage, prev = clocker(0)
		CMD = ["python", "-c", "from pyqum.directive import multiprocessor as mp; print(mp.worker_cwsweep(%s,%s,%s,%s))"%(y_count,x_count,'"freq"','"powa"')]
		with Popen(CMD, stdout=PIPE, shell=True) as proc:
			output = json.loads(proc.stdout.read().decode("utf-8").replace("\'", "\""))
			try: os.kill(os.getppid(), signal.SIGTERM) # terminate parent process
			except: pass
		stage, prev = clocker(stage, prev) # Marking time

		print("x is of length %s and of type %s" %(len(x),type(x)))
		print("y is of length %s and of type %s" %(len(y),type(y)))
		
		Amp = output['rA']
		print("Amp of shape %s" %str(array(Amp).shape))
		ZZ = Amp

	elif session['iifb'] == "x":
		pass
	
	# x = list(range(len(x))) # for repetitive data
	return jsonify(x=x, y=y, ZZ=ZZ, xtitle=xtitle, ytitle=ytitle)







print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this



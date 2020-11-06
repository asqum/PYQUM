# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name

from importlib import import_module as im
from flask import Flask, request, render_template, Response, redirect, Blueprint, jsonify, session, send_from_directory, abort, g
from pyqum.instrument.logger import address, get_status, set_status, status_code, output_code, clocker

# Error handling
from contextlib import suppress

# Scientific
from scipy import constants as cnst
from si_prefix import si_format, si_parse
from numpy import cos, sin, pi, polyfit, poly1d, array, roots, isreal, sqrt, mean, power, linspace, float64

# Load instruments
from pyqum import get_db
from pyqum.instrument.modular import KMAWG, ALZDG # open native Agilent M933x -> Initiate VSA -> Initiate AWG (Success!!!)
from pyqum.instrument.benchtop import DSO, PNA, YOKO, KEIT, TKAWG
from pyqum.instrument.dilution import bluefors
from pyqum.instrument.serial import DC
from pyqum.instrument.toolbox import match, waveform, pauselog
from pyqum.instrument.analyzer import IQAParray

encryp = 'ghhgjadz'
bp = Blueprint(myname, __name__, url_prefix='/mach')

# Main
@bp.route('/')
def show():
	# Filter out Stranger:
	with suppress(KeyError):
		print(Fore.LIGHTBLUE_EX + "USER " + Fore.YELLOW + "%s [%s] from %s "%(session['user_name'], session['user_id'], request.remote_addr) + Fore.LIGHTBLUE_EX + "is trying to access MACHINE" )
		# Check User's Clearances:
		if not g.user['instrument']:
			print(Fore.RED + "Please check %s's Clearances for instrument!"%session['user_name'])
			abort(404)
		else: print(Fore.LIGHTBLUE_EX + "USER " + Fore.YELLOW + "%s [%s] "%(session['user_name'], session['user_id']) + Fore.LIGHTBLUE_EX + "has entered MACHINE" )
		return render_template("blog/machn/machine.html")
	return("<h3>WHO ARE YOU?</h3><h3>Please F**k*ng Login!</h3><h3>Courtesy from <a href='http://qum.phys.sinica.edu.tw:5300/auth/login'>HoDoR</a></h3>")

# region: ALL
@bp.route('/all', methods=['POST', 'GET'])
def all(): 
	# Test Bed # All Task # Great Work
	current_usr = session['user_name']
	return render_template("blog/machn/all.html", current_usr=current_usr)
@bp.route('/all/mxc', methods=['GET'])
def allmxc():
	dr = bluefors()
	dr.selectday(-1)

	# PENDING: use other route to display all BDR status, maybe in BDR pages itself
	# Logging Latest Key-Readings for ALL
	# latestbdr = {}
	# for i in range(6):
	# 	latestbdr.update({"P%s"%(i+1):dr.pressurelog(i+1)[1][-1]})
	# for i in [1,2,5,6,7]:
	# 	latestbdr.update({"T%s"%(i):dr.temperaturelog(i)[1][-1]})
	# for i in range(21):
	# 	latestbdr.update({"V%s"%(i+1):dr.channellog('v%s'%(i+1))[1][-1]})
	# latestbdr.update({"Pulse-Tube":dr.channellog("pulsetube")[1][-1]})
	# latestbdr.update({"Flow":dr.flowmeterlog()[1][-1]})
	# set_status("BDR", latestbdr)
	# log = pauselog() #disable logging (NOT applicable on Apache)

	return jsonify(mxcmk=dr.temperaturelog(6)[1][-1]*1000)
# endregion

# region: SG (user-specific)
@bp.route('/sg', methods=['GET'])
def sg(): 
	global sgbench, SG
	try: print(Fore.GREEN + "Connected SG: %s" %sgbench.keys())
	except: sgbench, SG = {}, {}
	return render_template("blog/machn/sg.html")
@bp.route('/sg/log', methods=['GET'])
def sglog():
	log = get_status(request.args.get('sgname').split('-')[0], request.args.get('sgname').split('-')[1])
	return jsonify(log=log)
@bp.route('/sg/connect', methods=['GET'])
def sgconnect():
	sgname = request.args.get('sgname')
	sgtag = '%s:%s' %(sgname,session['user_name'])
	sgtype, sglabel, sguser = sgtag.split('-')[0], sgtag.split('-')[1].split(':')[0], sgtag.split('-')[1].split(':')[1]
	linkedsg = ['%s-%s'%(x.split('-')[0],x.split('-')[1].split(':')[0]) for x in sgbench.keys()]
	if sgname not in linkedsg:
		'''get in if not currently initiated'''
		try:
			SG[sgtype] = im("pyqum.instrument.benchtop.%s" %sgtype)
			sgbench[sgtag] = SG[sgtype].Initiate(sglabel)
			message = "%s is successfully initiated by %s" %(sgname,sguser)
			status = "connected"
		except:
			message = "Please check if %s's connection configuration is OK or is it being used!" %(sgname)
			status = 'error'
	else:
		# Check who is currently using the instrument:
		db = get_db()
		instr_user = db.execute('SELECT u.username FROM user u JOIN machine m ON m.user_id = u.id WHERE m.codename = ?', ('%s_%s'%(sgtype,sglabel),)).fetchone()[0]
		message = "%s is being connected to %s" %(sgname,instr_user)
		# Connecting or Waiting?
		if instr_user == session['user_name']: status = 'connected'
		else: status = 'waiting'
	return jsonify(message=message,status=status)
@bp.route('/sg/closet', methods=['GET'])
def sgcloset():
	sgtag, sgtype = '%s:%s' %(request.args.get('sgname'),session['user_name']), request.args.get('sgtype')
	try: status = SG[sgtype].close(sgbench[sgtag], sgtag.split('-')[1].split(':')[0])
	except: 
		status = "Connection lost"
		pass
	del sgbench[sgtag]
	return jsonify(message=status)
@bp.route('/sg/set/freq', methods=['GET'])
def sgsetfreq():
	sgtag, sgtype = '%s:%s' %(request.args.get('sgname'),session['user_name']), request.args.get('sgtype')
	freq = request.args.get('freq')
	frequnit = request.args.get('frequnit')
	stat = SG[sgtype].frequency(sgbench[sgtag], action=['Set', freq + frequnit])
	message = 'frequency: %s <%s>' %(stat[1], stat[0])
	return jsonify(message=message) #message will go to debug log
@bp.route('/sg/set/powa', methods=['GET'])
def sgsetpowa():
	sgtag, sgtype = '%s:%s' %(request.args.get('sgname'),session['user_name']), request.args.get('sgtype')
	powa = request.args.get('powa')
	powaunit = request.args.get('powaunit')
	stat = SG[sgtype].power(sgbench[sgtag], action=['Set', powa + powaunit])
	message = 'power: %s <%s>' %(stat[1], stat[0])
	return jsonify(message=message) #message will go to debug log
@bp.route('/sg/set/oupt', methods=['GET'])
def sgsetoupt():
	sgtag, sgtype = '%s:%s' %(request.args.get('sgname'),session['user_name']), request.args.get('sgtype')
	oupt = request.args.get('oupt')
	stat = SG[sgtype].rfoutput(sgbench[sgtag], action=['Set',int(oupt)])
	message = 'RF output: %s <%s>' %(stat[1], stat[0])
	return jsonify(message=message) #message will go to debug log
@bp.route('/sg/get', methods=['GET'])
def sgget():
	sgtag, sgtype = '%s:%s' %(request.args.get('sgname'),session['user_name']), request.args.get('sgtype')
	message = {}
	try:
		message['frequency'] = si_format(float(SG[sgtype].frequency(sgbench[sgtag])[1]['CW']),precision=3) + "Hz" # frequency
		message['power'] = si_format(float(SG[sgtype].power(sgbench[sgtag])[1]['AMPLITUDE']),precision=1) + "dBm" # power
		message['rfoutput'] = int(SG[sgtype].rfoutput(sgbench[sgtag])[1]['STATE']) # rf output
	except:
		message = dict(status='%s is not connected' %sgtype)
	return jsonify(message=message)
# endregion

# region: TKAWG (user-specific)
@bp.route('/tkawg', methods=['GET'])
def tkawg(): 
	global tkawgbench
	try: print(Fore.GREEN + "\nConnected TKAWG: %s" %tkawgbench.keys())
	except: 
		print(Fore.BLUE + "\nTKAWG status log not yet initialized")
		tkawgbench = {}
	return render_template("blog/machn/tkawg.html")
@bp.route('/tkawg/log', methods=['GET'])
def tkawglog():
	tkawglabel = request.args.get('tkawglabel')
	log = get_status(tkawglabel.split('-')[0], tkawglabel.split('-')[1])
	return jsonify(log=log)
@bp.route('/tkawg/connect', methods=['GET'])
def tkawgconnect():
	tkawglabel = request.args.get('tkawglabel')
	tkawgtag = '%s:%s' %(tkawglabel,session['user_name'])
	tkawgnum, tkawguser = tkawglabel.split('-')[1], tkawgtag.split(':')[1]
	linkedtkawg = [x.split(':')[0] for x in tkawgbench.keys()]
	if tkawglabel not in linkedtkawg:
		try:
			tkawgbench[tkawgtag] = TKAWG.Initiate(tkawgnum)
			message = "%s is successfully initiated by %s" %(tkawglabel,tkawguser)
			status = "connected"
		except:
			message = "Please check if %s's connection configuration is OK or is it being used by non-user!" %(tkawglabel)
			status = 'error'
	else:
		# Check who is currently using the board:
		db = get_db()
		instr_user = db.execute('SELECT u.username FROM user u JOIN machine m ON m.user_id = u.id WHERE m.codename = ?', (tkawglabel.replace('-','_'),)).fetchone()[0]
		message = "%s is being connected to %s" %(tkawglabel,instr_user)
		# Connecting or Waiting?
		if instr_user == session['user_name']: status = 'connected'
		else: status = 'waiting'
	return jsonify(message=message,status=status)
@bp.route('/tkawg/closet', methods=['GET'])
def tkawgcloset():
	tkawglabel = request.args.get('tkawglabel')
	tkawgtag = '%s:%s' %(tkawglabel,session['user_name'])
	status = TKAWG.close(tkawgbench[tkawgtag], tkawglabel.split('-')[1])
	del tkawgbench[tkawgtag]
	return jsonify(message=status)
@bp.route('/tkawg/testing', methods=['GET'])
def tkawgtesting():
	tkawglabel = request.args.get('tkawglabel')
	tkawgtag = '%s:%s' %(tkawglabel,session['user_name'])
	status = TKAWG.test(tkawgbench[tkawgtag])
	return jsonify(message=status)
@bp.route('/tkawg/alloff', methods=['GET'])
def tkawgalloff():
	tkawglabel = request.args.get('tkawglabel')
	tkawgtag = '%s:%s' %(tkawglabel,session['user_name'])
	status = TKAWG.alloff(tkawgbench[tkawgtag], action=['Set',1])
	return jsonify(message=status)
@bp.route('/tkawg/clearall', methods=['GET'])
def tkawgclearall():
	tkawglabel = request.args.get('tkawglabel')
	tkawgtag = '%s:%s' %(tkawglabel,session['user_name'])
	status = TKAWG.clear_waveform(tkawgbench[tkawgtag], 'all')
	return jsonify(message=status)
@bp.route('/tkawg/set/clockfreq', methods=['GET'])
def tkawgsetclockfreq():
	tkawglabel = request.args.get('tkawglabel')
	tkawgtag = '%s:%s' %(tkawglabel,session['user_name'])
	clockfreq = request.args.get('clockfreq')
	clockfrequnit = request.args.get('clockfrequnit')[0]
	stat = TKAWG.clock(tkawgbench[tkawgtag], action=['Set', 'EFIXed', si_parse(clockfreq + clockfrequnit)])
	message = 'frequency: %s <%s>' %(stat[1], stat[0])
	return jsonify(message=message)
@bp.route('/tkawg/get/channels', methods=['GET'])
def tkawggetchannels():
	tkawglabel = request.args.get('tkawglabel')
	tkawgtag = '%s:%s' %(tkawglabel,session['user_name'])
	Channel = request.args.get('Channel')
	level = TKAWG.sourcelevel(tkawgbench[tkawgtag], Channel)[1]
	message = {}
	message['source-amplitude'], message['source-offset'] = si_format(float(level['AMPLITUDE']), precision=3) + "V", si_format(float(level['OFFSET']), precision=3) + "V"
	return jsonify(message=message)
@bp.route('/tkawg/get', methods=['GET'])
def tkawgget():
	tkawglabel = request.args.get('tkawglabel')
	tkawgtag = '%s:%s' %(tkawglabel,session['user_name'])
	message = {}
	try:
		message['clockfreq'] = si_format(float(TKAWG.clock(tkawgbench[tkawgtag])[1]['SRATe']),precision=3) + "S/s" # clock-frequency
		message['model'] = TKAWG.model(tkawgbench[tkawgtag])[1]['IDN']
	except:
		message = dict(status='%s is not connected or busy or error' %tkawglabel)
	print("message: %s" %message)
	return jsonify(message=message)
# endregion

# region: ALZDG (user-specific)
@bp.route('/alzdg', methods=['GET'])
def alzdg(): 
	global alzdgboard
	try: print(Fore.GREEN + "\nConnected ALZDG: %s" %alzdgboard.keys())
	except: 
		print(Fore.BLUE + "\nALZDG status log not yet initialized")
		alzdgboard = {}
	return render_template("blog/machn/alzdg.html")
@bp.route('/alzdg/log', methods=['GET'])
def alzdglog():
	log = get_status(request.args.get('alzdglabel').split('-')[0], request.args.get('alzdglabel').split('-')[1])
	return jsonify(log=log)
@bp.route('/alzdg/connect', methods=['GET'])
def alzdgconnect():
	alzdglabel = request.args.get('alzdglabel')
	alzdgtag = '%s:%s' %(alzdglabel,session['user_name'])
	alzdgnum, alzdguser = alzdglabel.split('-')[1], alzdgtag.split(':')[1]
	linkedalzdg = [x.split(':')[0] for x in alzdgboard.keys()]
	if alzdglabel not in linkedalzdg:
		try:
			alzdgboard[alzdgtag] = ALZDG.Initiate(alzdgnum)
			message = "%s is successfully initiated by %s" %(alzdglabel,alzdguser)
			status = "connected"
		except:
			message = "Please check if %s's connection configuration is OK or is it being used by non-user!" %(alzdglabel)
			status = 'error'
	else: 
		# Check who is currently using the board:
		db = get_db()
		instr_user = db.execute('SELECT u.username FROM user u JOIN machine m ON m.user_id = u.id WHERE m.codename = ?', (alzdglabel.replace('-','_'),)).fetchone()[0]
		message = "%s is being connected to %s" %(alzdglabel,instr_user)
		# Connecting or Waiting?
		if instr_user == session['user_name']: status = 'connected'
		else: status = 'waiting'
	return jsonify(message=message,status=status)
@bp.route('/alzdg/configureboard', methods=['GET'])
def alzdgconfigureboard():
	alzdglabel = request.args.get('alzdglabel')
	alzdgtag = '%s:%s' %(alzdglabel,session['user_name'])
	trigdelay, trigdelayunit = request.args.get('trigdelay'), request.args.get('trigdelayunit')[0]
	status = ALZDG.ConfigureBoard_NPT(alzdgboard[alzdgtag], triggerDelay_sec=si_parse(trigdelay + trigdelayunit))
	return jsonify(message=status)
@bp.route('/alzdg/acquiredata', methods=['GET'])
def alzdgacquiredata():
	alzdglabel = request.args.get('alzdglabel')
	alzdgtag = '%s:%s' %(alzdglabel,session['user_name'])
	recordtime, recordtimeunit = request.args.get('recordtime'), request.args.get('recordtimeunit')[0]
	recordsum = int(request.args.get('recordsum'))
	[DATA, transferTime_sec, recordsPerBuff, buffersPerAcq] = ALZDG.AcquireData_NPT(alzdgboard[alzdgtag], recordtime=si_parse(recordtime + recordtimeunit), recordsum=recordsum)
	global I_data, Q_data, t_data
	I_data, Q_data, t_data = {}, {}, {}
	I_data[alzdgtag] = DATA[:,:,0]
	Q_data[alzdgtag] = DATA[:,:,1]
	t_data[alzdgtag] = list(1e-9*linspace(1, len(DATA[0,:,0]), len(DATA[0,:,0])))
	# print(Fore.GREEN + "Data-type: %s" %DATA.dtype) # numpy default: float64 (But we adapted to float32 for Quadro-GPU sake!)
	return jsonify(datalen=len(DATA[0,:,0]), transferTime_sec=transferTime_sec, recordsPerBuff=recordsPerBuff, buffersPerAcq=buffersPerAcq)
@bp.route('/alzdg/playdata', methods=['GET'])
def alzdgplaydata():
	alzdglabel = request.args.get('alzdglabel')
	alzdgtag = '%s:%s' %(alzdglabel,session['user_name'])
	average = int(request.args.get('average'))
	integrate = int(request.args.get('integrate'))
	tracenum = int(request.args.get('tracenum'))
	# data post-processing:
	if average: # PENDING: verify fast CUDA average?
		trace_I = mean(I_data[alzdgtag][:,:], 0)
		trace_Q = mean(Q_data[alzdgtag][:,:], 0)
	else:
		trace_I = I_data[alzdgtag][tracenum,:]
		trace_Q = Q_data[alzdgtag][tracenum,:]
	trace_A = sqrt(power(trace_I, 2) + power(trace_Q, 2))
	t = t_data[alzdgtag]
	# print(Fore.CYAN + "plotting trace #%s"%tracenum)
	return jsonify(I=list(trace_I.astype(float64)), Q=list(trace_Q.astype(float64)), A=list(trace_A.astype(float64)), t=t) # JSON only supports float64 conversion (to str-list eventually)
@bp.route('/alzdg/closet', methods=['GET'])
def alzdgcloset():
	alzdglabel = request.args.get('alzdglabel')
	alzdgtag = '%s:%s' %(alzdglabel,session['user_name'])
	status = ALZDG.close(alzdglabel.split('-')[1])
	del alzdgboard[alzdgtag]
	return jsonify(message=status)
@bp.route('/alzdg/testing', methods=['GET'])
def alzdgtesting():
	alzdglabel = request.args.get('alzdglabel')
	alzdgtag = '%s:%s' %(alzdglabel,session['user_name'])
	status = ALZDG.test(alzdgboard[alzdgtag])
	return jsonify(message=status)
@bp.route('/alzdg/get', methods=['GET'])
def alzdgget():
	alzdglabel = request.args.get('alzdglabel')
	alzdgtag = '%s:%s' %(alzdglabel,session['user_name'])
	message = {}
	try:
		message['model'] = ALZDG.model(alzdgboard[alzdgtag])
	except:
		message = dict(status='%s is not connected or busy or error' %alzdglabel)
	print("message: %s" %message)
	return jsonify(message=message)
# endregion

# region: NA (user-specific)
@bp.route('/na', methods=['GET'])
def na(): 
	global nabench, NA
	try: print(Fore.GREEN + "Connected NA: %s" %nabench.keys())
	except: nabench, NA = {}, {}
	return render_template("blog/machn/na.html")
@bp.route('/na/log', methods=['GET'])
def nalog():
	log = get_status(request.args.get('natype'))
	return jsonify(log=log)
@bp.route('/na/connect', methods=['GET'])
def naconnect():
	naname = request.args.get('naname')
	natag = '%s:%s' %(naname,session['user_name'])
	natype, nalabel, nauser = natag.split('-')[0], natag.split('-')[1].split(':')[0], natag.split('-')[1].split(':')[1]
	linkedna = ['%s-%s'%(x.split('-')[0],x.split('-')[1].split(':')[0]) for x in nabench.keys()]
	if naname not in linkedna:
		'''get in if not currently initiated'''
		try:
			NA[natype] = im("pyqum.instrument.benchtop.%s" %natype)
			nabench[natag] = NA[natype].Initiate(which=nalabel)
			message = "%s is successfully initiated by %s" %(naname,nauser)
			status = "connected"
		except:
			message = "Please check if %s's connection configuration is OK or is it being used!" %(naname)
			status = 'error'
	else:
		# Check who is currently using the instrument:
		db = get_db()
		instr_user = db.execute('SELECT u.username FROM user u JOIN machine m ON m.user_id = u.id WHERE m.codename = ?', ('%s_%s'%(natype,nalabel),)).fetchone()[0]
		message = "%s is being connected to %s" %(naname,instr_user)
		# Connecting or Waiting?
		if instr_user == session['user_name']: status = 'connected'
		else: status = 'waiting'
	return jsonify(message=message,status=status)
@bp.route('/na/closet', methods=['GET'])
def nacloset():
	natag, natype = '%s:%s' %(request.args.get('naname'),session['user_name']), request.args.get('natype')
	try: status = NA[natype].close(nabench[natag], natag.split('-')[1].split(':')[0])
	except: 
		status = "Connection lost"
		pass
	del nabench[natag]
	return jsonify(message=status)
@bp.route('/na/set/freqrange', methods=['GET'])
def nasetfreqrange():
	natag, natype = '%s:%s' %(request.args.get('naname'),session['user_name']), request.args.get('natype')
	freqrange = waveform(request.args.get('freqrange'))
	frequnit = request.args.get('frequnit').replace("Hz","")
	NA[natype].sweep(nabench[natag], action=['Set', 'ON', freqrange.count])
	fstart, fstop = si_parse(str(freqrange.data[0])+frequnit), si_parse(str(freqrange.data[-1])+frequnit)
	NA[natype].sweep(nabench[natag], action=['Set', 'ON', freqrange.count])
	NA[natype].linfreq(nabench[natag], action=['Set', fstart, fstop])
	message = 'frequency: %s to %s' %(fstart, fstop)
	return jsonify(message=message)
@bp.route('/na/set/powa', methods=['GET'])
def nasetpowa():
	natag, natype = '%s:%s' %(request.args.get('naname'),session['user_name']), request.args.get('natype')
	powa = request.args.get('powa')
	stat = NA[natype].power(nabench[natag], action=['Set', powa])
	message = 'power: %s <%s>' %(stat[1], stat[0])
	return jsonify(message=message)
@bp.route('/na/set/ifb', methods=['GET'])
def nasetifb():
	natag, natype = '%s:%s' %(request.args.get('naname'),session['user_name']), request.args.get('natype')
	ifb = request.args.get('ifb')
	ifbunit = request.args.get('ifbunit').replace("Hz","")
	stat = NA[natype].ifbw(nabench[natag], action=['Set', si_parse(ifb + ifbunit)])
	message = 'ifb: %s <%s>' %(stat[1], stat[0])
	return jsonify(message=message)
@bp.route('/na/set/autoscale', methods=['GET'])
def nasetautoscale():
	natag, natype = '%s:%s' %(request.args.get('naname'),session['user_name']), request.args.get('natype')
	status = NA[natype].autoscal(nabench[natag])
	return jsonify(message=status)
@bp.route('/na/set/scanning', methods=['GET'])
def nasetscanning():
	natag, natype = '%s:%s' %(request.args.get('naname'),session['user_name']), request.args.get('natype')
	scan = int(request.args.get('scan'))
	NA[natype].rfports(nabench[natag], action=['Set', scan])
	status = NA[natype].scanning(nabench[natag], scan)
	return jsonify(message=status)
@bp.route('/na/set/sweep', methods=['GET'])
def nasetsweep():
	natag, natype = '%s:%s' %(request.args.get('naname'),session['user_name']), request.args.get('natype')
	s21, s11 = int(request.args.get('s21')), int(request.args.get('s11'))
	s22, s12 = int(request.args.get('s22')), int(request.args.get('s12'))
	s43, s33 = int(request.args.get('s43')), int(request.args.get('s33'))
	s44, s34 = int(request.args.get('s44')), int(request.args.get('s34'))
	mparam = ['S11']*s11 + ['S22']*s22 + ['S21']*s21 + ['S12']*s12 + ['S33']*s33 + ['S44']*s44 + ['S43']*s43 + ['S34']*s34
	mwindow = 'D1_2_3_4'[:len(mparam)*2]
	mreturn = NA[natype].setrace(nabench[natag], Mparam=mparam, window=mwindow)
	print("sweeping %s"%mreturn)
	NA[natype].rfports(nabench[natag], action=['Set', 'ON'])
	stat = NA[natype].measure(nabench[natag])
	swptime = NA[natype].sweep(nabench[natag])[1]['TIME']
	NA[natype].autoscal(nabench[natag])
	NA[natype].rfports(nabench[natag], action=['Set', 'OFF'])
	return jsonify(sweep_complete=bool(stat), swptime=swptime)
@bp.route('/na/get', methods=['GET'])
def naget():
	natag, natype = '%s:%s' %(request.args.get('naname'),session['user_name']), request.args.get('natype')
	message = {}
	try:
		start_val, start_unit = si_format(float(NA[natype].linfreq(nabench[natag])[1]['START']),precision=1).split(" ")
		stop_val, stop_unit = si_format(float(NA[natype].linfreq(nabench[natag])[1]['STOP']),precision=1).split(" ")
		stop_conversion = si_parse("1%s"%stop_unit) / si_parse("1%s"%start_unit) # equalizing both unit-range:
		message['start-frequency'] = "%s %sHz" %(start_val,start_unit) # start-frequency
		message['stop-frequency'] = "%s %sHz" %(float(stop_val)*stop_conversion,start_unit) # stop-frequency
		message['step-points'] = int(NA[natype].sweep(nabench[natag])[1]['POINTS']) - 1 # step-points in waveform
		message['power'] = "%.1f dBm" %float(NA[natype].power(nabench[natag])[1]['LEVEL']) # power (fixed unit)
		message['ifb'] = si_format(float(NA[natype].ifbw(nabench[natag])[1]['BANDWIDTH']),precision=0) + "Hz" # ifb (adjusted by si_prefix)
		message['s21'], message['s11'] = int('S21' in NA[natype].getrace(nabench[natag])), int('S11' in NA[natype].getrace(nabench[natag]))
		message['s12'], message['s22'] = int('S12' in NA[natype].getrace(nabench[natag])), int('S22' in NA[natype].getrace(nabench[natag]))
		message['s43'], message['s33'] = int('S43' in NA[natype].getrace(nabench[natag])), int('S33' in NA[natype].getrace(nabench[natag]))
		message['s34'], message['s44'] = int('S34' in NA[natype].getrace(nabench[natag])), int('S44' in NA[natype].getrace(nabench[natag]))
	except:
		# raise
		message = dict(status='%s is not connected' %natype)
	return jsonify(message=message)
# endregion

# region: BDR
@bp.route('/bdr')
def bdr():
	# monitoring traffic:
	print("User %s is visiting BDR using IP: %s\n" %(session['user_name'], request.remote_addr))
	return render_template("blog/machn/bdr.html")
@bp.route('/bdr/init', methods=['GET'])
def bdrinit():
	global b
	b = bluefors()
	return jsonify(Days=b.Days)
@bp.route('/bdr/history', methods=['GET'])
def bdrhistory():
	global b, bdrlogs
	wday = int(request.args.get('wday'))
	P_Ch = int(request.args.get('P_Ch'))
	T_Ch = int(request.args.get('T_Ch'))
	P_Ch2 = int(request.args.get('P_Ch2'))
	T_Ch2 = int(request.args.get('T_Ch2'))
	OptionS = request.args.get('OptS')
	OptionV = request.args.get('OptV')

	b = bluefors()
	b.selectday(wday)

	tp, P, P_stat = b.pressurelog(P_Ch)
	tt, T = b.temperaturelog(T_Ch)
	tp2, P2, P_stat2 = b.pressurelog(P_Ch2)
	tt2, T2 = b.temperaturelog(T_Ch2)

	if OptionS == 'flow': tos, Opts = b.flowmeterlog()
	else: tos, Opts = b.statuslog(OptionS)
	tov, Optv = b.channellog(OptionV)

	bdrlogs = dict(bdr_P=P,bdr_T=T) # for forecast
	# print("T: %s"%bdrlogs['bdr_%s'%('T')][-15:])

	log = pauselog() #disable logging (NOT applicable on Apache)
	return jsonify(log=str(log), tp=tp, P=P, P_stat=P_stat, tt=tt, T=T, tp2=tp2, P2=P2, P_stat2=P_stat2, tt2=tt2, T2=T2, tos=tos, Opts=Opts, tov=tov, Optv=Optv)
@bp.route('/bdr/history/forecast', methods=['GET'])
def bdrhistoryforecast():
	# logging interval: 1 min
	# original unit: mbar, K
	target = float(request.args.get('target'))
	predicting = str(request.args.get('predicting'))
	# Data:
	y = bdrlogs['bdr_%s'%predicting]
	sampling = 37
	coeff = polyfit(array(range(sampling)), array(y[-sampling:]), 1) # 1: linear fit
	coeff[-1] -= target
	eta_time = roots(coeff)
	eta_time = ["%.3f"%(x.real/60) for x in eta_time if isreal(x)] # convert to hours
	# fore = poly1d(coeff)
	
	return jsonify(eta_time=list(eta_time))
# endregion

# region: DC
@bp.route('/dc', methods=['GET'])
def dc():
	print("loading dc.html")
	return render_template("blog/machn/dc.html")
# YOKOGAWA 7651
@bp.route('/dc/yokogawa', methods=['GET'])
def dcyokogawa():
	global yokog
	yokostat = request.args.get('yokostat')
	ykwhich = int(request.args.get('ykwhich'))
	print(Fore.GREEN + "Connecting to YoKoGaWa-%s" %ykwhich)
	ykvaunit = bool(int(request.args.get('ykvaunit')))
	print(Fore.YELLOW + "Current mode: %s" %ykvaunit)
	if yokostat == 'true':
		yokog = YOKO.Initiate(current=ykvaunit, which=ykwhich)
		prev = YOKO.previous(yokog)
	elif yokostat == 'false':
		prev = YOKO.previous(yokog)
		YOKO.close(yokog, True, which=ykwhich)
	return jsonify(prev=prev)
@bp.route('/dc/yokogawa/vwave', methods=['GET'])
def dc_yokogawa_vwave():
	global yokog
	YOKO.output(yokog, 1)
	vwave = request.args.get('vwave') #V-waveform command
	pwidth = float(request.args.get("pwidth")) #ms
	swprate = float(request.args.get("swprate")) #V/s
	stat = YOKO.sweep(yokog, vwave, pulsewidth=pwidth*1e-3, sweeprate=swprate)
	return jsonify(SweepTime=stat[1])
@bp.route('/dc/yokogawa/vpulse', methods=['GET'])
def dc_yokogawa_vpulse():
	global yokog
	YOKO.output(yokog, 1)
	vset = float(request.args.get('vset'))
	pwidth = float(request.args.get("pwidth"))
	stat = YOKO.sweep(yokog, "%sto0*1"%vset, pulsewidth=pwidth*1e-3, sweeprate=abs(vset)*60)
	return jsonify(SweepTime=stat[1])
@bp.route('/dc/yokogawa/onoff', methods=['GET'])
def dc_yokogawa_onoff():
	global yokog
	YOKO.output(yokog, 1)
	YOKO.output(yokog, 0)
	return jsonify()
# KEITHLEY 2400
@bp.route('/dc/keithley', methods=['GET'])
def dckeithley():
	keitstat = request.args.get('keitstat')
	if keitstat == 'true':
		global keith
		keith = KEIT.Initiate()
	elif keitstat == 'false':
		KEIT.close(keith, True)
	return jsonify()
@bp.route('/dc/keithley/vpulse', methods=['GET'])
def dc_keithley_vpulse():
	vset = float(request.args.get('vset'))
	pwidth = float(request.args.get("pwidth"))
	return_width, VI_List = KEIT.single_pulse(keith, pwidth*1e-3, vset)
	t = [x*return_width for x in range(len(VI_List)//2)]
	print("t: %s" %t)
	V, I = VI_List[0::2], VI_List[1::2]
	return jsonify(return_width=return_width, V=V, I=I, t=t)
# endregion


# Download File:
@bp.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
	uploads = "C:/Users/ASQUM/HODOR/CONFIG/PORTAL"
	print(Fore.GREEN + "User %s is downloading %s" %(session['user_name'], filename))
	return send_from_directory(directory=uploads, filename=filename)


print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this



# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
from os.path import getmtime
myname = bs(__file__).split('.')[0] # This py-script's name

import requests, json
from flask import Flask, request, render_template, Response, redirect, Blueprint, jsonify, stream_with_context, g, session, abort
from werkzeug.security import check_password_hash
from numpy import array, unwrap, mean, trunc, sqrt, zeros, ones, shape
from time import sleep, strptime, mktime 
from datetime import timedelta, datetime

from pyqum import get_db
from pyqum.instrument.logger import address, get_status, set_status, status_code, output_code, set_csv, clocker
from pyqum.instrument.toolbox import cdatasearch, gotocdata, waveform
from pyqum.instrument.analyzer import IQAP, UnwraPhase
from pyqum.directive.characterize import F_Response, CW_Sweep, SQE_Pulse

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
    # Security implementation:
    if not g.user['instrument'] or not g.user['measurement']:
        abort(404)
    return render_template("blog/msson/mission.html", encryp=encryp)

# ALL
@bp.route('/all', methods=['GET'])
def all(): 
    # Test Bed # All Task # Great Work
    return render_template("blog/msson/all.html")
@bp.route('/all/measurequm', methods=['GET']) # PENDING: horizontal tabs for different Quantum Universal Machines in the future
def all_measurequm():
    print("Queue: %s" %g.qumlist)
    return jsonify(qumlist=g.qumlist, loginuser=session['user_name'])
@bp.route('/all/measurequm/in', methods=['GET']) # PENDING: horizontal tabs for different Quantum Universal Machines in the future
def all_measurequm_in():
    try:
        db = get_db()
        db.execute('INSERT INTO qum (people_id) VALUES (?)', (g.user['id'],))
        db.commit()
        message = "Queued-in successfully"
    except:
        message = "You may have queued-in already"
    return jsonify(message=message)
@bp.route('/all/measurequm/out', methods=['GET']) # PENDING: horizontal tabs for different Quantum Universal Machines in the future
def all_measurequm_out():
    try:
        db = get_db()
        db.execute('DELETE FROM qum WHERE people_id = ?', (g.user['id'],))
        db.commit()
        message = "Queued-out successfully"
    except:
        message = "You may have queued-out already"
    return jsonify(message=message)

# CHAR:
@bp.route('/char', methods=['GET'])
def char(): 
    print('User %s is allowed to run measurement: %s'%(g.user['username'],session['run_clearance']))
    samplename = get_status("MSSN")[session['user_name']]['sample']
    return render_template("blog/msson/char.html", samplename=samplename, people=session['people'])

# CHAR -> 1. F-Response ============================================================================================================================================
@bp.route('/char/fresp', methods=['GET'])
def char_fresp(): 
    return render_template("blog/msson/char/fresp.html")
# Initialize and list days specific to task
@bp.route('/char/fresp/init', methods=['GET'])
def char_fresp_init(): 
    run_status = not get_status("F_Response")['pause']
    global M_fresp
    try: print(Fore.GREEN + "Connected F-Resp M-USER(s): %s" %M_fresp.keys())
    except: M_fresp = {}
    # set_status("F_Response", dict(repeat=False))
    M_fresp[session['user_name']] = F_Response(session['people']) # initializing Law Maker -> Executioner
    return jsonify(run_status=run_status, daylist=M_fresp[session['user_name']].daylist, run_permission=session['run_clearance'])
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

# NEW measurement setup
@bp.route('/char/fresp/new', methods=['GET'])
def char_fresp_new():
    # Check user's current queue status:
    if session['run_clearance']:
        set_status("F_Response", dict(pause=False))
        global Run_fresp # need to be removed in the future for security sake
        Run_fresp = {}
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
        Run_fresp['TOKEN'] = F_Response(session['people'], corder=CORDER, comment=comment, tag='', dayindex=wday, testeach=simulate)
    else: all()
    return jsonify(testeach=simulate)
# ETA (Estimated Time of Arrival for the WHOLE measurement)
@bp.route('/char/fresp/eta100', methods=['GET'])
def char_fresp_eta100():
    eta_time_100 = sum([a*b for a,b in zip(Run_fresp['TOKEN'].loopcount, Run_fresp['TOKEN'].loop_dur)])
    print(Fore.RED + "ETA: %s" %str(timedelta(seconds=eta_time_100)))
    eta_time_100 = str(timedelta(seconds=eta_time_100)).split('.')[0]
    return jsonify(eta_time_100=eta_time_100)
# pause the measurement:
@bp.route('/char/fresp/pause', methods=['GET'])
def char_fresp_pause():
    set_status("F_Response", dict(pause=True))
    return jsonify(pause=get_status("F_Response")['pause'])
# toggle between repeat or not
@bp.route('/char/fresp/setrepeat', methods=['GET'])
def char_fresp_setrepeat():
    set_status("F_Response", dict(repeat=bool(int(request.args.get('repeat')))))
    return jsonify(repeat=get_status("F_Response")['repeat'])
@bp.route('/char/fresp/getrepeat', methods=['GET'])
def char_fresp_getrepeat():
    return jsonify(repeat=get_status("F_Response")['repeat'])
# search through logs of data specific to task
@bp.route('/char/fresp/search', methods=['GET'])
def char_fresp_search():
    wday = int(request.args.get('wday'))
    keyword = request.args.get('keyword')
    filelist = M_fresp[session['user_name']].searchcomment(wday, keyword)
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

    # Measurement time:
    filetime = getmtime(M_fresp[session['user_name']].pqfile) # in seconds
    startmeasure = mktime(strptime(M_fresp[session['user_name']].day + " " + M_fresp[session['user_name']].startime(), "%Y-%m-%d(%a) %H:%M")) # made into seconds
    measureacheta = str(timedelta(seconds=(filetime-startmeasure)/data_progress*(trunc(data_progress/100+1)*100-data_progress)))

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

    return jsonify(data_progress=data_progress, measureacheta=measureacheta, corder=M_fresp[session['user_name']].corder, comment=M_fresp[session['user_name']].comment, 
        cfluxbias_data=cfluxbias_data,
        csparam_data=csparam_data, cifb_data=cifb_data, cpowa_data=cpowa_data, cfreq_data=cfreq_data)
# Resume the unfinished measurement
@bp.route('/char/fresp/resume', methods=['GET'])
def char_fresp_resume():
    set_status("F_Response", dict(pause=False))
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

    # selecting data
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
    
    # Preparing data:
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
        xtitle, ytitle = "<b>Flux-Bias(V/A)</b>", "<b>Frequency(GHz)</b>"
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
        Pha = output['rP']
        print("Amp of shape %s" %str(array(Amp).shape))
        ZZA, ZZP = Amp, Pha
        
    elif ipowa == "x" and ifreq == "y":
        print("X: Power, Y: Frequency")
        xtitle, ytitle = "<b>Power(dBm)</b>", "<b>Frequency(GHz)</b>"
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
        Pha = output['rP']
        print("Amp of shape %s" %str(array(Amp).shape))
        ZZA, ZZP = Amp, Pha

    elif iifb == "x":
        pass
    
    # x = list(range(len(x))) # for repetitive data
    return jsonify(x=x, y=y, ZZA=ZZA, ZZP=ZZP, xtitle=xtitle, ytitle=ytitle)

# CHAR -> 2. CW-Sweeping =============================================================================================================================================
@bp.route('/char/cwsweep', methods=['GET'])
def char_cwsweep(): 
    return render_template("blog/msson/char/cwsweep.html")
# Initialize and list days specific to task
@bp.route('/char/cwsweep/init', methods=['GET'])
def char_cwsweep_init():
    global M_cwsweep

    # check currently-connected users:
    try: print(Fore.GREEN + "Connected CW-Sweep M-USER(s): %s" %M_cwsweep.keys())
    except: M_cwsweep = {}

    # check configuration:
    run_status = not get_status("CW_Sweep")['pause'] 
    # set_status("CW_Sweep", dict(repeat=False))
    
    # 'user_name' accessing 'people' data:
    M_cwsweep[session['user_name']] = CW_Sweep(session['people'])
    print(Fore.BLUE + "User %s is looking at %s's data" %(session['user_name'],session['people']))

    return jsonify(run_status=run_status, daylist=M_cwsweep[session['user_name']].daylist, run_permission=session['run_clearance'])
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
    # pending: YOKO switching between V and I source
    # PSG type selection
    return jsonify()

# run NEW measurement:
@bp.route('/char/cwsweep/new', methods=['GET'])
def char_cwsweep_new():
    # Check user's current queue status:
    if session['run_clearance']:
        set_status("CW_Sweep", dict(pause=False))
        global Run_cwsweep # for ETA calculation as well
        Run_cwsweep = {}
        wday = int(request.args.get('wday'))
        print("wday: %s" %wday)
        fluxbias = request.args.get('fluxbias')
        xyfreq = request.args.get('xyfreq')
        xypowa = request.args.get('xypowa')
        sparam = request.args.get('sparam')
        ifb = request.args.get('ifb')
        freq = request.args.get('freq')
        powa = request.args.get('powa')
        comment = request.args.get('comment').replace("\"","")
        simulate = bool(int(request.args.get('simulate')))
        CORDER = {'Flux-Bias':fluxbias, 'XY-Frequency':xyfreq, 'XY-Power':xypowa, 'S-Parameter':sparam, 'IF-Bandwidth':ifb, 'Frequency':freq, 'Power':powa}
        Run_cwsweep['TOKEN'] = CW_Sweep(session['people'], corder=CORDER, comment=comment, tag='', dayindex=wday, testeach=simulate)
    else: all()
    return jsonify(testeach=simulate)
# ETA (Estimated Time of Arrival for the WHOLE measurement)
@bp.route('/char/cwsweep/eta100', methods=['GET'])
def char_cwsweep_eta100():
    eta_time_100 = sum([a*b for a,b in zip(Run_cwsweep['TOKEN'].loopcount, Run_cwsweep['TOKEN'].loop_dur)])
    print(Fore.RED + "ETA: %s" %str(timedelta(seconds=eta_time_100)))
    eta_time_100 = str(timedelta(seconds=eta_time_100)).split('.')[0]
    return jsonify(eta_time_100=eta_time_100)
# pause the measurement:
@bp.route('/char/cwsweep/pause', methods=['GET'])
def char_cwsweep_pause():
    set_status("CW_Sweep", dict(pause=True))
    return jsonify(pause=get_status("CW_Sweep")['pause'])
# toggle between repeat or not
@bp.route('/char/cwsweep/setrepeat', methods=['GET'])
def char_cwsweep_setrepeat():
    set_status("CW_Sweep", dict(repeat=bool(int(request.args.get('repeat')))))
    return jsonify(repeat=get_status("CW_Sweep")['repeat'])
@bp.route('/char/cwsweep/getrepeat', methods=['GET'])
def char_cwsweep_getrepeat():
    return jsonify(repeat=get_status("CW_Sweep")['repeat'])
# search through logs of data specific to task (pending)
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
    data_repeat = data_progress // 100 + int(bool(data_progress % 100))

    # Measurement time:
    filetime = getmtime(M_cwsweep[session['user_name']].pqfile) # in seconds
    startmeasure = mktime(strptime(M_cwsweep[session['user_name']].day + " " + M_cwsweep[session['user_name']].startime(), "%Y-%m-%d(%a) %H:%M")) # made into seconds
    measureacheta = str(timedelta(seconds=(filetime-startmeasure)/data_progress*(trunc(data_progress/100+1)*100-data_progress)))

    # Scale-up optional parameters:
    try: cfluxbias = waveform(M_cwsweep[session['user_name']].corder['Flux-Bias'])
    except(KeyError): cfluxbias = waveform('opt,') # create virtual list for the absence of this in older file
    try: cxyfreq = waveform(M_cwsweep[session['user_name']].corder['XY-Frequency'])
    except(KeyError): cxyfreq = waveform('opt,') # create virtual list for the absence of this in older file
    try: cxypowa = waveform(M_cwsweep[session['user_name']].corder['XY-Power'])
    except(KeyError): cxypowa = waveform('opt,') # create virtual list for the absence of this in older file
    csparam = waveform(M_cwsweep[session['user_name']].corder['S-Parameter'])
    cifb = waveform(M_cwsweep[session['user_name']].corder['IF-Bandwidth'])
    cfreq = waveform(M_cwsweep[session['user_name']].corder['Frequency'])
    cpowa = waveform(M_cwsweep[session['user_name']].corder['Power'])
    cpowa_repeat = cpowa.inner_repeat
    session['c_cwsweep_structure'] = [data_repeat, cfluxbias.count,cxyfreq.count,cxypowa.count,csparam.count,cifb.count,cfreq.count,cpowa.count*cpowa_repeat*M_cwsweep[session['user_name']].datadensity]
    session['c_cwsweep_address'] = cdatasearch(M_cwsweep[session['user_name']].resumepoint-1, session['c_cwsweep_structure'])
    
    # list each parameter range based on data-progress:
    cfluxbias_data = cfluxbias.data[0:session['c_cwsweep_address'][1]+1]
    cxyfreq_data = cxyfreq.data[0:session['c_cwsweep_address'][2]+1]
    cxypowa_data = cxypowa.data[0:session['c_cwsweep_address'][3]+1]
    csparam_data = csparam.data[0:session['c_cwsweep_address'][4]+1]
    cifb_data = cifb.data[0:session['c_cwsweep_address'][5]+1]
    cfreq_data = cfreq.data[0:session['c_cwsweep_address'][6]+1]
    cpowa_data = cpowa.data[0:(session['c_cwsweep_address'][7]+1)//cpowa_repeat//2]  # (to be adjusted ***)
    # print("cpowa_data: %s" %cpowa_data)
    
    return jsonify(data_progress=data_progress, measureacheta=measureacheta, corder=M_cwsweep[session['user_name']].corder, comment=M_cwsweep[session['user_name']].comment, 
        data_repeat=data_repeat, cfluxbias_data=cfluxbias_data, cxyfreq_data=cxyfreq_data, cxypowa_data=cxypowa_data,
        csparam_data=csparam_data, cifb_data=cifb_data, cfreq_data=cfreq_data, cpowa_data=cpowa_data)
# Resume the unfinished measurement
@bp.route('/char/cwsweep/resume', methods=['GET'])
def char_cwsweep_resume():
    set_status("CW_Sweep", dict(pause=False))
    wday = int(request.args.get('wday'))
    wmoment = int(request.args.get('wmoment'))
    fluxbias = request.args.get('fluxbias')
    xyfreq = request.args.get('xyfreq')
    xypowa = request.args.get('xypowa')
    sparam = request.args.get('sparam')
    ifb = request.args.get('ifb')
    freq = request.args.get('freq')
    powa = request.args.get('powa')
    CORDER = {'Flux-Bias':fluxbias, 'XY-Frequency':xyfreq, 'XY-Power':xypowa, 'S-Parameter':sparam, 'IF-Bandwidth':ifb, 'Frequency':freq, 'Power':powa}
    M_cwsweep[session['user_name']].accesstructure()
    CW_Sweep(session['people'], corder=CORDER, dayindex=wday, taskentry=wmoment, resumepoint=M_cwsweep[session['user_name']].resumepoint)
    return jsonify(resumepoint=str(M_cwsweep[session['user_name']].resumepoint), datasize=str(M_cwsweep[session['user_name']].datasize))

@bp.route('/char/cwsweep/trackdata', methods=['GET'])
def char_cwsweep_trackdata():
    ifluxbias = request.args.get('ifluxbias')
    ixyfreq = request.args.get('ixyfreq')
    ixypowa = request.args.get('ixypowa')

    # list data position in file:
    try:
        data_location = {}
        data_location['fluxbias'] = int(gotocdata([session['c_cwsweep_structure'][0]-1, int(ifluxbias), 0, 0, 0, 0, 0, 0], session['c_cwsweep_structure']))
        data_location['xyfreq'] = int(gotocdata([session['c_cwsweep_structure'][0]-1, session['c_cwsweep_structure'][1]-1, int(ixyfreq), 0, 0, 0, 0, 0], session['c_cwsweep_structure']))
        data_location['xypowa'] = int(gotocdata([session['c_cwsweep_structure'][0]-1, session['c_cwsweep_structure'][1]-1, session['c_cwsweep_structure'][0]-1, int(ixypowa), 0, 0, 0, 0], session['c_cwsweep_structure']))
    except(ValueError):
        print(Back.RED + Fore.WHITE + "All parameters must be FIXED!")
        pass

    # print("Data location: %s" %data_location)
    return jsonify(data_location=data_location)
@bp.route('/char/cwsweep/resetdata', methods=['GET'])
def char_cwsweep_resetdata():
    ownerpassword = request.args.get('ownerpassword')
    truncateafter = int(request.args.get('truncateafter'))

    db = get_db()
    people = db.execute(
        'SELECT password FROM user WHERE username = ?', (session['people'],)
    ).fetchone()

    if check_password_hash(people['password'], ownerpassword):
        message = M_cwsweep[session['user_name']].resetdata(truncateafter)
    else:
        message = 'PASSWORD NOT VALID'

    return jsonify(message=message)

# Chart is supposedly shared by all measurements (under construction for multi-purpose)
@bp.route('/char/cwsweep/1ddata', methods=['GET'])
def char_cwsweep_1ddata():
    print(Fore.GREEN + "User %s is plotting 1D-Data" %session['user_name'])
    M_cwsweep[session['user_name']].loadata()
    selectedata = M_cwsweep[session['user_name']].selectedata
    
    # load parameter indexes from json call:
    irepeat = request.args.get('irepeat')
    ifluxbias = request.args.get('ifluxbias')
    ixyfreq = request.args.get('ixyfreq')
    ixypowa = request.args.get('ixypowa')
    isparam = request.args.get('isparam')
    iifb = request.args.get('iifb')
    ifreq = request.args.get('ifreq')
    ipowa = request.args.get('ipowa')

    # pre-transform ipowa:
    xpowa = waveform(M_cwsweep[session['user_name']].corder['Power'])
    ipowa_repeat = xpowa.inner_repeat

    # selecting data:
    if "x" in ifluxbias:
        xtitle = "<b>Flux-Bias(V/A)</b>"
        selected_sweep = M_cwsweep[session['user_name']].corder['Flux-Bias']
        
        if int(irepeat) < session['c_cwsweep_address'][0]: # address's part before x
            # print("Well within Progress!")
            xsweep = range(session['c_cwsweep_structure'][1]) # can access full-range if selection is well within progress resume-point
        else: xsweep = range(session['c_cwsweep_address'][1]+1) # can only access until progress resume-point

        selected_Ir, selected_Qr = [], []
        for i_prepeat in range(ipowa_repeat):
            r_powa = int(ipowa) * ipowa_repeat + i_prepeat # from the beginning position of repeating power
            selected_Ir += [selectedata[gotocdata([int(irepeat), x, int(ixyfreq), int(ixypowa), int(isparam), int(iifb), int(ifreq), 2*r_powa], session['c_cwsweep_structure'])] for x in xsweep]
            selected_Qr += [selectedata[gotocdata([int(irepeat), x, int(ixyfreq), int(ixypowa), int(isparam), int(iifb), int(ifreq), 2*r_powa+1], session['c_cwsweep_structure'])] for x in xsweep]
        # AVERAGE up those power repeats:
        selected_I = list(mean(array(selected_Ir).reshape(ipowa_repeat, len(xsweep)), axis=0))
        selected_Q = list(mean(array(selected_Qr).reshape(ipowa_repeat, len(xsweep)), axis=0))
    elif "x" in ixyfreq:
        xtitle = "<b>XY-Frequency(GHz)</b>"
        selected_sweep = M_cwsweep[session['user_name']].corder['XY-Frequency']
        
        if [int(irepeat), int(ifluxbias)] < session['c_cwsweep_address'][0:2]: # address's part before x
            xsweep = range(session['c_cwsweep_structure'][2]) # can access full-range if selection is well within progress resume-point
        else: xsweep = range(session['c_cwsweep_address'][2]+1) # can only access until progress resume-point
        
        selected_Ir, selected_Qr = [], []
        for i_prepeat in range(ipowa_repeat):
            r_powa = int(ipowa) * ipowa_repeat + i_prepeat # from the beginning position of repeating power
            selected_Ir += [selectedata[gotocdata([int(irepeat), int(ifluxbias), x, int(ixypowa), int(isparam), int(iifb), int(ifreq), 2*r_powa], session['c_cwsweep_structure'])] for x in xsweep]
            selected_Qr += [selectedata[gotocdata([int(irepeat), int(ifluxbias), x, int(ixypowa), int(isparam), int(iifb), int(ifreq), 2*r_powa+1], session['c_cwsweep_structure'])] for x in xsweep]
        # AVERAGE up those power repeats:
        selected_I = list(mean(array(selected_Ir).reshape(ipowa_repeat, len(xsweep)), axis=0))
        selected_Q = list(mean(array(selected_Qr).reshape(ipowa_repeat, len(xsweep)), axis=0))
    elif "x" in ixypowa:
        xtitle = "<b>XY-Power(dBm)</b>"
        selected_sweep = M_cwsweep[session['user_name']].corder['XY-Power']
        
        if [int(irepeat), int(ifluxbias), int(ixyfreq)] < session['c_cwsweep_address'][0:3]: # address's part before x
            xsweep = range(session['c_cwsweep_structure'][3]) # can access full-range if selection is well within progress resume-point
        else: xsweep = range(session['c_cwsweep_address'][3]+1) # can only access until progress resume-point
        
        selected_Ir, selected_Qr = [], []
        for i_prepeat in range(ipowa_repeat):
            r_powa = int(ipowa) * ipowa_repeat + i_prepeat # from the beginning position of repeating power
            selected_Ir += [selectedata[gotocdata([int(irepeat), int(ifluxbias), int(ixyfreq), x, int(isparam), int(iifb), int(ifreq), 2*r_powa], session['c_cwsweep_structure'])] for x in xsweep]
            selected_Qr += [selectedata[gotocdata([int(irepeat), int(ifluxbias), int(ixyfreq), x, int(isparam), int(iifb), int(ifreq), 2*r_powa+1], session['c_cwsweep_structure'])] for x in xsweep]
        # AVERAGE up those power repeats:
        selected_I = list(mean(array(selected_Ir).reshape(ipowa_repeat, len(xsweep)), axis=0))
        selected_Q = list(mean(array(selected_Qr).reshape(ipowa_repeat, len(xsweep)), axis=0))
    
    elif "x" in isparam:
        pass
    elif "x" in iifb:
        pass

    elif "x" in ifreq:
        xtitle = "<b>frequency(GHz)</b>"
        selected_sweep = M_cwsweep[session['user_name']].corder['Frequency']
        
        if [int(irepeat), int(ifluxbias), int(ixyfreq), int(ixypowa), int(isparam), int(iifb)] < session['c_cwsweep_address'][0:6]: # address's part before x
            xsweep = range(session['c_cwsweep_structure'][6]) # can access full-range if selection is well within progress resume-point
        else: xsweep = range(session['c_cwsweep_address'][6]+1) # can only access until progress resume-point
        
        selected_Ir, selected_Qr = [], []
        for i_prepeat in range(ipowa_repeat):
            r_powa = int(ipowa) * ipowa_repeat + i_prepeat # from the beginning position of repeating power
            selected_Ir += [selectedata[gotocdata([int(irepeat), int(ifluxbias), int(ixyfreq), int(ixypowa), int(isparam), int(iifb), x, 2*r_powa], session['c_cwsweep_structure'])] for x in xsweep]
            selected_Qr += [selectedata[gotocdata([int(irepeat), int(ifluxbias), int(ixyfreq), int(ixypowa), int(isparam), int(iifb), x, 2*r_powa+1], session['c_cwsweep_structure'])] for x in xsweep]
        # AVERAGE up those power repeats:
        selected_I = list(mean(array(selected_Ir).reshape(ipowa_repeat, len(xsweep)), axis=0))
        selected_Q = list(mean(array(selected_Qr).reshape(ipowa_repeat, len(xsweep)), axis=0))
    elif "x" in ipowa:
        xtitle = "<b>Power(dBm)</b>"
        xpowa_repeat = ipowa_repeat
        
        if [int(irepeat), int(ifluxbias), int(ixyfreq), int(ixypowa), int(isparam), int(iifb), int(ifreq)] < session['c_cwsweep_address'][0:7]: # address's part before x
            xsweep = range(session['c_cwsweep_structure'][7] // 2) # can access full-range if selection is well within progress resume-point
        else: xsweep = range((session['c_cwsweep_address'][7]+1) // 2) # can only access until progress resume-point
        
        selected_Ir = [selectedata[gotocdata([int(irepeat), int(ifluxbias), int(ixyfreq), int(ixypowa), int(isparam), int(iifb), int(ifreq), 2*x], session['c_cwsweep_structure'])] for x in xsweep]
        selected_Qr = [selectedata[gotocdata([int(irepeat), int(ifluxbias), int(ixyfreq), int(ixypowa), int(isparam), int(iifb), int(ifreq), 2*x+1], session['c_cwsweep_structure'])] for x in xsweep]
        # AVERAGE up those repeated IQ-pairs:
        selected_I = list(mean(array(selected_Ir).reshape(len(xsweep)//xpowa_repeat, xpowa_repeat), axis=1)) #-->
        selected_Q = list(mean(array(selected_Qr).reshape(len(xsweep)//xpowa_repeat, xpowa_repeat), axis=1)) #-->

    # preparing data:
    # assembly amplitude & phase:
    MagPha = [IQAP(x[0],x[1]) for x in zip(selected_I, selected_Q)]
    Amp, Pha = [], []
    for i,j in MagPha:
        Amp.append(i); Pha.append(j)

    # x-range:
    if "x" in ipowa: selected_progress = xpowa.data[0:(len(xsweep) // xpowa_repeat)]
    else: selected_progress = waveform(selected_sweep).data[0:len(xsweep)]

    # to avoid exception when encountering recursive parameters:
    if "c" in ixyfreq + ixypowa + ifluxbias + isparam + iifb + ifreq + ipowa:
        selected_progress = list(range(len(selected_progress)))

    x1, y1, yup, yp = selected_progress, Amp, list(UnwraPhase(selected_progress, Pha)), Pha #list(unwrap(Pha)) 

    global data_dict
    data_dict = {xtitle: x1, 'Amplitude': y1, 'UPhase': yup, 'I': selected_I, 'Q': selected_Q, "exported by": session['user_name']}
    
    return jsonify(x1=x1, y1=y1, yup=yup, yp=yp, x1title=xtitle)

# Pending renovation below:
@bp.route('/char/cwsweep/2ddata', methods=['GET'])
def char_cwsweep_2ddata():
    irepeat = request.args.get('irepeat')
    ifluxbias = request.args.get('ifluxbias')
    ixyfreq = request.args.get('ixyfreq')
    ixypowa = request.args.get('ixypowa')
    isparam = request.args.get('isparam')
    iifb = request.args.get('iifb')
    ipowa = request.args.get('ipowa')
    ifreq = request.args.get('ifreq')

    # pre-transform ipowa:
    powa_order = M_cwsweep[session['user_name']].corder['Power']

    # preparing MPW dictionary
    dict_for_MPW = {
            "pqfile": str(M_cwsweep[session['user_name']].pqfile), "datalocation": M_cwsweep[session['user_name']].datalocation, "writtensize": M_cwsweep[session['user_name']].writtensize,
            "c_cwsweep_structure": session['c_cwsweep_structure'], "irepeat": irepeat, "ifluxbias": ifluxbias, "ixyfreq": ixyfreq, "ixypowa": ixypowa, 
            "isparam": isparam, "iifb": iifb, "ifreq": ifreq, "ipowa": ipowa, "powa_order": powa_order
        }
    set_status("MPW", dict_for_MPW)

    # Check progress:
    if not M_cwsweep[session['user_name']].data_progress%100:
        offset = 1
        print(Fore.GREEN + "The data is complete: we can see the whole picture now")
    else: 
        offset = 0 # to avoid incomplete array error
        print(Back.RED + "The data is NOT YET complete!")

    # Selecting 2D options:
    # REPEAT:
    if irepeat == "x" and ifluxbias == "y":
        x_name, y_name = "repeat", "fluxbias"
        print("X: REPEAT#, Y: Flux-Bias")
        xtitle, ytitle = "<b>REPEAT#</b>", "<b>Flux-Bias(V/A)</b>"
        x, y = list(range(session['c_cwsweep_address'][0]+offset)), waveform(M_cwsweep[session['user_name']].corder['Flux-Bias']).data
        x_count, y_count = session['c_cwsweep_address'][0]+offset, waveform(M_cwsweep[session['user_name']].corder['Flux-Bias']).count
    if irepeat == "x" and ixyfreq == "y":
        x_name, y_name = "repeat", "xyfreq"
        print("X: REPEAT#, Y: XY-Frequency")
        xtitle, ytitle = "<b>REPEAT#</b>", "<b>XY-Frequency(GHz)</b>"
        x, y = list(range(session['c_cwsweep_address'][0]+offset)), waveform(M_cwsweep[session['user_name']].corder['XY-Frequency']).data
        x_count, y_count = session['c_cwsweep_address'][0]+offset, waveform(M_cwsweep[session['user_name']].corder['XY-Frequency']).count
    # ONCE:
    elif ifluxbias == "x" and ixyfreq == "y":
        x_name, y_name = "fluxbias", "xyfreq"
        print("X: Flux-Bias, Y: XY-Frequency")
        xtitle, ytitle = "<b>Flux-Bias(V/A)</b>", "<b>XY-Frequency(GHz)</b>"
        x, y = waveform(M_cwsweep[session['user_name']].corder['Flux-Bias']).data[0:session['c_cwsweep_address'][1]+offset], waveform(M_cwsweep[session['user_name']].corder['XY-Frequency']).data
        x_count, y_count = session['c_cwsweep_address'][1]+offset, waveform(M_cwsweep[session['user_name']].corder['XY-Frequency']).count
    elif ixyfreq == "x" and ixypowa == "y":
        x_name, y_name = "xyfreq", "xypowa"
        print("X: XY-Frequency, Y: XY-Power")
        xtitle, ytitle = "<b>XY-Frequency(GHz)</b>", "<b>XY-Power(dBm)</b>"
        x, y = waveform(M_cwsweep[session['user_name']].corder['XY-Frequency']).data[0:session['c_cwsweep_address'][2]+offset], waveform(M_cwsweep[session['user_name']].corder['XY-Power']).data
        x_count, y_count = session['c_cwsweep_address'][2]+offset, waveform(M_cwsweep[session['user_name']].corder['XY-Power']).count
    elif ixyfreq == "x" and ifreq == "y":
        x_name, y_name = "xyfreq", "freq"
        print("X: XY-Frequency, Y: Frequency")
        xtitle, ytitle = "<b>XY-Frequency(GHz)</b>", "<b>Probe-Frequency(GHz)</b>"
        x, y = waveform(M_cwsweep[session['user_name']].corder['XY-Frequency']).data[0:session['c_cwsweep_address'][2]+offset], waveform(M_cwsweep[session['user_name']].corder['Frequency']).data
        x_count, y_count = session['c_cwsweep_address'][2]+offset, waveform(M_cwsweep[session['user_name']].corder['Frequency']).count
    elif ixyfreq == "x" and ipowa == "y":
        x_name, y_name = "xyfreq", "powa"
        print("X: XY-Frequency, Y: Power")
        xtitle, ytitle = "<b>XY-Frequency(GHz)</b>", "<b>Probing-Power(dBm)</b>"
        x, y = waveform(M_cwsweep[session['user_name']].corder['XY-Frequency']).data[0:session['c_cwsweep_address'][2]+offset], waveform(M_cwsweep[session['user_name']].corder['Power']).data
        x_count, y_count = session['c_cwsweep_address'][2]+offset, waveform(M_cwsweep[session['user_name']].corder['Power']).count

    # fast iteration method (parallel computing):
    stage, prev = clocker(0)
    CMD = ["python", "-c", "from pyqum.directive import MP_cwsweep as mp; print(mp.worker(%s,%s,'%s','%s'))"%(y_count,x_count,y_name,x_name)]
    with Popen(CMD, stdout=PIPE, shell=True) as proc:
        doutput = proc.stdout.read().decode("utf-8")
        output = json.loads(doutput.replace("\'", "\""))
        # try: os.kill(os.getppid(), signal.SIGTERM) # terminate parent process
        # except: pass
    Amp = output['rA']
    Pha = output['rP']
    stage, prev = clocker(stage, prev) # Marking time

    print("x is of length %s and of type %s" %(len(x),type(x)))
    print("y is of length %s and of type %s" %(len(y),type(y)))
    print("Amp of shape %s" %str(array(Amp).shape))
    ZZA, ZZP = Amp, Pha
    
    # x = list(range(len(x))) # for repetitive data
    return jsonify(x=x, y=y, ZZA=ZZA, ZZP=ZZP, xtitle=xtitle, ytitle=ytitle)


# CHAR -> 3. SQE-Pulsing =============================================================================================================================================
@bp.route('/char/sqepulse', methods=['GET'])
def char_sqepulse(): 
    return render_template("blog/msson/char/sqepulse.html")
# Initialize and list days specific to task
@bp.route('/char/sqepulse/init', methods=['GET'])
def char_sqepulse_init():
    global M_sqepulse, CParameters

    # check currently-connected users:
    try: print(Fore.GREEN + "Connected M-USER(s) for SQE-Pulse: %s" %M_sqepulse.keys())
    except: M_sqepulse = {}

    # check configuration:
    run_status = not get_status("SQE_Pulse")['pause'] 
    
    # 'user_name' accessing 'people' data:
    M_sqepulse[session['user_name']] = SQE_Pulse(session['people'])
    print(Fore.BLUE + "User %s is looking at %s's data" %(session['user_name'],session['people']))

    # PENDING: Flexible C-Structure:
    CParameters = {}
    CParameters['SQE_Pulse'] = ['repeat', 'Flux-Bias', 'XY-Frequency', 'XY-Power', 'RO-Frequency', 'RO-Power',
                'Pulse-Period', 'RO-ifLevel', 'RO-Pulse-Delay', 'RO-Pulse-Width', 'XY-ifLevel', 'XY-Pulse-Delay', 'XY-Pulse-Width', 
                'LO-Frequency', 'LO-Power', 'ADC-delay', 'Average', 'Sampling-Time']

    return jsonify(run_status=run_status, daylist=M_sqepulse[session['user_name']].daylist, run_permission=session['run_clearance'])
# list task entries based on day picked
@bp.route('/char/sqepulse/time', methods=['GET'])
def char_sqepulse_time():
    wday = int(request.args.get('wday'))
    M_sqepulse[session['user_name']].selectday(wday)
    return jsonify(taskentries=M_sqepulse[session['user_name']].taskentries)

# adjust settings input for certain instruments' set
@bp.route('/char/sqepulse/settings', methods=['GET'])
def char_sqepulse_settings():
    # under construction ***
    # pending: YOKO switching between V and I source
    # PSG type selection
    return jsonify()

# run NEW measurement:
@bp.route('/char/sqepulse/new', methods=['GET'])
def char_sqepulse_new():
    # Check user's current queue status:
    if session['run_clearance']:
        set_status("SQE_Pulse", dict(pause=False))
        global Run_sqepulse # for ETA calculation as well
        Run_sqepulse = {}
        wday = int(request.args.get('wday'))
        if wday < 0: print("Running New SQE-Pulse...")

        CORDER = json.loads(request.args.get('CORDER'))
        comment = request.args.get('comment').replace("\"","")
        simulate = bool(int(request.args.get('simulate')))
        
        Run_sqepulse['TOKEN'] = SQE_Pulse(session['people'], corder=CORDER, comment=comment, tag='', dayindex=wday, testeach=simulate)
    else: all()
    return jsonify(testeach=simulate)
# ETA (Estimated Time of Arrival for the WHOLE measurement)
@bp.route('/char/sqepulse/eta100', methods=['GET'])
def char_sqepulse_eta100():
    eta_time_100 = sum([a*b for a,b in zip(Run_sqepulse['TOKEN'].loopcount, Run_sqepulse['TOKEN'].loop_dur)])
    print(Fore.RED + "ETA: %s" %str(timedelta(seconds=eta_time_100)))
    eta_time_100 = str(timedelta(seconds=eta_time_100)).split('.')[0]
    return jsonify(eta_time_100=eta_time_100)
# pause the measurement:
@bp.route('/char/sqepulse/pause', methods=['GET'])
def char_sqepulse_pause():
    set_status("SQE_Pulse", dict(pause=True))
    return jsonify(pause=get_status("SQE_Pulse")['pause'])
# toggle between repeat or not
@bp.route('/char/sqepulse/setrepeat', methods=['GET'])
def char_sqepulse_setrepeat():
    set_status("SQE_Pulse", dict(repeat=bool(int(request.args.get('repeat')))))
    return jsonify(repeat=get_status("SQE_Pulse")['repeat'])
@bp.route('/char/sqepulse/getrepeat', methods=['GET'])
def char_sqepulse_getrepeat():
    return jsonify(repeat=get_status("SQE_Pulse")['repeat'])
# search through logs of data specific to task (pending)
@bp.route('/char/sqepulse/search', methods=['GET'])
def char_sqepulse_search():
    wday = int(request.args.get('wday'))
    filelist = M_sqepulse[session['user_name']].searchcomment()
    return jsonify(filelist=str(filelist))
# export to csv
@bp.route('/char/sqepulse/export/1dcsv', methods=['GET'])
def char_sqepulse_export_1dcsv():
    ifreq = request.args.get('ifreq') # merely for security reason to block out unsolicited visits by return None from this request
    print("ifreq: %s" %ifreq)
    status = None
    if ifreq is not None:
        set_csv(data_dict, '1Dsqepulse.csv')
        status = "csv written"
    return jsonify(status=status)
# list set-parameters based on selected task-entry
@bp.route('/char/sqepulse/access', methods=['GET'])
def char_sqepulse_access():
    wmoment = int(request.args.get('wmoment'))
    M_sqepulse[session['user_name']].selectmoment(wmoment)
    M_sqepulse[session['user_name']].accesstructure()
    corder = M_sqepulse[session['user_name']].corder
    data_progress = M_sqepulse[session['user_name']].data_progress
    data_repeat = data_progress // 100 + int(bool(data_progress % 100))

    global cmd_repeat
    cmd_repeat = {}
    cmd_repeat[session['user_name']] = '0 to %s * %s' %(int(data_repeat-1), int(data_repeat-1))
    corder['repeat'] = cmd_repeat[session['user_name']]

    # Measurement time:
    filetime = getmtime(M_sqepulse[session['user_name']].pqfile) # in seconds
    startmeasure = mktime(strptime(M_sqepulse[session['user_name']].day + " " + M_sqepulse[session['user_name']].startime(), "%Y-%m-%d(%a) %H:%M")) # made into seconds
    measureacheta = str(timedelta(seconds=(filetime-startmeasure)/data_progress*(trunc(data_progress/100+1)*100-data_progress)))

    # Structure & Addresses:
    session['c_sqepulse_structure'] = [waveform(corder[param]).count for param in CParameters['SQE_Pulse']][:-1] \
                                        + [waveform(corder[CParameters['SQE_Pulse'][-1]]).count*M_sqepulse[session['user_name']].datadensity]
    session['c_sqepulse_progress'] = cdatasearch(M_sqepulse[session['user_name']].resumepoint-1, session['c_sqepulse_structure'])
    
    pdata = dict()
    for params in CParameters['SQE_Pulse']:
        pdata[params] = waveform(corder[params]).data[0:session['c_sqepulse_progress'][CParameters['SQE_Pulse'].index(params)]+1]
    print(pdata['repeat'])

    return jsonify(data_progress=data_progress, measureacheta=measureacheta, corder=corder, comment=M_sqepulse[session['user_name']].comment, pdata=pdata)
# Resume the unfinished measurement
@bp.route('/char/sqepulse/resume', methods=['GET'])
def char_sqepulse_resume():
    set_status("SQE_Pulse", dict(pause=False))
    wday = int(request.args.get('wday'))
    wmoment = int(request.args.get('wmoment'))
    CORDER = json.loads(request.args.get('CORDER'))
    M_sqepulse[session['user_name']].accesstructure()
    SQE_Pulse(session['people'], corder=CORDER, dayindex=wday, taskentry=wmoment, resumepoint=M_sqepulse[session['user_name']].resumepoint)
    return jsonify(resumepoint=str(M_sqepulse[session['user_name']].resumepoint), datasize=str(M_sqepulse[session['user_name']].datasize))

@bp.route('/char/sqepulse/trackdata', methods=['GET'])
def char_sqepulse_trackdata():
    # PENDING 
    data_location = None
    return jsonify(data_location=data_location)
@bp.route('/char/sqepulse/resetdata', methods=['GET'])
def char_sqepulse_resetdata():
    ownerpassword = request.args.get('ownerpassword')
    truncateafter = int(request.args.get('truncateafter'))

    db = get_db()
    people = db.execute(
        'SELECT password FROM user WHERE username = ?', (session['people'],)
    ).fetchone()

    if check_password_hash(people['password'], ownerpassword):
        message = M_sqepulse[session['user_name']].resetdata(truncateafter)
    else:
        message = 'PASSWORD NOT VALID'

    return jsonify(message=message)

# Chart is supposedly shared by all measurements (under construction for multi-purpose)
@bp.route('/char/sqepulse/1ddata', methods=['GET'])
def char_sqepulse_1ddata():
    print(Fore.GREEN + "User %s is plotting 1D-Data" %session['user_name'])
    M_sqepulse[session['user_name']].loadata()
    selectedata = M_sqepulse[session['user_name']].selectedata
    print("Data length: %s" %len(selectedata))
    
    # load parameter indexes from json call:
    cselect = json.loads(request.args.get('cselect'))

    for k in cselect.keys():
        if "x" in cselect[k]:
            xtitle = "<b>" + k + "</b>"
            cselection = (",").join([s for s in cselect.values()])
            selected_caddress = [s for s in cselect.values()]
        
            # Sweep-command:
            if k == 'repeat':
                selected_sweep = cmd_repeat[session['user_name']]
            else:
                selected_sweep = M_sqepulse[session['user_name']].corder[k]

            # Adjusting c-parameters range for data analysis:
            parent_address = selected_caddress[:CParameters['SQE_Pulse'].index(k)] # address's part before x
            if [int(s) for s in parent_address] < session['c_sqepulse_progress'][0:len(parent_address)]:
                print(Fore.YELLOW + "selection is well within progress")
                sweepables = session['c_sqepulse_structure'][CParameters['SQE_Pulse'].index(k)]
            else: sweepables = session['c_sqepulse_progress'][CParameters['SQE_Pulse'].index(k)]+1

            # Special treatment on the last 'buffer' parameter to factor out the data-density first: 
            if CParameters['SQE_Pulse'].index(k) == len(CParameters['SQE_Pulse'])-1 :
                isweep = range(sweepables//M_sqepulse[session['user_name']].datadensity)
            else:
                isweep = range(sweepables) # flexible access until progress resume-point
            print(Back.WHITE + Fore.BLACK + "Sweeping %s points" %len(isweep))

            Idata = zeros(len(isweep))
            Qdata = zeros(len(isweep))
            for i in isweep:
                selected_caddress[CParameters['SQE_Pulse'].index(k)] = i
                if [c for c in cselect.values()][-1] == "s": # sampling mode currently limited to time-range (last 'basic' parameter) only
                    srange = request.args.get('srange').split("-") # sample range
                    if [int(srange[1]) , int(srange[0])] > [session['c_sqepulse_structure'][-1]//M_sqepulse[session['user_name']].datadensity] * 2:
                        print(Back.WHITE + Fore.RED + "Out of range")
                    else:
                        # FASTEST PARALLEL VECTORIZATION OF BIG DATA BY NUMPY:
                        slength = int(srange[1]) - int(srange[0]) + 1
                        # Assemble stacks of selected c-address for this sample range:
                        selected_caddress_I = array([[int(s) for s in selected_caddress[:-1]] + [0]] * slength)
                        selected_caddress_Q = array([[int(s) for s in selected_caddress[:-1]] + [0]] * slength)
                        
                        selected_caddress_I[:,-1] = 2 * array(range(int(srange[0]),int(srange[1])+1))
                        selected_caddress_Q[:,-1] = 2 * array(range(int(srange[0]),int(srange[1])+1)) + ones(slength)
                        # Compressing I & Q of this sample range:
                        selectedata = array(selectedata)
                        Idata[i] = mean(selectedata[gotocdata(selected_caddress_I, session['c_sqepulse_structure'])])
                        Qdata[i] = mean(selectedata[gotocdata(selected_caddress_Q, session['c_sqepulse_structure'])]) 

                else:
                    selected_caddress = [int(s) for s in selected_caddress]
                    Basic = selected_caddress[-1]
                    # Extracting I & Q:
                    Idata[i] = selectedata[gotocdata(selected_caddress[:-1]+[2*Basic], session['c_sqepulse_structure'])]
                    Qdata[i] = selectedata[gotocdata(selected_caddress[:-1]+[2*Basic+1], session['c_sqepulse_structure'])]
            Adata = sqrt(Idata**2 + Qdata**2)    

    print("Structure: %s" %session['c_sqepulse_structure'])
    # print("I: %s" %Idata[0])
    # print("Q: %s" %Qdata[0])    
    # x-range:
    selected_progress = waveform(selected_sweep).data[0:len(isweep)]

    # facilitate index location for range clipping:
    if "c" in cselection:
        selected_progress = list(range(len(selected_progress)))

    x, yI, yQ, yA = selected_progress, list(Idata), list(Qdata), list(Adata)

    global data_dict
    data_dict = {xtitle: x, 'I': yI, 'Q': yQ, 'A(V)': yA, "exported by": session['user_name']}
    
    return jsonify(x=x, yI=yI, yQ=yQ, yA=yA, xtitle=xtitle)

# Pending renovation below:
@bp.route('/char/sqepulse/2ddata', methods=['GET'])
def char_sqepulse_2ddata():
    irepeat = request.args.get('irepeat')
    ifluxbias = request.args.get('ifluxbias')
    ixyfreq = request.args.get('ixyfreq')
    ixypowa = request.args.get('ixypowa')
    isparam = request.args.get('isparam')
    iifb = request.args.get('iifb')
    ipowa = request.args.get('ipowa')
    ifreq = request.args.get('ifreq')

    # pre-transform ipowa:
    powa_order = M_sqepulse[session['user_name']].corder['Power']

    # preparing MPW dictionary
    dict_for_MPW = {
            "pqfile": str(M_sqepulse[session['user_name']].pqfile), "datalocation": M_sqepulse[session['user_name']].datalocation, "writtensize": M_sqepulse[session['user_name']].writtensize,
            "c_sqepulse_structure": session['c_sqepulse_structure'], "irepeat": irepeat, "ifluxbias": ifluxbias, "ixyfreq": ixyfreq, "ixypowa": ixypowa, 
            "isparam": isparam, "iifb": iifb, "ifreq": ifreq, "ipowa": ipowa, "powa_order": powa_order
        }
    set_status("MPW", dict_for_MPW)

    # Check progress:
    if not M_sqepulse[session['user_name']].data_progress%100:
        offset = 1
        print(Fore.GREEN + "The data is complete: we can see the whole picture now")
    else: 
        offset = 0 # to avoid incomplete array error
        print(Back.RED + "The data is NOT YET complete!")

    # Selecting 2D options:
    # REPEAT:
    if irepeat == "x" and ifluxbias == "y":
        x_name, y_name = "repeat", "fluxbias"
        print("X: REPEAT#, Y: Flux-Bias")
        xtitle, ytitle = "<b>REPEAT#</b>", "<b>Flux-Bias(V/A)</b>"
        x, y = list(range(session['c_sqepulse_progress'][0]+offset)), waveform(M_sqepulse[session['user_name']].corder['Flux-Bias']).data
        x_count, y_count = session['c_sqepulse_progress'][0]+offset, waveform(M_sqepulse[session['user_name']].corder['Flux-Bias']).count
    if irepeat == "x" and ixyfreq == "y":
        x_name, y_name = "repeat", "xyfreq"
        print("X: REPEAT#, Y: XY-Frequency")
        xtitle, ytitle = "<b>REPEAT#</b>", "<b>XY-Frequency(GHz)</b>"
        x, y = list(range(session['c_sqepulse_progress'][0]+offset)), waveform(M_sqepulse[session['user_name']].corder['XY-Frequency']).data
        x_count, y_count = session['c_sqepulse_progress'][0]+offset, waveform(M_sqepulse[session['user_name']].corder['XY-Frequency']).count
    # ONCE:
    elif ifluxbias == "x" and ixyfreq == "y":
        x_name, y_name = "fluxbias", "xyfreq"
        print("X: Flux-Bias, Y: XY-Frequency")
        xtitle, ytitle = "<b>Flux-Bias(V/A)</b>", "<b>XY-Frequency(GHz)</b>"
        x, y = waveform(M_sqepulse[session['user_name']].corder['Flux-Bias']).data[0:session['c_sqepulse_progress'][1]+offset], waveform(M_sqepulse[session['user_name']].corder['XY-Frequency']).data
        x_count, y_count = session['c_sqepulse_progress'][1]+offset, waveform(M_sqepulse[session['user_name']].corder['XY-Frequency']).count
    elif ixyfreq == "x" and ixypowa == "y":
        x_name, y_name = "xyfreq", "xypowa"
        print("X: XY-Frequency, Y: XY-Power")
        xtitle, ytitle = "<b>XY-Frequency(GHz)</b>", "<b>XY-Power(dBm)</b>"
        x, y = waveform(M_sqepulse[session['user_name']].corder['XY-Frequency']).data[0:session['c_sqepulse_progress'][2]+offset], waveform(M_sqepulse[session['user_name']].corder['XY-Power']).data
        x_count, y_count = session['c_sqepulse_progress'][2]+offset, waveform(M_sqepulse[session['user_name']].corder['XY-Power']).count
    elif ixyfreq == "x" and ifreq == "y":
        x_name, y_name = "xyfreq", "freq"
        print("X: XY-Frequency, Y: Frequency")
        xtitle, ytitle = "<b>XY-Frequency(GHz)</b>", "<b>Probe-Frequency(GHz)</b>"
        x, y = waveform(M_sqepulse[session['user_name']].corder['XY-Frequency']).data[0:session['c_sqepulse_progress'][2]+offset], waveform(M_sqepulse[session['user_name']].corder['Frequency']).data
        x_count, y_count = session['c_sqepulse_progress'][2]+offset, waveform(M_sqepulse[session['user_name']].corder['Frequency']).count
    elif ixyfreq == "x" and ipowa == "y":
        x_name, y_name = "xyfreq", "powa"
        print("X: XY-Frequency, Y: Power")
        xtitle, ytitle = "<b>XY-Frequency(GHz)</b>", "<b>Probing-Power(dBm)</b>"
        x, y = waveform(M_sqepulse[session['user_name']].corder['XY-Frequency']).data[0:session['c_sqepulse_progress'][2]+offset], waveform(M_sqepulse[session['user_name']].corder['Power']).data
        x_count, y_count = session['c_sqepulse_progress'][2]+offset, waveform(M_sqepulse[session['user_name']].corder['Power']).count

    # fast iteration method (parallel computing):
    stage, prev = clocker(0)
    CMD = ["python", "-c", "from pyqum.directive import MP_sqepulse as mp; print(mp.worker(%s,%s,'%s','%s'))"%(y_count,x_count,y_name,x_name)]
    with Popen(CMD, stdout=PIPE, shell=True) as proc:
        doutput = proc.stdout.read().decode("utf-8")
        output = json.loads(doutput.replace("\'", "\""))
        # try: os.kill(os.getppid(), signal.SIGTERM) # terminate parent process
        # except: pass
    Amp = output['rA']
    Pha = output['rP']
    stage, prev = clocker(stage, prev) # Marking time

    print("x is of length %s and of type %s" %(len(x),type(x)))
    print("y is of length %s and of type %s" %(len(y),type(y)))
    print("Amp of shape %s" %str(array(Amp).shape))
    ZZA, ZZP = Amp, Pha
    
    # x = list(range(len(x))) # for repetitive data
    return jsonify(x=x, y=y, ZZA=ZZA, ZZP=ZZP, xtitle=xtitle, ytitle=ytitle)






print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this



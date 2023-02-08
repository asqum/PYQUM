# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name

from json import loads, dumps
from importlib import import_module as im
from flask import Flask, request, render_template, Response, redirect, Blueprint, jsonify, session, send_from_directory, abort, g
from pyqum.instrument.logger import get_status, set_status, status_code, output_code, clocker, set_mat, bdr_zip_log, address, acting

# Error handling
from contextlib import suppress

# Scientific
from scipy import constants as cnst
from si_prefix import si_format, si_parse
from numpy import cos, sin, pi, polyfit, poly1d, array, roots, isreal, sqrt, mean, power, linspace, float64

# Load instruments
from pyqum import get_db, close_db
try: from pyqum.instrument.machine import YOKO, KEIT, ALZDG
except: print(Fore.RED + Back.WHITE + "Some Drivers Missing... Entering Virtual Mode.")
from pyqum.instrument.dilution import bluefors
from pyqum.instrument.toolbox import match, waveform, pauselog
from pyqum.instrument.analyzer import IQAParray, pulse_baseband, UnwraPhase
from pyqum.instrument.composer import pulser
from pyqum.instrument.reader import inst_designate, inst_order, device_port

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
        else: 
            acting("ENTERING MACHINE")
            print(Fore.LIGHTBLUE_EX + "USER " + Fore.YELLOW + "%s [%s] "%(session['user_name'], session['user_id']) + Fore.LIGHTBLUE_EX + "has entered MACHINE" )
        return render_template("blog/machn/machine.html")
    return("<h3>WHO ARE YOU?</h3><h3>Please F**k*ng Login!</h3><h3>Courtesy from <a href='http://qum.phys.sinica.edu.tw:%s/auth/login'>HoDoR</a></h3>" %get_status("WEB")["port"])

# region: ALL (for Machine Overview)
@bp.route('/all', methods=['POST', 'GET'])
def all(): 
    current_usr = session['user_name']
    try: Bob_Address="http://qum.phys.sinica.edu.tw:%s/"%(device_port("TC"))
    except: abort(404)
    try: Scope_Address="%s"%(device_port("RTP"))
    except: abort(404)
    try: MXA_Address="http://qum.phys.sinica.edu.tw:%s/"%(device_port("MXA"))
    except: abort(404)
    return render_template("blog/machn/all.html", current_usr=current_usr, Bob_Address=Bob_Address, Scope_Address=Scope_Address, MXA_Address=MXA_Address)
@bp.route('/all/machine', methods=['GET'])
def allmachine():
    print(Fore.CYAN + "Registered Instrument-list:\n%s"%g.instlist)
    return jsonify(machlist=g.machlist)
@bp.route('/all/set/machine', methods=['GET'])
def allsetmachine():
    # PENDING
    return jsonify()
@bp.route('/all/mxc', methods=['GET'])
def allmxc():
    '''DR-specific T6 to be appended at the bottomline of measurement comment:'''
    dr = bluefors(designation=device_port("BDR"))
    dr.selectday(-1)

    mxcmk=dr.temperaturelog(6)[1][-1]
    try: mxcmk = round(float(mxcmk) * 1000, 3) # convert to mK
    except(ValueError): pass # in case the sensor is off (giving ~)

    print(Fore.YELLOW + "T6 for %s: %smK" %(device_port("BDR"), mxcmk))
    return jsonify(mxcmk=mxcmk)
@bp.route('/all/bdr/current/status', methods=['GET'])
def allbdrcurrentstatus():
    '''Display all BDR current status: Logging Latest Key-Readings for ALL'''
    dr = bluefors(designation=device_port("BDR"))
    dr.selectday(-1)
    
    latestbdr = {}
    for i in range(6):
        latestbdr.update({"P%s"%(i+1):dr.pressurelog(i+1)[1][-1]})
    for i in [1,2,5,6,7]:
        latestbdr.update({"T%s"%(i):dr.temperaturelog(i)[1][-1]})
    for i in range(21):
        latestbdr.update({"V%s"%(i+1):dr.channellog('v%s'%(i+1))[1][-1]})
    latestbdr.update({"Pulse-Tube":dr.channellog("pulsetube")[1][-1]})
    latestbdr.update({"Flow":dr.flowmeterlog()[1][-1]})
    set_status("BDR", latestbdr)

    return jsonify(latestbdr=latestbdr)
# endregion

# region: SG (user-specific, Generalized)
def sg_container():
    global sgbench, SG, sgchannel
    try: print(Fore.GREEN + "Connected SG: %s" %sgbench.keys())
    except: sgbench, SG = {}, {}
    try: print(Fore.GREEN + "SG Channel: %s" %sgchannel.keys())
    except: sgchannel = {}
    return
@bp.route('/sg', methods=['GET'])
def sg(): 
    sg_container()
    return render_template("blog/machn/sg.html")
@bp.route('/sg/log', methods=['GET'])
def sglog():
    log = get_status(request.args.get('sgname').split('-')[0], request.args.get('sgname').split('-')[1])
    return jsonify(log=log)
@bp.route('/sg/connect', methods=['GET'])
def sgconnect():
    sg_container()
    sgname = request.args.get('sgname') # name = type + label
    sgtag = '%s:%s' %(sgname,session['user_name']) # tag = <type>-<label>:<user>
    sgtype, sglabel, sguser = sgtag.split('-')[0], sgtag.split('-')[1].split(':')[0], sgtag.split('-')[1].split(':')[1]
    linkedsg = ['%s-%s'%(x.split('-')[0],x.split('-')[1].split(':')[0]) for x in sgbench.keys()]
    print("sgname: %s, linkedsg: %s" %(sgname,linkedsg))
    if sgname not in linkedsg and int(g.user['instrument'])>=3:
        '''get in if not currently initiated'''
        try:
            SG[sgtype] = im("pyqum.instrument.machine.%s" %sgtype)
            sgbench[sgtag] = SG[sgtype].Initiate(sglabel)
            sgchannel[sgtag] = request.args.get('channel') # Default channel
            message = "%s is successfully initiated by %s" %(sgname,sguser)
            status = "connected"
            acting("CONNECTING SG: %s" %(request.args.get('sgname')))
        except:
            # raise
            message = "Please check if %s's connection configuration is OK or is it being used!" %(sgname)
            status = 'error'
    else:
        # Check who is currently using the instrument:
        
        try: 
            db = get_db()
            instr_user = db.execute('SELECT u.username FROM user u JOIN machine m ON m.user_id = u.id WHERE m.codename = ?', ('%s_%s'%(sgtype,sglabel),)).fetchone()[0]
            close_db()
            message = "%s is being connected to %s" %(sgname,instr_user)
        except(TypeError):
            instr_user = None
            message = "INSTRUMENT IS COMING SOON" # in the process of procurement
        
        # Connecting or Waiting or Forbidden?
        if instr_user == session['user_name']: status = 'connected'
        elif int(g.user['instrument'])>=3: status = 'waiting'
        else: message, status = 'NOT ENOUGH CLEARANCE', 'forbidden'
    return jsonify(message=message,status=status)
@bp.route('/sg/closet', methods=['GET'])
def sgcloset():
    sgtag, sgtype = '%s:%s' %(request.args.get('sgname'),session['user_name']), request.args.get('sgtype')
    try: 
        status = SG[sgtype].close(sgbench[sgtag], sgtag.split('-')[1].split(':')[0], reset=False)
        acting("CLOSING SG: %s" %(request.args.get('sgname')))
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
    stat = SG[sgtype].frequency(sgbench[sgtag], action=['Set_%s'%sgchannel[sgtag], freq + frequnit])
    message = 'frequency: %s <%s>' %(stat[1], stat[0])
    return jsonify(message=message)
@bp.route('/sg/set/powa', methods=['GET'])
def sgsetpowa():
    sgtag, sgtype = '%s:%s' %(request.args.get('sgname'),session['user_name']), request.args.get('sgtype')
    powa = request.args.get('powa')
    powaunit = '' #request.args.get('powaunit') # UNIT DOESN'T WORK IN DDSLO's SCPI-COMMAND!
    stat = SG[sgtype].power(sgbench[sgtag], action=['Set_%s'%sgchannel[sgtag], powa + powaunit])
    message = 'power: %s <%s>' %(stat[1], stat[0])
    return jsonify(message=message)
@bp.route('/sg/set/oupt', methods=['GET'])
def sgsetoupt():
    sgtag, sgtype = '%s:%s' %(request.args.get('sgname'),session['user_name']), request.args.get('sgtype')
    oupt = request.args.get('oupt')
    stat = SG[sgtype].rfoutput(sgbench[sgtag], action=['Set_%s'%sgchannel[sgtag], int(oupt)])
    message = 'RF output: %s <%s>' %(stat[1], stat[0])
    return jsonify(message=message)
@bp.route('/sg/set/channel', methods=['GET'])
def sgsetchannel():
    sgtag, sgtype = '%s:%s' %(request.args.get('sgname'),session['user_name']), request.args.get('sgtype')
    sgchannel[sgtag] = request.args.get('channel')
    message = {}
    if sgtype=='DDSLO': parakeys = dict(frequency="FREQUENCY", power="POWER")
    else: parakeys = dict(frequency="CW", power="AMPLITUDE")
    try:
        message['frequency'] = si_format(float(SG[sgtype].frequency(sgbench[sgtag], ['Get_%s'%sgchannel[sgtag], ''])[1][parakeys['frequency']]),precision=12) + "Hz"
        message['power'] = si_format(float(SG[sgtype].power(sgbench[sgtag], ['Get_%s'%sgchannel[sgtag], ''])[1][parakeys['power']]),precision=2) + "dBm"
        message['rfoutput'] = int(SG[sgtype].rfoutput(sgbench[sgtag], ['Get_%s'%sgchannel[sgtag], ''])[1]['STATE']) # rf output
    except:
        # raise
        message = dict(status='%s is not connected' %sgtype)
    return jsonify(message=message)
# endregion

# region: DAC (user-specific, Generalized)
def dac_container():
    global DAC_handle, DAC
    try: print(Fore.GREEN + "Connected DAC: %s" %DAC_handle.keys())
    except: DAC_handle, DAC = {}, {}
    return
@bp.route('/dac', methods=['GET'])
def dac(): 
    dac_container
    return render_template("blog/machn/dac.html")
@bp.route('/dac/log', methods=['GET'])
def daclog():
    log = get_status(request.args.get('dacname').split('-')[0], request.args.get('dacname').split('-')[1])
    return jsonify(log=log)
@bp.route('/dac/connect', methods=['GET'])
def dacconnect():
    dac_container()
    dacname = request.args.get('dacname')
    dactag = '%s:%s' %(dacname,session['user_name'])
    print("dactag: %s" %dactag)
    dactype, daclabel, dacuser = dactag.split('-')[0], dactag.split('-')[1].split(':')[0], dactag.split('-')[1].split(':')[1]
    linkeddac = ['%s-%s'%(x.split('-')[0],x.split('-')[1].split(':')[0]) for x in DAC_handle.keys()]
    if dacname not in linkeddac and int(g.user['instrument'])>=3:
        '''get in if not currently initiated'''
        try:
            DAC[dactype] = im("pyqum.instrument.machine.%s" %dactype)
            DAC_handle[dactag] = DAC[dactype].Initiate(daclabel)
            message = "%s is successfully initiated by %s" %(dacname,dacuser)
            status = "connected"
            acting("CONNECTING DAC: %s" %(request.args.get('dacname')))
        except:
            message = "Please check if %s's connection configuration is OK or is it being used!" %(dacname)
            status = 'error'
    else:
        # Check who is currently using the instrument:
        
        try: 
            db = get_db()
            instr_user = db.execute('SELECT u.username FROM user u JOIN machine m ON m.user_id = u.id WHERE m.codename = ?', ('%s_%s'%(dactype,daclabel),)).fetchone()[0]
            close_db()
            message = "%s is being connected to %s" %(dacname,instr_user)
        except(TypeError):
            instr_user = None
            message = "INSTRUMENT IS COMING SOON" # in the process of procurement
        
        # Connecting or Waiting or Forbidden?
        if instr_user == session['user_name']: status = 'connected'
        elif int(g.user['instrument'])>=3: status = 'waiting'
        else: message, status = 'NOT ENOUGH CLEARANCE', 'forbidden'
    return jsonify(message=message,status=status)
@bp.route('/dac/closet', methods=['GET'])
def daccloset():
    dactag, dactype = '%s:%s' %(request.args.get('dacname'),session['user_name']), request.args.get('dactype')
    status = DAC[dactype].close(DAC_handle[dactag], dactag.split('-')[1].split(':')[0], reset=False)
    acting("CLOSING DAC: %s" %(request.args.get('dacname')))
    del DAC_handle[dactag]
    return jsonify(message=status)
@bp.route('/dac/testing', methods=['GET'])
def dactesting():
    dactag, dactype = '%s:%s' %(request.args.get('dacname'),session['user_name']), request.args.get('dactype')
    status = DAC[dactype].test(DAC_handle[dactag])
    return jsonify(message=status)
@bp.route('/dac/alloff', methods=['GET'])
def dacalloff():
    dactag, dactype = '%s:%s' %(request.args.get('dacname'),session['user_name']), request.args.get('dactype')
    status = DAC[dactype].alloff(DAC_handle[dactag], action=['Set',1])
    return jsonify(message=status)
@bp.route('/dac/clearall', methods=['GET'])
def dacclearall():
    dactag, dactype = '%s:%s' %(request.args.get('dacname'),session['user_name']), request.args.get('dactype')
    status = DAC[dactype].clear_waveform(DAC_handle[dactag], 'all')
    set_status(request.args.get('dacname').split('-')[0], {'resend': 0}, request.args.get('dacname').split('-')[1])
    return jsonify(message=status)
@bp.route('/dac/set/clockfreq', methods=['GET'])
def dacsetclockfreq():
    dactag, dactype = '%s:%s' %(request.args.get('dacname'),session['user_name']), request.args.get('dactype')
    clockfreq = request.args.get('clockfreq')
    clockfrequnit = request.args.get('clockfrequnit')[0]
    stat = DAC[dactype].clock(DAC_handle[dactag], action=['Set', 'EFIXed', si_parse(clockfreq + clockfrequnit)])
    message = 'frequency: %s <%s>' %(stat[1], stat[0])
    return jsonify(message=message)
@bp.route('/dac/get/channels', methods=['GET'])
def dacgetchannels():
    dactag, dactype, Channel = '%s:%s' %(request.args.get('dacname'),session['user_name']), request.args.get('dactype'), request.args.get('Channel')
    dac_status = get_status(request.args.get('dacname').split('-')[0], request.args.get('dacname').split('-')[1])
    level = DAC[dactype].sourcelevel(DAC_handle[dactag], Channel)[1]
    message = {}
    try: message['source-amplitude'], message['source-offset'] = si_format(float(level['AMPLITUDE']), precision=3) + "Vpp", si_format(float(level['OFFSET']), precision=3) + "V"
    except(TypeError): message['source-amplitude'], message['source-offset'] = "1.5 Vpp", "0 V" # Default values
    if dactype=="TKAWG": message['chstate'] = int(DAC[dactype].output(DAC_handle[dactag], Channel)[1]['STATE']) # TKAWG ONLY
    try: message['score'] = dac_status['SCORE-%s'%Channel]
    except(KeyError): pass
    try: message['master'] = dac_status['master']
    except(KeyError): pass
    try: message['resend'] = dac_status['resend']
    except(KeyError): pass
    try: message['markeroption'] = dac_status['markeroption-ch%s'%Channel]
    except(KeyError): pass
    return jsonify(message=message)
@bp.route('/dac/set/channels', methods=['GET'])
def dacsetchannels():
    dactag, dactype, Channel = '%s:%s' %(request.args.get('dacname'),session['user_name']), request.args.get('dactype'), int(request.args.get('Channel'))
    score, master = request.args.get('score'), bool(int(request.args.get('master')))
    maxlevel = si_parse(request.args.get('maxlvl') + request.args.get('maxlvlunit').split("Vpp")[0])
    trigbyPXI, markerdelay, markeroption = int(request.args.get('trigbyPXI')), int(request.args.get('markerdelay')), request.args.get('markeroption')

    # Extract PINSW option from markeroption:
    markeroption = int(markeroption.split("-")[0])
    try: PINSW = bool(int(markeroption.split("-")[1]))
    except: PINSW = False

    # PULSE ASSEMBLY:
    dt = round(1/float(DAC[dactype].clock(DAC_handle[dactag])[1]['SRATe'])/1e-9, 2)
    pulseq = pulser(dt=dt, clock_multiples=1, score=score)
    pulseq.song()

    # SCORE INJECTION:
    if dactype=="TKAWG": New = True
    elif dactype=="SDAWG": New = not bool(int(request.args.get('resend')))
    if New: DAC[dactype].prepare_DAC(DAC_handle[dactag], Channel, pulseq.totalpoints, maxlevel, dict(Master=master, trigbyPXI=trigbyPXI, markerdelay=markerdelay, markeroption=markeroption))
    DAC[dactype].compose_DAC(DAC_handle[dactag], Channel, pulseq.music, pulseq.envelope, markeroption, dict(PINSW=PINSW, clearQ=int(request.args.get('clearQ'))))

    update_items = {'SCORE-%s'%Channel: score, 'master': int(master), 'trigbyPXI': trigbyPXI, 'markerdelay': markerdelay, 'markeroption-ch%s'%Channel: markeroption}
    set_status(request.args.get('dacname').split('-')[0], update_items, request.args.get('dacname').split('-')[1])
    
    music, timeline =list(pulseq.music)[::20], list(pulseq.timeline)[::20]
    return jsonify(music=music, timeline=timeline)
@bp.route('/dac/live/update/channel', methods=['GET'])
def dacliveupdatechannel():
    Channel = int(request.args.get('Channel'))
    dacupdate = int(request.args.get('dacupdate'))
    set_status('RELAY', {'dacupdate_%s/%s'%(request.args.get('dacname'),Channel): dacupdate})
    return jsonify(message="RELAY UPDATED!")
@bp.route('/dac/output/channels', methods=['GET'])
def dacoutputchannels():
    '''TKAWG ONLY'''
    dactag, dactype = '%s:%s' %(request.args.get('dacname'),session['user_name']), request.args.get('dactype')
    Channel = int(request.args.get('Channel'))
    state = request.args.get('state')
    status = DAC[dactype].output(DAC_handle[dactag], Channel, action=['Set',state])
    return jsonify(status=status)
@bp.route('/dac/get', methods=['GET'])
def dacget():
    dactag, dactype = '%s:%s' %(request.args.get('dacname'),session['user_name']), request.args.get('dactype')
    dac_status = get_status(request.args.get('dacname').split('-')[0], request.args.get('dacname').split('-')[1])
    message = {}
    try:
        message['clockfreq'] = si_format(float(DAC[dactype].clock(DAC_handle[dactag])[1]['SRATe']),precision=3) + "S/s" # clock-frequency
        message['model'] = DAC[dactype].model(DAC_handle[dactag])[1]['IDN']
        message['runstate'] = int(DAC[dactype].runstate(DAC_handle[dactag])[1]['RSTATE'])
        try: message['wlist'] = [x.split('-')[1] for x in DAC[dactype].waveformlist(DAC_handle[dactag])[1]['LIST'].replace('\"','').split(',')]
        except: message['wlist'] = []

        # Check waveform presence in each channels:
        if dactype=="TKAWG": pass #PENDING: check output-state instead?
        elif dactype=="SDAWG":
            try: 
                message['ready2play'] = []
                for i in range(4): message['ready2play'].append(int(DAC[dactype].ready(DAC_handle[dactag], channel=(i+1))))
            except: message['ready2play'] = [0,0,0,0]
    except:
        message = dict(status='%s is not connected or busy or error' %request.args.get('dacname'))
    try: message['trigbyPXI'] = dac_status['trigbyPXI']
    except(KeyError): pass
    try: message['markerdelay'] = dac_status['markerdelay']
    except(KeyError): pass
    
    print("message: %s" %message)
    return jsonify(message=message)
@bp.route('/dac/play', methods=['GET'])
def dacplay():
    dactag, dactype = '%s:%s' %(request.args.get('dacname'),session['user_name']), request.args.get('dactype')
    DAC[dactype].alloff(DAC_handle[dactag], action=['Set',0])
    DAC[dactype].ready(DAC_handle[dactag])
    status = DAC[dactype].play(DAC_handle[dactag])
    set_status(request.args.get('dacname').split('-')[0], {'resend': 1}, request.args.get('dacname').split('-')[1])
    return jsonify(status=status)
@bp.route('/dac/stop', methods=['GET'])
def dacstop():
    dactag, dactype = '%s:%s' %(request.args.get('dacname'),session['user_name']), request.args.get('dactype')
    status = DAC[dactype].stop(DAC_handle[dactag])
    set_status(request.args.get('dacname').split('-')[0], {'resend': 0}, request.args.get('dacname').split('-')[1])
    return jsonify(status=status)
# endregion

# region: ADC (user-specific, Generalized)
def adc_container():
    global adcboard, ADC, adc_1Ddata
    try: print(Fore.GREEN + "Connected ADC: %s" %adcboard.keys())
    except: adcboard, ADC = {}, {}
    # Initialize 1D Data-Holder:
    try: print(Fore.CYAN + "Connected M-USER(s) holding ADC's 1D-DATA: %s" %adc_1Ddata.keys())
    except: adc_1Ddata = {}
    return
@bp.route('/adc', methods=['GET'])
def adc(): 
    adc_container()
    return render_template("blog/machn/adc.html")
@bp.route('/adc/log', methods=['GET'])
def adclog():
    log = get_status(request.args.get('adcname').split('-')[0], request.args.get('adcname').split('-')[1])
    return jsonify(log=log)
@bp.route('/adc/connect', methods=['GET'])
def adcconnect():
    adc_container()
    adcname = request.args.get('adcname')
    adctag = '%s:%s' %(adcname,session['user_name'])
    print("adctag: %s" %adctag)
    adctype, adclabel, adcuser = adctag.split('-')[0], adctag.split('-')[1].split(':')[0], adctag.split('-')[1].split(':')[1]
    linkedadc = ['%s-%s'%(x.split('-')[0],x.split('-')[1].split(':')[0]) for x in adcboard.keys()]
    if adcname not in linkedadc and int(g.user['instrument'])>=3:
        '''get in if not currently initiated'''
        try:
            ADC[adctype] = im("pyqum.instrument.machine.%s" %adctype)
            adcboard[adctag] = ADC[adctype].Initiate(adclabel)
            message = "%s is successfully initiated by %s" %(adcname,adcuser)
            status = "connected"
            acting("CONNECTING ADC: %s" %(request.args.get('adcname')))
        except:
            message = "Please check if %s's connection configuration is OK or is it being used!" %(adcname)
            status = 'error'
    else:
        # Check who is currently using the instrument:
        
        try: 
            db = get_db()
            instr_user = db.execute('SELECT u.username FROM user u JOIN machine m ON m.user_id = u.id WHERE m.codename = ?', ('%s_%s'%(adctype,adclabel),)).fetchone()[0]
            close_db()
            message = "%s is being connected to %s" %(adcname,instr_user)
        except(TypeError):
            instr_user = None
            message = "INSTRUMENT IS COMING SOON" # in the process of procurement
        
        # Connecting or Waiting or Forbidden?
        if instr_user == session['user_name']: status = 'connected'
        elif int(g.user['instrument'])>=3: status = 'waiting'
        else: message, status = 'NOT ENOUGH CLEARANCE', 'forbidden'
    return jsonify(message=message,status=status)
@bp.route('/adc/configureboard', methods=['GET'])
def adcconfigureboard():
    adctag, adctype = '%s:%s' %(request.args.get('adcname'),session['user_name']), request.args.get('adctype')
    trigdelay, trigdelayunit = request.args.get('trigdelay'), request.args.get('trigdelayunit')[0]
    FPGA = request.args.get('FPGA')
    
    # PENDING: EXTRACT & STORE MACHINE's SPEC IN DATABASE (Sampling-rate etc.)

    update_items = dict( triggerDelay_sec=si_parse(trigdelay+trigdelayunit), TOTAL_POINTS=round(int(request.args.get('recordtime'))/2), NUM_CYCLES=int(request.args.get('recordsum')), \
                            PXI=int(request.args.get('PXI')), FULL_SCALE=float(request.args.get('fullscale')), FPGA=int(FPGA) )
    dt_ns = ADC[adctype].ConfigureBoard(adcboard[adctag], update_items)
    update_items.update(trigdelay=trigdelay)
    set_status(request.args.get('adcname').split('-')[0], update_items, request.args.get('adcname').split('-')[1])

    # print(Fore.YELLOW + "configureboard: FPGA: %s" %(FPGA))
    status = "Configure Board Successfully: %s-ns/point, FPGA: %s" %(dt_ns, adcboard[adctag].FPGA)
    return jsonify(message=status)
@bp.route('/adc/acquiredata', methods=['GET'])
def adcacquiredata():
    adctag, adctype = '%s:%s' %(request.args.get('adcname'),session['user_name']), request.args.get('adctype')
    recordtime = si_parse(request.args.get('recordtime') + request.args.get('recordtimeunit')[0])
    recordsum = int(request.args.get('recordsum'))
    recordbuff = int(request.args.get('recordbuff')) # default: 32MB
    FPGA = request.args.get('FPGA')

    update_items = dict(OPT_DMA_Buffer_Size=recordbuff, FULL_SCALE=float(request.args.get('fullscale')), IQ_PAIR=[int(x) for x in request.args.get('iqpair').split(',')], FPGA=int(FPGA))
    [DATA, transferTime_sec, recordsPerBuff, buffersPerAcq] = ADC[adctype].AcquireData(adcboard[adctag], recordtime, recordsum, update_items)
    update_items.update(recordtime=request.args.get('recordtime'),recordsum=recordsum)
    set_status(request.args.get('adcname').split('-')[0], update_items, request.args.get('adcname').split('-')[1])

    global I_data, Q_data, t_data, TIME_RESOLUTION_NS
    I_data, Q_data, t_data = {}, {}, {}
    I_data[adctag] = DATA[:,:,0]
    Q_data[adctag] = DATA[:,:,1]
    t_data[adctag] = list(1 / ADC[adctype].sampling_rate(adcboard[adctag]) * linspace(1, len(DATA[0,:,0]), len(DATA[0,:,0])))
    TIME_RESOLUTION_NS = round(1 / ADC[adctype].sampling_rate(adcboard[adctag]) / 1e-9)
    recordtime_ns = TIME_RESOLUTION_NS * len(DATA[0,:,0])
    
    print(Fore.GREEN + "acquiredata: FPGA: %s(module: %s)" %(FPGA, adcboard[adctag].FPGA))
    print(Fore.GREEN + "Data-type: %s" %DATA.dtype) # numpy default: float64 (But we adapted to float32 for Quadro-GPU sake!)
    return jsonify(recordtime_ns=recordtime_ns, transferTime_sec=si_format(transferTime_sec,1), recordsPerBuff=recordsPerBuff, buffersPerAcq=buffersPerAcq)
@bp.route('/adc/playdata', methods=['GET'])
def adcplaydata():
    adctag = '%s:%s' %(request.args.get('adcname'),session['user_name'])
    average = int(request.args.get('average'))
    signal_processing = request.args.get('signal_processing')
    rotation_compensate_MHz = float(request.args.get('rotation_compensate'))
    ifreqcorrection_kHz = float(request.args.get('ifreqcorrection'))
    print(Fore.GREEN + "Signal Processing: %s" %signal_processing)
    tracenum = int(request.args.get('tracenum'))
    # data post-processing:
    if average or adcboard[adctag].FPGA: # NOTE: CUDA-averaging speed is bottlenecked by the Data Transfer Rate between GPU's and CPU's associated memory.
        trace_I = mean(I_data[adctag][:,:], 0)
        trace_Q = mean(Q_data[adctag][:,:], 0)
    else:
        trace_I = I_data[adctag][tracenum,:]
        trace_Q = Q_data[adctag][tracenum,:]

    # signal processing
    if signal_processing != "original":
        trace_I, trace_Q = pulse_baseband(signal_processing, trace_I, trace_Q, rotation_compensate_MHz, ifreqcorrection_kHz, dt=TIME_RESOLUTION_NS)

    trace_A = sqrt(power(trace_I, 2) + power(trace_Q, 2))
    t = t_data[adctag]
    # print(Fore.CYAN + "plotting trace #%s"%tracenum)
    log = pauselog() #disable logging (NOT applicable on Apache)

    adc_1Ddata[adctag] = dict(t=t, I=list(trace_I.astype(float64)), Q=list(trace_Q.astype(float64)))

    return jsonify(log=str(log), I=list(trace_I.astype(float64)), Q=list(trace_Q.astype(float64)), A=list(trace_A.astype(float64)), t=t) # JSON only supports float64 conversion (to str-list eventually)
# export to mat
@bp.route('/adc/export/1dmat', methods=['GET'])
def adc_export_1dmat():
    adctag = '%s:%s' %(request.args.get('adcname'),session['user_name'])
    set_mat(adc_1Ddata[adctag], '1Dadc[%s].mat'%adctag.replace(':','-')) # colon is not allowed in filename
    status = "adc-mat written"
    print(Fore.GREEN + "User %s has setup MAT-FILE in ALZDG-%s" %(adctag.split(':')[1],adctag.split(':')[0]))
    return jsonify(status=status, adctag=adctag)

@bp.route('/adc/closet', methods=['GET'])
def adccloset():
    adctag, adctype = '%s:%s' %(request.args.get('adcname'),session['user_name']), request.args.get('adctype')
    status = ADC[adctype].close(adcboard[adctag], adctag.split('-')[1].split(':')[0])
    acting("CLOSING ADC: %s" %(request.args.get('adcname')))
    del adcboard[adctag]
    return jsonify(message=status)
@bp.route('/adc/testing', methods=['GET'])
def adctesting():
    adctag, adctype = '%s:%s' %(request.args.get('adcname'),session['user_name']), request.args.get('adctype')
    status = ADC[adctype].test(adcboard[adctag])
    return jsonify(message=status)
@bp.route('/adc/get', methods=['GET'])
def adcget():
    adctag, adctype = '%s:%s' %(request.args.get('adcname'),session['user_name']), request.args.get('adctype')
    adc_history = get_status(request.args.get('adcname').split('-')[0], request.args.get('adcname').split('-')[1])
    message = {}
    try:
        message['model'] = ADC[adctype].model(adcboard[adctag])[1]['IDN']
        if adctype=="ALZDG": message['sampling_rate'] = '1GSPS'
        elif adctype=="SDDIG": message['sampling_rate'] = '500MSPS'
        else: message['sampling_rate'] = 'SPEC NOT FOUND INSIDE DATABASE!'
    except:
        message = dict(status='%s is not connected or busy or error' %request.args.get('adcname'))
    print("message: %s" %message)
    return jsonify(message=message, adc_history=adc_history)
# endregion

# region: NA (user-specific, Generalized)
def na_container():
    global NA, nabench, freqrange
    try: print(Fore.GREEN + "Connected NA: %s" %nabench.keys())
    except: NA, nabench, freqrange = {}, {}, {}
    return
@bp.route('/na', methods=['GET'])
def na(): 
    na_container()
    return render_template("blog/machn/na.html")
@bp.route('/na/log', methods=['GET'])
def nalog():
    log = get_status(request.args.get('natype'))
    return jsonify(log=log)
@bp.route('/na/connect', methods=['GET'])
def naconnect():
    na_container()
    naname = request.args.get('naname')
    natag = '%s:%s' %(naname,session['user_name'])
    natype, nalabel, nauser = natag.split('-')[0], natag.split('-')[1].split(':')[0], natag.split('-')[1].split(':')[1]
    linkedna = ['%s-%s'%(x.split('-')[0],x.split('-')[1].split(':')[0]) for x in nabench.keys()]
    if naname not in linkedna and int(g.user['instrument'])>=2:
        '''get in if not currently initiated'''
        try:
            NA[natype] = im("pyqum.instrument.machine.%s" %natype)
            nabench[natag] = NA[natype].Initiate(reset=False, which=nalabel)
            message = "%s is successfully initiated by %s" %(naname,nauser)
            status = "connected"
            acting("CONNECTING NA: %s" %(request.args.get('naname')))
        except:
            message = "Please check if %s's connection configuration is OK or is it being used!" %(naname)
            status = 'error'
    else:
        # Check who is currently using the instrument:
        try:
            db = get_db()
            instr_user = db.execute('SELECT u.username FROM user u JOIN machine m ON m.user_id = u.id WHERE m.codename = ?', ('%s_%s'%(natype,nalabel),)).fetchone()[0]
            close_db()
            message = "%s is being connected to %s" %(naname,instr_user)
        except(TypeError):
            instr_user = None
            message = "INSTRUMENT IS COMING SOON" # in the process of procurement

        # Connecting or Waiting or Forbidden?
        if instr_user == session['user_name']: status = 'connected'
        elif int(g.user['instrument'])>=2: status = 'waiting'
        else: message, status = 'NOT ENOUGH CLEARANCE', 'forbidden'
    return jsonify(message=message,status=status)
@bp.route('/na/closet', methods=['GET'])
def nacloset():
    natag, natype = '%s:%s' %(request.args.get('naname'),session['user_name']), request.args.get('natype')
    try: 
        status = NA[natype].close(nabench[natag], which=natag.split('-')[1].split(':')[0])
        acting("CLOSING NA: %s" %(request.args.get('naname')))
    except: 
        status = "Connection lost"
        pass
    del nabench[natag], freqrange[natag]
    return jsonify(message=status)
@bp.route('/na/set/freqrange', methods=['GET'])
def nasetfreqrange():
    natag, natype = '%s:%s' %(request.args.get('naname'),session['user_name']), request.args.get('natype')
    freqrange[natag] = waveform(request.args.get('freqrange'))
    frequnit = request.args.get('frequnit').replace("Hz","")
    NA[natype].sweep(nabench[natag], action=['Set', 'ON', freqrange[natag].count])
    fstart, fstop = si_parse(str(freqrange[natag].data[0])+frequnit), si_parse(str(freqrange[natag].data[-1])+frequnit)
    NA[natype].sweep(nabench[natag], action=['Set', 'ON', freqrange[natag].count])
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
    mreturn = NA[natype].setrace(nabench[natag], Mparam=mparam)
    print("sweeping %s"%mreturn)
    NA[natype].rfports(nabench[natag], action=['Set', 'ON'])
    stat = NA[natype].measure(nabench[natag])
    NA[natype].autoscal(nabench[natag])
    # Collecting Data:
    NA[natype].dataform(nabench[natag], action=['Set', 'REAL'])
    yI, yQ, yAmp, yPha = IQAParray(array(NA[natype].sdata(nabench[natag])))
    NA[natype].rfports(nabench[natag], action=['Set', 'OFF'])
    print(Fore.CYAN + "Collected %s Data" %len(yAmp))
    xdata = list(freqrange[natag].data)
    yUPha = list(UnwraPhase(xdata, yPha))
    return jsonify(sweep_complete=bool(stat), xdata=xdata, yAmp=list(yAmp), yUPha=yUPha)
@bp.route('/na/get', methods=['GET'])
def naget():
    natag, natype = '%s:%s' %(request.args.get('naname'),session['user_name']), request.args.get('natype')
    print(Fore.YELLOW + "Getting %s attributes"%(natag))
    message = {}
    try:
        start_val, start_unit = si_format(float(NA[natype].linfreq(nabench[natag])[1]['START']),precision=7).split(" ")
        stop_val, stop_unit = si_format(float(NA[natype].linfreq(nabench[natag])[1]['STOP']),precision=7).split(" ")
        stop_conversion = si_parse("1%s"%stop_unit) / si_parse("1%s"%start_unit) # equalizing both unit-range:
        step_points = int(NA[natype].sweep(nabench[natag])[1]['POINTS']) - 1 # step-points in waveform
        message['freq_waveform'] = "%s to %s * %s" %(start_val, float(stop_val)*stop_conversion, step_points)
        message['freq_unit'] = start_unit
        freqrange[natag] = waveform(message['freq_waveform']) # for NA-PLOT

        message['power'] = "%.1f dBm" %float(NA[natype].power(nabench[natag])[1]['LEVEL']) # power (fixed unit)
        message['ifb'] = si_format(float(NA[natype].ifbw(nabench[natag])[1]['BANDWIDTH']),precision=0) + "Hz" # ifb (adjusted by si_prefix)
        message['s21'], message['s11'] = int('S21' in NA[natype].getrace(nabench[natag])), int('S11' in NA[natype].getrace(nabench[natag]))
        message['s12'], message['s22'] = int('S12' in NA[natype].getrace(nabench[natag])), int('S22' in NA[natype].getrace(nabench[natag]))
        message['s43'], message['s33'] = int('S43' in NA[natype].getrace(nabench[natag])), int('S33' in NA[natype].getrace(nabench[natag]))
        message['s34'], message['s44'] = int('S34' in NA[natype].getrace(nabench[natag])), int('S44' in NA[natype].getrace(nabench[natag]))
        message['swptime'] = NA[natype].sweep(nabench[natag])[1]['TIME']
    except:
        raise
        message = dict(status='%s is not connected' %natype)
    return jsonify(message=message)
# endregion

# region: SA (user-specific, Generalized, Databased)
def sa_container():
    global sabench, SA
    try: print(Fore.GREEN + "Connected SA: %s" %sabench.keys())
    except: sabench, SA = {}, {}
    return
@bp.route('/sa', methods=['GET'])
def sa(): 
    sa_container()
    return render_template("blog/machn/sa.html")
@bp.route('/sa/log', methods=['GET'])
def salog():
    log = get_status(request.args.get('satype'))
    return jsonify(log=log)
@bp.route('/sa/connect', methods=['GET'])
def saconnect():
    sa_container()
    saname = request.args.get('saname') # name: <type>-<label>
    satag = '%s:%s' %(saname,session['user_name']) # tag: <type>-<label>:<user>
    satype, salabel, sauser = satag.split('-')[0], satag.split('-')[1].split(':')[0], satag.split('-')[1].split(':')[1]
    # NOTE: LIMIT down to Single-User ONLY per Instrument:
    # linkedsa = ['%s-%s'%(x.split('-')[0],x.split('-')[1].split(':')[0]) for x in sabench.keys()] #OLD version without Database
    # if saname not in linkedsa and int(g.user['instrument'])>=3: #OLD version without Database
    if not address().macantouch([saname.replace('-','_')]) and int(g.user['instrument'])>=3:
        '''get in if not currently initiated'''
        try:
            SA[satype] = im("pyqum.instrument.machine.%s" %satype)
            sabench[satag] = SA[satype].Initiate(which=salabel)
            # g.shared_sabench = sabench[satag] # Sharing handle across pages: become None?
            message = "%s is successfully initiated by %s" %(saname,sauser)
            status = "connected"
            acting("CONNECTING SA: %s" %(request.args.get('saname')))
        except:
            raise
            message = "Please check if %s's connection configuration is OK or is it being used!" %(saname)
            status = 'error'
    else:
        # Check who is currently using the instrument:
        try:
            db = get_db()
            instr_user = db.execute('SELECT u.username FROM user u JOIN machine m ON m.user_id = u.id WHERE m.codename = ?', ('%s_%s'%(satype,salabel),)).fetchone()[0]
            close_db()
            message = "%s is being connected to %s" %(saname,instr_user)
        except(TypeError):
            instr_user = None
            message = "INSTRUMENT IS COMING SOON" # in the process of procurement

        # Connecting or Waiting or Forbidden?
        if instr_user == session['user_name']: status = 'connected'
        elif int(g.user['instrument'])>=3: status = 'waiting'
        else: message, status = 'NOT ENOUGH CLEARANCE', 'forbidden'
    return jsonify(message=message,status=status)
@bp.route('/sa/closet', methods=['GET'])
def sacloset():
    satag, satype = '%s:%s' %(request.args.get('saname'),session['user_name']), request.args.get('satype')
    try: 
        status = SA[satype].close(sabench[satag], satag.split('-')[1].split(':')[0])
        acting("CLOSING SA: %s" %(request.args.get('saname')))
    except: 
        status = "Connection lost"
        pass
    del sabench[satag]
    return jsonify(message=status)

@bp.route('/sa/set/powa', methods=['GET'])
def sasetpowa():
    satag, satype = '%s:%s' %(request.args.get('saname'),session['user_name']), request.args.get('satype')
    powa = request.args.get('powa')
    stat = SA[satype].power(sabench[satag], action=['Set', powa])
    message = 'power: %s <%s>' %(stat[1], stat[0])
    return jsonify(message=message)

@bp.route('/sa/get', methods=['GET'])
def saget():
    satag, satype = '%s:%s' %(request.args.get('saname'),session['user_name']), request.args.get('satype')
    message = {}
    try:
        start_val, start_unit = si_format(float(SA[satype].linfreq(sabench[satag])[1]['START']),precision=1).split(" ")
        stop_val, stop_unit = si_format(float(SA[satype].linfreq(sabench[satag])[1]['STOP']),precision=1).split(" ")
        stop_conversion = si_parse("1%s"%stop_unit) / si_parse("1%s"%start_unit) # equalizing both unit-range:
        message['start-frequency'] = "%s %sHz" %(start_val,start_unit) # start-frequency
        message['stop-frequency'] = "%s %sHz" %(float(stop_val)*stop_conversion,start_unit) # stop-frequency
        message['step-points'] = int(SA[satype].sweep(sabench[satag])[1]['POINTS']) - 1 # step-points in waveform
        message['power'] = "%.1f dBm" %float(SA[satype].power(sabench[satag])[1]['LEVEL']) # power (fixed unit)
        message['ifb'] = si_format(float(SA[satype].ifbw(sabench[satag])[1]['BANDWIDTH']),precision=0) + "Hz" # ifb (adjusted by si_prefix)
        message['s21'], message['s11'] = int('S21' in SA[satype].getrace(sabench[satag])), int('S11' in SA[satype].getrace(sabench[satag]))
        message['s12'], message['s22'] = int('S12' in SA[satype].getrace(sabench[satag])), int('S22' in SA[satype].getrace(sabench[satag]))
        message['s43'], message['s33'] = int('S43' in SA[satype].getrace(sabench[satag])), int('S33' in SA[satype].getrace(sabench[satag]))
        message['s34'], message['s44'] = int('S34' in SA[satype].getrace(sabench[satag])), int('S44' in SA[satype].getrace(sabench[satag]))
    except:
        # raise
        message = dict(status='%s is not connected' %satype)
    return jsonify(message=message)
# endregion

# region: BDR
global category
category = ['ROLE','CH','DC','SG','NA','DAC','ADC','SA','SC']
@bp.route('/bdr')
def bdr():
    if int(g.user['instrument'])>=1:
        # 0. monitoring traffic:
        print(Fore.GREEN + "User %s is visiting BDR using IP: %s\n" %(session['user_name'], request.remote_addr))
        
        # 1. OWNED samples:
        owned_new_samples = [s['samplename'] for s in g.samples if s['registered'].strftime("%Y-%m-%d")==g.latest_date]
        # 2. SHARED co-samples:
        shared_new_samples = [s['samplename'] for s in g.cosamples if s['registered'].strftime("%Y-%m-%d")==g.latest_date]
        # 3. SERVICE samples: (Training & Hero samples are to be categorized as SERVICE type of sample)
        global service_samples
        service_samples = [s['samplename'] for s in (g.samples + g.cosamples) if int(s['level'])>1]

        # service_samples = ['Sam', 'Same01', 'IDLE', 'DR-RFcable', '3SXQ-Al-Si-19-1']
        recent_samples = list(set(owned_new_samples).union(set(shared_new_samples))) + service_samples
        loaded = len(recent_samples) - len(service_samples)

        # 3. Wiring settings:
        machine_list = [x['codename'] for x in g.machlist]
        systemlist = [x['system'] for x in get_db().execute('SELECT system FROM queue').fetchall()]
        close_db()
        try: queue = get_status("MSSN")[session['user_name']]['queue']
        except: queue = 'CHAR0' # default
        
        DR_platform = int(get_status("WEB")['port']) - 5300
        return render_template("blog/machn/bdr.html", DR_platform=DR_platform, loaded=loaded, recent_samples=recent_samples, machine_list=machine_list, systemlist=systemlist, queue=queue, \
            category=category, CHAR0_sample=g.CHAR0_sample, CHAR1_sample=g.CHAR1_sample, QPC0_sample=g.QPC0_sample, QPC1_sample=g.QPC1_sample)
    else: abort(404)
@bp.route('/bdr/init', methods=['GET'])
def bdrinit():
    designation = request.args.get('designation')
    global b
    b = bluefors(designation)
    return jsonify(Days=b.Days)
@bp.route('/bdr/history', methods=['GET'])
def bdrhistory():
    designation = request.args.get('designation')
    global b, bdrlogs
    wday = int(request.args.get('wday'))
    P_Ch = int(request.args.get('P_Ch'))
    T_Ch = int(request.args.get('T_Ch'))
    P_Ch2 = int(request.args.get('P_Ch2'))
    T_Ch2 = int(request.args.get('T_Ch2'))
    OptionS = request.args.get('OptS')
    OptionV = request.args.get('OptV')

    b = bluefors(designation)
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
@bp.route('/bdr/history/ziplog', methods=['GET'])
def bdrhistoryziplog():
    logtype = request.args.get('logtype')
    designation = request.args.get('designation')
    print(Fore.CYAN + "User %s is ziplogging DR-%s's %s-DATA" %(session['user_name'],designation,logtype))
    if logtype.upper()=='P': LogDir = b.LogPath / b.Date
    elif logtype.upper()=='T': LogDir = b.LogPath / b._TPath / b.Date
    else: abort(Response('PLS Use Main Door to get in!'))
    zipname = "%s,DR-%s,(%s)-%s-LOG"%(session['user_name'],designation,b.Date,logtype.upper())
    bdr_zip_log(zipname, LogDir)
    # NOTE: DR-Alice will always get BOTH P- and T-LOG altogether in one ZIP-File.
    return jsonify(qumport=int(get_status("WEB")['port']), zipname=zipname)

# SAMPLE SEATS IN BDR:
@bp.route('/bdr/samples/queues', methods=['GET'])
def bdrsamplesqueues():
    db = get_db()
    bdrqlist = db.execute("SELECT system, samplename FROM queue ORDER BY id ASC").fetchall()
    close_db()
    bdrqlist = [dict(x) for x in bdrqlist]
    return jsonify(bdrqlist=bdrqlist, services=service_samples)
@bp.route('/bdr/samples/allocate', methods=['GET'])
def bdrsamplesallocate():
    set_system = request.args.get('set_system')
    set_sample = request.args.get('set_sample')
    if int(g.user['management'])>=3:
        try:
            db = get_db()
            if set_sample == "null": db.execute("UPDATE queue SET samplename = null WHERE system = ?", (set_system,))
            else: db.execute("UPDATE queue SET samplename = ? WHERE system = ?", (set_sample,set_system,))
            db.commit()
            close_db()
            status = "User %s has set sample %s into system %s" %(g.user['username'],set_sample,set_system)
            acting("Setting sample %s into system %s" %(set_sample,set_system))
        except: status = "COULD NOT COMMIT TO DATABASE"
        print(Fore.YELLOW + status)
    else: 
        status = "User %s does not have enough Management Clearance" %g.user['username']
        print(Fore.RED + status)
    
    return jsonify(status=status)

# ADMIN PAGE TO ASSIGN INSTRUMENTs FROM THE TOP-MOST UI:
@bp.route('/bdr/wiring/instruments', methods=['GET'])
def bdr_wiring_instruments():
    qsystem = request.args.get('qsystem')
    inst_list = inst_order(qsystem)
    instr_organized, instr_tabulated = {}, {}
    for cat in category: instr_organized[cat] = inst_order(qsystem,cat,False)
    print(Fore.CYAN + "Organized instruments: %s"%instr_organized)
    
    modules_mismatch, channels_mismatch = 0, 0
    if 'DUMMY_1' in instr_organized['ROLE']: pass
    else:
        # Check CH & ROLE structure alignment:
        for cat in category: instr_tabulated[cat] = inst_order(qsystem,cat)
        for key, value in instr_tabulated['ROLE'].items():
            modules_mismatch += len(value) - len(instr_tabulated['CH'][key])
            # print(Fore.YELLOW + "%s's ROLE: %s, %s's CH: %s" %(key, len(value), key, len(loads(instr_tabulated['CH'])[key])))
            
            for idx, channel_composition in enumerate(value):
                channels_mismatch += len(channel_composition) - len(instr_tabulated['CH'][key][idx])
                # print(Fore.YELLOW + "%s's ROLE's module-%s: %s, %s's CH's module-%s: %s" %(key, idx, len(channel_composition), key, idx, len(loads(instr_tabulated['CH'])[key][idx])))
        
    return jsonify(category=category, inst_list=inst_list, instr_organized=instr_organized, modules_mismatch=modules_mismatch, channels_mismatch=channels_mismatch)
@bp.route('/bdr/wiring/set/instruments', methods=['GET'])
def bdr_wiring_set_instruments():
    qsystem = request.args.get('qsystem')
    instr_organized = loads(request.args.get('instr_organized'))
    try:
        if int(g.user['management'])>=3:
            for key, val in instr_organized.items(): 
                inst_designate(qsystem, key, val)
        message = "%s's instrument assignment has been set successfully" %qsystem
        acting(message)
    except:
        message = "database error"
    return jsonify(message=message)
@bp.route('/bdr/wiring/check/instruments', methods=['GET'])
def bdr_wiring_check_instruments():
    instr_set = request.args.get('instr_set').upper() # CSV-string
    CAT = request.args.get('cat')
    message = "working on %s" %CAT

    if CAT=="CH" or CAT=="ROLE": pass # virtual-instruments
    else:
        instr_set = instr_set.replace(" ","") # omit spaces (only for real-instrument's list)
        for instr in instr_set.split(','):
            if instr.replace('_','-') not in g.instlist: # All registered machines 
                instr_set = instr_set.replace(instr,'')
                message = "Make sure %s is in ALL-MACHINE-LIST" %(instr)

    while ',,' in instr_set: instr_set = instr_set.replace(',,',',') # omit extra commas if any
    if instr_set[-1]==',': instr_set = instr_set[:-1] # omit last comma if any
    return jsonify(checked_instr_set=instr_set, message=message)

# endregion

# region: DC
@bp.route('/dc', methods=['GET'])
def dc():
    if int(g.user['instrument'])>=2:
        print("loading dc.html")
        return render_template("blog/machn/dc.html")
    else: abort(404)
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
    pwidth = float(request.args.get("pwidth")) #ms #PENDING: make it into the update_settings dict as optional parameter to accommodate all sort of DC sources.
    swprate = float(request.args.get("swprate")) #V/s
    stat = YOKO.sweep(yokog, vwave, update_settings=dict(sweeprate=swprate))
    return jsonify(SweepTime=stat[1])
@bp.route('/dc/yokogawa/vpulse', methods=['GET'])
def dc_yokogawa_vpulse():
    global yokog
    YOKO.output(yokog, 1)
    vset = float(request.args.get('vset'))
    pwidth = float(request.args.get("pwidth"))
    stat = YOKO.sweep(yokog, "%sto0*1"%vset, update_settings=dict(sweeprate=abs(vset)*60))
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
# SRSDC
@bp.route('/dc/srsdc', methods=['GET'])
def dcsrsdc():
    srsdcstat = request.args.get('srsdcstat')
    if srsdcstat == 'true':
        global keith
        keith = KEIT.Initiate()
    elif srsdcstat == 'false':
        KEIT.close(keith, True)
    return jsonify()
@bp.route('/dc/srsdc/vset', methods=['GET'])
def dc_srsdc_vset():
    vset = float(request.args.get('vset'))
    
    
    return jsonify()
# endregion


# Download File:
@bp.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = device_port("PORTAL") # The path is now stored in the SQL Database
    print(Fore.GREEN + "User %s is downloading %s from %s" %(session['user_name'], filename, uploads))
    acting("Downloading %s from %s" %(filename, uploads))
    return send_from_directory(directory=uploads, path=filename)



print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this



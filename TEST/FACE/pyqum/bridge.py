# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name

from json import loads
from importlib import import_module as im
from flask import Flask, request, render_template, Response, redirect, Blueprint, jsonify, session, send_from_directory, abort, g
from pyqum.instrument.logger import address, get_status, set_status, status_code, output_code
from pyqum.instrument.toolbox import waveform

# Error handling
from contextlib import suppress

# Scientific
from scipy import constants as cnst
#from si_prefix import si_format, si_parse # Not be used
from numpy import cos, sin, pi, polyfit, poly1d, array, roots, isreal, sqrt, mean

# Load instruments
from pyqum.instrument.machine import TKAWG, PSGA, MXA
from pyqum.directive.calibrate import IQ_Cal

encryp = 'ghhgjadz'
bp = Blueprint(myname, __name__, url_prefix='/bridge')

# Main
@bp.route('/')
def show():
    with suppress(KeyError):
        print(Fore.LIGHTBLUE_EX + "USER " + Fore.YELLOW + "%s "%session['user_name'] + Fore.LIGHTBLUE_EX + "has just logged in as Guest #%s!"%session['user_id'])
        # Security implementation:
        if not g.user['instrument']:
            abort(404)
        return render_template("blog/bridg/bridge.html")
    return("<h3>WHO ARE YOU?</h3><h3>Please Kindly Login!</h3><h3>Courtesy from <a href='http://qum.phys.sinica.edu.tw:%s/auth/login'>HoDoR</a></h3>" %get_status("WEB")["port"])

# IQ-CALIBRATION:
def iqcal_container():
    global IQCAL_instance, saname
    try: print(Fore.GREEN + "Connected IQCAL: %s" %IQCAL_instance.keys())
    except: IQCAL_instance = {}
    saname = 'MXA_1' # PENDING: ADD Options to choose from available SA-list. (via database)
    return
@bp.route('/iqcal', methods=['POST', 'GET'])
def iqcal(): 
    iqcal_container()
    return render_template("blog/bridg/iqcal.html", current_usr=session['user_name'])
@bp.route('/iqcal/load/mixermodules', methods=['GET'])
def iqcal_load_mixermodules():
    mixermodule_list = [x for x in get_status("MIXER").keys()]
    return jsonify(mixermodule_list=mixermodule_list)
@bp.route('/iqcal/check/daclive', methods=['GET'])
def iqcal_check_daclive():
    RELAY_dict = get_status("RELAY")
    live_dac_channel = [x.split('dacupdate_')[1] for x in RELAY_dict.keys() if ('dacupdate_' in x and RELAY_dict[x]==1)]
    print("Currently Live DAC-CH: %s" %(live_dac_channel))
    return jsonify(live_dac_channel=live_dac_channel)
@bp.route('/iqcal/load/calibrate', methods=['GET'])
def iqcal_load_calibrate():
    mixermodule_key = request.args.get('mixermodule_key')
    try: mixermodule_val = get_status("MIXER")['%s'%mixermodule_key]
    except(KeyError): mixermodule_val = "no-module-found"
    return jsonify(mixermodule_val=mixermodule_val)
@bp.route('/iqcal/manual/calibrate', methods=['GET'])
def iqcal_manual_calibrate():
    mixermodule_key = request.args.get('mixermodule_key')
    mixermodule_val = request.args.get('mixermodule_val')
    LO_GHz = float(request.args.get('LO_frequency_GHz'))
    IF_GHz = float(request.args.get('IF_frequency_MHz'))/1000
    npoints = int(request.args.get('Sweep_points'))
    RBW_kHz = int(request.args.get('RBW_kHz'))
    AveCount = int(request.args.get('AveCount'))
    set_status("MIXER", {'%s'%mixermodule_key : '%s'%mixermodule_val})
    
    try:
        # Load SA Respond:
        # a. Zero-span Sweep:
        freq_list = [LO_GHz-2*IF_GHz, LO_GHz-IF_GHz, LO_GHz, LO_GHz+IF_GHz, LO_GHz+2*IF_GHz]
        powa_list = []
        for freq in freq_list:
            powa_list.append(SA.fpower(iqcal_sabench[session['user_name']], frequency_GHz=freq, resBW_kHz=RBW_kHz, ave_points=4, ave_counts=AveCount)[0])
        # b. Full Spectrum:
        SA.sweep(iqcal_sabench[session['user_name']], action=['Set','%s'%(npoints)])
        fstart, fstop = freq_list[0] - IF_GHz / 2, freq_list[-1] + IF_GHz / 2
        SA.linfreq(iqcal_sabench[session['user_name']], action=['Set', '%sGHz'%fstart, '%sGHz'%fstop]) # F-sweep
        SA.rbw(iqcal_sabench[session['user_name']], action=['Set','100kHz'])
        SA.measure(iqcal_sabench[session['user_name']])
        SA.autoscal(iqcal_sabench[session['user_name']])
        full_spectrum_x = waveform('%s to %s * %s' %(fstart, fstop, npoints-1)).data
        full_spectrum_y = SA.sdata(iqcal_sabench[session['user_name']], mode="")
    except: 
        freq_list, powa_list, full_spectrum_x, full_spectrum_y = [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]

    return jsonify(freq_list=freq_list, powa_list=powa_list, full_spectrum_x=full_spectrum_x, full_spectrum_y=full_spectrum_y)
@bp.route('/iqcal/manual/sa/connect', methods=['GET'])
def iqcal_manual_saconnect():
    iqcal_container()
    if saname not in IQCAL_instance.keys() and not address().macantouch([saname]) and int(g.user['instrument'])>=3:
        IQCAL_instance[saname] = session['user_name']
        try:
            global iqcal_sabench, SA
            iqcal_sabench, SA = {}, im("pyqum.instrument.machine.%s"%(saname.split("_")[0]))
            iqcal_sabench[session['user_name']] = SA.Initiate(which=saname.split("_")[1], reset=True)
            SA.preamp(iqcal_sabench[session['user_name']], action=['Set','OFF'])
            SA.preamp_band(iqcal_sabench[session['user_name']], action=['Set','FULL'])
            SA.attenuation(iqcal_sabench[session['user_name']], action=['Set','0dB'])
            SA.attenuation_auto(iqcal_sabench[session['user_name']], action=['Set','ON'])
            status = "%s initiated by %s"%(saname, session['user_name'])
        except:
            status = "Please check if %s's connection configuration is OK" %(saname)
    else: status = "%s already connected to %s"%(saname, IQCAL_instance[saname])
    return jsonify(status=status)
@bp.route('/iqcal/manual/sa/closet', methods=['GET'])
def iqcal_manual_sacloset():
    status = SA.close(iqcal_sabench[session['user_name']],which=1,reset=False)
    del iqcal_sabench[session['user_name']], IQCAL_instance[saname]
    return jsonify(status=status)
@bp.route('/iqcal/auto/calibrate/run', methods=['GET'])
def iqcal_auto_calibrate_run():
    iqcal_container()
    if saname not in IQCAL_instance.keys() and not address().macantouch([saname]) and int(g.user['instrument'])>=3:
        IQCAL_instance[saname] = session['user_name']

        # IQ Auto-Calibration routine:
        Conv_frequency_GHz = float(request.args.get('Conv_frequency_GHz'))
        IF_rotation_MHz = int(request.args.get('IF_rotation_MHz')) # +/-: directional
        LO_power_dBm = float(request.args.get('LO_power_dBm'))
        IF_period_ns = int(request.args.get('IF_period_ns'))
        IF_scale = float(request.args.get('IF_scale'))
        Mixer_module = request.args.get('Mixer_module')
        Wiring_config = loads(request.args.get('Wiring_config'))
        Channels_group = int(request.args.get('Channels_group')) # 1:1,2; 2:2,3; 3:3,4; ...
        C = IQ_Cal(Conv_frequency_GHz, LO_power_dBm, IF_rotation_MHz, IF_period_ns, IF_scale, Mixer_module, Wiring_config, Channels_group)
        C.run()
        C.close()

        del IQCAL_instance[saname]
        message="AUTO-IQCAL closed"
    else: message="%s is currently used by %s" %(saname, IQCAL_instance[saname])

    return jsonify(message=message)
@bp.route('/iqcal/auto/check/status', methods=['GET'])
def iqcal_auto_check_status():
    running = get_status("RELAY")["autoIQCAL"]
    iteration = get_status("RELAY")["autoIQCAL_iteration"]
    autoIQCAL_dur_s = get_status("RELAY")["autoIQCAL_dur_s"]
    autoIQCAL_frequencies = get_status("RELAY")["autoIQCAL_frequencies"]
    autoIQCAL_spectrum = get_status("RELAY")["autoIQCAL_spectrum"]
    return jsonify(running=running, iteration=iteration, autoIQCAL_dur_s=autoIQCAL_dur_s, \
                    autoIQCAL_frequencies=autoIQCAL_frequencies, autoIQCAL_spectrum=autoIQCAL_spectrum)
@bp.route('/iqcal/auto/calibrate/stop', methods=['GET'])
def iqcal_auto_calibrate_stop():
    set_status("RELAY", dict(autoIQCAL=0))
    return jsonify(message="AUTO-IQCAL will stop on the next iteration. Please wait...")




print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this



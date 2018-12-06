# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name

import requests
from flask import Flask, request, render_template, Response, redirect, Blueprint, jsonify
from pyqum.instrument.logger import address, get_status, set_status, status_code, output_code

# This will run at server startup
# Modulars first, only then Benchtops (if and only if we use render_template)
from pyqum.instrument.modular import AWG, VSA
AWG.test(False) #seems like AWG's working-instance works differently than VSA's
# awgsess = AWG.InitWithOptions()
# vsasess = VSA.InitWithOptions()
from pyqum.instrument.benchtop import MXG, ESG, DSO
# esgbench = ESG.Initiate()
# mxgbench = MXG.Initiate()
# dsobench = DSO.Initiate()

bp = Blueprint(myname, __name__, url_prefix='/mach')

# Main
@bp.route('/')
def show():
    return render_template("blog/machn/machine.html")

# TEST
@bp.route('/test', methods=['POST', 'GET'])
def test(): 
    x = 100
    return render_template("blog/machn/test.html", x=x)

# AWG
@bp.route('/awg', methods=['GET'])
def awg(): 
    return render_template("blog/machn/awg.html")
@bp.route('/awg/log', methods=['GET'])
def awglog():
    log = get_status('AWG')
    return jsonify(log=log)
@bp.route('/awg/reset', methods=['GET'])
def awgreset():
    global awgsess
    awgsess = AWG.InitWithOptions()
    return jsonify(message=awgsess)
@bp.route('/awg/close', methods=['GET'])
def awgclose():
    global awgsess
    status = AWG.close(awgsess)
    return jsonify(message=status)
@bp.route('/awg/settings', methods=['GET'])
def awgsettings():
    global awgsess
    message = []
    active = request.args.get('active')
    stat = AWG.active_marker(awgsess, action=['Set',active])
    message += ['active marker: ' + status_code(stat[0])]
    delay = request.args.get('delay')
    stat = AWG.marker_delay(awgsess, action=['Set',float(delay)])
    message += ['marker delay: ' + status_code(stat[0])]
    pulsew = request.args.get('pulsew')
    stat = AWG.marker_pulse_width(awgsess, action=['Set',float(pulsew)])
    message += ['marker pulse width: ' + status_code(stat[0])]
    source = request.args.get('source')
    stat = AWG.marker_source(awgsess, action=['Set',int(source)])
    message += ['marker source: ' + status_code(stat[0])]
    predist = request.args.get('predist')
    stat = AWG.predistortion_enabled(awgsess, action=['Set',int(predist)])
    message += ['predistortion enabled: ' + status_code(stat[0])]
    return jsonify(message=message)
@bp.route('/awg/about', methods=['GET'])
def awgabout():
    global awgsess
    message = []
    status = AWG.model(awgsess) # model
    message += ['Model: %s (%s)' % (status[1], status_code(status[0]))]
    status = AWG.active_marker(awgsess) # active marker
    message += ['Active Marker: %s (%s)' % (status[1], status_code(status[0]))]
    status = AWG.marker_delay(awgsess) # marker delay
    message += ['Marker Delay: %s (%s)' % (status[1], status_code(status[0]))]
    status = AWG.marker_pulse_width(awgsess) # marker pulse width
    message += ['Marker Pulse Width: %s (%s)' % (status[1], status_code(status[0]))]
    status = AWG.marker_source(awgsess) # marker source
    message += ['Marker Source: %s (%s)' % (status[1], status_code(status[0]))]
    status = AWG.predistortion_enabled(awgsess) # predistortion enabled
    message += ['Predistortion Enabled: %s (%s)' % (status[1], status_code(status[0]))]
    return jsonify(message=message)

# VSA
@bp.route('/vsa', methods=['GET'])
def vsa(): 
    return render_template("blog/machn/vsa.html")
@bp.route('/vsa/log', methods=['GET'])
def vsalog():
    log = get_status('VSA')
    return jsonify(log=log)
@bp.route('/vsa/reset', methods=['GET'])
def vsareset():
    global vsasess
    vsasess = VSA.InitWithOptions()
    return jsonify(message=vsasess)
@bp.route('/vsa/close', methods=['GET'])
def vsaclose():
    global vsasess
    status = VSA.close(vsasess)
    return jsonify(message=status)
@bp.route('/vsa/settings', methods=['GET'])
def vsasettings():
    global vsasess
    message = []
    acquis = request.args.get('acquis')
    stat = VSA.acquisition_time(vsasess, action=['Set',float(acquis)])
    message += ['acquisition time: ' + status_code(stat[0])]
    return jsonify(message=message)
@bp.route('/vsa/about', methods=['GET'])
def vsaabout():
    global vsasess
    message = []
    status = VSA.model(vsasess) # model
    message += ['Model: %s (%s)' % (status[1], status_code(status[0]))]
    status = VSA.resource_descriptor(vsasess) # resource descriptor
    message += ['Resource Descriptor: %s (%s)' % (status[1], status_code(status[0]))]
    status = VSA.acquisition_time(vsasess) # acquisition time
    message += ['Acquisition Time: %s (%s)' % (status[1], status_code(status[0]))]
    return jsonify(message=message)

# ESG
@bp.route('/esg', methods=['GET'])
def esg(): 
    return render_template("blog/machn/esg.html")
@bp.route('/esg/log', methods=['GET'])
def esglog():
    log = get_status('ESG')
    return jsonify(log=log)
@bp.route('/esg/reset', methods=['GET'])
def esgreset():
    global esgbench
    try:
        esgbench = ESG.Initiate()
        status = "Success"
    except: status = "Error"
    return jsonify(message=status)
@bp.route('/esg/close', methods=['GET'])
def esgclose():
    global esgbench
    status = ESG.close(esgbench)
    return jsonify(message=status)
@bp.route('/esg/settings', methods=['GET'])
def esgsettings():
    global esgbench
    message = []
    freq = request.args.get('freq')
    stat = ESG.frequency(esgbench, action=['Set',float(freq)])
    message += ['frequency (GHz): %s <%s>' %(stat[1], stat[0])]
    powa = request.args.get('powa')
    stat = ESG.power(esgbench, action=['Set',float(powa)])
    message += ['power (dBm): %s <%s>' %(stat[1], stat[0])]
    oupt = request.args.get('oupt')
    stat = ESG.output(esgbench, action=['Set',int(oupt)])
    message += ['RF output: %s <%s>' %(stat[1], stat[0])]
    return jsonify(message=message)
@bp.route('/esg/about', methods=['GET'])
def esgabout():
    global esgbench
    message = []
    status = ESG.model(esgbench) # model
    message += ['Model: %s (%s)' % (status[1], status[0])]
    status = ESG.frequency(esgbench) # frequency
    message += ['Frequency: %s (%s)' % (status[1], status[0])]
    status = ESG.power(esgbench) # power
    message += ['Power: %s (%s)' % (status[1], status[0])]
    status = ESG.output(esgbench) # output
    message += ['RF output: %s (%s)' % (output_code(status[1]), status[0])]
    return jsonify(message=message)

# MXG
@bp.route('/mxg', methods=['GET'])
def mxg():
    return render_template("blog/machn/mxg.html")
@bp.route('/mxg/log', methods=['GET'])
def mxglog():
    log = get_status('MXG')
    return jsonify(log=log)
@bp.route('/mxg/reset', methods=['GET'])
def mxgreset():
    global mxgbench
    try:
        mxgbench = MXG.Initiate()
        status = "Success"
    except: status = "Error"
    return jsonify(message=status)
@bp.route('/mxg/close', methods=['GET'])
def mxgclose():
    global mxgbench
    status = MXG.close(mxgbench)
    return jsonify(message=status)
@bp.route('/mxg/settings', methods=['GET'])
def mxgsettings():
    global mxgbench
    message = []
    freq = request.args.get('freq')
    stat = MXG.frequency(mxgbench, action=['Set', freq + "GHZ"])
    message += ['frequency (GHz): %s <%s>' %(stat[1], stat[0])]
    powa = request.args.get('powa')
    stat = MXG.power(mxgbench, action=['Set',float(powa)])
    message += ['power (dBm): %s <%s>' %(stat[1], stat[0])]
    oupt = request.args.get('oupt')
    stat = MXG.output(mxgbench, action=['Set',int(oupt)])
    message += ['RF output: %s <%s>' %(stat[1], stat[0])]
    return jsonify(message=message)
@bp.route('/mxg/about', methods=['GET'])
def mxgabout():
    global mxgbench
    message = []
    status = MXG.model(mxgbench) # model
    message += ['Model: %s (%s)' % (status[1], status[0])]
    status = MXG.frequency(mxgbench) # frequency
    message += ['Frequency: %s (%s)' % (status[1], status[0])]
    status = MXG.power(mxgbench) # power
    message += ['Power: %s (%s)' % (status[1], status[0])]
    status = MXG.output(mxgbench) # output
    message += ['RF output: %s (%s)' % (output_code(status[1]), status[0])]
    return jsonify(message=message)

# DSO
@bp.route('/dso', methods=['GET'])
def dso():
    # default input/select value (pave way for future ML algorithm)
    df_rnge = 16.2
    df_trnge = 520
    return render_template("blog/machn/dso.html", df_rnge=df_rnge, df_trnge=df_trnge)
@bp.route('/dso/log', methods=['GET'])
def dsolog():
    log = get_status('DSO')
    return jsonify(log=log)
@bp.route('/dso/reset', methods=['GET'])
def dsoreset():
    global dsobench
    try:
        dsobench = DSO.Initiate()
        status = "Success"
    except: status = "Error"
    return jsonify(message=status)
@bp.route('/dso/close', methods=['GET'])
def dsoclose():
    global dsobench
    status = DSO.close(dsobench)
    return jsonify(message=status)
@bp.route('/dso/settings', methods=['GET'])
def dsosettings():
    global dsobench
    message = []
    rnge = request.args.get('rnge')
    scal = request.args.get('scal')
    ofset = request.args.get('ofset')
    stat = DSO.channel1(dsobench, action=['Set', 'DC', rnge, scal, ofset, 'Volt', 'OFF'])
    message += ['CHANNEL 1: %s <%s>' %(stat[1], stat[0])]
    trnge = request.args.get('trnge')
    tdelay = request.args.get('tdelay')
    tscal = request.args.get('tscal')
    stat = DSO.timebase(dsobench, action=['Set', 'NORMAL', trnge + 'ns', tdelay + 'ns', tscal + 'ns'])
    message += ['TIMEBASE: %s <%s>' %(stat[1], stat[0])]
    avenum = request.args.get('avenum')
    stat = DSO.acquiredata(dsobench, action=['Set', 'average', '100', avenum])
    message += ['ACQUIRE DATA: %s <%s>' %(stat[1], stat[0])]
    # Generate Figure
    DSO.waveform(dsobench, action=['Set', 'max', 'channel1', 'ascii', '?', '?']) # "error: undefined header" will appear #this will light up channel1:display
    ans = list(DSO.waveform(dsobench))[1]
    y, dx = ans['DATA'], float(ans['XINCrement'])
    unitY = list(DSO.channel1(dsobench))[1]["UNITs"]
    DSO.display2D(dx, y, units=['s', unitY]) #Figure will be in INSTLOG
    return jsonify(message=message)
@bp.route('/dso/about', methods=['GET'])
def dsoabout():
    global dsobench
    message = []
    status = DSO.model(dsobench) # model
    message += ['Model: %s (%s)' % (status[1], status[0])]
    status = DSO.channel1(dsobench) # channel 1
    message += ['Channel 1: %s (%s)' % (status[1], status[0])]
    status = DSO.timebase(dsobench) # timebase
    message += ['Timebase: %s (%s)' % (status[1], status[0])]
    status = DSO.acquiredata(dsobench) # acquire data
    message += ['Acquisition of Data: %s (%s)' % (status[1], status[0])]
    return jsonify(message=message)


print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this

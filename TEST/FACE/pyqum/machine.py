# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name

from importlib import import_module as im
from flask import Flask, request, render_template, Response, redirect, Blueprint, jsonify, session
from pyqum.instrument.logger import address, get_status, set_status, status_code, output_code

# Error handling
from contextlib import suppress

# Scientific Constants
from scipy import constants as cnst

# This will run at server startup
# Modulars first, only then Benchtops (if and only if we use render_template)
# from pyqum.instrument.modular import AWG, VSA
# AWG.test(False) #seems like AWG's working-instance works differently than VSA's
# awgsess = AWG.InitWithOptions()
# vsasess = VSA.InitWithOptions()
from pyqum.instrument.benchtop import DSO, PNA
# dsobench = DSO.Initiate()
from pyqum.instrument.dilution import bluefors

encryp = 'ghhgjad'
bp = Blueprint(myname, __name__, url_prefix='/mach')

# Main
@bp.route('/')
def show():
    return render_template("blog/machn/machine.html")

# ALL
@bp.route('/all', methods=['POST', 'GET'])
def all(): 
    # Test Bed # All Task # Great Work
    return render_template("blog/machn/all.html")

# AWG
@bp.route('/awg', methods=['GET'])
def awg(): 
    with suppress(KeyError):
        print("USER %s has just logged in!" %session['user_id'])
        return render_template("blog/machn/awg.html")
    return("Please Login")        
@bp.route('/awg/log', methods=['GET'])
def awglog():
    log = get_status('AWG')
    return jsonify(log=log)
@bp.route('/awg/reset', methods=['GET'])
def awgreset():
    global awgsess
    awgsess = AWG.InitWithOptions()
    AWG.Abort_Gen(awgsess)
    return jsonify(message=awgsess)
@bp.route('/awg/generate', methods=['GET'])
def awggenerate():
    global awgsess
    status = AWG.Init_Gen(awgsess)
    return jsonify(message=status)
@bp.route('/awg/close', methods=['GET'])
def awgclose():
    global awgsess
    status = AWG.close(awgsess)
    return jsonify(message=status)
@bp.route('/awg/abort', methods=['GET'])
def awgabort():
    global awgsess
    status = AWG.Abort_Gen(awgsess)
    return jsonify(message=status)
@bp.route('/awg/settings-marker', methods=['GET'])
def awgsettingsmarker():
    global awgsess
    message = []
    active = request.args.get('active')
    stat = AWG.active_marker(awgsess, action=['Set',active])
    message += ['active marker: %s <%s>' %(stat[1], status_code(stat[0]))]
    delay = request.args.get('delay')
    stat = AWG.marker_delay(awgsess, action=['Set',float(delay)])
    message += ['marker delay: %s <%s>' %(stat[1], status_code(stat[0]))]
    pulsew = request.args.get('pulsew')
    stat = AWG.marker_pulse_width(awgsess, action=['Set',float(pulsew)])
    message += ['marker pulse width: %s <%s>' %(stat[1], status_code(stat[0]))]
    source = request.args.get('source')
    stat = AWG.marker_source(awgsess, action=['Set',int(source)])
    message += ['marker source: %s <%s>' %(stat[1], status_code(stat[0]))]
    return jsonify(message=message)
@bp.route('/awg/settings-prepare', methods=['GET'])
def awgsettingsprepare():
    global awgsess
    message = []
    predist = request.args.get('predist')
    stat = AWG.predistortion_enabled(awgsess, action=['Set',int(predist)])
    message += ['predistortion enabled: %s <%s>' %(stat[1], status_code(stat[0]))]
    outpmode = request.args.get('outpmode')
    stat = AWG.output_mode_adv(awgsess, action=['Set',int(outpmode)])
    message += ['advanced output mode: %s <%s>' %(stat[1], status_code(stat[0]))]
    samprat = request.args.get('samprat')
    stat = AWG.arb_sample_rate(awgsess, action=['Set',float(samprat)])
    message += ['sample rate: %s <%s>' %(stat[1], status_code(stat[0]))]
    return jsonify(message=message)
@bp.route('/awg/settings-squarewave', methods=['GET'])
def awgsettingssquarewave():
    global awgsess, seqhandl
    message = []
    # Shaping parameters
    voltag = []
    voltag.append(float(request.args.get('voltag1')))
    voltag.append(float(request.args.get('voltag2')))
    pointnum = []
    pointnum.append(int(request.args.get('pointnum1')))
    pointnum.append(int(request.args.get('pointnum2')))
    wavefom = ([voltag[0]]*pointnum[0] + [voltag[1]]*pointnum[1])
    
    stat = AWG.CreateArbWaveform(awgsess, wavefom)
    print(Fore.YELLOW + "Arb Waveform Created: %s"%stat[0])
    message += ['Waveform created: %s <%s>' %(stat[1], status_code(stat[0]))]
    stat = AWG.CreateArbSequence(awgsess, [stat[1]], [1]) # loop# canbe >1 if longer sequence is needed in the future!
    print(Fore.YELLOW + "Arb Sequence Created: %s"%stat[0])
    seqhandl = stat[1]
    print("seq handle in set-waveform is %s"%seqhandl)
    message += ['Sequence assembled: %s <%s>' %(stat[1], status_code(stat[0]))]

    return jsonify(message=message)
@bp.route('/awg/settings-channel', methods=['GET'])
def awgsettingschannel():
    global awgsess, seqhandl
    print("seq handle in set-channel is %s"%seqhandl)
    message = [] 
    channel = request.args.get('channel')
    stat = AWG.arb_sequence_handle(awgsess, RepCap=channel, action=["Set", seqhandl])
    message += ['Sequence embeded: %s <%s>' %(stat[1], status_code(stat[0]))]
    outputch = request.args.get('outputch')
    stat = AWG.output_enabled(awgsess, RepCap=channel, action=["Set", int(outputch)])
    message += ['output channel %s: %s <%s>' %(channel, output_code(stat[1]), status_code(stat[0]))]
    oupfiltr = request.args.get('oupfiltr')
    stat = AWG.output_filter_enabled(awgsess, RepCap=channel, action=["Set", int(oupfiltr)])
    message += ['output filter channel %s: %s <%s>' %(channel, output_code(stat[1]), status_code(stat[0]))]

    # temporary:
    AWG.output_filter_bandwidth(awgsess, RepCap=channel, action=["Set", 0])
    AWG.output_config(awgsess, RepCap=channel, action=["Set", 0])
    AWG.arb_gain(awgsess, RepCap=channel, action=["Set", 0.25])
    AWG.output_impedance(awgsess, RepCap=channel, action=["Set", 50])
    AWG.operation_mode(awgsess, RepCap=channel, action=["Set", 0])
    AWG.trigger_source_adv(awgsess, RepCap=channel, action=["Set", 0])
    AWG.burst_count(awgsess, RepCap=channel, action=["Set", 1000001])

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
    status = AWG.output_mode_adv(awgsess) # advanced output mode
    message += ['Advanced Output Mode: %s (%s)' % (status[1], status_code(status[0]))]
    status = AWG.arb_sample_rate(awgsess) # sample rate
    message += ['Sample Rate: %s (%s)' % (status[1], status_code(status[0]))]
    
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

# SG
@bp.route('/sg', methods=['GET'])
def sg(): 
    return render_template("blog/machn/sg.html")
@bp.route('/sg/log', methods=['GET'])
def sglog():
    log = get_status('sg')
    return jsonify(log=log)
@bp.route('/sg/reset', methods=['GET'])
def sgreset():
    global sgbench, SG
    sgtype = request.args.get('sgtype')
    try:
        SG = im("pyqum.instrument.benchtop.%s" %sgtype)
        sgbench = SG.Initiate()
        status = "Success"
    except: status = "Error"
    return jsonify(message=status)
@bp.route('/sg/close', methods=['GET'])
def sgclose():
    global sgbench
    status = SG.close(sgbench)
    return jsonify(message=status)
@bp.route('/sg/settings', methods=['GET'])
def sgsettings():
    global sgbench
    message = []
    freq = request.args.get('freq')
    stat = SG.frequency(sgbench, action=['Set', freq + "GHZ"])
    message += ['frequency (GHz): %s <%s>' %(stat[1], stat[0])]
    powa = request.args.get('powa')
    stat = SG.power(sgbench, action=['Set',float(powa)])
    message += ['power (dBm): %s <%s>' %(stat[1], stat[0])]
    oupt = request.args.get('oupt')
    stat = SG.rfoutput(sgbench, action=['Set',int(oupt)])
    message += ['RF output: %s <%s>' %(stat[1], stat[0])]
    return jsonify(message=message)
@bp.route('/sg/about', methods=['GET'])
def sgabout():
    global sgbench
    message = []
    status = SG.model(sgbench) # model
    message += ['Model: %s (%s)' % (status[1], status[0])]
    status = SG.frequency(sgbench) # frequency
    message += ['Frequency: %s (%s)' % (status[1], status[0])]
    status = SG.power(sgbench) # power
    message += ['Power: %s (%s)' % (status[1], status[0])]
    status = SG.rfoutput(sgbench) # rf output
    message += ['RF output: %s (%s)' % (output_code(status[1]), status[0])]
    return jsonify(message=message)

# DSO
@bp.route('/dso', methods=['GET'])
def dso():
    # default input/select value (pave way for future ML algorithm)
    yrange, yscale, yoffset = 16.2, 2, 3
    yrange2, yscale2, yoffset2 = 16.2, 2, 3
    trange, tdelay, tscale = 520, 120, 50
    return render_template("blog/machn/dso.html", yrange=yrange, yscale=yscale, yoffset=yoffset, yrange2=yrange2, yscale2=yscale2, yoffset2=yoffset2, trange=trange, tdelay=tdelay, tscale=tscale)
@bp.route('/dso/autoscale', methods=['GET'])
def dsoautoscale():
    global dsobench
    dsobench.write(':AUTOSCALE')
    status = DSO.channel1(dsobench) # channel 1
    yrange, yscale, yoffset = status[1]['RANGE'], status[1]['SCALE'], status[1]['OFFSET']
    status = DSO.channel2(dsobench) # channel 2
    yrange2, yscale2, yoffset2 = status[1]['RANGE'], status[1]['SCALE'], status[1]['OFFSET']
    status = DSO.timebase(dsobench) # timebase
    trange, tdelay, tscale = status[1]['RANGE'], status[1]['DELAY'], status[1]['SCALE']
    trange, tdelay, tscale = float(trange)/cnst.nano, float(tdelay)/cnst.nano, float(tscale)/cnst.nano
    return jsonify(yrange=yrange, yscale=yscale, yoffset=yoffset, yrange2=yrange2, yscale2=yscale2, yoffset2=yoffset2, trange=trange, tdelay=tdelay, tscale=tscale)
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
    rnge2 = request.args.get('rnge2')
    scal2 = request.args.get('scal2')
    ofset2 = request.args.get('ofset2')
    stat = DSO.channel2(dsobench, action=['Set', 'DC', rnge2, scal2, ofset2, 'Volt', 'OFF'])
    message += ['CHANNEL 2: %s <%s>' %(stat[1], stat[0])]
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
    DSO.display2D(dx, y, units=['s', unitY], channel=1) #Figure will be in static/img
    DSO.waveform(dsobench, action=['Set', 'max', 'channel2', 'ascii', '?', '?']) # "error: undefined header" will appear #this will light up channel1:display
    ans = list(DSO.waveform(dsobench))[1]
    y, dx = ans['DATA'], float(ans['XINCrement'])
    unitY = list(DSO.channel2(dsobench))[1]["UNITs"]
    DSO.display2D(dx, y, units=['s', unitY], channel=2) #Figure will be in static/img
    return jsonify(message=message)
@bp.route('/dso/about', methods=['GET'])
def dsoabout():
    global dsobench
    message = []
    status = DSO.model(dsobench) # model
    message += ['Model: %s (%s)' % (status[1], status[0])]
    status = DSO.channel1(dsobench) # channel 1
    message += ['Channel 1: %s (%s)' % (status[1], status[0])]
    status = DSO.channel2(dsobench) # channel 2
    message += ['Channel 2: %s (%s)' % (status[1], status[0])]
    status = DSO.timebase(dsobench) # timebase
    message += ['Timebase: %s (%s)' % (status[1], status[0])]
    status = DSO.acquiredata(dsobench) # acquire data
    message += ['Acquisition of Data: %s (%s)' % (status[1], status[0])]
    return jsonify(message=message)

# BDR
@bp.route('/bdr', methods=['GET'])
def bdr():
    global b
    b = bluefors()
    return render_template("blog/machn/bdr.html", Days=b.Days)
@bp.route('/bdr/history', methods=['GET'])
def bdrhistory():
    global b
    wday = b.Days.index(request.args.get('wday'))
    P_Ch = int(request.args.get('P_Ch'))
    T_Ch = int(request.args.get('T_Ch'))
    P_Ch2 = int(request.args.get('P_Ch2'))
    T_Ch2 = int(request.args.get('T_Ch2'))
    b = bluefors()
    b.selectday(wday)
    [startimeP, tp, P, P_stat] = b.pressurelog(P_Ch)
    [startimeT, tt, T] = b.temperaturelog(T_Ch)
    if P_Ch2 > 0 and T_Ch2 > 0:
        [startimeP, tp2, P2, P_stat2] = b.pressurelog(P_Ch2)
        [startimeT, tt2, T2] = b.temperaturelog(T_Ch2)
    elif P_Ch2 > 0:
        [startimeP, tp2, P2, P_stat2] = b.pressurelog(P_Ch2)
        [startimeT, tt2, T2] = [startimeT, tt, T]
    elif T_Ch2 > 0:
        [startimeP, tp2, P2, P_stat2] = [startimeP, tp, P, P_stat]
        [startimeT, tt2, T2] = b.temperaturelog(T_Ch2)
    else:
        [startimeP, tp2, P2, P_stat2] = [startimeP, tp, P, P_stat]
        [startimeT, tt2, T2] = [startimeT, tt, T]
    return jsonify(startimeP=startimeP, startimeT=startimeT, tp=tp, P=P, P_stat=P_stat, tt=tt, T=T, tp2=tp2, P2=P2, P_stat2=P_stat2, tt2=tt2, T2=T2)

# DC
@bp.route('/dc', methods=['GET'])
def dc():
    global b
    b = bluefors()
    return render_template("blog/machn/dc.html", Days=b.Days)
@bp.route('/dc/state', methods=['GET'])
def dcstate():
    
    return jsonify()


print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this


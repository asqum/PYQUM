# import requests
from flask import Flask, request, render_template, Response, redirect, Blueprint, jsonify
from colorama import init
init(autoreset=True) #to convert termcolor to wins color
from pyqum.instrument.modular import AWG

bp = Blueprint('awgonly', __name__)
awgcache = {}

# import visa # putting this before AWG.Init.. will cripple all AWG command
status, session = AWG.InitWithOptions()
import visa

@bp.route('/awg', methods=['POST', 'GET'])
def show():
    stat = 'No reading'
    global session
    if request.method == 'POST':
        if request.form.get('reset'):
            status, session = AWG.InitWithOptions()
            awgcache.update(Initialized=status)
        if request.form.get('marker'):
            active = request.form.get('active')
            status = AWG.active_marker(session, action=['Set',active])
            awgcache.update(Marker=status)
            delay = request.form.get('delay')
            status = AWG.marker_delay(session, action=['Set',float(delay)])
            awgcache.update(Delay=status)
        if request.form.get('model'):
            stat = AWG.model(session)
                
    return render_template("blog/awgonly.html", stat=stat)


@bp.route("/off")
def off():
    global session
    status = AWG.close(session)
    awgcache.update(Closed=status)

    return 'Closed: %s' % awgcache \
    + "<br/> <a href='/awg'>AWG</a>"

@bp.route('/model', methods=['POST', 'GET'])
def model():
    global session
    status = AWG.model(session)
    awgcache.update(Model=status)
    message = 'Model: %s (error: %s)' % (status[1], status[0])
    return jsonify(message=message)

@bp.route("/getmarker")
def getmarker():
    global session
    status = AWG.active_marker(session)
    awgcache.update(Marker=status)
    message = 'Active Marker: %s (error: %s)' % (status[1], status[0])
    return jsonify(message=message)

@bp.route("/getdelay")
def getdelay():
    global session
    status = AWG.marker_delay(session)
    awgcache.update(Delay=status)
    message = 'Marker Delay: %s (error: %s)' % (status[1], status[0])
    return jsonify(message=message)


print('loading awgonly')
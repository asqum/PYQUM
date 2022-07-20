from flask import Blueprint, render_template, request, redirect, jsonify
import random, json, ctypes, requests
from pathlib import Path

# Initialize before Blueprint
from pyqum.instrument.modular import VSA, AWG
status, session = AWG.InitWithOptions()

# VISA conflicts the DLL Libraries!
# Hence it has to come AFTER Initiated the IVI-C Connection
from pyqum.instrument.benchtop import ESG 

bp = Blueprint('combo', __name__)

@bp.route('/comb', methods=['POST', 'GET']) #this will appear as the web address
def show():
    global session
    status, ans, mark = None, None, {}

    if request.form.get('model'):
        stat = AWG.model(session)
        ans = stat[1]

    if request.form.get('gemarker'):
        stat = AWG.active_marker(session)
        mark = dict(active=stat[1])
        stat = AWG.marker_delay(session)
        mark.update(delay=stat[1])

    if request.form.get('reset'):
        status = AWG.InitWithOptions()
        session = status[1]
        return redirect('/')

    if request.form.get('semarker'):
        active = request.form.get('active')
        AWG.active_marker(session, action=['Set',active])
        delay = request.form.get('delay')
        AWG.marker_delay(session, action=['Set',float(delay)])
        return redirect('/')
        
    if request.form.get('closeawg'):# or x == 1:
        AWG.close(session)
        return redirect('/')

    if request.form.get('esgon'):
        freq = request.form.get('frequency')
        powa = request.form.get('power')
        ESG.control(True, freq, powa)
        return redirect('/')

    if request.form.get('esgoff'):
        ESG.control(False)
        return redirect('/')

    return render_template('blog/combo.html', ans=ans, mark=mark) #this is where it really goes


print('loading combo')
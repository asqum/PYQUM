# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name

from flask import Flask, request, render_template, Response, redirect, Blueprint, jsonify, session, send_from_directory, abort, g
from pyqum.instrument.logger import address, get_status, set_status, status_code, output_code
from pyqum.instrument.toolbox import waveform

# Error handling
from contextlib import suppress

# Scientific
from scipy import constants as cnst
from si_prefix import si_format, si_parse
from numpy import cos, sin, pi, polyfit, poly1d, array, roots, isreal, sqrt, mean

encryp = '/' + 'hgdfhghfle7'
bp = Blueprint(myname, __name__, url_prefix=encryp+'/guide')

# Main
@bp.route('/')
def show():
    with suppress(KeyError):
        print(Fore.LIGHTBLUE_EX + "USER " + Fore.YELLOW + "%s "%session['user_name'] + Fore.LIGHTBLUE_EX + "has just logged in as Guest #%s!"%session['user_id'])
        # Security implementation:
        if not g.user: abort(404)
        return render_template("blog/guide/guide.html")
    return("<h3>Please Kindly Login!</h3><h3>Courtesy from <a href='http://qum.phys.sinica.edu.tw:%s/auth/login'>HoDoR</a></h3>" %get_status("WEB")["port"])

# ALL
@bp.route('/calc', methods=['POST', 'GET'])
def calc(): 
    current_usr = session['user_name']
    return render_template("blog/guide/calculate.html", current_usr=current_usr)
@bp.route('/calc/qfreq/predict', methods=['GET'])
def calc_qfreq_predict():
    Qubit_name = request.args.get('Qubit_name')
    filling_factor = waveform(request.args.get('filling_factor')).data
    flux_offset = float(request.args.get('flux_offset'))
    flux_halfill = float(request.args.get('flux_halfill'))
    MT_frequency = float(request.args.get('MT_frequency'))
    
    filling_factor = array(filling_factor)
    filling_period = abs(flux_offset - flux_halfill) * 2
    fluxrange = filling_period * filling_factor
    qfrequency, qzvalue = {}, {}
    qzvalue[Qubit_name] = list( fluxrange + flux_offset )
    qfrequency[Qubit_name] = list( MT_frequency * sqrt( abs( cos(pi*filling_factor) ) ) )
    
    return jsonify(fluxrange=fluxrange[0], qzvalue=qzvalue, qfrequency=qfrequency, filling_period=filling_period)

@bp.route('/qcirc', methods=['POST', 'GET'])
def qcirc(): 
    current_usr = session['user_name']
    return render_template("blog/guide/q_circuit.html", current_usr=current_usr)






print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this


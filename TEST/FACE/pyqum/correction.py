# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name

from importlib import import_module as im
from flask import Flask, request, render_template, Response, redirect, Blueprint, jsonify, session, send_from_directory, abort, g
from pyqum.instrument.logger import address, get_status, set_status, status_code, output_code

# Error handling
from contextlib import suppress

# Scientific
from scipy import constants as cnst
from si_prefix import si_format, si_parse
from numpy import cos, sin, pi, polyfit, poly1d, array, roots, isreal, sqrt, mean

# Load instruments
from pyqum.instrument.modular import AWG, VSA # open native Agilent M933x -> Initiate VSA -> Initiate AWG (Success!!!)
from pyqum.instrument.benchtop import PSGA, RSA5, MXA
from pyqum.instrument.toolbox import match, waveform, pauselog, squarewave
from pyqum.instrument.analyzer import IQAParray

encryp = 'ghhgjadz'
bp = Blueprint(myname, __name__, url_prefix='/corr')

# Main
@bp.route('/')
def show():
	with suppress(KeyError):
		print(Fore.LIGHTBLUE_EX + "USER " + Fore.YELLOW + "%s "%session['user_name'] + Fore.LIGHTBLUE_EX + "has just logged in as Guest #%s!"%session['user_id'])
		# Security implementation:
		if not g.user['instrument']:
			abort(404)
		return render_template("blog/machn/machine.html")
	return("<h3>WHO ARE YOU?</h3><h3>Please F**k*ng Login!</h3><h3>Courtesy from <a href='http://qum.phys.sinica.edu.tw:5300/auth/login'>HoDoR</a></h3>")

# ALL
@bp.route('/all', methods=['POST', 'GET'])
def all(): 
	# Test Bed # All Task # Great Work
	current_usr = session['user_name']
	return render_template("blog/machn/all.html", current_usr=current_usr)
@bp.route('/all/status', methods=['GET'])
def allstatus():
	
	return jsonify()

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
	AWG.Abort_Gen(awgsess)
	status = AWG.model(awgsess) # model
	print('Model: %s (%s)' % (status[1], status_code(status[0])))
	return jsonify(message=awgsess)





print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this


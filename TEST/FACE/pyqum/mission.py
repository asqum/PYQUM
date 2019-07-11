# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name

import requests
from flask import Flask, request, render_template, Response, redirect, Blueprint, jsonify
from numpy import array

from pyqum.instrument.logger import address, get_status, set_status, status_code, output_code
from pyqum.instrument.toolbox import cdatasearch, gotocdata, waveform
from pyqum.instrument.analyzer import IQAP, UnwraPhase

from pyqum.directive.characterize import F_Response

# Scientific Constants
from scipy import constants as cnst


encryp = 'ghhgjad'
bp = Blueprint(myname, __name__, url_prefix='/mssn')

# Main
@bp.route('/')
def show():
    return render_template("blog/msson/mission.html", encryp=encryp)

# ALL
@bp.route('/all', methods=['GET'])
def all(): 
    # Test Bed # All Task # Great Work
    return render_template("blog/msson/all.html")
@bp.route('/all/test', methods=['GET'])
def alltest():
    i = request.args.get('idea')
    print(Back.MAGENTA + 'i: %s'%i)
    return jsonify(i=i)
@bp.route('/all/insertopt', methods=['GET'])
def allinsertopt():
    x = [100, 200, 300, 400, 500, 600, 777]
    return jsonify(x=x)

# CHAR:
@bp.route('/char', methods=['GET'])
def char(): 
    return render_template("blog/msson/char.html")

# CHAR -> F-Response
@bp.route('/char/fresp', methods=['GET'])
def char_fresp(): 
    return render_template("blog/msson/char/fresp.html")
@bp.route('/char/fresp/init', methods=['GET'])
def char_fresp_init(): 
    global M_fresp
    M_fresp = F_Response()
    # ifb = eval(str(request.args.get('ifb')))
    return jsonify(daylist=M_fresp.daylist)
@bp.route('/char/fresp/time', methods=['GET'])
def char_fresp_time():
    wday = int(request.args.get('wday'))
    M_fresp.selectday(wday)
    return jsonify(taskentries=M_fresp.taskentries)
@bp.route('/char/fresp/new', methods=['GET'])
def char_fresp_new():
	wday = int(request.args.get('wday'))
	sparam = request.args.get('sparam')
	ifb = request.args.get('ifb')
	powa = request.args.get('powa')
	freq = request.args.get('freq')
	comment = request.args.get('comment')
	CORDER = {'S-Parameter':sparam, 'IF-Bandwidth':ifb, 'Power':powa, 'Frequency':freq}
	M = F_Response(corder=CORDER, comment=comment, tag='', dayindex=wday)
	M.accesstructure()
	return jsonify(complete=str(M.data_complete))
@bp.route('/char/fresp/access', methods=['GET'])
def char_fresp_access():
	wmoment = int(request.args.get('wmoment'))
	M_fresp.selectmoment(wmoment)
	M_fresp.accesstructure()
	data_progress = M_fresp.data_progress
	csparam = waveform(M_fresp.corder['S-Parameter'])
	cifb = waveform(M_fresp.corder['IF-Bandwidth'])
	cpowa = waveform(M_fresp.corder['Power'])
	cfreq = waveform(M_fresp.corder['Frequency'])
	global c_fresp_structure
	c_fresp_structure = [csparam.count,cifb.count,cpowa.count,cfreq.count*M_fresp.datadensity]
	return jsonify(data_progress=data_progress, corder=M_fresp.corder, comment=M_fresp.comment, csparam=csparam.data, cifb=cifb.data, cpowa=cpowa.data, cfreq=cfreq.data)
# Chart is supposedly shared by all measurements (under construction for nulti-purpose)
@bp.route('/char/fresp/1ddata', methods=['GET'])
def char_fresp_1ddata():
	try: isparam = int(request.args.get('isparam'))
	except(ValueError): isparam = request.args.get('isparam')
	try: iifb = int(request.args.get('iifb'))
	except(ValueError): iifb = request.args.get('iifb')
	try: ipowa = int(request.args.get('ipowa'))
	except(ValueError): ipowa = request.args.get('ipowa')
	# try: ifreq = int(request.args.get('ifreq'))
	# except(ValueError): ifreq = request.args.get('ifreq')
	M_fresp.loadata()
	selectedata=M_fresp.selectedata
	selected = [selectedata[gotocdata([isparam, iifb, ipowa, x], c_fresp_structure)] for x in range(waveform(M_fresp.corder['Frequency']).count*M_fresp.datadensity)]
	yI, yQ, Amp, Pha = IQAP(array(selected))
	x1, y1, y2 = waveform(M_fresp.corder['Frequency']).data, Amp, list(UnwraPhase(waveform(M_fresp.corder['Frequency']).data, Pha))
	return jsonify(x1=x1, y1=y1, y2=y2)









print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this



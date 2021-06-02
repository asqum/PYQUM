# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name

from importlib import import_module as im
from flask import Flask, request, render_template, Response, redirect, Blueprint, jsonify, session, send_from_directory, abort, g
from pyqum.instrument.logger import address, get_status, set_status, set_mat, set_csv, clocker, mac_for_ip, lisqueue, lisjob, measurement, qout, jobsearch, get_json_measurementinfo
from pyqum.instrument.toolbox import cdatasearch, gotocdata, waveform
from numpy import array, unwrap, mean, trunc, sqrt, zeros, ones, shape, arctan2, int64, isnan, abs

from pyqum.instrument.logger import address, get_status, set_status, set_mat, set_csv, clocker, mac_for_ip, lisqueue, lisjob, measurement, qout, jobsearch, get_json_measurementinfo

import json

# Error handling
from contextlib import suppress

# Scientific
from scipy import constants as cnst
from si_prefix import si_format, si_parse
from numpy import cos, sin, pi, polyfit, poly1d, array, roots, isreal, sqrt, mean

# Load instruments
from pyqum.instrument.benchtop import TKAWG, PSGA, MXA
from pyqum.directive import calibrate 
from pyqum.directive.MP_benchmark import assembler

# Fitting
from pyqum.directive.resonator_tools import circuit
from collections import defaultdict


encryp = 'ghhgjadz'
bp = Blueprint(myname, __name__, url_prefix='/benchmark')

# Main

def get_fileName():
	current_usr = session['user_name']
	jsonFileName = "measurement_info["+current_usr+"]"
	return jsonFileName

def find_nearestIndex( fArray, fValues ):
	idx = []
	for fv in fValues:
		idx.append( abs(fArray - fv).argmin() )
	return idx


@bp.route('/')
def show():
	with suppress(KeyError):
		print(Fore.LIGHTBLUE_EX + "USER " + Fore.YELLOW + "%s "%session['user_name'] + Fore.LIGHTBLUE_EX + "has just logged in as Guest #%s!"%session['user_id'])
		# Security implementation:
		if not g.user['instrument']:
			abort(404)
		return render_template("blog/benchmark/benchmark.html")
	return("<h3>WHO ARE YOU?</h3><h3>Please F**k*ng Login!</h3><h3>Courtesy from <a href='http://qum.phys.sinica.edu.tw:5300/auth/login'>HoDoR</a></h3>")

@bp.route('/get_parametersID', methods=['POST', 'GET'])
def get_parametersID():
	info = get_json_measurementinfo(get_fileName())
	htmlID = [ paras["htmlId"] for paras in info["measurement"]["parameters"] ]
	return jsonify(htmlID)

@bp.route('/qestimate', methods=['POST', 'GET'])
def qestimate(): 
	info = get_json_measurementinfo(get_fileName())
	print( "measurement_info", info['measurement']['type'])
	print("qestimate")
	return render_template("blog/benchmark/qestimate.html", info=info)

@bp.route('/measurement_info', methods=['POST', 'GET'])
def measurement_info(): 

	info = get_json_measurementinfo(get_fileName())
	print( "measurement_info", info['measurement']['type'])

	return render_template("blog/benchmark/measurement_info.html", info=info)

def get_iqData2D (valueIndex, axisIndex):

	info = get_json_measurementinfo(get_fileName())

	stage, prev = clocker(0, agenda="2D Fresp")
	output = assembler( valueIndex, axisIndex, info, session['user_name'] )
	stage, prev = clocker(stage, prev, agenda="2D Fresp") # Marking time

	return output



@bp.route('/qestimate/plot',methods=['POST','GET'])
def qestimate_plot():
	print(Fore.GREEN + "User %s is plotting 2D-Data" %session['user_name'])
	global iqData, valueIndex, axisIndex 

	valueIndex = [int(vi) for vi in json.loads(request.args.get('valueIndex'))]
	axisIndex = [int(ai) for ai in json.loads(request.args.get('axisIndex'))]
	plotDimension = len(axisIndex)

	print("valueIndex",valueIndex,",axisIndex",axisIndex)
	iqData = get_iqData2D(valueIndex, axisIndex)
	info = get_json_measurementinfo(get_fileName())
	paraInfo = info["measurement"]["parameters"]

	xtitle = paraInfo[axisIndex[0]]["lable"]
	ytitle = paraInfo[axisIndex[1]]["lable"]

	iAmp = iqData['I']
	qAmp = iqData['Q']
	TransAmp = sqrt(iAmp**2+qAmp**2)

	# if( plotDimension == 2):
	x = paraInfo[axisIndex[0]]["values"]
	y = paraInfo[axisIndex[1]]["values"]
	print("x is of length %s and of type %s" %(len(x),type(x)))
	print("y is of length %s and of type %s" %(len(y),type(y)))

	z = TransAmp
	return jsonify(x=x, y=y, zAmp=z.transpose().tolist(), zI=iAmp.transpose().tolist(), zQ=qAmp.transpose().tolist())
	# elif( plotDimension == 1 ):
	# 	x = paraInfo[axisIndex[0]]["values"]
	# 	print("x is of length %s and of type %s" %(len(x),type(x)))
	# 	y = TransAmp
	# 	return jsonify(x=x, y=y.tolist(), z=[], xtitle=xtitle, ytitle="ytitle")
	# else:
	# 	return 0

@bp.route('/qestimate/fitting',methods=['POST','GET'])
def qestimate_fitting():
	global fittingResult

	fittingRangeFrom = request.args.get('fittingRangeFrom')
	fittingRangeTo = request.args.get('fittingRangeTo')
	info = get_json_measurementinfo(get_fileName())
	print("I shape:", iqData["I"].shape, "Q shape:", iqData["Q"].shape )
	print("Fitting range:", fittingRangeFrom, fittingRangeTo)
	info = get_json_measurementinfo(get_fileName())


	fitIQ = iqData["I"].transpose()+1j*iqData["Q"].transpose()
	fitFrequency= array(info["measurement"]["parameters"][4]["values"])
	fittingRange = [float(fittingRangeFrom),float(fittingRangeTo)]

	fittingIndex = find_nearestIndex( fitFrequency, fittingRange )
	fittingIndex.sort()

	port = circuit.notch_port()
	fittingResult = {}
	for ifitIQ, i in zip(fitIQ, range(iqData["I"].shape[1]) ):
		port.add_data( fitFrequency[fittingIndex[0]:fittingIndex[1]] ,ifitIQ[fittingIndex[0]:fittingIndex[1]] )
		port.autofit()

		for key in port.fitresults.keys():
			fittingValue = port.fitresults[key]
			if isnan(fittingValue):
				fittingValue = 0
			if(i==0):
					fittingResult[key] = [fittingValue]
			else:
					fittingResult[key].append(fittingValue)

	fittingResult[info["measurement"]["parameters"][axisIndex[1]]["lable"]]= info["measurement"]["parameters"][axisIndex[1]]["values"]

	#print(dates_dict)
	return jsonify(fittingResult)


@bp.route('/test',methods=['POST','GET'])
def index():
	if request.method =='POST':
		if request.values['send']=='送出':
			return render_template('blog/benchmark/measurement_info.html',name=request.values['user'])
	return render_template('blog/benchmark/measurement_info.html',name="")

def get_fresp_parametersName():
	ParametersName = ["Flux-Bias","S-Parameter", "IF-Bandwidth", "Power", "Frequency"]
	return ParametersName

print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this


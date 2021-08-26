# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name
import sys, struct

from importlib import import_module as im
from flask import Flask, request, render_template, Response, redirect, Blueprint, jsonify, session, send_from_directory, abort, g
from pyqum.instrument.logger import address, get_status, set_status, set_mat, set_csv, clocker, mac_for_ip, lisqueue, lisjob, measurement, qout, jobsearch, get_json_measurementinfo, set_mat_analysis
from pyqum.instrument.toolbox import cdatasearch, gotocdata, waveform


# Json to Javascrpt
import json

# Error handling
from contextlib import suppress

# Scientific
from scipy import constants as cnst
from si_prefix import si_format, si_parse
from numpy import array, unwrap, mean, trunc, sqrt, zeros, ones, shape, arctan2, int64, isnan, abs, empty, ndarray, moveaxis, reshape, logical_and, nan

# Load instruments
from pyqum.directive.quantification import ExtendMeasurement, QEstimation, Decoherence
from pyqum.mission import get_measurementObject

# Fitting
from resonator_tools.circuit import notch_port
from collections import defaultdict

# Save file
from scipy.io import savemat


encryp = 'ghhgjadz'
bp = Blueprint(myname, __name__, url_prefix='/benchmark')

# Main


class NumpyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, ndarray):
			return obj.tolist()
			
		return json.JSONEncoder.default(self, obj)
	

@bp.route('/')
def show():
	with suppress(KeyError):
		print(Fore.LIGHTBLUE_EX + "USER " + Fore.YELLOW + "%s "%session['user_name'] + Fore.LIGHTBLUE_EX + "has just logged in as Guest #%s!"%session['user_id'])
		# Security implementation:
		if not g.user['instrument']:
			abort(404)
		#quantificationType = benchmarkDict[session['user_name']].quantificationType
		return render_template("blog/benchmark/benchmark.html")
	return("<h3>WHO ARE YOU?</h3><h3>Please F**k*ng Login!</h3><h3>Courtesy from <a href='http://qum.phys.sinica.edu.tw:5300/auth/login'>HoDoR</a></h3>")

# Get Information for Render HTML
@bp.route('/get_parametersID', methods=['POST', 'GET'])
def get_parametersID():
	myExtendMeasurement = benchmarkDict[session['user_name']]
	htmlInfo = myExtendMeasurement.get_htmlInfo()
	return jsonify(htmlInfo)

@bp.route('/get_parameterValue', methods=['POST', 'GET'])
def get_parameterValue():
	myExtendMeasurement = benchmarkDict[session['user_name']]
	parameterKey = request.args.get('parameterKey')
	htmlInfo = myExtendMeasurement.independentVars[parameterKey]
	return json.dumps(htmlInfo, cls=NumpyEncoder)

# Render HTML
@bp.route('/qestimate', methods=['POST', 'GET'])
def qestimate():
	return render_template("blog/benchmark/qestimate.html")

@bp.route('/decoherence', methods=['POST', 'GET'])
def decoherence():
	return render_template("blog/benchmark/decoherence.html")



@bp.route('/benchmark_getMeasurement', methods=['POST', 'GET'])
def benchmark_getMeasurement():
	'''
	quantification type "qfactor_estimation"
	''' 
	global benchmarkDict
	measurementType = request.args.get('measurementType')

	benchmarkDict[session['user_name']] = ExtendMeasurement( get_measurementObject(measurementType) )
	return "Send Measurement Object"


@bp.route('/get_user', methods=['POST', 'GET'])
def get_user():
	return jsonify(session['user_name'])

@bp.route('/measurement_info', methods=['POST', 'GET'])
def measurement_info(): 

	myMeasurement = benchmarkDict[session['user_name']].measurementObj

	if 'jobid' in myMeasurement.perimeter.keys(): 
		JOBID = myMeasurement.perimeter['jobid']

	return render_template("blog/benchmark/measurement_info.html", JOBID=JOBID)



# Each user have own Quantification object
benchmarkDict = {}
QDict = {}


@bp.route('/register_Quantification',methods=['POST','GET'])
def register_Quantification():
	myExtendMeasurement = benchmarkDict[session['user_name']]
	quantificationType = json.loads(request.args.get('quantificationType'))
	print("quantificationType",quantificationType)
	def get_qEstimation ( myExtendMeasurement ):
		return QEstimation(myExtendMeasurement)
	def get_decoherence ( myExtendMeasurement ):
		return Decoherence(myExtendMeasurement)
	quantification = {
		'qEstimation': get_qEstimation,
		'decoherence': get_decoherence,
	}
	try: QDict[session['user_name']] = quantification[quantificationType](myExtendMeasurement)
	except(KeyError): print("No such quantification type")
	return json.dumps(quantificationType, cls=NumpyEncoder)

@bp.route('/qestimate/getJson_plot',methods=['POST','GET'])
def getJson_plot():

	myExtendMeasurement = benchmarkDict[session['user_name']]
	myQuantification = QDict[session['user_name']] 

	analysisIndex = json.loads(request.args.get('analysisIndex'))
	plotType = json.loads(request.args.get('plotType'))


	valueInd = analysisIndex["valueIndex"]
	axisInd = analysisIndex["axisIndex"]
	dimension = len(axisInd)

	# Get average information from JS
	aveAxisInd = analysisIndex["aveInfo"]["axisIndex"]
	aveRange = 0
	# Construct average informaion to reshape
	if len(aveAxisInd) !=0:
		aveRange = [int(k) for k in analysisIndex["aveInfo"]["aveRange"].split(",")]
	aveInfo = {
		"axisIndex": aveAxisInd,
		"aveRange": aveRange
	}


	xAxisKey = myExtendMeasurement.measurementObj.corder["C-Structure"][axisInd[0]]

	if dimension == 2:
		yAxisKey = myExtendMeasurement.measurementObj.corder["C-Structure"][axisInd[1]]
		yAxisValInd = valueInd[axisInd[1]]
	elif dimension == 1:
		yAxisKey = None
		yAxisValInd = 0

	preAxisInd = myExtendMeasurement.axisInd
	preValueInd = myExtendMeasurement.varsInd
	if preAxisInd != axisInd  or ( yAxisKey==None and preValueInd != valueInd) or aveInfo!=aveInfo:
		print("Previous index",preValueInd,"New index",valueInd)
		myExtendMeasurement.reshape_Data( valueInd, axisInd=axisInd, aveInfo=aveInfo )


	print("Plot type: ", plotType)
	print("Plot shape Raw: ",myExtendMeasurement.rawData["iqSignal"].shape)
	print("Plot shape Fit:", myQuantification.fitCurve["iqSignal"].shape)
	print("yAxisKey: ",yAxisKey)

	plotData = {}

	#print(plotData)
	def plot_1D_show( originalArray ) :
		#fitRangeBoolean = logical_and(myExtendMeasurement.rawData["x"]>=float(myExtendMeasurement.fitParameters["range"]["from"]),myExtendMeasurement.rawData["x"]<=float(myExtendMeasurement.fitParameters["range"]["to"]) )
		#return originalArray[fitRangeBoolean]
		return originalArray

	def plot_2D_amp () :
		plotData[yAxisKey]= myExtendMeasurement.independentVars[yAxisKey]
		plotData[xAxisKey]= myExtendMeasurement.rawData["x"]
		plotData["amplitude"]= abs(myExtendMeasurement.rawData["iqSignal"])
		return plotData
	def plot_1D_amp () :
		plotData["Data_point_frequency"]= myExtendMeasurement.rawData["x"]
		plotData["Data_point_amplitude"]= abs(myExtendMeasurement.rawData["iqSignal"][yAxisValInd])
		if myQuantification.fitCurve["x"].shape[0] != 0:
			plotData["Fitted_curve_frequency"]=plot_1D_show( myQuantification.fitCurve["x"] )
			plotData["Fitted_curve_amplitude"]=plot_1D_show( abs(myQuantification.fitCurve["iqSignal"][yAxisValInd]) )
		if myQuantification.baseline["x"].shape[0] != 0:
			plotData["Fitted_baseline_frequency"]=myQuantification.fitCurve["x"]
			plotData["Fitted_baseline_amplitude"]=abs(myQuantification.baseline["iqSignal"][yAxisValInd])
		if myQuantification.correctedIQData["x"].shape[0] != 0:
			plotData["Corr_Data_point_frequency"]=myQuantification.fitCurve["x"]
			plotData["Corr_Data_point_amplitude"]=abs(myQuantification.correctedIQData["iqSignal"][yAxisValInd])
		return plotData
	def plot_1D_IQ () :
		plotData["Data_point_I"]= myExtendMeasurement.rawData["iqSignal"][yAxisValInd].real
		plotData["Data_point_Q"]= myExtendMeasurement.rawData["iqSignal"][yAxisValInd].imag
		if myQuantification.fitCurve["x"].shape[0] != 0:
			plotData["Fitted_curve_I"]= plot_1D_show( myQuantification.fitCurve["iqSignal"][yAxisValInd].real )
			plotData["Fitted_curve_Q"]= plot_1D_show( myQuantification.fitCurve["iqSignal"][yAxisValInd].imag )
		if myQuantification.correctedIQData["x"].shape[0] != 0:
			plotData["Corr_Data_point_I"]= myQuantification.correctedIQData["iqSignal"][yAxisValInd].real
			plotData["Corr_Data_point_Q"]= myQuantification.correctedIQData["iqSignal"][yAxisValInd].imag
		return plotData
	plotFunction = {
		'2D_amp': plot_2D_amp,
		'1D_amp': plot_1D_amp,
		'1D_IQ': plot_1D_IQ,
	}
	return json.dumps(plotFunction[plotType](), cls=NumpyEncoder)



@bp.route('/qestimate/getJson_fitParaPlot',methods=['POST','GET'])
def getJson_fitParaPlot():

	myExtendMeasurement = benchmarkDict[session['user_name']]
	myQuantification = QDict[session['user_name']] 

	fitParameters = json.loads(request.args.get('fitParameters'))
	
	if fitParameters == "None":
		myQuantification.fitParameters = None
	else:
		myQuantification.fitParameters = fitParameters
	#print( "Fit parameters: ",fitParameters)
	myQuantification.do_analysis()
	plotData = myQuantification.fitResult
	

	# plotData = myQuantification.fitResult["results"]
	# plotData.update(myQuantification.fitResult["errors"])
	# plotData.update(myQuantification.fitResult["extendResults"])
	#print("Fit plot results: ",plotData)
	analysisIndex = json.loads(request.args.get('analysisIndex'))

	dimension = len(analysisIndex["axisIndex"])
	if dimension == 2:
		axisInd = analysisIndex["axisIndex"][1]
		yAxisKey = myExtendMeasurement.measurementObj.corder["C-Structure"][axisInd] 
		plotData[yAxisKey] = myExtendMeasurement.independentVars[myExtendMeasurement.yAxisKey]

	else:
		yAxisKey = None
		plotData["Single_plot"] = array(1)
		#plotData["Single_plot"] = myExtendMeasurement.fitResult["extendResults"]["power_corr"]
	print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA Fit results: ", plotData)

	return json.dumps(plotData, cls=NumpyEncoder)


@bp.route('/qestimate/exportMat_fitPara',methods=['POST','GET'])
def exportMat_fitPara():
	try:
		myExtendMeasurement = benchmarkDict[session['user_name']]
		set_mat_analysis( myExtendMeasurement.fitResult, 'ExtendMeasurement[%s]'%session['user_name'] )
		status = "Success"
	except:
		status = "Fail"
	return jsonify(status=status, user_name=session['user_name'], qumport=int(get_status("WEB")['port']))



@bp.route('/test',methods=['POST','GET'])
def testFunc():

	measurementObj = get_measurementObject('frequency_response')

	print(measurementObj.corder[0])
	return jsonify(measurementObj.corder)

print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this

		#stage, prev = clocker(0, agenda="2D Fresp")
		#stage, prev = clocker(stage, prev, agenda="2D Fresp") # Marking time
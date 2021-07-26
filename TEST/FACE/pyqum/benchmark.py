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
# Please Delete this line in another branch (to: @Jackie)
from pyqum.directive.quantification import QEstimation 
from pyqum.mission import get_measurementObject

# Fitting
from resonator_tools.circuit import notch_port
from collections import defaultdict

# Save file
from scipy.io import savemat


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
		return render_template("blog/benchmark/benchmark.html")
	return("<h3>WHO ARE YOU?</h3><h3>Please F**k*ng Login!</h3><h3>Courtesy from <a href='http://qum.phys.sinica.edu.tw:5300/auth/login'>HoDoR</a></h3>")

@bp.route('/get_parametersID', methods=['POST', 'GET'])
def get_parametersID():
	myQEstimation = qEstimationDict[session['user_name']]
	htmlInfo = myQEstimation.get_htmlInfo()
	return jsonify(htmlInfo)

@bp.route('/qestimate', methods=['POST', 'GET'])
def qestimate(): 
	myQEstimation = qEstimationDict[session['user_name']]
	corder = myQEstimation.measurementObj.corder
	independentVars = myQEstimation.independentVars
	freqKey = myQEstimation.freqKey

	htmlInfo = myQEstimation.get_htmlInfo()
	varNumber = len(htmlInfo)
	return render_template("blog/benchmark/qestimate.html", corder=corder, independentVars=independentVars, freqKey=freqKey, varNumber=varNumber, htmlInfo=htmlInfo)

@bp.route('/benchmark_getMeasurement', methods=['POST', 'GET'])
def benchmark_getMeasurement(): 
	global qEstimationDict
	measurementType = request.args.get('measurementType')
	qEstimationDict[session['user_name']] = QEstimation( get_measurementObject(measurementType) )
	print("Measurement Obj Init", qEstimationDict[session['user_name']].measurementObj.corder)
	return "Send Measurement Object"



@bp.route('/get_user', methods=['POST', 'GET'])
def get_user():
	return jsonify(session['user_name'])

@bp.route('/measurement_info', methods=['POST', 'GET'])
def measurement_info(): 

	myMeasurement = qEstimationDict[session['user_name']].measurementObj

	if 'jobid' in myMeasurement.perimeter.keys(): 
		JOBID = myMeasurement.perimeter['jobid']

	return render_template("blog/benchmark/measurement_info.html", JOBID=JOBID)



# Each user have own QEstimation object
qEstimationDict = {}


@bp.route('/qestimate/getJson_plot',methods=['POST','GET'])
def getJson_plot():

	myQEstimation = qEstimationDict[session['user_name']]
	analysisIndex = json.loads(request.args.get('analysisIndex'))
	plotType = json.loads(request.args.get('plotType'))

	valueInd = analysisIndex["valueIndex"]
	dimension = len(analysisIndex["axisIndex"])
	if dimension == 1:
		axisInd = analysisIndex["axisIndex"][0]
		yAxisKey = myQEstimation.measurementObj.corder["C-Structure"][axisInd]
		yAxisValInd = valueInd[axisInd]
	else:
		yAxisKey = None
		yAxisValInd = 0

	preYAxisKey = myQEstimation.yAxisKey
	preValueInd = myQEstimation.varsInd
	if preYAxisKey != yAxisKey  or ( yAxisKey==None and preValueInd != valueInd):
		print("Previous index",preValueInd,"New index",valueInd)
		myQEstimation.reshape_Data( valueInd, yAxisKey=yAxisKey )


	print("Plot type: ", plotType)
	print("Plot shape Raw: ",myQEstimation.rawData["iqSignal"].shape, "Fit:", myQEstimation.fitCurve["iqSignal"].shape,)
	print("yAxisKey: ",yAxisKey)

	plotData = {}

	#print(plotData)
	def plot_1D_show( originalArray ) :
		fitRangeBoolean = logical_and(myQEstimation.rawData["frequency"]>=float(myQEstimation.fitParameters["range"]["from"]),myQEstimation.rawData["frequency"]<=float(myQEstimation.fitParameters["range"]["to"]) )
		return originalArray[fitRangeBoolean]

	def plot_2D_amp () :
		plotData[yAxisKey]= myQEstimation.independentVars[myQEstimation.yAxisKey]
		plotData["frequency"]= myQEstimation.rawData["frequency"]
		plotData["amplitude"]= abs(myQEstimation.rawData["iqSignal"])
		return plotData
	def plot_1D_amp () :
		plotData["Data_point_frequency"]= myQEstimation.rawData["frequency"]
		plotData["Data_point_amplitude"]= abs(myQEstimation.rawData["iqSignal"][yAxisValInd])
		if myQEstimation.fitCurve["frequency"].shape[0] != 0:
			plotData["Fitted_curve_frequency"]=plot_1D_show( myQEstimation.fitCurve["frequency"] )
			plotData["Fitted_curve_amplitude"]=plot_1D_show( abs(myQEstimation.fitCurve["iqSignal"][yAxisValInd]) )
		if myQEstimation.baseline["frequency"].shape[0] != 0:
			plotData["Fitted_baseline_frequency"]=myQEstimation.fitCurve["frequency"]
			plotData["Fitted_baseline_amplitude"]=abs(myQEstimation.baseline["iqSignal"][yAxisValInd])
		if myQEstimation.correctedIQData["frequency"].shape[0] != 0:
			plotData["Corr_Data_point_frequency"]=myQEstimation.fitCurve["frequency"]
			plotData["Corr_Data_point_amplitude"]=abs(myQEstimation.correctedIQData["iqSignal"][yAxisValInd])
		return plotData
	def plot_1D_IQ () :
		plotData["Data_point_I"]= myQEstimation.rawData["iqSignal"][yAxisValInd].real
		plotData["Data_point_Q"]= myQEstimation.rawData["iqSignal"][yAxisValInd].imag
		if myQEstimation.fitCurve["frequency"].shape[0] != 0:
			plotData["Fitted_curve_I"]= plot_1D_show( myQEstimation.fitCurve["iqSignal"][yAxisValInd].real )
			plotData["Fitted_curve_Q"]= plot_1D_show( myQEstimation.fitCurve["iqSignal"][yAxisValInd].imag )
		# if myQEstimation.baseline["frequency"].shape[0] != 0:
		# 	plotData["Fitted_baseline_I"]= myQEstimation.baseline["iqSignal"][yAxisValInd].real
		# 	plotData["Fitted_baseline_Q"]= myQEstimation.baseline["iqSignal"][yAxisValInd].imag
		if myQEstimation.correctedIQData["frequency"].shape[0] != 0:
			plotData["Corr_Data_point_I"]= myQEstimation.correctedIQData["iqSignal"][yAxisValInd].real
			plotData["Corr_Data_point_Q"]= myQEstimation.correctedIQData["iqSignal"][yAxisValInd].imag
		return plotData
	plotFunction = {
		'2D_amp': plot_2D_amp,
		'1D_amp': plot_1D_amp,
		'1D_IQ': plot_1D_IQ,
	}
	return json.dumps(plotFunction[plotType](), cls=NumpyEncoder)

	#return json.dumps(plotData, cls=NumpyEncoder)


@bp.route('/qestimate/getJson_fitParaPlot',methods=['POST','GET'])
def getJson_fitParaPlot():

	myQEstimation = qEstimationDict[session['user_name']]
	fitParameters = json.loads(request.args.get('fitParameters'))

	myQEstimation.fitParameters = fitParameters
	print( "Fit parameters: ",fitParameters)
	myQEstimation.do_analysis()
	print("Fit results: ",myQEstimation.fitResult)

	plotData = myQEstimation.fitResult["results"]
	plotData.update(myQEstimation.fitResult["errors"])
	plotData.update(myQEstimation.fitResult["extendResults"])
	print("Fit plot results: ",plotData)
	analysisIndex = json.loads(request.args.get('analysisIndex'))

	dimension = len(analysisIndex["axisIndex"])
	if dimension == 1:
		axisInd = analysisIndex["axisIndex"][0]
		yAxisKey = myQEstimation.measurementObj.corder["C-Structure"][axisInd] 
		plotData[yAxisKey] = myQEstimation.independentVars[myQEstimation.yAxisKey]

	else:
		yAxisKey = None
		plotData["Single_plot"] = array(1)
		#plotData["Single_plot"] = myQEstimation.fitResult["extendResults"]["power_corr"]

	return json.dumps(plotData, cls=NumpyEncoder)

@bp.route('/qestimate/exportMat_fitPara',methods=['POST','GET'])
def exportMat_fitPara():
	try:
		myQEstimation = qEstimationDict[session['user_name']]
		matData = myQEstimation.fitResult["results"]
		matData.update(myQEstimation.fitResult["errors"])
		matData.update(myQEstimation.fitResult["extendResults"])
		set_mat_analysis( matData, 'QEstimation[%s]'%session['user_name'] )
		status = "Success"
	except:
		status = "Fail"
	return jsonify(status=status, user_name=session['user_name'], qumport=int(get_status("WEB")['port']))

@bp.route('/test',methods=['POST','GET'])
def testFunc():

	measurementObj = get_measurementObject('frequency_response')

	print(measurementObj.corder[0])
	return jsonify(measurementObj.corder)


def send_Measurement_to_QEstimation():
	measurementObj =  get_measurementObject('frequency_response') 
	return measurementObj

print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this

		#stage, prev = clocker(0, agenda="2D Fresp")
		#stage, prev = clocker(stage, prev, agenda="2D Fresp") # Marking time
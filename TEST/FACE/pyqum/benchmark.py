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
from numpy import array, unwrap, mean, trunc, sqrt, zeros, ones, shape, arctan2, int64, isnan, abs, empty, ndarray, moveaxis, reshape, logical_and, nan, angle, arange, stack

# Load instruments
from pyqum.directive.quantification import ExtendMeasurement, QEstimation, PopulationDistribution, Common_fitting, Autoflux, Readout_fidelity
from pyqum.mission import get_measurementObject

# Fitting
from resonator_tools.circuit import notch_port
from collections import defaultdict

# Save file
from scipy.io import savemat


encryp = 'ghhgjadz'
bp = Blueprint(myname, __name__, url_prefix='/benchmark')

# Main

## Common function
class NumpyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, ndarray):
			return obj.tolist()
			
		return json.JSONEncoder.default(self, obj)
	
def find_nearestInd(array, value):
    #array = asarray(array)
    idx = int((abs(array - value)).argmin())
    return idx


@bp.route('/')
def show():
	with suppress(KeyError):
		print(Fore.LIGHTBLUE_EX + "USER " + Fore.YELLOW + "%s "%session['user_name'] + Fore.LIGHTBLUE_EX + "has just logged in as Guest #%s!"%session['user_id'])
		# Security implementation:
		if not g.user['instrument']:
			abort(404)
		#quantificationType = benchmarkDict[session['user_name']].quantificationType
		return render_template("blog/benchmark/benchmark.html")
	return("<h3>WHO ARE YOU?</h3><h3>Please Kindly Login!</h3><h3>Courtesy from <a href='http://qum.phys.sinica.edu.tw:%s/auth/login'>HoDoR</a></h3>" %get_status("WEB")["port"])

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

@bp.route('/populationDistribution', methods=['POST', 'GET'])
def populationDistribution():
	return render_template("blog/benchmark/populationDistribution.html")

@bp.route('/common_fitting', methods=['POST', 'GET'])
def common_fitting():
	return render_template("blog/benchmark/common_fitting.html")

@bp.route('/autoflux', methods=['POST', 'GET'])
def autoflux():
	return render_template("blog/benchmark/autoflux.html")

@bp.route('/plot', methods=['POST', 'GET'])
def plot():
	return render_template("blog/benchmark/plot.html", url ='fitness.png')

@bp.route('/fidelity', methods=['POST', 'GET'])
def fidelity():
	return render_template("blog/benchmark/fidelity.html")

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
# Test str

@bp.route('/register_Quantification',methods=['POST','GET'])
def register_Quantification():
	myExtendMeasurement = benchmarkDict[session['user_name']]
	quantificationType = json.loads(request.args.get('quantificationType'))
	def get_qEstimation ( myExtendMeasurement ):
		return QEstimation(myExtendMeasurement)
	def get_PopulationDistribution ( myExtendMeasurement ):
		return PopulationDistribution(myExtendMeasurement)
	def get_common_fitting ( myExtendMeasurement ):
		return Common_fitting(myExtendMeasurement)
	def get_autoflux ( myExtendMeasurement ):
		return Autoflux(myExtendMeasurement)
	def get_fidelity ( myExtendMeasurement ):
		return Readout_fidelity(myExtendMeasurement)
	
	quantification = {
		'qEstimation': get_qEstimation,
		'populationDistribution': get_PopulationDistribution,
		'common_fitting': get_common_fitting,
		'autoflux': get_autoflux,
		'fidelity':get_fidelity,
	}
	print(quantificationType+" is registed!!")
	try: QDict[session['user_name']] = quantification[quantificationType](myExtendMeasurement)
	except(KeyError): print("No such quantification type")
	return json.dumps(quantificationType, cls=NumpyEncoder)



### qestimate part

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
		"aveRange": aveRange,
		"oneShotAxisIndex": [],
	}


	xAxisKey = myExtendMeasurement.measurementObj.corder["C-Structure"][axisInd[0]]

	if dimension == 2:
		yAxisKey = myExtendMeasurement.measurementObj.corder["C-Structure"][axisInd[1]]
		yAxisValInd = valueInd[axisInd[1]]
	elif dimension == 1:
		yAxisKey = None
		yAxisValInd = 0

	## Block user click plot frequently
	# preAxisInd = myExtendMeasurement.axisInd
	# preValueInd = myExtendMeasurement.varsInd
	# if preAxisInd != axisInd  or ( yAxisKey==None and preValueInd != valueInd) or aveInfo!=aveInfo:
	# 	print("Previous index",preValueInd,"New index",valueInd)
	# 	myExtendMeasurement.reshape_Data( valueInd, axisInd=axisInd, aveInfo=aveInfo )
	myExtendMeasurement.reshape_Data( valueInd, axisInd=axisInd, aveInfo=aveInfo )

	print("Plot type: ", plotType)
	print("Plot shape Raw: ",myExtendMeasurement.rawData["iqSignal"].shape)
	print("Plot shape Fit:", myQuantification.fitCurve["iqSignal"].shape)
	print("yAxisKey: ",yAxisKey)

	plotData = {}

	#print(plotData)
	def plot_1D_show( originalArray ) :
		fitRangeBoolean = logical_and(myExtendMeasurement.rawData["x"]>=float(myQuantification.fitParameters["interval"]["start"]),myExtendMeasurement.rawData["x"]<=float(myQuantification.fitParameters["interval"]["end"]) )
		return originalArray[fitRangeBoolean]

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
			plotData["Fitted_baseline_frequency"]=myExtendMeasurement.rawData["x"]
			plotData["Fitted_baseline_amplitude"]=abs(myQuantification.baseline["iqSignal"][yAxisValInd])
		if myQuantification.correctedIQData["x"].shape[0] != 0:
			plotData["Corr_Data_point_frequency"]=myExtendMeasurement.rawData["x"]
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
	def plot_1D_all () :
		rawDataComplex = myExtendMeasurement.rawData["iqSignal"][yAxisValInd]
		RawDataXaxis = myExtendMeasurement.rawData["x"]
		plotData = {}
		plotRaw = {
			xAxisKey: RawDataXaxis,
			"I": rawDataComplex.real,
			"Q": rawDataComplex.imag,
			"Amplitude": abs(rawDataComplex),
			"Phase": angle(rawDataComplex),
		}

		plotData["raw"] = plotRaw
		# plot fitted cerve
		fitXaxis = myQuantification.fitCurve["x"]
		if fitXaxis.shape[0] != 0:
			complexFitData = myQuantification.fitCurve["iqSignal"][yAxisValInd]
			plotFit = {
				xAxisKey: plot_1D_show(fitXaxis) ,
				"I": complexFitData.real,
				"Q": complexFitData.imag,
				"Amplitude": abs(complexFitData),
				"Phase": angle(complexFitData),
			}
			plotData["fitted"] = plotFit

		try:
			baselineXaxis = myQuantification.baseline["x"]
			if baselineXaxis.shape[0] != 0:
				complexBaselineData = myQuantification.baseline["iqSignal"][yAxisValInd]
				plotBaseline = {
					xAxisKey: plot_1D_show(baselineXaxis) ,
					"I": complexBaselineData.real,
					"Q": complexBaselineData.imag,
					"Amplitude": abs(complexBaselineData),
					"Phase": angle(complexBaselineData),
				}
				plotData["baseline"] = plotBaseline
		except:
			pass

		try:
			corrXaxis = myQuantification.correctedIQData["x"]	
			if corrXaxis.shape[0] != 0:
				complexcorrectedData = myQuantification.correctedIQData["iqSignal"][yAxisValInd]
				plotCorrectedData = {
					xAxisKey: plot_1D_show(corrXaxis) ,
					"I": complexcorrectedData.real,
					"Q": complexcorrectedData.imag,
					"Amplitude": abs(complexcorrectedData),
					"Phase": angle(complexcorrectedData),
				}
				plotData["corrected"] = plotCorrectedData
		except:
			pass

		return plotData
	plotFunction = {
		'2D_amp': plot_2D_amp,
		'1D_amp': plot_1D_amp,
		'1D_IQ': plot_1D_IQ,
		'1D_all': plot_1D_all,
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
	plotData["dependentVar"] = {}

	# plotData = myQuantification.fitResult["results"]P1

	# plotData.update(myQuantification.fitResult["errors"])
	# plotData.update(myQuantification.fitResult["extendResults"])
	analysisIndex = json.loads(request.args.get('analysisIndex'))

	dimension = len(analysisIndex["axisIndex"])

	if dimension == 2:
		axisInd = analysisIndex["axisIndex"][1]
		yAxisKey = myExtendMeasurement.measurementObj.corder["C-Structure"][axisInd] 
		plotData["dependentVar"][yAxisKey] = myExtendMeasurement.independentVars[myExtendMeasurement.yAxisKey]

	else:
		yAxisKey = None
		plotData["Single_plot"] = array(1)
		#plotData["Single_plot"] = myExtendMeasurement.fitResult["extendResults"]["power_corr"]
	print("Fit plot results: ",json.dumps(plotData, cls=NumpyEncoder))
	return json.dumps(plotData, cls=NumpyEncoder).replace('NaN','null')
	#return json.dumps(plotData, cls=NumpyEncoder).replace('NaN','')


@bp.route('/qestimate/exportMat_fitPara',methods=['POST','GET'])
def exportMat_fitPara():
	try:
		myExtendMeasurement = benchmarkDict[session['user_name']]
		set_mat_analysis( myExtendMeasurement.fitResult, 'ExtendMeasurement[%s]'%session['user_name'] )

		status = "Success"
	except:
		status = "Fail"
	return jsonify(status=status, user_name=session['user_name'], qumport=int(get_status("WEB")['port']))

### common_fitting part
@bp.route('/common_fitting/load',methods=['POST','GET'])
def ComFit_load():
	myExtendMeasurement = benchmarkDict[session['user_name']]
	myQuantification = QDict[session['user_name']] 

	analysisIndex = json.loads(request.args.get('analysisIndex'))

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
		"aveRange": aveRange,
		"oneShotAxisIndex": [],
	}


	## Block user click plot frequently
	# preAxisInd = myExtendMeasurement.axisInd
	# preValueInd = myExtendMeasurement.varsInd
	# if preAxisInd != axisInd  or ( yAxisKey==None and preValueInd != valueInd) or aveInfo!=aveInfo:
	# 	print("Previous index",preValueInd,"New index",valueInd)
	# 	myExtendMeasurement.reshape_Data( valueInd, axisInd=axisInd, aveInfo=aveInfo )
	myExtendMeasurement.reshape_Data( valueInd, axisInd=axisInd, aveInfo=aveInfo )
	return json.dumps("Data reshaped", cls=NumpyEncoder)

def get_maskArray( refArray, maskRange ) :
		fitRangeBoolean = logical_and(refArray>=maskRange[0],refArray<=maskRange[1] )
		return fitRangeBoolean

@bp.route('/common_fitting/getJson_plotAxis',methods=['POST','GET'])
def ComFit_getJson_plotAxis():
	myExtendMeasurement = benchmarkDict[session['user_name']]
	myQuantification = QDict[session['user_name']] 

	
	yAxisKey = myExtendMeasurement.yAxisKey

	axisType = json.loads(request.args.get('plot1D_axisType'))
	print("Axis type: ", axisType)
	def plot_yAxis_index():
		if yAxisKey != None:
			plotData= arange( myExtendMeasurement.independentVars[yAxisKey].shape[0] )
		else:
			plotData=[0]
		return plotData

	def plot_yAxis_value():
		if yAxisKey != None:
			plotData= myExtendMeasurement.independentVars[yAxisKey]
		else:
			plotData=[0]
		return plotData

	def plot_xAxis():
		plotData= myExtendMeasurement.rawData["x"]
		return plotData

	def plot_xAxis_fit():
		maskArray= get_maskArray(myExtendMeasurement.rawData["x"],myQuantification.fitParameters["range"])
		plotData= myExtendMeasurement.rawData["x"][maskArray]
		return plotData

	plotFunction = {
		'y_index': plot_yAxis_index,
		'y_value': plot_yAxis_value,
		'x_value': plot_xAxis,
		'x_value_fit': plot_xAxis_fit,
	}
	return json.dumps(plotFunction[axisType](), cls=NumpyEncoder)


@bp.route('/common_fitting/getJson_plot2D',methods=['POST','GET'])
def ComFit_getJson_plot2D():
	myExtendMeasurement = benchmarkDict[session['user_name']]
	myQuantification = QDict[session['user_name']] 

	xAxisKey = myExtendMeasurement.xAxisKey
	yAxisKey = myExtendMeasurement.yAxisKey
	signalType = json.loads(request.args.get('plot2D_signalType'))
	print("Z Data type: ", signalType)
	def plot_2DAmp ():
		plotData= abs(myExtendMeasurement.rawData["iqSignal"])
		return plotData
	def plot_2DPhase ():
		plotData= angle(myExtendMeasurement.rawData["iqSignal"])
		return plotData

	plotFunction = {
		'amp': plot_2DAmp,
		'phase': plot_2DPhase,
	}
	return json.dumps(plotFunction[signalType](), cls=NumpyEncoder)


@bp.route('/common_fitting/getJson_plot1D',methods=['POST','GET'])
def ComFit_getJson_plot1D():
	myExtendMeasurement = benchmarkDict[session['user_name']]
	myQuantification = QDict[session['user_name']] 

	plotInfo = json.loads(request.args.get('plotInfo'))
	process = json.loads(request.args.get('process'))

	yAxisValInd = 0
	yAxisKey = myExtendMeasurement.yAxisKey
	if yAxisKey != None:
		if plotInfo["selectType"] == "y_index":
			yAxisValInd = int(plotInfo["selectValue"])
		else:
			yAxis = myExtendMeasurement.independentVars[yAxisKey]
			yAxisValInd = find_nearestInd(yAxis,float(plotInfo["selectValue"]))

	xAxisKey = myExtendMeasurement.xAxisKey

	print("yAxis value Index: ", yAxisValInd)


	plotData = {}

	#print(plotData)


	def plot_1D_raw () :
		# plot raw data
		rawDataComplex = myExtendMeasurement.rawData["iqSignal"][yAxisValInd]
		plotData = {
			"I": rawDataComplex.real,
			"Q": rawDataComplex.imag,
			"Amplitude": abs(rawDataComplex),
			"Phase": angle(rawDataComplex),
		}
		return plotData
	def plot_1D_fit () :
		# plot raw data
		try:
			fittedDataComplex = myQuantification.fitCurve["iqSignal"][yAxisValInd]
			plotData = {
				"I": fittedDataComplex.real,
				"Q": fittedDataComplex.imag,
				"Amplitude": abs(fittedDataComplex),
				"Phase": angle(fittedDataComplex),
			}
		except:
			plotData = {
				"I": [],
				"Q": [],
				"Amplitude": [],
				"Phase": [],
			}
		return plotData

	plotFunction = {
		'raw': plot_1D_raw,
		'fitted': plot_1D_fit,
	}
	return json.dumps(plotFunction[process](), cls=NumpyEncoder)


@bp.route('/common_fitting/getJson_fitParaPlot',methods=['POST','GET'])
def ComFit_getJson_fitParaPlot():

	myExtendMeasurement = benchmarkDict[session['user_name']]
	myQuantification = QDict[session['user_name']] 

	fitParameters = json.loads(request.args.get('fitParameters'))

	myQuantification.fitParameters = fitParameters
	myQuantification.do_analysis()

	plotData={
		"parKey":{},
		"data":{},
	}
	errorKeys=[]
	for par in myQuantification.fitResult.keys():
		plotData["data"][par]= myQuantification.fitResult[par]["value"]
		errorKey = par+"_err"
		errorKeys.append(errorKey)
		plotData["data"][errorKey]= myQuantification.fitResult[par]["error"]

	plotData["parKey"]["val"]=list(myQuantification.fitResult.keys())
	plotData["parKey"]["err"]=errorKeys

	# print("Fit plot results: ",json.dumps(plotData, cls=NumpyEncoder))
	return json.dumps(plotData, cls=NumpyEncoder).replace('NaN','null')


@bp.route('/common_fitting/exportMat_fitPara',methods=['POST','GET'])
def ComFit_exportMat_fitPara():
	try:
		myExtendMeasurement = benchmarkDict[session['user_name']]
		set_mat_analysis( myExtendMeasurement.fitResult, 'ExtendMeasurement[%s]'%session['user_name'] )

		status = "Success"
	except:
		status = "Fail"
	return jsonify(status=status, user_name=session['user_name'], qumport=int(get_status("WEB")['port']))


### populationDistribution part

@bp.route('/populationDistribution/load',methods=['POST','GET'])
def PopDis_load():
	myExtendMeasurement = benchmarkDict[session['user_name']]
	myQuantification = QDict[session['user_name']] 

	analysisIndex = json.loads(request.args.get('analysisIndex'))

	valueInd = analysisIndex["valueIndex"]
	axisInd = analysisIndex["axisIndex"]
	dimension = len(axisInd)

	# Get average information from JS
	aveAxisInd = analysisIndex["aveInfo"]["axisIndex"]
	aveRange = 0
	# Construct average informaion to reshape
	if len(aveAxisInd) !=0:
		aveRange = [int(k) for k in analysisIndex["aveInfo"]["aveRange"].split(",")]


	# Construct accumulate informaion to reshape
	oneShotAxisInd = analysisIndex["oneShot_Info"]["axisIndex"]
	if len(oneShotAxisInd) ==0:
		print("AAAAAAAAAAAAAAAAAAAAAAAAAA")

	aveInfo = {
		"axisIndex": aveAxisInd,
		"aveRange": aveRange,
		"oneShotAxisIndex": oneShotAxisInd,
	}
	myExtendMeasurement.reshape_Data( valueInd, axisInd=axisInd, aveInfo=aveInfo )
	return json.dumps("Data reshaped", cls=NumpyEncoder)



@bp.route('/populationDistribution/getJson_plotAxis',methods=['POST','GET'])
def PopDis_getJson_plotAxis():
	myExtendMeasurement = benchmarkDict[session['user_name']]
	myQuantification = QDict[session['user_name']] 

	
	yAxisKey = myExtendMeasurement.yAxisKey

	axisType = json.loads(request.args.get('plot1D_axisType'))
	print("Axis type: ", axisType)
	def plot_yAxis_index():
		if yAxisKey != None:
			plotData= arange( myExtendMeasurement.independentVars[yAxisKey].shape[0] )
		else:
			plotData=[0]
		return plotData

	def plot_yAxis_value():
		if yAxisKey != None:
			plotData= myExtendMeasurement.independentVars[yAxisKey]
		else:
			plotData=[0]
		return plotData

	def plot_xAxis():
		plotData= myExtendMeasurement.rawData["x"]
		return plotData

	def plot_xAxis_fit():
		maskArray= get_maskArray(myExtendMeasurement.rawData["x"],myQuantification.fitParameters["range"])
		plotData= myExtendMeasurement.rawData["x"][maskArray]
		return plotData

	plotFunction = {
		'y_index': plot_yAxis_index,
		'y_value': plot_yAxis_value,
		'x_value': plot_xAxis,
		'x_value_fit': plot_xAxis_fit,
	}
	return json.dumps(plotFunction[axisType](), cls=NumpyEncoder)


@bp.route('/populationDistribution/getJson_plot2D',methods=['POST','GET'])
def PopDis_getJson_plot2D():
	myExtendMeasurement = benchmarkDict[session['user_name']]
	myQuantification = QDict[session['user_name']] 

	xAxisKey = myExtendMeasurement.xAxisKey
	yAxisKey = myExtendMeasurement.yAxisKey
	signalType = json.loads(request.args.get('plot2D_signalType'))
	print("Z Data type: ", signalType)
	def plot_2DAmp ():
		plotData= abs(myExtendMeasurement.rawData["iqSignal"])
		return plotData
	def plot_2DPhase ():
		plotData= angle(myExtendMeasurement.rawData["iqSignal"])
		return plotData

	plotFunction = {
		'amp': plot_2DAmp,
		'phase': plot_2DPhase,
	}
	return json.dumps(plotFunction[signalType](), cls=NumpyEncoder)


@bp.route('/populationDistribution/getJson_plotProjection',methods=['POST','GET'])
def PopDis_getJson_plotProjection():
	myExtendMeasurement = benchmarkDict[session['user_name']]
	myQuantification = QDict[session['user_name']] 

	accInfo = json.loads(request.args.get('projectionLine'))
	process = json.loads(request.args.get('process'))
	accumulationIndex = [int(k) for k in accInfo["accumulationIndex"].split(",")]

	myQuantification.accumulate_data(accumulationIndex)

	projectionLine= myQuantification.fit_projectionLine()

	plotData = {}

	#print(plotData)


	def plot_1D_raw () :
		# plot raw data
		rawDataComplex = myQuantification.accData["raw"]
		plotData = {
			"I": rawDataComplex.real,
			"Q": rawDataComplex.imag,
		}
		return plotData
	def plot_1D_fit () :
		# plot fitted data
		fittedDataComplex = myQuantification.projectionLine["data"]
		plotData = {
			"I": fittedDataComplex.real,
			"Q": fittedDataComplex.imag,
		}
		return plotData

	plotFunction = {
		'raw': plot_1D_raw,
		'fitted': plot_1D_fit,
	}
	return json.dumps(plotFunction[process](), cls=NumpyEncoder)


@bp.route('/populationDistribution/getJson_plotDistribution',methods=['POST','GET'])
def PopDis_getJson_plotDistribution():

	myExtendMeasurement = benchmarkDict[session['user_name']]
	myQuantification = QDict[session['user_name']] 

	myQuantification.cal_projectedData()
	distributionData= myQuantification.cal_distribution()

	plotData={
		"x":distributionData["x"],
		"data":distributionData["count"],
		"fit":distributionData["fitted"],
	}

	# print("Fit plot results: ",json.dumps(plotData, cls=NumpyEncoder))
	return json.dumps(plotData, cls=NumpyEncoder).replace('NaN','null')


@bp.route('/populationDistribution/exportMat_fitPara',methods=['POST','GET'])
def PopDis_exportMat_fitPara():
	try:
		myExtendMeasurement = benchmarkDict[session['user_name']]
		set_mat_analysis( myExtendMeasurement.fitResult, 'ExtendMeasurement[%s]'%session['user_name'] )

		status = "Success"
	except:
		status = "Fail"
	return jsonify(status=status, user_name=session['user_name'], qumport=int(get_status("WEB")['port']))

print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this

		#stage, prev = clocker(0, agenda="2D Fresp")
		#stage, prev = clocker(stage, prev, agenda="2D Fresp") # Marking time

### autoflux part
@bp.route('/autoflux/load',methods=['POST','GET'])
def Auflux_load():
	myExtendMeasurement = benchmarkDict[session['user_name']]
	myQuantification = QDict[session['user_name']] 

	analysisIndex = json.loads(request.args.get('analysisIndex'))

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
		"aveRange": aveRange,
		"oneShotAxisIndex": [],
	}


	## Block user click plot frequently
	# preAxisInd = myExtendMeasurement.axisInd
	# preValueInd = myExtendMeasurement.varsInd
	# if preAxisInd != axisInd  or ( yAxisKey==None and preValueInd != valueInd) or aveInfo!=aveInfo:
	# 	print("Previous index",preValueInd,"New index",valueInd)
	# 	myExtendMeasurement.reshape_Data( valueInd, axisInd=axisInd, aveInfo=aveInfo )
	myExtendMeasurement.reshape_Data( valueInd, axisInd=axisInd, aveInfo=aveInfo )
	return json.dumps("Data reshaped", cls=NumpyEncoder)

@bp.route('/autoflux/getJson_fitParaPlot',methods=['POST','GET'])
def Auflux_getJson_fitParaPlot():

	myExtendMeasurement = benchmarkDict[session['user_name']]
	myQuantification = QDict[session['user_name']] 

	# fitParameters = json.loads(request.args.get('fitParameters'))

	# myQuantification.fitParameters = fitParameters
	myQuantification.do_analysis()
	return json.dumps("finished", cls=NumpyEncoder)

### readout_fidelity part
@bp.route('/fidelity/load',methods=['POST','GET'])
def Readout_fidelity_load():
	myExtendMeasurement = benchmarkDict[session['user_name']]
	myQuantification = QDict[session['user_name']] 

	analysisIndex = json.loads(request.args.get('analysisIndex'))

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
		"aveRange": aveRange,
		"oneShotAxisIndex": [],
	}


	## Block user click plot frequently
	# preAxisInd = myExtendMeasurement.axisInd
	# preValueInd = myExtendMeasurement.varsInd
	# if preAxisInd != axisInd  or ( yAxisKey==None and preValueInd != valueInd) or aveInfo!=aveInfo:
	# 	print("Previous index",preValueInd,"New index",valueInd)
	# 	myExtendMeasurement.reshape_Data( valueInd, axisInd=axisInd, aveInfo=aveInfo )
	myExtendMeasurement.reshape_Data( valueInd, axisInd=axisInd, aveInfo=aveInfo )
	return json.dumps("Data reshaped", cls=NumpyEncoder)

@bp.route('/fidelity/getJson_fitParaPlot',methods=['POST','GET'])
def Readout_fidelity_getJson_fitParaPlot():

	myExtendMeasurement = benchmarkDict[session['user_name']]
	myQuantification = QDict[session['user_name']] 

	# fitParameters = json.loads(request.args.get('fitParameters'))

	# myQuantification.fitParameters = fitParameters
	myQuantification.do_analysis()
	return json.dumps("AAAAAAA", cls=NumpyEncoder)

@bp.route('/fidelity/getJson_Pretrain',methods=['POST','GET'])
def Readout_fidelity_getJson_Pretrain():

	myExtendMeasurement = benchmarkDict[session['user_name']]
	myQuantification = QDict[session['user_name']] 

	# fitParameters = json.loads(request.args.get('fitParameters'))

	# myQuantification.fitParameters = fitParameters
	myQuantification.pre_analytic()
	return json.dumps("A", cls=NumpyEncoder)
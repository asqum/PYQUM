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

# Load quantification method
from pyqum.directive.quantification import ExtendMeasurement, QEstimation, PopulationDistribution, Common_fitting, Autoflux, Readout_fidelity, CavitySearch
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

@bp.route('/cavitySearch', methods=['POST', 'GET'])
def cavitySearch():
	return render_template("blog/benchmark/cavitySearch.html")

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
	def get_CavitySearch ( myExtendMeasurement ):
		return CavitySearch(myExtendMeasurement)
    
	quantification = {
		'qEstimation': get_qEstimation,
		'populationDistribution': get_PopulationDistribution,
		'common_fitting': get_common_fitting,
		'autoflux': get_autoflux,
		'fidelity':get_fidelity,
    'cavitySearch': get_CavitySearch,
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

	# plotData = myQuantification.fitResult["results"]

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
	oneShotAxisInd = analysisIndex["oneShot_Info"]["axisIndex"]
	aveRange = 0
	oneShotCenters = 0
	# Construct average informaion to reshape
	if len(aveAxisInd) !=0:
		aveRange = [int(k) for k in analysisIndex["aveInfo"]["aveRange"].split(",")]
	# Construct oneshot informaion to reshape
	if len(oneShotAxisInd) !=0:
		centerString = analysisIndex["oneShot_Info"]["centers"].replace("\n","").replace(" ","")
		print(centerString)
		oneShotCenters = [complex(k) for k in centerString.split(",")]
		print(oneShotCenters)
	aveInfo = {
		"axisIndex": aveAxisInd,
		"aveRange": aveRange,
		"oneShotAxisIndex": oneShotAxisInd,
		"oneShotCenters": oneShotCenters,
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
	# aveAxisInd = analysisIndex["aveInfo"]["axisIndex"]
	# aveRange = 0


	# Construct accumulate informaion to reshape
	# oneShotAxisInd = analysisIndex["oneShot_Info"]["axisIndex"]
	# if len(oneShotAxisInd) ==0:
	# 	print("AAAAAAAAAAAAAAAAAAAAAAAAAA")

	aveInfo = {
		"axisIndex": [],
		"oneShotAxisIndex": [],
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




@bp.route('/cavitySearch/getJson_plot',methods=['POST','GET'])
def cavitySearch_getJson_plot():

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
	print("yAxisKey: ",yAxisKey)

	plotData = {}
	myQuantification.do_analysis()
	#print(plotData)

	def plot_2D_amp () :
		plotData[yAxisKey]= myExtendMeasurement.independentVars[yAxisKey]
		plotData[xAxisKey]= myExtendMeasurement.rawData["x"]
		plotData["amplitude"]= abs(myExtendMeasurement.rawData["iqSignal"])
		return plotData
	def plot_1D_amp () :
		plotData["Data_point_frequency"]= myExtendMeasurement.rawData["x"]
		plotData["Data_point_amplitude"]= abs(myExtendMeasurement.rawData["iqSignal"][yAxisValInd])
		return plotData
	def plot_1D_IQ () :
		plotData["Data_point_I"]= myExtendMeasurement.rawData["iqSignal"][yAxisValInd].real
		plotData["Data_point_Q"]= myExtendMeasurement.rawData["iqSignal"][yAxisValInd].imag
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

		return plotData
	plotFunction = {
		'2D_amp': plot_2D_amp,
		'1D_amp': plot_1D_amp,
		'1D_IQ': plot_1D_IQ,
		'1D_all': plot_1D_all,
	}
	return json.dumps(plotFunction[plotType](), cls=NumpyEncoder)


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

@bp.route('/fidelity/autoscan1q',methods=['POST','GET'])
def Autoscan1Q_do_analysis():
	print("start gogogo\n")
	# search(self.quantificationObj)
	routine = AutoScan1Q(numCPW = "3",sparam="S21,",dcsweepch = "1")
	print("start step1\n")
	routine.cavitysearch()
	print(routine.cavity_list)
	print(routine.total_cavity_list)
	# for i in routine.total_cavity_list:
	for i in routine.total_cavity_list:
		print("start step2\n")
		routine.powerdepend(i)
		f_bare = float(i.split(" ")[0])
		print("start step3\n")
		routine.fluxdepend(i,f_bare)
		print("start step4\n")
		routine.qubitsearch(i)
		break #test once
	return routine.jobid_dict

# import sys
# sys.path.append('pyqum/directive/code')

from colorama import Fore, Back
from flask import session
from pyqum import get_db, close_db
from json import dumps
#---------------load package of load_data---------------
from pyqum.directive.code.LoadData_lab import jobid_search_pyqum, pyqum_load_data
#---------------load package of cavity search---------------
from pyqum.directive.code.CavitySearch import make_amp,make_pha,input_process,output_process,true_alt_info,find_best_ans,db_datamaker,Find_eps,dbscan,predict_dataset,compa_gru_db
from numpy import array,vstack, hstack
from pandas import Series, DataFrame, concat
from keras.models import load_model
from pyqum.directive.code.QubitFrequency import colect_cluster,cal_nopecenter,cal_distance,denoise,check_overpower,find_farest,cal_Ec_GHz,freq2idx
#---------------load package of power dependent---------------
from sklearn.cluster import KMeans
from numpy import median
from pyqum.directive.code.PowerDepend import loadmat_valid,outlier_detect, cloc
#---------------load package of flux dependent---------------
from pyqum.directive.code.FluxDepend import flux_load_data, fit_sin
#---------------save jobid list in pickle---------------
from pickle import dump,load
#---------------process---------------
from numpy import mean
from pyqum.directive.characterize import F_Response, CW_Sweep
from random import random
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class Load_From_pyqum:
    def __init__(self, jobid):
        self.jobid = jobid
        self.pyqum_path, self.task = jobid_search_pyqum(self.jobid)
        # self.pyqum_path = 'data/F_Response.pyqum(2)'
        
    def load(self):
        self.amp_data,self.jobid_check  = pyqum_load_data(self.pyqum_path)
        if self.jobid == self.jobid_check:
            print("JOBid ",self.jobid," checked")
        return self.amp_data
            
class CavitySearch:
    def __init__(self, dataframe):
        self.dataframe = dataframe

        # ans of prediction
        self.answer = {}
        self.amplitude, self.phase, self.freq = [], [], []
        self.fig = DataFrame()
        self.ans_array = {}

    def do_analysis(self,designed):
        I = self.dataframe['I']
        Q = self.dataframe['Q']
        self.freq = self.dataframe['Frequency']

        self.amplitude = make_amp(I,Q)
        self.phase = make_pha(I,Q)
        self.fig = DataFrame(concat([Series(self.freq),Series(self.amplitude),Series(self.phase)],axis=1))

        # GRU part
        AMP = load_model(r'C:\Users\ASQUM\Documents\GitHub\PYQUM\TEST\FACE\pyqum\directive\model\GRU_AMP_Accuracy.h5')
        PHA = load_model(r'C:\Users\ASQUM\Documents\GitHub\PYQUM\TEST\FACE\pyqum\directive\model\GRU_PHA_Accuracy.h5')

        amp, pha, comparison = input_process(self.fig)      # frequency,amplitude,phase; comparison[no.][0] for freq start, end for comparison[no.][1] 
        self.fig.columns = ['<b>frequency(GHz)</b>','Amplitude','UPhase']

        # prediction GRU
        amp_pred = AMP.predict(amp)
        pha_pred = PHA.predict(pha)

        # result process
        true_out ,alt = output_process(amp_pred,pha_pred,comparison)  
        zone, voted_amp, voted_pha = true_alt_info(true_out,alt,self.fig)

        gru_ans_amp, status_amp = find_best_ans(zone,voted_amp,self.fig,designed)  # status is the origin predict result with the default peak_limit = 8
        gru_ans_pha, status_pha = find_best_ans(zone,voted_pha,self.fig,designed)
        
        # DBSCAN part
        # dbscan for phase
        inp_db = db_datamaker(self.phase,self.freq)
        eps,mini = Find_eps(inp_db) 
        l_d_pha = dbscan(inp_db,eps,mini)
        ture_out_db_pha = predict_dataset(l_d_pha,self.freq)

        # dbscan for amplitude
        inp_db = db_datamaker(self.amplitude,self.freq)
        eps,mini = Find_eps(inp_db) 
        l_d_amp = dbscan(inp_db,eps,mini)
        ture_out_db_amp = predict_dataset(l_d_amp,self.freq)

        true_out_db = vstack((ture_out_db_amp,ture_out_db_pha))

        zone, voted_amp, voted_pha = true_alt_info(true_out_db,alt,self.fig)
        db_ans_amp, status_amp = find_best_ans(zone, voted_amp, self.fig, designed)
        db_ans_pha, status_pha = find_best_ans(zone, voted_pha, self.fig, designed)

        amp_ans = [gru_ans_amp,db_ans_amp]
        pha_ans = [gru_ans_pha,db_ans_pha]

        self.answer = compa_gru_db(amp_ans,pha_ans)   # answer looks: {'0':[start,end],'1':[...],...}
        return self.answer

    def give_answer_array(self,no):
        self.ans_array = {
        'Frequency':self.fig[self.fig["<b>frequency(GHz)</b>"].between(self.answer[str(no)][0],self.answer[str(no)][1])]['<b>frequency(GHz)</b>'],
        'Amplitude':self.fig[self.fig["<b>frequency(GHz)</b>"].between(self.answer[str(no)][0],self.answer[str(no)][1])]['Amplitude'],
        'UPhase':self.fig[self.fig["<b>frequency(GHz)</b>"].between(self.answer[str(no)][0],self.answer[str(no)][1])]['UPhase']
        }

class PowerDepend:
    def __init__(self, dataframe):
        self.data = loadmat_valid(dataframe)
    def do_analysis(self):
        model = KMeans(n_clusters=2, n_init=1, random_state=0)
        label = model.fit_predict(self.data)
        label_new = outlier_detect(self.data,label)
        power_0,power_1 = cloc(label_new)
        print("power : "+"{:.2f}".format(self.data[:, 0][power_0])+"{:<7}".format(' dBm ; ')+
            "fr : "+"{:.2f}".format(self.data[:, 1][power_0])+"{:<7}".format(' MHz ; \n')+
            "power : "+"{:.2f}".format(self.data[:, 0][power_1])+"{:<7}".format(' dBm ; ')+
            "fr : "+"{:.2f}".format(self.data[:, 1][power_1])+"{:<7}".format(' MHz ; '))
        self.low_power = min(self.data[:, 0][power_0],self.data[:, 0][power_1])
        self.high_power = max(self.data[:, 0][power_0],self.data[:, 0][power_1])
        return self.low_power, self.high_power
        
class FluxDepend:
    def __init__(self, dataframe):
        self.dataframe = dataframe
    def do_analysis(self,f_bare):
        tol = 0.1
        self.valid = flux_load_data(self.dataframe)
        self.valid = self.valid.drop(self.valid[(self.valid['fr']<f_bare+tol) & (self.valid['fr']>f_bare-tol)].index)
        ki = self.valid['fr']-f_bare
        f_qubit = f_bare-1/ki
        offset = self.valid['flux'][f_qubit ==f_qubit.max()]
        f_dress = self.valid['fr'][offset.index]
        res = fit_sin(self.valid['flux'],f_qubit)
        period = float(res['period'])
        print("{:<36}".format("Final_dressed cavity frquency"), " : " , "{:>8.2f}".format(float(f_dress)) ,"MHz")
        print("{:<36}".format("Final_bare cavity frquency"), " : " , "{:>8.2f}".format(float(f_bare)) ,"MHz")
        print("{:<36}".format("Final_dressed cavity frquency diff."), " : " , "{:>8.2f}".format(float(f_dress-f_bare)) ,"MHz")
        print("{:<36}".format("Final_offset")," : ","{:>8.2f}".format(float(offset)),"uA")
        print("{:<36}".format("Final_period")," : ","{:>8.2f}".format(float(period)),"uA")
    #     if plot:
    #         import matplotlib.pyplot as plt
    #         from numpy import linspace
    #         plt.rcParams["figure.figsize"] = [20,10]
    #         plt.subplot(211)
    #         plt.scatter(self.valid['flux'],self.valid['fr'],color='black', marker='o',label='real data')
    #         plt.subplot(212)
    #         plt.scatter(self.valid['flux'],f_qubit,color='r', marker='*',label='f_qubit')
    #         x = linspace(self.valid['flux'].min(),self.valid['flux'].max(),200)
    #         plt.plot(x, res["fitfunc"](x), "r-", label="fit curve", linewidth=2)
    #         plt.xlabel("Flux : uA")
    #         plt.ylabel("Freq : MHz")
    #         # plt.ylim(self.valid['fr'].min()-.20,self.valid['fr'].max()+.20)
    #         plt.legend()
    #         plt.show()
        return {"f_dress":float(f_dress/1000),"f_bare":float(f_bare/1000),"f_diff":float((f_dress-f_bare)/1000),"offset":float(offset),"period":float(period)}
    
class QubitFreq_Scan:
    def __init__(self,dataframe):#,Ec,status,area_Maxratio,density
        self.dataframe = dataframe

        self.fq = 0.0
        self.Ec = 0.0
        self.freq = 0.0
        self.status = 0
        self.target_freq = []
        self.sub = []
        self.title = ''
        self.answer = {} # <- 0630 update
        self.plot_items = {}



    def do_analysis(self):
        self.freq = self.dataframe['Frequency'].to_numpy()  #for qubit  <b>XY-Frequency(GHz)</b>
        I = self.dataframe['I'].to_numpy()
        Q = self.dataframe['Q'].to_numpy()

        inp_db = []
        for i in range(I.shape[0]):
            inp_db.append(list(hstack(([I[i]],[Q[i]]))))

        # start DBSCAN
        eps,min_samples = Find_eps(inp_db)
        labels_db = dbscan(array(inp_db),eps,min_samples)

        # output process
        peak_susp_idx, nope_idx = colect_cluster(labels_db,mode='db')
        nope_center = cal_nopecenter(nope_idx,I,Q)

        # redefine the background
        redef_sub = []
        for i in range(self.freq.shape[0]):
            redef_sub.append(cal_distance([I[i],Q[i]],nope_center))

        self.sub = array(redef_sub)
        self.title = 'Amplitude_Redefined'


        if len(peak_susp_idx) != 0:

            tip = denoise(peak_susp_idx,self.freq,self.sub)
            #filter out the overpower case within +-0.5 std
            overpower,_,_ = check_overpower(tip,self.sub,0.5)

            if overpower == 'safe':
                #farest 3 point in IQ
                denoised_freq = find_farest(tip,nope_center,self.sub,I,Q,self.freq)

                #calculate Ec based on farest
                self.fq, self.Ec, self.status, self.target_freq = cal_Ec_GHz(denoised_freq,self.sub,self.freq)
            else:
                self.fq, self.Ec, self.status, self.target_freq = 0, 0, 0, []
        else:
            self.fq, self.Ec, self.status, self.target_freq = 0, 0, 0, []

        self.answer = {'Fq':self.fq,'Ec':self.Ec,'Status':self.status,'Freqs':self.target_freq} 
        '''status = 0 for 0 peak detected -> overpower with high probability
           status = 1 for 1 peak detected -> so far, a stronger xy-power again
           status = 2 for 2 peak detected'''
        return self.answer
                                                                                         
    def give_result(self):
        farest = freq2idx(self.target_freq,self.freq)[:3]
        self.plot_items = {
            'Targets':self.sub[farest],
            'Targets_Freq':self.freq[farest],
            'Sub_Frequency':self.freq,
            'Substrate':self.sub
        }
      
def char_fresp_new(sparam,freq,powa,flux,dcsweepch = "1",comment = "By bot"):
    # Check user's current queue status:
    if session['run_clearance']:
        print(comment)
        wday = int(-1)
        sparam = sparam   #S-Parameter
        ifb = "100"     #IF-Bandwidth (Hz)
        freq = freq #Frequency (GHz)
        powa = powa    #Power (dBm)
        fluxbias = flux   #Flux-Bias (V/A)
        PERIMETER = {"dcsweepch":dcsweepch, "z-idle":'{}', "sweep-config":'{"sweeprate":0.0001,"pulsewidth":1001e-3,"current":1}'} # DC=YOKO
        CORDER = {'Flux-Bias':fluxbias, 'S-Parameter':sparam, 'IF-Bandwidth':ifb, 'Power':powa, 'Frequency':freq}
        comment = comment.replace("\"","")+str(CORDER) #comment
        print(CORDER)
        # Start Running:
        workspace = F_Response(session['people'], corder=CORDER, comment=comment, tag='', dayindex=wday, perimeter=PERIMETER)
        return workspace.jobid_analysis
    else: return show()
def char_cwsweep_new(sparam,freq,powa,flux,f_bare,f_dress,dcsweepch = "1",comment = "By bot"):
    # Check user's current queue status:
    ki = f_dress-f_bare
    f_qubit = f_bare-40**2/ki
    if session['run_clearance']:
        print(comment)
        wday = int(-1)
        sparam = sparam   #S-Parameter
        ifb = "100"     #IF-Bandwidth (Hz)
        freq = freq  #Frequency (GHz)
        powa = powa    #Power (dBm)
        fluxbias = flux   #Flux-Bias (V/A)
        xyfreq = "{} to {} * 400".format(f_qubit-1,f_qubit+1)#"OPT,"
        xypowa = "-10 -30 r 10"#"OPT,"
        PERIMETER = {"dcsweepch":dcsweepch, "z-idle":'{}', 'sg-locked': '{}', "sweep-config":'{"sweeprate":0.0001,"pulsewidth":1001e-3,"current":0}'} # DC=YOKO
        CORDER = {'Flux-Bias':fluxbias, 'XY-Frequency':xyfreq, 'XY-Power':xypowa, 'S-Parameter':sparam, 'IF-Bandwidth':ifb, 'Frequency':freq, 'Power':powa}
        comment = comment.replace("\"","")+str(CORDER) #comment
        print(CORDER)
        # Start Running:
        workspace = CW_Sweep(session['people'], corder=CORDER, comment=comment, tag='', dayindex=wday, perimeter=PERIMETER)
        return workspace.jobid_analysis
    else: return show()

class Quest_command:
    def __init__(self,sparam="S21,"):
        self.sparam = sparam

    def jobnote(JOBID, note):
        '''Add NOTE to a JOB after analyzing the data'''
        if g.user['measurement']:
            try:
                db = get_db()
                db.execute('UPDATE job SET note = ? WHERE id = ?', (note,JOBID))
                db.commit()
                close_db()
                print(Fore.GREEN + "User %s has successfully updated JOB#%s with NOTE: %s" %(g.user['username'],JOBID,note))
            except:
                print(Fore.RED + Back.WHITE + "INVALID JOBID")
                raise
        else: pass
    
    def cavitysearch(self,dcsweepch,add_comment=""):
        jobid = char_fresp_new(sparam=self.sparam,freq = "3 to 9 *3000",powa = "0",flux = "OPT,",dcsweepch = "1",comment = "By bot - step1 cavitysearch "+add_comment)
        return jobid
    def powerdepend(self,select_freq,add_comment=""):
        freq_command = "{} to {} *200".format(select_freq[0],select_freq[1])
        if select_freq[0]>12 | select_freq[1]>12 | select_freq[0]<2 | select_freq[1]<2:
            raise ValueError("Frequency is out of range with "+freq_command)
        jobid = char_fresp_new(sparam=self.sparam,freq=freq_command,powa = "-50 to 10 * 13",flux = "OPT,",dcsweepch = "1",comment = "By bot - step2 power dependent"+add_comment)
        return jobid
    def fluxdepend(self,select_freq,select_powa,add_comment=""):
        freq_command = "{} to {} *200".format(select_freq[0],select_freq[1])
        if select_freq[0]>12 | select_freq[1]>12 | select_freq[0]<2 | select_freq[1]<2:
            raise ValueError("Frequency is out of range with "+freq_command)
        if select_powa >20 | select_powa <-60:
            raise ValueError("Power is out of range with "+select_powa)
        jobid = char_fresp_new(sparam=self.sparam,freq=freq_command,powa = select_powa,flux = "-500e-6 to 500e-6 * 50",dcsweepch = "1",comment = "By bot - step3 flux dependent "+add_comment)
        return jobid
    def qubitsearch(self,select_freq,select_powa,select_flux,f_bare,f_dress,dcsweepch,add_comment=""):
        if select_freq>12 | select_freq<2:
            raise ValueError("frequency is out of range with "+ select_freq)
        if select_powa >20 | select_powa <-60:
            raise ValueError("Power is out of range with "+select_powa)
        if select_flux >500e-6 | select_flux <-500e-6:
            raise ValueError("Flux is out of range with "+select_flux)
        jobid = char_cwsweep_new(sparam=self.sparam,freq = select_freq, powa = select_powa, flux = select_flux, f_bare = f_bare,f_dress =f_dress,dcsweepch = dcsweepch,comment = "By bot - step4 qubit search "+add_comment)
        return jobid

class AutoScan1Q:
    def __init__(self,numCPW="3",sparam="S21,",dcsweepch = "1"):
        self.jobid_dict = {"CavitySearch":0,"PowerDepend":0,"FluxDepend":0,"QubitSearch":0}
        self.readout_para = {}
        self.sparam = sparam
        self.dcsweepch = dcsweepch
        try:
            self.numCPW = int(numCPW)
        except:
            pass
        
    def cavitysearch(self):
        # jobid = Quest_command(self.sparam).cavitysearch(self.dcsweepch)
        jobid = 5094
        print("do measurement\n")
        self.jobid_dict["CavitySearch"] = jobid
        dataframe = Load_From_pyqum(jobid).load()
        # self.cavity_list = CavitySearch(dataframe).do_analysis(self.numCPW) #model h5 cannot import
        self.cavity_list = {'7116.0 MHz': [7.102, 7.128], '6334.0 MHz': [6.32, 6.346]}
        self.total_cavity_list = list(self.cavity_list.keys())
        self.readout_para = {i: {} for i in self.total_cavity_list}
        self.readout_para["cavity_list"] = self.cavity_list
    
    def powerdepend(self,cavity_num):
        # jobid = Quest_command(self.sparam).powerdepend(select_freq=self.cavity_list[cavity_num],add_comment="with Cavity "+str(cavity_num))
        jobid = 5097
        self.jobid_dict["PowerDepend"] = jobid
        dataframe = Load_From_pyqum(jobid).load()
        self.low_power, self.high_power = PowerDepend(dataframe).do_analysis() #pass
        print("Select Power : %f"%self.low_power)
        self.readout_para[cavity_num]["low_power"] = self.low_power
        self.readout_para[cavity_num]["high_power"] = self.high_power
      
    def fluxdepend(self,cavity_num, f_bare):
        # jobid = Quest_command(self.sparam).fluxdepend(select_freq=self.cavity_list[cavity_num],select_powa=self.low_power,add_comment="with Cavity "+str(cavity_num))
        jobid = 5105
        self.jobid_dict["FluxDepend"] = jobid
        dataframe = Load_From_pyqum(jobid).load()
        self.wave = FluxDepend(dataframe).do_analysis(f_bare) #pass
        print(self.wave)#{"f_dress":float(f_dress/1000),"f_bare":float(f_bare/1000),"f_diff":float((f_dress-f_bare)/1000),"offset":float(offset),"period":float(period)}
        self.readout_para[cavity_num]["f_bare"] = self.wave["f_bare"]
        self.readout_para[cavity_num]["f_dress"] = self.wave["f_dress"]
    
    def qubitsearch(self,cavity_num):
        jobid = Quest_command(self.sparam).qubitsearch(select_freq=self.wave["f_dress"],select_powa=self.low_power,select_flux=str(self.wave["offset"])+'e-6',f_bare = self.wave["f_bare"],f_dress = self.wave["f_dress"],dcsweepch = self.dcsweepch,add_comment="with Cavity "+str(cavity_num))
        # jobid = 5106
        self.jobid_dict["QubitSearch"] = jobid
        dataframe = Load_From_pyqum(jobid).load()
        self.qubit = QubitFreq_Scan(dataframe).do_analysis() #examine the input data form is dataframe because Series cannot reshape 
        print(self.qubit)
        self.readout_para[cavity_num]["qubit"] = self.qubit


def save_class(item,path = "save.pickle"):
    with open(path, 'wb') as f:
        dump(item, f)
def load_class(path = "save.pickle"):
    with open(path, 'rb') as f:
        item = load(f)
    return item


# if __name__ == "__main__":
#     routine = AutoScan1Q(numCPW = "3",sparam="S21,",dcsweepch = "1")
#     routine.cavitysearch()
#     print(routine.cavity_list)
#     print(routine.total_cavity_len)
#     for i in range(routine.total_cavity_len):
#         routine.powerdepend(i)
#         f_bare = mean(routine.cavity_list[str(i)])
#         routine.fluxdepend(i,f_bare)
#         routine.qubitsearch(i)
    # id = int(input("id? : "))
    # pyqum_path,task = jobid_search_pyqum(id)
    # amp_data,jobid  = pyqum_load_data(pyqum_path)
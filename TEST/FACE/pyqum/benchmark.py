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
from pyqum.directive.code.CavitySearch import normalize_1d, peak_info, corr_peak_loc, compu_peak_center_dist, poopoo_filter, rm_empty, gaus, gaussian_fitor, gaussian_filter, amp_pha_compa, ena_clutch_filter, pred_filter, find_best_ans 
from scipy.optimize import curve_fit
import numpy as np
from numpy import array, log10, diff, unwrap, arctan2, vstack, hstack, average, std
from scipy.signal import savgol_filter as SGF
from pandas import Series, DataFrame, concat
#-----------------load package of qubit frequency search-------------------
from pyqum.directive.code.QubitFrequency import Find_eps,dbscan,colect_cluster,cal_nopecenter,cal_distance,denoise,check_overpower,find_farest,cal_Ec_GHz,freq2idx,freq_sorter,check_acStark_power,freq_clustering
from colorama import init, Fore, Back, Style
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
    def __init__(self,dataframe):
        self.df = dataframe
        self.overview = {}
        self.info = {}
        self.region = {}
        self.peak_amp, self.peak_pha = [], []
        self.sliced_freq = []
        self.final_answer = {}
        self.progress = 0.0
        # data pre-smooth : Savitzky-Golay filter
        self.SGF_width = 11
        self.polyorder = 1
        
    
    def make_amp_uph_from_IQ(self):
        UPhase = diff(unwrap(arctan2(array(self.df['Q']),array(self.df['I']))))
        self.overview = {'Frequency':array(self.df['Frequency']),'Amplitude':array(self.df['Amp']),'UPhase':array(UPhase)}
        df = self.df[self.df['Frequency'].between(4,8)]
        freq = array(df['Frequency'])
        I = array(df['I'])
        Q = array(df['Q'])
        amplitude = normalize_1d(20*log10((I**2+Q**2)**(1/2)))
        phase = diff(unwrap(arctan2(Q,I)))
        uphase = normalize_1d(hstack((phase,average(phase))))
        
        amplitude -= SGF(amplitude,self.SGF_width,self.polyorder)
        uphase -= SGF(uphase,self.SGF_width,self.polyorder)
        
        p2p = (freq[-1]-freq[0])/freq.shape[0]

        compa_fig = concat([Series(freq),Series(amplitude),Series(uphase)],axis=1) 
        compa_fig.columns = ['Frequency','Amplitude','UPhase']

        self.info = {"Frequency":freq,"Amplitude":amplitude,"UPhase":uphase,"p2p_freq":p2p,"Comparison_fig":compa_fig}
        
    def strong_slice(self):
        freq_shifted = [] 
        freq_sliced = []    #[[freq_st,freq_ed],[...],...]
        range_point = int(0.03/self.info['p2p_freq'])
        for i in range(0,self.info['Frequency'].shape[0]-range_point,range_point):
            freq_sliced.append([array(self.info['Frequency'][i:i+range_point])[0],array(self.info['Frequency'][i:i+range_point])[-1]])

            sliced_amp = array(self.info['Amplitude'][i:i+range_point])
            sliced_pha = array(self.info['UPhase'][i:i+range_point])
            min_max_mid_amp = 0.5*(np.max(sliced_amp)+np.min(sliced_amp))
            median_amp = median(sliced_amp)
            sd_amp = std(sliced_amp)
            min_max_mid_pha = 0.5*(np.max(sliced_pha)+np.min(sliced_pha))
            median_pha = median(sliced_pha)
            sd_pha = std(sliced_pha)
            condi_amp = (median_amp-sd_amp > min_max_mid_amp or min_max_mid_amp > median_amp+sd_amp)
            condi_pha = (median_pha-sd_pha > min_max_mid_pha or min_max_mid_pha > median_pha+sd_pha)

            if  condi_amp or condi_pha :
                if i != 0 or i != (self.info['Frequency'].shape[0]-range_point):
                    if abs(sliced_amp[0]-median_amp) > abs(0.34*(np.max(sliced_amp)-np.min(sliced_amp))) or  abs(sliced_pha[0]-median_pha) > abs(0.34*(np.max(sliced_pha)+np.min(sliced_pha))):
                        freq_shifted.append([array(self.info['Frequency'][i-int(range_point/2):i-int(range_point/2)+range_point])[0],array(self.info['Frequency'][i-int(range_point/2):i-int(range_point/2)+range_point])[-1]])

                    if abs(sliced_amp[-1]-median_amp) > abs(0.34*(np.max(sliced_amp)-np.min(sliced_amp))) or  abs(sliced_pha[-1]-median_pha) > abs(0.34*(np.max(sliced_pha)+np.min(sliced_pha))):
                        freq_shifted.append([array(self.info['Frequency'][i+int(range_point/2):i+int(range_point/2)+range_point])[0],array(self.info['Frequency'][i+int(range_point/2):i+int(range_point/2)+range_point])[-1]])
        
        freq_sliced.extend(freq_shifted)
        self.sliced_freq = array(freq_sliced) 

    def zscore_filter(self,region,designed_CPW_num):
        amp_voted, pha_voted = pred_filter(region,self.info['Comparison_fig'])

        true, _ =  find_best_ans(region, pha_voted,self.info['Comparison_fig'],designed_CPW_num)
        for i in region.keys():
            for j in true:
                if region[i][0] == j[0] and region[i][1] == j[1] :
                    self.final_answer[i] = region[i]
        
    def give_region(self,peak_list):
        for tip_freq in peak_list: 
            freq = self.info['Comparison_fig'][self.info['Comparison_fig']['Frequency'].between(tip_freq-0.015,tip_freq+0.015)]['Frequency']
            amp = self.info['Comparison_fig'][self.info['Comparison_fig']['Frequency'].between(tip_freq-0.015,tip_freq+0.015)]['Amplitude']
            pha = self.info['Comparison_fig'][self.info['Comparison_fig']['Frequency'].between(tip_freq-0.015,tip_freq+0.015)]['UPhase']
            
            amp_tip_idx,FWHM_amp = peak_info(amp,self.info['p2p_freq'])  # unit: GHz
            pha_tip_idx,FWHM_pha = peak_info(pha,self.info['p2p_freq'])
            avg_tip_idx = 0.5*(array(freq)[amp_tip_idx]+array(freq)[pha_tip_idx])
            avg_FWHM = 0.5*(FWHM_amp*self.info['p2p_freq']+FWHM_pha*self.info['p2p_freq'])
            self.region['%d MHz'%(avg_tip_idx*1000)] = [tip_freq-5*avg_FWHM,tip_freq+5*avg_FWHM]
        self.final_answer = self.region
        
    def amp_pha_compa(self,designed_CPW_num):
        amp_loc_array = list(self.peak_amp)
        pha_loc_array = list(self.peak_pha)
        nearest = []
        for amp_peak in amp_loc_array:
            for pha_peak in pha_loc_array: 
                if abs(amp_peak - pha_peak)<0.01:
                    near_center_freq = compu_peak_center_dist(amp_peak,pha_peak,self.info['Comparison_fig'],self.info['p2p_freq'])
                    nearest.append(near_center_freq)
                
        x = ena_clutch_filter(list(set(poopoo_filter(array(nearest),self.info['Comparison_fig']))))    # 1D array contain tip freq [freq1,freq2,...]
        self.give_region(x,designed_CPW_num)

    # to call below do analysis  
    '''                   
    def do_analysis(self,designed_CPW_num): 
        self.make_amp_uph_from_IQ()
        self.strong_slice()
        gaussian_exist = {"peak_freq_amp":[],"peak_freq_pha":[]}
        step = 0
        for i in range(self.sliced_freq.shape[0]):
            peak_amp, peak_pha =  gaussian_filter(self.sliced_freq[i],self.info['Comparison_fig'],self.info['p2p_freq'])

            gaussian_exist['peak_freq_amp'].append(peak_amp)
            gaussian_exist['peak_freq_pha'].append(peak_pha)
            step += 1
            self.progress = step*100/self.sliced_freq.shape[0]

        self.peak_amp = rm_empty(gaussian_exist["peak_freq_amp"])
        self.peak_pha = rm_empty(gaussian_exist["peak_freq_pha"])
        self.amp_pha_compa(designed_CPW_num)

        return self.final_answer  # return out {'5487 MHz':[freq_start,freq_end],'... MHz':[...],....}
    '''
    def do_analysis(self,designed):   
        self.make_amp_uph_from_IQ()
        peak = []
        fig_copy = self.info['Comparison_fig']
        up_lim = abs(np.average(fig_copy["UPhase"])+2*np.std(fig_copy["UPhase"]))
        bt_lim = abs(np.average(fig_copy["UPhase"])-2*np.std(fig_copy["UPhase"]))
        avg = np.average(fig_copy["UPhase"])
        while designed > 0 :
            
            target = fig_copy["UPhase"].tolist()
            
            if abs(max(target)) < up_lim:
                if designed >0 and abs(min(target)) > bt_lim:
                    min_idx = target.index(min(target))
                    for i in peak:
                        if abs(fig_copy['Frequency'][min_idx] - i ) > 0.05:   # 超過 50MHz 視為不同peak
                            peak.append(fig_copy['Frequency'][min_idx])
                            idx_within_60MHz = int(0.06/self.info["p2p_freq"])
                            for i in range(min_idx-int(idx_within_60MHz/2),min_idx+int(idx_within_60MHz/2),1):
                                target[i] = avg

                            revised = fig_copy.drop(columns=["UPhase"])
                            uphase = Series(target)
                            fig_copy = concat([revised,uphase],axis=1) 
                            fig_copy.columns = ['Frequency','Amplitude','UPhase']
                            designed -= 1
                        
            else:
                max_idx = target.index(max(target))
                peak.append(fig_copy['Frequency'][max_idx])
                idx_within_60MHz = int(0.06/self.info["p2p_freq"])
                for i in range(max_idx-int(idx_within_60MHz/2),max_idx+int(idx_within_60MHz/2),1):
                    target[i] = avg

                revised = fig_copy.drop(columns=["UPhase"])
                uphase = Series(target)
                fig_copy = concat([revised,uphase],axis=1) 
                fig_copy.columns = ['Frequency','Amplitude','UPhase']
                designed -= 1
        peak.sort()
        self.give_region(peak)
        return self.final_answer
        
    #to call below send arrays to js plotly            
    def give_plot_info(self):
        plot_items = {}
        for cavity in self.final_answer.keys():
            plot_items[cavity] = {
				'Frequency':array(self.info['Comparison_fig'][self.info['Comparison_fig']['Frequency'].between(self.final_answer[cavity][0],self.final_answer[cavity][1])]['Frequency']),
				'Amplitude':array(self.info['Comparison_fig'][self.info['Comparison_fig']['Frequency'].between(self.final_answer[cavity][0],self.final_answer[cavity][1])]['Amplitude']),
				'UPhase':array(self.info['Comparison_fig'][self.info['Comparison_fig']['Frequency'].between(self.final_answer[cavity][0],self.final_answer[cavity][1])]['UPhase'])
            }
        return plot_items
        

class PowerDepend:
    def __init__(self, dataframe):
        self.dataframe = dataframe
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
    def give_plot_info(self):
        plot_items  = {
			'Frequency':array(self.dataframe['Frequency']),
			'Power':array(self.dataframe['Power']),
			'Amplitude':array(self.dataframe['Amp'])
		}
        plot_scatter = {
			'Power':array(self.data[:, 0]),
			'Fr':array(self.data[:, 1])/1000
		}
        return {'heatmap':plot_items,'scatter':plot_scatter}

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
    def give_plot_info(self):
        plot_items = {
			'Frequency':array(self.dataframe['Frequency']),
			'Flux':array(self.dataframe['Flux-Bias'])*1e6,
			'Amplitude':array(self.dataframe['Amp'])
		}
        plot_scatter = {
			'Flux':array(self.valid['flux']),
			'Fr':array(self.valid['fr'])/1000
		}
        return {'heatmap':plot_items,'scatter':plot_scatter}

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
        
        self.freq = self.dataframe['XY-Frequency'].to_numpy()  #for qubit  <b>XY-Frequency(GHz)</b>
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
            'Targets_value':array(self.sub[farest]),
            'Targets_Freq':array(self.freq[farest]),
            'Sub_Frequency':self.freq,
            'Substrate_value':self.sub
        }
        

# 0820 add compare different xy-power
class QubitFreq_Compa:
    def __init__(self,dataframe):
        self.lab_df = dataframe
        self.sep_dfS = []
        self.fqS = {}
        self.ecS = {}
        self.stS = {}
        self.plot_items = {}
        self.sorted = {}
    # make different xy-power dataframes    
    def seperate_lab_df(self):
        xy_powa = self.lab_df['XY-Power'].unique()    #[xy-power_1,xy_power_2,....]
        for powa in xy_powa:
            self.sep_dfS.append(self.lab_df[(self.lab_df['XY-Power']==powa)])
    
    def calcu(self):
        self.seperate_lab_df()
        for powa_df in self.sep_dfS :
            FQ_db = QubitFreq_Scan(powa_df)
            FQ_db.do_analysis()
            FQ_db.give_result()
            self.fqS[str(powa_df['XY-Power'].unique()[0])] = FQ_db.target_freq
            self.ecS[str(powa_df['XY-Power'].unique()[0])] = FQ_db.Ec
            self.stS[str(powa_df['XY-Power'].unique()[0])] = FQ_db.status
            self.plot_items[str(powa_df['XY-Power'].unique()[0])]= FQ_db.plot_items
    
    def compa(self):
        y = []    # frequency set
        for powa in self.fqS.keys():
            for j in self.fqS[powa]:
                y.append(j)
        y = array(y)        
        x = arange(0,y.shape[0])
        if y.shape[0] >= 2:
            group = freq_clustering(x,y)
            self.sorted = freq_sorter(y,group)  #{'low':[...],'mid':[...],'high':[...]}
        else:
            init()
            print(Style.BRIGHT+Fore.RED+'Warning! DB-scan somewhere maybe goes wrong check it plz!'+Style.RESET_ALL)
            self.sorted =  {'high':y,'mid':array([]),'low':array([])}
        
    def do_analysis(self):
        self.calcu()
        self.compa()
        high_freq_group = self.sorted['high']
        mid_freq_group = self.sorted['mid']
        if mid_freq_group.shape[0] != 0:
            power_with_Ec = []
            for powa in self.fqS.keys():
                for high_freq in high_freq_group:
                    for mid_freq in mid_freq_group:
                        if high_freq in self.fqS[powa] and mid_freq in self.fqS[powa]:
                            power_with_Ec.append(powa)
                        else:
                            power_with_Ec.append([])
            with_Ec = rm_empty(power_with_Ec)
            Ec_collector = []
            fq_collector = []
            if len(with_Ec) != 0:
                for powa in with_Ec:
                    Ec_collector.append(self.fqS[powa][0]-self.fqS[powa][1])
                    fq_collector.append(self.fqS[powa][0])
                init()    
                print(Style.BRIGHT+Fore.YELLOW+'After compare different power, there is a ordinary Ec & Fq with average!\n'+Style.RESET_ALL)
                compa_ans = {'Ec_avg':mean(Ec_collector)*2,'Fq_avg':mean(fq_collector)}  
            else:
                print(Style.BRIGHT+Fore.YELLOW+'After compare different power, there "only exist Fq" with average!\n'+Style.RESET_ALL)
                compa_ans = {'Ec_avg':array([]),'Fq_avg':mean(high_freq_group)}
        else:
            print(Style.BRIGHT+Fore.YELLOW+'After compare different power, there "only exist Fq" with average!\n'+Style.RESET_ALL)
            compa_ans = {'Ec_avg':array([]),'Fq_avg':mean(high_freq_group)}
        
        compa_ans['acStark_power'] = check_acStark_power(self.stS,self.fqS,high_freq_group)
        
        return compa_ans
        

      
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
    if (f_qubit>12) | (f_qubit<2):
            raise ValueError("frequency is out of range with "+ f_qubit)
    if session['run_clearance']:
        print(comment)
        wday = int(-1)
        sparam = sparam   #S-Parameter
        ifb = "100"     #IF-Bandwidth (Hz)
        freq = freq  #Frequency (GHz)
        powa = powa    #Power (dBm)
        fluxbias = flux   #Flux-Bias (V/A)
        xyfreq = "{} to {} * 400".format(f_qubit-1,f_qubit+1)#"OPT,"
        xypowa = "0 -10 -20 -30 r 10"#"OPT,"
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
    
    def cavitysearch(self,add_comment=""):
        jobid = char_fresp_new(sparam=self.sparam,freq = "3 to 9 *10000",powa = "0",flux = "OPT,",dcsweepch = "1",comment = "By bot - step1 cavitysearch "+add_comment)
        print('JOBID: ',jobid)
        return jobid
    def powerdepend(self,select_freq,add_comment=""):
        freq_command = "{} to {} *200".format(select_freq[0],select_freq[1])
        print('check PD freq_range: ',freq_command)
        if (select_freq[0]>12) | (select_freq[1]>12) | (select_freq[0]<2) | (select_freq[1]<2):
            raise ValueError("Frequency is out of range with "+freq_command)
        jobid = char_fresp_new(sparam=self.sparam,freq=freq_command,powa = "-50 to 0 * 11",flux = "OPT,",dcsweepch = "1",comment = "By bot - step2 power dependent"+add_comment)
        return jobid
    def fluxdepend(self,select_freq,select_powa,dc_ch,add_comment=""):
        freq_command = "{} to {} *200".format(select_freq[0],select_freq[1])
        print('check FD freq_range: ',freq_command)
        if (select_freq[0]>12) | (select_freq[1]>12) | (select_freq[0]<2) | (select_freq[1]<2):
            raise ValueError("Frequency is out of range with "+freq_command)
        if (select_powa >20) | (select_powa <-60):
            raise ValueError("Power is out of range with "+select_powa)
        jobid = char_fresp_new(sparam=self.sparam,freq=freq_command,powa = select_powa,flux = "-0.2 to 0.2 * 50",dcsweepch=dc_ch,comment = "By bot - step3 flux dependent "+add_comment)
        return jobid
    def qubitsearch(self,select_freq,select_powa,select_flux,f_bare,f_dress,dcsweepch,add_comment):
        if (select_freq>12) | (select_freq<2):
            raise ValueError("frequency is out of range with "+ select_freq)
        if (select_powa >20) | (select_powa <-60):
            raise ValueError("Power is out of range with "+select_powa)
        if (float(select_flux) >0.2) | (float(select_flux) <-0.2):  # 0915 TypeError: '>' not supported between instances of 'str' and 'float'  
            raise ValueError("Flux is out of range with "+select_flux)
        jobid = char_cwsweep_new(sparam=self.sparam,freq = select_freq, powa = select_powa, flux = select_flux, f_bare = f_bare,f_dress =f_dress,dcsweepch = dcsweepch,comment = "By bot - step4 qubit search "+add_comment)
        return jobid
# first version
'''
class AutoScan1Q:
    def __init__(self,sparam="S21,",dcsweepch = "1",designed=""):
        self.jobid_dict = {"PowerDepend":0,"FluxDepend":0,"QubitSearch":0}
        self.CS_jobid = 0
        self.readout_para = {}
        self.sparam = sparam
        self.dcsweepch = dcsweepch
        if designed != "":
            self.designed = int(designed)
        else:
            self.designed = 0
        self.CS_progress = 0
        self.id = id(self.CS_progress)

        
    def cavitysearch(self,jobid_check):
        if jobid_check == "":
            jobid = Quest_command(self.sparam).cavitysearch(self.dcsweepch)
            plot_ornot = 0
            self.CS_jobid = jobid
        else:
            jobid = jobid_check
            plot_ornot = 1
        print("do measurement\n")
        dataframe = Load_From_pyqum(jobid).load()
        CS = CavitySearch(dataframe)
        self.CS_progress = CS.progress
        self.cavity_list = CS.do_analysis(self.designed) #model h5 cannot import <- 0818 update, no need it anymore
        if plot_ornot:
            self.CS_plot_items = CS.give_plot_info()
            self.CS_overview = CS.overview    # ena scan results
        else:
            self.readout_para = {i: {} for i in self.cavity_list}
            self.readout_para["cavity_list"] = self.cavity_list
        self.total_cavity_list = list(self.cavity_list.keys())
    
    def powerdepend(self,cavity_freq,jobid_check):
        if jobid_check == "":
            jobid = Quest_command(self.sparam).powerdepend(select_freq=self.cavity_list[cavity_freq],add_comment="with Cavity "+str(cavity_freq))
            plot_ornot = 0
            self.jobid_dict["PowerDepend"] = jobid
        else:
            jobid = jobid_check
            plot_ornot = 1
        
        dataframe = Load_From_pyqum(jobid).load()
        PD = PowerDepend(dataframe)
        self.low_power, self.high_power = PD.do_analysis() #pass
        print("Select Power : %f"%self.low_power)
        if not plot_ornot:
            self.readout_para[cavity_freq]["low_power"] = self.low_power
            self.readout_para[cavity_freq]["high_power"] = self.high_power
        else:	
            self.PD_plot_items = PD.give_plot_info()    # assume the function named `get_plot_items()`


    def fluxdepend(self,cavity_freq, f_bare,jobid_check):
        if jobid_check == "":
            jobid = Quest_command(self.sparam).fluxdepend(select_freq=self.cavity_list[cavity_freq],select_powa=self.low_power,add_comment="with Cavity "+str(cavity_freq))
            plot_ornot = 0
            self.jobid_dict["FluxDepend"] = jobid
        else:
            jobid = jobid_check
            plot_ornot = 1
        
        dataframe = Load_From_pyqum(jobid).load()
        FD = FluxDepend(dataframe)
        self.wave = FD.do_analysis(f_bare) #pass
        print(self.wave)#{"f_dress":float(f_dress/1000),"f_bare":float(f_bare/1000),"f_diff":float((f_dress-f_bare)/1000),"offset":float(offset),"period":float(period)}
        if not plot_ornot:
            self.readout_para[cavity_freq]["f_bare"] = self.wave["f_bare"]
            self.readout_para[cavity_freq]["f_dress"] = self.wave["f_dress"]
            self.readout_para[cavity_freq]["offset"] = self.wave["offset"]
        else:
            self.FD_plot_items = FD.give_plot_info()  # assume the function named `get_plot_items()`
    
    def qubitsearch(self,cavity_freq,jobid_check):
        if jobid_check == "":
            jobid = Quest_command(self.sparam).qubitsearch(select_freq=self.wave["f_dress"],select_powa=self.low_power,select_flux=str(self.wave["offset"])+'e-6',f_bare = self.wave["f_bare"],f_dress = self.wave["f_dress"],dcsweepch = self.dcsweepch,add_comment="with Cavity "+str(cavity_freq))
            plot_ornot = 0
            self.jobid_dict["QubitSearch"] = jobid
        else:
            jobid = jobid_check
            plot_ornot = 1    
        
        dataframe = Load_From_pyqum(jobid).load()
        CW = QubitFreq_Compa(dataframe)
        self.qubit_info = CW.do_analysis() #examine the input data form is dataframe because Series cannot reshape 
        if not plot_ornot:
            self.readout_para[cavity_freq]["qubit"] = self.qubit_info['Fq_avg']
            self.readout_para[cavity_freq]["Ec"] = self.qubit_info['Ec_avg']
            self.readout_para[cavity_freq]["acStark"] = self.qubit_info['acStark_power']
        else:
            self.CW_plot_items = CW.plot_items
        print(self.qubit_info)                                     #0820update QubitFreq_Compa.do_analysis() return form: {'Ec_avg':Float_Number or array([]),'Fq_avg':Float_Number,'acStark_power':array([poerw_1,...]) or array([]) }
		# 0820 update
        # 
'''
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

# second version
from sqlite3 import connect
from pandas import read_sql_query
import ast
sql_path = r'C:\Users\ASQUM\HODOR\CONFIG\pyqum.sqlite'
class AutoScan1Q:
    def __init__(self,sparam="S21,",dcsweepch = "1",designed=""):
        self.jobid_dict = {"PowerDepend":0,"FluxDepend":0,"QubitSearch":0}
        self.CS_jobid = 0
        self.readout_para = {}
        self.sparam = sparam
        self.dcsweepch = dcsweepch
        if designed != "":
            self.designed = int(designed)
        else:
            self.designed = 0


    def write_specification(self,specifications):
        db = connect(sql_path)
        samplename = get_status("MSSN")[session['user_name']]['sample']
        # samplename = "2QAS-19-3"
        print("Check: ",samplename)
        db.execute('UPDATE sample SET specifications = ? WHERE samplename = ?', (str(specifications).replace("\'","\""),samplename))
        db.commit()
        db.close()

    def read_specification(self):
        connection = connect(sql_path)
        sample = read_sql_query("SELECT * FROM sample", connection)
        samplename = get_status("MSSN")[session['user_name']]['sample']
        # samplename = "2QAS-19-3"
        specifications = sample[sample['samplename']==samplename]['specifications'].iloc[0]
        if specifications != "":
            spec_dict = ast.literal_eval(specifications)
            step_list = spec_dict["step"].split("-")
            if self.sparam == "" and self.dcsweepch == "":
                self.sparam = spec_dict["I/O"]
                self.cavity_list = spec_dict["results"]["CavitySearch"]["region"]


        else:
            spec_dict = {}
            step_list = []
        return spec_dict, step_list

        
    def cavitysearch(self,jobid_check):
        if jobid_check == "":
            jobid = Quest_command(self.sparam).cavitysearch()
            plot_ornot = 0
            self.CS_jobid = jobid
        else:
            jobid = jobid_check   
            speci,_ = self.read_specification()
            if speci != {}:
                self.designed = int(speci["CPW"])
            else:
                print("No designed CPW number record input manually plz!")
            plot_ornot = 1
        if self.designed != 0 :
            print("do measurement\n")
            dataframe = Load_From_pyqum(jobid).load()
            CS = CavitySearch(dataframe)
        
            self.cavity_list = CS.do_analysis(self.designed) #model h5 cannot import <- 0818 update, no need it anymore
            self.total_cavity_list = list(self.cavity_list.keys())
            if plot_ornot:
                self.CS_plot_items = CS.give_plot_info()
                self.CS_overview = CS.overview    # ena scan results
        else:
            self.cavity_list = {} #model h5 cannot import <- 0818 update, no need it anymore
            self.total_cavity_list = []
            if plot_ornot:
                self.CS_plot_items = {}
                self.CS_overview = {}    # ena scan results


        
    
    def powerdepend(self,cavity_freq,jobid_check):
        if jobid_check == "":
            jobid = Quest_command(self.sparam).powerdepend(select_freq=self.cavity_list[cavity_freq],add_comment="with Cavity "+str(cavity_freq))
            plot_ornot = 0
            self.jobid_dict["PowerDepend"] = jobid
        else:
            jobid = jobid_check
            plot_ornot = 1
        
        dataframe = Load_From_pyqum(jobid).load()
        PD = PowerDepend(dataframe)
        self.low_power, self.high_power = PD.do_analysis() #pass
        print("Select Power : %f"%self.low_power)
        if plot_ornot:	
            self.PD_plot_items = PD.give_plot_info()    # assume the function named `get_plot_items()`


    def fluxdepend(self,cavity_freq,f_bare,jobid_check):
        if jobid_check == "":
            jobid = Quest_command(self.sparam).fluxdepend(select_freq=self.cavity_list[cavity_freq],select_powa=self.low_power,dc_ch=self.dcsweepch,add_comment="with Cavity "+str(cavity_freq))
            plot_ornot = 0
            self.jobid_dict["FluxDepend"] = jobid
        else:
            jobid = jobid_check
            plot_ornot = 1
        
        dataframe = Load_From_pyqum(jobid).load()
        FD = FluxDepend(dataframe)
        self.wave = FD.do_analysis(f_bare) #pass
        print(self.wave)#{"f_dress":float(f_dress/1000),"f_bare":float(f_bare/1000),"f_diff":float((f_dress-f_bare)/1000),"offset":float(offset),"period":float(period)}
        
        if plot_ornot:	
            self.FD_plot_items = FD.give_plot_info()  # assume the function named `get_plot_items()`
    
    def qubitsearch(self,cavity_freq,jobid_check):
        if jobid_check == "":
            jobid = Quest_command(self.sparam).qubitsearch(select_freq=self.wave["f_dress"],select_powa=self.low_power,select_flux=str(self.wave["offset"])+'e-6',f_bare = self.wave["f_bare"],f_dress = self.wave["f_dress"],dcsweepch = self.dcsweepch,add_comment="with Cavity "+str(cavity_freq))
            plot_ornot = 0
            self.jobid_dict["QubitSearch"] = jobid
        else:
            jobid = jobid_check
            plot_ornot = 1    
        
        dataframe = Load_From_pyqum(jobid).load()
        CW = QubitFreq_Compa(dataframe)
        self.qubit_info = CW.do_analysis() #examine the input data form is dataframe because Series cannot reshape 

        if plot_ornot:	
            self.CW_plot_items = CW.plot_items
        print(self.qubit_info) 
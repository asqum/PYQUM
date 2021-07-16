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
from numpy import array, unwrap, mean, trunc, sqrt, zeros, ones, shape, arctan2, int64, isnan, abs, empty, ndarray, moveaxis, reshape, expand_dims, logical_and, nan


# Json to Javascrpt
import json

# Error handling
from contextlib import suppress

# Scientific
from scipy import constants as cnst
from si_prefix import si_format, si_parse
from numpy import cos, sin, pi, polyfit, poly1d, array, roots, isreal, sqrt, mean

# Load instruments
# Please Delete this line in another branch (to: @Jackie)
from pyqum.directive import calibrate 
from pyqum.directive.MP_benchmark import assembler
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

class QEstimation():

	def __init__( self, measurementObj, *args,**kwargs ):

		self.measurementObj = measurementObj
		self.independentVars = {}
		# Key and index
		self.freqKey = "Frequency"
		self.powerKey = "Power"

		self.yAxisKey = None
		self.varsInd = []

		# Data
		self.rawData = {}
		
		# Fit
		self.fitCurve = {}
		self.baseline = {}
		self.correctedIQData = {}
		self.fitResult = {}

		self._fitParameters = None
		self._init_fitResult()
		self._init_rawData()
		self._init_fitCurve()
		self._init_baselineCorrection()
		C_Shape = []
		for k in measurementObj.corder["C-Structure"] :
			# Get wavefrom object from c-order
			try:
				varWaveform = waveform( measurementObj.corder[k] )
			except(KeyError):
				varWaveform = waveform('opt,')
			# Get array from Waveform object
			self.independentVars[k]=array(varWaveform.data)
			# Get C-Shape from Waveform object
			C_Shape.append( varWaveform.count )
		# Append datadensity to C-Shape (list) and Measurement.corder["C-Structure"] (list)
		measurementObj.corder["C-Structure"].append("datadensity")
		C_Shape.append( measurementObj.datadensity )
		# Add C-Shape (list) to Measurement.corder (Dict)
		self.measurementObj.corder["C_Shape"] = C_Shape
		print("Init", self.measurementObj.corder)

		# Optimize (developing)
		'''
		self.optCShpae = C_Shape
		self.optCStructure = measurementObj.corder["C-Structure"]
		for s, k in zip(C_Shape,measurementObj.corder["C-Structure"]) :
			if s == 1:
				self.optCShpae.remove(s)
				self.optCStructure.remove(k)
		'''	
	def _init_rawData( self, yAxisLen=0, xAxisLen=0 ):
		self.rawData = {
			"frequency": empty([xAxisLen]),
			"iqSignal": empty([yAxisLen,xAxisLen], dtype=complex),
		}

	def _init_fitResult( self, yAxisLen=0 ):
		nanArray = empty([yAxisLen])
		nanArray.fill( nan )

		resultKeys = ["Qi_dia_corr","Qi_no_corr","absQc","Qc_dia_corr","Ql","fr","theta0","phi0"]
		errorKeys = ["phi0_err", "Ql_err", "absQc_err", "fr_err","chi_square","Qi_no_corr_err","Qi_dia_corr_err"]
		extendResultKeys = ["power_corr", "single_photon_limit", "photons_in_resonator"]
		results ={}
		errors ={}
		extendResults ={}
		for rk in resultKeys:
			results[rk] = nanArray.copy()
		for ek in errorKeys:
			errors[ek] = nanArray.copy()
		for erk in extendResultKeys:
			extendResults[erk] = nanArray.copy()

		self.fitResult={
			"results": results,
			"errors": errors,
			"extendResults": extendResults,
		}

	def _init_fitCurve( self, yAxisLen=0, xAxisLen=0 ):
		self.fitCurve = {
			"frequency": empty([xAxisLen]),
			"iqSignal": empty([yAxisLen,xAxisLen], dtype=complex),
		}
	def _init_baselineCorrection( self, yAxisLen=0, xAxisLen=0  ):
		self.baseline = {
			"frequency": empty([xAxisLen]),
			"iqSignal": empty([yAxisLen,xAxisLen], dtype=complex),
		}
		self.correctedIQData = {
			"frequency": empty([xAxisLen]),
			"iqSignal": empty([yAxisLen,xAxisLen], dtype=complex),
		}
	@property
	def fitParameters(self):
		return self._fitParameters

	@fitParameters.setter
	def fitParameters(self, fitParameters=None):
		if fitParameters == None:
			fitParameters={
				"range": {
					"from": 5,
					"to": 8
				},
				"baseline":{
					"correction": False,
					"smoothness": 1e9,
					"asymmetry": 0.995,
				},				
				"gain":0,
			}
		else:
			fitParameters["range"]["from"] = float(fitParameters["range"]["from"])*1e9
			fitParameters["range"]["to"] = float(fitParameters["range"]["to"])*1e9
			fitParameters["baseline"]["smoothness"] = float(fitParameters["baseline"]["smoothness"])
			fitParameters["baseline"]["asymmetry"] = float(fitParameters["baseline"]["asymmetry"])
			fitParameters["gain"] = float(fitParameters["gain"])
		self._fitParameters = fitParameters


	def _get_data_from_Measurement( self ):
		writtensize = self.measurementObj.writtensize
		pqfile = self.measurementObj.pqfile
		datalocation = self.measurementObj.datalocation

		with open(pqfile, 'rb') as datapie:
			datapie.seek(datalocation+7)
			pie = datapie.read(writtensize)
			selectedata = list(struct.unpack('>' + 'd'*((writtensize)//8), pie))
			
		return array(selectedata)

	def reshape_Data ( self, varsInd, yAxisKey=None ):
		# Data dimension should <= 3
		print("Reshape Data")

		cShape = self.measurementObj.corder["C_Shape"]
		self.yAxisKey = yAxisKey
		self.varsInd = varsInd.copy()
		self._init_baselineCorrection()
		self._init_fitResult()

		data = self._get_data_from_Measurement()

		data = reshape( data, tuple(cShape) )
		varsInd.append(1) # Temporary for connect with old data type

		if yAxisKey == None:
			moveAxisKey = ["datadensity", self.freqKey]
		else:
			moveAxisKey = ["datadensity", self.yAxisKey, self.freqKey]
		
		selectValInd = []
		includeAxisInd = []
		for i, k in enumerate(self.measurementObj.corder["C-Structure"]):
			if k not in moveAxisKey:	
				selectValInd.append(varsInd[i])
			else:
				includeAxisInd.append(i)

		includeAxisInd = []
		newAxisPosition = []
		for i, k in enumerate(moveAxisKey):
			includeAxisInd.append(self.measurementObj.corder["C-Structure"].index(k) )
			newAxisPosition.append(-len(moveAxisKey)+i)


		data = moveaxis( data, includeAxisInd, newAxisPosition )

		# To 3 dimension
		for vi in selectValInd:
			data = data[vi]
		if data.ndim == 2:
			data = expand_dims(data,axis=1)

		# Convert to complex number
		self.rawData = { 
			"frequency": self.independentVars[self.freqKey]*1e9, #GHz to Hz
			"iqSignal": data[0]+1j*data[1],
		}


	def do_analysis( self ):
		fitRange = ( self.fitParameters["range"]["from"], self.fitParameters["range"]["to"] )

		xAxisLen = self.rawData["frequency"].shape[0]

		# Get 1D or 2D data to self.rawData
		if self.yAxisKey == None:
			yAxisLen = 1
		else:
			yAxisLen = self.independentVars[self.yAxisKey].shape[0]

		self._init_fitCurve(yAxisLen=yAxisLen,xAxisLen=xAxisLen)
		self._init_baselineCorrection(yAxisLen=yAxisLen,xAxisLen=xAxisLen)
		self._init_fitResult(yAxisLen=yAxisLen)

		# Set x-axis (frequency) of fit curve 
		self.fitCurve["frequency"] = self.rawData["frequency"]

		if self.fitParameters["baseline"]["correction"] == True :
			self.baseline["frequency"] = self.rawData["frequency"]
			self.correctedIQData["frequency"] = self.rawData["frequency"]
		else: 
			self._init_baselineCorrection()
		myResonator = notch_port()
		# Creat notch port list
		for i in range(yAxisLen):
			# Fit baseline
			if self.fitParameters["baseline"]["correction"] == True :
				fittedBaseline = myResonator.fit_baseline_amp( self.rawData["iqSignal"][i], self.fitParameters["baseline"]["smoothness"], self.fitParameters["baseline"]["asymmetry"],niter=1)
				correctedIQ = self.rawData["iqSignal"][i]/fittedBaseline
				# Save Corrected IQData
				self.correctedIQData["iqSignal"][i] = correctedIQ
				# Save baseline
				self.baseline["iqSignal"][i] = fittedBaseline
			else: 
				self._init_baselineCorrection()
				correctedIQ = self.rawData["iqSignal"][i]
			# Add data
			myResonator.add_data(self.rawData["frequency"], correctedIQ)
			# Fit
			try:
				myResonator.autofit(fcrop=fitRange)
				fitSuccess = True
			except:
				fitSuccess = False

			if fitSuccess:

				for k in self.fitResult["results"].keys():
					self.fitResult["results"][k][i] = myResonator.fitresults[k]

				for k in self.fitResult["errors"].keys():
					self.fitResult["errors"][k][i] = myResonator.fitresults[k]


				self.fitResult["extendResults"]["single_photon_limit"][i] = myResonator.get_single_photon_limit(unit='dBm',diacorr=True)

				if self.yAxisKey == self.powerKey:
					powerIndex = i
				else:
					powerAxisIndex = self.measurementObj.corder["C-Structure"].index(self.powerKey)
					powerIndex = self.varsInd[powerAxisIndex]
				self.fitResult["extendResults"]["power_corr"][i] = self.independentVars["Power"][powerIndex]+self.fitParameters["gain"]
				self.fitResult["extendResults"]["photons_in_resonator"][i] = myResonator.get_photons_in_resonator(self.fitResult["extendResults"]["power_corr"][i],unit='dBm',diacorr=True)
				self.fitCurve["iqSignal"][i] =myResonator.z_data_sim


	def get_htmlInfo( self ):
		hiddenKeys = ["datadensity",self.freqKey]
		htmlInfo = []
		for i, (k, l) in enumerate(zip(self.measurementObj.corder["C-Structure"],self.measurementObj.corder["C_Shape"])):
			if k not in hiddenKeys:
				info = {
					"name": k,
					"length": l,
					"structurePosition": i,
				}
				htmlInfo.append(info)
		return htmlInfo

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
		set_mat_analysis( myQEstimation.fitResult, 'QEstimation[%s]'%session['user_name'] )
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
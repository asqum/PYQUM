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
from numpy import array, unwrap, mean, trunc, sqrt, zeros, ones, shape, arctan2, int64, isnan, abs, empty, ndarray


# Json to Javascrpt
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
from pyqum.mission import get_measurementObject

# Fitting
from resonator_tools import circuit
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
	info = get_json_measurementinfo(get_fileName())
	htmlID = [ paras["htmlId"] for paras in info["measurement"]["parameters"] ]
	return jsonify(htmlID)

@bp.route('/qestimate', methods=['POST', 'GET'])
def qestimate(): 
	info = get_json_measurementinfo(get_fileName())
	global qEstimationDict
	qEstimationDict[session['user_name']] = QEstimation( get_measurementObject('frequency_response') )
	print(qEstimationDict[session['user_name']].measurementObj.corder)
	return render_template("blog/benchmark/qestimate.html", info=info)

@bp.route('/get_user', methods=['POST', 'GET'])
def get_user():
	return jsonify(session['user_name'])

@bp.route('/measurement_info', methods=['POST', 'GET'])
def measurement_info(): 

	info = get_json_measurementinfo(get_fileName())
	print( "measurement_info", info['measurement']['type'])

	return render_template("blog/benchmark/measurement_info.html", info=info)

class QEstimation():

	def __init__( self, measurementObj, *args,**kwargs ):

		self.measurementObj = measurementObj
		self.independentVars = {}


		self.freqKey = "Frequency"
		self.yAxisKey = None

		self.iqData = empty([0])
		self.fitCurve = empty([0])
		self.fitResult = {}

		C_Shape = []
		for k in measurementObj.corder["C-Structure"] :
			# Get wavefrom object from c-order
			try:
				varWaveform = waveform( measurementObj.corder[k] )
			except(KeyError):
				varWaveform = waveform('opt,')
			# Get array from Waveform object
			self.independentVars[k]=varWaveform.data
			# Get C-Shape from Waveform object
			C_Shape.append( varWaveform.count )

		# Append datadensity to C-Shape (list) and Measurement.corder["C-Structure"] (list)
		measurementObj.corder["C-Structure"].append("datadensity")
		C_Shape.append( measurementObj.datadensity )
		# Add C-Shape (list) to Measurement.corder (Dict)
		self.measurementObj.corder["C_Shape"] = C_Shape

		# Optimize (developing)
		self.optCShpae = C_Shape
		self.optCStructure = measurementObj.corder["C-Structure"]
		for s, k in zip(C_Shape,measurementObj.corder["C-Structure"]) :
			if s == 1:
				self.optCShpae.remove(s)
				self.optCStructure.remove(k)
		
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

		cShape = self.measurementObj.corder["C_Shape"]
		self.yAxisKey = yAxisKey
		data = self._get_data_from_Measurement()
		data.reshape( tuple(cShape) )
		varsInd.append(1) # Temporary for connect with old data type
		yAxisInd = self.measurementObj.corder["C-Structure"].index(self.yAxisKey) 
		densityInd = self.measurementObj.corder["C-Structure"].index("datadensity")
		freqInd = self.measurementObj.corder["C-Structure"].index(self.freqKey)
		varNumber = len(varsInd)

  		varsInd.insert( varNumber, varsInd.pop(freqInd))
		if yAxisKey == None:
  			varsInd.insert( varNumber-1, varsInd.pop(densityInd))
			data.moveaxis( [densityInd, freqInd], [-2, -1] )
			varsInd = varsInd[:-2]
		else:
			varsInd.insert( varNumber-1, varsInd.pop(densityInd))
			varsInd.insert( varNumber-2, varsInd.pop(yAxisInd))
			varsInd = varsInd[:-3]
			data.moveaxis( [densityInd, yAxisInd, freqInd], [-3, -2, -1] )
		for vi in varsInd:
			data = data[vi]
		data.squeeze()
		self.iqData = data


	def do_analysis( self, fittingRange=None ):


		rawFrequency = self.independentVars[self.freqKey]
		xAxisLen = rawFrequency.shape[0]

		rawIQ = self.iqData[0]+1j*self.iqData[1]

		# Get 1D or 2D data to self.iqData
		if self.yAxisKey == None:
			yAxisLen = 1
			self.fitCurve = empty([xAxisLen])
		else:
			yAxisLen = self.independentVars[self.yAxisKey].shape[0]
			self.fitCurve = empty([yAxisLen,xAxisLen])

		
		# Creat notch port list
		resonator = circuit.notch_port() 
		for i in range(yAxisLen):
			# Add data
			resonator.add_data(f_data=rawFrequency, z_data_raw=rawIQ[i])
			# Fit
			resonator.autofit( electric_delay=None, fcrop=fittingRange, Ql_guess=None, fr_guess=None )

			for key in resonator.fitresults.keys():
				fittingValue = resonator.fitresults[key]
				if isnan(fittingValue):
					fittingValue = 0
				if i==0 :
						self.fitResult[key] = empty(yAxisLen)
				self.fitResult[key][i] = fittingValue
			# Save fitted curve	
			self.fitCurve[i] = resonator.z_data_sim

	

# Test return plot data in new way
qEstimationDict = {}

@bp.route('/qestimate/getJson_2Dplot_test',methods=['POST','GET'])
def getJson_2Dplot_test():
	myQEstimation = qEstimationDict[session['user_name']]

	indexData = json.loads(request.args.get('indexData'))
	dimension = len(indexData["axisIndex"]["data"])
	if dimension == 2:
		axisInd = indexData["axisIndex"]["data"][1]
		yAxisKey = myQEstimation.measurementObj["C-Structure"][axisInd] # Temporary for connect with old data type
	else:
		yAxisKey = None
	valueInd = indexData["valueIndex"]["data"]
	preYAxisKey = myQEstimation.yAxisKey
	if preYAxisKey != yAxisKey or preYAxisKey == None:
		myQEstimation.reshape_Data( valueInd, yAxisKey=yAxisKey )
	plotData = {
			"frequency": myQEstimation.independentVars[myQEstimation.freqKey],
			yAxisKey: myQEstimation.independentVars[myQEstimation.yAxisKey],
			"amplitude": 10(myQEstimation.iqData[0]**2+myQEstimation.iqData[1]**2)
		}

	#print(plotData)
	return json.dumps(plotData, cls=NumpyEncoder)
@bp.route('/qestimate/getJson_1Dplot_test',methods=['POST','GET'])
def getJson_1Dplot_test():

	myQEstimation = qEstimationDict[session['user_name']]

	indexData = json.loads(request.args.get('indexData'))
	dimension = len(indexData["axisIndex"]["data"])
	if dimension == 2:
		axisInd = indexData["axisIndex"]["data"][1]
		yAxisKey = myQEstimation.measurementObj["C-Structure"][axisInd] # Temporary for connect with old data type
	else:
		yAxisKey = None
	valueInd = indexData["valueIndex"]["data"]
	preYAxisKey = myQEstimation.yAxisKey
	if preYAxisKey != yAxisKey or preYAxisKey == None:
		myQEstimation.reshape_Data( valueInd, yAxisKey=yAxisKey )
	plotData = {
		"Data_point": {
			"frequency": myQEstimation.independentVars[myQEstimation.freqKey],
			"amplitude": 10(myQEstimation.iqData[0]**2+myQEstimation.iqData[1]**2),
		},
		"Fitted_curve": {
			"frequency": myQEstimation.independentVars[myQEstimation.freqKey],
			"amplitude": 20*abs(myQEstimation.fitCurve)
		}
	}
	#print(plotData)
	return json.dumps(plotData, cls=NumpyEncoder)

@bp.route('/qestimate/getJson_fitParaPlot_test',methods=['POST','GET'])
def getJson_fitParaPlot_test():

	myQEstimation = qEstimationDict[session['user_name']]

	myQEstimation.do_analysis()
	plotData = myQEstimation.fitResult

	indexData = json.loads(request.args.get('indexData'))
	dimension = len(indexData["axisIndex"]["data"])
	if dimension == 2:
		axisInd = indexData["axisIndex"]["data"][1]
		yAxisKey = myQEstimation.measurementObj["C-Structure"][axisInd] # Temporary for connect with old data type
	else:
		yAxisKey = None

	plotData[yAxisKey] = myQEstimation.independentVars[myQEstimation.yAxisKey]

	#print(plotData)
	return json.dumps(plotData, cls=NumpyEncoder)

def renew_iqData (valueIndex, axisIndex):

	global iqData
	info = get_json_measurementinfo(get_fileName())

	stage, prev = clocker(0, agenda="2D Fresp")
	iqData = assembler( valueIndex, axisIndex, info, session['user_name'] )
	stage, prev = clocker(stage, prev, agenda="2D Fresp") # Marking time

	return iqData


def get_qestimate_plot_rawData(indexData):
	global gIqData2D, gIqData1D, gValueIndex, gAxisIndex
	
	valueIndex = [int(vi) for vi in indexData["valueIndex"]["data"]]
	axisIndex = [int(ai) for ai in indexData["axisIndex"]["data"]]
	plotDimension = len(axisIndex)

	if indexData["axisIndex"]["isChange"]:
		renew_iqData(valueIndex, axisIndex)

	info = get_json_measurementinfo(get_fileName())

	paraInfo = info["measurement"]["parameters"]

	if( plotDimension == 2):
		iAmp = iqData['I']
		qAmp = iqData['Q']
		transAmp = sqrt(iAmp**2+qAmp**2)
		plotData = {
				paraInfo[axisIndex[0]]["htmlId"]: paraInfo[axisIndex[0]]["values"],
				paraInfo[axisIndex[1]]["htmlId"]: paraInfo[axisIndex[1]]["values"],
				"I": iAmp.transpose(),
				"Q": qAmp.transpose(),
				"amplitude": transAmp.transpose(),
		}
		gIqData2D = iqData
		gAxisIndex = axisIndex

		set_mat_analysis(plotData, "IQ_2Ddata[%s]"%session['user_name'])
	else:
		iAmp = iqData['I']
		qAmp = iqData['Q']
		transAmp = sqrt(iAmp**2+qAmp**2)
		plotData = {
			paraInfo[axisIndex[0]]["htmlId"]: paraInfo[axisIndex[0]]["values"],
			"I": iAmp,
			"Q": qAmp,			
			"amplitude": transAmp
		}

	return plotData



def get_qestimate_plot_fitCurve(indexData):

	valueIndex = [int(vi) for vi in indexData["valueIndex"]["data"]]
	axisIndex = [int(ai) for ai in indexData["axisIndex"]["data"]]
	plotDimension = len(axisIndex)

	print(Fore.GREEN + "User %s is plotting %dD Data" %(session['user_name'],plotDimension) )

	print("valueIndex",valueIndex,",axisIndex",axisIndex)
	print("valueIndex",valueIndex,",axisIndex",axisIndex)

	if( plotDimension == 2):
		plotData = {
			"Frequency": fitResult["Frequency"],			
			"amplitude": fitResult["amplitude"]
		}
	else:
		plotData = {
			"Frequency": fitResult["Frequency"],			
			"amplitude": fitResult["amplitude"][valueIndex[axisIndex[0]]]
		}

	return plotData

@bp.route('/qestimate/getJson_qestimate_plot',methods=['POST','GET'])
def getJson_qestimate_plot():
	indexData = json.loads(request.args.get('indexData'))
	print(indexData)
	try:
		print("Try get_qestimate_plot_fitCurve(indexData)")
		fitCurveData = get_qestimate_plot_fitCurve(indexData)
	except:
		fitCurveData = {"amplitude":[]}
	rawData = get_qestimate_plot_rawData(indexData)
	plotData = {
		"Frequency": rawData["Frequency"],
		"Data_point": rawData["amplitude"],
		"Fitted_curve": fitCurveData["amplitude"]
	}
	#print(plotData)
	return json.dumps(plotData, cls=NumpyEncoder)

def do_qestimate_fitting( fittingRange ):
	global fitResult
	info = get_json_measurementinfo(get_fileName())
	print("I shape:", gIqData2D["I"].shape, "Q shape:", gIqData2D["Q"].shape )

	yAxisInfo = info["measurement"]["parameters"][gAxisIndex[1]]
	yAxisLen = len(yAxisInfo["values"])

	fitIQ = gIqData2D["I"].transpose()+1j*gIqData2D["Q"].transpose()
	fitFrequency= array(info["measurement"]["parameters"][4]["values"])
	#fittingRange = [float(fittingRangeFrom),float(fittingRangeTo)]

	# get range for fitting
	fittingIndex = find_nearestIndex( fitFrequency, fittingRange )
	fittingIndex.sort()
	xAxisLen = fitFrequency.shape[0]

	port = circuit.notch_port()
	fitResult = {
		"amplitude" : empty([yAxisLen,xAxisLen]),
		"Frequency" : fitFrequency,
		yAxisInfo["lable"] : empty(xAxisLen)
	}
	for ifitIQ, i in zip(fitIQ, range(yAxisLen) ):
		port.add_data( fitFrequency ,ifitIQ )
		#port.autofit( electric_delay=None,fcrop=fittingRange,Ql_guess=None, fr_guess=None )
		port.autofit( )
		for key in port.fitresults.keys():
			fittingValue = port.fitresults[key]
			if isnan(fittingValue):
				fittingValue = 0
			if i==0 :
					fitResult[key] = empty(yAxisLen)
			fitResult[key][i] = fittingValue			
		fitResult["amplitude"][i] = abs(port.z_data_sim)

	#set_mat_analysis(fitResult, "resonator_fit[%s]"%session['user_name'])
	return fitResult

@bp.route('/qestimate/getJson_qestimate_fitResult',methods=['POST','GET'])
def getJson_qestimate_fitResult():

	fittingRangeFrom = request.args.get('fittingRangeFrom')
	fittingRangeTo = request.args.get('fittingRangeTo')
	info = get_json_measurementinfo(get_fileName())
	print("I shape:", gIqData2D["I"].shape, "Q shape:", gIqData2D["Q"].shape )
	print("Fitting range:", fittingRangeFrom, fittingRangeTo)

	fittingRange = (float(fittingRangeFrom),float(fittingRangeTo))

	print(json.dumps(do_qestimate_fitting(fittingRange), cls=NumpyEncoder))

	return json.dumps(do_qestimate_fitting(fittingRange), cls=NumpyEncoder)#jsonify(fitResult)



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
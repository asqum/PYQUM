# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name

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
	print( "measurement_info", info['measurement']['type'])
	print("qestimate")
	return render_template("blog/benchmark/qestimate.html", info=info)

@bp.route('/get_user', methods=['POST', 'GET'])
def get_user():
	return jsonify(session['user_name'])

@bp.route('/measurement_info', methods=['POST', 'GET'])
def measurement_info(): 

	info = get_json_measurementinfo(get_fileName())
	print( "measurement_info", info['measurement']['type'])

	return render_template("blog/benchmark/measurement_info.html", info=info)

def get_iqData (valueIndex, axisIndex):

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
		get_iqData(valueIndex, axisIndex)

	info = get_json_measurementinfo(get_fileName())

	paraInfo = info["measurement"]["parameters"]

	iAmp = iqData['I']
	qAmp = iqData['Q']
	transAmp = sqrt(iAmp**2+qAmp**2)

	if( plotDimension == 2):
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
		plotData = {
			paraInfo[axisIndex[0]]["htmlId"]: paraInfo[axisIndex[0]]["values"],
			"I": iAmp,
			"Q": qAmp,			
			"amplitude": transAmp
		}
		gIqData1D = iqData

	return plotData



def get_qestimate_plot_fitCurve(indexData):

	valueIndex = [int(vi) for vi in indexData["valueIndex"]["data"]]
	axisIndex = [int(ai) for ai in indexData["axisIndex"]["data"]]
	plotDimension = len(axisIndex)

	print(Fore.GREEN + "User %s is plotting %dD Data" %(session['user_name'],plotDimension) )

	print("valueIndex",valueIndex,",axisIndex",axisIndex)
	print("valueIndex",valueIndex,",axisIndex",axisIndex)

	info = get_json_measurementinfo(get_fileName())
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



print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this


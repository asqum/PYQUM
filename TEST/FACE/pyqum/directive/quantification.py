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
from numpy import array, unwrap, mean, trunc, sqrt, zeros, ones, shape, arctan2, int64, isnan, abs, empty, ndarray, moveaxis, reshape, expand_dims, logical_and, nan, arange, exp, amax, amin, diag, concatenate, append


# Json to Javascrpt
import json

# Error handling
from contextlib import suppress

# Scientific
from scipy import constants as cnst
from scipy.optimize import curve_fit
from scipy.stats import linregress

#from si_prefix import si_format, si_parse
from numpy import cos, sin, pi, polyfit, poly1d, array, roots, isreal, sqrt, mean, std, histogram

# Load instruments
# Please Delete this line in another branch (to: @Jackie)
from pyqum.directive import calibrate 
from pyqum.mission import get_measurementObject

# Fitting
from resonator_tools.circuit import notch_port
from collections import defaultdict

# Save file
from scipy.io import savemat

# Cavuty searching
from pyqum.directive.cavity_search.toolfunc import input_process,output_process,true_alt_info
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

class ExtendMeasurement ():
	def __init__( self, measurementObj, *args,**kwargs ):
		self.measurementObj = measurementObj
		self.independentVars = {}
		# Key and index
		self.xAxisKey = None
		self.yAxisKey = None
		self.aveAxisKey = None

		self.varsInd = []
		self.axisInd = []
		self.averageInd = []
		self.innerRepeatKeys = []
		# Selected Data
		self.rawData = {}
		# Initialize
		self._init_rawData()

		# Integrate R-Parameters back into C-Order:
		if "R-JSON" in self.measurementObj.perimeter:
			RJSON = json.loads(self.measurementObj.perimeter['R-JSON'].replace("'",'"'))

			# Recombine Buffer back into C-Order:
			if self.measurementObj.perimeter['READOUTYPE'] == 'one-shot': bufferkey = 'RECORD-SUM'
			else: bufferkey = 'RECORD_TIME_NS'

			# Extend C-Structure with R-Parameters & Buffer keys:
			self.measurementObj.corder['C-Structure'] = self.measurementObj.corder['C-Structure'] + [k for k in RJSON.keys()] + [bufferkey] # Fixed-Structure + R-Structure + Buffer

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
			C_Shape.append( varWaveform.count*varWaveform.inner_repeat  )
			if varWaveform.inner_repeat != 1:
				self.innerRepeatKeys.append( k )

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

	def _get_data_from_Measurement( self ):
		writtensize = self.measurementObj.writtensize
		pqfile = self.measurementObj.pqfile
		datalocation = self.measurementObj.datalocation

		with open(pqfile, 'rb') as datapie:
			datapie.seek(datalocation+7)
			pie = datapie.read(writtensize)
			selectedata = list(struct.unpack('>' + 'd'*((writtensize)//8), pie))
			
		return array(selectedata)

	def _init_rawData( self, yAxisLen=0, xAxisLen=0 ):
		self.rawData = {
			"x": empty([xAxisLen]),
			"iqSignal": empty([yAxisLen,xAxisLen], dtype=complex),
		}

	def reshape_Data ( self, varsInd, axisInd=[], aveInfo=None ):
		# Data dimension should <= 3
		print("Reshape Data")

		# Get average parameters
		if len(aveInfo["axisIndex"]) != 0:
			self.aveAxisKey = self.measurementObj.corder["C-Structure"][aveInfo["axisIndex"][0]]
			self.averageInd = aveInfo["aveRange"]
		else:
			self.aveAxisKey = None

		cShape = self.measurementObj.corder["C_Shape"]
		self.xAxisKey = self.measurementObj.corder["C-Structure"][axisInd[0]]
		# Get axis key from C-order
		if len(axisInd)== 2:
			self.yAxisKey = self.measurementObj.corder["C-Structure"][axisInd[1]]
		else:
			self.yAxisKey = None

		self.varsInd = varsInd.copy()
		self.axisInd = axisInd.copy()


		self.measurementObj.loadata()
		data = self.measurementObj.selectedata
		data = reshape( data, tuple(cShape) )
		varsInd.append(1) # Temporary for connect with old data type

		if self.yAxisKey == None:
			moveAxisKey = ["datadensity", self.xAxisKey]
		else:
			moveAxisKey = ["datadensity", self.yAxisKey, self.xAxisKey]
		
		if self.aveAxisKey != None:
			moveAxisKey = moveAxisKey +[self.aveAxisKey]
		
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

		# Remove one value dimension
		for vi in selectValInd:
			data = data[vi]

		# Get average from independentVars aveAxisKey
		if self.aveAxisKey != None:
			data = mean(data, axis=len(data.shape)-1, where=self.array_mask())

		# To 3 dimension
		if data.ndim == 2:
			data = expand_dims(data,axis=1)

		
		# Get data to analysis
		self.rawData = { 
			"x": self.independentVars[self.xAxisKey], 
			"iqSignal": data[0]+1j*data[1],
		}

	def array_mask( self ) :
		indexArray = arange(len(self.independentVars[self.aveAxisKey]))
		mask = logical_and(indexArray>=self.averageInd[0], indexArray<=self.averageInd[1]) 
		return mask

	def get_htmlInfo( self ):
		hiddenKeys = ["datadensity"]
		htmlInfo = []
		for i, (k, l) in enumerate(zip(self.measurementObj.corder["C-Structure"],self.measurementObj.corder["C_Shape"])):
			if k not in hiddenKeys:
				info = {
					"name": k,
					"length": l,
					"structurePosition": i,
					"c_order": self.measurementObj.corder[k]
				}
				htmlInfo.append(info)
		return htmlInfo

class QEstimation():

	def __init__( self, quantificationObj, *args,**kwargs ):

		self.quantificationObj = quantificationObj
		# Key and index
		self.powerKey = "Power"
		
		# Fit
		self.fitCurve = {}
		self.baseline = {}
		self.correctedIQData = {}
		self.fitResult = {}

		self._fitParameters = None
		self._init_fitResult()
		
		self._init_fitCurve()
		self._init_baselineCorrection()



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
			"x": empty([xAxisLen]),
			"iqSignal": empty([yAxisLen,xAxisLen], dtype=complex),
		}
	def _init_baselineCorrection( self, yAxisLen=0, xAxisLen=0  ):
		self.baseline = {
			"x": empty([xAxisLen]),
			"iqSignal": empty([yAxisLen,xAxisLen], dtype=complex),
		}
		self.correctedIQData = {
			"x": empty([xAxisLen]),
			"iqSignal": empty([yAxisLen,xAxisLen], dtype=complex),
		}
	@property
	def fitParameters(self):
		return self._fitParameters

	@fitParameters.setter
	def fitParameters(self, fitParameters=None):
		if fitParameters == None:
			fitParameters={
				"interval": {
					"start": 5,
					"end": 8
				},
				"baseline":{
					"correction": False,
					"smoothness": 1e9,
					"asymmetry": 0.995,
				},				
				"gain":0,
			}
		else:
			fitRange = [float(k) for k in fitParameters["interval"]["input"].split(",")]
			fitParameters["interval"]["start"] = fitRange[0]
			fitParameters["interval"]["end"] = fitRange[1]
			fitParameters["baseline"]["smoothness"] = float(fitParameters["baseline"]["smoothness"])
			fitParameters["baseline"]["asymmetry"] = float(fitParameters["baseline"]["asymmetry"])
			fitParameters["gain"] = float(fitParameters["gain"])
		self._fitParameters = fitParameters





	def do_analysis( self, freqUnit = "GHz" ):

		qObj = self.quantificationObj
		xAxisLen = qObj.rawData["x"].shape[0]


		freqUnitConvertor = 1 # Convert to Hz
		if freqUnit == "GHz":
			freqUnitConvertor = 1e9

		fitRange = ( self.fitParameters["interval"]["start"]*freqUnitConvertor, self.fitParameters["interval"]["end"]*freqUnitConvertor )

		# Get 1D or 2D data to self.rawData
		if qObj.yAxisKey == None:
			yAxisLen = 1
		else:
			yAxisLen = qObj.independentVars[qObj.yAxisKey].shape[0]

		self._init_fitCurve(yAxisLen=yAxisLen,xAxisLen=xAxisLen)
		self._init_baselineCorrection(yAxisLen=yAxisLen,xAxisLen=xAxisLen)
		self._init_fitResult(yAxisLen=yAxisLen)



		myResonator = notch_port()
		# Creat notch port list
		for i in range(yAxisLen):
			# Fit baseline
			if self.fitParameters["baseline"]["correction"] == True :
				fittedBaseline = myResonator.fit_baseline_amp( qObj.rawData["iqSignal"][i], self.fitParameters["baseline"]["smoothness"], self.fitParameters["baseline"]["asymmetry"],niter=1)
				correctedIQ = qObj.rawData["iqSignal"][i]/fittedBaseline
				# Save Corrected IQ Data
				self.correctedIQData["iqSignal"][i] = correctedIQ
				# Save baseline
				self.baseline["iqSignal"][i] = fittedBaseline
			else: 
				self._init_baselineCorrection()
				correctedIQ = qObj.rawData["iqSignal"][i]
			# Add data
			myResonator.add_data(qObj.rawData["x"]*freqUnitConvertor, correctedIQ)
			# Fit
			try:
				myResonator.autofit(fcrop=fitRange)
				fitSuccess = True
				print("Good fitting")

			except:
				fitSuccess = False
				print("Bad fitting")


			if fitSuccess:

				for k in self.fitResult["results"].keys():
					self.fitResult["results"][k][i] = myResonator.fitresults[k]

				for k in self.fitResult["errors"].keys():
					self.fitResult["errors"][k][i] = myResonator.fitresults[k]


				self.fitResult["extendResults"]["single_photon_limit"][i] = myResonator.get_single_photon_limit(unit='dBm',diacorr=True)

				if qObj.yAxisKey == self.powerKey:
					powerIndex = i
				else:
					powerAxisIndex = qObj.measurementObj.corder["C-Structure"].index(self.powerKey)
					powerIndex = qObj.varsInd[powerAxisIndex]

				self.fitResult["extendResults"]["power_corr"][i] = qObj.independentVars["Power"][powerIndex]+self.fitParameters["gain"]
				self.fitResult["extendResults"]["photons_in_resonator"][i] = myResonator.get_photons_in_resonator(self.fitResult["extendResults"]["power_corr"][i],unit='dBm',diacorr=True)
				
				# Set x-axis (frequency) of fit curve 
				
				self.fitCurve["x"] = qObj.rawData["x"]
				self.fitCurve["iqSignal"][i] = myResonator.z_data_sim
				# Set x-axis (frequency) of baseline and corrected data 
				if self.fitParameters["baseline"]["correction"] == True :
					self.baseline["x"] = qObj.rawData["x"]
					self.correctedIQData["x"] = qObj.rawData["x"]
				else: 
					self._init_baselineCorrection()




class Decoherence():

	def __init__( self, quantificationObj, *args,**kwargs ):

		self.quantificationObj = quantificationObj
		# Key and index
		self.resultKeys = ["ampI", "offsetI", "ampQ", "offsetQ", "tau"]
		self.errorKeys = ["ampI_cov", "offsetI_cov", "ampQ_cov", "offsetQ_cov", "tau_cov"]		
		# Fit
		self.fitCurve = {}
		self.baseline = {}
		self.fitResult = {}

		self._fitParameters = None
		self._init_fitResult()
		self._init_fitCurve()




	def _init_fitResult( self, yAxisLen=0 ):
		nanArray = empty([yAxisLen])
		nanArray.fill( nan )

		results ={}
		errors ={}
		for rk in self.resultKeys:
			results[rk] = nanArray.copy()
		for ek in self.errorKeys:
			errors[ek] = nanArray.copy()

		self.fitResult={
			"results": results,
			"errors": errors,
		}

	def _init_fitCurve( self, yAxisLen=0, xAxisLen=0 ):
		self.fitCurve = {
			"x": empty([xAxisLen]),
			"iqSignal": empty([yAxisLen,xAxisLen], dtype=complex),
		}

	@property
	def fitParameters(self):
		return self._fitParameters

	@fitParameters.setter
	def fitParameters(self, fitParameters=None):
		if fitParameters == None:
			
			fitParameters={
				"interval": {
					"start": 5,
					"end": 8
				},
				"initial_value":{
				}
			}

		else:
			fitRange = [float(k) for k in fitParameters["interval"]["input"].split(",")]
			fitParameters["interval"]["start"] = fitRange[0]
			fitParameters["interval"]["end"] = fitRange[1]

		self._fitParameters = fitParameters

	def do_analysis ( self ):

		qObj = self.quantificationObj

		xAxisLen = qObj.rawData["x"].shape[0]

		# Get 1D or 2D data to self.rawData
		if qObj.yAxisKey == None:
			yAxisLen = 1
		else:
			yAxisLen = qObj.independentVars[qObj.yAxisKey].shape[0]

		self._init_fitCurve(yAxisLen=yAxisLen,xAxisLen=xAxisLen)
		self._init_fitResult(yAxisLen=yAxisLen)

		def expDecay ( x, amp, offset, tau):
			return amp*exp(-x/tau)+offset

		def iqExpDecay ( x, ampI, offsetI, ampQ, offsetQ, tau):
			return concatenate( (expDecay( x, ampI, offsetI, tau), expDecay( x, ampQ, offsetQ, tau )) )

		for i in range(yAxisLen):
			# Find initial value
			ampI = qObj.rawData["iqSignal"][i].real
			ampIEndPoint = (ampI[0],ampI[ampI.shape[0]-1])
			ampQ = qObj.rawData["iqSignal"][i].imag
			ampQEndPoint = (ampQ[0],ampQ[ampQ.shape[0]-1])
			guess = array([ampIEndPoint[0]-ampIEndPoint[1], ampIEndPoint[1], ampQEndPoint[0]-ampQEndPoint[1], ampQEndPoint[1],1000 ])
			# start fitting
			try:
				popt,pcov=curve_fit(iqExpDecay,qObj.rawData["x"],append(ampI,ampQ),guess)
				fitSuccess = True
				print("Good fitting")
			except:
				fitSuccess = False
				print("Bad fitting")

			if fitSuccess:
				self.fitCurve["iqSignal"][i] = expDecay( qObj.rawData["x"],popt[0],popt[1],popt[4]) +1j*expDecay( qObj.rawData["x"],popt[2],popt[3],popt[4])
				perr = sqrt(diag(pcov))

				for ki, k in enumerate(self.resultKeys):
					self.fitResult["results"][k][i] = popt[ki]
				for ki, k in enumerate(self.errorKeys):
					self.fitResult["errors"][k][i] = perr[ki]

		# Set x-axis (frequency) of fit curve 
		self.fitCurve["x"] = qObj.rawData["x"]


class RabiOscillation():

	def __init__( self, quantificationObj, *args,**kwargs ):

		self.quantificationObj = quantificationObj
		# Key and index
		self.resultKeys = ["ampI", "offsetI", "ampQ", "offsetQ", "tau", "omega", "phi"]
		self.errorKeys = ["ampI_cov", "offsetI_cov", "ampQ_cov", "offsetQ_cov", "tau_cov", "omega_cov", "phi_cov"]
		
		# Fit
		self.fitCurve = {}
		self.fitResult = {}

		self._fitParameters = None
		self._init_fitResult()
		
		self._init_fitCurve()


	def _init_fitResult( self, yAxisLen=0 ):
		nanArray = empty([yAxisLen])
		nanArray.fill( nan )

		results ={}
		errors ={}
		for rk in self.resultKeys:
			results[rk] = nanArray.copy()
		for ek in self.errorKeys:
			errors[ek] = nanArray.copy()


		self.fitResult={
			"results": results,
			"errors": errors,
		}

	def _init_fitCurve( self, yAxisLen=0, xAxisLen=0 ):
		self.fitCurve = {
			"x": empty([xAxisLen]),
			"iqSignal": empty([yAxisLen,xAxisLen], dtype=complex),
		}

	@property
	def fitParameters(self):
		return self._fitParameters

	@fitParameters.setter
	def fitParameters(self, fitParameters=None):
		if fitParameters == None:
			fitParameters={
				"interval": {
					"start": 5,
					"end": 8
				},
				"initial_value":{

				}

			}
		else:
			fitRange = [float(k) for k in fitParameters["interval"]["input"].split(",")]
			fitParameters["interval"]["start"] = fitRange[0]
			fitParameters["interval"]["end"] = fitRange[1]
		self._fitParameters = fitParameters

	def do_analysis ( self ):

		qObj = self.quantificationObj

		xAxisLen = qObj.rawData["x"].shape[0]

		# Get 1D or 2D data to self.rawData
		if qObj.yAxisKey == None:
			yAxisLen = 1
		else:
			yAxisLen = qObj.independentVars[qObj.yAxisKey].shape[0]

		self._init_fitCurve(yAxisLen=yAxisLen,xAxisLen=xAxisLen)
		self._init_fitResult(yAxisLen=yAxisLen)

		def dampingOscillation ( x, amp, offset, tau, omega, phi):
			return amp*exp(-x/tau)*cos(omega*x+phi)+offset

		def iqDampingOscillation ( x, ampI, offsetI, ampQ, offsetQ, tau, omega, phi):
			return concatenate( (dampingOscillation( x, ampI, offsetI, tau, omega, phi), dampingOscillation( x, ampQ, offsetQ, tau, omega, phi )) )

		# Creat notch port list
		for i in range(yAxisLen):
			ampI = qObj.rawData["iqSignal"][i].real
			ampIEndPoint = (amax(ampI),amin(ampI))
			ampQ = qObj.rawData["iqSignal"][i].imag
			ampQEndPoint = (amax(ampQ),amin(ampQ))
			guess = array([ (ampIEndPoint[0]-ampIEndPoint[1])/2, (ampIEndPoint[0]+ampIEndPoint[1])/2, (ampQEndPoint[0]-ampQEndPoint[1])/2, (ampQEndPoint[0]+ampQEndPoint[1])/2,1000, 0.01, 0])
			try:
				popt,pcov=curve_fit(iqDampingOscillation,qObj.rawData["x"],append(ampI,ampQ),guess)
				fitSuccess = True
				print("Good fitting")
			except:
				fitSuccess = False
				print("Bad fitting")

			if fitSuccess:
				self.fitCurve["iqSignal"][i] = dampingOscillation( qObj.rawData["x"],popt[0],popt[1],popt[4],popt[5],popt[6]) +1j*dampingOscillation( qObj.rawData["x"],popt[2],popt[3],popt[4],popt[5],popt[6])
				perr = sqrt(diag(pcov))

				for ki, k in enumerate(self.resultKeys):
					self.fitResult["results"][k][i] = popt[ki]
				for ki, k in enumerate(self.errorKeys):
					self.fitResult["errors"][k][i] = perr[ki]

		# Set x-axis (frequency) of fit curve 
		self.fitCurve["x"] = qObj.rawData["x"]

class PopulationDistribution():

	def __init__( self, quantificationObj, *args,**kwargs ):

		self.quantificationObj = quantificationObj
		# Key and index
		self.resultKeys = ["excitedCenterI", "excitedCenterQ", "excitedDeviationI", "excitedDeviationQ", "groundCenterI", "groundCenterQ", "groundDeviationQ", "groundDeviationI"]
		self.errorKeys = ["excitedCenterI_cov", "excitedCenterQ_cov", "excitedDeviationI_cov", "excitedDeviationQ_cov", "groundCenterI_cov", "groundCenterQ_cov", "groundDeviationQ_cov",  "groundDeviationI_cov"]
		
		# Fit
		self.fitCurve = {}
		self.fitResult = {}

		self._fitParameters = None
		self._init_fitResult()
		
		self._init_fitCurve()


	def _init_fitResult( self, yAxisLen=0 ):
		nanArray = empty([yAxisLen])
		nanArray.fill( nan )

		results ={}
		errors ={}
		for rk in self.resultKeys:
			results[rk] = nanArray.copy()
		for ek in self.errorKeys:
			errors[ek] = nanArray.copy()


		self.fitResult={
			"results": results,
			"errors": errors,
		}

	def _init_fitCurve( self, yAxisLen=0, xAxisLen=0 ):
		self.fitCurve = {
			"x": empty([xAxisLen]),
			"iqSignal": empty([yAxisLen,xAxisLen], dtype=complex),
		}

	@property
	def fitParameters(self):
		return self._fitParameters

	@fitParameters.setter
	def fitParameters(self, fitParameters=None):
		if fitParameters == None:
			fitParameters={
				"interval": {
					"start": 5,
					"end": 8
				},
				"initial_value":{

				}

			}
		else:
			fitRange = [float(k) for k in fitParameters["interval"]["input"].split(",")]
			fitParameters["interval"]["start"] = fitRange[0]
			fitParameters["interval"]["end"] = fitRange[1]
		self._fitParameters = fitParameters

	def do_analysis ( self ):

		qObj = self.quantificationObj

		xAxisLen = qObj.rawData["x"].shape[0]

		meanAll = mean(qObj.rawData["iqSignal"])
		ampIMeanAll = mean(qObj.rawData["iqSignal"].real)
		AmpQMeanAll = mean(qObj.rawData["iqSignal"].imag)

		slope, intercept, r, p, se = linregress(ampIMeanAll, AmpQMeanAll)
		rotateAngle = arctan2(slope)
		shiftedData = qObj.rawData["iqSignal"] - meanAll
		rotatedData = shiftedData*exp(-1j*rotateAngle)


		distributionData = histogram(rotatedData, bins='auto')
		# Get 1D or 2D data to self.rawData
		if qObj.yAxisKey == None:
			yAxisLen = 1
		else:
			yAxisLen = qObj.independentVars[qObj.yAxisKey].shape[0]

		for i in range(yAxisLen):
			shiftedData = qObj.rawData["iqSignal"][i] - meanAll
			rotatedData = rotateAngle*exp(-1j*rotateAngle)



class CavitySearch():

	def __init__( self, quantificationObj, *args,**kwargs ):

		self.quantificationObj = quantificationObj


	def do_analysis ( self ):



		AMP = load_model('LSTM_AMP_2.h5')
		PHA = load_model('LSTM_PHA_1.h5')
		# files = '/content/gdrive/MyDrive/Colab Notebooks/test/CPW-5-8.csv'

		#Generate input data(amp,pha), and comparison(to find the prediction frequency range)
		amp , pha , comparison = input_process(self.quantificationObj)      # comparison[no.][0] for freq start, end for comparison[no.][1]
		comparison = np.array(comparison)

		# prediction 
		amp_pred = AMP.predict(amp)
		pha_pred = PHA.predict(pha)
		true ,alt = output_process(amp_pred,pha_pred,comparison)  
		fig = pd.read_csv(files)
		zone = true_alt_info(true,alt,fig)
		print(zone)
# if __name__ == "__main__":
# 	worker_fresp(int(sys.argv[1]),int(sys.argv[2]))
	

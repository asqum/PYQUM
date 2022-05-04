class Common_fitting():

	def __init__( self, quantificationObj:ExtendMeasurement, *args,**kwargs ):

		self.quantificationObj = quantificationObj

		# Fit
		self.fitCurve = {}
		self.fitResult = {}

		self._fitParameters = None
		#self._init_fitResult()
		
		self._init_fitCurve()



	def _init_fitResult( self, yAxisLen=0, paraNames=[] ):
		nanArray = empty([yAxisLen])
		nanArray.fill( nan )
		fitParas = self.fitParameters

		# set names of fitting parameters
		if paraNames==[]:
			if fitParas["function"]=="ExpDecay":
				if fitParas["signal_type"]=="indpendent":
					paraNames= ["tau","ampI","offsetI","ampQ","offsetQ"]
				else:
					paraNames= ["amp","tau","offset"]

			elif fitParas["function"]=="RabiOscillation":
				if fitParas["signal_type"]=="indpendent":
					paraNames= ["tau", "frequency", "phi", "ampI", "offsetI", "ampQ", "offsetQ"]
				else:
					paraNames= ["amp","tau", "frequency", "phi", "offset"]
		self.paraNames =paraNames
		self.fitResult ={}
		for rk in paraNames:
			self.fitResult[rk]={}
			self.fitResult[rk]["value"] = nanArray.copy()
			self.fitResult[rk]["error"] = nanArray.copy()



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
				"function": "ExpDecay",
				"signal_type": "indpendent",
				"range": 0,
			}
		else:
			try:
			# convert string to float list
				fitRange = [float(k) for k in fitParameters["range"].split(",")]
				fitParameters["range"] = fitRange
			except:
				xData= self.quantificationObj.rawData["x"]
				fitParameters["range"] =[amin(xData),amax(xData)]
				
		self._fitParameters = fitParameters


	def amp_signal (self, yInd, mask):
		data = abs(self.quantificationObj.rawData["iqSignal"][yInd])[mask]
		return data
	def phase_signal (self, yInd, mask):
		data = angle(self.quantificationObj.rawData["iqSignal"][yInd])[mask]
		return data
	def indpendent_signal (self, yInd, mask):
		dataRe = self.quantificationObj.rawData["iqSignal"][yInd].real[mask]
		dataIm = self.quantificationObj.rawData["iqSignal"][yInd].imag[mask]
		data = append(dataRe,dataIm)
		return data


	def do_analysis( self ):

		qObj = self.quantificationObj
		xAxisLen = qObj.rawData["x"].shape[0]
		fitParas = self.fitParameters
		signalType = {
			'amp': self.amp_signal,
			'phase': self.phase_signal,
			'indpendent': self.indpendent_signal,
		}


				
		def fit_ExpDecay ( yInd, mask ) :
			guess = array([])
			data=signalType[fitParas["signal_type"]](yInd, mask)
			# Guess initial value
			if fitParas["signal_type"] == "indpendent":
				dataRe = qObj.rawData["iqSignal"][yInd].real
				dataIm = qObj.rawData["iqSignal"][yInd].imag
				guess = array([4000,dataRe[0]-dataRe[-1],dataRe[-1],dataIm[0],dataIm[-1]])
			else:
				# p: tau, IAmp, Ioffset, QAmp, Qoffset
				guess = array([data[0]-data[-1],4000,data[-1]])

			popt,pcov= curve_fit(fit_ExpDecay_func,qObj.rawData["x"][mask],data,p0=guess)
			return popt,pcov
		def fit_Rabi ( yInd, mask ) :
			guess = array([])

			data=signalType[fitParas["signal_type"]](yInd, mask)
			# Guess initial value
			timeStep= qObj.rawData["x"][mask][1]-qObj.rawData["x"][mask][0]
			freqAxis= fftfreq(qObj.rawData["iqSignal"][yInd].shape[-1],timeStep)
			freqInd=1
			# p: 0:tau, 1:omega, 2:phi, 3:IAmp, 4:Ioffset, 5:QAmp, 6:Qoffset
			if fitParas["signal_type"] == "indpendent":
				dataRe = qObj.rawData["iqSignal"][yInd].real
				dataIm = qObj.rawData["iqSignal"][yInd].imag
				if amax(fft(dataRe-mean(dataRe))) > amax(fft(dataIm-mean(dataIm))):
					freqInd = argmax( fft(dataRe) )
				else:
					freqInd = argmax( fft(dataIm) )

				guess = array([2000,abs(freqAxis[freqInd]),0,dataRe[0]-mean(dataRe),mean(dataRe),dataIm[0]-mean(dataIm),mean(dataIm)])
			else:
				# p: 0:amp, 1:tau, 2:omega, 3:phi, 4:offset
				freqInd = argmax(fft(data-mean(data)))
				guess = array([data[0]-mean(data),2000,abs(freqAxis[freqInd]),0,mean(data)])
			popt,pcov= curve_fit(fit_RabiOscillation_func,qObj.rawData["x"][mask],data,p0=guess)

			return popt,pcov
		fit = {
			'ExpDecay': fit_ExpDecay,
			'RabiOscillation': fit_Rabi,
		}
		getFitCurve = {
			'ExpDecay': get_ExpDecay_fitCurve,
			'RabiOscillation': get_RabiOscillation_fitCurve,
		}		



		# Get 1D or 2D data to self.rawData
		if qObj.yAxisKey == None:
			yAxisLen = 1
		else:
			yAxisLen = qObj.independentVars[qObj.yAxisKey].shape[0]
		
		self._init_fitCurve(yAxisLen=yAxisLen,xAxisLen=xAxisLen)
		self._init_fitResult(yAxisLen=yAxisLen)

		# Set x-axis (frequency) of fit curve 
		fitRangeBoolean = logical_and(qObj.rawData["x"]>=fitParas["range"][0],qObj.rawData["x"]<=fitParas["range"][1]) 
		self.fitCurve["x"] = qObj.rawData["x"]

		for i in range(yAxisLen):
			
			try:
			# 	# Fit
				popt,pcov= fit[fitParas["function"]](i, fitRangeBoolean)
				fitSuccess = True
			#print("Good fitting")

			except:
				fitSuccess = False
				print("Bad fitting")
			if fitSuccess:
				self.fitCurve["iqSignal"][i] = getFitCurve[fitParas["function"]]( qObj.rawData["x"], popt, fitParas["signal_type"])
				perr = sqrt(diag(pcov))

				for ki, k in enumerate(self.paraNames):
					if perr[ki] < abs(popt[ki])*10 :
						self.fitResult[k]["value"][i] = popt[ki]
						self.fitResult[k]["error"][i] = perr[ki]

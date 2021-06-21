'''
Multi Processor for fresp 2D-plotting:
'''

import sys, struct

from numpy import array
from multiprocessing import Pool
# Can't print over here (multiprocess pipeline)
# print("Running Parallel Calculation outside App Context!")
from numpy import meshgrid
from numpy import arange
from numpy import empty
from numpy import ndarray

from flask import session

from pyqum.instrument.logger import get_status, set_status,get_json_measurementinfo
from pyqum.instrument.toolbox import cdatasearch, gotocdata
from pyqum.instrument.analyzer import IQAP


def openPqfile( pqfile, datalocation, writtensize):

	with open(pqfile, 'rb') as datapie:
		datapie.seek(datalocation+7)
		pie = datapie.read(writtensize)
		selectedata = list(struct.unpack('>' + 'd'*((writtensize)//8), pie))
	return selectedata

def iqdata_access( position, selectedata, c_structure ):
	#print("AA = ",position)
	position[4]*=2
	I = selectedata[gotocdata(position,c_structure)]
	position[4]+=1
	Q = selectedata[gotocdata(position,c_structure)]
	#Amp,P = IQAP(I,Q)
	return I, Q #, Amp, P


def assembler( dataPosition, dimensionIndice, info, userName ):
	
	data = openPqfile(info["pqfile"],info["datalocation"],info["writtensize"])
	axisLength = []
	axis = []
	paraInfo = info["measurement"]["parameters"]
	#Two column
	for i, v in enumerate(dimensionIndice):
		axisLength.append( int(paraInfo[v]["length"]))
		axis.append( arange(axisLength[i]) )
	axisLength.insert(0,2)
	npdata = empty(axisLength)
	print("axisLength: ",axisLength)
	print("shape: ",npdata.shape)

	if len(axisLength) == 3:
		xv, yv = meshgrid(axis[0], axis[1], indexing='xy')
		#print(xv,yv)
		#print("shape: ",xv.shape, yv.shape)
		for indXY in zip(xv.flatten(), yv.flatten()):
			for indAxis,indDim in enumerate(dimensionIndice):
				dataPosition[indDim] = indXY[indAxis]
			npdata[0][indXY[0]][indXY[1]], npdata[1][indXY[0]][indXY[1]] = iqdata_access( dataPosition, data, info["c_structure"] )
			
	elif len(axisLength) == 2:
		for indX in axis[0]:
			dataPosition[dimensionIndice[0]] = indX
			npdata[0][indX], npdata[1][indX] = iqdata_access( dataPosition, data, info["c_structure"]  )

	# 2D array wih shape axis[0]*axis[1] 0=x & 1=y
	print("Data position: ",dataPosition) 


	data = {
		"I": array(npdata[0]), #.tolist()
		"Q": array(npdata[1])		
	}
 #.tolist()
	
	return data

def get_data( pqfile, datalocation, writtensize):

	with open(pqfile, 'rb') as datapie:
		datapie.seek(datalocation+7)
		pie = datapie.read(writtensize)
		selectedata = list(struct.unpack('>' + 'd'*((writtensize)//8), pie))
	return array(selectedata)

def assembler2( axisIndex, measurement ):


	cShape = measurement.corder["C_Shape"]
	axisIndex
	reduceCShape = []
	for s in cShape:
		if s != 1:
			reduceCShape.append(s)

	data = get_data( measurement.pqfile, measurement.datalocation, measurement.writtensize )
	data.reshape( tuple(reduceCShape) )
	data.moveaxis( -1, 0 )
	return data
	
# if __name__ == "__main__":
# 	worker_fresp(int(sys.argv[1]),int(sys.argv[2]))
	


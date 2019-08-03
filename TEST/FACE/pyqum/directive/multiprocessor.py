import sys, struct
from numpy import array
from multiprocessing import Pool

from pyqum.instrument.logger import get_status, set_status
from pyqum.instrument.toolbox import cdatasearch, gotocdata
from pyqum.instrument.analyzer import IQAP

pqfile = get_status("MPW")["pqfile"]
datalocation = get_status("MPW")["datalocation"]
writtensize = get_status("MPW")["writtensize"]
c_fresp_structure = get_status("MPW")["c_fresp_structure"]
isparam = int(get_status("MPW")["isparam"])
iifb = int(get_status("MPW")["iifb"])
ipowa = int(get_status("MPW")["ipowa"])

with open(pqfile, 'rb') as datapie:
	datapie.seek(datalocation+7)
	pie = datapie.read(writtensize)
	selectedata = list(struct.unpack('>' + 'd'*((writtensize)//8), pie))

def fresp_assembler(args):
	# (x,y) = args
	I = selectedata[gotocdata([args[1],isparam,iifb,ipowa,2*args[0]],c_fresp_structure)]
	Q = selectedata[gotocdata([args[1],isparam,iifb,ipowa,2*args[0]+1],c_fresp_structure)]
	Amp,P = IQAP(I,Q)
	return I, Q, Amp, P
def fresp_scanner(a, b):
	for i in a:
		for j in b:
			yield i, j

def worker_fresp(y_count,x_count):			
	pool = Pool()
	IQ = pool.map(fresp_assembler, fresp_scanner(range(y_count),range(x_count)), max(x_count,y_count)) #f_stream(range(1000),range(350)), 35000)
	pool.close(); pool.join()
	rI, rQ, rA, rP = [], [], [], []
	for i,j,k,l in IQ:
		rI.append(i); rQ.append(j); rA.append(k); rP.append(l)
	rI, rQ, rA, rP = array(rI).reshape(y_count,x_count), array(rQ).reshape(y_count,x_count), array(rA).reshape(y_count,x_count), array(rP).reshape(y_count,x_count)
	print("Finished processing results of shape %s" %str(rA.shape))
	set_status("MPW", {"Amp": rA.tolist()})
	return rI, rQ, rA, rP
	
# if __name__ == "__main__":
# 	worker_fresp(int(sys.argv[1]),int(sys.argv[2]))
	


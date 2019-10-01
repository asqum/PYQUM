'''
Multi Processor for fresp 2D-plotting:
'''

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
ifluxbias = get_status("MPW")["ifluxbias"]
ixyfreq = get_status("MPW")["ixyfreq"]
ixypowa = get_status("MPW")["ixypowa"]
isparam = get_status("MPW")["isparam"]
iifb = get_status("MPW")["iifb"]
ipowa = get_status("MPW")["ipowa"]
ifreq = get_status("MPW")["ifreq"]

with open(pqfile, 'rb') as datapie:
	datapie.seek(datalocation+7)
	pie = datapie.read(writtensize)
	selectedata = list(struct.unpack('>' + 'd'*((writtensize)//8), pie))

# y: xyfreq, x: fluxbias
def assembler_xyfreq_fluxbias(args):
	(y,x) = args
	I = selectedata[gotocdata([x,int(isparam),int(iifb),int(ipowa),2*y],c_fresp_structure)]
	Q = selectedata[gotocdata([x,int(isparam),int(iifb),int(ipowa),2*y+1],c_fresp_structure)]
	Amp,P = IQAP(I,Q)
	return I, Q, Amp, P

# y: freq, x: powa
def assembler_freq_powa(args):
	(y,x) = args
	I = selectedata[gotocdata([int(ifluxbias),int(isparam),int(iifb),x,2*y],c_fresp_structure)]
	Q = selectedata[gotocdata([int(ifluxbias),int(isparam),int(iifb),x,2*y+1],c_fresp_structure)]
	Amp,P = IQAP(I,Q)
	return I, Q, Amp, P

def scanner(a, b):
	for i in a:
		for j in b:
			yield i, j
def worker(y_count,x_count,y="xyfreq",x="fluxbias"):		
	pool = Pool()
	IQ = pool.map(eval("assembler_%s_%s" %(y,x)), scanner(range(y_count),range(x_count)), max(x_count,y_count))
	pool.close(); pool.join()
	rI, rQ, rA, rP = [], [], [], []
	for i,j,k,l in IQ:
		rI.append(i); rQ.append(j); rA.append(k); rP.append(l)
	rI, rQ, rA, rP = array(rI).reshape(y_count,x_count).tolist(), array(rQ).reshape(y_count,x_count).tolist(),\
					 array(rA).reshape(y_count,x_count).tolist(), array(rP).reshape(y_count,x_count).tolist()
	return {'rI': rI, 'rQ': rQ, 'rA': rA, 'rP': rP}

	
# if __name__ == "__main__":
# 	worker_fresp(int(sys.argv[1]),int(sys.argv[2]))
	


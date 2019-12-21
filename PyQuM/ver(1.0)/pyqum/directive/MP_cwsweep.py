'''
Multi Processor for fresp 2D-plotting:
'''

import sys, struct
from numpy import array
from multiprocessing import Pool

from pyqum.instrument.logger import get_status, set_status
from pyqum.instrument.toolbox import cdatasearch, gotocdata, waveform
from pyqum.instrument.analyzer import IQAP

pqfile = get_status("MPW")["pqfile"]
datalocation = get_status("MPW")["datalocation"]
writtensize = get_status("MPW")["writtensize"]
c_cwsweep_structure = get_status("MPW")["c_cwsweep_structure"]
irepeat = get_status("MPW")["irepeat"]
ifluxbias = get_status("MPW")["ifluxbias"]
ixyfreq = get_status("MPW")["ixyfreq"]
ixypowa = get_status("MPW")["ixypowa"]
isparam = get_status("MPW")["isparam"]
iifb = get_status("MPW")["iifb"]
ipowa = get_status("MPW")["ipowa"]
ifreq = get_status("MPW")["ifreq"]
powa_order = get_status("MPW")["powa_order"]
powa_wave = waveform(powa_order)
powa_repeat = powa_wave.inner_repeat

with open(pqfile, 'rb') as datapie:
	datapie.seek(datalocation+7)
	pie = datapie.read(writtensize)
	selectedata = list(struct.unpack('>' + 'd'*((writtensize)//8), pie))

# y: fluxbias, x: repeat
def assembler_fluxbias_repeat(args):
	(y,x) = args
	I, Q = 0, 0
	for i_prepeat in range(powa_repeat):
		r_powa = int(ipowa) * powa_repeat + i_prepeat # from the beginning position of repeating power
		I += selectedata[gotocdata([x,y,int(ixyfreq),int(ixypowa),int(isparam),int(iifb),int(ifreq),2*r_powa],c_cwsweep_structure)]
		Q += selectedata[gotocdata([x,y,int(ixyfreq),int(ixypowa),int(isparam),int(iifb),int(ifreq),2*r_powa+1],c_cwsweep_structure)]
	I /= powa_repeat
	Q /= powa_repeat
	Amp,P = IQAP(I,Q)
	return I, Q, Amp, P

# y: xyfreq, x: repeat
def assembler_xyfreq_repeat(args):
	(y,x) = args
	I, Q = 0, 0
	for i_prepeat in range(powa_repeat):
		r_powa = int(ipowa) * powa_repeat + i_prepeat # from the beginning position of repeating power
		I += selectedata[gotocdata([x,int(ifluxbias),y,int(ixypowa),int(isparam),int(iifb),int(ifreq),2*r_powa],c_cwsweep_structure)]
		Q += selectedata[gotocdata([x,int(ifluxbias),y,int(ixypowa),int(isparam),int(iifb),int(ifreq),2*r_powa+1],c_cwsweep_structure)]
	I /= powa_repeat
	Q /= powa_repeat
	Amp,P = IQAP(I,Q)
	return I, Q, Amp, P

# y: xyfreq, x: fluxbias
def assembler_xyfreq_fluxbias(args):
	(y,x) = args
	I, Q = 0, 0
	for i_prepeat in range(powa_repeat):
		r_powa = int(ipowa) * powa_repeat + i_prepeat # from the beginning position of repeating power
		I += selectedata[gotocdata([int(irepeat),x,y,int(ixypowa),int(isparam),int(iifb),int(ifreq),2*r_powa],c_cwsweep_structure)]
		Q += selectedata[gotocdata([int(irepeat),x,y,int(ixypowa),int(isparam),int(iifb),int(ifreq),2*r_powa+1],c_cwsweep_structure)]
	I /= powa_repeat
	Q /= powa_repeat
	Amp,P = IQAP(I,Q)
	return I, Q, Amp, P

# y: xypowa, x: xyfreq
def assembler_xypowa_xyfreq(args):
	(y,x) = args
	I, Q = 0, 0
	for i_prepeat in range(powa_repeat):
		r_powa = int(ipowa) * powa_repeat + i_prepeat # from the beginning position of repeating power
		I += selectedata[gotocdata([int(irepeat),int(ifluxbias),x,y,int(isparam),int(iifb),int(ifreq),2*r_powa],c_cwsweep_structure)]
		Q += selectedata[gotocdata([int(irepeat),int(ifluxbias),x,y,int(isparam),int(iifb),int(ifreq),2*r_powa+1],c_cwsweep_structure)]
	I /= powa_repeat
	Q /= powa_repeat
	Amp,P = IQAP(I,Q)
	return I, Q, Amp, P

# y: freq, x: xyfreq
def assembler_freq_xyfreq(args):
	(y,x) = args
	I, Q = 0, 0
	for i_prepeat in range(powa_repeat):
		r_powa = int(ipowa) * powa_repeat + i_prepeat # from the beginning position of repeating power
		I += selectedata[gotocdata([int(irepeat),int(ifluxbias),x,int(ixypowa),int(isparam),int(iifb),y,2*r_powa],c_cwsweep_structure)]
		Q += selectedata[gotocdata([int(irepeat),int(ifluxbias),x,int(ixypowa),int(isparam),int(iifb),y,2*r_powa+1],c_cwsweep_structure)]
	I /= powa_repeat
	Q /= powa_repeat
	Amp,P = IQAP(I,Q)
	return I, Q, Amp, P

# y: powa, x: xyfreq
def assembler_powa_xyfreq(args):
	(y,x) = args
	I, Q = 0, 0
	for i_prepeat in range(powa_repeat):
		r_powa = y * powa_repeat + i_prepeat # from the beginning position of repeating power
		I += selectedata[gotocdata([int(irepeat),int(ifluxbias),x,int(ixypowa),int(isparam),int(iifb),int(ifreq),2*r_powa],c_cwsweep_structure)]
		Q += selectedata[gotocdata([int(irepeat),int(ifluxbias),x,int(ixypowa),int(isparam),int(iifb),int(ifreq),2*r_powa+1],c_cwsweep_structure)]
	I /= powa_repeat
	Q /= powa_repeat
	Amp,P = IQAP(I,Q)
	return I, Q, Amp, P


# pending:
# y: freq, x: fluxbias
def assembler_freq_fluxbias(args):
	(y,x) = args
	I, Q = 0, 0
	for i_prepeat in range(powa_repeat):
		r_powa = int(ipowa) * powa_repeat + i_prepeat # from the beginning position of repeating power
		I += selectedata[gotocdata([int(irepeat),x,int(ixyfreq),int(ixypowa),int(isparam),int(iifb),y,2*r_powa],c_cwsweep_structure)]
		Q += selectedata[gotocdata([int(irepeat),x,int(ixyfreq),int(ixypowa),int(isparam),int(iifb),y,2*r_powa+1],c_cwsweep_structure)]
	I /= powa_repeat
	Q /= powa_repeat
	Amp,P = IQAP(I,Q)
	return I, Q, Amp, P


def scanner(a, b):
	for i in a:
		for j in b:
			yield i, j
def worker(y_count,x_count,y_name="xyfreq",x_name="fluxbias"):		
	pool = Pool()
	IQ = pool.map(eval("assembler_%s_%s" %(y_name,x_name)), scanner(range(y_count),range(x_count)), max(x_count,y_count))
	pool.close(); pool.join()
	rI, rQ, rA, rP = [], [], [], []
	for i,j,k,l in IQ:
		rI.append(i); rQ.append(j); rA.append(k); rP.append(l)
	rI, rQ, rA, rP = array(rI).reshape(y_count,x_count).tolist(), array(rQ).reshape(y_count,x_count).tolist(),\
					 array(rA).reshape(y_count,x_count).tolist(), array(rP).reshape(y_count,x_count).tolist()
	return {'rI': rI, 'rQ': rQ, 'rA': rA, 'rP': rP}

	
# if __name__ == "__main__":
# 	worker_fresp(int(sys.argv[1]),int(sys.argv[2]))
	


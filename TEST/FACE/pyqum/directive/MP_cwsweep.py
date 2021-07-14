'''
Multi Processor for fresp 2D-plotting:
THIS IS OUTSIDE APP-CONTEXT, ANY CHANGES HERE WILL BE REFLECTED IMMEDIATELY WITHOUT THE NEED OF SERVER RESTART.
'''

# import sys, struct
from numpy import array, mean, concatenate, arange, ones, ndarray
from multiprocessing import Pool, cpu_count
# Can't print over here (multiprocess pipeline)
# print("Running Parallel Calculation outside App Context!")

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
    # selectedata = list(struct.unpack('>' + 'd'*((writtensize)//8), pie))
    selectedata = ndarray(shape=(writtensize//8,), dtype=">d", buffer=pie) # speed up with numpy ndarray, with the ability to do indexing in it.

# A. Backward compatibility with OLD data(s) that are allowed to log more than 100%: (preserve the old method of sequential (slower) averaging)
# A1. y: fluxbias, x: repeat
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

# A2. y: xyfreq, x: repeat
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

# B. NEW data taking method ONLY requires the following: (using vectorized (faster) averaging against Power-Repeat)
# B1. y: xyfreq, x: fluxbias (NEW: Directly Vectorize then Mean along power-repeat)
def assembler_xyfreq_fluxbias(args):
    (y,x) = args
    c_addresses_head, c_addresses_body = ones([powa_repeat,1])*array([int(irepeat),x,y,int(ixypowa),int(isparam),int(iifb),int(ifreq)]), ones([powa_repeat,1])*array([]) # repeated constants # A + [] = A
    c_addresses_tail_I, c_addresses_tail_Q = 2 * ((ones([1,1])*arange(powa_repeat)).T + int(ipowa) * powa_repeat), 2 * ((ones([1,1])*arange(powa_repeat)).T + int(ipowa) * powa_repeat) + 1
    c_addresses_I, c_addresses_Q = concatenate((c_addresses_head, c_addresses_body, c_addresses_tail_I), axis=1), concatenate((c_addresses_head, c_addresses_body, c_addresses_tail_Q), axis=1) # 2D stack of c-addresses
    I, Q = mean(selectedata[gotocdata(c_addresses_I, c_cwsweep_structure)]), mean(selectedata[gotocdata(c_addresses_Q, c_cwsweep_structure)])
    Amp,P = IQAP(I,Q)
    return I, Q, Amp, P

# B2. y: freq, x: fluxbias
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

# B3. y: xypowa, x: xyfreq (NEW: Directly Vectorize then Mean along power-repeat)
def assembler_xypowa_xyfreq(args):
    (y,x) = args
    c_addresses_head, c_addresses_body = ones([powa_repeat,1])*array([int(irepeat),int(ifluxbias),x,y,int(isparam),int(iifb),int(ifreq)]), ones([powa_repeat,1])*array([]) # repeated constants # A + [] = A
    c_addresses_tail_I, c_addresses_tail_Q = 2 * ((ones([1,1])*arange(powa_repeat)).T + int(ipowa) * powa_repeat), 2 * ((ones([1,1])*arange(powa_repeat)).T + int(ipowa) * powa_repeat) + 1
    c_addresses_I, c_addresses_Q = concatenate((c_addresses_head, c_addresses_body, c_addresses_tail_I), axis=1), concatenate((c_addresses_head, c_addresses_body, c_addresses_tail_Q), axis=1) # 2D stack of c-addresses
    I, Q = mean(selectedata[gotocdata(c_addresses_I, c_cwsweep_structure)]), mean(selectedata[gotocdata(c_addresses_Q, c_cwsweep_structure)])
    Amp,P = IQAP(I,Q)
    return I, Q, Amp, P

# B4. y: freq, x: xyfreq
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

# B5. y: powa, x: xyfreq (NEW: Directly Vectorize then Mean along power-repeat)
def assembler_powa_xyfreq(args):
    (y,x) = args
    c_addresses_head, c_addresses_body = ones([powa_repeat,1])*array([int(irepeat),int(ifluxbias),x,int(ixypowa),int(isparam),int(iifb),int(ifreq)]), ones([powa_repeat,1])*array([]) # repeated constants # A + [] = A
    c_addresses_tail_I, c_addresses_tail_Q = 2 * ((ones([1,1])*arange(powa_repeat)).T + y * powa_repeat), 2 * ((ones([1,1])*arange(powa_repeat)).T + y * powa_repeat) + 1
    c_addresses_I, c_addresses_Q = concatenate((c_addresses_head, c_addresses_body, c_addresses_tail_I), axis=1), concatenate((c_addresses_head, c_addresses_body, c_addresses_tail_Q), axis=1) # 2D stack of c-addresses
    I, Q = mean(selectedata[gotocdata(c_addresses_I, c_cwsweep_structure)]), mean(selectedata[gotocdata(c_addresses_Q, c_cwsweep_structure)])
    Amp,P = IQAP(I,Q)
    return I, Q, Amp, P

# B6. y: powa, x: freq (NEW: Directly Vectorize then Mean along power-repeat)
def assembler_powa_freq(args):
    (y,x) = args
    c_addresses_head, c_addresses_body = ones([powa_repeat,1])*array([int(irepeat),int(ifluxbias),int(ixyfreq),int(ixypowa),int(isparam),int(iifb),x]), ones([powa_repeat,1])*array([]) # repeated constants # A + [] = A
    c_addresses_tail_I, c_addresses_tail_Q = 2 * ((ones([1,1])*arange(powa_repeat)).T + y * powa_repeat), 2 * ((ones([1,1])*arange(powa_repeat)).T + y * powa_repeat) + 1
    c_addresses_I, c_addresses_Q = concatenate((c_addresses_head, c_addresses_body, c_addresses_tail_I), axis=1), concatenate((c_addresses_head, c_addresses_body, c_addresses_tail_Q), axis=1) # 2D stack of c-addresses
    I, Q = mean(selectedata[gotocdata(c_addresses_I, c_cwsweep_structure)]), mean(selectedata[gotocdata(c_addresses_Q, c_cwsweep_structure)])
    Amp,P = IQAP(I,Q)
    return I, Q, Amp, P


def scanner(a, b):
    for i in a:
        for j in b:
            yield i, j
def worker(y_count,x_count,y_name="xyfreq",x_name="fluxbias"):
    worker_count = 1000000 # the more the merrier? # max(x_count,y_count)		
    pool = Pool()
    IQ = pool.map(eval("assembler_%s_%s" %(y_name,x_name)), scanner(range(y_count),range(x_count)), worker_count)
    pool.close(); pool.join()
    rI, rQ, rA, rP = [], [], [], []
    for i,j,k,l in IQ:
        rI.append(i); rQ.append(j); rA.append(k); rP.append(l)
    rI, rQ, rA, rP = array(rI).reshape(y_count,x_count).tolist(), array(rQ).reshape(y_count,x_count).tolist(),\
                     array(rA).reshape(y_count,x_count).tolist(), array(rP).reshape(y_count,x_count).tolist()
    return {'rI': rI, 'rQ': rQ, 'rA': rA, 'rP': rP, 'coresum': cpu_count(), 'x': '%s(%s)'%(x_name,x_count), 'y': '%s(%s)'%(y_name,y_count)}

    
# if __name__ == "__main__":
# 	worker_fresp(int(sys.argv[1]),int(sys.argv[2]))
    


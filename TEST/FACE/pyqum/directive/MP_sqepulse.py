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
cselect = get_status("MPW")["cselect"]


# Loading DATA:
with open(pqfile, 'rb') as datapie:
	datapie.seek(datalocation+7)
	pie = datapie.read(writtensize)
	selectedata = list(struct.unpack('>' + 'd'*((writtensize)//8), pie))

# Assembling 2D mesh:
def assembler(args):
	(y,x) = args

	selected_caddress = [s for s in cselect.values()]
        
	# Sweep-command:
	if k == 'repeat':
		selected_sweep = cmd_repeat[session['user_name']]
	else:
		selected_sweep = M_sqepulse[session['user_name']].corder[k]

	# Adjusting c-parameters range for data analysis based on progress:
	parent_address = selected_caddress[:CParameters['SQE_Pulse'].index(k)] # address's part before x
	if [int(s) for s in parent_address] < session['c_sqepulse_progress'][0:len(parent_address)]:
		print(Fore.YELLOW + "selection is well within progress")
		sweepables = session['c_sqepulse_structure'][CParameters['SQE_Pulse'].index(k)]
	else: sweepables = session['c_sqepulse_progress'][CParameters['SQE_Pulse'].index(k)]+1

	# Special treatment on the last 'buffer' parameter to factor out the data-density first: 
	if CParameters['SQE_Pulse'].index(k) == len(CParameters['SQE_Pulse'])-1 :
		isweep = range(sweepables//M_sqepulse[session['user_name']].datadensity)
	else:
		isweep = range(sweepables) # flexible access until progress resume-point
	print(Back.WHITE + Fore.BLACK + "Sweeping %s points" %len(isweep))

	Idata = zeros(len(isweep))
	Qdata = zeros(len(isweep))
	for i in isweep:
		selected_caddress[CParameters['SQE_Pulse'].index(k)] = i # register x-th position
		if [c for c in cselect.values()][-1] == "s": # sampling mode currently limited to time-range (last 'basic' parameter) only
			srange = request.args.get('srange').split("-") # sample range
			if [int(srange[1]) , int(srange[0])] > [session['c_sqepulse_structure'][-1]//M_sqepulse[session['user_name']].datadensity] * 2:
				print(Back.WHITE + Fore.RED + "Out of range")
			else:
				# FASTEST PARALLEL VECTORIZATION OF BIG DATA BY NUMPY:
				slength = int(srange[1]) - int(srange[0]) + 1
				# Assemble stacks of selected c-address for this sample range:
				selected_caddress_I = array([[int(s) for s in selected_caddress[:-1]] + [0]] * slength)
				selected_caddress_Q = array([[int(s) for s in selected_caddress[:-1]] + [0]] * slength)
				# sort-out interleaved IQ:
				selected_caddress_I[:,-1] = 2 * array(range(int(srange[0]),int(srange[1])+1))
				selected_caddress_Q[:,-1] = 2 * array(range(int(srange[0]),int(srange[1])+1)) + ones(slength)
				# Compressing I & Q of this sample range:
				selectedata = array(selectedata)
				Idata[i] = mean(selectedata[gotocdata(selected_caddress_I, session['c_sqepulse_structure'])]-0)
				Qdata[i] = mean(selectedata[gotocdata(selected_caddress_Q, session['c_sqepulse_structure'])]-0) 

		else:
			# Ground level Pulse shape response:
			selected_caddress = [int(s) for s in selected_caddress]
			Basic = selected_caddress[-1]
			# Extracting I & Q:
			Idata[i] = selectedata[gotocdata(selected_caddress[:-1]+[2*Basic], session['c_sqepulse_structure'])]
			Qdata[i] = selectedata[gotocdata(selected_caddress[:-1]+[2*Basic+1], session['c_sqepulse_structure'])]    





	I, Q = 0, 0
	for i_prepeat in range(powa_repeat):
		r_powa = int(ipowa) * powa_repeat + i_prepeat # from the beginning position of repeating power
		I += selectedata[gotocdata([x,y,int(ixyfreq),int(ixypowa),int(isparam),int(iifb),int(ifreq),2*r_powa],c_cwsweep_structure)]
		Q += selectedata[gotocdata([x,y,int(ixyfreq),int(ixypowa),int(isparam),int(iifb),int(ifreq),2*r_powa+1],c_cwsweep_structure)]
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
	


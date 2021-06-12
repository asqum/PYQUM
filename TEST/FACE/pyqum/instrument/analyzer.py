'''For analyzing data'''

# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color

from time import time
from numpy import ones, convolve, log10, sqrt, arctan2, diff, array, unwrap, gradient, mean
from scipy.fftpack import rfft, rfftfreq, irfft
from sklearn.preprocessing import minmax_scale
import matplotlib.pyplot as plt

# homemade modules
import qspp.digital_homodyne as sa_dh
import qspp.core as sa_core
from pyqum.instrument.toolbox import gotocdata
# from pyqum.instrument.booster import cuda_streamean

# curve display
def curve(x, y, title, xlabel, ylabel, xscal='linear', yscal='linear', basx=10, basy=2, style="-k"):
	fig, ax = plt.subplots(1, 1, sharex=True, sharey=False)
	ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
	ax.set_xscale(xscal, basex=basx)
	ax.set_yscale(yscal, basey=basy)
	if len(array(x).shape) == 1:
		ax.plot(x, y, style)
	elif len(array(x).shape) > 1:
		for x,y,s in zip(x,y,style):
			ax.plot(x, y, s)
	fig.tight_layout()
	plt.show()

# differentiation
def derivative(x, y, step=1):
	X, Y = x[::step], y[::step]
	dydx = diff(Y) / diff(X)
	return X[1::], dydx

# Extract IQ (to be changed to take in list instead of np.array)
def IQAP(I, Q):
	if I==0 and Q==0:
		Amp = -1000
		Pha = 0
	else:
		Amp = 20*log10(sqrt(I**2 + Q**2)) # I, Q is a ratio in this formula
		Pha = arctan2(Q, I) # -pi < phase < pi
	return Amp, Pha
def IQAParray(datas, interlace=True):
	'''
	datas: interlaced IQ (default) OR horizontally stacked IQ
	output: nd-array
	'''
	if interlace: IQdata = datas.reshape(len(datas)//2, 2) # sort out interlaced IQ-pairs into I-list & Q-list
	else: IQdata = datas
	Idata, Qdata = IQdata[:,0], IQdata[:,1]
	# yI, yQ = [float(i) for i in Idata], [float(i) for i in Qdata]
	Amp = 20*log10(sqrt(Idata**2 + Qdata**2)) # I, Q is a ratio in this formula
	Pha = arctan2(Qdata, Idata) # -pi < phase < pi

	return Idata, Qdata, Amp, Pha

# moving average
def smooth(y, box_pts):
	box = ones(box_pts)/box_pts
	y_smooth = convolve(y, box, mode='same')
	return y_smooth

def FFT_deNoise(y, dx, noise_level, noise_filter=0.1):
	w = rfft(y)
	f = rfftfreq(len(y), dx)
	spectrum = w**2
	cutoff = spectrum < (spectrum.max()*noise_level*noise_filter)
	w_clean = w.copy()
	w_clean[cutoff] = 0
	y_clean = irfft(w_clean)
	return f, spectrum, w_clean, y_clean

def UnwraPhase(X, Pha, Flatten=True, Normalized=True):
	'''unwrap, flatten & normalized'''
	UPHA = unwrap(Pha)
	if Flatten:
		UPHA = gradient(UPHA, X)
	if Normalized:
		UPHA = minmax_scale(UPHA)
	return UPHA
	
def cleantrace(V):
	'''take out repeating element(s) from a trace / list in a progressing manner.
	1. Please note that it is NOT removing duplicate(s) per se
	2. Intrusive: V will be modified directly by this method'''
	turn = 0
	order = [x for x in range(len(V))] # V's indexes
	if len(V) > 1:
		while turn < len(V) - 1:
			if V[turn] == V[turn+1]:
				V.pop(turn+1)
				order.pop(turn+1)
				# print(turn)
			else: 
				turn += 1        
		return order
	else: return order

# Pulse Response Sampler:
def pulseresp_sampler(srange, selected_caddress, selectedata, c_structure, datadensity, mode='A'):
	'''
	\nsrange: Active(Start), Active(End), [Relax(Start), Relax(End)]
	\nmode as follows: (The level of integration/average in emerging order: B(average first) -> A -> D -> C(average last))
	\nA. DRSMr: sqrt(square(mean(I_A)) + square(mean(Q_A))) - sqrt(square(mean(I_R)) + square(mean(Q_R)))
	\nB. RSDMr: 
	\nC. MON (pulswipe):
	\nD. RMS (poweroot):
	'''
	# tStart = time()

	# 1. Cropping Active Region:
	if [int(srange[1]) , int(srange[0])] > [c_structure[-1]//datadensity] * 2:
		print(Back.WHITE + Fore.RED + "Out of range")
	else:
		step = (int(srange[1]) - int(srange[0])) // abs(int(srange[1]) - int(srange[0]))
		active_len = abs(int(srange[1]) - int(srange[0]) + step)
		# 1. ACTIVE Region of the Pulse Response:
		# FASTEST PARALLEL VECTORIZATION OF BIG DATA BY NUMPY:
		# Assemble stacks of selected c-address for this sample range:
		selected_caddress_I = array([[int(s) for s in selected_caddress[:-1]] + [0]] * active_len)
		selected_caddress_Q = array([[int(s) for s in selected_caddress[:-1]] + [0]] * active_len)
		# sort-out interleaved IQ:
		selected_caddress_I[:,-1] = 2 * array(range(int(srange[0]),int(srange[1])+step,step))
		selected_caddress_Q[:,-1] = 2 * array(range(int(srange[0]),int(srange[1])+step,step)) + ones(active_len)
		# Compressing I- & Q-pulse of this sample range into just one point:
		# selectedata = array(selectedata)
		I_Pulse_active = selectedata[gotocdata(selected_caddress_I, c_structure)]
		Idata_active = mean(I_Pulse_active)
		Q_Pulse_active = selectedata[gotocdata(selected_caddress_Q, c_structure)]
		Qdata_active = mean(Q_Pulse_active)
		# print("Go to IQ-Pulsection in %ss" %(time()-tStart))
		if mode == 'C':
			A_Pulse_active = sqrt( I_Pulse_active**2 + Q_Pulse_active**2 )
			A_Pulse_active = A_Pulse_active/A_Pulse_active[0]
			Adata_active = mean(A_Pulse_active - A_Pulse_active[-1])
			P_Pulse_active = arctan2( Q_Pulse_active, I_Pulse_active )
			P_Pulse_active = P_Pulse_active/P_Pulse_active[0]
			Pdata_active = mean(P_Pulse_active - P_Pulse_active[-1])
		if mode == 'D':
			A_Pulse_active = I_Pulse_active**2 + Q_Pulse_active**2 # Power
			Adata_active = mean(A_Pulse_active)
			P_Pulse_active = arctan2( Q_Pulse_active, I_Pulse_active )
			Pdata_active = mean(P_Pulse_active)

		# 2. Cropping Relax Region (Optional):
		try:
			step = (int(srange[3]) - int(srange[2])) // abs(int(srange[3]) - int(srange[2]))
			relax_len = abs(int(srange[3]) - int(srange[2]) + step)
			# 2. RELAXED Region of the Pulse Response:
			# FASTEST PARALLEL VECTORIZATION OF BIG DATA BY NUMPY:
			# Assemble stacks of selected c-address for this sample range:
			selected_caddress_I = array([[int(s) for s in selected_caddress[:-1]] + [0]] * relax_len)
			selected_caddress_Q = array([[int(s) for s in selected_caddress[:-1]] + [0]] * relax_len)
			# sort-out interleaved IQ:
			selected_caddress_I[:,-1] = 2 * array(range(int(srange[2]),int(srange[3])+step,step))
			selected_caddress_Q[:,-1] = 2 * array(range(int(srange[2]),int(srange[3])+step,step)) + ones(relax_len)
			# Compressing I & Q of this sample range:
			# selectedata = array(selectedata)
			I_Pulse_relax = selectedata[gotocdata(selected_caddress_I, c_structure)]
			Idata_relax = mean(I_Pulse_relax)
			Q_Pulse_relax = selectedata[gotocdata(selected_caddress_Q, c_structure)]
			Qdata_relax = mean(Q_Pulse_relax)
			if mode == 'C':
				A_Pulse_relax = sqrt( I_Pulse_relax**2 + Q_Pulse_relax**2 )
				A_Pulse_relax = A_Pulse_relax/A_Pulse_relax[0]
				Adata_relax = mean(A_Pulse_relax - A_Pulse_relax[-1])
				P_Pulse_relax = arctan2( Q_Pulse_relax, I_Pulse_relax )
				P_Pulse_relax = P_Pulse_relax/P_Pulse_relax[0]
				Pdata_relax = mean(P_Pulse_relax - P_Pulse_relax[-1])
			if mode == 'D':
				A_Pulse_relax = I_Pulse_relax**2 + Q_Pulse_relax**2 # Power
				Adata_relax = mean(A_Pulse_relax)
				P_Pulse_relax = arctan2( Q_Pulse_relax, I_Pulse_relax )
				Pdata_relax = mean(P_Pulse_relax)
		except(IndexError): Idata_relax, Qdata_relax, Adata_relax, Pdata_relax = 0, 0, 0, 0

		# Independent IQ (Deviation)
		dIdata = Idata_active - Idata_relax
		dQdata = Qdata_active - Qdata_relax

		# Post-IQAP:
		# PENDING: VECTORIZE THIS:
		# A and B converge for only 2-range (differ for 4-range)
		if mode == 'A': # deviation of root square mean(range) (same as mean root square!)
			Adata = sqrt(Idata_active**2+Qdata_active**2) - sqrt(Idata_relax**2+Qdata_relax**2)
			Pdata = arctan2(Qdata_active, Idata_active) - arctan2(Qdata_relax, Idata_relax) # -pi < phase < pi
		elif mode == 'B': # root square deviation mean(range)
			Adata = sqrt(dIdata**2 + dQdata**2)
			Pdata = arctan2(dQdata, dIdata) # -pi < phase < pi
		elif mode == 'C': # mean offset normalize
			Adata = Adata_active - Adata_relax
			Pdata = Pdata_active - Pdata_relax
		elif mode == 'D': # RMS (Power-like)
			Adata = sqrt(Adata_active) - sqrt(Adata_relax)
			Pdata = Pdata_active - Pdata_relax
		
	# print("Pulse sampled in %ss" %(time()-tStart))
	return dIdata, dQdata, Adata, Pdata

def pulse_baseband(method, trace_I, trace_Q, rotation_compensate_MHz, ifreqcorrection_kHz, t0=0, dt=1):
	'''
	dt: digitizer-resolution in ns
	'''
	mixer_down = sa_core.IQMixer(1,0,(0,0)) # amplitude balance, quadrature skew, offsets (already taken care of by process_DownConversion)
	if method == "dual_digital_homodyne": processing_data = sa_dh.DualChannel(t0, dt, array([trace_I, trace_Q]))
	elif method == "i_digital_homodyne": processing_data = sa_dh.SingleChannel(t0, dt, array([trace_I]))
	elif method == "q_digital_homodyne": processing_data = sa_dh.SingleChannel(t0, dt, array([trace_Q]))
	
	try: 
		processing_data.process_DownConversion(rotation_compensate_MHz/1e3 + ifreqcorrection_kHz/1e6) # in GHz (ns timescale)
		if method == "dual_digital_homodyne": processing_data.process_LowPass(4,0.05)
	except: print(Fore.RED + "INVALID DH METHOD")

	trace_I = processing_data.signal[0]
	trace_Q = processing_data.signal[1]
	return (trace_I, trace_Q)

# Fitting



def test():
	x = [1,2,2,2,3,3,3,3,3,3,3.5,5,5,5,5,5,5,5,7,7,7,8,8,8,8,8,8,12,12,13,12,12,12,10,8,7,5,5,5,5,5,3]
	y = [1,2,2,2,3,3,3,3,3,3,3.5,5,5,5,5,5,5,5,7,7,7,8,8,8,8,8,8,12,12,13,12,12,12,10,8,7,5,5,5,5,5,3]
	print('x-before: %s' %x)
	order = cleantrace(x)
	print('x-after: %s' %x)
	ycleaned = [y[i] for i in order]
	print('order:\n%s\ny-cleaned:\n%s' %(order, ycleaned))
	return

# test()


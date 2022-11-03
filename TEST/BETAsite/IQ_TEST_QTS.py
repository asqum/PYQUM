import numpy as np 
import matplotlib.pyplot as plt

DATAPTS = 5001
def generate_signal(f, time_array, amp1, amp2,namp, phi1, phi2):
	"""
	Args:
	f : singal frequency
	time_array: corresponding time array
	amp1: amplitude for in phase data
	amp2: amplitidde for quardure data
	namp: noise amplitude
	phi1: phase shift for in phase data
	phi2: phase shift for quardure data
	for balanced operation amp1 = amp2, phi1 = phi2
	"""
	i_data = amp1*np. cos(2*np.pi*f*time_array + phi1)+ (np.random.rand(DATAPTS)-0.5)*namp
	q_data = amp2*np.sin(2*np.pi*f*time_array + phi2)+ (np.random.rand(DATAPTS)-0.5)*namp
	return np.array([i_data, q_data])

def rotation_matrix(f, t, corr_amp, corr_phase):
	omega = 2*np.pi*f # relative IF omega = freq(LO) - freq(RF)
	R = np.array([[np.cos(omega*t+corr_phase)/corr_amp, np.sin(omega*t)],[-np.sin(omega*t+corr_phase)/corr_amp, np.cos(omega*t)]]) 
	return R.transpose(2,0,1) 

def moveAvg(inputArray, intperiod):
	"""
	Args:
	inputArray: array needs to be moving averaged
	intperiod: moving average points
	"""
	csum = np.cumsum(inputArray)/intperiod
	output = np.append(csum[0:intperiod], csum[intperiod:]-csum[0:-intperiod])
	return output 


def single_channel(f, time_array, signal):
	"""
	function for single channel DDC
	Args:
	f: LO frequency in GHz
	time_array: corresponding time array
	signal: two colum array with I, Q data, only single[0] is used to analysis
	"""
	conv_array = generate_signal(f, time_array, 1, 1, 0, 0, 0)
	output = np.array([signal[0], signal[0]])*conv_array
	intperiod = int(1/f)# in the unit of ns
	i_out = moveAvg(output[0], intperiod)
	q_out = moveAvg(output[1], intperiod)
	i_square = i_out*i_out
	q_square = q_out*q_out
	total = np.sqrt(i_square+q_square)
	return i_out, q_out, total

def dual_channel(f, time_array, signal, corr_amp, corr_phase):
	"""
	function for dual channel DDC
	Args:
	f: LO frequency in GHz
	time_array: corresponding time array
	signal: two colum array with I, Q data
	corr_amp: amplitude correction term for ration matrix
	corr_phase:phase correction term for ration matrix
	"""
	R = rotation_matrix(f, time_array, corr_amp, corr_phase)
	test = signal.transpose().reshape(DATAPTS,2,1)
	out = R @ signal.transpose().reshape(DATAPTS,2,1)
	out = out.reshape(DATAPTS,2).transpose()
	i_square = out[0]*out[0]
	q_square = out[1]*out[1]
	total = np.sqrt(i_square+q_square)
	return out[0], out[1], total



if __name__ =="__main__":
	f = 0.01 # unit GHz
	intperiod = int(1/f)# in the unit of ns
	time_array = np.linspace(0, 5000, DATAPTS) # time unit: ns
	signal = generate_signal(f,time_array, 1, 1, 0,  np.pi/8,np.pi/8)
	i_out_single, q_out_single, total_single = single_channel(f, time_array, signal)
	i_out_dual, q_out_dual, total_dual = dual_channel(f, time_array, signal, 1 , 0)
	fig, ((ax1 , ax2, ax3), (ax4, ax5, ax6),(ax7, ax8, ax9)) = plt.subplots(nrows =3, ncols=3, figsize = (16,8), tight_layout = True)
	ax1.plot(i_out_single, label ="i")
	ax1.plot(q_out_single, label="q")
	ax1.plot(total_single, label ="total")
	ax1.title.set_text("no noise, blanced single ch output")
	ax2.plot(i_out_dual, label ="i")
	ax2.plot(q_out_dual, label="q")
	ax2.plot(total_dual, label ="total")
	ax2.title.set_text("no noise, blanced dual ch output")
	signal_uba = generate_signal(f,time_array, 1, 0.95, 0, np.pi/8,np.pi/8)
	i_uba_single, q_uba_single, total_uba_single = single_channel(f, time_array, signal_uba)
	i_uba_dual, q_uba_dual, total_uba_dual = dual_channel(f, time_array, signal_uba, 1 , 0)
	i_ubac_dual, q_ubac_dual, total_ubac_dual = dual_channel(f, time_array, signal_uba, 1.0526 , 0)
	i_uba_ave = moveAvg(i_uba_dual, intperiod)
	q_uba_ave = moveAvg(q_uba_dual, intperiod)
	t_uba_ave = moveAvg(total_uba_dual, intperiod)
	ax3.plot(i_uba_single, label ="i")
	ax3.plot(q_uba_single, label="q")
	ax3.plot(total_uba_single, label ="total")
	ax3.title.set_text("no noise, amplitude unbalnaced single ch output")
	ax4.plot(i_uba_dual, label ="i")
	ax4.plot(q_uba_dual, label="q")
	ax4.plot(total_uba_dual, label ="total")
	ax4.plot(i_uba_ave, label ="i_ave")
	ax4.plot(q_uba_ave, label = "q_ave")
	ax4.plot(t_uba_ave, label="total_ave")
	ax4.title.set_text("no noise, amplitude unbalnaced dual ch output")
	ax5.plot(i_ubac_dual, label ="i")
	ax5.plot(q_ubac_dual, label="q")
	ax5.plot(total_ubac_dual, label ="total")
	ax5.title.set_text("no noise, amplitude unbalnaced dual ch output \n with rotation correction")
	signal_ubp = generate_signal(f,time_array, 1, 1, 0, np.pi/8 ,np.pi/8-0.1)
	# i_ubp_single, q_ubp_single, total_ubp_single = single_channel(f, time_array, signal_uba)
	i_ubp_dual, q_ubp_dual, total_ubp_dual = dual_channel(f, time_array, signal_ubp, 1 , 0)
	i_ubpc_dual, q_ubpc_dual, total_ubpc_dual = dual_channel(f, time_array, signal_ubp, 1 , -0.1)
	i_ubp_ave = moveAvg(i_ubp_dual, intperiod)
	q_ubp_ave = moveAvg(q_ubp_dual, intperiod)
	t_ubp_ave = moveAvg(total_ubp_dual, intperiod)
	ax6.plot(i_ubp_dual, label ="i")
	ax6.plot(q_ubp_dual, label="q")
	ax6.plot(total_ubp_dual, label ="total")
	ax6.plot(i_ubp_ave, label ="i_ave")
	ax6.plot(q_ubp_ave, label = "q_ave")
	ax6.plot(t_ubp_ave, label="total_ave")
	ax6.title.set_text("no noise, phase unbalnaced dual ch output")
	ax7.plot(i_ubpc_dual, label ="i")
	ax7.plot(q_ubpc_dual, label="q")
	ax7.plot(total_ubpc_dual, label ="total")
	ax7.title.set_text("no noise, phase unbalnaced dual ch output \n with rotation correction")
	signal_noise = generate_signal(f,time_array, 1, 1, 0.1, np.pi/8 ,np.pi/8)
	i_noise_single, q_noise_single, total_noise_single = single_channel(f, time_array, signal_noise)
	i_noise_dual, q_noise_dual, total_noise_dual = dual_channel(f, time_array, signal_noise, 1 , 0)
	i_ave = moveAvg(i_noise_dual, intperiod)
	q_ave = moveAvg(q_noise_dual, intperiod)
	t_ave = moveAvg(total_noise_dual, intperiod)
	ax8.plot(i_noise_single, label ="i")
	ax8.plot(q_noise_single, label="q")
	ax8.plot(total_noise_single, label ="total")
	ax8.title.set_text("noisy, balnaced single ch output")
	
	ax9.plot(i_noise_dual, label ="i")
	ax9.plot(q_noise_dual, label="q")
	ax9.plot(total_noise_dual, label ="total")
	ax9.plot(i_ave, label ="i_ave")
	ax9.plot(q_ave, label="q_ave")
	ax9.plot(t_ave, label ="total_ave")
	ax9.title.set_text("noisy, unbalnaced dual ch output")
	ax1.legend()
	ax2.legend()
	ax3.legend()
	ax4.legend()
	ax5.legend()
	ax6.legend()
	ax7.legend()
	ax8.legend()
	ax9.legend()
	plt.show()





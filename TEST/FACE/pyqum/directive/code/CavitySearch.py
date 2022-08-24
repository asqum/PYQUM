#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from numpy import array 
from scipy.signal import savgol_filter as SGF


# 1D array normalize method
def normalize_1d(ary):
	max = np.max(ary)
	min = np.min(ary)
	normalized = []
	for i in range(ary.shape[0]):
		normalized.append((ary[i]-min)/(max-min))
	return array(normalized)
    
# return the peak idx & expected eidth of a peak in the given dataframe
def peak_info(target_df,p2p):
    target_ary = array(target_df)
    slope = list(np.diff(target_ary))
  
    max_idx = slope.index(max(slope))               # <<<< assume the peak tip should always be in the prediction  window
    min_idx = slope.index(min(slope))           
    distance = abs(max_idx - min_idx)
  
    if distance*p2p < 0.03:       # determine whole peak or not 
        if max_idx > min_idx :      # find the location of the tip of the peak
            loc_idx = min_idx + int(distance/2) + 1
            return loc_idx,distance
        else:
            loc_idx = max_idx + int(distance/2) + 1
            return loc_idx,distance
    else:
        if max_idx > min_idx :
            loc_idx = min_idx + int(distance/2) + 1
            return loc_idx,int(distance*2)
        else:
            loc_idx = max_idx + int(distance/2) + 1
            return loc_idx,int(distance*2)

# give the frequency return a frame where the peak (weather true or not) located in the center
def corr_peak_loc(df_start,df_end,origin_fig,p2p):

    freq = origin_fig["Frequency"]

    target_pha_df = origin_fig[freq.between(df_start,df_end)]['UPhase']   # plot true[1]
    target_amp_df = origin_fig[freq.between(df_start,df_end)]['Amplitude'] 
    target_freq_df = origin_fig[freq.between(df_start,df_end)]['Frequency']
    target = pd.concat([target_freq_df,target_amp_df,target_pha_df],axis=1)

    tip_loc_pha, _ = peak_info(target_pha_df,p2p)
    tip_loc_amp, _ = peak_info(target_amp_df,p2p)

    tip_freq_pha = array(target)[tip_loc_pha][0]
    tip_freq_amp = array(target)[tip_loc_amp][0]
    
    
    window_info_amp = {'start':tip_freq_amp-float(30/2000),'end':tip_freq_amp+float(30/2000)}
    window_info_pha = {'start':tip_freq_pha-float(30/2000),'end':tip_freq_pha+float(30/2000)}

    return window_info_amp, window_info_pha

def compu_peak_center_dist(freq_1,freq_2,compa_fig,p2p):
    df_1 = compa_fig[compa_fig['Frequency'].between(freq_1-0.015,freq_1+0.015)]
    df_2 = compa_fig[compa_fig['Frequency'].between(freq_2-0.015,freq_2+0.015)]
    
    l = [df_1['Amplitude'],df_2['Amplitude'],df_1['UPhase'],df_2['UPhase']]
    score = {'freq_1':0,'freq_2':0}
    for substrate in l:
        loc_idx ,_ = peak_info(substrate,p2p)
        for target_freq in [array(df_1['Frequency'])[loc_idx],array(df_2['Frequency'])[loc_idx]]:
            if abs(freq_1-target_freq) < abs(freq_2-target_freq):
                score['freq_1']+=1
            else:
                score['freq_2']+=1
    if score['freq_1']>score['freq_2']:
        return freq_1
    else:
        return freq_2
    
def poopoo_filter(freq_ary,compa_fig):
    filtered=[]
    for freq in freq_ary:
        window_op_freq = freq - 0.015   # set window width ~ 30MHz
        window_ed_freq = freq + 0.015
        amp = array(compa_fig[compa_fig['Frequency'].between(window_op_freq,window_ed_freq)]['Amplitude'])
        pha = array(compa_fig[compa_fig['Frequency'].between(window_op_freq,window_ed_freq)]['UPhase'])
        score = 0
        for i in [amp,pha]:
            median = np.median(i)
            min_max_mid = 0.5*(np.max(i)+np.min(i))
            sd = 1*np.std(i)
            if median-sd<min_max_mid<median+sd:
                score += 1
        if score != 2:
            filtered.append(freq)
            
    return array(filtered)
        

# remove the empty list from a given array
def rm_empty(ary):
    ret = []
    for i in ary:
        if array(i).size != 0:
            ret.append(i)
    return array(list(set(ret)))


def gaus(x, a, mu, sig,c):
    return a*np.exp(-(x-mu)**2/(2*sig**2))+c


def gaussian_fitor(x,y,mode):
    true = 0
    if mode == 'amp':
        a = np.min(y)-np.max(y)
    else:
        a = np.max(y)-np.min(y)
    #median = array([np.median(y)]*x.shape[0]) 
    #mu = sum(x*(y-median))/sum(y-median)
    mu = sum(x*abs(y))/sum(abs(y))

    sig = 0.0001
    c = np.average(y)
    #try :
    popt,_ = curve_fit(gaus,x,y,p0=[a,mu,sig,c], maxfev=500000)
    fitted_gaussian = gaus(x,*popt)
    std = 2*np.std(y)
    if mode == 'amp':
        condi = ( -5e-3 < popt[2] < 5e-3 and popt[2] != 0)
    else:
        condi = ( -1e-3 < popt[2] < 1e-3 and popt[2] != 0)

    if condi :
        if np.max(fitted_gaussian) > (popt[3]+std) or np.min(fitted_gaussian) < (popt[3]-std):
            true += 1

    return true, popt, std

    #except:
        #return 0,[],0

def gaussian_filter(seq,origin_fig,p2p):  # true : [[no., start_freq, end_freq],[...],...]

    seq_start = seq[0]
    seq_end = seq[1]
  # contract the values between the given frequency range 
    amp_window_info, pha_window_info = corr_peak_loc(seq_start,seq_end,origin_fig,p2p) #50MHz window width
    
    freq_seq_amp= origin_fig[origin_fig['Frequency'].between(amp_window_info['start'],amp_window_info['end'])]['Frequency']
    freq_seq_pha= origin_fig[origin_fig['Frequency'].between(pha_window_info['start'],pha_window_info['end'])]['Frequency']
    amp_seq = origin_fig[origin_fig['Frequency'].between(amp_window_info['start'],amp_window_info['end'])]['Amplitude']
    pha_seq = origin_fig[origin_fig['Frequency'].between(pha_window_info['start'],pha_window_info['end'])]['UPhase']
    

  # gaussian fiting
    amp_true, _, _ = gaussian_fitor(freq_seq_amp,amp_seq,'amp')
    pha_true, _, _ = gaussian_fitor(freq_seq_pha,pha_seq,'pha')
   
    if amp_true == 1 or pha_true == 1:
        peak_loc = []
        for i in [amp_seq,pha_seq]:
            diff = list(np.diff(i))
            max_idx = diff.index(max(diff))
            min_idx = diff.index(min(diff))
            if max_idx > min_idx:
                peak_loc.append(min_idx+int(0.5*(max_idx-min_idx)))
            else:
                peak_loc.append(max_idx+int(0.5*(min_idx-max_idx)))
            
        peak_freq_amp = array(freq_seq_amp)[peak_loc[0]]
        peak_freq_pha = array(freq_seq_pha)[peak_loc[1]]
        
        return  peak_freq_amp, peak_freq_pha
    else:
        return [],[]


# compare with each other in different array, difference within 10MHz seem to be the same prediction
def amp_pha_compa(amp_loc_array,pha_loc_array):
    amp_loc_array = list(amp_loc_array)
    pha_loc_array = list(pha_loc_array)
    for amp_peak in amp_loc_array:
        for pha_peak in pha_loc_array: 
            if abs(amp_peak - pha_peak)<0.01:
                pha_loc_array.remove(pha_peak)

    if len(pha_loc_array) != 0:
        return array(amp_loc_array.extend(pha_loc_array))
    else:
        return array(amp_loc_array)
    


def ena_clutch_filter(freq_list):
    clutch_freq_maybe = np.arange(6.5,8,0.5)  #[6.5, 7, 7.5]
    to_remove = []
    for freq in freq_list:
        for clutch in clutch_freq_maybe:
            if abs(freq-clutch) <= 0.0011:
                to_remove.append(freq)
    for i in to_remove :
        freq_list.remove(i)
   
    return array(freq_list)


class CavitySearch:
    def __init__(self,dataframe):
        self.df = dataframe
        self.info = {}
        self.peak_amp, self.peak_pha = [], []
        self.sliced_freq = []
        self.final_answer = []
        # data pre-smooth : Savitzky-Golay filter
        self.SGF_width = 11
        self.polyorder = 1
        
    
    def make_amp_uph_from_IQ(self):
        df = self.df[self.df['Frequency'].between(4,8)]
        freq = array(df['Frequency'])
        I = array(df['I'])
        Q = array(df['Q'])
        amplitude = normalize_1d(20*np.log10((I**2+Q**2)**(1/2)))
        phase = np.diff(np.unwrap(np.arctan2(Q,I)))
        uphase = normalize_1d(np.hstack((phase,np.average(phase))))
        
        amplitude -= SGF(amplitude,self.SGF_width,self.polyorder)
        uphase -= SGF(uphase,self.SGF_width,self.polyorder)
        
        p2p = (freq[-1]-freq[0])/freq.shape[0]

        compa_fig = pd.concat([pd.Series(freq),pd.Series(amplitude),pd.Series(uphase)],axis=1) 
        compa_fig.columns = ['Frequency','Amplitude','UPhase']

        self.info = {"Frequency":freq,"Amplitude":amplitude,"UPhase":uphase,"p2p_freq":p2p,"Comparison_fig":compa_fig}
        
    def strong_slice(self):
        freq_shifted = [] 
        freq_sliced = []    #[[freq_st,freq_ed],[...],...]
        range_point = int(0.03/self.info['p2p_freq'])
        for i in range(0,self.info['Frequency'].shape[0]-range_point,range_point):
            freq_sliced.append([array(self.info['Frequency'][i:i+range_point])[0],array(self.info['Frequency'][i:i+range_point])[-1]])

            sliced_amp = array(self.info['Amplitude'][i:i+range_point])
            sliced_pha = array(self.info['UPhase'][i:i+range_point])
            min_max_mid_amp = 0.5*(np.max(sliced_amp)+np.min(sliced_amp))
            median_amp = np.median(sliced_amp)
            sd_amp = np.std(sliced_amp)
            min_max_mid_pha = 0.5*(np.max(sliced_pha)+np.min(sliced_pha))
            median_pha = np.median(sliced_pha)
            sd_pha = np.std(sliced_pha)
            condi_amp = (median_amp-sd_amp > min_max_mid_amp or min_max_mid_amp > median_amp+sd_amp)
            condi_pha = (median_pha-sd_pha > min_max_mid_pha or min_max_mid_pha > median_pha+sd_pha)

            if  condi_amp or condi_pha :
                if i != 0 or i != (self.info['Frequency'].shape[0]-range_point):
                    if abs(sliced_amp[0]-median_amp) > abs(0.34*(np.max(sliced_amp)-np.min(sliced_amp))) or  abs(sliced_pha[0]-median_pha) > abs(0.34*(np.max(sliced_pha)+np.min(sliced_pha))):
                        freq_shifted.append([array(self.info['Frequency'][i-int(range_point/2):i-int(range_point/2)+range_point])[0],array(self.info['Frequency'][i-int(range_point/2):i-int(range_point/2)+range_point])[-1]])

                    if abs(sliced_amp[-1]-median_amp) > abs(0.34*(np.max(sliced_amp)-np.min(sliced_amp))) or  abs(sliced_pha[-1]-median_pha) > abs(0.34*(np.max(sliced_pha)+np.min(sliced_pha))):
                        freq_shifted.append([array(self.info['Frequency'][i+int(range_point/2):i+int(range_point/2)+range_point])[0],array(self.info['Frequency'][i+int(range_point/2):i+int(range_point/2)+range_point])[-1]])
        
        freq_sliced.extend(freq_shifted)
        self.sliced_freq = array(freq_sliced) 
        
    def give_region(self):
        region = {}
    
        for tip_freq in self.final_answer: 
            freq = self.info['Comparison_fig'][self.info['Comparison_fig']['Frequency'].between(tip_freq-0.015,tip_freq+0.015)]['Frequency']
            amp = self.info['Comparison_fig'][self.info['Comparison_fig']['Frequency'].between(tip_freq-0.015,tip_freq+0.015)]['Amplitude']
            pha = self.info['Comparison_fig'][self.info['Comparison_fig']['Frequency'].between(tip_freq-0.015,tip_freq+0.015)]['UPhase']
            
            amp_tip_idx,FWHM_amp = peak_info(amp,self.info['p2p_freq'])  # unit: GHz
            pha_tip_idx,FWHM_pha = peak_info(pha,self.info['p2p_freq'])
            avg_tip_idx = 0.5*(array(freq)[amp_tip_idx]+array(freq)[pha_tip_idx])
            avg_FWHM = 0.5*(FWHM_amp*self.info['p2p_freq']+FWHM_pha*self.info['p2p_freq'])
            region['%d MHz'%(avg_tip_idx*1000)] = [tip_freq-4*avg_FWHM,tip_freq+4*avg_FWHM]

        self.final_answer = region  #{'5487 MHz':[freq_start,freq_end],'... MHz':[...],....}
        
    def amp_pha_compa(self):
        amp_loc_array = list(self.peak_amp)
        pha_loc_array = list(self.peak_pha)
        nearest = []
        for amp_peak in amp_loc_array:
            for pha_peak in pha_loc_array: 
                if abs(amp_peak - pha_peak)<0.01:
                    near_center_freq = compu_peak_center_dist(amp_peak,pha_peak,self.info['Comparison_fig'],self.info['p2p_freq'])
                    nearest.append(near_center_freq)
                
        self.final_answer = ena_clutch_filter(list(set(poopoo_filter(array(nearest),self.info['Comparison_fig']))))    # 1D array contain tip freq [freq1,freq2,...]
          
    # to call below do analysis                     
    def do_analysis(self): 
        self.make_amp_uph_from_IQ()
        self.strong_slice()
        gaussian_exist = {"peak_freq_amp":[],"peak_freq_pha":[]}
        for i in range(self.sliced_freq.shape[0]):
            peak_amp, peak_pha =  gaussian_filter(self.sliced_freq[i],self.info['Comparison_fig'],self.info['p2p_freq'])

            gaussian_exist['peak_freq_amp'].append(peak_amp)
            gaussian_exist['peak_freq_pha'].append(peak_pha)

        self.peak_amp = rm_empty(gaussian_exist["peak_freq_amp"])
        self.peak_pha = rm_empty(gaussian_exist["peak_freq_pha"])
        self.amp_pha_compa()
        self.give_region()
        
    #to call below send arrays to js plotly            
    def give_js_info(self,freq_MHz):
        self.ans_array = {
        'Frequency':array(self.info['Comparison_fig'][self.info['Comparison_fig']['Frequency'].between(self.answer['%d MHz'%freq_MHz][0],self.answer['%d MHz'%freq_MHz][1])]['Frequency']),
        'Amplitude':array(self.info['Comparison_fig'][self.info['Comparison_fig']['Frequency'].between(self.answer['%d MHz'%freq_MHz][0],self.answer['%d MHz'%freq_MHz][1])]['Amplitude']),
        'UPhase':array(self.info['Comparison_fig'][self.info['Comparison_fig']['Frequency'].between(self.answer['%d MHz'%freq_MHz][0],self.answer['%d MHz'%freq_MHz][1])]['UPhase'])
        }
            
            
  


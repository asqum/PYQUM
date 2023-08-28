# This file is central algorithm for calibration. 

from numpy import array, linspace, pi
from scipy.optimize import curve_fit
# IQparams = array([Ioffset, Qoffset, Qamp/Iamp, Iphase, Qphase])
# leakage_freq = [LO_freq, MR_freq]

def find_minimum(x,y):
    popt, pcov = curve_fit(
        f=target_function,         # model function
        xdata=x,    # x data
        ydata=y,     # y data
        p0=(1,1,1),    # initial value of the parameters
    )
    minimum = -popt[1]/2/popt[0]
    return minimum

def calibration(SA, mxa, leakage_freq, Conv_freq, IQparams, DAC, daca):
    step_rate = 0.9
    count = 0
    Iamp, Qamp = 1, 1
    Ioffset, Qoffset = IQparams[0], IQparams[1]
    print('MR:%s'%{SA.mark_power(mxa, leakage_freq[1])[0]})
    print('Conv:%s'%{SA.mark_power(mxa, Conv_freq)[0]})
    if SA.mark_power(mxa, leakage_freq[1])[0] > SA.mark_power(mxa, Conv_freq)[0]:
        start_point = 90
        print('A'*10)
    elif SA.mark_power(mxa, leakage_freq[1])[0] < SA.mark_power(mxa, Conv_freq)[0]:
        start_point = -90
        print('B'*10)
    low_phai_bound, high_phai_bound = start_point-30, start_point+30
    low_a_bound, high_a_bound = 0.1, 1.5
    low_offsetI_bound, high_offsetI_bound = -1, 1
    low_offsetQ_bound, high_offsetQ_bound = -1, 1
    while(1):
        Phai = linspace(low_phai_bound, high_phai_bound, 5)
        mirror = []
        for phai_IQ in Phai:
            IQparams = array([Ioffset, Qoffset, Qamp/Iamp, 0, phai_IQ])
            pulsettings = Update_DAC(daca, IF_freq, IQparams, IF_period, IF_scale, mixer_module, channels_group, iqcal_config[mode]['marker'])
            signal = SA.mark_power(mxa, leakage_freq[1])[0]
            mirror.append(signal)
        phai_IQ = find_minimum(Phai,mirror)
        # Choose phai_IQ as center and decrease point choose with range (-0.5*step_rate**i, 0.5*step_rate**i)
        low_phai_bound, high_phai_bound = phai_IQ-45*step_rate**count, phai_IQ+45*step_rate**count

        A_IQ = np.linspace(low_a_bound, high_a_bound, 5)
        mirror = []
        for a_IQ in A_IQ:
            IQparams = array([Ioffset, Qoffset, a_IQ, 0, phai_IQ])
            pulsettings = Update_DAC(daca, IF_freq, IQparams, IF_period, IF_scale, mixer_module, channels_group, iqcal_config[mode]['marker'])
            signal = SA.mark_power(mxa, leakage_freq[1])[0]
            mirror.append(signal)
        a_IQ = find_minimum(A_IQ,mirror)
        # Decrease bound with the range 
        low_a_bound, high_a_bound = a_IQ-1.4*step_rate**count, a_IQ+1.4*step_rate**count
        # Criterion of when the loop will stop
        if SA.mark_power(mxa, leakage_freq[1])[0] < SA.mark_power(mxa, Conv_freq)[0]-40 or count >= 10:
            break
        count += 1
    
    count = 0    
    while(1):
        Offset_I = np.linspace(low_offsetI_bound, high_offsetI_bound, 5)
        leakage = []
        for offset_I in Offset_I:
            IQparams = array([offset_I, Qoffset, a_IQ, 0, phai_IQ])
            pulsettings = Update_DAC(daca, IF_freq, IQparams, IF_period, IF_scale, mixer_module, channels_group, iqcal_config[mode]['marker'])
            signal = SA.mark_power(mxa, leakage_freq[0])[0]
            leakage.append(signal)
        offset_I = find_minimum(Offset_I,leakage)
        # Decrease the range 
        low_offsetI_bound, high_offsetI_bound = offset_I-2*step_rate**count, offset_I+2*step_rate**count

        Offset_Q = np.linspace(low_offsetQ_bound, high_offsetQ_bound, 5)
        leakage = []
        for offset_Q in Offset_Q:
            IQparams = array([offset_I, offset_Q, a_IQ, 0, phai_IQ])
            pulsettings = Update_DAC(daca, IF_freq, IQparams, IF_period, IF_scale, mixer_module, channels_group, iqcal_config[mode]['marker'])
            signal = SA.mark_power(mxa, leakage_freq[0])[0]
            leakage.append(signal)
        offset_Q = find_minimum(Offset_Q,leakage)
        # Decrease the range 
        low_offsetQ_bound, high_offsetQ_bound = offset_Q-2*step_rate**count, offset_Q+2*step_rate**count
        if SA.mark_power(mxa, leakage_freq[0])[0] < SA.mark_power(mxa, Conv_freq)[0]-40 or count >= 10:
            break
        count += 1
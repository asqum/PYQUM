"""
Created on Wed Jan 15 11:17:10 2020
@author: mesch
"""

import copy
from pyqum.instrument.benchtop import RSA5, PSGA
from pyqum.instrument.modular import AWG
from pyqum.instrument.logger import status_code
from numpy import sin, cos, pi, array, lcm, float64

# print('lcm of 12 ad 10 is %s' %lcm(12,10))

# Initialize instruments:
# PSGA
saga = PSGA.Initiate()
PSGA.rfoutput(saga, action=['Set', 1])
PSGA.frequency(saga, action=['Set', "5.5" + "GHz"])
PSGA.power(saga, action=['Set', "0" + "dBm"])
# Rigol SA
rsa = RSA5.Initiate()
RSA5.frequency(rsa, action=['Set','5.525GHz'])
RSA5.fspan(rsa, action=['Set','150MHz'])
RSA5.rbw(rsa, action=['Set','1MHz'])
RSA5.vbw(rsa, action=['Set','100kHz'])
# AWG
awgsess = AWG.InitWithOptions()
AWG.Abort_Gen(awgsess)
AWG.ref_clock_source(awgsess, action=['Set',int(1)]) # External 10MHz clock-reference
AWG.predistortion_enabled(awgsess, action=['Set',True])
AWG.output_mode_adv(awgsess, action=['Set',int(2)]) # Sequence output mode
AWG.arb_sample_rate(awgsess, action=['Set',float(1250000000)]) # maximum sampling rate
AWG.active_marker(awgsess, action=['Set','1']) # master
AWG.marker_delay(awgsess, action=['Set',float(0)])
AWG.marker_pulse_width(awgsess, action=['Set',float(1e-7)])
AWG.marker_source(awgsess, action=['Set',int(7)])
samplingrate = AWG.arb_sample_rate(awgsess)[1]
dt = 1e9/samplingrate # in ns
# PRESET Output:
for ch in range(2):
    channel = str(ch + 1)
    AWG.output_config(awgsess, RepCap=channel, action=["Set", 0]) # Single-ended
    AWG.output_filter_bandwidth(awgsess, RepCap=channel, action=["Set", 0])
    AWG.arb_gain(awgsess, RepCap=channel, action=["Set", 0.5])
    AWG.output_impedance(awgsess, RepCap=channel, action=["Set", 50])
# output settings:
for ch in range(2):
    channel = str(ch + 1)
    AWG.output_enabled(awgsess, RepCap=channel, action=["Set", int(1)])  # ON
    AWG.output_filter_enabled(awgsess, RepCap=channel, action=["Set", True])
    AWG.output_config(awgsess, RepCap=channel, action=["Set", int(2)]) # Amplified 1:2
    AWG.output_filter_bandwidth(awgsess, RepCap=channel, action=["Set", 0])
    AWG.arb_gain(awgsess, RepCap=channel, action=["Set", 0.5])
    AWG.output_impedance(awgsess, RepCap=channel, action=["Set", 50])

def AWG_Sinewave(ifreq,Ioffset,Qoffset,Iamp,Qamp,Iphase,Qphase):
    '''
    ifreq: IF frequency in MHz
    '''

    AWG.Clear_ArbMemory(awgsess)
    WAVE = []
    ifvoltag = [min(abs(Qamp),1), min(abs(Iamp),1)] # contain amplitude within 1V
    iffunction = ['sin', 'cos']
    iffreq = [ifreq, ifreq]
    ifoffset = [Qoffset, Ioffset]
    ifphase = [Qphase, Iphase]

    # construct waveform:
    for ch in range(2):
        channel = str(ch + 1)

        Nperiod = lcm(round(1000/iffreq[ch]/dt*100),800)//100
        print("Waveform contains %s points per sequence" %Nperiod)
        wavefom = [ifvoltag[ch] * eval(iffunction[ch] + '(x*%s*%s/1000*2*pi + %s/180*pi)' %(dt,iffreq[ch],ifphase[ch])) + ifoffset[ch] for x in range(Nperiod)]

        stat, wave = AWG.CreateArbWaveform(awgsess, wavefom)
        # print('Waveform channel %s: %s <%s>' %(channel, wave, status_code(stat)))
        WAVE.append(wave)
    # Building Sequences:
    for ch in range(2):
        channel = str(ch + 1)	
        status, seqhandl = AWG.CreateArbSequence(awgsess, [WAVE[ch]], [1]) # loop# canbe >1 if longer sequence is needed in the future!
        # print('Sequence channel %s: %s <%s>' %(channel, seqhandl, status_code(status)))
        # Channel Assignment:
        stat = AWG.arb_sequence_handle(awgsess, RepCap=channel, action=["Set", seqhandl])
        # print('Sequence channel %s embeded: %s <%s>' %(channel, stat[1], status_code(stat[0])))
    # Trigger Settings:
    for ch in range(2):
        channel = str(ch + 1)
        AWG.operation_mode(awgsess, RepCap=channel, action=["Set", 0])
        AWG.trigger_source_adv(awgsess, RepCap=channel, action=["Set", 0])
    AWG.Init_Gen(awgsess)
    AWG.Send_Pulse(awgsess, 1)

    return


'''
    Pure Python/Numpy implementation of the Nelder-Mead algorithm.
    Reference: https://en.wikipedia.org/wiki/Nelder%E2%80%93Mead_method
'''
def nelder_mead(x_start,
                step=[-0.1,-0.1,0.1,-0.1,10,10], no_improve_thr=10e-6,
                no_improv_break=10, max_iter=0,
                alpha=1., gamma=2., rho=-0.5, sigma=0.5):
    '''
        @param f (function): function to optimize, must return a scalar score
            and operate over a numpy array of the same dimensions as x_start
        @param x_start (numpy array): initial position
        @param step (float): look-around radius in initial step
        @no_improv_thr,  no_improv_break (float, int): break after no_improv_break iterations with
            an improvement lower than no_improv_thr
        @max_iter (int): always break after this number of iterations.
            Set it to 0 to loop indefinitely.
        @alpha, gamma, rho, sigma (floats): parameters of the algorithm
            (see Wikipedia page for reference)
        return: tuple (best parameter array, best score)
    '''

    # init
    dim = len(x_start)
    "tell AWG to apply DC offset(x) on I & Q"
    AWG_Sinewave(25,x_start[0],x_start[1],x_start[2],x_start[3],x_start[4],x_start[5])

    "read signal amplitude at LO frequency in and assign it as score"
    LOpower = float((RSA5.fpower(rsa,'5.5GHz')).split('dBm')[0])
    Mrrpower = float((RSA5.fpower(rsa,'5.475GHz')).split('dBm')[0])
    prev_best = Mrrpower + 0
    no_improv = 0
    res = [[x_start, prev_best]]

    while True:
        print("LO Power: %s" %LOpower)
        print("Mirror Power: %s" %Mrrpower)
        if bool(input('hello')): break

    for i in range(dim):
        x = copy.copy(x_start)
        x[i] = x[i] + step[i]
        print('applying %s' %x)
        "tell AWG to apply DC offset(x) on I & Q"
        AWG_Sinewave(25,x[0],x[1],x[2],x[3],x[4],x[5])
        "read signal amplitude at LO frequency in and assign it as score"
        LOpower = float((RSA5.fpower(rsa,'5.5GHz')).split('dBm')[0])
        Mrrpower = float((RSA5.fpower(rsa,'5.475GHz')).split('dBm')[0])
        score = Mrrpower + 0
        res.append([x, score])

    # simplex iter
    iters = 0
    while 1:
        # order
        res.sort(key=lambda x: x[1])
        best = res[0][1]

        # break after max_iter
        if max_iter and iters >= max_iter:
            return res[0]
        iters += 1

        # break after no_improv_break iterations with no improvement
        print('...best so far:', best)

        if best < prev_best - no_improve_thr:
            no_improv = 0
            prev_best = best
        else:
            no_improv += 1

        if no_improv >= no_improv_break:
            print("Rest at Optimized IQ Settings: %s" %res[0][0])
            AWG_Sinewave(25,res[0][0][0],res[0][0][1],res[0][0][2],res[0][0][3],res[0][0][4],res[0][0][5])
            return res[0] # Optimized parameters

        # centroid
        x0 = [0.] * dim
        for tup in res[:-1]:
            for i, c in enumerate(tup[0]):
                x0[i] += c / (len(res)-1)

        # reflection
        xr = x0 + alpha*(x0 - res[-1][0])
        "tell AWG to apply DC offset(x) on I & Q"
        AWG_Sinewave(25,xr[0],xr[1],xr[2],xr[3],xr[4],xr[5])

        "read signal amplitude at LO frequency in and assign it as score"
        LOpower = float((RSA5.fpower(rsa,'5.5GHz')).split('dBm')[0])
        Mrrpower = float((RSA5.fpower(rsa,'5.475GHz')).split('dBm')[0])
        rscore = Mrrpower + 0
        if res[0][1] <= rscore < res[-2][1]:
            del res[-1]
            res.append([xr, rscore])
            continue

        # expansion
        if rscore < res[0][1]:
            xe = x0 + gamma*(x0 - res[-1][0])
            "tell AWG to apply DC offset(x) on I & Q"
            AWG_Sinewave(25,xe[0],xe[1],xe[2],xe[3],xe[4],xe[5])

            "read signal amplitude at LO frequency in and assign it as score"
            LOpower = float((RSA5.fpower(rsa,'5.5GHz')).split('dBm')[0])
            Mrrpower = float((RSA5.fpower(rsa,'5.475GHz')).split('dBm')[0])
            escore = Mrrpower + 0
            if escore < rscore:
                del res[-1]
                res.append([xe, escore])
                continue
            else:
                del res[-1]
                res.append([xr, rscore])
                continue

        # contraction
        xc = x0 + rho*(x0 - res[-1][0])
        "tell AWG to apply DC offset(x) on I & Q"
        AWG_Sinewave(25,xc[0],xc[1],xc[2],xc[3],xc[4],xc[5])

        "read signal amplitude at LO frequency in and assign it as score"
        LOpower = float((RSA5.fpower(rsa,'5.5GHz')).split('dBm')[0])
        Mrrpower = float((RSA5.fpower(rsa,'5.475GHz')).split('dBm')[0])
        cscore = Mrrpower + 0
        if cscore < res[-1][1]:
            del res[-1]
            res.append([xc, cscore])
            continue

        # reduction
        x1 = res[0][0]
        nres = []
        for tup in res:
            redx = x1 + sigma*(tup[0] - x1)
            "tell AWG to apply DC offset(x) on I & Q"
            AWG_Sinewave(25,redx[0],redx[1],redx[2],redx[3],redx[4],redx[5])

            "read signal amplitude at LO frequency in and assign it as score"
            LOpower = float((RSA5.fpower(rsa,'5.5GHz')).split('dBm')[0])
            Mrrpower = float((RSA5.fpower(rsa,'5.475GHz')).split('dBm')[0])
            score = Mrrpower + 0
            nres.append([redx, score])
        res = nres


if __name__ == "__main__":
    # test
#    import math
    from scipy.optimize import rosen 

#    def f(x):
#        return math.sin(x[0]) * math.cos(x[1]) * (1. / (abs(x[2]) + 1))

    # Initial = [0, 0, -1, 1, 0, 0]
    Initial = [0.018, -0.022, 0.707, -1, -7.1, 0] # manual mirror minimized
    # Initial = [-0.00199462, -0.04195287,  0.97458273,  1.01026642, -0.02495974, -0.02041564]
    # Initial = [-0.00199462, -0.04195287,  0.97458273,  1.01026642, -0.02495974, -0.02041564] # The Best
    print("Optimized IQ parameters:\n %s" %nelder_mead(array(Initial,dtype=float64)))


# closing instruments:
ans = input("Press any keys to close AWG, PSGA and RSA-5 ")
AWG.Abort_Gen(awgsess)
AWG.close(awgsess)
PSGA.rfoutput(saga, action=['Set', 0])
PSGA.close(saga, False)
RSA5.close(rsa,False)



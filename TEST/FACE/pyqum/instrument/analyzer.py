'''For analyzing data'''

from numpy import ones, convolve, log10, sqrt, arctan2, diff, array, unwrap, gradient
from scipy.fftpack import rfft, rfftfreq, irfft
from sklearn.preprocessing import minmax_scale

import matplotlib.pyplot as plt

# curve display
def curve(x, y, title, xlabel, ylabel, style="-k"):
    fig, ax = plt.subplots(1, 1, sharex=True, sharey=False)
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
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
        Amp = 20*log10(sqrt(I**2 + Q**2))
        Pha = arctan2(Q, I) # -pi < phase < pi
    return Amp, Pha
def IQAParray(datas): # datas
    '''
    Slice datas-array into IQ-data, then list the Amp (dB/dBm) & Pha (rad) out of it
    '''
    IQdata = datas.reshape(len(datas)//2, 2) # sort out interlaced IQ-pairs into I-list & Q-list
    Idata, Qdata = IQdata[:,0], IQdata[:,1]
    yI, yQ = [float(i) for i in Idata], [float(i) for i in Qdata]
    Amp, Pha = [], []
    for I, Q in zip(yI, yQ):
        if I==0 and Q==0:
            Amp.append(-1000)
            Pha.append(0)
        else:
            Amp.append(20*log10(sqrt(I**2 + Q**2)))
            Pha.append(arctan2(Q, I)) # -pi < phase < pi
    return yI, yQ, Amp, Pha

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


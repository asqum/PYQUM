'''For analyzing data'''
from numpy import ones, convolve, log10, sqrt, arctan2, diff, array
from scipy.fftpack import rfft, rfftfreq, irfft

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
def IQAP(datas):
    # Slicing datas into IQ-data
    IQdata = datas.reshape(len(datas)/2, 2)
    Idata, Qdata = IQdata[:,0], IQdata[:,1]
    yI, yQ = [float(i) for i in Idata], [float(i) for i in Qdata]
    Amp, Pha = [], []
    for i in zip(yI, yQ):
        Amp.append(20*log10(sqrt(i[0]**2 + i[1]**2)))
        Pha.append(arctan2(i[1], i[0])) # -pi < phase < pi
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


def test():

    return
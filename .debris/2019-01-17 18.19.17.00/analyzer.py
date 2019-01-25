'''For analyzing data'''
from numpy import ones, convolve, log10, sqrt, arctan2
from scipy.fftpack import rfft, rfftfreq, irfft

# Extract IQ
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
    wselected = w.copy()
    wselected[cutoff] = 0
    y_clean = irfft(wselected)
    return f, spectrum, wselected, y_clean

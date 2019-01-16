from pyqum.instrument.logger import get_data, search_allpaths, goto_siblings
from numpy import arange, sqrt, arctan2, array, linspace, pi, log10, reshape, unwrap, gradient, ones, convolve
from statistics import median, mean
from scipy.fftpack import rfft, rfftfreq, irfft
import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale
from peakutils import indexes

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
    w2 = w.copy()
    w2[cutoff] = 0
    y_clean = irfft(w2)
    return f, spectrum, y_clean

USR = get_data("LTH")

p = search_allpaths(USR, 'NCHUQ_S21')
selectedP = p[8]
print("The path [%s] gives: " %selectedP)
data_sib = goto_siblings(USR, selectedP)
print("This data has these keys: %s" %data_sib.keys())

X = data_sib['X']
yI = data_sib['yI']
yQ = data_sib['yQ']
Amp = data_sib['Amp']
Pha = data_sib['Pha']

Mname = data_sib['Sdata']
fcenter = median(X)

# Plotting
def plotdata():
    fig, ax = plt.subplots(2, 2, sharex=True, sharey=False)
    fig.suptitle("%s-measurement: I, Q, Amplitude & Phase"%Mname, fontsize=16) # global title
    ax[0, 0].plot(X, yI)
    ax[0, 0].set(ylabel=r'I-Data (V)') #title=""
    ax[0, 1].plot(X, yQ)
    ax[0, 1].set(ylabel=r'Q-Data (V)')
    ax[1, 0].scatter(X, Amp, s=12, c='k')
    ax[1, 0].set(ylabel=r'Amplitude (dB)')
    ax[1, 1].plot(X, Pha)
    ax[1, 1].set(ylabel=r'Phase (rad)')

    # universal settings:
    for row in ax:
        for eachaxes in row:
            eachaxes.grid(color='b', linestyle=':', linewidth=0.7)
    for eachaxes in ax[1, :]:
        eachaxes.set(xlabel=r'$frequency, {\omega}_r\ (f_{center}:\ {%.1e})$'%(fcenter))

    # # Fine-tune figure; hide x ticks for top plots and y ticks for right plots
    plt.setp([a.get_xticklabels() for a in ax[0, :]], visible=False)

    # Tight layout often produces nice results
    # but requires the title to be spaced accordingly
    fig.tight_layout()
    fig.subplots_adjust(top=0.88)

    plt.show()
    return

UPHA = unwrap(Pha)
avebox = int(len(X)/1000)
UPHA_smooth = smooth(UPHA, avebox)
UPHA_flat = gradient(UPHA_smooth, X)
UPHA_flat = minmax_scale(UPHA_flat)

f, spec, UPHA_fft = FFT_deNoise(UPHA_flat[avebox:-avebox]*1e8, X[1]-X[0], 0.0006)

indices = indexes(UPHA_fft, thres=0.02/max(UPHA_fft), min_dist=0.1)
X_peak = [X(i) for i in indices]
Y_peak = [UPHA_fft(i) for i in indices]

# Plot unwrapped phase 
fig, ax = plt.subplots()
ax.plot(X, UPHA)
ax.set(ylabel=r' unwrapped Phase (rad)', xlabel=r'$frequency (Hz)$',
        title='Unwrapped Phase')
ax.grid(linewidth=0.5)
plt.show()

# Plot derivative of unwrapped phase
fig, ax = plt.subplots()
ax.plot(X[avebox:-avebox], UPHA_flat[avebox:-avebox])
ax.set(ylabel=r' unwrapped Phase (rad)', xlabel=r'$frequency (Hz)$',
        title='Flatten Unwrapped Phase by Derivative')
ax.grid(linewidth=0.5)
plt.show()

# Smoothing by moving average (convolution)
fig, ax = plt.subplots()
ax.plot(X[avebox:-avebox], UPHA_smooth[avebox:-avebox])
ax.set(ylabel=r' unwrapped Phase (rad)', xlabel=r'$frequency (Hz)$',
        title='Smoothing by moving average')
ax.grid(linewidth=0.5)
plt.show()

# Filter out low-contributing noise by FFT
fig, ax = plt.subplots()
ax.plot(X[avebox:-avebox], UPHA_fft)
ax.plot(X_peak, Y_peak)
ax.set(ylabel=r' unwrapped Phase (rad)', xlabel=r'$frequency (Hz)$',
        title='Filter out low-contributing noise by FFT')
ax.grid(linewidth=0.5)
plt.show()

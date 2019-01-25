from pyqum.instrument.logger import get_data
from pyqum.instrument.reader import search_allpaths, goto_siblings, search_time
from pyqum.instrument.analyzer import smooth, FFT_deNoise
from numpy import arange, sqrt, arctan2, array, linspace, pi, log10, reshape, unwrap, gradient
from statistics import median, mean
import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale
from peakutils import indexes
from time import ctime
from datetime import datetime
from operator import itemgetter

USR = get_data("LTH")
p = search_allpaths(USR, 'NCHUQ_S21')

# Sorting paths based on time
nearest, selectedP = search_time(p, '2019 01 15')
print("The nearest being %s away in the path: %s" %(nearest, selectedP))

# selectedP = p[0]
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
avebox = max([1, int(len(X)/500)])
print("Box: %s" %avebox)
UPHA_smooth = smooth(UPHA, avebox)
UPHA_flat = gradient(UPHA_smooth, X)
UPHA_flat = minmax_scale(UPHA_flat)

f, spec, wsel, UPHA_fft = FFT_deNoise(UPHA_flat[avebox:-avebox]*1e8, X[1]-X[0], 0.00001)

# finding peak and dip
indices = indexes(UPHA_fft, thres=0.88, min_dist=0.1)
X_peak = [X[i] for i in indices]
Y_peak = [UPHA_fft[i] for i in indices]
indices = indexes(-1*UPHA_fft, thres=0.88, min_dist=0.1)
X_dip = [X[i] for i in indices]
Y_dip = [UPHA_fft[i] for i in indices]
xshift = mean([X_dip[0], X_peak[0]])
print("Peak: %s, Dip: %s, Shift: %s" %(X_peak, X_dip, xshift))
# deduce the in-between
ishift, shift = min(enumerate([abs(x-xshift) for x in X]), key=itemgetter(1))
X_shift = [X[ishift]]
Y_shfit = [UPHA_fft[ishift]]

# FIGURES
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
ax.plot(X_peak, Y_peak, marker='P', color='b', markersize=15, linestyle='')
ax.plot(X_dip, Y_dip, marker='P', color='r', markersize=15, linestyle='')
ax.plot(X_shift, Y_shfit, marker='P', color='g', markersize=15, linestyle='')
ax.set(ylabel=r' unwrapped Phase (rad)', xlabel=r'$frequency (Hz)$',
        title='Filter out low-contributing noise by FFT')
ax.grid(linewidth=0.5)
plt.show()


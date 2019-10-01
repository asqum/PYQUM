from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
from matplotlib import cm
from numpy import mean, array, meshgrid

from pyqum.instrument.toolbox import waveform, cdatasearch, gotocdata
from pyqum.instrument.analyzer import IQAP
from pyqum.directive.characterize import CW_Sweep

CORDER = {'Flux-Bias':'-0.005125 to 0.006263 *130', 'XY-Frequency':'4.85 to 4.95 *300', 'XY-Power':'-22',
            'S-Parameter':'S21,', 'IF-Bandwidth':'10', 'Frequency':'4.895932', 'Power':'-18  r 100'}

case = CW_Sweep('abc')
case.selectday(case.whichday())
m = case.whichmoment()
case.selectmoment(m)
print("File selected: %s" %case.pqfile)
case.accesstructure()
print("Data progress: %s%%" %case.data_progress)

# Scale-up optional parameters:
try: cfluxbias = waveform(case.corder['Flux-Bias'])
except(KeyError): cfluxbias = waveform('opt,') # create virtual list for the absence of this in older file
try: cxyfreq = waveform(case.corder['XY-Frequency'])
except(KeyError): cxyfreq = waveform('opt,') # create virtual list for the absence of this in older file
try: cxypowa = waveform(case.corder['XY-Power'])
except(KeyError): cxypowa = waveform('opt,') # create virtual list for the absence of this in older file
csparam = waveform(case.corder['S-Parameter'])
cifb = waveform(case.corder['IF-Bandwidth'])
cfreq = waveform(case.corder['Frequency'])
cpowa = waveform(case.corder['Power'])
cpowa_repeat = cpowa.inner_repeat
c_cwsweep_structure= [cfluxbias.count,cxyfreq.count,cxypowa.count,csparam.count,cifb.count,cfreq.count,cpowa.count*cpowa_repeat*case.datadensity]
c_cwsweep_address = cdatasearch(case.resumepoint-1, c_cwsweep_structure)

# loading data
case.loadata()
selectedata = case.selectedata

X = cxyfreq.data
Y = cfluxbias.data[7:38]
AMP, PHA = [], []
for i_flux in range(7,38):
    print("retrieving Flux #%s/49" %(i_flux+1))
    # pre-transform ipowa:
    ipowa_repeat = waveform(case.corder['Power']).inner_repeat
    # print("repeating power at %s times" %ipowa_repeat)
    selected_Ir, selected_Qr = [], []
    for i_repeat in range(ipowa_repeat):
        r_powa = 0 * ipowa_repeat + i_repeat # from the beginning position of repeating power
        selected_Ir += [selectedata[gotocdata([i_flux, x, 0, 0, 0, 0, 2*r_powa], c_cwsweep_structure)] for x in range(cxyfreq.count)]
        selected_Qr += [selectedata[gotocdata([i_flux, x, 0, 0, 0, 0, 2*r_powa+1], c_cwsweep_structure)] for x in range(cxyfreq.count)]
    # AVERAGE up those power repeats:
    selected_I = list(mean(array(selected_Ir).reshape(ipowa_repeat, cxyfreq.count), axis=0))
    selected_Q = list(mean(array(selected_Qr).reshape(ipowa_repeat, cxyfreq.count), axis=0))

    # assembly amplitude & phase:
    MagPha = [IQAP(x[0],x[1]) for x in zip(selected_I, selected_Q)]
    Amp, Pha = [], []
    for i,j in MagPha:
        Amp.append(i); Pha.append(j)

    
    # fig, ax = plt.subplots()
    # ax.plot(X, Amp)
    # plt.show()

    AMP += [Amp]

# Assembly 3D data.
X, Y = meshgrid(X, Y)
Z = array(AMP)

# Plot the surface.
# fig = plt.figure()
# ax = fig.gca(projection='3d')
# surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
# plt.show()

plt.pcolormesh(X, Y, Z)
plt.show()
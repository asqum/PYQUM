from resonator_tools import circuit
from pathlib import Path
from pandas import read_csv
from numpy import float64

from pyqum.instrument.analyzer import curve

import inspect

pyfilename = inspect.getfile(inspect.currentframe()) # current pyscript filename (usually with path)
MAIN_PATH = Path(pyfilename).parents[5] / "HODOR" / "CONFIG" # ...parents[7]... for logger
PORTAL_PATH = MAIN_PATH / "PORTAL"
Datafile = Path(PORTAL_PATH) / '1Dfresp[abc].csv'

title = "<b>frequency(GHz)</b>"
dataf = read_csv(Datafile, dtype={'I': float64})
print('I: %.8f' %dataf['I'][0])

port1 = circuit.notch_port()
port1.add_fromtxt(Datafile,'realimag',1,(0,3,4),fdata_unit=1e9,delimiter=',')
port1.autofit()
print("Fit results:", port1.fitresults)
# port1.plotall()
print('z_data %s' %port1.z_data)
print('z_data_sim %s' %port1.z_data_sim)
print('z_data_raw %s' %port1.z_data_raw)

x, y = [], []
for i in range(2):
    x.append(dataf[title])
y.append(abs(port1.z_data_raw))
y.append(abs(port1.z_data_sim))
curve(x,y,'Q_fit','freq','I',style=['or','.b'])

I, Q = [], []
I.append(port1.z_data_raw.real)
I.append(port1.z_data_sim.real)
Q.append(port1.z_data_raw.imag)
Q.append(port1.z_data_sim.imag)
curve(I,Q,'IQ_fit','I','Q',style=['or','.b'])

print("single photon limit:", port1.get_single_photon_limit(diacorr=True), "dBm")
print("photons in resonator for input -140dBm:", port1.get_photons_in_resonator(-140,unit='dBm',diacorr=True), "photons")





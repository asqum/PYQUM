from numpy import exp, pi, genfromtxt, sqrt, linspace, cos
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.constants import physical_constants as pc

data = genfromtxt('C:\\Users\\ASQUM\\Documents\\GitHub\\PYQUM\\TEST\\BETAsite\\test.dat')
# data = genfromtxt('test.dat')
xdata,ydata = (data[:,0])*1,(data[:,1])*1
# print(len(xdata))

t = linspace(1e-8, 1e-3, 100000)
dt = t[1] - t[0]
print("dt: %s" %dt)
print(pc['Bohr magneton'])
print(pc['reduced Planck constant'])

def func(B, c, D, tsf):
	Bfactor, val = 100, []
	print(len(B))
	for i in range(len(B)):
		Rnl = (c / sqrt(4*pi*D*t) * exp(-(3e-6)**2 / (4*D*t)) * cos(2*pc['Bohr magneton'][0]/pc['reduced Planck constant'][0]*B[i]*Bfactor*t) * exp(-1*t/tsf)) * dt
		print(sum(Rnl))
		val.append(sum(Rnl))
		# print('Value #%s: %s' %(i,val[i]))

	return val

plt.plot(xdata, ydata, 'b.', label='data')
popt, pcov = curve_fit(func, xdata, ydata)
plt.plot(xdata, func(xdata, *popt), 'r-', label='fit c=%.5f, D=%.3f,tsf=%.3f' %tuple(popt))    

plt.xlabel('t')
plt.ylabel('y')
plt.legend()

plt.show()
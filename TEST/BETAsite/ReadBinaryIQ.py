import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os, csv

pathstr = "D:\TEMP\stream.bin"
header = pathstr + ".txt"
with open(header, 'r') as myfile: 
    rows = csv.reader(myfile, delimiter='\t')
    matcheader = [row for row in rows]
print(matcheader)
YScale = [el for el in matcheader if 'YScale' in el]
XDelta = [el for el in matcheader if 'XDelta' in el]
print(YScale[0][0] + ': ' + YScale[0][1])
print("Acquisition rate (Bandwidth): " + str(1/float(XDelta[0][1])))
f = open(pathstr,'rb')
data = np.fromfile(f, dtype='<h', count=10000) # reads only subset of the file h:short l:long e,f:float
data = [x*float(YScale[0][1])/1e-3 for x in data] # rescaling back to 1V output
dataI = data[::2]
dataQ = data[1::2]
fs = os.path.getsize(pathstr)
f.close()
print(fs)
print(data[:25])

# Plotting
t = np.arange(0, len(dataI), 1)
t = [x*float(XDelta[0][1])/1e-6 for x in t]
fig, ax = plt.subplots()
ax.plot(t, dataI)
ax.plot(t, dataQ)
ax.set(xlabel='t($\mu s$)', ylabel='I/Q(mV)', title='IQ Modulated Waveform')
fig.savefig("datastreambin.png")
plt.show()
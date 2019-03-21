'''Reading Dilution Status'''

from pathlib import Path
from datetime import datetime
from time import mktime
from os import listdir
from numpy import diff
import matplotlib.pyplot as plt
from pyqum.instrument.analyzer import derivative

class bluefors:

    def __init__(self):
        self.LogPath = Path(r'\\BLUEFORSAS\BlueLogs')
        self.Days = listdir(self.LogPath)
        
    def selectday(self, num):
        try:
            self.Date = self.Days[num-1]
            print("Date selected: %s"%self.Date)
        except(ValueError): 
            print("index might be out of range")
            pass
    
    def Pressure(self, Channel):
        LogFile = self.LogPath / self.Date / ("maxigauge " + self.Date + ".log")
        with open(LogFile, 'r') as L:
            L = L.read()
        Plog = L.split('\n')[:-1]
        Plog = [x for x in Plog if ',,' not in x] #filter-out bad logs
        t = [datetime.strptime(x.split("CH")[0][:-1].split(',')[1], '%H:%M:%S') for x in Plog]
        startime = t[0].strftime('%H:%M:%S')
        t = [(x-t[0]).total_seconds()/3600 for x in t]
        P = [float(x.split("CH")[Channel][14:21]) for x in Plog]
        P_stat = [int(x.split("CH")[Channel][11]) for x in Plog]

        return startime, t, P, P_stat



# derivative to check the rate
fig, ax = plt.subplots(1, sharex=True, sharey=False)
ax.set(title="P-Data for Ch-%s on %s starting %s"%(Ch, Date, startime), xlabel="t(hour)", ylabel='P(mbar)')
ax.plot(t[1:], diff(P)/diff(t))
fig.tight_layout()
plt.show()


# Extracting T-data
Ch = 5
LogFile = LogPath / Date / ("CH%s T "%Ch + Date + ".log")
print(LogFile)

with open(LogFile, 'r') as L:
    L = L.read()

Tlog = list([x.split(',') for x in L.split('\n')[:-1]])
t, T = [datetime.strptime(x[1], '%H:%M:%S') for x in Tlog], [float(x[2]) for x in Tlog]
startime = t[0].strftime('%H:%M:%S')
t = [(x-t[0]).total_seconds()/3600 for x in t]

fig, ax = plt.subplots(1, sharex=True, sharey=False)
ax.set(title="T-Data for Ch-%s on %s starting %s"%(Ch, Date, startime), xlabel="t(hour)", ylabel='T(K)')
ax.plot(t, T)
fig.tight_layout()
plt.show()
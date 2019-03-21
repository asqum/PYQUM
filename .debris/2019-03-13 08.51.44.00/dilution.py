'''Reading Dilution Status'''

from pathlib import Path
from datetime import datetime
from time import mktime
from os import listdir
import matplotlib.pyplot as plt

LogPath = Path(r'\\BLUEFORSAS\BlueLogs')
print(LogPath)

Days = listdir(LogPath)


Date = Days[0] #"19-02-25"

# Extracting P-data
Ch = 5
LogFile = LogPath / Date / ("maxigauge " + Date + ".log")
print(LogFile)

with open(LogFile, 'r') as L:
    L = L.read()

Plog = L.split('\n')[1:-1]
Plog = [x for x in Plog if ',,' is not in Plog] #filter-out bad logs
t = [datetime.strptime(x.split("CH")[0][:-1].split(',')[1], '%H:%M:%S') for x in Plog]
startime = t[0].strftime('%H:%M:%S')
t = [(x-t[0]).total_seconds()/3600 for x in t]
P = [float(x.split("CH")[Ch][14:21]) for x in Plog]
P_stat = [int(x.split("CH")[Ch][11]) for x in Plog]

fig, ax = plt.subplots(1, sharex=True, sharey=False)
ax.set(title="P-Data for Channel %s from %s"%(Ch, startime), xlabel="t(hour)", ylabel='P(mbar)')
ax.plot(t, P)
fig.tight_layout()
plt.show()


# Extracting T-data
Ch = 5
LogFile = LogPath / Date / ("CH%s T "%Ch + Date + ".log")
print(LogFile)

with open(LogFile, 'r') as L:
    L = L.read()

Tlog = list([x.split(',') for x in L.split('\n')[1:-1]])
t, T = [datetime.strptime(x[1], '%H:%M:%S') for x in Tlog], [float(x[2]) for x in Tlog]
startime = t[0].strftime('%H:%M:%S')
t = [(x-t[0]).total_seconds()/3600 for x in t]

fig, ax = plt.subplots(1, sharex=True, sharey=False)
ax.set(title="T-Data for Channel %s from %s"%(Ch, startime), xlabel="t(hour)", ylabel='T(K)')
ax.plot(t, T)
fig.tight_layout()
plt.show()
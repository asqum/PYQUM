'''Reading Dilution Status'''

from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

LogPath = Path(r'\\BLUEFORSAS\BlueLogs')
print(LogPath)

Date = "19-02-27"
LogFile = LogPath / Date / ("maxigauge " + Date + ".log")
print(LogFile)

with open(LogFile, 'r') as L:
    L = L.read()

L = L.split('\n')[0]
print(L)

Time = L.split("CH")[0][:-1]
print(Time)
for i in range(6):
    Ch = i + 1
    Channel_State = L.split("CH")[Ch]
    Channel_data = bool(int(Channel_State[11]))
    if Channel_data:
        Channel_P = Channel_State[14:21]
    else: Channel_P = None
    print("Channel %s: data=%s, P=%s" %(Ch, Channel_data, Channel_P))


# Extracting T-data
Ch = 2
Date = "19-02-24"
LogFile = LogPath / Date / ("CH%s T "%Ch + Date + ".log")
print(LogFile)

with open(LogFile, 'r') as L:
    L = L.read()

Tlog = list([x.split(',') for x in L.split('\n')[:-1]])
t, T = [datetime.strptime(x[1], '%H:%M:%S') for x in Tlog], [float(x[2]) for x in Tlog]
t = [x-t[0] for x in t]

fig, ax = plt.subplots(1, sharex=True, sharey=False)
ax.set(title="T-Data for Channel %s"%Ch, xlabel="clock", ylabel='T(K)')
ax.plot(t, T)
fig.tight_layout()
plt.show()
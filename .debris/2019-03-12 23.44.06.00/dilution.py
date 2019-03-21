'''Reading Dilution Status'''

from pathlib import Path

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


Date = "19-02-24"
LogFile = LogPath / Date / ("CH2 T " + Date + ".log")
print(LogFile)

with open(LogFile, 'r') as L:
    L = L.read()

T = [x.split(',') for x in L.split('\n')]
print(T[1][0])
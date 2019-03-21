'''Reading Dilution Status'''

from pathlib import Path

LogPath = Path(r'\\BLUEFORSAS\BlueLogs')
print(LogPath)

Date = "19-02-27"
LogFile = LogPath / Date / ("maxigauge " + Date + ".log")
print(LogFile)

with open(LogFile, 'r') as L:
    L = L.read()

print(L)

print(L.split("CH1,        ")[1])
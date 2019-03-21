'''Reading Dilution Status'''

from pathlib import Path
from datetime import datetime
from time import mktime
from os import listdir
from numpy import diff
from pyqum.instrument.analyzer import derivative, curve

class bluefors:

    def __init__(self):
        self.LogPath = Path(r'\\BLUEFORSAS\BlueLogs')
        self.Days = listdir(self.LogPath)

    def whichday(self):
        total = len(self.Days)
        for i,day in enumerate(self.Days):
            print("%s. %s" %(i+1,day))
        while True:
            try:
                k = int(input("Which day would you like to check out (1-%s): " %total))
                if k-1 in range(total):
                    break
            except(ValueError):
                print("Bad index. Please use numeric!")

        return k-1

        
    def selectday(self, index):
        try:
            self.Date = self.Days[index]
            print("Date selected: %s"%self.Date)
        except(ValueError): 
            print("index might be out of range")
            pass
    
    def pressure(self, Channel):
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

    def temperature(self, Channel):
        LogFile = self.LogPath / self.Date / ("CH%s T "%Channel + self.Date + ".log")
        with open(LogFile, 'r') as L:
            L = L.read()
        Tlog = list([x.split(',') for x in L.split('\n')[:-1]])
        t, T = [datetime.strptime(x[1], '%H:%M:%S') for x in Tlog], [float(x[2]) for x in Tlog]
        startime = t[0].strftime('%H:%M:%S')
        t = [(x-t[0]).total_seconds()/3600 for x in t]

        return startime, t, T


def test():
    b = bluefors()
    b.selectday(b.whichday())
    P = b.pressure(3)
    curve(P[1], P[2], "Starting %s"%P[0], "t(hr)", "P(mbar)")
    T = b.temperature(2)
    curve(T[1], T[2], "Starting %s"%T[0], "t(hr)", "T(K)")
    t, dTdt = derivative(T[1], T[2], 3)
    curve(t, dTdt, "Starting %s"%T[0], "t(hr)", "dT/dt(K)")    

test()
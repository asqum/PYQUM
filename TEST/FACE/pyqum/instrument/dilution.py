'''Reading Dilution Status
    Controlling via Server'''

from pathlib import Path
from datetime import datetime
from time import mktime
from os import listdir
from numpy import diff
from telnetlib import Telnet, IAC, NOP
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
    
    def pressurelog(self, Channel):
        try:
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
        except:
            startime, t, P, P_stat = '', [], [], []
            pass

        return startime, t, P, P_stat

    def temperaturelog(self, Channel, Unit='K'):
        try:
            LogFile = self.LogPath / self.Date / ("CH%s T "%Channel + self.Date + ".log")
            with open(LogFile, 'r') as L:
                L = L.read()
            Tlog = list([x.split(',') for x in L.split('\n')[:-1]])
            t, T = [datetime.strptime(x[1], '%H:%M:%S') for x in Tlog], [float(x[2]) for x in Tlog]
            startime = t[0].strftime('%H:%M:%S')
            t = [(x-t[0]).total_seconds()/3600 for x in t] # in hour(s)
            if Unit.upper() == 'C':
                T = [x - 273 for x in T]
        except:
            startime, t, T = 'NOT FOUND', [], []
            pass

        return startime, t, T

    def connecting(self, ip="192.168.1.23", port=8325):
        try:
            self.connect = Telnet(ip, port, timeout=13)
            self.connect.write("remote\n".encode('ascii'))
            remote_status = self.connect.read_until(b"\r\n", timeout=7).decode('ascii').replace('\r\n','')
            if remote_status:
                self.connect.write("control 1\n".encode('ascii'))
                control = self.connect.read_until(b"\r\n").decode('ascii').replace('\r\n','')
                self.connect.write("remote 1\n".encode('ascii'))
                remote = self.connect.read_until(b"\r\n").decode('ascii').replace('\r\n','')
                if remote.split(': ')[1] == '1': 
                    print("Dilution connected: %s"%control.split(' ')[3])
                    return True
                else: 
                    print("NO remote: make sure the server is not busy!")
                    return None
            else: 
                print("Check the server status and make sure it's running!")
                return None
        except:
            pass 
            print("Check the IP/Port and connection speed!")
            return None
        
    def gauge(self, Channel):
            self.connect.write(("mgstatus %s\n"%Channel).encode('ascii'))
            output = self.connect.read_until(b"\r\n").decode('ascii').replace('\r\n','').split(": ")
            return output[1]

    def close(self):
        self.connect.write("exit\n".encode('ascii'))
        self.connect.close()
        print("Dilution's server disconnected!")

class valve(bluefors):
    '''Initialize the valves'''
    def __init__(self, connect):
        super().__init__()
        self.connect = connect
    
    def status(self, Channel):
        self.connect.write(("status v%s\n"%Channel).encode('ascii'))
        output = self.connect.read_until(b"\r\n").decode('ascii').replace('\r\n','').split(": ")
        return output[1]

class scroll(bluefors):
    '''Initialize the scrolls'''
    def __init__(self, connect):
        super().__init__()
        self.connect = connect
    
    def status(self, Channel):
        self.connect.write(("status scroll%s\n"%Channel).encode('ascii'))
        output = self.connect.read_until(b"\r\n").decode('ascii').replace('\r\n','').split(": ")
        return output[1]

    def off(self, Channel):
        self.connect.write(("off scroll%s\n"%Channel).encode('ascii'))
        output = self.connect.read_until(b"\r\n").decode('ascii').replace('\r\n','').split(": ")
        return output[1]

    def on(self, Channel):
        self.connect.write(("on scroll%s\n"%Channel).encode('ascii'))
        output = self.connect.read_until(b"\r\n").decode('ascii').replace('\r\n','').split(": ")
        return output[1]

class warmup(bluefors):
    '''Initialize the scrolls'''
    def __init__(self, connect):
        super().__init__()
        self.connect = connect
    
    def status(self):
        self.connect.write(("status e1302p=30\n").encode('ascii'))
        output = self.connect.read_until(b"\r\n").decode('ascii').replace('\r\n','').split(": ")
        return output[1]

    def off(self, Channel):
        self.connect.write(("off e1302%s\n"%Channel).encode('ascii'))
        output = self.connect.read_until(b"\r\n").decode('ascii').replace('\r\n','').split(": ")
        return output[1]

    def on(self, Channel):
        self.connect.write(("on e1302%s\n"%Channel).encode('ascii'))
        output = self.connect.read_until(b"\r\n").decode('ascii').replace('\r\n','').split(": ")
        return output[1]

def test():
    from scipy.stats import linregress
    from pyqum.instrument.network import notify
    from time import sleep

    b = bluefors()
    # b.selectday(b.whichday())
    b.selectday(len(b.Days)-1)

    # Ch = 5
    # P = b.pressurelog(Ch)
    # curve(P[1], P[2], "P%s Starting %s"%(Ch, P[0]), "t(hr)", "P(mbar)")
    # t, dPdt = derivative(P[1], P[2], 3)
    # curve(t, dPdt, "dP%s/dt Starting %s"%(Ch, P[0]), "t(hr)", "dP/dt(mbar/hr)")

    Ch, T_unit = 2, 'C'
    while True:
        T = b.temperaturelog(Ch, T_unit)
        print("Current 4K-plate Temperature: %s" %T[2][len(T[2])-7:-1])
        reg = linregress(T[1][len(T[2])-7:-1], T[2][len(T[2])-7:-1])
        ETA = (28-T[2][-1]) / reg[0]
        print("ETA for T%s in %s hour(s)" %(Ch,ETA))
        sleep(10)
        if ETA < 0:
            # notify('ufocrew@gmail.com', 'T2', 'Exceeding 28C')
            break

    # curve(T[1], T[2], "T%s Starting %s"%(Ch, T[0]), "t(hr)", "T(%s)"%T_unit)
    # t, dTdt = derivative(T[1], T[2], 3)
    # curve(t, dTdt, "dT%s/dt Starting %s"%(Ch, T[0]), "t(hr)", "dT/dt(%s/hr)"%T_unit)    

    # if b.connecting():
    #     v, s, w = valve(b.connect), scroll(b.connect), warmup(b.connect)
    #     print(v.status(17))
    #     print("P2: %s"%b.gauge(2))
    #     print(s.status(2))
    #     # print("ON Scroll2: %s"%s.on(2).upper())
    #     # if int(input("TURN OFF SCROLL2(0/1)? ")):
    #     #     print("OFF Scroll2: %s"%s.off(2).upper())
    #     print("warmup heater: %s" %w.status())
    #     b.close()

# test()


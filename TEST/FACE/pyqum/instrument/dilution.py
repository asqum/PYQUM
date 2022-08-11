'''Reading Dilution Status
    Controlling via Server'''

from pathlib import Path
from datetime import datetime
from time import mktime, sleep
from os import listdir
from numpy import diff
from telnetlib import Telnet, IAC, NOP
from pyqum.instrument.analyzer import derivative, curve, cleantrace
from pyqum.instrument.reader import bdr_address

class bluefors:

    def __init__(self, designation="Alice"):

        # if designation=="Alice":
        #     self.LogPath = Path(r'\\BLUEFORSAS\BlueLogs') # direct-access without password
        #     self._TPath = Path(r'') # compensate for temperature path
        #     self.T_name = 'T'
        # elif designation=="Bob":
        #     self.LogPath = Path(r'\\BLUEFORSAS2\dr_bob') # direct-access without password
        #     self._TPath = Path(r'\log-data\192.168.1.188') # compensate for temperature path
        #     self.T_name = 'TEMPERATURE'

        self.LogPath = Path(r'%s' %bdr_address(designation)[0]) # direct-access without password
        self._TPath = Path(r'%s' %bdr_address(designation)[1]) # compensate for temperature path
        self.T_name = bdr_address(designation)[2]

        P_Days, T_Days = set(listdir(self.LogPath)), set(listdir(self.LogPath / self._TPath))
        self.Days = list((P_Days | T_Days) - {'log-data'})
        self.Days.sort()

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
            # print("Date selected: %s"%self.Date)
        except(ValueError): 
            print("index might be out of range")
            pass

    def temperaturelog(self, Channel, Unit='K'):
        try:
            LogFile = self.LogPath / self._TPath / self.Date / ("CH%s %s %s.log"%(Channel, self.T_name, self.Date))
            with open(LogFile, 'r') as L:
                L = L.read()
            Tlog = list([x.split(',') for x in L.split('\n')[:-1]])
            t, T = [datetime.strptime(x[1], '%H:%M:%S') for x in Tlog], [float(x[2]) for x in Tlog]
            daystart = datetime.strptime('00:00:00', '%H:%M:%S')
            t = [(x-daystart).total_seconds()/3600 for x in t] # converted to time lapsed in hour(s)
            if Unit.upper() == 'C':
                T = [x - 273 for x in T]
        
        except(FileNotFoundError):
            t, T = ['~ '], ['~ ']
            pass
        if not T: t, T = ['Nil '], ['Nil '] # check for empty-list

        return t, T

    def pressurelog(self, Channel):
        try:
            LogFile = self.LogPath / self.Date / ("maxigauge " + self.Date + ".log")
            with open(LogFile, 'r') as L:
                L = L.read()
            stat = 'CH%s' %Channel
            Plog = list([x.split(',') for x in L.split('\n')[:-1]])
            t, P, P_stat = [datetime.strptime(x[1], '%H:%M:%S') for x in Plog if stat in x], [float(x[x.index(stat)+3]) for x in Plog if stat in x], [float(x[x.index(stat)+2]) for x in Plog if stat in x]
            daystart = datetime.strptime('00:00:00', '%H:%M:%S')
            t = [(x-daystart).total_seconds()/3600 for x in t] # converted to time lapsed in hour(s)
        
        except(FileNotFoundError):
            t, P, P_stat = ['~ '], ['~ '], ['~ ']
            pass
        if not P: t, P, P_stat = ['Nil '], ['Nil '], ['Nil '] # check for empty-list

        return t, P, P_stat

    def flowmeterlog(self):
        try:
            LogFile = self.LogPath / self.Date / ("Flowmeter " + self.Date + ".log")
            with open(LogFile, 'r') as L:
                L = L.read()
            Flog = list([x.split(',') for x in L.split('\n')[:-1]])
            t, F = [datetime.strptime(x[1], '%H:%M:%S') for x in Flog], [float(x[2]) for x in Flog]
            daystart = datetime.strptime('00:00:00', '%H:%M:%S')
            t = [(x-daystart).total_seconds()/3600 for x in t] # converted to time lapsed in hour(s)
            
        except(FileNotFoundError):
            t, F = ['~ '], ['~ ']
            pass
        if not F: t, F = ['Nil '], ['Nil '] # check for empty-list

        return t, F

    def statuslog(self, stat):
        try:
            LogFile = self.LogPath / self.Date / ("Status_" + self.Date + ".log")
            with open(LogFile, 'r') as L:
                L = L.read()
            Slog = list([x.split(',') for x in L.split('\n')[:-1]])
            # List equipments' Status:
            t, S = [datetime.strptime(x[1], '%H:%M:%S') for x in Slog if stat in x], [float(x[x.index(stat)+1]) for x in Slog if stat in x]
            daystart = datetime.strptime('00:00:00', '%H:%M:%S')
            t = [(x-daystart).total_seconds()/3600 for x in t] # converted to time lapsed in hour(s)

        except(FileNotFoundError):
            t, S = ['~ '], ['~ ']
            pass
        if not S: t, S = ['Nil '], ['Nil '] # check for empty-list

        return t, S

    def channellog(self, stat):
        try:
            LogFile = self.LogPath / self.Date / ("Channels " + self.Date + ".log")
            with open(LogFile, 'r') as L:
                L = L.read()
            Vlog = list([x.split(',') for x in L.split('\n')[:-1]])
            # List equipments' Status:
            t, V = [datetime.strptime(x[1], '%H:%M:%S') for x in Vlog if stat in x], [int(x[x.index(stat)+1]) for x in Vlog if stat in x]
            daystart = datetime.strptime('00:00:00', '%H:%M:%S')
            t = [(x-daystart).total_seconds()/3600 for x in t] # converted to time lapsed in hour(s)
            
        except(FileNotFoundError):
            t, V = ['~ '], ['~ ']
            pass

        # Post processing:
        if not V:
             t, V = ['Nil '], ['Nil '] # check for empty-list
        
        # Cleanup repeating progress:
        t = [t[i] for i in cleantrace(V)]

        return t, V

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

class control(bluefors):
    '''Initialize the control-panel'''
    def __init__(self):
        super().__init__()
        self.connecting()
        self.selectday(len(self.Days)-1) #Get the latest
    
    def status(self, Node="v", Channel=""):
        self.connect.write(("status %s%s\n"%(Node,Channel)).encode('ascii'))
        output = self.connect.read_until(b"\r\n").decode('ascii').replace('\r\n','').split(": ")
        print(output[1].upper())
        return output[1]

    def maxigauge(self, Channel):
        self.connect.write(("mgstatus %s\n"%Channel).encode('ascii'))
        output = self.connect.read_until(b"\r\n").decode('ascii').replace('\r\n','').split(": ")
        print(output[1].upper())
        return output[1]

    def on(self, Node="v", Channel=""):
        '''Turn on <Node> of channel-<Channel>'''
        self.connect.write(("on %s%s\n"%(Node,Channel)).encode('ascii'))
        output = self.connect.read_until(b"\r\n").decode('ascii').replace('\r\n','').split(": ")
        print("%s%s was turned ON: %s"%(Node,Channel,output[1].upper()))
        return output[1]
    
    def off(self, Node="v", Channel=""):
        '''Turn off <Node> of channel-<Channel>'''
        self.connect.write(("off %s%s\n"%(Node,Channel)).encode('ascii'))
        output = self.connect.read_until(b"\r\n").decode('ascii').replace('\r\n','').split(": ")
        print("%s%s was turned OFF: %s"%(Node,Channel,output[1].upper()))
        return output[1]

    def condense_circ(self):
        self.on('v',5)
        sleep(3)
        self.on('v',6)
        sleep(3)
        self.on('compressor')
        sleep(5)
        self.off('v',4)

    def prepare_circ(self):
        self.off('compressor')
        sleep(2)
        self.off('v',6)
        sleep(2)
        if self.pressurelog(3)[2][-1] < 800: # attn: use maxigauge instead!
            self.off('v',5)
            self.off('v',7)
        else: print("Please close V5 then V7 manually after P3<800")
        
    def close(self):
        self.connect.write("exit\n".encode('ascii'))
        self.connect.close()
        print("Dilution's server disconnected!")
    

class warmup(bluefors): #to be verified..
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

    b = bluefors()
    # b.selectday(b.whichday())
    b.selectday(len(b.Days)-2) #latest reading

    valve = 'compressor'
    V = b.channellog(valve)
    curve(V[0], V[1], valve, "t(hr)", "State")

    # Ch = 5
    # P = b.pressurelog(Ch)
    # curve(P[1], P[2], "P%s Starting %s"%(Ch, P[0]), "t(hr)", "P(mbar)")
    # t, dPdt = derivative(P[1], P[2], 3)
    # curve(t, dPdt, "dP%s/dt Starting %s"%(Ch, P[0]), "t(hr)", "dP/dt(mbar/hr)")

    # F = b.flowmeterlog()
    # curve(F[1], F[2], "Flow Starting %s"%(F[0]), "t(hr)", "Flow(mmol/s)")

    # Ch, T_unit = 2, 'C'
    # while True:
    #     T = b.temperaturelog(Ch, T_unit)
    #     print("Current 4K-plate Temperature: %s" %T[2][len(T[2])-7:-1])
    #     reg = linregress(T[1][len(T[2])-7:-1], T[2][len(T[2])-7:-1])
    #     ETA = (28-T[2][-1]) / reg[0]
    #     print("ETA for T%s in %s hour(s)" %(Ch,ETA))
    #     sleep(10)
    #     if ETA < 0:
    #         # notify('ufocrew@gmail.com', 'T2', 'Exceeding 28C')
    #         break

    # curve(T[1], T[2], "T%s Starting %s"%(Ch, T[0]), "t(hr)", "T(%s)"%T_unit)
    # t, dTdt = derivative(T[1], T[2], 3)
    # curve(t, dTdt, "dT%s/dt Starting %s"%(Ch, T[0]), "t(hr)", "dT/dt(%s/hr)"%T_unit)    

    # Control-panel:
    # c = control()
    # c.maxigauge(3)
    # c.status('v',5)
    # c.prepare_circ()
    # c.close()

# test()


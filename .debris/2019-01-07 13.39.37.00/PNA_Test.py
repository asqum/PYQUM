import visa
from numpy import arange, sqrt, arctan, frombuffer, array, linspace, pi, log10, reshape
import matplotlib.pyplot as plt
from time import sleep, time

# pna
rm = visa.ResourceManager()
pna = rm.open_resource("TCPIP0::192.168.0.6::hpib7,16::INSTR") #PNA

pna.read_termination = '\n' #omit termination tag from output 
pna.timeout = 8000000 #set timeout

#Checking Connections & Identities

# print('All connected GPIB Instruments:', rm.list_resources())
print(pna.query('*IDN?'))  #inquiring machine identity: "who r u?"

#Clear buffer memory
pna.write(':SENS:CORR:COLL:CLE') 

# START TRANSLATION FROM LABVIEW

pna.write("SENS:SWE:TYPE LIN")
status = pna.query("SENS:SWE:TYPE?")
print("Sweeping Type: %s" %status)
N = 150
pna.write("SENSe:SWEep:POINts %s" %N)
datapts = pna.query("SENSe:SWEep:POINts?")
print("Sweeping Points#: %s" %datapts)
sweeptime = pna.query("SENS:SWE:TIME?")
print("Sweeping Time: %s" %sweeptime)

f_start, f_stop = 5e9, 7e9
pna.write("SENS:FREQuency:STARt %s" %f_start)
pna.write("SENS:FREQuency:STOP %s" %f_stop)
fstart = pna.query("SENSe:FREQuency:STARt?")
print("Start Frequency(Hz): %s" %fstart)
fstop = pna.query("SENSe:FREQuency:STOP?")
print("Stop Frequency(Hz): %s" %fstop)

IFB = (float(fstart) - float(fstop))/N
pna.write("SENSe:BANDwidth %s" %IFB)#unit is Hz
status = pna.query("SENSe:BANDwidth?") #IF Freq
print("Bandwidth (Hz): %s" %status)
status = pna.query("SOURce:POWer?")
print("Power (dBm): %s" %status)

Ave_num = 1
status = pna.write("SENSe:SWE:GRO:COUN %s" %Ave_num) #Averaged by VNA itself
print("Set Trigger group count=%s: %s" %(Ave_num, [x for x in status]))
status = pna.write("TRIG:SOUR IMM")
print("Set immediate: %s" %[x for x in status])

status = pna.write("SENSe:AVER:COUN %s" %Ave_num) #Averaged by VNA itself
print("Set Average Number=%s: %s" %(Ave_num, [x for x in status]))
status = pna.write("SENSe:AVER:CLE")
print("Clear Average: %s" %[x for x in status])
status = pna.write("SENSe:AVER OFF") #OFF
print("Set Average OFF: %s" %[x for x in status])

# switch on pna
# pna.write('OUTP ON')

# when opc return, the sweep is done
pna.query("SENS:SWE:MODE GRO;*OPC?")

status = pna.query("CALC1:PAR:CAT?")
Catalog = status.replace('"', '').split(',')
print(Catalog)
Mname = Catalog[0]
print("Mname: %s" %Mname)

chnum = 1
# select measurement name
status = pna.write('CALC%d:PAR:SEL %s'%(chnum, Mname))
print("select parameter: %s" %[x for x in status])
status = pna.write('CALC%d:DATA SDATA %s'%(chnum, Mname))
print("select sdata: %s" %[x for x in status])

# RAW DATA ACQuisite
# pna.write("CALC%d:DATA? SDATA"%chnum)
# data = pna.read_raw()
# i0 = data.find(b'#')
# nDig = int(data[i0+1:i0+2])
# nByte = int(data[i0+2:i0+2+nDig])
# nData = int(nByte/4)
# nPts = int(nData/2)
# datas = frombuffer(data[(i0+2+nDig):(i0+2+nDig+nByte)], dtype='>f', count=nData-1)

pna.write("FORMat:DATA REAL,32")

start = time() #in seconds
databin = pna.query_binary_values(":CALC:SEL:DATA:SDAT?", datatype='f', is_big_endian=True)
# print("raw data with %s points" %len(data))
# print(data)
stop = time()
DataAcqTimeb = stop - start
print("It take %ss to retrieve data from machine using binary" %DataAcqTimeb)

start = time() #in seconds
pna.write("FORMat:DATA ASCII,0")
data = pna.query(":CALC:SEL:DATA:SDAT?")
datascii = data.split(',')
stop = time()
DataAcqTimes = stop - start
print("It take %ss to retrieve data from machine using ascii" %DataAcqTimes)

if DataAcqTimeb > DataAcqTimes:
    print("ASCII is transferred faster than Binary by %sms" %((DataAcqTimeb - DataAcqTimes)/1e-3))
elif DataAcqTimes > DataAcqTimeb:
    print("Binary is transferred faster than ASCII by %sms" %((DataAcqTimes - DataAcqTimeb)/1e-3))
else: print("ascii and binary has the exact same speed")

databoth = array(databin + datascii)
if len(databin) == len(datascii):
    DATA = databoth.reshape(2, len(databin))
else: print("inconsistency between binary and ascii data handling!")

for i in range(len(DATA[:])):
    datas = DATA[i]
    print("Data #%s:" %i)
    print("Data-length: %s" %len(datas))
    # print("Data: %s" %datas)

    IQdata = datas.reshape(datapts, 2)
    Idata, Qdata = IQdata[:,0], IQdata[:,1]

    print("Idata-length: %s" %len(Idata))
    yI = [float(i) for i in Idata]
    yQ = [float(i) for i in Qdata]

    Amp, Pha = [], []
    for i in zip(yI, yQ):
        Amp.append(20*log10(sqrt(i[0]**2 + i[1]**2)))
        if i[0] == 0:
            Pha.append(pi/2)
        else: Pha.append(arctan(i[1]/i[0]))

    # Plotting
    fig, ax = plt.subplots(2, 2, sharex=True, sharey=False)
    ax[0][0].set(title="IQ-Data")
    ax[0][0].plot(X, yI)
    # ax[0].set(ylabel=r'I-Data (V)')
    ax[0][1].plot(X, yQ)
    # ax[1].set(ylabel=r'Q-Data (V)')
    # ax[1].set(xlabel=r'$time({\times} 10^{%d}s)$'%(x_order))
    ax[1][0].plot(X, Amp)
    ax[1][1].plot(X, Pha)
    # [axe.grid(True) for axe in ax]
    fig.tight_layout()
    plt.show()

pna.close()


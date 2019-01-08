import visa
from numpy import arange, sqrt, frombuffer
import matplotlib.pyplot as plt

from time import sleep

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
pna.write("SENSe:SWEep:POINts 300")
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

IFB = 70
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

# input("Ready?")
# sleep(37)

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

status = pna.write("FORMat:DATA REAL,32")
# status = pna.write("FORMat:DATA ASCII,0")
print("Format data: %s" %[x for x in status])
data = pna.query_binary_values("CALC%d:DATA? SDATA"%chnum)#, datatype='d', is_big_endian=True)
# data = pna.query("CALC%d:DATA? SDATA"%chnum)
print(data)
i0 = data.find(b'#')
nDig = int(data[i0+1:i0+2])
nByte = int(data[i0+2:i0+2+nDig])
nData = int(nByte/4)
nPts = int(nData/2)
# get data to numpy array
datas = frombuffer(data[(i0+2+nDig):(i0+2+nDig+nByte)], dtype='>f', count=nData)
# datas = data.split(',')
print("Data-length: %s" %len(datas))
# print(datas)

i, Idata, Qdata, Amp = 1, [], [], []
for x in datas:
    if i%2: #odd
        Idata.append(x)
    else: Qdata.append(x) #even
    i += 1

print("Idata-length: %s" %len(Idata))
yI = [float(i) for i in Idata]
yQ = [float(i) for i in Qdata]

for i in zip(yI, yQ):
    Amp.append(sqrt(i[0]**2 + i[1]**2))
# print(Amp)

fstart, fstop, datapts = float(fstart), float(fstop), float(datapts)
print("data points: %s" %(datapts-1))
X = list(arange(fstart, fstop, (fstop-fstart)/(datapts-1))) + [fstop]

# Plotting
fig, ax = plt.subplots(3, 1, sharex=True, sharey=False)
ax[0].set(title="IQ-Data")
ax[0].plot(X, yI)
# ax[0].set(ylabel=r'I-Data (V)')
ax[1].plot(X, yQ)
# ax[1].set(ylabel=r'Q-Data (V)')
# ax[1].set(xlabel=r'$time({\times} 10^{%d}s)$'%(x_order))
ax[2].plot(X, Amp)
[axe.grid(True) for axe in ax]
fig.tight_layout()
plt.show()


# switch off pna
pna.write('OUTP OFF')
pna.close()

import visa
from numpy import arange, sqrt, arctan, frombuffer, array, linspace, pi, log10
import matplotlib.pyplot as plt
from time import sleep

# ena
rm = visa.ResourceManager()
# ena = rm.open_resource('GPIB0::16::INSTR') #establishing GPIB connection with ENA E5071C
ena = rm.open_resource('TCPIP0::169.254.176.142::INSTR') #establishing LAN connection with ENA E5071C

ena.read_termination = '\n' #omit termination tag from output 
ena.timeout = 8000000 #set timeout

print(ena.query('*IDN?'))  #inquiring machine identity: "who r u?"

#Clear buffer memory
ena.write('*RST;*CLS;')

# Setting Trace
ena.write("CALC:PAR:COUN 1")
ena.write("CALC1:PAR1:DEF S21")

ena.write(":SENS1:SWE:TYPE LIN")
status = ena.query("SENS:SWE:TYPE?")
print("Sweeping Type: %s" %status)
N = 30
ena.write("SENSe:SWEep:POINts %s" %N)
datapts = ena.query("SENSe:SWEep:POINts?")
print("Sweeping Points#: %s" %datapts)

ena.write("SENSe:FREQuency:STARt 5e9")
fstart = ena.query("SENSe:FREQuency:STARt?")
print("Start Frequency(Hz): %s" %fstart)
ena.write("SENSe:FREQuency:STOP 7e9")
fstop = ena.query("SENSe:FREQuency:STOP?")
print("Stop Frequency(Hz): %s" %fstop)

IFB = (float(fstart) - float(fstop))/N
ena.write("SENSe:BANDwidth %s" %IFB)
status = ena.query("SENSe:BANDwidth?") #IF Freq
print("Bandwidth (Hz): %s" %status)
ena.write("SOURce:POWer -10")
status = ena.query("SOURce:POWer?")
print("Power (dBm): %s" %status)

status = ena.write("SENSe:AVER ON") #OFF
print("Set Average ON: %s" %[x for x in status])
Ave_num = 1
status = ena.write("SENSe:AVER:COUN %s" %Ave_num) #Averaged by VNA itself
print("Set Average Number=%s: %s" %(Ave_num, [x for x in status]))
status = ena.write("SENSe:AVER:CLE")
print("Clear Average: %s" %[x for x in status])

# switch on ena
# ena.write('OUTP ON')

# start measurement
ena.write(':ABOR;:INIT:CONT ON;:TRIG:SOUR BUS;:TRIG:SING;')

ena.write(":DISP:WIND1:TRAC1:Y:AUTO") #auto-scale
sweeptime = ena.query("SENS:SWE:TIME?")
print("Sweeping Time: %s" %sweeptime)
# sleep(float(sweeptime))

# make the machine inform us when the measurement is done
ena.query("*OPC?")

chnum = 1
# select measurement name
status = ena.write('CALC%d:PAR1:SEL'%(chnum))

if input("REAL? "):
    ena.write(':FORM:DATA REAL32')
    if input("RAW? "):
        ena.write(":CALC:SEL:DATA:SDAT?")
        data = ena.read_raw()
        i0 = data.find(b'#')
        print("header location: %s" %i0)
        nDig = int(data[i0+1:i0+2])
        print("byte size: %s" %nDig)
        nByte = int(data[i0+2:i0+2+nDig])
        print("number of bytes transferred: %s" %nByte)
        nData = int(nByte/4)
        print("data size: %s" %nData)
        nCPair = int(nData/2)
        print("# of complex-pairs: %s" %nCPair)
        print("Main Data:")
        chunck = data[(i0+2+nDig):(i0+2+nDig+nByte)]
        print(chunck)
        datas = frombuffer(data[(i0+2+nDig):(i0+2+nDig+nByte)], dtype='>f', count=nData)
    else:
        data = ena.query_binary_values(":CALC:SEL:DATA:SDAT?", datatype='f', is_big_endian=True)
        print("raw data with %s points" %len(data))
        print(data)
        datas = list(data)
else:
    ena.write(':FORM:DATA ASCII')
    data = ena.query(":CALC:SEL:DATA:SDAT?")
    datas = data.split(',')

# switch off ena
state = ena.query("OUTPUT?")
print(state)
ena.write('OUTP OFF')

print("Data-length: %s" %len(datas))
print("Data: %s" %datas)

i, Idata, Qdata, Amp, Pha = 1, [], [], [], []
for x in datas:
    if i%2: #odd
        Idata.append(x)
    else: Qdata.append(x) #even
    i += 1

print("Idata-length: %s" %len(Idata))
yI = [float(i) for i in Idata]
yQ = [float(i) for i in Qdata]

for i in zip(yI, yQ):
    Amp.append(20*log10(sqrt(i[0]**2 + i[1]**2)))
    if i[0] == 0:
        Pha.append(pi/2)
    else: Pha.append(arctan(i[1]/i[0]))

fstart, fstop, datapts = float(fstart), float(fstop), float(datapts)
X = list(linspace(fstart, fstop, datapts))

# Plotting
fig, ax = plt.subplots(4, 1, sharex=True, sharey=False)
ax[0].set(title="IQ-Data")
ax[0].plot(X, yI)
# ax[0].set(ylabel=r'I-Data (V)')
ax[1].plot(X, yQ)
# ax[1].set(ylabel=r'Q-Data (V)')
# ax[1].set(xlabel=r'$time({\times} 10^{%d}s)$'%(x_order))
ax[2].plot(X, Amp)
ax[3].plot(X, Pha)
[axe.grid(True) for axe in ax]
fig.tight_layout()
plt.show()

ena.close()

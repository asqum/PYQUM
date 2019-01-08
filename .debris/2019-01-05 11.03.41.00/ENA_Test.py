import visa
from numpy import arange, sqrt, arctan, frombuffer, array
import matplotlib.pyplot as plt
from time import sleep

# ena
rm = visa.ResourceManager()
# ena = rm.open_resource('GPIB0::16::INSTR') #establishing GPIB connection with ENA E5071C
ena = rm.open_resource('TCPIP0::169.254.176.142::INSTR') #establishing LAN connection with ENA E5071C
# ena = rm.open_resource("visa://140.109.103.227:5300/TCPIP0::169.254.176.142::INSTR") #remote visa with ENA E5071C
# ena = rm.open_resource("TCPIP0::192.168.0.6::hpib7,16::INSTR") #PNA

ena.read_termination = '\n' #omit termination tag from output 
ena.timeout = 8000 #set timeout

#Checking Connections & Identities

# print('All connected GPIB Instruments:', rm.list_resources())
print(ena.query('*IDN?'))  #inquiring machine identity: "who r u?"

#Clear buffer memory
ena.write(':SENS:CORR:COLL:CLE') 

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
sweeptime = ena.query("SENS:SWE:TIME?")
print("Sweeping Time: %s" %sweeptime)

ena.write("SENSe:FREQuency:STARt 1e9")
fstart = ena.query("SENSe:FREQuency:STARt?")
print("Start Frequency(Hz): %s" %fstart)
ena.write("SENSe:FREQuency:STOP 9e9")
fstop = ena.query("SENSe:FREQuency:STOP?")
print("Stop Frequency(Hz): %s" %fstop)

IFB = (float(fstart) - float(fstop))/N/10
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
ena.write('OUTP ON')

# start measurement
# ena.write("TRIG:SOUR INT")
# ena.write("INIT:CONT ON")
ena.write(':ABOR;:INIT:CONT OFF;:INIT:IMM;')
# ena.write("INIT:CONT OFF")
# ena.write("INIT:IMM")
# ena.write("TRIG:SING")

# when opc return, the sweep is done
# ena.query("*OPC?") 

sleep(float(sweeptime))

chnum = 1
# select measurement name
status = ena.write('CALC%d:PAR1:SEL'%(chnum))
ena.write(':FORM:DATA REAL32')
data = ena.query_binary_values(":CALC:SEL:DATA:SDAT?", datatype='d', is_big_endian=True)
datas = [x for x in data]
print(datas[0:15])

# switch off ena
ena.write('OUTP OFF')

# datas = data.split(',')
print("Data-length: %s" %len(datas))
# print(datas)

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
    Amp.append(sqrt(i[0]**2 + i[1]**2))
    Pha.append(arctan(i[1]/i[0]))



fstart, fstop, datapts = float(fstart), float(fstop), float(datapts)
X = list(arange(fstart, fstop, (fstop-fstart)/(datapts-1))) + [fstop]

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

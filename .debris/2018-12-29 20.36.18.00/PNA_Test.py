import visa
from numpy import arange
import matplotlib.pyplot as plt

# ena
rm = visa.ResourceManager()
# ena = rm.open_resource('GPIB0::16::INSTR') #establishing GPIB connection with ENA E5071C
# ena = rm.open_resource('TCPIP0::169.254.176.142::INSTR') #establishing LAN connection with ENA E5071C
# ena = rm.open_resource("visa://140.109.103.227:5300/TCPIP0::169.254.176.142::INSTR") #remote visa with ENA E5071C
ena = rm.open_resource("TCPIP0::192.168.0.6::hpib7,16::INSTR") #PNA

ena.read_termination = '\n' #omit termination tag from output 
ena.timeout = 8000 #set timeout

#Checking Connections & Identities

# print('All connected GPIB Instruments:', rm.list_resources())
print(ena.query('*IDN?'))  #inquiring machine identity: "who r u?"

#Clear buffer memory
ena.write(':SENS:CORR:COLL:CLE') 

# set trace#
def setrace(chnum, trace_num):
    
    trace_info, Mname = '', {}
    for i in range(trace_num):
        Mname[str(i+1)] = ena.query('CALC1:PAR%s:DEF?' %(i+1))
        trace_info += ('trace#%s: ' %(i+1) + Mname[str(i+1)] +'\n')
    print(trace_info)
    # turn on two windows (can up to 4?)
    for i in range(trace_num):
        status = ena.write("DISP:WIND%s:STATe ON" %(i+1))
        print("Display Windows: %s" %[x for x in status])
    return Mname


# START TRANSLATION FROM LABVIEW
status = ena.write("FORMat:DATA ASCii,0")
print("Format data: %s" %[x for x in status])

# Setting Trace
Mname = "S21" #setrace(1, 1)

status = ena.query("SENS:SWE:TYPE?")
print("Sweeping Type: %s" %status)
datapts = ena.query("SENSe:SWEep:POINts?")
print("Sweeping Points#: %s" %datapts)
sweeptime = ena.query("SENS:SWE:TIME?")
print("Sweeping Time: %s" %sweeptime)

fstart = ena.query("SENSe:FREQuency:STARt?")
print("Start Frequency(Hz): %s" %fstart)
fstop = ena.query("SENSe:FREQuency:STOP?")
print("Stop Frequency(Hz): %s" %fstop)

status = ena.query("SENSe:BANDwidth?") #IF Freq
print("Bandwidth (Hz): %s" %status)
status = ena.query("SOURce:POWer?")
print("Power (dBm): %s" %status)

status = ena.write("SENSe:AVER ON") #OFF
print("Set Average ON: %s" %[x for x in status])
Ave_num = 5
status = ena.write("SENSe:AVER:COUN %s" %Ave_num) #Averaged by VNA itself
print("Set Average Number=%s: %s" %(Ave_num, [x for x in status]))
status = ena.write("SENSe:AVER:CLE")
print("Clear Average: %s" %[x for x in status])
status = ena.write("TRIG:SOUR INT;INIT:CONT ON") #INIT:CONT OFF;INIT:IMM
print("Set Continuous: %s" %[x for x in status])

# switch on ena
ena.write('OUTP ON')

# when opc return, the sweep is done
ena.query("*OPC?") 

chnum = 1
# select measurement name
status = ena.write('CALC%d:PAR:SEL %s'%(chnum, Mname))
data = ena.query("CALC%d:DATA:FDATA?"%chnum)
# print(data)
datas = data.split(',')
print("Data-length: %s" %len(datas))
# print(datas)

i, Idata, Qdata = 1, [], []
for x in datas:
    if i%2: #odd
        Idata.append(x)
    else: Qdata.append(x) #even
    i += 1

print("Idata-length: %s" %len(Idata))
yI = [float(i) for i in Idata]
yQ = [float(i) for i in Qdata]
print(yI)
fstart, fstop, datapts = float(fstart), float(fstop), float(datapts)
X = list(arange(fstart, fstop, (fstop-fstart)/(datapts-1))) + [fstop]

# Plotting
fig, ax = plt.subplots(2, 1, sharex=True, sharey=False)
ax[0].set(title="IQ-Data")
ax[0].plot(X, yI)
# ax[0].set(ylabel=r'I-Data (V)')
ax[1].plot(X, yQ)
# ax[1].set(ylabel=r'Q-Data (V)')
# ax[1].set(xlabel=r'$time({\times} 10^{%d}s)$'%(x_order))
[axe.grid(True) for axe in ax]
fig.tight_layout()
plt.show()


# switch off ena
ena.write('OUTP OFF')
ena.close()

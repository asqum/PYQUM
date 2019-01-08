from visa import ResourceManager
from time import sleep

rm = ResourceManager()

ip = "192.168.0.6"
pna = rm.open_resource("TCPIP0::%s::hpib7,16::INSTR" %ip)
pna.read_termination = '\n'
pna.timeout = 8000 #milisecond
pna.write("*RST")

pna.write("FORMat:DATA ASCII,0")
pna.write("SENS:SWE:TYPE LOG")
sweep_type = pna.query("SENS:SWE:TYPE?")
print("sweep type is %s" %sweep_type)

#sweep frequency
pna.write("SENS:FREQuency:STARt 1e9")
pna.write("SENS:FREQuency:STOP 5e9")
start_freq = pna.query("SENS:FREQuency:STARt?")
stop_freq = pna.query("SENS:FREQuency:STOP?")

start_freq = float(start_freq)/1e9
stop_freq = float(stop_freq)/1e9
print("start frequency = %s GHz" %start_freq)
print("stop frequency = %s GHz" %stop_freq)

#sweep point
pna.write("SENSe:SWEep:POINTs 1001")
point = pna.query("SENSe:SWEep:POINTs?")
print("point = %s" %point)

#trigger
pna.write("SENS:SWE:GRO:COUN 10")
pna.write("Trigger:SOUR IMM")

#average
pna.write("SENSe:AVER:COUN 5")
pna.write("SENSe:AVER:CLE")
average = pna.query("SENSe:AVER ON;*OPC?")
print("average on =%s" %average)

#bandwidth
pna.write("SENSe:BANDwidth 10000")#unit is Hz
IFB = pna.query("SENSe:BANDwidth?")
print("IFB =%s Hz" %IFB)

#power
power = pna.query("SOUR1:POW?")
print("power = %s dBm" %power)

#time
time = pna.query("SENS:SWE:TIME?") #unit?
print("time %s ms" %time)
'''
#sweep mode
sweep_mode = pna.query("SENS:SWE:MODE GRO;*OPC?")
print("sweep mode is %s" %sweep_mode)
'''
#data
pna.timeout = 10000
pna.write("CALC1:PAR:SEL 'CH1_S11_1'")
pna.write("CALC1:DATA SDATA 'CH1_S11_1'")
SDATA = pna.query("CALC1:DATA? SDATA")
string = list(SDATA)
results = []
#return every sdata from str to float
for i in range(19):
    results.append(string[i])
print(results)
data_temp = 0
for number in range(16):
    if number==0:
        continue
    if number == 2:
        continue
    if number == 14:
        continue
    elif number==15:
        if results[number]=='-':
            point = -1
        else:
            point = 1
        points = 0
        for ii in range(3):
            points = points+(10**(ii))*int(results[18-ii])
        point = point*points
    elif number==1:
        data_temp = int(results[number])
    else:
        data_temp = data_temp + int(results[number])*(10**(-1*(number-2)))
data_temp = data_temp*(10**(point))
print(data_temp)
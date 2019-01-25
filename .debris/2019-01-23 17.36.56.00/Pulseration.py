import matplotlib.pyplot as plt
from numpy import *
import visa
import time
import csv

# Open Comm
rm = visa.ResourceManager()
rigo = rm.open_resource('TCPIP0::192.168.1.81::INSTR') #establishing LAN connection with RIGOL DS6104
psg = rm.open_resource('TCPIP0::192.168.1.35::INSTR') #establishing LAN connection with PSG E8267D
# psg = rm.open_resource('GPIB0::27::INSTR') #backup by establishing GPIB connection with PSG E8267D

rigo.read_termination = '\n' #omit termination tag from output 
rigo.timeout = 80000 #set timeout
rigo_name = rigo.query('*IDN?') #inquiring psg identity
psg.read_termination = '\n' #omit termination tag from output 
psg.timeout = 8000 #set timeout
psg_name = psg.query('*IDN?') #inquiring psg identity

#Checking Connections & Identities
# print('All connected Instruments:', rm.list_resources())
print([rigo_name, psg_name])

#Clear buffer memory
psg.write('*CLS')
psg.write('*RST') 
rigo.write('*CLS') 

# Run RIGOLSCOPE
rigo.write(':RUN')

# set basics
psg.write(':POWer:LEVel -15.0DBM')
psg.write(':SOUR:FREQ:FIX 300MHZ')

# Setting Pulse Modulation Parameters
psg.write(':SOURce:PULM:SOURce:INTernal FRUN')
psg.write(':PULM:INT:DEL 200E-9')
psg.write(':PULM:INT:FREQ 10HZ') #for continuous square wave modulation
psg.write(':SOURce:PULM:INTernal:PERiod 7 MS')
psg.write(':SOURce:PULM:INTernal:PWIDth 2 MS')
psg.write(':SOURce:PULM:STATe OFF') # Starting Pulse Modulation

# Setting AM Modulation Parameters
psg.write(':SOURce:AM2:DEPTh:LINear 80')
psg.write(':SOURce:AM2:INTernal:SWEep:RATE 700HZ')
psg.write(':SOURce:AM2:INTernal:FUNCtion:SHAPe TRIangle') #TRIangle
psg.write(':SOURce:AM2:STATe OFF')

# setting arbitrary RF modulation
psg.write(':SOURce:RADio:ARB:STATe OFF')

# Fire-up RF
psg.write(':OUTPut:MODulation:STATe ON') #Modulation state in general
psg.write(':OUTPut:STATe ON')

# switch off INSTRUMENTS
# time.sleep(7)
# psg.write('AM:STAT OFF')
# psg.write(':OUTPut:MODulation:STATe OFF')
# psg.write(':OUTPut:STATe OFF')

# Data extraction from RIGOL
scal = rigo.query(':CHAN1:SCAL?')
print([scal])
rigo.write(':ACQuire:TYPE NORMal')
rigo.write(':WAV:POIN:MODE RAW') # to maximum memory depth
rigo.write(':WAV:MODE MAX') # taking data on screen while in RUN mode
rigo.write(':WAV:FORM ASCii')
# rigo.write(':STOP') # Acquire
rigo.write(':WAVeform:SOURCE CHAN1')
wave = rigo.query(':WAVeform:DATA?')
print(len(wave))
# print(wave)
wavef = wave.split(",")
# print(wavef)
wavefo = [float(x) for x in wavef[0:len(wavef)-1]] # to avoid the last empty string
print(sum(wavefo))

# Plotting
t = arange(0, len(wavefo), 1)
fig, ax = plt.subplots()
ax.plot(t, wavefo)
ax.set(xlabel='arb. time', ylabel='voltage (mV)',
       title='Modulated Waveform')
# fig.savefig("rigol05.png")
plt.show()

# Close Comm
psg.write('SYSTem:COMMunicate:GTLocal')
psg.close()
rigo.close()

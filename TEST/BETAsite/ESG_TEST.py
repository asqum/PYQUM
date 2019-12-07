# ESG TEST:
import matplotlib.pyplot as plt
import visa, time
import numpy as np

# esg
rm = visa.ResourceManager()
esg = rm.open_resource('GPIB0::27::INSTR') #establishing connection using GPIB# with the machine
esg.read_termination = '\n' #omit termination tag from output 
esg.timeout = 8000 #set timeout

#Checking Connections & Identities
print(esg.query('*IDN?'))  #inquiring machine identity: "who r u?"

#Clear buffer memory
esg.write('*CLS')
esg.write('*RST')

# set basics
fa = 3
powa = -5.0
esg.write(':POWer:LEVel %sDBM' %powa)
esg.write(':SOUR:FREQ:FIX %sGHZ' %fa)
print('Power: %s' %(esg.query(':SOUR:POW:LEV?')))
print('Frequency: %s' %(esg.query(':SOUR:FREQ?')))

# switch on ESG
esg.write('OUTP ON')
print('STATE: %s' %(esg.query(':OUTPut:STATe?')))



esg.write('OUTP OFF')
print('STATE: %s' %(esg.query(':OUTPut:STATe?')))
esg.close()



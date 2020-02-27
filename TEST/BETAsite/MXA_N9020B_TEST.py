'''
KeySight Spectrum Analyzer (up to 26.5GHz)
'''

import visa
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

rm = visa.ResourceManager()
inst = rm.open_resource('TCPIP0::192.168.1.109::INSTR')
inst.timeout = 5000000 #set timeout in ms
inst.write_termination = '\n'
print(inst.query("*IDN?"))

freq_cent = 5.5e9
span = 0.2e9
f = np.linspace(freq_cent-span/2, freq_cent+span/2, 1001, endpoint = True)

inst.write(":INIT:CONT ON")
# inst.write("SYST:SCPI:DISP ON")
inst.write(":FREQ:CENT %s" %freq_cent)
inst.write(":FREQ:SPAN %s" %span)
# inst.write(":FREQ:CENT %s;SPAN %s" %('5.525GHz',span))
inst.write(":BANDwidth:RESolution %s" %1e6)
inst.write(":BANDwidth:VIDeo %s" %1e5)

# inst.write("*SRE 128")
# print("Ready: %s" %inst.query('*STB?'))
# sleep(1)
for i in range(2):
    inst.write(":FORM:TRAC:DATA ASCii")
    values = inst.query_ascii_values(':TRAC:DATA? TRACE1', container=np.array)
# print("DONE with length %s: %s" %(len(values),(values)))

plt.plot(f, values, 'k')
plt.xlabel ('Frequency (Hz)')
plt.ylabel ('Power (dBm)')
plt.show()

inst.query('*OPC?')
inst.write(":CALC:MARK1:MODE POS")
inst.write(":CALC:MARK1:X 5.5GHz")
print(inst.query(":CALCulate:MARKer1:Y?"))

# fileobject = open(file1, r, 1)
# fileobject.read()
# fileobject.seek(1, 1)

# f = int('01000001101011000111101011100001', 2)
# print(struct.unpack('f', struct.pack('I', f))[0])
# a1 = []
# for i in range(5):
#     a1.append(i*4)

# print(a1)

inst.close()

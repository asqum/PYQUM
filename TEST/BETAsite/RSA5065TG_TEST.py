'''
Prerequisition: NI-MAX, NI-488.2, NI-VISA, NI-DAQ, pip install pyvisa
If problems persist:
1. BOTH PC and Instrument have to be restarted;
   this is to resolve the conflict between visa-objects.
2. Plug the usb cable into the port of rear panel.
'''

import visa
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

rm = visa.ResourceManager()
# inst = rm.open_resource('USB0::0x1AB1::0x0968::RSA5B212300041::INSTR')
inst = rm.open_resource('TCPIP0::192.168.1.157::INSTR')
inst.timeout = 5000000 #set timeout in ms
inst.write_termination = '\n'
# inst.set_visa_attribute(visa.constants.VI_ATTR_SEND_END_EN, False)
# inst.set_visa_attribute(visa.constants.VI_ATTR_TERMCHAR_EN, True) #termination character disabled
# inst.set_visa_attribute(visa.constants.VI_ATTR_TERMCHAR, 0xA)
# inst.read_termination = '\n' #omit termination tag from output
# print("USB Protocol: %s" %inst.get_visa_attribute(visa.constants.VI_ATTR_USB_PROTOCOL))
# print("RSC LOCK-STATE: %s" %inst.get_visa_attribute(visa.constants.VI_ATTR_RSRC_LOCK_STATE))
# print("SEND END: %s" %inst.get_visa_attribute(visa.constants.VI_ATTR_SEND_END_EN))
# print("MAX QUEUE LENGTH: %s" %inst.get_visa_attribute(visa.constants.VI_ATTR_MAX_QUEUE_LENGTH))
# print("MAX INTERRUPT: %s" %inst.get_visa_attribute(visa.constants.VI_ATTR_USB_MAX_INTR_SIZE))
# print("IO PROTOCOL: %s" %inst.get_visa_attribute(visa.constants.VI_ATTR_IO_PROT))
# print("TERMINATION CHARACTER ENABLED: %s" %inst.get_visa_attribute(visa.constants.VI_ATTR_TERMCHAR_EN), "\n")

freq_cent = 3e9
span = 6e9
f = np.linspace(freq_cent-span/2, freq_cent+span/2, 801, endpoint = True)

inst.write("SYST:SCPI:DISP ON")
inst.write(":FREQ:CENT %s" %freq_cent)
inst.write(":FREQ:SPAN %s" %span)
inst.write(":INIT:CONT OFF")
inst.write(":FORM:TRAC:DATA ASCii")
values = inst.query_ascii_values(':TRAC:DATA? TRACE1', container=np.array)
print("DONE with length %s: %s" %(len(values),(values)))

plt.plot(f, values, 'k')
plt.xlabel ('Frequency (Hz)')
plt.ylabel ('Power (dBm)')
plt.show()

# inst.write(":CALC:MARK<1>:MODE POS")
# inst.write(":CALC:MARK<1>:X 3e9")
# print(inst.query(":CALCulate:MARKer<1>:Y?"))

# fileobject = open(file1, r, 1)
# fileobject.read()
# fileobject.seek(1, 1)

# f = int('01000001101011000111101011100001', 2)
# print(struct.unpack('f', struct.pack('I', f))[0])
# a1 = []
# for i in range(5):
#     a1.append(i*4)

# print(a1)
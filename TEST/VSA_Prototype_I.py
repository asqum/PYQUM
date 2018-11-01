# This prototype uses heavy hybrid with VI
import matplotlib.pyplot as plt
import visa, time
import numpy as np
# from Callout import Call_VI
from NImodules import *

# vsa
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

# Calling VSA control on-off.vi
# VSA_control(True)

# Calling AWG waveform sequence.vi
AWG_state = AWG_Seq(True)
print('AWG: ', AWG_state)

# Calling AWG Generate waveform.vi
CH1 = [1000, 8000, 40000]
CH2 = [400, 8000, 40000]
waveforms = [CH1, CH2]
timeseq = AWG_Gen(waveforms)
print("time sequence: ", timeseq[0][1])

# Calling measure VSA one curve no log.vi
Acqtime = (2*timeseq[0][0] + timeseq[0][1]) * 1e-6
# Acqtime = 2e-5
datapoints = 1000
Bndwidth = datapoints / Acqtime / 1000
# Parameters=[fa, powa, Acqtime, Bndwidth]
Parameters = [[fa, Bndwidth, powa, Acqtime]] # Format updated by Watson's Lab
# print(Parameters)

avenum = 13; # averaging times
#setting up figure
t = np.linspace(0, Acqtime, 2*datapoints) / 1e-6  # micro sec # len(Idata)
Idatacc = np.zeros(2 * datapoints)
Qdatacc = np.zeros(2 * datapoints) # Idatacc
for i in range(avenum):
    # Start digitizing (measuring)
    start = time.time()
    IQdata = DigitizeIQ(Parameters)
    IQdata = np.array(IQdata)
    # print(IQdata.shape)

    Idata = IQdata[0][0]
    Qdata = IQdata[0][1]
    
    Idatacc += Idata
    Qdatacc += Qdata

    Idata = Idatacc / (i + 1)
    Qdata = Qdatacc / (i + 1)

    end = time.time()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set(xlabel='t($\mu s$)', ylabel='I/Q(mV)', title='IQ Modulated Waveform')
    ax.plot(t, Idata)
    ax.plot(t, Qdata)
    print("#%s loop: %ss" % (i, end - start))
    plt.ioff()
    plt.show()
    # fig.canvas.draw()
    # time.sleep(0.3)
    # plt.clf()

#fig.savefig("vsaprototype(I).png")

# VSA_control(False)

esg.write('OUTP OFF')
print('STATE: %s' %(esg.query(':OUTPut:STATe?')))
esg.close()



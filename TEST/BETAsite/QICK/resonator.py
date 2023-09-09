from tmpqcs.qcontrol import QProgram, ForLoop, Variable
from tmpqcs.backendMgr.qickBackend import QickSCBackend
from tmpqcs.backendMgr.zcu216_qick1 import *
import matplotlib.pyplot as plt
import time
import numpy as np 

myqick = QickSCBackend()
myqick.connect('myqick',ns_ip ='192.168.1.98') 
ro = myqick.add_readout('ro',[ADC226_0, ADC226_2], DAC230_0)
ro.set_freq(100)
ro.set_phase(0)
ro.add_const('ro_const',length= 0.5, gain = 32766)
ro.set_readout_length(0.8)
loops = 10
with QProgram(myqick) as prog:
    repts = Variable('int')
    with ForLoop(repts, repeat = 1):
        prog.play_waveform(ro, 'ro_const')
        prog.measure(ch = ro, trigger_delay=0.05, relax_delay=20)


freq_list = np.linspace(1, 2000, loops)
index = 0
amp = np.zeros(2)
for index in range(loops):
    ro.set_freq(freq_list[index])
    datai, dataq = myqick.run_get_singleIQ(prog=prog)
    amptemp = np.sqrt(datai*datai + dataq*dataq).reshape(1, -1)
    amp = np.vstack((amp, amptemp))
amp = amp.T[:,1:]
plt.plot(freq_list, amp[0])
plt.plot(freq_list, amp[1])
plt.show()


from tmpqcs.qcontrol import QProgram, ForLoop, Variable
from tmpqcs.backendMgr.qickBackend import QickSCBackend
from tmpqcs.backendMgr.zcu216_qick1 import *
import matplotlib.pyplot as plt
import time
import numpy as np 

myqick = QickSCBackend()
myqick.connect('myqick',ns_ip ='192.168.1.98')
q1 = myqick.add_qubit('q1') 
xy = q1.add_channel('xy', DAC230_2)
xy.set_freq(4000)
xy.set_nqz(2)
xy.set_phase(0)
xy.set_gain(32766)
xy.add_gauss('pi', sigma=0.05, length = 0.2, gain = 32766)
ro = myqick.add_readout('ro',[ADC226_0], DAC230_0)
ro.set_freq(150)
ro.set_phase(0)
ro.add_const('ro_const',length= 0.5, gain = 32766)

ro.set_readout_length(0.3)

with QProgram(myqick) as prog:
    repts = Variable('int')
    tau = Variable('fixed')
    with ForLoop(repts, repeat = 40):
        with ForLoop(tau, start = 0, stop = 0.1, loops = 100):
            prog.play_waveform(q1.xy, 'pi')
            
            prog.sync(tau, xy)
            prog.play_waveform(ro, 'ro_const')
            prog.measure(ch = ro, trigger_delay=0.05, relax_delay=50)

myqick.run_get_datas(prog)
plt.ion()
fig = plt.figure()
axis = fig.add_subplot(111)
time.sleep(1)
count = 0
print("repeat in repts",repts.repeat)
while count < repts.repeat:
    data2d, count = myqick.get_datas()
    axis.clear()
    axis.plot(data2d[0,0,:,0])
    axis.plot(data2d[0,0,:,1])
    print("count=", count)
    plt.draw()
    plt.pause(20)
plt.ioff()
plt.show()


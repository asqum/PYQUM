from tmpqcs.qcontrol import QProgram, ForLoop
from tmpqcs.backendMgr.qickBackend import QickSCBackend
from tmpqcs.backendMgr.zcu216_qick1 import *
import matplotlib.pyplot as plt


myqick = QickSCBackend()


ro = myqick.add_readout('ro', [ADC226_0], DAC230_0)
ro.set_freq(300)
ro.set_phase(0)
ro.add_const(name ='const', length = 0.5, gain = 30000)
ro.add_gauss(name = 'gauss', sigma = 0.1, length = 4*0.15, gain = 30000)
ro.set_readout_length(0.8)


# myqick.testmode = False
# run = True
soc = myqick.connect('myqick', ns_ip ='192.168.1.98')

with QProgram(myqick) as prog: 
    repts = prog.declare_var('int')
    with ForLoop(repts, repeat = 1):
        prog.play_waveform(myqick.ro, 'const')
        prog.measure(ch=myqick.ro, trigger_delay=0.2, relax_delay= 0.1)



repeat = 1
myqick.run_get_waveform(prog, repts= repeat)
readcount = 0
plt.ion()
fig = plt.figure()
axis = fig.add_subplot(111)

while readcount < repeat:
    data, readcount = myqick.get_waveform()
    axis.clear()
    # print(data)
    axis.plot(data[0])
    plt.draw()
    plt.pause(0.5)
plt.ioff()
plt.show()


    

    
# # print("finished")









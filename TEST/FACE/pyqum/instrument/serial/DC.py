import nidaqmx
from nidaqmx.system import System

sys = System.local()
for i,dev in enumerate(sys.devices):
    print("%s. %s" %(i,dev))

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    V = task.read()

print("V: %sV" %V)
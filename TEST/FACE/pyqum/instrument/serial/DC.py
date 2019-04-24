import nidaqmx
from nidaqmx.system import System
from nidaqmx.constants import TerminalConfiguration, AcquisitionType
from nidaqmx.stream_readers import AnalogSingleChannelReader
from numpy import ndarray

from pyqum.instrument.analyzer import curve
from pyqum.instrument.toolbox import waveform

D = []
sys = System.local()
for i,dev in enumerate(sys.devices):
    print("%s. %s" %(i+1,dev.name))
    D.append(dev.name)
device = sys.devices[(D[0])]
print(device)

X = waveform("0 to 10 *10 to 0 * 1500")
# print("X: %s" %X)
V = []
with nidaqmx.Task() as write_task, nidaqmx.Task() as read_task:
    write_task.ao_channels.add_ao_voltage_chan("Dev1/ao0")
    # write_task.timing.cfg_samp_clk_timing(rate=1000, sample_mode=AcquisitionType.CONTINUOUS)
    read_task.ai_channels.add_ai_voltage_chan("Dev1/ai0", terminal_config=TerminalConfiguration.RSE, min_val=-10, max_val=10)
    # read_task.timing.cfg_samp_clk_timing(rate=1000)
    for x in X:
        write_task.write(x, auto_start=True)
        V += read_task.read(1)
        # stream
        # reader = AnalogSingleChannelReader(read_task.in_stream)
        # read_task.timing.cfg_implicit_timing(samps_per_chan=8)
        # VS = reader.read_many_sample(ndarray(8))

# print("V: %s" %V)
# print("VS: %sV" %VS)

curve(range(len(X)), X, "", "#", "Aout(V)")
curve(range(len(V)), V, "", "#", "Ain(V)")
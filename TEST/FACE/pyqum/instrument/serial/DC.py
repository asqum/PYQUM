import nidaqmx, random

from nidaqmx.system import System
from nidaqmx.constants import TerminalConfiguration, AcquisitionType, Edge
from nidaqmx.utils import flatten_channel_string

from nidaqmx.stream_readers import (
    AnalogSingleChannelReader, AnalogMultiChannelReader)
from nidaqmx.stream_writers import (
    AnalogSingleChannelWriter, AnalogMultiChannelWriter)

from numpy import ndarray, array, zeros
from pyqum.instrument.analyzer import curve
from pyqum.instrument.toolbox import waveform

D = []
sys = System.local()
for i,dev in enumerate(sys.devices):
    print("%s. %s" %(i+1,dev.name))
    D.append(dev.name)
device = sys.devices[(D[0])]
print(device)

X0, X1 = waveform("0 to 10 *10 to 0 * 20"), waveform("0 to 5 *7 to 10*13 to 0 * 10")
X = list(array([X0.data, X1.data]).T)
V0, V1 = [], []
with nidaqmx.Task() as write_task, nidaqmx.Task() as read_task:
    write_task.ao_channels.add_ao_voltage_chan("Dev1/ao0, Dev1/ao1")
    read_task.ai_channels.add_ai_voltage_chan("Dev1/ai0:1", 
        terminal_config=TerminalConfiguration.RSE, min_val=-10, max_val=10)
    print("First reading: %sV" %read_task.read(1))
    for x in X:
        write_task.write(list(x), auto_start=True)
        v = read_task.read(1)
        V0 += v[0]
        V1 += v[1]

print(V1)
curve([range(X0.count),range(len(V0))], [X0.data,V0], "Channel #0", "arb time", "V(V)", ["-k","or"])
curve([range(X1.count),range(len(V1))], [X1.data,V1], "Channel #1", "arb time", "V(V)", ["-k","or"])

# stream data
X0, X1 = waveform("0 to 10 *10 to 0 * 20"), waveform("0 to 5 *7 to 10*13 to 0 * 10")
X = array([X0.data, X1.data])
number_of_samples = X0.count #should be the same for both channels
print("X:\n%s" %X)
sample_rate = 10 #max 500K over all channels
with nidaqmx.Task() as write_task, nidaqmx.Task() as read_task, \
        nidaqmx.Task() as sample_clk_task:
        # Use a counter output pulse train task as the sample clock source
        # for both the AI and AO tasks.
        # duty cycle = pulse width / pulse period
        sample_clk_task.co_channels.add_co_pulse_chan_freq(
            '{0}/ctr0'.format("Dev1"), freq=sample_rate, initial_delay=0, duty_cycle=0.5)
        sample_clk_task.timing.cfg_implicit_timing(
            sample_mode=AcquisitionType.FINITE,
            samps_per_chan=number_of_samples)

        samp_clk_terminal = '/{0}/Ctr0InternalOutput'.format("Dev1")

        write_task.ao_channels.add_ao_voltage_chan(
            "Dev1/ao0:1", max_val=10, min_val=-10)
        write_task.timing.cfg_samp_clk_timing(
            sample_rate, source=samp_clk_terminal, active_edge=Edge.RISING,
            samps_per_chan=number_of_samples)
        # write_task.ao_channels.add_ao_func_gen_chan

        read_task.ai_channels.add_ai_voltage_chan(
            "Dev1/ai0:1", terminal_config=TerminalConfiguration.RSE, max_val=10, min_val=-10)
        read_task.timing.cfg_samp_clk_timing(
            sample_rate, source=samp_clk_terminal,
            active_edge=Edge.FALLING, samps_per_chan=number_of_samples)
        # read_task.channels.ai_averaging_win_size = 3 #FPGA

        # Single Channel:
        # writer = AnalogSingleChannelWriter(write_task.out_stream)
        # reader = AnalogSingleChannelReader(read_task.in_stream)

        # Multi Channel:
        writer = AnalogMultiChannelWriter(write_task.out_stream)
        reader = AnalogMultiChannelReader(read_task.in_stream)

        # start writing waveform into AO
        writer.write_many_sample(X)

        # Start the read and write tasks before starting the sample clock
        # source task.
        read_task.start()
        write_task.start()
        sample_clk_task.start()

        V = zeros((2,number_of_samples))
        reader.read_many_sample(
            V, number_of_samples_per_channel=number_of_samples,
            timeout=88)

        # print(V)

print(range(V.size))
curve([range(X0.count),range(V[0].size)], [X0.data,list(V[0])], "Channel #0", "arb time", "V(V)", ["-k","or"])
curve([range(X1.count),range(V[1].size)], [X1.data,list(V[1])], "Channel #1", "arb time", "V(V)", ["-k","or"])


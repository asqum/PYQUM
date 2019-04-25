import nidaqmx, random

from nidaqmx.system import System
from nidaqmx.constants import TerminalConfiguration, AcquisitionType, Edge

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

X = waveform("0 to 10 *10 to 0 * 20")
# print("X: %s" %X)
V = []
with nidaqmx.Task() as write_task, nidaqmx.Task() as read_task:
    write_task.ao_channels.add_ao_voltage_chan("Dev1/ao0")
    read_task.ai_channels.add_ai_voltage_chan("Dev1/ai0", terminal_config=TerminalConfiguration.RSE, min_val=-10, max_val=10)
    for x in X:
        write_task.write(x, auto_start=True)
        V += read_task.read(1)

# print("V: %s" %V)
curve(range(len(X)), X, "", "#", "Aout(V)")
curve(range(len(V)), V, "", "#", "Ain(V)")

# stream data
number_of_samples = 3502
print("number of samples: %s" %number_of_samples)
sample_rate = 5000 #random.uniform(1000, 5000)
with nidaqmx.Task() as write_task, nidaqmx.Task() as read_task, \
        nidaqmx.Task() as sample_clk_task:

        # Use a counter output pulse train task as the sample clock source
        # for both the AI and AO tasks.
        sample_clk_task.co_channels.add_co_pulse_chan_freq(
            '{0}/ctr0'.format("Dev1"), freq=sample_rate)
        sample_clk_task.timing.cfg_implicit_timing(
            samps_per_chan=number_of_samples)

        samp_clk_terminal = '/{0}/Ctr0InternalOutput'.format("Dev1")

        write_task.ao_channels.add_ao_voltage_chan(
            "Dev1/ao0", max_val=10, min_val=-10)
        write_task.timing.cfg_samp_clk_timing(
            sample_rate, source=samp_clk_terminal, active_edge=Edge.RISING,
            samps_per_chan=number_of_samples)

        read_task.ai_channels.add_ai_voltage_chan(
            "Dev1/ai0", max_val=10, min_val=-10)
        read_task.timing.cfg_samp_clk_timing(
            sample_rate, source=samp_clk_terminal,
            active_edge=Edge.FALLING, samps_per_chan=number_of_samples)

        writer = AnalogSingleChannelWriter(write_task.out_stream)
        reader = AnalogSingleChannelReader(read_task.in_stream)

        # start writing waveform into AO
        X = array(waveform("0 to 10 *%s to 0 * %s" %(round(number_of_samples/2), number_of_samples-round(number_of_samples/2))))
        # X = array([random.uniform(-10, 10) for _ in range(number_of_samples)],dtype=float64)
        writer.write_many_sample(X)

        # Start the read and write tasks before starting the sample clock
        # source task.
        read_task.start()
        write_task.start()
        sample_clk_task.start()

        V = zeros(number_of_samples)
        reader.read_many_sample(
            V, number_of_samples_per_channel=number_of_samples,
            timeout=2)

        print(V)

curve(range(len(X)), X, "", "#", "Aout(V)")
curve(range(len(V)), V, "", "#", "Ain(V)")

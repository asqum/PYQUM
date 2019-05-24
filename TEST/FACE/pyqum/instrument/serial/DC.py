'''Communicating with DC-Box'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # instrument-module's name e.g. ENA, PSG, YOKO

import nidaqmx, random
from nidaqmx.constants import TerminalConfiguration, AcquisitionType, Edge
from nidaqmx.utils import flatten_channel_string

from nidaqmx.stream_readers import (
    AnalogSingleChannelReader, AnalogMultiChannelReader)
from nidaqmx.stream_writers import (
    AnalogSingleChannelWriter, AnalogMultiChannelWriter)

from numpy import ndarray, array, zeros

from pyqum.instrument.logger import address
from pyqum.instrument.analyzer import curve
from pyqum.instrument.toolbox import waveform

# INITIALIZATION
def openall():
    ad = address()
    rs = ad.lookup(mdlname) # Instrument's Address
    write_task = nidaqmx.Task()
    write_task.ao_channels.add_ao_voltage_chan("Dev1/ao0:3")
    read_task = nidaqmx.Task()
    read_task.ai_channels.add_ai_voltage_chan("Dev1/ai0:31", terminal_config=TerminalConfiguration.RSE, min_val=-10, max_val=10)
    return write_task, read_task

w, r = openall()

print("Previous Reading:")
for i,v in enumerate(r.read(1)):
    print("AI%s: %sV" %(i,v[0]))

w.write([0, 0, 0, 0], auto_start=True)
v = r.read(1)

print("\nReading Now:")
for i,v in enumerate(v):
    print("AI%s: %sV"%(i,v[0]))

w.close()
r.close()

A = input("pause")

# def apply_voltage()

X0 = waveform("10")#, waveform("10")
# X = list(array([X0.data, X1.data]).T)
V0, V1 = [], []
with nidaqmx.Task() as write_task, nidaqmx.Task() as read_task:
    write_task.ao_channels.add_ao_voltage_chan("Dev1/ao0")
    read_task.ai_channels.add_ai_voltage_chan("Dev1/ai0:31", 
        terminal_config=TerminalConfiguration.RSE, min_val=-10, max_val=10)

    print("Previous Reading:")
    for i,v in enumerate(read_task.read(1)):
        print("AI%s: %sV" %(i,v[0]))
    # for x in X0:
    write_task.write([0], auto_start=True)
    v = read_task.read(1)
    # V0 += v[0]
    # V1 += v[1]
    print("\nReading Now:")
    for i,v in enumerate(v):
        print("AI%s: %sV"%(i,v[0]))

A = input("pause")

# print(V1)
# curve([range(X0.count),range(len(V0))], [X0.data,V0], "Channel #0", "arb time", "V(V)", ["-k","or"])
# curve([range(X1.count),range(len(V1))], [X1.data,V1], "Channel #1", "arb time", "V(V)", ["-k","or"])

# stream data
X0, X1, X3 = waveform("0 to 10 *1000 to 0 * 2000"), waveform("0 to 5 *700 to 10*1300 to 0 * 1000"), waveform("0 to 3 *700  to 1*1500 to 7*500 to 0 * 300")
X = array([X0.data, X1.data, X3.data])
number_of_samples = X0.count #should be the same for both channels
print("X:\n%s" %X)
sample_rate = 10000 #max 500K over all channels
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
            "Dev1/ao0:1, Dev1/ao3", max_val=10, min_val=-10)
        write_task.timing.cfg_samp_clk_timing(
            sample_rate, source=samp_clk_terminal, active_edge=Edge.RISING,
            samps_per_chan=number_of_samples)
        # write_task.ao_channels.add_ao_func_gen_chan

        read_task.ai_channels.add_ai_voltage_chan(
            "Dev1/ai0:1, Dev1/ai17", terminal_config=TerminalConfiguration.RSE, max_val=10, min_val=-10)
        read_task.timing.cfg_samp_clk_timing(
            sample_rate, source=samp_clk_terminal,
            active_edge=Edge.FALLING, samps_per_chan=number_of_samples)
        # read_task.channels.ai_averaging_win_size = 3 #FPGA
        print("Max reading rate: %s" %read_task.timing.samp_clk_max_rate)

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

        V = zeros((3,number_of_samples))
        reader.read_many_sample(
            V, number_of_samples_per_channel=number_of_samples,
            timeout=88)

        # print(V)

print(range(V.size))
curve([range(X0.count),range(V[0].size)], [X0.data,list(V[0])], "Channel #0", "arb time", "V(V)", ["-k","or"])
curve([range(X1.count),range(V[1].size)], [X1.data,list(V[1])], "Channel #1", "arb time", "V(V)", ["-k","or"])
curve([range(X3.count),range(V[2].size)], [X3.data,list(V[2])], "Channel #3->17", "arb time", "V(V)", ["-k","or"])


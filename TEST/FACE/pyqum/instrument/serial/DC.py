'''Communicating with DC-Box'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # instrument-module's name e.g. ENA, PSG, YOKO

import nidaqmx, inspect, json

from nidaqmx.constants import TerminalConfiguration, AcquisitionType, Edge
from nidaqmx.utils import flatten_channel_string
from nidaqmx.stream_readers import (AnalogSingleChannelReader, AnalogMultiChannelReader)
from nidaqmx.stream_writers import (AnalogSingleChannelWriter, AnalogMultiChannelWriter)

from numpy import ndarray, array, zeros
from pathlib import Path

from pyqum.instrument.logger import address
from pyqum.instrument.analyzer import curve
from pyqum.instrument.toolbox import waveform, match

__author__ = "Teik-Hui Lee"
__copyright__ = "Copyright 2019, The Pyqum Project"
__credits__ = ["Chii-Dong Chen"]
__license__ = "GPL"
__version__ = "beta3"
__email__ = "teikhui@phys.sinica.edu.tw"
__status__ = "development"

pyfilename = inspect.getfile(inspect.currentframe()) # current pyscript filename (usually with path)

# INITIALIZATION
def openall(aoi=0, aof=3, aii=0, aif=31, read=True, write=False):
    '''
    4 output channels, 32 input channels
    '''
    ad = address()
    rs = ad.lookup(mdlname) # Instrument's Address
    write_task, read_task = None, None
    if write:
        write_task = nidaqmx.Task()
        write_task.ao_channels.add_ao_voltage_chan("%s/ao%s:%s" %(rs,aoi,aof))
    if read:
        read_task = nidaqmx.Task()
        read_task.ai_channels.add_ai_voltage_chan("%s/ai%s:%s" %(rs,aii,aif), terminal_config=TerminalConfiguration.RSE, min_val=-10, max_val=10)
    return write_task, read_task

def closeall(w, r):
    w.close()
    r.close()
    return

class amplifier:
    def __init__(self):
        self.sense = openall(aof=1, aii=6, aif=15)[1]
        with open(Path(pyfilename).parent / 'calibration.json') as ad:
            self.book = json.load(ad)

    def sensehardpanel(self):
        '''Indicating Amplifier Settings on Hard Front-panel
        '''
        vis = self.sense.read(1)
        self.VSupplyP, self.VSupplyN, self.VSym, self.VDiv, self.VRb, self.VBiasMode, self.VVGain1, self.VVGain2, self.VVgMode1, self.VVgMode2 = vis[0:10]
        self.SupplyP = bool(self.book['DC']['Power']['State'][match(self.book['DC']['Power']['ai6'], self.VSupplyP)])
        self.SupplyN = bool(self.book['DC']['Power']['State'][match(self.book['DC']['Power']['ai7'], self.VSupplyN)])
        self.Symmetry = str(self.book['DC']['Symmetry']['mode'][match(self.book['DC']['Symmetry']['ai8'], self.VSym)])
        self.Division = float(self.book['DC']['Div']['ratio'][match(self.book['DC']['Div']['ai9'], self.VDiv)])
        self.Rb = int(self.book['DC']['Rb']['order'][match(self.book['DC']['Rb']['ai10'], self.VRb)])
        self.BiasMode = str(self.book['DC']['Bias']['mode'][match(self.book['DC']['Bias']['ai11'], self.VBiasMode)])
        self.VGain1 = int(self.book['DC']['Vgain1']['gain'][match(self.book['DC']['Vgain1']['ai12'], self.VVGain1)])
        self.VGain2 = int(self.book['DC']['Vgain2']['gain'][match(self.book['DC']['Vgain2']['ai13'], self.VVGain2)])
        self.VgMode1 = str(self.book['DC']['Vg']['mode'][match(self.book['DC']['Vg']['ai-value'], self.VVgMode1)])
        self.VgMode2 = str(self.book['DC']['Vg']['mode'][match(self.book['DC']['Vg']['ai-value'], self.VVgMode2)])

    def close(self):
        self.sense.close()


# w.write([0, 0, 0, 0], auto_start=True)

def test():
    A = amplifier()
    for i in range(3):
        print("\nSensing Hard Panel #%s:" %(i+1))
        A.sensehardpanel()
        print("SupplyP: %s" %A.SupplyP)
        print("SupplyN: %s" %A.SupplyN)
        print("Symmetry: %s" %A.Symmetry)
        print("Division: %s" %A.Division)
        print("Rb: %s" %10**A.Rb)
        print("Bias Mode: %s" %A.BiasMode)
        print("V Gain 1: %s" %A.VGain1)
        print("V Gain 2: %s" %A.VGain2)
        print("Vg Mode 1: %s" %A.VgMode1)
        print("Vg Mode 2: %s" %A.VgMode2)
    A.close()

test()

A = input("pause")

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


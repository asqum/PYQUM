# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 15:05:24 2022

@author: zhinst

Requirements:

    LabOne Version >= 22.02
    Instruments: 1 x SHFQC Instrument
"""
# In[1]

from zhinst.toolkit import Session, SHFQAChannelMode

session = Session("localhost")
device = session.connect_device("DEV12139")

# In[2] Parameter

qachannel_center_frequency = 7.1e9
qachannel_power_in = 5
qachannel_power_out = 0

max_amplitude_readout = 1

# In[3] Device configuration

device.qachannels[0].configure_channel(
    center_frequency=qachannel_center_frequency,
    input_range=qachannel_power_in,
    output_range=qachannel_power_out,
    mode=SHFQAChannelMode.SPECTROSCOPY,
)

# In[4] Sweeper configuration

sweeper = session.modules.shfqa_sweeper
sweeper.device(device)

sweeper.rf.center_freq(qachannel_center_frequency)
sweeper.rf.input_range(qachannel_power_in)
sweeper.rf.output_range(qachannel_power_out)

sweeper.sweep.start_freq(-700e6)
sweeper.sweep.stop_freq(700e6)
sweeper.sweep.num_points(1001)
sweeper.sweep.mapping("linear")
sweeper.sweep.oscillator_gain(max_amplitude_readout)
sweeper.sweep.mode(True)

sweeper.average.integration_time(10000e-6)
sweeper.average.num_averages(1)
sweeper.average.mode("cyclic")

# In[5] Run Sweep

device.qachannels[0].input.on(1)
device.qachannels[0].output.on(1)

wide_resonator_spectrum = sweeper.run()

device.qachannels[0].input.on(0)
device.qachannels[0].output.on(0)

# In[6] Results

# use sweeper plotting function
sweeper.plot()

# custom-made plot with data conversion and slope compensation

slope = 0.03

import matplotlib.pyplot as plt
from shfqc_helper import voltage_to_power_dBm, voltage_to_phase

xaxis = sweeper.get_offset_freq_vector() / 10 ** 6
fig1, axs = plt.subplots(1, 2, figsize=(24,10))
axs[0].plot(xaxis, voltage_to_power_dBm(wide_resonator_spectrum["vector"]))
axs[0].set_xlabel("frequency [MHz]", fontsize=30)
axs[0].set_ylabel("amplitude [dBm]", fontsize=30)
axs[0].tick_params(axis="both", which="major", labelsize=30)

axs[1].plot(
    xaxis, voltage_to_phase(wide_resonator_spectrum["vector"]) + xaxis * slope
)
axs[1].set_xlabel("frequency [MHz]", fontsize=30)
axs[1].set_ylabel("phase [rad]", fontsize=30)
axs[1].tick_params(axis="both", which="major", labelsize=30)
plt.show()
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 15:37:41 2022

@author: zhinst

Requirements:

    LabOne Version >= 22.02
    Instruments: 1 x SHFQC Instrument

"""
# In[1]

from zhinst.toolkit import Session, SHFQAChannelMode

session = Session("localhost")
device = session.connect_device("DEV12131")

# In[2] Parameter

number_of_qubits = 1

qachannel_center_frequency = 6.4e9
qachannel_power_in = -50
qachannel_power_out = -30

max_amplitude_readout = 1 / number_of_qubits # * 0.98

# Sweep Parameter
qubit_readout_frequencies = [-1e6]
qubit_readout_widths = [4e6]
number_amplitude_values = 20
average_factor = 1e-6 # if set to 1, scales averages with amplitude

# In[3] Device configuration

device.qachannels[0].configure_channel(
    center_frequency=qachannel_center_frequency,
    input_range=qachannel_power_in,
    output_range=qachannel_power_out,
    mode=SHFQAChannelMode.SPECTROSCOPY,
)

# In[4] Sweeper configuration

# initiates sweeper parameters
sweeper = session.modules.shfqa_sweeper
sweeper.device(device)

sweeper.rf.center_freq(qachannel_center_frequency)
sweeper.rf.input_range(qachannel_power_in)
sweeper.rf.output_range(qachannel_power_out)

# sweeper.sweep.start_freq(-700e6)
# sweeper.sweep.stop_freq(700e6)
sweeper.sweep.num_points(3001)
sweeper.sweep.mapping("linear")
sweeper.sweep.oscillator_gain(max_amplitude_readout)
sweeper.sweep.mode(True)

sweeper.average.integration_time(1000e-6)
sweeper.average.num_averages(1)
sweeper.average.mode("cyclic")

# In[5] Measure each resonator with different powers

import sys
import os
import numpy as np

resonator_spectrum_data = {"qubits": [[]] * number_of_qubits}
relative_amplitude_values = np.linspace(
    max_amplitude_readout / number_amplitude_values,
    max_amplitude_readout,
    number_amplitude_values,
)

device.qachannels[0].input.on(1)
device.qachannels[0].output.on(1)

print(f"sweep {number_of_qubits} qubits at {number_amplitude_values} amplitudes")

for qubit in range(number_of_qubits):
    sweeper.sweep.start_freq(
        qubit_readout_frequencies[qubit] - qubit_readout_widths[qubit]
    )
    sweeper.sweep.stop_freq(
        qubit_readout_frequencies[qubit] + qubit_readout_widths[qubit]
    )

    for i, amplitude in enumerate(relative_amplitude_values):
        sweeper.sweep.oscillator_gain(amplitude)
        sweeper.average.num_averages(int(np.ceil(average_factor * 1 / amplitude ** 2)))
        print(
            f"qubit: {qubit+1} amp: {amplitude:.5f} ({i+1}/{number_amplitude_values})",
            end="\r",
        )
        old_stdout = sys.stdout  # backup current stdout
        sys.stdout = open(os.devnull, "w")
        resonator_spectrum_data["qubits"][qubit].append(sweeper.run())
        sys.stdout = old_stdout  # reset old stdout

device.qachannels[0].input.on(0)
device.qachannels[0].output.on(0)

# In[6] Plot the data for each qubit

#resonator_spectrum_data['qubits'][0]==resonator_spectrum_data['qubits'][1]

import matplotlib.pyplot as plt
from shfqc_helper import voltage_to_power_dBm

font_large=15
font_medium=10

num_points = sweeper.sweep.num_points()

for qubit in range(number_of_qubits):
    number_amplitude_values = np.size(relative_amplitude_values)
    x_data = np.zeros((number_amplitude_values, num_points))
    y_data = np.zeros((number_amplitude_values, num_points))
    z_data = np.zeros((number_amplitude_values, num_points), dtype=complex)
    slope_array = np.zeros((number_amplitude_values, num_points))

    for amp_ind, amplitude in enumerate(relative_amplitude_values):
        spec_path = resonator_spectrum_data["qubits"][qubit][qubit*number_of_qubits+amp_ind]
        spec_path_props = spec_path["properties"]

        z_data[amp_ind] = spec_path["vector"]

        
    fig = plt.figure()
    fig.suptitle(f"Qubit {qubit+1}, amplitude [dBm]", fontsize=font_large)
    plt_extent = [qachannel_center_frequency+spec_path_props["startfreq"],
                  qachannel_center_frequency+spec_path_props["stopfreq"],
                  np.max(relative_amplitude_values), np.min(relative_amplitude_values)]
    
    plt.imshow(voltage_to_power_dBm(abs(z_data)), aspect = 'auto', extent = plt_extent)
    
    plt.ylabel('Readout amplitude (a.u.)')
    plt.xlabel('Frequency (Hz)')
    plt.colorbar()

    plt.show()

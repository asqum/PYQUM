# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 13:50:35 2022

@author: zhinst


Requirements:

    LabOne Version >= 22.02
    Instruments: 1 x SHFQC Instrument
"""

# In[1]

from zhinst.toolkit import Session, SHFQAChannelMode

session = Session("localhost")
device = session.connect_device("DEV12131")

# In[2] Device configuration

import numpy as np
number_of_qubits = 1

# configure qa channels
qachannel_center_frequency = 6.5e9
qachannel_power_in = -50
qachannel_power_out = -30

max_amplitude_readout = (1/3.333) / number_of_qubits # for multiplexed readout

device.qachannels[0].configure_channel(
    center_frequency=qachannel_center_frequency,
    input_range=qachannel_power_in,
    output_range=qachannel_power_out,
    mode=SHFQAChannelMode.READOUT,
)

# configure sg channels
sgchannel_number = list(range(number_of_qubits))
sgchannel_center_frequency = [3.9e9] # depends on number of qubits
sgchannel_power_out = [-13] * number_of_qubits
sgchannel_trigger_input = 0

with device.set_transaction():
    device.qachannels[0].markers[0].source("channel0_sequencer_trigger0")
    device.qachannels[0].markers[1].source("channel0_sequencer_trigger0")
    device.qachannels[0].generator.configure_sequencer_triggering(
    aux_trigger="internal_trigger", # Set QA Channel trigger source to internal trigger
    play_pulse_delay=0
    )
    device.qachannels[0].triggers[0].level(1)
    for qubit in range(number_of_qubits):
        sg_channel = sgchannel_number[qubit]
        synth_channel = int(np.floor(sg_channel / 2)) + 1  # shared channel for LO synthesizers
        device.synthesizers[synth_channel].centerfreq(
            sgchannel_center_frequency[qubit]
        )
        device.sgchannels[sg_channel].output.range(sgchannel_power_out[qubit])
        device.sgchannels[sg_channel].trigger.level(1)
        # Set trigger source
        device.sgchannels[sg_channel].awg.auxtriggers[0].channel(8) # set SG channel trigger source to internal trigger
        device.sgchannels[sg_channel].marker.source(0) # set SG channel marker output to AWG sequencer trigger 1

        
# In[3] Setup SHFQC for qubit spectroscopy

# Generate readout pulses and weights
readout_pulse_duration_qubit_spectroscopy = 2e-6
qubit_readout_frequencies =[-100.3249e6]
qubit_readout_amplitudes = [max_amplitude_readout] * 1
propagation_delay = 324e-9
num_sweep_steps_qubit_spectroscopy = 100 #1000
integration_time_qubit_spectroscopy = 50e-3 # 20e-3 # the higher the better
max_drive_strength=[1]
qubit_drive_frequency = [0] * number_of_qubits

min_max_frequencies=[[-50e6,50e6]]

from shfqc_helper import generate_flat_top_gaussian, voltage_to_power_dBm
import numpy as np
from zhinst.utils.shfqa import SHFQA_SAMPLING_FREQUENCY

# generate readout pulses and weights
readout_pulses = generate_flat_top_gaussian(
    frequencies=qubit_readout_frequencies,
    pulse_duration=readout_pulse_duration_qubit_spectroscopy,
    rise_fall_time=5e-9,
    sampling_rate=SHFQA_SAMPLING_FREQUENCY,
    scaling=1,
)

weights = {}
rotation_angle=0
for waveform_slot, pulse in readout_pulses.items():
    weights[waveform_slot] = np.conj(pulse * np.exp(1j * rotation_angle))

for qubit in range(number_of_qubits):
    readout_pulses[qubit] = (
        readout_pulses[qubit] * qubit_readout_amplitudes[qubit]
    )

device.qachannels[0].generator.write_to_waveform_memory(readout_pulses)
    
    # configure result logger and weighted integration
device.qachannels[0].readout.write_integration_weights(
    weights,
    # compensation for the delay between generator output and input of the integration unit
    integration_delay=propagation_delay,
)

# In[4] Configure Readout Channel

from zhinst.toolkit import AveragingMode

averages_per_sweep_step = int(
    np.round(
        integration_time_qubit_spectroscopy
        / readout_pulse_duration_qubit_spectroscopy
    )
)
device.qachannels[0].readout.configure_result_logger(
    result_length=num_sweep_steps_qubit_spectroscopy,
    num_averages=averages_per_sweep_step,
    result_source="result_of_integration",
    averaging_mode=AveragingMode.SEQUENTIAL,
)
device.qachannels[0].readout.run()

pulse_startQA_string = "QA_GEN_0"
weight_startQA_string = "QA_INT_0"
for i in range(number_of_qubits - 1):
    pulse_startQA_string = pulse_startQA_string + f" | QA_GEN_{i+1}"
    weight_startQA_string = weight_startQA_string + f" | QA_INT_{i+1}"

seqc_program_qa = f"""


repeat({num_sweep_steps_qubit_spectroscopy}) {{
    waitDigTrigger(1);              // wait for internal trigger to start experiment
    repeat({averages_per_sweep_step}) {{
        playZero(4048);
        startQA({pulse_startQA_string}, {weight_startQA_string}, true, 0, 0x0);
    }}

}}
"""

# configure sequencer

device.qachannels[0].generator.load_sequencer_program(seqc_program_qa)
device.qachannels[0].generator.enable_sequencer(single=True)

# In[5] Configure Control channels

for qubit in range(number_of_qubits):
    seqc_program = f"""
const OSC0 = 0;
const FREQ_START = {min_max_frequencies[qubit][0]};
const FREQ_STEP = {(min_max_frequencies[qubit][1]-min_max_frequencies[qubit][0])/num_sweep_steps_qubit_spectroscopy};

configFreqSweep(OSC0, FREQ_START, FREQ_STEP);

// Frequency sweep
for(var i = 0; i < {num_sweep_steps_qubit_spectroscopy}; i++) {{
    waitDigTrigger(1);
    playZero(4048);
    repeat({averages_per_sweep_step}) {{
        playZero(4048);
    }}
    setSweepStep(OSC0, i);
}}
    """
    channel = sgchannel_number[qubit]
    gain = 0.5 * max_drive_strength[qubit]
    device.sgchannels[channel].configure_sine_generation(
        enable=1,
        osc_index=0,
        osc_frequency=qubit_drive_frequency[qubit],
        gains=[gain, gain, gain, -gain],
    )

    device.sgchannels[channel].awg.load_sequencer_program(seqc_program)
    device.sgchannels[channel].awg.enable(1)
    
# In[6] Measurements

device.system.internaltrigger.enable(0)

device.qachannels[0].input.on(1)
device.qachannels[0].output.on(1)


for qubit in range(number_of_qubits):
    channel = sgchannel_number[qubit]
    
    device.sgchannels[channel].awg.enable_sequencer(single=True)
    device.sgchannels[channel].output.on(1)

# Set up internal trigger 

repetitions = num_sweep_steps_qubit_spectroscopy
device.system.internaltrigger.repetitions(num_sweep_steps_qubit_spectroscopy)
device.system.internaltrigger.holdoff(2024e-9*averages_per_sweep_step+2024e-9) # spec sequence repetition rate # to align with playZero(4048)
device.system.internaltrigger.enable(1)

readout_results = device.qachannels[0].readout.read(timeout = 100) # in seconds

# Reset AWG CW output
for qubit in range(number_of_qubits):
    device.sgchannels[sgchannel_number[qubit]].configure_sine_generation(enable=0)

# In[7] results

import matplotlib.pyplot as plt
import numpy as np

for qubit in range(number_of_qubits):
    x_axis = np.linspace(min_max_frequencies[qubit][0],min_max_frequencies[qubit][1],num_sweep_steps_qubit_spectroscopy)/10**6
    # y_axis = np.abs(readout_results[qubit])
    y_axis = voltage_to_power_dBm(np.abs(readout_results[qubit]))

    fig3, axs = plt.subplots(1, 2, figsize=(24,10))
    fig3.suptitle(f"Qubit {qubit+1}", fontsize=30)
    axs[0].plot(x_axis, y_axis)
    axs[0].set_title("amplitude [dBm]", fontsize=20)
    axs[0].set_xlabel("qubit drive frequency [MHz]", fontsize=20)
    axs[0].set_ylabel("amplitude [A.U.]", fontsize=20)
    axs[0].tick_params(axis="both", which="major", labelsize=20)

    axs[1].plot(x_axis, np.unwrap(np.angle(readout_results[qubit])))
    axs[1].set_title("phase [rad]", fontsize=20)
    axs[1].set_xlabel("qubit drive frequency [MHz]", fontsize=20)
    axs[1].set_ylabel("phase [rad]", fontsize=20)
    axs[1].tick_params(axis="both", which="major", labelsize=20)

    plt.show()
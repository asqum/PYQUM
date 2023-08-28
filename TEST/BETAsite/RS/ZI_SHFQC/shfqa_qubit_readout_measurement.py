# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 10:21:10 2022

@author: zhinst

Parallel read-out of qubits.

Requirements:

    LabOne Version >= 22.02
    Instruments: 1 x SHFQA Instrument
    Loopback configuration between input and output of channel 0

"""

# In[1]

from zhinst.toolkit import Session, SHFQAChannelMode, Waveforms

session = Session("localhost")
device = session.connect_device("DEV12139")

# In[2] Configure channel inputs and outputs

CHANNEL_INDEX = 0

device.qachannels[CHANNEL_INDEX].configure_channel(
    center_frequency=2e9,
    input_range=0,
    output_range=-5,
    mode=SHFQAChannelMode.READOUT,
)
device.qachannels[CHANNEL_INDEX].input.on(1)
device.qachannels[CHANNEL_INDEX].output.on(1)

# In[3] Generate readout waveforms

from scipy.signal import gaussian
import numpy as np


NUM_QUBITS = device.max_qubits_per_channel
RISE_FALL_TIME = 10e-9
SAMPLING_RATE = 2e9
PULSE_DURATION = 500e-9
FREQUENCIES = np.linspace(32e6, 230e6, NUM_QUBITS)
SCALING = 0.9 / NUM_QUBITS

rise_fall_len = int(RISE_FALL_TIME * SAMPLING_RATE)
pulse_len = int(PULSE_DURATION * SAMPLING_RATE)
std_dev = rise_fall_len // 10

gauss = gaussian(2 * rise_fall_len, std_dev)
flat_top_gaussian = np.ones(pulse_len)
flat_top_gaussian[0:rise_fall_len] = gauss[0:rise_fall_len]
flat_top_gaussian[-rise_fall_len:] = gauss[-rise_fall_len:]
# Scaling
flat_top_gaussian *= SCALING

time_vec = np.linspace(0, PULSE_DURATION, pulse_len)

readout_pulses = Waveforms()
for i, f in enumerate(FREQUENCIES):
    readout_pulses.assign_waveform(
        slot=i,
        wave1=flat_top_gaussian * np.exp(2j * np.pi * f * time_vec)
    )

device.qachannels[CHANNEL_INDEX].generator.write_to_waveform_memory(readout_pulses)

# In[4] Configure result logger and weighted integration

ROTATION_ANGLE = 0
NUM_READOUTS = 100

weights =  Waveforms()

for waveform_slot, pulse in readout_pulses.items():
    weights.assign_waveform(
        slot=waveform_slot,
        wave1=np.conj(pulse[0] * np.exp(1j * ROTATION_ANGLE))
    )

device.qachannels[CHANNEL_INDEX].readout.write_integration_weights(
    weights=weights,
    # compensation for the delay between generator output and input of the integration unit
    integration_delay=240e-9
)
device.qachannels[CHANNEL_INDEX].readout.configure_result_logger(
    result_length=NUM_READOUTS,
    result_source='result_of_integration'
)

# In[5] Configure sequencer

device.qachannels[CHANNEL_INDEX].generator.configure_sequencer_triggering(
    aux_trigger="internal_trigger",
    play_pulse_delay=0
)

# Set trigger level
device.qachannels[CHANNEL_INDEX].triggers[0].level(1) # set trigger level

seqc_program = f"""
    repeat({NUM_READOUTS}) {{
        waitDigTrigger(1);
        startQA(QA_GEN_ALL, QA_INT_ALL, true, 0, 0x0);
    }}
"""
device.qachannels[CHANNEL_INDEX].generator.load_sequencer_program(seqc_program)

# In[6] Run experiment

device.system.internaltrigger.enable(0)

device.qachannels[CHANNEL_INDEX].readout.run()
device.qachannels[CHANNEL_INDEX].generator.enable_sequencer(single=True)
# device.start_continuous_sw_trigger(
#     num_triggers=NUM_READOUTS, wait_time=2e-3
# )
device.system.internaltrigger.repetitions(NUM_READOUTS)
device.system.internaltrigger.holdoff(2e-3)
device.system.internaltrigger.enable(1)

# In[7] Get results and plot results

readout_results = device.qachannels[CHANNEL_INDEX].readout.read()

import matplotlib.pyplot as plt

max_value = 0
readout_results = readout_results[:NUM_QUBITS]
plt.rcParams["figure.figsize"] = [10, 10]

for complex_number in readout_results:
    real = np.real(complex_number)
    imag = np.imag(complex_number)

    plt.plot(real, imag, "x")

    max_value = max(max_value, max(abs(real)))
    max_value = max(max_value, max(abs(imag)))

# zoom so that the origin is in the middle
max_value *= 1.05
plt.xlim([-max_value, max_value])
plt.ylim([-max_value, max_value])

plt.legend(range(len(readout_results)))
plt.title("qubit readout results")
plt.xlabel("real part")
plt.ylabel("imaginary part")
plt.grid()
plt.show()




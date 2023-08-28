# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 14:46:41 2022

@author: zhinst
"""
import numpy as np
from zhinst.toolkit import Waveforms
from zhinst.toolkit import Session

def generate_flat_top_gaussian(
    frequency, pulse_duration, rise_fall_time, width, sampling_rate, amplitude
):
    """Returns complex flat top Gaussian waveforms modulated with the given frequencies.
    Arguments:
        frequency (array): modulation frequencies applied to the output wave
        pulse_duration (float): total duration of each Gaussian in seconds
        rise_fall_time (float): rise-fall time of each Gaussian edge in seconds
        width (float): standard deviation, width of the Gaussian edge
        sampling_rate (float): sampling rate in samples per second based on which to generate the waveform
        amplitude (float): between 0 and 1
    Returns:
        pulse:  the flat top Gaussians as values for both I and Q
    """
    from scipy.signal import gaussian
    rise_fall_len = int(rise_fall_time * sampling_rate)
    pulse_len = int(pulse_duration * sampling_rate)
    std_dev = rise_fall_len // width
    gauss = amplitude*gaussian(2 * rise_fall_len, std_dev)
    flat_top_gaussian = amplitude*np.ones(pulse_len)
    flat_top_gaussian[0:rise_fall_len] = gauss[0:rise_fall_len]
    flat_top_gaussian[-rise_fall_len:] = gauss[-rise_fall_len:]
    time_vec = np.linspace(0, pulse_duration, pulse_len)
    if not frequency==0:
        pulse_I = np.real(flat_top_gaussian * np.exp(2j * np.pi * frequency * time_vec))
        pulse_Q = np.imag(flat_top_gaussian * np.exp(2j * np.pi * frequency * time_vec))
    else:
        pulse_I = flat_top_gaussian
        pulse_Q = flat_top_gaussian
    return [pulse_I, pulse_Q]

# In[1] connect to device
session = Session('localhost')
device = session.connect_device("DEV12139")

# In[2] channel setup
SG_CHAN_INDEX=0
synth = device.sgchannels[SG_CHAN_INDEX].synthesizer()

with device.set_transaction():
    # RF output settings
    device.sgchannels[SG_CHAN_INDEX].output.range(0) #output range in dBm
    device.sgchannels[SG_CHAN_INDEX].output.rflfpath(1) #use RF path, not LF path
    device.synthesizers[synth].centerfreq(2.0e9) #synthesizer frequency in Hz
    device.sgchannels[SG_CHAN_INDEX].output.on(1) #enable output

    # Digital modulation settings
    device.sgchannels[SG_CHAN_INDEX].awg.outputamplitude(0.5) #amplitude for the AWG outputs
    device.sgchannels[SG_CHAN_INDEX].oscs[0].freq(-200.0e6) #frequency of oscillator 1 in Hz
    device.sgchannels[SG_CHAN_INDEX].oscs[1].freq(300e6) #frequency of oscillator 2 in Hz
    device.sgchannels[SG_CHAN_INDEX].awg.modulation.enable(1) #enable digital modulation

    # Trigger and marker settings
    device.sgchannels[SG_CHAN_INDEX].marker.source(4) #use first marker bit of waveform as marker source

# In[3] seqc
pulse_duration = 10e-6
rise_fall_time = 8e-9
wait_time = 10e-6
pulse_amp = 1

sampling_rate = 2e9

rise_fall_len = int(rise_fall_time * sampling_rate)
pulse_len = int(pulse_duration * sampling_rate)
wait_len = int(wait_time * sampling_rate)

SEQUENCER_CODE = f"""\
// Define waveforms
wave w0 = placeholder({rise_fall_len}, true, false);
wave w1 = placeholder({rise_fall_len});

// Assign waveforms to an index in the waveform memory
assignWaveIndex(1,2,w0,1,2,w0,0);
assignWaveIndex(1,2,w1,1,2,w1,1);
resetOscPhase();
// switch to osc0 freq and Play wavr rise edge
executeTableEntry(0);
// Hold output level
playHold({pulse_len}-{rise_fall_len}*2);
// Play wave fall edge
executeTableEntry(1);
// Wait 
playZero({wait_len});

// switch to osc1 freq and Play wavr rise edge
executeTableEntry(2);
// Hold output level
playHold({pulse_len}-{rise_fall_len}*2);
// Play wave fall edge
executeTableEntry(1);

"""

device.sgchannels[SG_CHAN_INDEX].awg.load_sequencer_program(SEQUENCER_CODE)

# In[4] define waveform

waveforms = Waveforms()
# Waveform at index 0 with markers
# qubit drive pulse as pulse envelope (freq = 0)
wf0 = generate_flat_top_gaussian(0,pulse_duration,rise_fall_time,5,sampling_rate,pulse_amp)
waveforms[0] = (np.array(wf0[0][0:rise_fall_len]), np.array(wf0[0][0:rise_fall_len]), np.ones(rise_fall_len))
# Waveform at index 1 without markers
waveforms[1] = (np.array(wf0[0][-rise_fall_len:]), np.array(wf0[0][-rise_fall_len:]))

device.sgchannels[SG_CHAN_INDEX].awg.write_to_waveform_memory(waveforms)

# In[5] define command table

from zhinst.toolkit import CommandTable

# Predefine command table
ct_schema = device.sgchannels[SG_CHAN_INDEX].awg.commandtable.load_validation_schema()
ct = CommandTable(ct_schema)

ct.table[0].waveform.index = 0
ct.table[0].amplitude00.value = pulse_amp
ct.table[0].amplitude00.increment = False
ct.table[0].amplitude01.value = -pulse_amp
ct.table[0].amplitude01.increment = False
ct.table[0].amplitude10.value = pulse_amp
ct.table[0].amplitude10.increment = False
ct.table[0].amplitude11.value = pulse_amp
ct.table[0].amplitude11.increment = False
ct.table[0].phase.value = 0
ct.table[0].oscillatorSelect.value = 0

ct.table[1].waveform.index = 1
ct.table[1].amplitude00.value = pulse_amp
ct.table[1].amplitude00.increment = False
ct.table[1].amplitude01.value = -pulse_amp
ct.table[1].amplitude01.increment = False
ct.table[1].amplitude10.value = pulse_amp
ct.table[1].amplitude10.increment = False
ct.table[1].amplitude11.value = pulse_amp
ct.table[1].amplitude11.increment = False

ct.table[2].waveform.index = 0
ct.table[2].amplitude00.value = pulse_amp
ct.table[2].amplitude00.increment = False
ct.table[2].amplitude01.value = -pulse_amp
ct.table[2].amplitude01.increment = False
ct.table[2].amplitude10.value = pulse_amp
ct.table[2].amplitude10.increment = False
ct.table[2].amplitude11.value = pulse_amp
ct.table[2].amplitude11.increment = False
ct.table[2].phase.value = 90
ct.table[2].oscillatorSelect.value = 1


device.sgchannels[SG_CHAN_INDEX].awg.commandtable.upload_to_device(ct)


# In[6] run experiment
device.sgchannels[SG_CHAN_INDEX].awg.single(1)
device.sgchannels[SG_CHAN_INDEX].awg.enable(1)

# single = 1
# device.sgchannels[SG_CHAN_INDEX].awg.enable_sequencer(single = single)
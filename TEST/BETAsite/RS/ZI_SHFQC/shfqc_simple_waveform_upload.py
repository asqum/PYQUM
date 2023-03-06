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
    device.sgchannels[SG_CHAN_INDEX].awg.modulation.enable(0) #enable digital modulation

    # Trigger and marker settings
    device.sgchannels[SG_CHAN_INDEX].marker.source(4) #use first marker bit of waveform as marker source


# In[3] seqc
pulse_duration = 1e-6
rise_fall_time = 8e-9
wait_time = 1e-6
pulse_amp = 1
IF_freq = 100e6

sampling_rate = 2e9

rise_fall_len = int(rise_fall_time * sampling_rate)
pulse_len = int(pulse_duration * sampling_rate)
wait_len = int(wait_time * sampling_rate)

SEQUENCER_CODE = f"""\
// Define waveforms
wave w0 = placeholder({pulse_len}, true, false);
wave w1 = placeholder({pulse_len});

// Assign waveforms to an index in the waveform memory
assignWaveIndex(1,2,w0,1,2,w0,0);
assignWaveIndex(1,2,w1,1,2,w1,2);
// Play wave 1
playWave(1, 2, w0, 1, 2, w0);

playZero({wait_len});

// Play wave 2
playWave(1, 2, w1, 1, 2, w1);

"""

device.sgchannels[SG_CHAN_INDEX].awg.load_sequencer_program(SEQUENCER_CODE)

# In[4] define waveform

waveforms = Waveforms()
# Waveform at index 0 with markers
# qubit drive pulse as sampled complex pulse
wf0 = generate_flat_top_gaussian(IF_freq,pulse_duration,rise_fall_time,5,sampling_rate,pulse_amp)
waveforms[0] = (np.array(wf0)[0], np.array(wf0)[1], np.ones(pulse_len))
# Waveform at index 2 without markers
waveforms[2] = (np.array(wf0)[0], np.array(wf0)[1])

device.sgchannels[SG_CHAN_INDEX].awg.write_to_waveform_memory(waveforms)


# In[5] run experiment
device.sgchannels[SG_CHAN_INDEX].awg.single(1)
device.sgchannels[SG_CHAN_INDEX].awg.enable(1)

# single = True
# device.sgchannels[SG_CHAN_INDEX].awg.enable_sequencer(single = single)
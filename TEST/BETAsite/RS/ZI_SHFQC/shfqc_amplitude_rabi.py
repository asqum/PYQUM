# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 16:40:27 2022

@author: zhinst

SHFQC Amplitude Rabi

Requirements:

    LabOne >= 22.08
    Instruments: 1 x SHFQC
    
"""

# In[1] import and connect to instrument

from zhinst.toolkit import Session, SHFQAChannelMode, Waveforms

session = Session('localhost')
device = session.connect_device("DEV12131")

# In[2] Rabi Sequence parameter configuration

SG_CHANNEL = 0
# Center Frequency of the SG synthesizer
RF_FREQUENCY_HZ = 1e9
# Frequency of digital sine generator
OSC_FREQ_HZ = 100e6
OUTPUT_POWER_DBM = 0

# In[3] Configure SG center frequency and RF output

device.sgchannels[SG_CHANNEL].configure_channel(
    enable=True,
    output_range=0,
    center_frequency=RF_FREQUENCY_HZ,
    rf_path=True
)

# In[4] Configure SG digital demodulation

with device.set_transaction():
    # Set modulation frequency
    device.sgchannels[SG_CHANNEL].oscs[0].freq(OSC_FREQ_HZ)
    # Set sine generator
    device.sgchannels[SG_CHANNEL].sines[0].oscselect(0)
    # Set harmonic of sine generator
    device.sgchannels[SG_CHANNEL].sines[0].harmonic(1)
    # Set phase of sine generator
    device.sgchannels[SG_CHANNEL].sines[0].phaseshift(0)
    # Enable digital modulation
    device.sgchannels[SG_CHANNEL].awg.modulation.enable(1)
    # Set marker source
    device.sgchannels[SG_CHANNEL].marker.source(0) # set SG channel marker output to AWG sequencer trigger 1
    # Set trigger source
    device.sgchannels[SG_CHANNEL].awg.auxtriggers[0].channel(8) # set SG channel trigger source to internal trigger

# In[5] Load SG sequencer code

SG_SEQUENCER_CODE = """\
// Define constants in time domain
const t_wid = 50e-9;
const t_len = t_wid*8;
const amp = 1;
const n_amps = 100;
const n_aves = 1;
const t_readout = 1e-6;

// Convert to samples
const s_rate = 2.0e9;
const s_wid = t_wid*s_rate;
const s_len= round(s_rate*t_len/16)*16; //Account for waveform granularity of 16 samples
const s_readout = round(s_rate*t_readout/16)*16;

// Define waveform and assign index
wave w = gauss(s_len, amp, s_len/2, s_wid);
assignWaveIndex(1,2,w,1,2,w,0);

while(1)
{
// Reset oscillator phases and trigger scope
waitDigTrigger(1); // Wait for internal trigger to start Rabi Sequence
setTrigger(1);  // Send marker to scope for scope trigger
setTrigger(0);

//First Rabi amplitude and readout
resetOscPhase();
executeTableEntry(0);
//Readout window
playZero(s_readout);

//Increment Rabi amplitude each loop iteration
repeat (n_amps-1) {
  resetOscPhase();
  //setTrigger(1);
  //setTrigger(0);

  executeTableEntry(1);
  //Readout window
  playZero(s_readout);
}
}
"""
device.sgchannels[SG_CHANNEL].awg.load_sequencer_program(SG_SEQUENCER_CODE)

# In[6] Create and upload command table

from zhinst.toolkit import CommandTable

ct_schema = device.sgchannels[SG_CHANNEL].awg.commandtable.load_validation_schema()
ct = CommandTable(ct_schema)

ct.table[0].waveform.index = 0
ct.table[0].amplitude00.value = 0.007
ct.table[0].amplitude00.increment = False
ct.table[0].amplitude01.value = -0.007
ct.table[0].amplitude01.increment = False
ct.table[0].amplitude10.value = 0.007
ct.table[0].amplitude10.increment = False
ct.table[0].amplitude11.value = 0.007
ct.table[0].amplitude11.increment = False

ct.table[1].waveform.index = 0
ct.table[1].amplitude00.value = 0.007
ct.table[1].amplitude00.increment = True
ct.table[1].amplitude01.value = -0.007
ct.table[1].amplitude01.increment = True
ct.table[1].amplitude10.value = 0.007
ct.table[1].amplitude10.increment = True
ct.table[1].amplitude11.value = 0.007
ct.table[1].amplitude11.increment = True

device.sgchannels[SG_CHANNEL].awg.commandtable.upload_to_device(ct)

# In[7] Run the SG sequencer

device.sgchannels[SG_CHANNEL].awg.enable_sequencer(single=True)

# In[8] Configure QA channel inputs and outputs

QA_CHANNEL_INDEX = 0

device.qachannels[QA_CHANNEL_INDEX].configure_channel(
    center_frequency=2e9,
    input_range=0,
    output_range=-5,
    mode=SHFQAChannelMode.READOUT,
)
device.qachannels[QA_CHANNEL_INDEX].input.on(1)
device.qachannels[QA_CHANNEL_INDEX].output.on(1)

input("press enter to proceed")

# In[9] Configure QA scope

SCOPE_CHANNEL = 0
#NUM_QUBITS = device.max_qubits_per_channel
NUM_QUBITS = 1
READOUT_DURATION = 600e-9
NUM_SEGMENTS = 1
NUM_AVERAGES = 1
NUM_MEASUREMENTS = NUM_SEGMENTS * NUM_AVERAGES
SHFQA_SAMPLING_FREQUENCY = 2e9

# device.scopes[SCOPE_CHANNEL].configure(
#     input_select={SCOPE_CHANNEL: f"channel{QA_CHANNEL_INDEX}_signal_input"},
#     num_samples=int(READOUT_DURATION * SHFQA_SAMPLING_FREQUENCY),
#     trigger_input=f"channel{QA_CHANNEL_INDEX}_sequencer_monitor0",
#     num_segments=NUM_SEGMENTS,
#     num_averages=NUM_AVERAGES,
#     trigger_delay=200e-9,
# )

# In[10] Generate QA waveforms

from scipy.signal import gaussian
import numpy as np

RISE_FALL_TIME = 10e-9
PULSE_DURATION = 500e-9

rise_fall_len = int(RISE_FALL_TIME * SHFQA_SAMPLING_FREQUENCY)
pulse_len = int(PULSE_DURATION * SHFQA_SAMPLING_FREQUENCY)
std_dev = rise_fall_len // 10

gauss = gaussian(2 * rise_fall_len, std_dev)
flat_top_gaussian = np.ones(pulse_len)
flat_top_gaussian[0:rise_fall_len] = gauss[0:rise_fall_len]
flat_top_gaussian[-rise_fall_len:] = gauss[-rise_fall_len:]
# Scaling
flat_top_gaussian *= 0.9

readout_pulses = Waveforms()
time_vec = np.linspace(0, PULSE_DURATION, pulse_len)

for i, f in enumerate(np.linspace(20e6, 100e6, NUM_QUBITS)):
    readout_pulses.assign_waveform(
        slot=i,
        wave1=flat_top_gaussian * np.exp(2j * np.pi * f * time_vec)
    )

device.qachannels[QA_CHANNEL_INDEX].generator.write_to_waveform_memory(readout_pulses)

# In[11] Configure QA sequencer

device.qachannels[QA_CHANNEL_INDEX].generator.configure_sequencer_triggering(
    aux_trigger="internal_trigger", # Set QA Channel trigger source to internal trigger
    play_pulse_delay=0
)

# qubit_result = {
#     'weights': None,
#     'ground_states': None,
#     'excited_states': None
# }
# print(f"Measuring qubit {i}.")

# upload sequencer program
seqc_program = f"""
const t_wid = 50e-9;
const t_len = t_wid*8;
const amp = 1;
const n_amps = 100;
const n_aves = 1;
const t_readout = 1e-6;

// Convert to samples
const s_rate = 2.0e9;
const s_wid = t_wid*s_rate;
const s_len= round(s_rate*t_len/16)*16; //Account for waveform granularity of 16 samples
const s_readout = round(s_rate*t_readout/16)*16;

while(1)
{{
  waitDigTrigger(1);
  repeat({NUM_MEASUREMENTS}*n_amps) {{
        resetOscPhase();
        playZero(s_len);
        playZero(s_readout);
        
        startQA(QA_GEN_0, 0x0, true,  0, 0x0);
    }}
}}
"""
device.qachannels[QA_CHANNEL_INDEX].generator.load_sequencer_program(seqc_program)
device.qachannels[QA_CHANNEL_INDEX].generator.enable_sequencer(single=True)

input("press enter to proceed")

# In[12] Run the measurement

# results = []

# Set up internal trigger 
device.system.internaltrigger.enable(0)
device.system.internaltrigger.repetitions(1e9)
device.system.internaltrigger.holdoff(200e-6) # rabi sequence repetition rate
device.system.internaltrigger.enable(1)

input("press enter to proceed")

# Start a measurement
# device.scopes[SCOPE_CHANNEL].run(single=True)


# # get results to calculate weights and plot data
# scope_data, *_ = device.scopes[0].read()

# # Calculates the weights from scope measurements
# # for the excited and ground states
# split_data = np.split(scope_data[SCOPE_CHANNEL], 2)
# ground_state_data = split_data[0]
# excited_state_data = split_data[1]
# qubit_result['ground_state_data'] = ground_state_data
# qubit_result['excited_state_data'] = excited_state_data
# qubit_result['weights'] = np.conj(excited_state_data - ground_state_data)
# results.append(qubit_result)
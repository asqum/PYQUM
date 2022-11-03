# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 16:40:27 2022

@author: zhinst

SHFQC Ramsey

Requirements:

    LabOne >= 22.08
    Instruments: 1 x SHFQC
    
"""

# In[1] import and connect to instrument

from zhinst.toolkit import Session, SHFQAChannelMode

session = Session('localhost')
device = session.connect_device("DEV12139")

# In[2] Device configuration

import numpy as np
number_of_qubits = 5

# configure QA channel

qachannel_number = 0
# qachannel_center_frequency = 7.1e9
# qachannel_power_in = -50
# qachannel_power_out = -30
qachannel_center_frequency = 1.5e9
qachannel_power_in = 0
qachannel_power_out = -5

device.qachannels[qachannel_number].configure_channel(
    center_frequency=qachannel_center_frequency,
    input_range=qachannel_power_in,
    output_range=qachannel_power_out,
    mode=SHFQAChannelMode.READOUT,
)

# Set QA channel trigger source to internal trigger
device.qachannels[qachannel_number].markers[0].source("channel0_sequencer_trigger0")
device.qachannels[qachannel_number].markers[1].source("channel0_sequencer_trigger0")
device.qachannels[qachannel_number].generator.configure_sequencer_triggering(
    aux_trigger="internal_trigger", # Set QA Channel trigger source to internal trigger
    play_pulse_delay=0
)
# Set trigger level
device.qachannels[qachannel_number].triggers[0].level(1) # 1V

#################################################

# configure SG channels
sgchannel_number = list(range(number_of_qubits))
sgchannel_center_frequency = [1e9, 1e9, 1.4e9, 1.4e9, 1.6e9] # 2 adjacent channels share one center freq

#sgchannel_power_out = [10] * number_of_qubits
sgchannel_power_out = [0] * number_of_qubits
#sgchannel_trigger_input = 0

# configure sg channels
with device.set_transaction():
    for qubit in range(number_of_qubits):
        sg_channel = sgchannel_number[qubit]
        synth_channel = int(np.floor(sg_channel / 2)) + 1
        device.synthesizers[synth_channel].centerfreq(
            sgchannel_center_frequency[qubit]
        )
        device.sgchannels[sg_channel].output.range(sgchannel_power_out[qubit])
        # Set marker source
        device.sgchannels[sg_channel].marker.source(0) # set SG channel marker output to AWG sequencer trigger 1
        # Set trigger source
        device.sgchannels[sg_channel].awg.auxtriggers[0].channel(8) # set SG channel trigger source to internal trigger
        # Set trigger level
        device.sgchannels[sg_channel].trigger.level(1) # 1V
       
# In[3] Ramsey measurement parameters

# define parameters

qubit_drive_frequency=[100e6, 200e6, -100e6, 100e6, 100e6]
qubit_T1_time = [50e-6, 50e-6, 50e-6, 50e-6, 50e-6]
qubit_single_gate_time = [16e-9, 16e-9, 16e-9, 16e-9, 16e-9]
#max_drive_strength = [1, 1, 1, 1, 1]

qubit_readout_frequencies=[407e6,130e6,-570e6,-157.5e6,-352e6]
readout_pulse_duration=  2e-6
max_amplitude_readout = 1 / number_of_qubits * 0.98
qubit_readout_amplitudes = [max_amplitude_readout] * 5

#wait_factor_in_T1 = 5
wait_factor_in_T1 = 0.05 # for scope test
# Readout line propagation delay
propagation_delay= 240e-9
# Readout line reference delay
ref_delay = 40e-9

START_ZERO_DURATION = 16e-9 # multiples of 8 ns
STEP_ZERO_DURATION = 32e-9 # 8 ns resolution
num_steps_ramsey_experiment = 10
SHFSG_SAMPLING_FREQUENCY = 2e9

#num_averages_ramsey_experiment = 2 ** 12
num_averages_ramsey_experiment = 2 ** 2

pulse_amp = [1, 1, 1, 1, 1]
start_zero_len = int(np.ceil((START_ZERO_DURATION * SHFSG_SAMPLING_FREQUENCY)/16)*16)
step_zero_len = int(np.ceil((STEP_ZERO_DURATION * SHFSG_SAMPLING_FREQUENCY)/16)*16)

# In[4] Generate readout pulses and weights

from shfqc_helper import generate_flat_top_gaussian
from zhinst.utils.shfqa import SHFQA_SAMPLING_FREQUENCY
import numpy as np

# generate readout pulses and weights
readout_pulses = generate_flat_top_gaussian(
    frequencies=qubit_readout_frequencies,
    pulse_duration=readout_pulse_duration,
    rise_fall_time=5e-9,
    sampling_rate=SHFQA_SAMPLING_FREQUENCY,
    scaling=1,
)

# generate integration weights
weights = {}
rotation_angle=0
for waveform_slot, pulse in readout_pulses.items():
    weights[waveform_slot] = np.conj(pulse * np.exp(1j * rotation_angle))

# scale readout pulses according to max readout amplitudes
for qubit in range(number_of_qubits):
    readout_pulses[qubit] = (
        readout_pulses[qubit] * qubit_readout_amplitudes[qubit]
    )

device.qachannels[qachannel_number].generator.write_to_waveform_memory(readout_pulses)

# Rotate integration weights
qubit_readout_rotation = [
    0 * np.pi,
    0 * np.pi,
    0 * np.pi,
    0 * np.pi,
    0 * np.pi,
]

# rotate weights according to readout parameter settings
weightsrot = {
    i: np.multiply(weights[i], np.exp(1j * qubit_readout_rotation[i]))
    for i in range(number_of_qubits)
}

# configure result logger and weighted integration
device.qachannels[qachannel_number].readout.write_integration_weights(
    weightsrot,
    # compensation for the delay between generator output and input of the integration unit
    integration_delay=propagation_delay,
)

# In[5] Configure readout channel

from zhinst.toolkit import AveragingMode
pulse_startQA_string = "QA_GEN_0"
weight_startQA_string = "QA_INT_0"
for i in range(number_of_qubits - 1):
    pulse_startQA_string = pulse_startQA_string + f" | QA_GEN_{i+1}"
    weight_startQA_string = weight_startQA_string + f" | QA_INT_{i+1}"

# converts width of single qubit gate assuming its a gaussian to a good waveform length in samples
# assuming the optimal waveform length is 8 times the width of the gaussian
single_qubit_pulse_time_samples = int(
    np.max(qubit_single_gate_time) * SHFQA_SAMPLING_FREQUENCY
)
readout_pulse_duration_samples = int(
    np.ceil(
        (readout_pulse_duration * SHFQA_SAMPLING_FREQUENCY)
        / 16
    )
    * 16
)
time_to_next_experiment_samples = int(
    np.max(qubit_T1_time)
    * wait_factor_in_T1
    * SHFQA_SAMPLING_FREQUENCY
)
ref_compensation_samples = int(
    np.ceil(
        (ref_delay * SHFQA_SAMPLING_FREQUENCY)
        / 16
    )
    * 16
)
seqc_program_qa = f"""
var i;

waitDigTrigger(1); // wait for internal trigger to start experiment
resetOscPhase();
repeat({num_averages_ramsey_experiment}) {{
    for (i = 0; i < {num_steps_ramsey_experiment}; i++) {{

        // wait until control sequence finished
        playZero(2*{single_qubit_pulse_time_samples}+{start_zero_len}+i*{step_zero_len});
                
        // reference compensation
        playZero({ref_compensation_samples});

        //start readout
        playZero({readout_pulse_duration_samples});
        startQA({pulse_startQA_string}, {weight_startQA_string}, true, 0, 0x0);

        //wait for qubit decay
        playZero({time_to_next_experiment_samples});
    }}
}}

"""

# Configure result logger cyclic averaging
device.qachannels[qachannel_number].readout.configure_result_logger(
    result_source="result_of_integration",
    result_length=num_steps_ramsey_experiment,
    num_averages=num_averages_ramsey_experiment,
    averaging_mode=AveragingMode.CYCLIC,
)

# In[6] configure control channels

import inspect
from zhinst.toolkit import CommandTable

for qubit in range(number_of_qubits):
    with device.set_transaction():
        device.sgchannels[sgchannel_number[qubit]].sines[0].i.enable(0)
        device.sgchannels[sgchannel_number[qubit]].sines[0].q.enable(0)
        device.sgchannels[sgchannel_number[qubit]].awg.modulation.enable(1)
        device.sgchannels[sgchannel_number[qubit]].oscs[0].freq(
            qubit_drive_frequency[qubit]
        )

    # Predefine command table
    ct_schema = device.sgchannels[0].awg.commandtable.load_validation_schema()
    ct = CommandTable(ct_schema)
    
    ct.table[0].waveform.index = 0
    ct.table[0].amplitude00.value = pulse_amp[qubit]
    ct.table[0].amplitude00.increment = False
    ct.table[0].amplitude01.value = -pulse_amp[qubit]
    ct.table[0].amplitude01.increment = False
    ct.table[0].amplitude10.value = pulse_amp[qubit]
    ct.table[0].amplitude10.increment = False
    ct.table[0].amplitude11.value = pulse_amp[qubit]
    ct.table[0].amplitude11.increment = False
    
    # Upload waveform
    seqc = inspect.cleandoc(
    f"""
    var i;

    // Define a single waveform
    wave ramsey_pulse=gauss({single_qubit_pulse_time_samples}, {pulse_amp[qubit]}, {single_qubit_pulse_time_samples/2}, {single_qubit_pulse_time_samples/4});

    // Assign a dual channel waveform to wave table entry
    assignWaveIndex(1,2,ramsey_pulse, 1,2,ramsey_pulse, 0);
    

    // Wait for start trigger
    waitDigTrigger(1);
    setTrigger(1);  // Send marker to scope for scope trigger
    setTrigger(0);
    resetOscPhase();
    
    repeat ({num_averages_ramsey_experiment}) {{
        for (i = 0; i < {num_steps_ramsey_experiment}; i++){{
        
        executeTableEntry(0);
        playZero({start_zero_len}+i*{step_zero_len});
        executeTableEntry(0);
        
        playZero({ref_compensation_samples});
        playZero({readout_pulse_duration_samples});
        playZero({time_to_next_experiment_samples});
        }}
    }}
    """
    )

    device.sgchannels[sgchannel_number[qubit]].awg.load_sequencer_program(seqc)

    device.sgchannels[sgchannel_number[qubit]].awg.commandtable.upload_to_device(ct)

# In[7] Run Experiment

device.system.internaltrigger.enable(0)

device.qachannels[qachannel_number].generator.load_sequencer_program(seqc_program_qa)
device.qachannels[qachannel_number].generator.enable_sequencer(single=True)
device.qachannels[qachannel_number].readout.run()

device.qachannels[qachannel_number].input.on(1)
device.qachannels[qachannel_number].output.on(1)


for qubit in range(number_of_qubits):
    channel = sgchannel_number[qubit]
    
    device.sgchannels[channel].awg.enable_sequencer(single=True)
    device.sgchannels[channel].output.on(1)

# Set up internal trigger 

device.system.internaltrigger.repetitions(1)
device.system.internaltrigger.holdoff(200e-6) # ramsey sequence repetition rate
device.system.internaltrigger.enable(1)

readout_results = device.qachannels[qachannel_number].readout.read(timeout=100)

# In[8] Plot results

import matplotlib.pyplot as plt
import numpy as np
import pickle

saveloc="Ramsey1"

with open(saveloc+".pkl", "wb") as f:
    pickle.dump(readout_results, f)

interactive = 1
if interactive ==1:
    #matplotlib widget
    figsize=(12,5)
    font_large=15
    font_medium=10
else:
    #matplotlib inline
    figsize=(24,10)
    font_large=30
    font_medium=20

for qubit in range(number_of_qubits):
    x_axis = np.linspace(
        int(START_ZERO_DURATION*1e9),
        int(START_ZERO_DURATION*1e9)+(num_steps_ramsey_experiment-1)*int(STEP_ZERO_DURATION*1e9),
        num_steps_ramsey_experiment
    )
    fig3, axs = plt.subplots(1, 2, figsize=figsize)
    fig3.suptitle(f"Qubit {qubit}", fontsize=font_large)
    axs[0].plot(x_axis, np.real(readout_results[qubit] - readout_results[qubit][0]))
    axs[0].set_title("I quadrature [A.U.]", fontsize=font_medium)
    axs[0].set_xlabel("zero length [ns]", fontsize=font_medium)
    axs[0].set_ylabel("quadrature [A.U.]", fontsize=font_medium)
    axs[0].tick_params(axis="both", which="major", labelsize=font_medium)

    axs[1].plot(x_axis, np.imag(readout_results[qubit] - readout_results[qubit][0]))
    axs[1].set_title("Q quadrature [A.U.]", fontsize=font_medium)
    axs[1].set_xlabel("zero length [ns]", fontsize=font_medium)
    axs[1].set_ylabel("quadrature [A.U.]", fontsize=font_medium)
    axs[1].tick_params(axis="both", which="major", labelsize=font_medium)

    plt.savefig(saveloc + f"{qubit}.png")
    plt.show()
    
    # plot integration results
    max_value = 0
    
    plt.rcParams["figure.figsize"] = [10, 10]
    
    for complex_number in readout_results[qubit]:
        real = np.real(complex_number)
        imag = np.imag(complex_number)
    
        plt.plot(real, imag, "x" , color = 'b')

    #plt.legend(range(len(readout_results)))
    plt.title(f"Qubit {qubit} readout results")
    plt.xlabel("real part")
    plt.ylabel("imaginary part")
    plt.grid()
    plt.show()



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




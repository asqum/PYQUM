from configurations import *
from two_tone_pulsed import TwoTonePulsed
import matplotlib.pyplot as plt

qubit = dr2b.q4
feedline = dr2b.feedline

experiment = TwoTonePulsed(

    readout_freq=qubit['readout_freq'],
    control_freq_center=qubit['control_freq'] - 6e6,
    readout_amp=qubit['readout_amp'],
    control_port=qubit['control_port'],

    readout_duration=feedline['readout_duration'],
    sample_duration=feedline['sample_duration'],
    readout_port=feedline['readout_port'],
    sample_port=feedline['sample_port'],
    readout_sample_delay=feedline['readout_sample_delay'],

    control_freq_span=3.35e6,
    control_freq_nr=160,
    control_amp=0.007,
    # control_duration=20e-9,
    control_duration=7e-6, # why not 20e-6
    # wait_delay=50e-6,
    wait_delay=40e-6,
    num_averages=2000,

)

# presto_address = "192.168.1.84"
# save_filename = experiment.run(presto_address)
presto_address = "qum.phys.sinica.edu.tw" 
save_filename = experiment.run(presto_address, 5070)


experiment.analyze()
plt.show()
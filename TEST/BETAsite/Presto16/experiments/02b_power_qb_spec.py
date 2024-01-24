from configurations import *
from two_tone_power import TwoTonePower
import numpy as np
import matplotlib.pyplot as plt

qubit = dr2b.q5
feedline = dr2b.feedline

experiment = TwoTonePower(

    readout_freq=qubit['readout_freq'],
    control_freq_center=qubit['control_freq'],# - 6e6,
    readout_amp=qubit['readout_amp'],
    control_port=qubit['control_port'],

    # readout_duration=feedline['readout_duration'],
    # sample_duration=feedline['sample_duration'],
    readout_port=feedline['readout_port'],
    # sample_port=feedline['sample_port'],
    # readout_sample_delay=feedline['readout_sample_delay'],

    control_freq_span=200e6,
    df=400e3,
    control_amp_arr=np.linspace(0.008,0.8, 10),
    input_port=1,
    num_averages=3000,
)

presto_address = "qum.phys.sinica.edu.tw" 
save_filename = experiment.run(presto_address, 5070)

experiment.analyze()
plt.show()  


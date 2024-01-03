from configurations import *
from rabi_time import RabiTime
import numpy as np
import matplotlib.pyplot as plt

qubit = dr2b.q4
feedline = dr2b.feedline

experiment = RabiTime(
    readout_freq=qubit['readout_freq'],
    control_freq=qubit['control_freq'],
    readout_amp=qubit['readout_amp'],
    control_port=qubit['control_port'],

    control_amp_arr=np.linspace(0.005, 0.05, 21), # (0.1, 1, 20), (0.005, 0.05, 21)
    control_duration_arr=np.linspace(100e-9, 5e-6, 99), # (100e-9, 5e-6, 99)
    wait_delay=40e-6,
    num_averages=4000,

    readout_duration=feedline['readout_duration'],
    sample_duration=feedline['sample_duration'],
    readout_port=feedline['readout_port'],
    sample_port=feedline['sample_port'],
    readout_sample_delay=feedline['readout_sample_delay'],
)

# presto_address = "192.168.1.84"
# save_filename = experiment.run(presto_address)
presto_address = "qum.phys.sinica.edu.tw" 
save_filename = experiment.run(presto_address, 5070)

experiment.analyze()
plt.show()


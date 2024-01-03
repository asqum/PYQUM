from configurations import *
from rabi_amp import RabiAmp
import numpy as np
import matplotlib.pyplot as plt

qubit = dr2b.q4
feedline = dr2b.feedline

experiment = RabiAmp(
    readout_freq=qubit['readout_freq'],
    control_freq=qubit['control_freq'],
    readout_amp=qubit['readout_amp'],
    control_port=qubit['control_port'],
    readout_duration=feedline['readout_duration'],
    sample_duration=feedline['sample_duration'],
    readout_port=feedline['readout_port'],
    sample_port=feedline['sample_port'],
    readout_sample_delay=feedline['readout_sample_delay'],

    control_amp_arr=np.linspace(0, 1, 101),
    control_duration=30e-9,
    wait_delay=40e-6,
    num_averages=2000,
    num_pulses=1,

)

# presto_address = "192.168.1.84"
# save_filename = experiment.run(presto_address)
presto_address = "qum.phys.sinica.edu.tw" 
save_filename = experiment.run(presto_address, 5070)

experiment.analyze()
plt.show()


from configurations import *
from t1 import T1
import numpy as np
import matplotlib.pyplot as plt

qubit = dr2b.q5
feedline = dr2b.feedline

experiment = T1(
    delay_arr=np.linspace(0, 100e-6, 201),
    wait_delay=40e-6,
    num_averages=3000,

    readout_freq=qubit['readout_freq'],
    control_freq=qubit['control_freq'],
    readout_amp=qubit['readout_amp'],
    control_port=qubit['control_port'],
    control_amp=qubit['control_amp_180'],
    control_duration=qubit['control_duration'],

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

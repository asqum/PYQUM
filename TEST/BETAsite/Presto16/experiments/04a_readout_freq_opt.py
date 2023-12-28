from configurations import *
from excited_sweep import ExcitedSweep
import numpy as np
import matplotlib.pyplot as plt

experiment = ExcitedSweep(
    readout_freq_center=5.7473e9,
    readout_freq_span=10e6,
    readout_freq_nr=101,
    control_freq=4.100629e9,
    readout_amp=0.2,
    control_amp=0.585,
    readout_duration=5e-6,
    control_duration=20e-9,
    sample_duration=5e-6,
    readout_port=1,
    control_port=2,
    sample_port=1,
    wait_delay=20e-6,
    readout_sample_delay=0e-9,
    num_averages=6000,
)

presto_address = "192.168.50.70"  # your Presto IP address
save_filename = experiment.run(presto_address)

experiment.analyze()
plt.show()
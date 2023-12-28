from configurations import *
from rabi_amp import RabiAmp
import numpy as np
import matplotlib.pyplot as plt

experiment = RabiAmp(
    readout_freq=5.7465e9,
    control_freq=4.100629e9,
    readout_amp=0.1,
    control_amp_arr=np.linspace(0, 1, 101),
    readout_duration=5e-6,
    control_duration=30e-9,
    sample_duration=5e-6,
    readout_port=1,
    control_port=2,
    sample_port=1,
    wait_delay=10e-6,
    readout_sample_delay=0e-9,
    num_averages=40000,
    num_pulses=1,
)

presto_address = "192.168.50.70"  # your Presto IP address
save_filename = experiment.run(presto_address)

experiment.analyze()
plt.show()

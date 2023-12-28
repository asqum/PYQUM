from configurations import *
from ramsey_single import RamseySingle
import numpy as np
import matplotlib.pyplot as plt

experiment = RamseySingle(
    readout_freq=5.7465e9,
    control_freq=4.101e9,
    readout_amp=0.2,
    control_amp=0.288,
    readout_duration=5.1e-6,
    control_duration=20e-9,
    sample_duration=5.5e-6,
    delay_arr=np.linspace(0, 10e-6, 201),
    readout_port=1,
    control_port=2,
    sample_port=1,
    wait_delay=20e-6,
    readout_sample_delay=0e-9,
    num_averages=10000,
)

presto_address = "192.168.50.70"  # your Presto IP address
save_filename = experiment.run(presto_address)

experiment.analyze()
plt.show()
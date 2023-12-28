from configurations import *
from rabi_time import RabiTime
import numpy as np
import matplotlib.pyplot as plt

experiment = RabiTime(
    readout_freq=5.7465e9,
    control_freq=4.100629e9,
    readout_amp=0.1,
    control_amp_arr=np.linspace(0.1, 1, 20),
    # control_amp_arr=np.linspace(0.005, 0.05, 21),
    readout_duration=5e-6,
    control_duration_arr=np.linspace(2e-9, 202e-9, 101),
    # control_duration_arr=np.linspace(100e-9, 5e-6, 99),
    sample_duration=5e-6,
    readout_port=1,
    control_port=2,
    sample_port=1,
    wait_delay=20e-6,
    readout_sample_delay=0e-9,
    num_averages=8000,
)

presto_address = "192.168.50.70"  # your Presto IP address
port = None
# presto_address = "10.10.90.33"  # your Presto IP address
# port = 5070
save_filename = experiment.run(presto_address, port)

experiment.analyze()
plt.show()

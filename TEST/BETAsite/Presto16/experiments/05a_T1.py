from configurations import *
from t1 import T1
import numpy as np
import matplotlib.pyplot as plt

experiment = T1(
    readout_freq=5.7473e9,
    control_freq=4.100629e9,
    readout_amp=0.2,
    control_amp=0.581,
    readout_duration=2e-6,
    control_duration=20e-9,
    sample_duration=2e-6,
    delay_arr=np.linspace(0, 40e-6, 101),
    readout_port=1,
    control_port=2, 
    sample_port=1,
    wait_delay=10e-6,
    readout_sample_delay=0e-9,
    num_averages=10000,
)

# presto_address = "192.168.50.70"  # your Presto IP address
# save_filename = experiment.run(presto_address)
presto_address = "qum.phys.sinica.edu.tw"
save_filename = experiment.run(presto_address, 5070)

experiment.analyze()
plt.show()
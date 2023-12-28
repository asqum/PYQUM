from configurations import *
from ramsey_fringes import RamseyFringes
import numpy as np
import matplotlib.pyplot as plt

experiment = RamseyFringes(
    readout_freq=5.7465e9,
    control_freq_center=4.1006e9,
    control_freq_span=1e6,
    control_freq_nr=41,
    readout_amp=0.4,
    control_amp=0.288,
    readout_duration=5e-6,
    control_duration=20e-9,
    sample_duration=5.1e-6,
    delay_arr=np.linspace(0, 10e-6, 51),
    readout_port=1,
    control_port=2,
    sample_port=1,
    wait_delay=10e-6,
    readout_sample_delay=0e-9,
    num_averages=4000,
)

presto_address = "192.168.50.70"  # your Presto IP address
save_filename = experiment.run(presto_address)

experiment.analyze()
plt.show()
from configurations import *
from two_tone_power import TwoTonePower
import numpy as np
import matplotlib.pyplot as plt

experiment = TwoTonePower(
    readout_freq=5.7475e9,
    control_freq_center=4.055e9,
    control_freq_span=200e6,
    df=400e3,
    readout_amp=0.02,
    control_amp_arr=np.linspace(0.005,0.05, 5),
    readout_port=1,
    control_port=2,
    input_port=1,
    num_averages=5000,
)

presto_address = "192.168.50.70"  # your Presto IP address
save_filename = experiment.run(presto_address)

experiment.analyze()
plt.show()  
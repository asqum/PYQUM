from configurations import *
from two_tone_pulsed import TwoTonePulsed
import matplotlib.pyplot as plt

experiment = TwoTonePulsed(
    readout_freq=5.90648e9,
    control_freq_center=4.5e9,
    control_freq_span=300e6,
    control_freq_nr=301,
    readout_amp=0.2,
    control_amp=0.05,
    readout_duration=3e-6,
    # control_duration=20e-9,
    control_duration=7e-6,
    sample_duration=3e-6,
    readout_port=1,
    control_port=3,
    sample_port=1,
    # wait_delay=50e-6,
    wait_delay=40e-6,
    readout_sample_delay=0,
    num_averages=3000,
)
# presto_address = "192.168.50.70"  # your Presto IP address
# save_filename = experiment.run(presto_address)
# presto_address = "qum.phys.sinica.edu.tw"
# save_filename = experiment.run(presto_address, 5070)
presto_address = "192.168.1.84"
save_filename = experiment.run(presto_address)

experiment.analyze()
plt.show()
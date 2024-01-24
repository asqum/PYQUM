from configurations import *
from ramsey_fringes import RamseyFringes
import numpy as np
import matplotlib.pyplot as plt

qubit = dr2b.q5
feedline = dr2b.feedline

experiment = RamseyFringes(
    control_freq_span=1e6,
    control_freq_nr=41,
    delay_arr=np.linspace(0, 10e-6, 51),
    wait_delay=40e-6,
    num_averages=4000,

    readout_freq=qubit['readout_freq'],
    control_freq_center=qubit['control_freq'],
    readout_amp=qubit['readout_amp'],
    control_port=qubit['control_port'],
    control_amp=qubit['control_amp_90'],
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

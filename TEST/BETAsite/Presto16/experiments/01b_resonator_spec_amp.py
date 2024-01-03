from configurations import *
from sweep_power import SweepPower
import numpy as np
import matplotlib.pyplot as plt

experiment = SweepPower(
    freq_center=6.102e9, # 6.102, 5.90648
    freq_span=10e6,
    df=80e3,
    num_averages=800,
    amp_arr=np.linspace(0.01, 0.3, 40),
    output_port=1,
    input_port=1,
)

# presto_address = "192.168.50.70"  # your Presto IP address
# save_filename = experiment.run(presto_address)
# presto_address = "qum2.phys.sinica.edu.tw"  # 10.10.233.10
presto_address = "qum.phys.sinica.edu.tw"
save_filename = experiment.run(presto_address, 5070)

experiment.analyze()
plt.show()
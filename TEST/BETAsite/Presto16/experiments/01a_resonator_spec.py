from configurations import *
from sweep import Sweep
import matplotlib.pyplot as plt

experiment = Sweep(
    freq_center=(5.90648)*1e9, # 5.93(wide), 6.102, 5.90648
    freq_span=9e6,
    df=30e3,
    num_averages=900,
    amp=0.07,
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
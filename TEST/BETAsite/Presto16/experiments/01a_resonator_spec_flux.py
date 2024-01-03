from configurations import *
from sweep_freq_and_DC_flux import SweepFreqAndDC
import numpy as np
import matplotlib.pyplot as plt

loadata = True
qubit = dr2b.q5
feedline = dr2b.feedline

if loadata:
    experiment = SweepFreqAndDC.load("data/sweep_freq_and_DC_flux_20231231_200525.h5")

else:

    experiment = SweepFreqAndDC(
        freq_span=6e6,
        df=240e3,
        num_averages=1000,
        bias_arr = np.linspace(-1, 1, 41),

        bias_port = qubit['bias_port'],
        freq_center=qubit['readout_freq'] + 6e6/4,
        amp=qubit['readout_amp'],
        output_port=feedline['readout_port'],
        input_port=feedline['sample_port'],
    )

    presto_address = "qum.phys.sinica.edu.tw"
    save_filename = experiment.run(presto_address, 5070) # External port

experiment.analyze("amplitude")
plt.show()

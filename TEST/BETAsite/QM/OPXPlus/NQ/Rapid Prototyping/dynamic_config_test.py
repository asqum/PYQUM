import matplotlib.pyplot as plt
from QM_config_dynamic import QM_config
myConfig = QM_config()
myConfig.set_wiring("con1")
mRO_common = {
        "I":("con1",1),
        "Q":("con1",2),
        "freq_LO": 6, # GHz
        "mixer": "octave_octave1_1",
        "time_of_flight": 200, # ns
        "integration_time": 2000, # ns
    }
mRO_individual = [
    {
        "name":"rr1", 
        "freq_RO": 6.11, # GHz
        "amp": 0.05, # V
    },
    {
        "name":"rr2", 
        "freq_RO": 5.91, # GHz
        "amp": 0.05, # V
    }
]
n_avg = 50  # The number of averages
# The frequency sweep around the resonators' frequency "resonator_IF_q"

myConfig.update_multiplex_readout_channel(mRO_common, mRO_individual )
myConfig.export_config("testing.pkl")

r_config  = QM_config()
r_config.import_config("testing.pkl")
print(r_config.get_config())

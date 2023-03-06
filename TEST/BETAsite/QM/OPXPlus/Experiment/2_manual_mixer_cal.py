from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm.simulate.credentials import create_credentials
from qm import SimulationConfig
from configuration import config, IQ_imbalance
from qm.simulate import LoopbackInterface
# import matplotlib
# matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
# import asyncio
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

qmm = QuantumMachinesManager(host="192.168.1.82", port=80)
qm = qmm.open_qm(config)

# qm.set_dc_offset_by_qe("rr1", "I", 0.05)

with program() as manual_mixer_calib:
    with infinite_loop_():
        # play("cw", "rr2")
        play("cw", "q1_xy")
        # play("cw", "rrc")
 
job = qm.execute(manual_mixer_calib)

# job = qmm.simulate(config, manual_mixer_calib, SimulationConfig(4000))
# job.get_simulated_samples().con1.plot()
# plt.show()
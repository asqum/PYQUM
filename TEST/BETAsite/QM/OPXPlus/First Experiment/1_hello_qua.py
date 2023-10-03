from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm.simulate.credentials import create_credentials
from qm import SimulationConfig
from configuration import config, qop_ip
from qm.simulate import LoopbackInterface
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
# import asyncio
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# QUA program
with program() as hello_qua:
    
    play("cw", "q1_xy")

# open communication with opx
# qmm = QuantumMachinesManager(host="niv-0ce2f504.dev.quantum-machines.co", port=443, credentials=create_credentials())
qmm = QuantumMachinesManager(host=qop_ip, port=80)

# simulate the test_config QUA program
job = qmm.simulate(config, hello_qua, SimulationConfig(400))
job.get_simulated_samples().con1.plot()
plt.show()
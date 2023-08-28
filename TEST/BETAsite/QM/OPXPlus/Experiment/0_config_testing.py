# config_testing.py tests all the operations in the configuration file 

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm.simulate.credentials import create_credentials
from qm import SimulationConfig
from configuration import config
from qm.simulate import LoopbackInterface
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# QUA program
with program() as test_config:
    
    I1 = declare(fixed)
    I2 = declare(fixed)
    Ic = declare(fixed)
    I1_st = declare_stream()
    I2_st = declare_stream()
    Ic_st = declare_stream()

    play("cw", "rr1")
    measure("readout", "rr1", None, dual_demod.full("cos", "out1", "sin", "out2", I1))
    save(I1, I1_st)
    play("cw", "rr2")
    measure("readout", "rr2", None, dual_demod.full("cos", "out1", "sin", "out2", I2))
    save(I2, I2_st)
    play("cw", "rrc")
    measure("readout", "rrc", None, dual_demod.full("cos", "out1", "sin", "out2", Ic))
    save(Ic, Ic_st)

    align()
    update_frequency("q1_xy", 0)
    play("cw", "q1_xy")
    play("x180", "q1_xy")
    play("x90", "q1_xy")
    play("-x90", "q1_xy")
    play("y90", "q1_xy")
    play("y180", "q1_xy")
    play("-y90", "q1_xy")
    update_frequency("q2_xy", 0)
    play("cw", "q2_xy")
    play("x180", "q2_xy")
    play("x90", "q2_xy")
    play("-x90", "q2_xy")
    play("y90", "q2_xy")
    play("y180", "q2_xy")
    play("-y90", "q2_xy")

    align()
    play("const", "q1_z")
    play("const"*amp(0.8), "q2_z")
    play("const"*amp(0.6), "qc_z")

    with stream_processing():
        I1_st.save_all("I1")
        I2_st.save_all("I2")
        Ic_st.save_all("Ic")


# open communication with opx
# qmm = QuantumMachinesManager(host="niv-0ce2f504.dev.quantum-machines.co", port=443, credentials=create_credentials())
qmm = QuantumMachinesManager(host="172.16.2.123", port=80)

# simulate the test_config QUA program
job = qmm.simulate(config, test_config, SimulationConfig(400))
job.get_simulated_samples().con1.plot()
print(job.result_handles.get("I1").fetch_all())
print(job.result_handles.get("I2").fetch_all())
print('niv')
plt.show()

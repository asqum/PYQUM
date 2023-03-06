# config_testing.py tests all the operations in the configuration file 

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm.simulate.credentials import create_credentials
from qm import SimulationConfig
from configuration import *
from qm.simulate import LoopbackInterface
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
# import asyncio
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qualang_tools.analysis import two_state_discriminator

pts = 20000
s = 1.0

# QUA program
with program() as iq_blobs:

    n = declare(int)
    I_g = [declare(fixed) for i in range(2)]
    Q_g = [declare(fixed) for i in range(2)]
    I_g_st = [declare_stream() for i in range(2)]
    Q_g_st = [declare_stream() for i in range(2)]
    I_e = [declare(fixed) for i in range(2)]
    Q_e = [declare(fixed) for i in range(2)]
    I_e_st = [declare_stream() for i in range(2)]
    Q_e_st = [declare_stream() for i in range(2)]

    with for_(n, 0, n < pts, n + 1):
        
        # ground iq blobs for both qubits
        wait(10000)
        align()
        measure("readout"*amp(s), "rr1", None, dual_demod.full("rotated_cos", "out1", "rotated_minus_sin", "out2", I_g[0]),
                dual_demod.full("rotated_sin", "out1", "rotated_cos", "out2", Q_g[0]))
        measure("readout"*amp(s), "rr2", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", I_g[1]),
                dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", Q_g[1]))
        save(I_g[0], I_g_st[0])
        save(Q_g[0], Q_g_st[0])
        save(I_g[1], I_g_st[1])
        save(Q_g[1], Q_g_st[1])

        # excited iq blobs for both qubits
        wait(10000)
        align()
        play("flattop", "q2_xy")
        align()
        measure("readout"*amp(s), "rr1", None, dual_demod.full("rotated_cos", "out1", "rotated_minus_sin", "out2", I_e[0]),
                dual_demod.full("rotated_sin", "out1", "rotated_cos", "out2", Q_e[0]))
        measure("readout"*amp(s), "rr2", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", I_e[1]),
                dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", Q_e[1]))
        save(I_e[0], I_e_st[0])
        save(Q_e[0], Q_e_st[0])
        save(I_e[1], I_e_st[1])
        save(Q_e[1], Q_e_st[1])
    
    with stream_processing():
        for i in range(2):
            I_g_st[i].save_all(f"I_g_q{i}")
            Q_g_st[i].save_all(f"Q_g_q{i}")
            I_e_st[i].save_all(f"I_e_q{i}")
            Q_e_st[i].save_all(f"Q_e_q{i}")

# open communication with opx
qmm = QuantumMachinesManager(host="192.168.1.82", port=80)

# open quantum machine
qm = qmm.open_qm(config)

# run job 
job = qm.execute(iq_blobs)

# fetch data
job.result_handles.wait_for_all_values()
results = fetching_tool(job, ["I_g_q0", "Q_g_q0", "I_e_q0", "Q_e_q0", "I_g_q1", "Q_g_q1", "I_e_q1", "Q_e_q1"])
I_g_q1, Q_g_q1, I_e_q1, Q_e_q1, I_g_q2, Q_g_q2, I_e_q2, Q_e_q2 = results.fetch_all()

two_state_discriminator(I_g_q1, Q_g_q1, I_e_q1, Q_e_q1, True, True)
plt.suptitle("qubit 1")
two_state_discriminator(I_g_q2, Q_g_q2, I_e_q2, Q_e_q2, True, True)
plt.suptitle("qubit 2")
plt.show()
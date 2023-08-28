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

pts = 4000
s = 1.0
freqs = np.arange(-0.5e6, 0.5e6, 0.02e6) + resonator_IF_q2

# QUA program
with program() as iq_blobs:

    n = declare(int)
    I_g = [declare(fixed) for i in range(2)]
    Q_g = [declare(fixed) for i in range(2)]
    I_e = [declare(fixed) for i in range(2)]
    Q_e = [declare(fixed) for i in range(2)]
    DI = declare(fixed)
    DQ = declare(fixed)
    D = declare(fixed)
    f = declare(int)
    D_st = declare_stream()

    with for_(n, 0, n < pts, n + 1):
        
        with for_(*from_array(f, freqs)):
            
            update_frequency("rr2", f)

            # ground iq blobs for both qubits
            wait(10000)
            align()
            measure("readout"*amp(s), "rr1", None, dual_demod.full("rotated_cos", "out1", "rotated_minus_sin", "out2", I_g[0]),
                    dual_demod.full("rotated_sin", "out1", "rotated_cos", "out2", Q_g[0]))
            measure("readout"*amp(s), "rr2", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", I_g[1]),
                    dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", Q_g[1]))
            
            # excited iq blobs for both qubits
            wait(10000)
            align()
            play("flattop", "q2_xy")
            align()
            measure("readout"*amp(s), "rr1", None, dual_demod.full("rotated_cos", "out1", "rotated_minus_sin", "out2", I_e[0]),
                    dual_demod.full("rotated_sin", "out1", "rotated_cos", "out2", Q_e[0]))
            measure("readout"*amp(s), "rr2", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", I_e[1]),
                    dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", Q_e[1]))

            assign(DI, (I_e[1]-I_g[1])*100)
            assign(DQ, (Q_e[1]-Q_g[1])*100)
            assign(D, DI*DI+DQ*DQ)
            save(D, D_st)
        
    with stream_processing():
        D_st.buffer(len(freqs)).average().save('D')
        
# open communication with opx
qmm = QuantumMachinesManager(host=qop_ip, port=80)

# open quantum machine
qm = qmm.open_qm(config)

# run job 
job = qm.execute(iq_blobs)

# fetch data
job.result_handles.wait_for_all_values()
results = fetching_tool(job, ["D"])
D = results.fetch_all()
plt.plot(freqs-resonator_IF_q2, D[0])
plt.show()

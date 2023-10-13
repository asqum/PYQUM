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
from qm.simulate import LoopbackInterface

fres_q1 = resonator_IF_q1
fres_q2 = resonator_IF_q2
dfs = np.arange(- 5e6, + 5e6, 0.05e6)
n_avg = 1000

# QUA program
with program() as multi_res_spec:
    
    I = [declare(fixed) for i in range(2)]
    Q = [declare(fixed) for i in range(2)] 
    I_st = [declare_stream() for i in range(2)]
    Q_st = [declare_stream() for i in range(2)]
    n = declare(int)
    df = declare(int)
    f_q1 = declare(int)
    f_q2 = declare(int)

    with for_(n, 0, n < n_avg, n+1):

        with for_(*from_array(df, dfs)):
            
            # wait for the resonators to relax 
            wait(250, "rr1", "rr2")

            # resonator 1
            assign(f_q1, df + fres_q1)
            update_frequency("rr1", f_q1)
            measure("readout", "rr1", None, dual_demod.full("cos", "out1", "sin", "out2", I[0]),
            dual_demod.full("minus_sin", "out1", "cos", "out2", Q[0]))
            save(I[0], I_st[0])
            save(Q[0], Q_st[0])
            
            # resonator 2 (in parallel)
            assign(f_q2, df + fres_q2)
            update_frequency("rr2", f_q2)
            measure("readout", "rr2", None, dual_demod.full("cos", "out1", "sin", "out2", I[1]),
            dual_demod.full("minus_sin", "out1", "cos", "out2", Q[1]))
            save(I[1], I_st[1])
            save(Q[1], Q_st[1])

    with stream_processing():

        # resonator 1
        I_st[0].buffer(len(dfs)).average().save("I1")
        Q_st[0].buffer(len(dfs)).average().save("Q1")
        
        # resonator 2
        I_st[1].buffer(len(dfs)).average().save("I2")
        Q_st[1].buffer(len(dfs)).average().save("Q2")
        


# open communication with opx
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

# simulate the test_config QUA program
# job = qmm.simulate(config, multi_res_spec, SimulationConfig(11000, 
# simulation_interface=LoopbackInterface([("con1", 1, "con1", 1), ("con1", 2, "con1", 2) ], latency=250)))
# job.get_simulated_samples().con1.plot()

# execute QUA:
qm = qmm.open_qm(config)
job = qm.execute(multi_res_spec)
res_handle = job.result_handles
res_handle.wait_for_all_values()

plt.show()
results = fetching_tool(job, ["I1", "Q1", "I2", "Q2"])
I1, Q1, I2, Q2 = results.fetch_all()

s1 = I1 + 1j*Q1
s2 = I2 + 1j*Q2

u = unit()
LO = resonator_LO/u.MHz

# plt.figure()
fig, ax = plt.subplots(1, 2)

ax[0].plot( -dfs/u.MHz, np.abs(s1))
ax[0].set_title("rr1")
ax[0].set_ylabel("Amp (V)")
ax[0].set_xlabel("Freq (MHz)")
ax[1].plot( -dfs/u.MHz, np.abs(s2))
ax[1].set_title("rr2")
ax[1].set_xlabel("Freq (MHz)")

# plt.plot(I1, Q1, '.')
# plt.plot(I2, Q2, '.')
# plt.axis('equal')

plt.show()

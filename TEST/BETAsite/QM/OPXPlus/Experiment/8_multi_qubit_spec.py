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
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter

t = 17000//4 //100
fres_q1 = qubit_IF_q1
fres_q2 = qubit_IF_q2
dfs = np.arange(- 20e6, + 20e6, 0.5e6)
n_avg = 10000000

# QUA program
with program() as multi_qubit_spec:
    
    I = [declare(fixed) for i in range(2)]
    Q = [declare(fixed) for i in range(2)] 
    I_st = [declare_stream() for i in range(2)]
    Q_st = [declare_stream() for i in range(2)]
    n = declare(int)
    n_st = declare_stream()
    df = declare(int)
    f_q1 = declare(int)
    f_q2 = declare(int)

    # set_dc_offset("q1_z", "single", 0.4)
    # set_dc_offset("q2_z", "single", -0.48)
    with for_(n, 0, n < n_avg, n+1):
        
        save(n, n_st)

        with for_(*from_array(df, dfs)):

            assign(f_q1, df + fres_q1)
            update_frequency("q1_xy", f_q1)
            # assign(f_q2, df + fres_q2)
            # update_frequency("q2_xy", f_q2)  

            wait(4000)

            # qubit 1
            play("cw"*amp(0.77), "q1_xy", duration=t)
            align("q1_xy", "rr1")
            measure("readout"*amp(1.0), "rr1", None, dual_demod.full("cos", "out1", "minus_sin", "out2", I[0]),
            dual_demod.full("sin", "out1", "cos", "out2", Q[0]))
            save(I[0], I_st[0])
            save(Q[0], Q_st[0])
            
            # qubit 2
            # play("cw"*amp(0.037), "q2_xy", duration=t)
            # align("q2_xy", "rr2")
            measure("readout"*amp(0.8), "rr2", None, dual_demod.full("cos", "out1", "sin", "out2", I[1]),
            dual_demod.full("minus_sin", "out1", "cos", "out2", Q[1]))
            save(I[1], I_st[1])
            save(Q[1], Q_st[1])

    with stream_processing():

        n_st.save("n")

        # resonator 1
        I_st[0].buffer(len(dfs)).average().save("I1")
        Q_st[0].buffer(len(dfs)).average().save("Q1")
        
        # resonator 2
        I_st[1].buffer(len(dfs)).average().save("I2")
        Q_st[1].buffer(len(dfs)).average().save("Q2")
        


# open communication with opx
qmm = QuantumMachinesManager(host="192.168.1.82", port=80)

# simulate the test_config QUA program
# job = qmm.simulate(config, multi_qubit_spec, SimulationConfig(11000, 
# simulation_interface=LoopbackInterface([("con1", 1, "con1", 1), ("con1", 2, "con1", 2) ], latency=250)))
# job.get_simulated_samples().con1.plot()

# execute QUA:
qm = qmm.open_qm(config)
job = qm.execute(multi_qubit_spec)
res_handle = job.result_handles
# res_handle.wait_for_all_values()

# plt.show()
LO = qubit_LO/u.MHz
IF1 = -qubit_IF_q1/u.MHz
IF2 = -qubit_IF_q2/u.MHz

fig, ax = plt.subplots(2, 2)
interrupt_on_close(fig, job)


while job.result_handles.is_processing():
    results = fetching_tool(job, ["n", "I1", "Q1", "I2", "Q2"], mode="live")
    n, I1, Q1, I2, Q2 = results.fetch_all()
    progress_counter(n, n_avg)
    s1 = I1 + 1j*Q1
    s2 = I2 + 1j*Q2

    u = unit()

    ax[0,0].cla()
    ax[1,0].cla()
    ax[0,1].cla()
    ax[1,1].cla()
    # ax[0].plot( - fres_q1/u.MHz - dfs/u.MHz, np.abs(s1))
    ax[0,0].plot(- dfs/u.MHz, np.abs(s1))
    ax[0,0].set_title("q1 amp (fcent1: %s, n: %s)" %(LO+IF1,n))
    ax[1,0].plot(- dfs/u.MHz, np.angle(s1))
    ax[1,0].set_title("q1 pha (fcent1: %s, n: %s)" %(LO+IF1,n))
    # ax[1].plot( - fres_q2/u.MHz - dfs/u.MHz, np.abs(s2))
    ax[0,1].plot(- dfs/u.MHz, np.abs(s2))
    ax[0,1].set_title("q2 amp (fcent2: %s, n: %s)" %(LO+IF2,n))
    ax[1,1].plot(- dfs/u.MHz, np.angle(s2))
    ax[1,1].set_title("q2 pha (fcent2: %s, n: %s)" %(LO+IF2,n))
    plt.pause(1.0)

# plt.plot(I1, Q1, '.')
# plt.plot(I2, Q2, '.')
# plt.axis('equal')

plt.show()

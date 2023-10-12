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
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.plot import interrupt_on_close
from qm.simulate import LoopbackInterface

amps = np.arange(0.005, 1.99, 0.005)
max_amp = 1.5
min_amp = 0.1
n_max = max_amp**2
n_min = min_amp**2

logn_max = np.log10(n_max)*10
logn_min = np.log10(n_min)*10
logn_list = np.linspace(logn_min, logn_max, 20)
print(logn_max,logn_min)
amps = 10**(logn_list/10/2)
print(amps[0],amps[-1])
fres_q1 = resonator_IF_q1
fres_q2 = resonator_IF_q2
dfs = np.arange(-2.0e6, + 2.0e6, 0.02e6)
n_avg = 10000

# QUA program
with program() as multi_res_spec_vs_amp:
    
    I = [declare(fixed) for i in range(2)]
    Q = [declare(fixed) for i in range(2)] 
    I_st = [declare_stream() for i in range(2)]
    Q_st = [declare_stream() for i in range(2)]
    n = declare(int)
    df = declare(int)
    f_q1 = declare(int)
    f_q2 = declare(int)
    a = declare(fixed)
    n_st = declare_stream()

    with for_(n, 0, n < n_avg, n+1):

        save(n, n_st)

        with for_(*from_array(df, dfs)):

            assign(f_q1, df +fres_q1)
            update_frequency("rr1", f_q1)
            assign(f_q2, df +fres_q2)
            update_frequency("rr2", f_q2)

            with for_(*from_array(a, amps)):
            
                # wait for the resonators to relax 
                wait(1000, "rr1")

                # resonator 1
                measure("readout"*amp(a), "rr1", None, dual_demod.full("cos", "out1", "sin", "out2", I[0]),
                dual_demod.full("minus_sin", "out1", "cos", "out2", Q[0]))
                save(I[0], I_st[0])
                save(Q[0], Q_st[0])

                # align("rr1", "rr2") # sequential to avoid overflow
                wait(1000, "rr2")

                # resonator 2 (sequential)
                measure("readout"*amp(a), "rr2", None, dual_demod.full("cos", "out1", "sin", "out2", I[1]),
                dual_demod.full("minus_sin", "out1", "cos", "out2", Q[1]))
                save(I[1], I_st[1])
                save(Q[1], Q_st[1])

    with stream_processing():

        n_st.save("n")

        # resonator 1
        I_st[0].buffer(len(dfs), len(amps)).average().save("I1")
        Q_st[0].buffer(len(dfs), len(amps)).average().save("Q1")
        
        # resonator 2
        I_st[1].buffer(len(dfs), len(amps)).average().save("I2")
        Q_st[1].buffer(len(dfs), len(amps)).average().save("Q2")
        


# open communication with opx
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

# simulate the test_config QUA program
# job = qmm.simulate(config, multi_res_spec_vs_amp, SimulationConfig(11000, 
# simulation_interface=LoopbackInterface([("con1", 1, "con1", 1), ("con1", 2, "con1", 2) ], latency=250)))
# job.get_simulated_samples().con1.plot()
# plt.show()

# execute QUA:
qm = qmm.open_qm(config)
job = qm.execute(multi_res_spec_vs_amp)
# res_handle = job.result_handles
# res_handle.wait_for_all_values()

u = unit()
LO = resonator_LO/u.MHz

# plt.figure()
fig, ax = plt.subplots(1, 2)
interrupt_on_close(fig, job)

while job.result_handles.is_processing():
    results = fetching_tool(job, ["n", "I1", "Q1", "I2", "Q2"], mode="live")
    n, I1, Q1, I2, Q2 = results.fetch_all()
    progress_counter(n, n_avg)
    s1 = I1 + 1j*Q1
    s2 = I2 + 1j*Q2

    A1 = np.abs(s1)
    A2 = np.abs(s2)

    row_sums = A1.sum(axis=0)
    A1 = A1 / row_sums[np.newaxis, :]
    row_sums = A2.sum(axis=0)
    A2 = A2 / row_sums[np.newaxis, :]


    ax[0].cla()
    ax[0].set_title("rr1-%s (fcent: %s)"%(n, LO -fres_q1/u.MHz))
    ax[0].set_xlabel("amp")
    ax[0].set_ylabel("freq")
    ax[0].pcolor(logn_list,  dfs/u.MHz, A1)
    ax[1].cla()
    ax[1].set_title("rr2-%s (fcent: %s)"%(n, LO -fres_q2/u.MHz))
    ax[1].set_xlabel("amp")
    ax[1].set_ylabel("freq")
    ax[1].pcolor(logn_list,  dfs/u.MHz, A2)

    plt.pause(1.0) # every second

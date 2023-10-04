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

fres_q1 = qubit_IF_q1
fres_q2 = qubit_IF_q2
t_idx_delay = np.arange(0, 3000, 10)
n_avg = 100000
fvec = np.arange(-1e6, 1e6, 0.02e6)

# QUA program
with program() as ramsey:
    
    I = [declare(fixed) for i in range(2)]
    Q = [declare(fixed) for i in range(2)]
    I_st = [declare_stream() for i in range(2)]
    Q_st = [declare_stream() for i in range(2)]
    n = declare(int)
    n_st = declare_stream()
    t = declare(int)
    f = declare(int)

    with for_(n, 0, n < n_avg, n+1):
        
        save(n, n_st)

        with for_(*from_array(f, fvec)):

            update_frequency("q1_xy", f + fres_q1)
            update_frequency("q2_xy", f + fres_q2)

            with for_(*from_array(t, t_idx_delay)):
                    
                wait(10000)

                # qubit 1
                play("x90", "q1_xy")
                wait(t, "q1_xy")
                play("x90", "q1_xy")

                # qubit 2
                play("x90", "q2_xy")
                wait(t, "q2_xy")
                play("x90", "q2_xy")

                align() # equivalent to align("q2_xy", "rr1", "rr2")

                # a. rotated readout:
                measure("readout"*amp(1), "rr1", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", I[0]),
                        dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", Q[0]))
                save(I[0], I_st[0])
                # save(Q[0], Q_st[0])
                measure("readout"*amp(1), "rr2", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", I[1]),
                        dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", Q[1]))
                save(I[1], I_st[1])
                # save(Q[1], Q_st[1])

                # b. normal readout:
                # measure("readout"*amp(1.0), "rr1", None, dual_demod.full("cos", "out1", "minus_sin", "out2", I[0]),
                # dual_demod.full("sin", "out1", "cos", "out2", Q[0]))
                # save(I[0], I_st[0])
                # save(Q[0], Q_st[0])
                # measure("readout"*amp(1.0), "rr2", None, dual_demod.full("cos", "out1", "sin", "out2", I[1]),
                # dual_demod.full("minus_sin", "out1", "cos", "out2", Q[1]))
                # save(I[1], I_st[1])
                # save(Q[1], Q_st[1])

    with stream_processing():

        n_st.save("n")

        # resonator 1
        I_st[0].buffer(len(fvec), len(t_idx_delay)).average().save("I1")
        # Q_st[0].buffer(len(fvec), len(t_idx_delay)).average().save("Q1")
        # resonator 2
        I_st[1].buffer(len(fvec), len(t_idx_delay)).average().save("I2")
        # Q_st[1].buffer(len(fvec), len(t_idx_delay)).average().save("Q2")


# open communication with opx
qmm = QuantumMachinesManager(host=qop_ip, port=80)

# simulate the test_config QUA program
# job = qmm.simulate(config, ramsey, SimulationConfig(11000))
# job.get_simulated_samples().con1.plot()
# plt.show()

# execute QUA:
qm = qmm.open_qm(config)
job = qm.execute(ramsey)
res_handle = job.result_handles
# res_handle.wait_for_all_values()

# plt.show()
LO = qubit_LO_q1/u.MHz
IF1 = -fres_q1/u.MHz
IF2 = -fres_q2/u.MHz

fig, ax = plt.subplots(1,2)
interrupt_on_close(fig, job)
t_delay = 4*t_idx_delay
while job.result_handles.is_processing():
    # results = fetching_tool(job, ["n", "I1", "Q1", "I2", "Q2"], mode="live")
    results = fetching_tool(job, ["n", "I1", "I2"], mode="live")
    # n, I1, Q1, I2, Q2 = results.fetch_all()
    n, I1, I2 = results.fetch_all()
    progress_counter(n, n_avg)

    u = unit()
    ax[0].cla()
    ax[0].pcolor(t_delay, fvec, I1)
    ax[0].set_title('Q1-I, n={}, fcent={}'.format(n, LO+IF1))
    # ax[1,0].cla()
    # ax[1,0].pcolor(t_delay, fvec, Q1)
    # ax[1,0].set_title('Q1-Q, n={}'.format(n))
    ax[1].cla()
    ax[1].pcolor(t_delay, fvec, I2)
    ax[1].set_title('Q2-I, n={}, fcent={}'.format(n, LO+IF2))
    # ax[1,1].cla()
    # ax[1,1].pcolor(t_delay, fvec, Q2)
    # ax[1,1].set_title('Q2-Q, n={}'.format(n))
    plt.pause(1.0)

plt.show()

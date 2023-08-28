# config_testing.py tests all the operations in the configuration file 

# from qm.QuantumMachinesManager import QuantumMachinesManager
# from qm.qua import *
# from qm.simulate.credentials import create_credentials
# from qm import SimulationConfig
# from configuration import *
# from qm.simulate import LoopbackInterface
# import matplotlib
# matplotlib.use('TKAgg')
# import matplotlib.pyplot as plt
# # import asyncio
# # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# from qualang_tools.loops import from_array
# from qualang_tools.results import fetching_tool
# from qm.simulate import LoopbackInterface
# from qualang_tools.plot import interrupt_on_close
# from qualang_tools.results import progress_counter


####################
# QUA START        #
####################

from qm.qua import *
from configuration import *
from qualang_tools.loops import from_array

t_delay = np.arange(4, 3500, 40)
n_avg = 1000000

# QUA program
with program() as TASK:
    
    I = [declare(fixed) for i in range(2)]
    Q = [declare(fixed) for i in range(2)]
    I_st = [declare_stream() for i in range(2)]
    Q_st = [declare_stream() for i in range(2)]
    n = declare(int)
    n_st = declare_stream()
    t = declare(int)

    with for_(n, 0, n < n_avg, n+1):
        
        save(n, n_st)

        with for_(*from_array(t, t_delay)):
                
            wait(10000)

            # qubit 1
            play("x180_ft", "q1_xy")
            wait(t, "q1_xy")

            # qubit 2
            play("x180_ft", "q2_xy")
            wait(t, "q2_xy")

            align() # equivalent to align("q2_xy", "rr1", "rr2")

            measure("readout"*amp(1.0), "rr1", None, dual_demod.full("rotated_cos", "out1", "rotated_minus_sin", "out2", I[0]),
            dual_demod.full("rotated_sin", "out1", "rotated_cos", "out2", Q[0]))
            save(I[0], I_st[0])
            save(Q[0], Q_st[0])
            measure("readout"*amp(1.0), "rr2", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", I[1]),
            dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", Q[1]))
            save(I[1], I_st[1])
            save(Q[1], Q_st[1])

    with stream_processing():

        n_st.save("n")

        # resonator 1
        I_st[0].buffer(len(t_delay)).average().save("I1")
        Q_st[0].buffer(len(t_delay)).average().save("Q1")
        
        # resonator 2
        I_st[1].buffer(len(t_delay)).average().save("I2")
        Q_st[1].buffer(len(t_delay)).average().save("Q2")

        # Oracle SCOPE:
        SCOPE = ["n", "I1", "Q1", "I2", "Q2"]

####################
# QUA END          #
####################


# # open communication with opx
# qmm = QuantumMachinesManager(host=qop_ip, port=80)

# # simulate the test_config QUA program
# # job = qmm.simulate(config, TASK, SimulationConfig(11000))
# # job.get_simulated_samples().con1.plot()
# # plt.show()

# # execute QUA:
# qm = qmm.open_qm(config)
# job = qm.execute(TASK)
# res_handle = job.result_handles
# # res_handle.wait_for_all_values()

# # plt.show()
# LO = qubit_LO/u.MHz

# fig, ax = plt.subplots(2,2)
# interrupt_on_close(fig, job)

# while job.result_handles.is_processing():
#     results = fetching_tool(job, ["n", "I1", "Q1", "I2", "Q2"], mode="live")
#     n, I1, Q1, I2, Q2 = results.fetch_all()
#     progress_counter(n, n_avg)

#     u = unit()
#     ax[0,0].cla()
#     ax[0,0].plot(4*t_delay, I1)
#     ax[0,0].set_title('n={}'.format(n))
#     ax[1,0].cla()
#     ax[1,0].plot(4*t_delay, Q1)
#     ax[1,0].set_title('n={}'.format(n))
#     ax[0,1].cla()
#     ax[0,1].plot(4*t_delay, I2)
#     ax[0,1].set_title('n={}'.format(n))
#     ax[1,1].cla()
#     ax[1,1].plot(4*t_delay, Q2)
#     ax[1,1].set_title('n={}'.format(n))
#     plt.pause(1.0)

# plt.show()

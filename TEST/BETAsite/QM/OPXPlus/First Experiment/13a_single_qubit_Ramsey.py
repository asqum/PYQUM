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
from qualang_tools.plot.fitting import Fit

fres_q1 = qubit_IF_q1
fres_q2 = qubit_IF_q2
t_delay = np.arange(0, 15000, 100)
Phi = np.arange(0, 5, 0.05) # 5 rotations
n_avg = 100000

# QUA program
with program() as ramsey:
    
    I = [declare(fixed) for i in range(2)]
    Q = [declare(fixed) for i in range(2)] 
    I_st = [declare_stream() for i in range(2)]
    Q_st = [declare_stream() for i in range(2)]
    n = declare(int)
    n_st = declare_stream()
    t = declare(int)
    phi = declare(fixed)

    with for_(n, 0, n < n_avg, n+1):
        
        save(n, n_st)

        update_frequency("q1_xy", fres_q1 + 0.25e6)
        update_frequency("q2_xy", fres_q2 + 0.25e6)

        # with for_(*from_array(t, t_delay)):
        with for_(*from_array(phi, Phi)):
                
            wait(20000)

            # qubit 1
            play("x90", "q1_xy")
            # wait(t, "q1_xy")
            frame_rotation_2pi(phi, "q1_xy")
            play("x90", "q1_xy")

            # qubit 2
            play("x90", "q2_xy")
            # wait(t, "q2_xy")
            frame_rotation_2pi(phi, "q2_xy")
            play("x90", "q2_xy")

            align() # equivalent to align("q2_xy", "rr1", "rr2")

            # rotated readout:
            measure("readout"*amp(1.0), "rr1", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", I[0]),
                    dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", Q[0]))
            save(I[0], I_st[0])
            save(Q[0], Q_st[0])
            measure("readout"*amp(1.0), "rr2", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", I[1]),
                    dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", Q[1]))
            save(I[1], I_st[1])
            save(Q[1], Q_st[1])


    with stream_processing():

        n_st.save("n")
        # var = t_delay
        var = Phi

        # resonator 1
        I_st[0].buffer(len(var)).average().save("I1")
        Q_st[0].buffer(len(var)).average().save("Q1")
        # resonator 2
        I_st[1].buffer(len(var)).average().save("I2")
        Q_st[1].buffer(len(var)).average().save("Q2")

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

fit = Fit()
# fig, ax = plt.subplots(1,2)
fig = plt.figure()
interrupt_on_close(fig, job)

while job.result_handles.is_processing():
    results = fetching_tool(job, ["n", "I1", "Q1", "I2", "Q2"], mode="live")
    n, I1, Q1, I2, Q2 = results.fetch_all()
    progress_counter(n, n_avg)

    u = unit()
    plt.cla()
    # x_var = 4*t_delay
    x_var = Phi

    plt.subplot(121)
    plt.cla()
    plt.plot(x_var, I1)
    ramsey_fit = fit.ramsey(x_var, I1, plot=True)
    # qubit_T1 = np.round(np.abs(ramsey_fit["T1"][0]) / 4) * 4
    plt.title('n={}'.format(n))
    
    plt.subplot(122)
    plt.cla()
    plt.plot(x_var, I2)
    ramsey_fit = fit.ramsey(x_var, I2, plot=True)
    plt.title('n={}'.format(n))

    plt.pause(1.0)

plt.show()

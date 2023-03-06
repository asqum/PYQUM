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

t_delay = np.arange(4, 100, 1)
n_avg = 100000
dphi = 10e6 * (t_delay[1]-t_delay[0])*(4e-9)

# QUA program
with program() as ramsey:
    
    I = [declare(fixed) for i in range(2)]
    # Q = [declare(fixed) for i in range(2)] 
    I_st = [declare_stream() for i in range(2)]
    # Q_st = [declare_stream() for i in range(2)]
    n = declare(int)
    n_st = declare_stream()
    t = declare(int)
    phi = declare(fixed)

    with for_(n, 0, n < n_avg, n+1):
        
        save(n, n_st)

        assign(phi, 0)
        with for_(*from_array(t, t_delay)):
                
            wait(10000)

            # qubit 2
            play("x90_ft", "q2_xy")
            wait(t, "q2_xy")
            frame_rotation_2pi(phi)
            play("x90_ft", "q2_xy")

            align() # equivalent to align("q2_xy", "rr1", "rr2")

            measure("readout"*amp(1), "rr1", None, dual_demod.full("rotated_cos", "out1", "rotated_minus_sin", "out2", I[0]))
            save(I[0], I_st[0])
            measure("readout"*amp(1), "rr2", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", I[1]))
            save(I[1], I_st[1])

            assign(phi, phi + dphi)

    with stream_processing():

        n_st.save("n")

        # resonator 1
        I_st[0].buffer(len(t_delay)).average().save("I1")
        
        # resonator 2
        I_st[1].buffer(len(t_delay)).average().save("I2")


# open communication with opx
qmm = QuantumMachinesManager(host="192.168.1.82", port=80)

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
LO = qubit_LO/u.MHz

fig = plt.figure()
interrupt_on_close(fig, job)

while job.result_handles.is_processing():
    results = fetching_tool(job, ["n", "I1", "I2"], mode="live")
    n, I1, I2 = results.fetch_all()
    progress_counter(n, n_avg)

    u = unit()
    plt.cla()
    plt.plot(4*t_delay, I2)
    plt.title('n={}'.format(n))
    plt.pause(1.0)

plt.show()

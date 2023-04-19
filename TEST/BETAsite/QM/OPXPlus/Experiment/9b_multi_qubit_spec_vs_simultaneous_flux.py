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

num_pts = 100
t = 17000//4 #//100
fres_q1 = qubit_IF_q1
fres_q2 = qubit_IF_q2
# dfs1 = np.linspace(- 450e6, + 200e6, num_pts) # qubit 1
dfs1 = np.linspace( -100e6, 380e6, num_pts) # qubit 1
ddf1 = dfs1[1] - dfs1[0]
dcs1 = np.linspace(-0.49, 0.49, num_pts) # flux 1
ddc1 = dcs1[1] - dcs1[0]
# dfs2 = np.linspace(- 450e6, + 100e6, num_pts) # qubit 2
dfs2 = np.linspace(- 120e6, 160e6, num_pts) # qubit 2
ddf2 = dfs2[1] - dfs2[0]
dcs2 = np.linspace(-0.49, 0.49, num_pts) # flux 2 
ddc2 = dcs2[1] - dcs2[0]
n_avg = 4000000

# Equalization for comparison:
fres_q2 = fres_q1
dfs2 = dfs1
ddf2 = ddf1

# QUA program
with program() as multi_qubit_spec_vs_flux:
    
    I = [declare(fixed) for i in range(2)]
    Q = [declare(fixed) for i in range(2)] 
    I_st = [declare_stream() for i in range(2)]
    Q_st = [declare_stream() for i in range(2)]
    n = declare(int)
    n_st = declare_stream()
    f_q1 = declare(int)
    f_q2 = declare(int)
    dc1 = declare(fixed)
    dc2 = declare(fixed)
    i = declare(int)
    j = declare(int)

    with for_(n, 0, n < n_avg, n+1):
        
        save(n, n_st)
        
        assign(f_q1, dfs1[0] + fres_q1)
        assign(f_q2, dfs2[0] + fres_q2)

        with for_(i, 0, i<num_pts, i+1):

            update_frequency("q1_xy", f_q1)
            update_frequency("q2_xy", f_q2)  

            # assign(dc1, dcs1[0])
            assign(dc2, dcs2[0])

            with for_(j, 0, j<num_pts, j+1):

                # Flux sweeping 
                # set_dc_offset("q1_z", "single", dc1)
                set_dc_offset("q1_z", "single", dc2)
                
                # Saturate qubit
                play("cw"*amp(0.07), "q1_xy", duration=t)
                play("cw"*amp(0.3), "q2_xy", duration=t)

                # align()
                
                # readout
                measure("readout"*amp(0.9), "rr1", None, dual_demod.full("cos", "out1", "minus_sin", "out2", I[0]),
                dual_demod.full("sin", "out1", "cos", "out2", Q[0]))
                measure("readout"*amp(0.9), "rr2", None, dual_demod.full("cos", "out1", "sin", "out2", I[1]),
                dual_demod.full("minus_sin", "out1", "cos", "out2", Q[1]))
                save(I[0], I_st[0])
                save(Q[0], Q_st[0])
                save(I[1], I_st[1])
                save(Q[1], Q_st[1])

                # assign(dc1, dc1 + ddc1)
                assign(dc2, dc2 + ddc2)
                
                # DC waiting time will affect the edges of the curve:
                wait(1000)

            assign(f_q1, f_q1 + ddf1)
            assign(f_q2, f_q2 + ddf2)

    with stream_processing():

        n_st.save("n")

        # resonator 1
        I_st[0].buffer(num_pts, num_pts).average().save("I1")
        Q_st[0].buffer(num_pts, num_pts).average().save("Q1")
        
        # resonator 2
        I_st[1].buffer(num_pts, num_pts).average().save("I2")
        Q_st[1].buffer(num_pts, num_pts).average().save("Q2")
        


# open communication with opx
# qmm = QuantumMachinesManager(host="192.168.1.82", port=80)
qmm = QuantumMachinesManager(host=qop_ip, port=80)

simulate = False

if simulate:
    # simulate the test_config QUA program
    job = qmm.simulate(config, multi_qubit_spec_vs_flux, SimulationConfig(110000, 
    simulation_interface=LoopbackInterface([("con1", 1, "con1", 1), ("con1", 2, "con1", 2) ], latency=250)))
    job.get_simulated_samples().con1.plot()
    plt.show()

else:
    # # execute QUA:
    qm = qmm.open_qm(config)
    job = qm.execute(multi_qubit_spec_vs_flux)
    res_handle = job.result_handles
    # res_handle.wait_for_all_values()

    # plt.show()
    LO = qubit_LO/u.MHz
    IF_q1 = -fres_q1/u.MHz
    IF_q2 = -fres_q2/u.MHz

    fig, ax = plt.subplots(2, 3)
    interrupt_on_close(fig, job)


    while job.result_handles.is_processing():
        results = fetching_tool(job, ["n", "I1", "Q1", "I2", "Q2"], mode="live")
        n, I1, Q1, I2, Q2 = results.fetch_all()

        progress_counter(n, n_avg)
        s1 = I1 + 1j*Q1
        s2 = I2 + 1j*Q2

        # Normalize:
        A1 = np.abs(s1)
        P1 = np.unwrap(np.angle(s1))
        A2 = np.abs(s2)
        P2 = np.unwrap(np.angle(s2))

        row_sums = A1.sum(axis=0)
        A1 = A1 / row_sums[np.newaxis, :]
        row_sums = A2.sum(axis=0)
        A2 = A2 / row_sums[np.newaxis, :]

        u = unit()

        ax[0,0].cla()
        ax[1,0].cla()
        ax[0,1].cla()
        ax[1,1].cla()
        ax[0,2].cla()
        ax[1,2].cla()
    
        ax[0,0].set_title("q1 amp (LO: %s, n: %s)" %(LO,n))
        ax[0,0].set_xlabel("flux-1")
        ax[0,0].set_ylabel("freq")
        ax[0,0].pcolor(dcs1, LO + IF_q1 - dfs1/u.MHz, A1)

        ax[1,0].set_title("q1 pha (LO+IF0: %s, n: %s)" %(LO+IF_q1,n))
        ax[1,0].set_xlabel("flux-1")
        ax[1,0].set_ylabel("ifreq")
        ax[1,0].pcolor(dcs1, - dfs1/u.MHz, P1)
    
        ax[0,1].set_title("q2 amp (LO: %s, n: %s)" %(LO,n))
        ax[0,1].set_xlabel("flux-1")
        ax[0,1].pcolor(dcs1, LO + IF_q2 - dfs2/u.MHz, A2)

        ax[1,1].set_title("q2 pha (LO+IF0: %s, n: %s)" %(LO+IF_q2,n))
        ax[1,1].set_xlabel("flux-1")
        ax[1,1].pcolor(dcs1, - dfs2/u.MHz, P2)

        # Add both to compare:
        ax[0,2].set_title("q1 + q2 (Amp)")
        ax[0,2].set_xlabel("flux-1")
        ax[0,2].pcolor(dcs1, LO + IF_q1 - dfs1/u.MHz, A1+A2)

        ax[1,2].set_title("q1 + q2 (Pha)")
        ax[1,2].set_xlabel("flux-1")
        ax[1,2].pcolor(dcs1, - dfs1/u.MHz, P1+P2)

        plt.pause(1.0)

    # plt.plot(I1, Q1, '.')
    # plt.plot(I2, Q2, '.')
    # plt.axis('equal')

    plt.show()

# np.savez(save_dir/"9_multi_qubit_spec_vs_flux.npz", n=n, I1=I1, Q1=Q1, I2=I2, Q2=Q2)
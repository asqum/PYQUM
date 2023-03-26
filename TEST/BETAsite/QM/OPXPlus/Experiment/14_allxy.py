"""
allxy.py: Performs an ALLXY experiment to correct for gates imperfections
(see [Reed's Thesis](https://rsl.yale.edu/sites/default/files/files/RSL_Theses/reed.pdf) for more details)
"""
from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from configuration import *
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import numpy as np
from qm import SimulationConfig
from qualang_tools.loops import from_array
from qualang_tools.results import fetching_tool
from qm.simulate import LoopbackInterface
from qualang_tools.plot import interrupt_on_close
from qualang_tools.results import progress_counter

##############################
# Program-specific variables #
##############################
qb = "q2_xy" # when changing qubit not to forget to change readout resonator
n_points = 10000000
cooldown_time = 10000

# All XY sequences. The sequence names must match corresponding operation in the config
sequence = [  # based on https://rsl.yale.edu/sites/default/files/physreva.82.pdf-optimized_driving_0.pdf
    ("I", "I"),
    ("x180_ft", "x180_ft"),
    ("y180_ft", "y180_ft"),
    ("x180_ft", "y180_ft"),
    ("y180_ft", "x180_ft"),
    ("x90_ft", "I"),
    ("y90_ft", "I"),
    ("x90_ft", "y90_ft"),
    ("y90_ft", "x90_ft"),
    ("x90_ft", "y180_ft"),
    ("y90_ft", "x180_ft"),
    ("x180_ft", "y90_ft"),
    ("y180_ft", "x90_ft"),
    ("x90_ft", "x180_ft"),
    ("x180_ft", "x90_ft"),
    ("y90_ft", "y180_ft"),
    ("y180_ft", "y90_ft"),
    ("x180_ft", "I"),
    ("y180_ft", "I"),
    ("x90_ft", "x90_ft"),
    ("y90_ft", "y90_ft"),
]
# All XY macro generating the pulse sequences from a python list.
def allXY(pulses):
    """
    Generate a QUA sequence based on the two operations written in pulses. Used to generate the all XY program.
    **Example:** I, Q = allXY(['I', 'y90'])
    :param pulses: tuple containing a particular set of operations to play. The pulse names must match corresponding
        operations in the config except for the identity operation that must be called 'I'.
    :return: two QUA variables for the 'I' and 'Q' quadratures measured after the sequence.
    """
    I_xy = declare(fixed)
    if pulses[0] != "I":
        play(pulses[0], qb)  # Either play the sequence
    else:
        wait(tot_ft_len // 4, qb)  # or wait if sequence is identity
    if pulses[1] != "I":
        play(pulses[1], qb)  # Either play the sequence
    else:
        wait(tot_ft_len // 4, qb)  # or wait if sequence is identity

    # change according to the qubit!!
    align(qb, "rr1", "rr2")
    measure("readout", "rr2", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", I_xy))
    measure("readout", "rr1", None)
    return I_xy


###################
# The QUA program #
###################
with program() as ALLXY:
    n = declare(int)
    n_st = declare_stream()
    r = Random()
    r_ = declare(int)
    I_st = [declare_stream() for _ in range(21)]

    with for_(n, 0, n < n_points, n + 1):
        save(n, n_st)
        assign(r_, r.rand_int(21))
        # Can replace by active reset
        wait(cooldown_time, qb)
        # Plays a random XY sequence
        with switch_(r_):
            for i in range(21):
                with case_(i):
                    I= allXY(sequence[i])
                    save(I, I_st[i])
     

    with stream_processing():
        n_st.save("n")
        for i in range(21):
            I_st[i].average().save(f"I{i}")
     
#####################################
#  Open Communication with the QOP  #
#####################################
qmm = QuantumMachinesManager(host=qop_ip, port=80)

simulate = False

if simulate:
    simulation_config = SimulationConfig(duration=50000)  # in clock cycles
    job = qmm.simulate(config, ALLXY, simulation_config)
    job.get_simulated_samples().con1.plot()
    plt.show()

else:

    qm = qmm.open_qm(config)

    job = qm.execute(ALLXY)
    # job.result_handles.wait_for_all_values()
    fig = plt.figure()
    interrupt_on_close(fig, job)

    while job.result_handles.is_processing():
        I = []
        for x in range(21):
            I.append(job.result_handles.get(f"I{x}").fetch_all())
        n = job.result_handles.get("n").fetch_all()
        I = np.array(I)

        plt.cla()
        plt.plot(-I, '-*')
        plt.plot([np.max(-I)]*5 + [(np.mean(-I))]*12 + [np.min(-I)]*4, '-')
        plt.ylabel("I quadrature [a.u.]")
        # plt.xticklabels("")
        plt.xticks(ticks=range(21), labels=[str(el) for el in sequence], rotation=45)
        plt.suptitle("All XY (n: %s)" %(n))
        plt.tight_layout()
        plt.pause(1.0)

    plt.show()
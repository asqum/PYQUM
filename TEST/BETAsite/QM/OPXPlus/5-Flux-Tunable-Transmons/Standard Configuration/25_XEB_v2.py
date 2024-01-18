from qm import QuantumMachinesManager
from qm.qua import *
from configuration import *
from qm.simulate import SimulationConfig
from matplotlib import pyplot as plt
import pprint
from macros import multiplexed_readout, qua_declaration, cz_gate
from qualang_tools.results import progress_counter
import time
import random

# qmm = QuantumMachinesManager(host=qop_ip, cluster_name=cluster_name)
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

qubits = [4, 5]
multiplexed = [4, 5, 1, 2, 3]
cz_type = "const_wf"
simulate = False

random_gates = 3
seqs = 77
depth = 7
avgs = 101
depths = np.arange(depth)

filename = f"XEB_q{qubits[0]}_{qubits[1]}_seqs({seqs})_depth({depth})_avgs({avgs})_random_gates({random_gates})"
# filename = "XEB_test"

"""
0 => x90, [1,0,0,1]
1 => y90, [0,1,-1,0]
2 => x90 + y90, [1, 1, -1, 1] * 0.70710678
"""
x90_amp = [1, 0, 0, 1]
y90_amp = [0, 1, -1, 0]
xy90_amp = [1, 1, -1, 1] * 0.70710678

with program() as xeb:
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=len(multiplexed))
    state = [declare(bool) for _ in range(len(multiplexed))]
    d, d_, _d = declare(int), declare(int), declare(int)
    s = declare(int)
    g = [declare(int, size=depths[-1]) for _ in range(2)]  # Gates for all qubits
    a = [[declare(fixed, size=depths[-1]) for _ in range(4)] for _ in range(2)]  # amplitude matrices for all qubits
    ref_amps = [declare(fixed, value= ref_amp) for ref_amp in [x90_amp, y90_amp, xy90_amp]]
    counts = [declare(int, value=0) for _ in range(4)]
    tot_state_ = declare(int)
    counts_st = [declare_stream() for _ in range(4)]

    state_st = [declare_stream() for _ in range(len(multiplexed))]
    s_st = declare_stream()
    g_st = [declare_stream() for _ in range(2)]
    r = Random();
    r.set_seed(12321)

    if simulate:
        a_st = [[declare_stream() for _ in range(4)] for _ in range(2)]

        for i in range(2):
            update_frequency(f"q{qubits[i]}_xy", 0)

    with for_(s, 0, s < seqs, s + 1):
        with for_each_(d, depths):
            # randomize the sequence
            for q in range(2):
                assign(g[q][0], r.rand_int(3))
                with for_(d_, 1, d_ < d, d_ + 1):
                    assign(g[q][d_], r.rand_int(3))
                    with while_(g[q][d_] == g[q][d_ - 1]):
                        assign(g[q][d_], r.rand_int(3))
                    save(g[q][d_], g_st[q])

            # map sequence indices into amplitude matrix arguments
            if True:
                with for_(_d, 0, _d < d, _d + 1):
                    for q in range(2):
                        with switch_(g[q][_d]):
                            for i in range(3):
                                with case_(i):
                                    for j in range(4):
                                        assign(a[q][j][_d], ref_amps[i][j])
                    if simulate:
                        for q in range(2):
                            for amp_matrix_element in range(4):
                                save(a[q][amp_matrix_element][_d], a_st[q][amp_matrix_element])

            with for_(n, 0, n < avgs, n + 1):

                # play sequence s at depth d
                if True:
                    if simulate:
                        wait(25, *[f"q{qubit}_xy" for qubit in qubits])
                    else:
                        wait(3 * thermalization_time * u.ns, f"q{qubits[0]}_xy", f"q{qubits[1]}_xy")
                    with for_(d_, 0, d_ < d, d_ + 1):
                        for q in range(2):
                            play("x90" * amp(*[a[q][i][_d] for i in range(4)]), f"q{qubits[q]}_xy")

                        # align()
                        # play("cz", "q1_z")
                        # frame_rotation_2pi(0, f"q{qubits[0]}_xy")

                        # align()
                        # cz_gate(2, 1, cz_type)
                        # frame_rotation_2pi(eval(f"cz{1}_{2}_2pi_dev"), "q2_xy")
                        # frame_rotation_2pi(eval(f"cz{2}_{1}_2pi_dev"), "q1_xy")
                        # align()

                        # align()
                        # cz_gate(3, 2, cz_type)
                        # frame_rotation_2pi(eval(f"cz{2}_{3}_2pi_dev"), "q3_xy")
                        # frame_rotation_2pi(eval(f"cz{3}_{2}_2pi_dev"), "q2_xy")
                        # align()

                        # align()
                        # cz_gate(3, 4, cz_type)
                        # frame_rotation_2pi(eval(f"cz{4}_{3}_2pi_dev"), "q4_xy")
                        # frame_rotation_2pi(eval(f"cz{3}_{4}_2pi_dev"), "q3_xy")
                        # align()

                        align()
                        cz_gate(4, 5, cz_type)
                        frame_rotation_2pi(eval(f"cz{5}_{4}_2pi_dev"), "q5_xy")
                        frame_rotation_2pi(eval(f"cz{4}_{5}_2pi_dev"), "q4_xy")
                        align()

                    # multiplexed_readout(I, I_st, Q, Q_st, resonators=multiplexed)
                    multiplexed_readout(I, I_st, Q, Q_st, resonators=multiplexed, weights="rotated_")

                    # State discrimination
                    for i in range(2):
                        assign(state[i], I[i] > eval(f"ge_threshold_q{qubits[i]}"))
                        save(state[i], state_st[i])

                    assign(tot_state_, Cast.to_int(state[0]) + 2 * Cast.to_int(state[1]))
                    with switch_(tot_state_):
                        for i in range(4):
                            with case_(i):
                                assign(counts[i], counts[i] + 1)
                                save(counts[i], counts_st[i])
            # Save the sequence iteration to get the progress bar
            save(s, s_st)

    with stream_processing():
        s_st.save("s")
        for i in range(2):
            g_st[i].save_all(f"g{i + 1}")
            I_st[i].buffer(avgs).map(FUNCTIONS.average()).buffer(len(depths)).save_all(f"I{i + 1}")
            Q_st[i].buffer(avgs).map(FUNCTIONS.average()).buffer(len(depths)).save_all(f"Q{i + 1}")
            state_st[i].buffer(avgs).map(FUNCTIONS.average()).buffer(len(depths)).save_all(f"state{i + 1}")
        for i in range(4):
            string = "state" + bin(i)[2:]
            counts_st[i].buffer(len(depths)).save_all(string)

        if simulate:
            for i in range(2):
                for j in range(4):
                    a_st[i][j].save_all(f"a{i + 1}_{bin(j)[2:]}")

if simulate:
    job = qmm.simulate(config, xeb, SimulationConfig(50000))
    job.result_handles.wait_for_all_values()
    g1, g2 = [job.result_handles.get(f"g{i}").fetch_all()['value'].flatten() for i in [1, 2]]

    a1_00, a1_01, a1_10, a1_11 = [job.result_handles.get(f"a1_{bin(i)[2:]}").fetch_all()['value'].flatten() for i in range(4)]
    a2_00, a2_01, a2_10, a2_11 = [job.result_handles.get(f"a2_{bin(i)[2:]}").fetch_all()['value'].flatten() for i in range(4)]

    gates = list(zip(g1, g2))
    replacement_dict = {0: 'x', 1: 'y', 2: 'w'}
    gates = [(replacement_dict[item[0]], replacement_dict[item[1]]) for item in gates]

    # printing the randomized gates
    if True:
        idx = 0
        for i in range(seqs):
            print(f"\nseq{i + 1}:")
            for j in depths:
                print(f"depth = {j}")
                k = 0
                while k < j:
                    pprint.pprint(gates[idx])
                    if simulate:
                        print(f"g1 = [{a1_00[idx]},{a1_01[idx]},{a1_10[idx]},{a1_11[idx]}]")
                        print(f"g2 = [{a2_00[idx]},{a2_01[idx]},{a2_10[idx]},{a2_11[idx]}]")
                    k += 1;
                    idx += 1

    job.get_simulated_samples().con1.plot()
    plt.show()

else:
    qm = qmm.open_qm(config)
    job = qm.execute(xeb)
    job.result_handles.wait_for_all_values()
    g1, g2 = [job.result_handles.get(f"g{i}").fetch_all()['value'].flatten() for i in [1, 2]]
    I1, I2, Q1, Q2 = [job.result_handles.get(f"{i}{j}").fetch_all()['value'] for i in ["I", "Q"] for j in [1, 2]]

    state1, state2 = [job.result_handles.get(f'state{i}').fetch_all()['value'] for i in [1, 2]]
    state00, state01, state10, state11 = [job.result_handles.get(f'state{bin(i)[2:]}').fetch_all()['value'] for i in range(4)]
    S1 = I1 + 1J * Q1
    S2 = I2 + 1J * Q2

    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()

    save = True
    if save:
        np.savez(save_dir / filename, g1=g1, g2=g2, I1=I1, I2=I2, Q1=Q1, Q2=Q2, seqs=seqs, depth=depth, avgs=avgs,
                 random_gates=random_gates,
                 state1=state1, state2=state2, state00=state00, state01=state01, state10=state10, state11=state11)
        print("Data saved as %s.npz" % filename)

    # Create a pcolor plot
    def create_subplot(data, subplot_number, title):
        plt.subplot(subplot_number)
        plt.pcolor(np.abs(data))
        ax = plt.gca()
        ax.set_title(title)
        ax.set_xlabel('Circuit depth')
        ax.set_ylabel('Sequences')
        ax.set_xticks(np.array(depths))
        ax.set_yticks(np.arange(1, seqs + 1))
        plt.colorbar()

    titles = ["q1 measured", "q2 measured", f'q{qubits[0]}-I', f'q{qubits[1]}-I', 'state00', 'state11', 'state01',
              'state10']
    data = [S1, S2, I1, I2, state00, state11, state01, state10]
    plot_number = [241, 242, 245, 246, 243, 244, 247, 248]
    plt.suptitle(f"XEB for q{qubits[0]}-q{qubits[1]}, inner-average: {avgs}, random-gates: {random_gates}")
    for title, d, n in zip(titles, data, plot_number):
        create_subplot(data, n, title)

    plt.show()

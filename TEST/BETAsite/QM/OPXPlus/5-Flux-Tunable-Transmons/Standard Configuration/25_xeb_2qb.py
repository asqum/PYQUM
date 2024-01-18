"""
Cross entropy benchmarking of two qubits (XEB) is a method for characterizing the fidelity of a two-qubit gate.
The XEB sequence consists of a random sequence of single-qubit gates and a two-qubit gate, followed by a measurement.
The sequence is repeated many times, and the results are used to calculate the cross entropy between the ideal and measured states.
The cross entropy is a measure of the distance between two probability distributions, and is related to the fidelity of the two-qubit gate.
The cross entropy is calculated as follows:
    1. The ideal state is calculated by applying the sequence of single-qubit gates and the two-qubit gate to the initial state |00>.
    2. The measured state is calculated by applying the sequence of single-qubit gates to the initial state |00>, followed by a measurement.
    3. The cross entropy is calculated between the ideal and measured states.
The cross entropy is calculated for a range of sequence depths, and the results are used to calculate the fidelity of the two-qubit gate.
In this script, we provide an example of how to run an XEB sequence on the OPX.

Author: Arthur Strauss - Quantum Machines
Created: 16/01/2024 (Last modified: 16/01/2024)
"""
import numpy as np
from qm import QuantumMachinesManager
from qm.qua import *
from scipy.optimize import curve_fit

from configuration import *
from qm.simulate import SimulationConfig
from matplotlib import pyplot as plt
import pprint
from macros import multiplexed_readout, qua_declaration, cz_gate

qubits = [4, 5]
qubits_el = [f"q{i}_xy" for i in qubits]
multiplexed = [4,5,1,2,3]
cz_type = "const_wf"

# qop_ip = ""
# qop_port = 443
# cluster_name = ""
# octave_config = None
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

# qubits = ["q0", "q1"]  # Fix which qubits to use on the chip (quantum elements in the configuration)
# readout_elements = ["rr0", "rr1"]  # Fix which readout resonators to use on the chip (readout elements in the
# configuration)
# ge_threshold = 0.1  # Threshold for the ground state population (used for the readout)
# thermalization_time = 100  # Thermalization time for the qubits (in ns)
simulate = False

seqs = 10  # Number of random sequences to run per depth
max_depth = 3#7  # Max depth of the XEB sequence
avgs = 10#101  # Number of averages per sequence
depths = np.arange(max_depth)  # Create an array of depths to iterate through

random_gates = 3  # Number of random gates to apply
# Amplitude matrices for the random gates
x90_amp = [1, 0, 0, 1]
y90_amp = [0, 1, -1, 0]
xy90_amp = np.array([1, 1, -1, 1]) * 0.70710678


def assign_amplitude_matrix(gate, a, ref_amps):
    """
    QUA Macro for assigning the amplitude matrix arguments for a given gate index.
    :param gate: Gate index
    :param a: Amplitude matrix arguments
    :param ref_amps: Reference amplitude matrices (given as QUA arrays)
    """
    with switch_(gate):
        for i in range(len(ref_amps)):
            with case_(i):
                for j in range(4):
                    assign(a[j], ref_amps[i][j])


# QUA Program

with program() as xeb:
    # Declare QUA variables
    I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=len(multiplexed))
    # I, Q = [declare(fixed) for _ in range(2)], [declare(fixed) for _ in range(2)]
    s, tot_state_ = declare(int), declare(int)
    d, d_, _d = declare(int), declare(int), declare(int)
    g = [declare(int, size=max_depth) for _ in range(2)]  # Gate indices list for both qubits
    a = [[declare(fixed, size=max_depth) for _ in range(4)] for _ in range(2)]  # Amplitude matrices for both qubits
    ref_amps = [declare(fixed, value=ref_amp) for ref_amp in [x90_amp, y90_amp, xy90_amp]]
    counts = [declare(int, value=0) for _ in range(4)]
    state = [declare(bool) for _ in range(len(multiplexed))]

    # Declare streams
    # I_st, Q_st = [declare_stream() for _ in range(2)], [declare_stream() for _ in range(2)]
    s_st = declare_stream()
    counts_st = [declare_stream() for _ in range(4)]
    state_st = [declare_stream() for _ in range(len(multiplexed))]
    g_st = [declare_stream() for _ in range(len(qubits))]

    # Randomize the random number generator
    r = Random()
    r.set_seed(12321)

    # If we are simulating, we need to update the frequency of the qubits to 0 to visualize the sequence
    if simulate:
        a_st = [[declare_stream() for _ in range(4)] for _ in range(random_gates - 1)]
        for qubit in qubits:
            update_frequency(qubit, 0)

    # Generate and run the XEB sequences
    with for_(s, 0, s < seqs, s + 1):
        with for_each_(d, depths):
            # Randomize the sequence
            for q in range(len(qubits)):
                # Randomize the first gate
                assign(g[q][0], r.rand_int(random_gates))
                # Map the sequence indices into amplitude matrix arguments (each index corresponds to a random gate)
                assign_amplitude_matrix(g[q][0], [a[q][i][0] for i in range(4)], ref_amps)
                save(g[q][0], g_st[q])

            with for_(d_, 1, d_ < d, d_ + 1):
                for q in range(len(qubits)):
                    assign(g[q][d_], r.rand_int(random_gates))
                    with while_(g[q][d_] == g[q][d_ - 1]):  # Make sure the same gate is not applied twice in a row
                        assign(g[q][d_], r.rand_int(random_gates))
                    # Map the sequence indices into amplitude matrix arguments (each index corresponds to a random gate)
                    assign_amplitude_matrix(g[q][d_], [a[q][i][d_] for i in range(4)], ref_amps)
                    save(g[q][d_], g_st[q])

                    if simulate:
                        for amp_matrix_element in range(4):
                            save(a[q][amp_matrix_element][_d], a_st[q][amp_matrix_element])

            # Run the XEB sequence
            with for_(n, 0, n < avgs, n + 1):
                # save(n, n_st)
                # Reset the qubits to their ground states (here simple wait but could be an active reset macro)
                if simulate:
                    wait(25, *qubits_el)
                else:
                    wait(3 * thermalization_time, *qubits_el)

                # Play all cycles generated for sequence s of depth d
                with for_(d_, 0, d_ < d, d_ + 1):
                    for q in range(2):  # Play single qubit gates on both qubits
                        play("x90" * amp(*[a[q][i][_d] for i in range(4)]), qubits_el[q])
                    align()
                    # Insert your two-qubit gate macro here
                    cz_gate(qubits[0], qubits[1], cz_type)
                    frame_rotation_2pi(eval(f"cz{5}_{4}_2pi_dev"), "q5_xy")
                    frame_rotation_2pi(eval(f"cz{4}_{5}_2pi_dev"), "q4_xy")
                    align()

                # Measure the state (insert your readout macro here)
                multiplexed_readout(I, I_st, Q, Q_st, resonators=multiplexed, weights="rotated_")

                # State discrimination
                assign(state[0], I[0] > eval(f"ge_threshold_q{qubits[0]}"))
                assign(state[1], I[1] > eval(f"ge_threshold_q{qubits[1]}"))
                save(state[0], state_st[0])
                save(state[1], state_st[1])

                # State Estimation: returned as an integer, to be later converted to bitstrings
                assign(tot_state_, Cast.to_int(state[0]) + 2 * Cast.to_int(state[1]))
                with switch_(tot_state_):
                    for i in range(2**len(qubits)):  # Bitstring conversion
                        with case_(i):
                            assign(counts[i], counts[i] + 1)  # counts for 00, 01, 10 and 11
                            save(counts[i], counts_st[i])
            # Save the sequence iteration to get the progress bar
            save(s, s_st)

    # Save the results
    with stream_processing():
        s_st.save("s")
        for i in range(2):
            g_st[i].save_all(f"g{i + 1}")
            I_st[i].buffer(avgs).map(FUNCTIONS.average()).buffer(len(depths)).save_all(f"I{i + 1}")
            Q_st[i].buffer(avgs).map(FUNCTIONS.average()).buffer(len(depths)).save_all(f"Q{i + 1}")
            state_st[i].boolean_to_int().buffer(avgs).map(FUNCTIONS.average()).buffer(len(depths)).save_all(f"state{i + 1}")
        for i in range(4):
            string = "state" + bin(i)[2:].zfill(2)
            counts_st[i].buffer(len(depths)).save_all(string)

        if simulate:
            for i in range(2):
                for j in range(4):
                    a_st[i][j].save_all(f"a{i + 1}_{bin(j)[2:]}")

if simulate:
    job = qmm.simulate(config, xeb, SimulationConfig(50000))
    job.result_handles.wait_for_all_values()
    g1, g2 = [job.result_handles.get(f"g{i}").fetch_all()['value'].flatten() for i in [1, 2]]

    a1_00, a1_01, a1_10, a1_11 = [job.result_handles.get(f"a1_{bin(i)[2:]}").fetch_all()['value'].flatten() for i in
                                  range(4)]
    a2_00, a2_01, a2_10, a2_11 = [job.result_handles.get(f"a2_{bin(i)[2:]}").fetch_all()['value'].flatten() for i in
                                  range(4)]

    gates = list(zip(g1, g2))
    replacement_dict = {0: 'x', 1: 'y', 2: 'w'}
    gates = [(replacement_dict[item[0]], replacement_dict[item[1]]) for item in gates]

    print("Randomized gates:")
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
                k += 1
                idx += 1
    job.get_simulated_samples().con1.plot()
    plt.show()

else:
    qm = qmm.open_qm(config)
    job = qm.execute(xeb)
    job.result_handles.wait_for_all_values()
    g1, g2 = [job.result_handles.get(f"g{i}").fetch_all()['value'] for i in [1, 2]]
    I1, I2, Q1, Q2 = [job.result_handles.get(f"{i}{j}").fetch_all()['value'] for i in ["I", "Q"] for j in [1, 2]]

    state1, state2 = [job.result_handles.get(f'state{i}').fetch_all()['value'] for i in [1, 2]]
    state00, state01, state10, state11 = [job.result_handles.get(f'state{bin(i)[2:].zfill(2)}').fetch_all()['value'] for i in
                                          range(4)]
    S1 = I1 + 1J * Q1
    S2 = I2 + 1J * Q2

    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()

    # Process results

    def cross_entropy(p, q, epsilon=1e-15):
        """
        Calculate cross entropy between two probability distributions.

        Parameters:
        - p: numpy array, the true probability distribution
        - q: numpy array, the predicted probability distribution
        - epsilon: small value to avoid taking the logarithm of zero

        Returns:
        - Cross entropy between p and q
        """
        q = np.maximum(q, epsilon)  # Avoid taking the logarithm of zero

        # print(f"p: {p}, \nq: {q}")

        x_entropy = -np.sum(p * np.log(q))

        return x_entropy


    X90 = np.array([[np.cos(np.pi / 4), -1j * np.sin(np.pi / 4)], [-1j * np.sin(np.pi / 4), np.cos(np.pi / 4)]])
    Y90 = np.array([[np.cos(np.pi / 4), -np.sin(np.pi / 4)], [+np.sin(np.pi / 4), np.cos(np.pi / 4)]])
    XY90 = (X90 + Y90) / np.sqrt(3)
    CZ = np.array([[+1, 0, 0, 0], [0, +1, 0, 0], [0, 0, +1, 0], [0, 0, 0, -1]])
    gate_dict = {0: {"name": "x90", "matrix": X90},
                 1: {"name": "y90", "matrix": Y90},
                 2: {"name": "xy90", "matrix": XY90}
                 }

    incoherent_state = 0.25 * np.ones(4)
    fidelities = np.zeros((seqs, len(depths)))

    expected_probs = np.zeros((seqs, len(depths), 2 ** len(qubits)))
    measured_probs = np.zeros((seqs, len(depths), 2 ** len(qubits)))

    idx = 0
    for i in range(seqs):
        for j in range(len(depths)):
            state = np.array([[1., 0., 0., 0.]]).T
            for k in range(j):
                sq_gate1, sq_gate2 = gate_dict[g1[k]], gate_dict[g2[k]]
                # Retrieve random single qubit gates applied on both qubits
                sq_gates = np.kron(sq_gate2["matrix"], sq_gate1["matrix"])

                state = CZ @ sq_gates @ state

                print("computed state: %s" %state)

            expected_probs[i, j] = np.transpose(np.abs(state) ** 2).ravel()
            print("expected prob: %s" %expected_probs[i, j])
            # expected_probs[i, j] = [np.longdouble(x) for x in expected_probs[i, j]]
            measured_probs[i, j] = np.array([state00[i][j], state01[i][j],
                                                       state10[i][j], state11[i][j]]) / avgs
            xe_incoherent = cross_entropy(incoherent_state, expected_probs[i, j])
            xe_measured = cross_entropy(measured_probs[i, j], expected_probs[i, j])
            xe_expected = cross_entropy(expected_probs[i, j], expected_probs[i, j])

            f_xeb = ((xe_incoherent - xe_measured) / (xe_incoherent - xe_expected))
            fidelities[i, j] = f_xeb
            print(f"seq {i + 1}, depth {depths[j]}: f_xeb = {f_xeb}")

    # Plot the results
    def create_subplot(data, subplot_number, title):
        print(title)
        print("data: %s" %data)
        print(subplot_number)
        plt.subplot(subplot_number)
        plt.pcolor(np.abs(data))
        ax = plt.gca()
        ax.set_title(title)
        ax.set_xlabel('Circuit depth')
        ax.set_ylabel('Sequences')
        ax.set_xticks(depths)
        ax.set_yticks(np.arange(1, seqs + 1))
        plt.colorbar()


    titles = ["q1 measured", "q2 measured", f'q{qubits[0]}-I', f'q{qubits[1]}-I']
    titles = []
    titles += [f'<{bin(i)[2:].zfill(2)}> Measured' for i in range(4)]
    titles += [f'<{bin(i)[2:].zfill(2)}> Expected' for i in range(4)]

    # data = [S1, S2, I1, I2]
    data = []
    data += [measured_prob for measured_prob in measured_probs]
    data += [expected_prob for expected_prob in expected_probs]

    plot_number = [241, 242, 245, 246, 243, 244, 247, 248, 249, 250, 251, 252]
    plt.suptitle(f"XEB for q{qubits[0]}-q{qubits[1]}, inner-average: {avgs}, random-gates: {random_gates}")
    for title, d, n in zip(titles, data, plot_number):
        create_subplot(d, n, title)

    plt.subplot(5, 2, 10)
    Fxeb = np.mean(fidelities, axis=0)
    print(Fxeb)


    def exponential_decay(x, a, b, c):
        return a * np.exp(-b * x) + c


    try:
        params, covariance = curve_fit(exponential_decay, depths, Fxeb)
        a_fit, b_fit, c_fit = params
        x = exponential_decay(depths, a_fit, b_fit, c_fit)
        xeb_err_per_cycle = 1 - (x[2] - c_fit) / (x[1] - c_fit)
    except:
        pass

    plt.scatter(depths, Fxeb, label='Original Data')
    # plt.plot(np.arange(depth), exponential_decay(np.arange(depth), a_fit, b_fit, c_fit), label='err_per_cycle={:.2f}'.format(xeb_err_per_cycle), color='red')
    plt.legend()
    ax = plt.gca()
    ax.set_title('XEB')
    ax.set_ylabel('fidelity')
    ax.set_xticks(depths)
    plt.show()

    plt.show()

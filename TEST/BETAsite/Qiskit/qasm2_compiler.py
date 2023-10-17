from qiskit import qasm2, execute

program = """
    OPENQASM 2.0;include "qelib1.inc";qreg q[7];creg c[7];x q[3];
             h q[0];
                         cx q[0], q[1];
    cx q[1], q[2];
                         cx q[2], q[3];
    cx q[3], q[4];
                  cx q[4], q[5];
      cx q[5], q[6];

    measure q -> c;
    """

circuit = qasm2.loads(program)
print(str(circuit.draw()))

from qiskit_aer import AerSimulator

# Construct an ideal simulator
aersim = AerSimulator()

# Perform an ideal simulation
result_ideal = execute(circuit, aersim, shots=13700).result()
counts_ideal = result_ideal.get_counts(0)
print('Counts(ideal):', counts_ideal)

# import matplotlib
# matplotlib.use('TkAgg')
# from qiskit.visualization import plot_histogram
# plt = plot_histogram(counts_ideal)
# plt.show()


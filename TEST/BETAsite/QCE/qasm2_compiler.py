from qiskit import qasm2, qasm3, execute

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

# using qiskit to output openQASM 3:
# from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, qasm3
# qreg_q = QuantumRegister(5, 'q')
# creg_c = ClassicalRegister(5, 'c')
# circuit = QuantumCircuit(qreg_q, creg_c)

# circuit.x(qreg_q[0])
# circuit.swap(qreg_q[0], qreg_q[1])
# circuit.measure(qreg_q, creg_c)

# program = qasm3.dumps(circuit)
# print(program)

# using qBraid to convert openQASM 2 to 3:
# from qbraid.interface.qbraid_qasm3.tools import convert_to_qasm3
# program = convert_to_qasm3(program)
# print(program)

circuit = qasm2.loads(program)
# circuit = qasm3.loads(program)
print(str(circuit.draw()))

from qiskit_aer import AerSimulator

# Construct an ideal simulator
aersim = AerSimulator(method="matrix_product_state") # method: stabilizer, statevector, density_matrix and matrix_product_state

# Perform an ideal simulation
result_ideal = execute(circuit, aersim, shots=13700).result()
counts_ideal = result_ideal.get_counts(0)
print('Counts(ideal):', counts_ideal)

# import matplotlib
# matplotlib.use('TkAgg')
# from qiskit.visualization import plot_histogram
# plt = plot_histogram(counts_ideal)
# plt.show()


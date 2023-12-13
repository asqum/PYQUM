import qiskit
from qiskit import IBMQ, qasm3
from qiskit_aer import AerSimulator

# Generate 3-qubit GHZ state
circ = qiskit.QuantumCircuit(3)
circ.h(0)
circ.cx(0, 1)
circ.cx(1, 2)
circ.measure_all()

print("openQASM 2.0 output:\n ")
print(qasm3.dumps(circ))

# Construct an ideal simulator
aersim = AerSimulator()

# Perform an ideal simulation
result_ideal = qiskit.execute(circ, aersim).result()
counts_ideal = result_ideal.get_counts(0)
print('Counts(ideal):', counts_ideal)
# Counts(ideal): {'000': 493, '111': 531}

try:
    # Construct a noisy simulator backend from an IBMQ backend
    # This simulator backend will be automatically configured
    # using the device configuration and noise model 
    provider = IBMQ.load_account()
    backend = provider.get_backend('ibmq_athens')
    aersim_backend = AerSimulator.from_backend(backend)

    # Perform noisy simulation
    result_noise = qiskit.execute(circ, aersim_backend).result()
    counts_noise = result_noise.get_counts(0)

    print('Counts(noise):', counts_noise)
    # Counts(noise): {'000': 492, '001': 6, '010': 8, '011': 14, '100': 3, '101': 14, '110': 18, '111': 469}

except: print("IBM credentials required.")

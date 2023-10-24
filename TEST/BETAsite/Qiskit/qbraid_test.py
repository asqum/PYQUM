from qbraid import circuit_wrapper
from qbraid.interface import random_circuit
from qbraid.interface.qbraid_qasm3.tools import convert_to_qasm3

from braket.circuits.serialization import IRType

for _ in range(100):
    circuit = random_circuit("braket")
    qasm2_str = circuit_wrapper(circuit).transpile("qasm")
    qasm3_test = convert_to_qasm3(qasm2_str)
    qasm3_expected = circuit.to_ir(IRType.OPENQASM).source
    assert qasm3_test.strip() == qasm3_expected.strip()
    
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color

from qiskit import qasm2, qasm3, execute
from qiskit_aer import AerSimulator

from pyqum.OpenQASM.Circuit import simple_circuit

def running_qc(backend, qasm_script, shots):
    circuit_map = {}

    # circuit preview:
    if "OPENQASM 2" in qasm_script: 
        circuit = qasm2.loads(qasm_script)
        circuit_map['script'] = qasm3.dumps(circuit)
        print("openQASM 3.0:\n" + circuit_map['script'])
        # need to convert to OQ3 for the compiler to orchestrate pulses:
        qasm_script = circuit_map['script']
    elif "OPENQASM 3" in qasm_script: 
        circuit = qasm3.loads(qasm_script)
        circuit_map['script'] = circuit.qasm()
        print("openQASM 2.0:\n" + circuit_map['script'])
    else: print(Fore.RED + "Invalid openQASM!")
    
    
    circuit_map['draw'] = str(circuit.draw())
    print(circuit_map['draw'])

    if backend=="Ideal":
        # Construct an ideal simulator
        aersim = AerSimulator(method="statevector")
        # Perform an ideal simulation
        result_ideal = execute(circuit, aersim, shots=shots).result()
        counts_ideal = result_ideal.get_counts(0)
        print('Counts(ideal):', counts_ideal)
        result = counts_ideal
        message = "Ideal QC execution completed."

    elif backend=="AS_5q_dr2a":
        result = simple_circuit(shots=shots, script=circuit_map['script'])
        message = "Live QC execution completed."

    else: 
        result = {"00001": "hahaha", "11000": "hohoho", "11011": "hehehe"}
        message = "QPU under calibration"

    print(Fore.GREEN + message)
    return result, circuit_map, message



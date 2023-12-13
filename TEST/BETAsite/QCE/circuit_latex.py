from qiskit import QuantumCircuit,QuantumRegister,ClassicalRegister
import matplotlib.pyplot as plt
from numpy import pi

import matplotlib
matplotlib.use('TkAgg')

qreg_q = QuantumRegister(2, 'q')
creg_c = ClassicalRegister(2, 'c')
qc = QuantumCircuit(qreg_q, creg_c)

qc.rx(0.3*pi, 0)
qc.h(0)
qc.cx(0,1)

figure = qc.draw(style="clifford", output='latex', scale=3, initial_state=True)
figure.show()




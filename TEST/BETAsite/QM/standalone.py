from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
import matplotlib.pyplot as plt

config = {
    "version": 1,
    "controllers": {
        "con1": {
            "type": "opx1",
            "analog_outputs": {
                1: {"offset": +0.0},
                2: {"offset": +0.0},
            },
        },
    },
    "elements": {
        "qubit": {
            "singleInput": {"port": ("con1", 1)},
            "intermediate_frequency": 0e6,
            "operations": {
                "cw1": "const_pulse1",
                "cw2": "const_pulse2",
            },
        },
        "resonator": {
            "singleInput": {"port": ("con1", 2)},
            "intermediate_frequency": 10e6,
            "operations": {
                "cw2": "const_pulse2",
            },
        },
    },
    "pulses": {
        "const_pulse1": {
            "operation": "control",
            "length": 1000,  # in ns
            "waveforms": {"single": "const_wf1"},
        },
        "const_pulse2": {
            "operation": "control",
            "length": 2000,  # in ns
            "waveforms": {"single": "const_wf2"},
        },
    },
    "waveforms": {
        "const_wf1": {"type": "constant", "sample": 0.2},
        "const_wf2": {"type": "constant", "sample": 0.4},
    },
}

qop_ip = "192.168.1.82"
port = 80

# connecting to the Quantum Orchestration Platform #
qmm = QuantumMachinesManager(host=qop_ip, port=port)

# QUA program #
with program() as prog:
    play("cw1", "qubit")
    align("qubit", "resonator")
    play("cw2", "resonator")

simulate = True

# Simulation of the QUA program
if simulate == True:
    job = qmm.simulate(config, prog, SimulationConfig(int(1000)))  # in clock cycles, 4 ns
    job.get_simulated_samples().con1.plot()
    plt.show()

# Execution of the QUA program on the real HW
if simulate !=True:
    qm = qmm.open_qm(config)
    job = qm.execute(prog)
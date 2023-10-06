#%%
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pylab as plt
from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qualang_tools.bakery.bakery import Baking
# from qw_qm_admin import get_machine
# from config_module import config  # config generation not in scope of example

# from configuration_2qrb import *
from configuration import *

# from lib.execution import generate_qmm
from two_qubit_rb import TwoQubitRb
# from qualang_tools import 

#%%

q1 = '0'
q2 = '1'
def bake_phased_xz(baker: Baking, q, x, z, a):
    element = f"qubit{q}_xy"

    baker.frame_rotation_2pi(-a, element)
    baker.play("x$drag", element, amp=x)
    baker.frame_rotation_2pi(a + z, element)

qubit1_frame_update = 0.23  # examples, should be taken from QPU parameters
qubit2_frame_update = 0.12  # examples, should be taken from QPU parameters

def bake_cz(baker: Baking, q1, q2):
    q1_xy_element = f"qubit{q1}_xy"
    q2_xy_element = f"qubit{q2}_xy"
    q2_z_element = f"qubit{q2}_z"
    
    baker.play("cz_qubit1_qubit0$rect", q2_z_element)
    baker.align()
    baker.frame_rotation_2pi(qubit1_frame_update, q2_xy_element)
    baker.frame_rotation_2pi(qubit2_frame_update, q1_xy_element)
    baker.align()


def prep():
    wait(10000)  # thermal preparation
    align()


def meas():
    rr0_name = f"qubit0_rr"
    rr1_name = f"qubit1_rr"
    Iq0 = declare(fixed)
    Qq0 = declare(fixed)

    Iq1 = declare(fixed)
    Qq1 = declare(fixed)
    
    measure("readout$rect$rotation", rr0_name, None,
            dual_demod.full("w1", "out1", "w2", "out2", Iq0),
            dual_demod.full("w3", "out1", "w1", "out2", Qq0)
            )
    measure("readout$rect$rotation", rr1_name, None,
            dual_demod.full("w1", "out1", "w2", "out2", Iq1),
            dual_demod.full("w3", "out1", "w1", "out2", Qq1)
            )

    return Iq0 > 0, Iq1 > 0  # example, should be taken from QPU parameters


#%%
rb = TwoQubitRb(config, bake_phased_xz, {"CZ": bake_cz}, prep, meas, verify_generation=True)

# qmm = QuantumMachinesManager('qum.phys.sinica.edu.tw',port=80)
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

res = rb.run(qmm, circuit_depths=[1, 2, 3, 4, 5], num_circuits_per_depth=50, num_shots_per_circuit=10000)

# %%

res.plot_hist()
plt.show()

res.plot_fidelity()
plt.show()


# %%

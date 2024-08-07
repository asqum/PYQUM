import matplotlib.pylab as plt
from qm.qua import *
from qm import QuantumMachinesManager, generate_qua_script
from qualang_tools.bakery.bakery import Baking
from configuration import *
from test_two_qubit_rb.two_qubit_rb import TwoQubitRb

from test_two_qubit_rb.two_qubit_rb.tracker.operation_tracker import OperationTracker
from test_two_qubit_rb.two_qubit_rb.tracker.sequence_tracker import SequenceTracker
ot = OperationTracker()
st = SequenceTracker(ot)
##############################
## General helper functions ##
##############################
def multiplexed_readout(I, I_st, Q, Q_st, resonators, sequential=False, amplitude=1.0, weights=""):
    """Perform multiplexed readout on two resonators"""
    if type(resonators) is not list:
        resonators = [resonators]

    for ind, res in enumerate(resonators):
        measure(
            "readout" * amp(amplitude),
            f"rr{res}",
            None,
            dual_demod.full(weights + "cos", "out1", weights + "sin", "out2", I[ind]),
            dual_demod.full(weights + "minus_sin", "out1", weights + "cos", "out2", Q[ind]),
        )

        if I_st is not None:
            save(I[ind], I_st[ind])
        if Q_st is not None:
            save(Q[ind], Q_st[ind])

        if sequential and ind < len(resonators) - 1:
            align(f"rr{res}", f"rr{res+1}")


##############################
##  Two-qubit RB functions  ##
##############################
# assign a string to a variable to be able to call them in the functions
q1 = "5" # flux tuned
q2 = "4"


# single qubit generic gate constructor Z^{z}Z^{a}X^{x}Z^{-a} that can reach any point on the Bloch sphere (starting from arbitrary points)
def bake_phased_xz(baker: Baking, q, x, z, a):
    ot.register_phase_xz(q=q, x=x, z=z, a=a)
    if q == 1: element = f"q{q1}_xy"
    elif q ==2: element = f"q{q2}_xy"
    else: raise Exception()
    element = f"q{q}_xy"
    baker.frame_rotation_2pi(a/2, element)
    baker.play("x180", element, amp=x)
    baker.frame_rotation_2pi(-(a + z)/2, element)


# single qubit phase corrections in units of 2pi applied after the CZ gate
qubit1_frame_update = -220.618 / 360  # example values, should be taken from QPU parameters
qubit2_frame_update = -327.317 / 360  # example values, should be taken from QPU parameters


# defines the CZ gate that realizes the mapping |00> -> |00>, |01> -> |01>, |10> -> |10>, |11> -> -|11>
def bake_cz(baker: Baking, q1, q2):
    ot.register_cz()
    cz_sqr_amp, cz_sqr_len = cz5_4_amp, cz5_4_len
    wf = np.array([cz_sqr_amp]*(cz_sqr_len+1)) # cz_len+1 is the exactly time of z pulse.
    wf = wf.tolist()
    q1_xy_element = f"q{q1}_xy"  
    q2_xy_element = f"q{q2}_xy"
    q1_z_element = f"q{q1}_z"
    baker.add_op("cz",q1_z_element,wf)
    baker.wait(20,q1_xy_element,q2_xy_element,q1_z_element) # The unit is 1 ns.
    baker.play("cz", q1_z_element)
    baker.align(q1_xy_element,q2_xy_element,q1_z_element)
    baker.wait(20,q1_xy_element,q2_xy_element,q1_z_element)
    baker.frame_rotation_2pi(qubit1_frame_update, q1_xy_element)
    baker.frame_rotation_2pi(qubit2_frame_update, q2_xy_element)
    baker.align(q1_xy_element,q2_xy_element,q1_z_element)


def prep():
    # wait(int(16* u.ns))
    wait(int(10 * 12000 * u.ns))  # thermal preparation in clock cycles (time = 10 x T1 x 4ns)
    align()

def meas():
    threshold1 = ge_threshold_q5 # threshold for state discrimination 0 <-> 1 using the I quadrature
    threshold2 = ge_threshold_q4  # threshold for state discrimination 0 <-> 1 using the I quadrature
    I1 = declare(fixed)
    I2 = declare(fixed)
    Q1 = declare(fixed)
    Q2 = declare(fixed)
    I3 = declare(fixed)
    I4 = declare(fixed)
    Q3 = declare(fixed)
    Q4 = declare(fixed)
    I5 = declare(fixed)
    Q5 = declare(fixed)
    state1 = declare(bool)
    state2 = declare(bool)
    multiplexed_readout(
        [I1, I2, I3, I4, I5], None, [Q1, Q2, Q3, Q4, Q5], None, resonators=[ 4, 5, 1, 2, 3 ], weights="rotated_"
    )  # readout macro for multiplexed readout
    assign(state1, I5 > threshold1)  # assume that all information is in I
    assign(state2, I4 > threshold2)  # assume that all information is in I
    return state1, state2


##############################
##  Two-qubit RB execution  ##
##############################

rb = TwoQubitRb(
    config, bake_phased_xz, {"CZ": bake_cz}, prep, meas, verify_generation=False, interleaving_gate=None, 
    operation_tracker = ot,
    sequence_tracker = st
)  # create RB experiment from configuration and defined functions

qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name)  # initialize qmm
res = rb.run(qmm, circuit_depths=[x for x in range(5)], num_circuits_per_depth=5, num_shots_per_circuit=2000)

st.print_sequences()
# st.verify_sequences()

# ot.print_operations()  
# circuit_depths ~ how many consecutive Clifford gates within one executed circuit https://qiskit.org/documentation/apidoc/circuit.html
# num_circuits_per_depth ~ how many random circuits within one depth
# num_shots_per_circuit ~ repetitions of the same circuit (averaging)


# res.plot_hist()
# plt.show()

res.plot_fidelity()
plt.show()

# import xarray as xr
# ds = xr.Dataset()
# ds['data'] = res.data.state
# ds.to_netcdf("data.nc")

# print(res.data.state.mean("average"))


"""
This file contains useful QUA macros meant to simplify and ease QUA programs.
All the macros below have been written and tested with the basic configuration. If you modify this configuration
(elements, operations, integration weights...) these macros will need to be modified accordingly.
"""

from qm.qua import *
from qualang_tools.addons.variables import assign_variables_to_element
from pyqum.OpenQASM.configuration import *

from numpy import pi

##############
# QUA macros #
##############

# 1.1 Single-Qubit Clifford:
def sx_gate(qubit):
    play("x90", "q%s_xy"%qubit)
def id_gate(qubit):
    wait(1)
def x_gate(qubit):
    play("x180", "q%s_xy"%qubit)
def y_gate(qubit):
    play("y180", "q%s_xy"%qubit)
def z_gate(qubit):
    frame_rotation_2pi(0.5, "q%s_xy"%qubit)
def s_gate(qubit):
    frame_rotation_2pi(0.5**2, "q%s_xy"%qubit)
def t_gate(qubit):
    frame_rotation_2pi(0.5**3, "q%s_xy"%qubit)
def h_gate(qubit):
    play("y90", "q%s_xy"%qubit)
    play("x180", "q%s_xy"%qubit)
# 1.2 Single-Qubit Non-Clifford:
def rx_gate(qubit,theta):
    if theta<=pi/2: play("x90"*amp(theta/(pi/2)), "q%s_xy"%qubit)
    if theta>pi/2 and theta<=pi: play("x180"*amp(theta/pi), "q%s_xy"%qubit)
    if theta>pi: 
        theta -= 2*pi
        play("-x90"*amp(-theta/(pi/2)), "q%s_xy"%qubit)
def ry_gate(qubit,theta):
    if theta<=pi/2: play("y90"*amp(theta/(pi/2)), "q%s_xy"%qubit)
    if theta>pi/2 and theta<=pi: play("y180"*amp(theta/pi), "q%s_xy"%qubit)
    if theta>pi: 
        theta -= 2*pi
        play("-y90"*amp(-theta/(pi/2)), "q%s_xy"%qubit)
def rz_gate(qubit,phi):
    frame_rotation_2pi(phi/2/pi, "q%s_xy"%qubit)
def p_gate(qubit,phi): # P(pi/4)=T
    frame_rotation_2pi(phi/2/pi, "q%s_xy"%qubit)

# 2. Two-Qubit Clifford:
def cz_gate(c, t):
    '''
    target: paired with H
    '''
    if c > 2: 
        control, target = c, t
        cz_corr_target = float(eval(f"cz{target}_{control}_2pi_dev"))
        target_phase_correction = declare(fixed, value=cz_corr_target)
        cz_corr_control = float(eval(f"cz{control}_{target}_2pi_dev"))
        control_phase_correction = declare(fixed, value=cz_corr_control)
    else: 
        control, target = t, c
        cz_corr_target = float(eval(f"cz{control}_{target}_2pi_dev"))
        target_phase_correction = declare(fixed, value=cz_corr_target)
        cz_corr_control = float(eval(f"cz{target}_{control}_2pi_dev"))
        control_phase_correction = declare(fixed, value=cz_corr_control)

    
    align()
    wait(flux_settle_time * u.ns, f"q{target}_z")
    align()
    # align(f"q{control}_xy",f"q{control}_z",f"q{target}_xy",f"q{target}_z")
    play(f"cz_{control}c{target}t", f"q{target}_z")
    frame_rotation_2pi(target_phase_correction, f"q{target}_xy")
    frame_rotation_2pi(control_phase_correction, f"q{control}_xy")
    align()
    # align(f"q{control}_xy",f"q{control}_z",f"q{target}_xy",f"q{target}_z")
    wait(flux_settle_time * u.ns, f"q{target}_z")
    align()

def cx_gate(control, target):
    align()
    h_gate(target)
    align()
    cz_gate(control, target)
    align()
    h_gate(target)
    align()

# 3. Readouts:
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

            
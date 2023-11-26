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

# 1. Single-Qubit Clifford:
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
def rx_gate(qubit,theta):
    play("x180"*(theta/pi), "q%s_xy"%qubit)
def ry_gate(qubit,theta):
    play("y180"*(theta/pi), "q%s_xy"%qubit)
def rz_gate(qubit,phi):
    frame_rotation_2pi(phi/2/pi, "q%s_xy"%qubit)

# 2. Two-Qubit Clifford:
def cz_gate(c, t):
    '''
    target: paired with H
    '''
    if c > 2: control, target = c, t
    else: control, target = t, c

    cz_corr = float(eval(f"cz{target}_{control}_2pi_dev"))
    global_phase_correction = declare(fixed, value=cz_corr)

    wait(flux_settle_time * u.ns, f"q{target}_z")
    align()
    # align(f"q{control}_xy",f"q{control}_z",f"q{target}_xy",f"q{target}_z")
    play(f"cz_{control}c{target}t", f"q{target}_z")
    frame_rotation_2pi(global_phase_correction, f"q{target}_xy")
    align()
    # align(f"q{control}_xy",f"q{control}_z",f"q{target}_xy",f"q{target}_z")
    wait(flux_settle_time * u.ns, f"q{target}_z")

def cx_gate(control, target):
    align()
    h_gate(target)
    align()
    cz_gate(control, target)
    align()
    h_gate(target)
    align()

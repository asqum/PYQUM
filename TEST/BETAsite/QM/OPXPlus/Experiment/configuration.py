import numpy as np
from qualang_tools.config.waveform_tools import drag_gaussian_pulse_waveforms
from qualang_tools.units import unit
from qualang_tools.config.waveform_tools import flattop_gaussian_waveform

#########
# PATHS #
#########

from pathlib import Path
save_dir = (Path().absolute()/"TEST"/"BETAsite"/"QM"/"OPXPlus"/"data")

#######################
# AUXILIARY FUNCTIONS #
#######################

# IQ imbalance matrix
def IQ_imbalance(g, phi):
    """
    Creates the correction matrix for the mixer imbalance caused by the gain and phase imbalances, more information can
    be seen here:
    https://docs.qualang.io/libs/examples/mixer-calibration/#non-ideal-mixer
    :param g: relative gain imbalance between the I & Q ports. (unit-less), set to 0 for no gain imbalance.
    :param phi: relative phase imbalance between the I & Q ports (radians), set to 0 for no phase imbalance.
    """
    c = np.cos(phi)
    s = np.sin(phi)
    N = 1 / ((1 - g**2) * (2 * c**2 - 1))
    return [float(N * x) for x in [(1 - g) * c, (1 + g) * s, (1 - g) * s, (1 + g) * c]]


#############
# VARIABLES #
#############
u = unit()

qop_ip = "qum.phys.sinica.edu.tw"

# Qubits
qubit_LO = 3.95 * u.GHz  # Used only for mixer correction and frequency rescaling for plots or computation
# qubit_IF_q1 = (41) * u.MHz
# qubit_IF_q2 = (+362.3) * u.MHz
qubit_IF_q1 = (3950-3911) * u.MHz # 3911, 3544, 3783
qubit_IF_q2 = (3950-3624.9) * u.MHz # 3624.9, 3705.7, 3667
mixer_qubit_g_q1 = 0.007
mixer_qubit_g_q2 = 0.009
mixer_qubit_phi_q1 = 0.085
mixer_qubit_phi_q2 = 0.035

qubit_T1 = int(3 * u.us)

const_len = 100
const_amp = 270 * u.mV

# generate flattop waveforms

# qubit-1 (uses X to tune up the rest of the Q-gates)
flattop_len_1 = 40 #40, 60, 300
flattop_rise_len_1 = 8
flattop_amp_1 = 0.24 *0.131*4 *1.5 #RB1
# flattop_amp_1 = 0.22 *0.32*0.857 #RB2

tot_ft_len_1 = flattop_len_1 + 2 * flattop_rise_len_1
x = np.array(flattop_gaussian_waveform(flattop_amp_1, flattop_len_1, flattop_rise_len_1))
y = np.array([0] * tot_ft_len_1)
x180_flattop_I_1 = x
x180_flattop_Q_1 = y 
x90_flattop_I_1 = x * 0.5 
x90_flattop_Q_1 = y * 0.5
y180_flattop_I_1 = -y
y180_flattop_Q_1 = x
y90_flattop_I_1 = -y * 0.5
y90_flattop_Q_1 = x * 0.5
mx90_flattop_I_1 = - x * 0.5 
mx90_flattop_Q_1 = - y * 0.5
my90_flattop_I_1 = - y * 0.5
my90_flattop_Q_1 = x * 0.5

# qubit-2
flattop_len = 40 #40, 60, 300
flattop_rise_len = 8
flattop_amp = 0.24 *1.2 *1.5 #RB1
# flattop_amp = 0.22 *1.14 #RB2
 
tot_ft_len = flattop_len + 2 * flattop_rise_len
x = np.array(flattop_gaussian_waveform(flattop_amp, flattop_len, flattop_rise_len))
y = np.array([0] * tot_ft_len)
x180_flattop_I = x
x180_flattop_Q = y 
x90_flattop_I = x * 0.5 
x90_flattop_Q = y * 0.5
y180_flattop_I = -y
y180_flattop_Q = x
y90_flattop_I = -y * 0.5
y90_flattop_Q = x * 0.5
mx90_flattop_I = - x * 0.5 
mx90_flattop_Q = - y * 0.5
my90_flattop_I = - y * 0.5
my90_flattop_Q = x * 0.5

pi_len = 800
pi_sigma = 230
pi_amp_q1 = 0.22
pi_amp_q2 = 0.22
drag_coef_q1 = 0
drag_coef_q2 = 0
anharmonicity_q1 = -200 * u.MHz
anharmonicity_q2 = -180 * u.MHz
AC_stark_detuning_q1 = 0 * u.MHz
AC_stark_detuning_q2 = 0 * u.MHz

x180_wf_q1, x180_der_wf_q1 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q1, pi_len, pi_sigma, drag_coef_q1, anharmonicity_q1, AC_stark_detuning_q1))
x180_I_wf_q1 = x180_wf_q1
x180_Q_wf_q1 = x180_der_wf_q1
x180_wf_q2, x180_der_wf_q2 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q2, pi_len, pi_sigma, drag_coef_q2, anharmonicity_q2, AC_stark_detuning_q2))
x180_I_wf_q2 = x180_wf_q2
x180_Q_wf_q2 = x180_der_wf_q2
# No DRAG when alpha=0, it's just a gaussian.

x90_wf_q1, x90_der_wf_q1 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q1/2, pi_len, pi_sigma, drag_coef_q1, anharmonicity_q1, AC_stark_detuning_q1))
x90_I_wf_q1 = x90_wf_q1
x90_Q_wf_q1 = x90_der_wf_q1
x90_wf_q2, x90_der_wf_q2 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q2/2, pi_len, pi_sigma, drag_coef_q2, anharmonicity_q2, AC_stark_detuning_q2))
x90_I_wf_q2 = x90_wf_q2
x90_Q_wf_q2 = x90_der_wf_q2
# No DRAG when alpha=0, it's just a gaussian.

minus_x90_wf_q1, minus_x90_der_wf_q1 = np.array(drag_gaussian_pulse_waveforms(-pi_amp_q1/2, pi_len, pi_sigma, drag_coef_q1, anharmonicity_q1, AC_stark_detuning_q1))
minus_x90_I_wf_q1 = minus_x90_wf_q1
minus_x90_Q_wf_q1 = minus_x90_der_wf_q1
minus_x90_wf_q2, minus_x90_der_wf_q2 = np.array(drag_gaussian_pulse_waveforms(-pi_amp_q2/2, pi_len, pi_sigma, drag_coef_q2, anharmonicity_q2, AC_stark_detuning_q2))
minus_x90_I_wf_q2 = minus_x90_wf_q2
minus_x90_Q_wf_q2 = minus_x90_der_wf_q2
# No DRAG when alpha=0, it's just a gaussian.

y180_wf_q1, y180_der_wf_q1 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q1, pi_len, pi_sigma, drag_coef_q1, anharmonicity_q1, AC_stark_detuning_q1))
y180_I_wf_q1 = (-1) * y180_der_wf_q1
y180_Q_wf_q1 = y180_wf_q1
y180_wf_q2, y180_der_wf_q2 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q2, pi_len, pi_sigma, drag_coef_q2, anharmonicity_q2, AC_stark_detuning_q2))
y180_I_wf_q2 = (-1) * y180_der_wf_q2
y180_Q_wf_q2 = y180_wf_q2
# No DRAG when alpha=0, it's just a gaussian.

y90_wf_q1, y90_der_wf_q1 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q1/2, pi_len, pi_sigma, drag_coef_q1, anharmonicity_q1, AC_stark_detuning_q1))
y90_I_wf_q1 = (-1) * y90_der_wf_q1
y90_Q_wf_q1 = y90_wf_q1
y90_wf_q2, y90_der_wf_q2 = np.array(drag_gaussian_pulse_waveforms(pi_amp_q2/2, pi_len, pi_sigma, drag_coef_q2, anharmonicity_q2, AC_stark_detuning_q2))
y90_I_wf_q2 = (-1) * y90_der_wf_q2
y90_Q_wf_q2 = y90_wf_q2
# No DRAG when alpha=0, it's just a gaussian.

minus_y90_wf_q1, minus_y90_der_wf_q1 = np.array(drag_gaussian_pulse_waveforms(-pi_amp_q1/2, pi_len, pi_sigma, drag_coef_q1, anharmonicity_q1, AC_stark_detuning_q1))
minus_y90_I_wf_q1 = (-1) * minus_y90_der_wf_q1
minus_y90_Q_wf_q1 = minus_y90_wf_q1
minus_y90_wf_q2, minus_y90_der_wf_q2 = np.array(drag_gaussian_pulse_waveforms(-pi_amp_q2/2, pi_len, pi_sigma, drag_coef_q2, anharmonicity_q2, AC_stark_detuning_q2))
minus_y90_I_wf_q2 = (-1) * minus_y90_der_wf_q2
minus_y90_Q_wf_q2 = minus_y90_wf_q2
# No DRAG when alpha=0, it's just a gaussian.

# Resonators
resonator_LO = 6.35 * u.GHz  # Used only for mixer correction and frequency rescaling for plots or computation

# RB1:
resonator_IF_q1 = int((6398.95 - 6350) * u.MHz)
resonator_IF_q2 = int((6350 - 6481.953) * u.MHz) 
# RB2:
# resonator_IF_q1 = int((6398.933 - 6350) * u.MHz)
# resonator_IF_q2 = int((6350 - 6482.139) * u.MHz)

resonator_IF_qc = -220 * u.MHz
mixer_resonator_g_q1 = -0.014
mixer_resonator_g_q2 = 0.029
mixer_resonator_g_qc = 0.020
mixer_resonator_phi_q1 = -0.017
mixer_resonator_phi_q2 = -0.018
mixer_resonator_phi_qc = -0.0010

readout_len = 4000 # 20000 for 4-7
readout_amp_q1 = 0.07 *0.892
readout_amp_q2 = 0.07 *0.822
readout_amp_qc = 0.0525

time_of_flight = 260 # should be a multiple of 4

# Flux line
const_flux_len = 200
const_flux_amp = 0.45

# state discrimination
rotation_angle_q1 = (0.0 / 180) * np.pi
rotation_angle_q2 = (-139 / 180) * np.pi
ge_threshold_q1 = 0.0
ge_threshold_q2 = 0.0

config = {
    "version": 1,
    "controllers": {
        "con1": {
            "analog_outputs": {
                2: {"offset": -0.0147},  # Q readout line
                1: {"offset": +0.0029},  # I readout line
                3: {"offset": -0.0247},  # I qubit1
                4: {"offset": -0.0885},  # Q qubit1
                5: {"offset": -0.0446},  # I qubit2
                6: {"offset": -0.110},  # Q qubit2
                # 7: {"offset": 0.168},  # Z qubit1 => offset at q1 max frequency
                # 8: {"offset": -0.48},  # Z qubit2 => offset at q2 max frequency
                7: {"offset": 0},  # Z qubit1 => offset at 3 chosen idle-points => 0.137, -0.35, -0.15
                8: {"offset": 0.49},  # Z qubit2 => offset near q2 max frequency  => -0.499
                9: {"offset": -0.12},  # Z coupler => offset at q1<=>q2 coupling off=> 0.097 (will heat-up mK when > 0.1V)
            },
            "digital_outputs": {
                1: {},
            },
            "analog_inputs": {
                1: {"offset": +0.0164, "gain_db": 6},  # I from down-conversion
                2: {"offset": +0.0117, "gain_db": 6},  # Q from down-conversion
            },
        },
    },
    "elements": {
        "rr1": {
            "mixInputs": {
                "I": ("con1", 2),
                "Q": ("con1", 1),
                "lo_frequency": resonator_LO,
                "mixer": "mixer_resonator",
            },
            "intermediate_frequency": resonator_IF_q1, # frequency at offset ch7
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q1",
            },
            "outputs": {
                "out1": ("con1", 1),
                "out2": ("con1", 2),
            },
            "time_of_flight": time_of_flight,
            "smearing": 0,
        },
        "rr2": {
            "mixInputs": {
                "I": ("con1", 1),
                "Q": ("con1", 2),
                "lo_frequency": resonator_LO,
                "mixer": "mixer_resonator",
            },
            "intermediate_frequency": resonator_IF_q2, # frequency at offset ch8
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q2",
            },
            "outputs": {
                "out1": ("con1", 1),
                "out2": ("con1", 2),
            },
            "time_of_flight": time_of_flight,
            "smearing": 0,
        },
        "rrc": {
            "mixInputs": {
                "I": ("con1", 1),
                "Q": ("con1", 2),
                "lo_frequency": resonator_LO,
                "mixer": "mixer_resonator",
            },
            "intermediate_frequency": resonator_IF_qc, # frequency at offset ch8
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_qc",
            },
            "outputs": {
                "out1": ("con1", 1),
                "out2": ("con1", 2),
            },
            "time_of_flight": time_of_flight,
            "smearing": 0,
        },
        "q1_xy": {
            "mixInputs": {
                "I": ("con1", 3),
                "Q": ("con1", 4),
                "lo_frequency": qubit_LO,
                "mixer": "mixer_qubit_q1",
            },
            "intermediate_frequency": qubit_IF_q1, # frequency at offset ch7 (max freq)
            "operations": {
                "cw": "const_pulse",
                "flattop": "flattop_pulse_q1",
                "x180": "x180_pulse_q1",
                "x90": "x90_pulse_q1",
                "-x90": "-x90_pulse_q1",
                "y90": "y90_pulse_q1",
                "y180": "y180_pulse_q1",
                "-y90": "-y90_pulse_q1",
                "x180_ft": "x_180_ft_pulse_q1",
                "x90_ft": "x_90_ft_pulse_q1",
                "y180_ft": "y_180_ft_pulse_q1",
                "y90_ft": "y_90_ft_pulse_q1",
                "-x90_ft": "mx_90_ft_pulse_q1",
                "-y90_ft": "my_90_ft_pulse_q1",
            },
        },
        "q2_xy": {
            "mixInputs": {
                "I": ("con1", 5),
                "Q": ("con1", 6),
                "lo_frequency": qubit_LO,
                "mixer": "mixer_qubit_q2",
            },
            "intermediate_frequency": qubit_IF_q2, # frequency at offset ch8 (max freq)
            "operations": {
                "cw": "const_pulse",
                "flattop": "flattop_pulse_q2",
                "x180": "x180_pulse_q2",
                "x90": "x90_pulse_q2",
                "-x90": "-x90_pulse_q2",
                "y90": "y90_pulse_q2",
                "y180": "y180_pulse_q2",
                "-y90": "-y90_pulse_q2",
                "x180_ft": "x_180_ft_pulse_q2",
                "x90_ft": "x_90_ft_pulse_q2",
                "y180_ft": "y_180_ft_pulse_q2",
                "y90_ft": "y_90_ft_pulse_q2",
                "-x90_ft": "mx_90_ft_pulse_q2",
                "-y90_ft": "my_90_ft_pulse_q2",
            },
        },
        "q1_z": {
            "singleInput": {
                "port": ("con1", 7),
            },
            "operations": {
                "const": "const_flux_pulse",
            },
        },
        "q2_z": {
            "singleInput": {
                "port": ("con1", 8),
            },
            "operations": {
                "const": "const_flux_pulse",
            },
        },
        "qc_z": {
            "singleInput": {
                "port": ("con1", 9),
            },
            "operations": {
                "const": "const_flux_pulse",
            },
        },
    },
    "pulses": {
        "const_flux_pulse": {
            "operation": "control",
            "length": const_flux_len,
            "waveforms": {
                "single": "const_flux_wf",
            },
        },
        "x_180_ft_pulse_q2": {
            "operation": "control",
            "length": tot_ft_len,
            "waveforms": {
                "I": "x180_ft_I_wf_q2",
                "Q": "x180_ft_Q_wf_q2",
            },
        },
        "x_90_ft_pulse_q2": {
            "operation": "control",
            "length": tot_ft_len,
            "waveforms": {
                "I": "x90_ft_I_wf_q2",
                "Q": "x90_ft_Q_wf_q2",
            },
        },
        "y_180_ft_pulse_q2": {
            "operation": "control",
            "length": tot_ft_len,
            "waveforms": {
                "I": "y180_ft_I_wf_q2",
                "Q": "y180_ft_Q_wf_q2",
            },
        },
        "y_90_ft_pulse_q2": {
            "operation": "control",
            "length": tot_ft_len,
            "waveforms": {
                "I": "y90_ft_I_wf_q2",
                "Q": "y90_ft_Q_wf_q2",
            },
        },
        "mx_90_ft_pulse_q2": {
            "operation": "control",
            "length": tot_ft_len,
            "waveforms": {
                "I": "mx90_ft_I_wf_q2",
                "Q": "mx90_ft_Q_wf_q2",
            },
        },
        "my_90_ft_pulse_q2": {
            "operation": "control",
            "length": tot_ft_len,
            "waveforms": {
                "I": "my90_ft_I_wf_q2",
                "Q": "my90_ft_Q_wf_q2",
            },
        },
        "x_180_ft_pulse_q1": {
            "operation": "control",
            "length": tot_ft_len_1,
            "waveforms": {
                "I": "x180_ft_I_wf_q1",
                "Q": "x180_ft_Q_wf_q1",
            },
        },
        "x_90_ft_pulse_q1": {
            "operation": "control",
            "length": tot_ft_len_1,
            "waveforms": {
                "I": "x90_ft_I_wf_q1",
                "Q": "x90_ft_Q_wf_q1",
            },
        },
        "y_180_ft_pulse_q1": {
            "operation": "control",
            "length": tot_ft_len_1,
            "waveforms": {
                "I": "y180_ft_I_wf_q1",
                "Q": "y180_ft_Q_wf_q1",
            },
        },
        "y_90_ft_pulse_q1": {
            "operation": "control",
            "length": tot_ft_len_1,
            "waveforms": {
                "I": "y90_ft_I_wf_q1",
                "Q": "y90_ft_Q_wf_q1",
            },
        },
        "mx_90_ft_pulse_q1": {
            "operation": "control",
            "length": tot_ft_len_1,
            "waveforms": {
                "I": "mx90_ft_I_wf_q1",
                "Q": "mx90_ft_Q_wf_q1",
            },
        },
        "my_90_ft_pulse_q1": {
            "operation": "control",
            "length": tot_ft_len_1,
            "waveforms": {
                "I": "my90_ft_I_wf_q1",
                "Q": "my90_ft_Q_wf_q1",
            },
        },
        "flattop_pulse_q1": {
            "operation": "control",
            "length": tot_ft_len_1,
            "waveforms": {
                "I": "flattop_wf_1",
                "Q": "zero_wf",
            },
        },
        "flattop_pulse_q2": {
            "operation": "control",
            "length": len(flattop_gaussian_waveform(flattop_amp, flattop_len, flattop_rise_len)),
            "waveforms": {
                "I": "flattop_wf",
                "Q": "zero_wf",
            },
        },
        "const_pulse": {
            "operation": "control",
            "length": const_len,
            "waveforms": {
                "I": "const_wf",
                "Q": "zero_wf",
            },
        },
        "x90_pulse_q1": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "x90_wf_q1",
                "Q": "x90_der_wf_q1",
            },
        },
        "x180_pulse_q1": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "x180_wf_q1",
                "Q": "x180_der_wf_q1",
            },
        },
        "-x90_pulse_q1": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "minus_x90_wf_q1",
                "Q": "minus_x90_der_wf_q1",
            },
        },
        "y90_pulse_q1": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "y90_der_wf_q1",
                "Q": "y90_wf_q1",
            },
        },
        "y180_pulse_q1": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "y180_der_wf_q1",
                "Q": "y180_wf_q1",
            },
        },
        "-y90_pulse_q1": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "minus_y90_der_wf_q1",
                "Q": "minus_y90_wf_q1",
            },
        },
        "readout_pulse_q1": {
            "operation": "measurement",
            "length": readout_len,
            "waveforms": {
                "I": "readout_wf_q1",
                "Q": "zero_wf",
            },
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q1",
                "rotated_sin": "rotated_sine_weights_q1",
                "rotated_minus_sin": "rotated_minus_sine_weights_q1",
            },
            "digital_marker": "ON",
        },
        "x90_pulse_q2": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "x90_wf_q2",
                "Q": "x90_der_wf_q2",
            },
        },
        "x180_pulse_q2": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "x180_wf_q2",
                "Q": "x180_der_wf_q2",
            },
        },
        "-x90_pulse_q2": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "minus_x90_wf_q2",
                "Q": "minus_x90_der_wf_q2",
            },
        },
        "y90_pulse_q2": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "y90_der_wf_q2",
                "Q": "y90_wf_q2",
            },
        },
        "y180_pulse_q2": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "y180_der_wf_q2",
                "Q": "y180_wf_q2",
            },
        },
        "-y90_pulse_q2": {
            "operation": "control",
            "length": pi_len,
            "waveforms": {
                "I": "minus_y90_der_wf_q2",
                "Q": "minus_y90_wf_q2",
            },
        },
        "readout_pulse_q2": {
            "operation": "measurement",
            "length": readout_len,
            "waveforms": {
                "I": "readout_wf_q2",
                "Q": "zero_wf",
            },
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q2",
                "rotated_sin": "rotated_sine_weights_q2",
                "rotated_minus_sin": "rotated_minus_sine_weights_q2",
            },
            "digital_marker": "ON",
        },
        "readout_pulse_qc": {
            "operation": "measurement",
            "length": readout_len,
            "waveforms": {
                "I": "readout_wf_qc",
                "Q": "zero_wf",
            },
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
            },
            "digital_marker": "ON",
        },
     },
    "waveforms": {
    
        "x180_ft_I_wf_q1": {"type": "arbitrary", "samples": x180_flattop_I_1.tolist()},
        "x180_ft_Q_wf_q1": {"type": "arbitrary", "samples": x180_flattop_Q_1.tolist()},
        "x90_ft_I_wf_q1": {"type": "arbitrary", "samples": x90_flattop_I_1.tolist()},
        "x90_ft_Q_wf_q1": {"type": "arbitrary", "samples": x90_flattop_Q_1.tolist()},
        "y180_ft_I_wf_q1": {"type": "arbitrary", "samples": y180_flattop_I_1.tolist()},
        "y180_ft_Q_wf_q1": {"type": "arbitrary", "samples": y180_flattop_Q_1.tolist()},
        "y90_ft_I_wf_q1": {"type": "arbitrary", "samples": y90_flattop_I_1.tolist()},
        "y90_ft_Q_wf_q1": {"type": "arbitrary", "samples": y90_flattop_Q_1.tolist()},
        "mx90_ft_I_wf_q1": {"type": "arbitrary", "samples": mx90_flattop_I_1.tolist()},
        "mx90_ft_Q_wf_q1": {"type": "arbitrary", "samples": mx90_flattop_Q_1.tolist()},
        "my90_ft_I_wf_q1": {"type": "arbitrary", "samples": my90_flattop_I_1.tolist()},
        "my90_ft_Q_wf_q1": {"type": "arbitrary", "samples": my90_flattop_Q_1.tolist()},

        "x180_ft_I_wf_q2": {"type": "arbitrary", "samples": x180_flattop_I.tolist()},
        "x180_ft_Q_wf_q2": {"type": "arbitrary", "samples": x180_flattop_Q.tolist()},
        "x90_ft_I_wf_q2": {"type": "arbitrary", "samples": x90_flattop_I.tolist()},
        "x90_ft_Q_wf_q2": {"type": "arbitrary", "samples": x90_flattop_Q.tolist()},
        "y180_ft_I_wf_q2": {"type": "arbitrary", "samples": y180_flattop_I.tolist()},
        "y180_ft_Q_wf_q2": {"type": "arbitrary", "samples": y180_flattop_Q.tolist()},
        "y90_ft_I_wf_q2": {"type": "arbitrary", "samples": y90_flattop_I.tolist()},
        "y90_ft_Q_wf_q2": {"type": "arbitrary", "samples": y90_flattop_Q.tolist()},
        "mx90_ft_I_wf_q2": {"type": "arbitrary", "samples": mx90_flattop_I.tolist()},
        "mx90_ft_Q_wf_q2": {"type": "arbitrary", "samples": mx90_flattop_Q.tolist()},
        "my90_ft_I_wf_q2": {"type": "arbitrary", "samples": my90_flattop_I.tolist()},
        "my90_ft_Q_wf_q2": {"type": "arbitrary", "samples": my90_flattop_Q.tolist()},
        
        "flattop_wf_1": {"type": "arbitrary", "samples": flattop_gaussian_waveform(flattop_amp_1, flattop_len_1, flattop_rise_len_1)},
        "flattop_wf": {"type": "arbitrary", "samples": flattop_gaussian_waveform(flattop_amp, flattop_len, flattop_rise_len)},
        "const_wf": {"type": "constant", "sample": const_amp},
        "const_flux_wf": {"type": "constant", "sample": const_flux_amp},
        "zero_wf": {"type": "constant", "sample": 0.0},
        "x90_wf_q1": {"type": "arbitrary", "samples": x90_wf_q1.tolist()},
        "x90_der_wf_q1": {"type": "arbitrary", "samples": x90_der_wf_q1.tolist()},
        "x180_wf_q1": {"type": "arbitrary", "samples": x180_wf_q1.tolist()},
        "x180_der_wf_q1": {"type": "arbitrary", "samples": x180_der_wf_q1.tolist()},
        "minus_x90_wf_q1": {"type": "arbitrary", "samples": minus_x90_wf_q1.tolist()},
        "minus_x90_der_wf_q1": {"type": "arbitrary", "samples": minus_x90_der_wf_q1.tolist()},
        "y90_wf_q1": {"type": "arbitrary", "samples": y90_wf_q1.tolist()},
        "y90_der_wf_q1": {"type": "arbitrary", "samples": y90_der_wf_q1.tolist()},
        "y180_wf_q1": {"type": "arbitrary", "samples": y180_wf_q1.tolist()},
        "y180_der_wf_q1": {"type": "arbitrary", "samples": y180_der_wf_q1.tolist()},
        "minus_y90_wf_q1": {"type": "arbitrary", "samples": minus_y90_wf_q1.tolist()},
        "minus_y90_der_wf_q1": {"type": "arbitrary", "samples": minus_y90_der_wf_q1.tolist()},
        "readout_wf_q1": {"type": "constant", "sample": readout_amp_q1},
        "x90_wf_q2": {"type": "arbitrary", "samples": x90_wf_q2.tolist()},
        "x90_der_wf_q2": {"type": "arbitrary", "samples": x90_der_wf_q2.tolist()},
        "x180_wf_q2": {"type": "arbitrary", "samples": x180_wf_q2.tolist()},
        "x180_der_wf_q2": {"type": "arbitrary", "samples": x180_der_wf_q2.tolist()},
        "minus_x90_wf_q2": {"type": "arbitrary", "samples": minus_x90_wf_q2.tolist()},
        "minus_x90_der_wf_q2": {"type": "arbitrary", "samples": minus_x90_der_wf_q2.tolist()},
        "y90_wf_q2": {"type": "arbitrary", "samples": y90_wf_q2.tolist()},
        "y90_der_wf_q2": {"type": "arbitrary", "samples": y90_der_wf_q2.tolist()},
        "y180_wf_q2": {"type": "arbitrary", "samples": y180_wf_q2.tolist()},
        "y180_der_wf_q2": {"type": "arbitrary", "samples": y180_der_wf_q2.tolist()},
        "minus_y90_wf_q2": {"type": "arbitrary", "samples": minus_y90_wf_q2.tolist()},
        "minus_y90_der_wf_q2": {"type": "arbitrary", "samples": minus_y90_der_wf_q2.tolist()},
        "readout_wf_q2": {"type": "constant", "sample": readout_amp_q2},
        "readout_wf_qc": {"type": "constant", "sample": readout_amp_qc},
    },
    "digital_waveforms": {
        "ON": {"samples": [(1, 0)]},
    },
    "integration_weights": {
        "cosine_weights": {
            "cosine": [(1.0, readout_len)],
            "sine": [(0.0, readout_len)],
        },
        "sine_weights": {
            "cosine": [(0.0, readout_len)],
            "sine": [(1.0, readout_len)],
        },
        "minus_sine_weights": {
            "cosine": [(0.0, readout_len)],
            "sine": [(-1.0, readout_len)],
        },
        "rotated_cosine_weights_q1": {
            "cosine": [(np.cos(rotation_angle_q1), readout_len)],
            "sine": [(-np.sin(rotation_angle_q1), readout_len)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(np.sin(rotation_angle_q1), readout_len)],
            "sine": [(np.cos(rotation_angle_q1), readout_len)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(-np.sin(rotation_angle_q1), readout_len)],
            "sine": [(-np.cos(rotation_angle_q1), readout_len)],
        },
        "rotated_cosine_weights_q2": {
            "cosine": [(np.cos(rotation_angle_q2), readout_len)],
            "sine": [(-np.sin(rotation_angle_q2), readout_len)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(np.sin(rotation_angle_q2), readout_len)],
            "sine": [(np.cos(rotation_angle_q2), readout_len)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(-np.sin(rotation_angle_q2), readout_len)],
            "sine": [(-np.cos(rotation_angle_q2), readout_len)],
        },
    },
    "mixers": {
        "mixer_qubit_q1": [
            {
                "intermediate_frequency": qubit_IF_q1,
                "lo_frequency": qubit_LO,
                "correction": IQ_imbalance(mixer_qubit_g_q1, mixer_qubit_phi_q1),
            }
        ],
        "mixer_qubit_q2": [
            {
                "intermediate_frequency": qubit_IF_q2,
                "lo_frequency": qubit_LO,
                "correction": IQ_imbalance(mixer_qubit_g_q2, mixer_qubit_phi_q2),
            }
        ],
        "mixer_resonator": [
            {
                "intermediate_frequency": resonator_IF_q1,
                "lo_frequency": resonator_LO,
                "correction": IQ_imbalance(mixer_resonator_g_q1, mixer_resonator_phi_q1),
            },
            {
                "intermediate_frequency": resonator_IF_q2,
                "lo_frequency": resonator_LO,
                "correction": IQ_imbalance(mixer_resonator_g_q2, mixer_resonator_phi_q2),
            },
            {
                "intermediate_frequency": resonator_IF_qc,
                "lo_frequency": resonator_LO,
                "correction": IQ_imbalance(mixer_resonator_g_qc, mixer_resonator_phi_qc),
            },
        ],
    },
}
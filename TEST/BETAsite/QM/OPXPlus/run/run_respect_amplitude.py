
# Single QUA script generated at 2024-05-22 11:00:46.950717
# QUA library version: 1.1.3

from qm.qua import *

with program() as prog:
    v1 = declare(int, )
    v2 = declare(fixed, )
    v3 = declare(fixed, )
    v4 = declare(fixed, )
    v5 = declare(fixed, )
    v6 = declare(fixed, )
    v7 = declare(fixed, )
    v8 = declare(fixed, )
    v9 = declare(fixed, )
    v10 = declare(fixed, )
    v11 = declare(fixed, )
    v12 = declare(int, )
    v13 = declare(fixed, )
    wait((4+(0*(Cast.to_int(v2)+Cast.to_int(v7)))), "rr1")
    wait((4+(0*(Cast.to_int(v3)+Cast.to_int(v8)))), "rr2")
    wait((4+(0*(Cast.to_int(v4)+Cast.to_int(v9)))), "rr3")
    wait((4+(0*(Cast.to_int(v5)+Cast.to_int(v10)))), "rr4")
    wait((4+(0*(Cast.to_int(v6)+Cast.to_int(v11)))), "rr5")
    with for_(v1,0,(v1<13700),(v1+1)):
        with for_(v12,-4000000,(v12<=3800000),(v12+200000)):
            update_frequency("rr1", (v12+34300000), "Hz", False)
            update_frequency("rr2", (v12+134400000), "Hz", False)
            update_frequency("rr3", (v12+-22200000), "Hz", False)
            update_frequency("rr4", (v12+158000000), "Hz", False)
            update_frequency("rr5", (v12+63300000), "Hz", False)
            with for_(v13,0.0,(v13<1.9849999999999999),(v13+0.01)):
                measure("readout"*amp(v13), "rr1", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", v2), dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", v7))
                r2 = declare_stream()
                save(v2, r2)
                r7 = declare_stream()
                save(v7, r7)
                measure("readout"*amp(v13), "rr2", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", v3), dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", v8))
                r3 = declare_stream()
                save(v3, r3)
                r8 = declare_stream()
                save(v8, r8)
                measure("readout"*amp(v13), "rr3", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", v4), dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", v9))
                r4 = declare_stream()
                save(v4, r4)
                r9 = declare_stream()
                save(v9, r9)
                measure("readout"*amp(v13), "rr4", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", v5), dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", v10))
                r5 = declare_stream()
                save(v5, r5)
                r10 = declare_stream()
                save(v10, r10)
                measure("readout"*amp(v13), "rr5", None, dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", v6), dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", v11))
                r6 = declare_stream()
                save(v6, r6)
                r11 = declare_stream()
                save(v11, r11)
                wait(9250, )
        r1 = declare_stream()
        save(v1, r1)
    with stream_processing():
        r1.save("n")
        r2.buffer(199).buffer(40).average().save("I1")
        r7.buffer(199).buffer(40).average().save("Q1")
        r3.buffer(199).buffer(40).average().save("I2")
        r8.buffer(199).buffer(40).average().save("Q2")
        r4.buffer(199).buffer(40).average().save("I3")
        r9.buffer(199).buffer(40).average().save("Q3")
        r5.buffer(199).buffer(40).average().save("I4")
        r10.buffer(199).buffer(40).average().save("Q4")
        r6.buffer(199).buffer(40).average().save("I5")
        r11.buffer(199).buffer(40).average().save("Q5")


config = {
    "version": 1,
    "controllers": {
        "con1": {
            "analog_outputs": {
                "1": {
                    "offset": 0.01953125,
                },
                "2": {
                    "offset": -0.00244140625,
                },
                "3": {
                    "offset": -0.00183868408203125,
                },
                "4": {
                    "offset": 0.01373291015625,
                },
                "5": {
                    "offset": -0.014556884765625,
                },
                "6": {
                    "offset": 0.01129150390625,
                },
                "7": {
                    "offset": 0.0161895751953125,
                },
                "8": {
                    "offset": -0.0023956298828125,
                },
                "9": {
                    "offset": 0.0078125,
                },
                "10": {
                    "offset": -0.0123291015625,
                },
            },
            "digital_outputs": {
                "1": {},
                "3": {},
                "5": {},
                "7": {},
                "10": {},
            },
            "analog_inputs": {
                "1": {
                    "offset": 0.006487780227661133,
                    "gain_db": 0,
                },
                "2": {
                    "offset": 0.004683707580566406,
                    "gain_db": 0,
                },
            },
        },
        "con2": {
            "analog_outputs": {
                "1": {
                    "offset": -0.03914642333984375,
                },
                "2": {
                    "offset": -0.0126953125,
                },
                "3": {
                    "offset": 0.0,
                },
                "4": {
                    "offset": 0.0,
                },
                "5": {
                    "offset": 0.0,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "6": {
                    "offset": 0.0,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "7": {
                    "offset": 0.0,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "8": {
                    "offset": 0.0,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "9": {
                    "offset": 0.0,
                    "filter": {
                        "feedforward": [1.06569937, -0.98851684],
                        "feedback": [0.92281746],
                    },
                },
                "10": {
                    "offset": 0.0,
                },
            },
            "digital_outputs": {
                "1": {},
                "3": {},
            },
            "analog_inputs": {
                "1": {
                    "offset": 0.0,
                    "gain_db": 0,
                },
                "2": {
                    "offset": 0.0,
                    "gain_db": 0,
                },
            },
        },
    },
    "elements": {
        "rr1": {
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "lo_frequency": 5880000000,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": 34300000,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q1",
            },
            "outputs": {
                "out1": ('con1', 1),
                "out2": ('con1', 2),
            },
            "time_of_flight": 284,
            "smearing": 0,
        },
        "rr2": {
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "lo_frequency": 5880000000,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": 134400000,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q2",
            },
            "outputs": {
                "out1": ('con1', 1),
                "out2": ('con1', 2),
            },
            "time_of_flight": 284,
            "smearing": 0,
        },
        "rr3": {
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "lo_frequency": 5880000000,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": -22200000,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q3",
            },
            "outputs": {
                "out1": ('con1', 1),
                "out2": ('con1', 2),
            },
            "time_of_flight": 284,
            "smearing": 0,
        },
        "rr4": {
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "lo_frequency": 5880000000,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": 158000000,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q4",
            },
            "outputs": {
                "out1": ('con1', 1),
                "out2": ('con1', 2),
            },
            "time_of_flight": 284,
            "smearing": 0,
        },
        "rr5": {
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "lo_frequency": 5880000000,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": 63300000,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q5",
            },
            "outputs": {
                "out1": ('con1', 1),
                "out2": ('con1', 2),
            },
            "time_of_flight": 284,
            "smearing": 0,
        },
        "q1_xy": {
            "mixInputs": {
                "I": ('con1', 3),
                "Q": ('con1', 4),
                "lo_frequency": 3200000000,
                "mixer": "octave_octave1_2",
            },
            "intermediate_frequency": -124637000,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q1",
                "x90": "x90_pulse_q1",
                "-x90": "-x90_pulse_q1",
                "y90": "y90_pulse_q1",
                "y180": "y180_pulse_q1",
                "-y90": "-y90_pulse_q1",
            },
        },
        "q2_xy": {
            "mixInputs": {
                "I": ('con1', 7),
                "Q": ('con1', 8),
                "lo_frequency": 3960000000,
                "mixer": "octave_octave1_4",
            },
            "intermediate_frequency": -138111000,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q2",
                "x90": "x90_pulse_q2",
                "-x90": "-x90_pulse_q2",
                "y90": "y90_pulse_q2",
                "y180": "y180_pulse_q2",
                "-y90": "-y90_pulse_q2",
            },
        },
        "q3_xy": {
            "mixInputs": {
                "I": ('con1', 5),
                "Q": ('con1', 6),
                "lo_frequency": 3200000000,
                "mixer": "octave_octave1_3",
            },
            "intermediate_frequency": -197837000,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q3",
                "x90": "x90_pulse_q3",
                "-x90": "-x90_pulse_q3",
                "y90": "y90_pulse_q3",
                "y180": "y180_pulse_q3",
                "-y90": "-y90_pulse_q3",
            },
        },
        "q4_xy": {
            "mixInputs": {
                "I": ('con1', 9),
                "Q": ('con1', 10),
                "lo_frequency": 3960000000,
                "mixer": "octave_octave1_5",
            },
            "intermediate_frequency": -368481000,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q4",
                "x90": "x90_pulse_q4",
                "-x90": "-x90_pulse_q4",
                "y90": "y90_pulse_q4",
                "y180": "y180_pulse_q4",
                "-y90": "-y90_pulse_q4",
            },
        },
        "q00_xy": {
            "mixInputs": {
                "I": ('con1', 9),
                "Q": ('con1', 10),
                "lo_frequency": 3960000000,
                "mixer": "octave_octave1_5",
            },
            "intermediate_frequency": -368481000,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q4",
                "x90": "x90_pulse_q4",
                "-x90": "-x90_pulse_q4",
                "y90": "y90_pulse_q4",
                "y180": "y180_pulse_q4",
                "-y90": "-y90_pulse_q4",
            },
        },
        "q5_xy": {
            "mixInputs": {
                "I": ('con2', 1),
                "Q": ('con2', 2),
                "lo_frequency": 4600000000,
                "mixer": "octave_octave2_1",
            },
            "intermediate_frequency": -131436000,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q5",
                "x90": "x90_pulse_q5",
                "-x90": "-x90_pulse_q5",
                "y90": "y90_pulse_q5",
                "y180": "y180_pulse_q5",
                "-y90": "-y90_pulse_q5",
            },
        },
        "q1_z": {
            "singleInput": {
                "port": ('con2', 5),
            },
            "operations": {
                "const": "const_flux_pulse",
                "cz_2c1t": "cz_2c1t_pulse",
            },
        },
        "q2_z": {
            "singleInput": {
                "port": ('con2', 6),
            },
            "operations": {
                "const": "const_flux_pulse",
                "cz_3c2t": "cz_3c2t_pulse",
                "cz_1_2": "gft_cz_pulse_1_2_q2",
            },
        },
        "q3_z": {
            "singleInput": {
                "port": ('con2', 7),
            },
            "operations": {
                "const": "const_flux_pulse",
                "cz_2c3t": "cz_2c3t_pulse",
            },
        },
        "q4_z": {
            "singleInput": {
                "port": ('con2', 8),
            },
            "operations": {
                "const": "const_flux_pulse",
                "cz_3c4t": "cz_3c4t_pulse",
            },
        },
        "q5_z": {
            "singleInput": {
                "port": ('con2', 9),
            },
            "operations": {
                "const": "const_flux_pulse",
                "cz_4c5t": "cz_4c5t_pulse",
            },
        },
    },
    "pulses": {
        "const_flux_pulse": {
            "operation": "control",
            "length": 200,
            "waveforms": {
                "single": "const_flux_wf",
            },
        },
        "const_pulse": {
            "operation": "control",
            "length": 100,
            "waveforms": {
                "I": "const_wf",
                "Q": "zero_wf",
            },
        },
        "saturation_pulse": {
            "operation": "control",
            "length": 1000,
            "waveforms": {
                "I": "saturation_wf",
                "Q": "zero_wf",
            },
        },
        "cz_4c5t_pulse": {
            "operation": "control",
            "length": 28,
            "waveforms": {
                "single": "cz_4c5t_wf",
            },
        },
        "cz_3c4t_pulse": {
            "operation": "control",
            "length": 48,
            "waveforms": {
                "single": "cz_3c4t_wf",
            },
        },
        "cz_3c2t_pulse": {
            "operation": "control",
            "length": 52,
            "waveforms": {
                "single": "cz_3c2t_wf",
            },
        },
        "cz_2c3t_pulse": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "single": "cz_2c3t_wf",
            },
        },
        "cz_2c1t_pulse": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "single": "cz_2c1t_wf",
            },
        },
        "x90_pulse_q1": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "x90_I_wf_q1",
                "Q": "x90_Q_wf_q1",
            },
        },
        "x180_pulse_q1": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "x180_I_wf_q1",
                "Q": "x180_Q_wf_q1",
            },
        },
        "-x90_pulse_q1": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "minus_x90_I_wf_q1",
                "Q": "minus_x90_Q_wf_q1",
            },
        },
        "y90_pulse_q1": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "y90_I_wf_q1",
                "Q": "y90_Q_wf_q1",
            },
        },
        "y180_pulse_q1": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "y180_I_wf_q1",
                "Q": "y180_Q_wf_q1",
            },
        },
        "-y90_pulse_q1": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "minus_y90_I_wf_q1",
                "Q": "minus_y90_Q_wf_q1",
            },
        },
        "readout_pulse_q1": {
            "operation": "measurement",
            "length": 1800,
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
                "opt_cos": "opt_cosine_weights_q1",
                "opt_sin": "opt_sine_weights_q1",
                "opt_minus_sin": "opt_minus_sine_weights_q1",
            },
            "digital_marker": "ON",
        },
        "x90_pulse_q2": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "x90_I_wf_q2",
                "Q": "x90_Q_wf_q2",
            },
        },
        "x180_pulse_q2": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "x180_I_wf_q2",
                "Q": "x180_Q_wf_q2",
            },
        },
        "-x90_pulse_q2": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "minus_x90_I_wf_q2",
                "Q": "minus_x90_Q_wf_q2",
            },
        },
        "y90_pulse_q2": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "y90_I_wf_q2",
                "Q": "y90_Q_wf_q2",
            },
        },
        "y180_pulse_q2": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "y180_I_wf_q2",
                "Q": "y180_Q_wf_q2",
            },
        },
        "-y90_pulse_q2": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "minus_y90_I_wf_q2",
                "Q": "minus_y90_Q_wf_q2",
            },
        },
        "readout_pulse_q2": {
            "operation": "measurement",
            "length": 1800,
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
                "opt_cos": "opt_cosine_weights_q2",
                "opt_sin": "opt_sine_weights_q2",
                "opt_minus_sin": "opt_minus_sine_weights_q2",
            },
            "digital_marker": "ON",
        },
        "x90_pulse_q3": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "x90_I_wf_q3",
                "Q": "x90_Q_wf_q3",
            },
        },
        "x180_pulse_q3": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "x180_I_wf_q3",
                "Q": "x180_Q_wf_q3",
            },
        },
        "-x90_pulse_q3": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "minus_x90_I_wf_q3",
                "Q": "minus_x90_Q_wf_q3",
            },
        },
        "y90_pulse_q3": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "y90_I_wf_q3",
                "Q": "y90_Q_wf_q3",
            },
        },
        "y180_pulse_q3": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "y180_I_wf_q3",
                "Q": "y180_Q_wf_q3",
            },
        },
        "-y90_pulse_q3": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "minus_y90_I_wf_q3",
                "Q": "minus_y90_Q_wf_q3",
            },
        },
        "readout_pulse_q3": {
            "operation": "measurement",
            "length": 1800,
            "waveforms": {
                "I": "readout_wf_q3",
                "Q": "zero_wf",
            },
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q3",
                "rotated_sin": "rotated_sine_weights_q3",
                "rotated_minus_sin": "rotated_minus_sine_weights_q3",
                "opt_cos": "opt_cosine_weights_q3",
                "opt_sin": "opt_sine_weights_q3",
                "opt_minus_sin": "opt_minus_sine_weights_q3",
            },
            "digital_marker": "ON",
        },
        "x90_pulse_q4": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "x90_I_wf_q4",
                "Q": "x90_Q_wf_q4",
            },
        },
        "x180_pulse_q4": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "x180_I_wf_q4",
                "Q": "x180_Q_wf_q4",
            },
        },
        "-x90_pulse_q4": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "minus_x90_I_wf_q4",
                "Q": "minus_x90_Q_wf_q4",
            },
        },
        "y90_pulse_q4": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "y90_I_wf_q4",
                "Q": "y90_Q_wf_q4",
            },
        },
        "y180_pulse_q4": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "y180_I_wf_q4",
                "Q": "y180_Q_wf_q4",
            },
        },
        "-y90_pulse_q4": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "minus_y90_I_wf_q4",
                "Q": "minus_y90_Q_wf_q4",
            },
        },
        "readout_pulse_q4": {
            "operation": "measurement",
            "length": 1800,
            "waveforms": {
                "I": "readout_wf_q4",
                "Q": "zero_wf",
            },
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q4",
                "rotated_sin": "rotated_sine_weights_q4",
                "rotated_minus_sin": "rotated_minus_sine_weights_q4",
                "opt_cos": "opt_cosine_weights_q4",
                "opt_sin": "opt_sine_weights_q4",
                "opt_minus_sin": "opt_minus_sine_weights_q4",
            },
            "digital_marker": "ON",
        },
        "x90_pulse_q5": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "x90_I_wf_q5",
                "Q": "x90_Q_wf_q5",
            },
        },
        "x180_pulse_q5": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "x180_I_wf_q5",
                "Q": "x180_Q_wf_q5",
            },
        },
        "-x90_pulse_q5": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "minus_x90_I_wf_q5",
                "Q": "minus_x90_Q_wf_q5",
            },
        },
        "y90_pulse_q5": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "y90_I_wf_q5",
                "Q": "y90_Q_wf_q5",
            },
        },
        "y180_pulse_q5": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "y180_I_wf_q5",
                "Q": "y180_Q_wf_q5",
            },
        },
        "-y90_pulse_q5": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "I": "minus_y90_I_wf_q5",
                "Q": "minus_y90_Q_wf_q5",
            },
        },
        "readout_pulse_q5": {
            "operation": "measurement",
            "length": 1800,
            "waveforms": {
                "I": "readout_wf_q5",
                "Q": "zero_wf",
            },
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q5",
                "rotated_sin": "rotated_sine_weights_q5",
                "rotated_minus_sin": "rotated_minus_sine_weights_q5",
                "opt_cos": "opt_cosine_weights_q5",
                "opt_sin": "opt_sine_weights_q5",
                "opt_minus_sin": "opt_minus_sine_weights_q5",
            },
            "digital_marker": "ON",
        },
        "gft_cz_pulse_1_2_q2": {
            "operation": "control",
            "length": 24,
            "waveforms": {
                "single": "gft_cz_wf_1_2_q2",
            },
        },
        "g_cz_pulse_1_2_q2": {
            "operation": "control",
            "length": 16,
            "waveforms": {
                "single": "g_cz_wf_1_2_q2",
            },
        },
    },
    "waveforms": {
        "const_wf": {
            "type": "constant",
            "sample": 0.27,
        },
        "saturation_wf": {
            "type": "constant",
            "sample": 0.27,
        },
        "const_flux_wf": {
            "type": "constant",
            "sample": 0.48,
        },
        "zero_wf": {
            "type": "constant",
            "sample": 0.0,
        },
        "x90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007544496482014039, 0.0016719663934131246, 0.0027464431239315745, 0.003955228231179286, 0.005257272897700412, 0.006593597485558204, 0.007890560914059744, 0.009065942537806505, 0.010037269651154779, 0.010731276544516957] + [0.011093009024062787] * 2 + [0.010731276544516957, 0.010037269651154779, 0.009065942537806505, 0.007890560914059744, 0.006593597485558204, 0.005257272897700412, 0.003955228231179286, 0.0027464431239315745, 0.0016719663934131246, 0.0007544496482014039, 0.0],
        },
        "x90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.0004843311170773316, -0.0006002538063475515, -0.0007169792467158665, -0.0008237122522291399, -0.0009076695128639909, -0.0009554896585398429, -0.0009551195563474098, -0.0008978964195749315, -0.0007804349549344685, -0.0006058985092187082, -0.0003843072747623774, -0.00013171070865373793, 0.00013171070865373793, 0.0003843072747623774, 0.0006058985092187082, 0.0007804349549344685, 0.0008978964195749315, 0.0009551195563474098, 0.0009554896585398429, 0.0009076695128639909, 0.0008237122522291399, 0.0007169792467158665, 0.0006002538063475515, 0.0004843311170773316],
        },
        "x180_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0015088992964028079, 0.003343932786826249, 0.005492886247863149, 0.007910456462358571, 0.010514545795400823, 0.013187194971116409, 0.01578112182811949, 0.01813188507561301, 0.020074539302309558, 0.021462553089033914] + [0.022186018048125575] * 2 + [0.021462553089033914, 0.020074539302309558, 0.01813188507561301, 0.01578112182811949, 0.013187194971116409, 0.010514545795400823, 0.007910456462358571, 0.005492886247863149, 0.003343932786826249, 0.0015088992964028079, 0.0],
        },
        "x180_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.0009686622341546632, -0.001200507612695103, -0.001433958493431733, -0.0016474245044582798, -0.0018153390257279818, -0.0019109793170796858, -0.0019102391126948196, -0.001795792839149863, -0.001560869909868937, -0.0012117970184374164, -0.0007686145495247548, -0.00026342141730747586, 0.00026342141730747586, 0.0007686145495247548, 0.0012117970184374164, 0.001560869909868937, 0.001795792839149863, 0.0019102391126948196, 0.0019109793170796858, 0.0018153390257279818, 0.0016474245044582798, 0.001433958493431733, 0.001200507612695103, 0.0009686622341546632],
        },
        "minus_x90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, -0.0007544496482014039, -0.0016719663934131246, -0.0027464431239315745, -0.003955228231179286, -0.005257272897700412, -0.006593597485558204, -0.007890560914059744, -0.009065942537806505, -0.010037269651154779, -0.010731276544516957] + [-0.011093009024062787] * 2 + [-0.010731276544516957, -0.010037269651154779, -0.009065942537806505, -0.007890560914059744, -0.006593597485558204, -0.005257272897700412, -0.003955228231179286, -0.0027464431239315745, -0.0016719663934131246, -0.0007544496482014039, 0.0],
        },
        "minus_x90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0004843311170773316, 0.0006002538063475515, 0.0007169792467158665, 0.0008237122522291399, 0.0009076695128639909, 0.0009554896585398429, 0.0009551195563474098, 0.0008978964195749315, 0.0007804349549344685, 0.0006058985092187082, 0.0003843072747623774, 0.00013171070865373793, -0.00013171070865373793, -0.0003843072747623774, -0.0006058985092187082, -0.0007804349549344685, -0.0008978964195749315, -0.0009551195563474098, -0.0009554896585398429, -0.0009076695128639909, -0.0008237122522291399, -0.0007169792467158665, -0.0006002538063475515, -0.0004843311170773316],
        },
        "y90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0004843311170773316, 0.0006002538063475515, 0.0007169792467158665, 0.0008237122522291399, 0.0009076695128639909, 0.0009554896585398429, 0.0009551195563474098, 0.0008978964195749315, 0.0007804349549344685, 0.0006058985092187082, 0.0003843072747623774, 0.00013171070865373793, -0.00013171070865373793, -0.0003843072747623774, -0.0006058985092187082, -0.0007804349549344685, -0.0008978964195749315, -0.0009551195563474098, -0.0009554896585398429, -0.0009076695128639909, -0.0008237122522291399, -0.0007169792467158665, -0.0006002538063475515, -0.0004843311170773316],
        },
        "y90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007544496482014039, 0.0016719663934131246, 0.0027464431239315745, 0.003955228231179286, 0.005257272897700412, 0.006593597485558204, 0.007890560914059744, 0.009065942537806505, 0.010037269651154779, 0.010731276544516957] + [0.011093009024062787] * 2 + [0.010731276544516957, 0.010037269651154779, 0.009065942537806505, 0.007890560914059744, 0.006593597485558204, 0.005257272897700412, 0.003955228231179286, 0.0027464431239315745, 0.0016719663934131246, 0.0007544496482014039, 0.0],
        },
        "y180_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0009686622341546632, 0.001200507612695103, 0.001433958493431733, 0.0016474245044582798, 0.0018153390257279818, 0.0019109793170796858, 0.0019102391126948196, 0.001795792839149863, 0.001560869909868937, 0.0012117970184374164, 0.0007686145495247548, 0.00026342141730747586, -0.00026342141730747586, -0.0007686145495247548, -0.0012117970184374164, -0.001560869909868937, -0.001795792839149863, -0.0019102391126948196, -0.0019109793170796858, -0.0018153390257279818, -0.0016474245044582798, -0.001433958493431733, -0.001200507612695103, -0.0009686622341546632],
        },
        "y180_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0015088992964028079, 0.003343932786826249, 0.005492886247863149, 0.007910456462358571, 0.010514545795400823, 0.013187194971116409, 0.01578112182811949, 0.01813188507561301, 0.020074539302309558, 0.021462553089033914] + [0.022186018048125575] * 2 + [0.021462553089033914, 0.020074539302309558, 0.01813188507561301, 0.01578112182811949, 0.013187194971116409, 0.010514545795400823, 0.007910456462358571, 0.005492886247863149, 0.003343932786826249, 0.0015088992964028079, 0.0],
        },
        "minus_y90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.0004843311170773316, -0.0006002538063475515, -0.0007169792467158665, -0.0008237122522291399, -0.0009076695128639909, -0.0009554896585398429, -0.0009551195563474098, -0.0008978964195749315, -0.0007804349549344685, -0.0006058985092187082, -0.0003843072747623774, -0.00013171070865373793, 0.00013171070865373793, 0.0003843072747623774, 0.0006058985092187082, 0.0007804349549344685, 0.0008978964195749315, 0.0009551195563474098, 0.0009554896585398429, 0.0009076695128639909, 0.0008237122522291399, 0.0007169792467158665, 0.0006002538063475515, 0.0004843311170773316],
        },
        "minus_y90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, -0.0007544496482014039, -0.0016719663934131246, -0.0027464431239315745, -0.003955228231179286, -0.005257272897700412, -0.006593597485558204, -0.007890560914059744, -0.009065942537806505, -0.010037269651154779, -0.010731276544516957] + [-0.011093009024062787] * 2 + [-0.010731276544516957, -0.010037269651154779, -0.009065942537806505, -0.007890560914059744, -0.006593597485558204, -0.005257272897700412, -0.003955228231179286, -0.0027464431239315745, -0.0016719663934131246, -0.0007544496482014039, 0.0],
        },
        "readout_wf_q1": {
            "type": "constant",
            "sample": 0.0324,
        },
        "x90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.002670203474077361, 0.005917545965957568, 0.009720412738426047, 0.013998633558702928, 0.018606925444366956, 0.02333654333934451, 0.027926851335103017, 0.032086848099071884, 0.03552464018859211, 0.03798092023605078] + [0.039261190332103686] * 2 + [0.03798092023605078, 0.03552464018859211, 0.032086848099071884, 0.027926851335103017, 0.02333654333934451, 0.018606925444366956, 0.013998633558702928, 0.009720412738426047, 0.005917545965957568, 0.002670203474077361, 0.0],
        },
        "x90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.0011938334743415641, -0.0014795726763189318, -0.0017672905889318123, -0.0020303780311918635, -0.0022373252716763126, -0.0023551977119197235, -0.0023542854426669853, -0.002213235458932608, -0.0019237033114233198, -0.0014934863709024312, -0.0009472835274613423, -0.0003246552768877233, 0.0003246552768877233, 0.0009472835274613423, 0.0014934863709024312, 0.0019237033114233198, 0.002213235458932608, 0.0023542854426669853, 0.0023551977119197235, 0.0022373252716763126, 0.0020303780311918635, 0.0017672905889318123, 0.0014795726763189318, 0.0011938334743415641],
        },
        "x180_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.005201361798326289, 0.011526948349060446, 0.01893465571910518, 0.02726831813675344, 0.0362449349385543, 0.04545788596586014, 0.05439947146055351, 0.06250284203112216, 0.06919941052060677, 0.07398406507179489] + [0.07647793792972385] * 2 + [0.07398406507179489, 0.06919941052060677, 0.06250284203112216, 0.05439947146055351, 0.04545788596586014, 0.0362449349385543, 0.02726831813675344, 0.01893465571910518, 0.011526948349060446, 0.005201361798326289, 0.0],
        },
        "x180_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.002325500617195082, -0.002882099761746364, -0.003442553290433316, -0.003955028457616458, -0.004358146602497455, -0.004587753527104358, -0.004585976493074163, -0.00431122140262023, -0.003747233876552562, -0.0029092026249486515, -0.0018452392859775167, -0.0006324048227868956, 0.0006324048227868956, 0.0018452392859775167, 0.0029092026249486515, 0.003747233876552562, 0.00431122140262023, 0.004585976493074163, 0.004587753527104358, 0.004358146602497455, 0.003955028457616458, 0.003442553290433316, 0.002882099761746364, 0.002325500617195082],
        },
        "minus_x90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, -0.002670203474077361, -0.005917545965957568, -0.009720412738426047, -0.013998633558702928, -0.018606925444366956, -0.02333654333934451, -0.027926851335103017, -0.032086848099071884, -0.03552464018859211, -0.03798092023605078] + [-0.039261190332103686] * 2 + [-0.03798092023605078, -0.03552464018859211, -0.032086848099071884, -0.027926851335103017, -0.02333654333934451, -0.018606925444366956, -0.013998633558702928, -0.009720412738426047, -0.005917545965957568, -0.002670203474077361, 0.0],
        },
        "minus_x90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0011938334743415641, 0.0014795726763189318, 0.0017672905889318123, 0.0020303780311918635, 0.0022373252716763126, 0.0023551977119197235, 0.0023542854426669853, 0.002213235458932608, 0.0019237033114233198, 0.0014934863709024312, 0.0009472835274613423, 0.0003246552768877233, -0.0003246552768877233, -0.0009472835274613423, -0.0014934863709024312, -0.0019237033114233198, -0.002213235458932608, -0.0023542854426669853, -0.0023551977119197235, -0.0022373252716763126, -0.0020303780311918635, -0.0017672905889318123, -0.0014795726763189318, -0.0011938334743415641],
        },
        "y90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.001162750308597541, 0.001441049880873182, 0.001721276645216658, 0.001977514228808229, 0.0021790733012487275, 0.002293876763552179, 0.0022929882465370817, 0.002155610701310115, 0.001873616938276281, 0.0014546013124743257, 0.0009226196429887583, 0.0003162024113934478, -0.0003162024113934478, -0.0009226196429887583, -0.0014546013124743257, -0.001873616938276281, -0.002155610701310115, -0.0022929882465370817, -0.002293876763552179, -0.0021790733012487275, -0.001977514228808229, -0.001721276645216658, -0.001441049880873182, -0.001162750308597541],
        },
        "y90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0026006808991631443, 0.005763474174530223, 0.00946732785955259, 0.01363415906837672, 0.01812246746927715, 0.02272894298293007, 0.027199735730276755, 0.03125142101556108, 0.034599705260303384, 0.036992032535897446] + [0.038238968964861925] * 2 + [0.036992032535897446, 0.034599705260303384, 0.03125142101556108, 0.027199735730276755, 0.02272894298293007, 0.01812246746927715, 0.01363415906837672, 0.00946732785955259, 0.005763474174530223, 0.0026006808991631443, 0.0],
        },
        "y180_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.002325500617195082, 0.002882099761746364, 0.003442553290433316, 0.003955028457616458, 0.004358146602497455, 0.004587753527104358, 0.004585976493074163, 0.00431122140262023, 0.003747233876552562, 0.0029092026249486515, 0.0018452392859775167, 0.0006324048227868956, -0.0006324048227868956, -0.0018452392859775167, -0.0029092026249486515, -0.003747233876552562, -0.00431122140262023, -0.004585976493074163, -0.004587753527104358, -0.004358146602497455, -0.003955028457616458, -0.003442553290433316, -0.002882099761746364, -0.002325500617195082],
        },
        "y180_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.005201361798326289, 0.011526948349060446, 0.01893465571910518, 0.02726831813675344, 0.0362449349385543, 0.04545788596586014, 0.05439947146055351, 0.06250284203112216, 0.06919941052060677, 0.07398406507179489] + [0.07647793792972385] * 2 + [0.07398406507179489, 0.06919941052060677, 0.06250284203112216, 0.05439947146055351, 0.04545788596586014, 0.0362449349385543, 0.02726831813675344, 0.01893465571910518, 0.011526948349060446, 0.005201361798326289, 0.0],
        },
        "minus_y90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.001162750308597541, -0.001441049880873182, -0.001721276645216658, -0.001977514228808229, -0.0021790733012487275, -0.002293876763552179, -0.0022929882465370817, -0.002155610701310115, -0.001873616938276281, -0.0014546013124743257, -0.0009226196429887583, -0.0003162024113934478, 0.0003162024113934478, 0.0009226196429887583, 0.0014546013124743257, 0.001873616938276281, 0.002155610701310115, 0.0022929882465370817, 0.002293876763552179, 0.0021790733012487275, 0.001977514228808229, 0.001721276645216658, 0.001441049880873182, 0.001162750308597541],
        },
        "minus_y90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, -0.0026006808991631443, -0.005763474174530223, -0.00946732785955259, -0.01363415906837672, -0.01812246746927715, -0.02272894298293007, -0.027199735730276755, -0.03125142101556108, -0.034599705260303384, -0.036992032535897446] + [-0.038238968964861925] * 2 + [-0.036992032535897446, -0.034599705260303384, -0.03125142101556108, -0.027199735730276755, -0.02272894298293007, -0.01812246746927715, -0.01363415906837672, -0.00946732785955259, -0.005763474174530223, -0.0026006808991631443, 0.0],
        },
        "readout_wf_q2": {
            "type": "constant",
            "sample": 0.144,
        },
        "x90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0006718872338699294, 0.001488996486209424, 0.00244588897074661, 0.0035223919341823076, 0.004681948693801121, 0.005872033987138627, 0.0070270655687475455, 0.008073820524235227, 0.0089388514629152, 0.00955691043209812] + [0.009879057093127613] * 2 + [0.00955691043209812, 0.0089388514629152, 0.008073820524235227, 0.0070270655687475455, 0.005872033987138627, 0.004681948693801121, 0.0035223919341823076, 0.00244588897074661, 0.001488996486209424, 0.0006718872338699294, 0.0],
        },
        "x90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.00047033333302028704, 0.0005829057094270503, 0.0006962576364062219, 0.0007999059225813085, 0.0008814367118147775, 0.0009278747945812992, 0.0009275153888120072, 0.0008719460733270016, 0.0007578793941114009, 0.0005883872732202693, 0.000373200306710981, 0.00012790410198997286, -0.00012790410198997286, -0.000373200306710981, -0.0005883872732202693, -0.0007578793941114009, -0.0008719460733270016, -0.0009275153888120072, -0.0009278747945812992, -0.0008814367118147775, -0.0007999059225813085, -0.0006962576364062219, -0.0005829057094270503, -0.00047033333302028704],
        },
        "x180_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0013437744677398588, 0.002977992972418848, 0.00489177794149322, 0.007044783868364615, 0.009363897387602241, 0.011744067974277255, 0.014054131137495091, 0.016147641048470454, 0.0178777029258304, 0.01911382086419624] + [0.019758114186255227] * 2 + [0.01911382086419624, 0.0178777029258304, 0.016147641048470454, 0.014054131137495091, 0.011744067974277255, 0.009363897387602241, 0.007044783868364615, 0.00489177794149322, 0.002977992972418848, 0.0013437744677398588, 0.0],
        },
        "x180_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0009406666660405741, 0.0011658114188541006, 0.0013925152728124438, 0.001599811845162617, 0.001762873423629555, 0.0018557495891625983, 0.0018550307776240144, 0.001743892146654003, 0.0015157587882228018, 0.0011767745464405387, 0.000746400613421962, 0.00025580820397994573, -0.00025580820397994573, -0.000746400613421962, -0.0011767745464405387, -0.0015157587882228018, -0.001743892146654003, -0.0018550307776240144, -0.0018557495891625983, -0.001762873423629555, -0.001599811845162617, -0.0013925152728124438, -0.0011658114188541006, -0.0009406666660405741],
        },
        "minus_x90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, -0.0006718872338699294, -0.001488996486209424, -0.00244588897074661, -0.0035223919341823076, -0.004681948693801121, -0.005872033987138627, -0.0070270655687475455, -0.008073820524235227, -0.0089388514629152, -0.00955691043209812] + [-0.009879057093127613] * 2 + [-0.00955691043209812, -0.0089388514629152, -0.008073820524235227, -0.0070270655687475455, -0.005872033987138627, -0.004681948693801121, -0.0035223919341823076, -0.00244588897074661, -0.001488996486209424, -0.0006718872338699294, 0.0],
        },
        "minus_x90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.00047033333302028704, -0.0005829057094270503, -0.0006962576364062219, -0.0007999059225813085, -0.0008814367118147775, -0.0009278747945812992, -0.0009275153888120072, -0.0008719460733270016, -0.0007578793941114009, -0.0005883872732202693, -0.000373200306710981, -0.00012790410198997286, 0.00012790410198997286, 0.000373200306710981, 0.0005883872732202693, 0.0007578793941114009, 0.0008719460733270016, 0.0009275153888120072, 0.0009278747945812992, 0.0008814367118147775, 0.0007999059225813085, 0.0006962576364062219, 0.0005829057094270503, 0.00047033333302028704],
        },
        "y90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.00047033333302028704, -0.0005829057094270503, -0.0006962576364062219, -0.0007999059225813085, -0.0008814367118147775, -0.0009278747945812992, -0.0009275153888120072, -0.0008719460733270016, -0.0007578793941114009, -0.0005883872732202693, -0.000373200306710981, -0.00012790410198997286, 0.00012790410198997286, 0.000373200306710981, 0.0005883872732202693, 0.0007578793941114009, 0.0008719460733270016, 0.0009275153888120072, 0.0009278747945812992, 0.0008814367118147775, 0.0007999059225813085, 0.0006962576364062219, 0.0005829057094270503, 0.00047033333302028704],
        },
        "y90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0006718872338699294, 0.001488996486209424, 0.00244588897074661, 0.0035223919341823076, 0.004681948693801121, 0.005872033987138627, 0.0070270655687475455, 0.008073820524235227, 0.0089388514629152, 0.00955691043209812] + [0.009879057093127613] * 2 + [0.00955691043209812, 0.0089388514629152, 0.008073820524235227, 0.0070270655687475455, 0.005872033987138627, 0.004681948693801121, 0.0035223919341823076, 0.00244588897074661, 0.001488996486209424, 0.0006718872338699294, 0.0],
        },
        "y180_I_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.0009406666660405741, -0.0011658114188541006, -0.0013925152728124438, -0.001599811845162617, -0.001762873423629555, -0.0018557495891625983, -0.0018550307776240144, -0.001743892146654003, -0.0015157587882228018, -0.0011767745464405387, -0.000746400613421962, -0.00025580820397994573, 0.00025580820397994573, 0.000746400613421962, 0.0011767745464405387, 0.0015157587882228018, 0.001743892146654003, 0.0018550307776240144, 0.0018557495891625983, 0.001762873423629555, 0.001599811845162617, 0.0013925152728124438, 0.0011658114188541006, 0.0009406666660405741],
        },
        "y180_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0013437744677398588, 0.002977992972418848, 0.00489177794149322, 0.007044783868364615, 0.009363897387602241, 0.011744067974277255, 0.014054131137495091, 0.016147641048470454, 0.0178777029258304, 0.01911382086419624] + [0.019758114186255227] * 2 + [0.01911382086419624, 0.0178777029258304, 0.016147641048470454, 0.014054131137495091, 0.011744067974277255, 0.009363897387602241, 0.007044783868364615, 0.00489177794149322, 0.002977992972418848, 0.0013437744677398588, 0.0],
        },
        "minus_y90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.00047033333302028704, 0.0005829057094270503, 0.0006962576364062219, 0.0007999059225813085, 0.0008814367118147775, 0.0009278747945812992, 0.0009275153888120072, 0.0008719460733270016, 0.0007578793941114009, 0.0005883872732202693, 0.000373200306710981, 0.00012790410198997286, -0.00012790410198997286, -0.000373200306710981, -0.0005883872732202693, -0.0007578793941114009, -0.0008719460733270016, -0.0009275153888120072, -0.0009278747945812992, -0.0008814367118147775, -0.0007999059225813085, -0.0006962576364062219, -0.0005829057094270503, -0.00047033333302028704],
        },
        "minus_y90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, -0.0006718872338699294, -0.001488996486209424, -0.00244588897074661, -0.0035223919341823076, -0.004681948693801121, -0.005872033987138627, -0.0070270655687475455, -0.008073820524235227, -0.0089388514629152, -0.00955691043209812] + [-0.009879057093127613] * 2 + [-0.00955691043209812, -0.0089388514629152, -0.008073820524235227, -0.0070270655687475455, -0.005872033987138627, -0.004681948693801121, -0.0035223919341823076, -0.00244588897074661, -0.001488996486209424, -0.0006718872338699294, 0.0],
        },
        "readout_wf_q3": {
            "type": "constant",
            "sample": 0.0891,
        },
        "x90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0032645524905044986, 0.00723470687098729, 0.011884037273573345, 0.017114528720892336, 0.022748560321242322, 0.02853092336139178, 0.03414296811573922, 0.039228920526537314, 0.04343191585503292, 0.04643492863070854] + [0.04800016849769362] * 2 + [0.04643492863070854, 0.04343191585503292, 0.039228920526537314, 0.03414296811573922, 0.02853092336139178, 0.022748560321242322, 0.017114528720892336, 0.011884037273573345, 0.00723470687098729, 0.0032645524905044986, 0.0],
        },
        "x90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.002341149429575977, 0.0029014940539263383, 0.0034657189994229806, 0.003981642726319167, 0.004387473543116882, 0.004618625543935746, 0.004616836551847176, 0.004340232573102515, 0.0037724498491684866, 0.002928779298340698, 0.001857656312733222, 0.0006366604159040895, -0.0006366604159040895, -0.001857656312733222, -0.002928779298340698, -0.0037724498491684866, -0.004340232573102515, -0.004616836551847176, -0.004618625543935746, -0.004387473543116882, -0.003981642726319167, -0.0034657189994229806, -0.0029014940539263383, -0.002341149429575977],
        },
        "x180_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.006452640225472251, 0.014299957103161412, 0.023489717863479788, 0.03382818833075763, 0.04496428708908453, 0.05639357439865581, 0.0674862144570966, 0.0775389923512213, 0.08584653735256745, 0.09178222412442785] + [0.09487604165611044] * 2 + [0.09178222412442785, 0.08584653735256745, 0.0775389923512213, 0.0674862144570966, 0.05639357439865581, 0.04496428708908453, 0.03382818833075763, 0.023489717863479788, 0.014299957103161412, 0.006452640225472251, 0.0],
        },
        "x180_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.004627462730975668, 0.005735027174717087, 0.006850261373008041, 0.007870024480854845, 0.00867218044582158, 0.009129070234857166, 0.009125534153771831, 0.008578805018625457, 0.007456538596369603, 0.0057889585684324715, 0.00367180122957448, 0.0012584085021079738, -0.0012584085021079738, -0.00367180122957448, -0.0057889585684324715, -0.007456538596369603, -0.008578805018625457, -0.009125534153771831, -0.009129070234857166, -0.00867218044582158, -0.007870024480854845, -0.006850261373008041, -0.005735027174717087, -0.004627462730975668],
        },
        "minus_x90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, -0.0032645524905044986, -0.00723470687098729, -0.011884037273573345, -0.017114528720892336, -0.022748560321242322, -0.02853092336139178, -0.03414296811573922, -0.039228920526537314, -0.04343191585503292, -0.04643492863070854] + [-0.04800016849769362] * 2 + [-0.04643492863070854, -0.04343191585503292, -0.039228920526537314, -0.03414296811573922, -0.02853092336139178, -0.022748560321242322, -0.017114528720892336, -0.011884037273573345, -0.00723470687098729, -0.0032645524905044986, 0.0],
        },
        "minus_x90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.002341149429575977, -0.0029014940539263383, -0.0034657189994229806, -0.003981642726319167, -0.004387473543116882, -0.004618625543935746, -0.004616836551847176, -0.004340232573102515, -0.0037724498491684866, -0.002928779298340698, -0.001857656312733222, -0.0006366604159040895, 0.0006366604159040895, 0.001857656312733222, 0.002928779298340698, 0.0037724498491684866, 0.004340232573102515, 0.004616836551847176, 0.004618625543935746, 0.004387473543116882, 0.003981642726319167, 0.0034657189994229806, 0.0029014940539263383, 0.002341149429575977],
        },
        "y90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.002313731365487834, -0.0028675135873585437, -0.0034251306865040205, -0.003935012240427423, -0.00433609022291079, -0.004564535117428583, -0.004562767076885916, -0.004289402509312729, -0.0037282692981848017, -0.0028944792842162358, -0.00183590061478724, -0.0006292042510539869, 0.0006292042510539869, 0.00183590061478724, 0.0028944792842162358, 0.0037282692981848017, 0.004289402509312729, 0.004562767076885916, 0.004564535117428583, 0.00433609022291079, 0.003935012240427423, 0.0034251306865040205, 0.0028675135873585437, 0.002313731365487834],
        },
        "y90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0032263201127361255, 0.007149978551580706, 0.011744858931739894, 0.016914094165378816, 0.022482143544542265, 0.028196787199327906, 0.0337431072285483, 0.03876949617561065, 0.042923268676283724, 0.045891112062213926] + [0.04743802082805522] * 2 + [0.045891112062213926, 0.042923268676283724, 0.03876949617561065, 0.0337431072285483, 0.028196787199327906, 0.022482143544542265, 0.016914094165378816, 0.011744858931739894, 0.007149978551580706, 0.0032263201127361255, 0.0],
        },
        "y180_I_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.004627462730975668, -0.005735027174717087, -0.006850261373008041, -0.007870024480854845, -0.00867218044582158, -0.009129070234857166, -0.009125534153771831, -0.008578805018625457, -0.007456538596369603, -0.0057889585684324715, -0.00367180122957448, -0.0012584085021079738, 0.0012584085021079738, 0.00367180122957448, 0.0057889585684324715, 0.007456538596369603, 0.008578805018625457, 0.009125534153771831, 0.009129070234857166, 0.00867218044582158, 0.007870024480854845, 0.006850261373008041, 0.005735027174717087, 0.004627462730975668],
        },
        "y180_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.006452640225472251, 0.014299957103161412, 0.023489717863479788, 0.03382818833075763, 0.04496428708908453, 0.05639357439865581, 0.0674862144570966, 0.0775389923512213, 0.08584653735256745, 0.09178222412442785] + [0.09487604165611044] * 2 + [0.09178222412442785, 0.08584653735256745, 0.0775389923512213, 0.0674862144570966, 0.05639357439865581, 0.04496428708908453, 0.03382818833075763, 0.023489717863479788, 0.014299957103161412, 0.006452640225472251, 0.0],
        },
        "minus_y90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.002313731365487834, 0.0028675135873585437, 0.0034251306865040205, 0.003935012240427423, 0.00433609022291079, 0.004564535117428583, 0.004562767076885916, 0.004289402509312729, 0.0037282692981848017, 0.0028944792842162358, 0.00183590061478724, 0.0006292042510539869, -0.0006292042510539869, -0.00183590061478724, -0.0028944792842162358, -0.0037282692981848017, -0.004289402509312729, -0.004562767076885916, -0.004564535117428583, -0.00433609022291079, -0.003935012240427423, -0.0034251306865040205, -0.0028675135873585437, -0.002313731365487834],
        },
        "minus_y90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, -0.0032263201127361255, -0.007149978551580706, -0.011744858931739894, -0.016914094165378816, -0.022482143544542265, -0.028196787199327906, -0.0337431072285483, -0.03876949617561065, -0.042923268676283724, -0.045891112062213926] + [-0.04743802082805522] * 2 + [-0.045891112062213926, -0.042923268676283724, -0.03876949617561065, -0.0337431072285483, -0.028196787199327906, -0.022482143544542265, -0.016914094165378816, -0.011744858931739894, -0.007149978551580706, -0.0032263201127361255, 0.0],
        },
        "readout_wf_q4": {
            "type": "constant",
            "sample": 0.0691,
        },
        "x90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.0026121100591890095, 0.005788802798532825, 0.009508933734828941, 0.013694076832936275, 0.018202109912468303, 0.02282882941138589, 0.027319269861673892, 0.031388761006767796, 0.03475175988891816, 0.03715460067706034] + [0.03840701699246275] * 2 + [0.03715460067706034, 0.03475175988891816, 0.031388761006767796, 0.027319269861673892, 0.02282882941138589, 0.018202109912468303, 0.013694076832936275, 0.009508933734828941, 0.005788802798532825, 0.0026121100591890095, 0.0],
        },
        "x90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0002455604341849997, -0.0003043343285423653, -0.00036351522526080216, -0.0004176298634733303, -0.00046019698469999603, -0.0004844422485719789, -0.0004842546032775466, -0.000455241934432167, -0.00039568786648135095, -0.00030719624601785407, -0.00019484740485099886, -6.677856875890505e-05, 6.677856875890505e-05, 0.00019484740485099886, 0.00030719624601785407, 0.00039568786648135095, 0.000455241934432167, 0.0004842546032775466, 0.0004844422485719789, 0.00046019698469999603, 0.0004176298634733303, 0.00036351522526080216, 0.0003043343285423653, 0.0002455604341849997],
        },
        "x180_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.005200109678661469, 0.011524173476005501, 0.018930097594580936, 0.027261753856342007, 0.03623620972436113, 0.04544694292533617, 0.054386375919306354, 0.062487795771959925, 0.06918275220186906, 0.07396625494699463] + [0.07645952745690551] * 2 + [0.07396625494699463, 0.06918275220186906, 0.062487795771959925, 0.054386375919306354, 0.04544694292533617, 0.03623620972436113, 0.027261753856342007, 0.018930097594580936, 0.011524173476005501, 0.005200109678661469, 0.0],
        },
        "x180_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.000488854283153056, -0.000605859573885428, -0.00072367511260471, -0.0008314048971657783, -0.0009161462342717137, -0.0009644129720681843, -0.0009640394134930774, -0.0009062818701093581, -0.0007877234333906347, -0.0006115569926107478, -0.00038789631863457146, -0.00013294075435632918, 0.00013294075435632918, 0.00038789631863457146, 0.0006115569926107478, 0.0007877234333906347, 0.0009062818701093581, 0.0009640394134930774, 0.0009644129720681843, 0.0009161462342717137, 0.0008314048971657783, 0.00072367511260471, 0.000605859573885428, 0.000488854283153056],
        },
        "minus_x90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, -0.0026121100591890095, -0.005788802798532825, -0.009508933734828941, -0.013694076832936275, -0.018202109912468303, -0.02282882941138589, -0.027319269861673892, -0.031388761006767796, -0.03475175988891816, -0.03715460067706034] + [-0.03840701699246275] * 2 + [-0.03715460067706034, -0.03475175988891816, -0.031388761006767796, -0.027319269861673892, -0.02282882941138589, -0.018202109912468303, -0.013694076832936275, -0.009508933734828941, -0.005788802798532825, -0.0026121100591890095, 0.0],
        },
        "minus_x90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0002455604341849997, 0.0003043343285423653, 0.00036351522526080216, 0.0004176298634733303, 0.00046019698469999603, 0.0004844422485719789, 0.0004842546032775466, 0.000455241934432167, 0.00039568786648135095, 0.00030719624601785407, 0.00019484740485099886, 6.677856875890505e-05, -6.677856875890505e-05, -0.00019484740485099886, -0.00030719624601785407, -0.00039568786648135095, -0.000455241934432167, -0.0004842546032775466, -0.0004844422485719789, -0.00046019698469999603, -0.0004176298634733303, -0.00036351522526080216, -0.0003043343285423653, -0.0002455604341849997],
        },
        "y90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.000244427141576528, 0.000302929786942714, 0.000361837556302355, 0.00041570244858288915, 0.00045807311713585687, 0.00048220648603409215, 0.0004820197067465387, 0.00045314093505467907, 0.00039386171669531737, 0.0003057784963053739, 0.00019394815931728573, 6.647037717816459e-05, -6.647037717816459e-05, -0.00019394815931728573, -0.0003057784963053739, -0.00039386171669531737, -0.00045314093505467907, -0.0004820197067465387, -0.00048220648603409215, -0.00045807311713585687, -0.00041570244858288915, -0.000361837556302355, -0.000302929786942714, -0.000244427141576528],
        },
        "y90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.0026000548393307343, 0.0057620867380027505, 0.009465048797290468, 0.013630876928171004, 0.018118104862180566, 0.022723471462668086, 0.027193187959653177, 0.031243897885979963, 0.03459137610093453, 0.036983127473497315] + [0.038229763728452756] * 2 + [0.036983127473497315, 0.03459137610093453, 0.031243897885979963, 0.027193187959653177, 0.022723471462668086, 0.018118104862180566, 0.013630876928171004, 0.009465048797290468, 0.0057620867380027505, 0.0026000548393307343, 0.0],
        },
        "y180_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.000488854283153056, 0.000605859573885428, 0.00072367511260471, 0.0008314048971657783, 0.0009161462342717137, 0.0009644129720681843, 0.0009640394134930774, 0.0009062818701093581, 0.0007877234333906347, 0.0006115569926107478, 0.00038789631863457146, 0.00013294075435632918, -0.00013294075435632918, -0.00038789631863457146, -0.0006115569926107478, -0.0007877234333906347, -0.0009062818701093581, -0.0009640394134930774, -0.0009644129720681843, -0.0009161462342717137, -0.0008314048971657783, -0.00072367511260471, -0.000605859573885428, -0.000488854283153056],
        },
        "y180_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.005200109678661469, 0.011524173476005501, 0.018930097594580936, 0.027261753856342007, 0.03623620972436113, 0.04544694292533617, 0.054386375919306354, 0.062487795771959925, 0.06918275220186906, 0.07396625494699463] + [0.07645952745690551] * 2 + [0.07396625494699463, 0.06918275220186906, 0.062487795771959925, 0.054386375919306354, 0.04544694292533617, 0.03623620972436113, 0.027261753856342007, 0.018930097594580936, 0.011524173476005501, 0.005200109678661469, 0.0],
        },
        "minus_y90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.000244427141576528, -0.000302929786942714, -0.000361837556302355, -0.00041570244858288915, -0.00045807311713585687, -0.00048220648603409215, -0.0004820197067465387, -0.00045314093505467907, -0.00039386171669531737, -0.0003057784963053739, -0.00019394815931728573, -6.647037717816459e-05, 6.647037717816459e-05, 0.00019394815931728573, 0.0003057784963053739, 0.00039386171669531737, 0.00045314093505467907, 0.0004820197067465387, 0.00048220648603409215, 0.00045807311713585687, 0.00041570244858288915, 0.000361837556302355, 0.000302929786942714, 0.000244427141576528],
        },
        "minus_y90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, -0.0026000548393307343, -0.0057620867380027505, -0.009465048797290468, -0.013630876928171004, -0.018118104862180566, -0.022723471462668086, -0.027193187959653177, -0.031243897885979963, -0.03459137610093453, -0.036983127473497315] + [-0.038229763728452756] * 2 + [-0.036983127473497315, -0.03459137610093453, -0.031243897885979963, -0.027193187959653177, -0.022723471462668086, -0.018118104862180566, -0.013630876928171004, -0.009465048797290468, -0.0057620867380027505, -0.0026000548393307343, 0.0],
        },
        "readout_wf_q5": {
            "type": "constant",
            "sample": 0.131,
        },
        "gft_cz_wf_1_2_q2": {
            "type": "arbitrary",
            "samples": [2.4584008754312155e-06, 3.785965707138443e-05, 0.00039450668590304175, 0.0027815429979183397, 0.01326999947723866, 0.04283608303386536, 0.09356260729473384, 0.13827656985454806] + [0.14519591] * 8 + [0.13827656985454806, 0.09356260729473384, 0.04283608303386536, 0.01326999947723866, 0.0027815429979183397, 0.00039450668590304175, 3.785965707138443e-05, 2.4584008754312155e-06],
        },
        "g_cz_wf_1_2_q2": {
            "type": "arbitrary",
            "samples": [0.043105405973438204, 0.06676295880658584, 0.09713953187809103, 0.1327739977588363, 0.17048518779758703, 0.20564439059966616, 0.2330256230898819] + [0.24805448456506088] * 2 + [0.2330256230898819, 0.20564439059966616, 0.17048518779758703, 0.1327739977588363, 0.09713953187809103, 0.06676295880658584, 0.043105405973438204],
        },
        "cz_4c5t_wf": {
            "type": "arbitrary",
            "samples": [0.0] + [0.194652068517] * 27,
        },
        "cz_3c4t_wf": {
            "type": "arbitrary",
            "samples": [0.0] + [0.1591175284349345] * 47,
        },
        "cz_3c2t_wf": {
            "type": "arbitrary",
            "samples": [0.0] + [0.2687859507460096] * 51,
        },
        "cz_2c3t_wf": {
            "type": "arbitrary",
            "samples": [0.0] + [0.015] * 31,
        },
        "cz_2c1t_wf": {
            "type": "arbitrary",
            "samples": [0.0] + [-0.13840394169773318] * 23,
        },
    },
    "digital_waveforms": {
        "ON": {
            "samples": [(1, 0)],
        },
    },
    "integration_weights": {
        "cosine_weights": {
            "cosine": [(1.0, 1800)],
            "sine": [(0.0, 1800)],
        },
        "sine_weights": {
            "cosine": [(0.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "minus_sine_weights": {
            "cosine": [(0.0, 1800)],
            "sine": [(-1.0, 1800)],
        },
        "rotated_cosine_weights_q1": {
            "cosine": [(-0.1581580672544845, 1800)],
            "sine": [(-0.9874138067509113, 1800)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(0.9874138067509113, 1800)],
            "sine": [(-0.1581580672544845, 1800)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(-0.9874138067509113, 1800)],
            "sine": [(0.1581580672544845, 1800)],
        },
        "rotated_cosine_weights_q2": {
            "cosine": [(-0.335451569750255, 1800)],
            "sine": [(0.9420574527872967, 1800)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(-0.9420574527872967, 1800)],
            "sine": [(-0.335451569750255, 1800)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(0.9420574527872967, 1800)],
            "sine": [(0.335451569750255, 1800)],
        },
        "rotated_cosine_weights_q3": {
            "cosine": [(-0.6691306063588585, 1800)],
            "sine": [(0.743144825477394, 1800)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(-0.743144825477394, 1800)],
            "sine": [(-0.6691306063588585, 1800)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(0.743144825477394, 1800)],
            "sine": [(0.6691306063588585, 1800)],
        },
        "rotated_cosine_weights_q4": {
            "cosine": [(-0.061048539534856804, 1800)],
            "sine": [(-0.998134798421867, 1800)],
        },
        "rotated_sine_weights_q4": {
            "cosine": [(0.998134798421867, 1800)],
            "sine": [(-0.061048539534856804, 1800)],
        },
        "rotated_minus_sine_weights_q4": {
            "cosine": [(-0.998134798421867, 1800)],
            "sine": [(0.061048539534856804, 1800)],
        },
        "rotated_cosine_weights_q5": {
            "cosine": [(-0.9258705848099948, 1800)],
            "sine": [(-0.3778407868184669, 1800)],
        },
        "rotated_sine_weights_q5": {
            "cosine": [(0.3778407868184669, 1800)],
            "sine": [(-0.9258705848099948, 1800)],
        },
        "rotated_minus_sine_weights_q5": {
            "cosine": [(-0.3778407868184669, 1800)],
            "sine": [(0.9258705848099948, 1800)],
        },
        "opt_cosine_weights_q1": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_sine_weights_q1": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_minus_sine_weights_q1": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_cosine_weights_q2": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_sine_weights_q2": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_minus_sine_weights_q2": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_cosine_weights_q3": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_sine_weights_q3": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_minus_sine_weights_q3": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_cosine_weights_q4": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_sine_weights_q4": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_minus_sine_weights_q4": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_cosine_weights_q5": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_sine_weights_q5": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_minus_sine_weights_q5": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
    },
    "mixers": {
        "octave_octave1_2": [
            {'intermediate_frequency': -346063000, 'lo_frequency': 3670000000, 'correction': [1.139035176485777, 0.16698597371578217, 0.19680260121822357, 0.9664653651416302]},
            {'intermediate_frequency': -130602000, 'lo_frequency': 3200000000, 'correction': [0.9145237021148205, 0.06326756626367569, 0.051882900297641754, 1.1151976510882378]},
            {'intermediate_frequency': -131046000, 'lo_frequency': 3200000000, 'correction': [0.8735883422195911, 0.07953835651278496, 0.05841812118887901, 1.1894216872751713]},
            {'intermediate_frequency': -131211000, 'lo_frequency': 3200000000, 'correction': [0.9102895632386208, 0.06404534727334976, 0.05197123438119888, 1.12177075445652]},
            {'intermediate_frequency': -131239000, 'lo_frequency': 3200000000, 'correction': [0.8902681805193424, 0.07561632618308067, 0.05812149867415428, 1.1582427732646465]},
            {'intermediate_frequency': -131235000, 'lo_frequency': 3200000000, 'correction': [0.9070513471961021, 0.06460833549499512, 0.05200457572937012, 1.12688310444355]},
            {'intermediate_frequency': -131392000, 'lo_frequency': 3200000000, 'correction': [0.9075584001839161, 0.06511697918176651, 0.05247024446725845, 1.1263042837381363]},
            {'intermediate_frequency': -131416000, 'lo_frequency': 3200000000, 'correction': [0.9092047810554504, 0.064693134278059, 0.05234674736857414, 1.1236477829515934]},
            {'intermediate_frequency': -131158000, 'lo_frequency': 3200000000, 'correction': [0.9102209247648716, 0.06425825506448746, 0.05213155597448349, 1.121954008936882]},
            {'intermediate_frequency': -135838000, 'lo_frequency': 3200000000, 'correction': [0.90909468755126, 0.06442656740546227, 0.05212172493338585, 1.1237128004431725]},
            {'intermediate_frequency': -135236000, 'lo_frequency': 3200000000, 'correction': [0.9105560258030891, 0.06402204185724258, 0.0519864484667778, 1.1213625334203243]},
            {'intermediate_frequency': -131126000, 'lo_frequency': 3200000000, 'correction': [0.9128555990755558, 0.06409711018204689, 0.05233735218644142, 1.1179664805531502]},
            {'intermediate_frequency': -131407000, 'lo_frequency': 3200000000, 'correction': [0.9095721393823624, 0.06452245637774467, 0.05225850269198418, 1.1230292730033398]},
            {'intermediate_frequency': -124539000, 'lo_frequency': 3200000000, 'correction': [0.907289020717144, 0.06597277894616127, 0.053109172731637955, 1.1270440630614758]},
            {'intermediate_frequency': -124637000, 'lo_frequency': 3200000000, 'correction': [0.9103271849453449, 0.06431788206100464, 0.05219238996505737, 1.1218171119689941]},
        ],
        "octave_octave1_3": [
            {'intermediate_frequency': 471832000, 'lo_frequency': 3670000000, 'correction': [1.0509245730936527, 0.1871345043182373, 0.1878669261932373, 1.0468274168670177]},
            {'intermediate_frequency': -261857000, 'lo_frequency': 3200000000, 'correction': [0.8728884682059288, -0.00466681644320488, -0.003476236015558243, 1.1718457750976086]},
            {'intermediate_frequency': -262513000, 'lo_frequency': 3200000000, 'correction': [0.8368789926171303, 0.003159593790769577, 0.0021197572350502014, 1.247405406087637]},
            {'intermediate_frequency': -262884000, 'lo_frequency': 3200000000, 'correction': [0.869447585195303, -0.0047644078731536865, -0.0035155974328517914, 1.1782930493354797]},
            {'intermediate_frequency': -262526000, 'lo_frequency': 3200000000, 'correction': [0.8509256765246391, 0.0001483820378780365, 0.00010387226939201355, 1.2155497074127197]},
            {'intermediate_frequency': -262792000, 'lo_frequency': 3200000000, 'correction': [0.8665041476488113, -0.003685157746076584, -0.0026972107589244843, 1.1838915720582008]},
            {'intermediate_frequency': -262349000, 'lo_frequency': 3200000000, 'correction': [0.8670051544904709, -0.003754355013370514, -0.002751685678958893, 1.1829278953373432]},
            {'intermediate_frequency': -262383000, 'lo_frequency': 3200000000, 'correction': [0.8687931708991528, -0.004607435315847397, -0.003393646329641342, 1.1795302629470825]},
            {'intermediate_frequency': -262114000, 'lo_frequency': 3200000000, 'correction': [0.868685033172369, -0.004248201847076416, -0.003128141164779663, 1.1797262392938137]},
            {'intermediate_frequency': -269833000, 'lo_frequency': 3200000000, 'correction': [0.8694386668503284, -0.007623564451932907, -0.005624677985906601, 1.1784180253744125]},
            {'intermediate_frequency': -266474000, 'lo_frequency': 3200000000, 'correction': [0.8699318952858448, -0.006611298769712448, -0.004884641617536545, 1.17744155600667]},
            {'intermediate_frequency': -207105000, 'lo_frequency': 3200000000, 'correction': [0.884800311177969, -0.014048315584659576, -0.010798372328281403, 1.1510951593518257]},
            {'intermediate_frequency': -207068000, 'lo_frequency': 3200000000, 'correction': [0.886374693363905, -0.014085430651903152, -0.010871652513742447, 1.1483967043459415]},
            {'intermediate_frequency': -208140000, 'lo_frequency': 3200000000, 'correction': [0.8805629462003708, -0.013572819530963898, -0.01031697541475296, 1.1584521941840649]},
            {'intermediate_frequency': -206772000, 'lo_frequency': 3200000000, 'correction': [0.882083285599947, -0.012483000755310059, -0.009527675807476044, 1.155690737068653]},
            {'intermediate_frequency': -195512000, 'lo_frequency': 3200000000, 'correction': [0.8857291266322136, -0.007012851536273956, -0.005405761301517487, 1.1490495018661022]},
            {'intermediate_frequency': -197837000, 'lo_frequency': 3200000000, 'correction': [0.886171780526638, -0.009882315993309021, -0.007625512778759003, 1.148438461124897]},
        ],
        "octave_octave1_4": [
            {'intermediate_frequency': -106551000, 'lo_frequency': 3960000000, 'correction': [1.3551864996552467, -0.023040927946567535, -0.038992561399936676, 0.8007874302566051]},
            {'intermediate_frequency': -106458000, 'lo_frequency': 3960000000, 'correction': [1.2996150106191635, -0.023949556052684784, -0.038025788962841034, 0.818528775125742]},
            {'intermediate_frequency': -106481000, 'lo_frequency': 3960000000, 'correction': [1.3489361219108105, -0.02309318631887436, -0.03881271928548813, 0.8026037104427814]},
            {'intermediate_frequency': -106486000, 'lo_frequency': 3960000000, 'correction': [1.3209210634231567, -0.024531234055757523, -0.039934027940034866, 0.8114338889718056]},
            {'intermediate_frequency': -106443000, 'lo_frequency': 3960000000, 'correction': [1.3447312489151955, -0.02273653820157051, -0.03803752735257149, 0.8037991337478161]},
            {'intermediate_frequency': -106377000, 'lo_frequency': 3960000000, 'correction': [1.3451869115233421, -0.021947916597127914, -0.036741312593221664, 0.8035654686391354]},
            {'intermediate_frequency': -106405000, 'lo_frequency': 3960000000, 'correction': [1.3458872437477112, -0.021549977362155914, -0.036105431616306305, 0.8033095933496952]},
            {'intermediate_frequency': -106395000, 'lo_frequency': 3960000000, 'correction': [1.3420724086463451, -0.02118780091404915, -0.03534986451268196, 0.8044037185609341]},
            {'intermediate_frequency': -109030000, 'lo_frequency': 3960000000, 'correction': [1.3440575115382671, -0.021957125514745712, -0.0367104671895504, 0.803902555257082]},
            {'intermediate_frequency': -158909000, 'lo_frequency': 3960000000, 'correction': [1.3499786704778671, -0.050194740295410156, -0.08388614654541016, 0.807783305644989]},
            {'intermediate_frequency': -99150000, 'lo_frequency': 3960000000, 'correction': [1.339694682508707, -0.020223990082740784, -0.033656731247901917, 0.8050089813768864]},
            {'intermediate_frequency': -99223000, 'lo_frequency': 3960000000, 'correction': [1.3419710472226143, -0.020403068512678146, -0.03404061123728752, 0.8043429665267467]},
            {'intermediate_frequency': -99228000, 'lo_frequency': 3960000000, 'correction': [1.3357893414795399, -0.020450826734304428, -0.03388380631804466, 0.8062256798148155]},
            {'intermediate_frequency': -99092000, 'lo_frequency': 3960000000, 'correction': [1.335228979587555, -0.02045520767569542, -0.03386959061026573, 0.8063984476029873]},
            {'intermediate_frequency': -100534000, 'lo_frequency': 3960000000, 'correction': [1.3411707878112793, -0.02001633495092392, -0.03336729854345322, 0.8045399077236652]},
            {'intermediate_frequency': -132534000, 'lo_frequency': 3960000000, 'correction': [1.3550899401307106, -0.03831326216459274, -0.06462227553129196, 0.8034058660268784]},
            {'intermediate_frequency': -138111000, 'lo_frequency': 3960000000, 'correction': [1.354216042906046, -0.0438227653503418, -0.0737299919128418, 0.8049030043184757]},
        ],
        "octave_octave1_5": [
            {'intermediate_frequency': -368712000, 'lo_frequency': 3960000000, 'correction': [1.5205974765121937, -0.035888671875, -0.071044921875, 0.7681368701159954]},
            {'intermediate_frequency': -368884000, 'lo_frequency': 3960000000, 'correction': [1.3623402081429958, -0.024932861328125, -0.042510986328125, 0.7990179099142551]},
            {'intermediate_frequency': -368950000, 'lo_frequency': 3960000000, 'correction': [1.4819180443882942, -0.02796586975455284, -0.053621333092451096, 0.772885050624609]},
            {'intermediate_frequency': -368836000, 'lo_frequency': 3960000000, 'correction': [1.4405015744268894, -0.036540985107421875, -0.06730270385742188, 0.7820985391736031]},
            {'intermediate_frequency': -368583000, 'lo_frequency': 3960000000, 'correction': [1.4771419242024422, -0.02573089674115181, -0.04914436861872673, 0.7733985595405102]},
            {'intermediate_frequency': -368508000, 'lo_frequency': 3960000000, 'correction': [1.464051179587841, -0.024200439453125, -0.045684814453125, 0.7755461484193802]},
            {'intermediate_frequency': -368530000, 'lo_frequency': 3960000000, 'correction': [1.4773151688277721, -0.024126052856445312, -0.04609870910644531, 0.7731622979044914]},
            {'intermediate_frequency': -368885000, 'lo_frequency': 3960000000, 'correction': [1.4773151688277721, -0.024126052856445312, -0.04609870910644531, 0.7731622979044914]},
            {'intermediate_frequency': -368843000, 'lo_frequency': 3960000000, 'correction': [1.47405668720603, -0.02565453201532364, -0.048862673342227936, 0.7739288546144962]},
            {'intermediate_frequency': -371061000, 'lo_frequency': 3960000000, 'correction': [1.464051179587841, -0.024200439453125, -0.045684814453125, 0.7755461484193802]},
            {'intermediate_frequency': -251555000, 'lo_frequency': 3960000000, 'correction': [1.3939951211214066, 0.012137506157159805, 0.021433237940073013, 0.7894106432795525]},
            {'intermediate_frequency': -368097000, 'lo_frequency': 3960000000, 'correction': [1.464051179587841, -0.024200439453125, -0.045684814453125, 0.7755461484193802]},
            {'intermediate_frequency': -364122000, 'lo_frequency': 3960000000, 'correction': [1.4679120182991028, -0.01510683074593544, -0.02865377441048622, 0.7739119343459606]},
            {'intermediate_frequency': -364152000, 'lo_frequency': 3960000000, 'correction': [1.4631172642111778, -0.01815032958984375, -0.03426361083984375, 0.7750514298677444]},
            {'intermediate_frequency': -364128000, 'lo_frequency': 3960000000, 'correction': [1.4631172642111778, -0.01815032958984375, -0.03426361083984375, 0.7750514298677444]},
            {'intermediate_frequency': -364103000, 'lo_frequency': 3960000000, 'correction': [1.4631172642111778, -0.01815032958984375, -0.03426361083984375, 0.7750514298677444]},
            {'intermediate_frequency': -365006000, 'lo_frequency': 3960000000, 'correction': [1.4674560204148293, -0.016525495797395706, -0.03132681921124458, 0.7741110809147358]},
            {'intermediate_frequency': -368831000, 'lo_frequency': 3960000000, 'correction': [1.4697413854300976, -0.02643631398677826, -0.050147637724876404, 0.7748030871152878]},
            {'intermediate_frequency': -368481000, 'lo_frequency': 3960000000, 'correction': [1.4695789776742458, -0.02719360962510109, -0.05156952515244484, 0.7749374620616436]},
        ],
        "octave_octave2_1": [
            {'intermediate_frequency': -122859000, 'lo_frequency': 4600000000, 'correction': [1.255867786705494, -0.0473419725894928, -0.0707947313785553, 0.8398260287940502]},
            {'intermediate_frequency': -122900000, 'lo_frequency': 4600000000, 'correction': [1.253316655755043, -0.04247363284230232, -0.06340106204152107, 0.8396217599511147]},
            {'intermediate_frequency': -122911000, 'lo_frequency': 4600000000, 'correction': [1.2556648589670658, -0.046525731682777405, -0.06957413256168365, 0.8396903276443481]},
            {'intermediate_frequency': -122888000, 'lo_frequency': 4600000000, 'correction': [1.2544812224805355, -0.04737443849444389, -0.07071657106280327, 0.84040192887187]},
            {'intermediate_frequency': -122908000, 'lo_frequency': 4600000000, 'correction': [1.2530965767800808, -0.047407008707523346, -0.0706385150551796, 0.8409797437489033]},
            {'intermediate_frequency': -122891000, 'lo_frequency': 4600000000, 'correction': [1.2526950538158417, -0.045772284269332886, -0.06820270419120789, 0.840710274875164]},
            {'intermediate_frequency': -122906000, 'lo_frequency': 4600000000, 'correction': [1.2526950538158417, -0.045772284269332886, -0.06820270419120789, 0.840710274875164]},
            {'intermediate_frequency': -122907000, 'lo_frequency': 4600000000, 'correction': [1.2523072995245457, -0.044137559831142426, -0.06576689332723618, 0.840450044721365]},
            {'intermediate_frequency': -128097000, 'lo_frequency': 4600000000, 'correction': [1.2526950538158417, -0.045772284269332886, -0.06820270419120789, 0.840710274875164]},
            {'intermediate_frequency': -128279000, 'lo_frequency': 4600000000, 'correction': [1.2526530660688877, -0.04412997141480446, -0.06578505411744118, 0.8403054997324944]},
            {'intermediate_frequency': -128741000, 'lo_frequency': 4600000000, 'correction': [1.2523072995245457, -0.044137559831142426, -0.06576689332723618, 0.840450044721365]},
            {'intermediate_frequency': -128925000, 'lo_frequency': 4600000000, 'correction': [1.2523072995245457, -0.044137559831142426, -0.06576689332723618, 0.840450044721365]},
            {'intermediate_frequency': -129200000, 'lo_frequency': 4600000000, 'correction': [1.2523072995245457, -0.044137559831142426, -0.06576689332723618, 0.840450044721365]},
            {'intermediate_frequency': -126767000, 'lo_frequency': 4600000000, 'correction': [1.2523072995245457, -0.044137559831142426, -0.06576689332723618, 0.840450044721365]},
            {'intermediate_frequency': -127400000, 'lo_frequency': 4600000000, 'correction': [1.2523072995245457, -0.044137559831142426, -0.06576689332723618, 0.840450044721365]},
            {'intermediate_frequency': -131436000, 'lo_frequency': 4600000000, 'correction': [1.2523072995245457, -0.044137559831142426, -0.06576689332723618, 0.840450044721365]},
        ],
        "octave_octave1_1": [
            {'intermediate_frequency': -157000000, 'lo_frequency': 5900000000, 'correction': [1.0789089314639568, -0.13434219360351562, -0.14752578735351562, 0.9824925884604454]},
            {'intermediate_frequency': 136800000, 'lo_frequency': 5900000000, 'correction': [1.096462655812502, -0.1716594696044922, -0.1885051727294922, 0.9984776265919209]},
            {'intermediate_frequency': -157100000, 'lo_frequency': 5900000000, 'correction': [1.0455858372151852, -0.090911865234375, -0.096771240234375, 0.9822769500315189]},
            {'intermediate_frequency': 136710000, 'lo_frequency': 5900000000, 'correction': [1.0058116912841797, -0.0625, -0.0625, 1.0058116912841797]},
            {'intermediate_frequency': -38800000, 'lo_frequency': 5900000000, 'correction': [1.127538651227951, -0.1143798828125, -0.1378173828125, 0.935787171125412]},
            {'intermediate_frequency': 229500000, 'lo_frequency': 5900000000, 'correction': [1.06640625, 0.0, 0.0, 0.94140625]},
            {'intermediate_frequency': 36100000, 'lo_frequency': 5900000000, 'correction': [1.055631846189499, -0.1212158203125, -0.1290283203125, 0.9917146861553192]},
            {'intermediate_frequency': -157100000, 'lo_frequency': 5950000000, 'correction': [1.0032808110117912, -0.046875, -0.046875, 1.0032808110117912]},
            {'intermediate_frequency': 136710000, 'lo_frequency': 5950000000, 'correction': [0.9697265625, 0.0, 0.0, 1.0322265625]},
            {'intermediate_frequency': -38800000, 'lo_frequency': 5950000000, 'correction': [1.055631846189499, -0.1212158203125, -0.1290283203125, 0.9917146861553192]},
            {'intermediate_frequency': 229500000, 'lo_frequency': 5950000000, 'correction': [1.0322265625, 0.0, 0.0, 0.9697265625]},
            {'intermediate_frequency': 36100000, 'lo_frequency': 5950000000, 'correction': [1.0455858372151852, -0.090911865234375, -0.096771240234375, 0.9822769500315189]},
            {'intermediate_frequency': -157100000, 'lo_frequency': 5960000000, 'correction': [0.9697265625, 0.0, 0.0, 1.0322265625]},
            {'intermediate_frequency': 136710000, 'lo_frequency': 5960000000, 'correction': [1.0337355360388756, -0.030303955078125, -0.032257080078125, 0.9711441695690155]},
            {'intermediate_frequency': -38800000, 'lo_frequency': 5960000000, 'correction': [1.1564223431050777, -0.17156982421875, -0.20672607421875, 0.9597588442265987]},
            {'intermediate_frequency': 229500000, 'lo_frequency': 5960000000, 'correction': [1.0322265625, 0.0, 0.0, 0.9697265625]},
            {'intermediate_frequency': 36100000, 'lo_frequency': 5960000000, 'correction': [1.090586543083191, -0.11767578125, -0.13330078125, 0.9627522230148315]},
            {'intermediate_frequency': -237000000, 'lo_frequency': 5960000000, 'correction': [0.9900021366775036, 0.004639901220798492, 0.004546832293272018, 1.010266449302435]},
            {'intermediate_frequency': 54400000, 'lo_frequency': 5960000000, 'correction': [1.0382255427539349, -0.06060791015625, -0.06451416015625, 0.9753623120486736]},
            {'intermediate_frequency': -123500000, 'lo_frequency': 5960000000, 'correction': [1.0726038739085197, -0.058837890625, -0.066650390625, 0.9468774124979973]},
            {'intermediate_frequency': 142600000, 'lo_frequency': 5960000000, 'correction': [1.0855363868176937, -0.14926910400390625, -0.16391754150390625, 0.9885277822613716]},
            {'intermediate_frequency': -50200000, 'lo_frequency': 5960000000, 'correction': [1.0488719940185547, -0.1875, -0.1875, 1.0488719940185547]},
            {'intermediate_frequency': 54500000, 'lo_frequency': 5960000000, 'correction': [1.0828662104904652, -0.1535702347755432, -0.1673336625099182, 0.9937989488244057]},
            {'intermediate_frequency': -124000000, 'lo_frequency': 5960000000, 'correction': [1.1054573729634285, -0.17039823532104492, -0.19005155563354492, 0.9911415092647076]},
            {'intermediate_frequency': -50500000, 'lo_frequency': 5960000000, 'correction': [1.0967981033027172, -0.16761727631092072, -0.18478341400623322, 0.9949069954454899]},
            {'intermediate_frequency': -237000000, 'lo_frequency': 6000000000, 'correction': [1.0047452114522457, 0.04827943444252014, 0.0484004020690918, 1.0022340379655361]},
            {'intermediate_frequency': -163122000, 'lo_frequency': 5900000000, 'correction': [1.0789089314639568, -0.13434219360351562, -0.14752578735351562, 0.9824925884604454]},
            {'intermediate_frequency': 126410000, 'lo_frequency': 5900000000, 'correction': [1.096462655812502, -0.1716594696044922, -0.1885051727294922, 0.9984776265919209]},
            {'intermediate_frequency': -49753000, 'lo_frequency': 5900000000, 'correction': [1.0886195003986359, -0.15085554867982864, -0.1663050726056099, 0.9874881729483604]},
            {'intermediate_frequency': 218194000, 'lo_frequency': 5900000000, 'correction': [1.1093690656125546, -0.17780685424804688, -0.19831466674804688, 0.9946486912667751]},
            {'intermediate_frequency': 28632000, 'lo_frequency': 5900000000, 'correction': [1.089952491223812, -0.1585984230041504, -0.1741623878479004, 0.9925492443144321]},
            {'intermediate_frequency': -163272000, 'lo_frequency': 5900000000, 'correction': [1.0789089314639568, -0.13434219360351562, -0.14752578735351562, 0.9824925884604454]},
            {'intermediate_frequency': 126110000, 'lo_frequency': 5900000000, 'correction': [1.096462655812502, -0.1716594696044922, -0.1885051727294922, 0.9984776265919209]},
            {'intermediate_frequency': -50303000, 'lo_frequency': 5900000000, 'correction': [1.0855363868176937, -0.14926910400390625, -0.16391754150390625, 0.9885277822613716]},
            {'intermediate_frequency': 217644000, 'lo_frequency': 5900000000, 'correction': [1.1093690656125546, -0.17780685424804688, -0.19831466674804688, 0.9946486912667751]},
            {'intermediate_frequency': 28031999, 'lo_frequency': 5900000000, 'correction': [1.089952491223812, -0.1585984230041504, -0.1741623878479004, 0.9925492443144321]},
            {'intermediate_frequency': 21500000, 'lo_frequency': 5880000000, 'correction': [1.0912747457623482, -0.156442791223526, -0.172464519739151, 0.9898967482149601]},
            {'intermediate_frequency': 129800000, 'lo_frequency': 5880000000, 'correction': [1.096462655812502, -0.1716594696044922, -0.1885051727294922, 0.9984776265919209]},
            {'intermediate_frequency': -28500000, 'lo_frequency': 5880000000, 'correction': [1.0908435992896557, -0.1505773365497589, -0.1666448414325714, 0.9856670163571835]},
            {'intermediate_frequency': 153000000, 'lo_frequency': 5880000000, 'correction': [1.1003425158560276, -0.1791229248046875, -0.1967010498046875, 1.002010766416788]},
            {'intermediate_frequency': 57900000, 'lo_frequency': 5880000000, 'correction': [1.0890531428158283, -0.15673255920410156, -0.17211341857910156, 0.9917302653193474]},
            {'intermediate_frequency': 34200000, 'lo_frequency': 5880000000, 'correction': [1.0930849835276604, -0.1601676195859909, -0.1765708178281784, 0.9915388189256191]},
            {'intermediate_frequency': 134400000, 'lo_frequency': 5880000000, 'correction': [1.1003425158560276, -0.1791229248046875, -0.1967010498046875, 1.002010766416788]},
            {'intermediate_frequency': -22200000, 'lo_frequency': 5880000000, 'correction': [1.0908435992896557, -0.1505773365497589, -0.1666448414325714, 0.9856670163571835]},
            {'intermediate_frequency': 157600000, 'lo_frequency': 5880000000, 'correction': [1.1003425158560276, -0.1791229248046875, -0.1967010498046875, 1.002010766416788]},
            {'intermediate_frequency': 63300000, 'lo_frequency': 5880000000, 'correction': [1.0926973298192024, -0.16419601440429688, -0.18030929565429688, 0.9950487911701202]},
            {'intermediate_frequency': 34300000, 'lo_frequency': 5880000000, 'correction': (1, 0, 0, 1)},
            {'intermediate_frequency': 158000000, 'lo_frequency': 5880000000, 'correction': (1, 0, 0, 1)},
        ],
    },
}

loaded_config = {
    "version": 1,
    "controllers": {
        "con1": {
            "type": "opx1",
            "analog_outputs": {
                "1": {
                    "offset": 0.01953125,
                    "delay": 0,
                    "shareable": False,
                },
                "2": {
                    "offset": -0.00244140625,
                    "delay": 0,
                    "shareable": False,
                },
                "3": {
                    "offset": -0.00183868408203125,
                    "delay": 0,
                    "shareable": False,
                },
                "4": {
                    "offset": 0.01373291015625,
                    "delay": 0,
                    "shareable": False,
                },
                "5": {
                    "offset": -0.014556884765625,
                    "delay": 0,
                    "shareable": False,
                },
                "6": {
                    "offset": 0.01129150390625,
                    "delay": 0,
                    "shareable": False,
                },
                "7": {
                    "offset": 0.0161895751953125,
                    "delay": 0,
                    "shareable": False,
                },
                "8": {
                    "offset": -0.0023956298828125,
                    "delay": 0,
                    "shareable": False,
                },
                "9": {
                    "offset": 0.0078125,
                    "delay": 0,
                    "shareable": False,
                },
                "10": {
                    "offset": -0.0123291015625,
                    "delay": 0,
                    "shareable": False,
                },
            },
            "analog_inputs": {
                "1": {
                    "offset": 0.006487780227661133,
                    "gain_db": 0,
                    "shareable": False,
                },
                "2": {
                    "offset": 0.004683707580566406,
                    "gain_db": 0,
                    "shareable": False,
                },
            },
            "digital_outputs": {
                "1": {
                    "shareable": False,
                    "inverted": False,
                },
                "3": {
                    "shareable": False,
                    "inverted": False,
                },
                "5": {
                    "shareable": False,
                    "inverted": False,
                },
                "7": {
                    "shareable": False,
                    "inverted": False,
                },
                "10": {
                    "shareable": False,
                    "inverted": False,
                },
            },
        },
        "con2": {
            "type": "opx1",
            "analog_outputs": {
                "1": {
                    "offset": -0.03914642333984375,
                    "delay": 0,
                    "shareable": False,
                },
                "2": {
                    "offset": -0.0126953125,
                    "delay": 0,
                    "shareable": False,
                },
                "3": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                },
                "4": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                },
                "5": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "6": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "7": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "8": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "9": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                    "filter": {
                        "feedforward": [1.06569937, -0.98851684],
                        "feedback": [0.92281746],
                    },
                },
                "10": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                },
            },
            "analog_inputs": {
                "1": {
                    "offset": 0.0,
                    "gain_db": 0,
                    "shareable": False,
                },
                "2": {
                    "offset": 0.0,
                    "gain_db": 0,
                    "shareable": False,
                },
            },
            "digital_outputs": {
                "1": {
                    "shareable": False,
                    "inverted": False,
                },
                "3": {
                    "shareable": False,
                    "inverted": False,
                },
            },
        },
    },
    "oscillators": {},
    "elements": {
        "rr1": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "outputs": {
                "out1": ('con1', 1),
                "out2": ('con1', 2),
            },
            "time_of_flight": 284,
            "smearing": 0,
            "intermediate_frequency": 34300000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q1",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "octave_octave1_1",
                "lo_frequency": 5880000000.0,
            },
        },
        "rr2": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "outputs": {
                "out1": ('con1', 1),
                "out2": ('con1', 2),
            },
            "time_of_flight": 284,
            "smearing": 0,
            "intermediate_frequency": 134400000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q2",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "octave_octave1_1",
                "lo_frequency": 5880000000.0,
            },
        },
        "rr3": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "outputs": {
                "out1": ('con1', 1),
                "out2": ('con1', 2),
            },
            "time_of_flight": 284,
            "smearing": 0,
            "intermediate_frequency": 22200000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q3",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "octave_octave1_1",
                "lo_frequency": 5880000000.0,
            },
        },
        "rr4": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "outputs": {
                "out1": ('con1', 1),
                "out2": ('con1', 2),
            },
            "time_of_flight": 284,
            "smearing": 0,
            "intermediate_frequency": 158000000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q4",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "octave_octave1_1",
                "lo_frequency": 5880000000.0,
            },
        },
        "rr5": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "outputs": {
                "out1": ('con1', 1),
                "out2": ('con1', 2),
            },
            "time_of_flight": 284,
            "smearing": 0,
            "intermediate_frequency": 63300000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q5",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "octave_octave1_1",
                "lo_frequency": 5880000000.0,
            },
        },
        "q1_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": 124637000.0,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q1",
                "x90": "x90_pulse_q1",
                "-x90": "-x90_pulse_q1",
                "y90": "y90_pulse_q1",
                "y180": "y180_pulse_q1",
                "-y90": "-y90_pulse_q1",
            },
            "mixInputs": {
                "I": ('con1', 3),
                "Q": ('con1', 4),
                "mixer": "octave_octave1_2",
                "lo_frequency": 3200000000.0,
            },
        },
        "q2_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": 138111000.0,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q2",
                "x90": "x90_pulse_q2",
                "-x90": "-x90_pulse_q2",
                "y90": "y90_pulse_q2",
                "y180": "y180_pulse_q2",
                "-y90": "-y90_pulse_q2",
            },
            "mixInputs": {
                "I": ('con1', 7),
                "Q": ('con1', 8),
                "mixer": "octave_octave1_4",
                "lo_frequency": 3960000000.0,
            },
        },
        "q3_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": 197837000.0,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q3",
                "x90": "x90_pulse_q3",
                "-x90": "-x90_pulse_q3",
                "y90": "y90_pulse_q3",
                "y180": "y180_pulse_q3",
                "-y90": "-y90_pulse_q3",
            },
            "mixInputs": {
                "I": ('con1', 5),
                "Q": ('con1', 6),
                "mixer": "octave_octave1_3",
                "lo_frequency": 3200000000.0,
            },
        },
        "q4_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": 368481000.0,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q4",
                "x90": "x90_pulse_q4",
                "-x90": "-x90_pulse_q4",
                "y90": "y90_pulse_q4",
                "y180": "y180_pulse_q4",
                "-y90": "-y90_pulse_q4",
            },
            "mixInputs": {
                "I": ('con1', 9),
                "Q": ('con1', 10),
                "mixer": "octave_octave1_5",
                "lo_frequency": 3960000000.0,
            },
        },
        "q00_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": 368481000.0,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q4",
                "x90": "x90_pulse_q4",
                "-x90": "-x90_pulse_q4",
                "y90": "y90_pulse_q4",
                "y180": "y180_pulse_q4",
                "-y90": "-y90_pulse_q4",
            },
            "mixInputs": {
                "I": ('con1', 9),
                "Q": ('con1', 10),
                "mixer": "octave_octave1_5",
                "lo_frequency": 3960000000.0,
            },
        },
        "q5_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": 131436000.0,
            "operations": {
                "cw": "const_pulse",
                "saturation": "saturation_pulse",
                "x180": "x180_pulse_q5",
                "x90": "x90_pulse_q5",
                "-x90": "-x90_pulse_q5",
                "y90": "y90_pulse_q5",
                "y180": "y180_pulse_q5",
                "-y90": "-y90_pulse_q5",
            },
            "mixInputs": {
                "I": ('con2', 1),
                "Q": ('con2', 2),
                "mixer": "octave_octave2_1",
                "lo_frequency": 4600000000.0,
            },
        },
        "q1_z": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "operations": {
                "const": "const_flux_pulse",
                "cz_2c1t": "cz_2c1t_pulse",
            },
            "singleInput": {
                "port": ('con2', 5),
            },
        },
        "q2_z": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "operations": {
                "const": "const_flux_pulse",
                "cz_3c2t": "cz_3c2t_pulse",
                "cz_1_2": "gft_cz_pulse_1_2_q2",
            },
            "singleInput": {
                "port": ('con2', 6),
            },
        },
        "q3_z": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "operations": {
                "const": "const_flux_pulse",
                "cz_2c3t": "cz_2c3t_pulse",
            },
            "singleInput": {
                "port": ('con2', 7),
            },
        },
        "q4_z": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "operations": {
                "const": "const_flux_pulse",
                "cz_3c4t": "cz_3c4t_pulse",
            },
            "singleInput": {
                "port": ('con2', 8),
            },
        },
        "q5_z": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "operations": {
                "const": "const_flux_pulse",
                "cz_4c5t": "cz_4c5t_pulse",
            },
            "singleInput": {
                "port": ('con2', 9),
            },
        },
    },
    "pulses": {
        "const_flux_pulse": {
            "length": 200,
            "waveforms": {
                "single": "const_flux_wf",
            },
            "operation": "control",
        },
        "const_pulse": {
            "length": 100,
            "waveforms": {
                "I": "const_wf",
                "Q": "zero_wf",
            },
            "operation": "control",
        },
        "saturation_pulse": {
            "length": 1000,
            "waveforms": {
                "I": "saturation_wf",
                "Q": "zero_wf",
            },
            "operation": "control",
        },
        "cz_4c5t_pulse": {
            "length": 28,
            "waveforms": {
                "single": "cz_4c5t_wf",
            },
            "operation": "control",
        },
        "cz_3c4t_pulse": {
            "length": 48,
            "waveforms": {
                "single": "cz_3c4t_wf",
            },
            "operation": "control",
        },
        "cz_3c2t_pulse": {
            "length": 52,
            "waveforms": {
                "single": "cz_3c2t_wf",
            },
            "operation": "control",
        },
        "cz_2c3t_pulse": {
            "length": 32,
            "waveforms": {
                "single": "cz_2c3t_wf",
            },
            "operation": "control",
        },
        "cz_2c1t_pulse": {
            "length": 24,
            "waveforms": {
                "single": "cz_2c1t_wf",
            },
            "operation": "control",
        },
        "x90_pulse_q1": {
            "length": 24,
            "waveforms": {
                "I": "x90_I_wf_q1",
                "Q": "x90_Q_wf_q1",
            },
            "operation": "control",
        },
        "x180_pulse_q1": {
            "length": 24,
            "waveforms": {
                "I": "x180_I_wf_q1",
                "Q": "x180_Q_wf_q1",
            },
            "operation": "control",
        },
        "-x90_pulse_q1": {
            "length": 24,
            "waveforms": {
                "I": "minus_x90_I_wf_q1",
                "Q": "minus_x90_Q_wf_q1",
            },
            "operation": "control",
        },
        "y90_pulse_q1": {
            "length": 24,
            "waveforms": {
                "I": "y90_I_wf_q1",
                "Q": "y90_Q_wf_q1",
            },
            "operation": "control",
        },
        "y180_pulse_q1": {
            "length": 24,
            "waveforms": {
                "I": "y180_I_wf_q1",
                "Q": "y180_Q_wf_q1",
            },
            "operation": "control",
        },
        "-y90_pulse_q1": {
            "length": 24,
            "waveforms": {
                "I": "minus_y90_I_wf_q1",
                "Q": "minus_y90_Q_wf_q1",
            },
            "operation": "control",
        },
        "readout_pulse_q1": {
            "length": 1800,
            "waveforms": {
                "I": "readout_wf_q1",
                "Q": "zero_wf",
            },
            "digital_marker": "ON",
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q1",
                "rotated_sin": "rotated_sine_weights_q1",
                "rotated_minus_sin": "rotated_minus_sine_weights_q1",
                "opt_cos": "opt_cosine_weights_q1",
                "opt_sin": "opt_sine_weights_q1",
                "opt_minus_sin": "opt_minus_sine_weights_q1",
            },
            "operation": "measurement",
        },
        "x90_pulse_q2": {
            "length": 24,
            "waveforms": {
                "I": "x90_I_wf_q2",
                "Q": "x90_Q_wf_q2",
            },
            "operation": "control",
        },
        "x180_pulse_q2": {
            "length": 24,
            "waveforms": {
                "I": "x180_I_wf_q2",
                "Q": "x180_Q_wf_q2",
            },
            "operation": "control",
        },
        "-x90_pulse_q2": {
            "length": 24,
            "waveforms": {
                "I": "minus_x90_I_wf_q2",
                "Q": "minus_x90_Q_wf_q2",
            },
            "operation": "control",
        },
        "y90_pulse_q2": {
            "length": 24,
            "waveforms": {
                "I": "y90_I_wf_q2",
                "Q": "y90_Q_wf_q2",
            },
            "operation": "control",
        },
        "y180_pulse_q2": {
            "length": 24,
            "waveforms": {
                "I": "y180_I_wf_q2",
                "Q": "y180_Q_wf_q2",
            },
            "operation": "control",
        },
        "-y90_pulse_q2": {
            "length": 24,
            "waveforms": {
                "I": "minus_y90_I_wf_q2",
                "Q": "minus_y90_Q_wf_q2",
            },
            "operation": "control",
        },
        "readout_pulse_q2": {
            "length": 1800,
            "waveforms": {
                "I": "readout_wf_q2",
                "Q": "zero_wf",
            },
            "digital_marker": "ON",
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q2",
                "rotated_sin": "rotated_sine_weights_q2",
                "rotated_minus_sin": "rotated_minus_sine_weights_q2",
                "opt_cos": "opt_cosine_weights_q2",
                "opt_sin": "opt_sine_weights_q2",
                "opt_minus_sin": "opt_minus_sine_weights_q2",
            },
            "operation": "measurement",
        },
        "x90_pulse_q3": {
            "length": 24,
            "waveforms": {
                "I": "x90_I_wf_q3",
                "Q": "x90_Q_wf_q3",
            },
            "operation": "control",
        },
        "x180_pulse_q3": {
            "length": 24,
            "waveforms": {
                "I": "x180_I_wf_q3",
                "Q": "x180_Q_wf_q3",
            },
            "operation": "control",
        },
        "-x90_pulse_q3": {
            "length": 24,
            "waveforms": {
                "I": "minus_x90_I_wf_q3",
                "Q": "minus_x90_Q_wf_q3",
            },
            "operation": "control",
        },
        "y90_pulse_q3": {
            "length": 24,
            "waveforms": {
                "I": "y90_I_wf_q3",
                "Q": "y90_Q_wf_q3",
            },
            "operation": "control",
        },
        "y180_pulse_q3": {
            "length": 24,
            "waveforms": {
                "I": "y180_I_wf_q3",
                "Q": "y180_Q_wf_q3",
            },
            "operation": "control",
        },
        "-y90_pulse_q3": {
            "length": 24,
            "waveforms": {
                "I": "minus_y90_I_wf_q3",
                "Q": "minus_y90_Q_wf_q3",
            },
            "operation": "control",
        },
        "readout_pulse_q3": {
            "length": 1800,
            "waveforms": {
                "I": "readout_wf_q3",
                "Q": "zero_wf",
            },
            "digital_marker": "ON",
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q3",
                "rotated_sin": "rotated_sine_weights_q3",
                "rotated_minus_sin": "rotated_minus_sine_weights_q3",
                "opt_cos": "opt_cosine_weights_q3",
                "opt_sin": "opt_sine_weights_q3",
                "opt_minus_sin": "opt_minus_sine_weights_q3",
            },
            "operation": "measurement",
        },
        "x90_pulse_q4": {
            "length": 24,
            "waveforms": {
                "I": "x90_I_wf_q4",
                "Q": "x90_Q_wf_q4",
            },
            "operation": "control",
        },
        "x180_pulse_q4": {
            "length": 24,
            "waveforms": {
                "I": "x180_I_wf_q4",
                "Q": "x180_Q_wf_q4",
            },
            "operation": "control",
        },
        "-x90_pulse_q4": {
            "length": 24,
            "waveforms": {
                "I": "minus_x90_I_wf_q4",
                "Q": "minus_x90_Q_wf_q4",
            },
            "operation": "control",
        },
        "y90_pulse_q4": {
            "length": 24,
            "waveforms": {
                "I": "y90_I_wf_q4",
                "Q": "y90_Q_wf_q4",
            },
            "operation": "control",
        },
        "y180_pulse_q4": {
            "length": 24,
            "waveforms": {
                "I": "y180_I_wf_q4",
                "Q": "y180_Q_wf_q4",
            },
            "operation": "control",
        },
        "-y90_pulse_q4": {
            "length": 24,
            "waveforms": {
                "I": "minus_y90_I_wf_q4",
                "Q": "minus_y90_Q_wf_q4",
            },
            "operation": "control",
        },
        "readout_pulse_q4": {
            "length": 1800,
            "waveforms": {
                "I": "readout_wf_q4",
                "Q": "zero_wf",
            },
            "digital_marker": "ON",
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q4",
                "rotated_sin": "rotated_sine_weights_q4",
                "rotated_minus_sin": "rotated_minus_sine_weights_q4",
                "opt_cos": "opt_cosine_weights_q4",
                "opt_sin": "opt_sine_weights_q4",
                "opt_minus_sin": "opt_minus_sine_weights_q4",
            },
            "operation": "measurement",
        },
        "x90_pulse_q5": {
            "length": 24,
            "waveforms": {
                "I": "x90_I_wf_q5",
                "Q": "x90_Q_wf_q5",
            },
            "operation": "control",
        },
        "x180_pulse_q5": {
            "length": 24,
            "waveforms": {
                "I": "x180_I_wf_q5",
                "Q": "x180_Q_wf_q5",
            },
            "operation": "control",
        },
        "-x90_pulse_q5": {
            "length": 24,
            "waveforms": {
                "I": "minus_x90_I_wf_q5",
                "Q": "minus_x90_Q_wf_q5",
            },
            "operation": "control",
        },
        "y90_pulse_q5": {
            "length": 24,
            "waveforms": {
                "I": "y90_I_wf_q5",
                "Q": "y90_Q_wf_q5",
            },
            "operation": "control",
        },
        "y180_pulse_q5": {
            "length": 24,
            "waveforms": {
                "I": "y180_I_wf_q5",
                "Q": "y180_Q_wf_q5",
            },
            "operation": "control",
        },
        "-y90_pulse_q5": {
            "length": 24,
            "waveforms": {
                "I": "minus_y90_I_wf_q5",
                "Q": "minus_y90_Q_wf_q5",
            },
            "operation": "control",
        },
        "readout_pulse_q5": {
            "length": 1800,
            "waveforms": {
                "I": "readout_wf_q5",
                "Q": "zero_wf",
            },
            "digital_marker": "ON",
            "integration_weights": {
                "cos": "cosine_weights",
                "sin": "sine_weights",
                "minus_sin": "minus_sine_weights",
                "rotated_cos": "rotated_cosine_weights_q5",
                "rotated_sin": "rotated_sine_weights_q5",
                "rotated_minus_sin": "rotated_minus_sine_weights_q5",
                "opt_cos": "opt_cosine_weights_q5",
                "opt_sin": "opt_sine_weights_q5",
                "opt_minus_sin": "opt_minus_sine_weights_q5",
            },
            "operation": "measurement",
        },
        "gft_cz_pulse_1_2_q2": {
            "length": 24,
            "waveforms": {
                "single": "gft_cz_wf_1_2_q2",
            },
            "operation": "control",
        },
        "g_cz_pulse_1_2_q2": {
            "length": 16,
            "waveforms": {
                "single": "g_cz_wf_1_2_q2",
            },
            "operation": "control",
        },
    },
    "waveforms": {
        "const_wf": {
            "sample": 0.27,
            "type": "constant",
        },
        "saturation_wf": {
            "sample": 0.27,
            "type": "constant",
        },
        "const_flux_wf": {
            "sample": 0.48,
            "type": "constant",
        },
        "zero_wf": {
            "sample": 0.0,
            "type": "constant",
        },
        "x90_I_wf_q1": {
            "samples": [0.0, 0.0007544496482014039, 0.0016719663934131246, 0.0027464431239315745, 0.003955228231179286, 0.005257272897700412, 0.006593597485558204, 0.007890560914059744, 0.009065942537806505, 0.010037269651154779, 0.010731276544516957] + [0.011093009024062787] * 2 + [0.010731276544516957, 0.010037269651154779, 0.009065942537806505, 0.007890560914059744, 0.006593597485558204, 0.005257272897700412, 0.003955228231179286, 0.0027464431239315745, 0.0016719663934131246, 0.0007544496482014039, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q1": {
            "samples": [-0.0004843311170773316, -0.0006002538063475515, -0.0007169792467158665, -0.0008237122522291399, -0.0009076695128639909, -0.0009554896585398429, -0.0009551195563474098, -0.0008978964195749315, -0.0007804349549344685, -0.0006058985092187082, -0.0003843072747623774, -0.00013171070865373793, 0.00013171070865373793, 0.0003843072747623774, 0.0006058985092187082, 0.0007804349549344685, 0.0008978964195749315, 0.0009551195563474098, 0.0009554896585398429, 0.0009076695128639909, 0.0008237122522291399, 0.0007169792467158665, 0.0006002538063475515, 0.0004843311170773316],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q1": {
            "samples": [0.0, 0.0015088992964028079, 0.003343932786826249, 0.005492886247863149, 0.007910456462358571, 0.010514545795400823, 0.013187194971116409, 0.01578112182811949, 0.01813188507561301, 0.020074539302309558, 0.021462553089033914] + [0.022186018048125575] * 2 + [0.021462553089033914, 0.020074539302309558, 0.01813188507561301, 0.01578112182811949, 0.013187194971116409, 0.010514545795400823, 0.007910456462358571, 0.005492886247863149, 0.003343932786826249, 0.0015088992964028079, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q1": {
            "samples": [-0.0009686622341546632, -0.001200507612695103, -0.001433958493431733, -0.0016474245044582798, -0.0018153390257279818, -0.0019109793170796858, -0.0019102391126948196, -0.001795792839149863, -0.001560869909868937, -0.0012117970184374164, -0.0007686145495247548, -0.00026342141730747586, 0.00026342141730747586, 0.0007686145495247548, 0.0012117970184374164, 0.001560869909868937, 0.001795792839149863, 0.0019102391126948196, 0.0019109793170796858, 0.0018153390257279818, 0.0016474245044582798, 0.001433958493431733, 0.001200507612695103, 0.0009686622341546632],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q1": {
            "samples": [0.0, -0.0007544496482014039, -0.0016719663934131246, -0.0027464431239315745, -0.003955228231179286, -0.005257272897700412, -0.006593597485558204, -0.007890560914059744, -0.009065942537806505, -0.010037269651154779, -0.010731276544516957] + [-0.011093009024062787] * 2 + [-0.010731276544516957, -0.010037269651154779, -0.009065942537806505, -0.007890560914059744, -0.006593597485558204, -0.005257272897700412, -0.003955228231179286, -0.0027464431239315745, -0.0016719663934131246, -0.0007544496482014039, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q1": {
            "samples": [0.0004843311170773316, 0.0006002538063475515, 0.0007169792467158665, 0.0008237122522291399, 0.0009076695128639909, 0.0009554896585398429, 0.0009551195563474098, 0.0008978964195749315, 0.0007804349549344685, 0.0006058985092187082, 0.0003843072747623774, 0.00013171070865373793, -0.00013171070865373793, -0.0003843072747623774, -0.0006058985092187082, -0.0007804349549344685, -0.0008978964195749315, -0.0009551195563474098, -0.0009554896585398429, -0.0009076695128639909, -0.0008237122522291399, -0.0007169792467158665, -0.0006002538063475515, -0.0004843311170773316],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q1": {
            "samples": [0.0004843311170773316, 0.0006002538063475515, 0.0007169792467158665, 0.0008237122522291399, 0.0009076695128639909, 0.0009554896585398429, 0.0009551195563474098, 0.0008978964195749315, 0.0007804349549344685, 0.0006058985092187082, 0.0003843072747623774, 0.00013171070865373793, -0.00013171070865373793, -0.0003843072747623774, -0.0006058985092187082, -0.0007804349549344685, -0.0008978964195749315, -0.0009551195563474098, -0.0009554896585398429, -0.0009076695128639909, -0.0008237122522291399, -0.0007169792467158665, -0.0006002538063475515, -0.0004843311170773316],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q1": {
            "samples": [0.0, 0.0007544496482014039, 0.0016719663934131246, 0.0027464431239315745, 0.003955228231179286, 0.005257272897700412, 0.006593597485558204, 0.007890560914059744, 0.009065942537806505, 0.010037269651154779, 0.010731276544516957] + [0.011093009024062787] * 2 + [0.010731276544516957, 0.010037269651154779, 0.009065942537806505, 0.007890560914059744, 0.006593597485558204, 0.005257272897700412, 0.003955228231179286, 0.0027464431239315745, 0.0016719663934131246, 0.0007544496482014039, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q1": {
            "samples": [0.0009686622341546632, 0.001200507612695103, 0.001433958493431733, 0.0016474245044582798, 0.0018153390257279818, 0.0019109793170796858, 0.0019102391126948196, 0.001795792839149863, 0.001560869909868937, 0.0012117970184374164, 0.0007686145495247548, 0.00026342141730747586, -0.00026342141730747586, -0.0007686145495247548, -0.0012117970184374164, -0.001560869909868937, -0.001795792839149863, -0.0019102391126948196, -0.0019109793170796858, -0.0018153390257279818, -0.0016474245044582798, -0.001433958493431733, -0.001200507612695103, -0.0009686622341546632],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q1": {
            "samples": [0.0, 0.0015088992964028079, 0.003343932786826249, 0.005492886247863149, 0.007910456462358571, 0.010514545795400823, 0.013187194971116409, 0.01578112182811949, 0.01813188507561301, 0.020074539302309558, 0.021462553089033914] + [0.022186018048125575] * 2 + [0.021462553089033914, 0.020074539302309558, 0.01813188507561301, 0.01578112182811949, 0.013187194971116409, 0.010514545795400823, 0.007910456462358571, 0.005492886247863149, 0.003343932786826249, 0.0015088992964028079, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q1": {
            "samples": [-0.0004843311170773316, -0.0006002538063475515, -0.0007169792467158665, -0.0008237122522291399, -0.0009076695128639909, -0.0009554896585398429, -0.0009551195563474098, -0.0008978964195749315, -0.0007804349549344685, -0.0006058985092187082, -0.0003843072747623774, -0.00013171070865373793, 0.00013171070865373793, 0.0003843072747623774, 0.0006058985092187082, 0.0007804349549344685, 0.0008978964195749315, 0.0009551195563474098, 0.0009554896585398429, 0.0009076695128639909, 0.0008237122522291399, 0.0007169792467158665, 0.0006002538063475515, 0.0004843311170773316],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q1": {
            "samples": [0.0, -0.0007544496482014039, -0.0016719663934131246, -0.0027464431239315745, -0.003955228231179286, -0.005257272897700412, -0.006593597485558204, -0.007890560914059744, -0.009065942537806505, -0.010037269651154779, -0.010731276544516957] + [-0.011093009024062787] * 2 + [-0.010731276544516957, -0.010037269651154779, -0.009065942537806505, -0.007890560914059744, -0.006593597485558204, -0.005257272897700412, -0.003955228231179286, -0.0027464431239315745, -0.0016719663934131246, -0.0007544496482014039, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q1": {
            "sample": 0.0324,
            "type": "constant",
        },
        "x90_I_wf_q2": {
            "samples": [0.0, 0.002670203474077361, 0.005917545965957568, 0.009720412738426047, 0.013998633558702928, 0.018606925444366956, 0.02333654333934451, 0.027926851335103017, 0.032086848099071884, 0.03552464018859211, 0.03798092023605078] + [0.039261190332103686] * 2 + [0.03798092023605078, 0.03552464018859211, 0.032086848099071884, 0.027926851335103017, 0.02333654333934451, 0.018606925444366956, 0.013998633558702928, 0.009720412738426047, 0.005917545965957568, 0.002670203474077361, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q2": {
            "samples": [-0.0011938334743415641, -0.0014795726763189318, -0.0017672905889318123, -0.0020303780311918635, -0.0022373252716763126, -0.0023551977119197235, -0.0023542854426669853, -0.002213235458932608, -0.0019237033114233198, -0.0014934863709024312, -0.0009472835274613423, -0.0003246552768877233, 0.0003246552768877233, 0.0009472835274613423, 0.0014934863709024312, 0.0019237033114233198, 0.002213235458932608, 0.0023542854426669853, 0.0023551977119197235, 0.0022373252716763126, 0.0020303780311918635, 0.0017672905889318123, 0.0014795726763189318, 0.0011938334743415641],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q2": {
            "samples": [0.0, 0.005201361798326289, 0.011526948349060446, 0.01893465571910518, 0.02726831813675344, 0.0362449349385543, 0.04545788596586014, 0.05439947146055351, 0.06250284203112216, 0.06919941052060677, 0.07398406507179489] + [0.07647793792972385] * 2 + [0.07398406507179489, 0.06919941052060677, 0.06250284203112216, 0.05439947146055351, 0.04545788596586014, 0.0362449349385543, 0.02726831813675344, 0.01893465571910518, 0.011526948349060446, 0.005201361798326289, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q2": {
            "samples": [-0.002325500617195082, -0.002882099761746364, -0.003442553290433316, -0.003955028457616458, -0.004358146602497455, -0.004587753527104358, -0.004585976493074163, -0.00431122140262023, -0.003747233876552562, -0.0029092026249486515, -0.0018452392859775167, -0.0006324048227868956, 0.0006324048227868956, 0.0018452392859775167, 0.0029092026249486515, 0.003747233876552562, 0.00431122140262023, 0.004585976493074163, 0.004587753527104358, 0.004358146602497455, 0.003955028457616458, 0.003442553290433316, 0.002882099761746364, 0.002325500617195082],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q2": {
            "samples": [0.0, -0.002670203474077361, -0.005917545965957568, -0.009720412738426047, -0.013998633558702928, -0.018606925444366956, -0.02333654333934451, -0.027926851335103017, -0.032086848099071884, -0.03552464018859211, -0.03798092023605078] + [-0.039261190332103686] * 2 + [-0.03798092023605078, -0.03552464018859211, -0.032086848099071884, -0.027926851335103017, -0.02333654333934451, -0.018606925444366956, -0.013998633558702928, -0.009720412738426047, -0.005917545965957568, -0.002670203474077361, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q2": {
            "samples": [0.0011938334743415641, 0.0014795726763189318, 0.0017672905889318123, 0.0020303780311918635, 0.0022373252716763126, 0.0023551977119197235, 0.0023542854426669853, 0.002213235458932608, 0.0019237033114233198, 0.0014934863709024312, 0.0009472835274613423, 0.0003246552768877233, -0.0003246552768877233, -0.0009472835274613423, -0.0014934863709024312, -0.0019237033114233198, -0.002213235458932608, -0.0023542854426669853, -0.0023551977119197235, -0.0022373252716763126, -0.0020303780311918635, -0.0017672905889318123, -0.0014795726763189318, -0.0011938334743415641],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q2": {
            "samples": [0.001162750308597541, 0.001441049880873182, 0.001721276645216658, 0.001977514228808229, 0.0021790733012487275, 0.002293876763552179, 0.0022929882465370817, 0.002155610701310115, 0.001873616938276281, 0.0014546013124743257, 0.0009226196429887583, 0.0003162024113934478, -0.0003162024113934478, -0.0009226196429887583, -0.0014546013124743257, -0.001873616938276281, -0.002155610701310115, -0.0022929882465370817, -0.002293876763552179, -0.0021790733012487275, -0.001977514228808229, -0.001721276645216658, -0.001441049880873182, -0.001162750308597541],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q2": {
            "samples": [0.0, 0.0026006808991631443, 0.005763474174530223, 0.00946732785955259, 0.01363415906837672, 0.01812246746927715, 0.02272894298293007, 0.027199735730276755, 0.03125142101556108, 0.034599705260303384, 0.036992032535897446] + [0.038238968964861925] * 2 + [0.036992032535897446, 0.034599705260303384, 0.03125142101556108, 0.027199735730276755, 0.02272894298293007, 0.01812246746927715, 0.01363415906837672, 0.00946732785955259, 0.005763474174530223, 0.0026006808991631443, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q2": {
            "samples": [0.002325500617195082, 0.002882099761746364, 0.003442553290433316, 0.003955028457616458, 0.004358146602497455, 0.004587753527104358, 0.004585976493074163, 0.00431122140262023, 0.003747233876552562, 0.0029092026249486515, 0.0018452392859775167, 0.0006324048227868956, -0.0006324048227868956, -0.0018452392859775167, -0.0029092026249486515, -0.003747233876552562, -0.00431122140262023, -0.004585976493074163, -0.004587753527104358, -0.004358146602497455, -0.003955028457616458, -0.003442553290433316, -0.002882099761746364, -0.002325500617195082],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q2": {
            "samples": [0.0, 0.005201361798326289, 0.011526948349060446, 0.01893465571910518, 0.02726831813675344, 0.0362449349385543, 0.04545788596586014, 0.05439947146055351, 0.06250284203112216, 0.06919941052060677, 0.07398406507179489] + [0.07647793792972385] * 2 + [0.07398406507179489, 0.06919941052060677, 0.06250284203112216, 0.05439947146055351, 0.04545788596586014, 0.0362449349385543, 0.02726831813675344, 0.01893465571910518, 0.011526948349060446, 0.005201361798326289, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q2": {
            "samples": [-0.001162750308597541, -0.001441049880873182, -0.001721276645216658, -0.001977514228808229, -0.0021790733012487275, -0.002293876763552179, -0.0022929882465370817, -0.002155610701310115, -0.001873616938276281, -0.0014546013124743257, -0.0009226196429887583, -0.0003162024113934478, 0.0003162024113934478, 0.0009226196429887583, 0.0014546013124743257, 0.001873616938276281, 0.002155610701310115, 0.0022929882465370817, 0.002293876763552179, 0.0021790733012487275, 0.001977514228808229, 0.001721276645216658, 0.001441049880873182, 0.001162750308597541],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q2": {
            "samples": [0.0, -0.0026006808991631443, -0.005763474174530223, -0.00946732785955259, -0.01363415906837672, -0.01812246746927715, -0.02272894298293007, -0.027199735730276755, -0.03125142101556108, -0.034599705260303384, -0.036992032535897446] + [-0.038238968964861925] * 2 + [-0.036992032535897446, -0.034599705260303384, -0.03125142101556108, -0.027199735730276755, -0.02272894298293007, -0.01812246746927715, -0.01363415906837672, -0.00946732785955259, -0.005763474174530223, -0.0026006808991631443, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q2": {
            "sample": 0.144,
            "type": "constant",
        },
        "x90_I_wf_q3": {
            "samples": [0.0, 0.0006718872338699294, 0.001488996486209424, 0.00244588897074661, 0.0035223919341823076, 0.004681948693801121, 0.005872033987138627, 0.0070270655687475455, 0.008073820524235227, 0.0089388514629152, 0.00955691043209812] + [0.009879057093127613] * 2 + [0.00955691043209812, 0.0089388514629152, 0.008073820524235227, 0.0070270655687475455, 0.005872033987138627, 0.004681948693801121, 0.0035223919341823076, 0.00244588897074661, 0.001488996486209424, 0.0006718872338699294, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q3": {
            "samples": [0.00047033333302028704, 0.0005829057094270503, 0.0006962576364062219, 0.0007999059225813085, 0.0008814367118147775, 0.0009278747945812992, 0.0009275153888120072, 0.0008719460733270016, 0.0007578793941114009, 0.0005883872732202693, 0.000373200306710981, 0.00012790410198997286, -0.00012790410198997286, -0.000373200306710981, -0.0005883872732202693, -0.0007578793941114009, -0.0008719460733270016, -0.0009275153888120072, -0.0009278747945812992, -0.0008814367118147775, -0.0007999059225813085, -0.0006962576364062219, -0.0005829057094270503, -0.00047033333302028704],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q3": {
            "samples": [0.0, 0.0013437744677398588, 0.002977992972418848, 0.00489177794149322, 0.007044783868364615, 0.009363897387602241, 0.011744067974277255, 0.014054131137495091, 0.016147641048470454, 0.0178777029258304, 0.01911382086419624] + [0.019758114186255227] * 2 + [0.01911382086419624, 0.0178777029258304, 0.016147641048470454, 0.014054131137495091, 0.011744067974277255, 0.009363897387602241, 0.007044783868364615, 0.00489177794149322, 0.002977992972418848, 0.0013437744677398588, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q3": {
            "samples": [0.0009406666660405741, 0.0011658114188541006, 0.0013925152728124438, 0.001599811845162617, 0.001762873423629555, 0.0018557495891625983, 0.0018550307776240144, 0.001743892146654003, 0.0015157587882228018, 0.0011767745464405387, 0.000746400613421962, 0.00025580820397994573, -0.00025580820397994573, -0.000746400613421962, -0.0011767745464405387, -0.0015157587882228018, -0.001743892146654003, -0.0018550307776240144, -0.0018557495891625983, -0.001762873423629555, -0.001599811845162617, -0.0013925152728124438, -0.0011658114188541006, -0.0009406666660405741],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q3": {
            "samples": [0.0, -0.0006718872338699294, -0.001488996486209424, -0.00244588897074661, -0.0035223919341823076, -0.004681948693801121, -0.005872033987138627, -0.0070270655687475455, -0.008073820524235227, -0.0089388514629152, -0.00955691043209812] + [-0.009879057093127613] * 2 + [-0.00955691043209812, -0.0089388514629152, -0.008073820524235227, -0.0070270655687475455, -0.005872033987138627, -0.004681948693801121, -0.0035223919341823076, -0.00244588897074661, -0.001488996486209424, -0.0006718872338699294, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q3": {
            "samples": [-0.00047033333302028704, -0.0005829057094270503, -0.0006962576364062219, -0.0007999059225813085, -0.0008814367118147775, -0.0009278747945812992, -0.0009275153888120072, -0.0008719460733270016, -0.0007578793941114009, -0.0005883872732202693, -0.000373200306710981, -0.00012790410198997286, 0.00012790410198997286, 0.000373200306710981, 0.0005883872732202693, 0.0007578793941114009, 0.0008719460733270016, 0.0009275153888120072, 0.0009278747945812992, 0.0008814367118147775, 0.0007999059225813085, 0.0006962576364062219, 0.0005829057094270503, 0.00047033333302028704],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q3": {
            "samples": [-0.00047033333302028704, -0.0005829057094270503, -0.0006962576364062219, -0.0007999059225813085, -0.0008814367118147775, -0.0009278747945812992, -0.0009275153888120072, -0.0008719460733270016, -0.0007578793941114009, -0.0005883872732202693, -0.000373200306710981, -0.00012790410198997286, 0.00012790410198997286, 0.000373200306710981, 0.0005883872732202693, 0.0007578793941114009, 0.0008719460733270016, 0.0009275153888120072, 0.0009278747945812992, 0.0008814367118147775, 0.0007999059225813085, 0.0006962576364062219, 0.0005829057094270503, 0.00047033333302028704],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q3": {
            "samples": [0.0, 0.0006718872338699294, 0.001488996486209424, 0.00244588897074661, 0.0035223919341823076, 0.004681948693801121, 0.005872033987138627, 0.0070270655687475455, 0.008073820524235227, 0.0089388514629152, 0.00955691043209812] + [0.009879057093127613] * 2 + [0.00955691043209812, 0.0089388514629152, 0.008073820524235227, 0.0070270655687475455, 0.005872033987138627, 0.004681948693801121, 0.0035223919341823076, 0.00244588897074661, 0.001488996486209424, 0.0006718872338699294, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q3": {
            "samples": [-0.0009406666660405741, -0.0011658114188541006, -0.0013925152728124438, -0.001599811845162617, -0.001762873423629555, -0.0018557495891625983, -0.0018550307776240144, -0.001743892146654003, -0.0015157587882228018, -0.0011767745464405387, -0.000746400613421962, -0.00025580820397994573, 0.00025580820397994573, 0.000746400613421962, 0.0011767745464405387, 0.0015157587882228018, 0.001743892146654003, 0.0018550307776240144, 0.0018557495891625983, 0.001762873423629555, 0.001599811845162617, 0.0013925152728124438, 0.0011658114188541006, 0.0009406666660405741],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q3": {
            "samples": [0.0, 0.0013437744677398588, 0.002977992972418848, 0.00489177794149322, 0.007044783868364615, 0.009363897387602241, 0.011744067974277255, 0.014054131137495091, 0.016147641048470454, 0.0178777029258304, 0.01911382086419624] + [0.019758114186255227] * 2 + [0.01911382086419624, 0.0178777029258304, 0.016147641048470454, 0.014054131137495091, 0.011744067974277255, 0.009363897387602241, 0.007044783868364615, 0.00489177794149322, 0.002977992972418848, 0.0013437744677398588, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q3": {
            "samples": [0.00047033333302028704, 0.0005829057094270503, 0.0006962576364062219, 0.0007999059225813085, 0.0008814367118147775, 0.0009278747945812992, 0.0009275153888120072, 0.0008719460733270016, 0.0007578793941114009, 0.0005883872732202693, 0.000373200306710981, 0.00012790410198997286, -0.00012790410198997286, -0.000373200306710981, -0.0005883872732202693, -0.0007578793941114009, -0.0008719460733270016, -0.0009275153888120072, -0.0009278747945812992, -0.0008814367118147775, -0.0007999059225813085, -0.0006962576364062219, -0.0005829057094270503, -0.00047033333302028704],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q3": {
            "samples": [0.0, -0.0006718872338699294, -0.001488996486209424, -0.00244588897074661, -0.0035223919341823076, -0.004681948693801121, -0.005872033987138627, -0.0070270655687475455, -0.008073820524235227, -0.0089388514629152, -0.00955691043209812] + [-0.009879057093127613] * 2 + [-0.00955691043209812, -0.0089388514629152, -0.008073820524235227, -0.0070270655687475455, -0.005872033987138627, -0.004681948693801121, -0.0035223919341823076, -0.00244588897074661, -0.001488996486209424, -0.0006718872338699294, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q3": {
            "sample": 0.0891,
            "type": "constant",
        },
        "x90_I_wf_q4": {
            "samples": [0.0, 0.0032645524905044986, 0.00723470687098729, 0.011884037273573345, 0.017114528720892336, 0.022748560321242322, 0.02853092336139178, 0.03414296811573922, 0.039228920526537314, 0.04343191585503292, 0.04643492863070854] + [0.04800016849769362] * 2 + [0.04643492863070854, 0.04343191585503292, 0.039228920526537314, 0.03414296811573922, 0.02853092336139178, 0.022748560321242322, 0.017114528720892336, 0.011884037273573345, 0.00723470687098729, 0.0032645524905044986, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q4": {
            "samples": [0.002341149429575977, 0.0029014940539263383, 0.0034657189994229806, 0.003981642726319167, 0.004387473543116882, 0.004618625543935746, 0.004616836551847176, 0.004340232573102515, 0.0037724498491684866, 0.002928779298340698, 0.001857656312733222, 0.0006366604159040895, -0.0006366604159040895, -0.001857656312733222, -0.002928779298340698, -0.0037724498491684866, -0.004340232573102515, -0.004616836551847176, -0.004618625543935746, -0.004387473543116882, -0.003981642726319167, -0.0034657189994229806, -0.0029014940539263383, -0.002341149429575977],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q4": {
            "samples": [0.0, 0.006452640225472251, 0.014299957103161412, 0.023489717863479788, 0.03382818833075763, 0.04496428708908453, 0.05639357439865581, 0.0674862144570966, 0.0775389923512213, 0.08584653735256745, 0.09178222412442785] + [0.09487604165611044] * 2 + [0.09178222412442785, 0.08584653735256745, 0.0775389923512213, 0.0674862144570966, 0.05639357439865581, 0.04496428708908453, 0.03382818833075763, 0.023489717863479788, 0.014299957103161412, 0.006452640225472251, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q4": {
            "samples": [0.004627462730975668, 0.005735027174717087, 0.006850261373008041, 0.007870024480854845, 0.00867218044582158, 0.009129070234857166, 0.009125534153771831, 0.008578805018625457, 0.007456538596369603, 0.0057889585684324715, 0.00367180122957448, 0.0012584085021079738, -0.0012584085021079738, -0.00367180122957448, -0.0057889585684324715, -0.007456538596369603, -0.008578805018625457, -0.009125534153771831, -0.009129070234857166, -0.00867218044582158, -0.007870024480854845, -0.006850261373008041, -0.005735027174717087, -0.004627462730975668],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q4": {
            "samples": [0.0, -0.0032645524905044986, -0.00723470687098729, -0.011884037273573345, -0.017114528720892336, -0.022748560321242322, -0.02853092336139178, -0.03414296811573922, -0.039228920526537314, -0.04343191585503292, -0.04643492863070854] + [-0.04800016849769362] * 2 + [-0.04643492863070854, -0.04343191585503292, -0.039228920526537314, -0.03414296811573922, -0.02853092336139178, -0.022748560321242322, -0.017114528720892336, -0.011884037273573345, -0.00723470687098729, -0.0032645524905044986, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q4": {
            "samples": [-0.002341149429575977, -0.0029014940539263383, -0.0034657189994229806, -0.003981642726319167, -0.004387473543116882, -0.004618625543935746, -0.004616836551847176, -0.004340232573102515, -0.0037724498491684866, -0.002928779298340698, -0.001857656312733222, -0.0006366604159040895, 0.0006366604159040895, 0.001857656312733222, 0.002928779298340698, 0.0037724498491684866, 0.004340232573102515, 0.004616836551847176, 0.004618625543935746, 0.004387473543116882, 0.003981642726319167, 0.0034657189994229806, 0.0029014940539263383, 0.002341149429575977],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q4": {
            "samples": [-0.002313731365487834, -0.0028675135873585437, -0.0034251306865040205, -0.003935012240427423, -0.00433609022291079, -0.004564535117428583, -0.004562767076885916, -0.004289402509312729, -0.0037282692981848017, -0.0028944792842162358, -0.00183590061478724, -0.0006292042510539869, 0.0006292042510539869, 0.00183590061478724, 0.0028944792842162358, 0.0037282692981848017, 0.004289402509312729, 0.004562767076885916, 0.004564535117428583, 0.00433609022291079, 0.003935012240427423, 0.0034251306865040205, 0.0028675135873585437, 0.002313731365487834],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q4": {
            "samples": [0.0, 0.0032263201127361255, 0.007149978551580706, 0.011744858931739894, 0.016914094165378816, 0.022482143544542265, 0.028196787199327906, 0.0337431072285483, 0.03876949617561065, 0.042923268676283724, 0.045891112062213926] + [0.04743802082805522] * 2 + [0.045891112062213926, 0.042923268676283724, 0.03876949617561065, 0.0337431072285483, 0.028196787199327906, 0.022482143544542265, 0.016914094165378816, 0.011744858931739894, 0.007149978551580706, 0.0032263201127361255, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q4": {
            "samples": [-0.004627462730975668, -0.005735027174717087, -0.006850261373008041, -0.007870024480854845, -0.00867218044582158, -0.009129070234857166, -0.009125534153771831, -0.008578805018625457, -0.007456538596369603, -0.0057889585684324715, -0.00367180122957448, -0.0012584085021079738, 0.0012584085021079738, 0.00367180122957448, 0.0057889585684324715, 0.007456538596369603, 0.008578805018625457, 0.009125534153771831, 0.009129070234857166, 0.00867218044582158, 0.007870024480854845, 0.006850261373008041, 0.005735027174717087, 0.004627462730975668],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q4": {
            "samples": [0.0, 0.006452640225472251, 0.014299957103161412, 0.023489717863479788, 0.03382818833075763, 0.04496428708908453, 0.05639357439865581, 0.0674862144570966, 0.0775389923512213, 0.08584653735256745, 0.09178222412442785] + [0.09487604165611044] * 2 + [0.09178222412442785, 0.08584653735256745, 0.0775389923512213, 0.0674862144570966, 0.05639357439865581, 0.04496428708908453, 0.03382818833075763, 0.023489717863479788, 0.014299957103161412, 0.006452640225472251, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q4": {
            "samples": [0.002313731365487834, 0.0028675135873585437, 0.0034251306865040205, 0.003935012240427423, 0.00433609022291079, 0.004564535117428583, 0.004562767076885916, 0.004289402509312729, 0.0037282692981848017, 0.0028944792842162358, 0.00183590061478724, 0.0006292042510539869, -0.0006292042510539869, -0.00183590061478724, -0.0028944792842162358, -0.0037282692981848017, -0.004289402509312729, -0.004562767076885916, -0.004564535117428583, -0.00433609022291079, -0.003935012240427423, -0.0034251306865040205, -0.0028675135873585437, -0.002313731365487834],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q4": {
            "samples": [0.0, -0.0032263201127361255, -0.007149978551580706, -0.011744858931739894, -0.016914094165378816, -0.022482143544542265, -0.028196787199327906, -0.0337431072285483, -0.03876949617561065, -0.042923268676283724, -0.045891112062213926] + [-0.04743802082805522] * 2 + [-0.045891112062213926, -0.042923268676283724, -0.03876949617561065, -0.0337431072285483, -0.028196787199327906, -0.022482143544542265, -0.016914094165378816, -0.011744858931739894, -0.007149978551580706, -0.0032263201127361255, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q4": {
            "sample": 0.0691,
            "type": "constant",
        },
        "x90_I_wf_q5": {
            "samples": [0.0, 0.0026121100591890095, 0.005788802798532825, 0.009508933734828941, 0.013694076832936275, 0.018202109912468303, 0.02282882941138589, 0.027319269861673892, 0.031388761006767796, 0.03475175988891816, 0.03715460067706034] + [0.03840701699246275] * 2 + [0.03715460067706034, 0.03475175988891816, 0.031388761006767796, 0.027319269861673892, 0.02282882941138589, 0.018202109912468303, 0.013694076832936275, 0.009508933734828941, 0.005788802798532825, 0.0026121100591890095, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q5": {
            "samples": [-0.0002455604341849997, -0.0003043343285423653, -0.00036351522526080216, -0.0004176298634733303, -0.00046019698469999603, -0.0004844422485719789, -0.0004842546032775466, -0.000455241934432167, -0.00039568786648135095, -0.00030719624601785407, -0.00019484740485099886, -6.677856875890505e-05, 6.677856875890505e-05, 0.00019484740485099886, 0.00030719624601785407, 0.00039568786648135095, 0.000455241934432167, 0.0004842546032775466, 0.0004844422485719789, 0.00046019698469999603, 0.0004176298634733303, 0.00036351522526080216, 0.0003043343285423653, 0.0002455604341849997],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q5": {
            "samples": [0.0, 0.005200109678661469, 0.011524173476005501, 0.018930097594580936, 0.027261753856342007, 0.03623620972436113, 0.04544694292533617, 0.054386375919306354, 0.062487795771959925, 0.06918275220186906, 0.07396625494699463] + [0.07645952745690551] * 2 + [0.07396625494699463, 0.06918275220186906, 0.062487795771959925, 0.054386375919306354, 0.04544694292533617, 0.03623620972436113, 0.027261753856342007, 0.018930097594580936, 0.011524173476005501, 0.005200109678661469, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q5": {
            "samples": [-0.000488854283153056, -0.000605859573885428, -0.00072367511260471, -0.0008314048971657783, -0.0009161462342717137, -0.0009644129720681843, -0.0009640394134930774, -0.0009062818701093581, -0.0007877234333906347, -0.0006115569926107478, -0.00038789631863457146, -0.00013294075435632918, 0.00013294075435632918, 0.00038789631863457146, 0.0006115569926107478, 0.0007877234333906347, 0.0009062818701093581, 0.0009640394134930774, 0.0009644129720681843, 0.0009161462342717137, 0.0008314048971657783, 0.00072367511260471, 0.000605859573885428, 0.000488854283153056],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q5": {
            "samples": [0.0, -0.0026121100591890095, -0.005788802798532825, -0.009508933734828941, -0.013694076832936275, -0.018202109912468303, -0.02282882941138589, -0.027319269861673892, -0.031388761006767796, -0.03475175988891816, -0.03715460067706034] + [-0.03840701699246275] * 2 + [-0.03715460067706034, -0.03475175988891816, -0.031388761006767796, -0.027319269861673892, -0.02282882941138589, -0.018202109912468303, -0.013694076832936275, -0.009508933734828941, -0.005788802798532825, -0.0026121100591890095, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q5": {
            "samples": [0.0002455604341849997, 0.0003043343285423653, 0.00036351522526080216, 0.0004176298634733303, 0.00046019698469999603, 0.0004844422485719789, 0.0004842546032775466, 0.000455241934432167, 0.00039568786648135095, 0.00030719624601785407, 0.00019484740485099886, 6.677856875890505e-05, -6.677856875890505e-05, -0.00019484740485099886, -0.00030719624601785407, -0.00039568786648135095, -0.000455241934432167, -0.0004842546032775466, -0.0004844422485719789, -0.00046019698469999603, -0.0004176298634733303, -0.00036351522526080216, -0.0003043343285423653, -0.0002455604341849997],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q5": {
            "samples": [0.000244427141576528, 0.000302929786942714, 0.000361837556302355, 0.00041570244858288915, 0.00045807311713585687, 0.00048220648603409215, 0.0004820197067465387, 0.00045314093505467907, 0.00039386171669531737, 0.0003057784963053739, 0.00019394815931728573, 6.647037717816459e-05, -6.647037717816459e-05, -0.00019394815931728573, -0.0003057784963053739, -0.00039386171669531737, -0.00045314093505467907, -0.0004820197067465387, -0.00048220648603409215, -0.00045807311713585687, -0.00041570244858288915, -0.000361837556302355, -0.000302929786942714, -0.000244427141576528],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q5": {
            "samples": [0.0, 0.0026000548393307343, 0.0057620867380027505, 0.009465048797290468, 0.013630876928171004, 0.018118104862180566, 0.022723471462668086, 0.027193187959653177, 0.031243897885979963, 0.03459137610093453, 0.036983127473497315] + [0.038229763728452756] * 2 + [0.036983127473497315, 0.03459137610093453, 0.031243897885979963, 0.027193187959653177, 0.022723471462668086, 0.018118104862180566, 0.013630876928171004, 0.009465048797290468, 0.0057620867380027505, 0.0026000548393307343, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q5": {
            "samples": [0.000488854283153056, 0.000605859573885428, 0.00072367511260471, 0.0008314048971657783, 0.0009161462342717137, 0.0009644129720681843, 0.0009640394134930774, 0.0009062818701093581, 0.0007877234333906347, 0.0006115569926107478, 0.00038789631863457146, 0.00013294075435632918, -0.00013294075435632918, -0.00038789631863457146, -0.0006115569926107478, -0.0007877234333906347, -0.0009062818701093581, -0.0009640394134930774, -0.0009644129720681843, -0.0009161462342717137, -0.0008314048971657783, -0.00072367511260471, -0.000605859573885428, -0.000488854283153056],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q5": {
            "samples": [0.0, 0.005200109678661469, 0.011524173476005501, 0.018930097594580936, 0.027261753856342007, 0.03623620972436113, 0.04544694292533617, 0.054386375919306354, 0.062487795771959925, 0.06918275220186906, 0.07396625494699463] + [0.07645952745690551] * 2 + [0.07396625494699463, 0.06918275220186906, 0.062487795771959925, 0.054386375919306354, 0.04544694292533617, 0.03623620972436113, 0.027261753856342007, 0.018930097594580936, 0.011524173476005501, 0.005200109678661469, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q5": {
            "samples": [-0.000244427141576528, -0.000302929786942714, -0.000361837556302355, -0.00041570244858288915, -0.00045807311713585687, -0.00048220648603409215, -0.0004820197067465387, -0.00045314093505467907, -0.00039386171669531737, -0.0003057784963053739, -0.00019394815931728573, -6.647037717816459e-05, 6.647037717816459e-05, 0.00019394815931728573, 0.0003057784963053739, 0.00039386171669531737, 0.00045314093505467907, 0.0004820197067465387, 0.00048220648603409215, 0.00045807311713585687, 0.00041570244858288915, 0.000361837556302355, 0.000302929786942714, 0.000244427141576528],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q5": {
            "samples": [0.0, -0.0026000548393307343, -0.0057620867380027505, -0.009465048797290468, -0.013630876928171004, -0.018118104862180566, -0.022723471462668086, -0.027193187959653177, -0.031243897885979963, -0.03459137610093453, -0.036983127473497315] + [-0.038229763728452756] * 2 + [-0.036983127473497315, -0.03459137610093453, -0.031243897885979963, -0.027193187959653177, -0.022723471462668086, -0.018118104862180566, -0.013630876928171004, -0.009465048797290468, -0.0057620867380027505, -0.0026000548393307343, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q5": {
            "sample": 0.131,
            "type": "constant",
        },
        "gft_cz_wf_1_2_q2": {
            "samples": [2.4584008754312155e-06, 3.785965707138443e-05, 0.00039450668590304175, 0.0027815429979183397, 0.01326999947723866, 0.04283608303386536, 0.09356260729473384, 0.13827656985454806] + [0.14519591] * 8 + [0.13827656985454806, 0.09356260729473384, 0.04283608303386536, 0.01326999947723866, 0.0027815429979183397, 0.00039450668590304175, 3.785965707138443e-05, 2.4584008754312155e-06],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "g_cz_wf_1_2_q2": {
            "samples": [0.043105405973438204, 0.06676295880658584, 0.09713953187809103, 0.1327739977588363, 0.17048518779758703, 0.20564439059966616, 0.2330256230898819] + [0.24805448456506088] * 2 + [0.2330256230898819, 0.20564439059966616, 0.17048518779758703, 0.1327739977588363, 0.09713953187809103, 0.06676295880658584, 0.043105405973438204],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "cz_4c5t_wf": {
            "samples": [0.0] + [0.194652068517] * 27,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "cz_3c4t_wf": {
            "samples": [0.0] + [0.1591175284349345] * 47,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "cz_3c2t_wf": {
            "samples": [0.0] + [0.2687859507460096] * 51,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "cz_2c3t_wf": {
            "samples": [0.0] + [0.015] * 31,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "cz_2c1t_wf": {
            "samples": [0.0] + [-0.13840394169773318] * 23,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
    },
    "digital_waveforms": {
        "ON": {
            "samples": [(1, 0)],
        },
    },
    "integration_weights": {
        "cosine_weights": {
            "cosine": [(1.0, 1800)],
            "sine": [(0.0, 1800)],
        },
        "sine_weights": {
            "cosine": [(0.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "minus_sine_weights": {
            "cosine": [(0.0, 1800)],
            "sine": [(-1.0, 1800)],
        },
        "rotated_cosine_weights_q1": {
            "cosine": [(-0.1581580672544845, 1800)],
            "sine": [(-0.9874138067509113, 1800)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(0.9874138067509113, 1800)],
            "sine": [(-0.1581580672544845, 1800)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(-0.9874138067509113, 1800)],
            "sine": [(0.1581580672544845, 1800)],
        },
        "rotated_cosine_weights_q2": {
            "cosine": [(-0.335451569750255, 1800)],
            "sine": [(0.9420574527872967, 1800)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(-0.9420574527872967, 1800)],
            "sine": [(-0.335451569750255, 1800)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(0.9420574527872967, 1800)],
            "sine": [(0.335451569750255, 1800)],
        },
        "rotated_cosine_weights_q3": {
            "cosine": [(-0.6691306063588585, 1800)],
            "sine": [(0.743144825477394, 1800)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(-0.743144825477394, 1800)],
            "sine": [(-0.6691306063588585, 1800)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(0.743144825477394, 1800)],
            "sine": [(0.6691306063588585, 1800)],
        },
        "rotated_cosine_weights_q4": {
            "cosine": [(-0.061048539534856804, 1800)],
            "sine": [(-0.998134798421867, 1800)],
        },
        "rotated_sine_weights_q4": {
            "cosine": [(0.998134798421867, 1800)],
            "sine": [(-0.061048539534856804, 1800)],
        },
        "rotated_minus_sine_weights_q4": {
            "cosine": [(-0.998134798421867, 1800)],
            "sine": [(0.061048539534856804, 1800)],
        },
        "rotated_cosine_weights_q5": {
            "cosine": [(-0.9258705848099948, 1800)],
            "sine": [(-0.3778407868184669, 1800)],
        },
        "rotated_sine_weights_q5": {
            "cosine": [(0.3778407868184669, 1800)],
            "sine": [(-0.9258705848099948, 1800)],
        },
        "rotated_minus_sine_weights_q5": {
            "cosine": [(-0.3778407868184669, 1800)],
            "sine": [(0.9258705848099948, 1800)],
        },
        "opt_cosine_weights_q1": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_sine_weights_q1": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_minus_sine_weights_q1": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_cosine_weights_q2": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_sine_weights_q2": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_minus_sine_weights_q2": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_cosine_weights_q3": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_sine_weights_q3": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_minus_sine_weights_q3": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_cosine_weights_q4": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_sine_weights_q4": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_minus_sine_weights_q4": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_cosine_weights_q5": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_sine_weights_q5": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
        "opt_minus_sine_weights_q5": {
            "cosine": [(1.0, 1800)],
            "sine": [(1.0, 1800)],
        },
    },
    "mixers": {
        "octave_octave1_2": [
            {'intermediate_frequency': 346063000.0, 'lo_frequency': 3670000000.0, 'correction': [1.139035176485777, 0.16698597371578217, 0.19680260121822357, 0.9664653651416302]},
            {'intermediate_frequency': 130602000.0, 'lo_frequency': 3200000000.0, 'correction': [0.9145237021148205, 0.06326756626367569, 0.051882900297641754, 1.1151976510882378]},
            {'intermediate_frequency': 131046000.0, 'lo_frequency': 3200000000.0, 'correction': [0.8735883422195911, 0.07953835651278496, 0.05841812118887901, 1.1894216872751713]},
            {'intermediate_frequency': 131211000.0, 'lo_frequency': 3200000000.0, 'correction': [0.9102895632386208, 0.06404534727334976, 0.05197123438119888, 1.12177075445652]},
            {'intermediate_frequency': 131239000.0, 'lo_frequency': 3200000000.0, 'correction': [0.8902681805193424, 0.07561632618308067, 0.05812149867415428, 1.1582427732646465]},
            {'intermediate_frequency': 131235000.0, 'lo_frequency': 3200000000.0, 'correction': [0.9070513471961021, 0.06460833549499512, 0.05200457572937012, 1.12688310444355]},
            {'intermediate_frequency': 131392000.0, 'lo_frequency': 3200000000.0, 'correction': [0.9075584001839161, 0.06511697918176651, 0.05247024446725845, 1.1263042837381363]},
            {'intermediate_frequency': 131416000.0, 'lo_frequency': 3200000000.0, 'correction': [0.9092047810554504, 0.064693134278059, 0.05234674736857414, 1.1236477829515934]},
            {'intermediate_frequency': 131158000.0, 'lo_frequency': 3200000000.0, 'correction': [0.9102209247648716, 0.06425825506448746, 0.05213155597448349, 1.121954008936882]},
            {'intermediate_frequency': 135838000.0, 'lo_frequency': 3200000000.0, 'correction': [0.90909468755126, 0.06442656740546227, 0.05212172493338585, 1.1237128004431725]},
            {'intermediate_frequency': 135236000.0, 'lo_frequency': 3200000000.0, 'correction': [0.9105560258030891, 0.06402204185724258, 0.0519864484667778, 1.1213625334203243]},
            {'intermediate_frequency': 131126000.0, 'lo_frequency': 3200000000.0, 'correction': [0.9128555990755558, 0.06409711018204689, 0.05233735218644142, 1.1179664805531502]},
            {'intermediate_frequency': 131407000.0, 'lo_frequency': 3200000000.0, 'correction': [0.9095721393823624, 0.06452245637774467, 0.05225850269198418, 1.1230292730033398]},
            {'intermediate_frequency': 124539000.0, 'lo_frequency': 3200000000.0, 'correction': [0.907289020717144, 0.06597277894616127, 0.053109172731637955, 1.1270440630614758]},
            {'intermediate_frequency': 124637000.0, 'lo_frequency': 3200000000.0, 'correction': [0.9103271849453449, 0.06431788206100464, 0.05219238996505737, 1.1218171119689941]},
        ],
        "octave_octave1_3": [
            {'intermediate_frequency': 471832000.0, 'lo_frequency': 3670000000.0, 'correction': [1.0509245730936527, 0.1871345043182373, 0.1878669261932373, 1.0468274168670177]},
            {'intermediate_frequency': 261857000.0, 'lo_frequency': 3200000000.0, 'correction': [0.8728884682059288, -0.00466681644320488, -0.003476236015558243, 1.1718457750976086]},
            {'intermediate_frequency': 262513000.0, 'lo_frequency': 3200000000.0, 'correction': [0.8368789926171303, 0.003159593790769577, 0.0021197572350502014, 1.247405406087637]},
            {'intermediate_frequency': 262884000.0, 'lo_frequency': 3200000000.0, 'correction': [0.869447585195303, -0.0047644078731536865, -0.0035155974328517914, 1.1782930493354797]},
            {'intermediate_frequency': 262526000.0, 'lo_frequency': 3200000000.0, 'correction': [0.8509256765246391, 0.0001483820378780365, 0.00010387226939201355, 1.2155497074127197]},
            {'intermediate_frequency': 262792000.0, 'lo_frequency': 3200000000.0, 'correction': [0.8665041476488113, -0.003685157746076584, -0.0026972107589244843, 1.1838915720582008]},
            {'intermediate_frequency': 262349000.0, 'lo_frequency': 3200000000.0, 'correction': [0.8670051544904709, -0.003754355013370514, -0.002751685678958893, 1.1829278953373432]},
            {'intermediate_frequency': 262383000.0, 'lo_frequency': 3200000000.0, 'correction': [0.8687931708991528, -0.004607435315847397, -0.003393646329641342, 1.1795302629470825]},
            {'intermediate_frequency': 262114000.0, 'lo_frequency': 3200000000.0, 'correction': [0.868685033172369, -0.004248201847076416, -0.003128141164779663, 1.1797262392938137]},
            {'intermediate_frequency': 269833000.0, 'lo_frequency': 3200000000.0, 'correction': [0.8694386668503284, -0.007623564451932907, -0.005624677985906601, 1.1784180253744125]},
            {'intermediate_frequency': 266474000.0, 'lo_frequency': 3200000000.0, 'correction': [0.8699318952858448, -0.006611298769712448, -0.004884641617536545, 1.17744155600667]},
            {'intermediate_frequency': 207105000.0, 'lo_frequency': 3200000000.0, 'correction': [0.884800311177969, -0.014048315584659576, -0.010798372328281403, 1.1510951593518257]},
            {'intermediate_frequency': 207068000.0, 'lo_frequency': 3200000000.0, 'correction': [0.886374693363905, -0.014085430651903152, -0.010871652513742447, 1.1483967043459415]},
            {'intermediate_frequency': 208140000.0, 'lo_frequency': 3200000000.0, 'correction': [0.8805629462003708, -0.013572819530963898, -0.01031697541475296, 1.1584521941840649]},
            {'intermediate_frequency': 206772000.0, 'lo_frequency': 3200000000.0, 'correction': [0.882083285599947, -0.012483000755310059, -0.009527675807476044, 1.155690737068653]},
            {'intermediate_frequency': 195512000.0, 'lo_frequency': 3200000000.0, 'correction': [0.8857291266322136, -0.007012851536273956, -0.005405761301517487, 1.1490495018661022]},
            {'intermediate_frequency': 197837000.0, 'lo_frequency': 3200000000.0, 'correction': [0.886171780526638, -0.009882315993309021, -0.007625512778759003, 1.148438461124897]},
        ],
        "octave_octave1_4": [
            {'intermediate_frequency': 106551000.0, 'lo_frequency': 3960000000.0, 'correction': [1.3551864996552467, -0.023040927946567535, -0.038992561399936676, 0.8007874302566051]},
            {'intermediate_frequency': 106458000.0, 'lo_frequency': 3960000000.0, 'correction': [1.2996150106191635, -0.023949556052684784, -0.038025788962841034, 0.818528775125742]},
            {'intermediate_frequency': 106481000.0, 'lo_frequency': 3960000000.0, 'correction': [1.3489361219108105, -0.02309318631887436, -0.03881271928548813, 0.8026037104427814]},
            {'intermediate_frequency': 106486000.0, 'lo_frequency': 3960000000.0, 'correction': [1.3209210634231567, -0.024531234055757523, -0.039934027940034866, 0.8114338889718056]},
            {'intermediate_frequency': 106443000.0, 'lo_frequency': 3960000000.0, 'correction': [1.3447312489151955, -0.02273653820157051, -0.03803752735257149, 0.8037991337478161]},
            {'intermediate_frequency': 106377000.0, 'lo_frequency': 3960000000.0, 'correction': [1.3451869115233421, -0.021947916597127914, -0.036741312593221664, 0.8035654686391354]},
            {'intermediate_frequency': 106405000.0, 'lo_frequency': 3960000000.0, 'correction': [1.3458872437477112, -0.021549977362155914, -0.036105431616306305, 0.8033095933496952]},
            {'intermediate_frequency': 106395000.0, 'lo_frequency': 3960000000.0, 'correction': [1.3420724086463451, -0.02118780091404915, -0.03534986451268196, 0.8044037185609341]},
            {'intermediate_frequency': 109030000.0, 'lo_frequency': 3960000000.0, 'correction': [1.3440575115382671, -0.021957125514745712, -0.0367104671895504, 0.803902555257082]},
            {'intermediate_frequency': 158909000.0, 'lo_frequency': 3960000000.0, 'correction': [1.3499786704778671, -0.050194740295410156, -0.08388614654541016, 0.807783305644989]},
            {'intermediate_frequency': 99150000.0, 'lo_frequency': 3960000000.0, 'correction': [1.339694682508707, -0.020223990082740784, -0.033656731247901917, 0.8050089813768864]},
            {'intermediate_frequency': 99223000.0, 'lo_frequency': 3960000000.0, 'correction': [1.3419710472226143, -0.020403068512678146, -0.03404061123728752, 0.8043429665267467]},
            {'intermediate_frequency': 99228000.0, 'lo_frequency': 3960000000.0, 'correction': [1.3357893414795399, -0.020450826734304428, -0.03388380631804466, 0.8062256798148155]},
            {'intermediate_frequency': 99092000.0, 'lo_frequency': 3960000000.0, 'correction': [1.335228979587555, -0.02045520767569542, -0.03386959061026573, 0.8063984476029873]},
            {'intermediate_frequency': 100534000.0, 'lo_frequency': 3960000000.0, 'correction': [1.3411707878112793, -0.02001633495092392, -0.03336729854345322, 0.8045399077236652]},
            {'intermediate_frequency': 132534000.0, 'lo_frequency': 3960000000.0, 'correction': [1.3550899401307106, -0.03831326216459274, -0.06462227553129196, 0.8034058660268784]},
            {'intermediate_frequency': 138111000.0, 'lo_frequency': 3960000000.0, 'correction': [1.354216042906046, -0.0438227653503418, -0.0737299919128418, 0.8049030043184757]},
        ],
        "octave_octave1_5": [
            {'intermediate_frequency': 368712000.0, 'lo_frequency': 3960000000.0, 'correction': [1.5205974765121937, -0.035888671875, -0.071044921875, 0.7681368701159954]},
            {'intermediate_frequency': 368884000.0, 'lo_frequency': 3960000000.0, 'correction': [1.3623402081429958, -0.024932861328125, -0.042510986328125, 0.7990179099142551]},
            {'intermediate_frequency': 368950000.0, 'lo_frequency': 3960000000.0, 'correction': [1.4819180443882942, -0.02796586975455284, -0.053621333092451096, 0.772885050624609]},
            {'intermediate_frequency': 368836000.0, 'lo_frequency': 3960000000.0, 'correction': [1.4405015744268894, -0.036540985107421875, -0.06730270385742188, 0.7820985391736031]},
            {'intermediate_frequency': 368583000.0, 'lo_frequency': 3960000000.0, 'correction': [1.4771419242024422, -0.02573089674115181, -0.04914436861872673, 0.7733985595405102]},
            {'intermediate_frequency': 368508000.0, 'lo_frequency': 3960000000.0, 'correction': [1.464051179587841, -0.024200439453125, -0.045684814453125, 0.7755461484193802]},
            {'intermediate_frequency': 368530000.0, 'lo_frequency': 3960000000.0, 'correction': [1.4773151688277721, -0.024126052856445312, -0.04609870910644531, 0.7731622979044914]},
            {'intermediate_frequency': 368885000.0, 'lo_frequency': 3960000000.0, 'correction': [1.4773151688277721, -0.024126052856445312, -0.04609870910644531, 0.7731622979044914]},
            {'intermediate_frequency': 368843000.0, 'lo_frequency': 3960000000.0, 'correction': [1.47405668720603, -0.02565453201532364, -0.048862673342227936, 0.7739288546144962]},
            {'intermediate_frequency': 371061000.0, 'lo_frequency': 3960000000.0, 'correction': [1.464051179587841, -0.024200439453125, -0.045684814453125, 0.7755461484193802]},
            {'intermediate_frequency': 251555000.0, 'lo_frequency': 3960000000.0, 'correction': [1.3939951211214066, 0.012137506157159805, 0.021433237940073013, 0.7894106432795525]},
            {'intermediate_frequency': 368097000.0, 'lo_frequency': 3960000000.0, 'correction': [1.464051179587841, -0.024200439453125, -0.045684814453125, 0.7755461484193802]},
            {'intermediate_frequency': 364122000.0, 'lo_frequency': 3960000000.0, 'correction': [1.4679120182991028, -0.01510683074593544, -0.02865377441048622, 0.7739119343459606]},
            {'intermediate_frequency': 364152000.0, 'lo_frequency': 3960000000.0, 'correction': [1.4631172642111778, -0.01815032958984375, -0.03426361083984375, 0.7750514298677444]},
            {'intermediate_frequency': 364128000.0, 'lo_frequency': 3960000000.0, 'correction': [1.4631172642111778, -0.01815032958984375, -0.03426361083984375, 0.7750514298677444]},
            {'intermediate_frequency': 364103000.0, 'lo_frequency': 3960000000.0, 'correction': [1.4631172642111778, -0.01815032958984375, -0.03426361083984375, 0.7750514298677444]},
            {'intermediate_frequency': 365006000.0, 'lo_frequency': 3960000000.0, 'correction': [1.4674560204148293, -0.016525495797395706, -0.03132681921124458, 0.7741110809147358]},
            {'intermediate_frequency': 368831000.0, 'lo_frequency': 3960000000.0, 'correction': [1.4697413854300976, -0.02643631398677826, -0.050147637724876404, 0.7748030871152878]},
            {'intermediate_frequency': 368481000.0, 'lo_frequency': 3960000000.0, 'correction': [1.4695789776742458, -0.02719360962510109, -0.05156952515244484, 0.7749374620616436]},
        ],
        "octave_octave2_1": [
            {'intermediate_frequency': 122859000.0, 'lo_frequency': 4600000000.0, 'correction': [1.255867786705494, -0.0473419725894928, -0.0707947313785553, 0.8398260287940502]},
            {'intermediate_frequency': 122900000.0, 'lo_frequency': 4600000000.0, 'correction': [1.253316655755043, -0.04247363284230232, -0.06340106204152107, 0.8396217599511147]},
            {'intermediate_frequency': 122911000.0, 'lo_frequency': 4600000000.0, 'correction': [1.2556648589670658, -0.046525731682777405, -0.06957413256168365, 0.8396903276443481]},
            {'intermediate_frequency': 122888000.0, 'lo_frequency': 4600000000.0, 'correction': [1.2544812224805355, -0.04737443849444389, -0.07071657106280327, 0.84040192887187]},
            {'intermediate_frequency': 122908000.0, 'lo_frequency': 4600000000.0, 'correction': [1.2530965767800808, -0.047407008707523346, -0.0706385150551796, 0.8409797437489033]},
            {'intermediate_frequency': 122891000.0, 'lo_frequency': 4600000000.0, 'correction': [1.2526950538158417, -0.045772284269332886, -0.06820270419120789, 0.840710274875164]},
            {'intermediate_frequency': 122906000.0, 'lo_frequency': 4600000000.0, 'correction': [1.2526950538158417, -0.045772284269332886, -0.06820270419120789, 0.840710274875164]},
            {'intermediate_frequency': 122907000.0, 'lo_frequency': 4600000000.0, 'correction': [1.2523072995245457, -0.044137559831142426, -0.06576689332723618, 0.840450044721365]},
            {'intermediate_frequency': 128097000.0, 'lo_frequency': 4600000000.0, 'correction': [1.2526950538158417, -0.045772284269332886, -0.06820270419120789, 0.840710274875164]},
            {'intermediate_frequency': 128279000.0, 'lo_frequency': 4600000000.0, 'correction': [1.2526530660688877, -0.04412997141480446, -0.06578505411744118, 0.8403054997324944]},
            {'intermediate_frequency': 128741000.0, 'lo_frequency': 4600000000.0, 'correction': [1.2523072995245457, -0.044137559831142426, -0.06576689332723618, 0.840450044721365]},
            {'intermediate_frequency': 128925000.0, 'lo_frequency': 4600000000.0, 'correction': [1.2523072995245457, -0.044137559831142426, -0.06576689332723618, 0.840450044721365]},
            {'intermediate_frequency': 129200000.0, 'lo_frequency': 4600000000.0, 'correction': [1.2523072995245457, -0.044137559831142426, -0.06576689332723618, 0.840450044721365]},
            {'intermediate_frequency': 126767000.0, 'lo_frequency': 4600000000.0, 'correction': [1.2523072995245457, -0.044137559831142426, -0.06576689332723618, 0.840450044721365]},
            {'intermediate_frequency': 127400000.0, 'lo_frequency': 4600000000.0, 'correction': [1.2523072995245457, -0.044137559831142426, -0.06576689332723618, 0.840450044721365]},
            {'intermediate_frequency': 131436000.0, 'lo_frequency': 4600000000.0, 'correction': [1.2523072995245457, -0.044137559831142426, -0.06576689332723618, 0.840450044721365]},
        ],
        "octave_octave1_1": [
            {'intermediate_frequency': 157000000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0789089314639568, -0.13434219360351562, -0.14752578735351562, 0.9824925884604454]},
            {'intermediate_frequency': 136800000.0, 'lo_frequency': 5900000000.0, 'correction': [1.096462655812502, -0.1716594696044922, -0.1885051727294922, 0.9984776265919209]},
            {'intermediate_frequency': 157100000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0455858372151852, -0.090911865234375, -0.096771240234375, 0.9822769500315189]},
            {'intermediate_frequency': 136710000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0058116912841797, -0.0625, -0.0625, 1.0058116912841797]},
            {'intermediate_frequency': 38800000.0, 'lo_frequency': 5900000000.0, 'correction': [1.127538651227951, -0.1143798828125, -0.1378173828125, 0.935787171125412]},
            {'intermediate_frequency': 229500000.0, 'lo_frequency': 5900000000.0, 'correction': [1.06640625, 0.0, 0.0, 0.94140625]},
            {'intermediate_frequency': 36100000.0, 'lo_frequency': 5900000000.0, 'correction': [1.055631846189499, -0.1212158203125, -0.1290283203125, 0.9917146861553192]},
            {'intermediate_frequency': 157100000.0, 'lo_frequency': 5950000000.0, 'correction': [1.0032808110117912, -0.046875, -0.046875, 1.0032808110117912]},
            {'intermediate_frequency': 136710000.0, 'lo_frequency': 5950000000.0, 'correction': [0.9697265625, 0.0, 0.0, 1.0322265625]},
            {'intermediate_frequency': 38800000.0, 'lo_frequency': 5950000000.0, 'correction': [1.055631846189499, -0.1212158203125, -0.1290283203125, 0.9917146861553192]},
            {'intermediate_frequency': 229500000.0, 'lo_frequency': 5950000000.0, 'correction': [1.0322265625, 0.0, 0.0, 0.9697265625]},
            {'intermediate_frequency': 36100000.0, 'lo_frequency': 5950000000.0, 'correction': [1.0455858372151852, -0.090911865234375, -0.096771240234375, 0.9822769500315189]},
            {'intermediate_frequency': 157100000.0, 'lo_frequency': 5960000000.0, 'correction': [0.9697265625, 0.0, 0.0, 1.0322265625]},
            {'intermediate_frequency': 136710000.0, 'lo_frequency': 5960000000.0, 'correction': [1.0337355360388756, -0.030303955078125, -0.032257080078125, 0.9711441695690155]},
            {'intermediate_frequency': 38800000.0, 'lo_frequency': 5960000000.0, 'correction': [1.1564223431050777, -0.17156982421875, -0.20672607421875, 0.9597588442265987]},
            {'intermediate_frequency': 229500000.0, 'lo_frequency': 5960000000.0, 'correction': [1.0322265625, 0.0, 0.0, 0.9697265625]},
            {'intermediate_frequency': 36100000.0, 'lo_frequency': 5960000000.0, 'correction': [1.090586543083191, -0.11767578125, -0.13330078125, 0.9627522230148315]},
            {'intermediate_frequency': 237000000.0, 'lo_frequency': 5960000000.0, 'correction': [0.9900021366775036, 0.004639901220798492, 0.004546832293272018, 1.010266449302435]},
            {'intermediate_frequency': 54400000.0, 'lo_frequency': 5960000000.0, 'correction': [1.0382255427539349, -0.06060791015625, -0.06451416015625, 0.9753623120486736]},
            {'intermediate_frequency': 123500000.0, 'lo_frequency': 5960000000.0, 'correction': [1.0726038739085197, -0.058837890625, -0.066650390625, 0.9468774124979973]},
            {'intermediate_frequency': 142600000.0, 'lo_frequency': 5960000000.0, 'correction': [1.0855363868176937, -0.14926910400390625, -0.16391754150390625, 0.9885277822613716]},
            {'intermediate_frequency': 50200000.0, 'lo_frequency': 5960000000.0, 'correction': [1.0488719940185547, -0.1875, -0.1875, 1.0488719940185547]},
            {'intermediate_frequency': 54500000.0, 'lo_frequency': 5960000000.0, 'correction': [1.0828662104904652, -0.1535702347755432, -0.1673336625099182, 0.9937989488244057]},
            {'intermediate_frequency': 124000000.0, 'lo_frequency': 5960000000.0, 'correction': [1.1054573729634285, -0.17039823532104492, -0.19005155563354492, 0.9911415092647076]},
            {'intermediate_frequency': 50500000.0, 'lo_frequency': 5960000000.0, 'correction': [1.0967981033027172, -0.16761727631092072, -0.18478341400623322, 0.9949069954454899]},
            {'intermediate_frequency': 237000000.0, 'lo_frequency': 6000000000.0, 'correction': [1.0047452114522457, 0.04827943444252014, 0.0484004020690918, 1.0022340379655361]},
            {'intermediate_frequency': 163122000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0789089314639568, -0.13434219360351562, -0.14752578735351562, 0.9824925884604454]},
            {'intermediate_frequency': 126410000.0, 'lo_frequency': 5900000000.0, 'correction': [1.096462655812502, -0.1716594696044922, -0.1885051727294922, 0.9984776265919209]},
            {'intermediate_frequency': 49753000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0886195003986359, -0.15085554867982864, -0.1663050726056099, 0.9874881729483604]},
            {'intermediate_frequency': 218194000.0, 'lo_frequency': 5900000000.0, 'correction': [1.1093690656125546, -0.17780685424804688, -0.19831466674804688, 0.9946486912667751]},
            {'intermediate_frequency': 28632000.0, 'lo_frequency': 5900000000.0, 'correction': [1.089952491223812, -0.1585984230041504, -0.1741623878479004, 0.9925492443144321]},
            {'intermediate_frequency': 163272000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0789089314639568, -0.13434219360351562, -0.14752578735351562, 0.9824925884604454]},
            {'intermediate_frequency': 126110000.0, 'lo_frequency': 5900000000.0, 'correction': [1.096462655812502, -0.1716594696044922, -0.1885051727294922, 0.9984776265919209]},
            {'intermediate_frequency': 50303000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0855363868176937, -0.14926910400390625, -0.16391754150390625, 0.9885277822613716]},
            {'intermediate_frequency': 217644000.0, 'lo_frequency': 5900000000.0, 'correction': [1.1093690656125546, -0.17780685424804688, -0.19831466674804688, 0.9946486912667751]},
            {'intermediate_frequency': 28031999.0, 'lo_frequency': 5900000000.0, 'correction': [1.089952491223812, -0.1585984230041504, -0.1741623878479004, 0.9925492443144321]},
            {'intermediate_frequency': 21500000.0, 'lo_frequency': 5880000000.0, 'correction': [1.0912747457623482, -0.156442791223526, -0.172464519739151, 0.9898967482149601]},
            {'intermediate_frequency': 129800000.0, 'lo_frequency': 5880000000.0, 'correction': [1.096462655812502, -0.1716594696044922, -0.1885051727294922, 0.9984776265919209]},
            {'intermediate_frequency': 28500000.0, 'lo_frequency': 5880000000.0, 'correction': [1.0908435992896557, -0.1505773365497589, -0.1666448414325714, 0.9856670163571835]},
            {'intermediate_frequency': 153000000.0, 'lo_frequency': 5880000000.0, 'correction': [1.1003425158560276, -0.1791229248046875, -0.1967010498046875, 1.002010766416788]},
            {'intermediate_frequency': 57900000.0, 'lo_frequency': 5880000000.0, 'correction': [1.0890531428158283, -0.15673255920410156, -0.17211341857910156, 0.9917302653193474]},
            {'intermediate_frequency': 34200000.0, 'lo_frequency': 5880000000.0, 'correction': [1.0930849835276604, -0.1601676195859909, -0.1765708178281784, 0.9915388189256191]},
            {'intermediate_frequency': 134400000.0, 'lo_frequency': 5880000000.0, 'correction': [1.1003425158560276, -0.1791229248046875, -0.1967010498046875, 1.002010766416788]},
            {'intermediate_frequency': 22200000.0, 'lo_frequency': 5880000000.0, 'correction': [1.0908435992896557, -0.1505773365497589, -0.1666448414325714, 0.9856670163571835]},
            {'intermediate_frequency': 157600000.0, 'lo_frequency': 5880000000.0, 'correction': [1.1003425158560276, -0.1791229248046875, -0.1967010498046875, 1.002010766416788]},
            {'intermediate_frequency': 63300000.0, 'lo_frequency': 5880000000.0, 'correction': [1.0926973298192024, -0.16419601440429688, -0.18030929565429688, 0.9950487911701202]},
            {'intermediate_frequency': 34300000.0, 'lo_frequency': 5880000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
            {'intermediate_frequency': 158000000.0, 'lo_frequency': 5880000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
        ],
    },
}




# Single QUA script generated at 2023-12-14 12:42:47.319890
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
        with for_(v12,-1200000,(v12<=1100000),(v12+100000)):
            update_frequency("rr1", (v12+-163122000), "Hz", False)
            update_frequency("rr2", (v12+126410000), "Hz", False)
            update_frequency("rr3", (v12+-49753000), "Hz", False)
            update_frequency("rr4", (v12+218194000), "Hz", False)
            update_frequency("rr5", (v12+28632000), "Hz", False)
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
                wait(1750, )
        r1 = declare_stream()
        save(v1, r1)
    with stream_processing():
        r1.save("n")
        r2.buffer(199).buffer(24).average().save("I1")
        r7.buffer(199).buffer(24).average().save("Q1")
        r3.buffer(199).buffer(24).average().save("I2")
        r8.buffer(199).buffer(24).average().save("Q2")
        r4.buffer(199).buffer(24).average().save("I3")
        r9.buffer(199).buffer(24).average().save("Q3")
        r5.buffer(199).buffer(24).average().save("I4")
        r10.buffer(199).buffer(24).average().save("Q4")
        r6.buffer(199).buffer(24).average().save("I5")
        r11.buffer(199).buffer(24).average().save("Q5")


config = {
    "version": 1,
    "controllers": {
        "con1": {
            "analog_outputs": {
                "1": {
                    "offset": 0.01953125,
                },
                "2": {
                    "offset": -0.001953125,
                },
                "3": {
                    "offset": -0.0018310546875,
                },
                "4": {
                    "offset": 0.0138702392578125,
                },
                "5": {
                    "offset": -0.0139617919921875,
                },
                "6": {
                    "offset": 0.01104736328125,
                },
                "7": {
                    "offset": 0.0152587890625,
                },
                "8": {
                    "offset": -0.00072479248046875,
                },
                "9": {
                    "offset": 0.0,
                },
                "10": {
                    "offset": 0.0,
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
                    "offset": 0.0,
                },
                "2": {
                    "offset": 0.0,
                },
                "3": {
                    "offset": 0.0,
                },
                "4": {
                    "offset": 0.0,
                },
                "5": {
                    "offset": -0.20299999999999996,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "6": {
                    "offset": 0.044,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "7": {
                    "offset": -0.116,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "8": {
                    "offset": 0.033,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "9": {
                    "offset": 0.037,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
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
                "lo_frequency": 5900000000,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": -163122000,
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
                "lo_frequency": 5900000000,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": 126410000,
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
                "lo_frequency": 5900000000,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": -49753000,
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
                "lo_frequency": 5900000000,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": 218194000,
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
                "lo_frequency": 5900000000,
                "mixer": "octave_octave1_1",
            },
            "intermediate_frequency": 28632000,
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
            "intermediate_frequency": -131235000,
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
            "intermediate_frequency": -106443000,
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
            "intermediate_frequency": -262792000,
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
            "intermediate_frequency": -368508000,
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
            "intermediate_frequency": -368508000,
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
            "intermediate_frequency": -122908000,
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
            "length": 360,
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
            "length": 40,
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
            "length": 64,
            "waveforms": {
                "single": "cz_3c2t_wf",
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
            "length": 32,
            "waveforms": {
                "I": "x90_I_wf_q1",
                "Q": "x90_Q_wf_q1",
            },
        },
        "x180_pulse_q1": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "I": "x180_I_wf_q1",
                "Q": "x180_Q_wf_q1",
            },
        },
        "-x90_pulse_q1": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "I": "minus_x90_I_wf_q1",
                "Q": "minus_x90_Q_wf_q1",
            },
        },
        "y90_pulse_q1": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "I": "y90_I_wf_q1",
                "Q": "y90_Q_wf_q1",
            },
        },
        "y180_pulse_q1": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "I": "y180_I_wf_q1",
                "Q": "y180_Q_wf_q1",
            },
        },
        "-y90_pulse_q1": {
            "operation": "control",
            "length": 32,
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
            "length": 32,
            "waveforms": {
                "I": "x90_I_wf_q2",
                "Q": "x90_Q_wf_q2",
            },
        },
        "x180_pulse_q2": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "I": "x180_I_wf_q2",
                "Q": "x180_Q_wf_q2",
            },
        },
        "-x90_pulse_q2": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "I": "minus_x90_I_wf_q2",
                "Q": "minus_x90_Q_wf_q2",
            },
        },
        "y90_pulse_q2": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "I": "y90_I_wf_q2",
                "Q": "y90_Q_wf_q2",
            },
        },
        "y180_pulse_q2": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "I": "y180_I_wf_q2",
                "Q": "y180_Q_wf_q2",
            },
        },
        "-y90_pulse_q2": {
            "operation": "control",
            "length": 32,
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
            "length": 32,
            "waveforms": {
                "I": "x90_I_wf_q3",
                "Q": "x90_Q_wf_q3",
            },
        },
        "x180_pulse_q3": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "I": "x180_I_wf_q3",
                "Q": "x180_Q_wf_q3",
            },
        },
        "-x90_pulse_q3": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "I": "minus_x90_I_wf_q3",
                "Q": "minus_x90_Q_wf_q3",
            },
        },
        "y90_pulse_q3": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "I": "y90_I_wf_q3",
                "Q": "y90_Q_wf_q3",
            },
        },
        "y180_pulse_q3": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "I": "y180_I_wf_q3",
                "Q": "y180_Q_wf_q3",
            },
        },
        "-y90_pulse_q3": {
            "operation": "control",
            "length": 32,
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
            "length": 32,
            "waveforms": {
                "I": "x90_I_wf_q4",
                "Q": "x90_Q_wf_q4",
            },
        },
        "x180_pulse_q4": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "I": "x180_I_wf_q4",
                "Q": "x180_Q_wf_q4",
            },
        },
        "-x90_pulse_q4": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "I": "minus_x90_I_wf_q4",
                "Q": "minus_x90_Q_wf_q4",
            },
        },
        "y90_pulse_q4": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "I": "y90_I_wf_q4",
                "Q": "y90_Q_wf_q4",
            },
        },
        "y180_pulse_q4": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "I": "y180_I_wf_q4",
                "Q": "y180_Q_wf_q4",
            },
        },
        "-y90_pulse_q4": {
            "operation": "control",
            "length": 32,
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
            "length": 32,
            "waveforms": {
                "I": "x90_I_wf_q5",
                "Q": "x90_Q_wf_q5",
            },
        },
        "x180_pulse_q5": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "I": "x180_I_wf_q5",
                "Q": "x180_Q_wf_q5",
            },
        },
        "-x90_pulse_q5": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "I": "minus_x90_I_wf_q5",
                "Q": "minus_x90_Q_wf_q5",
            },
        },
        "y90_pulse_q5": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "I": "y90_I_wf_q5",
                "Q": "y90_Q_wf_q5",
            },
        },
        "y180_pulse_q5": {
            "operation": "control",
            "length": 32,
            "waveforms": {
                "I": "y180_I_wf_q5",
                "Q": "y180_Q_wf_q5",
            },
        },
        "-y90_pulse_q5": {
            "operation": "control",
            "length": 32,
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
            "samples": [0.0, 0.00039408485680079226, 0.0008552891680868398, 0.0013839759753206781, 0.001977104938193513, 0.0026276783406505716, 0.0033244048316005406, 0.004051659489571117, 0.004789799324340885, 0.005515862361583035, 0.0062046385889545225, 0.006830056759396672, 0.007366788223346909, 0.007791934005011461, 0.008086640125007488] + [0.008237482958741243] * 2 + [0.008086640125007488, 0.007791934005011461, 0.007366788223346909, 0.006830056759396672, 0.0062046385889545225, 0.005515862361583035, 0.004789799324340885, 0.004051659489571117, 0.0033244048316005406, 0.0026276783406505716, 0.001977104938193513, 0.0013839759753206781, 0.0008552891680868398, 0.00039408485680079226, 0.0],
        },
        "x90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.0002632848221374642, -0.00031135073611762265, -0.00036075933775814593, -0.0004092699818010895, -0.00045417992565017264, -0.0004924518322689368, -0.0005209026618169576, -0.000536444205609312, -0.0005363566956554597, -0.0005185692479126707, -0.0004819158377872311, -0.00042633430538791786, -0.00035297928223602574, -0.00026422793691546027, -0.00016356925919376895, -5.5381700073764175e-05, 5.5381700073764175e-05, 0.00016356925919376895, 0.00026422793691546027, 0.00035297928223602574, 0.00042633430538791786, 0.0004819158377872311, 0.0005185692479126707, 0.0005363566956554597, 0.000536444205609312, 0.0005209026618169576, 0.0004924518322689368, 0.00045417992565017264, 0.0004092699818010895, 0.00036075933775814593, 0.00031135073611762265, 0.0002632848221374642],
        },
        "x180_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007890929523558408, 0.0017125820571805804, 0.002771194247911413, 0.003958841721200831, 0.005261512651102933, 0.006656597882723868, 0.008112810967974766, 0.009590819907974099, 0.011044646960109398, 0.012423813039164868, 0.013676114572843573, 0.014750834923554378, 0.01560212249334013, 0.016192225153444505] + [0.016494264206604208] * 2 + [0.016192225153444505, 0.01560212249334013, 0.014750834923554378, 0.013676114572843573, 0.012423813039164868, 0.011044646960109398, 0.009590819907974099, 0.008112810967974766, 0.006656597882723868, 0.005261512651102933, 0.003958841721200831, 0.002771194247911413, 0.0017125820571805804, 0.0007890929523558408, 0.0],
        },
        "x180_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.0005271864524242647, -0.0006234308863723009, -0.0007223638412105082, -0.0008194987771714698, -0.000909423877236712, -0.0009860573516392917, -0.001043025663660398, -0.0010741451610570606, -0.0010739699361361986, -0.0010383533692673844, -0.0009649606795695586, -0.0008536674016357496, -0.0007067855035111596, -0.0005290748914539217, -0.0003275217187985322, -0.00011089314512732731, 0.00011089314512732731, 0.0003275217187985322, 0.0005290748914539217, 0.0007067855035111596, 0.0008536674016357496, 0.0009649606795695586, 0.0010383533692673844, 0.0010739699361361986, 0.0010741451610570606, 0.001043025663660398, 0.0009860573516392917, 0.000909423877236712, 0.0008194987771714698, 0.0007223638412105082, 0.0006234308863723009, 0.0005271864524242647],
        },
        "minus_x90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, -0.00039408485680079226, -0.0008552891680868398, -0.0013839759753206781, -0.001977104938193513, -0.0026276783406505716, -0.0033244048316005406, -0.004051659489571117, -0.004789799324340885, -0.005515862361583035, -0.0062046385889545225, -0.006830056759396672, -0.007366788223346909, -0.007791934005011461, -0.008086640125007488] + [-0.008237482958741243] * 2 + [-0.008086640125007488, -0.007791934005011461, -0.007366788223346909, -0.006830056759396672, -0.0062046385889545225, -0.005515862361583035, -0.004789799324340885, -0.004051659489571117, -0.0033244048316005406, -0.0026276783406505716, -0.001977104938193513, -0.0013839759753206781, -0.0008552891680868398, -0.00039408485680079226, 0.0],
        },
        "minus_x90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0002632848221374642, 0.00031135073611762265, 0.00036075933775814593, 0.0004092699818010895, 0.00045417992565017264, 0.0004924518322689368, 0.0005209026618169576, 0.000536444205609312, 0.0005363566956554597, 0.0005185692479126707, 0.0004819158377872311, 0.00042633430538791786, 0.00035297928223602574, 0.00026422793691546027, 0.00016356925919376895, 5.5381700073764175e-05, -5.5381700073764175e-05, -0.00016356925919376895, -0.00026422793691546027, -0.00035297928223602574, -0.00042633430538791786, -0.0004819158377872311, -0.0005185692479126707, -0.0005363566956554597, -0.000536444205609312, -0.0005209026618169576, -0.0004924518322689368, -0.00045417992565017264, -0.0004092699818010895, -0.00036075933775814593, -0.00031135073611762265, -0.0002632848221374642],
        },
        "y90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.00026359322621213237, 0.00031171544318615044, 0.0003611819206052541, 0.0004097493885857349, 0.000454711938618356, 0.0004930286758196459, 0.000521512831830199, 0.0005370725805285303, 0.0005369849680680993, 0.0005191766846336922, 0.0004824803397847793, 0.0004268337008178748, 0.0003533927517555798, 0.00026453744572696084, 0.0001637608593992661, 5.5446572563663654e-05, -5.5446572563663654e-05, -0.0001637608593992661, -0.00026453744572696084, -0.0003533927517555798, -0.0004268337008178748, -0.0004824803397847793, -0.0005191766846336922, -0.0005369849680680993, -0.0005370725805285303, -0.000521512831830199, -0.0004930286758196459, -0.000454711938618356, -0.0004097493885857349, -0.0003611819206052541, -0.00031171544318615044, -0.00026359322621213237],
        },
        "y90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0003945464761779204, 0.0008562910285902902, 0.0013855971239557065, 0.0019794208606004155, 0.0026307563255514666, 0.003328298941361934, 0.004056405483987383, 0.0047954099539870496, 0.005522323480054699, 0.006211906519582434, 0.006838057286421786, 0.007375417461777189, 0.007801061246670065, 0.008096112576722252] + [0.008247132103302104] * 2 + [0.008096112576722252, 0.007801061246670065, 0.007375417461777189, 0.006838057286421786, 0.006211906519582434, 0.005522323480054699, 0.0047954099539870496, 0.004056405483987383, 0.003328298941361934, 0.0026307563255514666, 0.0019794208606004155, 0.0013855971239557065, 0.0008562910285902902, 0.0003945464761779204, 0.0],
        },
        "y180_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0005271864524242647, 0.0006234308863723009, 0.0007223638412105082, 0.0008194987771714698, 0.000909423877236712, 0.0009860573516392917, 0.001043025663660398, 0.0010741451610570606, 0.0010739699361361986, 0.0010383533692673844, 0.0009649606795695586, 0.0008536674016357496, 0.0007067855035111596, 0.0005290748914539217, 0.0003275217187985322, 0.00011089314512732731, -0.00011089314512732731, -0.0003275217187985322, -0.0005290748914539217, -0.0007067855035111596, -0.0008536674016357496, -0.0009649606795695586, -0.0010383533692673844, -0.0010739699361361986, -0.0010741451610570606, -0.001043025663660398, -0.0009860573516392917, -0.000909423877236712, -0.0008194987771714698, -0.0007223638412105082, -0.0006234308863723009, -0.0005271864524242647],
        },
        "y180_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007890929523558408, 0.0017125820571805804, 0.002771194247911413, 0.003958841721200831, 0.005261512651102933, 0.006656597882723868, 0.008112810967974766, 0.009590819907974099, 0.011044646960109398, 0.012423813039164868, 0.013676114572843573, 0.014750834923554378, 0.01560212249334013, 0.016192225153444505] + [0.016494264206604208] * 2 + [0.016192225153444505, 0.01560212249334013, 0.014750834923554378, 0.013676114572843573, 0.012423813039164868, 0.011044646960109398, 0.009590819907974099, 0.008112810967974766, 0.006656597882723868, 0.005261512651102933, 0.003958841721200831, 0.002771194247911413, 0.0017125820571805804, 0.0007890929523558408, 0.0],
        },
        "minus_y90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.00026359322621213237, -0.00031171544318615044, -0.0003611819206052541, -0.0004097493885857349, -0.000454711938618356, -0.0004930286758196459, -0.000521512831830199, -0.0005370725805285303, -0.0005369849680680993, -0.0005191766846336922, -0.0004824803397847793, -0.0004268337008178748, -0.0003533927517555798, -0.00026453744572696084, -0.0001637608593992661, -5.5446572563663654e-05, 5.5446572563663654e-05, 0.0001637608593992661, 0.00026453744572696084, 0.0003533927517555798, 0.0004268337008178748, 0.0004824803397847793, 0.0005191766846336922, 0.0005369849680680993, 0.0005370725805285303, 0.000521512831830199, 0.0004930286758196459, 0.000454711938618356, 0.0004097493885857349, 0.0003611819206052541, 0.00031171544318615044, 0.00026359322621213237],
        },
        "minus_y90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, -0.0003945464761779204, -0.0008562910285902902, -0.0013855971239557065, -0.0019794208606004155, -0.0026307563255514666, -0.003328298941361934, -0.004056405483987383, -0.0047954099539870496, -0.005522323480054699, -0.006211906519582434, -0.006838057286421786, -0.007375417461777189, -0.007801061246670065, -0.008096112576722252] + [-0.008247132103302104] * 2 + [-0.008096112576722252, -0.007801061246670065, -0.007375417461777189, -0.006838057286421786, -0.006211906519582434, -0.005522323480054699, -0.0047954099539870496, -0.004056405483987383, -0.003328298941361934, -0.0026307563255514666, -0.0019794208606004155, -0.0013855971239557065, -0.0008562910285902902, -0.0003945464761779204, 0.0],
        },
        "readout_wf_q1": {
            "type": "constant",
            "sample": 0.0868910316,
        },
        "x90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0012451006481807685, 0.0027022634318202843, 0.004372635370786272, 0.006246610590547289, 0.008302079992909828, 0.010503368853712294, 0.012801110648163878, 0.015133243869878767, 0.01742722077025806, 0.01960339098424132, 0.0215793830985366, 0.023275171916936357, 0.024618408733035172, 0.025549524899255625] + [0.026026108829884206] * 2 + [0.025549524899255625, 0.024618408733035172, 0.023275171916936357, 0.0215793830985366, 0.01960339098424132, 0.01742722077025806, 0.015133243869878767, 0.012801110648163878, 0.010503368853712294, 0.008302079992909828, 0.006246610590547289, 0.004372635370786272, 0.0027022634318202843, 0.0012451006481807685, 0.0],
        },
        "x90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.000483561125459141, 0.0005718412141925976, 0.0006625873454077859, 0.0007516842460179772, 0.0008341679335152796, 0.0009044598937118083, 0.0009567140078867002, 0.0009852583286211463, 0.0009850976037778755, 0.0009524283515979763, 0.0008851089971882523, 0.0007830253748071536, 0.0006482981343022296, 0.0004852932938377907, 0.00030041889397239936, 0.00010171660105620371, -0.00010171660105620371, -0.00030041889397239936, -0.0004852932938377907, -0.0006482981343022296, -0.0007830253748071536, -0.0008851089971882523, -0.0009524283515979763, -0.0009850976037778755, -0.0009852583286211463, -0.0009567140078867002, -0.0009044598937118083, -0.0008341679335152796, -0.0007516842460179772, -0.0006625873454077859, -0.0005718412141925976, -0.000483561125459141],
        },
        "x180_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0024543135459211152, 0.005326639059303513, 0.008619237519131436, 0.012313174048118136, 0.01636486770422195, 0.020703997297838846, 0.025233252679234222, 0.02983029964512457, 0.03435213375456568, 0.0386417500536279, 0.04253677992116044, 0.04587947954476214, 0.048527236830848336, 0.050362631441653496] + [0.05130206264219065] * 2 + [0.050362631441653496, 0.048527236830848336, 0.04587947954476214, 0.04253677992116044, 0.0386417500536279, 0.03435213375456568, 0.02983029964512457, 0.025233252679234222, 0.020703997297838846, 0.01636486770422195, 0.012313174048118136, 0.008619237519131436, 0.005326639059303513, 0.0024543135459211152, 0.0],
        },
        "x180_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.000953184485309917, 0.0011272001505737777, 0.001306076821633896, 0.0014817025675418144, 0.001644292501004577, 0.0017828503841217026, 0.0018858524831383003, 0.001942118386734149, 0.0019418015696474483, 0.0018774046967702299, 0.001744706345298115, 0.0015434814743668364, 0.0012779102598156733, 0.0009565988954796877, 0.0005921787624192545, 0.0002005014070003524, -0.0002005014070003524, -0.0005921787624192545, -0.0009565988954796877, -0.0012779102598156733, -0.0015434814743668364, -0.001744706345298115, -0.0018774046967702299, -0.0019418015696474483, -0.001942118386734149, -0.0018858524831383003, -0.0017828503841217026, -0.001644292501004577, -0.0014817025675418144, -0.001306076821633896, -0.0011272001505737777, -0.000953184485309917],
        },
        "minus_x90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, -0.0012451006481807685, -0.0027022634318202843, -0.004372635370786272, -0.006246610590547289, -0.008302079992909828, -0.010503368853712294, -0.012801110648163878, -0.015133243869878767, -0.01742722077025806, -0.01960339098424132, -0.0215793830985366, -0.023275171916936357, -0.024618408733035172, -0.025549524899255625] + [-0.026026108829884206] * 2 + [-0.025549524899255625, -0.024618408733035172, -0.023275171916936357, -0.0215793830985366, -0.01960339098424132, -0.01742722077025806, -0.015133243869878767, -0.012801110648163878, -0.010503368853712294, -0.008302079992909828, -0.006246610590547289, -0.004372635370786272, -0.0027022634318202843, -0.0012451006481807685, 0.0],
        },
        "minus_x90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.000483561125459141, -0.0005718412141925976, -0.0006625873454077859, -0.0007516842460179772, -0.0008341679335152796, -0.0009044598937118083, -0.0009567140078867002, -0.0009852583286211463, -0.0009850976037778755, -0.0009524283515979763, -0.0008851089971882523, -0.0007830253748071536, -0.0006482981343022296, -0.0004852932938377907, -0.00030041889397239936, -0.00010171660105620371, 0.00010171660105620371, 0.00030041889397239936, 0.0004852932938377907, 0.0006482981343022296, 0.0007830253748071536, 0.0008851089971882523, 0.0009524283515979763, 0.0009850976037778755, 0.0009852583286211463, 0.0009567140078867002, 0.0009044598937118083, 0.0008341679335152796, 0.0007516842460179772, 0.0006625873454077859, 0.0005718412141925976, 0.000483561125459141],
        },
        "y90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.0004765922426549585, -0.0005636000752868888, -0.000653038410816948, -0.0007408512837709072, -0.0008221462505022885, -0.0008914251920608513, -0.0009429262415691502, -0.0009710591933670746, -0.0009709007848237241, -0.0009387023483851149, -0.0008723531726490575, -0.0007717407371834182, -0.0006389551299078366, -0.00047829944773984385, -0.00029608938120962726, -0.0001002507035001762, 0.0001002507035001762, 0.00029608938120962726, 0.00047829944773984385, 0.0006389551299078366, 0.0007717407371834182, 0.0008723531726490575, 0.0009387023483851149, 0.0009709007848237241, 0.0009710591933670746, 0.0009429262415691502, 0.0008914251920608513, 0.0008221462505022885, 0.0007408512837709072, 0.000653038410816948, 0.0005636000752868888, 0.0004765922426549585],
        },
        "y90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0012271567729605576, 0.0026633195296517564, 0.004309618759565718, 0.006156587024059068, 0.008182433852110975, 0.010351998648919423, 0.012616626339617111, 0.014915149822562285, 0.01717606687728284, 0.01932087502681395, 0.02126838996058022, 0.02293973977238107, 0.024263618415424168, 0.025181315720826748] + [0.025651031321095325] * 2 + [0.025181315720826748, 0.024263618415424168, 0.02293973977238107, 0.02126838996058022, 0.01932087502681395, 0.01717606687728284, 0.014915149822562285, 0.012616626339617111, 0.010351998648919423, 0.008182433852110975, 0.006156587024059068, 0.004309618759565718, 0.0026633195296517564, 0.0012271567729605576, 0.0],
        },
        "y180_I_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.000953184485309917, -0.0011272001505737777, -0.001306076821633896, -0.0014817025675418144, -0.001644292501004577, -0.0017828503841217026, -0.0018858524831383003, -0.001942118386734149, -0.0019418015696474483, -0.0018774046967702299, -0.001744706345298115, -0.0015434814743668364, -0.0012779102598156733, -0.0009565988954796877, -0.0005921787624192545, -0.0002005014070003524, 0.0002005014070003524, 0.0005921787624192545, 0.0009565988954796877, 0.0012779102598156733, 0.0015434814743668364, 0.001744706345298115, 0.0018774046967702299, 0.0019418015696474483, 0.001942118386734149, 0.0018858524831383003, 0.0017828503841217026, 0.001644292501004577, 0.0014817025675418144, 0.001306076821633896, 0.0011272001505737777, 0.000953184485309917],
        },
        "y180_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0024543135459211152, 0.005326639059303513, 0.008619237519131436, 0.012313174048118136, 0.01636486770422195, 0.020703997297838846, 0.025233252679234222, 0.02983029964512457, 0.03435213375456568, 0.0386417500536279, 0.04253677992116044, 0.04587947954476214, 0.048527236830848336, 0.050362631441653496] + [0.05130206264219065] * 2 + [0.050362631441653496, 0.048527236830848336, 0.04587947954476214, 0.04253677992116044, 0.0386417500536279, 0.03435213375456568, 0.02983029964512457, 0.025233252679234222, 0.020703997297838846, 0.01636486770422195, 0.012313174048118136, 0.008619237519131436, 0.005326639059303513, 0.0024543135459211152, 0.0],
        },
        "minus_y90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0004765922426549585, 0.0005636000752868888, 0.000653038410816948, 0.0007408512837709072, 0.0008221462505022885, 0.0008914251920608513, 0.0009429262415691502, 0.0009710591933670746, 0.0009709007848237241, 0.0009387023483851149, 0.0008723531726490575, 0.0007717407371834182, 0.0006389551299078366, 0.00047829944773984385, 0.00029608938120962726, 0.0001002507035001762, -0.0001002507035001762, -0.00029608938120962726, -0.00047829944773984385, -0.0006389551299078366, -0.0007717407371834182, -0.0008723531726490575, -0.0009387023483851149, -0.0009709007848237241, -0.0009710591933670746, -0.0009429262415691502, -0.0008914251920608513, -0.0008221462505022885, -0.0007408512837709072, -0.000653038410816948, -0.0005636000752868888, -0.0004765922426549585],
        },
        "minus_y90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, -0.0012271567729605576, -0.0026633195296517564, -0.004309618759565718, -0.006156587024059068, -0.008182433852110975, -0.010351998648919423, -0.012616626339617111, -0.014915149822562285, -0.01717606687728284, -0.01932087502681395, -0.02126838996058022, -0.02293973977238107, -0.024263618415424168, -0.025181315720826748] + [-0.025651031321095325] * 2 + [-0.025181315720826748, -0.024263618415424168, -0.02293973977238107, -0.02126838996058022, -0.01932087502681395, -0.01717606687728284, -0.014915149822562285, -0.012616626339617111, -0.010351998648919423, -0.008182433852110975, -0.006156587024059068, -0.004309618759565718, -0.0026633195296517564, -0.0012271567729605576, 0.0],
        },
        "readout_wf_q2": {
            "type": "constant",
            "sample": 0.1309075425,
        },
        "x90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.00042906451058445866, 0.0009312061145726083, 0.0015068200776153797, 0.0021525961935373976, 0.0028609156168985608, 0.0036194847567470093, 0.004411291796544398, 0.005214950200268544, 0.006005459849019764, 0.006755373046137981, 0.0074363044155639196, 0.00802067709297309, 0.008483559549857644, 0.008804424295001246] + [0.00896865619966401] * 2 + [0.008804424295001246, 0.008483559549857644, 0.00802067709297309, 0.0074363044155639196, 0.006755373046137981, 0.006005459849019764, 0.005214950200268544, 0.004411291796544398, 0.0036194847567470093, 0.0028609156168985608, 0.0021525961935373976, 0.0015068200776153797, 0.0009312061145726083, 0.00042906451058445866, 0.0],
        },
        "x90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.00038493898076757147, -0.00045521437221236814, -0.0005274528575236247, -0.0005983784723109421, -0.0006640396367914714, -0.0007199955730518868, -0.0007615924765091205, -0.0007843151916979962, -0.0007841872466377023, -0.0007581808785190316, -0.0007045912859979105, -0.0006233275874011091, -0.0005160779266837588, -0.00038631787393141336, -0.00023914855177668305, -8.097153115966341e-05, 8.097153115966341e-05, 0.00023914855177668305, 0.00038631787393141336, 0.0005160779266837588, 0.0006233275874011091, 0.0007045912859979105, 0.0007581808785190316, 0.0007841872466377023, 0.0007843151916979962, 0.0007615924765091205, 0.0007199955730518868, 0.0006640396367914714, 0.0005983784723109421, 0.0005274528575236247, 0.00045521437221236814, 0.00038493898076757147],
        },
        "x180_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0008581290211689173, 0.0018624122291452166, 0.0030136401552307594, 0.004305192387074795, 0.0057218312337971216, 0.007238969513494019, 0.008822583593088795, 0.010429900400537089, 0.012010919698039527, 0.013510746092275962, 0.014872608831127839, 0.01604135418594618, 0.016967119099715287, 0.01760884859000249] + [0.01793731239932802] * 2 + [0.01760884859000249, 0.016967119099715287, 0.01604135418594618, 0.014872608831127839, 0.013510746092275962, 0.012010919698039527, 0.010429900400537089, 0.008822583593088795, 0.007238969513494019, 0.0057218312337971216, 0.004305192387074795, 0.0030136401552307594, 0.0018624122291452166, 0.0008581290211689173, 0.0],
        },
        "x180_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.0007698779615351429, -0.0009104287444247363, -0.0010549057150472494, -0.0011967569446218842, -0.0013280792735829428, -0.0014399911461037737, -0.001523184953018241, -0.0015686303833959924, -0.0015683744932754047, -0.0015163617570380632, -0.001409182571995821, -0.0012466551748022182, -0.0010321558533675176, -0.0007726357478628267, -0.0004782971035533661, -0.00016194306231932681, 0.00016194306231932681, 0.0004782971035533661, 0.0007726357478628267, 0.0010321558533675176, 0.0012466551748022182, 0.001409182571995821, 0.0015163617570380632, 0.0015683744932754047, 0.0015686303833959924, 0.001523184953018241, 0.0014399911461037737, 0.0013280792735829428, 0.0011967569446218842, 0.0010549057150472494, 0.0009104287444247363, 0.0007698779615351429],
        },
        "minus_x90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, -0.00042906451058445866, -0.0009312061145726083, -0.0015068200776153797, -0.0021525961935373976, -0.0028609156168985608, -0.0036194847567470093, -0.004411291796544398, -0.005214950200268544, -0.006005459849019764, -0.006755373046137981, -0.0074363044155639196, -0.00802067709297309, -0.008483559549857644, -0.008804424295001246] + [-0.00896865619966401] * 2 + [-0.008804424295001246, -0.008483559549857644, -0.00802067709297309, -0.0074363044155639196, -0.006755373046137981, -0.006005459849019764, -0.005214950200268544, -0.004411291796544398, -0.0036194847567470093, -0.0028609156168985608, -0.0021525961935373976, -0.0015068200776153797, -0.0009312061145726083, -0.00042906451058445866, 0.0],
        },
        "minus_x90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.00038493898076757147, 0.00045521437221236814, 0.0005274528575236247, 0.0005983784723109421, 0.0006640396367914714, 0.0007199955730518868, 0.0007615924765091205, 0.0007843151916979962, 0.0007841872466377023, 0.0007581808785190316, 0.0007045912859979105, 0.0006233275874011091, 0.0005160779266837588, 0.00038631787393141336, 0.00023914855177668305, 8.097153115966341e-05, -8.097153115966341e-05, -0.00023914855177668305, -0.00038631787393141336, -0.0005160779266837588, -0.0006233275874011091, -0.0007045912859979105, -0.0007581808785190316, -0.0007841872466377023, -0.0007843151916979962, -0.0007615924765091205, -0.0007199955730518868, -0.0006640396367914714, -0.0005983784723109421, -0.0005274528575236247, -0.00045521437221236814, -0.00038493898076757147],
        },
        "y90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.00038493898076757147, 0.00045521437221236814, 0.0005274528575236247, 0.0005983784723109421, 0.0006640396367914714, 0.0007199955730518868, 0.0007615924765091205, 0.0007843151916979962, 0.0007841872466377023, 0.0007581808785190316, 0.0007045912859979105, 0.0006233275874011091, 0.0005160779266837588, 0.00038631787393141336, 0.00023914855177668305, 8.097153115966341e-05, -8.097153115966341e-05, -0.00023914855177668305, -0.00038631787393141336, -0.0005160779266837588, -0.0006233275874011091, -0.0007045912859979105, -0.0007581808785190316, -0.0007841872466377023, -0.0007843151916979962, -0.0007615924765091205, -0.0007199955730518868, -0.0006640396367914714, -0.0005983784723109421, -0.0005274528575236247, -0.00045521437221236814, -0.00038493898076757147],
        },
        "y90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.00042906451058445866, 0.0009312061145726083, 0.0015068200776153797, 0.0021525961935373976, 0.0028609156168985608, 0.0036194847567470093, 0.004411291796544398, 0.005214950200268544, 0.006005459849019764, 0.006755373046137981, 0.0074363044155639196, 0.00802067709297309, 0.008483559549857644, 0.008804424295001246] + [0.00896865619966401] * 2 + [0.008804424295001246, 0.008483559549857644, 0.00802067709297309, 0.0074363044155639196, 0.006755373046137981, 0.006005459849019764, 0.005214950200268544, 0.004411291796544398, 0.0036194847567470093, 0.0028609156168985608, 0.0021525961935373976, 0.0015068200776153797, 0.0009312061145726083, 0.00042906451058445866, 0.0],
        },
        "y180_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0007698779615351429, 0.0009104287444247363, 0.0010549057150472494, 0.0011967569446218842, 0.0013280792735829428, 0.0014399911461037737, 0.001523184953018241, 0.0015686303833959924, 0.0015683744932754047, 0.0015163617570380632, 0.001409182571995821, 0.0012466551748022182, 0.0010321558533675176, 0.0007726357478628267, 0.0004782971035533661, 0.00016194306231932681, -0.00016194306231932681, -0.0004782971035533661, -0.0007726357478628267, -0.0010321558533675176, -0.0012466551748022182, -0.001409182571995821, -0.0015163617570380632, -0.0015683744932754047, -0.0015686303833959924, -0.001523184953018241, -0.0014399911461037737, -0.0013280792735829428, -0.0011967569446218842, -0.0010549057150472494, -0.0009104287444247363, -0.0007698779615351429],
        },
        "y180_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0008581290211689173, 0.0018624122291452166, 0.0030136401552307594, 0.004305192387074795, 0.0057218312337971216, 0.007238969513494019, 0.008822583593088795, 0.010429900400537089, 0.012010919698039527, 0.013510746092275962, 0.014872608831127839, 0.01604135418594618, 0.016967119099715287, 0.01760884859000249] + [0.01793731239932802] * 2 + [0.01760884859000249, 0.016967119099715287, 0.01604135418594618, 0.014872608831127839, 0.013510746092275962, 0.012010919698039527, 0.010429900400537089, 0.008822583593088795, 0.007238969513494019, 0.0057218312337971216, 0.004305192387074795, 0.0030136401552307594, 0.0018624122291452166, 0.0008581290211689173, 0.0],
        },
        "minus_y90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.00038493898076757147, -0.00045521437221236814, -0.0005274528575236247, -0.0005983784723109421, -0.0006640396367914714, -0.0007199955730518868, -0.0007615924765091205, -0.0007843151916979962, -0.0007841872466377023, -0.0007581808785190316, -0.0007045912859979105, -0.0006233275874011091, -0.0005160779266837588, -0.00038631787393141336, -0.00023914855177668305, -8.097153115966341e-05, 8.097153115966341e-05, 0.00023914855177668305, 0.00038631787393141336, 0.0005160779266837588, 0.0006233275874011091, 0.0007045912859979105, 0.0007581808785190316, 0.0007841872466377023, 0.0007843151916979962, 0.0007615924765091205, 0.0007199955730518868, 0.0006640396367914714, 0.0005983784723109421, 0.0005274528575236247, 0.00045521437221236814, 0.00038493898076757147],
        },
        "minus_y90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, -0.00042906451058445866, -0.0009312061145726083, -0.0015068200776153797, -0.0021525961935373976, -0.0028609156168985608, -0.0036194847567470093, -0.004411291796544398, -0.005214950200268544, -0.006005459849019764, -0.006755373046137981, -0.0074363044155639196, -0.00802067709297309, -0.008483559549857644, -0.008804424295001246] + [-0.00896865619966401] * 2 + [-0.008804424295001246, -0.008483559549857644, -0.00802067709297309, -0.0074363044155639196, -0.006755373046137981, -0.006005459849019764, -0.005214950200268544, -0.004411291796544398, -0.0036194847567470093, -0.0028609156168985608, -0.0021525961935373976, -0.0015068200776153797, -0.0009312061145726083, -0.00042906451058445866, 0.0],
        },
        "readout_wf_q3": {
            "type": "constant",
            "sample": 0.102461516,
        },
        "x90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0016968708271060682, 0.003682748050377406, 0.005959194872398877, 0.008513120039636026, 0.011314392426711162, 0.014314393153870814, 0.017445843631327455, 0.020624164062398618, 0.023750483598089428, 0.026716251671795588, 0.029409209368218295, 0.03172029528651704, 0.03355090984001778, 0.03481987059545138] + [0.03546937742024726] * 2 + [0.03481987059545138, 0.03355090984001778, 0.03172029528651704, 0.029409209368218295, 0.026716251671795588, 0.023750483598089428, 0.020624164062398618, 0.017445843631327455, 0.014314393153870814, 0.011314392426711162, 0.008513120039636026, 0.005959194872398877, 0.003682748050377406, 0.0016968708271060682, 0.0],
        },
        "x90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0013682867578607449, 0.0016180844980783187, 0.0018748601633076928, 0.0021269691581232006, 0.002360365375064587, 0.0025592638250375097, 0.002707122303945135, 0.0027878914435983436, 0.0027874366558515037, 0.0026949955914368946, 0.0025045084403055896, 0.0022156521585565384, 0.0018344273466344232, 0.0013731881093758014, 0.000850066667462784, 0.0002878177565404143, -0.0002878177565404143, -0.000850066667462784, -0.0013731881093758014, -0.0018344273466344232, -0.0022156521585565384, -0.0025045084403055896, -0.0026949955914368946, -0.0027874366558515037, -0.0027878914435983436, -0.002707122303945135, -0.0025592638250375097, -0.002360365375064587, -0.0021269691581232006, -0.0018748601633076928, -0.0016180844980783187, -0.0013682867578607449],
        },
        "x180_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0033695215815437857, 0.007312930858914043, 0.011833331925104714, 0.016904729129410285, 0.022467290293909772, 0.02842447161457115, 0.03464267620432228, 0.040953951708905166, 0.04716196765097761, 0.053051172280212354, 0.05839865007954254, 0.06298783492149682, 0.06662293498154592, 0.06914274414041854] + [0.07043248713590755] * 2 + [0.06914274414041854, 0.06662293498154592, 0.06298783492149682, 0.05839865007954254, 0.053051172280212354, 0.04716196765097761, 0.040953951708905166, 0.03464267620432228, 0.02842447161457115, 0.022467290293909772, 0.016904729129410285, 0.011833331925104714, 0.007312930858914043, 0.0033695215815437857, 0.0],
        },
        "x180_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0027170434465039945, 0.0032130734702621737, 0.0037229597455075395, 0.004223579289059315, 0.004687040371348002, 0.005081998319244572, 0.0053756048376282705, 0.005535990268762329, 0.005535087184624444, 0.005351524501719982, 0.004973269093888868, 0.0043996794842555585, 0.003642671224892489, 0.002726776190708738, 0.0016880000150935538, 0.0005715273824751895, -0.0005715273824751895, -0.0016880000150935538, -0.002726776190708738, -0.003642671224892489, -0.0043996794842555585, -0.004973269093888868, -0.005351524501719982, -0.005535087184624444, -0.005535990268762329, -0.0053756048376282705, -0.005081998319244572, -0.004687040371348002, -0.004223579289059315, -0.0037229597455075395, -0.0032130734702621737, -0.0027170434465039945],
        },
        "minus_x90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, -0.0016968708271060682, -0.003682748050377406, -0.005959194872398877, -0.008513120039636026, -0.011314392426711162, -0.014314393153870814, -0.017445843631327455, -0.020624164062398618, -0.023750483598089428, -0.026716251671795588, -0.029409209368218295, -0.03172029528651704, -0.03355090984001778, -0.03481987059545138] + [-0.03546937742024726] * 2 + [-0.03481987059545138, -0.03355090984001778, -0.03172029528651704, -0.029409209368218295, -0.026716251671795588, -0.023750483598089428, -0.020624164062398618, -0.017445843631327455, -0.014314393153870814, -0.011314392426711162, -0.008513120039636026, -0.005959194872398877, -0.003682748050377406, -0.0016968708271060682, 0.0],
        },
        "minus_x90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.0013682867578607449, -0.0016180844980783187, -0.0018748601633076928, -0.0021269691581232006, -0.002360365375064587, -0.0025592638250375097, -0.002707122303945135, -0.0027878914435983436, -0.0027874366558515037, -0.0026949955914368946, -0.0025045084403055896, -0.0022156521585565384, -0.0018344273466344232, -0.0013731881093758014, -0.000850066667462784, -0.0002878177565404143, 0.0002878177565404143, 0.000850066667462784, 0.0013731881093758014, 0.0018344273466344232, 0.0022156521585565384, 0.0025045084403055896, 0.0026949955914368946, 0.0027874366558515037, 0.0027878914435983436, 0.002707122303945135, 0.0025592638250375097, 0.002360365375064587, 0.0021269691581232006, 0.0018748601633076928, 0.0016180844980783187, 0.0013682867578607449],
        },
        "y90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.0013585217232519973, -0.0016065367351310869, -0.0018614798727537697, -0.0021117896445296577, -0.002343520185674001, -0.002540999159622286, -0.0026878024188141353, -0.0027679951343811647, -0.002767543592312222, -0.002675762250859991, -0.002486634546944434, -0.0021998397421277792, -0.0018213356124462444, -0.001363388095354369, -0.0008440000075467769, -0.00028576369123759475, 0.00028576369123759475, 0.0008440000075467769, 0.001363388095354369, 0.0018213356124462444, 0.0021998397421277792, 0.002486634546944434, 0.002675762250859991, 0.002767543592312222, 0.0027679951343811647, 0.0026878024188141353, 0.002540999159622286, 0.002343520185674001, 0.0021117896445296577, 0.0018614798727537697, 0.0016065367351310869, 0.0013585217232519973],
        },
        "y90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0016847607907718928, 0.0036564654294570214, 0.005916665962552357, 0.008452364564705142, 0.011233645146954886, 0.014212235807285575, 0.01732133810216114, 0.020476975854452583, 0.023580983825488806, 0.026525586140106177, 0.02919932503977127, 0.03149391746074841, 0.03331146749077296, 0.03457137207020927] + [0.035216243567953776] * 2 + [0.03457137207020927, 0.03331146749077296, 0.03149391746074841, 0.02919932503977127, 0.026525586140106177, 0.023580983825488806, 0.020476975854452583, 0.01732133810216114, 0.014212235807285575, 0.011233645146954886, 0.008452364564705142, 0.005916665962552357, 0.0036564654294570214, 0.0016847607907718928, 0.0],
        },
        "y180_I_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.0027170434465039945, -0.0032130734702621737, -0.0037229597455075395, -0.004223579289059315, -0.004687040371348002, -0.005081998319244572, -0.0053756048376282705, -0.005535990268762329, -0.005535087184624444, -0.005351524501719982, -0.004973269093888868, -0.0043996794842555585, -0.003642671224892489, -0.002726776190708738, -0.0016880000150935538, -0.0005715273824751895, 0.0005715273824751895, 0.0016880000150935538, 0.002726776190708738, 0.003642671224892489, 0.0043996794842555585, 0.004973269093888868, 0.005351524501719982, 0.005535087184624444, 0.005535990268762329, 0.0053756048376282705, 0.005081998319244572, 0.004687040371348002, 0.004223579289059315, 0.0037229597455075395, 0.0032130734702621737, 0.0027170434465039945],
        },
        "y180_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0033695215815437857, 0.007312930858914043, 0.011833331925104714, 0.016904729129410285, 0.022467290293909772, 0.02842447161457115, 0.03464267620432228, 0.040953951708905166, 0.04716196765097761, 0.053051172280212354, 0.05839865007954254, 0.06298783492149682, 0.06662293498154592, 0.06914274414041854] + [0.07043248713590755] * 2 + [0.06914274414041854, 0.06662293498154592, 0.06298783492149682, 0.05839865007954254, 0.053051172280212354, 0.04716196765097761, 0.040953951708905166, 0.03464267620432228, 0.02842447161457115, 0.022467290293909772, 0.016904729129410285, 0.011833331925104714, 0.007312930858914043, 0.0033695215815437857, 0.0],
        },
        "minus_y90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0013585217232519973, 0.0016065367351310869, 0.0018614798727537697, 0.0021117896445296577, 0.002343520185674001, 0.002540999159622286, 0.0026878024188141353, 0.0027679951343811647, 0.002767543592312222, 0.002675762250859991, 0.002486634546944434, 0.0021998397421277792, 0.0018213356124462444, 0.001363388095354369, 0.0008440000075467769, 0.00028576369123759475, -0.00028576369123759475, -0.0008440000075467769, -0.001363388095354369, -0.0018213356124462444, -0.0021998397421277792, -0.002486634546944434, -0.002675762250859991, -0.002767543592312222, -0.0027679951343811647, -0.0026878024188141353, -0.002540999159622286, -0.002343520185674001, -0.0021117896445296577, -0.0018614798727537697, -0.0016065367351310869, -0.0013585217232519973],
        },
        "minus_y90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, -0.0016847607907718928, -0.0036564654294570214, -0.005916665962552357, -0.008452364564705142, -0.011233645146954886, -0.014212235807285575, -0.01732133810216114, -0.020476975854452583, -0.023580983825488806, -0.026525586140106177, -0.02919932503977127, -0.03149391746074841, -0.03331146749077296, -0.03457137207020927] + [-0.035216243567953776] * 2 + [-0.03457137207020927, -0.03331146749077296, -0.03149391746074841, -0.02919932503977127, -0.026525586140106177, -0.023580983825488806, -0.020476975854452583, -0.01732133810216114, -0.014212235807285575, -0.011233645146954886, -0.008452364564705142, -0.005916665962552357, -0.0036564654294570214, -0.0016847607907718928, 0.0],
        },
        "readout_wf_q4": {
            "type": "constant",
            "sample": 0.21388562800000002,
        },
        "x90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.0024070937766195385, 0.00522415717879925, 0.008453407685414676, 0.01207627471678022, 0.016050015806456708, 0.02030566270947739, 0.02474777747488551, 0.0292563795484928, 0.03369121582352001, 0.037898302043093975, 0.04171839347740419, 0.04499678122637469, 0.04759359698201814, 0.04939367951534094] + [0.05031503652782752] * 2 + [0.04939367951534094, 0.04759359698201814, 0.04499678122637469, 0.04171839347740419, 0.037898302043093975, 0.03369121582352001, 0.0292563795484928, 0.02474777747488551, 0.02030566270947739, 0.016050015806456708, 0.01207627471678022, 0.008453407685414676, 0.00522415717879925, 0.0024070937766195385, 0.0],
        },
        "x90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0005085350420277795, -0.0006013744293785681, -0.0006968072200264041, -0.0007905056041827563, -0.0008772492303338852, -0.0009511714772862556, -0.001006124298654644, -0.0010361428145776582, -0.0010359737889661595, -0.001001617306081919, -0.0009308211876149381, -0.0008234653716389774, -0.0006817800307269992, -0.0005103566696832274, -0.00031593427765132026, -0.00010696983952943943, 0.00010696983952943943, 0.00031593427765132026, 0.0005103566696832274, 0.0006817800307269992, 0.0008234653716389774, 0.0009308211876149381, 0.001001617306081919, 0.0010359737889661595, 0.0010361428145776582, 0.001006124298654644, 0.0009511714772862556, 0.0008772492303338852, 0.0007905056041827563, 0.0006968072200264041, 0.0006013744293785681, 0.0005085350420277795],
        },
        "x180_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.004771186147728274, 0.010354987664854026, 0.01675579989508867, 0.02393681343224628, 0.03181330691408699, 0.0402485759304151, 0.04905344952578413, 0.05799010997838356, 0.06678055661921553, 0.07511957177853329, 0.08269151081616938, 0.08918971972132347, 0.09433696054836291, 0.0979049681312743] + [0.09973122262031289] * 2 + [0.0979049681312743, 0.09433696054836291, 0.08918971972132347, 0.08269151081616938, 0.07511957177853329, 0.06678055661921553, 0.05799010997838356, 0.04905344952578413, 0.0402485759304151, 0.03181330691408699, 0.02393681343224628, 0.01675579989508867, 0.010354987664854026, 0.004771186147728274, 0.0],
        },
        "x180_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0010079853854156088, -0.0011920056355588066, -0.0013811663625735464, -0.0015668892608227116, -0.0017388268859854566, -0.0018853507996334814, -0.001994274740461268, -0.002053775508041826, -0.0020534404763683503, -0.001985341270257586, -0.0018450137670154977, -0.0016322199876298393, -0.001351380436440954, -0.0010115960983510214, -0.0006262245633152881, -0.00021202872174940063, 0.00021202872174940063, 0.0006262245633152881, 0.0010115960983510214, 0.001351380436440954, 0.0016322199876298393, 0.0018450137670154977, 0.001985341270257586, 0.0020534404763683503, 0.002053775508041826, 0.001994274740461268, 0.0018853507996334814, 0.0017388268859854566, 0.0015668892608227116, 0.0013811663625735464, 0.0011920056355588066, 0.0010079853854156088],
        },
        "minus_x90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, -0.0024070937766195385, -0.00522415717879925, -0.008453407685414676, -0.01207627471678022, -0.016050015806456708, -0.02030566270947739, -0.02474777747488551, -0.0292563795484928, -0.03369121582352001, -0.037898302043093975, -0.04171839347740419, -0.04499678122637469, -0.04759359698201814, -0.04939367951534094] + [-0.05031503652782752] * 2 + [-0.04939367951534094, -0.04759359698201814, -0.04499678122637469, -0.04171839347740419, -0.037898302043093975, -0.03369121582352001, -0.0292563795484928, -0.02474777747488551, -0.02030566270947739, -0.016050015806456708, -0.01207627471678022, -0.008453407685414676, -0.00522415717879925, -0.0024070937766195385, 0.0],
        },
        "minus_x90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0005085350420277795, 0.0006013744293785681, 0.0006968072200264041, 0.0007905056041827563, 0.0008772492303338852, 0.0009511714772862556, 0.001006124298654644, 0.0010361428145776582, 0.0010359737889661595, 0.001001617306081919, 0.0009308211876149381, 0.0008234653716389774, 0.0006817800307269992, 0.0005103566696832274, 0.00031593427765132026, 0.00010696983952943943, -0.00010696983952943943, -0.00031593427765132026, -0.0005103566696832274, -0.0006817800307269992, -0.0008234653716389774, -0.0009308211876149381, -0.001001617306081919, -0.0010359737889661595, -0.0010361428145776582, -0.001006124298654644, -0.0009511714772862556, -0.0008772492303338852, -0.0007905056041827563, -0.0006968072200264041, -0.0006013744293785681, -0.0005085350420277795],
        },
        "y90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0005039926927078044, 0.0005960028177794033, 0.0006905831812867732, 0.0007834446304113558, 0.0008694134429927283, 0.0009426753998167407, 0.000997137370230634, 0.001026887754020913, 0.0010267202381841751, 0.000992670635128793, 0.0009225068835077489, 0.0008161099938149197, 0.000675690218220477, 0.0005057980491755107, 0.00031311228165764403, 0.00010601436087470031, -0.00010601436087470031, -0.00031311228165764403, -0.0005057980491755107, -0.000675690218220477, -0.0008161099938149197, -0.0009225068835077489, -0.000992670635128793, -0.0010267202381841751, -0.001026887754020913, -0.000997137370230634, -0.0009426753998167407, -0.0008694134429927283, -0.0007834446304113558, -0.0006905831812867732, -0.0005960028177794033, -0.0005039926927078044],
        },
        "y90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.002385593073864137, 0.005177493832427013, 0.008377899947544336, 0.01196840671612314, 0.015906653457043497, 0.02012428796520755, 0.024526724762892065, 0.02899505498919178, 0.033390278309607765, 0.037559785889266645, 0.04134575540808469, 0.04459485986066174, 0.047168480274181454, 0.04895248406563715] + [0.049865611310156446] * 2 + [0.04895248406563715, 0.047168480274181454, 0.04459485986066174, 0.04134575540808469, 0.037559785889266645, 0.033390278309607765, 0.02899505498919178, 0.024526724762892065, 0.02012428796520755, 0.015906653457043497, 0.01196840671612314, 0.008377899947544336, 0.005177493832427013, 0.002385593073864137, 0.0],
        },
        "y180_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0010079853854156088, 0.0011920056355588066, 0.0013811663625735464, 0.0015668892608227116, 0.0017388268859854566, 0.0018853507996334814, 0.001994274740461268, 0.002053775508041826, 0.0020534404763683503, 0.001985341270257586, 0.0018450137670154977, 0.0016322199876298393, 0.001351380436440954, 0.0010115960983510214, 0.0006262245633152881, 0.00021202872174940063, -0.00021202872174940063, -0.0006262245633152881, -0.0010115960983510214, -0.001351380436440954, -0.0016322199876298393, -0.0018450137670154977, -0.001985341270257586, -0.0020534404763683503, -0.002053775508041826, -0.001994274740461268, -0.0018853507996334814, -0.0017388268859854566, -0.0015668892608227116, -0.0013811663625735464, -0.0011920056355588066, -0.0010079853854156088],
        },
        "y180_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.004771186147728274, 0.010354987664854026, 0.01675579989508867, 0.02393681343224628, 0.03181330691408699, 0.0402485759304151, 0.04905344952578413, 0.05799010997838356, 0.06678055661921553, 0.07511957177853329, 0.08269151081616938, 0.08918971972132347, 0.09433696054836291, 0.0979049681312743] + [0.09973122262031289] * 2 + [0.0979049681312743, 0.09433696054836291, 0.08918971972132347, 0.08269151081616938, 0.07511957177853329, 0.06678055661921553, 0.05799010997838356, 0.04905344952578413, 0.0402485759304151, 0.03181330691408699, 0.02393681343224628, 0.01675579989508867, 0.010354987664854026, 0.004771186147728274, 0.0],
        },
        "minus_y90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0005039926927078044, -0.0005960028177794033, -0.0006905831812867732, -0.0007834446304113558, -0.0008694134429927283, -0.0009426753998167407, -0.000997137370230634, -0.001026887754020913, -0.0010267202381841751, -0.000992670635128793, -0.0009225068835077489, -0.0008161099938149197, -0.000675690218220477, -0.0005057980491755107, -0.00031311228165764403, -0.00010601436087470031, 0.00010601436087470031, 0.00031311228165764403, 0.0005057980491755107, 0.000675690218220477, 0.0008161099938149197, 0.0009225068835077489, 0.000992670635128793, 0.0010267202381841751, 0.001026887754020913, 0.000997137370230634, 0.0009426753998167407, 0.0008694134429927283, 0.0007834446304113558, 0.0006905831812867732, 0.0005960028177794033, 0.0005039926927078044],
        },
        "minus_y90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, -0.002385593073864137, -0.005177493832427013, -0.008377899947544336, -0.01196840671612314, -0.015906653457043497, -0.02012428796520755, -0.024526724762892065, -0.02899505498919178, -0.033390278309607765, -0.037559785889266645, -0.04134575540808469, -0.04459485986066174, -0.047168480274181454, -0.04895248406563715] + [-0.049865611310156446] * 2 + [-0.04895248406563715, -0.047168480274181454, -0.04459485986066174, -0.04134575540808469, -0.037559785889266645, -0.033390278309607765, -0.02899505498919178, -0.024526724762892065, -0.02012428796520755, -0.015906653457043497, -0.01196840671612314, -0.008377899947544336, -0.005177493832427013, -0.002385593073864137, 0.0],
        },
        "readout_wf_q5": {
            "type": "constant",
            "sample": 0.056009617,
        },
        "gft_cz_wf_1_2_q2": {
            "type": "arbitrary",
            "samples": [1.7134099282414948e-06, 2.638671054595603e-05, 0.000274955837812804, 0.001938627437084657, 0.00924867424157258, 0.029855086162189872, 0.06520950340242525, 0.0963733986591603] + [0.10119591000000001] * 8 + [0.0963733986591603, 0.06520950340242525, 0.029855086162189872, 0.00924867424157258, 0.001938627437084657, 0.000274955837812804, 2.638671054595603e-05, 1.7134099282414948e-06],
        },
        "g_cz_wf_1_2_q2": {
            "type": "arbitrary",
            "samples": [0.03931213024777564, 0.06088781843160629, 0.08859125307281902, 0.12108988595605871, 0.15548249127139938, 0.18754768422689555, 0.2125193682579723] + [0.22622568992333553] * 2 + [0.2125193682579723, 0.18754768422689555, 0.15548249127139938, 0.12108988595605871, 0.08859125307281902, 0.06088781843160629, 0.03931213024777564],
        },
        "cz_4c5t_wf": {
            "type": "arbitrary",
            "samples": [0.0] + [0.17576251507999996] * 39,
        },
        "cz_3c4t_wf": {
            "type": "arbitrary",
            "samples": [0.0] + [0.22160121899378024] * 47,
        },
        "cz_3c2t_wf": {
            "type": "arbitrary",
            "samples": [0.0] + [0.19218309803099998] * 63,
        },
        "cz_2c1t_wf": {
            "type": "arbitrary",
            "samples": [0.0] + [0.14464637680397693] * 23,
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
            "cosine": [(0.5210096318405759, 1800)],
            "sine": [(-0.8535507972753277, 1800)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(0.8535507972753277, 1800)],
            "sine": [(0.5210096318405759, 1800)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(-0.8535507972753277, 1800)],
            "sine": [(-0.5210096318405759, 1800)],
        },
        "rotated_cosine_weights_q2": {
            "cosine": [(-0.8348478632634064, 1800)],
            "sine": [(0.5504807400849958, 1800)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(-0.5504807400849958, 1800)],
            "sine": [(-0.8348478632634064, 1800)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(0.5504807400849958, 1800)],
            "sine": [(0.8348478632634064, 1800)],
        },
        "rotated_cosine_weights_q3": {
            "cosine": [(0.9573194975320672, 1800)],
            "sine": [(0.2890317969444716, 1800)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(-0.2890317969444716, 1800)],
            "sine": [(0.9573194975320672, 1800)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(0.2890317969444716, 1800)],
            "sine": [(-0.9573194975320672, 1800)],
        },
        "rotated_cosine_weights_q4": {
            "cosine": [(-0.41628079226040127, 1800)],
            "sine": [(-0.9092361090470685, 1800)],
        },
        "rotated_sine_weights_q4": {
            "cosine": [(0.9092361090470685, 1800)],
            "sine": [(-0.41628079226040127, 1800)],
        },
        "rotated_minus_sine_weights_q4": {
            "cosine": [(-0.9092361090470685, 1800)],
            "sine": [(0.41628079226040127, 1800)],
        },
        "rotated_cosine_weights_q5": {
            "cosine": [(-0.9973144772244582, 1800)],
            "sine": [(-0.07323819712763101, 1800)],
        },
        "rotated_sine_weights_q5": {
            "cosine": [(0.07323819712763101, 1800)],
            "sine": [(-0.9973144772244582, 1800)],
        },
        "rotated_minus_sine_weights_q5": {
            "cosine": [(-0.07323819712763101, 1800)],
            "sine": [(0.9973144772244582, 1800)],
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
            {'intermediate_frequency': -131235000, 'lo_frequency': 3200000000, 'correction': [0.909939993172884, 0.06435194984078407, 0.05217019096016884, 1.1224113143980503]},
        ],
        "octave_octave1_3": [
            {'intermediate_frequency': 471832000, 'lo_frequency': 3670000000, 'correction': [1.0509245730936527, 0.1871345043182373, 0.1878669261932373, 1.0468274168670177]},
            {'intermediate_frequency': -261857000, 'lo_frequency': 3200000000, 'correction': [0.8728884682059288, -0.00466681644320488, -0.003476236015558243, 1.1718457750976086]},
            {'intermediate_frequency': -262513000, 'lo_frequency': 3200000000, 'correction': [0.8368789926171303, 0.003159593790769577, 0.0021197572350502014, 1.247405406087637]},
            {'intermediate_frequency': -262884000, 'lo_frequency': 3200000000, 'correction': [0.869447585195303, -0.0047644078731536865, -0.0035155974328517914, 1.1782930493354797]},
            {'intermediate_frequency': -262526000, 'lo_frequency': 3200000000, 'correction': [0.8509256765246391, 0.0001483820378780365, 0.00010387226939201355, 1.2155497074127197]},
            {'intermediate_frequency': -262792000, 'lo_frequency': 3200000000, 'correction': [0.8692551776766777, -0.004460126161575317, -0.003289349377155304, 1.1786490269005299]},
        ],
        "octave_octave1_4": [
            {'intermediate_frequency': -106551000, 'lo_frequency': 3960000000, 'correction': [1.3551864996552467, -0.023040927946567535, -0.038992561399936676, 0.8007874302566051]},
            {'intermediate_frequency': -106458000, 'lo_frequency': 3960000000, 'correction': [1.2996150106191635, -0.023949556052684784, -0.038025788962841034, 0.818528775125742]},
            {'intermediate_frequency': -106481000, 'lo_frequency': 3960000000, 'correction': [1.3489361219108105, -0.02309318631887436, -0.03881271928548813, 0.8026037104427814]},
            {'intermediate_frequency': -106486000, 'lo_frequency': 3960000000, 'correction': [1.3209210634231567, -0.024531234055757523, -0.039934027940034866, 0.8114338889718056]},
            {'intermediate_frequency': -106443000, 'lo_frequency': 3960000000, 'correction': [1.3499723672866821, -0.0223989337682724, -0.03769315779209137, 0.8022129610180855]},
        ],
        "octave_octave1_5": [
            {'intermediate_frequency': -368712000, 'lo_frequency': 3960000000, 'correction': [1.5205974765121937, -0.035888671875, -0.071044921875, 0.7681368701159954]},
            {'intermediate_frequency': -368884000, 'lo_frequency': 3960000000, 'correction': [1.3623402081429958, -0.024932861328125, -0.042510986328125, 0.7990179099142551]},
            {'intermediate_frequency': -368950000, 'lo_frequency': 3960000000, 'correction': [1.4819180443882942, -0.02796586975455284, -0.053621333092451096, 0.772885050624609]},
            {'intermediate_frequency': -368836000, 'lo_frequency': 3960000000, 'correction': [1.4405015744268894, -0.036540985107421875, -0.06730270385742188, 0.7820985391736031]},
            {'intermediate_frequency': -368583000, 'lo_frequency': 3960000000, 'correction': [1.4771419242024422, -0.02573089674115181, -0.04914436861872673, 0.7733985595405102]},
            {'intermediate_frequency': -368508000, 'lo_frequency': 3960000000, 'correction': (1, 0, 0, 1)},
        ],
        "octave_octave2_1": [
            {'intermediate_frequency': -122859000, 'lo_frequency': 4600000000, 'correction': [1.255867786705494, -0.0473419725894928, -0.0707947313785553, 0.8398260287940502]},
            {'intermediate_frequency': -122900000, 'lo_frequency': 4600000000, 'correction': [1.253316655755043, -0.04247363284230232, -0.06340106204152107, 0.8396217599511147]},
            {'intermediate_frequency': -122911000, 'lo_frequency': 4600000000, 'correction': [1.2556648589670658, -0.046525731682777405, -0.06957413256168365, 0.8396903276443481]},
            {'intermediate_frequency': -122888000, 'lo_frequency': 4600000000, 'correction': [1.2544812224805355, -0.04737443849444389, -0.07071657106280327, 0.84040192887187]},
            {'intermediate_frequency': -122908000, 'lo_frequency': 4600000000, 'correction': (1, 0, 0, 1)},
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
            {'intermediate_frequency': 218194000, 'lo_frequency': 5900000000, 'correction': [1.113389290869236, -0.18521547317504883, -0.20657777786254883, 0.9982531815767288]},
            {'intermediate_frequency': 28632000, 'lo_frequency': 5900000000, 'correction': [1.089952491223812, -0.1585984230041504, -0.1741623878479004, 0.9925492443144321]},
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
                    "offset": -0.001953125,
                    "delay": 0,
                    "shareable": False,
                },
                "3": {
                    "offset": -0.0018310546875,
                    "delay": 0,
                    "shareable": False,
                },
                "4": {
                    "offset": 0.0138702392578125,
                    "delay": 0,
                    "shareable": False,
                },
                "5": {
                    "offset": -0.0139617919921875,
                    "delay": 0,
                    "shareable": False,
                },
                "6": {
                    "offset": 0.01104736328125,
                    "delay": 0,
                    "shareable": False,
                },
                "7": {
                    "offset": 0.0152587890625,
                    "delay": 0,
                    "shareable": False,
                },
                "8": {
                    "offset": -0.00072479248046875,
                    "delay": 0,
                    "shareable": False,
                },
                "9": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                },
                "10": {
                    "offset": 0.0,
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
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                },
                "2": {
                    "offset": 0.0,
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
                    "offset": -0.20299999999999996,
                    "delay": 0,
                    "shareable": False,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "6": {
                    "offset": 0.044,
                    "delay": 0,
                    "shareable": False,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "7": {
                    "offset": -0.116,
                    "delay": 0,
                    "shareable": False,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "8": {
                    "offset": 0.033,
                    "delay": 0,
                    "shareable": False,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "9": {
                    "offset": 0.037,
                    "delay": 0,
                    "shareable": False,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
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
            "intermediate_frequency": 163122000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q1",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "octave_octave1_1",
                "lo_frequency": 5900000000.0,
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
            "intermediate_frequency": 126410000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q2",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "octave_octave1_1",
                "lo_frequency": 5900000000.0,
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
            "intermediate_frequency": 49753000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q3",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "octave_octave1_1",
                "lo_frequency": 5900000000.0,
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
            "intermediate_frequency": 218194000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q4",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "octave_octave1_1",
                "lo_frequency": 5900000000.0,
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
            "intermediate_frequency": 28632000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q5",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "octave_octave1_1",
                "lo_frequency": 5900000000.0,
            },
        },
        "q1_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": 131235000.0,
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
            "intermediate_frequency": 106443000.0,
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
            "intermediate_frequency": 262792000.0,
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
            "intermediate_frequency": 368508000.0,
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
            "intermediate_frequency": 368508000.0,
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
            "intermediate_frequency": 122908000.0,
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
            "length": 360,
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
            "length": 40,
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
            "length": 64,
            "waveforms": {
                "single": "cz_3c2t_wf",
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
            "length": 32,
            "waveforms": {
                "I": "x90_I_wf_q1",
                "Q": "x90_Q_wf_q1",
            },
            "operation": "control",
        },
        "x180_pulse_q1": {
            "length": 32,
            "waveforms": {
                "I": "x180_I_wf_q1",
                "Q": "x180_Q_wf_q1",
            },
            "operation": "control",
        },
        "-x90_pulse_q1": {
            "length": 32,
            "waveforms": {
                "I": "minus_x90_I_wf_q1",
                "Q": "minus_x90_Q_wf_q1",
            },
            "operation": "control",
        },
        "y90_pulse_q1": {
            "length": 32,
            "waveforms": {
                "I": "y90_I_wf_q1",
                "Q": "y90_Q_wf_q1",
            },
            "operation": "control",
        },
        "y180_pulse_q1": {
            "length": 32,
            "waveforms": {
                "I": "y180_I_wf_q1",
                "Q": "y180_Q_wf_q1",
            },
            "operation": "control",
        },
        "-y90_pulse_q1": {
            "length": 32,
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
            "length": 32,
            "waveforms": {
                "I": "x90_I_wf_q2",
                "Q": "x90_Q_wf_q2",
            },
            "operation": "control",
        },
        "x180_pulse_q2": {
            "length": 32,
            "waveforms": {
                "I": "x180_I_wf_q2",
                "Q": "x180_Q_wf_q2",
            },
            "operation": "control",
        },
        "-x90_pulse_q2": {
            "length": 32,
            "waveforms": {
                "I": "minus_x90_I_wf_q2",
                "Q": "minus_x90_Q_wf_q2",
            },
            "operation": "control",
        },
        "y90_pulse_q2": {
            "length": 32,
            "waveforms": {
                "I": "y90_I_wf_q2",
                "Q": "y90_Q_wf_q2",
            },
            "operation": "control",
        },
        "y180_pulse_q2": {
            "length": 32,
            "waveforms": {
                "I": "y180_I_wf_q2",
                "Q": "y180_Q_wf_q2",
            },
            "operation": "control",
        },
        "-y90_pulse_q2": {
            "length": 32,
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
            "length": 32,
            "waveforms": {
                "I": "x90_I_wf_q3",
                "Q": "x90_Q_wf_q3",
            },
            "operation": "control",
        },
        "x180_pulse_q3": {
            "length": 32,
            "waveforms": {
                "I": "x180_I_wf_q3",
                "Q": "x180_Q_wf_q3",
            },
            "operation": "control",
        },
        "-x90_pulse_q3": {
            "length": 32,
            "waveforms": {
                "I": "minus_x90_I_wf_q3",
                "Q": "minus_x90_Q_wf_q3",
            },
            "operation": "control",
        },
        "y90_pulse_q3": {
            "length": 32,
            "waveforms": {
                "I": "y90_I_wf_q3",
                "Q": "y90_Q_wf_q3",
            },
            "operation": "control",
        },
        "y180_pulse_q3": {
            "length": 32,
            "waveforms": {
                "I": "y180_I_wf_q3",
                "Q": "y180_Q_wf_q3",
            },
            "operation": "control",
        },
        "-y90_pulse_q3": {
            "length": 32,
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
            "length": 32,
            "waveforms": {
                "I": "x90_I_wf_q4",
                "Q": "x90_Q_wf_q4",
            },
            "operation": "control",
        },
        "x180_pulse_q4": {
            "length": 32,
            "waveforms": {
                "I": "x180_I_wf_q4",
                "Q": "x180_Q_wf_q4",
            },
            "operation": "control",
        },
        "-x90_pulse_q4": {
            "length": 32,
            "waveforms": {
                "I": "minus_x90_I_wf_q4",
                "Q": "minus_x90_Q_wf_q4",
            },
            "operation": "control",
        },
        "y90_pulse_q4": {
            "length": 32,
            "waveforms": {
                "I": "y90_I_wf_q4",
                "Q": "y90_Q_wf_q4",
            },
            "operation": "control",
        },
        "y180_pulse_q4": {
            "length": 32,
            "waveforms": {
                "I": "y180_I_wf_q4",
                "Q": "y180_Q_wf_q4",
            },
            "operation": "control",
        },
        "-y90_pulse_q4": {
            "length": 32,
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
            "length": 32,
            "waveforms": {
                "I": "x90_I_wf_q5",
                "Q": "x90_Q_wf_q5",
            },
            "operation": "control",
        },
        "x180_pulse_q5": {
            "length": 32,
            "waveforms": {
                "I": "x180_I_wf_q5",
                "Q": "x180_Q_wf_q5",
            },
            "operation": "control",
        },
        "-x90_pulse_q5": {
            "length": 32,
            "waveforms": {
                "I": "minus_x90_I_wf_q5",
                "Q": "minus_x90_Q_wf_q5",
            },
            "operation": "control",
        },
        "y90_pulse_q5": {
            "length": 32,
            "waveforms": {
                "I": "y90_I_wf_q5",
                "Q": "y90_Q_wf_q5",
            },
            "operation": "control",
        },
        "y180_pulse_q5": {
            "length": 32,
            "waveforms": {
                "I": "y180_I_wf_q5",
                "Q": "y180_Q_wf_q5",
            },
            "operation": "control",
        },
        "-y90_pulse_q5": {
            "length": 32,
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
            "samples": [0.0, 0.00039408485680079226, 0.0008552891680868398, 0.0013839759753206781, 0.001977104938193513, 0.0026276783406505716, 0.0033244048316005406, 0.004051659489571117, 0.004789799324340885, 0.005515862361583035, 0.0062046385889545225, 0.006830056759396672, 0.007366788223346909, 0.007791934005011461, 0.008086640125007488] + [0.008237482958741243] * 2 + [0.008086640125007488, 0.007791934005011461, 0.007366788223346909, 0.006830056759396672, 0.0062046385889545225, 0.005515862361583035, 0.004789799324340885, 0.004051659489571117, 0.0033244048316005406, 0.0026276783406505716, 0.001977104938193513, 0.0013839759753206781, 0.0008552891680868398, 0.00039408485680079226, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q1": {
            "samples": [-0.0002632848221374642, -0.00031135073611762265, -0.00036075933775814593, -0.0004092699818010895, -0.00045417992565017264, -0.0004924518322689368, -0.0005209026618169576, -0.000536444205609312, -0.0005363566956554597, -0.0005185692479126707, -0.0004819158377872311, -0.00042633430538791786, -0.00035297928223602574, -0.00026422793691546027, -0.00016356925919376895, -5.5381700073764175e-05, 5.5381700073764175e-05, 0.00016356925919376895, 0.00026422793691546027, 0.00035297928223602574, 0.00042633430538791786, 0.0004819158377872311, 0.0005185692479126707, 0.0005363566956554597, 0.000536444205609312, 0.0005209026618169576, 0.0004924518322689368, 0.00045417992565017264, 0.0004092699818010895, 0.00036075933775814593, 0.00031135073611762265, 0.0002632848221374642],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q1": {
            "samples": [0.0, 0.0007890929523558408, 0.0017125820571805804, 0.002771194247911413, 0.003958841721200831, 0.005261512651102933, 0.006656597882723868, 0.008112810967974766, 0.009590819907974099, 0.011044646960109398, 0.012423813039164868, 0.013676114572843573, 0.014750834923554378, 0.01560212249334013, 0.016192225153444505] + [0.016494264206604208] * 2 + [0.016192225153444505, 0.01560212249334013, 0.014750834923554378, 0.013676114572843573, 0.012423813039164868, 0.011044646960109398, 0.009590819907974099, 0.008112810967974766, 0.006656597882723868, 0.005261512651102933, 0.003958841721200831, 0.002771194247911413, 0.0017125820571805804, 0.0007890929523558408, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q1": {
            "samples": [-0.0005271864524242647, -0.0006234308863723009, -0.0007223638412105082, -0.0008194987771714698, -0.000909423877236712, -0.0009860573516392917, -0.001043025663660398, -0.0010741451610570606, -0.0010739699361361986, -0.0010383533692673844, -0.0009649606795695586, -0.0008536674016357496, -0.0007067855035111596, -0.0005290748914539217, -0.0003275217187985322, -0.00011089314512732731, 0.00011089314512732731, 0.0003275217187985322, 0.0005290748914539217, 0.0007067855035111596, 0.0008536674016357496, 0.0009649606795695586, 0.0010383533692673844, 0.0010739699361361986, 0.0010741451610570606, 0.001043025663660398, 0.0009860573516392917, 0.000909423877236712, 0.0008194987771714698, 0.0007223638412105082, 0.0006234308863723009, 0.0005271864524242647],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q1": {
            "samples": [0.0, -0.00039408485680079226, -0.0008552891680868398, -0.0013839759753206781, -0.001977104938193513, -0.0026276783406505716, -0.0033244048316005406, -0.004051659489571117, -0.004789799324340885, -0.005515862361583035, -0.0062046385889545225, -0.006830056759396672, -0.007366788223346909, -0.007791934005011461, -0.008086640125007488] + [-0.008237482958741243] * 2 + [-0.008086640125007488, -0.007791934005011461, -0.007366788223346909, -0.006830056759396672, -0.0062046385889545225, -0.005515862361583035, -0.004789799324340885, -0.004051659489571117, -0.0033244048316005406, -0.0026276783406505716, -0.001977104938193513, -0.0013839759753206781, -0.0008552891680868398, -0.00039408485680079226, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q1": {
            "samples": [0.0002632848221374642, 0.00031135073611762265, 0.00036075933775814593, 0.0004092699818010895, 0.00045417992565017264, 0.0004924518322689368, 0.0005209026618169576, 0.000536444205609312, 0.0005363566956554597, 0.0005185692479126707, 0.0004819158377872311, 0.00042633430538791786, 0.00035297928223602574, 0.00026422793691546027, 0.00016356925919376895, 5.5381700073764175e-05, -5.5381700073764175e-05, -0.00016356925919376895, -0.00026422793691546027, -0.00035297928223602574, -0.00042633430538791786, -0.0004819158377872311, -0.0005185692479126707, -0.0005363566956554597, -0.000536444205609312, -0.0005209026618169576, -0.0004924518322689368, -0.00045417992565017264, -0.0004092699818010895, -0.00036075933775814593, -0.00031135073611762265, -0.0002632848221374642],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q1": {
            "samples": [0.00026359322621213237, 0.00031171544318615044, 0.0003611819206052541, 0.0004097493885857349, 0.000454711938618356, 0.0004930286758196459, 0.000521512831830199, 0.0005370725805285303, 0.0005369849680680993, 0.0005191766846336922, 0.0004824803397847793, 0.0004268337008178748, 0.0003533927517555798, 0.00026453744572696084, 0.0001637608593992661, 5.5446572563663654e-05, -5.5446572563663654e-05, -0.0001637608593992661, -0.00026453744572696084, -0.0003533927517555798, -0.0004268337008178748, -0.0004824803397847793, -0.0005191766846336922, -0.0005369849680680993, -0.0005370725805285303, -0.000521512831830199, -0.0004930286758196459, -0.000454711938618356, -0.0004097493885857349, -0.0003611819206052541, -0.00031171544318615044, -0.00026359322621213237],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q1": {
            "samples": [0.0, 0.0003945464761779204, 0.0008562910285902902, 0.0013855971239557065, 0.0019794208606004155, 0.0026307563255514666, 0.003328298941361934, 0.004056405483987383, 0.0047954099539870496, 0.005522323480054699, 0.006211906519582434, 0.006838057286421786, 0.007375417461777189, 0.007801061246670065, 0.008096112576722252] + [0.008247132103302104] * 2 + [0.008096112576722252, 0.007801061246670065, 0.007375417461777189, 0.006838057286421786, 0.006211906519582434, 0.005522323480054699, 0.0047954099539870496, 0.004056405483987383, 0.003328298941361934, 0.0026307563255514666, 0.0019794208606004155, 0.0013855971239557065, 0.0008562910285902902, 0.0003945464761779204, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q1": {
            "samples": [0.0005271864524242647, 0.0006234308863723009, 0.0007223638412105082, 0.0008194987771714698, 0.000909423877236712, 0.0009860573516392917, 0.001043025663660398, 0.0010741451610570606, 0.0010739699361361986, 0.0010383533692673844, 0.0009649606795695586, 0.0008536674016357496, 0.0007067855035111596, 0.0005290748914539217, 0.0003275217187985322, 0.00011089314512732731, -0.00011089314512732731, -0.0003275217187985322, -0.0005290748914539217, -0.0007067855035111596, -0.0008536674016357496, -0.0009649606795695586, -0.0010383533692673844, -0.0010739699361361986, -0.0010741451610570606, -0.001043025663660398, -0.0009860573516392917, -0.000909423877236712, -0.0008194987771714698, -0.0007223638412105082, -0.0006234308863723009, -0.0005271864524242647],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q1": {
            "samples": [0.0, 0.0007890929523558408, 0.0017125820571805804, 0.002771194247911413, 0.003958841721200831, 0.005261512651102933, 0.006656597882723868, 0.008112810967974766, 0.009590819907974099, 0.011044646960109398, 0.012423813039164868, 0.013676114572843573, 0.014750834923554378, 0.01560212249334013, 0.016192225153444505] + [0.016494264206604208] * 2 + [0.016192225153444505, 0.01560212249334013, 0.014750834923554378, 0.013676114572843573, 0.012423813039164868, 0.011044646960109398, 0.009590819907974099, 0.008112810967974766, 0.006656597882723868, 0.005261512651102933, 0.003958841721200831, 0.002771194247911413, 0.0017125820571805804, 0.0007890929523558408, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q1": {
            "samples": [-0.00026359322621213237, -0.00031171544318615044, -0.0003611819206052541, -0.0004097493885857349, -0.000454711938618356, -0.0004930286758196459, -0.000521512831830199, -0.0005370725805285303, -0.0005369849680680993, -0.0005191766846336922, -0.0004824803397847793, -0.0004268337008178748, -0.0003533927517555798, -0.00026453744572696084, -0.0001637608593992661, -5.5446572563663654e-05, 5.5446572563663654e-05, 0.0001637608593992661, 0.00026453744572696084, 0.0003533927517555798, 0.0004268337008178748, 0.0004824803397847793, 0.0005191766846336922, 0.0005369849680680993, 0.0005370725805285303, 0.000521512831830199, 0.0004930286758196459, 0.000454711938618356, 0.0004097493885857349, 0.0003611819206052541, 0.00031171544318615044, 0.00026359322621213237],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q1": {
            "samples": [0.0, -0.0003945464761779204, -0.0008562910285902902, -0.0013855971239557065, -0.0019794208606004155, -0.0026307563255514666, -0.003328298941361934, -0.004056405483987383, -0.0047954099539870496, -0.005522323480054699, -0.006211906519582434, -0.006838057286421786, -0.007375417461777189, -0.007801061246670065, -0.008096112576722252] + [-0.008247132103302104] * 2 + [-0.008096112576722252, -0.007801061246670065, -0.007375417461777189, -0.006838057286421786, -0.006211906519582434, -0.005522323480054699, -0.0047954099539870496, -0.004056405483987383, -0.003328298941361934, -0.0026307563255514666, -0.0019794208606004155, -0.0013855971239557065, -0.0008562910285902902, -0.0003945464761779204, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q1": {
            "sample": 0.0868910316,
            "type": "constant",
        },
        "x90_I_wf_q2": {
            "samples": [0.0, 0.0012451006481807685, 0.0027022634318202843, 0.004372635370786272, 0.006246610590547289, 0.008302079992909828, 0.010503368853712294, 0.012801110648163878, 0.015133243869878767, 0.01742722077025806, 0.01960339098424132, 0.0215793830985366, 0.023275171916936357, 0.024618408733035172, 0.025549524899255625] + [0.026026108829884206] * 2 + [0.025549524899255625, 0.024618408733035172, 0.023275171916936357, 0.0215793830985366, 0.01960339098424132, 0.01742722077025806, 0.015133243869878767, 0.012801110648163878, 0.010503368853712294, 0.008302079992909828, 0.006246610590547289, 0.004372635370786272, 0.0027022634318202843, 0.0012451006481807685, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q2": {
            "samples": [0.000483561125459141, 0.0005718412141925976, 0.0006625873454077859, 0.0007516842460179772, 0.0008341679335152796, 0.0009044598937118083, 0.0009567140078867002, 0.0009852583286211463, 0.0009850976037778755, 0.0009524283515979763, 0.0008851089971882523, 0.0007830253748071536, 0.0006482981343022296, 0.0004852932938377907, 0.00030041889397239936, 0.00010171660105620371, -0.00010171660105620371, -0.00030041889397239936, -0.0004852932938377907, -0.0006482981343022296, -0.0007830253748071536, -0.0008851089971882523, -0.0009524283515979763, -0.0009850976037778755, -0.0009852583286211463, -0.0009567140078867002, -0.0009044598937118083, -0.0008341679335152796, -0.0007516842460179772, -0.0006625873454077859, -0.0005718412141925976, -0.000483561125459141],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q2": {
            "samples": [0.0, 0.0024543135459211152, 0.005326639059303513, 0.008619237519131436, 0.012313174048118136, 0.01636486770422195, 0.020703997297838846, 0.025233252679234222, 0.02983029964512457, 0.03435213375456568, 0.0386417500536279, 0.04253677992116044, 0.04587947954476214, 0.048527236830848336, 0.050362631441653496] + [0.05130206264219065] * 2 + [0.050362631441653496, 0.048527236830848336, 0.04587947954476214, 0.04253677992116044, 0.0386417500536279, 0.03435213375456568, 0.02983029964512457, 0.025233252679234222, 0.020703997297838846, 0.01636486770422195, 0.012313174048118136, 0.008619237519131436, 0.005326639059303513, 0.0024543135459211152, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q2": {
            "samples": [0.000953184485309917, 0.0011272001505737777, 0.001306076821633896, 0.0014817025675418144, 0.001644292501004577, 0.0017828503841217026, 0.0018858524831383003, 0.001942118386734149, 0.0019418015696474483, 0.0018774046967702299, 0.001744706345298115, 0.0015434814743668364, 0.0012779102598156733, 0.0009565988954796877, 0.0005921787624192545, 0.0002005014070003524, -0.0002005014070003524, -0.0005921787624192545, -0.0009565988954796877, -0.0012779102598156733, -0.0015434814743668364, -0.001744706345298115, -0.0018774046967702299, -0.0019418015696474483, -0.001942118386734149, -0.0018858524831383003, -0.0017828503841217026, -0.001644292501004577, -0.0014817025675418144, -0.001306076821633896, -0.0011272001505737777, -0.000953184485309917],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q2": {
            "samples": [0.0, -0.0012451006481807685, -0.0027022634318202843, -0.004372635370786272, -0.006246610590547289, -0.008302079992909828, -0.010503368853712294, -0.012801110648163878, -0.015133243869878767, -0.01742722077025806, -0.01960339098424132, -0.0215793830985366, -0.023275171916936357, -0.024618408733035172, -0.025549524899255625] + [-0.026026108829884206] * 2 + [-0.025549524899255625, -0.024618408733035172, -0.023275171916936357, -0.0215793830985366, -0.01960339098424132, -0.01742722077025806, -0.015133243869878767, -0.012801110648163878, -0.010503368853712294, -0.008302079992909828, -0.006246610590547289, -0.004372635370786272, -0.0027022634318202843, -0.0012451006481807685, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q2": {
            "samples": [-0.000483561125459141, -0.0005718412141925976, -0.0006625873454077859, -0.0007516842460179772, -0.0008341679335152796, -0.0009044598937118083, -0.0009567140078867002, -0.0009852583286211463, -0.0009850976037778755, -0.0009524283515979763, -0.0008851089971882523, -0.0007830253748071536, -0.0006482981343022296, -0.0004852932938377907, -0.00030041889397239936, -0.00010171660105620371, 0.00010171660105620371, 0.00030041889397239936, 0.0004852932938377907, 0.0006482981343022296, 0.0007830253748071536, 0.0008851089971882523, 0.0009524283515979763, 0.0009850976037778755, 0.0009852583286211463, 0.0009567140078867002, 0.0009044598937118083, 0.0008341679335152796, 0.0007516842460179772, 0.0006625873454077859, 0.0005718412141925976, 0.000483561125459141],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q2": {
            "samples": [-0.0004765922426549585, -0.0005636000752868888, -0.000653038410816948, -0.0007408512837709072, -0.0008221462505022885, -0.0008914251920608513, -0.0009429262415691502, -0.0009710591933670746, -0.0009709007848237241, -0.0009387023483851149, -0.0008723531726490575, -0.0007717407371834182, -0.0006389551299078366, -0.00047829944773984385, -0.00029608938120962726, -0.0001002507035001762, 0.0001002507035001762, 0.00029608938120962726, 0.00047829944773984385, 0.0006389551299078366, 0.0007717407371834182, 0.0008723531726490575, 0.0009387023483851149, 0.0009709007848237241, 0.0009710591933670746, 0.0009429262415691502, 0.0008914251920608513, 0.0008221462505022885, 0.0007408512837709072, 0.000653038410816948, 0.0005636000752868888, 0.0004765922426549585],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q2": {
            "samples": [0.0, 0.0012271567729605576, 0.0026633195296517564, 0.004309618759565718, 0.006156587024059068, 0.008182433852110975, 0.010351998648919423, 0.012616626339617111, 0.014915149822562285, 0.01717606687728284, 0.01932087502681395, 0.02126838996058022, 0.02293973977238107, 0.024263618415424168, 0.025181315720826748] + [0.025651031321095325] * 2 + [0.025181315720826748, 0.024263618415424168, 0.02293973977238107, 0.02126838996058022, 0.01932087502681395, 0.01717606687728284, 0.014915149822562285, 0.012616626339617111, 0.010351998648919423, 0.008182433852110975, 0.006156587024059068, 0.004309618759565718, 0.0026633195296517564, 0.0012271567729605576, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q2": {
            "samples": [-0.000953184485309917, -0.0011272001505737777, -0.001306076821633896, -0.0014817025675418144, -0.001644292501004577, -0.0017828503841217026, -0.0018858524831383003, -0.001942118386734149, -0.0019418015696474483, -0.0018774046967702299, -0.001744706345298115, -0.0015434814743668364, -0.0012779102598156733, -0.0009565988954796877, -0.0005921787624192545, -0.0002005014070003524, 0.0002005014070003524, 0.0005921787624192545, 0.0009565988954796877, 0.0012779102598156733, 0.0015434814743668364, 0.001744706345298115, 0.0018774046967702299, 0.0019418015696474483, 0.001942118386734149, 0.0018858524831383003, 0.0017828503841217026, 0.001644292501004577, 0.0014817025675418144, 0.001306076821633896, 0.0011272001505737777, 0.000953184485309917],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q2": {
            "samples": [0.0, 0.0024543135459211152, 0.005326639059303513, 0.008619237519131436, 0.012313174048118136, 0.01636486770422195, 0.020703997297838846, 0.025233252679234222, 0.02983029964512457, 0.03435213375456568, 0.0386417500536279, 0.04253677992116044, 0.04587947954476214, 0.048527236830848336, 0.050362631441653496] + [0.05130206264219065] * 2 + [0.050362631441653496, 0.048527236830848336, 0.04587947954476214, 0.04253677992116044, 0.0386417500536279, 0.03435213375456568, 0.02983029964512457, 0.025233252679234222, 0.020703997297838846, 0.01636486770422195, 0.012313174048118136, 0.008619237519131436, 0.005326639059303513, 0.0024543135459211152, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q2": {
            "samples": [0.0004765922426549585, 0.0005636000752868888, 0.000653038410816948, 0.0007408512837709072, 0.0008221462505022885, 0.0008914251920608513, 0.0009429262415691502, 0.0009710591933670746, 0.0009709007848237241, 0.0009387023483851149, 0.0008723531726490575, 0.0007717407371834182, 0.0006389551299078366, 0.00047829944773984385, 0.00029608938120962726, 0.0001002507035001762, -0.0001002507035001762, -0.00029608938120962726, -0.00047829944773984385, -0.0006389551299078366, -0.0007717407371834182, -0.0008723531726490575, -0.0009387023483851149, -0.0009709007848237241, -0.0009710591933670746, -0.0009429262415691502, -0.0008914251920608513, -0.0008221462505022885, -0.0007408512837709072, -0.000653038410816948, -0.0005636000752868888, -0.0004765922426549585],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q2": {
            "samples": [0.0, -0.0012271567729605576, -0.0026633195296517564, -0.004309618759565718, -0.006156587024059068, -0.008182433852110975, -0.010351998648919423, -0.012616626339617111, -0.014915149822562285, -0.01717606687728284, -0.01932087502681395, -0.02126838996058022, -0.02293973977238107, -0.024263618415424168, -0.025181315720826748] + [-0.025651031321095325] * 2 + [-0.025181315720826748, -0.024263618415424168, -0.02293973977238107, -0.02126838996058022, -0.01932087502681395, -0.01717606687728284, -0.014915149822562285, -0.012616626339617111, -0.010351998648919423, -0.008182433852110975, -0.006156587024059068, -0.004309618759565718, -0.0026633195296517564, -0.0012271567729605576, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q2": {
            "sample": 0.1309075425,
            "type": "constant",
        },
        "x90_I_wf_q3": {
            "samples": [0.0, 0.00042906451058445866, 0.0009312061145726083, 0.0015068200776153797, 0.0021525961935373976, 0.0028609156168985608, 0.0036194847567470093, 0.004411291796544398, 0.005214950200268544, 0.006005459849019764, 0.006755373046137981, 0.0074363044155639196, 0.00802067709297309, 0.008483559549857644, 0.008804424295001246] + [0.00896865619966401] * 2 + [0.008804424295001246, 0.008483559549857644, 0.00802067709297309, 0.0074363044155639196, 0.006755373046137981, 0.006005459849019764, 0.005214950200268544, 0.004411291796544398, 0.0036194847567470093, 0.0028609156168985608, 0.0021525961935373976, 0.0015068200776153797, 0.0009312061145726083, 0.00042906451058445866, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q3": {
            "samples": [-0.00038493898076757147, -0.00045521437221236814, -0.0005274528575236247, -0.0005983784723109421, -0.0006640396367914714, -0.0007199955730518868, -0.0007615924765091205, -0.0007843151916979962, -0.0007841872466377023, -0.0007581808785190316, -0.0007045912859979105, -0.0006233275874011091, -0.0005160779266837588, -0.00038631787393141336, -0.00023914855177668305, -8.097153115966341e-05, 8.097153115966341e-05, 0.00023914855177668305, 0.00038631787393141336, 0.0005160779266837588, 0.0006233275874011091, 0.0007045912859979105, 0.0007581808785190316, 0.0007841872466377023, 0.0007843151916979962, 0.0007615924765091205, 0.0007199955730518868, 0.0006640396367914714, 0.0005983784723109421, 0.0005274528575236247, 0.00045521437221236814, 0.00038493898076757147],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q3": {
            "samples": [0.0, 0.0008581290211689173, 0.0018624122291452166, 0.0030136401552307594, 0.004305192387074795, 0.0057218312337971216, 0.007238969513494019, 0.008822583593088795, 0.010429900400537089, 0.012010919698039527, 0.013510746092275962, 0.014872608831127839, 0.01604135418594618, 0.016967119099715287, 0.01760884859000249] + [0.01793731239932802] * 2 + [0.01760884859000249, 0.016967119099715287, 0.01604135418594618, 0.014872608831127839, 0.013510746092275962, 0.012010919698039527, 0.010429900400537089, 0.008822583593088795, 0.007238969513494019, 0.0057218312337971216, 0.004305192387074795, 0.0030136401552307594, 0.0018624122291452166, 0.0008581290211689173, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q3": {
            "samples": [-0.0007698779615351429, -0.0009104287444247363, -0.0010549057150472494, -0.0011967569446218842, -0.0013280792735829428, -0.0014399911461037737, -0.001523184953018241, -0.0015686303833959924, -0.0015683744932754047, -0.0015163617570380632, -0.001409182571995821, -0.0012466551748022182, -0.0010321558533675176, -0.0007726357478628267, -0.0004782971035533661, -0.00016194306231932681, 0.00016194306231932681, 0.0004782971035533661, 0.0007726357478628267, 0.0010321558533675176, 0.0012466551748022182, 0.001409182571995821, 0.0015163617570380632, 0.0015683744932754047, 0.0015686303833959924, 0.001523184953018241, 0.0014399911461037737, 0.0013280792735829428, 0.0011967569446218842, 0.0010549057150472494, 0.0009104287444247363, 0.0007698779615351429],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q3": {
            "samples": [0.0, -0.00042906451058445866, -0.0009312061145726083, -0.0015068200776153797, -0.0021525961935373976, -0.0028609156168985608, -0.0036194847567470093, -0.004411291796544398, -0.005214950200268544, -0.006005459849019764, -0.006755373046137981, -0.0074363044155639196, -0.00802067709297309, -0.008483559549857644, -0.008804424295001246] + [-0.00896865619966401] * 2 + [-0.008804424295001246, -0.008483559549857644, -0.00802067709297309, -0.0074363044155639196, -0.006755373046137981, -0.006005459849019764, -0.005214950200268544, -0.004411291796544398, -0.0036194847567470093, -0.0028609156168985608, -0.0021525961935373976, -0.0015068200776153797, -0.0009312061145726083, -0.00042906451058445866, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q3": {
            "samples": [0.00038493898076757147, 0.00045521437221236814, 0.0005274528575236247, 0.0005983784723109421, 0.0006640396367914714, 0.0007199955730518868, 0.0007615924765091205, 0.0007843151916979962, 0.0007841872466377023, 0.0007581808785190316, 0.0007045912859979105, 0.0006233275874011091, 0.0005160779266837588, 0.00038631787393141336, 0.00023914855177668305, 8.097153115966341e-05, -8.097153115966341e-05, -0.00023914855177668305, -0.00038631787393141336, -0.0005160779266837588, -0.0006233275874011091, -0.0007045912859979105, -0.0007581808785190316, -0.0007841872466377023, -0.0007843151916979962, -0.0007615924765091205, -0.0007199955730518868, -0.0006640396367914714, -0.0005983784723109421, -0.0005274528575236247, -0.00045521437221236814, -0.00038493898076757147],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q3": {
            "samples": [0.00038493898076757147, 0.00045521437221236814, 0.0005274528575236247, 0.0005983784723109421, 0.0006640396367914714, 0.0007199955730518868, 0.0007615924765091205, 0.0007843151916979962, 0.0007841872466377023, 0.0007581808785190316, 0.0007045912859979105, 0.0006233275874011091, 0.0005160779266837588, 0.00038631787393141336, 0.00023914855177668305, 8.097153115966341e-05, -8.097153115966341e-05, -0.00023914855177668305, -0.00038631787393141336, -0.0005160779266837588, -0.0006233275874011091, -0.0007045912859979105, -0.0007581808785190316, -0.0007841872466377023, -0.0007843151916979962, -0.0007615924765091205, -0.0007199955730518868, -0.0006640396367914714, -0.0005983784723109421, -0.0005274528575236247, -0.00045521437221236814, -0.00038493898076757147],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q3": {
            "samples": [0.0, 0.00042906451058445866, 0.0009312061145726083, 0.0015068200776153797, 0.0021525961935373976, 0.0028609156168985608, 0.0036194847567470093, 0.004411291796544398, 0.005214950200268544, 0.006005459849019764, 0.006755373046137981, 0.0074363044155639196, 0.00802067709297309, 0.008483559549857644, 0.008804424295001246] + [0.00896865619966401] * 2 + [0.008804424295001246, 0.008483559549857644, 0.00802067709297309, 0.0074363044155639196, 0.006755373046137981, 0.006005459849019764, 0.005214950200268544, 0.004411291796544398, 0.0036194847567470093, 0.0028609156168985608, 0.0021525961935373976, 0.0015068200776153797, 0.0009312061145726083, 0.00042906451058445866, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q3": {
            "samples": [0.0007698779615351429, 0.0009104287444247363, 0.0010549057150472494, 0.0011967569446218842, 0.0013280792735829428, 0.0014399911461037737, 0.001523184953018241, 0.0015686303833959924, 0.0015683744932754047, 0.0015163617570380632, 0.001409182571995821, 0.0012466551748022182, 0.0010321558533675176, 0.0007726357478628267, 0.0004782971035533661, 0.00016194306231932681, -0.00016194306231932681, -0.0004782971035533661, -0.0007726357478628267, -0.0010321558533675176, -0.0012466551748022182, -0.001409182571995821, -0.0015163617570380632, -0.0015683744932754047, -0.0015686303833959924, -0.001523184953018241, -0.0014399911461037737, -0.0013280792735829428, -0.0011967569446218842, -0.0010549057150472494, -0.0009104287444247363, -0.0007698779615351429],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q3": {
            "samples": [0.0, 0.0008581290211689173, 0.0018624122291452166, 0.0030136401552307594, 0.004305192387074795, 0.0057218312337971216, 0.007238969513494019, 0.008822583593088795, 0.010429900400537089, 0.012010919698039527, 0.013510746092275962, 0.014872608831127839, 0.01604135418594618, 0.016967119099715287, 0.01760884859000249] + [0.01793731239932802] * 2 + [0.01760884859000249, 0.016967119099715287, 0.01604135418594618, 0.014872608831127839, 0.013510746092275962, 0.012010919698039527, 0.010429900400537089, 0.008822583593088795, 0.007238969513494019, 0.0057218312337971216, 0.004305192387074795, 0.0030136401552307594, 0.0018624122291452166, 0.0008581290211689173, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q3": {
            "samples": [-0.00038493898076757147, -0.00045521437221236814, -0.0005274528575236247, -0.0005983784723109421, -0.0006640396367914714, -0.0007199955730518868, -0.0007615924765091205, -0.0007843151916979962, -0.0007841872466377023, -0.0007581808785190316, -0.0007045912859979105, -0.0006233275874011091, -0.0005160779266837588, -0.00038631787393141336, -0.00023914855177668305, -8.097153115966341e-05, 8.097153115966341e-05, 0.00023914855177668305, 0.00038631787393141336, 0.0005160779266837588, 0.0006233275874011091, 0.0007045912859979105, 0.0007581808785190316, 0.0007841872466377023, 0.0007843151916979962, 0.0007615924765091205, 0.0007199955730518868, 0.0006640396367914714, 0.0005983784723109421, 0.0005274528575236247, 0.00045521437221236814, 0.00038493898076757147],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q3": {
            "samples": [0.0, -0.00042906451058445866, -0.0009312061145726083, -0.0015068200776153797, -0.0021525961935373976, -0.0028609156168985608, -0.0036194847567470093, -0.004411291796544398, -0.005214950200268544, -0.006005459849019764, -0.006755373046137981, -0.0074363044155639196, -0.00802067709297309, -0.008483559549857644, -0.008804424295001246] + [-0.00896865619966401] * 2 + [-0.008804424295001246, -0.008483559549857644, -0.00802067709297309, -0.0074363044155639196, -0.006755373046137981, -0.006005459849019764, -0.005214950200268544, -0.004411291796544398, -0.0036194847567470093, -0.0028609156168985608, -0.0021525961935373976, -0.0015068200776153797, -0.0009312061145726083, -0.00042906451058445866, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q3": {
            "sample": 0.102461516,
            "type": "constant",
        },
        "x90_I_wf_q4": {
            "samples": [0.0, 0.0016968708271060682, 0.003682748050377406, 0.005959194872398877, 0.008513120039636026, 0.011314392426711162, 0.014314393153870814, 0.017445843631327455, 0.020624164062398618, 0.023750483598089428, 0.026716251671795588, 0.029409209368218295, 0.03172029528651704, 0.03355090984001778, 0.03481987059545138] + [0.03546937742024726] * 2 + [0.03481987059545138, 0.03355090984001778, 0.03172029528651704, 0.029409209368218295, 0.026716251671795588, 0.023750483598089428, 0.020624164062398618, 0.017445843631327455, 0.014314393153870814, 0.011314392426711162, 0.008513120039636026, 0.005959194872398877, 0.003682748050377406, 0.0016968708271060682, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q4": {
            "samples": [0.0013682867578607449, 0.0016180844980783187, 0.0018748601633076928, 0.0021269691581232006, 0.002360365375064587, 0.0025592638250375097, 0.002707122303945135, 0.0027878914435983436, 0.0027874366558515037, 0.0026949955914368946, 0.0025045084403055896, 0.0022156521585565384, 0.0018344273466344232, 0.0013731881093758014, 0.000850066667462784, 0.0002878177565404143, -0.0002878177565404143, -0.000850066667462784, -0.0013731881093758014, -0.0018344273466344232, -0.0022156521585565384, -0.0025045084403055896, -0.0026949955914368946, -0.0027874366558515037, -0.0027878914435983436, -0.002707122303945135, -0.0025592638250375097, -0.002360365375064587, -0.0021269691581232006, -0.0018748601633076928, -0.0016180844980783187, -0.0013682867578607449],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q4": {
            "samples": [0.0, 0.0033695215815437857, 0.007312930858914043, 0.011833331925104714, 0.016904729129410285, 0.022467290293909772, 0.02842447161457115, 0.03464267620432228, 0.040953951708905166, 0.04716196765097761, 0.053051172280212354, 0.05839865007954254, 0.06298783492149682, 0.06662293498154592, 0.06914274414041854] + [0.07043248713590755] * 2 + [0.06914274414041854, 0.06662293498154592, 0.06298783492149682, 0.05839865007954254, 0.053051172280212354, 0.04716196765097761, 0.040953951708905166, 0.03464267620432228, 0.02842447161457115, 0.022467290293909772, 0.016904729129410285, 0.011833331925104714, 0.007312930858914043, 0.0033695215815437857, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q4": {
            "samples": [0.0027170434465039945, 0.0032130734702621737, 0.0037229597455075395, 0.004223579289059315, 0.004687040371348002, 0.005081998319244572, 0.0053756048376282705, 0.005535990268762329, 0.005535087184624444, 0.005351524501719982, 0.004973269093888868, 0.0043996794842555585, 0.003642671224892489, 0.002726776190708738, 0.0016880000150935538, 0.0005715273824751895, -0.0005715273824751895, -0.0016880000150935538, -0.002726776190708738, -0.003642671224892489, -0.0043996794842555585, -0.004973269093888868, -0.005351524501719982, -0.005535087184624444, -0.005535990268762329, -0.0053756048376282705, -0.005081998319244572, -0.004687040371348002, -0.004223579289059315, -0.0037229597455075395, -0.0032130734702621737, -0.0027170434465039945],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q4": {
            "samples": [0.0, -0.0016968708271060682, -0.003682748050377406, -0.005959194872398877, -0.008513120039636026, -0.011314392426711162, -0.014314393153870814, -0.017445843631327455, -0.020624164062398618, -0.023750483598089428, -0.026716251671795588, -0.029409209368218295, -0.03172029528651704, -0.03355090984001778, -0.03481987059545138] + [-0.03546937742024726] * 2 + [-0.03481987059545138, -0.03355090984001778, -0.03172029528651704, -0.029409209368218295, -0.026716251671795588, -0.023750483598089428, -0.020624164062398618, -0.017445843631327455, -0.014314393153870814, -0.011314392426711162, -0.008513120039636026, -0.005959194872398877, -0.003682748050377406, -0.0016968708271060682, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q4": {
            "samples": [-0.0013682867578607449, -0.0016180844980783187, -0.0018748601633076928, -0.0021269691581232006, -0.002360365375064587, -0.0025592638250375097, -0.002707122303945135, -0.0027878914435983436, -0.0027874366558515037, -0.0026949955914368946, -0.0025045084403055896, -0.0022156521585565384, -0.0018344273466344232, -0.0013731881093758014, -0.000850066667462784, -0.0002878177565404143, 0.0002878177565404143, 0.000850066667462784, 0.0013731881093758014, 0.0018344273466344232, 0.0022156521585565384, 0.0025045084403055896, 0.0026949955914368946, 0.0027874366558515037, 0.0027878914435983436, 0.002707122303945135, 0.0025592638250375097, 0.002360365375064587, 0.0021269691581232006, 0.0018748601633076928, 0.0016180844980783187, 0.0013682867578607449],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q4": {
            "samples": [-0.0013585217232519973, -0.0016065367351310869, -0.0018614798727537697, -0.0021117896445296577, -0.002343520185674001, -0.002540999159622286, -0.0026878024188141353, -0.0027679951343811647, -0.002767543592312222, -0.002675762250859991, -0.002486634546944434, -0.0021998397421277792, -0.0018213356124462444, -0.001363388095354369, -0.0008440000075467769, -0.00028576369123759475, 0.00028576369123759475, 0.0008440000075467769, 0.001363388095354369, 0.0018213356124462444, 0.0021998397421277792, 0.002486634546944434, 0.002675762250859991, 0.002767543592312222, 0.0027679951343811647, 0.0026878024188141353, 0.002540999159622286, 0.002343520185674001, 0.0021117896445296577, 0.0018614798727537697, 0.0016065367351310869, 0.0013585217232519973],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q4": {
            "samples": [0.0, 0.0016847607907718928, 0.0036564654294570214, 0.005916665962552357, 0.008452364564705142, 0.011233645146954886, 0.014212235807285575, 0.01732133810216114, 0.020476975854452583, 0.023580983825488806, 0.026525586140106177, 0.02919932503977127, 0.03149391746074841, 0.03331146749077296, 0.03457137207020927] + [0.035216243567953776] * 2 + [0.03457137207020927, 0.03331146749077296, 0.03149391746074841, 0.02919932503977127, 0.026525586140106177, 0.023580983825488806, 0.020476975854452583, 0.01732133810216114, 0.014212235807285575, 0.011233645146954886, 0.008452364564705142, 0.005916665962552357, 0.0036564654294570214, 0.0016847607907718928, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q4": {
            "samples": [-0.0027170434465039945, -0.0032130734702621737, -0.0037229597455075395, -0.004223579289059315, -0.004687040371348002, -0.005081998319244572, -0.0053756048376282705, -0.005535990268762329, -0.005535087184624444, -0.005351524501719982, -0.004973269093888868, -0.0043996794842555585, -0.003642671224892489, -0.002726776190708738, -0.0016880000150935538, -0.0005715273824751895, 0.0005715273824751895, 0.0016880000150935538, 0.002726776190708738, 0.003642671224892489, 0.0043996794842555585, 0.004973269093888868, 0.005351524501719982, 0.005535087184624444, 0.005535990268762329, 0.0053756048376282705, 0.005081998319244572, 0.004687040371348002, 0.004223579289059315, 0.0037229597455075395, 0.0032130734702621737, 0.0027170434465039945],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q4": {
            "samples": [0.0, 0.0033695215815437857, 0.007312930858914043, 0.011833331925104714, 0.016904729129410285, 0.022467290293909772, 0.02842447161457115, 0.03464267620432228, 0.040953951708905166, 0.04716196765097761, 0.053051172280212354, 0.05839865007954254, 0.06298783492149682, 0.06662293498154592, 0.06914274414041854] + [0.07043248713590755] * 2 + [0.06914274414041854, 0.06662293498154592, 0.06298783492149682, 0.05839865007954254, 0.053051172280212354, 0.04716196765097761, 0.040953951708905166, 0.03464267620432228, 0.02842447161457115, 0.022467290293909772, 0.016904729129410285, 0.011833331925104714, 0.007312930858914043, 0.0033695215815437857, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q4": {
            "samples": [0.0013585217232519973, 0.0016065367351310869, 0.0018614798727537697, 0.0021117896445296577, 0.002343520185674001, 0.002540999159622286, 0.0026878024188141353, 0.0027679951343811647, 0.002767543592312222, 0.002675762250859991, 0.002486634546944434, 0.0021998397421277792, 0.0018213356124462444, 0.001363388095354369, 0.0008440000075467769, 0.00028576369123759475, -0.00028576369123759475, -0.0008440000075467769, -0.001363388095354369, -0.0018213356124462444, -0.0021998397421277792, -0.002486634546944434, -0.002675762250859991, -0.002767543592312222, -0.0027679951343811647, -0.0026878024188141353, -0.002540999159622286, -0.002343520185674001, -0.0021117896445296577, -0.0018614798727537697, -0.0016065367351310869, -0.0013585217232519973],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q4": {
            "samples": [0.0, -0.0016847607907718928, -0.0036564654294570214, -0.005916665962552357, -0.008452364564705142, -0.011233645146954886, -0.014212235807285575, -0.01732133810216114, -0.020476975854452583, -0.023580983825488806, -0.026525586140106177, -0.02919932503977127, -0.03149391746074841, -0.03331146749077296, -0.03457137207020927] + [-0.035216243567953776] * 2 + [-0.03457137207020927, -0.03331146749077296, -0.03149391746074841, -0.02919932503977127, -0.026525586140106177, -0.023580983825488806, -0.020476975854452583, -0.01732133810216114, -0.014212235807285575, -0.011233645146954886, -0.008452364564705142, -0.005916665962552357, -0.0036564654294570214, -0.0016847607907718928, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q4": {
            "sample": 0.21388562800000002,
            "type": "constant",
        },
        "x90_I_wf_q5": {
            "samples": [0.0, 0.0024070937766195385, 0.00522415717879925, 0.008453407685414676, 0.01207627471678022, 0.016050015806456708, 0.02030566270947739, 0.02474777747488551, 0.0292563795484928, 0.03369121582352001, 0.037898302043093975, 0.04171839347740419, 0.04499678122637469, 0.04759359698201814, 0.04939367951534094] + [0.05031503652782752] * 2 + [0.04939367951534094, 0.04759359698201814, 0.04499678122637469, 0.04171839347740419, 0.037898302043093975, 0.03369121582352001, 0.0292563795484928, 0.02474777747488551, 0.02030566270947739, 0.016050015806456708, 0.01207627471678022, 0.008453407685414676, 0.00522415717879925, 0.0024070937766195385, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q5": {
            "samples": [-0.0005085350420277795, -0.0006013744293785681, -0.0006968072200264041, -0.0007905056041827563, -0.0008772492303338852, -0.0009511714772862556, -0.001006124298654644, -0.0010361428145776582, -0.0010359737889661595, -0.001001617306081919, -0.0009308211876149381, -0.0008234653716389774, -0.0006817800307269992, -0.0005103566696832274, -0.00031593427765132026, -0.00010696983952943943, 0.00010696983952943943, 0.00031593427765132026, 0.0005103566696832274, 0.0006817800307269992, 0.0008234653716389774, 0.0009308211876149381, 0.001001617306081919, 0.0010359737889661595, 0.0010361428145776582, 0.001006124298654644, 0.0009511714772862556, 0.0008772492303338852, 0.0007905056041827563, 0.0006968072200264041, 0.0006013744293785681, 0.0005085350420277795],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q5": {
            "samples": [0.0, 0.004771186147728274, 0.010354987664854026, 0.01675579989508867, 0.02393681343224628, 0.03181330691408699, 0.0402485759304151, 0.04905344952578413, 0.05799010997838356, 0.06678055661921553, 0.07511957177853329, 0.08269151081616938, 0.08918971972132347, 0.09433696054836291, 0.0979049681312743] + [0.09973122262031289] * 2 + [0.0979049681312743, 0.09433696054836291, 0.08918971972132347, 0.08269151081616938, 0.07511957177853329, 0.06678055661921553, 0.05799010997838356, 0.04905344952578413, 0.0402485759304151, 0.03181330691408699, 0.02393681343224628, 0.01675579989508867, 0.010354987664854026, 0.004771186147728274, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q5": {
            "samples": [-0.0010079853854156088, -0.0011920056355588066, -0.0013811663625735464, -0.0015668892608227116, -0.0017388268859854566, -0.0018853507996334814, -0.001994274740461268, -0.002053775508041826, -0.0020534404763683503, -0.001985341270257586, -0.0018450137670154977, -0.0016322199876298393, -0.001351380436440954, -0.0010115960983510214, -0.0006262245633152881, -0.00021202872174940063, 0.00021202872174940063, 0.0006262245633152881, 0.0010115960983510214, 0.001351380436440954, 0.0016322199876298393, 0.0018450137670154977, 0.001985341270257586, 0.0020534404763683503, 0.002053775508041826, 0.001994274740461268, 0.0018853507996334814, 0.0017388268859854566, 0.0015668892608227116, 0.0013811663625735464, 0.0011920056355588066, 0.0010079853854156088],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q5": {
            "samples": [0.0, -0.0024070937766195385, -0.00522415717879925, -0.008453407685414676, -0.01207627471678022, -0.016050015806456708, -0.02030566270947739, -0.02474777747488551, -0.0292563795484928, -0.03369121582352001, -0.037898302043093975, -0.04171839347740419, -0.04499678122637469, -0.04759359698201814, -0.04939367951534094] + [-0.05031503652782752] * 2 + [-0.04939367951534094, -0.04759359698201814, -0.04499678122637469, -0.04171839347740419, -0.037898302043093975, -0.03369121582352001, -0.0292563795484928, -0.02474777747488551, -0.02030566270947739, -0.016050015806456708, -0.01207627471678022, -0.008453407685414676, -0.00522415717879925, -0.0024070937766195385, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q5": {
            "samples": [0.0005085350420277795, 0.0006013744293785681, 0.0006968072200264041, 0.0007905056041827563, 0.0008772492303338852, 0.0009511714772862556, 0.001006124298654644, 0.0010361428145776582, 0.0010359737889661595, 0.001001617306081919, 0.0009308211876149381, 0.0008234653716389774, 0.0006817800307269992, 0.0005103566696832274, 0.00031593427765132026, 0.00010696983952943943, -0.00010696983952943943, -0.00031593427765132026, -0.0005103566696832274, -0.0006817800307269992, -0.0008234653716389774, -0.0009308211876149381, -0.001001617306081919, -0.0010359737889661595, -0.0010361428145776582, -0.001006124298654644, -0.0009511714772862556, -0.0008772492303338852, -0.0007905056041827563, -0.0006968072200264041, -0.0006013744293785681, -0.0005085350420277795],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q5": {
            "samples": [0.0005039926927078044, 0.0005960028177794033, 0.0006905831812867732, 0.0007834446304113558, 0.0008694134429927283, 0.0009426753998167407, 0.000997137370230634, 0.001026887754020913, 0.0010267202381841751, 0.000992670635128793, 0.0009225068835077489, 0.0008161099938149197, 0.000675690218220477, 0.0005057980491755107, 0.00031311228165764403, 0.00010601436087470031, -0.00010601436087470031, -0.00031311228165764403, -0.0005057980491755107, -0.000675690218220477, -0.0008161099938149197, -0.0009225068835077489, -0.000992670635128793, -0.0010267202381841751, -0.001026887754020913, -0.000997137370230634, -0.0009426753998167407, -0.0008694134429927283, -0.0007834446304113558, -0.0006905831812867732, -0.0005960028177794033, -0.0005039926927078044],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q5": {
            "samples": [0.0, 0.002385593073864137, 0.005177493832427013, 0.008377899947544336, 0.01196840671612314, 0.015906653457043497, 0.02012428796520755, 0.024526724762892065, 0.02899505498919178, 0.033390278309607765, 0.037559785889266645, 0.04134575540808469, 0.04459485986066174, 0.047168480274181454, 0.04895248406563715] + [0.049865611310156446] * 2 + [0.04895248406563715, 0.047168480274181454, 0.04459485986066174, 0.04134575540808469, 0.037559785889266645, 0.033390278309607765, 0.02899505498919178, 0.024526724762892065, 0.02012428796520755, 0.015906653457043497, 0.01196840671612314, 0.008377899947544336, 0.005177493832427013, 0.002385593073864137, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q5": {
            "samples": [0.0010079853854156088, 0.0011920056355588066, 0.0013811663625735464, 0.0015668892608227116, 0.0017388268859854566, 0.0018853507996334814, 0.001994274740461268, 0.002053775508041826, 0.0020534404763683503, 0.001985341270257586, 0.0018450137670154977, 0.0016322199876298393, 0.001351380436440954, 0.0010115960983510214, 0.0006262245633152881, 0.00021202872174940063, -0.00021202872174940063, -0.0006262245633152881, -0.0010115960983510214, -0.001351380436440954, -0.0016322199876298393, -0.0018450137670154977, -0.001985341270257586, -0.0020534404763683503, -0.002053775508041826, -0.001994274740461268, -0.0018853507996334814, -0.0017388268859854566, -0.0015668892608227116, -0.0013811663625735464, -0.0011920056355588066, -0.0010079853854156088],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q5": {
            "samples": [0.0, 0.004771186147728274, 0.010354987664854026, 0.01675579989508867, 0.02393681343224628, 0.03181330691408699, 0.0402485759304151, 0.04905344952578413, 0.05799010997838356, 0.06678055661921553, 0.07511957177853329, 0.08269151081616938, 0.08918971972132347, 0.09433696054836291, 0.0979049681312743] + [0.09973122262031289] * 2 + [0.0979049681312743, 0.09433696054836291, 0.08918971972132347, 0.08269151081616938, 0.07511957177853329, 0.06678055661921553, 0.05799010997838356, 0.04905344952578413, 0.0402485759304151, 0.03181330691408699, 0.02393681343224628, 0.01675579989508867, 0.010354987664854026, 0.004771186147728274, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q5": {
            "samples": [-0.0005039926927078044, -0.0005960028177794033, -0.0006905831812867732, -0.0007834446304113558, -0.0008694134429927283, -0.0009426753998167407, -0.000997137370230634, -0.001026887754020913, -0.0010267202381841751, -0.000992670635128793, -0.0009225068835077489, -0.0008161099938149197, -0.000675690218220477, -0.0005057980491755107, -0.00031311228165764403, -0.00010601436087470031, 0.00010601436087470031, 0.00031311228165764403, 0.0005057980491755107, 0.000675690218220477, 0.0008161099938149197, 0.0009225068835077489, 0.000992670635128793, 0.0010267202381841751, 0.001026887754020913, 0.000997137370230634, 0.0009426753998167407, 0.0008694134429927283, 0.0007834446304113558, 0.0006905831812867732, 0.0005960028177794033, 0.0005039926927078044],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q5": {
            "samples": [0.0, -0.002385593073864137, -0.005177493832427013, -0.008377899947544336, -0.01196840671612314, -0.015906653457043497, -0.02012428796520755, -0.024526724762892065, -0.02899505498919178, -0.033390278309607765, -0.037559785889266645, -0.04134575540808469, -0.04459485986066174, -0.047168480274181454, -0.04895248406563715] + [-0.049865611310156446] * 2 + [-0.04895248406563715, -0.047168480274181454, -0.04459485986066174, -0.04134575540808469, -0.037559785889266645, -0.033390278309607765, -0.02899505498919178, -0.024526724762892065, -0.02012428796520755, -0.015906653457043497, -0.01196840671612314, -0.008377899947544336, -0.005177493832427013, -0.002385593073864137, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q5": {
            "sample": 0.056009617,
            "type": "constant",
        },
        "gft_cz_wf_1_2_q2": {
            "samples": [1.7134099282414948e-06, 2.638671054595603e-05, 0.000274955837812804, 0.001938627437084657, 0.00924867424157258, 0.029855086162189872, 0.06520950340242525, 0.0963733986591603] + [0.10119591000000001] * 8 + [0.0963733986591603, 0.06520950340242525, 0.029855086162189872, 0.00924867424157258, 0.001938627437084657, 0.000274955837812804, 2.638671054595603e-05, 1.7134099282414948e-06],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "g_cz_wf_1_2_q2": {
            "samples": [0.03931213024777564, 0.06088781843160629, 0.08859125307281902, 0.12108988595605871, 0.15548249127139938, 0.18754768422689555, 0.2125193682579723] + [0.22622568992333553] * 2 + [0.2125193682579723, 0.18754768422689555, 0.15548249127139938, 0.12108988595605871, 0.08859125307281902, 0.06088781843160629, 0.03931213024777564],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "cz_4c5t_wf": {
            "samples": [0.0] + [0.17576251507999996] * 39,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "cz_3c4t_wf": {
            "samples": [0.0] + [0.22160121899378024] * 47,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "cz_3c2t_wf": {
            "samples": [0.0] + [0.19218309803099998] * 63,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "cz_2c1t_wf": {
            "samples": [0.0] + [0.14464637680397693] * 23,
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
            "cosine": [(0.5210096318405759, 1800)],
            "sine": [(-0.8535507972753277, 1800)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(0.8535507972753277, 1800)],
            "sine": [(0.5210096318405759, 1800)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(-0.8535507972753277, 1800)],
            "sine": [(-0.5210096318405759, 1800)],
        },
        "rotated_cosine_weights_q2": {
            "cosine": [(-0.8348478632634064, 1800)],
            "sine": [(0.5504807400849958, 1800)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(-0.5504807400849958, 1800)],
            "sine": [(-0.8348478632634064, 1800)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(0.5504807400849958, 1800)],
            "sine": [(0.8348478632634064, 1800)],
        },
        "rotated_cosine_weights_q3": {
            "cosine": [(0.9573194975320672, 1800)],
            "sine": [(0.2890317969444716, 1800)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(-0.2890317969444716, 1800)],
            "sine": [(0.9573194975320672, 1800)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(0.2890317969444716, 1800)],
            "sine": [(-0.9573194975320672, 1800)],
        },
        "rotated_cosine_weights_q4": {
            "cosine": [(-0.41628079226040127, 1800)],
            "sine": [(-0.9092361090470685, 1800)],
        },
        "rotated_sine_weights_q4": {
            "cosine": [(0.9092361090470685, 1800)],
            "sine": [(-0.41628079226040127, 1800)],
        },
        "rotated_minus_sine_weights_q4": {
            "cosine": [(-0.9092361090470685, 1800)],
            "sine": [(0.41628079226040127, 1800)],
        },
        "rotated_cosine_weights_q5": {
            "cosine": [(-0.9973144772244582, 1800)],
            "sine": [(-0.07323819712763101, 1800)],
        },
        "rotated_sine_weights_q5": {
            "cosine": [(0.07323819712763101, 1800)],
            "sine": [(-0.9973144772244582, 1800)],
        },
        "rotated_minus_sine_weights_q5": {
            "cosine": [(-0.07323819712763101, 1800)],
            "sine": [(0.9973144772244582, 1800)],
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
            {'intermediate_frequency': 131235000.0, 'lo_frequency': 3200000000.0, 'correction': [0.909939993172884, 0.06435194984078407, 0.05217019096016884, 1.1224113143980503]},
        ],
        "octave_octave1_3": [
            {'intermediate_frequency': 471832000.0, 'lo_frequency': 3670000000.0, 'correction': [1.0509245730936527, 0.1871345043182373, 0.1878669261932373, 1.0468274168670177]},
            {'intermediate_frequency': 261857000.0, 'lo_frequency': 3200000000.0, 'correction': [0.8728884682059288, -0.00466681644320488, -0.003476236015558243, 1.1718457750976086]},
            {'intermediate_frequency': 262513000.0, 'lo_frequency': 3200000000.0, 'correction': [0.8368789926171303, 0.003159593790769577, 0.0021197572350502014, 1.247405406087637]},
            {'intermediate_frequency': 262884000.0, 'lo_frequency': 3200000000.0, 'correction': [0.869447585195303, -0.0047644078731536865, -0.0035155974328517914, 1.1782930493354797]},
            {'intermediate_frequency': 262526000.0, 'lo_frequency': 3200000000.0, 'correction': [0.8509256765246391, 0.0001483820378780365, 0.00010387226939201355, 1.2155497074127197]},
            {'intermediate_frequency': 262792000.0, 'lo_frequency': 3200000000.0, 'correction': [0.8692551776766777, -0.004460126161575317, -0.003289349377155304, 1.1786490269005299]},
        ],
        "octave_octave1_4": [
            {'intermediate_frequency': 106551000.0, 'lo_frequency': 3960000000.0, 'correction': [1.3551864996552467, -0.023040927946567535, -0.038992561399936676, 0.8007874302566051]},
            {'intermediate_frequency': 106458000.0, 'lo_frequency': 3960000000.0, 'correction': [1.2996150106191635, -0.023949556052684784, -0.038025788962841034, 0.818528775125742]},
            {'intermediate_frequency': 106481000.0, 'lo_frequency': 3960000000.0, 'correction': [1.3489361219108105, -0.02309318631887436, -0.03881271928548813, 0.8026037104427814]},
            {'intermediate_frequency': 106486000.0, 'lo_frequency': 3960000000.0, 'correction': [1.3209210634231567, -0.024531234055757523, -0.039934027940034866, 0.8114338889718056]},
            {'intermediate_frequency': 106443000.0, 'lo_frequency': 3960000000.0, 'correction': [1.3499723672866821, -0.0223989337682724, -0.03769315779209137, 0.8022129610180855]},
        ],
        "octave_octave1_5": [
            {'intermediate_frequency': 368712000.0, 'lo_frequency': 3960000000.0, 'correction': [1.5205974765121937, -0.035888671875, -0.071044921875, 0.7681368701159954]},
            {'intermediate_frequency': 368884000.0, 'lo_frequency': 3960000000.0, 'correction': [1.3623402081429958, -0.024932861328125, -0.042510986328125, 0.7990179099142551]},
            {'intermediate_frequency': 368950000.0, 'lo_frequency': 3960000000.0, 'correction': [1.4819180443882942, -0.02796586975455284, -0.053621333092451096, 0.772885050624609]},
            {'intermediate_frequency': 368836000.0, 'lo_frequency': 3960000000.0, 'correction': [1.4405015744268894, -0.036540985107421875, -0.06730270385742188, 0.7820985391736031]},
            {'intermediate_frequency': 368583000.0, 'lo_frequency': 3960000000.0, 'correction': [1.4771419242024422, -0.02573089674115181, -0.04914436861872673, 0.7733985595405102]},
            {'intermediate_frequency': 368508000.0, 'lo_frequency': 3960000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
        ],
        "octave_octave2_1": [
            {'intermediate_frequency': 122859000.0, 'lo_frequency': 4600000000.0, 'correction': [1.255867786705494, -0.0473419725894928, -0.0707947313785553, 0.8398260287940502]},
            {'intermediate_frequency': 122900000.0, 'lo_frequency': 4600000000.0, 'correction': [1.253316655755043, -0.04247363284230232, -0.06340106204152107, 0.8396217599511147]},
            {'intermediate_frequency': 122911000.0, 'lo_frequency': 4600000000.0, 'correction': [1.2556648589670658, -0.046525731682777405, -0.06957413256168365, 0.8396903276443481]},
            {'intermediate_frequency': 122888000.0, 'lo_frequency': 4600000000.0, 'correction': [1.2544812224805355, -0.04737443849444389, -0.07071657106280327, 0.84040192887187]},
            {'intermediate_frequency': 122908000.0, 'lo_frequency': 4600000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
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
            {'intermediate_frequency': 218194000.0, 'lo_frequency': 5900000000.0, 'correction': [1.113389290869236, -0.18521547317504883, -0.20657777786254883, 0.9982531815767288]},
            {'intermediate_frequency': 28632000.0, 'lo_frequency': 5900000000.0, 'correction': [1.089952491223812, -0.1585984230041504, -0.1741623878479004, 0.9925492443144321]},
        ],
    },
}



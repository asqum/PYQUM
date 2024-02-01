
# Single QUA script generated at 2024-01-26 10:17:32.662207
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
                wait(9250, )
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
                    "offset": 0.0,
                },
                "4": {
                    "offset": 0.0,
                },
                "5": {
                    "offset": 0.0,
                },
                "6": {
                    "offset": 0.0,
                },
                "7": {
                    "offset": 0.0150146484375,
                },
                "8": {
                    "offset": -0.0006103515625,
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
                    "offset": 0.008000000000000007,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "6": {
                    "offset": 0.0018,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "7": {
                    "offset": -0.032,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "8": {
                    "offset": 0.0018,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "9": {
                    "offset": 0.0095,
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
            "intermediate_frequency": -131052000,
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
            "intermediate_frequency": -99223000,
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
            "intermediate_frequency": -207885000,
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
            "intermediate_frequency": -364117000,
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
            "intermediate_frequency": -364117000,
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
            "intermediate_frequency": -128925000,
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
            "samples": [0.0, 0.00039553854454216306, 0.000858444131688, 0.0013890811420758993, 0.001984398020286004, 0.0026373712373101363, 0.0033366677908786098, 0.004066605122803545, 0.004807467784423178, 0.0055362091000068754, 0.006227526063316317, 0.006855251256502205, 0.00739396259848147, 0.007820676644443511, 0.008116469867043332] + [0.008267869125045842] * 2 + [0.008116469867043332, 0.007820676644443511, 0.00739396259848147, 0.006855251256502205, 0.006227526063316317, 0.0055362091000068754, 0.004807467784423178, 0.004066605122803545, 0.0033366677908786098, 0.0026373712373101363, 0.001984398020286004, 0.0013890811420758993, 0.000858444131688, 0.00039553854454216306, 0.0],
        },
        "x90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.0002604878496619217, -0.0003080431415814431, -0.00035692685729150653, -0.00040492215474113944, -0.0004493550035727267, -0.00048722033350951527, -0.0005153689193258006, -0.0005307453595247848, -0.0005306587792216822, -0.000513060294144279, -0.0004767962668112972, -0.0004218051976791304, -0.00034922945218947857, -0.00026142094538126524, -0.00016183160218758203, -5.4793359699649524e-05, 5.4793359699649524e-05, 0.00016183160218758203, 0.00026142094538126524, 0.00034922945218947857, 0.0004218051976791304, 0.0004767962668112972, 0.000513060294144279, 0.0005306587792216822, 0.0005307453595247848, 0.0005153689193258006, 0.00048722033350951527, 0.0004493550035727267, 0.00040492215474113944, 0.00035692685729150653, 0.0003080431415814431, 0.0002604878496619217],
        },
        "x180_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007905412930152419, 0.001715725415917432, 0.0027762806363937414, 0.003966107977238008, 0.0052711698944984, 0.006668815735307714, 0.008127701626865933, 0.00960842337837419, 0.011064918857372331, 0.012446616326807602, 0.013701216397336295, 0.014777909343514813, 0.015630759409070532, 0.01622194517310239] + [0.01652453860384222] * 2 + [0.01622194517310239, 0.015630759409070532, 0.014777909343514813, 0.013701216397336295, 0.012446616326807602, 0.011064918857372331, 0.00960842337837419, 0.008127701626865933, 0.006668815735307714, 0.0052711698944984, 0.003966107977238008, 0.0027762806363937414, 0.001715725415917432, 0.0007905412930152419, 0.0],
        },
        "x180_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.0005206228427746682, -0.0006156690082685806, -0.0007133702218621998, -0.0008092958023853374, -0.0008981013113612889, -0.0009737806789013761, -0.0010300397204911513, -0.0010607717719804618, -0.001060598728655838, -0.0010254255973891917, -0.0009529466659340054, -0.0008430390185102795, -0.000697985838554467, -0.0005224877702429396, -0.0003234439874682353, -0.0001095124963756669, 0.0001095124963756669, 0.0003234439874682353, 0.0005224877702429396, 0.000697985838554467, 0.0008430390185102795, 0.0009529466659340054, 0.0010254255973891917, 0.001060598728655838, 0.0010607717719804618, 0.0010300397204911513, 0.0009737806789013761, 0.0008981013113612889, 0.0008092958023853374, 0.0007133702218621998, 0.0006156690082685806, 0.0005206228427746682],
        },
        "minus_x90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, -0.00039553854454216306, -0.000858444131688, -0.0013890811420758993, -0.001984398020286004, -0.0026373712373101363, -0.0033366677908786098, -0.004066605122803545, -0.004807467784423178, -0.0055362091000068754, -0.006227526063316317, -0.006855251256502205, -0.00739396259848147, -0.007820676644443511, -0.008116469867043332] + [-0.008267869125045842] * 2 + [-0.008116469867043332, -0.007820676644443511, -0.00739396259848147, -0.006855251256502205, -0.006227526063316317, -0.0055362091000068754, -0.004807467784423178, -0.004066605122803545, -0.0033366677908786098, -0.0026373712373101363, -0.001984398020286004, -0.0013890811420758993, -0.000858444131688, -0.00039553854454216306, 0.0],
        },
        "minus_x90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0002604878496619217, 0.0003080431415814431, 0.00035692685729150653, 0.00040492215474113944, 0.0004493550035727267, 0.00048722033350951527, 0.0005153689193258006, 0.0005307453595247848, 0.0005306587792216822, 0.000513060294144279, 0.0004767962668112972, 0.0004218051976791304, 0.00034922945218947857, 0.00026142094538126524, 0.00016183160218758203, 5.4793359699649524e-05, -5.4793359699649524e-05, -0.00016183160218758203, -0.00026142094538126524, -0.00034922945218947857, -0.0004218051976791304, -0.0004767962668112972, -0.000513060294144279, -0.0005306587792216822, -0.0005307453595247848, -0.0005153689193258006, -0.00048722033350951527, -0.0004493550035727267, -0.00040492215474113944, -0.00035692685729150653, -0.0003080431415814431, -0.0002604878496619217],
        },
        "y90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0002603114213873341, 0.0003078345041342903, 0.0003566851109310999, 0.0004046479011926687, 0.00044905065568064443, 0.00048689033945068807, 0.0005150198602455756, 0.0005303858859902309, 0.000530299364327919, 0.0005127127986945958, 0.0004764733329670027, 0.00042151950925513977, 0.0003489929192772335, 0.0002612438851214698, 0.00016172199373411765, 5.475624818783345e-05, -5.475624818783345e-05, -0.00016172199373411765, -0.0002612438851214698, -0.0003489929192772335, -0.00042151950925513977, -0.0004764733329670027, -0.0005127127986945958, -0.000530299364327919, -0.0005303858859902309, -0.0005150198602455756, -0.00048689033945068807, -0.00044905065568064443, -0.0004046479011926687, -0.0003566851109310999, -0.0003078345041342903, -0.0002603114213873341],
        },
        "y90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.00039527064650762096, 0.000857862707958716, 0.0013881403181968707, 0.001983053988619004, 0.0026355849472492, 0.003334407867653857, 0.004063850813432967, 0.004804211689187095, 0.0055324594286861655, 0.006223308163403801, 0.006850608198668147, 0.007388954671757406, 0.007815379704535266, 0.008110972586551196] + [0.00826226930192111] * 2 + [0.008110972586551196, 0.007815379704535266, 0.007388954671757406, 0.006850608198668147, 0.006223308163403801, 0.0055324594286861655, 0.004804211689187095, 0.004063850813432967, 0.003334407867653857, 0.0026355849472492, 0.001983053988619004, 0.0013881403181968707, 0.000857862707958716, 0.00039527064650762096, 0.0],
        },
        "y180_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0005206228427746682, 0.0006156690082685806, 0.0007133702218621998, 0.0008092958023853374, 0.0008981013113612889, 0.0009737806789013761, 0.0010300397204911513, 0.0010607717719804618, 0.001060598728655838, 0.0010254255973891917, 0.0009529466659340054, 0.0008430390185102795, 0.000697985838554467, 0.0005224877702429396, 0.0003234439874682353, 0.0001095124963756669, -0.0001095124963756669, -0.0003234439874682353, -0.0005224877702429396, -0.000697985838554467, -0.0008430390185102795, -0.0009529466659340054, -0.0010254255973891917, -0.001060598728655838, -0.0010607717719804618, -0.0010300397204911513, -0.0009737806789013761, -0.0008981013113612889, -0.0008092958023853374, -0.0007133702218621998, -0.0006156690082685806, -0.0005206228427746682],
        },
        "y180_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007905412930152419, 0.001715725415917432, 0.0027762806363937414, 0.003966107977238008, 0.0052711698944984, 0.006668815735307714, 0.008127701626865933, 0.00960842337837419, 0.011064918857372331, 0.012446616326807602, 0.013701216397336295, 0.014777909343514813, 0.015630759409070532, 0.01622194517310239] + [0.01652453860384222] * 2 + [0.01622194517310239, 0.015630759409070532, 0.014777909343514813, 0.013701216397336295, 0.012446616326807602, 0.011064918857372331, 0.00960842337837419, 0.008127701626865933, 0.006668815735307714, 0.0052711698944984, 0.003966107977238008, 0.0027762806363937414, 0.001715725415917432, 0.0007905412930152419, 0.0],
        },
        "minus_y90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.0002603114213873341, -0.0003078345041342903, -0.0003566851109310999, -0.0004046479011926687, -0.00044905065568064443, -0.00048689033945068807, -0.0005150198602455756, -0.0005303858859902309, -0.000530299364327919, -0.0005127127986945958, -0.0004764733329670027, -0.00042151950925513977, -0.0003489929192772335, -0.0002612438851214698, -0.00016172199373411765, -5.475624818783345e-05, 5.475624818783345e-05, 0.00016172199373411765, 0.0002612438851214698, 0.0003489929192772335, 0.00042151950925513977, 0.0004764733329670027, 0.0005127127986945958, 0.000530299364327919, 0.0005303858859902309, 0.0005150198602455756, 0.00048689033945068807, 0.00044905065568064443, 0.0004046479011926687, 0.0003566851109310999, 0.0003078345041342903, 0.0002603114213873341],
        },
        "minus_y90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, -0.00039527064650762096, -0.000857862707958716, -0.0013881403181968707, -0.001983053988619004, -0.0026355849472492, -0.003334407867653857, -0.004063850813432967, -0.004804211689187095, -0.0055324594286861655, -0.006223308163403801, -0.006850608198668147, -0.007388954671757406, -0.007815379704535266, -0.008110972586551196] + [-0.00826226930192111] * 2 + [-0.008110972586551196, -0.007815379704535266, -0.007388954671757406, -0.006850608198668147, -0.006223308163403801, -0.0055324594286861655, -0.004804211689187095, -0.004063850813432967, -0.003334407867653857, -0.0026355849472492, -0.001983053988619004, -0.0013881403181968707, -0.000857862707958716, -0.00039527064650762096, 0.0],
        },
        "readout_wf_q1": {
            "type": "constant",
            "sample": 0.0868910316,
        },
        "x90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0011767776395012744, 0.002553980826573635, 0.004132693640110123, 0.005903837313367679, 0.007846515951366519, 0.00992701242629847, 0.012098669126508935, 0.014302830076599219, 0.016470928475586538, 0.018527684651326967, 0.020395247196837694, 0.021997982177118097, 0.023267510911240546, 0.02414753349077044] + [0.024597965601402445] * 2 + [0.02414753349077044, 0.023267510911240546, 0.021997982177118097, 0.020395247196837694, 0.018527684651326967, 0.016470928475586538, 0.014302830076599219, 0.012098669126508935, 0.00992701242629847, 0.007846515951366519, 0.005903837313367679, 0.004132693640110123, 0.002553980826573635, 0.0011767776395012744, 0.0],
        },
        "x90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.000450549977112142, 0.0005328034707538214, 0.0006173546581620267, 0.0007003692025850697, 0.0007772219964872851, 0.0008427153527359765, 0.0008914022481582638, 0.0009179979407739079, 0.0009178481880939582, 0.000887409159712699, 0.0008246854791031253, 0.0007295707742482685, 0.0006040409251144289, 0.00045216389597837445, 0.00027991027127087867, 9.477273888442422e-05, -9.477273888442422e-05, -0.00027991027127087867, -0.00045216389597837445, -0.0006040409251144289, -0.0007295707742482685, -0.0008246854791031253, -0.000887409159712699, -0.0009178481880939582, -0.0009179979407739079, -0.0008914022481582638, -0.0008427153527359765, -0.0007772219964872851, -0.0007003692025850697, -0.0006173546581620267, -0.0005328034707538214, -0.000450549977112142],
        },
        "x180_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.002331815702908935, 0.0050607798758452675, 0.008189040649518762, 0.011698608209928985, 0.015548076794079909, 0.01967063503044225, 0.023973829639938972, 0.028341432271594552, 0.03263757601405464, 0.03671309222600359, 0.040413716306209685, 0.04358957763223146, 0.04610518205752919, 0.047848969839502944] + [0.04874151285987445] * 2 + [0.047848969839502944, 0.04610518205752919, 0.04358957763223146, 0.040413716306209685, 0.03671309222600359, 0.03263757601405464, 0.028341432271594552, 0.023973829639938972, 0.01967063503044225, 0.015548076794079909, 0.011698608209928985, 0.008189040649518762, 0.0050607798758452675, 0.002331815702908935, 0.0],
        },
        "x180_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0008927765758878672, 0.0010557640270889915, 0.0012233044186464024, 0.0013877999118965302, 0.0015400857351634976, 0.0016698625353087063, 0.0017663368933018518, 0.001819036954544672, 0.0018187402156885463, 0.00175842448400045, 0.001634135868649435, 0.0014456635906988616, 0.0011969229080341824, 0.0008959745983767177, 0.0005546495310971008, 0.0001877946634268533, -0.0001877946634268533, -0.0005546495310971008, -0.0008959745983767177, -0.0011969229080341824, -0.0014456635906988616, -0.001634135868649435, -0.00175842448400045, -0.0018187402156885463, -0.001819036954544672, -0.0017663368933018518, -0.0016698625353087063, -0.0015400857351634976, -0.0013877999118965302, -0.0012233044186464024, -0.0010557640270889915, -0.0008927765758878672],
        },
        "minus_x90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, -0.0011767776395012744, -0.002553980826573635, -0.004132693640110123, -0.005903837313367679, -0.007846515951366519, -0.00992701242629847, -0.012098669126508935, -0.014302830076599219, -0.016470928475586538, -0.018527684651326967, -0.020395247196837694, -0.021997982177118097, -0.023267510911240546, -0.02414753349077044] + [-0.024597965601402445] * 2 + [-0.02414753349077044, -0.023267510911240546, -0.021997982177118097, -0.020395247196837694, -0.018527684651326967, -0.016470928475586538, -0.014302830076599219, -0.012098669126508935, -0.00992701242629847, -0.007846515951366519, -0.005903837313367679, -0.004132693640110123, -0.002553980826573635, -0.0011767776395012744, 0.0],
        },
        "minus_x90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.000450549977112142, -0.0005328034707538214, -0.0006173546581620267, -0.0007003692025850697, -0.0007772219964872851, -0.0008427153527359765, -0.0008914022481582638, -0.0009179979407739079, -0.0009178481880939582, -0.000887409159712699, -0.0008246854791031253, -0.0007295707742482685, -0.0006040409251144289, -0.00045216389597837445, -0.00027991027127087867, -9.477273888442422e-05, 9.477273888442422e-05, 0.00027991027127087867, 0.00045216389597837445, 0.0006040409251144289, 0.0007295707742482685, 0.0008246854791031253, 0.000887409159712699, 0.0009178481880939582, 0.0009179979407739079, 0.0008914022481582638, 0.0008427153527359765, 0.0007772219964872851, 0.0007003692025850697, 0.0006173546581620267, 0.0005328034707538214, 0.000450549977112142],
        },
        "y90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.0004463882879439336, -0.0005278820135444957, -0.0006116522093232012, -0.0006938999559482651, -0.0007700428675817488, -0.0008349312676543531, -0.0008831684466509259, -0.000909518477272336, -0.0009093701078442732, -0.000879212242000225, -0.0008170679343247175, -0.0007228317953494308, -0.0005984614540170912, -0.0004479872991883588, -0.0002773247655485504, -9.389733171342665e-05, 9.389733171342665e-05, 0.0002773247655485504, 0.0004479872991883588, 0.0005984614540170912, 0.0007228317953494308, 0.0008170679343247175, 0.000879212242000225, 0.0009093701078442732, 0.000909518477272336, 0.0008831684466509259, 0.0008349312676543531, 0.0007700428675817488, 0.0006938999559482651, 0.0006116522093232012, 0.0005278820135444957, 0.0004463882879439336],
        },
        "y90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0011659078514544676, 0.0025303899379226337, 0.004094520324759381, 0.0058493041049644924, 0.007774038397039954, 0.009835317515221126, 0.011986914819969486, 0.014170716135797276, 0.01631878800702732, 0.018356546113001793, 0.020206858153104842, 0.02179478881611573, 0.023052591028764596, 0.023924484919751472] + [0.024370756429937225] * 2 + [0.023924484919751472, 0.023052591028764596, 0.02179478881611573, 0.020206858153104842, 0.018356546113001793, 0.01631878800702732, 0.014170716135797276, 0.011986914819969486, 0.009835317515221126, 0.007774038397039954, 0.0058493041049644924, 0.004094520324759381, 0.0025303899379226337, 0.0011659078514544676, 0.0],
        },
        "y180_I_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.0008927765758878672, -0.0010557640270889915, -0.0012233044186464024, -0.0013877999118965302, -0.0015400857351634976, -0.0016698625353087063, -0.0017663368933018518, -0.001819036954544672, -0.0018187402156885463, -0.00175842448400045, -0.001634135868649435, -0.0014456635906988616, -0.0011969229080341824, -0.0008959745983767177, -0.0005546495310971008, -0.0001877946634268533, 0.0001877946634268533, 0.0005546495310971008, 0.0008959745983767177, 0.0011969229080341824, 0.0014456635906988616, 0.001634135868649435, 0.00175842448400045, 0.0018187402156885463, 0.001819036954544672, 0.0017663368933018518, 0.0016698625353087063, 0.0015400857351634976, 0.0013877999118965302, 0.0012233044186464024, 0.0010557640270889915, 0.0008927765758878672],
        },
        "y180_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.002331815702908935, 0.0050607798758452675, 0.008189040649518762, 0.011698608209928985, 0.015548076794079909, 0.01967063503044225, 0.023973829639938972, 0.028341432271594552, 0.03263757601405464, 0.03671309222600359, 0.040413716306209685, 0.04358957763223146, 0.04610518205752919, 0.047848969839502944] + [0.04874151285987445] * 2 + [0.047848969839502944, 0.04610518205752919, 0.04358957763223146, 0.040413716306209685, 0.03671309222600359, 0.03263757601405464, 0.028341432271594552, 0.023973829639938972, 0.01967063503044225, 0.015548076794079909, 0.011698608209928985, 0.008189040649518762, 0.0050607798758452675, 0.002331815702908935, 0.0],
        },
        "minus_y90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0004463882879439336, 0.0005278820135444957, 0.0006116522093232012, 0.0006938999559482651, 0.0007700428675817488, 0.0008349312676543531, 0.0008831684466509259, 0.000909518477272336, 0.0009093701078442732, 0.000879212242000225, 0.0008170679343247175, 0.0007228317953494308, 0.0005984614540170912, 0.0004479872991883588, 0.0002773247655485504, 9.389733171342665e-05, -9.389733171342665e-05, -0.0002773247655485504, -0.0004479872991883588, -0.0005984614540170912, -0.0007228317953494308, -0.0008170679343247175, -0.000879212242000225, -0.0009093701078442732, -0.000909518477272336, -0.0008831684466509259, -0.0008349312676543531, -0.0007700428675817488, -0.0006938999559482651, -0.0006116522093232012, -0.0005278820135444957, -0.0004463882879439336],
        },
        "minus_y90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, -0.0011659078514544676, -0.0025303899379226337, -0.004094520324759381, -0.0058493041049644924, -0.007774038397039954, -0.009835317515221126, -0.011986914819969486, -0.014170716135797276, -0.01631878800702732, -0.018356546113001793, -0.020206858153104842, -0.02179478881611573, -0.023052591028764596, -0.023924484919751472] + [-0.024370756429937225] * 2 + [-0.023924484919751472, -0.023052591028764596, -0.02179478881611573, -0.020206858153104842, -0.018356546113001793, -0.01631878800702732, -0.014170716135797276, -0.011986914819969486, -0.009835317515221126, -0.007774038397039954, -0.0058493041049644924, -0.004094520324759381, -0.0025303899379226337, -0.0011659078514544676, 0.0],
        },
        "readout_wf_q2": {
            "type": "constant",
            "sample": 0.1309075425,
        },
        "x90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0003914564519015011, 0.0008495846955578522, 0.0013747453510750155, 0.0019639183561255113, 0.002610152666915237, 0.003302232241621976, 0.004024636371405401, 0.004757853077756023, 0.005479073534494639, 0.006163255871034504, 0.006784502726200445, 0.007317654383453965, 0.007739964594971236, 0.008032705130661542] + [0.008182541896701078] * 2 + [0.008032705130661542, 0.007739964594971236, 0.007317654383453965, 0.006784502726200445, 0.006163255871034504, 0.005479073534494639, 0.004757853077756023, 0.004024636371405401, 0.003302232241621976, 0.002610152666915237, 0.0019639183561255113, 0.0013747453510750155, 0.0008495846955578522, 0.0003914564519015011, 0.0],
        },
        "x90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.00028111199180189496, 0.00033243247699752917, 0.0003851865640221966, 0.00043698189221390147, 0.0004849327146906164, 0.0005257960345444275, 0.0005561732864411759, 0.0005727671572753405, 0.0005726737219712079, 0.0005536818757134056, 0.0005145466416993674, 0.0004552016511551929, 0.0003768797163794159, 0.0002821189654344346, 0.00017464462963046707, 5.9131627454705774e-05, -5.9131627454705774e-05, -0.00017464462963046707, -0.0002821189654344346, -0.0003768797163794159, -0.0004552016511551929, -0.0005145466416993674, -0.0005536818757134056, -0.0005726737219712079, -0.0005727671572753405, -0.0005561732864411759, -0.0005257960345444275, -0.0004849327146906164, -0.00043698189221390147, -0.0003851865640221966, -0.00033243247699752917, -0.00028111199180189496],
        },
        "x180_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007852873575538541, 0.0017043227090830916, 0.002757829482209652, 0.0039397492335146705, 0.005236137712528403, 0.0066244948025661, 0.00807368494212819, 0.009544565820569556, 0.010991381434247478, 0.012363896145747502, 0.013610158147337039, 0.014679695394881048, 0.015526877421028502, 0.016114134165947307] + [0.016414716561501255] * 2 + [0.016114134165947307, 0.015526877421028502, 0.014679695394881048, 0.013610158147337039, 0.012363896145747502, 0.010991381434247478, 0.009544565820569556, 0.00807368494212819, 0.0066244948025661, 0.005236137712528403, 0.0039397492335146705, 0.002757829482209652, 0.0017043227090830916, 0.0007852873575538541, 0.0],
        },
        "x180_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0005639291219917285, 0.0006668813865716002, 0.0007727095505947881, 0.0008766143814175357, 0.0009728068812278295, 0.0010547813851937305, 0.0011157201480008583, 0.0011490085429568058, 0.0011488211055988877, 0.0011107222144184931, 0.0010322143641663057, 0.0009131644147220707, 0.0007560454685409223, 0.0005659491772473826, 0.0003503485995627169, 0.00011862192907079469, -0.00011862192907079469, -0.0003503485995627169, -0.0005659491772473826, -0.0007560454685409223, -0.0009131644147220707, -0.0010322143641663057, -0.0011107222144184931, -0.0011488211055988877, -0.0011490085429568058, -0.0011157201480008583, -0.0010547813851937305, -0.0009728068812278295, -0.0008766143814175357, -0.0007727095505947881, -0.0006668813865716002, -0.0005639291219917285],
        },
        "minus_x90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, -0.0003914564519015011, -0.0008495846955578522, -0.0013747453510750155, -0.0019639183561255113, -0.002610152666915237, -0.003302232241621976, -0.004024636371405401, -0.004757853077756023, -0.005479073534494639, -0.006163255871034504, -0.006784502726200445, -0.007317654383453965, -0.007739964594971236, -0.008032705130661542] + [-0.008182541896701078] * 2 + [-0.008032705130661542, -0.007739964594971236, -0.007317654383453965, -0.006784502726200445, -0.006163255871034504, -0.005479073534494639, -0.004757853077756023, -0.004024636371405401, -0.003302232241621976, -0.002610152666915237, -0.0019639183561255113, -0.0013747453510750155, -0.0008495846955578522, -0.0003914564519015011, 0.0],
        },
        "minus_x90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.00028111199180189496, -0.00033243247699752917, -0.0003851865640221966, -0.00043698189221390147, -0.0004849327146906164, -0.0005257960345444275, -0.0005561732864411759, -0.0005727671572753405, -0.0005726737219712079, -0.0005536818757134056, -0.0005145466416993674, -0.0004552016511551929, -0.0003768797163794159, -0.0002821189654344346, -0.00017464462963046707, -5.9131627454705774e-05, 5.9131627454705774e-05, 0.00017464462963046707, 0.0002821189654344346, 0.0003768797163794159, 0.0004552016511551929, 0.0005145466416993674, 0.0005536818757134056, 0.0005726737219712079, 0.0005727671572753405, 0.0005561732864411759, 0.0005257960345444275, 0.0004849327146906164, 0.00043698189221390147, 0.0003851865640221966, 0.00033243247699752917, 0.00028111199180189496],
        },
        "y90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.00028196456099586424, -0.0003334406932858001, -0.00038635477529739404, -0.00043830719070876787, -0.00048640344061391476, -0.0005273906925968653, -0.0005578600740004291, -0.0005745042714784029, -0.0005744105527994438, -0.0005553611072092466, -0.0005161071820831528, -0.0004565822073610353, -0.00037802273427046116, -0.0002829745886236913, -0.00017517429978135846, -5.9310964535397346e-05, 5.9310964535397346e-05, 0.00017517429978135846, 0.0002829745886236913, 0.00037802273427046116, 0.0004565822073610353, 0.0005161071820831528, 0.0005553611072092466, 0.0005744105527994438, 0.0005745042714784029, 0.0005578600740004291, 0.0005273906925968653, 0.00048640344061391476, 0.00043830719070876787, 0.00038635477529739404, 0.0003334406932858001, 0.00028196456099586424],
        },
        "y90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.00039264367877692706, 0.0008521613545415458, 0.001378914741104826, 0.0019698746167573352, 0.0026180688562642013, 0.00331224740128305, 0.004036842471064095, 0.004772282910284778, 0.005495690717123739, 0.006181948072873751, 0.0068050790736685195, 0.007339847697440524, 0.007763438710514251, 0.008057067082973653] + [0.008207358280750627] * 2 + [0.008057067082973653, 0.007763438710514251, 0.007339847697440524, 0.0068050790736685195, 0.006181948072873751, 0.005495690717123739, 0.004772282910284778, 0.004036842471064095, 0.00331224740128305, 0.0026180688562642013, 0.0019698746167573352, 0.001378914741104826, 0.0008521613545415458, 0.00039264367877692706, 0.0],
        },
        "y180_I_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.0005639291219917285, -0.0006668813865716002, -0.0007727095505947881, -0.0008766143814175357, -0.0009728068812278295, -0.0010547813851937305, -0.0011157201480008583, -0.0011490085429568058, -0.0011488211055988877, -0.0011107222144184931, -0.0010322143641663057, -0.0009131644147220707, -0.0007560454685409223, -0.0005659491772473826, -0.0003503485995627169, -0.00011862192907079469, 0.00011862192907079469, 0.0003503485995627169, 0.0005659491772473826, 0.0007560454685409223, 0.0009131644147220707, 0.0010322143641663057, 0.0011107222144184931, 0.0011488211055988877, 0.0011490085429568058, 0.0011157201480008583, 0.0010547813851937305, 0.0009728068812278295, 0.0008766143814175357, 0.0007727095505947881, 0.0006668813865716002, 0.0005639291219917285],
        },
        "y180_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007852873575538541, 0.0017043227090830916, 0.002757829482209652, 0.0039397492335146705, 0.005236137712528403, 0.0066244948025661, 0.00807368494212819, 0.009544565820569556, 0.010991381434247478, 0.012363896145747502, 0.013610158147337039, 0.014679695394881048, 0.015526877421028502, 0.016114134165947307] + [0.016414716561501255] * 2 + [0.016114134165947307, 0.015526877421028502, 0.014679695394881048, 0.013610158147337039, 0.012363896145747502, 0.010991381434247478, 0.009544565820569556, 0.00807368494212819, 0.0066244948025661, 0.005236137712528403, 0.0039397492335146705, 0.002757829482209652, 0.0017043227090830916, 0.0007852873575538541, 0.0],
        },
        "minus_y90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.00028196456099586424, 0.0003334406932858001, 0.00038635477529739404, 0.00043830719070876787, 0.00048640344061391476, 0.0005273906925968653, 0.0005578600740004291, 0.0005745042714784029, 0.0005744105527994438, 0.0005553611072092466, 0.0005161071820831528, 0.0004565822073610353, 0.00037802273427046116, 0.0002829745886236913, 0.00017517429978135846, 5.9310964535397346e-05, -5.9310964535397346e-05, -0.00017517429978135846, -0.0002829745886236913, -0.00037802273427046116, -0.0004565822073610353, -0.0005161071820831528, -0.0005553611072092466, -0.0005744105527994438, -0.0005745042714784029, -0.0005578600740004291, -0.0005273906925968653, -0.00048640344061391476, -0.00043830719070876787, -0.00038635477529739404, -0.0003334406932858001, -0.00028196456099586424],
        },
        "minus_y90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, -0.00039264367877692706, -0.0008521613545415458, -0.001378914741104826, -0.0019698746167573352, -0.0026180688562642013, -0.00331224740128305, -0.004036842471064095, -0.004772282910284778, -0.005495690717123739, -0.006181948072873751, -0.0068050790736685195, -0.007339847697440524, -0.007763438710514251, -0.008057067082973653] + [-0.008207358280750627] * 2 + [-0.008057067082973653, -0.007763438710514251, -0.007339847697440524, -0.0068050790736685195, -0.006181948072873751, -0.005495690717123739, -0.004772282910284778, -0.004036842471064095, -0.00331224740128305, -0.0026180688562642013, -0.0019698746167573352, -0.001378914741104826, -0.0008521613545415458, -0.00039264367877692706, 0.0],
        },
        "readout_wf_q3": {
            "type": "constant",
            "sample": 0.102461516,
        },
        "x90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0015929601412333159, 0.003457228894942401, 0.005594273738421689, 0.007991805082654709, 0.010621536931459287, 0.013437827662431684, 0.016377518601276883, 0.019361209334765685, 0.022296083533532976, 0.025080237904088906, 0.027608287891102277, 0.02977785064862464, 0.03149636449841577, 0.03268761834750365] + [0.03329735154983784] * 2 + [0.03268761834750365, 0.03149636449841577, 0.02977785064862464, 0.027608287891102277, 0.025080237904088906, 0.022296083533532976, 0.019361209334765685, 0.016377518601276883, 0.013437827662431684, 0.010621536931459287, 0.007991805082654709, 0.005594273738421689, 0.003457228894942401, 0.0015929601412333159, 0.0],
        },
        "x90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0015975270321798617, 0.0018891754313786727, 0.0021889708244520003, 0.002483317701639608, 0.0027558166961890586, 0.002988038230648106, 0.003160668650137971, 0.003254969704519032, 0.0032544387224604046, 0.00314651025027618, 0.002924109228365419, 0.0025868584906395516, 0.0021417639672258824, 0.0016032495472115505, 0.000992485290546863, 0.00033603821989298905, -0.00033603821989298905, -0.000992485290546863, -0.0016032495472115505, -0.0021417639672258824, -0.0025868584906395516, -0.002924109228365419, -0.00314651025027618, -0.0032544387224604046, -0.003254969704519032, -0.003160668650137971, -0.002988038230648106, -0.0027558166961890586, -0.002483317701639608, -0.0021889708244520003, -0.0018891754313786727, -0.0015975270321798617],
        },
        "x180_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0031695503085252073, 0.006878929752833022, 0.011131058207056467, 0.015901482786499603, 0.02113392217840044, 0.026737562171764734, 0.0325867344649093, 0.03852345418568736, 0.04436304249766073, 0.049902740017866834, 0.05493286061467074, 0.059249690728289166, 0.06266905820762429, 0.06503932404615623] + [0.06625252455855582] * 2 + [0.06503932404615623, 0.06266905820762429, 0.059249690728289166, 0.05493286061467074, 0.049902740017866834, 0.04436304249766073, 0.03852345418568736, 0.0325867344649093, 0.026737562171764734, 0.02113392217840044, 0.015901482786499603, 0.011131058207056467, 0.006878929752833022, 0.0031695503085252073, 0.0],
        },
        "x180_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0031786371589955635, 0.003758936847439608, 0.004355446801464143, 0.004941115715113858, 0.00548331338214294, 0.005945370038263041, 0.006288856849509498, 0.006476489878278399, 0.006475433370771288, 0.006260685547862604, 0.005818168996840925, 0.0051471332614572525, 0.004261518205881264, 0.003190023381924021, 0.0019747713564408605, 0.0006686231600958084, -0.0006686231600958084, -0.0019747713564408605, -0.003190023381924021, -0.004261518205881264, -0.0051471332614572525, -0.005818168996840925, -0.006260685547862604, -0.006475433370771288, -0.006476489878278399, -0.006288856849509498, -0.005945370038263041, -0.00548331338214294, -0.004941115715113858, -0.004355446801464143, -0.003758936847439608, -0.0031786371589955635],
        },
        "minus_x90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, -0.0015929601412333159, -0.003457228894942401, -0.005594273738421689, -0.007991805082654709, -0.010621536931459287, -0.013437827662431684, -0.016377518601276883, -0.019361209334765685, -0.022296083533532976, -0.025080237904088906, -0.027608287891102277, -0.02977785064862464, -0.03149636449841577, -0.03268761834750365] + [-0.03329735154983784] * 2 + [-0.03268761834750365, -0.03149636449841577, -0.02977785064862464, -0.027608287891102277, -0.025080237904088906, -0.022296083533532976, -0.019361209334765685, -0.016377518601276883, -0.013437827662431684, -0.010621536931459287, -0.007991805082654709, -0.005594273738421689, -0.003457228894942401, -0.0015929601412333159, 0.0],
        },
        "minus_x90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.0015975270321798617, -0.0018891754313786727, -0.0021889708244520003, -0.002483317701639608, -0.0027558166961890586, -0.002988038230648106, -0.003160668650137971, -0.003254969704519032, -0.0032544387224604046, -0.00314651025027618, -0.002924109228365419, -0.0025868584906395516, -0.0021417639672258824, -0.0016032495472115505, -0.000992485290546863, -0.00033603821989298905, 0.00033603821989298905, 0.000992485290546863, 0.0016032495472115505, 0.0021417639672258824, 0.0025868584906395516, 0.002924109228365419, 0.00314651025027618, 0.0032544387224604046, 0.003254969704519032, 0.003160668650137971, 0.002988038230648106, 0.0027558166961890586, 0.002483317701639608, 0.0021889708244520003, 0.0018891754313786727, 0.0015975270321798617],
        },
        "y90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.0015893185794977817, -0.001879468423719804, -0.0021777234007320716, -0.002470557857556929, -0.00274165669107147, -0.0029726850191315207, -0.003144428424754749, -0.0032382449391391995, -0.003237716685385644, -0.003130342773931302, -0.0029090844984204626, -0.0025735666307286262, -0.002130759102940632, -0.0015950116909620104, -0.0009873856782204302, -0.0003343115800479042, 0.0003343115800479042, 0.0009873856782204302, 0.0015950116909620104, 0.002130759102940632, 0.0025735666307286262, 0.0029090844984204626, 0.003130342773931302, 0.003237716685385644, 0.0032382449391391995, 0.003144428424754749, 0.0029726850191315207, 0.00274165669107147, 0.002470557857556929, 0.0021777234007320716, 0.001879468423719804, 0.0015893185794977817],
        },
        "y90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0015847751542626036, 0.003439464876416511, 0.005565529103528233, 0.007950741393249802, 0.01056696108920022, 0.013368781085882367, 0.01629336723245465, 0.01926172709284368, 0.022181521248830365, 0.024951370008933417, 0.02746643030733537, 0.029624845364144583, 0.031334529103812146, 0.032519662023078114] + [0.03312626227927791] * 2 + [0.032519662023078114, 0.031334529103812146, 0.029624845364144583, 0.02746643030733537, 0.024951370008933417, 0.022181521248830365, 0.01926172709284368, 0.01629336723245465, 0.013368781085882367, 0.01056696108920022, 0.007950741393249802, 0.005565529103528233, 0.003439464876416511, 0.0015847751542626036, 0.0],
        },
        "y180_I_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.0031786371589955635, -0.003758936847439608, -0.004355446801464143, -0.004941115715113858, -0.00548331338214294, -0.005945370038263041, -0.006288856849509498, -0.006476489878278399, -0.006475433370771288, -0.006260685547862604, -0.005818168996840925, -0.0051471332614572525, -0.004261518205881264, -0.003190023381924021, -0.0019747713564408605, -0.0006686231600958084, 0.0006686231600958084, 0.0019747713564408605, 0.003190023381924021, 0.004261518205881264, 0.0051471332614572525, 0.005818168996840925, 0.006260685547862604, 0.006475433370771288, 0.006476489878278399, 0.006288856849509498, 0.005945370038263041, 0.00548331338214294, 0.004941115715113858, 0.004355446801464143, 0.003758936847439608, 0.0031786371589955635],
        },
        "y180_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0031695503085252073, 0.006878929752833022, 0.011131058207056467, 0.015901482786499603, 0.02113392217840044, 0.026737562171764734, 0.0325867344649093, 0.03852345418568736, 0.04436304249766073, 0.049902740017866834, 0.05493286061467074, 0.059249690728289166, 0.06266905820762429, 0.06503932404615623] + [0.06625252455855582] * 2 + [0.06503932404615623, 0.06266905820762429, 0.059249690728289166, 0.05493286061467074, 0.049902740017866834, 0.04436304249766073, 0.03852345418568736, 0.0325867344649093, 0.026737562171764734, 0.02113392217840044, 0.015901482786499603, 0.011131058207056467, 0.006878929752833022, 0.0031695503085252073, 0.0],
        },
        "minus_y90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0015893185794977817, 0.001879468423719804, 0.0021777234007320716, 0.002470557857556929, 0.00274165669107147, 0.0029726850191315207, 0.003144428424754749, 0.0032382449391391995, 0.003237716685385644, 0.003130342773931302, 0.0029090844984204626, 0.0025735666307286262, 0.002130759102940632, 0.0015950116909620104, 0.0009873856782204302, 0.0003343115800479042, -0.0003343115800479042, -0.0009873856782204302, -0.0015950116909620104, -0.002130759102940632, -0.0025735666307286262, -0.0029090844984204626, -0.003130342773931302, -0.003237716685385644, -0.0032382449391391995, -0.003144428424754749, -0.0029726850191315207, -0.00274165669107147, -0.002470557857556929, -0.0021777234007320716, -0.001879468423719804, -0.0015893185794977817],
        },
        "minus_y90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, -0.0015847751542626036, -0.003439464876416511, -0.005565529103528233, -0.007950741393249802, -0.01056696108920022, -0.013368781085882367, -0.01629336723245465, -0.01926172709284368, -0.022181521248830365, -0.024951370008933417, -0.02746643030733537, -0.029624845364144583, -0.031334529103812146, -0.032519662023078114] + [-0.03312626227927791] * 2 + [-0.032519662023078114, -0.031334529103812146, -0.029624845364144583, -0.02746643030733537, -0.024951370008933417, -0.022181521248830365, -0.01926172709284368, -0.01629336723245465, -0.013368781085882367, -0.01056696108920022, -0.007950741393249802, -0.005565529103528233, -0.003439464876416511, -0.0015847751542626036, 0.0],
        },
        "readout_wf_q4": {
            "type": "constant",
            "sample": 0.21388562800000002,
        },
        "x90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.002424713297309757, 0.00526239712873177, 0.008515285204713157, 0.01216467101205539, 0.016167499216669906, 0.020454296737662497, 0.024928927034363033, 0.029470531315151236, 0.033937829844148185, 0.03817571122567691, 0.04202376508534801, 0.04532615008001563, 0.047941974089255046, 0.049755232923288706] + [0.05068333411379704] * 2 + [0.049755232923288706, 0.047941974089255046, 0.04532615008001563, 0.04202376508534801, 0.03817571122567691, 0.033937829844148185, 0.029470531315151236, 0.024928927034363033, 0.020454296737662497, 0.016167499216669906, 0.01216467101205539, 0.008515285204713157, 0.00526239712873177, 0.002424713297309757, 0.0],
        },
        "x90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.00017884902826885524, -0.0002115001394814772, -0.00024506333662968507, -0.0002780165523803709, -0.00030852381729526104, -0.00033452187237945633, -0.00035384848291779427, -0.00036440583287247253, -0.0003643463874776212, -0.0003522633979670452, -0.0003273647853905404, -0.00028960832461696445, -0.0002397783552976338, -0.00017948968487876242, -0.00011111237945265272, -3.7620714941548775e-05, 3.7620714941548775e-05, 0.00011111237945265272, 0.00017948968487876242, 0.0002397783552976338, 0.00028960832461696445, 0.0003273647853905404, 0.0003522633979670452, 0.0003643463874776212, 0.00036440583287247253, 0.00035384848291779427, 0.00033452187237945633, 0.00030852381729526104, 0.0002780165523803709, 0.00024506333662968507, 0.0002115001394814772, 0.00017884902826885524],
        },
        "x180_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.00480381199779446, 0.010425796110496325, 0.016870377737618757, 0.02410049576655942, 0.03203084950189457, 0.04052379973494186, 0.0493888819402623, 0.05838665217457876, 0.06723720877239805, 0.07563324695489362, 0.08325696367214713, 0.08979960798243405, 0.09498204615920536, 0.09857445213631702] + [0.10041319473696919] * 2 + [0.09857445213631702, 0.09498204615920536, 0.08979960798243405, 0.08325696367214713, 0.07563324695489362, 0.06723720877239805, 0.05838665217457876, 0.0493888819402623, 0.04052379973494186, 0.03203084950189457, 0.02410049576655942, 0.016870377737618757, 0.010425796110496325, 0.00480381199779446, 0.0],
        },
        "x180_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.00035433348295035535, -0.0004190214606830385, -0.00048551645179138503, -0.0005508029552987027, -0.0006112435712596262, -0.0006627505964701305, -0.0007010402382532548, -0.0007219563294189474, -0.0007218385569378391, -0.0006978998875518418, -0.0006485710642405842, -0.0005737684310964526, -0.0004750459121365747, -0.00035560274390279586, -0.0002201344720261808, -7.4533695180511e-05, 7.4533695180511e-05, 0.0002201344720261808, 0.00035560274390279586, 0.0004750459121365747, 0.0005737684310964526, 0.0006485710642405842, 0.0006978998875518418, 0.0007218385569378391, 0.0007219563294189474, 0.0007010402382532548, 0.0006627505964701305, 0.0006112435712596262, 0.0005508029552987027, 0.00048551645179138503, 0.0004190214606830385, 0.00035433348295035535],
        },
        "minus_x90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, -0.002424713297309757, -0.00526239712873177, -0.008515285204713157, -0.01216467101205539, -0.016167499216669906, -0.020454296737662497, -0.024928927034363033, -0.029470531315151236, -0.033937829844148185, -0.03817571122567691, -0.04202376508534801, -0.04532615008001563, -0.047941974089255046, -0.049755232923288706] + [-0.05068333411379704] * 2 + [-0.049755232923288706, -0.047941974089255046, -0.04532615008001563, -0.04202376508534801, -0.03817571122567691, -0.033937829844148185, -0.029470531315151236, -0.024928927034363033, -0.020454296737662497, -0.016167499216669906, -0.01216467101205539, -0.008515285204713157, -0.00526239712873177, -0.002424713297309757, 0.0],
        },
        "minus_x90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.00017884902826885524, 0.0002115001394814772, 0.00024506333662968507, 0.0002780165523803709, 0.00030852381729526104, 0.00033452187237945633, 0.00035384848291779427, 0.00036440583287247253, 0.0003643463874776212, 0.0003522633979670452, 0.0003273647853905404, 0.00028960832461696445, 0.0002397783552976338, 0.00017948968487876242, 0.00011111237945265272, 3.7620714941548775e-05, -3.7620714941548775e-05, -0.00011111237945265272, -0.00017948968487876242, -0.0002397783552976338, -0.00028960832461696445, -0.0003273647853905404, -0.0003522633979670452, -0.0003643463874776212, -0.00036440583287247253, -0.00035384848291779427, -0.00033452187237945633, -0.00030852381729526104, -0.0002780165523803709, -0.00024506333662968507, -0.0002115001394814772, -0.00017884902826885524],
        },
        "y90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.00017716674147517767, 0.00020951073034151924, 0.00024275822589569251, 0.0002754014776493514, 0.0003056217856298131, 0.00033137529823506524, 0.0003505201191266274, 0.0003609781647094737, 0.00036091927846891955, 0.0003489499437759209, 0.0003242855321202921, 0.0002868842155482263, 0.00023752295606828736, 0.00017780137195139793, 0.0001100672360130904, 3.72668475902555e-05, -3.72668475902555e-05, -0.0001100672360130904, -0.00017780137195139793, -0.00023752295606828736, -0.0002868842155482263, -0.0003242855321202921, -0.0003489499437759209, -0.00036091927846891955, -0.0003609781647094737, -0.0003505201191266274, -0.00033137529823506524, -0.0003056217856298131, -0.0002754014776493514, -0.00024275822589569251, -0.00020951073034151924, -0.00017716674147517767],
        },
        "y90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.00240190599889723, 0.0052128980552481625, 0.008435188868809378, 0.01205024788327971, 0.016015424750947284, 0.02026189986747093, 0.02469444097013115, 0.02919332608728938, 0.03361860438619903, 0.03781662347744681, 0.041628481836073566, 0.04489980399121703, 0.04749102307960268, 0.04928722606815851] + [0.050206597368484596] * 2 + [0.04928722606815851, 0.04749102307960268, 0.04489980399121703, 0.041628481836073566, 0.03781662347744681, 0.03361860438619903, 0.02919332608728938, 0.02469444097013115, 0.02026189986747093, 0.016015424750947284, 0.01205024788327971, 0.008435188868809378, 0.0052128980552481625, 0.00240190599889723, 0.0],
        },
        "y180_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.00035433348295035535, 0.0004190214606830385, 0.00048551645179138503, 0.0005508029552987027, 0.0006112435712596262, 0.0006627505964701305, 0.0007010402382532548, 0.0007219563294189474, 0.0007218385569378391, 0.0006978998875518418, 0.0006485710642405842, 0.0005737684310964526, 0.0004750459121365747, 0.00035560274390279586, 0.0002201344720261808, 7.4533695180511e-05, -7.4533695180511e-05, -0.0002201344720261808, -0.00035560274390279586, -0.0004750459121365747, -0.0005737684310964526, -0.0006485710642405842, -0.0006978998875518418, -0.0007218385569378391, -0.0007219563294189474, -0.0007010402382532548, -0.0006627505964701305, -0.0006112435712596262, -0.0005508029552987027, -0.00048551645179138503, -0.0004190214606830385, -0.00035433348295035535],
        },
        "y180_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.00480381199779446, 0.010425796110496325, 0.016870377737618757, 0.02410049576655942, 0.03203084950189457, 0.04052379973494186, 0.0493888819402623, 0.05838665217457876, 0.06723720877239805, 0.07563324695489362, 0.08325696367214713, 0.08979960798243405, 0.09498204615920536, 0.09857445213631702] + [0.10041319473696919] * 2 + [0.09857445213631702, 0.09498204615920536, 0.08979960798243405, 0.08325696367214713, 0.07563324695489362, 0.06723720877239805, 0.05838665217457876, 0.0493888819402623, 0.04052379973494186, 0.03203084950189457, 0.02410049576655942, 0.016870377737618757, 0.010425796110496325, 0.00480381199779446, 0.0],
        },
        "minus_y90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.00017716674147517767, -0.00020951073034151924, -0.00024275822589569251, -0.0002754014776493514, -0.0003056217856298131, -0.00033137529823506524, -0.0003505201191266274, -0.0003609781647094737, -0.00036091927846891955, -0.0003489499437759209, -0.0003242855321202921, -0.0002868842155482263, -0.00023752295606828736, -0.00017780137195139793, -0.0001100672360130904, -3.72668475902555e-05, 3.72668475902555e-05, 0.0001100672360130904, 0.00017780137195139793, 0.00023752295606828736, 0.0002868842155482263, 0.0003242855321202921, 0.0003489499437759209, 0.00036091927846891955, 0.0003609781647094737, 0.0003505201191266274, 0.00033137529823506524, 0.0003056217856298131, 0.0002754014776493514, 0.00024275822589569251, 0.00020951073034151924, 0.00017716674147517767],
        },
        "minus_y90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, -0.00240190599889723, -0.0052128980552481625, -0.008435188868809378, -0.01205024788327971, -0.016015424750947284, -0.02026189986747093, -0.02469444097013115, -0.02919332608728938, -0.03361860438619903, -0.03781662347744681, -0.041628481836073566, -0.04489980399121703, -0.04749102307960268, -0.04928722606815851] + [-0.050206597368484596] * 2 + [-0.04928722606815851, -0.04749102307960268, -0.04489980399121703, -0.041628481836073566, -0.03781662347744681, -0.03361860438619903, -0.02919332608728938, -0.02469444097013115, -0.02026189986747093, -0.016015424750947284, -0.01205024788327971, -0.008435188868809378, -0.0052128980552481625, -0.00240190599889723, 0.0],
        },
        "readout_wf_q5": {
            "type": "constant",
            "sample": 0.056009617,
        },
        "gft_cz_wf_1_2_q2": {
            "type": "arbitrary",
            "samples": [2.4279239730461816e-06, 3.7390309258980545e-05, 0.0003896159693902593, 0.0027470600886115074, 0.013105490717597775, 0.04230504225275136, 0.0924027075900485, 0.13656234921473673] + [0.14339591000000002] * 8 + [0.13656234921473673, 0.0924027075900485, 0.04230504225275136, 0.013105490717597775, 0.0027470600886115074, 0.0003896159693902593, 3.7390309258980545e-05, 2.4279239730461816e-06],
        },
        "g_cz_wf_1_2_q2": {
            "type": "arbitrary",
            "samples": [0.04295022651193382, 0.06652261215488213, 0.0967898295633299, 0.1322960113669045, 0.16987144112151573, 0.20490407079350736, 0.2321867308467583] + [0.24716148842062666] * 2 + [0.2321867308467583, 0.20490407079350736, 0.16987144112151573, 0.1322960113669045, 0.0967898295633299, 0.06652261215488213, 0.04295022651193382],
        },
        "cz_4c5t_wf": {
            "type": "arbitrary",
            "samples": [0.0] + [0.18326382712099998] * 39,
        },
        "cz_3c4t_wf": {
            "type": "arbitrary",
            "samples": [0.0] + [0.15726814504911504] * 47,
        },
        "cz_3c2t_wf": {
            "type": "arbitrary",
            "samples": [0.0] + [0.2674505421331572] * 51,
        },
        "cz_2c3t_wf": {
            "type": "arbitrary",
            "samples": [0.0] + [0.047] * 31,
        },
        "cz_2c1t_wf": {
            "type": "arbitrary",
            "samples": [0.0] + [-0.14656833826000001] * 23,
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
            "cosine": [(0.869494929505219, 1800)],
            "sine": [(0.493941866584231, 1800)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(-0.493941866584231, 1800)],
            "sine": [(0.869494929505219, 1800)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(0.493941866584231, 1800)],
            "sine": [(-0.869494929505219, 1800)],
        },
        "rotated_cosine_weights_q2": {
            "cosine": [(-0.9510565162951535, 1800)],
            "sine": [(0.3090169943749475, 1800)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(-0.3090169943749475, 1800)],
            "sine": [(-0.9510565162951535, 1800)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(0.3090169943749475, 1800)],
            "sine": [(0.9510565162951535, 1800)],
        },
        "rotated_cosine_weights_q3": {
            "cosine": [(0.5165333288666419, 1800)],
            "sine": [(0.8562670846003282, 1800)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(-0.8562670846003282, 1800)],
            "sine": [(0.5165333288666419, 1800)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(0.8562670846003282, 1800)],
            "sine": [(-0.5165333288666419, 1800)],
        },
        "rotated_cosine_weights_q4": {
            "cosine": [(-0.6560590289905077, 1800)],
            "sine": [(-0.7547095802227717, 1800)],
        },
        "rotated_sine_weights_q4": {
            "cosine": [(0.7547095802227717, 1800)],
            "sine": [(-0.6560590289905077, 1800)],
        },
        "rotated_minus_sine_weights_q4": {
            "cosine": [(-0.7547095802227717, 1800)],
            "sine": [(0.6560590289905077, 1800)],
        },
        "rotated_cosine_weights_q5": {
            "cosine": [(-0.8845809752150838, 1800)],
            "sine": [(-0.46638664033989147, 1800)],
        },
        "rotated_sine_weights_q5": {
            "cosine": [(0.46638664033989147, 1800)],
            "sine": [(-0.8845809752150838, 1800)],
        },
        "rotated_minus_sine_weights_q5": {
            "cosine": [(-0.46638664033989147, 1800)],
            "sine": [(0.8845809752150838, 1800)],
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
            {'intermediate_frequency': -131052000, 'lo_frequency': 3200000000, 'correction': (1, 0, 0, 1)},
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
            {'intermediate_frequency': -207885000, 'lo_frequency': 3200000000, 'correction': (1, 0, 0, 1)},
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
            {'intermediate_frequency': -364117000, 'lo_frequency': 3960000000, 'correction': (1, 0, 0, 1)},
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
            {'intermediate_frequency': -128925000, 'lo_frequency': 4600000000, 'correction': (1, 0, 0, 1)},
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
                },
                "6": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                },
                "7": {
                    "offset": 0.0150146484375,
                    "delay": 0,
                    "shareable": False,
                },
                "8": {
                    "offset": -0.0006103515625,
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
                    "offset": 0.008000000000000007,
                    "delay": 0,
                    "shareable": False,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "6": {
                    "offset": 0.0018,
                    "delay": 0,
                    "shareable": False,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "7": {
                    "offset": -0.032,
                    "delay": 0,
                    "shareable": False,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "8": {
                    "offset": 0.0018,
                    "delay": 0,
                    "shareable": False,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "9": {
                    "offset": 0.0095,
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
            "intermediate_frequency": 131052000.0,
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
            "intermediate_frequency": 99223000.0,
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
            "intermediate_frequency": 207885000.0,
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
            "intermediate_frequency": 364117000.0,
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
            "intermediate_frequency": 364117000.0,
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
            "intermediate_frequency": 128925000.0,
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
            "samples": [0.0, 0.00039553854454216306, 0.000858444131688, 0.0013890811420758993, 0.001984398020286004, 0.0026373712373101363, 0.0033366677908786098, 0.004066605122803545, 0.004807467784423178, 0.0055362091000068754, 0.006227526063316317, 0.006855251256502205, 0.00739396259848147, 0.007820676644443511, 0.008116469867043332] + [0.008267869125045842] * 2 + [0.008116469867043332, 0.007820676644443511, 0.00739396259848147, 0.006855251256502205, 0.006227526063316317, 0.0055362091000068754, 0.004807467784423178, 0.004066605122803545, 0.0033366677908786098, 0.0026373712373101363, 0.001984398020286004, 0.0013890811420758993, 0.000858444131688, 0.00039553854454216306, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q1": {
            "samples": [-0.0002604878496619217, -0.0003080431415814431, -0.00035692685729150653, -0.00040492215474113944, -0.0004493550035727267, -0.00048722033350951527, -0.0005153689193258006, -0.0005307453595247848, -0.0005306587792216822, -0.000513060294144279, -0.0004767962668112972, -0.0004218051976791304, -0.00034922945218947857, -0.00026142094538126524, -0.00016183160218758203, -5.4793359699649524e-05, 5.4793359699649524e-05, 0.00016183160218758203, 0.00026142094538126524, 0.00034922945218947857, 0.0004218051976791304, 0.0004767962668112972, 0.000513060294144279, 0.0005306587792216822, 0.0005307453595247848, 0.0005153689193258006, 0.00048722033350951527, 0.0004493550035727267, 0.00040492215474113944, 0.00035692685729150653, 0.0003080431415814431, 0.0002604878496619217],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q1": {
            "samples": [0.0, 0.0007905412930152419, 0.001715725415917432, 0.0027762806363937414, 0.003966107977238008, 0.0052711698944984, 0.006668815735307714, 0.008127701626865933, 0.00960842337837419, 0.011064918857372331, 0.012446616326807602, 0.013701216397336295, 0.014777909343514813, 0.015630759409070532, 0.01622194517310239] + [0.01652453860384222] * 2 + [0.01622194517310239, 0.015630759409070532, 0.014777909343514813, 0.013701216397336295, 0.012446616326807602, 0.011064918857372331, 0.00960842337837419, 0.008127701626865933, 0.006668815735307714, 0.0052711698944984, 0.003966107977238008, 0.0027762806363937414, 0.001715725415917432, 0.0007905412930152419, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q1": {
            "samples": [-0.0005206228427746682, -0.0006156690082685806, -0.0007133702218621998, -0.0008092958023853374, -0.0008981013113612889, -0.0009737806789013761, -0.0010300397204911513, -0.0010607717719804618, -0.001060598728655838, -0.0010254255973891917, -0.0009529466659340054, -0.0008430390185102795, -0.000697985838554467, -0.0005224877702429396, -0.0003234439874682353, -0.0001095124963756669, 0.0001095124963756669, 0.0003234439874682353, 0.0005224877702429396, 0.000697985838554467, 0.0008430390185102795, 0.0009529466659340054, 0.0010254255973891917, 0.001060598728655838, 0.0010607717719804618, 0.0010300397204911513, 0.0009737806789013761, 0.0008981013113612889, 0.0008092958023853374, 0.0007133702218621998, 0.0006156690082685806, 0.0005206228427746682],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q1": {
            "samples": [0.0, -0.00039553854454216306, -0.000858444131688, -0.0013890811420758993, -0.001984398020286004, -0.0026373712373101363, -0.0033366677908786098, -0.004066605122803545, -0.004807467784423178, -0.0055362091000068754, -0.006227526063316317, -0.006855251256502205, -0.00739396259848147, -0.007820676644443511, -0.008116469867043332] + [-0.008267869125045842] * 2 + [-0.008116469867043332, -0.007820676644443511, -0.00739396259848147, -0.006855251256502205, -0.006227526063316317, -0.0055362091000068754, -0.004807467784423178, -0.004066605122803545, -0.0033366677908786098, -0.0026373712373101363, -0.001984398020286004, -0.0013890811420758993, -0.000858444131688, -0.00039553854454216306, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q1": {
            "samples": [0.0002604878496619217, 0.0003080431415814431, 0.00035692685729150653, 0.00040492215474113944, 0.0004493550035727267, 0.00048722033350951527, 0.0005153689193258006, 0.0005307453595247848, 0.0005306587792216822, 0.000513060294144279, 0.0004767962668112972, 0.0004218051976791304, 0.00034922945218947857, 0.00026142094538126524, 0.00016183160218758203, 5.4793359699649524e-05, -5.4793359699649524e-05, -0.00016183160218758203, -0.00026142094538126524, -0.00034922945218947857, -0.0004218051976791304, -0.0004767962668112972, -0.000513060294144279, -0.0005306587792216822, -0.0005307453595247848, -0.0005153689193258006, -0.00048722033350951527, -0.0004493550035727267, -0.00040492215474113944, -0.00035692685729150653, -0.0003080431415814431, -0.0002604878496619217],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q1": {
            "samples": [0.0002603114213873341, 0.0003078345041342903, 0.0003566851109310999, 0.0004046479011926687, 0.00044905065568064443, 0.00048689033945068807, 0.0005150198602455756, 0.0005303858859902309, 0.000530299364327919, 0.0005127127986945958, 0.0004764733329670027, 0.00042151950925513977, 0.0003489929192772335, 0.0002612438851214698, 0.00016172199373411765, 5.475624818783345e-05, -5.475624818783345e-05, -0.00016172199373411765, -0.0002612438851214698, -0.0003489929192772335, -0.00042151950925513977, -0.0004764733329670027, -0.0005127127986945958, -0.000530299364327919, -0.0005303858859902309, -0.0005150198602455756, -0.00048689033945068807, -0.00044905065568064443, -0.0004046479011926687, -0.0003566851109310999, -0.0003078345041342903, -0.0002603114213873341],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q1": {
            "samples": [0.0, 0.00039527064650762096, 0.000857862707958716, 0.0013881403181968707, 0.001983053988619004, 0.0026355849472492, 0.003334407867653857, 0.004063850813432967, 0.004804211689187095, 0.0055324594286861655, 0.006223308163403801, 0.006850608198668147, 0.007388954671757406, 0.007815379704535266, 0.008110972586551196] + [0.00826226930192111] * 2 + [0.008110972586551196, 0.007815379704535266, 0.007388954671757406, 0.006850608198668147, 0.006223308163403801, 0.0055324594286861655, 0.004804211689187095, 0.004063850813432967, 0.003334407867653857, 0.0026355849472492, 0.001983053988619004, 0.0013881403181968707, 0.000857862707958716, 0.00039527064650762096, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q1": {
            "samples": [0.0005206228427746682, 0.0006156690082685806, 0.0007133702218621998, 0.0008092958023853374, 0.0008981013113612889, 0.0009737806789013761, 0.0010300397204911513, 0.0010607717719804618, 0.001060598728655838, 0.0010254255973891917, 0.0009529466659340054, 0.0008430390185102795, 0.000697985838554467, 0.0005224877702429396, 0.0003234439874682353, 0.0001095124963756669, -0.0001095124963756669, -0.0003234439874682353, -0.0005224877702429396, -0.000697985838554467, -0.0008430390185102795, -0.0009529466659340054, -0.0010254255973891917, -0.001060598728655838, -0.0010607717719804618, -0.0010300397204911513, -0.0009737806789013761, -0.0008981013113612889, -0.0008092958023853374, -0.0007133702218621998, -0.0006156690082685806, -0.0005206228427746682],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q1": {
            "samples": [0.0, 0.0007905412930152419, 0.001715725415917432, 0.0027762806363937414, 0.003966107977238008, 0.0052711698944984, 0.006668815735307714, 0.008127701626865933, 0.00960842337837419, 0.011064918857372331, 0.012446616326807602, 0.013701216397336295, 0.014777909343514813, 0.015630759409070532, 0.01622194517310239] + [0.01652453860384222] * 2 + [0.01622194517310239, 0.015630759409070532, 0.014777909343514813, 0.013701216397336295, 0.012446616326807602, 0.011064918857372331, 0.00960842337837419, 0.008127701626865933, 0.006668815735307714, 0.0052711698944984, 0.003966107977238008, 0.0027762806363937414, 0.001715725415917432, 0.0007905412930152419, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q1": {
            "samples": [-0.0002603114213873341, -0.0003078345041342903, -0.0003566851109310999, -0.0004046479011926687, -0.00044905065568064443, -0.00048689033945068807, -0.0005150198602455756, -0.0005303858859902309, -0.000530299364327919, -0.0005127127986945958, -0.0004764733329670027, -0.00042151950925513977, -0.0003489929192772335, -0.0002612438851214698, -0.00016172199373411765, -5.475624818783345e-05, 5.475624818783345e-05, 0.00016172199373411765, 0.0002612438851214698, 0.0003489929192772335, 0.00042151950925513977, 0.0004764733329670027, 0.0005127127986945958, 0.000530299364327919, 0.0005303858859902309, 0.0005150198602455756, 0.00048689033945068807, 0.00044905065568064443, 0.0004046479011926687, 0.0003566851109310999, 0.0003078345041342903, 0.0002603114213873341],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q1": {
            "samples": [0.0, -0.00039527064650762096, -0.000857862707958716, -0.0013881403181968707, -0.001983053988619004, -0.0026355849472492, -0.003334407867653857, -0.004063850813432967, -0.004804211689187095, -0.0055324594286861655, -0.006223308163403801, -0.006850608198668147, -0.007388954671757406, -0.007815379704535266, -0.008110972586551196] + [-0.00826226930192111] * 2 + [-0.008110972586551196, -0.007815379704535266, -0.007388954671757406, -0.006850608198668147, -0.006223308163403801, -0.0055324594286861655, -0.004804211689187095, -0.004063850813432967, -0.003334407867653857, -0.0026355849472492, -0.001983053988619004, -0.0013881403181968707, -0.000857862707958716, -0.00039527064650762096, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q1": {
            "sample": 0.0868910316,
            "type": "constant",
        },
        "x90_I_wf_q2": {
            "samples": [0.0, 0.0011767776395012744, 0.002553980826573635, 0.004132693640110123, 0.005903837313367679, 0.007846515951366519, 0.00992701242629847, 0.012098669126508935, 0.014302830076599219, 0.016470928475586538, 0.018527684651326967, 0.020395247196837694, 0.021997982177118097, 0.023267510911240546, 0.02414753349077044] + [0.024597965601402445] * 2 + [0.02414753349077044, 0.023267510911240546, 0.021997982177118097, 0.020395247196837694, 0.018527684651326967, 0.016470928475586538, 0.014302830076599219, 0.012098669126508935, 0.00992701242629847, 0.007846515951366519, 0.005903837313367679, 0.004132693640110123, 0.002553980826573635, 0.0011767776395012744, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q2": {
            "samples": [0.000450549977112142, 0.0005328034707538214, 0.0006173546581620267, 0.0007003692025850697, 0.0007772219964872851, 0.0008427153527359765, 0.0008914022481582638, 0.0009179979407739079, 0.0009178481880939582, 0.000887409159712699, 0.0008246854791031253, 0.0007295707742482685, 0.0006040409251144289, 0.00045216389597837445, 0.00027991027127087867, 9.477273888442422e-05, -9.477273888442422e-05, -0.00027991027127087867, -0.00045216389597837445, -0.0006040409251144289, -0.0007295707742482685, -0.0008246854791031253, -0.000887409159712699, -0.0009178481880939582, -0.0009179979407739079, -0.0008914022481582638, -0.0008427153527359765, -0.0007772219964872851, -0.0007003692025850697, -0.0006173546581620267, -0.0005328034707538214, -0.000450549977112142],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q2": {
            "samples": [0.0, 0.002331815702908935, 0.0050607798758452675, 0.008189040649518762, 0.011698608209928985, 0.015548076794079909, 0.01967063503044225, 0.023973829639938972, 0.028341432271594552, 0.03263757601405464, 0.03671309222600359, 0.040413716306209685, 0.04358957763223146, 0.04610518205752919, 0.047848969839502944] + [0.04874151285987445] * 2 + [0.047848969839502944, 0.04610518205752919, 0.04358957763223146, 0.040413716306209685, 0.03671309222600359, 0.03263757601405464, 0.028341432271594552, 0.023973829639938972, 0.01967063503044225, 0.015548076794079909, 0.011698608209928985, 0.008189040649518762, 0.0050607798758452675, 0.002331815702908935, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q2": {
            "samples": [0.0008927765758878672, 0.0010557640270889915, 0.0012233044186464024, 0.0013877999118965302, 0.0015400857351634976, 0.0016698625353087063, 0.0017663368933018518, 0.001819036954544672, 0.0018187402156885463, 0.00175842448400045, 0.001634135868649435, 0.0014456635906988616, 0.0011969229080341824, 0.0008959745983767177, 0.0005546495310971008, 0.0001877946634268533, -0.0001877946634268533, -0.0005546495310971008, -0.0008959745983767177, -0.0011969229080341824, -0.0014456635906988616, -0.001634135868649435, -0.00175842448400045, -0.0018187402156885463, -0.001819036954544672, -0.0017663368933018518, -0.0016698625353087063, -0.0015400857351634976, -0.0013877999118965302, -0.0012233044186464024, -0.0010557640270889915, -0.0008927765758878672],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q2": {
            "samples": [0.0, -0.0011767776395012744, -0.002553980826573635, -0.004132693640110123, -0.005903837313367679, -0.007846515951366519, -0.00992701242629847, -0.012098669126508935, -0.014302830076599219, -0.016470928475586538, -0.018527684651326967, -0.020395247196837694, -0.021997982177118097, -0.023267510911240546, -0.02414753349077044] + [-0.024597965601402445] * 2 + [-0.02414753349077044, -0.023267510911240546, -0.021997982177118097, -0.020395247196837694, -0.018527684651326967, -0.016470928475586538, -0.014302830076599219, -0.012098669126508935, -0.00992701242629847, -0.007846515951366519, -0.005903837313367679, -0.004132693640110123, -0.002553980826573635, -0.0011767776395012744, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q2": {
            "samples": [-0.000450549977112142, -0.0005328034707538214, -0.0006173546581620267, -0.0007003692025850697, -0.0007772219964872851, -0.0008427153527359765, -0.0008914022481582638, -0.0009179979407739079, -0.0009178481880939582, -0.000887409159712699, -0.0008246854791031253, -0.0007295707742482685, -0.0006040409251144289, -0.00045216389597837445, -0.00027991027127087867, -9.477273888442422e-05, 9.477273888442422e-05, 0.00027991027127087867, 0.00045216389597837445, 0.0006040409251144289, 0.0007295707742482685, 0.0008246854791031253, 0.000887409159712699, 0.0009178481880939582, 0.0009179979407739079, 0.0008914022481582638, 0.0008427153527359765, 0.0007772219964872851, 0.0007003692025850697, 0.0006173546581620267, 0.0005328034707538214, 0.000450549977112142],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q2": {
            "samples": [-0.0004463882879439336, -0.0005278820135444957, -0.0006116522093232012, -0.0006938999559482651, -0.0007700428675817488, -0.0008349312676543531, -0.0008831684466509259, -0.000909518477272336, -0.0009093701078442732, -0.000879212242000225, -0.0008170679343247175, -0.0007228317953494308, -0.0005984614540170912, -0.0004479872991883588, -0.0002773247655485504, -9.389733171342665e-05, 9.389733171342665e-05, 0.0002773247655485504, 0.0004479872991883588, 0.0005984614540170912, 0.0007228317953494308, 0.0008170679343247175, 0.000879212242000225, 0.0009093701078442732, 0.000909518477272336, 0.0008831684466509259, 0.0008349312676543531, 0.0007700428675817488, 0.0006938999559482651, 0.0006116522093232012, 0.0005278820135444957, 0.0004463882879439336],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q2": {
            "samples": [0.0, 0.0011659078514544676, 0.0025303899379226337, 0.004094520324759381, 0.0058493041049644924, 0.007774038397039954, 0.009835317515221126, 0.011986914819969486, 0.014170716135797276, 0.01631878800702732, 0.018356546113001793, 0.020206858153104842, 0.02179478881611573, 0.023052591028764596, 0.023924484919751472] + [0.024370756429937225] * 2 + [0.023924484919751472, 0.023052591028764596, 0.02179478881611573, 0.020206858153104842, 0.018356546113001793, 0.01631878800702732, 0.014170716135797276, 0.011986914819969486, 0.009835317515221126, 0.007774038397039954, 0.0058493041049644924, 0.004094520324759381, 0.0025303899379226337, 0.0011659078514544676, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q2": {
            "samples": [-0.0008927765758878672, -0.0010557640270889915, -0.0012233044186464024, -0.0013877999118965302, -0.0015400857351634976, -0.0016698625353087063, -0.0017663368933018518, -0.001819036954544672, -0.0018187402156885463, -0.00175842448400045, -0.001634135868649435, -0.0014456635906988616, -0.0011969229080341824, -0.0008959745983767177, -0.0005546495310971008, -0.0001877946634268533, 0.0001877946634268533, 0.0005546495310971008, 0.0008959745983767177, 0.0011969229080341824, 0.0014456635906988616, 0.001634135868649435, 0.00175842448400045, 0.0018187402156885463, 0.001819036954544672, 0.0017663368933018518, 0.0016698625353087063, 0.0015400857351634976, 0.0013877999118965302, 0.0012233044186464024, 0.0010557640270889915, 0.0008927765758878672],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q2": {
            "samples": [0.0, 0.002331815702908935, 0.0050607798758452675, 0.008189040649518762, 0.011698608209928985, 0.015548076794079909, 0.01967063503044225, 0.023973829639938972, 0.028341432271594552, 0.03263757601405464, 0.03671309222600359, 0.040413716306209685, 0.04358957763223146, 0.04610518205752919, 0.047848969839502944] + [0.04874151285987445] * 2 + [0.047848969839502944, 0.04610518205752919, 0.04358957763223146, 0.040413716306209685, 0.03671309222600359, 0.03263757601405464, 0.028341432271594552, 0.023973829639938972, 0.01967063503044225, 0.015548076794079909, 0.011698608209928985, 0.008189040649518762, 0.0050607798758452675, 0.002331815702908935, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q2": {
            "samples": [0.0004463882879439336, 0.0005278820135444957, 0.0006116522093232012, 0.0006938999559482651, 0.0007700428675817488, 0.0008349312676543531, 0.0008831684466509259, 0.000909518477272336, 0.0009093701078442732, 0.000879212242000225, 0.0008170679343247175, 0.0007228317953494308, 0.0005984614540170912, 0.0004479872991883588, 0.0002773247655485504, 9.389733171342665e-05, -9.389733171342665e-05, -0.0002773247655485504, -0.0004479872991883588, -0.0005984614540170912, -0.0007228317953494308, -0.0008170679343247175, -0.000879212242000225, -0.0009093701078442732, -0.000909518477272336, -0.0008831684466509259, -0.0008349312676543531, -0.0007700428675817488, -0.0006938999559482651, -0.0006116522093232012, -0.0005278820135444957, -0.0004463882879439336],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q2": {
            "samples": [0.0, -0.0011659078514544676, -0.0025303899379226337, -0.004094520324759381, -0.0058493041049644924, -0.007774038397039954, -0.009835317515221126, -0.011986914819969486, -0.014170716135797276, -0.01631878800702732, -0.018356546113001793, -0.020206858153104842, -0.02179478881611573, -0.023052591028764596, -0.023924484919751472] + [-0.024370756429937225] * 2 + [-0.023924484919751472, -0.023052591028764596, -0.02179478881611573, -0.020206858153104842, -0.018356546113001793, -0.01631878800702732, -0.014170716135797276, -0.011986914819969486, -0.009835317515221126, -0.007774038397039954, -0.0058493041049644924, -0.004094520324759381, -0.0025303899379226337, -0.0011659078514544676, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q2": {
            "sample": 0.1309075425,
            "type": "constant",
        },
        "x90_I_wf_q3": {
            "samples": [0.0, 0.0003914564519015011, 0.0008495846955578522, 0.0013747453510750155, 0.0019639183561255113, 0.002610152666915237, 0.003302232241621976, 0.004024636371405401, 0.004757853077756023, 0.005479073534494639, 0.006163255871034504, 0.006784502726200445, 0.007317654383453965, 0.007739964594971236, 0.008032705130661542] + [0.008182541896701078] * 2 + [0.008032705130661542, 0.007739964594971236, 0.007317654383453965, 0.006784502726200445, 0.006163255871034504, 0.005479073534494639, 0.004757853077756023, 0.004024636371405401, 0.003302232241621976, 0.002610152666915237, 0.0019639183561255113, 0.0013747453510750155, 0.0008495846955578522, 0.0003914564519015011, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q3": {
            "samples": [0.00028111199180189496, 0.00033243247699752917, 0.0003851865640221966, 0.00043698189221390147, 0.0004849327146906164, 0.0005257960345444275, 0.0005561732864411759, 0.0005727671572753405, 0.0005726737219712079, 0.0005536818757134056, 0.0005145466416993674, 0.0004552016511551929, 0.0003768797163794159, 0.0002821189654344346, 0.00017464462963046707, 5.9131627454705774e-05, -5.9131627454705774e-05, -0.00017464462963046707, -0.0002821189654344346, -0.0003768797163794159, -0.0004552016511551929, -0.0005145466416993674, -0.0005536818757134056, -0.0005726737219712079, -0.0005727671572753405, -0.0005561732864411759, -0.0005257960345444275, -0.0004849327146906164, -0.00043698189221390147, -0.0003851865640221966, -0.00033243247699752917, -0.00028111199180189496],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q3": {
            "samples": [0.0, 0.0007852873575538541, 0.0017043227090830916, 0.002757829482209652, 0.0039397492335146705, 0.005236137712528403, 0.0066244948025661, 0.00807368494212819, 0.009544565820569556, 0.010991381434247478, 0.012363896145747502, 0.013610158147337039, 0.014679695394881048, 0.015526877421028502, 0.016114134165947307] + [0.016414716561501255] * 2 + [0.016114134165947307, 0.015526877421028502, 0.014679695394881048, 0.013610158147337039, 0.012363896145747502, 0.010991381434247478, 0.009544565820569556, 0.00807368494212819, 0.0066244948025661, 0.005236137712528403, 0.0039397492335146705, 0.002757829482209652, 0.0017043227090830916, 0.0007852873575538541, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q3": {
            "samples": [0.0005639291219917285, 0.0006668813865716002, 0.0007727095505947881, 0.0008766143814175357, 0.0009728068812278295, 0.0010547813851937305, 0.0011157201480008583, 0.0011490085429568058, 0.0011488211055988877, 0.0011107222144184931, 0.0010322143641663057, 0.0009131644147220707, 0.0007560454685409223, 0.0005659491772473826, 0.0003503485995627169, 0.00011862192907079469, -0.00011862192907079469, -0.0003503485995627169, -0.0005659491772473826, -0.0007560454685409223, -0.0009131644147220707, -0.0010322143641663057, -0.0011107222144184931, -0.0011488211055988877, -0.0011490085429568058, -0.0011157201480008583, -0.0010547813851937305, -0.0009728068812278295, -0.0008766143814175357, -0.0007727095505947881, -0.0006668813865716002, -0.0005639291219917285],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q3": {
            "samples": [0.0, -0.0003914564519015011, -0.0008495846955578522, -0.0013747453510750155, -0.0019639183561255113, -0.002610152666915237, -0.003302232241621976, -0.004024636371405401, -0.004757853077756023, -0.005479073534494639, -0.006163255871034504, -0.006784502726200445, -0.007317654383453965, -0.007739964594971236, -0.008032705130661542] + [-0.008182541896701078] * 2 + [-0.008032705130661542, -0.007739964594971236, -0.007317654383453965, -0.006784502726200445, -0.006163255871034504, -0.005479073534494639, -0.004757853077756023, -0.004024636371405401, -0.003302232241621976, -0.002610152666915237, -0.0019639183561255113, -0.0013747453510750155, -0.0008495846955578522, -0.0003914564519015011, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q3": {
            "samples": [-0.00028111199180189496, -0.00033243247699752917, -0.0003851865640221966, -0.00043698189221390147, -0.0004849327146906164, -0.0005257960345444275, -0.0005561732864411759, -0.0005727671572753405, -0.0005726737219712079, -0.0005536818757134056, -0.0005145466416993674, -0.0004552016511551929, -0.0003768797163794159, -0.0002821189654344346, -0.00017464462963046707, -5.9131627454705774e-05, 5.9131627454705774e-05, 0.00017464462963046707, 0.0002821189654344346, 0.0003768797163794159, 0.0004552016511551929, 0.0005145466416993674, 0.0005536818757134056, 0.0005726737219712079, 0.0005727671572753405, 0.0005561732864411759, 0.0005257960345444275, 0.0004849327146906164, 0.00043698189221390147, 0.0003851865640221966, 0.00033243247699752917, 0.00028111199180189496],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q3": {
            "samples": [-0.00028196456099586424, -0.0003334406932858001, -0.00038635477529739404, -0.00043830719070876787, -0.00048640344061391476, -0.0005273906925968653, -0.0005578600740004291, -0.0005745042714784029, -0.0005744105527994438, -0.0005553611072092466, -0.0005161071820831528, -0.0004565822073610353, -0.00037802273427046116, -0.0002829745886236913, -0.00017517429978135846, -5.9310964535397346e-05, 5.9310964535397346e-05, 0.00017517429978135846, 0.0002829745886236913, 0.00037802273427046116, 0.0004565822073610353, 0.0005161071820831528, 0.0005553611072092466, 0.0005744105527994438, 0.0005745042714784029, 0.0005578600740004291, 0.0005273906925968653, 0.00048640344061391476, 0.00043830719070876787, 0.00038635477529739404, 0.0003334406932858001, 0.00028196456099586424],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q3": {
            "samples": [0.0, 0.00039264367877692706, 0.0008521613545415458, 0.001378914741104826, 0.0019698746167573352, 0.0026180688562642013, 0.00331224740128305, 0.004036842471064095, 0.004772282910284778, 0.005495690717123739, 0.006181948072873751, 0.0068050790736685195, 0.007339847697440524, 0.007763438710514251, 0.008057067082973653] + [0.008207358280750627] * 2 + [0.008057067082973653, 0.007763438710514251, 0.007339847697440524, 0.0068050790736685195, 0.006181948072873751, 0.005495690717123739, 0.004772282910284778, 0.004036842471064095, 0.00331224740128305, 0.0026180688562642013, 0.0019698746167573352, 0.001378914741104826, 0.0008521613545415458, 0.00039264367877692706, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q3": {
            "samples": [-0.0005639291219917285, -0.0006668813865716002, -0.0007727095505947881, -0.0008766143814175357, -0.0009728068812278295, -0.0010547813851937305, -0.0011157201480008583, -0.0011490085429568058, -0.0011488211055988877, -0.0011107222144184931, -0.0010322143641663057, -0.0009131644147220707, -0.0007560454685409223, -0.0005659491772473826, -0.0003503485995627169, -0.00011862192907079469, 0.00011862192907079469, 0.0003503485995627169, 0.0005659491772473826, 0.0007560454685409223, 0.0009131644147220707, 0.0010322143641663057, 0.0011107222144184931, 0.0011488211055988877, 0.0011490085429568058, 0.0011157201480008583, 0.0010547813851937305, 0.0009728068812278295, 0.0008766143814175357, 0.0007727095505947881, 0.0006668813865716002, 0.0005639291219917285],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q3": {
            "samples": [0.0, 0.0007852873575538541, 0.0017043227090830916, 0.002757829482209652, 0.0039397492335146705, 0.005236137712528403, 0.0066244948025661, 0.00807368494212819, 0.009544565820569556, 0.010991381434247478, 0.012363896145747502, 0.013610158147337039, 0.014679695394881048, 0.015526877421028502, 0.016114134165947307] + [0.016414716561501255] * 2 + [0.016114134165947307, 0.015526877421028502, 0.014679695394881048, 0.013610158147337039, 0.012363896145747502, 0.010991381434247478, 0.009544565820569556, 0.00807368494212819, 0.0066244948025661, 0.005236137712528403, 0.0039397492335146705, 0.002757829482209652, 0.0017043227090830916, 0.0007852873575538541, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q3": {
            "samples": [0.00028196456099586424, 0.0003334406932858001, 0.00038635477529739404, 0.00043830719070876787, 0.00048640344061391476, 0.0005273906925968653, 0.0005578600740004291, 0.0005745042714784029, 0.0005744105527994438, 0.0005553611072092466, 0.0005161071820831528, 0.0004565822073610353, 0.00037802273427046116, 0.0002829745886236913, 0.00017517429978135846, 5.9310964535397346e-05, -5.9310964535397346e-05, -0.00017517429978135846, -0.0002829745886236913, -0.00037802273427046116, -0.0004565822073610353, -0.0005161071820831528, -0.0005553611072092466, -0.0005744105527994438, -0.0005745042714784029, -0.0005578600740004291, -0.0005273906925968653, -0.00048640344061391476, -0.00043830719070876787, -0.00038635477529739404, -0.0003334406932858001, -0.00028196456099586424],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q3": {
            "samples": [0.0, -0.00039264367877692706, -0.0008521613545415458, -0.001378914741104826, -0.0019698746167573352, -0.0026180688562642013, -0.00331224740128305, -0.004036842471064095, -0.004772282910284778, -0.005495690717123739, -0.006181948072873751, -0.0068050790736685195, -0.007339847697440524, -0.007763438710514251, -0.008057067082973653] + [-0.008207358280750627] * 2 + [-0.008057067082973653, -0.007763438710514251, -0.007339847697440524, -0.0068050790736685195, -0.006181948072873751, -0.005495690717123739, -0.004772282910284778, -0.004036842471064095, -0.00331224740128305, -0.0026180688562642013, -0.0019698746167573352, -0.001378914741104826, -0.0008521613545415458, -0.00039264367877692706, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q3": {
            "sample": 0.102461516,
            "type": "constant",
        },
        "x90_I_wf_q4": {
            "samples": [0.0, 0.0015929601412333159, 0.003457228894942401, 0.005594273738421689, 0.007991805082654709, 0.010621536931459287, 0.013437827662431684, 0.016377518601276883, 0.019361209334765685, 0.022296083533532976, 0.025080237904088906, 0.027608287891102277, 0.02977785064862464, 0.03149636449841577, 0.03268761834750365] + [0.03329735154983784] * 2 + [0.03268761834750365, 0.03149636449841577, 0.02977785064862464, 0.027608287891102277, 0.025080237904088906, 0.022296083533532976, 0.019361209334765685, 0.016377518601276883, 0.013437827662431684, 0.010621536931459287, 0.007991805082654709, 0.005594273738421689, 0.003457228894942401, 0.0015929601412333159, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q4": {
            "samples": [0.0015975270321798617, 0.0018891754313786727, 0.0021889708244520003, 0.002483317701639608, 0.0027558166961890586, 0.002988038230648106, 0.003160668650137971, 0.003254969704519032, 0.0032544387224604046, 0.00314651025027618, 0.002924109228365419, 0.0025868584906395516, 0.0021417639672258824, 0.0016032495472115505, 0.000992485290546863, 0.00033603821989298905, -0.00033603821989298905, -0.000992485290546863, -0.0016032495472115505, -0.0021417639672258824, -0.0025868584906395516, -0.002924109228365419, -0.00314651025027618, -0.0032544387224604046, -0.003254969704519032, -0.003160668650137971, -0.002988038230648106, -0.0027558166961890586, -0.002483317701639608, -0.0021889708244520003, -0.0018891754313786727, -0.0015975270321798617],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q4": {
            "samples": [0.0, 0.0031695503085252073, 0.006878929752833022, 0.011131058207056467, 0.015901482786499603, 0.02113392217840044, 0.026737562171764734, 0.0325867344649093, 0.03852345418568736, 0.04436304249766073, 0.049902740017866834, 0.05493286061467074, 0.059249690728289166, 0.06266905820762429, 0.06503932404615623] + [0.06625252455855582] * 2 + [0.06503932404615623, 0.06266905820762429, 0.059249690728289166, 0.05493286061467074, 0.049902740017866834, 0.04436304249766073, 0.03852345418568736, 0.0325867344649093, 0.026737562171764734, 0.02113392217840044, 0.015901482786499603, 0.011131058207056467, 0.006878929752833022, 0.0031695503085252073, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q4": {
            "samples": [0.0031786371589955635, 0.003758936847439608, 0.004355446801464143, 0.004941115715113858, 0.00548331338214294, 0.005945370038263041, 0.006288856849509498, 0.006476489878278399, 0.006475433370771288, 0.006260685547862604, 0.005818168996840925, 0.0051471332614572525, 0.004261518205881264, 0.003190023381924021, 0.0019747713564408605, 0.0006686231600958084, -0.0006686231600958084, -0.0019747713564408605, -0.003190023381924021, -0.004261518205881264, -0.0051471332614572525, -0.005818168996840925, -0.006260685547862604, -0.006475433370771288, -0.006476489878278399, -0.006288856849509498, -0.005945370038263041, -0.00548331338214294, -0.004941115715113858, -0.004355446801464143, -0.003758936847439608, -0.0031786371589955635],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q4": {
            "samples": [0.0, -0.0015929601412333159, -0.003457228894942401, -0.005594273738421689, -0.007991805082654709, -0.010621536931459287, -0.013437827662431684, -0.016377518601276883, -0.019361209334765685, -0.022296083533532976, -0.025080237904088906, -0.027608287891102277, -0.02977785064862464, -0.03149636449841577, -0.03268761834750365] + [-0.03329735154983784] * 2 + [-0.03268761834750365, -0.03149636449841577, -0.02977785064862464, -0.027608287891102277, -0.025080237904088906, -0.022296083533532976, -0.019361209334765685, -0.016377518601276883, -0.013437827662431684, -0.010621536931459287, -0.007991805082654709, -0.005594273738421689, -0.003457228894942401, -0.0015929601412333159, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q4": {
            "samples": [-0.0015975270321798617, -0.0018891754313786727, -0.0021889708244520003, -0.002483317701639608, -0.0027558166961890586, -0.002988038230648106, -0.003160668650137971, -0.003254969704519032, -0.0032544387224604046, -0.00314651025027618, -0.002924109228365419, -0.0025868584906395516, -0.0021417639672258824, -0.0016032495472115505, -0.000992485290546863, -0.00033603821989298905, 0.00033603821989298905, 0.000992485290546863, 0.0016032495472115505, 0.0021417639672258824, 0.0025868584906395516, 0.002924109228365419, 0.00314651025027618, 0.0032544387224604046, 0.003254969704519032, 0.003160668650137971, 0.002988038230648106, 0.0027558166961890586, 0.002483317701639608, 0.0021889708244520003, 0.0018891754313786727, 0.0015975270321798617],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q4": {
            "samples": [-0.0015893185794977817, -0.001879468423719804, -0.0021777234007320716, -0.002470557857556929, -0.00274165669107147, -0.0029726850191315207, -0.003144428424754749, -0.0032382449391391995, -0.003237716685385644, -0.003130342773931302, -0.0029090844984204626, -0.0025735666307286262, -0.002130759102940632, -0.0015950116909620104, -0.0009873856782204302, -0.0003343115800479042, 0.0003343115800479042, 0.0009873856782204302, 0.0015950116909620104, 0.002130759102940632, 0.0025735666307286262, 0.0029090844984204626, 0.003130342773931302, 0.003237716685385644, 0.0032382449391391995, 0.003144428424754749, 0.0029726850191315207, 0.00274165669107147, 0.002470557857556929, 0.0021777234007320716, 0.001879468423719804, 0.0015893185794977817],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q4": {
            "samples": [0.0, 0.0015847751542626036, 0.003439464876416511, 0.005565529103528233, 0.007950741393249802, 0.01056696108920022, 0.013368781085882367, 0.01629336723245465, 0.01926172709284368, 0.022181521248830365, 0.024951370008933417, 0.02746643030733537, 0.029624845364144583, 0.031334529103812146, 0.032519662023078114] + [0.03312626227927791] * 2 + [0.032519662023078114, 0.031334529103812146, 0.029624845364144583, 0.02746643030733537, 0.024951370008933417, 0.022181521248830365, 0.01926172709284368, 0.01629336723245465, 0.013368781085882367, 0.01056696108920022, 0.007950741393249802, 0.005565529103528233, 0.003439464876416511, 0.0015847751542626036, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q4": {
            "samples": [-0.0031786371589955635, -0.003758936847439608, -0.004355446801464143, -0.004941115715113858, -0.00548331338214294, -0.005945370038263041, -0.006288856849509498, -0.006476489878278399, -0.006475433370771288, -0.006260685547862604, -0.005818168996840925, -0.0051471332614572525, -0.004261518205881264, -0.003190023381924021, -0.0019747713564408605, -0.0006686231600958084, 0.0006686231600958084, 0.0019747713564408605, 0.003190023381924021, 0.004261518205881264, 0.0051471332614572525, 0.005818168996840925, 0.006260685547862604, 0.006475433370771288, 0.006476489878278399, 0.006288856849509498, 0.005945370038263041, 0.00548331338214294, 0.004941115715113858, 0.004355446801464143, 0.003758936847439608, 0.0031786371589955635],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q4": {
            "samples": [0.0, 0.0031695503085252073, 0.006878929752833022, 0.011131058207056467, 0.015901482786499603, 0.02113392217840044, 0.026737562171764734, 0.0325867344649093, 0.03852345418568736, 0.04436304249766073, 0.049902740017866834, 0.05493286061467074, 0.059249690728289166, 0.06266905820762429, 0.06503932404615623] + [0.06625252455855582] * 2 + [0.06503932404615623, 0.06266905820762429, 0.059249690728289166, 0.05493286061467074, 0.049902740017866834, 0.04436304249766073, 0.03852345418568736, 0.0325867344649093, 0.026737562171764734, 0.02113392217840044, 0.015901482786499603, 0.011131058207056467, 0.006878929752833022, 0.0031695503085252073, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q4": {
            "samples": [0.0015893185794977817, 0.001879468423719804, 0.0021777234007320716, 0.002470557857556929, 0.00274165669107147, 0.0029726850191315207, 0.003144428424754749, 0.0032382449391391995, 0.003237716685385644, 0.003130342773931302, 0.0029090844984204626, 0.0025735666307286262, 0.002130759102940632, 0.0015950116909620104, 0.0009873856782204302, 0.0003343115800479042, -0.0003343115800479042, -0.0009873856782204302, -0.0015950116909620104, -0.002130759102940632, -0.0025735666307286262, -0.0029090844984204626, -0.003130342773931302, -0.003237716685385644, -0.0032382449391391995, -0.003144428424754749, -0.0029726850191315207, -0.00274165669107147, -0.002470557857556929, -0.0021777234007320716, -0.001879468423719804, -0.0015893185794977817],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q4": {
            "samples": [0.0, -0.0015847751542626036, -0.003439464876416511, -0.005565529103528233, -0.007950741393249802, -0.01056696108920022, -0.013368781085882367, -0.01629336723245465, -0.01926172709284368, -0.022181521248830365, -0.024951370008933417, -0.02746643030733537, -0.029624845364144583, -0.031334529103812146, -0.032519662023078114] + [-0.03312626227927791] * 2 + [-0.032519662023078114, -0.031334529103812146, -0.029624845364144583, -0.02746643030733537, -0.024951370008933417, -0.022181521248830365, -0.01926172709284368, -0.01629336723245465, -0.013368781085882367, -0.01056696108920022, -0.007950741393249802, -0.005565529103528233, -0.003439464876416511, -0.0015847751542626036, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q4": {
            "sample": 0.21388562800000002,
            "type": "constant",
        },
        "x90_I_wf_q5": {
            "samples": [0.0, 0.002424713297309757, 0.00526239712873177, 0.008515285204713157, 0.01216467101205539, 0.016167499216669906, 0.020454296737662497, 0.024928927034363033, 0.029470531315151236, 0.033937829844148185, 0.03817571122567691, 0.04202376508534801, 0.04532615008001563, 0.047941974089255046, 0.049755232923288706] + [0.05068333411379704] * 2 + [0.049755232923288706, 0.047941974089255046, 0.04532615008001563, 0.04202376508534801, 0.03817571122567691, 0.033937829844148185, 0.029470531315151236, 0.024928927034363033, 0.020454296737662497, 0.016167499216669906, 0.01216467101205539, 0.008515285204713157, 0.00526239712873177, 0.002424713297309757, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q5": {
            "samples": [-0.00017884902826885524, -0.0002115001394814772, -0.00024506333662968507, -0.0002780165523803709, -0.00030852381729526104, -0.00033452187237945633, -0.00035384848291779427, -0.00036440583287247253, -0.0003643463874776212, -0.0003522633979670452, -0.0003273647853905404, -0.00028960832461696445, -0.0002397783552976338, -0.00017948968487876242, -0.00011111237945265272, -3.7620714941548775e-05, 3.7620714941548775e-05, 0.00011111237945265272, 0.00017948968487876242, 0.0002397783552976338, 0.00028960832461696445, 0.0003273647853905404, 0.0003522633979670452, 0.0003643463874776212, 0.00036440583287247253, 0.00035384848291779427, 0.00033452187237945633, 0.00030852381729526104, 0.0002780165523803709, 0.00024506333662968507, 0.0002115001394814772, 0.00017884902826885524],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q5": {
            "samples": [0.0, 0.00480381199779446, 0.010425796110496325, 0.016870377737618757, 0.02410049576655942, 0.03203084950189457, 0.04052379973494186, 0.0493888819402623, 0.05838665217457876, 0.06723720877239805, 0.07563324695489362, 0.08325696367214713, 0.08979960798243405, 0.09498204615920536, 0.09857445213631702] + [0.10041319473696919] * 2 + [0.09857445213631702, 0.09498204615920536, 0.08979960798243405, 0.08325696367214713, 0.07563324695489362, 0.06723720877239805, 0.05838665217457876, 0.0493888819402623, 0.04052379973494186, 0.03203084950189457, 0.02410049576655942, 0.016870377737618757, 0.010425796110496325, 0.00480381199779446, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q5": {
            "samples": [-0.00035433348295035535, -0.0004190214606830385, -0.00048551645179138503, -0.0005508029552987027, -0.0006112435712596262, -0.0006627505964701305, -0.0007010402382532548, -0.0007219563294189474, -0.0007218385569378391, -0.0006978998875518418, -0.0006485710642405842, -0.0005737684310964526, -0.0004750459121365747, -0.00035560274390279586, -0.0002201344720261808, -7.4533695180511e-05, 7.4533695180511e-05, 0.0002201344720261808, 0.00035560274390279586, 0.0004750459121365747, 0.0005737684310964526, 0.0006485710642405842, 0.0006978998875518418, 0.0007218385569378391, 0.0007219563294189474, 0.0007010402382532548, 0.0006627505964701305, 0.0006112435712596262, 0.0005508029552987027, 0.00048551645179138503, 0.0004190214606830385, 0.00035433348295035535],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q5": {
            "samples": [0.0, -0.002424713297309757, -0.00526239712873177, -0.008515285204713157, -0.01216467101205539, -0.016167499216669906, -0.020454296737662497, -0.024928927034363033, -0.029470531315151236, -0.033937829844148185, -0.03817571122567691, -0.04202376508534801, -0.04532615008001563, -0.047941974089255046, -0.049755232923288706] + [-0.05068333411379704] * 2 + [-0.049755232923288706, -0.047941974089255046, -0.04532615008001563, -0.04202376508534801, -0.03817571122567691, -0.033937829844148185, -0.029470531315151236, -0.024928927034363033, -0.020454296737662497, -0.016167499216669906, -0.01216467101205539, -0.008515285204713157, -0.00526239712873177, -0.002424713297309757, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q5": {
            "samples": [0.00017884902826885524, 0.0002115001394814772, 0.00024506333662968507, 0.0002780165523803709, 0.00030852381729526104, 0.00033452187237945633, 0.00035384848291779427, 0.00036440583287247253, 0.0003643463874776212, 0.0003522633979670452, 0.0003273647853905404, 0.00028960832461696445, 0.0002397783552976338, 0.00017948968487876242, 0.00011111237945265272, 3.7620714941548775e-05, -3.7620714941548775e-05, -0.00011111237945265272, -0.00017948968487876242, -0.0002397783552976338, -0.00028960832461696445, -0.0003273647853905404, -0.0003522633979670452, -0.0003643463874776212, -0.00036440583287247253, -0.00035384848291779427, -0.00033452187237945633, -0.00030852381729526104, -0.0002780165523803709, -0.00024506333662968507, -0.0002115001394814772, -0.00017884902826885524],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q5": {
            "samples": [0.00017716674147517767, 0.00020951073034151924, 0.00024275822589569251, 0.0002754014776493514, 0.0003056217856298131, 0.00033137529823506524, 0.0003505201191266274, 0.0003609781647094737, 0.00036091927846891955, 0.0003489499437759209, 0.0003242855321202921, 0.0002868842155482263, 0.00023752295606828736, 0.00017780137195139793, 0.0001100672360130904, 3.72668475902555e-05, -3.72668475902555e-05, -0.0001100672360130904, -0.00017780137195139793, -0.00023752295606828736, -0.0002868842155482263, -0.0003242855321202921, -0.0003489499437759209, -0.00036091927846891955, -0.0003609781647094737, -0.0003505201191266274, -0.00033137529823506524, -0.0003056217856298131, -0.0002754014776493514, -0.00024275822589569251, -0.00020951073034151924, -0.00017716674147517767],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q5": {
            "samples": [0.0, 0.00240190599889723, 0.0052128980552481625, 0.008435188868809378, 0.01205024788327971, 0.016015424750947284, 0.02026189986747093, 0.02469444097013115, 0.02919332608728938, 0.03361860438619903, 0.03781662347744681, 0.041628481836073566, 0.04489980399121703, 0.04749102307960268, 0.04928722606815851] + [0.050206597368484596] * 2 + [0.04928722606815851, 0.04749102307960268, 0.04489980399121703, 0.041628481836073566, 0.03781662347744681, 0.03361860438619903, 0.02919332608728938, 0.02469444097013115, 0.02026189986747093, 0.016015424750947284, 0.01205024788327971, 0.008435188868809378, 0.0052128980552481625, 0.00240190599889723, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q5": {
            "samples": [0.00035433348295035535, 0.0004190214606830385, 0.00048551645179138503, 0.0005508029552987027, 0.0006112435712596262, 0.0006627505964701305, 0.0007010402382532548, 0.0007219563294189474, 0.0007218385569378391, 0.0006978998875518418, 0.0006485710642405842, 0.0005737684310964526, 0.0004750459121365747, 0.00035560274390279586, 0.0002201344720261808, 7.4533695180511e-05, -7.4533695180511e-05, -0.0002201344720261808, -0.00035560274390279586, -0.0004750459121365747, -0.0005737684310964526, -0.0006485710642405842, -0.0006978998875518418, -0.0007218385569378391, -0.0007219563294189474, -0.0007010402382532548, -0.0006627505964701305, -0.0006112435712596262, -0.0005508029552987027, -0.00048551645179138503, -0.0004190214606830385, -0.00035433348295035535],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q5": {
            "samples": [0.0, 0.00480381199779446, 0.010425796110496325, 0.016870377737618757, 0.02410049576655942, 0.03203084950189457, 0.04052379973494186, 0.0493888819402623, 0.05838665217457876, 0.06723720877239805, 0.07563324695489362, 0.08325696367214713, 0.08979960798243405, 0.09498204615920536, 0.09857445213631702] + [0.10041319473696919] * 2 + [0.09857445213631702, 0.09498204615920536, 0.08979960798243405, 0.08325696367214713, 0.07563324695489362, 0.06723720877239805, 0.05838665217457876, 0.0493888819402623, 0.04052379973494186, 0.03203084950189457, 0.02410049576655942, 0.016870377737618757, 0.010425796110496325, 0.00480381199779446, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q5": {
            "samples": [-0.00017716674147517767, -0.00020951073034151924, -0.00024275822589569251, -0.0002754014776493514, -0.0003056217856298131, -0.00033137529823506524, -0.0003505201191266274, -0.0003609781647094737, -0.00036091927846891955, -0.0003489499437759209, -0.0003242855321202921, -0.0002868842155482263, -0.00023752295606828736, -0.00017780137195139793, -0.0001100672360130904, -3.72668475902555e-05, 3.72668475902555e-05, 0.0001100672360130904, 0.00017780137195139793, 0.00023752295606828736, 0.0002868842155482263, 0.0003242855321202921, 0.0003489499437759209, 0.00036091927846891955, 0.0003609781647094737, 0.0003505201191266274, 0.00033137529823506524, 0.0003056217856298131, 0.0002754014776493514, 0.00024275822589569251, 0.00020951073034151924, 0.00017716674147517767],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q5": {
            "samples": [0.0, -0.00240190599889723, -0.0052128980552481625, -0.008435188868809378, -0.01205024788327971, -0.016015424750947284, -0.02026189986747093, -0.02469444097013115, -0.02919332608728938, -0.03361860438619903, -0.03781662347744681, -0.041628481836073566, -0.04489980399121703, -0.04749102307960268, -0.04928722606815851] + [-0.050206597368484596] * 2 + [-0.04928722606815851, -0.04749102307960268, -0.04489980399121703, -0.041628481836073566, -0.03781662347744681, -0.03361860438619903, -0.02919332608728938, -0.02469444097013115, -0.02026189986747093, -0.016015424750947284, -0.01205024788327971, -0.008435188868809378, -0.0052128980552481625, -0.00240190599889723, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q5": {
            "sample": 0.056009617,
            "type": "constant",
        },
        "gft_cz_wf_1_2_q2": {
            "samples": [2.4279239730461816e-06, 3.7390309258980545e-05, 0.0003896159693902593, 0.0027470600886115074, 0.013105490717597775, 0.04230504225275136, 0.0924027075900485, 0.13656234921473673] + [0.14339591000000002] * 8 + [0.13656234921473673, 0.0924027075900485, 0.04230504225275136, 0.013105490717597775, 0.0027470600886115074, 0.0003896159693902593, 3.7390309258980545e-05, 2.4279239730461816e-06],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "g_cz_wf_1_2_q2": {
            "samples": [0.04295022651193382, 0.06652261215488213, 0.0967898295633299, 0.1322960113669045, 0.16987144112151573, 0.20490407079350736, 0.2321867308467583] + [0.24716148842062666] * 2 + [0.2321867308467583, 0.20490407079350736, 0.16987144112151573, 0.1322960113669045, 0.0967898295633299, 0.06652261215488213, 0.04295022651193382],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "cz_4c5t_wf": {
            "samples": [0.0] + [0.18326382712099998] * 39,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "cz_3c4t_wf": {
            "samples": [0.0] + [0.15726814504911504] * 47,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "cz_3c2t_wf": {
            "samples": [0.0] + [0.2674505421331572] * 51,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "cz_2c3t_wf": {
            "samples": [0.0] + [0.047] * 31,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "cz_2c1t_wf": {
            "samples": [0.0] + [-0.14656833826000001] * 23,
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
            "cosine": [(0.869494929505219, 1800)],
            "sine": [(0.493941866584231, 1800)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(-0.493941866584231, 1800)],
            "sine": [(0.869494929505219, 1800)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(0.493941866584231, 1800)],
            "sine": [(-0.869494929505219, 1800)],
        },
        "rotated_cosine_weights_q2": {
            "cosine": [(-0.9510565162951535, 1800)],
            "sine": [(0.3090169943749475, 1800)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(-0.3090169943749475, 1800)],
            "sine": [(-0.9510565162951535, 1800)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(0.3090169943749475, 1800)],
            "sine": [(0.9510565162951535, 1800)],
        },
        "rotated_cosine_weights_q3": {
            "cosine": [(0.5165333288666419, 1800)],
            "sine": [(0.8562670846003282, 1800)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(-0.8562670846003282, 1800)],
            "sine": [(0.5165333288666419, 1800)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(0.8562670846003282, 1800)],
            "sine": [(-0.5165333288666419, 1800)],
        },
        "rotated_cosine_weights_q4": {
            "cosine": [(-0.6560590289905077, 1800)],
            "sine": [(-0.7547095802227717, 1800)],
        },
        "rotated_sine_weights_q4": {
            "cosine": [(0.7547095802227717, 1800)],
            "sine": [(-0.6560590289905077, 1800)],
        },
        "rotated_minus_sine_weights_q4": {
            "cosine": [(-0.7547095802227717, 1800)],
            "sine": [(0.6560590289905077, 1800)],
        },
        "rotated_cosine_weights_q5": {
            "cosine": [(-0.8845809752150838, 1800)],
            "sine": [(-0.46638664033989147, 1800)],
        },
        "rotated_sine_weights_q5": {
            "cosine": [(0.46638664033989147, 1800)],
            "sine": [(-0.8845809752150838, 1800)],
        },
        "rotated_minus_sine_weights_q5": {
            "cosine": [(-0.46638664033989147, 1800)],
            "sine": [(0.8845809752150838, 1800)],
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
            {'intermediate_frequency': 131052000.0, 'lo_frequency': 3200000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
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
            {'intermediate_frequency': 207885000.0, 'lo_frequency': 3200000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
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
            {'intermediate_frequency': 364117000.0, 'lo_frequency': 3960000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
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
            {'intermediate_frequency': 128925000.0, 'lo_frequency': 4600000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
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
        ],
    },
}




# Single QUA script generated at 2024-06-04 11:33:11.556475
# QUA library version: 1.1.6

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
        with for_(v12,-3000000,(v12<=2850000),(v12+150000)):
            update_frequency("rr1", (v12+33900000), "Hz", False)
            update_frequency("rr2", (v12+133700000), "Hz", False)
            update_frequency("rr3", (v12+-22800000), "Hz", False)
            update_frequency("rr4", (v12+156000000), "Hz", False)
            update_frequency("rr5", (v12+62500000), "Hz", False)
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
                    "offset": 0.0,
                },
                "6": {
                    "offset": 0.0,
                },
                "7": {
                    "offset": 0.0,
                },
                "8": {
                    "offset": 0.0,
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
                    "offset": 0,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "4": {
                    "offset": 0,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
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
                    "offset": 0,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
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
            "RF_outputs": {
                "port": ('octave1', 1),
            },
            "RF_inputs": {
                "port": ('octave1', 1),
            },
            "intermediate_frequency": 33900000,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q1",
            },
            "time_of_flight": 284,
            "smearing": 0,
        },
        "rr2": {
            "RF_outputs": {
                "port": ('octave1', 1),
            },
            "RF_inputs": {
                "port": ('octave1', 1),
            },
            "intermediate_frequency": 133700000,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q2",
            },
            "time_of_flight": 284,
            "smearing": 0,
        },
        "rr3": {
            "RF_outputs": {
                "port": ('octave1', 1),
            },
            "RF_inputs": {
                "port": ('octave1', 1),
            },
            "intermediate_frequency": -22800000,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q3",
            },
            "time_of_flight": 284,
            "smearing": 0,
        },
        "rr4": {
            "RF_outputs": {
                "port": ('octave1', 1),
            },
            "RF_inputs": {
                "port": ('octave1', 1),
            },
            "intermediate_frequency": 156000000,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q4",
            },
            "time_of_flight": 284,
            "smearing": 0,
        },
        "rr5": {
            "RF_outputs": {
                "port": ('octave1', 1),
            },
            "RF_inputs": {
                "port": ('octave1', 1),
            },
            "intermediate_frequency": 62500000,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q5",
            },
            "time_of_flight": 284,
            "smearing": 0,
        },
        "q1_xy": {
            "RF_inputs": {
                "port": ('octave2', 1),
            },
            "intermediate_frequency": -118000000,
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
            "RF_inputs": {
                "port": ('octave1', 4),
            },
            "intermediate_frequency": -164000000,
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
            "RF_inputs": {
                "port": ('octave1', 3),
            },
            "intermediate_frequency": -137000000,
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
            "RF_inputs": {
                "port": ('octave1', 5),
            },
            "intermediate_frequency": -180000000,
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
            "RF_inputs": {
                "port": ('octave1', 5),
            },
            "intermediate_frequency": -180000000,
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
            "RF_inputs": {
                "port": ('octave1', 2),
            },
            "intermediate_frequency": -237000000,
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
        "c1_2": {
            "singleInput": {
                "port": ('con2', 3),
            },
            "operations": {
                "const": "const_flux_pulse",
            },
        },
        "c2_3": {
            "singleInput": {
                "port": ('con2', 4),
            },
            "operations": {
                "const": "const_flux_pulse",
            },
        },
        "c3_4": {
            "singleInput": {
                "port": ('con2', 5),
            },
            "operations": {
                "const": "const_flux_pulse",
            },
        },
        "c4_5": {
            "singleInput": {
                "port": ('con2', 10),
            },
            "operations": {
                "const": "const_flux_pulse",
            },
        },
    },
    "octaves": {
        "octave1": {
            "RF_outputs": {
                "1": {
                    "LO_frequency": 5880000000,
                    "LO_source": "internal",
                    "output_mode": "always_on",
                    "gain": 6,
                },
                "2": {
                    "LO_frequency": 4600000000,
                    "LO_source": "internal",
                    "output_mode": "always_on",
                    "gain": 20,
                },
                "3": {
                    "LO_frequency": 4600000000,
                    "LO_source": "internal",
                    "output_mode": "always_on",
                    "gain": 15,
                },
                "4": {
                    "LO_frequency": 4600000000,
                    "LO_source": "internal",
                    "output_mode": "always_on",
                    "gain": 20,
                },
                "5": {
                    "LO_frequency": 4600000000,
                    "LO_source": "internal",
                    "output_mode": "always_on",
                    "gain": 20,
                },
            },
            "RF_inputs": {
                "1": {
                    "LO_frequency": 5880000000,
                    "LO_source": "internal",
                },
            },
            "connectivity": "con1",
        },
        "octave2": {
            "RF_outputs": {
                "1": {
                    "LO_frequency": 5200000000,
                    "LO_source": "internal",
                    "output_mode": "always_on",
                    "gain": 15,
                },
            },
            "connectivity": "con2",
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
            "samples": [0.0, 0.002818510006488263, 0.0062462140735056355, 0.010260296953555697, 0.014776135656103749, 0.019640377995182673, 0.024632684946047638, 0.029477944546864705, 0.03386899287708845, 0.037497724357144276, 0.04009042935498788] + [0.04144180729744212] * 2 + [0.04009042935498788, 0.037497724357144276, 0.03386899287708845, 0.029477944546864705, 0.024632684946047638, 0.019640377995182673, 0.014776135656103749, 0.010260296953555697, 0.0062462140735056355, 0.002818510006488263, 0.0],
        },
        "x90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.0017647859941029365, -0.0021871803668976255, -0.0026124997714417056, -0.003001409148925006, -0.0033073291950408493, -0.0034815742937947054, -0.0034802257305028518, -0.003271718395842828, -0.002843717096039479, -0.002207748305270042, -0.0014003231921690122, -0.00047992211466432776, 0.00047992211466432776, 0.0014003231921690122, 0.002207748305270042, 0.002843717096039479, 0.003271718395842828, 0.0034802257305028518, 0.0034815742937947054, 0.0033073291950408493, 0.003001409148925006, 0.0026124997714417056, 0.0021871803668976255, 0.0017647859941029365],
        },
        "x180_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.005637020012976526, 0.012492428147011271, 0.020520593907111393, 0.029552271312207497, 0.039280755990365346, 0.049265369892095276, 0.05895588909372941, 0.0677379857541769, 0.07499544871428855, 0.08018085870997577] + [0.08288361459488423] * 2 + [0.08018085870997577, 0.07499544871428855, 0.0677379857541769, 0.05895588909372941, 0.049265369892095276, 0.039280755990365346, 0.029552271312207497, 0.020520593907111393, 0.012492428147011271, 0.005637020012976526, 0.0],
        },
        "x180_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.003529571988205873, -0.004374360733795251, -0.005224999542883411, -0.006002818297850012, -0.0066146583900816985, -0.006963148587589411, -0.0069604514610057035, -0.006543436791685656, -0.005687434192078958, -0.004415496610540084, -0.0028006463843380245, -0.0009598442293286555, 0.0009598442293286555, 0.0028006463843380245, 0.004415496610540084, 0.005687434192078958, 0.006543436791685656, 0.0069604514610057035, 0.006963148587589411, 0.0066146583900816985, 0.006002818297850012, 0.005224999542883411, 0.004374360733795251, 0.003529571988205873],
        },
        "minus_x90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, -0.002818510006488263, -0.0062462140735056355, -0.010260296953555697, -0.014776135656103749, -0.019640377995182673, -0.024632684946047638, -0.029477944546864705, -0.03386899287708845, -0.037497724357144276, -0.04009042935498788] + [-0.04144180729744212] * 2 + [-0.04009042935498788, -0.037497724357144276, -0.03386899287708845, -0.029477944546864705, -0.024632684946047638, -0.019640377995182673, -0.014776135656103749, -0.010260296953555697, -0.0062462140735056355, -0.002818510006488263, 0.0],
        },
        "minus_x90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0017647859941029365, 0.0021871803668976255, 0.0026124997714417056, 0.003001409148925006, 0.0033073291950408493, 0.0034815742937947054, 0.0034802257305028518, 0.003271718395842828, 0.002843717096039479, 0.002207748305270042, 0.0014003231921690122, 0.00047992211466432776, -0.00047992211466432776, -0.0014003231921690122, -0.002207748305270042, -0.002843717096039479, -0.003271718395842828, -0.0034802257305028518, -0.0034815742937947054, -0.0033073291950408493, -0.003001409148925006, -0.0026124997714417056, -0.0021871803668976255, -0.0017647859941029365],
        },
        "y90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0017647859941029365, 0.0021871803668976255, 0.0026124997714417056, 0.003001409148925006, 0.0033073291950408493, 0.0034815742937947054, 0.0034802257305028518, 0.003271718395842828, 0.002843717096039479, 0.002207748305270042, 0.0014003231921690122, 0.00047992211466432776, -0.00047992211466432776, -0.0014003231921690122, -0.002207748305270042, -0.002843717096039479, -0.003271718395842828, -0.0034802257305028518, -0.0034815742937947054, -0.0033073291950408493, -0.003001409148925006, -0.0026124997714417056, -0.0021871803668976255, -0.0017647859941029365],
        },
        "y90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.002818510006488263, 0.0062462140735056355, 0.010260296953555697, 0.014776135656103749, 0.019640377995182673, 0.024632684946047638, 0.029477944546864705, 0.03386899287708845, 0.037497724357144276, 0.04009042935498788] + [0.04144180729744212] * 2 + [0.04009042935498788, 0.037497724357144276, 0.03386899287708845, 0.029477944546864705, 0.024632684946047638, 0.019640377995182673, 0.014776135656103749, 0.010260296953555697, 0.0062462140735056355, 0.002818510006488263, 0.0],
        },
        "y180_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.003529571988205873, 0.004374360733795251, 0.005224999542883411, 0.006002818297850012, 0.0066146583900816985, 0.006963148587589411, 0.0069604514610057035, 0.006543436791685656, 0.005687434192078958, 0.004415496610540084, 0.0028006463843380245, 0.0009598442293286555, -0.0009598442293286555, -0.0028006463843380245, -0.004415496610540084, -0.005687434192078958, -0.006543436791685656, -0.0069604514610057035, -0.006963148587589411, -0.0066146583900816985, -0.006002818297850012, -0.005224999542883411, -0.004374360733795251, -0.003529571988205873],
        },
        "y180_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.005637020012976526, 0.012492428147011271, 0.020520593907111393, 0.029552271312207497, 0.039280755990365346, 0.049265369892095276, 0.05895588909372941, 0.0677379857541769, 0.07499544871428855, 0.08018085870997577] + [0.08288361459488423] * 2 + [0.08018085870997577, 0.07499544871428855, 0.0677379857541769, 0.05895588909372941, 0.049265369892095276, 0.039280755990365346, 0.029552271312207497, 0.020520593907111393, 0.012492428147011271, 0.005637020012976526, 0.0],
        },
        "minus_y90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.0017647859941029365, -0.0021871803668976255, -0.0026124997714417056, -0.003001409148925006, -0.0033073291950408493, -0.0034815742937947054, -0.0034802257305028518, -0.003271718395842828, -0.002843717096039479, -0.002207748305270042, -0.0014003231921690122, -0.00047992211466432776, 0.00047992211466432776, 0.0014003231921690122, 0.002207748305270042, 0.002843717096039479, 0.003271718395842828, 0.0034802257305028518, 0.0034815742937947054, 0.0033073291950408493, 0.003001409148925006, 0.0026124997714417056, 0.0021871803668976255, 0.0017647859941029365],
        },
        "minus_y90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, -0.002818510006488263, -0.0062462140735056355, -0.010260296953555697, -0.014776135656103749, -0.019640377995182673, -0.024632684946047638, -0.029477944546864705, -0.03386899287708845, -0.037497724357144276, -0.04009042935498788] + [-0.04144180729744212] * 2 + [-0.04009042935498788, -0.037497724357144276, -0.03386899287708845, -0.029477944546864705, -0.024632684946047638, -0.019640377995182673, -0.014776135656103749, -0.010260296953555697, -0.0062462140735056355, -0.002818510006488263, 0.0],
        },
        "readout_wf_q1": {
            "type": "constant",
            "sample": 0.0065,
        },
        "x90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.003852628076704988, 0.008537964973443802, 0.014024824473783162, 0.020197535209334032, 0.026846479709900825, 0.03367047603496476, 0.04029347298514784, 0.046295607461961874, 0.051255729210936955, 0.05479970388064235] + [0.056646905626016285] * 2 + [0.05479970388064235, 0.051255729210936955, 0.046295607461961874, 0.04029347298514784, 0.03367047603496476, 0.026846479709900825, 0.020197535209334032, 0.014024824473783162, 0.008537964973443802, 0.003852628076704988, 0.0],
        },
        "x90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.0016116979263006178, -0.0019974512907250082, -0.0023858759521908587, -0.0027410490096058527, -0.0030204317254627507, -0.003179561764610861, -0.00317833018374597, -0.002987910019480756, -0.0025970361063535918, -0.0020162350433918313, -0.0012788508025964184, -0.00043829080668983833, 0.00043829080668983833, 0.0012788508025964184, 0.0020162350433918313, 0.0025970361063535918, 0.002987910019480756, 0.00317833018374597, 0.003179561764610861, 0.0030204317254627507, 0.0027410490096058527, 0.0023858759521908587, 0.0019974512907250082, 0.0016116979263006178],
        },
        "x180_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.007504638764750569, 0.016631333634101877, 0.027319336130881628, 0.03934332685807018, 0.052294986257880316, 0.065587633856345, 0.07848874931872259, 0.09018046992323753, 0.09984242566205283, 0.10674583008055356] + [0.11034404448086606] * 2 + [0.10674583008055356, 0.09984242566205283, 0.09018046992323753, 0.07848874931872259, 0.065587633856345, 0.052294986257880316, 0.03934332685807018, 0.027319336130881628, 0.016631333634101877, 0.007504638764750569, 0.0],
        },
        "x180_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.003139470121166824, -0.003890889566453162, -0.004647512503727403, -0.005339363739248481, -0.005883580912013875, -0.00619355463297802, -0.006191155603194567, -0.005820230998513521, -0.0050588370974721675, -0.003927478947936227, -0.0024911081776950775, -0.0008537585545842521, 0.0008537585545842521, 0.0024911081776950775, 0.003927478947936227, 0.0050588370974721675, 0.005820230998513521, 0.006191155603194567, 0.00619355463297802, 0.005883580912013875, 0.005339363739248481, 0.004647512503727403, 0.003890889566453162, 0.003139470121166824],
        },
        "minus_x90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, -0.003852628076704988, -0.008537964973443802, -0.014024824473783162, -0.020197535209334032, -0.026846479709900825, -0.03367047603496476, -0.04029347298514784, -0.046295607461961874, -0.051255729210936955, -0.05479970388064235] + [-0.056646905626016285] * 2 + [-0.05479970388064235, -0.051255729210936955, -0.046295607461961874, -0.04029347298514784, -0.03367047603496476, -0.026846479709900825, -0.020197535209334032, -0.014024824473783162, -0.008537964973443802, -0.003852628076704988, 0.0],
        },
        "minus_x90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0016116979263006178, 0.0019974512907250082, 0.0023858759521908587, 0.0027410490096058527, 0.0030204317254627507, 0.003179561764610861, 0.00317833018374597, 0.002987910019480756, 0.0025970361063535918, 0.0020162350433918313, 0.0012788508025964184, 0.00043829080668983833, -0.00043829080668983833, -0.0012788508025964184, -0.0020162350433918313, -0.0025970361063535918, -0.002987910019480756, -0.00317833018374597, -0.003179561764610861, -0.0030204317254627507, -0.0027410490096058527, -0.0023858759521908587, -0.0019974512907250082, -0.0016116979263006178],
        },
        "y90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.001569735060583412, 0.001945444783226581, 0.0023237562518637015, 0.0026696818696242404, 0.0029417904560069376, 0.00309677731648901, 0.0030955778015972833, 0.0029101154992567605, 0.0025294185487360838, 0.0019637394739681134, 0.0012455540888475388, 0.00042687927729212607, -0.00042687927729212607, -0.0012455540888475388, -0.0019637394739681134, -0.0025294185487360838, -0.0029101154992567605, -0.0030955778015972833, -0.00309677731648901, -0.0029417904560069376, -0.0026696818696242404, -0.0023237562518637015, -0.001945444783226581, -0.001569735060583412],
        },
        "y90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0037523193823752847, 0.008315666817050938, 0.013659668065440814, 0.01967166342903509, 0.026147493128940158, 0.0327938169281725, 0.03924437465936129, 0.045090234961618764, 0.049921212831026414, 0.05337291504027678] + [0.05517202224043303] * 2 + [0.05337291504027678, 0.049921212831026414, 0.045090234961618764, 0.03924437465936129, 0.0327938169281725, 0.026147493128940158, 0.01967166342903509, 0.013659668065440814, 0.008315666817050938, 0.0037523193823752847, 0.0],
        },
        "y180_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.003139470121166824, 0.003890889566453162, 0.004647512503727403, 0.005339363739248481, 0.005883580912013875, 0.00619355463297802, 0.006191155603194567, 0.005820230998513521, 0.0050588370974721675, 0.003927478947936227, 0.0024911081776950775, 0.0008537585545842521, -0.0008537585545842521, -0.0024911081776950775, -0.003927478947936227, -0.0050588370974721675, -0.005820230998513521, -0.006191155603194567, -0.00619355463297802, -0.005883580912013875, -0.005339363739248481, -0.004647512503727403, -0.003890889566453162, -0.003139470121166824],
        },
        "y180_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.007504638764750569, 0.016631333634101877, 0.027319336130881628, 0.03934332685807018, 0.052294986257880316, 0.065587633856345, 0.07848874931872259, 0.09018046992323753, 0.09984242566205283, 0.10674583008055356] + [0.11034404448086606] * 2 + [0.10674583008055356, 0.09984242566205283, 0.09018046992323753, 0.07848874931872259, 0.065587633856345, 0.052294986257880316, 0.03934332685807018, 0.027319336130881628, 0.016631333634101877, 0.007504638764750569, 0.0],
        },
        "minus_y90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.001569735060583412, -0.001945444783226581, -0.0023237562518637015, -0.0026696818696242404, -0.0029417904560069376, -0.00309677731648901, -0.0030955778015972833, -0.0029101154992567605, -0.0025294185487360838, -0.0019637394739681134, -0.0012455540888475388, -0.00042687927729212607, 0.00042687927729212607, 0.0012455540888475388, 0.0019637394739681134, 0.0025294185487360838, 0.0029101154992567605, 0.0030955778015972833, 0.00309677731648901, 0.0029417904560069376, 0.0026696818696242404, 0.0023237562518637015, 0.001945444783226581, 0.001569735060583412],
        },
        "minus_y90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, -0.0037523193823752847, -0.008315666817050938, -0.013659668065440814, -0.01967166342903509, -0.026147493128940158, -0.0327938169281725, -0.03924437465936129, -0.045090234961618764, -0.049921212831026414, -0.05337291504027678] + [-0.05517202224043303] * 2 + [-0.05337291504027678, -0.049921212831026414, -0.045090234961618764, -0.03924437465936129, -0.0327938169281725, -0.026147493128940158, -0.01967166342903509, -0.013659668065440814, -0.008315666817050938, -0.0037523193823752847, 0.0],
        },
        "readout_wf_q2": {
            "type": "constant",
            "sample": 0.033,
        },
        "x90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.00554591665923145, 0.012290530318372706, 0.020188947944976256, 0.029074658846555662, 0.038645915489510956, 0.04846916189383918, 0.05800306664372974, 0.06664323042885688, 0.07378340105830004, 0.07888500644799634] + [0.08154408142971438] * 2 + [0.07888500644799634, 0.07378340105830004, 0.06664323042885688, 0.05800306664372974, 0.04846916189383918, 0.038645915489510956, 0.029074658846555662, 0.020188947944976256, 0.012290530318372706, 0.00554591665923145, 0.0],
        },
        "x90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.003042155140335954, 0.0037702826395002477, 0.004503452336643101, 0.005173858077502959, 0.00570120600746893, 0.006001571391500573, 0.005999246725074112, 0.005639819767894428, 0.0049020269938028155, 0.0038057378503047546, 0.0024138906425048012, 0.0008272943761824908, -0.0008272943761824908, -0.0024138906425048012, -0.0038057378503047546, -0.0049020269938028155, -0.005639819767894428, -0.005999246725074112, -0.006001571391500573, -0.00570120600746893, -0.005173858077502959, -0.004503452336643101, -0.0037702826395002477, -0.003042155140335954],
        },
        "x180_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0110918333184629, 0.02458106063674541, 0.04037789588995251, 0.058149317693111324, 0.07729183097902191, 0.09693832378767836, 0.11600613328745948, 0.13328646085771376, 0.1475668021166001, 0.15777001289599268] + [0.16308816285942876] * 2 + [0.15777001289599268, 0.1475668021166001, 0.13328646085771376, 0.11600613328745948, 0.09693832378767836, 0.07729183097902191, 0.058149317693111324, 0.04037789588995251, 0.02458106063674541, 0.0110918333184629, 0.0],
        },
        "x180_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.006084310280671908, 0.007540565279000495, 0.009006904673286202, 0.010347716155005918, 0.01140241201493786, 0.012003142783001146, 0.011998493450148223, 0.011279639535788855, 0.009804053987605631, 0.007611475700609509, 0.0048277812850096025, 0.0016545887523649815, -0.0016545887523649815, -0.0048277812850096025, -0.007611475700609509, -0.009804053987605631, -0.011279639535788855, -0.011998493450148223, -0.012003142783001146, -0.01140241201493786, -0.010347716155005918, -0.009006904673286202, -0.007540565279000495, -0.006084310280671908],
        },
        "minus_x90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, -0.00554591665923145, -0.012290530318372706, -0.020188947944976256, -0.029074658846555662, -0.038645915489510956, -0.04846916189383918, -0.05800306664372974, -0.06664323042885688, -0.07378340105830004, -0.07888500644799634] + [-0.08154408142971438] * 2 + [-0.07888500644799634, -0.07378340105830004, -0.06664323042885688, -0.05800306664372974, -0.04846916189383918, -0.038645915489510956, -0.029074658846555662, -0.020188947944976256, -0.012290530318372706, -0.00554591665923145, 0.0],
        },
        "minus_x90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.003042155140335954, -0.0037702826395002477, -0.004503452336643101, -0.005173858077502959, -0.00570120600746893, -0.006001571391500573, -0.005999246725074112, -0.005639819767894428, -0.0049020269938028155, -0.0038057378503047546, -0.0024138906425048012, -0.0008272943761824908, 0.0008272943761824908, 0.0024138906425048012, 0.0038057378503047546, 0.0049020269938028155, 0.005639819767894428, 0.005999246725074112, 0.006001571391500573, 0.00570120600746893, 0.005173858077502959, 0.004503452336643101, 0.0037702826395002477, 0.003042155140335954],
        },
        "y90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.003042155140335954, -0.0037702826395002477, -0.004503452336643101, -0.005173858077502959, -0.00570120600746893, -0.006001571391500573, -0.005999246725074112, -0.005639819767894428, -0.0049020269938028155, -0.0038057378503047546, -0.0024138906425048012, -0.0008272943761824908, 0.0008272943761824908, 0.0024138906425048012, 0.0038057378503047546, 0.0049020269938028155, 0.005639819767894428, 0.005999246725074112, 0.006001571391500573, 0.00570120600746893, 0.005173858077502959, 0.004503452336643101, 0.0037702826395002477, 0.003042155140335954],
        },
        "y90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.00554591665923145, 0.012290530318372706, 0.020188947944976256, 0.029074658846555662, 0.038645915489510956, 0.04846916189383918, 0.05800306664372974, 0.06664323042885688, 0.07378340105830004, 0.07888500644799634] + [0.08154408142971438] * 2 + [0.07888500644799634, 0.07378340105830004, 0.06664323042885688, 0.05800306664372974, 0.04846916189383918, 0.038645915489510956, 0.029074658846555662, 0.020188947944976256, 0.012290530318372706, 0.00554591665923145, 0.0],
        },
        "y180_I_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.006084310280671908, -0.007540565279000495, -0.009006904673286202, -0.010347716155005918, -0.01140241201493786, -0.012003142783001146, -0.011998493450148223, -0.011279639535788855, -0.009804053987605631, -0.007611475700609509, -0.0048277812850096025, -0.0016545887523649815, 0.0016545887523649815, 0.0048277812850096025, 0.007611475700609509, 0.009804053987605631, 0.011279639535788855, 0.011998493450148223, 0.012003142783001146, 0.01140241201493786, 0.010347716155005918, 0.009006904673286202, 0.007540565279000495, 0.006084310280671908],
        },
        "y180_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0110918333184629, 0.02458106063674541, 0.04037789588995251, 0.058149317693111324, 0.07729183097902191, 0.09693832378767836, 0.11600613328745948, 0.13328646085771376, 0.1475668021166001, 0.15777001289599268] + [0.16308816285942876] * 2 + [0.15777001289599268, 0.1475668021166001, 0.13328646085771376, 0.11600613328745948, 0.09693832378767836, 0.07729183097902191, 0.058149317693111324, 0.04037789588995251, 0.02458106063674541, 0.0110918333184629, 0.0],
        },
        "minus_y90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.003042155140335954, 0.0037702826395002477, 0.004503452336643101, 0.005173858077502959, 0.00570120600746893, 0.006001571391500573, 0.005999246725074112, 0.005639819767894428, 0.0049020269938028155, 0.0038057378503047546, 0.0024138906425048012, 0.0008272943761824908, -0.0008272943761824908, -0.0024138906425048012, -0.0038057378503047546, -0.0049020269938028155, -0.005639819767894428, -0.005999246725074112, -0.006001571391500573, -0.00570120600746893, -0.005173858077502959, -0.004503452336643101, -0.0037702826395002477, -0.003042155140335954],
        },
        "minus_y90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, -0.00554591665923145, -0.012290530318372706, -0.020188947944976256, -0.029074658846555662, -0.038645915489510956, -0.04846916189383918, -0.05800306664372974, -0.06664323042885688, -0.07378340105830004, -0.07888500644799634] + [-0.08154408142971438] * 2 + [-0.07888500644799634, -0.07378340105830004, -0.06664323042885688, -0.05800306664372974, -0.04846916189383918, -0.038645915489510956, -0.029074658846555662, -0.020188947944976256, -0.012290530318372706, -0.00554591665923145, 0.0],
        },
        "readout_wf_q3": {
            "type": "constant",
            "sample": 0.0246,
        },
        "x90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.004061810889195392, 0.009001543468572511, 0.014786318230693984, 0.021294183298987135, 0.028304139784886988, 0.03549865273270312, 0.042481252816531936, 0.0488092799945899, 0.05403871718151735, 0.05777511597679206] + [0.0597226136367057] * 2 + [0.05777511597679206, 0.05403871718151735, 0.0488092799945899, 0.042481252816531936, 0.03549865273270312, 0.028304139784886988, 0.021294183298987135, 0.014786318230693984, 0.009001543468572511, 0.004061810889195392, 0.0],
        },
        "x90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.002564170188378035, 0.003177893927164464, 0.003795867631236719, 0.0043609388835333706, 0.004805429640428921, 0.005058601463635019, 0.005056642049971453, 0.004753688437816817, 0.004131818036980678, 0.0032077783973422525, 0.0020346189257238125, 0.0006973094660076023, -0.0006973094660076023, -0.0020346189257238125, -0.0032077783973422525, -0.004131818036980678, -0.004753688437816817, -0.005056642049971453, -0.005058601463635019, -0.004805429640428921, -0.0043609388835333706, -0.003795867631236719, -0.003177893927164464, -0.002564170188378035],
        },
        "x180_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.00802848304878475, 0.01779224614877363, 0.029226300413158643, 0.04208959853556825, 0.05594531913779306, 0.07016582984631749, 0.08396747840622067, 0.0964753130438277, 0.10681169968398671, 0.11419698058693514] + [0.11804636018059267] * 2 + [0.11419698058693514, 0.10681169968398671, 0.0964753130438277, 0.08396747840622067, 0.07016582984631749, 0.05594531913779306, 0.04208959853556825, 0.029226300413158643, 0.01779224614877363, 0.00802848304878475, 0.0],
        },
        "x180_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.005068280491923697, 0.006281352879560064, 0.007502825651947461, 0.008619732641016545, 0.009498302964556232, 0.009998716633850109, 0.009994843701354575, 0.009396032479930769, 0.008166857585320417, 0.006340421843819946, 0.004021581506751552, 0.0013782860355441512, -0.0013782860355441512, -0.004021581506751552, -0.006340421843819946, -0.008166857585320417, -0.009396032479930769, -0.009994843701354575, -0.009998716633850109, -0.009498302964556232, -0.008619732641016545, -0.007502825651947461, -0.006281352879560064, -0.005068280491923697],
        },
        "minus_x90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, -0.004061810889195392, -0.009001543468572511, -0.014786318230693984, -0.021294183298987135, -0.028304139784886988, -0.03549865273270312, -0.042481252816531936, -0.0488092799945899, -0.05403871718151735, -0.05777511597679206] + [-0.0597226136367057] * 2 + [-0.05777511597679206, -0.05403871718151735, -0.0488092799945899, -0.042481252816531936, -0.03549865273270312, -0.028304139784886988, -0.021294183298987135, -0.014786318230693984, -0.009001543468572511, -0.004061810889195392, 0.0],
        },
        "minus_x90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.002564170188378035, -0.003177893927164464, -0.003795867631236719, -0.0043609388835333706, -0.004805429640428921, -0.005058601463635019, -0.005056642049971453, -0.004753688437816817, -0.004131818036980678, -0.0032077783973422525, -0.0020346189257238125, -0.0006973094660076023, 0.0006973094660076023, 0.0020346189257238125, 0.0032077783973422525, 0.004131818036980678, 0.004753688437816817, 0.005056642049971453, 0.005058601463635019, 0.004805429640428921, 0.0043609388835333706, 0.003795867631236719, 0.003177893927164464, 0.002564170188378035],
        },
        "y90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.0025341402459618484, -0.003140676439780032, -0.0037514128259737304, -0.004309866320508273, -0.004749151482278116, -0.0049993583169250545, -0.0049974218506772874, -0.0046980162399653845, -0.004083428792660208, -0.003170210921909973, -0.002010790753375776, -0.0006891430177720756, 0.0006891430177720756, 0.002010790753375776, 0.003170210921909973, 0.004083428792660208, 0.0046980162399653845, 0.0049974218506772874, 0.0049993583169250545, 0.004749151482278116, 0.004309866320508273, 0.0037514128259737304, 0.003140676439780032, 0.0025341402459618484],
        },
        "y90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.004014241524392375, 0.008896123074386815, 0.014613150206579321, 0.021044799267784124, 0.02797265956889653, 0.035082914923158744, 0.04198373920311033, 0.04823765652191385, 0.053405849841993355, 0.05709849029346757] + [0.059023180090296334] * 2 + [0.05709849029346757, 0.053405849841993355, 0.04823765652191385, 0.04198373920311033, 0.035082914923158744, 0.02797265956889653, 0.021044799267784124, 0.014613150206579321, 0.008896123074386815, 0.004014241524392375, 0.0],
        },
        "y180_I_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.005068280491923697, -0.006281352879560064, -0.007502825651947461, -0.008619732641016545, -0.009498302964556232, -0.009998716633850109, -0.009994843701354575, -0.009396032479930769, -0.008166857585320417, -0.006340421843819946, -0.004021581506751552, -0.0013782860355441512, 0.0013782860355441512, 0.004021581506751552, 0.006340421843819946, 0.008166857585320417, 0.009396032479930769, 0.009994843701354575, 0.009998716633850109, 0.009498302964556232, 0.008619732641016545, 0.007502825651947461, 0.006281352879560064, 0.005068280491923697],
        },
        "y180_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.00802848304878475, 0.01779224614877363, 0.029226300413158643, 0.04208959853556825, 0.05594531913779306, 0.07016582984631749, 0.08396747840622067, 0.0964753130438277, 0.10681169968398671, 0.11419698058693514] + [0.11804636018059267] * 2 + [0.11419698058693514, 0.10681169968398671, 0.0964753130438277, 0.08396747840622067, 0.07016582984631749, 0.05594531913779306, 0.04208959853556825, 0.029226300413158643, 0.01779224614877363, 0.00802848304878475, 0.0],
        },
        "minus_y90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0025341402459618484, 0.003140676439780032, 0.0037514128259737304, 0.004309866320508273, 0.004749151482278116, 0.0049993583169250545, 0.0049974218506772874, 0.0046980162399653845, 0.004083428792660208, 0.003170210921909973, 0.002010790753375776, 0.0006891430177720756, -0.0006891430177720756, -0.002010790753375776, -0.003170210921909973, -0.004083428792660208, -0.0046980162399653845, -0.0049974218506772874, -0.0049993583169250545, -0.004749151482278116, -0.004309866320508273, -0.0037514128259737304, -0.003140676439780032, -0.0025341402459618484],
        },
        "minus_y90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, -0.004014241524392375, -0.008896123074386815, -0.014613150206579321, -0.021044799267784124, -0.02797265956889653, -0.035082914923158744, -0.04198373920311033, -0.04823765652191385, -0.053405849841993355, -0.05709849029346757] + [-0.059023180090296334] * 2 + [-0.05709849029346757, -0.053405849841993355, -0.04823765652191385, -0.04198373920311033, -0.035082914923158744, -0.02797265956889653, -0.021044799267784124, -0.014613150206579321, -0.008896123074386815, -0.004014241524392375, 0.0],
        },
        "readout_wf_q4": {
            "type": "constant",
            "sample": 0.0155,
        },
        "x90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.0073220605394498685, 0.0162267146411717, 0.02665469176044265, 0.03838615423186577, 0.05102271638821851, 0.06399197093817635, 0.0765792188261966, 0.08798649488040082, 0.09741338764189966, 0.10414884109476791] + [0.10765951555877512] * 2 + [0.10414884109476791, 0.09741338764189966, 0.08798649488040082, 0.0765792188261966, 0.06399197093817635, 0.05102271638821851, 0.03838615423186577, 0.02665469176044265, 0.0162267146411717, 0.0073220605394498685, 0.0],
        },
        "x90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0006148801292574054, -0.0007620491953138363, -0.0009102373899819839, -0.001045739739329392, -0.0011523272565279047, -0.0012130370815164589, -0.0012125672201429114, -0.0011399198751870477, -0.000990797264612844, -0.000769215399401612, -0.0004878953642425624, -0.00016721266651274031, 0.00016721266651274031, 0.0004878953642425624, 0.000769215399401612, 0.000990797264612844, 0.0011399198751870477, 0.0012125672201429114, 0.0012130370815164589, 0.0011523272565279047, 0.001045739739329392, 0.0009102373899819839, 0.0007620491953138363, 0.0006148801292574054],
        },
        "x180_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.014576536599212028, 0.03230365258217056, 0.053063353941621365, 0.07641799450429412, 0.10157448013670231, 0.1273932797209736, 0.15245159199994676, 0.1751608520512049, 0.1939276249581603, 0.207336361916705] + [0.2143253064271754] * 2 + [0.207336361916705, 0.1939276249581603, 0.1751608520512049, 0.15245159199994676, 0.1273932797209736, 0.10157448013670231, 0.07641799450429412, 0.053063353941621365, 0.03230365258217056, 0.014576536599212028, 0.0],
        },
        "x180_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0012240847586494005, -0.0015170644828794045, -0.0018120730575167433, -0.0020818270350890333, -0.0022940182396129984, -0.002414877522476003, -0.0024139421366688014, -0.002269318000214408, -0.001972449218661253, -0.0015313307451699284, -0.0009712873302740991, -0.0003328819176163112, 0.0003328819176163112, 0.0009712873302740991, 0.0015313307451699284, 0.001972449218661253, 0.002269318000214408, 0.0024139421366688014, 0.002414877522476003, 0.0022940182396129984, 0.0020818270350890333, 0.0018120730575167433, 0.0015170644828794045, 0.0012240847586494005],
        },
        "minus_x90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, -0.0073220605394498685, -0.0162267146411717, -0.02665469176044265, -0.03838615423186577, -0.05102271638821851, -0.06399197093817635, -0.0765792188261966, -0.08798649488040082, -0.09741338764189966, -0.10414884109476791] + [-0.10765951555877512] * 2 + [-0.10414884109476791, -0.09741338764189966, -0.08798649488040082, -0.0765792188261966, -0.06399197093817635, -0.05102271638821851, -0.03838615423186577, -0.02665469176044265, -0.0162267146411717, -0.0073220605394498685, 0.0],
        },
        "minus_x90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0006148801292574054, 0.0007620491953138363, 0.0009102373899819839, 0.001045739739329392, 0.0011523272565279047, 0.0012130370815164589, 0.0012125672201429114, 0.0011399198751870477, 0.000990797264612844, 0.000769215399401612, 0.0004878953642425624, 0.00016721266651274031, -0.00016721266651274031, -0.0004878953642425624, -0.000769215399401612, -0.000990797264612844, -0.0011399198751870477, -0.0012125672201429114, -0.0012130370815164589, -0.0011523272565279047, -0.001045739739329392, -0.0009102373899819839, -0.0007620491953138363, -0.0006148801292574054],
        },
        "y90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0006120423793247003, 0.0007585322414397022, 0.0009060365287583717, 0.0010409135175445167, 0.0011470091198064992, 0.0012074387612380016, 0.0012069710683344007, 0.001134659000107204, 0.0009862246093306265, 0.0007656653725849642, 0.00048564366513704956, 0.0001664409588081556, -0.0001664409588081556, -0.00048564366513704956, -0.0007656653725849642, -0.0009862246093306265, -0.001134659000107204, -0.0012069710683344007, -0.0012074387612380016, -0.0011470091198064992, -0.0010409135175445167, -0.0009060365287583717, -0.0007585322414397022, -0.0006120423793247003],
        },
        "y90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.007288268299606014, 0.01615182629108528, 0.026531676970810682, 0.03820899725214706, 0.050787240068351155, 0.0636966398604868, 0.07622579599997338, 0.08758042602560245, 0.09696381247908015, 0.1036681809583525] + [0.1071626532135877] * 2 + [0.1036681809583525, 0.09696381247908015, 0.08758042602560245, 0.07622579599997338, 0.0636966398604868, 0.050787240068351155, 0.03820899725214706, 0.026531676970810682, 0.01615182629108528, 0.007288268299606014, 0.0],
        },
        "y180_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0012240847586494005, 0.0015170644828794045, 0.0018120730575167433, 0.0020818270350890333, 0.0022940182396129984, 0.002414877522476003, 0.0024139421366688014, 0.002269318000214408, 0.001972449218661253, 0.0015313307451699284, 0.0009712873302740991, 0.0003328819176163112, -0.0003328819176163112, -0.0009712873302740991, -0.0015313307451699284, -0.001972449218661253, -0.002269318000214408, -0.0024139421366688014, -0.002414877522476003, -0.0022940182396129984, -0.0020818270350890333, -0.0018120730575167433, -0.0015170644828794045, -0.0012240847586494005],
        },
        "y180_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.014576536599212028, 0.03230365258217056, 0.053063353941621365, 0.07641799450429412, 0.10157448013670231, 0.1273932797209736, 0.15245159199994676, 0.1751608520512049, 0.1939276249581603, 0.207336361916705] + [0.2143253064271754] * 2 + [0.207336361916705, 0.1939276249581603, 0.1751608520512049, 0.15245159199994676, 0.1273932797209736, 0.10157448013670231, 0.07641799450429412, 0.053063353941621365, 0.03230365258217056, 0.014576536599212028, 0.0],
        },
        "minus_y90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0006120423793247003, -0.0007585322414397022, -0.0009060365287583717, -0.0010409135175445167, -0.0011470091198064992, -0.0012074387612380016, -0.0012069710683344007, -0.001134659000107204, -0.0009862246093306265, -0.0007656653725849642, -0.00048564366513704956, -0.0001664409588081556, 0.0001664409588081556, 0.00048564366513704956, 0.0007656653725849642, 0.0009862246093306265, 0.001134659000107204, 0.0012069710683344007, 0.0012074387612380016, 0.0011470091198064992, 0.0010409135175445167, 0.0009060365287583717, 0.0007585322414397022, 0.0006120423793247003],
        },
        "minus_y90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, -0.007288268299606014, -0.01615182629108528, -0.026531676970810682, -0.03820899725214706, -0.050787240068351155, -0.0636966398604868, -0.07622579599997338, -0.08758042602560245, -0.09696381247908015, -0.1036681809583525] + [-0.1071626532135877] * 2 + [-0.1036681809583525, -0.09696381247908015, -0.08758042602560245, -0.07622579599997338, -0.0636966398604868, -0.050787240068351155, -0.03820899725214706, -0.026531676970810682, -0.01615182629108528, -0.007288268299606014, 0.0],
        },
        "readout_wf_q5": {
            "type": "constant",
            "sample": 0.0188,
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
            "cosine": [(-0.984807753012208, 1800)],
            "sine": [(0.17364817766693072, 1800)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(-0.17364817766693072, 1800)],
            "sine": [(-0.984807753012208, 1800)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(0.17364817766693072, 1800)],
            "sine": [(0.984807753012208, 1800)],
        },
        "rotated_cosine_weights_q2": {
            "cosine": [(-0.8737722230354653, 1800)],
            "sine": [(-0.48633538042349034, 1800)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(0.48633538042349034, 1800)],
            "sine": [(-0.8737722230354653, 1800)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(-0.48633538042349034, 1800)],
            "sine": [(0.8737722230354653, 1800)],
        },
        "rotated_cosine_weights_q3": {
            "cosine": [(0.6600016679609366, 1800)],
            "sine": [(0.7512641335035113, 1800)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(-0.7512641335035113, 1800)],
            "sine": [(0.6600016679609366, 1800)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(0.7512641335035113, 1800)],
            "sine": [(-0.6600016679609366, 1800)],
        },
        "rotated_cosine_weights_q4": {
            "cosine": [(-0.02966624408511127, 1800)],
            "sine": [(0.999559860119384, 1800)],
        },
        "rotated_sine_weights_q4": {
            "cosine": [(-0.999559860119384, 1800)],
            "sine": [(-0.02966624408511127, 1800)],
        },
        "rotated_minus_sine_weights_q4": {
            "cosine": [(0.999559860119384, 1800)],
            "sine": [(0.02966624408511127, 1800)],
        },
        "rotated_cosine_weights_q5": {
            "cosine": [(-0.10626407133623386, 1800)],
            "sine": [(-0.9943379441332045, 1800)],
        },
        "rotated_sine_weights_q5": {
            "cosine": [(0.9943379441332045, 1800)],
            "sine": [(-0.10626407133623386, 1800)],
        },
        "rotated_minus_sine_weights_q5": {
            "cosine": [(-0.9943379441332045, 1800)],
            "sine": [(0.10626407133623386, 1800)],
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
}

loaded_config = {
    "version": 1,
    "controllers": {
        "con1": {
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
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                },
                "8": {
                    "offset": 0.0,
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
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
                },
                "4": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
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
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
                    },
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
            "intermediate_frequency": 33900000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q1",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "rr1_mixer_5ea",
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
            "intermediate_frequency": 133700000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q2",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "rr2_mixer_642",
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
            "intermediate_frequency": -22800000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q3",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "rr3_mixer_746",
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
            "intermediate_frequency": 156000000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q4",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "rr4_mixer_85f",
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
            "intermediate_frequency": 62500000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q5",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "rr5_mixer_6be",
                "lo_frequency": 5880000000.0,
            },
        },
        "q1_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": -118000000.0,
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
                "I": ('con2', 1),
                "Q": ('con2', 2),
                "mixer": "q1_xy_mixer_cd2",
                "lo_frequency": 5200000000.0,
            },
        },
        "q2_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": -164000000.0,
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
                "mixer": "q2_xy_mixer_bb4",
                "lo_frequency": 4600000000.0,
            },
        },
        "q3_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": -137000000.0,
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
                "mixer": "q3_xy_mixer_c2b",
                "lo_frequency": 4600000000.0,
            },
        },
        "q4_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": -180000000.0,
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
                "mixer": "q4_xy_mixer_9a4",
                "lo_frequency": 4600000000.0,
            },
        },
        "q00_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": -180000000.0,
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
                "mixer": "q00_xy_mixer_b32",
                "lo_frequency": 4600000000.0,
            },
        },
        "q5_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": -237000000.0,
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
                "I": ('con1', 3),
                "Q": ('con1', 4),
                "mixer": "q5_xy_mixer_6df",
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
        "c1_2": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "operations": {
                "const": "const_flux_pulse",
            },
            "singleInput": {
                "port": ('con2', 3),
            },
        },
        "c2_3": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "operations": {
                "const": "const_flux_pulse",
            },
            "singleInput": {
                "port": ('con2', 4),
            },
        },
        "c3_4": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "operations": {
                "const": "const_flux_pulse",
            },
            "singleInput": {
                "port": ('con2', 5),
            },
        },
        "c4_5": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "operations": {
                "const": "const_flux_pulse",
            },
            "singleInput": {
                "port": ('con2', 10),
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
            "samples": [0.0, 0.002818510006488263, 0.0062462140735056355, 0.010260296953555697, 0.014776135656103749, 0.019640377995182673, 0.024632684946047638, 0.029477944546864705, 0.03386899287708845, 0.037497724357144276, 0.04009042935498788] + [0.04144180729744212] * 2 + [0.04009042935498788, 0.037497724357144276, 0.03386899287708845, 0.029477944546864705, 0.024632684946047638, 0.019640377995182673, 0.014776135656103749, 0.010260296953555697, 0.0062462140735056355, 0.002818510006488263, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q1": {
            "samples": [-0.0017647859941029365, -0.0021871803668976255, -0.0026124997714417056, -0.003001409148925006, -0.0033073291950408493, -0.0034815742937947054, -0.0034802257305028518, -0.003271718395842828, -0.002843717096039479, -0.002207748305270042, -0.0014003231921690122, -0.00047992211466432776, 0.00047992211466432776, 0.0014003231921690122, 0.002207748305270042, 0.002843717096039479, 0.003271718395842828, 0.0034802257305028518, 0.0034815742937947054, 0.0033073291950408493, 0.003001409148925006, 0.0026124997714417056, 0.0021871803668976255, 0.0017647859941029365],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q1": {
            "samples": [0.0, 0.005637020012976526, 0.012492428147011271, 0.020520593907111393, 0.029552271312207497, 0.039280755990365346, 0.049265369892095276, 0.05895588909372941, 0.0677379857541769, 0.07499544871428855, 0.08018085870997577] + [0.08288361459488423] * 2 + [0.08018085870997577, 0.07499544871428855, 0.0677379857541769, 0.05895588909372941, 0.049265369892095276, 0.039280755990365346, 0.029552271312207497, 0.020520593907111393, 0.012492428147011271, 0.005637020012976526, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q1": {
            "samples": [-0.003529571988205873, -0.004374360733795251, -0.005224999542883411, -0.006002818297850012, -0.0066146583900816985, -0.006963148587589411, -0.0069604514610057035, -0.006543436791685656, -0.005687434192078958, -0.004415496610540084, -0.0028006463843380245, -0.0009598442293286555, 0.0009598442293286555, 0.0028006463843380245, 0.004415496610540084, 0.005687434192078958, 0.006543436791685656, 0.0069604514610057035, 0.006963148587589411, 0.0066146583900816985, 0.006002818297850012, 0.005224999542883411, 0.004374360733795251, 0.003529571988205873],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q1": {
            "samples": [0.0, -0.002818510006488263, -0.0062462140735056355, -0.010260296953555697, -0.014776135656103749, -0.019640377995182673, -0.024632684946047638, -0.029477944546864705, -0.03386899287708845, -0.037497724357144276, -0.04009042935498788] + [-0.04144180729744212] * 2 + [-0.04009042935498788, -0.037497724357144276, -0.03386899287708845, -0.029477944546864705, -0.024632684946047638, -0.019640377995182673, -0.014776135656103749, -0.010260296953555697, -0.0062462140735056355, -0.002818510006488263, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q1": {
            "samples": [0.0017647859941029365, 0.0021871803668976255, 0.0026124997714417056, 0.003001409148925006, 0.0033073291950408493, 0.0034815742937947054, 0.0034802257305028518, 0.003271718395842828, 0.002843717096039479, 0.002207748305270042, 0.0014003231921690122, 0.00047992211466432776, -0.00047992211466432776, -0.0014003231921690122, -0.002207748305270042, -0.002843717096039479, -0.003271718395842828, -0.0034802257305028518, -0.0034815742937947054, -0.0033073291950408493, -0.003001409148925006, -0.0026124997714417056, -0.0021871803668976255, -0.0017647859941029365],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q1": {
            "samples": [0.0017647859941029365, 0.0021871803668976255, 0.0026124997714417056, 0.003001409148925006, 0.0033073291950408493, 0.0034815742937947054, 0.0034802257305028518, 0.003271718395842828, 0.002843717096039479, 0.002207748305270042, 0.0014003231921690122, 0.00047992211466432776, -0.00047992211466432776, -0.0014003231921690122, -0.002207748305270042, -0.002843717096039479, -0.003271718395842828, -0.0034802257305028518, -0.0034815742937947054, -0.0033073291950408493, -0.003001409148925006, -0.0026124997714417056, -0.0021871803668976255, -0.0017647859941029365],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q1": {
            "samples": [0.0, 0.002818510006488263, 0.0062462140735056355, 0.010260296953555697, 0.014776135656103749, 0.019640377995182673, 0.024632684946047638, 0.029477944546864705, 0.03386899287708845, 0.037497724357144276, 0.04009042935498788] + [0.04144180729744212] * 2 + [0.04009042935498788, 0.037497724357144276, 0.03386899287708845, 0.029477944546864705, 0.024632684946047638, 0.019640377995182673, 0.014776135656103749, 0.010260296953555697, 0.0062462140735056355, 0.002818510006488263, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q1": {
            "samples": [0.003529571988205873, 0.004374360733795251, 0.005224999542883411, 0.006002818297850012, 0.0066146583900816985, 0.006963148587589411, 0.0069604514610057035, 0.006543436791685656, 0.005687434192078958, 0.004415496610540084, 0.0028006463843380245, 0.0009598442293286555, -0.0009598442293286555, -0.0028006463843380245, -0.004415496610540084, -0.005687434192078958, -0.006543436791685656, -0.0069604514610057035, -0.006963148587589411, -0.0066146583900816985, -0.006002818297850012, -0.005224999542883411, -0.004374360733795251, -0.003529571988205873],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q1": {
            "samples": [0.0, 0.005637020012976526, 0.012492428147011271, 0.020520593907111393, 0.029552271312207497, 0.039280755990365346, 0.049265369892095276, 0.05895588909372941, 0.0677379857541769, 0.07499544871428855, 0.08018085870997577] + [0.08288361459488423] * 2 + [0.08018085870997577, 0.07499544871428855, 0.0677379857541769, 0.05895588909372941, 0.049265369892095276, 0.039280755990365346, 0.029552271312207497, 0.020520593907111393, 0.012492428147011271, 0.005637020012976526, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q1": {
            "samples": [-0.0017647859941029365, -0.0021871803668976255, -0.0026124997714417056, -0.003001409148925006, -0.0033073291950408493, -0.0034815742937947054, -0.0034802257305028518, -0.003271718395842828, -0.002843717096039479, -0.002207748305270042, -0.0014003231921690122, -0.00047992211466432776, 0.00047992211466432776, 0.0014003231921690122, 0.002207748305270042, 0.002843717096039479, 0.003271718395842828, 0.0034802257305028518, 0.0034815742937947054, 0.0033073291950408493, 0.003001409148925006, 0.0026124997714417056, 0.0021871803668976255, 0.0017647859941029365],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q1": {
            "samples": [0.0, -0.002818510006488263, -0.0062462140735056355, -0.010260296953555697, -0.014776135656103749, -0.019640377995182673, -0.024632684946047638, -0.029477944546864705, -0.03386899287708845, -0.037497724357144276, -0.04009042935498788] + [-0.04144180729744212] * 2 + [-0.04009042935498788, -0.037497724357144276, -0.03386899287708845, -0.029477944546864705, -0.024632684946047638, -0.019640377995182673, -0.014776135656103749, -0.010260296953555697, -0.0062462140735056355, -0.002818510006488263, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q1": {
            "sample": 0.0065,
            "type": "constant",
        },
        "x90_I_wf_q2": {
            "samples": [0.0, 0.003852628076704988, 0.008537964973443802, 0.014024824473783162, 0.020197535209334032, 0.026846479709900825, 0.03367047603496476, 0.04029347298514784, 0.046295607461961874, 0.051255729210936955, 0.05479970388064235] + [0.056646905626016285] * 2 + [0.05479970388064235, 0.051255729210936955, 0.046295607461961874, 0.04029347298514784, 0.03367047603496476, 0.026846479709900825, 0.020197535209334032, 0.014024824473783162, 0.008537964973443802, 0.003852628076704988, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q2": {
            "samples": [-0.0016116979263006178, -0.0019974512907250082, -0.0023858759521908587, -0.0027410490096058527, -0.0030204317254627507, -0.003179561764610861, -0.00317833018374597, -0.002987910019480756, -0.0025970361063535918, -0.0020162350433918313, -0.0012788508025964184, -0.00043829080668983833, 0.00043829080668983833, 0.0012788508025964184, 0.0020162350433918313, 0.0025970361063535918, 0.002987910019480756, 0.00317833018374597, 0.003179561764610861, 0.0030204317254627507, 0.0027410490096058527, 0.0023858759521908587, 0.0019974512907250082, 0.0016116979263006178],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q2": {
            "samples": [0.0, 0.007504638764750569, 0.016631333634101877, 0.027319336130881628, 0.03934332685807018, 0.052294986257880316, 0.065587633856345, 0.07848874931872259, 0.09018046992323753, 0.09984242566205283, 0.10674583008055356] + [0.11034404448086606] * 2 + [0.10674583008055356, 0.09984242566205283, 0.09018046992323753, 0.07848874931872259, 0.065587633856345, 0.052294986257880316, 0.03934332685807018, 0.027319336130881628, 0.016631333634101877, 0.007504638764750569, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q2": {
            "samples": [-0.003139470121166824, -0.003890889566453162, -0.004647512503727403, -0.005339363739248481, -0.005883580912013875, -0.00619355463297802, -0.006191155603194567, -0.005820230998513521, -0.0050588370974721675, -0.003927478947936227, -0.0024911081776950775, -0.0008537585545842521, 0.0008537585545842521, 0.0024911081776950775, 0.003927478947936227, 0.0050588370974721675, 0.005820230998513521, 0.006191155603194567, 0.00619355463297802, 0.005883580912013875, 0.005339363739248481, 0.004647512503727403, 0.003890889566453162, 0.003139470121166824],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q2": {
            "samples": [0.0, -0.003852628076704988, -0.008537964973443802, -0.014024824473783162, -0.020197535209334032, -0.026846479709900825, -0.03367047603496476, -0.04029347298514784, -0.046295607461961874, -0.051255729210936955, -0.05479970388064235] + [-0.056646905626016285] * 2 + [-0.05479970388064235, -0.051255729210936955, -0.046295607461961874, -0.04029347298514784, -0.03367047603496476, -0.026846479709900825, -0.020197535209334032, -0.014024824473783162, -0.008537964973443802, -0.003852628076704988, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q2": {
            "samples": [0.0016116979263006178, 0.0019974512907250082, 0.0023858759521908587, 0.0027410490096058527, 0.0030204317254627507, 0.003179561764610861, 0.00317833018374597, 0.002987910019480756, 0.0025970361063535918, 0.0020162350433918313, 0.0012788508025964184, 0.00043829080668983833, -0.00043829080668983833, -0.0012788508025964184, -0.0020162350433918313, -0.0025970361063535918, -0.002987910019480756, -0.00317833018374597, -0.003179561764610861, -0.0030204317254627507, -0.0027410490096058527, -0.0023858759521908587, -0.0019974512907250082, -0.0016116979263006178],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q2": {
            "samples": [0.001569735060583412, 0.001945444783226581, 0.0023237562518637015, 0.0026696818696242404, 0.0029417904560069376, 0.00309677731648901, 0.0030955778015972833, 0.0029101154992567605, 0.0025294185487360838, 0.0019637394739681134, 0.0012455540888475388, 0.00042687927729212607, -0.00042687927729212607, -0.0012455540888475388, -0.0019637394739681134, -0.0025294185487360838, -0.0029101154992567605, -0.0030955778015972833, -0.00309677731648901, -0.0029417904560069376, -0.0026696818696242404, -0.0023237562518637015, -0.001945444783226581, -0.001569735060583412],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q2": {
            "samples": [0.0, 0.0037523193823752847, 0.008315666817050938, 0.013659668065440814, 0.01967166342903509, 0.026147493128940158, 0.0327938169281725, 0.03924437465936129, 0.045090234961618764, 0.049921212831026414, 0.05337291504027678] + [0.05517202224043303] * 2 + [0.05337291504027678, 0.049921212831026414, 0.045090234961618764, 0.03924437465936129, 0.0327938169281725, 0.026147493128940158, 0.01967166342903509, 0.013659668065440814, 0.008315666817050938, 0.0037523193823752847, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q2": {
            "samples": [0.003139470121166824, 0.003890889566453162, 0.004647512503727403, 0.005339363739248481, 0.005883580912013875, 0.00619355463297802, 0.006191155603194567, 0.005820230998513521, 0.0050588370974721675, 0.003927478947936227, 0.0024911081776950775, 0.0008537585545842521, -0.0008537585545842521, -0.0024911081776950775, -0.003927478947936227, -0.0050588370974721675, -0.005820230998513521, -0.006191155603194567, -0.00619355463297802, -0.005883580912013875, -0.005339363739248481, -0.004647512503727403, -0.003890889566453162, -0.003139470121166824],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q2": {
            "samples": [0.0, 0.007504638764750569, 0.016631333634101877, 0.027319336130881628, 0.03934332685807018, 0.052294986257880316, 0.065587633856345, 0.07848874931872259, 0.09018046992323753, 0.09984242566205283, 0.10674583008055356] + [0.11034404448086606] * 2 + [0.10674583008055356, 0.09984242566205283, 0.09018046992323753, 0.07848874931872259, 0.065587633856345, 0.052294986257880316, 0.03934332685807018, 0.027319336130881628, 0.016631333634101877, 0.007504638764750569, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q2": {
            "samples": [-0.001569735060583412, -0.001945444783226581, -0.0023237562518637015, -0.0026696818696242404, -0.0029417904560069376, -0.00309677731648901, -0.0030955778015972833, -0.0029101154992567605, -0.0025294185487360838, -0.0019637394739681134, -0.0012455540888475388, -0.00042687927729212607, 0.00042687927729212607, 0.0012455540888475388, 0.0019637394739681134, 0.0025294185487360838, 0.0029101154992567605, 0.0030955778015972833, 0.00309677731648901, 0.0029417904560069376, 0.0026696818696242404, 0.0023237562518637015, 0.001945444783226581, 0.001569735060583412],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q2": {
            "samples": [0.0, -0.0037523193823752847, -0.008315666817050938, -0.013659668065440814, -0.01967166342903509, -0.026147493128940158, -0.0327938169281725, -0.03924437465936129, -0.045090234961618764, -0.049921212831026414, -0.05337291504027678] + [-0.05517202224043303] * 2 + [-0.05337291504027678, -0.049921212831026414, -0.045090234961618764, -0.03924437465936129, -0.0327938169281725, -0.026147493128940158, -0.01967166342903509, -0.013659668065440814, -0.008315666817050938, -0.0037523193823752847, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q2": {
            "sample": 0.033,
            "type": "constant",
        },
        "x90_I_wf_q3": {
            "samples": [0.0, 0.00554591665923145, 0.012290530318372706, 0.020188947944976256, 0.029074658846555662, 0.038645915489510956, 0.04846916189383918, 0.05800306664372974, 0.06664323042885688, 0.07378340105830004, 0.07888500644799634] + [0.08154408142971438] * 2 + [0.07888500644799634, 0.07378340105830004, 0.06664323042885688, 0.05800306664372974, 0.04846916189383918, 0.038645915489510956, 0.029074658846555662, 0.020188947944976256, 0.012290530318372706, 0.00554591665923145, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q3": {
            "samples": [0.003042155140335954, 0.0037702826395002477, 0.004503452336643101, 0.005173858077502959, 0.00570120600746893, 0.006001571391500573, 0.005999246725074112, 0.005639819767894428, 0.0049020269938028155, 0.0038057378503047546, 0.0024138906425048012, 0.0008272943761824908, -0.0008272943761824908, -0.0024138906425048012, -0.0038057378503047546, -0.0049020269938028155, -0.005639819767894428, -0.005999246725074112, -0.006001571391500573, -0.00570120600746893, -0.005173858077502959, -0.004503452336643101, -0.0037702826395002477, -0.003042155140335954],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q3": {
            "samples": [0.0, 0.0110918333184629, 0.02458106063674541, 0.04037789588995251, 0.058149317693111324, 0.07729183097902191, 0.09693832378767836, 0.11600613328745948, 0.13328646085771376, 0.1475668021166001, 0.15777001289599268] + [0.16308816285942876] * 2 + [0.15777001289599268, 0.1475668021166001, 0.13328646085771376, 0.11600613328745948, 0.09693832378767836, 0.07729183097902191, 0.058149317693111324, 0.04037789588995251, 0.02458106063674541, 0.0110918333184629, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q3": {
            "samples": [0.006084310280671908, 0.007540565279000495, 0.009006904673286202, 0.010347716155005918, 0.01140241201493786, 0.012003142783001146, 0.011998493450148223, 0.011279639535788855, 0.009804053987605631, 0.007611475700609509, 0.0048277812850096025, 0.0016545887523649815, -0.0016545887523649815, -0.0048277812850096025, -0.007611475700609509, -0.009804053987605631, -0.011279639535788855, -0.011998493450148223, -0.012003142783001146, -0.01140241201493786, -0.010347716155005918, -0.009006904673286202, -0.007540565279000495, -0.006084310280671908],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q3": {
            "samples": [0.0, -0.00554591665923145, -0.012290530318372706, -0.020188947944976256, -0.029074658846555662, -0.038645915489510956, -0.04846916189383918, -0.05800306664372974, -0.06664323042885688, -0.07378340105830004, -0.07888500644799634] + [-0.08154408142971438] * 2 + [-0.07888500644799634, -0.07378340105830004, -0.06664323042885688, -0.05800306664372974, -0.04846916189383918, -0.038645915489510956, -0.029074658846555662, -0.020188947944976256, -0.012290530318372706, -0.00554591665923145, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q3": {
            "samples": [-0.003042155140335954, -0.0037702826395002477, -0.004503452336643101, -0.005173858077502959, -0.00570120600746893, -0.006001571391500573, -0.005999246725074112, -0.005639819767894428, -0.0049020269938028155, -0.0038057378503047546, -0.0024138906425048012, -0.0008272943761824908, 0.0008272943761824908, 0.0024138906425048012, 0.0038057378503047546, 0.0049020269938028155, 0.005639819767894428, 0.005999246725074112, 0.006001571391500573, 0.00570120600746893, 0.005173858077502959, 0.004503452336643101, 0.0037702826395002477, 0.003042155140335954],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q3": {
            "samples": [-0.003042155140335954, -0.0037702826395002477, -0.004503452336643101, -0.005173858077502959, -0.00570120600746893, -0.006001571391500573, -0.005999246725074112, -0.005639819767894428, -0.0049020269938028155, -0.0038057378503047546, -0.0024138906425048012, -0.0008272943761824908, 0.0008272943761824908, 0.0024138906425048012, 0.0038057378503047546, 0.0049020269938028155, 0.005639819767894428, 0.005999246725074112, 0.006001571391500573, 0.00570120600746893, 0.005173858077502959, 0.004503452336643101, 0.0037702826395002477, 0.003042155140335954],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q3": {
            "samples": [0.0, 0.00554591665923145, 0.012290530318372706, 0.020188947944976256, 0.029074658846555662, 0.038645915489510956, 0.04846916189383918, 0.05800306664372974, 0.06664323042885688, 0.07378340105830004, 0.07888500644799634] + [0.08154408142971438] * 2 + [0.07888500644799634, 0.07378340105830004, 0.06664323042885688, 0.05800306664372974, 0.04846916189383918, 0.038645915489510956, 0.029074658846555662, 0.020188947944976256, 0.012290530318372706, 0.00554591665923145, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q3": {
            "samples": [-0.006084310280671908, -0.007540565279000495, -0.009006904673286202, -0.010347716155005918, -0.01140241201493786, -0.012003142783001146, -0.011998493450148223, -0.011279639535788855, -0.009804053987605631, -0.007611475700609509, -0.0048277812850096025, -0.0016545887523649815, 0.0016545887523649815, 0.0048277812850096025, 0.007611475700609509, 0.009804053987605631, 0.011279639535788855, 0.011998493450148223, 0.012003142783001146, 0.01140241201493786, 0.010347716155005918, 0.009006904673286202, 0.007540565279000495, 0.006084310280671908],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q3": {
            "samples": [0.0, 0.0110918333184629, 0.02458106063674541, 0.04037789588995251, 0.058149317693111324, 0.07729183097902191, 0.09693832378767836, 0.11600613328745948, 0.13328646085771376, 0.1475668021166001, 0.15777001289599268] + [0.16308816285942876] * 2 + [0.15777001289599268, 0.1475668021166001, 0.13328646085771376, 0.11600613328745948, 0.09693832378767836, 0.07729183097902191, 0.058149317693111324, 0.04037789588995251, 0.02458106063674541, 0.0110918333184629, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q3": {
            "samples": [0.003042155140335954, 0.0037702826395002477, 0.004503452336643101, 0.005173858077502959, 0.00570120600746893, 0.006001571391500573, 0.005999246725074112, 0.005639819767894428, 0.0049020269938028155, 0.0038057378503047546, 0.0024138906425048012, 0.0008272943761824908, -0.0008272943761824908, -0.0024138906425048012, -0.0038057378503047546, -0.0049020269938028155, -0.005639819767894428, -0.005999246725074112, -0.006001571391500573, -0.00570120600746893, -0.005173858077502959, -0.004503452336643101, -0.0037702826395002477, -0.003042155140335954],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q3": {
            "samples": [0.0, -0.00554591665923145, -0.012290530318372706, -0.020188947944976256, -0.029074658846555662, -0.038645915489510956, -0.04846916189383918, -0.05800306664372974, -0.06664323042885688, -0.07378340105830004, -0.07888500644799634] + [-0.08154408142971438] * 2 + [-0.07888500644799634, -0.07378340105830004, -0.06664323042885688, -0.05800306664372974, -0.04846916189383918, -0.038645915489510956, -0.029074658846555662, -0.020188947944976256, -0.012290530318372706, -0.00554591665923145, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q3": {
            "sample": 0.0246,
            "type": "constant",
        },
        "x90_I_wf_q4": {
            "samples": [0.0, 0.004061810889195392, 0.009001543468572511, 0.014786318230693984, 0.021294183298987135, 0.028304139784886988, 0.03549865273270312, 0.042481252816531936, 0.0488092799945899, 0.05403871718151735, 0.05777511597679206] + [0.0597226136367057] * 2 + [0.05777511597679206, 0.05403871718151735, 0.0488092799945899, 0.042481252816531936, 0.03549865273270312, 0.028304139784886988, 0.021294183298987135, 0.014786318230693984, 0.009001543468572511, 0.004061810889195392, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q4": {
            "samples": [0.002564170188378035, 0.003177893927164464, 0.003795867631236719, 0.0043609388835333706, 0.004805429640428921, 0.005058601463635019, 0.005056642049971453, 0.004753688437816817, 0.004131818036980678, 0.0032077783973422525, 0.0020346189257238125, 0.0006973094660076023, -0.0006973094660076023, -0.0020346189257238125, -0.0032077783973422525, -0.004131818036980678, -0.004753688437816817, -0.005056642049971453, -0.005058601463635019, -0.004805429640428921, -0.0043609388835333706, -0.003795867631236719, -0.003177893927164464, -0.002564170188378035],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q4": {
            "samples": [0.0, 0.00802848304878475, 0.01779224614877363, 0.029226300413158643, 0.04208959853556825, 0.05594531913779306, 0.07016582984631749, 0.08396747840622067, 0.0964753130438277, 0.10681169968398671, 0.11419698058693514] + [0.11804636018059267] * 2 + [0.11419698058693514, 0.10681169968398671, 0.0964753130438277, 0.08396747840622067, 0.07016582984631749, 0.05594531913779306, 0.04208959853556825, 0.029226300413158643, 0.01779224614877363, 0.00802848304878475, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q4": {
            "samples": [0.005068280491923697, 0.006281352879560064, 0.007502825651947461, 0.008619732641016545, 0.009498302964556232, 0.009998716633850109, 0.009994843701354575, 0.009396032479930769, 0.008166857585320417, 0.006340421843819946, 0.004021581506751552, 0.0013782860355441512, -0.0013782860355441512, -0.004021581506751552, -0.006340421843819946, -0.008166857585320417, -0.009396032479930769, -0.009994843701354575, -0.009998716633850109, -0.009498302964556232, -0.008619732641016545, -0.007502825651947461, -0.006281352879560064, -0.005068280491923697],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q4": {
            "samples": [0.0, -0.004061810889195392, -0.009001543468572511, -0.014786318230693984, -0.021294183298987135, -0.028304139784886988, -0.03549865273270312, -0.042481252816531936, -0.0488092799945899, -0.05403871718151735, -0.05777511597679206] + [-0.0597226136367057] * 2 + [-0.05777511597679206, -0.05403871718151735, -0.0488092799945899, -0.042481252816531936, -0.03549865273270312, -0.028304139784886988, -0.021294183298987135, -0.014786318230693984, -0.009001543468572511, -0.004061810889195392, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q4": {
            "samples": [-0.002564170188378035, -0.003177893927164464, -0.003795867631236719, -0.0043609388835333706, -0.004805429640428921, -0.005058601463635019, -0.005056642049971453, -0.004753688437816817, -0.004131818036980678, -0.0032077783973422525, -0.0020346189257238125, -0.0006973094660076023, 0.0006973094660076023, 0.0020346189257238125, 0.0032077783973422525, 0.004131818036980678, 0.004753688437816817, 0.005056642049971453, 0.005058601463635019, 0.004805429640428921, 0.0043609388835333706, 0.003795867631236719, 0.003177893927164464, 0.002564170188378035],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q4": {
            "samples": [-0.0025341402459618484, -0.003140676439780032, -0.0037514128259737304, -0.004309866320508273, -0.004749151482278116, -0.0049993583169250545, -0.0049974218506772874, -0.0046980162399653845, -0.004083428792660208, -0.003170210921909973, -0.002010790753375776, -0.0006891430177720756, 0.0006891430177720756, 0.002010790753375776, 0.003170210921909973, 0.004083428792660208, 0.0046980162399653845, 0.0049974218506772874, 0.0049993583169250545, 0.004749151482278116, 0.004309866320508273, 0.0037514128259737304, 0.003140676439780032, 0.0025341402459618484],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q4": {
            "samples": [0.0, 0.004014241524392375, 0.008896123074386815, 0.014613150206579321, 0.021044799267784124, 0.02797265956889653, 0.035082914923158744, 0.04198373920311033, 0.04823765652191385, 0.053405849841993355, 0.05709849029346757] + [0.059023180090296334] * 2 + [0.05709849029346757, 0.053405849841993355, 0.04823765652191385, 0.04198373920311033, 0.035082914923158744, 0.02797265956889653, 0.021044799267784124, 0.014613150206579321, 0.008896123074386815, 0.004014241524392375, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q4": {
            "samples": [-0.005068280491923697, -0.006281352879560064, -0.007502825651947461, -0.008619732641016545, -0.009498302964556232, -0.009998716633850109, -0.009994843701354575, -0.009396032479930769, -0.008166857585320417, -0.006340421843819946, -0.004021581506751552, -0.0013782860355441512, 0.0013782860355441512, 0.004021581506751552, 0.006340421843819946, 0.008166857585320417, 0.009396032479930769, 0.009994843701354575, 0.009998716633850109, 0.009498302964556232, 0.008619732641016545, 0.007502825651947461, 0.006281352879560064, 0.005068280491923697],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q4": {
            "samples": [0.0, 0.00802848304878475, 0.01779224614877363, 0.029226300413158643, 0.04208959853556825, 0.05594531913779306, 0.07016582984631749, 0.08396747840622067, 0.0964753130438277, 0.10681169968398671, 0.11419698058693514] + [0.11804636018059267] * 2 + [0.11419698058693514, 0.10681169968398671, 0.0964753130438277, 0.08396747840622067, 0.07016582984631749, 0.05594531913779306, 0.04208959853556825, 0.029226300413158643, 0.01779224614877363, 0.00802848304878475, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q4": {
            "samples": [0.0025341402459618484, 0.003140676439780032, 0.0037514128259737304, 0.004309866320508273, 0.004749151482278116, 0.0049993583169250545, 0.0049974218506772874, 0.0046980162399653845, 0.004083428792660208, 0.003170210921909973, 0.002010790753375776, 0.0006891430177720756, -0.0006891430177720756, -0.002010790753375776, -0.003170210921909973, -0.004083428792660208, -0.0046980162399653845, -0.0049974218506772874, -0.0049993583169250545, -0.004749151482278116, -0.004309866320508273, -0.0037514128259737304, -0.003140676439780032, -0.0025341402459618484],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q4": {
            "samples": [0.0, -0.004014241524392375, -0.008896123074386815, -0.014613150206579321, -0.021044799267784124, -0.02797265956889653, -0.035082914923158744, -0.04198373920311033, -0.04823765652191385, -0.053405849841993355, -0.05709849029346757] + [-0.059023180090296334] * 2 + [-0.05709849029346757, -0.053405849841993355, -0.04823765652191385, -0.04198373920311033, -0.035082914923158744, -0.02797265956889653, -0.021044799267784124, -0.014613150206579321, -0.008896123074386815, -0.004014241524392375, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q4": {
            "sample": 0.0155,
            "type": "constant",
        },
        "x90_I_wf_q5": {
            "samples": [0.0, 0.0073220605394498685, 0.0162267146411717, 0.02665469176044265, 0.03838615423186577, 0.05102271638821851, 0.06399197093817635, 0.0765792188261966, 0.08798649488040082, 0.09741338764189966, 0.10414884109476791] + [0.10765951555877512] * 2 + [0.10414884109476791, 0.09741338764189966, 0.08798649488040082, 0.0765792188261966, 0.06399197093817635, 0.05102271638821851, 0.03838615423186577, 0.02665469176044265, 0.0162267146411717, 0.0073220605394498685, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q5": {
            "samples": [-0.0006148801292574054, -0.0007620491953138363, -0.0009102373899819839, -0.001045739739329392, -0.0011523272565279047, -0.0012130370815164589, -0.0012125672201429114, -0.0011399198751870477, -0.000990797264612844, -0.000769215399401612, -0.0004878953642425624, -0.00016721266651274031, 0.00016721266651274031, 0.0004878953642425624, 0.000769215399401612, 0.000990797264612844, 0.0011399198751870477, 0.0012125672201429114, 0.0012130370815164589, 0.0011523272565279047, 0.001045739739329392, 0.0009102373899819839, 0.0007620491953138363, 0.0006148801292574054],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q5": {
            "samples": [0.0, 0.014576536599212028, 0.03230365258217056, 0.053063353941621365, 0.07641799450429412, 0.10157448013670231, 0.1273932797209736, 0.15245159199994676, 0.1751608520512049, 0.1939276249581603, 0.207336361916705] + [0.2143253064271754] * 2 + [0.207336361916705, 0.1939276249581603, 0.1751608520512049, 0.15245159199994676, 0.1273932797209736, 0.10157448013670231, 0.07641799450429412, 0.053063353941621365, 0.03230365258217056, 0.014576536599212028, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q5": {
            "samples": [-0.0012240847586494005, -0.0015170644828794045, -0.0018120730575167433, -0.0020818270350890333, -0.0022940182396129984, -0.002414877522476003, -0.0024139421366688014, -0.002269318000214408, -0.001972449218661253, -0.0015313307451699284, -0.0009712873302740991, -0.0003328819176163112, 0.0003328819176163112, 0.0009712873302740991, 0.0015313307451699284, 0.001972449218661253, 0.002269318000214408, 0.0024139421366688014, 0.002414877522476003, 0.0022940182396129984, 0.0020818270350890333, 0.0018120730575167433, 0.0015170644828794045, 0.0012240847586494005],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q5": {
            "samples": [0.0, -0.0073220605394498685, -0.0162267146411717, -0.02665469176044265, -0.03838615423186577, -0.05102271638821851, -0.06399197093817635, -0.0765792188261966, -0.08798649488040082, -0.09741338764189966, -0.10414884109476791] + [-0.10765951555877512] * 2 + [-0.10414884109476791, -0.09741338764189966, -0.08798649488040082, -0.0765792188261966, -0.06399197093817635, -0.05102271638821851, -0.03838615423186577, -0.02665469176044265, -0.0162267146411717, -0.0073220605394498685, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q5": {
            "samples": [0.0006148801292574054, 0.0007620491953138363, 0.0009102373899819839, 0.001045739739329392, 0.0011523272565279047, 0.0012130370815164589, 0.0012125672201429114, 0.0011399198751870477, 0.000990797264612844, 0.000769215399401612, 0.0004878953642425624, 0.00016721266651274031, -0.00016721266651274031, -0.0004878953642425624, -0.000769215399401612, -0.000990797264612844, -0.0011399198751870477, -0.0012125672201429114, -0.0012130370815164589, -0.0011523272565279047, -0.001045739739329392, -0.0009102373899819839, -0.0007620491953138363, -0.0006148801292574054],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q5": {
            "samples": [0.0006120423793247003, 0.0007585322414397022, 0.0009060365287583717, 0.0010409135175445167, 0.0011470091198064992, 0.0012074387612380016, 0.0012069710683344007, 0.001134659000107204, 0.0009862246093306265, 0.0007656653725849642, 0.00048564366513704956, 0.0001664409588081556, -0.0001664409588081556, -0.00048564366513704956, -0.0007656653725849642, -0.0009862246093306265, -0.001134659000107204, -0.0012069710683344007, -0.0012074387612380016, -0.0011470091198064992, -0.0010409135175445167, -0.0009060365287583717, -0.0007585322414397022, -0.0006120423793247003],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q5": {
            "samples": [0.0, 0.007288268299606014, 0.01615182629108528, 0.026531676970810682, 0.03820899725214706, 0.050787240068351155, 0.0636966398604868, 0.07622579599997338, 0.08758042602560245, 0.09696381247908015, 0.1036681809583525] + [0.1071626532135877] * 2 + [0.1036681809583525, 0.09696381247908015, 0.08758042602560245, 0.07622579599997338, 0.0636966398604868, 0.050787240068351155, 0.03820899725214706, 0.026531676970810682, 0.01615182629108528, 0.007288268299606014, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q5": {
            "samples": [0.0012240847586494005, 0.0015170644828794045, 0.0018120730575167433, 0.0020818270350890333, 0.0022940182396129984, 0.002414877522476003, 0.0024139421366688014, 0.002269318000214408, 0.001972449218661253, 0.0015313307451699284, 0.0009712873302740991, 0.0003328819176163112, -0.0003328819176163112, -0.0009712873302740991, -0.0015313307451699284, -0.001972449218661253, -0.002269318000214408, -0.0024139421366688014, -0.002414877522476003, -0.0022940182396129984, -0.0020818270350890333, -0.0018120730575167433, -0.0015170644828794045, -0.0012240847586494005],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q5": {
            "samples": [0.0, 0.014576536599212028, 0.03230365258217056, 0.053063353941621365, 0.07641799450429412, 0.10157448013670231, 0.1273932797209736, 0.15245159199994676, 0.1751608520512049, 0.1939276249581603, 0.207336361916705] + [0.2143253064271754] * 2 + [0.207336361916705, 0.1939276249581603, 0.1751608520512049, 0.15245159199994676, 0.1273932797209736, 0.10157448013670231, 0.07641799450429412, 0.053063353941621365, 0.03230365258217056, 0.014576536599212028, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q5": {
            "samples": [-0.0006120423793247003, -0.0007585322414397022, -0.0009060365287583717, -0.0010409135175445167, -0.0011470091198064992, -0.0012074387612380016, -0.0012069710683344007, -0.001134659000107204, -0.0009862246093306265, -0.0007656653725849642, -0.00048564366513704956, -0.0001664409588081556, 0.0001664409588081556, 0.00048564366513704956, 0.0007656653725849642, 0.0009862246093306265, 0.001134659000107204, 0.0012069710683344007, 0.0012074387612380016, 0.0011470091198064992, 0.0010409135175445167, 0.0009060365287583717, 0.0007585322414397022, 0.0006120423793247003],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q5": {
            "samples": [0.0, -0.007288268299606014, -0.01615182629108528, -0.026531676970810682, -0.03820899725214706, -0.050787240068351155, -0.0636966398604868, -0.07622579599997338, -0.08758042602560245, -0.09696381247908015, -0.1036681809583525] + [-0.1071626532135877] * 2 + [-0.1036681809583525, -0.09696381247908015, -0.08758042602560245, -0.07622579599997338, -0.0636966398604868, -0.050787240068351155, -0.03820899725214706, -0.026531676970810682, -0.01615182629108528, -0.007288268299606014, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q5": {
            "sample": 0.0188,
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
            "cosine": [(-0.984807753012208, 1800)],
            "sine": [(0.17364817766693072, 1800)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(-0.17364817766693072, 1800)],
            "sine": [(-0.984807753012208, 1800)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(0.17364817766693072, 1800)],
            "sine": [(0.984807753012208, 1800)],
        },
        "rotated_cosine_weights_q2": {
            "cosine": [(-0.8737722230354653, 1800)],
            "sine": [(-0.48633538042349034, 1800)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(0.48633538042349034, 1800)],
            "sine": [(-0.8737722230354653, 1800)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(-0.48633538042349034, 1800)],
            "sine": [(0.8737722230354653, 1800)],
        },
        "rotated_cosine_weights_q3": {
            "cosine": [(0.6600016679609366, 1800)],
            "sine": [(0.7512641335035113, 1800)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(-0.7512641335035113, 1800)],
            "sine": [(0.6600016679609366, 1800)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(0.7512641335035113, 1800)],
            "sine": [(-0.6600016679609366, 1800)],
        },
        "rotated_cosine_weights_q4": {
            "cosine": [(-0.02966624408511127, 1800)],
            "sine": [(0.999559860119384, 1800)],
        },
        "rotated_sine_weights_q4": {
            "cosine": [(-0.999559860119384, 1800)],
            "sine": [(-0.02966624408511127, 1800)],
        },
        "rotated_minus_sine_weights_q4": {
            "cosine": [(0.999559860119384, 1800)],
            "sine": [(0.02966624408511127, 1800)],
        },
        "rotated_cosine_weights_q5": {
            "cosine": [(-0.10626407133623386, 1800)],
            "sine": [(-0.9943379441332045, 1800)],
        },
        "rotated_sine_weights_q5": {
            "cosine": [(0.9943379441332045, 1800)],
            "sine": [(-0.10626407133623386, 1800)],
        },
        "rotated_minus_sine_weights_q5": {
            "cosine": [(-0.9943379441332045, 1800)],
            "sine": [(0.10626407133623386, 1800)],
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
        "rr1_mixer_5ea": [{'intermediate_frequency': 33900000.0, 'lo_frequency': 5880000000.0, 'correction': [1, 0.0, 0.0, 1]}],
        "rr2_mixer_642": [{'intermediate_frequency': 133700000.0, 'lo_frequency': 5880000000.0, 'correction': [1, 0.0, 0.0, 1]}],
        "rr3_mixer_746": [{'intermediate_frequency': -22800000.0, 'lo_frequency': 5880000000.0, 'correction': [1, 0.0, 0.0, 1]}],
        "rr4_mixer_85f": [{'intermediate_frequency': 156000000.0, 'lo_frequency': 5880000000.0, 'correction': [1, 0.0, 0.0, 1]}],
        "rr5_mixer_6be": [{'intermediate_frequency': 62500000.0, 'lo_frequency': 5880000000.0, 'correction': [1, 0.0, 0.0, 1]}],
        "q1_xy_mixer_cd2": [{'intermediate_frequency': -118000000.0, 'lo_frequency': 5200000000.0, 'correction': [1, 0.0, 0.0, 1]}],
        "q2_xy_mixer_bb4": [{'intermediate_frequency': -164000000.0, 'lo_frequency': 4600000000.0, 'correction': [1, 0.0, 0.0, 1]}],
        "q3_xy_mixer_c2b": [{'intermediate_frequency': -137000000.0, 'lo_frequency': 4600000000.0, 'correction': [1, 0.0, 0.0, 1]}],
        "q4_xy_mixer_9a4": [{'intermediate_frequency': -180000000.0, 'lo_frequency': 4600000000.0, 'correction': [1, 0.0, 0.0, 1]}],
        "q00_xy_mixer_b32": [{'intermediate_frequency': -180000000.0, 'lo_frequency': 4600000000.0, 'correction': [1, 0.0, 0.0, 1]}],
        "q5_xy_mixer_6df": [{'intermediate_frequency': -237000000.0, 'lo_frequency': 4600000000.0, 'correction': [1, 0.0, 0.0, 1]}],
    },
}



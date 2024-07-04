
# Single QUA script generated at 2024-06-13 08:57:49.332057
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
            update_frequency("rr3", (v12+-23300000), "Hz", False)
            update_frequency("rr4", (v12+157500000), "Hz", False)
            update_frequency("rr5", (v12+62300000), "Hz", False)
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
                    "offset": -0.03,
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
                    "offset": -0.003,
                    "filter": {
                        "feedforward": [],
                        "feedback": [],
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
            "intermediate_frequency": -23300000,
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
            "intermediate_frequency": 157500000,
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
            "intermediate_frequency": 62300000,
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
            "intermediate_frequency": -116000000,
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
            "intermediate_frequency": -64000000,
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
            "intermediate_frequency": -58000000,
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
            "intermediate_frequency": -85000000,
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
            "intermediate_frequency": -85000000,
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
            "intermediate_frequency": -138450000,
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
                    "gain": 0,
                },
                "2": {
                    "LO_frequency": 4500000000,
                    "LO_source": "internal",
                    "output_mode": "always_on",
                    "gain": 8,
                },
                "3": {
                    "LO_frequency": 4500000000,
                    "LO_source": "internal",
                    "output_mode": "always_on",
                    "gain": 8,
                },
                "4": {
                    "LO_frequency": 4500000000,
                    "LO_source": "internal",
                    "output_mode": "always_on",
                    "gain": 8,
                },
                "5": {
                    "LO_frequency": 4500000000,
                    "LO_source": "internal",
                    "output_mode": "always_on",
                    "gain": 8,
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
                    "gain": 8,
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
            "length": 40,
            "waveforms": {
                "I": "x90_I_wf_q1",
                "Q": "x90_Q_wf_q1",
            },
        },
        "x180_pulse_q1": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "x180_I_wf_q1",
                "Q": "x180_Q_wf_q1",
            },
        },
        "-x90_pulse_q1": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "minus_x90_I_wf_q1",
                "Q": "minus_x90_Q_wf_q1",
            },
        },
        "y90_pulse_q1": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "y90_I_wf_q1",
                "Q": "y90_Q_wf_q1",
            },
        },
        "y180_pulse_q1": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "y180_I_wf_q1",
                "Q": "y180_Q_wf_q1",
            },
        },
        "-y90_pulse_q1": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "minus_y90_I_wf_q1",
                "Q": "minus_y90_Q_wf_q1",
            },
        },
        "readout_pulse_q1": {
            "operation": "measurement",
            "length": 600,
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
            "length": 40,
            "waveforms": {
                "I": "x90_I_wf_q2",
                "Q": "x90_Q_wf_q2",
            },
        },
        "x180_pulse_q2": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "x180_I_wf_q2",
                "Q": "x180_Q_wf_q2",
            },
        },
        "-x90_pulse_q2": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "minus_x90_I_wf_q2",
                "Q": "minus_x90_Q_wf_q2",
            },
        },
        "y90_pulse_q2": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "y90_I_wf_q2",
                "Q": "y90_Q_wf_q2",
            },
        },
        "y180_pulse_q2": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "y180_I_wf_q2",
                "Q": "y180_Q_wf_q2",
            },
        },
        "-y90_pulse_q2": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "minus_y90_I_wf_q2",
                "Q": "minus_y90_Q_wf_q2",
            },
        },
        "readout_pulse_q2": {
            "operation": "measurement",
            "length": 600,
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
            "length": 40,
            "waveforms": {
                "I": "x90_I_wf_q3",
                "Q": "x90_Q_wf_q3",
            },
        },
        "x180_pulse_q3": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "x180_I_wf_q3",
                "Q": "x180_Q_wf_q3",
            },
        },
        "-x90_pulse_q3": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "minus_x90_I_wf_q3",
                "Q": "minus_x90_Q_wf_q3",
            },
        },
        "y90_pulse_q3": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "y90_I_wf_q3",
                "Q": "y90_Q_wf_q3",
            },
        },
        "y180_pulse_q3": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "y180_I_wf_q3",
                "Q": "y180_Q_wf_q3",
            },
        },
        "-y90_pulse_q3": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "minus_y90_I_wf_q3",
                "Q": "minus_y90_Q_wf_q3",
            },
        },
        "readout_pulse_q3": {
            "operation": "measurement",
            "length": 600,
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
            "length": 40,
            "waveforms": {
                "I": "x90_I_wf_q4",
                "Q": "x90_Q_wf_q4",
            },
        },
        "x180_pulse_q4": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "x180_I_wf_q4",
                "Q": "x180_Q_wf_q4",
            },
        },
        "-x90_pulse_q4": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "minus_x90_I_wf_q4",
                "Q": "minus_x90_Q_wf_q4",
            },
        },
        "y90_pulse_q4": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "y90_I_wf_q4",
                "Q": "y90_Q_wf_q4",
            },
        },
        "y180_pulse_q4": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "y180_I_wf_q4",
                "Q": "y180_Q_wf_q4",
            },
        },
        "-y90_pulse_q4": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "minus_y90_I_wf_q4",
                "Q": "minus_y90_Q_wf_q4",
            },
        },
        "readout_pulse_q4": {
            "operation": "measurement",
            "length": 600,
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
            "length": 40,
            "waveforms": {
                "I": "x90_I_wf_q5",
                "Q": "x90_Q_wf_q5",
            },
        },
        "x180_pulse_q5": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "x180_I_wf_q5",
                "Q": "x180_Q_wf_q5",
            },
        },
        "-x90_pulse_q5": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "minus_x90_I_wf_q5",
                "Q": "minus_x90_Q_wf_q5",
            },
        },
        "y90_pulse_q5": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "y90_I_wf_q5",
                "Q": "y90_Q_wf_q5",
            },
        },
        "y180_pulse_q5": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "y180_I_wf_q5",
                "Q": "y180_Q_wf_q5",
            },
        },
        "-y90_pulse_q5": {
            "operation": "control",
            "length": 40,
            "waveforms": {
                "I": "minus_y90_I_wf_q5",
                "Q": "minus_y90_Q_wf_q5",
            },
        },
        "readout_pulse_q5": {
            "operation": "measurement",
            "length": 600,
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
            "samples": [0.0, 0.00037509691642171163, 0.0008026006989536316, 0.001283500513975867, 0.0018172341492822906, 0.0024014258993920617, 0.003031675294130842, 0.003701419038254355, 0.00440188678434094, 0.005122167581056582, 0.0058493980694559015, 0.006569076002947401, 0.007265493920863071, 0.007922278481009626, 0.00852301186022549, 0.009051903631473335, 0.009494475457367089, 0.009838217510711114, 0.01007317523232978] + [0.010192428068089955] * 2 + [0.01007317523232978, 0.009838217510711114, 0.009494475457367089, 0.009051903631473335, 0.00852301186022549, 0.007922278481009626, 0.007265493920863071, 0.006569076002947401, 0.0058493980694559015, 0.005122167581056582, 0.00440188678434094, 0.003701419038254355, 0.003031675294130842, 0.0024014258993920617, 0.0018172341492822906, 0.001283500513975867, 0.0008026006989536316, 0.00037509691642171163, 0.0],
        },
        "x90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.0002448609334099765, -0.0002809134731460448, -0.0003181353260942, -0.0003555394970875079, -0.00039194283066283934, -0.00042599372431684684, -0.0004562156664862241, -0.0004810660647332144, -0.0004990084355173089, -0.000508594593233965, -0.0005085521484343401, -0.0004978715582409541, -0.0004758863121225932, -0.0004423397013519283, -0.0003974320822859854, -0.0003418436134471042, -0.0002767290679724698, -0.00020368337340640174, -0.0001246788302942287, -4.1977291123514775e-05, 4.1977291123514775e-05, 0.0001246788302942287, 0.00020368337340640174, 0.0002767290679724698, 0.0003418436134471042, 0.0003974320822859854, 0.0004423397013519283, 0.0004758863121225932, 0.0004978715582409541, 0.0005085521484343401, 0.000508594593233965, 0.0004990084355173089, 0.0004810660647332144, 0.0004562156664862241, 0.00042599372431684684, 0.00039194283066283934, 0.0003555394970875079, 0.0003181353260942, 0.0002809134731460448, 0.0002448609334099765],
        },
        "x180_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007501938328434233, 0.0016052013979072632, 0.002567001027951734, 0.003634468298564581, 0.004802851798784123, 0.006063350588261684, 0.00740283807650871, 0.00880377356868188, 0.010244335162113163, 0.011698796138911803, 0.013138152005894802, 0.014530987841726142, 0.01584455696201925, 0.01704602372045098, 0.01810380726294667, 0.018988950914734178, 0.019676435021422228, 0.02014635046465956] + [0.02038485613617991] * 2 + [0.02014635046465956, 0.019676435021422228, 0.018988950914734178, 0.01810380726294667, 0.01704602372045098, 0.01584455696201925, 0.014530987841726142, 0.013138152005894802, 0.011698796138911803, 0.010244335162113163, 0.00880377356868188, 0.00740283807650871, 0.006063350588261684, 0.004802851798784123, 0.003634468298564581, 0.002567001027951734, 0.0016052013979072632, 0.0007501938328434233, 0.0],
        },
        "x180_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.000489721866819953, -0.0005618269462920896, -0.0006362706521884, -0.0007110789941750158, -0.0007838856613256787, -0.0008519874486336937, -0.0009124313329724482, -0.0009621321294664288, -0.0009980168710346177, -0.00101718918646793, -0.0010171042968686803, -0.0009957431164819082, -0.0009517726242451864, -0.0008846794027038566, -0.0007948641645719708, -0.0006836872268942084, -0.0005534581359449396, -0.0004073667468128035, -0.0002493576605884574, -8.395458224702955e-05, 8.395458224702955e-05, 0.0002493576605884574, 0.0004073667468128035, 0.0005534581359449396, 0.0006836872268942084, 0.0007948641645719708, 0.0008846794027038566, 0.0009517726242451864, 0.0009957431164819082, 0.0010171042968686803, 0.00101718918646793, 0.0009980168710346177, 0.0009621321294664288, 0.0009124313329724482, 0.0008519874486336937, 0.0007838856613256787, 0.0007110789941750158, 0.0006362706521884, 0.0005618269462920896, 0.000489721866819953],
        },
        "minus_x90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, -0.00037509691642171163, -0.0008026006989536316, -0.001283500513975867, -0.0018172341492822906, -0.0024014258993920617, -0.003031675294130842, -0.003701419038254355, -0.00440188678434094, -0.005122167581056582, -0.0058493980694559015, -0.006569076002947401, -0.007265493920863071, -0.007922278481009626, -0.00852301186022549, -0.009051903631473335, -0.009494475457367089, -0.009838217510711114, -0.01007317523232978] + [-0.010192428068089955] * 2 + [-0.01007317523232978, -0.009838217510711114, -0.009494475457367089, -0.009051903631473335, -0.00852301186022549, -0.007922278481009626, -0.007265493920863071, -0.006569076002947401, -0.0058493980694559015, -0.005122167581056582, -0.00440188678434094, -0.003701419038254355, -0.003031675294130842, -0.0024014258993920617, -0.0018172341492822906, -0.001283500513975867, -0.0008026006989536316, -0.00037509691642171163, 0.0],
        },
        "minus_x90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0002448609334099765, 0.0002809134731460448, 0.0003181353260942, 0.0003555394970875079, 0.00039194283066283934, 0.00042599372431684684, 0.0004562156664862241, 0.0004810660647332144, 0.0004990084355173089, 0.000508594593233965, 0.0005085521484343401, 0.0004978715582409541, 0.0004758863121225932, 0.0004423397013519283, 0.0003974320822859854, 0.0003418436134471042, 0.0002767290679724698, 0.00020368337340640174, 0.0001246788302942287, 4.1977291123514775e-05, -4.1977291123514775e-05, -0.0001246788302942287, -0.00020368337340640174, -0.0002767290679724698, -0.0003418436134471042, -0.0003974320822859854, -0.0004423397013519283, -0.0004758863121225932, -0.0004978715582409541, -0.0005085521484343401, -0.000508594593233965, -0.0004990084355173089, -0.0004810660647332144, -0.0004562156664862241, -0.00042599372431684684, -0.00039194283066283934, -0.0003555394970875079, -0.0003181353260942, -0.0002809134731460448, -0.0002448609334099765],
        },
        "y90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0002448609334099765, 0.0002809134731460448, 0.0003181353260942, 0.0003555394970875079, 0.00039194283066283934, 0.00042599372431684684, 0.0004562156664862241, 0.0004810660647332144, 0.0004990084355173089, 0.000508594593233965, 0.0005085521484343401, 0.0004978715582409541, 0.0004758863121225932, 0.0004423397013519283, 0.0003974320822859854, 0.0003418436134471042, 0.0002767290679724698, 0.00020368337340640174, 0.0001246788302942287, 4.1977291123514775e-05, -4.1977291123514775e-05, -0.0001246788302942287, -0.00020368337340640174, -0.0002767290679724698, -0.0003418436134471042, -0.0003974320822859854, -0.0004423397013519283, -0.0004758863121225932, -0.0004978715582409541, -0.0005085521484343401, -0.000508594593233965, -0.0004990084355173089, -0.0004810660647332144, -0.0004562156664862241, -0.00042599372431684684, -0.00039194283066283934, -0.0003555394970875079, -0.0003181353260942, -0.0002809134731460448, -0.0002448609334099765],
        },
        "y90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.00037509691642171163, 0.0008026006989536316, 0.001283500513975867, 0.0018172341492822906, 0.0024014258993920617, 0.003031675294130842, 0.003701419038254355, 0.00440188678434094, 0.005122167581056582, 0.0058493980694559015, 0.006569076002947401, 0.007265493920863071, 0.007922278481009626, 0.00852301186022549, 0.009051903631473335, 0.009494475457367089, 0.009838217510711114, 0.01007317523232978] + [0.010192428068089955] * 2 + [0.01007317523232978, 0.009838217510711114, 0.009494475457367089, 0.009051903631473335, 0.00852301186022549, 0.007922278481009626, 0.007265493920863071, 0.006569076002947401, 0.0058493980694559015, 0.005122167581056582, 0.00440188678434094, 0.003701419038254355, 0.003031675294130842, 0.0024014258993920617, 0.0018172341492822906, 0.001283500513975867, 0.0008026006989536316, 0.00037509691642171163, 0.0],
        },
        "y180_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.000489721866819953, 0.0005618269462920896, 0.0006362706521884, 0.0007110789941750158, 0.0007838856613256787, 0.0008519874486336937, 0.0009124313329724482, 0.0009621321294664288, 0.0009980168710346177, 0.00101718918646793, 0.0010171042968686803, 0.0009957431164819082, 0.0009517726242451864, 0.0008846794027038566, 0.0007948641645719708, 0.0006836872268942084, 0.0005534581359449396, 0.0004073667468128035, 0.0002493576605884574, 8.395458224702955e-05, -8.395458224702955e-05, -0.0002493576605884574, -0.0004073667468128035, -0.0005534581359449396, -0.0006836872268942084, -0.0007948641645719708, -0.0008846794027038566, -0.0009517726242451864, -0.0009957431164819082, -0.0010171042968686803, -0.00101718918646793, -0.0009980168710346177, -0.0009621321294664288, -0.0009124313329724482, -0.0008519874486336937, -0.0007838856613256787, -0.0007110789941750158, -0.0006362706521884, -0.0005618269462920896, -0.000489721866819953],
        },
        "y180_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007501938328434233, 0.0016052013979072632, 0.002567001027951734, 0.003634468298564581, 0.004802851798784123, 0.006063350588261684, 0.00740283807650871, 0.00880377356868188, 0.010244335162113163, 0.011698796138911803, 0.013138152005894802, 0.014530987841726142, 0.01584455696201925, 0.01704602372045098, 0.01810380726294667, 0.018988950914734178, 0.019676435021422228, 0.02014635046465956] + [0.02038485613617991] * 2 + [0.02014635046465956, 0.019676435021422228, 0.018988950914734178, 0.01810380726294667, 0.01704602372045098, 0.01584455696201925, 0.014530987841726142, 0.013138152005894802, 0.011698796138911803, 0.010244335162113163, 0.00880377356868188, 0.00740283807650871, 0.006063350588261684, 0.004802851798784123, 0.003634468298564581, 0.002567001027951734, 0.0016052013979072632, 0.0007501938328434233, 0.0],
        },
        "minus_y90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.0002448609334099765, -0.0002809134731460448, -0.0003181353260942, -0.0003555394970875079, -0.00039194283066283934, -0.00042599372431684684, -0.0004562156664862241, -0.0004810660647332144, -0.0004990084355173089, -0.000508594593233965, -0.0005085521484343401, -0.0004978715582409541, -0.0004758863121225932, -0.0004423397013519283, -0.0003974320822859854, -0.0003418436134471042, -0.0002767290679724698, -0.00020368337340640174, -0.0001246788302942287, -4.1977291123514775e-05, 4.1977291123514775e-05, 0.0001246788302942287, 0.00020368337340640174, 0.0002767290679724698, 0.0003418436134471042, 0.0003974320822859854, 0.0004423397013519283, 0.0004758863121225932, 0.0004978715582409541, 0.0005085521484343401, 0.000508594593233965, 0.0004990084355173089, 0.0004810660647332144, 0.0004562156664862241, 0.00042599372431684684, 0.00039194283066283934, 0.0003555394970875079, 0.0003181353260942, 0.0002809134731460448, 0.0002448609334099765],
        },
        "minus_y90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, -0.00037509691642171163, -0.0008026006989536316, -0.001283500513975867, -0.0018172341492822906, -0.0024014258993920617, -0.003031675294130842, -0.003701419038254355, -0.00440188678434094, -0.005122167581056582, -0.0058493980694559015, -0.006569076002947401, -0.007265493920863071, -0.007922278481009626, -0.00852301186022549, -0.009051903631473335, -0.009494475457367089, -0.009838217510711114, -0.01007317523232978] + [-0.010192428068089955] * 2 + [-0.01007317523232978, -0.009838217510711114, -0.009494475457367089, -0.009051903631473335, -0.00852301186022549, -0.007922278481009626, -0.007265493920863071, -0.006569076002947401, -0.0058493980694559015, -0.005122167581056582, -0.00440188678434094, -0.003701419038254355, -0.003031675294130842, -0.0024014258993920617, -0.0018172341492822906, -0.001283500513975867, -0.0008026006989536316, -0.00037509691642171163, 0.0],
        },
        "readout_wf_q1": {
            "type": "constant",
            "sample": 0.0072000000000000015,
        },
        "x90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.00024850170712938384, 0.0005317229630567809, 0.000850319090509012, 0.0012039176238995174, 0.001590944658347241, 0.0020084848823616833, 0.0024521901128435105, 0.002916249994625872, 0.003393436022449986, 0.0038752262210145355, 0.004352012851952654, 0.004813389722571785, 0.005248509493668878, 0.0056464953573993875, 0.005996886155851085, 0.006290089990505696, 0.006517819100846113, 0.006673478591418479] + [0.0067524835951095945] * 2 + [0.006673478591418479, 0.006517819100846113, 0.006290089990505696, 0.005996886155851085, 0.0056464953573993875, 0.005248509493668878, 0.004813389722571785, 0.004352012851952654, 0.0038752262210145355, 0.003393436022449986, 0.002916249994625872, 0.0024521901128435105, 0.0020084848823616833, 0.001590944658347241, 0.0012039176238995174, 0.000850319090509012, 0.0005317229630567809, 0.00024850170712938384, 0.0],
        },
        "x90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.00010838257818769472, -0.00012434048193490877, -0.00014081595775403325, -0.00015737213284808325, -0.00017348530816182377, -0.0001885572250757286, -0.00020193433658364, -0.00021293384636044148, -0.00022087566205679748, -0.00022511877456060173, -0.00022509998725651884, -0.00022037244707440572, -0.00021064113704787174, -0.00019579243042019533, -0.00017591501074831778, -0.0001513099359968597, -0.00012248834237724954, -9.015619125649105e-05, -5.5186480278948396e-05, -1.8580371208846324e-05, 1.8580371208846324e-05, 5.5186480278948396e-05, 9.015619125649105e-05, 0.00012248834237724954, 0.0001513099359968597, 0.00017591501074831778, 0.00019579243042019533, 0.00021064113704787174, 0.00022037244707440572, 0.00022509998725651884, 0.00022511877456060173, 0.00022087566205679748, 0.00021293384636044148, 0.00020193433658364, 0.0001885572250757286, 0.00017348530816182377, 0.00015737213284808325, 0.00014081595775403325, 0.00012434048193490877, 0.00010838257818769472],
        },
        "x180_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0004970034142587677, 0.0010634459261135618, 0.001700638181018024, 0.002407835247799035, 0.003181889316694482, 0.004016969764723367, 0.004904380225687021, 0.005832499989251744, 0.006786872044899972, 0.007750452442029071, 0.008704025703905308, 0.00962677944514357, 0.010497018987337755, 0.011292990714798775, 0.01199377231170217, 0.012580179981011392, 0.013035638201692226, 0.013346957182836959] + [0.013504967190219189] * 2 + [0.013346957182836959, 0.013035638201692226, 0.012580179981011392, 0.01199377231170217, 0.011292990714798775, 0.010497018987337755, 0.00962677944514357, 0.008704025703905308, 0.007750452442029071, 0.006786872044899972, 0.005832499989251744, 0.004904380225687021, 0.004016969764723367, 0.003181889316694482, 0.002407835247799035, 0.001700638181018024, 0.0010634459261135618, 0.0004970034142587677, 0.0],
        },
        "x180_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.00021676515637538945, -0.00024868096386981755, -0.0002816319155080665, -0.0003147442656961665, -0.00034697061632364755, -0.0003771144501514572, -0.00040386867316728, -0.00042586769272088295, -0.00044175132411359495, -0.00045023754912120346, -0.0004501999745130377, -0.00044074489414881144, -0.0004212822740957435, -0.00039158486084039067, -0.00035183002149663555, -0.0003026198719937194, -0.0002449766847544991, -0.0001803123825129821, -0.00011037296055789679, -3.716074241769265e-05, 3.716074241769265e-05, 0.00011037296055789679, 0.0001803123825129821, 0.0002449766847544991, 0.0003026198719937194, 0.00035183002149663555, 0.00039158486084039067, 0.0004212822740957435, 0.00044074489414881144, 0.0004501999745130377, 0.00045023754912120346, 0.00044175132411359495, 0.00042586769272088295, 0.00040386867316728, 0.0003771144501514572, 0.00034697061632364755, 0.0003147442656961665, 0.0002816319155080665, 0.00024868096386981755, 0.00021676515637538945],
        },
        "minus_x90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, -0.00024850170712938384, -0.0005317229630567809, -0.000850319090509012, -0.0012039176238995174, -0.001590944658347241, -0.0020084848823616833, -0.0024521901128435105, -0.002916249994625872, -0.003393436022449986, -0.0038752262210145355, -0.004352012851952654, -0.004813389722571785, -0.005248509493668878, -0.0056464953573993875, -0.005996886155851085, -0.006290089990505696, -0.006517819100846113, -0.006673478591418479] + [-0.0067524835951095945] * 2 + [-0.006673478591418479, -0.006517819100846113, -0.006290089990505696, -0.005996886155851085, -0.0056464953573993875, -0.005248509493668878, -0.004813389722571785, -0.004352012851952654, -0.0038752262210145355, -0.003393436022449986, -0.002916249994625872, -0.0024521901128435105, -0.0020084848823616833, -0.001590944658347241, -0.0012039176238995174, -0.000850319090509012, -0.0005317229630567809, -0.00024850170712938384, 0.0],
        },
        "minus_x90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.00010838257818769472, 0.00012434048193490877, 0.00014081595775403325, 0.00015737213284808325, 0.00017348530816182377, 0.0001885572250757286, 0.00020193433658364, 0.00021293384636044148, 0.00022087566205679748, 0.00022511877456060173, 0.00022509998725651884, 0.00022037244707440572, 0.00021064113704787174, 0.00019579243042019533, 0.00017591501074831778, 0.0001513099359968597, 0.00012248834237724954, 9.015619125649105e-05, 5.5186480278948396e-05, 1.8580371208846324e-05, -1.8580371208846324e-05, -5.5186480278948396e-05, -9.015619125649105e-05, -0.00012248834237724954, -0.0001513099359968597, -0.00017591501074831778, -0.00019579243042019533, -0.00021064113704787174, -0.00022037244707440572, -0.00022509998725651884, -0.00022511877456060173, -0.00022087566205679748, -0.00021293384636044148, -0.00020193433658364, -0.0001885572250757286, -0.00017348530816182377, -0.00015737213284808325, -0.00014081595775403325, -0.00012434048193490877, -0.00010838257818769472],
        },
        "y90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.00010838257818769472, 0.00012434048193490877, 0.00014081595775403325, 0.00015737213284808325, 0.00017348530816182377, 0.0001885572250757286, 0.00020193433658364, 0.00021293384636044148, 0.00022087566205679748, 0.00022511877456060173, 0.00022509998725651884, 0.00022037244707440572, 0.00021064113704787174, 0.00019579243042019533, 0.00017591501074831778, 0.0001513099359968597, 0.00012248834237724954, 9.015619125649105e-05, 5.5186480278948396e-05, 1.8580371208846324e-05, -1.8580371208846324e-05, -5.5186480278948396e-05, -9.015619125649105e-05, -0.00012248834237724954, -0.0001513099359968597, -0.00017591501074831778, -0.00019579243042019533, -0.00021064113704787174, -0.00022037244707440572, -0.00022509998725651884, -0.00022511877456060173, -0.00022087566205679748, -0.00021293384636044148, -0.00020193433658364, -0.0001885572250757286, -0.00017348530816182377, -0.00015737213284808325, -0.00014081595775403325, -0.00012434048193490877, -0.00010838257818769472],
        },
        "y90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.00024850170712938384, 0.0005317229630567809, 0.000850319090509012, 0.0012039176238995174, 0.001590944658347241, 0.0020084848823616833, 0.0024521901128435105, 0.002916249994625872, 0.003393436022449986, 0.0038752262210145355, 0.004352012851952654, 0.004813389722571785, 0.005248509493668878, 0.0056464953573993875, 0.005996886155851085, 0.006290089990505696, 0.006517819100846113, 0.006673478591418479] + [0.0067524835951095945] * 2 + [0.006673478591418479, 0.006517819100846113, 0.006290089990505696, 0.005996886155851085, 0.0056464953573993875, 0.005248509493668878, 0.004813389722571785, 0.004352012851952654, 0.0038752262210145355, 0.003393436022449986, 0.002916249994625872, 0.0024521901128435105, 0.0020084848823616833, 0.001590944658347241, 0.0012039176238995174, 0.000850319090509012, 0.0005317229630567809, 0.00024850170712938384, 0.0],
        },
        "y180_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.00021676515637538945, 0.00024868096386981755, 0.0002816319155080665, 0.0003147442656961665, 0.00034697061632364755, 0.0003771144501514572, 0.00040386867316728, 0.00042586769272088295, 0.00044175132411359495, 0.00045023754912120346, 0.0004501999745130377, 0.00044074489414881144, 0.0004212822740957435, 0.00039158486084039067, 0.00035183002149663555, 0.0003026198719937194, 0.0002449766847544991, 0.0001803123825129821, 0.00011037296055789679, 3.716074241769265e-05, -3.716074241769265e-05, -0.00011037296055789679, -0.0001803123825129821, -0.0002449766847544991, -0.0003026198719937194, -0.00035183002149663555, -0.00039158486084039067, -0.0004212822740957435, -0.00044074489414881144, -0.0004501999745130377, -0.00045023754912120346, -0.00044175132411359495, -0.00042586769272088295, -0.00040386867316728, -0.0003771144501514572, -0.00034697061632364755, -0.0003147442656961665, -0.0002816319155080665, -0.00024868096386981755, -0.00021676515637538945],
        },
        "y180_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0004970034142587677, 0.0010634459261135618, 0.001700638181018024, 0.002407835247799035, 0.003181889316694482, 0.004016969764723367, 0.004904380225687021, 0.005832499989251744, 0.006786872044899972, 0.007750452442029071, 0.008704025703905308, 0.00962677944514357, 0.010497018987337755, 0.011292990714798775, 0.01199377231170217, 0.012580179981011392, 0.013035638201692226, 0.013346957182836959] + [0.013504967190219189] * 2 + [0.013346957182836959, 0.013035638201692226, 0.012580179981011392, 0.01199377231170217, 0.011292990714798775, 0.010497018987337755, 0.00962677944514357, 0.008704025703905308, 0.007750452442029071, 0.006786872044899972, 0.005832499989251744, 0.004904380225687021, 0.004016969764723367, 0.003181889316694482, 0.002407835247799035, 0.001700638181018024, 0.0010634459261135618, 0.0004970034142587677, 0.0],
        },
        "minus_y90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.00010838257818769472, -0.00012434048193490877, -0.00014081595775403325, -0.00015737213284808325, -0.00017348530816182377, -0.0001885572250757286, -0.00020193433658364, -0.00021293384636044148, -0.00022087566205679748, -0.00022511877456060173, -0.00022509998725651884, -0.00022037244707440572, -0.00021064113704787174, -0.00019579243042019533, -0.00017591501074831778, -0.0001513099359968597, -0.00012248834237724954, -9.015619125649105e-05, -5.5186480278948396e-05, -1.8580371208846324e-05, 1.8580371208846324e-05, 5.5186480278948396e-05, 9.015619125649105e-05, 0.00012248834237724954, 0.0001513099359968597, 0.00017591501074831778, 0.00019579243042019533, 0.00021064113704787174, 0.00022037244707440572, 0.00022509998725651884, 0.00022511877456060173, 0.00022087566205679748, 0.00021293384636044148, 0.00020193433658364, 0.0001885572250757286, 0.00017348530816182377, 0.00015737213284808325, 0.00014081595775403325, 0.00012434048193490877, 0.00010838257818769472],
        },
        "minus_y90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, -0.00024850170712938384, -0.0005317229630567809, -0.000850319090509012, -0.0012039176238995174, -0.001590944658347241, -0.0020084848823616833, -0.0024521901128435105, -0.002916249994625872, -0.003393436022449986, -0.0038752262210145355, -0.004352012851952654, -0.004813389722571785, -0.005248509493668878, -0.0056464953573993875, -0.005996886155851085, -0.006290089990505696, -0.006517819100846113, -0.006673478591418479] + [-0.0067524835951095945] * 2 + [-0.006673478591418479, -0.006517819100846113, -0.006290089990505696, -0.005996886155851085, -0.0056464953573993875, -0.005248509493668878, -0.004813389722571785, -0.004352012851952654, -0.0038752262210145355, -0.003393436022449986, -0.002916249994625872, -0.0024521901128435105, -0.0020084848823616833, -0.001590944658347241, -0.0012039176238995174, -0.000850319090509012, -0.0005317229630567809, -0.00024850170712938384, 0.0],
        },
        "readout_wf_q2": {
            "type": "constant",
            "sample": 0.014400000000000003,
        },
        "x90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.00026881945676889333, 0.000575197167583436, 0.000919842035016038, 0.001302351140318975, 0.0017210218945643107, 0.002172700627460437, 0.0026526836440822882, 0.003154685528777674, 0.003670886766423884, 0.0041920686164433965, 0.004707837802112305, 0.005206937309951868, 0.0056776329113902325, 0.006108158499828268, 0.006487197602555891, 0.006804374077779748, 0.007050722549342966, 0.007219108916503011] + [0.007304573448797801] * 2 + [0.007219108916503011, 0.007050722549342966, 0.006804374077779748, 0.006487197602555891, 0.006108158499828268, 0.0056776329113902325, 0.005206937309951868, 0.004707837802112305, 0.0041920686164433965, 0.003670886766423884, 0.003154685528777674, 0.0026526836440822882, 0.002172700627460437, 0.0017210218945643107, 0.001302351140318975, 0.000919842035016038, 0.000575197167583436, 0.00026881945676889333, 0.0],
        },
        "x90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.00015373482487367302, 0.00017637024819494088, 0.00019973981950535195, 0.0002232238583723165, 0.0002460795260122466, 0.0002674582249324461, 0.00028643293405426545, 0.00030203514372217335, 0.00031330017972402865, 0.00031931880530573396, 0.0003192921565310755, 0.00031258639648980963, 0.00029878305957223045, 0.00027772097236986536, 0.00024952592771144673, 0.00021462496003591948, 0.00017374308841244113, 0.0001278816808554905, 7.82790373041872e-05, 2.635525156942737e-05, -2.635525156942737e-05, -7.82790373041872e-05, -0.0001278816808554905, -0.00017374308841244113, -0.00021462496003591948, -0.00024952592771144673, -0.00027772097236986536, -0.00029878305957223045, -0.00031258639648980963, -0.0003192921565310755, -0.00031931880530573396, -0.00031330017972402865, -0.00030203514372217335, -0.00028643293405426545, -0.0002674582249324461, -0.0002460795260122466, -0.0002232238583723165, -0.00019973981950535195, -0.00017637024819494088, -0.00015373482487367302],
        },
        "x180_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0005376389135377867, 0.001150394335166872, 0.001839684070032076, 0.00260470228063795, 0.0034420437891286215, 0.004345401254920874, 0.0053053672881645765, 0.006309371057555348, 0.007341773532847768, 0.008384137232886793, 0.00941567560422461, 0.010413874619903736, 0.011355265822780465, 0.012216316999656536, 0.012974395205111781, 0.013608748155559496, 0.014101445098685932, 0.014438217833006022] + [0.014609146897595602] * 2 + [0.014438217833006022, 0.014101445098685932, 0.013608748155559496, 0.012974395205111781, 0.012216316999656536, 0.011355265822780465, 0.010413874619903736, 0.00941567560422461, 0.008384137232886793, 0.007341773532847768, 0.006309371057555348, 0.0053053672881645765, 0.004345401254920874, 0.0034420437891286215, 0.00260470228063795, 0.001839684070032076, 0.001150394335166872, 0.0005376389135377867, 0.0],
        },
        "x180_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.00030746964974734603, 0.00035274049638988177, 0.0003994796390107039, 0.000446447716744633, 0.0004921590520244932, 0.0005349164498648922, 0.0005728658681085309, 0.0006040702874443467, 0.0006266003594480573, 0.0006386376106114679, 0.000638584313062151, 0.0006251727929796193, 0.0005975661191444609, 0.0005554419447397307, 0.0004990518554228935, 0.00042924992007183896, 0.00034748617682488225, 0.000255763361710981, 0.0001565580746083744, 5.271050313885474e-05, -5.271050313885474e-05, -0.0001565580746083744, -0.000255763361710981, -0.00034748617682488225, -0.00042924992007183896, -0.0004990518554228935, -0.0005554419447397307, -0.0005975661191444609, -0.0006251727929796193, -0.000638584313062151, -0.0006386376106114679, -0.0006266003594480573, -0.0006040702874443467, -0.0005728658681085309, -0.0005349164498648922, -0.0004921590520244932, -0.000446447716744633, -0.0003994796390107039, -0.00035274049638988177, -0.00030746964974734603],
        },
        "minus_x90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, -0.00026881945676889333, -0.000575197167583436, -0.000919842035016038, -0.001302351140318975, -0.0017210218945643107, -0.002172700627460437, -0.0026526836440822882, -0.003154685528777674, -0.003670886766423884, -0.0041920686164433965, -0.004707837802112305, -0.005206937309951868, -0.0056776329113902325, -0.006108158499828268, -0.006487197602555891, -0.006804374077779748, -0.007050722549342966, -0.007219108916503011] + [-0.007304573448797801] * 2 + [-0.007219108916503011, -0.007050722549342966, -0.006804374077779748, -0.006487197602555891, -0.006108158499828268, -0.0056776329113902325, -0.005206937309951868, -0.004707837802112305, -0.0041920686164433965, -0.003670886766423884, -0.003154685528777674, -0.0026526836440822882, -0.002172700627460437, -0.0017210218945643107, -0.001302351140318975, -0.000919842035016038, -0.000575197167583436, -0.00026881945676889333, 0.0],
        },
        "minus_x90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.00015373482487367302, -0.00017637024819494088, -0.00019973981950535195, -0.0002232238583723165, -0.0002460795260122466, -0.0002674582249324461, -0.00028643293405426545, -0.00030203514372217335, -0.00031330017972402865, -0.00031931880530573396, -0.0003192921565310755, -0.00031258639648980963, -0.00029878305957223045, -0.00027772097236986536, -0.00024952592771144673, -0.00021462496003591948, -0.00017374308841244113, -0.0001278816808554905, -7.82790373041872e-05, -2.635525156942737e-05, 2.635525156942737e-05, 7.82790373041872e-05, 0.0001278816808554905, 0.00017374308841244113, 0.00021462496003591948, 0.00024952592771144673, 0.00027772097236986536, 0.00029878305957223045, 0.00031258639648980963, 0.0003192921565310755, 0.00031931880530573396, 0.00031330017972402865, 0.00030203514372217335, 0.00028643293405426545, 0.0002674582249324461, 0.0002460795260122466, 0.0002232238583723165, 0.00019973981950535195, 0.00017637024819494088, 0.00015373482487367302],
        },
        "y90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.00015373482487367302, -0.00017637024819494088, -0.00019973981950535195, -0.0002232238583723165, -0.0002460795260122466, -0.0002674582249324461, -0.00028643293405426545, -0.00030203514372217335, -0.00031330017972402865, -0.00031931880530573396, -0.0003192921565310755, -0.00031258639648980963, -0.00029878305957223045, -0.00027772097236986536, -0.00024952592771144673, -0.00021462496003591948, -0.00017374308841244113, -0.0001278816808554905, -7.82790373041872e-05, -2.635525156942737e-05, 2.635525156942737e-05, 7.82790373041872e-05, 0.0001278816808554905, 0.00017374308841244113, 0.00021462496003591948, 0.00024952592771144673, 0.00027772097236986536, 0.00029878305957223045, 0.00031258639648980963, 0.0003192921565310755, 0.00031931880530573396, 0.00031330017972402865, 0.00030203514372217335, 0.00028643293405426545, 0.0002674582249324461, 0.0002460795260122466, 0.0002232238583723165, 0.00019973981950535195, 0.00017637024819494088, 0.00015373482487367302],
        },
        "y90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.00026881945676889333, 0.000575197167583436, 0.000919842035016038, 0.001302351140318975, 0.0017210218945643107, 0.002172700627460437, 0.0026526836440822882, 0.003154685528777674, 0.003670886766423884, 0.0041920686164433965, 0.004707837802112305, 0.005206937309951868, 0.0056776329113902325, 0.006108158499828268, 0.006487197602555891, 0.006804374077779748, 0.007050722549342966, 0.007219108916503011] + [0.007304573448797801] * 2 + [0.007219108916503011, 0.007050722549342966, 0.006804374077779748, 0.006487197602555891, 0.006108158499828268, 0.0056776329113902325, 0.005206937309951868, 0.004707837802112305, 0.0041920686164433965, 0.003670886766423884, 0.003154685528777674, 0.0026526836440822882, 0.002172700627460437, 0.0017210218945643107, 0.001302351140318975, 0.000919842035016038, 0.000575197167583436, 0.00026881945676889333, 0.0],
        },
        "y180_I_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.00030746964974734603, -0.00035274049638988177, -0.0003994796390107039, -0.000446447716744633, -0.0004921590520244932, -0.0005349164498648922, -0.0005728658681085309, -0.0006040702874443467, -0.0006266003594480573, -0.0006386376106114679, -0.000638584313062151, -0.0006251727929796193, -0.0005975661191444609, -0.0005554419447397307, -0.0004990518554228935, -0.00042924992007183896, -0.00034748617682488225, -0.000255763361710981, -0.0001565580746083744, -5.271050313885474e-05, 5.271050313885474e-05, 0.0001565580746083744, 0.000255763361710981, 0.00034748617682488225, 0.00042924992007183896, 0.0004990518554228935, 0.0005554419447397307, 0.0005975661191444609, 0.0006251727929796193, 0.000638584313062151, 0.0006386376106114679, 0.0006266003594480573, 0.0006040702874443467, 0.0005728658681085309, 0.0005349164498648922, 0.0004921590520244932, 0.000446447716744633, 0.0003994796390107039, 0.00035274049638988177, 0.00030746964974734603],
        },
        "y180_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0005376389135377867, 0.001150394335166872, 0.001839684070032076, 0.00260470228063795, 0.0034420437891286215, 0.004345401254920874, 0.0053053672881645765, 0.006309371057555348, 0.007341773532847768, 0.008384137232886793, 0.00941567560422461, 0.010413874619903736, 0.011355265822780465, 0.012216316999656536, 0.012974395205111781, 0.013608748155559496, 0.014101445098685932, 0.014438217833006022] + [0.014609146897595602] * 2 + [0.014438217833006022, 0.014101445098685932, 0.013608748155559496, 0.012974395205111781, 0.012216316999656536, 0.011355265822780465, 0.010413874619903736, 0.00941567560422461, 0.008384137232886793, 0.007341773532847768, 0.006309371057555348, 0.0053053672881645765, 0.004345401254920874, 0.0034420437891286215, 0.00260470228063795, 0.001839684070032076, 0.001150394335166872, 0.0005376389135377867, 0.0],
        },
        "minus_y90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.00015373482487367302, 0.00017637024819494088, 0.00019973981950535195, 0.0002232238583723165, 0.0002460795260122466, 0.0002674582249324461, 0.00028643293405426545, 0.00030203514372217335, 0.00031330017972402865, 0.00031931880530573396, 0.0003192921565310755, 0.00031258639648980963, 0.00029878305957223045, 0.00027772097236986536, 0.00024952592771144673, 0.00021462496003591948, 0.00017374308841244113, 0.0001278816808554905, 7.82790373041872e-05, 2.635525156942737e-05, -2.635525156942737e-05, -7.82790373041872e-05, -0.0001278816808554905, -0.00017374308841244113, -0.00021462496003591948, -0.00024952592771144673, -0.00027772097236986536, -0.00029878305957223045, -0.00031258639648980963, -0.0003192921565310755, -0.00031931880530573396, -0.00031330017972402865, -0.00030203514372217335, -0.00028643293405426545, -0.0002674582249324461, -0.0002460795260122466, -0.0002232238583723165, -0.00019973981950535195, -0.00017637024819494088, -0.00015373482487367302],
        },
        "minus_y90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, -0.00026881945676889333, -0.000575197167583436, -0.000919842035016038, -0.001302351140318975, -0.0017210218945643107, -0.002172700627460437, -0.0026526836440822882, -0.003154685528777674, -0.003670886766423884, -0.0041920686164433965, -0.004707837802112305, -0.005206937309951868, -0.0056776329113902325, -0.006108158499828268, -0.006487197602555891, -0.006804374077779748, -0.007050722549342966, -0.007219108916503011] + [-0.007304573448797801] * 2 + [-0.007219108916503011, -0.007050722549342966, -0.006804374077779748, -0.006487197602555891, -0.006108158499828268, -0.0056776329113902325, -0.005206937309951868, -0.004707837802112305, -0.0041920686164433965, -0.003670886766423884, -0.003154685528777674, -0.0026526836440822882, -0.002172700627460437, -0.0017210218945643107, -0.001302351140318975, -0.000919842035016038, -0.000575197167583436, -0.00026881945676889333, 0.0],
        },
        "readout_wf_q3": {
            "type": "constant",
            "sample": 0.014400000000000003,
        },
        "x90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0003016404369557931, 0.0006454247287418786, 0.0010321483299889263, 0.001461359128381175, 0.0019311466607611165, 0.0024379722156968858, 0.002976557809929544, 0.0035398506224075064, 0.0041190764297663355, 0.004703890947520788, 0.005282631952370203, 0.005842668028027387, 0.006370832278478575, 0.0068539220375979995, 0.007279239170309808, 0.0076351406802993675, 0.007911566581530187, 0.008100511749331867] + [0.008196410904755673] * 2 + [0.008100511749331867, 0.007911566581530187, 0.0076351406802993675, 0.007279239170309808, 0.0068539220375979995, 0.006370832278478575, 0.005842668028027387, 0.005282631952370203, 0.004703890947520788, 0.0041190764297663355, 0.0035398506224075064, 0.002976557809929544, 0.0024379722156968858, 0.0019311466607611165, 0.001461359128381175, 0.0010321483299889263, 0.0006454247287418786, 0.0003016404369557931, 0.0],
        },
        "x90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.00019852730528736819, 0.00022775782998925512, 0.00025793640547980685, 0.00028826280001893186, 0.00031777773985658777, 0.00034538537846849474, 0.0003698885960944417, 0.00039003669620411765, 0.00040458393521291885, 0.0004123561593609051, 0.00041232174614694056, 0.0004036621826941565, 0.00038583707843119956, 0.00035863830014886154, 0.00032222829192143216, 0.00027715850978041434, 0.00022436521577443684, 0.000165141538468734, 0.00010108657130392946, 3.403416941183321e-05, -3.403416941183321e-05, -0.00010108657130392946, -0.000165141538468734, -0.00022436521577443684, -0.00027715850978041434, -0.00032222829192143216, -0.00035863830014886154, -0.00038583707843119956, -0.0004036621826941565, -0.00041232174614694056, -0.0004123561593609051, -0.00040458393521291885, -0.00039003669620411765, -0.0003698885960944417, -0.00034538537846849474, -0.00031777773985658777, -0.00028826280001893186, -0.00025793640547980685, -0.00022775782998925512, -0.00019852730528736819],
        },
        "x180_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0006032808739115862, 0.0012908494574837572, 0.0020642966599778525, 0.00292271825676235, 0.003862293321522233, 0.0048759444313937715, 0.005953115619859088, 0.007079701244815013, 0.008238152859532671, 0.009407781895041576, 0.010565263904740406, 0.011685336056054775, 0.01274166455695715, 0.013707844075195999, 0.014558478340619616, 0.015270281360598735, 0.015823133163060374, 0.016201023498663734] + [0.016392821809511345] * 2 + [0.016201023498663734, 0.015823133163060374, 0.015270281360598735, 0.014558478340619616, 0.013707844075195999, 0.01274166455695715, 0.011685336056054775, 0.010565263904740406, 0.009407781895041576, 0.008238152859532671, 0.007079701244815013, 0.005953115619859088, 0.0048759444313937715, 0.003862293321522233, 0.00292271825676235, 0.0020642966599778525, 0.0012908494574837572, 0.0006032808739115862, 0.0],
        },
        "x180_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.00039705461057473637, 0.00045551565997851024, 0.0005158728109596137, 0.0005765256000378637, 0.0006355554797131755, 0.0006907707569369895, 0.0007397771921888834, 0.0007800733924082353, 0.0008091678704258377, 0.0008247123187218102, 0.0008246434922938811, 0.000807324365388313, 0.0007716741568623991, 0.0007172766002977231, 0.0006444565838428643, 0.0005543170195608287, 0.00044873043154887367, 0.000330283076937468, 0.00020217314260785892, 6.806833882366642e-05, -6.806833882366642e-05, -0.00020217314260785892, -0.000330283076937468, -0.00044873043154887367, -0.0005543170195608287, -0.0006444565838428643, -0.0007172766002977231, -0.0007716741568623991, -0.000807324365388313, -0.0008246434922938811, -0.0008247123187218102, -0.0008091678704258377, -0.0007800733924082353, -0.0007397771921888834, -0.0006907707569369895, -0.0006355554797131755, -0.0005765256000378637, -0.0005158728109596137, -0.00045551565997851024, -0.00039705461057473637],
        },
        "minus_x90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, -0.0003016404369557931, -0.0006454247287418786, -0.0010321483299889263, -0.001461359128381175, -0.0019311466607611165, -0.0024379722156968858, -0.002976557809929544, -0.0035398506224075064, -0.0041190764297663355, -0.004703890947520788, -0.005282631952370203, -0.005842668028027387, -0.006370832278478575, -0.0068539220375979995, -0.007279239170309808, -0.0076351406802993675, -0.007911566581530187, -0.008100511749331867] + [-0.008196410904755673] * 2 + [-0.008100511749331867, -0.007911566581530187, -0.0076351406802993675, -0.007279239170309808, -0.0068539220375979995, -0.006370832278478575, -0.005842668028027387, -0.005282631952370203, -0.004703890947520788, -0.0041190764297663355, -0.0035398506224075064, -0.002976557809929544, -0.0024379722156968858, -0.0019311466607611165, -0.001461359128381175, -0.0010321483299889263, -0.0006454247287418786, -0.0003016404369557931, 0.0],
        },
        "minus_x90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.00019852730528736819, -0.00022775782998925512, -0.00025793640547980685, -0.00028826280001893186, -0.00031777773985658777, -0.00034538537846849474, -0.0003698885960944417, -0.00039003669620411765, -0.00040458393521291885, -0.0004123561593609051, -0.00041232174614694056, -0.0004036621826941565, -0.00038583707843119956, -0.00035863830014886154, -0.00032222829192143216, -0.00027715850978041434, -0.00022436521577443684, -0.000165141538468734, -0.00010108657130392946, -3.403416941183321e-05, 3.403416941183321e-05, 0.00010108657130392946, 0.000165141538468734, 0.00022436521577443684, 0.00027715850978041434, 0.00032222829192143216, 0.00035863830014886154, 0.00038583707843119956, 0.0004036621826941565, 0.00041232174614694056, 0.0004123561593609051, 0.00040458393521291885, 0.00039003669620411765, 0.0003698885960944417, 0.00034538537846849474, 0.00031777773985658777, 0.00028826280001893186, 0.00025793640547980685, 0.00022775782998925512, 0.00019852730528736819],
        },
        "y90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.00019852730528736819, -0.00022775782998925512, -0.00025793640547980685, -0.00028826280001893186, -0.00031777773985658777, -0.00034538537846849474, -0.0003698885960944417, -0.00039003669620411765, -0.00040458393521291885, -0.0004123561593609051, -0.00041232174614694056, -0.0004036621826941565, -0.00038583707843119956, -0.00035863830014886154, -0.00032222829192143216, -0.00027715850978041434, -0.00022436521577443684, -0.000165141538468734, -0.00010108657130392946, -3.403416941183321e-05, 3.403416941183321e-05, 0.00010108657130392946, 0.000165141538468734, 0.00022436521577443684, 0.00027715850978041434, 0.00032222829192143216, 0.00035863830014886154, 0.00038583707843119956, 0.0004036621826941565, 0.00041232174614694056, 0.0004123561593609051, 0.00040458393521291885, 0.00039003669620411765, 0.0003698885960944417, 0.00034538537846849474, 0.00031777773985658777, 0.00028826280001893186, 0.00025793640547980685, 0.00022775782998925512, 0.00019852730528736819],
        },
        "y90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0003016404369557931, 0.0006454247287418786, 0.0010321483299889263, 0.001461359128381175, 0.0019311466607611165, 0.0024379722156968858, 0.002976557809929544, 0.0035398506224075064, 0.0041190764297663355, 0.004703890947520788, 0.005282631952370203, 0.005842668028027387, 0.006370832278478575, 0.0068539220375979995, 0.007279239170309808, 0.0076351406802993675, 0.007911566581530187, 0.008100511749331867] + [0.008196410904755673] * 2 + [0.008100511749331867, 0.007911566581530187, 0.0076351406802993675, 0.007279239170309808, 0.0068539220375979995, 0.006370832278478575, 0.005842668028027387, 0.005282631952370203, 0.004703890947520788, 0.0041190764297663355, 0.0035398506224075064, 0.002976557809929544, 0.0024379722156968858, 0.0019311466607611165, 0.001461359128381175, 0.0010321483299889263, 0.0006454247287418786, 0.0003016404369557931, 0.0],
        },
        "y180_I_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.00039705461057473637, -0.00045551565997851024, -0.0005158728109596137, -0.0005765256000378637, -0.0006355554797131755, -0.0006907707569369895, -0.0007397771921888834, -0.0007800733924082353, -0.0008091678704258377, -0.0008247123187218102, -0.0008246434922938811, -0.000807324365388313, -0.0007716741568623991, -0.0007172766002977231, -0.0006444565838428643, -0.0005543170195608287, -0.00044873043154887367, -0.000330283076937468, -0.00020217314260785892, -6.806833882366642e-05, 6.806833882366642e-05, 0.00020217314260785892, 0.000330283076937468, 0.00044873043154887367, 0.0005543170195608287, 0.0006444565838428643, 0.0007172766002977231, 0.0007716741568623991, 0.000807324365388313, 0.0008246434922938811, 0.0008247123187218102, 0.0008091678704258377, 0.0007800733924082353, 0.0007397771921888834, 0.0006907707569369895, 0.0006355554797131755, 0.0005765256000378637, 0.0005158728109596137, 0.00045551565997851024, 0.00039705461057473637],
        },
        "y180_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0006032808739115862, 0.0012908494574837572, 0.0020642966599778525, 0.00292271825676235, 0.003862293321522233, 0.0048759444313937715, 0.005953115619859088, 0.007079701244815013, 0.008238152859532671, 0.009407781895041576, 0.010565263904740406, 0.011685336056054775, 0.01274166455695715, 0.013707844075195999, 0.014558478340619616, 0.015270281360598735, 0.015823133163060374, 0.016201023498663734] + [0.016392821809511345] * 2 + [0.016201023498663734, 0.015823133163060374, 0.015270281360598735, 0.014558478340619616, 0.013707844075195999, 0.01274166455695715, 0.011685336056054775, 0.010565263904740406, 0.009407781895041576, 0.008238152859532671, 0.007079701244815013, 0.005953115619859088, 0.0048759444313937715, 0.003862293321522233, 0.00292271825676235, 0.0020642966599778525, 0.0012908494574837572, 0.0006032808739115862, 0.0],
        },
        "minus_y90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.00019852730528736819, 0.00022775782998925512, 0.00025793640547980685, 0.00028826280001893186, 0.00031777773985658777, 0.00034538537846849474, 0.0003698885960944417, 0.00039003669620411765, 0.00040458393521291885, 0.0004123561593609051, 0.00041232174614694056, 0.0004036621826941565, 0.00038583707843119956, 0.00035863830014886154, 0.00032222829192143216, 0.00027715850978041434, 0.00022436521577443684, 0.000165141538468734, 0.00010108657130392946, 3.403416941183321e-05, -3.403416941183321e-05, -0.00010108657130392946, -0.000165141538468734, -0.00022436521577443684, -0.00027715850978041434, -0.00032222829192143216, -0.00035863830014886154, -0.00038583707843119956, -0.0004036621826941565, -0.00041232174614694056, -0.0004123561593609051, -0.00040458393521291885, -0.00039003669620411765, -0.0003698885960944417, -0.00034538537846849474, -0.00031777773985658777, -0.00028826280001893186, -0.00025793640547980685, -0.00022775782998925512, -0.00019852730528736819],
        },
        "minus_y90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, -0.0003016404369557931, -0.0006454247287418786, -0.0010321483299889263, -0.001461359128381175, -0.0019311466607611165, -0.0024379722156968858, -0.002976557809929544, -0.0035398506224075064, -0.0041190764297663355, -0.004703890947520788, -0.005282631952370203, -0.005842668028027387, -0.006370832278478575, -0.0068539220375979995, -0.007279239170309808, -0.0076351406802993675, -0.007911566581530187, -0.008100511749331867] + [-0.008196410904755673] * 2 + [-0.008100511749331867, -0.007911566581530187, -0.0076351406802993675, -0.007279239170309808, -0.0068539220375979995, -0.006370832278478575, -0.005842668028027387, -0.005282631952370203, -0.004703890947520788, -0.0041190764297663355, -0.0035398506224075064, -0.002976557809929544, -0.0024379722156968858, -0.0019311466607611165, -0.001461359128381175, -0.0010321483299889263, -0.0006454247287418786, -0.0003016404369557931, 0.0],
        },
        "readout_wf_q4": {
            "type": "constant",
            "sample": 0.012960000000000003,
        },
        "x90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.00028036457944733903, 0.0005999004459244612, 0.0009593469475945237, 0.0013582838613582944, 0.0017949354763558167, 0.0022660126800516725, 0.00276660976559947, 0.0032901713744803033, 0.0038285421629731045, 0.004372107468671673, 0.004910027649636389, 0.005430562231841546, 0.00592147303097478, 0.006370488615614989, 0.006765806498879991, 0.007096604909663088, 0.007353533431346302, 0.007529151571420432] + [0.007618286591416743] * 2 + [0.007529151571420432, 0.007353533431346302, 0.007096604909663088, 0.006765806498879991, 0.006370488615614989, 0.00592147303097478, 0.005430562231841546, 0.004910027649636389, 0.004372107468671673, 0.0038285421629731045, 0.0032901713744803033, 0.00276660976559947, 0.0022660126800516725, 0.0017949354763558167, 0.0013582838613582944, 0.0009593469475945237, 0.0005999004459244612, 0.00028036457944733903, 0.0],
        },
        "x90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0001917669927905499, -0.0002200021507284308, -0.00024915307613966657, -0.0002784467870200398, -0.00030695667510253024, -0.00033362420996374374, -0.000357293036531548, -0.0003767550473762665, -0.0003908069193547087, -0.00039831448134974986, -0.00039828123998506877, -0.0003899165546345292, -0.0003726984362717311, -0.00034642583910314014, -0.00031125567560776345, -0.0002677206234677183, -0.0002167250628501037, -0.00015951808831089304, -9.764434047196768e-05, -3.287522746951145e-05, 3.287522746951145e-05, 9.764434047196768e-05, 0.00015951808831089304, 0.0002167250628501037, 0.0002677206234677183, 0.00031125567560776345, 0.00034642583910314014, 0.0003726984362717311, 0.0003899165546345292, 0.00039828123998506877, 0.00039831448134974986, 0.0003908069193547087, 0.0003767550473762665, 0.000357293036531548, 0.00033362420996374374, 0.00030695667510253024, 0.0002784467870200398, 0.00024915307613966657, 0.0002200021507284308, 0.0001917669927905499],
        },
        "x180_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.0005720227975431103, 0.0012239660659042876, 0.0019573382838131976, 0.0027712820776554926, 0.003662174496572894, 0.004623304823549534, 0.005644664033337892, 0.006712877346119934, 0.007811305561111289, 0.00892033205592025, 0.010017840904494788, 0.011079878229316185, 0.012081474683539681, 0.012997593086843876, 0.01380415303799684, 0.014479075072484813, 0.015003281703834448, 0.015361592229302915] + [0.015543452803837182] * 2 + [0.015361592229302915, 0.015003281703834448, 0.014479075072484813, 0.01380415303799684, 0.012997593086843876, 0.012081474683539681, 0.011079878229316185, 0.010017840904494788, 0.00892033205592025, 0.007811305561111289, 0.006712877346119934, 0.005644664033337892, 0.004623304823549534, 0.003662174496572894, 0.0027712820776554926, 0.0019573382838131976, 0.0012239660659042876, 0.0005720227975431103, 0.0],
        },
        "x180_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0003912587385635993, -0.0004488664223321257, -0.0005083425299687457, -0.0005681099602241697, -0.0006262781709544071, -0.0006806874616178699, -0.000728978541805555, -0.0007686865317062597, -0.0007973563128022555, -0.0008126738562080496, -0.0008126060344509055, -0.000795539717713551, -0.0007604099011948913, -0.0007068063947864671, -0.0006350493441906633, -0.0005462255620801584, -0.0004421802390073616, -0.0003254618800784182, -0.00019922198771017775, -6.707473399116837e-05, 6.707473399116837e-05, 0.00019922198771017775, 0.0003254618800784182, 0.0004421802390073616, 0.0005462255620801584, 0.0006350493441906633, 0.0007068063947864671, 0.0007604099011948913, 0.000795539717713551, 0.0008126060344509055, 0.0008126738562080496, 0.0007973563128022555, 0.0007686865317062597, 0.000728978541805555, 0.0006806874616178699, 0.0006262781709544071, 0.0005681099602241697, 0.0005083425299687457, 0.0004488664223321257, 0.0003912587385635993],
        },
        "minus_x90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, -0.00028036457944733903, -0.0005999004459244612, -0.0009593469475945237, -0.0013582838613582944, -0.0017949354763558167, -0.0022660126800516725, -0.00276660976559947, -0.0032901713744803033, -0.0038285421629731045, -0.004372107468671673, -0.004910027649636389, -0.005430562231841546, -0.00592147303097478, -0.006370488615614989, -0.006765806498879991, -0.007096604909663088, -0.007353533431346302, -0.007529151571420432] + [-0.007618286591416743] * 2 + [-0.007529151571420432, -0.007353533431346302, -0.007096604909663088, -0.006765806498879991, -0.006370488615614989, -0.00592147303097478, -0.005430562231841546, -0.004910027649636389, -0.004372107468671673, -0.0038285421629731045, -0.0032901713744803033, -0.00276660976559947, -0.0022660126800516725, -0.0017949354763558167, -0.0013582838613582944, -0.0009593469475945237, -0.0005999004459244612, -0.00028036457944733903, 0.0],
        },
        "minus_x90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0001917669927905499, 0.0002200021507284308, 0.00024915307613966657, 0.0002784467870200398, 0.00030695667510253024, 0.00033362420996374374, 0.000357293036531548, 0.0003767550473762665, 0.0003908069193547087, 0.00039831448134974986, 0.00039828123998506877, 0.0003899165546345292, 0.0003726984362717311, 0.00034642583910314014, 0.00031125567560776345, 0.0002677206234677183, 0.0002167250628501037, 0.00015951808831089304, 9.764434047196768e-05, 3.287522746951145e-05, -3.287522746951145e-05, -9.764434047196768e-05, -0.00015951808831089304, -0.0002167250628501037, -0.0002677206234677183, -0.00031125567560776345, -0.00034642583910314014, -0.0003726984362717311, -0.0003899165546345292, -0.00039828123998506877, -0.00039831448134974986, -0.0003908069193547087, -0.0003767550473762665, -0.000357293036531548, -0.00033362420996374374, -0.00030695667510253024, -0.0002784467870200398, -0.00024915307613966657, -0.0002200021507284308, -0.0001917669927905499],
        },
        "y90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.00019562936928179964, 0.00022443321116606284, 0.00025417126498437285, 0.00028405498011208486, 0.00031313908547720353, 0.00034034373080893496, 0.0003644892709027775, 0.00038434326585312986, 0.00039867815640112775, 0.0004063369281040248, 0.00040630301722545273, 0.0003977698588567755, 0.00038020495059744563, 0.00035340319739323356, 0.00031752467209533166, 0.0002731127810400792, 0.0002210901195036808, 0.0001627309400392091, 9.961099385508887e-05, 3.3537366995584185e-05, -3.3537366995584185e-05, -9.961099385508887e-05, -0.0001627309400392091, -0.0002210901195036808, -0.0002731127810400792, -0.00031752467209533166, -0.00035340319739323356, -0.00038020495059744563, -0.0003977698588567755, -0.00040630301722545273, -0.0004063369281040248, -0.00039867815640112775, -0.00038434326585312986, -0.0003644892709027775, -0.00034034373080893496, -0.00031313908547720353, -0.00028405498011208486, -0.00025417126498437285, -0.00022443321116606284, -0.00019562936928179964],
        },
        "y90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.00028601139877155513, 0.0006119830329521438, 0.0009786691419065988, 0.0013856410388277463, 0.001831087248286447, 0.002311652411774767, 0.002822332016668946, 0.003356438673059967, 0.0039056527805556443, 0.004460166027960125, 0.005008920452247394, 0.005539939114658093, 0.006040737341769841, 0.006498796543421938, 0.00690207651899842, 0.007239537536242406, 0.007501640851917224, 0.007680796114651458] + [0.007771726401918591] * 2 + [0.007680796114651458, 0.007501640851917224, 0.007239537536242406, 0.00690207651899842, 0.006498796543421938, 0.006040737341769841, 0.005539939114658093, 0.005008920452247394, 0.004460166027960125, 0.0039056527805556443, 0.003356438673059967, 0.002822332016668946, 0.002311652411774767, 0.001831087248286447, 0.0013856410388277463, 0.0009786691419065988, 0.0006119830329521438, 0.00028601139877155513, 0.0],
        },
        "y180_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0003912587385635993, 0.0004488664223321257, 0.0005083425299687457, 0.0005681099602241697, 0.0006262781709544071, 0.0006806874616178699, 0.000728978541805555, 0.0007686865317062597, 0.0007973563128022555, 0.0008126738562080496, 0.0008126060344509055, 0.000795539717713551, 0.0007604099011948913, 0.0007068063947864671, 0.0006350493441906633, 0.0005462255620801584, 0.0004421802390073616, 0.0003254618800784182, 0.00019922198771017775, 6.707473399116837e-05, -6.707473399116837e-05, -0.00019922198771017775, -0.0003254618800784182, -0.0004421802390073616, -0.0005462255620801584, -0.0006350493441906633, -0.0007068063947864671, -0.0007604099011948913, -0.000795539717713551, -0.0008126060344509055, -0.0008126738562080496, -0.0007973563128022555, -0.0007686865317062597, -0.000728978541805555, -0.0006806874616178699, -0.0006262781709544071, -0.0005681099602241697, -0.0005083425299687457, -0.0004488664223321257, -0.0003912587385635993],
        },
        "y180_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.0005720227975431103, 0.0012239660659042876, 0.0019573382838131976, 0.0027712820776554926, 0.003662174496572894, 0.004623304823549534, 0.005644664033337892, 0.006712877346119934, 0.007811305561111289, 0.00892033205592025, 0.010017840904494788, 0.011079878229316185, 0.012081474683539681, 0.012997593086843876, 0.01380415303799684, 0.014479075072484813, 0.015003281703834448, 0.015361592229302915] + [0.015543452803837182] * 2 + [0.015361592229302915, 0.015003281703834448, 0.014479075072484813, 0.01380415303799684, 0.012997593086843876, 0.012081474683539681, 0.011079878229316185, 0.010017840904494788, 0.00892033205592025, 0.007811305561111289, 0.006712877346119934, 0.005644664033337892, 0.004623304823549534, 0.003662174496572894, 0.0027712820776554926, 0.0019573382838131976, 0.0012239660659042876, 0.0005720227975431103, 0.0],
        },
        "minus_y90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.00019562936928179964, -0.00022443321116606284, -0.00025417126498437285, -0.00028405498011208486, -0.00031313908547720353, -0.00034034373080893496, -0.0003644892709027775, -0.00038434326585312986, -0.00039867815640112775, -0.0004063369281040248, -0.00040630301722545273, -0.0003977698588567755, -0.00038020495059744563, -0.00035340319739323356, -0.00031752467209533166, -0.0002731127810400792, -0.0002210901195036808, -0.0001627309400392091, -9.961099385508887e-05, -3.3537366995584185e-05, 3.3537366995584185e-05, 9.961099385508887e-05, 0.0001627309400392091, 0.0002210901195036808, 0.0002731127810400792, 0.00031752467209533166, 0.00035340319739323356, 0.00038020495059744563, 0.0003977698588567755, 0.00040630301722545273, 0.0004063369281040248, 0.00039867815640112775, 0.00038434326585312986, 0.0003644892709027775, 0.00034034373080893496, 0.00031313908547720353, 0.00028405498011208486, 0.00025417126498437285, 0.00022443321116606284, 0.00019562936928179964],
        },
        "minus_y90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, -0.00028601139877155513, -0.0006119830329521438, -0.0009786691419065988, -0.0013856410388277463, -0.001831087248286447, -0.002311652411774767, -0.002822332016668946, -0.003356438673059967, -0.0039056527805556443, -0.004460166027960125, -0.005008920452247394, -0.005539939114658093, -0.006040737341769841, -0.006498796543421938, -0.00690207651899842, -0.007239537536242406, -0.007501640851917224, -0.007680796114651458] + [-0.007771726401918591] * 2 + [-0.007680796114651458, -0.007501640851917224, -0.007239537536242406, -0.00690207651899842, -0.006498796543421938, -0.006040737341769841, -0.005539939114658093, -0.005008920452247394, -0.004460166027960125, -0.0039056527805556443, -0.003356438673059967, -0.002822332016668946, -0.002311652411774767, -0.001831087248286447, -0.0013856410388277463, -0.0009786691419065988, -0.0006119830329521438, -0.00028601139877155513, 0.0],
        },
        "readout_wf_q5": {
            "type": "constant",
            "sample": 0.014400000000000003,
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
            "samples": [0.0] + [0.197654568417] * 27,
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
            "samples": [0.0] + [0.045] * 31,
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
            "cosine": [(1.0, 600)],
            "sine": [(0.0, 600)],
        },
        "sine_weights": {
            "cosine": [(0.0, 600)],
            "sine": [(1.0, 600)],
        },
        "minus_sine_weights": {
            "cosine": [(0.0, 600)],
            "sine": [(-1.0, 600)],
        },
        "rotated_cosine_weights_q1": {
            "cosine": [(-0.6401096994849559, 600)],
            "sine": [(-0.768283523593523, 600)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(0.768283523593523, 600)],
            "sine": [(-0.6401096994849559, 600)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(-0.768283523593523, 600)],
            "sine": [(0.6401096994849559, 600)],
        },
        "rotated_cosine_weights_q2": {
            "cosine": [(0.2469990127227423, 600)],
            "sine": [(-0.9690157314068697, 600)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(0.9690157314068697, 600)],
            "sine": [(0.2469990127227423, 600)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(-0.9690157314068697, 600)],
            "sine": [(-0.2469990127227423, 600)],
        },
        "rotated_cosine_weights_q3": {
            "cosine": [(-0.05756402695956744, 600)],
            "sine": [(-0.9983418166140283, 600)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(0.9983418166140283, 600)],
            "sine": [(-0.05756402695956744, 600)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(-0.9983418166140283, 600)],
            "sine": [(0.05756402695956744, 600)],
        },
        "rotated_cosine_weights_q4": {
            "cosine": [(-0.894934361602025, 600)],
            "sine": [(0.446197813109809, 600)],
        },
        "rotated_sine_weights_q4": {
            "cosine": [(-0.446197813109809, 600)],
            "sine": [(-0.894934361602025, 600)],
        },
        "rotated_minus_sine_weights_q4": {
            "cosine": [(0.446197813109809, 600)],
            "sine": [(0.894934361602025, 600)],
        },
        "rotated_cosine_weights_q5": {
            "cosine": [(-0.11146893220632534, 600)],
            "sine": [(0.9937679191605964, 600)],
        },
        "rotated_sine_weights_q5": {
            "cosine": [(-0.9937679191605964, 600)],
            "sine": [(-0.11146893220632534, 600)],
        },
        "rotated_minus_sine_weights_q5": {
            "cosine": [(0.9937679191605964, 600)],
            "sine": [(0.11146893220632534, 600)],
        },
        "opt_cosine_weights_q1": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_sine_weights_q1": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_minus_sine_weights_q1": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_cosine_weights_q2": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_sine_weights_q2": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_minus_sine_weights_q2": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_cosine_weights_q3": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_sine_weights_q3": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_minus_sine_weights_q3": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_cosine_weights_q4": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_sine_weights_q4": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_minus_sine_weights_q4": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_cosine_weights_q5": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_sine_weights_q5": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_minus_sine_weights_q5": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
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
                    "offset": -0.03,
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
                    "offset": -0.003,
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
                "mixer": "rr1_mixer_6a7",
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
                "mixer": "rr2_mixer_4a4",
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
            "intermediate_frequency": -23300000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q3",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "rr3_mixer_012",
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
            "intermediate_frequency": 157500000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q4",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "rr4_mixer_d71",
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
            "intermediate_frequency": 62300000.0,
            "operations": {
                "cw": "const_pulse",
                "readout": "readout_pulse_q5",
            },
            "mixInputs": {
                "I": ('con1', 1),
                "Q": ('con1', 2),
                "mixer": "rr5_mixer_bdd",
                "lo_frequency": 5880000000.0,
            },
        },
        "q1_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": -116000000.0,
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
                "mixer": "q1_xy_mixer_2d4",
                "lo_frequency": 5200000000.0,
            },
        },
        "q2_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": -64000000.0,
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
                "mixer": "q2_xy_mixer_4be",
                "lo_frequency": 4500000000.0,
            },
        },
        "q3_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": -58000000.0,
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
                "mixer": "q3_xy_mixer_6c3",
                "lo_frequency": 4500000000.0,
            },
        },
        "q4_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": -85000000.0,
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
                "mixer": "q4_xy_mixer_b68",
                "lo_frequency": 4500000000.0,
            },
        },
        "q00_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": -85000000.0,
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
                "mixer": "q00_xy_mixer_809",
                "lo_frequency": 4500000000.0,
            },
        },
        "q5_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": -138450000.0,
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
                "mixer": "q5_xy_mixer_37f",
                "lo_frequency": 4500000000.0,
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
            "length": 40,
            "waveforms": {
                "I": "x90_I_wf_q1",
                "Q": "x90_Q_wf_q1",
            },
            "operation": "control",
        },
        "x180_pulse_q1": {
            "length": 40,
            "waveforms": {
                "I": "x180_I_wf_q1",
                "Q": "x180_Q_wf_q1",
            },
            "operation": "control",
        },
        "-x90_pulse_q1": {
            "length": 40,
            "waveforms": {
                "I": "minus_x90_I_wf_q1",
                "Q": "minus_x90_Q_wf_q1",
            },
            "operation": "control",
        },
        "y90_pulse_q1": {
            "length": 40,
            "waveforms": {
                "I": "y90_I_wf_q1",
                "Q": "y90_Q_wf_q1",
            },
            "operation": "control",
        },
        "y180_pulse_q1": {
            "length": 40,
            "waveforms": {
                "I": "y180_I_wf_q1",
                "Q": "y180_Q_wf_q1",
            },
            "operation": "control",
        },
        "-y90_pulse_q1": {
            "length": 40,
            "waveforms": {
                "I": "minus_y90_I_wf_q1",
                "Q": "minus_y90_Q_wf_q1",
            },
            "operation": "control",
        },
        "readout_pulse_q1": {
            "length": 600,
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
            "length": 40,
            "waveforms": {
                "I": "x90_I_wf_q2",
                "Q": "x90_Q_wf_q2",
            },
            "operation": "control",
        },
        "x180_pulse_q2": {
            "length": 40,
            "waveforms": {
                "I": "x180_I_wf_q2",
                "Q": "x180_Q_wf_q2",
            },
            "operation": "control",
        },
        "-x90_pulse_q2": {
            "length": 40,
            "waveforms": {
                "I": "minus_x90_I_wf_q2",
                "Q": "minus_x90_Q_wf_q2",
            },
            "operation": "control",
        },
        "y90_pulse_q2": {
            "length": 40,
            "waveforms": {
                "I": "y90_I_wf_q2",
                "Q": "y90_Q_wf_q2",
            },
            "operation": "control",
        },
        "y180_pulse_q2": {
            "length": 40,
            "waveforms": {
                "I": "y180_I_wf_q2",
                "Q": "y180_Q_wf_q2",
            },
            "operation": "control",
        },
        "-y90_pulse_q2": {
            "length": 40,
            "waveforms": {
                "I": "minus_y90_I_wf_q2",
                "Q": "minus_y90_Q_wf_q2",
            },
            "operation": "control",
        },
        "readout_pulse_q2": {
            "length": 600,
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
            "length": 40,
            "waveforms": {
                "I": "x90_I_wf_q3",
                "Q": "x90_Q_wf_q3",
            },
            "operation": "control",
        },
        "x180_pulse_q3": {
            "length": 40,
            "waveforms": {
                "I": "x180_I_wf_q3",
                "Q": "x180_Q_wf_q3",
            },
            "operation": "control",
        },
        "-x90_pulse_q3": {
            "length": 40,
            "waveforms": {
                "I": "minus_x90_I_wf_q3",
                "Q": "minus_x90_Q_wf_q3",
            },
            "operation": "control",
        },
        "y90_pulse_q3": {
            "length": 40,
            "waveforms": {
                "I": "y90_I_wf_q3",
                "Q": "y90_Q_wf_q3",
            },
            "operation": "control",
        },
        "y180_pulse_q3": {
            "length": 40,
            "waveforms": {
                "I": "y180_I_wf_q3",
                "Q": "y180_Q_wf_q3",
            },
            "operation": "control",
        },
        "-y90_pulse_q3": {
            "length": 40,
            "waveforms": {
                "I": "minus_y90_I_wf_q3",
                "Q": "minus_y90_Q_wf_q3",
            },
            "operation": "control",
        },
        "readout_pulse_q3": {
            "length": 600,
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
            "length": 40,
            "waveforms": {
                "I": "x90_I_wf_q4",
                "Q": "x90_Q_wf_q4",
            },
            "operation": "control",
        },
        "x180_pulse_q4": {
            "length": 40,
            "waveforms": {
                "I": "x180_I_wf_q4",
                "Q": "x180_Q_wf_q4",
            },
            "operation": "control",
        },
        "-x90_pulse_q4": {
            "length": 40,
            "waveforms": {
                "I": "minus_x90_I_wf_q4",
                "Q": "minus_x90_Q_wf_q4",
            },
            "operation": "control",
        },
        "y90_pulse_q4": {
            "length": 40,
            "waveforms": {
                "I": "y90_I_wf_q4",
                "Q": "y90_Q_wf_q4",
            },
            "operation": "control",
        },
        "y180_pulse_q4": {
            "length": 40,
            "waveforms": {
                "I": "y180_I_wf_q4",
                "Q": "y180_Q_wf_q4",
            },
            "operation": "control",
        },
        "-y90_pulse_q4": {
            "length": 40,
            "waveforms": {
                "I": "minus_y90_I_wf_q4",
                "Q": "minus_y90_Q_wf_q4",
            },
            "operation": "control",
        },
        "readout_pulse_q4": {
            "length": 600,
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
            "length": 40,
            "waveforms": {
                "I": "x90_I_wf_q5",
                "Q": "x90_Q_wf_q5",
            },
            "operation": "control",
        },
        "x180_pulse_q5": {
            "length": 40,
            "waveforms": {
                "I": "x180_I_wf_q5",
                "Q": "x180_Q_wf_q5",
            },
            "operation": "control",
        },
        "-x90_pulse_q5": {
            "length": 40,
            "waveforms": {
                "I": "minus_x90_I_wf_q5",
                "Q": "minus_x90_Q_wf_q5",
            },
            "operation": "control",
        },
        "y90_pulse_q5": {
            "length": 40,
            "waveforms": {
                "I": "y90_I_wf_q5",
                "Q": "y90_Q_wf_q5",
            },
            "operation": "control",
        },
        "y180_pulse_q5": {
            "length": 40,
            "waveforms": {
                "I": "y180_I_wf_q5",
                "Q": "y180_Q_wf_q5",
            },
            "operation": "control",
        },
        "-y90_pulse_q5": {
            "length": 40,
            "waveforms": {
                "I": "minus_y90_I_wf_q5",
                "Q": "minus_y90_Q_wf_q5",
            },
            "operation": "control",
        },
        "readout_pulse_q5": {
            "length": 600,
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
            "samples": [0.0, 0.00037509691642171163, 0.0008026006989536316, 0.001283500513975867, 0.0018172341492822906, 0.0024014258993920617, 0.003031675294130842, 0.003701419038254355, 0.00440188678434094, 0.005122167581056582, 0.0058493980694559015, 0.006569076002947401, 0.007265493920863071, 0.007922278481009626, 0.00852301186022549, 0.009051903631473335, 0.009494475457367089, 0.009838217510711114, 0.01007317523232978] + [0.010192428068089955] * 2 + [0.01007317523232978, 0.009838217510711114, 0.009494475457367089, 0.009051903631473335, 0.00852301186022549, 0.007922278481009626, 0.007265493920863071, 0.006569076002947401, 0.0058493980694559015, 0.005122167581056582, 0.00440188678434094, 0.003701419038254355, 0.003031675294130842, 0.0024014258993920617, 0.0018172341492822906, 0.001283500513975867, 0.0008026006989536316, 0.00037509691642171163, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q1": {
            "samples": [-0.0002448609334099765, -0.0002809134731460448, -0.0003181353260942, -0.0003555394970875079, -0.00039194283066283934, -0.00042599372431684684, -0.0004562156664862241, -0.0004810660647332144, -0.0004990084355173089, -0.000508594593233965, -0.0005085521484343401, -0.0004978715582409541, -0.0004758863121225932, -0.0004423397013519283, -0.0003974320822859854, -0.0003418436134471042, -0.0002767290679724698, -0.00020368337340640174, -0.0001246788302942287, -4.1977291123514775e-05, 4.1977291123514775e-05, 0.0001246788302942287, 0.00020368337340640174, 0.0002767290679724698, 0.0003418436134471042, 0.0003974320822859854, 0.0004423397013519283, 0.0004758863121225932, 0.0004978715582409541, 0.0005085521484343401, 0.000508594593233965, 0.0004990084355173089, 0.0004810660647332144, 0.0004562156664862241, 0.00042599372431684684, 0.00039194283066283934, 0.0003555394970875079, 0.0003181353260942, 0.0002809134731460448, 0.0002448609334099765],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q1": {
            "samples": [0.0, 0.0007501938328434233, 0.0016052013979072632, 0.002567001027951734, 0.003634468298564581, 0.004802851798784123, 0.006063350588261684, 0.00740283807650871, 0.00880377356868188, 0.010244335162113163, 0.011698796138911803, 0.013138152005894802, 0.014530987841726142, 0.01584455696201925, 0.01704602372045098, 0.01810380726294667, 0.018988950914734178, 0.019676435021422228, 0.02014635046465956] + [0.02038485613617991] * 2 + [0.02014635046465956, 0.019676435021422228, 0.018988950914734178, 0.01810380726294667, 0.01704602372045098, 0.01584455696201925, 0.014530987841726142, 0.013138152005894802, 0.011698796138911803, 0.010244335162113163, 0.00880377356868188, 0.00740283807650871, 0.006063350588261684, 0.004802851798784123, 0.003634468298564581, 0.002567001027951734, 0.0016052013979072632, 0.0007501938328434233, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q1": {
            "samples": [-0.000489721866819953, -0.0005618269462920896, -0.0006362706521884, -0.0007110789941750158, -0.0007838856613256787, -0.0008519874486336937, -0.0009124313329724482, -0.0009621321294664288, -0.0009980168710346177, -0.00101718918646793, -0.0010171042968686803, -0.0009957431164819082, -0.0009517726242451864, -0.0008846794027038566, -0.0007948641645719708, -0.0006836872268942084, -0.0005534581359449396, -0.0004073667468128035, -0.0002493576605884574, -8.395458224702955e-05, 8.395458224702955e-05, 0.0002493576605884574, 0.0004073667468128035, 0.0005534581359449396, 0.0006836872268942084, 0.0007948641645719708, 0.0008846794027038566, 0.0009517726242451864, 0.0009957431164819082, 0.0010171042968686803, 0.00101718918646793, 0.0009980168710346177, 0.0009621321294664288, 0.0009124313329724482, 0.0008519874486336937, 0.0007838856613256787, 0.0007110789941750158, 0.0006362706521884, 0.0005618269462920896, 0.000489721866819953],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q1": {
            "samples": [0.0, -0.00037509691642171163, -0.0008026006989536316, -0.001283500513975867, -0.0018172341492822906, -0.0024014258993920617, -0.003031675294130842, -0.003701419038254355, -0.00440188678434094, -0.005122167581056582, -0.0058493980694559015, -0.006569076002947401, -0.007265493920863071, -0.007922278481009626, -0.00852301186022549, -0.009051903631473335, -0.009494475457367089, -0.009838217510711114, -0.01007317523232978] + [-0.010192428068089955] * 2 + [-0.01007317523232978, -0.009838217510711114, -0.009494475457367089, -0.009051903631473335, -0.00852301186022549, -0.007922278481009626, -0.007265493920863071, -0.006569076002947401, -0.0058493980694559015, -0.005122167581056582, -0.00440188678434094, -0.003701419038254355, -0.003031675294130842, -0.0024014258993920617, -0.0018172341492822906, -0.001283500513975867, -0.0008026006989536316, -0.00037509691642171163, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q1": {
            "samples": [0.0002448609334099765, 0.0002809134731460448, 0.0003181353260942, 0.0003555394970875079, 0.00039194283066283934, 0.00042599372431684684, 0.0004562156664862241, 0.0004810660647332144, 0.0004990084355173089, 0.000508594593233965, 0.0005085521484343401, 0.0004978715582409541, 0.0004758863121225932, 0.0004423397013519283, 0.0003974320822859854, 0.0003418436134471042, 0.0002767290679724698, 0.00020368337340640174, 0.0001246788302942287, 4.1977291123514775e-05, -4.1977291123514775e-05, -0.0001246788302942287, -0.00020368337340640174, -0.0002767290679724698, -0.0003418436134471042, -0.0003974320822859854, -0.0004423397013519283, -0.0004758863121225932, -0.0004978715582409541, -0.0005085521484343401, -0.000508594593233965, -0.0004990084355173089, -0.0004810660647332144, -0.0004562156664862241, -0.00042599372431684684, -0.00039194283066283934, -0.0003555394970875079, -0.0003181353260942, -0.0002809134731460448, -0.0002448609334099765],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q1": {
            "samples": [0.0002448609334099765, 0.0002809134731460448, 0.0003181353260942, 0.0003555394970875079, 0.00039194283066283934, 0.00042599372431684684, 0.0004562156664862241, 0.0004810660647332144, 0.0004990084355173089, 0.000508594593233965, 0.0005085521484343401, 0.0004978715582409541, 0.0004758863121225932, 0.0004423397013519283, 0.0003974320822859854, 0.0003418436134471042, 0.0002767290679724698, 0.00020368337340640174, 0.0001246788302942287, 4.1977291123514775e-05, -4.1977291123514775e-05, -0.0001246788302942287, -0.00020368337340640174, -0.0002767290679724698, -0.0003418436134471042, -0.0003974320822859854, -0.0004423397013519283, -0.0004758863121225932, -0.0004978715582409541, -0.0005085521484343401, -0.000508594593233965, -0.0004990084355173089, -0.0004810660647332144, -0.0004562156664862241, -0.00042599372431684684, -0.00039194283066283934, -0.0003555394970875079, -0.0003181353260942, -0.0002809134731460448, -0.0002448609334099765],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q1": {
            "samples": [0.0, 0.00037509691642171163, 0.0008026006989536316, 0.001283500513975867, 0.0018172341492822906, 0.0024014258993920617, 0.003031675294130842, 0.003701419038254355, 0.00440188678434094, 0.005122167581056582, 0.0058493980694559015, 0.006569076002947401, 0.007265493920863071, 0.007922278481009626, 0.00852301186022549, 0.009051903631473335, 0.009494475457367089, 0.009838217510711114, 0.01007317523232978] + [0.010192428068089955] * 2 + [0.01007317523232978, 0.009838217510711114, 0.009494475457367089, 0.009051903631473335, 0.00852301186022549, 0.007922278481009626, 0.007265493920863071, 0.006569076002947401, 0.0058493980694559015, 0.005122167581056582, 0.00440188678434094, 0.003701419038254355, 0.003031675294130842, 0.0024014258993920617, 0.0018172341492822906, 0.001283500513975867, 0.0008026006989536316, 0.00037509691642171163, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q1": {
            "samples": [0.000489721866819953, 0.0005618269462920896, 0.0006362706521884, 0.0007110789941750158, 0.0007838856613256787, 0.0008519874486336937, 0.0009124313329724482, 0.0009621321294664288, 0.0009980168710346177, 0.00101718918646793, 0.0010171042968686803, 0.0009957431164819082, 0.0009517726242451864, 0.0008846794027038566, 0.0007948641645719708, 0.0006836872268942084, 0.0005534581359449396, 0.0004073667468128035, 0.0002493576605884574, 8.395458224702955e-05, -8.395458224702955e-05, -0.0002493576605884574, -0.0004073667468128035, -0.0005534581359449396, -0.0006836872268942084, -0.0007948641645719708, -0.0008846794027038566, -0.0009517726242451864, -0.0009957431164819082, -0.0010171042968686803, -0.00101718918646793, -0.0009980168710346177, -0.0009621321294664288, -0.0009124313329724482, -0.0008519874486336937, -0.0007838856613256787, -0.0007110789941750158, -0.0006362706521884, -0.0005618269462920896, -0.000489721866819953],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q1": {
            "samples": [0.0, 0.0007501938328434233, 0.0016052013979072632, 0.002567001027951734, 0.003634468298564581, 0.004802851798784123, 0.006063350588261684, 0.00740283807650871, 0.00880377356868188, 0.010244335162113163, 0.011698796138911803, 0.013138152005894802, 0.014530987841726142, 0.01584455696201925, 0.01704602372045098, 0.01810380726294667, 0.018988950914734178, 0.019676435021422228, 0.02014635046465956] + [0.02038485613617991] * 2 + [0.02014635046465956, 0.019676435021422228, 0.018988950914734178, 0.01810380726294667, 0.01704602372045098, 0.01584455696201925, 0.014530987841726142, 0.013138152005894802, 0.011698796138911803, 0.010244335162113163, 0.00880377356868188, 0.00740283807650871, 0.006063350588261684, 0.004802851798784123, 0.003634468298564581, 0.002567001027951734, 0.0016052013979072632, 0.0007501938328434233, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q1": {
            "samples": [-0.0002448609334099765, -0.0002809134731460448, -0.0003181353260942, -0.0003555394970875079, -0.00039194283066283934, -0.00042599372431684684, -0.0004562156664862241, -0.0004810660647332144, -0.0004990084355173089, -0.000508594593233965, -0.0005085521484343401, -0.0004978715582409541, -0.0004758863121225932, -0.0004423397013519283, -0.0003974320822859854, -0.0003418436134471042, -0.0002767290679724698, -0.00020368337340640174, -0.0001246788302942287, -4.1977291123514775e-05, 4.1977291123514775e-05, 0.0001246788302942287, 0.00020368337340640174, 0.0002767290679724698, 0.0003418436134471042, 0.0003974320822859854, 0.0004423397013519283, 0.0004758863121225932, 0.0004978715582409541, 0.0005085521484343401, 0.000508594593233965, 0.0004990084355173089, 0.0004810660647332144, 0.0004562156664862241, 0.00042599372431684684, 0.00039194283066283934, 0.0003555394970875079, 0.0003181353260942, 0.0002809134731460448, 0.0002448609334099765],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q1": {
            "samples": [0.0, -0.00037509691642171163, -0.0008026006989536316, -0.001283500513975867, -0.0018172341492822906, -0.0024014258993920617, -0.003031675294130842, -0.003701419038254355, -0.00440188678434094, -0.005122167581056582, -0.0058493980694559015, -0.006569076002947401, -0.007265493920863071, -0.007922278481009626, -0.00852301186022549, -0.009051903631473335, -0.009494475457367089, -0.009838217510711114, -0.01007317523232978] + [-0.010192428068089955] * 2 + [-0.01007317523232978, -0.009838217510711114, -0.009494475457367089, -0.009051903631473335, -0.00852301186022549, -0.007922278481009626, -0.007265493920863071, -0.006569076002947401, -0.0058493980694559015, -0.005122167581056582, -0.00440188678434094, -0.003701419038254355, -0.003031675294130842, -0.0024014258993920617, -0.0018172341492822906, -0.001283500513975867, -0.0008026006989536316, -0.00037509691642171163, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q1": {
            "sample": 0.0072000000000000015,
            "type": "constant",
        },
        "x90_I_wf_q2": {
            "samples": [0.0, 0.00024850170712938384, 0.0005317229630567809, 0.000850319090509012, 0.0012039176238995174, 0.001590944658347241, 0.0020084848823616833, 0.0024521901128435105, 0.002916249994625872, 0.003393436022449986, 0.0038752262210145355, 0.004352012851952654, 0.004813389722571785, 0.005248509493668878, 0.0056464953573993875, 0.005996886155851085, 0.006290089990505696, 0.006517819100846113, 0.006673478591418479] + [0.0067524835951095945] * 2 + [0.006673478591418479, 0.006517819100846113, 0.006290089990505696, 0.005996886155851085, 0.0056464953573993875, 0.005248509493668878, 0.004813389722571785, 0.004352012851952654, 0.0038752262210145355, 0.003393436022449986, 0.002916249994625872, 0.0024521901128435105, 0.0020084848823616833, 0.001590944658347241, 0.0012039176238995174, 0.000850319090509012, 0.0005317229630567809, 0.00024850170712938384, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q2": {
            "samples": [-0.00010838257818769472, -0.00012434048193490877, -0.00014081595775403325, -0.00015737213284808325, -0.00017348530816182377, -0.0001885572250757286, -0.00020193433658364, -0.00021293384636044148, -0.00022087566205679748, -0.00022511877456060173, -0.00022509998725651884, -0.00022037244707440572, -0.00021064113704787174, -0.00019579243042019533, -0.00017591501074831778, -0.0001513099359968597, -0.00012248834237724954, -9.015619125649105e-05, -5.5186480278948396e-05, -1.8580371208846324e-05, 1.8580371208846324e-05, 5.5186480278948396e-05, 9.015619125649105e-05, 0.00012248834237724954, 0.0001513099359968597, 0.00017591501074831778, 0.00019579243042019533, 0.00021064113704787174, 0.00022037244707440572, 0.00022509998725651884, 0.00022511877456060173, 0.00022087566205679748, 0.00021293384636044148, 0.00020193433658364, 0.0001885572250757286, 0.00017348530816182377, 0.00015737213284808325, 0.00014081595775403325, 0.00012434048193490877, 0.00010838257818769472],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q2": {
            "samples": [0.0, 0.0004970034142587677, 0.0010634459261135618, 0.001700638181018024, 0.002407835247799035, 0.003181889316694482, 0.004016969764723367, 0.004904380225687021, 0.005832499989251744, 0.006786872044899972, 0.007750452442029071, 0.008704025703905308, 0.00962677944514357, 0.010497018987337755, 0.011292990714798775, 0.01199377231170217, 0.012580179981011392, 0.013035638201692226, 0.013346957182836959] + [0.013504967190219189] * 2 + [0.013346957182836959, 0.013035638201692226, 0.012580179981011392, 0.01199377231170217, 0.011292990714798775, 0.010497018987337755, 0.00962677944514357, 0.008704025703905308, 0.007750452442029071, 0.006786872044899972, 0.005832499989251744, 0.004904380225687021, 0.004016969764723367, 0.003181889316694482, 0.002407835247799035, 0.001700638181018024, 0.0010634459261135618, 0.0004970034142587677, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q2": {
            "samples": [-0.00021676515637538945, -0.00024868096386981755, -0.0002816319155080665, -0.0003147442656961665, -0.00034697061632364755, -0.0003771144501514572, -0.00040386867316728, -0.00042586769272088295, -0.00044175132411359495, -0.00045023754912120346, -0.0004501999745130377, -0.00044074489414881144, -0.0004212822740957435, -0.00039158486084039067, -0.00035183002149663555, -0.0003026198719937194, -0.0002449766847544991, -0.0001803123825129821, -0.00011037296055789679, -3.716074241769265e-05, 3.716074241769265e-05, 0.00011037296055789679, 0.0001803123825129821, 0.0002449766847544991, 0.0003026198719937194, 0.00035183002149663555, 0.00039158486084039067, 0.0004212822740957435, 0.00044074489414881144, 0.0004501999745130377, 0.00045023754912120346, 0.00044175132411359495, 0.00042586769272088295, 0.00040386867316728, 0.0003771144501514572, 0.00034697061632364755, 0.0003147442656961665, 0.0002816319155080665, 0.00024868096386981755, 0.00021676515637538945],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q2": {
            "samples": [0.0, -0.00024850170712938384, -0.0005317229630567809, -0.000850319090509012, -0.0012039176238995174, -0.001590944658347241, -0.0020084848823616833, -0.0024521901128435105, -0.002916249994625872, -0.003393436022449986, -0.0038752262210145355, -0.004352012851952654, -0.004813389722571785, -0.005248509493668878, -0.0056464953573993875, -0.005996886155851085, -0.006290089990505696, -0.006517819100846113, -0.006673478591418479] + [-0.0067524835951095945] * 2 + [-0.006673478591418479, -0.006517819100846113, -0.006290089990505696, -0.005996886155851085, -0.0056464953573993875, -0.005248509493668878, -0.004813389722571785, -0.004352012851952654, -0.0038752262210145355, -0.003393436022449986, -0.002916249994625872, -0.0024521901128435105, -0.0020084848823616833, -0.001590944658347241, -0.0012039176238995174, -0.000850319090509012, -0.0005317229630567809, -0.00024850170712938384, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q2": {
            "samples": [0.00010838257818769472, 0.00012434048193490877, 0.00014081595775403325, 0.00015737213284808325, 0.00017348530816182377, 0.0001885572250757286, 0.00020193433658364, 0.00021293384636044148, 0.00022087566205679748, 0.00022511877456060173, 0.00022509998725651884, 0.00022037244707440572, 0.00021064113704787174, 0.00019579243042019533, 0.00017591501074831778, 0.0001513099359968597, 0.00012248834237724954, 9.015619125649105e-05, 5.5186480278948396e-05, 1.8580371208846324e-05, -1.8580371208846324e-05, -5.5186480278948396e-05, -9.015619125649105e-05, -0.00012248834237724954, -0.0001513099359968597, -0.00017591501074831778, -0.00019579243042019533, -0.00021064113704787174, -0.00022037244707440572, -0.00022509998725651884, -0.00022511877456060173, -0.00022087566205679748, -0.00021293384636044148, -0.00020193433658364, -0.0001885572250757286, -0.00017348530816182377, -0.00015737213284808325, -0.00014081595775403325, -0.00012434048193490877, -0.00010838257818769472],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q2": {
            "samples": [0.00010838257818769472, 0.00012434048193490877, 0.00014081595775403325, 0.00015737213284808325, 0.00017348530816182377, 0.0001885572250757286, 0.00020193433658364, 0.00021293384636044148, 0.00022087566205679748, 0.00022511877456060173, 0.00022509998725651884, 0.00022037244707440572, 0.00021064113704787174, 0.00019579243042019533, 0.00017591501074831778, 0.0001513099359968597, 0.00012248834237724954, 9.015619125649105e-05, 5.5186480278948396e-05, 1.8580371208846324e-05, -1.8580371208846324e-05, -5.5186480278948396e-05, -9.015619125649105e-05, -0.00012248834237724954, -0.0001513099359968597, -0.00017591501074831778, -0.00019579243042019533, -0.00021064113704787174, -0.00022037244707440572, -0.00022509998725651884, -0.00022511877456060173, -0.00022087566205679748, -0.00021293384636044148, -0.00020193433658364, -0.0001885572250757286, -0.00017348530816182377, -0.00015737213284808325, -0.00014081595775403325, -0.00012434048193490877, -0.00010838257818769472],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q2": {
            "samples": [0.0, 0.00024850170712938384, 0.0005317229630567809, 0.000850319090509012, 0.0012039176238995174, 0.001590944658347241, 0.0020084848823616833, 0.0024521901128435105, 0.002916249994625872, 0.003393436022449986, 0.0038752262210145355, 0.004352012851952654, 0.004813389722571785, 0.005248509493668878, 0.0056464953573993875, 0.005996886155851085, 0.006290089990505696, 0.006517819100846113, 0.006673478591418479] + [0.0067524835951095945] * 2 + [0.006673478591418479, 0.006517819100846113, 0.006290089990505696, 0.005996886155851085, 0.0056464953573993875, 0.005248509493668878, 0.004813389722571785, 0.004352012851952654, 0.0038752262210145355, 0.003393436022449986, 0.002916249994625872, 0.0024521901128435105, 0.0020084848823616833, 0.001590944658347241, 0.0012039176238995174, 0.000850319090509012, 0.0005317229630567809, 0.00024850170712938384, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q2": {
            "samples": [0.00021676515637538945, 0.00024868096386981755, 0.0002816319155080665, 0.0003147442656961665, 0.00034697061632364755, 0.0003771144501514572, 0.00040386867316728, 0.00042586769272088295, 0.00044175132411359495, 0.00045023754912120346, 0.0004501999745130377, 0.00044074489414881144, 0.0004212822740957435, 0.00039158486084039067, 0.00035183002149663555, 0.0003026198719937194, 0.0002449766847544991, 0.0001803123825129821, 0.00011037296055789679, 3.716074241769265e-05, -3.716074241769265e-05, -0.00011037296055789679, -0.0001803123825129821, -0.0002449766847544991, -0.0003026198719937194, -0.00035183002149663555, -0.00039158486084039067, -0.0004212822740957435, -0.00044074489414881144, -0.0004501999745130377, -0.00045023754912120346, -0.00044175132411359495, -0.00042586769272088295, -0.00040386867316728, -0.0003771144501514572, -0.00034697061632364755, -0.0003147442656961665, -0.0002816319155080665, -0.00024868096386981755, -0.00021676515637538945],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q2": {
            "samples": [0.0, 0.0004970034142587677, 0.0010634459261135618, 0.001700638181018024, 0.002407835247799035, 0.003181889316694482, 0.004016969764723367, 0.004904380225687021, 0.005832499989251744, 0.006786872044899972, 0.007750452442029071, 0.008704025703905308, 0.00962677944514357, 0.010497018987337755, 0.011292990714798775, 0.01199377231170217, 0.012580179981011392, 0.013035638201692226, 0.013346957182836959] + [0.013504967190219189] * 2 + [0.013346957182836959, 0.013035638201692226, 0.012580179981011392, 0.01199377231170217, 0.011292990714798775, 0.010497018987337755, 0.00962677944514357, 0.008704025703905308, 0.007750452442029071, 0.006786872044899972, 0.005832499989251744, 0.004904380225687021, 0.004016969764723367, 0.003181889316694482, 0.002407835247799035, 0.001700638181018024, 0.0010634459261135618, 0.0004970034142587677, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q2": {
            "samples": [-0.00010838257818769472, -0.00012434048193490877, -0.00014081595775403325, -0.00015737213284808325, -0.00017348530816182377, -0.0001885572250757286, -0.00020193433658364, -0.00021293384636044148, -0.00022087566205679748, -0.00022511877456060173, -0.00022509998725651884, -0.00022037244707440572, -0.00021064113704787174, -0.00019579243042019533, -0.00017591501074831778, -0.0001513099359968597, -0.00012248834237724954, -9.015619125649105e-05, -5.5186480278948396e-05, -1.8580371208846324e-05, 1.8580371208846324e-05, 5.5186480278948396e-05, 9.015619125649105e-05, 0.00012248834237724954, 0.0001513099359968597, 0.00017591501074831778, 0.00019579243042019533, 0.00021064113704787174, 0.00022037244707440572, 0.00022509998725651884, 0.00022511877456060173, 0.00022087566205679748, 0.00021293384636044148, 0.00020193433658364, 0.0001885572250757286, 0.00017348530816182377, 0.00015737213284808325, 0.00014081595775403325, 0.00012434048193490877, 0.00010838257818769472],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q2": {
            "samples": [0.0, -0.00024850170712938384, -0.0005317229630567809, -0.000850319090509012, -0.0012039176238995174, -0.001590944658347241, -0.0020084848823616833, -0.0024521901128435105, -0.002916249994625872, -0.003393436022449986, -0.0038752262210145355, -0.004352012851952654, -0.004813389722571785, -0.005248509493668878, -0.0056464953573993875, -0.005996886155851085, -0.006290089990505696, -0.006517819100846113, -0.006673478591418479] + [-0.0067524835951095945] * 2 + [-0.006673478591418479, -0.006517819100846113, -0.006290089990505696, -0.005996886155851085, -0.0056464953573993875, -0.005248509493668878, -0.004813389722571785, -0.004352012851952654, -0.0038752262210145355, -0.003393436022449986, -0.002916249994625872, -0.0024521901128435105, -0.0020084848823616833, -0.001590944658347241, -0.0012039176238995174, -0.000850319090509012, -0.0005317229630567809, -0.00024850170712938384, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q2": {
            "sample": 0.014400000000000003,
            "type": "constant",
        },
        "x90_I_wf_q3": {
            "samples": [0.0, 0.00026881945676889333, 0.000575197167583436, 0.000919842035016038, 0.001302351140318975, 0.0017210218945643107, 0.002172700627460437, 0.0026526836440822882, 0.003154685528777674, 0.003670886766423884, 0.0041920686164433965, 0.004707837802112305, 0.005206937309951868, 0.0056776329113902325, 0.006108158499828268, 0.006487197602555891, 0.006804374077779748, 0.007050722549342966, 0.007219108916503011] + [0.007304573448797801] * 2 + [0.007219108916503011, 0.007050722549342966, 0.006804374077779748, 0.006487197602555891, 0.006108158499828268, 0.0056776329113902325, 0.005206937309951868, 0.004707837802112305, 0.0041920686164433965, 0.003670886766423884, 0.003154685528777674, 0.0026526836440822882, 0.002172700627460437, 0.0017210218945643107, 0.001302351140318975, 0.000919842035016038, 0.000575197167583436, 0.00026881945676889333, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q3": {
            "samples": [0.00015373482487367302, 0.00017637024819494088, 0.00019973981950535195, 0.0002232238583723165, 0.0002460795260122466, 0.0002674582249324461, 0.00028643293405426545, 0.00030203514372217335, 0.00031330017972402865, 0.00031931880530573396, 0.0003192921565310755, 0.00031258639648980963, 0.00029878305957223045, 0.00027772097236986536, 0.00024952592771144673, 0.00021462496003591948, 0.00017374308841244113, 0.0001278816808554905, 7.82790373041872e-05, 2.635525156942737e-05, -2.635525156942737e-05, -7.82790373041872e-05, -0.0001278816808554905, -0.00017374308841244113, -0.00021462496003591948, -0.00024952592771144673, -0.00027772097236986536, -0.00029878305957223045, -0.00031258639648980963, -0.0003192921565310755, -0.00031931880530573396, -0.00031330017972402865, -0.00030203514372217335, -0.00028643293405426545, -0.0002674582249324461, -0.0002460795260122466, -0.0002232238583723165, -0.00019973981950535195, -0.00017637024819494088, -0.00015373482487367302],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q3": {
            "samples": [0.0, 0.0005376389135377867, 0.001150394335166872, 0.001839684070032076, 0.00260470228063795, 0.0034420437891286215, 0.004345401254920874, 0.0053053672881645765, 0.006309371057555348, 0.007341773532847768, 0.008384137232886793, 0.00941567560422461, 0.010413874619903736, 0.011355265822780465, 0.012216316999656536, 0.012974395205111781, 0.013608748155559496, 0.014101445098685932, 0.014438217833006022] + [0.014609146897595602] * 2 + [0.014438217833006022, 0.014101445098685932, 0.013608748155559496, 0.012974395205111781, 0.012216316999656536, 0.011355265822780465, 0.010413874619903736, 0.00941567560422461, 0.008384137232886793, 0.007341773532847768, 0.006309371057555348, 0.0053053672881645765, 0.004345401254920874, 0.0034420437891286215, 0.00260470228063795, 0.001839684070032076, 0.001150394335166872, 0.0005376389135377867, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q3": {
            "samples": [0.00030746964974734603, 0.00035274049638988177, 0.0003994796390107039, 0.000446447716744633, 0.0004921590520244932, 0.0005349164498648922, 0.0005728658681085309, 0.0006040702874443467, 0.0006266003594480573, 0.0006386376106114679, 0.000638584313062151, 0.0006251727929796193, 0.0005975661191444609, 0.0005554419447397307, 0.0004990518554228935, 0.00042924992007183896, 0.00034748617682488225, 0.000255763361710981, 0.0001565580746083744, 5.271050313885474e-05, -5.271050313885474e-05, -0.0001565580746083744, -0.000255763361710981, -0.00034748617682488225, -0.00042924992007183896, -0.0004990518554228935, -0.0005554419447397307, -0.0005975661191444609, -0.0006251727929796193, -0.000638584313062151, -0.0006386376106114679, -0.0006266003594480573, -0.0006040702874443467, -0.0005728658681085309, -0.0005349164498648922, -0.0004921590520244932, -0.000446447716744633, -0.0003994796390107039, -0.00035274049638988177, -0.00030746964974734603],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q3": {
            "samples": [0.0, -0.00026881945676889333, -0.000575197167583436, -0.000919842035016038, -0.001302351140318975, -0.0017210218945643107, -0.002172700627460437, -0.0026526836440822882, -0.003154685528777674, -0.003670886766423884, -0.0041920686164433965, -0.004707837802112305, -0.005206937309951868, -0.0056776329113902325, -0.006108158499828268, -0.006487197602555891, -0.006804374077779748, -0.007050722549342966, -0.007219108916503011] + [-0.007304573448797801] * 2 + [-0.007219108916503011, -0.007050722549342966, -0.006804374077779748, -0.006487197602555891, -0.006108158499828268, -0.0056776329113902325, -0.005206937309951868, -0.004707837802112305, -0.0041920686164433965, -0.003670886766423884, -0.003154685528777674, -0.0026526836440822882, -0.002172700627460437, -0.0017210218945643107, -0.001302351140318975, -0.000919842035016038, -0.000575197167583436, -0.00026881945676889333, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q3": {
            "samples": [-0.00015373482487367302, -0.00017637024819494088, -0.00019973981950535195, -0.0002232238583723165, -0.0002460795260122466, -0.0002674582249324461, -0.00028643293405426545, -0.00030203514372217335, -0.00031330017972402865, -0.00031931880530573396, -0.0003192921565310755, -0.00031258639648980963, -0.00029878305957223045, -0.00027772097236986536, -0.00024952592771144673, -0.00021462496003591948, -0.00017374308841244113, -0.0001278816808554905, -7.82790373041872e-05, -2.635525156942737e-05, 2.635525156942737e-05, 7.82790373041872e-05, 0.0001278816808554905, 0.00017374308841244113, 0.00021462496003591948, 0.00024952592771144673, 0.00027772097236986536, 0.00029878305957223045, 0.00031258639648980963, 0.0003192921565310755, 0.00031931880530573396, 0.00031330017972402865, 0.00030203514372217335, 0.00028643293405426545, 0.0002674582249324461, 0.0002460795260122466, 0.0002232238583723165, 0.00019973981950535195, 0.00017637024819494088, 0.00015373482487367302],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q3": {
            "samples": [-0.00015373482487367302, -0.00017637024819494088, -0.00019973981950535195, -0.0002232238583723165, -0.0002460795260122466, -0.0002674582249324461, -0.00028643293405426545, -0.00030203514372217335, -0.00031330017972402865, -0.00031931880530573396, -0.0003192921565310755, -0.00031258639648980963, -0.00029878305957223045, -0.00027772097236986536, -0.00024952592771144673, -0.00021462496003591948, -0.00017374308841244113, -0.0001278816808554905, -7.82790373041872e-05, -2.635525156942737e-05, 2.635525156942737e-05, 7.82790373041872e-05, 0.0001278816808554905, 0.00017374308841244113, 0.00021462496003591948, 0.00024952592771144673, 0.00027772097236986536, 0.00029878305957223045, 0.00031258639648980963, 0.0003192921565310755, 0.00031931880530573396, 0.00031330017972402865, 0.00030203514372217335, 0.00028643293405426545, 0.0002674582249324461, 0.0002460795260122466, 0.0002232238583723165, 0.00019973981950535195, 0.00017637024819494088, 0.00015373482487367302],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q3": {
            "samples": [0.0, 0.00026881945676889333, 0.000575197167583436, 0.000919842035016038, 0.001302351140318975, 0.0017210218945643107, 0.002172700627460437, 0.0026526836440822882, 0.003154685528777674, 0.003670886766423884, 0.0041920686164433965, 0.004707837802112305, 0.005206937309951868, 0.0056776329113902325, 0.006108158499828268, 0.006487197602555891, 0.006804374077779748, 0.007050722549342966, 0.007219108916503011] + [0.007304573448797801] * 2 + [0.007219108916503011, 0.007050722549342966, 0.006804374077779748, 0.006487197602555891, 0.006108158499828268, 0.0056776329113902325, 0.005206937309951868, 0.004707837802112305, 0.0041920686164433965, 0.003670886766423884, 0.003154685528777674, 0.0026526836440822882, 0.002172700627460437, 0.0017210218945643107, 0.001302351140318975, 0.000919842035016038, 0.000575197167583436, 0.00026881945676889333, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q3": {
            "samples": [-0.00030746964974734603, -0.00035274049638988177, -0.0003994796390107039, -0.000446447716744633, -0.0004921590520244932, -0.0005349164498648922, -0.0005728658681085309, -0.0006040702874443467, -0.0006266003594480573, -0.0006386376106114679, -0.000638584313062151, -0.0006251727929796193, -0.0005975661191444609, -0.0005554419447397307, -0.0004990518554228935, -0.00042924992007183896, -0.00034748617682488225, -0.000255763361710981, -0.0001565580746083744, -5.271050313885474e-05, 5.271050313885474e-05, 0.0001565580746083744, 0.000255763361710981, 0.00034748617682488225, 0.00042924992007183896, 0.0004990518554228935, 0.0005554419447397307, 0.0005975661191444609, 0.0006251727929796193, 0.000638584313062151, 0.0006386376106114679, 0.0006266003594480573, 0.0006040702874443467, 0.0005728658681085309, 0.0005349164498648922, 0.0004921590520244932, 0.000446447716744633, 0.0003994796390107039, 0.00035274049638988177, 0.00030746964974734603],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q3": {
            "samples": [0.0, 0.0005376389135377867, 0.001150394335166872, 0.001839684070032076, 0.00260470228063795, 0.0034420437891286215, 0.004345401254920874, 0.0053053672881645765, 0.006309371057555348, 0.007341773532847768, 0.008384137232886793, 0.00941567560422461, 0.010413874619903736, 0.011355265822780465, 0.012216316999656536, 0.012974395205111781, 0.013608748155559496, 0.014101445098685932, 0.014438217833006022] + [0.014609146897595602] * 2 + [0.014438217833006022, 0.014101445098685932, 0.013608748155559496, 0.012974395205111781, 0.012216316999656536, 0.011355265822780465, 0.010413874619903736, 0.00941567560422461, 0.008384137232886793, 0.007341773532847768, 0.006309371057555348, 0.0053053672881645765, 0.004345401254920874, 0.0034420437891286215, 0.00260470228063795, 0.001839684070032076, 0.001150394335166872, 0.0005376389135377867, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q3": {
            "samples": [0.00015373482487367302, 0.00017637024819494088, 0.00019973981950535195, 0.0002232238583723165, 0.0002460795260122466, 0.0002674582249324461, 0.00028643293405426545, 0.00030203514372217335, 0.00031330017972402865, 0.00031931880530573396, 0.0003192921565310755, 0.00031258639648980963, 0.00029878305957223045, 0.00027772097236986536, 0.00024952592771144673, 0.00021462496003591948, 0.00017374308841244113, 0.0001278816808554905, 7.82790373041872e-05, 2.635525156942737e-05, -2.635525156942737e-05, -7.82790373041872e-05, -0.0001278816808554905, -0.00017374308841244113, -0.00021462496003591948, -0.00024952592771144673, -0.00027772097236986536, -0.00029878305957223045, -0.00031258639648980963, -0.0003192921565310755, -0.00031931880530573396, -0.00031330017972402865, -0.00030203514372217335, -0.00028643293405426545, -0.0002674582249324461, -0.0002460795260122466, -0.0002232238583723165, -0.00019973981950535195, -0.00017637024819494088, -0.00015373482487367302],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q3": {
            "samples": [0.0, -0.00026881945676889333, -0.000575197167583436, -0.000919842035016038, -0.001302351140318975, -0.0017210218945643107, -0.002172700627460437, -0.0026526836440822882, -0.003154685528777674, -0.003670886766423884, -0.0041920686164433965, -0.004707837802112305, -0.005206937309951868, -0.0056776329113902325, -0.006108158499828268, -0.006487197602555891, -0.006804374077779748, -0.007050722549342966, -0.007219108916503011] + [-0.007304573448797801] * 2 + [-0.007219108916503011, -0.007050722549342966, -0.006804374077779748, -0.006487197602555891, -0.006108158499828268, -0.0056776329113902325, -0.005206937309951868, -0.004707837802112305, -0.0041920686164433965, -0.003670886766423884, -0.003154685528777674, -0.0026526836440822882, -0.002172700627460437, -0.0017210218945643107, -0.001302351140318975, -0.000919842035016038, -0.000575197167583436, -0.00026881945676889333, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q3": {
            "sample": 0.014400000000000003,
            "type": "constant",
        },
        "x90_I_wf_q4": {
            "samples": [0.0, 0.0003016404369557931, 0.0006454247287418786, 0.0010321483299889263, 0.001461359128381175, 0.0019311466607611165, 0.0024379722156968858, 0.002976557809929544, 0.0035398506224075064, 0.0041190764297663355, 0.004703890947520788, 0.005282631952370203, 0.005842668028027387, 0.006370832278478575, 0.0068539220375979995, 0.007279239170309808, 0.0076351406802993675, 0.007911566581530187, 0.008100511749331867] + [0.008196410904755673] * 2 + [0.008100511749331867, 0.007911566581530187, 0.0076351406802993675, 0.007279239170309808, 0.0068539220375979995, 0.006370832278478575, 0.005842668028027387, 0.005282631952370203, 0.004703890947520788, 0.0041190764297663355, 0.0035398506224075064, 0.002976557809929544, 0.0024379722156968858, 0.0019311466607611165, 0.001461359128381175, 0.0010321483299889263, 0.0006454247287418786, 0.0003016404369557931, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q4": {
            "samples": [0.00019852730528736819, 0.00022775782998925512, 0.00025793640547980685, 0.00028826280001893186, 0.00031777773985658777, 0.00034538537846849474, 0.0003698885960944417, 0.00039003669620411765, 0.00040458393521291885, 0.0004123561593609051, 0.00041232174614694056, 0.0004036621826941565, 0.00038583707843119956, 0.00035863830014886154, 0.00032222829192143216, 0.00027715850978041434, 0.00022436521577443684, 0.000165141538468734, 0.00010108657130392946, 3.403416941183321e-05, -3.403416941183321e-05, -0.00010108657130392946, -0.000165141538468734, -0.00022436521577443684, -0.00027715850978041434, -0.00032222829192143216, -0.00035863830014886154, -0.00038583707843119956, -0.0004036621826941565, -0.00041232174614694056, -0.0004123561593609051, -0.00040458393521291885, -0.00039003669620411765, -0.0003698885960944417, -0.00034538537846849474, -0.00031777773985658777, -0.00028826280001893186, -0.00025793640547980685, -0.00022775782998925512, -0.00019852730528736819],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q4": {
            "samples": [0.0, 0.0006032808739115862, 0.0012908494574837572, 0.0020642966599778525, 0.00292271825676235, 0.003862293321522233, 0.0048759444313937715, 0.005953115619859088, 0.007079701244815013, 0.008238152859532671, 0.009407781895041576, 0.010565263904740406, 0.011685336056054775, 0.01274166455695715, 0.013707844075195999, 0.014558478340619616, 0.015270281360598735, 0.015823133163060374, 0.016201023498663734] + [0.016392821809511345] * 2 + [0.016201023498663734, 0.015823133163060374, 0.015270281360598735, 0.014558478340619616, 0.013707844075195999, 0.01274166455695715, 0.011685336056054775, 0.010565263904740406, 0.009407781895041576, 0.008238152859532671, 0.007079701244815013, 0.005953115619859088, 0.0048759444313937715, 0.003862293321522233, 0.00292271825676235, 0.0020642966599778525, 0.0012908494574837572, 0.0006032808739115862, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q4": {
            "samples": [0.00039705461057473637, 0.00045551565997851024, 0.0005158728109596137, 0.0005765256000378637, 0.0006355554797131755, 0.0006907707569369895, 0.0007397771921888834, 0.0007800733924082353, 0.0008091678704258377, 0.0008247123187218102, 0.0008246434922938811, 0.000807324365388313, 0.0007716741568623991, 0.0007172766002977231, 0.0006444565838428643, 0.0005543170195608287, 0.00044873043154887367, 0.000330283076937468, 0.00020217314260785892, 6.806833882366642e-05, -6.806833882366642e-05, -0.00020217314260785892, -0.000330283076937468, -0.00044873043154887367, -0.0005543170195608287, -0.0006444565838428643, -0.0007172766002977231, -0.0007716741568623991, -0.000807324365388313, -0.0008246434922938811, -0.0008247123187218102, -0.0008091678704258377, -0.0007800733924082353, -0.0007397771921888834, -0.0006907707569369895, -0.0006355554797131755, -0.0005765256000378637, -0.0005158728109596137, -0.00045551565997851024, -0.00039705461057473637],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q4": {
            "samples": [0.0, -0.0003016404369557931, -0.0006454247287418786, -0.0010321483299889263, -0.001461359128381175, -0.0019311466607611165, -0.0024379722156968858, -0.002976557809929544, -0.0035398506224075064, -0.0041190764297663355, -0.004703890947520788, -0.005282631952370203, -0.005842668028027387, -0.006370832278478575, -0.0068539220375979995, -0.007279239170309808, -0.0076351406802993675, -0.007911566581530187, -0.008100511749331867] + [-0.008196410904755673] * 2 + [-0.008100511749331867, -0.007911566581530187, -0.0076351406802993675, -0.007279239170309808, -0.0068539220375979995, -0.006370832278478575, -0.005842668028027387, -0.005282631952370203, -0.004703890947520788, -0.0041190764297663355, -0.0035398506224075064, -0.002976557809929544, -0.0024379722156968858, -0.0019311466607611165, -0.001461359128381175, -0.0010321483299889263, -0.0006454247287418786, -0.0003016404369557931, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q4": {
            "samples": [-0.00019852730528736819, -0.00022775782998925512, -0.00025793640547980685, -0.00028826280001893186, -0.00031777773985658777, -0.00034538537846849474, -0.0003698885960944417, -0.00039003669620411765, -0.00040458393521291885, -0.0004123561593609051, -0.00041232174614694056, -0.0004036621826941565, -0.00038583707843119956, -0.00035863830014886154, -0.00032222829192143216, -0.00027715850978041434, -0.00022436521577443684, -0.000165141538468734, -0.00010108657130392946, -3.403416941183321e-05, 3.403416941183321e-05, 0.00010108657130392946, 0.000165141538468734, 0.00022436521577443684, 0.00027715850978041434, 0.00032222829192143216, 0.00035863830014886154, 0.00038583707843119956, 0.0004036621826941565, 0.00041232174614694056, 0.0004123561593609051, 0.00040458393521291885, 0.00039003669620411765, 0.0003698885960944417, 0.00034538537846849474, 0.00031777773985658777, 0.00028826280001893186, 0.00025793640547980685, 0.00022775782998925512, 0.00019852730528736819],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q4": {
            "samples": [-0.00019852730528736819, -0.00022775782998925512, -0.00025793640547980685, -0.00028826280001893186, -0.00031777773985658777, -0.00034538537846849474, -0.0003698885960944417, -0.00039003669620411765, -0.00040458393521291885, -0.0004123561593609051, -0.00041232174614694056, -0.0004036621826941565, -0.00038583707843119956, -0.00035863830014886154, -0.00032222829192143216, -0.00027715850978041434, -0.00022436521577443684, -0.000165141538468734, -0.00010108657130392946, -3.403416941183321e-05, 3.403416941183321e-05, 0.00010108657130392946, 0.000165141538468734, 0.00022436521577443684, 0.00027715850978041434, 0.00032222829192143216, 0.00035863830014886154, 0.00038583707843119956, 0.0004036621826941565, 0.00041232174614694056, 0.0004123561593609051, 0.00040458393521291885, 0.00039003669620411765, 0.0003698885960944417, 0.00034538537846849474, 0.00031777773985658777, 0.00028826280001893186, 0.00025793640547980685, 0.00022775782998925512, 0.00019852730528736819],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q4": {
            "samples": [0.0, 0.0003016404369557931, 0.0006454247287418786, 0.0010321483299889263, 0.001461359128381175, 0.0019311466607611165, 0.0024379722156968858, 0.002976557809929544, 0.0035398506224075064, 0.0041190764297663355, 0.004703890947520788, 0.005282631952370203, 0.005842668028027387, 0.006370832278478575, 0.0068539220375979995, 0.007279239170309808, 0.0076351406802993675, 0.007911566581530187, 0.008100511749331867] + [0.008196410904755673] * 2 + [0.008100511749331867, 0.007911566581530187, 0.0076351406802993675, 0.007279239170309808, 0.0068539220375979995, 0.006370832278478575, 0.005842668028027387, 0.005282631952370203, 0.004703890947520788, 0.0041190764297663355, 0.0035398506224075064, 0.002976557809929544, 0.0024379722156968858, 0.0019311466607611165, 0.001461359128381175, 0.0010321483299889263, 0.0006454247287418786, 0.0003016404369557931, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q4": {
            "samples": [-0.00039705461057473637, -0.00045551565997851024, -0.0005158728109596137, -0.0005765256000378637, -0.0006355554797131755, -0.0006907707569369895, -0.0007397771921888834, -0.0007800733924082353, -0.0008091678704258377, -0.0008247123187218102, -0.0008246434922938811, -0.000807324365388313, -0.0007716741568623991, -0.0007172766002977231, -0.0006444565838428643, -0.0005543170195608287, -0.00044873043154887367, -0.000330283076937468, -0.00020217314260785892, -6.806833882366642e-05, 6.806833882366642e-05, 0.00020217314260785892, 0.000330283076937468, 0.00044873043154887367, 0.0005543170195608287, 0.0006444565838428643, 0.0007172766002977231, 0.0007716741568623991, 0.000807324365388313, 0.0008246434922938811, 0.0008247123187218102, 0.0008091678704258377, 0.0007800733924082353, 0.0007397771921888834, 0.0006907707569369895, 0.0006355554797131755, 0.0005765256000378637, 0.0005158728109596137, 0.00045551565997851024, 0.00039705461057473637],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q4": {
            "samples": [0.0, 0.0006032808739115862, 0.0012908494574837572, 0.0020642966599778525, 0.00292271825676235, 0.003862293321522233, 0.0048759444313937715, 0.005953115619859088, 0.007079701244815013, 0.008238152859532671, 0.009407781895041576, 0.010565263904740406, 0.011685336056054775, 0.01274166455695715, 0.013707844075195999, 0.014558478340619616, 0.015270281360598735, 0.015823133163060374, 0.016201023498663734] + [0.016392821809511345] * 2 + [0.016201023498663734, 0.015823133163060374, 0.015270281360598735, 0.014558478340619616, 0.013707844075195999, 0.01274166455695715, 0.011685336056054775, 0.010565263904740406, 0.009407781895041576, 0.008238152859532671, 0.007079701244815013, 0.005953115619859088, 0.0048759444313937715, 0.003862293321522233, 0.00292271825676235, 0.0020642966599778525, 0.0012908494574837572, 0.0006032808739115862, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q4": {
            "samples": [0.00019852730528736819, 0.00022775782998925512, 0.00025793640547980685, 0.00028826280001893186, 0.00031777773985658777, 0.00034538537846849474, 0.0003698885960944417, 0.00039003669620411765, 0.00040458393521291885, 0.0004123561593609051, 0.00041232174614694056, 0.0004036621826941565, 0.00038583707843119956, 0.00035863830014886154, 0.00032222829192143216, 0.00027715850978041434, 0.00022436521577443684, 0.000165141538468734, 0.00010108657130392946, 3.403416941183321e-05, -3.403416941183321e-05, -0.00010108657130392946, -0.000165141538468734, -0.00022436521577443684, -0.00027715850978041434, -0.00032222829192143216, -0.00035863830014886154, -0.00038583707843119956, -0.0004036621826941565, -0.00041232174614694056, -0.0004123561593609051, -0.00040458393521291885, -0.00039003669620411765, -0.0003698885960944417, -0.00034538537846849474, -0.00031777773985658777, -0.00028826280001893186, -0.00025793640547980685, -0.00022775782998925512, -0.00019852730528736819],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q4": {
            "samples": [0.0, -0.0003016404369557931, -0.0006454247287418786, -0.0010321483299889263, -0.001461359128381175, -0.0019311466607611165, -0.0024379722156968858, -0.002976557809929544, -0.0035398506224075064, -0.0041190764297663355, -0.004703890947520788, -0.005282631952370203, -0.005842668028027387, -0.006370832278478575, -0.0068539220375979995, -0.007279239170309808, -0.0076351406802993675, -0.007911566581530187, -0.008100511749331867] + [-0.008196410904755673] * 2 + [-0.008100511749331867, -0.007911566581530187, -0.0076351406802993675, -0.007279239170309808, -0.0068539220375979995, -0.006370832278478575, -0.005842668028027387, -0.005282631952370203, -0.004703890947520788, -0.0041190764297663355, -0.0035398506224075064, -0.002976557809929544, -0.0024379722156968858, -0.0019311466607611165, -0.001461359128381175, -0.0010321483299889263, -0.0006454247287418786, -0.0003016404369557931, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q4": {
            "sample": 0.012960000000000003,
            "type": "constant",
        },
        "x90_I_wf_q5": {
            "samples": [0.0, 0.00028036457944733903, 0.0005999004459244612, 0.0009593469475945237, 0.0013582838613582944, 0.0017949354763558167, 0.0022660126800516725, 0.00276660976559947, 0.0032901713744803033, 0.0038285421629731045, 0.004372107468671673, 0.004910027649636389, 0.005430562231841546, 0.00592147303097478, 0.006370488615614989, 0.006765806498879991, 0.007096604909663088, 0.007353533431346302, 0.007529151571420432] + [0.007618286591416743] * 2 + [0.007529151571420432, 0.007353533431346302, 0.007096604909663088, 0.006765806498879991, 0.006370488615614989, 0.00592147303097478, 0.005430562231841546, 0.004910027649636389, 0.004372107468671673, 0.0038285421629731045, 0.0032901713744803033, 0.00276660976559947, 0.0022660126800516725, 0.0017949354763558167, 0.0013582838613582944, 0.0009593469475945237, 0.0005999004459244612, 0.00028036457944733903, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q5": {
            "samples": [-0.0001917669927905499, -0.0002200021507284308, -0.00024915307613966657, -0.0002784467870200398, -0.00030695667510253024, -0.00033362420996374374, -0.000357293036531548, -0.0003767550473762665, -0.0003908069193547087, -0.00039831448134974986, -0.00039828123998506877, -0.0003899165546345292, -0.0003726984362717311, -0.00034642583910314014, -0.00031125567560776345, -0.0002677206234677183, -0.0002167250628501037, -0.00015951808831089304, -9.764434047196768e-05, -3.287522746951145e-05, 3.287522746951145e-05, 9.764434047196768e-05, 0.00015951808831089304, 0.0002167250628501037, 0.0002677206234677183, 0.00031125567560776345, 0.00034642583910314014, 0.0003726984362717311, 0.0003899165546345292, 0.00039828123998506877, 0.00039831448134974986, 0.0003908069193547087, 0.0003767550473762665, 0.000357293036531548, 0.00033362420996374374, 0.00030695667510253024, 0.0002784467870200398, 0.00024915307613966657, 0.0002200021507284308, 0.0001917669927905499],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q5": {
            "samples": [0.0, 0.0005720227975431103, 0.0012239660659042876, 0.0019573382838131976, 0.0027712820776554926, 0.003662174496572894, 0.004623304823549534, 0.005644664033337892, 0.006712877346119934, 0.007811305561111289, 0.00892033205592025, 0.010017840904494788, 0.011079878229316185, 0.012081474683539681, 0.012997593086843876, 0.01380415303799684, 0.014479075072484813, 0.015003281703834448, 0.015361592229302915] + [0.015543452803837182] * 2 + [0.015361592229302915, 0.015003281703834448, 0.014479075072484813, 0.01380415303799684, 0.012997593086843876, 0.012081474683539681, 0.011079878229316185, 0.010017840904494788, 0.00892033205592025, 0.007811305561111289, 0.006712877346119934, 0.005644664033337892, 0.004623304823549534, 0.003662174496572894, 0.0027712820776554926, 0.0019573382838131976, 0.0012239660659042876, 0.0005720227975431103, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q5": {
            "samples": [-0.0003912587385635993, -0.0004488664223321257, -0.0005083425299687457, -0.0005681099602241697, -0.0006262781709544071, -0.0006806874616178699, -0.000728978541805555, -0.0007686865317062597, -0.0007973563128022555, -0.0008126738562080496, -0.0008126060344509055, -0.000795539717713551, -0.0007604099011948913, -0.0007068063947864671, -0.0006350493441906633, -0.0005462255620801584, -0.0004421802390073616, -0.0003254618800784182, -0.00019922198771017775, -6.707473399116837e-05, 6.707473399116837e-05, 0.00019922198771017775, 0.0003254618800784182, 0.0004421802390073616, 0.0005462255620801584, 0.0006350493441906633, 0.0007068063947864671, 0.0007604099011948913, 0.000795539717713551, 0.0008126060344509055, 0.0008126738562080496, 0.0007973563128022555, 0.0007686865317062597, 0.000728978541805555, 0.0006806874616178699, 0.0006262781709544071, 0.0005681099602241697, 0.0005083425299687457, 0.0004488664223321257, 0.0003912587385635993],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q5": {
            "samples": [0.0, -0.00028036457944733903, -0.0005999004459244612, -0.0009593469475945237, -0.0013582838613582944, -0.0017949354763558167, -0.0022660126800516725, -0.00276660976559947, -0.0032901713744803033, -0.0038285421629731045, -0.004372107468671673, -0.004910027649636389, -0.005430562231841546, -0.00592147303097478, -0.006370488615614989, -0.006765806498879991, -0.007096604909663088, -0.007353533431346302, -0.007529151571420432] + [-0.007618286591416743] * 2 + [-0.007529151571420432, -0.007353533431346302, -0.007096604909663088, -0.006765806498879991, -0.006370488615614989, -0.00592147303097478, -0.005430562231841546, -0.004910027649636389, -0.004372107468671673, -0.0038285421629731045, -0.0032901713744803033, -0.00276660976559947, -0.0022660126800516725, -0.0017949354763558167, -0.0013582838613582944, -0.0009593469475945237, -0.0005999004459244612, -0.00028036457944733903, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q5": {
            "samples": [0.0001917669927905499, 0.0002200021507284308, 0.00024915307613966657, 0.0002784467870200398, 0.00030695667510253024, 0.00033362420996374374, 0.000357293036531548, 0.0003767550473762665, 0.0003908069193547087, 0.00039831448134974986, 0.00039828123998506877, 0.0003899165546345292, 0.0003726984362717311, 0.00034642583910314014, 0.00031125567560776345, 0.0002677206234677183, 0.0002167250628501037, 0.00015951808831089304, 9.764434047196768e-05, 3.287522746951145e-05, -3.287522746951145e-05, -9.764434047196768e-05, -0.00015951808831089304, -0.0002167250628501037, -0.0002677206234677183, -0.00031125567560776345, -0.00034642583910314014, -0.0003726984362717311, -0.0003899165546345292, -0.00039828123998506877, -0.00039831448134974986, -0.0003908069193547087, -0.0003767550473762665, -0.000357293036531548, -0.00033362420996374374, -0.00030695667510253024, -0.0002784467870200398, -0.00024915307613966657, -0.0002200021507284308, -0.0001917669927905499],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q5": {
            "samples": [0.00019562936928179964, 0.00022443321116606284, 0.00025417126498437285, 0.00028405498011208486, 0.00031313908547720353, 0.00034034373080893496, 0.0003644892709027775, 0.00038434326585312986, 0.00039867815640112775, 0.0004063369281040248, 0.00040630301722545273, 0.0003977698588567755, 0.00038020495059744563, 0.00035340319739323356, 0.00031752467209533166, 0.0002731127810400792, 0.0002210901195036808, 0.0001627309400392091, 9.961099385508887e-05, 3.3537366995584185e-05, -3.3537366995584185e-05, -9.961099385508887e-05, -0.0001627309400392091, -0.0002210901195036808, -0.0002731127810400792, -0.00031752467209533166, -0.00035340319739323356, -0.00038020495059744563, -0.0003977698588567755, -0.00040630301722545273, -0.0004063369281040248, -0.00039867815640112775, -0.00038434326585312986, -0.0003644892709027775, -0.00034034373080893496, -0.00031313908547720353, -0.00028405498011208486, -0.00025417126498437285, -0.00022443321116606284, -0.00019562936928179964],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q5": {
            "samples": [0.0, 0.00028601139877155513, 0.0006119830329521438, 0.0009786691419065988, 0.0013856410388277463, 0.001831087248286447, 0.002311652411774767, 0.002822332016668946, 0.003356438673059967, 0.0039056527805556443, 0.004460166027960125, 0.005008920452247394, 0.005539939114658093, 0.006040737341769841, 0.006498796543421938, 0.00690207651899842, 0.007239537536242406, 0.007501640851917224, 0.007680796114651458] + [0.007771726401918591] * 2 + [0.007680796114651458, 0.007501640851917224, 0.007239537536242406, 0.00690207651899842, 0.006498796543421938, 0.006040737341769841, 0.005539939114658093, 0.005008920452247394, 0.004460166027960125, 0.0039056527805556443, 0.003356438673059967, 0.002822332016668946, 0.002311652411774767, 0.001831087248286447, 0.0013856410388277463, 0.0009786691419065988, 0.0006119830329521438, 0.00028601139877155513, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q5": {
            "samples": [0.0003912587385635993, 0.0004488664223321257, 0.0005083425299687457, 0.0005681099602241697, 0.0006262781709544071, 0.0006806874616178699, 0.000728978541805555, 0.0007686865317062597, 0.0007973563128022555, 0.0008126738562080496, 0.0008126060344509055, 0.000795539717713551, 0.0007604099011948913, 0.0007068063947864671, 0.0006350493441906633, 0.0005462255620801584, 0.0004421802390073616, 0.0003254618800784182, 0.00019922198771017775, 6.707473399116837e-05, -6.707473399116837e-05, -0.00019922198771017775, -0.0003254618800784182, -0.0004421802390073616, -0.0005462255620801584, -0.0006350493441906633, -0.0007068063947864671, -0.0007604099011948913, -0.000795539717713551, -0.0008126060344509055, -0.0008126738562080496, -0.0007973563128022555, -0.0007686865317062597, -0.000728978541805555, -0.0006806874616178699, -0.0006262781709544071, -0.0005681099602241697, -0.0005083425299687457, -0.0004488664223321257, -0.0003912587385635993],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q5": {
            "samples": [0.0, 0.0005720227975431103, 0.0012239660659042876, 0.0019573382838131976, 0.0027712820776554926, 0.003662174496572894, 0.004623304823549534, 0.005644664033337892, 0.006712877346119934, 0.007811305561111289, 0.00892033205592025, 0.010017840904494788, 0.011079878229316185, 0.012081474683539681, 0.012997593086843876, 0.01380415303799684, 0.014479075072484813, 0.015003281703834448, 0.015361592229302915] + [0.015543452803837182] * 2 + [0.015361592229302915, 0.015003281703834448, 0.014479075072484813, 0.01380415303799684, 0.012997593086843876, 0.012081474683539681, 0.011079878229316185, 0.010017840904494788, 0.00892033205592025, 0.007811305561111289, 0.006712877346119934, 0.005644664033337892, 0.004623304823549534, 0.003662174496572894, 0.0027712820776554926, 0.0019573382838131976, 0.0012239660659042876, 0.0005720227975431103, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q5": {
            "samples": [-0.00019562936928179964, -0.00022443321116606284, -0.00025417126498437285, -0.00028405498011208486, -0.00031313908547720353, -0.00034034373080893496, -0.0003644892709027775, -0.00038434326585312986, -0.00039867815640112775, -0.0004063369281040248, -0.00040630301722545273, -0.0003977698588567755, -0.00038020495059744563, -0.00035340319739323356, -0.00031752467209533166, -0.0002731127810400792, -0.0002210901195036808, -0.0001627309400392091, -9.961099385508887e-05, -3.3537366995584185e-05, 3.3537366995584185e-05, 9.961099385508887e-05, 0.0001627309400392091, 0.0002210901195036808, 0.0002731127810400792, 0.00031752467209533166, 0.00035340319739323356, 0.00038020495059744563, 0.0003977698588567755, 0.00040630301722545273, 0.0004063369281040248, 0.00039867815640112775, 0.00038434326585312986, 0.0003644892709027775, 0.00034034373080893496, 0.00031313908547720353, 0.00028405498011208486, 0.00025417126498437285, 0.00022443321116606284, 0.00019562936928179964],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q5": {
            "samples": [0.0, -0.00028601139877155513, -0.0006119830329521438, -0.0009786691419065988, -0.0013856410388277463, -0.001831087248286447, -0.002311652411774767, -0.002822332016668946, -0.003356438673059967, -0.0039056527805556443, -0.004460166027960125, -0.005008920452247394, -0.005539939114658093, -0.006040737341769841, -0.006498796543421938, -0.00690207651899842, -0.007239537536242406, -0.007501640851917224, -0.007680796114651458] + [-0.007771726401918591] * 2 + [-0.007680796114651458, -0.007501640851917224, -0.007239537536242406, -0.00690207651899842, -0.006498796543421938, -0.006040737341769841, -0.005539939114658093, -0.005008920452247394, -0.004460166027960125, -0.0039056527805556443, -0.003356438673059967, -0.002822332016668946, -0.002311652411774767, -0.001831087248286447, -0.0013856410388277463, -0.0009786691419065988, -0.0006119830329521438, -0.00028601139877155513, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q5": {
            "sample": 0.014400000000000003,
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
            "samples": [0.0] + [0.197654568417] * 27,
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
            "samples": [0.0] + [0.045] * 31,
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
            "cosine": [(1.0, 600)],
            "sine": [(0.0, 600)],
        },
        "sine_weights": {
            "cosine": [(0.0, 600)],
            "sine": [(1.0, 600)],
        },
        "minus_sine_weights": {
            "cosine": [(0.0, 600)],
            "sine": [(-1.0, 600)],
        },
        "rotated_cosine_weights_q1": {
            "cosine": [(-0.6401096994849559, 600)],
            "sine": [(-0.768283523593523, 600)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(0.768283523593523, 600)],
            "sine": [(-0.6401096994849559, 600)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(-0.768283523593523, 600)],
            "sine": [(0.6401096994849559, 600)],
        },
        "rotated_cosine_weights_q2": {
            "cosine": [(0.2469990127227423, 600)],
            "sine": [(-0.9690157314068697, 600)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(0.9690157314068697, 600)],
            "sine": [(0.2469990127227423, 600)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(-0.9690157314068697, 600)],
            "sine": [(-0.2469990127227423, 600)],
        },
        "rotated_cosine_weights_q3": {
            "cosine": [(-0.05756402695956744, 600)],
            "sine": [(-0.9983418166140283, 600)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(0.9983418166140283, 600)],
            "sine": [(-0.05756402695956744, 600)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(-0.9983418166140283, 600)],
            "sine": [(0.05756402695956744, 600)],
        },
        "rotated_cosine_weights_q4": {
            "cosine": [(-0.894934361602025, 600)],
            "sine": [(0.446197813109809, 600)],
        },
        "rotated_sine_weights_q4": {
            "cosine": [(-0.446197813109809, 600)],
            "sine": [(-0.894934361602025, 600)],
        },
        "rotated_minus_sine_weights_q4": {
            "cosine": [(0.446197813109809, 600)],
            "sine": [(0.894934361602025, 600)],
        },
        "rotated_cosine_weights_q5": {
            "cosine": [(-0.11146893220632534, 600)],
            "sine": [(0.9937679191605964, 600)],
        },
        "rotated_sine_weights_q5": {
            "cosine": [(-0.9937679191605964, 600)],
            "sine": [(-0.11146893220632534, 600)],
        },
        "rotated_minus_sine_weights_q5": {
            "cosine": [(0.9937679191605964, 600)],
            "sine": [(0.11146893220632534, 600)],
        },
        "opt_cosine_weights_q1": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_sine_weights_q1": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_minus_sine_weights_q1": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_cosine_weights_q2": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_sine_weights_q2": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_minus_sine_weights_q2": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_cosine_weights_q3": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_sine_weights_q3": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_minus_sine_weights_q3": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_cosine_weights_q4": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_sine_weights_q4": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_minus_sine_weights_q4": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_cosine_weights_q5": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_sine_weights_q5": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
        "opt_minus_sine_weights_q5": {
            "cosine": [(1.0, 600)],
            "sine": [(1.0, 600)],
        },
    },
    "mixers": {
        "rr1_mixer_6a7": [{'intermediate_frequency': 33900000.0, 'lo_frequency': 5880000000.0, 'correction': [1, 0.0, 0.0, 1]}],
        "rr2_mixer_4a4": [{'intermediate_frequency': 133700000.0, 'lo_frequency': 5880000000.0, 'correction': [1, 0.0, 0.0, 1]}],
        "rr3_mixer_012": [{'intermediate_frequency': -23300000.0, 'lo_frequency': 5880000000.0, 'correction': [1, 0.0, 0.0, 1]}],
        "rr4_mixer_d71": [{'intermediate_frequency': 157500000.0, 'lo_frequency': 5880000000.0, 'correction': [1, 0.0, 0.0, 1]}],
        "rr5_mixer_bdd": [{'intermediate_frequency': 62300000.0, 'lo_frequency': 5880000000.0, 'correction': [1, 0.0, 0.0, 1]}],
        "q1_xy_mixer_2d4": [{'intermediate_frequency': -116000000.0, 'lo_frequency': 5200000000.0, 'correction': [1, 0.0, 0.0, 1]}],
        "q2_xy_mixer_4be": [{'intermediate_frequency': -64000000.0, 'lo_frequency': 4500000000.0, 'correction': [1, 0.0, 0.0, 1]}],
        "q3_xy_mixer_6c3": [{'intermediate_frequency': -58000000.0, 'lo_frequency': 4500000000.0, 'correction': [1, 0.0, 0.0, 1]}],
        "q4_xy_mixer_b68": [{'intermediate_frequency': -85000000.0, 'lo_frequency': 4500000000.0, 'correction': [1, 0.0, 0.0, 1]}],
        "q00_xy_mixer_809": [{'intermediate_frequency': -85000000.0, 'lo_frequency': 4500000000.0, 'correction': [1, 0.0, 0.0, 1]}],
        "q5_xy_mixer_37f": [{'intermediate_frequency': -138450000.0, 'lo_frequency': 4500000000.0, 'correction': [1, 0.0, 0.0, 1]}],
    },
}




# Single QUA script generated at 2023-11-07 08:50:36.361962
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
    with for_(v1,0,(v1<8888),(v1+1)):
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
                wait(250, )
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
                    "offset": 0.02001953125,
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
                    "offset": 0.01824951171875,
                },
                "8": {
                    "offset": -0.00244140625,
                },
                "9": {
                    "offset": 0.0092620849609375,
                },
                "10": {
                    "offset": -0.0152587890625,
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
                    "offset": -0.203,
                },
                "6": {
                    "offset": 0.044,
                },
                "7": {
                    "offset": -0.116,
                },
                "8": {
                    "offset": 0.033,
                },
                "9": {
                    "offset": 0.037,
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
            "intermediate_frequency": -135196000,
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
                "lo_frequency": 4000000000,
                "mixer": "octave_octave1_4",
            },
            "intermediate_frequency": -146495000,
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
            "intermediate_frequency": -261338000,
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
                "lo_frequency": 4000000000,
                "mixer": "octave_octave1_5",
            },
            "intermediate_frequency": -408869000,
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
                "lo_frequency": 4500000000,
                "mixer": "octave_octave2_1",
            },
            "intermediate_frequency": -24184000,
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
            },
        },
        "q2_z": {
            "singleInput": {
                "port": ('con2', 6),
            },
            "operations": {
                "const": "const_flux_pulse",
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
            },
        },
        "q5_z": {
            "singleInput": {
                "port": ('con2', 9),
            },
            "operations": {
                "const": "const_flux_pulse",
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
            "length": 5000,
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
            "length": 5000,
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
            "length": 5000,
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
            "length": 5000,
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
            "length": 5000,
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
            "sample": 0.45,
        },
        "zero_wf": {
            "type": "constant",
            "sample": 0.0,
        },
        "x90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.00035978111044912813, 0.0007808391551694244, 0.0012635055740989535, 0.0018050046782114443, 0.0023989478788327924, 0.0030350266985779938, 0.0036989763122425925, 0.00437286358509065, 0.005035725304558076, 0.005664545904127425, 0.006235523550118227, 0.006725534365759936, 0.007113672653213481, 0.007382725607871725] + [0.007520438086002945] * 2 + [0.007382725607871725, 0.007113672653213481, 0.006725534365759936, 0.006235523550118227, 0.005664545904127425, 0.005035725304558076, 0.00437286358509065, 0.0036989763122425925, 0.0030350266985779938, 0.0023989478788327924, 0.0018050046782114443, 0.0012635055740989535, 0.0007808391551694244, 0.00035978111044912813, 0.0],
        },
        "x90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "x180_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007195622208982563, 0.0015616783103388487, 0.002527011148197907, 0.0036100093564228886, 0.004797895757665585, 0.0060700533971559875, 0.007397952624485185, 0.0087457271701813, 0.010071450609116153, 0.01132909180825485, 0.012471047100236454, 0.013451068731519873, 0.014227345306426963, 0.01476545121574345] + [0.01504087617200589] * 2 + [0.01476545121574345, 0.014227345306426963, 0.013451068731519873, 0.012471047100236454, 0.01132909180825485, 0.010071450609116153, 0.0087457271701813, 0.007397952624485185, 0.0060700533971559875, 0.004797895757665585, 0.0036100093564228886, 0.002527011148197907, 0.0015616783103388487, 0.0007195622208982563, 0.0],
        },
        "x180_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "minus_x90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, -0.00035978111044912813, -0.0007808391551694244, -0.0012635055740989535, -0.0018050046782114443, -0.0023989478788327924, -0.0030350266985779938, -0.0036989763122425925, -0.00437286358509065, -0.005035725304558076, -0.005664545904127425, -0.006235523550118227, -0.006725534365759936, -0.007113672653213481, -0.007382725607871725] + [-0.007520438086002945] * 2 + [-0.007382725607871725, -0.007113672653213481, -0.006725534365759936, -0.006235523550118227, -0.005664545904127425, -0.005035725304558076, -0.00437286358509065, -0.0036989763122425925, -0.0030350266985779938, -0.0023989478788327924, -0.0018050046782114443, -0.0012635055740989535, -0.0007808391551694244, -0.00035978111044912813, 0.0],
        },
        "minus_x90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "y90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "y90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.00035978111044912813, 0.0007808391551694244, 0.0012635055740989535, 0.0018050046782114443, 0.0023989478788327924, 0.0030350266985779938, 0.0036989763122425925, 0.00437286358509065, 0.005035725304558076, 0.005664545904127425, 0.006235523550118227, 0.006725534365759936, 0.007113672653213481, 0.007382725607871725] + [0.007520438086002945] * 2 + [0.007382725607871725, 0.007113672653213481, 0.006725534365759936, 0.006235523550118227, 0.005664545904127425, 0.005035725304558076, 0.00437286358509065, 0.0036989763122425925, 0.0030350266985779938, 0.0023989478788327924, 0.0018050046782114443, 0.0012635055740989535, 0.0007808391551694244, 0.00035978111044912813, 0.0],
        },
        "y180_I_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "y180_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007195622208982563, 0.0015616783103388487, 0.002527011148197907, 0.0036100093564228886, 0.004797895757665585, 0.0060700533971559875, 0.007397952624485185, 0.0087457271701813, 0.010071450609116153, 0.01132909180825485, 0.012471047100236454, 0.013451068731519873, 0.014227345306426963, 0.01476545121574345] + [0.01504087617200589] * 2 + [0.01476545121574345, 0.014227345306426963, 0.013451068731519873, 0.012471047100236454, 0.01132909180825485, 0.010071450609116153, 0.0087457271701813, 0.007397952624485185, 0.0060700533971559875, 0.004797895757665585, 0.0036100093564228886, 0.002527011148197907, 0.0015616783103388487, 0.0007195622208982563, 0.0],
        },
        "minus_y90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "minus_y90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, -0.00035978111044912813, -0.0007808391551694244, -0.0012635055740989535, -0.0018050046782114443, -0.0023989478788327924, -0.0030350266985779938, -0.0036989763122425925, -0.00437286358509065, -0.005035725304558076, -0.005664545904127425, -0.006235523550118227, -0.006725534365759936, -0.007113672653213481, -0.007382725607871725] + [-0.007520438086002945] * 2 + [-0.007382725607871725, -0.007113672653213481, -0.006725534365759936, -0.006235523550118227, -0.005664545904127425, -0.005035725304558076, -0.00437286358509065, -0.0036989763122425925, -0.0030350266985779938, -0.0023989478788327924, -0.0018050046782114443, -0.0012635055740989535, -0.0007808391551694244, -0.00035978111044912813, 0.0],
        },
        "readout_wf_q1": {
            "type": "constant",
            "sample": 0.07030871999999999,
        },
        "x90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0015442290358603028, 0.003351466935671013, 0.005423136284334835, 0.007747323450300807, 0.010296607749596929, 0.013026743807379702, 0.015876505070524388, 0.01876892010679358, 0.021614011981361633, 0.024312994779513215, 0.026763707821855758, 0.028866900311463998, 0.03053284217446686, 0.031687653732662906] + [0.03227873425677668] * 2 + [0.031687653732662906, 0.03053284217446686, 0.028866900311463998, 0.026763707821855758, 0.024312994779513215, 0.021614011981361633, 0.01876892010679358, 0.015876505070524388, 0.013026743807379702, 0.010296607749596929, 0.007747323450300807, 0.005423136284334835, 0.003351466935671013, 0.0015442290358603028, 0.0],
        },
        "x90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "x180_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0030884580717206057, 0.006702933871342026, 0.01084627256866967, 0.015494646900601613, 0.020593215499193858, 0.026053487614759403, 0.031753010141048775, 0.03753784021358716, 0.043228023962723267, 0.04862598955902643, 0.053527415643711516, 0.057733800622927996, 0.06106568434893372, 0.06337530746532581] + [0.06455746851355336] * 2 + [0.06337530746532581, 0.06106568434893372, 0.057733800622927996, 0.053527415643711516, 0.04862598955902643, 0.043228023962723267, 0.03753784021358716, 0.031753010141048775, 0.026053487614759403, 0.020593215499193858, 0.015494646900601613, 0.01084627256866967, 0.006702933871342026, 0.0030884580717206057, 0.0],
        },
        "x180_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "minus_x90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, -0.0015442290358603028, -0.003351466935671013, -0.005423136284334835, -0.007747323450300807, -0.010296607749596929, -0.013026743807379702, -0.015876505070524388, -0.01876892010679358, -0.021614011981361633, -0.024312994779513215, -0.026763707821855758, -0.028866900311463998, -0.03053284217446686, -0.031687653732662906] + [-0.03227873425677668] * 2 + [-0.031687653732662906, -0.03053284217446686, -0.028866900311463998, -0.026763707821855758, -0.024312994779513215, -0.021614011981361633, -0.01876892010679358, -0.015876505070524388, -0.013026743807379702, -0.010296607749596929, -0.007747323450300807, -0.005423136284334835, -0.003351466935671013, -0.0015442290358603028, 0.0],
        },
        "minus_x90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "y90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "y90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0015442290358603028, 0.003351466935671013, 0.005423136284334835, 0.007747323450300807, 0.010296607749596929, 0.013026743807379702, 0.015876505070524388, 0.01876892010679358, 0.021614011981361633, 0.024312994779513215, 0.026763707821855758, 0.028866900311463998, 0.03053284217446686, 0.031687653732662906] + [0.03227873425677668] * 2 + [0.031687653732662906, 0.03053284217446686, 0.028866900311463998, 0.026763707821855758, 0.024312994779513215, 0.021614011981361633, 0.01876892010679358, 0.015876505070524388, 0.013026743807379702, 0.010296607749596929, 0.007747323450300807, 0.005423136284334835, 0.003351466935671013, 0.0015442290358603028, 0.0],
        },
        "y180_I_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "y180_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0030884580717206057, 0.006702933871342026, 0.01084627256866967, 0.015494646900601613, 0.020593215499193858, 0.026053487614759403, 0.031753010141048775, 0.03753784021358716, 0.043228023962723267, 0.04862598955902643, 0.053527415643711516, 0.057733800622927996, 0.06106568434893372, 0.06337530746532581] + [0.06455746851355336] * 2 + [0.06337530746532581, 0.06106568434893372, 0.057733800622927996, 0.053527415643711516, 0.04862598955902643, 0.043228023962723267, 0.03753784021358716, 0.031753010141048775, 0.026053487614759403, 0.020593215499193858, 0.015494646900601613, 0.01084627256866967, 0.006702933871342026, 0.0030884580717206057, 0.0],
        },
        "minus_y90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "minus_y90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, -0.0015442290358603028, -0.003351466935671013, -0.005423136284334835, -0.007747323450300807, -0.010296607749596929, -0.013026743807379702, -0.015876505070524388, -0.01876892010679358, -0.021614011981361633, -0.024312994779513215, -0.026763707821855758, -0.028866900311463998, -0.03053284217446686, -0.031687653732662906] + [-0.03227873425677668] * 2 + [-0.031687653732662906, -0.03053284217446686, -0.028866900311463998, -0.026763707821855758, -0.024312994779513215, -0.021614011981361633, -0.01876892010679358, -0.015876505070524388, -0.013026743807379702, -0.010296607749596929, -0.007747323450300807, -0.005423136284334835, -0.003351466935671013, -0.0015442290358603028, 0.0],
        },
        "readout_wf_q2": {
            "type": "constant",
            "sample": 0.08532,
        },
        "x90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.00043699256224214345, 0.0009484125019529751, 0.0015346623883156954, 0.002192370850726485, 0.002913778266312639, 0.0036863638889469783, 0.004492801565768812, 0.005311309590430329, 0.006116425903626158, 0.006880195643103085, 0.007573708941211014, 0.008168879381333136, 0.008640314761936826, 0.008967108294504872] + [0.009134374798841778] * 2 + [0.008967108294504872, 0.008640314761936826, 0.008168879381333136, 0.007573708941211014, 0.006880195643103085, 0.006116425903626158, 0.005311309590430329, 0.004492801565768812, 0.0036863638889469783, 0.002913778266312639, 0.002192370850726485, 0.0015346623883156954, 0.0009484125019529751, 0.00043699256224214345, 0.0],
        },
        "x90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "x180_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0008739851244842869, 0.0018968250039059502, 0.0030693247766313907, 0.00438474170145297, 0.005827556532625278, 0.007372727777893957, 0.008985603131537625, 0.010622619180860658, 0.012232851807252317, 0.01376039128620617, 0.015147417882422028, 0.01633775876266627, 0.01728062952387365, 0.017934216589009743] + [0.018268749597683556] * 2 + [0.017934216589009743, 0.01728062952387365, 0.01633775876266627, 0.015147417882422028, 0.01376039128620617, 0.012232851807252317, 0.010622619180860658, 0.008985603131537625, 0.007372727777893957, 0.005827556532625278, 0.00438474170145297, 0.0030693247766313907, 0.0018968250039059502, 0.0008739851244842869, 0.0],
        },
        "x180_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "minus_x90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, -0.00043699256224214345, -0.0009484125019529751, -0.0015346623883156954, -0.002192370850726485, -0.002913778266312639, -0.0036863638889469783, -0.004492801565768812, -0.005311309590430329, -0.006116425903626158, -0.006880195643103085, -0.007573708941211014, -0.008168879381333136, -0.008640314761936826, -0.008967108294504872] + [-0.009134374798841778] * 2 + [-0.008967108294504872, -0.008640314761936826, -0.008168879381333136, -0.007573708941211014, -0.006880195643103085, -0.006116425903626158, -0.005311309590430329, -0.004492801565768812, -0.0036863638889469783, -0.002913778266312639, -0.002192370850726485, -0.0015346623883156954, -0.0009484125019529751, -0.00043699256224214345, 0.0],
        },
        "minus_x90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "y90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "y90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.00043699256224214345, 0.0009484125019529751, 0.0015346623883156954, 0.002192370850726485, 0.002913778266312639, 0.0036863638889469783, 0.004492801565768812, 0.005311309590430329, 0.006116425903626158, 0.006880195643103085, 0.007573708941211014, 0.008168879381333136, 0.008640314761936826, 0.008967108294504872] + [0.009134374798841778] * 2 + [0.008967108294504872, 0.008640314761936826, 0.008168879381333136, 0.007573708941211014, 0.006880195643103085, 0.006116425903626158, 0.005311309590430329, 0.004492801565768812, 0.0036863638889469783, 0.002913778266312639, 0.002192370850726485, 0.0015346623883156954, 0.0009484125019529751, 0.00043699256224214345, 0.0],
        },
        "y180_I_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "y180_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0008739851244842869, 0.0018968250039059502, 0.0030693247766313907, 0.00438474170145297, 0.005827556532625278, 0.007372727777893957, 0.008985603131537625, 0.010622619180860658, 0.012232851807252317, 0.01376039128620617, 0.015147417882422028, 0.01633775876266627, 0.01728062952387365, 0.017934216589009743] + [0.018268749597683556] * 2 + [0.017934216589009743, 0.01728062952387365, 0.01633775876266627, 0.015147417882422028, 0.01376039128620617, 0.012232851807252317, 0.010622619180860658, 0.008985603131537625, 0.007372727777893957, 0.005827556532625278, 0.00438474170145297, 0.0030693247766313907, 0.0018968250039059502, 0.0008739851244842869, 0.0],
        },
        "minus_y90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "minus_y90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, -0.00043699256224214345, -0.0009484125019529751, -0.0015346623883156954, -0.002192370850726485, -0.002913778266312639, -0.0036863638889469783, -0.004492801565768812, -0.005311309590430329, -0.006116425903626158, -0.006880195643103085, -0.007573708941211014, -0.008168879381333136, -0.008640314761936826, -0.008967108294504872] + [-0.009134374798841778] * 2 + [-0.008967108294504872, -0.008640314761936826, -0.008168879381333136, -0.007573708941211014, -0.006880195643103085, -0.006116425903626158, -0.005311309590430329, -0.004492801565768812, -0.0036863638889469783, -0.002913778266312639, -0.002192370850726485, -0.0015346623883156954, -0.0009484125019529751, -0.00043699256224214345, 0.0],
        },
        "readout_wf_q3": {
            "type": "constant",
            "sample": 0.07729910999999999,
        },
        "x90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.002277939952113301, 0.004943852403797425, 0.007999835853986073, 0.011428316136765718, 0.015188844154182906, 0.019216152187064038, 0.023419923055603382, 0.027686613822455967, 0.031883496731668265, 0.03586484962894161, 0.039479972140355285, 0.042582456349502515, 0.04503993865264941, 0.04674343685433391] + [0.047615357993962465] * 2 + [0.04674343685433391, 0.04503993865264941, 0.042582456349502515, 0.039479972140355285, 0.03586484962894161, 0.031883496731668265, 0.027686613822455967, 0.023419923055603382, 0.019216152187064038, 0.015188844154182906, 0.011428316136765718, 0.007999835853986073, 0.004943852403797425, 0.002277939952113301, 0.0],
        },
        "x90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "x180_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.004555879904226602, 0.00988770480759485, 0.015999671707972146, 0.022856632273531435, 0.030377688308365812, 0.038432304374128076, 0.046839846111206764, 0.05537322764491193, 0.06376699346333653, 0.07172969925788322, 0.07895994428071057, 0.08516491269900503, 0.09007987730529882, 0.09348687370866782] + [0.09523071598792493] * 2 + [0.09348687370866782, 0.09007987730529882, 0.08516491269900503, 0.07895994428071057, 0.07172969925788322, 0.06376699346333653, 0.05537322764491193, 0.046839846111206764, 0.038432304374128076, 0.030377688308365812, 0.022856632273531435, 0.015999671707972146, 0.00988770480759485, 0.004555879904226602, 0.0],
        },
        "x180_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "minus_x90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, -0.002277939952113301, -0.004943852403797425, -0.007999835853986073, -0.011428316136765718, -0.015188844154182906, -0.019216152187064038, -0.023419923055603382, -0.027686613822455967, -0.031883496731668265, -0.03586484962894161, -0.039479972140355285, -0.042582456349502515, -0.04503993865264941, -0.04674343685433391] + [-0.047615357993962465] * 2 + [-0.04674343685433391, -0.04503993865264941, -0.042582456349502515, -0.039479972140355285, -0.03586484962894161, -0.031883496731668265, -0.027686613822455967, -0.023419923055603382, -0.019216152187064038, -0.015188844154182906, -0.011428316136765718, -0.007999835853986073, -0.004943852403797425, -0.002277939952113301, 0.0],
        },
        "minus_x90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "y90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "y90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.002277939952113301, 0.004943852403797425, 0.007999835853986073, 0.011428316136765718, 0.015188844154182906, 0.019216152187064038, 0.023419923055603382, 0.027686613822455967, 0.031883496731668265, 0.03586484962894161, 0.039479972140355285, 0.042582456349502515, 0.04503993865264941, 0.04674343685433391] + [0.047615357993962465] * 2 + [0.04674343685433391, 0.04503993865264941, 0.042582456349502515, 0.039479972140355285, 0.03586484962894161, 0.031883496731668265, 0.027686613822455967, 0.023419923055603382, 0.019216152187064038, 0.015188844154182906, 0.011428316136765718, 0.007999835853986073, 0.004943852403797425, 0.002277939952113301, 0.0],
        },
        "y180_I_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "y180_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.004555879904226602, 0.00988770480759485, 0.015999671707972146, 0.022856632273531435, 0.030377688308365812, 0.038432304374128076, 0.046839846111206764, 0.05537322764491193, 0.06376699346333653, 0.07172969925788322, 0.07895994428071057, 0.08516491269900503, 0.09007987730529882, 0.09348687370866782] + [0.09523071598792493] * 2 + [0.09348687370866782, 0.09007987730529882, 0.08516491269900503, 0.07895994428071057, 0.07172969925788322, 0.06376699346333653, 0.05537322764491193, 0.046839846111206764, 0.038432304374128076, 0.030377688308365812, 0.022856632273531435, 0.015999671707972146, 0.00988770480759485, 0.004555879904226602, 0.0],
        },
        "minus_y90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "minus_y90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, -0.002277939952113301, -0.004943852403797425, -0.007999835853986073, -0.011428316136765718, -0.015188844154182906, -0.019216152187064038, -0.023419923055603382, -0.027686613822455967, -0.031883496731668265, -0.03586484962894161, -0.039479972140355285, -0.042582456349502515, -0.04503993865264941, -0.04674343685433391] + [-0.047615357993962465] * 2 + [-0.04674343685433391, -0.04503993865264941, -0.042582456349502515, -0.039479972140355285, -0.03586484962894161, -0.031883496731668265, -0.027686613822455967, -0.023419923055603382, -0.019216152187064038, -0.015188844154182906, -0.011428316136765718, -0.007999835853986073, -0.004943852403797425, -0.002277939952113301, 0.0],
        },
        "readout_wf_q4": {
            "type": "constant",
            "sample": 0.11668859999999999,
        },
        "x90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.003161222790687845, 0.006860856397106627, 0.011101813021858222, 0.01585970402653202, 0.021078395969070157, 0.026667313239190908, 0.032501117709816944, 0.03842223959034707, 0.04424648526027434, 0.04977162805649041, 0.05478853276620734, 0.059094021056452485, 0.06250440466081958, 0.06486844298152461] + [0.06607845599162138] * 2 + [0.06486844298152461, 0.06250440466081958, 0.059094021056452485, 0.05478853276620734, 0.04977162805649041, 0.04424648526027434, 0.03842223959034707, 0.032501117709816944, 0.026667313239190908, 0.021078395969070157, 0.01585970402653202, 0.011101813021858222, 0.006860856397106627, 0.003161222790687845, 0.0],
        },
        "x90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "x180_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.00632244558137569, 0.013721712794213255, 0.022203626043716444, 0.03171940805306404, 0.042156791938140314, 0.053334626478381816, 0.06500223541963389, 0.07684447918069413, 0.08849297052054868, 0.09954325611298082, 0.10957706553241468, 0.11818804211290497, 0.12500880932163916, 0.12973688596304922] + [0.13215691198324275] * 2 + [0.12973688596304922, 0.12500880932163916, 0.11818804211290497, 0.10957706553241468, 0.09954325611298082, 0.08849297052054868, 0.07684447918069413, 0.06500223541963389, 0.053334626478381816, 0.042156791938140314, 0.03171940805306404, 0.022203626043716444, 0.013721712794213255, 0.00632244558137569, 0.0],
        },
        "x180_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "minus_x90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, -0.003161222790687845, -0.006860856397106627, -0.011101813021858222, -0.01585970402653202, -0.021078395969070157, -0.026667313239190908, -0.032501117709816944, -0.03842223959034707, -0.04424648526027434, -0.04977162805649041, -0.05478853276620734, -0.059094021056452485, -0.06250440466081958, -0.06486844298152461] + [-0.06607845599162138] * 2 + [-0.06486844298152461, -0.06250440466081958, -0.059094021056452485, -0.05478853276620734, -0.04977162805649041, -0.04424648526027434, -0.03842223959034707, -0.032501117709816944, -0.026667313239190908, -0.021078395969070157, -0.01585970402653202, -0.011101813021858222, -0.006860856397106627, -0.003161222790687845, 0.0],
        },
        "minus_x90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "y90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "y90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.003161222790687845, 0.006860856397106627, 0.011101813021858222, 0.01585970402653202, 0.021078395969070157, 0.026667313239190908, 0.032501117709816944, 0.03842223959034707, 0.04424648526027434, 0.04977162805649041, 0.05478853276620734, 0.059094021056452485, 0.06250440466081958, 0.06486844298152461] + [0.06607845599162138] * 2 + [0.06486844298152461, 0.06250440466081958, 0.059094021056452485, 0.05478853276620734, 0.04977162805649041, 0.04424648526027434, 0.03842223959034707, 0.032501117709816944, 0.026667313239190908, 0.021078395969070157, 0.01585970402653202, 0.011101813021858222, 0.006860856397106627, 0.003161222790687845, 0.0],
        },
        "y180_I_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "y180_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.00632244558137569, 0.013721712794213255, 0.022203626043716444, 0.03171940805306404, 0.042156791938140314, 0.053334626478381816, 0.06500223541963389, 0.07684447918069413, 0.08849297052054868, 0.09954325611298082, 0.10957706553241468, 0.11818804211290497, 0.12500880932163916, 0.12973688596304922] + [0.13215691198324275] * 2 + [0.12973688596304922, 0.12500880932163916, 0.11818804211290497, 0.10957706553241468, 0.09954325611298082, 0.08849297052054868, 0.07684447918069413, 0.06500223541963389, 0.053334626478381816, 0.042156791938140314, 0.03171940805306404, 0.022203626043716444, 0.013721712794213255, 0.00632244558137569, 0.0],
        },
        "minus_y90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "minus_y90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, -0.003161222790687845, -0.006860856397106627, -0.011101813021858222, -0.01585970402653202, -0.021078395969070157, -0.026667313239190908, -0.032501117709816944, -0.03842223959034707, -0.04424648526027434, -0.04977162805649041, -0.05478853276620734, -0.059094021056452485, -0.06250440466081958, -0.06486844298152461] + [-0.06607845599162138] * 2 + [-0.06486844298152461, -0.06250440466081958, -0.059094021056452485, -0.05478853276620734, -0.04977162805649041, -0.04424648526027434, -0.03842223959034707, -0.032501117709816944, -0.026667313239190908, -0.021078395969070157, -0.01585970402653202, -0.011101813021858222, -0.006860856397106627, -0.003161222790687845, 0.0],
        },
        "readout_wf_q5": {
            "type": "constant",
            "sample": 0.0545211,
        },
        "gft_cz_wf_1_2_q2": {
            "type": "arbitrary",
            "samples": [1.7134099282414948e-06, 2.638671054595603e-05, 0.000274955837812804, 0.001938627437084657, 0.00924867424157258, 0.029855086162189872, 0.06520950340242525, 0.0963733986591603] + [0.10119591000000001] * 8 + [0.0963733986591603, 0.06520950340242525, 0.029855086162189872, 0.00924867424157258, 0.001938627437084657, 0.000274955837812804, 2.638671054595603e-05, 1.7134099282414948e-06],
        },
        "g_cz_wf_1_2_q2": {
            "type": "arbitrary",
            "samples": [0.03931213024777564, 0.06088781843160629, 0.08859125307281902, 0.12108988595605871, 0.15548249127139938, 0.18754768422689555, 0.2125193682579723] + [0.22622568992333553] * 2 + [0.2125193682579723, 0.18754768422689555, 0.15548249127139938, 0.12108988595605871, 0.08859125307281902, 0.06088781843160629, 0.03931213024777564],
        },
    },
    "digital_waveforms": {
        "ON": {
            "samples": [(1, 0)],
        },
    },
    "integration_weights": {
        "cosine_weights": {
            "cosine": [(1.0, 5000)],
            "sine": [(0.0, 5000)],
        },
        "sine_weights": {
            "cosine": [(0.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "minus_sine_weights": {
            "cosine": [(0.0, 5000)],
            "sine": [(-1.0, 5000)],
        },
        "rotated_cosine_weights_q1": {
            "cosine": [(0.5195191118795094, 5000)],
            "sine": [(0.8544588301328074, 5000)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(-0.8544588301328074, 5000)],
            "sine": [(0.5195191118795094, 5000)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(0.8544588301328074, 5000)],
            "sine": [(-0.5195191118795094, 5000)],
        },
        "rotated_cosine_weights_q2": {
            "cosine": [(-0.9770455744352636, 5000)],
            "sine": [(-0.21303038627497642, 5000)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(0.21303038627497642, 5000)],
            "sine": [(-0.9770455744352636, 5000)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(-0.21303038627497642, 5000)],
            "sine": [(0.9770455744352636, 5000)],
        },
        "rotated_cosine_weights_q3": {
            "cosine": [(-0.27395921869243245, 5000)],
            "sine": [(0.9617413095492113, 5000)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(-0.9617413095492113, 5000)],
            "sine": [(-0.27395921869243245, 5000)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(0.9617413095492113, 5000)],
            "sine": [(0.27395921869243245, 5000)],
        },
        "rotated_cosine_weights_q4": {
            "cosine": [(0.3762242631393654, 5000)],
            "sine": [(-0.9265286308718375, 5000)],
        },
        "rotated_sine_weights_q4": {
            "cosine": [(0.9265286308718375, 5000)],
            "sine": [(0.3762242631393654, 5000)],
        },
        "rotated_minus_sine_weights_q4": {
            "cosine": [(-0.9265286308718375, 5000)],
            "sine": [(-0.3762242631393654, 5000)],
        },
        "rotated_cosine_weights_q5": {
            "cosine": [(-0.4756242090702756, 5000)],
            "sine": [(-0.8796485728666162, 5000)],
        },
        "rotated_sine_weights_q5": {
            "cosine": [(0.8796485728666162, 5000)],
            "sine": [(-0.4756242090702756, 5000)],
        },
        "rotated_minus_sine_weights_q5": {
            "cosine": [(-0.8796485728666162, 5000)],
            "sine": [(0.4756242090702756, 5000)],
        },
        "opt_cosine_weights_q1": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_sine_weights_q1": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_minus_sine_weights_q1": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_cosine_weights_q2": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_sine_weights_q2": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_minus_sine_weights_q2": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_cosine_weights_q3": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_sine_weights_q3": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_minus_sine_weights_q3": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_cosine_weights_q4": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_sine_weights_q4": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_minus_sine_weights_q4": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_cosine_weights_q5": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_sine_weights_q5": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_minus_sine_weights_q5": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
    },
    "mixers": {
        "octave_octave1_2": [
            {'intermediate_frequency': -346063000, 'lo_frequency': 3670000000, 'correction': [1.139035176485777, 0.16698597371578217, 0.19680260121822357, 0.9664653651416302]},
            {'intermediate_frequency': -135471000, 'lo_frequency': 3200000000, 'correction': [0.9071802385151386, 0.06404274702072144, 0.0515754371881485, 1.1264725401997566]},
            {'intermediate_frequency': -135196000, 'lo_frequency': 3200000000, 'correction': (1, 0, 0, 1)},
        ],
        "octave_octave1_3": [
            {'intermediate_frequency': 471832000, 'lo_frequency': 3670000000, 'correction': [1.0509245730936527, 0.1871345043182373, 0.1878669261932373, 1.0468274168670177]},
            {'intermediate_frequency': -262537000, 'lo_frequency': 3200000000, 'correction': [0.8680114857852459, -0.004036571830511093, -0.002966787666082382, 1.1810052506625652]},
            {'intermediate_frequency': -261338000, 'lo_frequency': 3200000000, 'correction': (1, 0, 0, 1)},
        ],
        "octave_octave1_4": [{'intermediate_frequency': -146495000, 'lo_frequency': 4000000000, 'correction': [1.4058866314589977, -0.06476316601037979, -0.11419019848108292, 0.7973509877920151]}],
        "octave_octave1_5": [{'intermediate_frequency': -408869000, 'lo_frequency': 4000000000, 'correction': [1.4832084812223911, -0.04674422740936279, -0.08931624889373779, 0.7762465998530388]}],
        "octave_octave2_1": [
            {'intermediate_frequency': -24209000, 'lo_frequency': 4500000000, 'correction': [1.2739626578986645, -0.05181884765625, -0.07916259765625, 0.8339200429618359]},
            {'intermediate_frequency': -24184000, 'lo_frequency': 4500000000, 'correction': (1, 0, 0, 1)},
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
            {'intermediate_frequency': -163070000, 'lo_frequency': 5900000000, 'correction': [1.0789089314639568, -0.13434219360351562, -0.14752578735351562, 0.9824925884604454]},
            {'intermediate_frequency': 126410000, 'lo_frequency': 5900000000, 'correction': [1.096462655812502, -0.1716594696044922, -0.1885051727294922, 0.9984776265919209]},
            {'intermediate_frequency': -49700000, 'lo_frequency': 5900000000, 'correction': [1.0855363868176937, -0.14926910400390625, -0.16391754150390625, 0.9885277822613716]},
            {'intermediate_frequency': 218300000, 'lo_frequency': 5900000000, 'correction': [1.1093690656125546, -0.17780685424804688, -0.19831466674804688, 0.9946486912667751]},
            {'intermediate_frequency': 28800000, 'lo_frequency': 5900000000, 'correction': [1.0890531428158283, -0.15673255920410156, -0.17211341857910156, 0.9917302653193474]},
            {'intermediate_frequency': -163122000, 'lo_frequency': 5900000000, 'correction': (1, 0, 0, 1)},
            {'intermediate_frequency': -49753000, 'lo_frequency': 5900000000, 'correction': (1, 0, 0, 1)},
            {'intermediate_frequency': 218194000, 'lo_frequency': 5900000000, 'correction': (1, 0, 0, 1)},
            {'intermediate_frequency': 28632000, 'lo_frequency': 5900000000, 'correction': (1, 0, 0, 1)},
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
                    "offset": 0.02001953125,
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
                    "offset": 0.01824951171875,
                    "delay": 0,
                    "shareable": False,
                },
                "8": {
                    "offset": -0.00244140625,
                    "delay": 0,
                    "shareable": False,
                },
                "9": {
                    "offset": 0.0092620849609375,
                    "delay": 0,
                    "shareable": False,
                },
                "10": {
                    "offset": -0.0152587890625,
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
                    "offset": -0.203,
                    "delay": 0,
                    "shareable": False,
                },
                "6": {
                    "offset": 0.044,
                    "delay": 0,
                    "shareable": False,
                },
                "7": {
                    "offset": -0.116,
                    "delay": 0,
                    "shareable": False,
                },
                "8": {
                    "offset": 0.033,
                    "delay": 0,
                    "shareable": False,
                },
                "9": {
                    "offset": 0.037,
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
            "intermediate_frequency": 135196000.0,
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
            "intermediate_frequency": 146495000.0,
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
                "lo_frequency": 4000000000.0,
            },
        },
        "q3_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": 261338000.0,
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
            "intermediate_frequency": 408869000.0,
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
                "lo_frequency": 4000000000.0,
            },
        },
        "q5_xy": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": 24184000.0,
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
                "lo_frequency": 4500000000.0,
            },
        },
        "q1_z": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "operations": {
                "const": "const_flux_pulse",
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
            "length": 5000,
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
            "length": 5000,
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
            "length": 5000,
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
            "length": 5000,
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
            "length": 5000,
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
            "sample": 0.45,
            "type": "constant",
        },
        "zero_wf": {
            "sample": 0.0,
            "type": "constant",
        },
        "x90_I_wf_q1": {
            "samples": [0.0, 0.00035978111044912813, 0.0007808391551694244, 0.0012635055740989535, 0.0018050046782114443, 0.0023989478788327924, 0.0030350266985779938, 0.0036989763122425925, 0.00437286358509065, 0.005035725304558076, 0.005664545904127425, 0.006235523550118227, 0.006725534365759936, 0.007113672653213481, 0.007382725607871725] + [0.007520438086002945] * 2 + [0.007382725607871725, 0.007113672653213481, 0.006725534365759936, 0.006235523550118227, 0.005664545904127425, 0.005035725304558076, 0.00437286358509065, 0.0036989763122425925, 0.0030350266985779938, 0.0023989478788327924, 0.0018050046782114443, 0.0012635055740989535, 0.0007808391551694244, 0.00035978111044912813, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q1": {
            "samples": [0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q1": {
            "samples": [0.0, 0.0007195622208982563, 0.0015616783103388487, 0.002527011148197907, 0.0036100093564228886, 0.004797895757665585, 0.0060700533971559875, 0.007397952624485185, 0.0087457271701813, 0.010071450609116153, 0.01132909180825485, 0.012471047100236454, 0.013451068731519873, 0.014227345306426963, 0.01476545121574345] + [0.01504087617200589] * 2 + [0.01476545121574345, 0.014227345306426963, 0.013451068731519873, 0.012471047100236454, 0.01132909180825485, 0.010071450609116153, 0.0087457271701813, 0.007397952624485185, 0.0060700533971559875, 0.004797895757665585, 0.0036100093564228886, 0.002527011148197907, 0.0015616783103388487, 0.0007195622208982563, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q1": {
            "samples": [0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q1": {
            "samples": [0.0, -0.00035978111044912813, -0.0007808391551694244, -0.0012635055740989535, -0.0018050046782114443, -0.0023989478788327924, -0.0030350266985779938, -0.0036989763122425925, -0.00437286358509065, -0.005035725304558076, -0.005664545904127425, -0.006235523550118227, -0.006725534365759936, -0.007113672653213481, -0.007382725607871725] + [-0.007520438086002945] * 2 + [-0.007382725607871725, -0.007113672653213481, -0.006725534365759936, -0.006235523550118227, -0.005664545904127425, -0.005035725304558076, -0.00437286358509065, -0.0036989763122425925, -0.0030350266985779938, -0.0023989478788327924, -0.0018050046782114443, -0.0012635055740989535, -0.0007808391551694244, -0.00035978111044912813, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q1": {
            "samples": [0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q1": {
            "samples": [-0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q1": {
            "samples": [0.0, 0.00035978111044912813, 0.0007808391551694244, 0.0012635055740989535, 0.0018050046782114443, 0.0023989478788327924, 0.0030350266985779938, 0.0036989763122425925, 0.00437286358509065, 0.005035725304558076, 0.005664545904127425, 0.006235523550118227, 0.006725534365759936, 0.007113672653213481, 0.007382725607871725] + [0.007520438086002945] * 2 + [0.007382725607871725, 0.007113672653213481, 0.006725534365759936, 0.006235523550118227, 0.005664545904127425, 0.005035725304558076, 0.00437286358509065, 0.0036989763122425925, 0.0030350266985779938, 0.0023989478788327924, 0.0018050046782114443, 0.0012635055740989535, 0.0007808391551694244, 0.00035978111044912813, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q1": {
            "samples": [-0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q1": {
            "samples": [0.0, 0.0007195622208982563, 0.0015616783103388487, 0.002527011148197907, 0.0036100093564228886, 0.004797895757665585, 0.0060700533971559875, 0.007397952624485185, 0.0087457271701813, 0.010071450609116153, 0.01132909180825485, 0.012471047100236454, 0.013451068731519873, 0.014227345306426963, 0.01476545121574345] + [0.01504087617200589] * 2 + [0.01476545121574345, 0.014227345306426963, 0.013451068731519873, 0.012471047100236454, 0.01132909180825485, 0.010071450609116153, 0.0087457271701813, 0.007397952624485185, 0.0060700533971559875, 0.004797895757665585, 0.0036100093564228886, 0.002527011148197907, 0.0015616783103388487, 0.0007195622208982563, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q1": {
            "samples": [-0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q1": {
            "samples": [0.0, -0.00035978111044912813, -0.0007808391551694244, -0.0012635055740989535, -0.0018050046782114443, -0.0023989478788327924, -0.0030350266985779938, -0.0036989763122425925, -0.00437286358509065, -0.005035725304558076, -0.005664545904127425, -0.006235523550118227, -0.006725534365759936, -0.007113672653213481, -0.007382725607871725] + [-0.007520438086002945] * 2 + [-0.007382725607871725, -0.007113672653213481, -0.006725534365759936, -0.006235523550118227, -0.005664545904127425, -0.005035725304558076, -0.00437286358509065, -0.0036989763122425925, -0.0030350266985779938, -0.0023989478788327924, -0.0018050046782114443, -0.0012635055740989535, -0.0007808391551694244, -0.00035978111044912813, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q1": {
            "sample": 0.07030871999999999,
            "type": "constant",
        },
        "x90_I_wf_q2": {
            "samples": [0.0, 0.0015442290358603028, 0.003351466935671013, 0.005423136284334835, 0.007747323450300807, 0.010296607749596929, 0.013026743807379702, 0.015876505070524388, 0.01876892010679358, 0.021614011981361633, 0.024312994779513215, 0.026763707821855758, 0.028866900311463998, 0.03053284217446686, 0.031687653732662906] + [0.03227873425677668] * 2 + [0.031687653732662906, 0.03053284217446686, 0.028866900311463998, 0.026763707821855758, 0.024312994779513215, 0.021614011981361633, 0.01876892010679358, 0.015876505070524388, 0.013026743807379702, 0.010296607749596929, 0.007747323450300807, 0.005423136284334835, 0.003351466935671013, 0.0015442290358603028, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q2": {
            "samples": [0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q2": {
            "samples": [0.0, 0.0030884580717206057, 0.006702933871342026, 0.01084627256866967, 0.015494646900601613, 0.020593215499193858, 0.026053487614759403, 0.031753010141048775, 0.03753784021358716, 0.043228023962723267, 0.04862598955902643, 0.053527415643711516, 0.057733800622927996, 0.06106568434893372, 0.06337530746532581] + [0.06455746851355336] * 2 + [0.06337530746532581, 0.06106568434893372, 0.057733800622927996, 0.053527415643711516, 0.04862598955902643, 0.043228023962723267, 0.03753784021358716, 0.031753010141048775, 0.026053487614759403, 0.020593215499193858, 0.015494646900601613, 0.01084627256866967, 0.006702933871342026, 0.0030884580717206057, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q2": {
            "samples": [0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q2": {
            "samples": [0.0, -0.0015442290358603028, -0.003351466935671013, -0.005423136284334835, -0.007747323450300807, -0.010296607749596929, -0.013026743807379702, -0.015876505070524388, -0.01876892010679358, -0.021614011981361633, -0.024312994779513215, -0.026763707821855758, -0.028866900311463998, -0.03053284217446686, -0.031687653732662906] + [-0.03227873425677668] * 2 + [-0.031687653732662906, -0.03053284217446686, -0.028866900311463998, -0.026763707821855758, -0.024312994779513215, -0.021614011981361633, -0.01876892010679358, -0.015876505070524388, -0.013026743807379702, -0.010296607749596929, -0.007747323450300807, -0.005423136284334835, -0.003351466935671013, -0.0015442290358603028, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q2": {
            "samples": [0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q2": {
            "samples": [-0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q2": {
            "samples": [0.0, 0.0015442290358603028, 0.003351466935671013, 0.005423136284334835, 0.007747323450300807, 0.010296607749596929, 0.013026743807379702, 0.015876505070524388, 0.01876892010679358, 0.021614011981361633, 0.024312994779513215, 0.026763707821855758, 0.028866900311463998, 0.03053284217446686, 0.031687653732662906] + [0.03227873425677668] * 2 + [0.031687653732662906, 0.03053284217446686, 0.028866900311463998, 0.026763707821855758, 0.024312994779513215, 0.021614011981361633, 0.01876892010679358, 0.015876505070524388, 0.013026743807379702, 0.010296607749596929, 0.007747323450300807, 0.005423136284334835, 0.003351466935671013, 0.0015442290358603028, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q2": {
            "samples": [-0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q2": {
            "samples": [0.0, 0.0030884580717206057, 0.006702933871342026, 0.01084627256866967, 0.015494646900601613, 0.020593215499193858, 0.026053487614759403, 0.031753010141048775, 0.03753784021358716, 0.043228023962723267, 0.04862598955902643, 0.053527415643711516, 0.057733800622927996, 0.06106568434893372, 0.06337530746532581] + [0.06455746851355336] * 2 + [0.06337530746532581, 0.06106568434893372, 0.057733800622927996, 0.053527415643711516, 0.04862598955902643, 0.043228023962723267, 0.03753784021358716, 0.031753010141048775, 0.026053487614759403, 0.020593215499193858, 0.015494646900601613, 0.01084627256866967, 0.006702933871342026, 0.0030884580717206057, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q2": {
            "samples": [-0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q2": {
            "samples": [0.0, -0.0015442290358603028, -0.003351466935671013, -0.005423136284334835, -0.007747323450300807, -0.010296607749596929, -0.013026743807379702, -0.015876505070524388, -0.01876892010679358, -0.021614011981361633, -0.024312994779513215, -0.026763707821855758, -0.028866900311463998, -0.03053284217446686, -0.031687653732662906] + [-0.03227873425677668] * 2 + [-0.031687653732662906, -0.03053284217446686, -0.028866900311463998, -0.026763707821855758, -0.024312994779513215, -0.021614011981361633, -0.01876892010679358, -0.015876505070524388, -0.013026743807379702, -0.010296607749596929, -0.007747323450300807, -0.005423136284334835, -0.003351466935671013, -0.0015442290358603028, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q2": {
            "sample": 0.08532,
            "type": "constant",
        },
        "x90_I_wf_q3": {
            "samples": [0.0, 0.00043699256224214345, 0.0009484125019529751, 0.0015346623883156954, 0.002192370850726485, 0.002913778266312639, 0.0036863638889469783, 0.004492801565768812, 0.005311309590430329, 0.006116425903626158, 0.006880195643103085, 0.007573708941211014, 0.008168879381333136, 0.008640314761936826, 0.008967108294504872] + [0.009134374798841778] * 2 + [0.008967108294504872, 0.008640314761936826, 0.008168879381333136, 0.007573708941211014, 0.006880195643103085, 0.006116425903626158, 0.005311309590430329, 0.004492801565768812, 0.0036863638889469783, 0.002913778266312639, 0.002192370850726485, 0.0015346623883156954, 0.0009484125019529751, 0.00043699256224214345, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q3": {
            "samples": [0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q3": {
            "samples": [0.0, 0.0008739851244842869, 0.0018968250039059502, 0.0030693247766313907, 0.00438474170145297, 0.005827556532625278, 0.007372727777893957, 0.008985603131537625, 0.010622619180860658, 0.012232851807252317, 0.01376039128620617, 0.015147417882422028, 0.01633775876266627, 0.01728062952387365, 0.017934216589009743] + [0.018268749597683556] * 2 + [0.017934216589009743, 0.01728062952387365, 0.01633775876266627, 0.015147417882422028, 0.01376039128620617, 0.012232851807252317, 0.010622619180860658, 0.008985603131537625, 0.007372727777893957, 0.005827556532625278, 0.00438474170145297, 0.0030693247766313907, 0.0018968250039059502, 0.0008739851244842869, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q3": {
            "samples": [0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q3": {
            "samples": [0.0, -0.00043699256224214345, -0.0009484125019529751, -0.0015346623883156954, -0.002192370850726485, -0.002913778266312639, -0.0036863638889469783, -0.004492801565768812, -0.005311309590430329, -0.006116425903626158, -0.006880195643103085, -0.007573708941211014, -0.008168879381333136, -0.008640314761936826, -0.008967108294504872] + [-0.009134374798841778] * 2 + [-0.008967108294504872, -0.008640314761936826, -0.008168879381333136, -0.007573708941211014, -0.006880195643103085, -0.006116425903626158, -0.005311309590430329, -0.004492801565768812, -0.0036863638889469783, -0.002913778266312639, -0.002192370850726485, -0.0015346623883156954, -0.0009484125019529751, -0.00043699256224214345, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q3": {
            "samples": [0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q3": {
            "samples": [-0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q3": {
            "samples": [0.0, 0.00043699256224214345, 0.0009484125019529751, 0.0015346623883156954, 0.002192370850726485, 0.002913778266312639, 0.0036863638889469783, 0.004492801565768812, 0.005311309590430329, 0.006116425903626158, 0.006880195643103085, 0.007573708941211014, 0.008168879381333136, 0.008640314761936826, 0.008967108294504872] + [0.009134374798841778] * 2 + [0.008967108294504872, 0.008640314761936826, 0.008168879381333136, 0.007573708941211014, 0.006880195643103085, 0.006116425903626158, 0.005311309590430329, 0.004492801565768812, 0.0036863638889469783, 0.002913778266312639, 0.002192370850726485, 0.0015346623883156954, 0.0009484125019529751, 0.00043699256224214345, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q3": {
            "samples": [-0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q3": {
            "samples": [0.0, 0.0008739851244842869, 0.0018968250039059502, 0.0030693247766313907, 0.00438474170145297, 0.005827556532625278, 0.007372727777893957, 0.008985603131537625, 0.010622619180860658, 0.012232851807252317, 0.01376039128620617, 0.015147417882422028, 0.01633775876266627, 0.01728062952387365, 0.017934216589009743] + [0.018268749597683556] * 2 + [0.017934216589009743, 0.01728062952387365, 0.01633775876266627, 0.015147417882422028, 0.01376039128620617, 0.012232851807252317, 0.010622619180860658, 0.008985603131537625, 0.007372727777893957, 0.005827556532625278, 0.00438474170145297, 0.0030693247766313907, 0.0018968250039059502, 0.0008739851244842869, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q3": {
            "samples": [-0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q3": {
            "samples": [0.0, -0.00043699256224214345, -0.0009484125019529751, -0.0015346623883156954, -0.002192370850726485, -0.002913778266312639, -0.0036863638889469783, -0.004492801565768812, -0.005311309590430329, -0.006116425903626158, -0.006880195643103085, -0.007573708941211014, -0.008168879381333136, -0.008640314761936826, -0.008967108294504872] + [-0.009134374798841778] * 2 + [-0.008967108294504872, -0.008640314761936826, -0.008168879381333136, -0.007573708941211014, -0.006880195643103085, -0.006116425903626158, -0.005311309590430329, -0.004492801565768812, -0.0036863638889469783, -0.002913778266312639, -0.002192370850726485, -0.0015346623883156954, -0.0009484125019529751, -0.00043699256224214345, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q3": {
            "sample": 0.07729910999999999,
            "type": "constant",
        },
        "x90_I_wf_q4": {
            "samples": [0.0, 0.002277939952113301, 0.004943852403797425, 0.007999835853986073, 0.011428316136765718, 0.015188844154182906, 0.019216152187064038, 0.023419923055603382, 0.027686613822455967, 0.031883496731668265, 0.03586484962894161, 0.039479972140355285, 0.042582456349502515, 0.04503993865264941, 0.04674343685433391] + [0.047615357993962465] * 2 + [0.04674343685433391, 0.04503993865264941, 0.042582456349502515, 0.039479972140355285, 0.03586484962894161, 0.031883496731668265, 0.027686613822455967, 0.023419923055603382, 0.019216152187064038, 0.015188844154182906, 0.011428316136765718, 0.007999835853986073, 0.004943852403797425, 0.002277939952113301, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q4": {
            "samples": [0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q4": {
            "samples": [0.0, 0.004555879904226602, 0.00988770480759485, 0.015999671707972146, 0.022856632273531435, 0.030377688308365812, 0.038432304374128076, 0.046839846111206764, 0.05537322764491193, 0.06376699346333653, 0.07172969925788322, 0.07895994428071057, 0.08516491269900503, 0.09007987730529882, 0.09348687370866782] + [0.09523071598792493] * 2 + [0.09348687370866782, 0.09007987730529882, 0.08516491269900503, 0.07895994428071057, 0.07172969925788322, 0.06376699346333653, 0.05537322764491193, 0.046839846111206764, 0.038432304374128076, 0.030377688308365812, 0.022856632273531435, 0.015999671707972146, 0.00988770480759485, 0.004555879904226602, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q4": {
            "samples": [0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q4": {
            "samples": [0.0, -0.002277939952113301, -0.004943852403797425, -0.007999835853986073, -0.011428316136765718, -0.015188844154182906, -0.019216152187064038, -0.023419923055603382, -0.027686613822455967, -0.031883496731668265, -0.03586484962894161, -0.039479972140355285, -0.042582456349502515, -0.04503993865264941, -0.04674343685433391] + [-0.047615357993962465] * 2 + [-0.04674343685433391, -0.04503993865264941, -0.042582456349502515, -0.039479972140355285, -0.03586484962894161, -0.031883496731668265, -0.027686613822455967, -0.023419923055603382, -0.019216152187064038, -0.015188844154182906, -0.011428316136765718, -0.007999835853986073, -0.004943852403797425, -0.002277939952113301, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q4": {
            "samples": [0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q4": {
            "samples": [-0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q4": {
            "samples": [0.0, 0.002277939952113301, 0.004943852403797425, 0.007999835853986073, 0.011428316136765718, 0.015188844154182906, 0.019216152187064038, 0.023419923055603382, 0.027686613822455967, 0.031883496731668265, 0.03586484962894161, 0.039479972140355285, 0.042582456349502515, 0.04503993865264941, 0.04674343685433391] + [0.047615357993962465] * 2 + [0.04674343685433391, 0.04503993865264941, 0.042582456349502515, 0.039479972140355285, 0.03586484962894161, 0.031883496731668265, 0.027686613822455967, 0.023419923055603382, 0.019216152187064038, 0.015188844154182906, 0.011428316136765718, 0.007999835853986073, 0.004943852403797425, 0.002277939952113301, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q4": {
            "samples": [-0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q4": {
            "samples": [0.0, 0.004555879904226602, 0.00988770480759485, 0.015999671707972146, 0.022856632273531435, 0.030377688308365812, 0.038432304374128076, 0.046839846111206764, 0.05537322764491193, 0.06376699346333653, 0.07172969925788322, 0.07895994428071057, 0.08516491269900503, 0.09007987730529882, 0.09348687370866782] + [0.09523071598792493] * 2 + [0.09348687370866782, 0.09007987730529882, 0.08516491269900503, 0.07895994428071057, 0.07172969925788322, 0.06376699346333653, 0.05537322764491193, 0.046839846111206764, 0.038432304374128076, 0.030377688308365812, 0.022856632273531435, 0.015999671707972146, 0.00988770480759485, 0.004555879904226602, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q4": {
            "samples": [-0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q4": {
            "samples": [0.0, -0.002277939952113301, -0.004943852403797425, -0.007999835853986073, -0.011428316136765718, -0.015188844154182906, -0.019216152187064038, -0.023419923055603382, -0.027686613822455967, -0.031883496731668265, -0.03586484962894161, -0.039479972140355285, -0.042582456349502515, -0.04503993865264941, -0.04674343685433391] + [-0.047615357993962465] * 2 + [-0.04674343685433391, -0.04503993865264941, -0.042582456349502515, -0.039479972140355285, -0.03586484962894161, -0.031883496731668265, -0.027686613822455967, -0.023419923055603382, -0.019216152187064038, -0.015188844154182906, -0.011428316136765718, -0.007999835853986073, -0.004943852403797425, -0.002277939952113301, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q4": {
            "sample": 0.11668859999999999,
            "type": "constant",
        },
        "x90_I_wf_q5": {
            "samples": [0.0, 0.003161222790687845, 0.006860856397106627, 0.011101813021858222, 0.01585970402653202, 0.021078395969070157, 0.026667313239190908, 0.032501117709816944, 0.03842223959034707, 0.04424648526027434, 0.04977162805649041, 0.05478853276620734, 0.059094021056452485, 0.06250440466081958, 0.06486844298152461] + [0.06607845599162138] * 2 + [0.06486844298152461, 0.06250440466081958, 0.059094021056452485, 0.05478853276620734, 0.04977162805649041, 0.04424648526027434, 0.03842223959034707, 0.032501117709816944, 0.026667313239190908, 0.021078395969070157, 0.01585970402653202, 0.011101813021858222, 0.006860856397106627, 0.003161222790687845, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q5": {
            "samples": [0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q5": {
            "samples": [0.0, 0.00632244558137569, 0.013721712794213255, 0.022203626043716444, 0.03171940805306404, 0.042156791938140314, 0.053334626478381816, 0.06500223541963389, 0.07684447918069413, 0.08849297052054868, 0.09954325611298082, 0.10957706553241468, 0.11818804211290497, 0.12500880932163916, 0.12973688596304922] + [0.13215691198324275] * 2 + [0.12973688596304922, 0.12500880932163916, 0.11818804211290497, 0.10957706553241468, 0.09954325611298082, 0.08849297052054868, 0.07684447918069413, 0.06500223541963389, 0.053334626478381816, 0.042156791938140314, 0.03171940805306404, 0.022203626043716444, 0.013721712794213255, 0.00632244558137569, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q5": {
            "samples": [0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q5": {
            "samples": [0.0, -0.003161222790687845, -0.006860856397106627, -0.011101813021858222, -0.01585970402653202, -0.021078395969070157, -0.026667313239190908, -0.032501117709816944, -0.03842223959034707, -0.04424648526027434, -0.04977162805649041, -0.05478853276620734, -0.059094021056452485, -0.06250440466081958, -0.06486844298152461] + [-0.06607845599162138] * 2 + [-0.06486844298152461, -0.06250440466081958, -0.059094021056452485, -0.05478853276620734, -0.04977162805649041, -0.04424648526027434, -0.03842223959034707, -0.032501117709816944, -0.026667313239190908, -0.021078395969070157, -0.01585970402653202, -0.011101813021858222, -0.006860856397106627, -0.003161222790687845, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q5": {
            "samples": [0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q5": {
            "samples": [-0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q5": {
            "samples": [0.0, 0.003161222790687845, 0.006860856397106627, 0.011101813021858222, 0.01585970402653202, 0.021078395969070157, 0.026667313239190908, 0.032501117709816944, 0.03842223959034707, 0.04424648526027434, 0.04977162805649041, 0.05478853276620734, 0.059094021056452485, 0.06250440466081958, 0.06486844298152461] + [0.06607845599162138] * 2 + [0.06486844298152461, 0.06250440466081958, 0.059094021056452485, 0.05478853276620734, 0.04977162805649041, 0.04424648526027434, 0.03842223959034707, 0.032501117709816944, 0.026667313239190908, 0.021078395969070157, 0.01585970402653202, 0.011101813021858222, 0.006860856397106627, 0.003161222790687845, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q5": {
            "samples": [-0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q5": {
            "samples": [0.0, 0.00632244558137569, 0.013721712794213255, 0.022203626043716444, 0.03171940805306404, 0.042156791938140314, 0.053334626478381816, 0.06500223541963389, 0.07684447918069413, 0.08849297052054868, 0.09954325611298082, 0.10957706553241468, 0.11818804211290497, 0.12500880932163916, 0.12973688596304922] + [0.13215691198324275] * 2 + [0.12973688596304922, 0.12500880932163916, 0.11818804211290497, 0.10957706553241468, 0.09954325611298082, 0.08849297052054868, 0.07684447918069413, 0.06500223541963389, 0.053334626478381816, 0.042156791938140314, 0.03171940805306404, 0.022203626043716444, 0.013721712794213255, 0.00632244558137569, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q5": {
            "samples": [-0.0] * 32,
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q5": {
            "samples": [0.0, -0.003161222790687845, -0.006860856397106627, -0.011101813021858222, -0.01585970402653202, -0.021078395969070157, -0.026667313239190908, -0.032501117709816944, -0.03842223959034707, -0.04424648526027434, -0.04977162805649041, -0.05478853276620734, -0.059094021056452485, -0.06250440466081958, -0.06486844298152461] + [-0.06607845599162138] * 2 + [-0.06486844298152461, -0.06250440466081958, -0.059094021056452485, -0.05478853276620734, -0.04977162805649041, -0.04424648526027434, -0.03842223959034707, -0.032501117709816944, -0.026667313239190908, -0.021078395969070157, -0.01585970402653202, -0.011101813021858222, -0.006860856397106627, -0.003161222790687845, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q5": {
            "sample": 0.0545211,
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
    },
    "digital_waveforms": {
        "ON": {
            "samples": [(1, 0)],
        },
    },
    "integration_weights": {
        "cosine_weights": {
            "cosine": [(1.0, 5000)],
            "sine": [(0.0, 5000)],
        },
        "sine_weights": {
            "cosine": [(0.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "minus_sine_weights": {
            "cosine": [(0.0, 5000)],
            "sine": [(-1.0, 5000)],
        },
        "rotated_cosine_weights_q1": {
            "cosine": [(0.5195191118795094, 5000)],
            "sine": [(0.8544588301328074, 5000)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(-0.8544588301328074, 5000)],
            "sine": [(0.5195191118795094, 5000)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(0.8544588301328074, 5000)],
            "sine": [(-0.5195191118795094, 5000)],
        },
        "rotated_cosine_weights_q2": {
            "cosine": [(-0.9770455744352636, 5000)],
            "sine": [(-0.21303038627497642, 5000)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(0.21303038627497642, 5000)],
            "sine": [(-0.9770455744352636, 5000)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(-0.21303038627497642, 5000)],
            "sine": [(0.9770455744352636, 5000)],
        },
        "rotated_cosine_weights_q3": {
            "cosine": [(-0.27395921869243245, 5000)],
            "sine": [(0.9617413095492113, 5000)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(-0.9617413095492113, 5000)],
            "sine": [(-0.27395921869243245, 5000)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(0.9617413095492113, 5000)],
            "sine": [(0.27395921869243245, 5000)],
        },
        "rotated_cosine_weights_q4": {
            "cosine": [(0.3762242631393654, 5000)],
            "sine": [(-0.9265286308718375, 5000)],
        },
        "rotated_sine_weights_q4": {
            "cosine": [(0.9265286308718375, 5000)],
            "sine": [(0.3762242631393654, 5000)],
        },
        "rotated_minus_sine_weights_q4": {
            "cosine": [(-0.9265286308718375, 5000)],
            "sine": [(-0.3762242631393654, 5000)],
        },
        "rotated_cosine_weights_q5": {
            "cosine": [(-0.4756242090702756, 5000)],
            "sine": [(-0.8796485728666162, 5000)],
        },
        "rotated_sine_weights_q5": {
            "cosine": [(0.8796485728666162, 5000)],
            "sine": [(-0.4756242090702756, 5000)],
        },
        "rotated_minus_sine_weights_q5": {
            "cosine": [(-0.8796485728666162, 5000)],
            "sine": [(0.4756242090702756, 5000)],
        },
        "opt_cosine_weights_q1": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_sine_weights_q1": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_minus_sine_weights_q1": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_cosine_weights_q2": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_sine_weights_q2": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_minus_sine_weights_q2": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_cosine_weights_q3": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_sine_weights_q3": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_minus_sine_weights_q3": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_cosine_weights_q4": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_sine_weights_q4": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_minus_sine_weights_q4": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_cosine_weights_q5": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_sine_weights_q5": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
        "opt_minus_sine_weights_q5": {
            "cosine": [(1.0, 5000)],
            "sine": [(1.0, 5000)],
        },
    },
    "mixers": {
        "octave_octave1_2": [
            {'intermediate_frequency': 346063000.0, 'lo_frequency': 3670000000.0, 'correction': [1.139035176485777, 0.16698597371578217, 0.19680260121822357, 0.9664653651416302]},
            {'intermediate_frequency': 135471000.0, 'lo_frequency': 3200000000.0, 'correction': [0.9071802385151386, 0.06404274702072144, 0.0515754371881485, 1.1264725401997566]},
            {'intermediate_frequency': 135196000.0, 'lo_frequency': 3200000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
        ],
        "octave_octave1_3": [
            {'intermediate_frequency': 471832000.0, 'lo_frequency': 3670000000.0, 'correction': [1.0509245730936527, 0.1871345043182373, 0.1878669261932373, 1.0468274168670177]},
            {'intermediate_frequency': 262537000.0, 'lo_frequency': 3200000000.0, 'correction': [0.8680114857852459, -0.004036571830511093, -0.002966787666082382, 1.1810052506625652]},
            {'intermediate_frequency': 261338000.0, 'lo_frequency': 3200000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
        ],
        "octave_octave1_4": [{'intermediate_frequency': 146495000.0, 'lo_frequency': 4000000000.0, 'correction': [1.4058866314589977, -0.06476316601037979, -0.11419019848108292, 0.7973509877920151]}],
        "octave_octave1_5": [{'intermediate_frequency': 408869000.0, 'lo_frequency': 4000000000.0, 'correction': [1.4832084812223911, -0.04674422740936279, -0.08931624889373779, 0.7762465998530388]}],
        "octave_octave2_1": [
            {'intermediate_frequency': 24209000.0, 'lo_frequency': 4500000000.0, 'correction': [1.2739626578986645, -0.05181884765625, -0.07916259765625, 0.8339200429618359]},
            {'intermediate_frequency': 24184000.0, 'lo_frequency': 4500000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
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
            {'intermediate_frequency': 163070000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0789089314639568, -0.13434219360351562, -0.14752578735351562, 0.9824925884604454]},
            {'intermediate_frequency': 126410000.0, 'lo_frequency': 5900000000.0, 'correction': [1.096462655812502, -0.1716594696044922, -0.1885051727294922, 0.9984776265919209]},
            {'intermediate_frequency': 49700000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0855363868176937, -0.14926910400390625, -0.16391754150390625, 0.9885277822613716]},
            {'intermediate_frequency': 218300000.0, 'lo_frequency': 5900000000.0, 'correction': [1.1093690656125546, -0.17780685424804688, -0.19831466674804688, 0.9946486912667751]},
            {'intermediate_frequency': 28800000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0890531428158283, -0.15673255920410156, -0.17211341857910156, 0.9917302653193474]},
            {'intermediate_frequency': 163122000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
            {'intermediate_frequency': 49753000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
            {'intermediate_frequency': 218194000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
            {'intermediate_frequency': 28632000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
        ],
    },
}



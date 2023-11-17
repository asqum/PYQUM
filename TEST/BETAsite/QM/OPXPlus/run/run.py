
# Single QUA script generated at 2023-11-16 23:29:48.889848
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
    with for_(v1,0,(v1<3700),(v1+1)):
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
                    "offset": 0.0,
                },
                "4": {
                    "offset": 0.0,
                },
                "5": {
                    "offset": -0.20299999999999996,
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
            "intermediate_frequency": -130602000,
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
            "intermediate_frequency": -106551000,
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
            "intermediate_frequency": -261857000,
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
            "intermediate_frequency": -368712000,
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
            "intermediate_frequency": -122859000,
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
            "length": 260,
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
        "cz5_4": {
            "operation": "control",
            "length": 260,
            "waveforms": {
                "single": "const_flux_wf",
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
            "sample": 0.022,
        },
        "zero_wf": {
            "type": "constant",
            "sample": 0.0,
        },
        "x90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.00039809550727867014, 0.0008640097535541232, 0.0013981078484774292, 0.0019973138124745166, 0.002654550522161637, 0.003358399976371321, 0.004093063380459563, 0.004838680820509531, 0.0055720389432298255, 0.006267654697625521, 0.006899178375921787, 0.007441015863320648, 0.007870034658436784, 0.008167196805786266, 0.008318958691953291, 0.00831829446289342, 0.008165235360326555, 0.007866867312416037, 0.0074367870375188746, 0.006894074807826563, 0.006261891956235823, 0.005565846601043941, 0.004832287695268742, 0.0040866841466468086, 0.003352224190500018, 0.0026487347528244905, 0.0019919771718915017, 0.001393330842623535, 0.0008598360496620314, 0.0003945359923225235, -2.961614437397859e-06],
        },
        "x90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.00016895330454536707, -0.0001995727427140031, -0.00023052694826886737, -0.00026026242723785646, -0.00028693610291169295, -0.0003085084424969275, -0.0003228771301870727, -0.00032804384657687585, -0.00032230078398879725, -0.00030441849118834524, -0.00027381349352685293, -0.0002306736960996015, -0.0001760223056684087, -0.00011170685634264173, -4.030829192172095e-05, 3.502515921260934e-05, 0.00011080482299855288, 0.00018346643648330682, 0.0002496450191576809, 0.0003064302349207538, 0.0003515752564532771, 0.0003836383275087917, 0.00040204504261929684, 0.0004070694145730957, 0.00039974152559080743, 0.0003816975492654202, 0.0003549931590612509, 0.0003219033074057695, 0.00028473013539124327, 0.00024563691867552463, 0.00020652037021062363, 0.00016892734520119513],
        },
        "x180_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007961910145573403, 0.0017280195071082464, 0.0027962156969548583, 0.003994627624949033, 0.005309101044323274, 0.006716799952742642, 0.008186126760919126, 0.009677361641019061, 0.011144077886459651, 0.012535309395251042, 0.013798356751843575, 0.014882031726641296, 0.015740069316873568, 0.01633439361157253, 0.016637917383906582, 0.01663658892578684, 0.01633047072065311, 0.015733734624832074, 0.014873574075037749, 0.013788149615653125, 0.012523783912471645, 0.011131693202087883, 0.009664575390537484, 0.008173368293293617, 0.006704448381000036, 0.005297469505648981, 0.003983954343783003, 0.00278666168524707, 0.0017196720993240629, 0.000789071984645047, -5.923228874795718e-06],
        },
        "x180_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.00033790660909073413, -0.0003991454854280062, -0.00046105389653773474, -0.0005205248544757129, -0.0005738722058233859, -0.000617016884993855, -0.0006457542603741454, -0.0006560876931537517, -0.0006446015679775945, -0.0006088369823766905, -0.0005476269870537059, -0.000461347392199203, -0.0003520446113368174, -0.00022341371268528345, -8.06165838434419e-05, 7.005031842521868e-05, 0.00022160964599710577, 0.00036693287296661365, 0.0004992900383153618, 0.0006128604698415076, 0.0007031505129065542, 0.0007672766550175834, 0.0008040900852385937, 0.0008141388291461914, 0.0007994830511816149, 0.0007633950985308404, 0.0007099863181225018, 0.000643806614811539, 0.0005694602707824865, 0.0004912738373510493, 0.00041304074042124725, 0.00033785469040239027],
        },
        "minus_x90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, -0.00039809550727867014, -0.0008640097535541232, -0.0013981078484774292, -0.0019973138124745166, -0.002654550522161637, -0.003358399976371321, -0.004093063380459563, -0.004838680820509531, -0.0055720389432298255, -0.006267654697625521, -0.006899178375921787, -0.007441015863320648, -0.007870034658436784, -0.008167196805786266, -0.008318958691953291, -0.00831829446289342, -0.008165235360326555, -0.007866867312416037, -0.0074367870375188746, -0.006894074807826563, -0.006261891956235823, -0.005565846601043941, -0.004832287695268742, -0.0040866841466468086, -0.003352224190500018, -0.0026487347528244905, -0.0019919771718915017, -0.001393330842623535, -0.0008598360496620314, -0.0003945359923225235, 2.961614437397859e-06],
        },
        "minus_x90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.00016895330454536707, 0.0001995727427140031, 0.00023052694826886737, 0.00026026242723785646, 0.00028693610291169295, 0.0003085084424969275, 0.0003228771301870727, 0.00032804384657687585, 0.00032230078398879725, 0.00030441849118834524, 0.00027381349352685293, 0.0002306736960996015, 0.0001760223056684087, 0.00011170685634264173, 4.030829192172095e-05, -3.502515921260934e-05, -0.00011080482299855288, -0.00018346643648330682, -0.0002496450191576809, -0.0003064302349207538, -0.0003515752564532771, -0.0003836383275087917, -0.00040204504261929684, -0.0004070694145730957, -0.00039974152559080743, -0.0003816975492654202, -0.0003549931590612509, -0.0003219033074057695, -0.00028473013539124327, -0.00024563691867552463, -0.00020652037021062363, -0.00016892734520119513],
        },
        "y90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.00016895330454536707, 0.0001995727427140031, 0.00023052694826886737, 0.00026026242723785646, 0.00028693610291169295, 0.0003085084424969275, 0.0003228771301870727, 0.00032804384657687585, 0.00032230078398879725, 0.00030441849118834524, 0.00027381349352685293, 0.0002306736960996015, 0.0001760223056684087, 0.00011170685634264173, 4.030829192172095e-05, -3.502515921260934e-05, -0.00011080482299855288, -0.00018346643648330682, -0.0002496450191576809, -0.0003064302349207538, -0.0003515752564532771, -0.0003836383275087917, -0.00040204504261929684, -0.0004070694145730957, -0.00039974152559080743, -0.0003816975492654202, -0.0003549931590612509, -0.0003219033074057695, -0.00028473013539124327, -0.00024563691867552463, -0.00020652037021062363, -0.00016892734520119513],
        },
        "y90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.00039809550727867014, 0.0008640097535541232, 0.0013981078484774292, 0.0019973138124745166, 0.002654550522161637, 0.003358399976371321, 0.004093063380459563, 0.004838680820509531, 0.0055720389432298255, 0.006267654697625521, 0.006899178375921787, 0.007441015863320648, 0.007870034658436784, 0.008167196805786266, 0.008318958691953291, 0.00831829446289342, 0.008165235360326555, 0.007866867312416037, 0.0074367870375188746, 0.006894074807826563, 0.006261891956235823, 0.005565846601043941, 0.004832287695268742, 0.0040866841466468086, 0.003352224190500018, 0.0026487347528244905, 0.0019919771718915017, 0.001393330842623535, 0.0008598360496620314, 0.0003945359923225235, -2.961614437397859e-06],
        },
        "y180_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.00033790660909073413, 0.0003991454854280062, 0.00046105389653773474, 0.0005205248544757129, 0.0005738722058233859, 0.000617016884993855, 0.0006457542603741454, 0.0006560876931537517, 0.0006446015679775945, 0.0006088369823766905, 0.0005476269870537059, 0.000461347392199203, 0.0003520446113368174, 0.00022341371268528345, 8.06165838434419e-05, -7.005031842521868e-05, -0.00022160964599710577, -0.00036693287296661365, -0.0004992900383153618, -0.0006128604698415076, -0.0007031505129065542, -0.0007672766550175834, -0.0008040900852385937, -0.0008141388291461914, -0.0007994830511816149, -0.0007633950985308404, -0.0007099863181225018, -0.000643806614811539, -0.0005694602707824865, -0.0004912738373510493, -0.00041304074042124725, -0.00033785469040239027],
        },
        "y180_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0007961910145573403, 0.0017280195071082464, 0.0027962156969548583, 0.003994627624949033, 0.005309101044323274, 0.006716799952742642, 0.008186126760919126, 0.009677361641019061, 0.011144077886459651, 0.012535309395251042, 0.013798356751843575, 0.014882031726641296, 0.015740069316873568, 0.01633439361157253, 0.016637917383906582, 0.01663658892578684, 0.01633047072065311, 0.015733734624832074, 0.014873574075037749, 0.013788149615653125, 0.012523783912471645, 0.011131693202087883, 0.009664575390537484, 0.008173368293293617, 0.006704448381000036, 0.005297469505648981, 0.003983954343783003, 0.00278666168524707, 0.0017196720993240629, 0.000789071984645047, -5.923228874795718e-06],
        },
        "minus_y90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.00016895330454536707, -0.0001995727427140031, -0.00023052694826886737, -0.00026026242723785646, -0.00028693610291169295, -0.0003085084424969275, -0.0003228771301870727, -0.00032804384657687585, -0.00032230078398879725, -0.00030441849118834524, -0.00027381349352685293, -0.0002306736960996015, -0.0001760223056684087, -0.00011170685634264173, -4.030829192172095e-05, 3.502515921260934e-05, 0.00011080482299855288, 0.00018346643648330682, 0.0002496450191576809, 0.0003064302349207538, 0.0003515752564532771, 0.0003836383275087917, 0.00040204504261929684, 0.0004070694145730957, 0.00039974152559080743, 0.0003816975492654202, 0.0003549931590612509, 0.0003219033074057695, 0.00028473013539124327, 0.00024563691867552463, 0.00020652037021062363, 0.00016892734520119513],
        },
        "minus_y90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, -0.00039809550727867014, -0.0008640097535541232, -0.0013981078484774292, -0.0019973138124745166, -0.002654550522161637, -0.003358399976371321, -0.004093063380459563, -0.004838680820509531, -0.0055720389432298255, -0.006267654697625521, -0.006899178375921787, -0.007441015863320648, -0.007870034658436784, -0.008167196805786266, -0.008318958691953291, -0.00831829446289342, -0.008165235360326555, -0.007866867312416037, -0.0074367870375188746, -0.006894074807826563, -0.006261891956235823, -0.005565846601043941, -0.004832287695268742, -0.0040866841466468086, -0.003352224190500018, -0.0026487347528244905, -0.0019919771718915017, -0.001393330842623535, -0.0008598360496620314, -0.0003945359923225235, 2.961614437397859e-06],
        },
        "readout_wf_q1": {
            "type": "constant",
            "sample": 0.0868910316,
        },
        "x90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.0012329577380560015, 0.002675909464344657, 0.004329991012361583, 0.006185690189376297, 0.008221113517348333, 0.010400934191756046, 0.012676267137460572, 0.01498565610620953, 0.017257260875170936, 0.019412207873695107, 0.021368929020068077, 0.023048179568053714, 0.024378316395843955, 0.025300351802257037] + [0.025772287822819078] * 2 + [0.025300351802257037, 0.024378316395843955, 0.023048179568053714, 0.021368929020068077, 0.019412207873695107, 0.017257260875170936, 0.01498565610620953, 0.012676267137460572, 0.010400934191756046, 0.008221113517348333, 0.006185690189376297, 0.004329991012361583, 0.002675909464344657, 0.0012329577380560015, 0.0],
        },
        "x90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "x180_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.002465915476112003, 0.005351818928689314, 0.008659982024723166, 0.012371380378752595, 0.016442227034696666, 0.02080186838351209, 0.025352534274921144, 0.02997131221241906, 0.03451452175034187, 0.03882441574739021, 0.042737858040136155, 0.04609635913610743, 0.04875663279168791, 0.050600703604514075] + [0.051544575645638156] * 2 + [0.050600703604514075, 0.04875663279168791, 0.04609635913610743, 0.042737858040136155, 0.03882441574739021, 0.03451452175034187, 0.02997131221241906, 0.025352534274921144, 0.02080186838351209, 0.016442227034696666, 0.012371380378752595, 0.008659982024723166, 0.005351818928689314, 0.002465915476112003, 0.0],
        },
        "x180_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "minus_x90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, -0.0012329577380560015, -0.002675909464344657, -0.004329991012361583, -0.006185690189376297, -0.008221113517348333, -0.010400934191756046, -0.012676267137460572, -0.01498565610620953, -0.017257260875170936, -0.019412207873695107, -0.021368929020068077, -0.023048179568053714, -0.024378316395843955, -0.025300351802257037] + [-0.025772287822819078] * 2 + [-0.025300351802257037, -0.024378316395843955, -0.023048179568053714, -0.021368929020068077, -0.019412207873695107, -0.017257260875170936, -0.01498565610620953, -0.012676267137460572, -0.010400934191756046, -0.008221113517348333, -0.006185690189376297, -0.004329991012361583, -0.002675909464344657, -0.0012329577380560015, 0.0],
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
            "samples": [0.0, 0.0012329577380560015, 0.002675909464344657, 0.004329991012361583, 0.006185690189376297, 0.008221113517348333, 0.010400934191756046, 0.012676267137460572, 0.01498565610620953, 0.017257260875170936, 0.019412207873695107, 0.021368929020068077, 0.023048179568053714, 0.024378316395843955, 0.025300351802257037] + [0.025772287822819078] * 2 + [0.025300351802257037, 0.024378316395843955, 0.023048179568053714, 0.021368929020068077, 0.019412207873695107, 0.017257260875170936, 0.01498565610620953, 0.012676267137460572, 0.010400934191756046, 0.008221113517348333, 0.006185690189376297, 0.004329991012361583, 0.002675909464344657, 0.0012329577380560015, 0.0],
        },
        "y180_I_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "y180_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.002465915476112003, 0.005351818928689314, 0.008659982024723166, 0.012371380378752595, 0.016442227034696666, 0.02080186838351209, 0.025352534274921144, 0.02997131221241906, 0.03451452175034187, 0.03882441574739021, 0.042737858040136155, 0.04609635913610743, 0.04875663279168791, 0.050600703604514075] + [0.051544575645638156] * 2 + [0.050600703604514075, 0.04875663279168791, 0.04609635913610743, 0.042737858040136155, 0.03882441574739021, 0.03451452175034187, 0.02997131221241906, 0.025352534274921144, 0.02080186838351209, 0.016442227034696666, 0.012371380378752595, 0.008659982024723166, 0.005351818928689314, 0.002465915476112003, 0.0],
        },
        "minus_y90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "minus_y90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, -0.0012329577380560015, -0.002675909464344657, -0.004329991012361583, -0.006185690189376297, -0.008221113517348333, -0.010400934191756046, -0.012676267137460572, -0.01498565610620953, -0.017257260875170936, -0.019412207873695107, -0.021368929020068077, -0.023048179568053714, -0.024378316395843955, -0.025300351802257037] + [-0.025772287822819078] * 2 + [-0.025300351802257037, -0.024378316395843955, -0.023048179568053714, -0.021368929020068077, -0.019412207873695107, -0.017257260875170936, -0.01498565610620953, -0.012676267137460572, -0.010400934191756046, -0.008221113517348333, -0.006185690189376297, -0.004329991012361583, -0.002675909464344657, -0.0012329577380560015, 0.0],
        },
        "readout_wf_q2": {
            "type": "constant",
            "sample": 0.1309075425,
        },
        "x90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.00043497132004860907, 0.0009440257651261808, 0.0015275640423937913, 0.0021822303750061956, 0.002900301031038298, 0.0036693131771572147, 0.004472020799969697, 0.005286742941075888, 0.006088135312027518, 0.006848372351506864, 0.007538677910030576, 0.008131095480401902, 0.008600350308828884, 0.008925632307943795] + [0.009092125146673223] * 2 + [0.008925632307943795, 0.008600350308828884, 0.008131095480401902, 0.007538677910030576, 0.006848372351506864, 0.006088135312027518, 0.005286742941075888, 0.004472020799969697, 0.0036693131771572147, 0.002900301031038298, 0.0021822303750061956, 0.0015275640423937913, 0.0009440257651261808, 0.00043497132004860907, 0.0],
        },
        "x90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "x180_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0008699426400972181, 0.0018880515302523615, 0.0030551280847875826, 0.004364460750012391, 0.005800602062076596, 0.007338626354314429, 0.008944041599939395, 0.010573485882151776, 0.012176270624055036, 0.013696744703013727, 0.015077355820061152, 0.016262190960803804, 0.017200700617657768, 0.01785126461588759] + [0.018184250293346447] * 2 + [0.01785126461588759, 0.017200700617657768, 0.016262190960803804, 0.015077355820061152, 0.013696744703013727, 0.012176270624055036, 0.010573485882151776, 0.008944041599939395, 0.007338626354314429, 0.005800602062076596, 0.004364460750012391, 0.0030551280847875826, 0.0018880515302523615, 0.0008699426400972181, 0.0],
        },
        "x180_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "minus_x90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, -0.00043497132004860907, -0.0009440257651261808, -0.0015275640423937913, -0.0021822303750061956, -0.002900301031038298, -0.0036693131771572147, -0.004472020799969697, -0.005286742941075888, -0.006088135312027518, -0.006848372351506864, -0.007538677910030576, -0.008131095480401902, -0.008600350308828884, -0.008925632307943795] + [-0.009092125146673223] * 2 + [-0.008925632307943795, -0.008600350308828884, -0.008131095480401902, -0.007538677910030576, -0.006848372351506864, -0.006088135312027518, -0.005286742941075888, -0.004472020799969697, -0.0036693131771572147, -0.002900301031038298, -0.0021822303750061956, -0.0015275640423937913, -0.0009440257651261808, -0.00043497132004860907, 0.0],
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
            "samples": [0.0, 0.00043497132004860907, 0.0009440257651261808, 0.0015275640423937913, 0.0021822303750061956, 0.002900301031038298, 0.0036693131771572147, 0.004472020799969697, 0.005286742941075888, 0.006088135312027518, 0.006848372351506864, 0.007538677910030576, 0.008131095480401902, 0.008600350308828884, 0.008925632307943795] + [0.009092125146673223] * 2 + [0.008925632307943795, 0.008600350308828884, 0.008131095480401902, 0.007538677910030576, 0.006848372351506864, 0.006088135312027518, 0.005286742941075888, 0.004472020799969697, 0.0036693131771572147, 0.002900301031038298, 0.0021822303750061956, 0.0015275640423937913, 0.0009440257651261808, 0.00043497132004860907, 0.0],
        },
        "y180_I_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "y180_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0008699426400972181, 0.0018880515302523615, 0.0030551280847875826, 0.004364460750012391, 0.005800602062076596, 0.007338626354314429, 0.008944041599939395, 0.010573485882151776, 0.012176270624055036, 0.013696744703013727, 0.015077355820061152, 0.016262190960803804, 0.017200700617657768, 0.01785126461588759] + [0.018184250293346447] * 2 + [0.01785126461588759, 0.017200700617657768, 0.016262190960803804, 0.015077355820061152, 0.013696744703013727, 0.012176270624055036, 0.010573485882151776, 0.008944041599939395, 0.007338626354314429, 0.005800602062076596, 0.004364460750012391, 0.0030551280847875826, 0.0018880515302523615, 0.0008699426400972181, 0.0],
        },
        "minus_y90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "minus_y90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, -0.00043497132004860907, -0.0009440257651261808, -0.0015275640423937913, -0.0021822303750061956, -0.002900301031038298, -0.0036693131771572147, -0.004472020799969697, -0.005286742941075888, -0.006088135312027518, -0.006848372351506864, -0.007538677910030576, -0.008131095480401902, -0.008600350308828884, -0.008925632307943795] + [-0.009092125146673223] * 2 + [-0.008925632307943795, -0.008600350308828884, -0.008131095480401902, -0.007538677910030576, -0.006848372351506864, -0.006088135312027518, -0.005286742941075888, -0.004472020799969697, -0.0036693131771572147, -0.002900301031038298, -0.0021822303750061956, -0.0015275640423937913, -0.0009440257651261808, -0.00043497132004860907, 0.0],
        },
        "readout_wf_q3": {
            "type": "constant",
            "sample": 0.102461516,
        },
        "x90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0016978434425689208, 0.003684858934507397, 0.005962610574399557, 0.008517999605042771, 0.011320877630446886, 0.014322597903401766, 0.017455843271257182, 0.020635985457731158, 0.02376409694285834, 0.026731564940826052, 0.02942606619156916, 0.03173847678223791, 0.033570140610670374, 0.034839828711304775] + [0.03548970782158693] * 2 + [0.034839828711304775, 0.033570140610670374, 0.03173847678223791, 0.02942606619156916, 0.026731564940826052, 0.02376409694285834, 0.020635985457731158, 0.017455843271257182, 0.014322597903401766, 0.011320877630446886, 0.008517999605042771, 0.005962610574399557, 0.003684858934507397, 0.0016978434425689208, 0.0],
        },
        "x90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "x180_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0033956868851378417, 0.007369717869014794, 0.011925221148799113, 0.017035999210085542, 0.02264175526089377, 0.028645195806803532, 0.034911686542514364, 0.041271970915462315, 0.04752819388571668, 0.053463129881652104, 0.05885213238313832, 0.06347695356447582, 0.06714028122134075, 0.06967965742260955] + [0.07097941564317387] * 2 + [0.06967965742260955, 0.06714028122134075, 0.06347695356447582, 0.05885213238313832, 0.053463129881652104, 0.04752819388571668, 0.041271970915462315, 0.034911686542514364, 0.028645195806803532, 0.02264175526089377, 0.017035999210085542, 0.011925221148799113, 0.007369717869014794, 0.0033956868851378417, 0.0],
        },
        "x180_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "minus_x90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, -0.0016978434425689208, -0.003684858934507397, -0.005962610574399557, -0.008517999605042771, -0.011320877630446886, -0.014322597903401766, -0.017455843271257182, -0.020635985457731158, -0.02376409694285834, -0.026731564940826052, -0.02942606619156916, -0.03173847678223791, -0.033570140610670374, -0.034839828711304775] + [-0.03548970782158693] * 2 + [-0.034839828711304775, -0.033570140610670374, -0.03173847678223791, -0.02942606619156916, -0.026731564940826052, -0.02376409694285834, -0.020635985457731158, -0.017455843271257182, -0.014322597903401766, -0.011320877630446886, -0.008517999605042771, -0.005962610574399557, -0.003684858934507397, -0.0016978434425689208, 0.0],
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
            "samples": [0.0, 0.0016978434425689208, 0.003684858934507397, 0.005962610574399557, 0.008517999605042771, 0.011320877630446886, 0.014322597903401766, 0.017455843271257182, 0.020635985457731158, 0.02376409694285834, 0.026731564940826052, 0.02942606619156916, 0.03173847678223791, 0.033570140610670374, 0.034839828711304775] + [0.03548970782158693] * 2 + [0.034839828711304775, 0.033570140610670374, 0.03173847678223791, 0.02942606619156916, 0.026731564940826052, 0.02376409694285834, 0.020635985457731158, 0.017455843271257182, 0.014322597903401766, 0.011320877630446886, 0.008517999605042771, 0.005962610574399557, 0.003684858934507397, 0.0016978434425689208, 0.0],
        },
        "y180_I_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "y180_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0033956868851378417, 0.007369717869014794, 0.011925221148799113, 0.017035999210085542, 0.02264175526089377, 0.028645195806803532, 0.034911686542514364, 0.041271970915462315, 0.04752819388571668, 0.053463129881652104, 0.05885213238313832, 0.06347695356447582, 0.06714028122134075, 0.06967965742260955] + [0.07097941564317387] * 2 + [0.06967965742260955, 0.06714028122134075, 0.06347695356447582, 0.05885213238313832, 0.053463129881652104, 0.04752819388571668, 0.041271970915462315, 0.034911686542514364, 0.028645195806803532, 0.02264175526089377, 0.017035999210085542, 0.011925221148799113, 0.007369717869014794, 0.0033956868851378417, 0.0],
        },
        "minus_y90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "minus_y90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, -0.0016978434425689208, -0.003684858934507397, -0.005962610574399557, -0.008517999605042771, -0.011320877630446886, -0.014322597903401766, -0.017455843271257182, -0.020635985457731158, -0.02376409694285834, -0.026731564940826052, -0.02942606619156916, -0.03173847678223791, -0.033570140610670374, -0.034839828711304775] + [-0.03548970782158693] * 2 + [-0.034839828711304775, -0.033570140610670374, -0.03173847678223791, -0.02942606619156916, -0.026731564940826052, -0.02376409694285834, -0.020635985457731158, -0.017455843271257182, -0.014322597903401766, -0.011320877630446886, -0.008517999605042771, -0.005962610574399557, -0.003684858934507397, -0.0016978434425689208, 0.0],
        },
        "readout_wf_q4": {
            "type": "constant",
            "sample": 0.218746665,
        },
        "x90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.002405278210305969, 0.005220216823885479, 0.008447031647066037, 0.012067166107143926, 0.01603790997646642, 0.020290347029819168, 0.02472911130094767, 0.029234312731785807, 0.03366580400238264, 0.037869716999503575, 0.04168692710472298, 0.044962842108170364, 0.04755769919844968, 0.049356424007681754] + [0.050277086080581485] * 2 + [0.049356424007681754, 0.04755769919844968, 0.044962842108170364, 0.04168692710472298, 0.037869716999503575, 0.03366580400238264, 0.029234312731785807, 0.02472911130094767, 0.020290347029819168, 0.01603790997646642, 0.012067166107143926, 0.008447031647066037, 0.005220216823885479, 0.002405278210305969, 0.0],
        },
        "x90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "x180_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.004810556420611938, 0.010440433647770957, 0.016894063294132074, 0.024134332214287853, 0.03207581995293284, 0.040580694059638336, 0.04945822260189534, 0.058468625463571615, 0.06733160800476529, 0.07573943399900715, 0.08337385420944596, 0.08992568421634073, 0.09511539839689936, 0.09871284801536351] + [0.10055417216116297] * 2 + [0.09871284801536351, 0.09511539839689936, 0.08992568421634073, 0.08337385420944596, 0.07573943399900715, 0.06733160800476529, 0.058468625463571615, 0.04945822260189534, 0.040580694059638336, 0.03207581995293284, 0.024134332214287853, 0.016894063294132074, 0.010440433647770957, 0.004810556420611938, 0.0],
        },
        "x180_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "minus_x90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, -0.002405278210305969, -0.005220216823885479, -0.008447031647066037, -0.012067166107143926, -0.01603790997646642, -0.020290347029819168, -0.02472911130094767, -0.029234312731785807, -0.03366580400238264, -0.037869716999503575, -0.04168692710472298, -0.044962842108170364, -0.04755769919844968, -0.049356424007681754] + [-0.050277086080581485] * 2 + [-0.049356424007681754, -0.04755769919844968, -0.044962842108170364, -0.04168692710472298, -0.037869716999503575, -0.03366580400238264, -0.029234312731785807, -0.02472911130094767, -0.020290347029819168, -0.01603790997646642, -0.012067166107143926, -0.008447031647066037, -0.005220216823885479, -0.002405278210305969, 0.0],
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
            "samples": [0.0, 0.002405278210305969, 0.005220216823885479, 0.008447031647066037, 0.012067166107143926, 0.01603790997646642, 0.020290347029819168, 0.02472911130094767, 0.029234312731785807, 0.03366580400238264, 0.037869716999503575, 0.04168692710472298, 0.044962842108170364, 0.04755769919844968, 0.049356424007681754] + [0.050277086080581485] * 2 + [0.049356424007681754, 0.04755769919844968, 0.044962842108170364, 0.04168692710472298, 0.037869716999503575, 0.03366580400238264, 0.029234312731785807, 0.02472911130094767, 0.020290347029819168, 0.01603790997646642, 0.012067166107143926, 0.008447031647066037, 0.005220216823885479, 0.002405278210305969, 0.0],
        },
        "y180_I_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "y180_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.004810556420611938, 0.010440433647770957, 0.016894063294132074, 0.024134332214287853, 0.03207581995293284, 0.040580694059638336, 0.04945822260189534, 0.058468625463571615, 0.06733160800476529, 0.07573943399900715, 0.08337385420944596, 0.08992568421634073, 0.09511539839689936, 0.09871284801536351] + [0.10055417216116297] * 2 + [0.09871284801536351, 0.09511539839689936, 0.08992568421634073, 0.08337385420944596, 0.07573943399900715, 0.06733160800476529, 0.058468625463571615, 0.04945822260189534, 0.040580694059638336, 0.03207581995293284, 0.024134332214287853, 0.016894063294132074, 0.010440433647770957, 0.004810556420611938, 0.0],
        },
        "minus_y90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "minus_y90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, -0.002405278210305969, -0.005220216823885479, -0.008447031647066037, -0.012067166107143926, -0.01603790997646642, -0.020290347029819168, -0.02472911130094767, -0.029234312731785807, -0.03366580400238264, -0.037869716999503575, -0.04168692710472298, -0.044962842108170364, -0.04755769919844968, -0.049356424007681754] + [-0.050277086080581485] * 2 + [-0.049356424007681754, -0.04755769919844968, -0.044962842108170364, -0.04168692710472298, -0.037869716999503575, -0.03366580400238264, -0.029234312731785807, -0.02472911130094767, -0.020290347029819168, -0.01603790997646642, -0.012067166107143926, -0.008447031647066037, -0.005220216823885479, -0.002405278210305969, 0.0],
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
            "cosine": [(0.971134279909636, 1800)],
            "sine": [(-0.23853345757858122, 1800)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(0.23853345757858122, 1800)],
            "sine": [(0.971134279909636, 1800)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(-0.23853345757858122, 1800)],
            "sine": [(-0.971134279909636, 1800)],
        },
        "rotated_cosine_weights_q2": {
            "cosine": [(-0.45243470931178276, 1800)],
            "sine": [(0.8917975296052141, 1800)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(-0.8917975296052141, 1800)],
            "sine": [(-0.45243470931178276, 1800)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(0.8917975296052141, 1800)],
            "sine": [(0.45243470931178276, 1800)],
        },
        "rotated_cosine_weights_q3": {
            "cosine": [(0.8754645270000179, 1800)],
            "sine": [(0.4832823832550023, 1800)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(-0.4832823832550023, 1800)],
            "sine": [(0.8754645270000179, 1800)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(0.4832823832550023, 1800)],
            "sine": [(-0.8754645270000179, 1800)],
        },
        "rotated_cosine_weights_q4": {
            "cosine": [(-0.981627183447664, 1800)],
            "sine": [(-0.19080899537654472, 1800)],
        },
        "rotated_sine_weights_q4": {
            "cosine": [(0.19080899537654472, 1800)],
            "sine": [(-0.981627183447664, 1800)],
        },
        "rotated_minus_sine_weights_q4": {
            "cosine": [(-0.19080899537654472, 1800)],
            "sine": [(0.981627183447664, 1800)],
        },
        "rotated_cosine_weights_q5": {
            "cosine": [(-0.9993908270190958, 1800)],
            "sine": [(0.03489949670250114, 1800)],
        },
        "rotated_sine_weights_q5": {
            "cosine": [(-0.03489949670250114, 1800)],
            "sine": [(-0.9993908270190958, 1800)],
        },
        "rotated_minus_sine_weights_q5": {
            "cosine": [(0.03489949670250114, 1800)],
            "sine": [(0.9993908270190958, 1800)],
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
        "octave_octave1_2": [{'intermediate_frequency': -130602000, 'lo_frequency': 3200000000, 'correction': (1, 0, 0, 1)}],
        "octave_octave1_3": [{'intermediate_frequency': -261857000, 'lo_frequency': 3200000000, 'correction': (1, 0, 0, 1)}],
        "octave_octave1_4": [{'intermediate_frequency': -106551000, 'lo_frequency': 3960000000, 'correction': (1, 0, 0, 1)}],
        "octave_octave1_5": [{'intermediate_frequency': -368712000, 'lo_frequency': 3960000000, 'correction': (1, 0, 0, 1)}],
        "octave_octave2_1": [{'intermediate_frequency': -122859000, 'lo_frequency': 4600000000, 'correction': (1, 0, 0, 1)}],
        "octave_octave1_1": [
            {'intermediate_frequency': -163122000, 'lo_frequency': 5900000000, 'correction': (1, 0, 0, 1)},
            {'intermediate_frequency': 126410000, 'lo_frequency': 5900000000, 'correction': (1, 0, 0, 1)},
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
            "intermediate_frequency": 130602000.0,
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
            "intermediate_frequency": 106551000.0,
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
            "intermediate_frequency": 261857000.0,
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
            "intermediate_frequency": 368712000.0,
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
            "intermediate_frequency": 122859000.0,
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
            "length": 260,
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
        "cz5_4": {
            "length": 260,
            "waveforms": {
                "single": "const_flux_wf",
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
            "sample": 0.022,
            "type": "constant",
        },
        "zero_wf": {
            "sample": 0.0,
            "type": "constant",
        },
        "x90_I_wf_q1": {
            "samples": [0.0, 0.00039809550727867014, 0.0008640097535541232, 0.0013981078484774292, 0.0019973138124745166, 0.002654550522161637, 0.003358399976371321, 0.004093063380459563, 0.004838680820509531, 0.0055720389432298255, 0.006267654697625521, 0.006899178375921787, 0.007441015863320648, 0.007870034658436784, 0.008167196805786266, 0.008318958691953291, 0.00831829446289342, 0.008165235360326555, 0.007866867312416037, 0.0074367870375188746, 0.006894074807826563, 0.006261891956235823, 0.005565846601043941, 0.004832287695268742, 0.0040866841466468086, 0.003352224190500018, 0.0026487347528244905, 0.0019919771718915017, 0.001393330842623535, 0.0008598360496620314, 0.0003945359923225235, -2.961614437397859e-06],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x90_Q_wf_q1": {
            "samples": [-0.00016895330454536707, -0.0001995727427140031, -0.00023052694826886737, -0.00026026242723785646, -0.00028693610291169295, -0.0003085084424969275, -0.0003228771301870727, -0.00032804384657687585, -0.00032230078398879725, -0.00030441849118834524, -0.00027381349352685293, -0.0002306736960996015, -0.0001760223056684087, -0.00011170685634264173, -4.030829192172095e-05, 3.502515921260934e-05, 0.00011080482299855288, 0.00018346643648330682, 0.0002496450191576809, 0.0003064302349207538, 0.0003515752564532771, 0.0003836383275087917, 0.00040204504261929684, 0.0004070694145730957, 0.00039974152559080743, 0.0003816975492654202, 0.0003549931590612509, 0.0003219033074057695, 0.00028473013539124327, 0.00024563691867552463, 0.00020652037021062363, 0.00016892734520119513],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_I_wf_q1": {
            "samples": [0.0, 0.0007961910145573403, 0.0017280195071082464, 0.0027962156969548583, 0.003994627624949033, 0.005309101044323274, 0.006716799952742642, 0.008186126760919126, 0.009677361641019061, 0.011144077886459651, 0.012535309395251042, 0.013798356751843575, 0.014882031726641296, 0.015740069316873568, 0.01633439361157253, 0.016637917383906582, 0.01663658892578684, 0.01633047072065311, 0.015733734624832074, 0.014873574075037749, 0.013788149615653125, 0.012523783912471645, 0.011131693202087883, 0.009664575390537484, 0.008173368293293617, 0.006704448381000036, 0.005297469505648981, 0.003983954343783003, 0.00278666168524707, 0.0017196720993240629, 0.000789071984645047, -5.923228874795718e-06],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "x180_Q_wf_q1": {
            "samples": [-0.00033790660909073413, -0.0003991454854280062, -0.00046105389653773474, -0.0005205248544757129, -0.0005738722058233859, -0.000617016884993855, -0.0006457542603741454, -0.0006560876931537517, -0.0006446015679775945, -0.0006088369823766905, -0.0005476269870537059, -0.000461347392199203, -0.0003520446113368174, -0.00022341371268528345, -8.06165838434419e-05, 7.005031842521868e-05, 0.00022160964599710577, 0.00036693287296661365, 0.0004992900383153618, 0.0006128604698415076, 0.0007031505129065542, 0.0007672766550175834, 0.0008040900852385937, 0.0008141388291461914, 0.0007994830511816149, 0.0007633950985308404, 0.0007099863181225018, 0.000643806614811539, 0.0005694602707824865, 0.0004912738373510493, 0.00041304074042124725, 0.00033785469040239027],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_I_wf_q1": {
            "samples": [0.0, -0.00039809550727867014, -0.0008640097535541232, -0.0013981078484774292, -0.0019973138124745166, -0.002654550522161637, -0.003358399976371321, -0.004093063380459563, -0.004838680820509531, -0.0055720389432298255, -0.006267654697625521, -0.006899178375921787, -0.007441015863320648, -0.007870034658436784, -0.008167196805786266, -0.008318958691953291, -0.00831829446289342, -0.008165235360326555, -0.007866867312416037, -0.0074367870375188746, -0.006894074807826563, -0.006261891956235823, -0.005565846601043941, -0.004832287695268742, -0.0040866841466468086, -0.003352224190500018, -0.0026487347528244905, -0.0019919771718915017, -0.001393330842623535, -0.0008598360496620314, -0.0003945359923225235, 2.961614437397859e-06],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_x90_Q_wf_q1": {
            "samples": [0.00016895330454536707, 0.0001995727427140031, 0.00023052694826886737, 0.00026026242723785646, 0.00028693610291169295, 0.0003085084424969275, 0.0003228771301870727, 0.00032804384657687585, 0.00032230078398879725, 0.00030441849118834524, 0.00027381349352685293, 0.0002306736960996015, 0.0001760223056684087, 0.00011170685634264173, 4.030829192172095e-05, -3.502515921260934e-05, -0.00011080482299855288, -0.00018346643648330682, -0.0002496450191576809, -0.0003064302349207538, -0.0003515752564532771, -0.0003836383275087917, -0.00040204504261929684, -0.0004070694145730957, -0.00039974152559080743, -0.0003816975492654202, -0.0003549931590612509, -0.0003219033074057695, -0.00028473013539124327, -0.00024563691867552463, -0.00020652037021062363, -0.00016892734520119513],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_I_wf_q1": {
            "samples": [0.00016895330454536707, 0.0001995727427140031, 0.00023052694826886737, 0.00026026242723785646, 0.00028693610291169295, 0.0003085084424969275, 0.0003228771301870727, 0.00032804384657687585, 0.00032230078398879725, 0.00030441849118834524, 0.00027381349352685293, 0.0002306736960996015, 0.0001760223056684087, 0.00011170685634264173, 4.030829192172095e-05, -3.502515921260934e-05, -0.00011080482299855288, -0.00018346643648330682, -0.0002496450191576809, -0.0003064302349207538, -0.0003515752564532771, -0.0003836383275087917, -0.00040204504261929684, -0.0004070694145730957, -0.00039974152559080743, -0.0003816975492654202, -0.0003549931590612509, -0.0003219033074057695, -0.00028473013539124327, -0.00024563691867552463, -0.00020652037021062363, -0.00016892734520119513],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y90_Q_wf_q1": {
            "samples": [0.0, 0.00039809550727867014, 0.0008640097535541232, 0.0013981078484774292, 0.0019973138124745166, 0.002654550522161637, 0.003358399976371321, 0.004093063380459563, 0.004838680820509531, 0.0055720389432298255, 0.006267654697625521, 0.006899178375921787, 0.007441015863320648, 0.007870034658436784, 0.008167196805786266, 0.008318958691953291, 0.00831829446289342, 0.008165235360326555, 0.007866867312416037, 0.0074367870375188746, 0.006894074807826563, 0.006261891956235823, 0.005565846601043941, 0.004832287695268742, 0.0040866841466468086, 0.003352224190500018, 0.0026487347528244905, 0.0019919771718915017, 0.001393330842623535, 0.0008598360496620314, 0.0003945359923225235, -2.961614437397859e-06],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_I_wf_q1": {
            "samples": [0.00033790660909073413, 0.0003991454854280062, 0.00046105389653773474, 0.0005205248544757129, 0.0005738722058233859, 0.000617016884993855, 0.0006457542603741454, 0.0006560876931537517, 0.0006446015679775945, 0.0006088369823766905, 0.0005476269870537059, 0.000461347392199203, 0.0003520446113368174, 0.00022341371268528345, 8.06165838434419e-05, -7.005031842521868e-05, -0.00022160964599710577, -0.00036693287296661365, -0.0004992900383153618, -0.0006128604698415076, -0.0007031505129065542, -0.0007672766550175834, -0.0008040900852385937, -0.0008141388291461914, -0.0007994830511816149, -0.0007633950985308404, -0.0007099863181225018, -0.000643806614811539, -0.0005694602707824865, -0.0004912738373510493, -0.00041304074042124725, -0.00033785469040239027],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "y180_Q_wf_q1": {
            "samples": [0.0, 0.0007961910145573403, 0.0017280195071082464, 0.0027962156969548583, 0.003994627624949033, 0.005309101044323274, 0.006716799952742642, 0.008186126760919126, 0.009677361641019061, 0.011144077886459651, 0.012535309395251042, 0.013798356751843575, 0.014882031726641296, 0.015740069316873568, 0.01633439361157253, 0.016637917383906582, 0.01663658892578684, 0.01633047072065311, 0.015733734624832074, 0.014873574075037749, 0.013788149615653125, 0.012523783912471645, 0.011131693202087883, 0.009664575390537484, 0.008173368293293617, 0.006704448381000036, 0.005297469505648981, 0.003983954343783003, 0.00278666168524707, 0.0017196720993240629, 0.000789071984645047, -5.923228874795718e-06],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_I_wf_q1": {
            "samples": [-0.00016895330454536707, -0.0001995727427140031, -0.00023052694826886737, -0.00026026242723785646, -0.00028693610291169295, -0.0003085084424969275, -0.0003228771301870727, -0.00032804384657687585, -0.00032230078398879725, -0.00030441849118834524, -0.00027381349352685293, -0.0002306736960996015, -0.0001760223056684087, -0.00011170685634264173, -4.030829192172095e-05, 3.502515921260934e-05, 0.00011080482299855288, 0.00018346643648330682, 0.0002496450191576809, 0.0003064302349207538, 0.0003515752564532771, 0.0003836383275087917, 0.00040204504261929684, 0.0004070694145730957, 0.00039974152559080743, 0.0003816975492654202, 0.0003549931590612509, 0.0003219033074057695, 0.00028473013539124327, 0.00024563691867552463, 0.00020652037021062363, 0.00016892734520119513],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "minus_y90_Q_wf_q1": {
            "samples": [0.0, -0.00039809550727867014, -0.0008640097535541232, -0.0013981078484774292, -0.0019973138124745166, -0.002654550522161637, -0.003358399976371321, -0.004093063380459563, -0.004838680820509531, -0.0055720389432298255, -0.006267654697625521, -0.006899178375921787, -0.007441015863320648, -0.007870034658436784, -0.008167196805786266, -0.008318958691953291, -0.00831829446289342, -0.008165235360326555, -0.007866867312416037, -0.0074367870375188746, -0.006894074807826563, -0.006261891956235823, -0.005565846601043941, -0.004832287695268742, -0.0040866841466468086, -0.003352224190500018, -0.0026487347528244905, -0.0019919771718915017, -0.001393330842623535, -0.0008598360496620314, -0.0003945359923225235, 2.961614437397859e-06],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q1": {
            "sample": 0.0868910316,
            "type": "constant",
        },
        "x90_I_wf_q2": {
            "samples": [0.0, 0.0012329577380560015, 0.002675909464344657, 0.004329991012361583, 0.006185690189376297, 0.008221113517348333, 0.010400934191756046, 0.012676267137460572, 0.01498565610620953, 0.017257260875170936, 0.019412207873695107, 0.021368929020068077, 0.023048179568053714, 0.024378316395843955, 0.025300351802257037] + [0.025772287822819078] * 2 + [0.025300351802257037, 0.024378316395843955, 0.023048179568053714, 0.021368929020068077, 0.019412207873695107, 0.017257260875170936, 0.01498565610620953, 0.012676267137460572, 0.010400934191756046, 0.008221113517348333, 0.006185690189376297, 0.004329991012361583, 0.002675909464344657, 0.0012329577380560015, 0.0],
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
            "samples": [0.0, 0.002465915476112003, 0.005351818928689314, 0.008659982024723166, 0.012371380378752595, 0.016442227034696666, 0.02080186838351209, 0.025352534274921144, 0.02997131221241906, 0.03451452175034187, 0.03882441574739021, 0.042737858040136155, 0.04609635913610743, 0.04875663279168791, 0.050600703604514075] + [0.051544575645638156] * 2 + [0.050600703604514075, 0.04875663279168791, 0.04609635913610743, 0.042737858040136155, 0.03882441574739021, 0.03451452175034187, 0.02997131221241906, 0.025352534274921144, 0.02080186838351209, 0.016442227034696666, 0.012371380378752595, 0.008659982024723166, 0.005351818928689314, 0.002465915476112003, 0.0],
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
            "samples": [0.0, -0.0012329577380560015, -0.002675909464344657, -0.004329991012361583, -0.006185690189376297, -0.008221113517348333, -0.010400934191756046, -0.012676267137460572, -0.01498565610620953, -0.017257260875170936, -0.019412207873695107, -0.021368929020068077, -0.023048179568053714, -0.024378316395843955, -0.025300351802257037] + [-0.025772287822819078] * 2 + [-0.025300351802257037, -0.024378316395843955, -0.023048179568053714, -0.021368929020068077, -0.019412207873695107, -0.017257260875170936, -0.01498565610620953, -0.012676267137460572, -0.010400934191756046, -0.008221113517348333, -0.006185690189376297, -0.004329991012361583, -0.002675909464344657, -0.0012329577380560015, 0.0],
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
            "samples": [0.0, 0.0012329577380560015, 0.002675909464344657, 0.004329991012361583, 0.006185690189376297, 0.008221113517348333, 0.010400934191756046, 0.012676267137460572, 0.01498565610620953, 0.017257260875170936, 0.019412207873695107, 0.021368929020068077, 0.023048179568053714, 0.024378316395843955, 0.025300351802257037] + [0.025772287822819078] * 2 + [0.025300351802257037, 0.024378316395843955, 0.023048179568053714, 0.021368929020068077, 0.019412207873695107, 0.017257260875170936, 0.01498565610620953, 0.012676267137460572, 0.010400934191756046, 0.008221113517348333, 0.006185690189376297, 0.004329991012361583, 0.002675909464344657, 0.0012329577380560015, 0.0],
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
            "samples": [0.0, 0.002465915476112003, 0.005351818928689314, 0.008659982024723166, 0.012371380378752595, 0.016442227034696666, 0.02080186838351209, 0.025352534274921144, 0.02997131221241906, 0.03451452175034187, 0.03882441574739021, 0.042737858040136155, 0.04609635913610743, 0.04875663279168791, 0.050600703604514075] + [0.051544575645638156] * 2 + [0.050600703604514075, 0.04875663279168791, 0.04609635913610743, 0.042737858040136155, 0.03882441574739021, 0.03451452175034187, 0.02997131221241906, 0.025352534274921144, 0.02080186838351209, 0.016442227034696666, 0.012371380378752595, 0.008659982024723166, 0.005351818928689314, 0.002465915476112003, 0.0],
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
            "samples": [0.0, -0.0012329577380560015, -0.002675909464344657, -0.004329991012361583, -0.006185690189376297, -0.008221113517348333, -0.010400934191756046, -0.012676267137460572, -0.01498565610620953, -0.017257260875170936, -0.019412207873695107, -0.021368929020068077, -0.023048179568053714, -0.024378316395843955, -0.025300351802257037] + [-0.025772287822819078] * 2 + [-0.025300351802257037, -0.024378316395843955, -0.023048179568053714, -0.021368929020068077, -0.019412207873695107, -0.017257260875170936, -0.01498565610620953, -0.012676267137460572, -0.010400934191756046, -0.008221113517348333, -0.006185690189376297, -0.004329991012361583, -0.002675909464344657, -0.0012329577380560015, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q2": {
            "sample": 0.1309075425,
            "type": "constant",
        },
        "x90_I_wf_q3": {
            "samples": [0.0, 0.00043497132004860907, 0.0009440257651261808, 0.0015275640423937913, 0.0021822303750061956, 0.002900301031038298, 0.0036693131771572147, 0.004472020799969697, 0.005286742941075888, 0.006088135312027518, 0.006848372351506864, 0.007538677910030576, 0.008131095480401902, 0.008600350308828884, 0.008925632307943795] + [0.009092125146673223] * 2 + [0.008925632307943795, 0.008600350308828884, 0.008131095480401902, 0.007538677910030576, 0.006848372351506864, 0.006088135312027518, 0.005286742941075888, 0.004472020799969697, 0.0036693131771572147, 0.002900301031038298, 0.0021822303750061956, 0.0015275640423937913, 0.0009440257651261808, 0.00043497132004860907, 0.0],
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
            "samples": [0.0, 0.0008699426400972181, 0.0018880515302523615, 0.0030551280847875826, 0.004364460750012391, 0.005800602062076596, 0.007338626354314429, 0.008944041599939395, 0.010573485882151776, 0.012176270624055036, 0.013696744703013727, 0.015077355820061152, 0.016262190960803804, 0.017200700617657768, 0.01785126461588759] + [0.018184250293346447] * 2 + [0.01785126461588759, 0.017200700617657768, 0.016262190960803804, 0.015077355820061152, 0.013696744703013727, 0.012176270624055036, 0.010573485882151776, 0.008944041599939395, 0.007338626354314429, 0.005800602062076596, 0.004364460750012391, 0.0030551280847875826, 0.0018880515302523615, 0.0008699426400972181, 0.0],
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
            "samples": [0.0, -0.00043497132004860907, -0.0009440257651261808, -0.0015275640423937913, -0.0021822303750061956, -0.002900301031038298, -0.0036693131771572147, -0.004472020799969697, -0.005286742941075888, -0.006088135312027518, -0.006848372351506864, -0.007538677910030576, -0.008131095480401902, -0.008600350308828884, -0.008925632307943795] + [-0.009092125146673223] * 2 + [-0.008925632307943795, -0.008600350308828884, -0.008131095480401902, -0.007538677910030576, -0.006848372351506864, -0.006088135312027518, -0.005286742941075888, -0.004472020799969697, -0.0036693131771572147, -0.002900301031038298, -0.0021822303750061956, -0.0015275640423937913, -0.0009440257651261808, -0.00043497132004860907, 0.0],
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
            "samples": [0.0, 0.00043497132004860907, 0.0009440257651261808, 0.0015275640423937913, 0.0021822303750061956, 0.002900301031038298, 0.0036693131771572147, 0.004472020799969697, 0.005286742941075888, 0.006088135312027518, 0.006848372351506864, 0.007538677910030576, 0.008131095480401902, 0.008600350308828884, 0.008925632307943795] + [0.009092125146673223] * 2 + [0.008925632307943795, 0.008600350308828884, 0.008131095480401902, 0.007538677910030576, 0.006848372351506864, 0.006088135312027518, 0.005286742941075888, 0.004472020799969697, 0.0036693131771572147, 0.002900301031038298, 0.0021822303750061956, 0.0015275640423937913, 0.0009440257651261808, 0.00043497132004860907, 0.0],
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
            "samples": [0.0, 0.0008699426400972181, 0.0018880515302523615, 0.0030551280847875826, 0.004364460750012391, 0.005800602062076596, 0.007338626354314429, 0.008944041599939395, 0.010573485882151776, 0.012176270624055036, 0.013696744703013727, 0.015077355820061152, 0.016262190960803804, 0.017200700617657768, 0.01785126461588759] + [0.018184250293346447] * 2 + [0.01785126461588759, 0.017200700617657768, 0.016262190960803804, 0.015077355820061152, 0.013696744703013727, 0.012176270624055036, 0.010573485882151776, 0.008944041599939395, 0.007338626354314429, 0.005800602062076596, 0.004364460750012391, 0.0030551280847875826, 0.0018880515302523615, 0.0008699426400972181, 0.0],
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
            "samples": [0.0, -0.00043497132004860907, -0.0009440257651261808, -0.0015275640423937913, -0.0021822303750061956, -0.002900301031038298, -0.0036693131771572147, -0.004472020799969697, -0.005286742941075888, -0.006088135312027518, -0.006848372351506864, -0.007538677910030576, -0.008131095480401902, -0.008600350308828884, -0.008925632307943795] + [-0.009092125146673223] * 2 + [-0.008925632307943795, -0.008600350308828884, -0.008131095480401902, -0.007538677910030576, -0.006848372351506864, -0.006088135312027518, -0.005286742941075888, -0.004472020799969697, -0.0036693131771572147, -0.002900301031038298, -0.0021822303750061956, -0.0015275640423937913, -0.0009440257651261808, -0.00043497132004860907, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q3": {
            "sample": 0.102461516,
            "type": "constant",
        },
        "x90_I_wf_q4": {
            "samples": [0.0, 0.0016978434425689208, 0.003684858934507397, 0.005962610574399557, 0.008517999605042771, 0.011320877630446886, 0.014322597903401766, 0.017455843271257182, 0.020635985457731158, 0.02376409694285834, 0.026731564940826052, 0.02942606619156916, 0.03173847678223791, 0.033570140610670374, 0.034839828711304775] + [0.03548970782158693] * 2 + [0.034839828711304775, 0.033570140610670374, 0.03173847678223791, 0.02942606619156916, 0.026731564940826052, 0.02376409694285834, 0.020635985457731158, 0.017455843271257182, 0.014322597903401766, 0.011320877630446886, 0.008517999605042771, 0.005962610574399557, 0.003684858934507397, 0.0016978434425689208, 0.0],
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
            "samples": [0.0, 0.0033956868851378417, 0.007369717869014794, 0.011925221148799113, 0.017035999210085542, 0.02264175526089377, 0.028645195806803532, 0.034911686542514364, 0.041271970915462315, 0.04752819388571668, 0.053463129881652104, 0.05885213238313832, 0.06347695356447582, 0.06714028122134075, 0.06967965742260955] + [0.07097941564317387] * 2 + [0.06967965742260955, 0.06714028122134075, 0.06347695356447582, 0.05885213238313832, 0.053463129881652104, 0.04752819388571668, 0.041271970915462315, 0.034911686542514364, 0.028645195806803532, 0.02264175526089377, 0.017035999210085542, 0.011925221148799113, 0.007369717869014794, 0.0033956868851378417, 0.0],
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
            "samples": [0.0, -0.0016978434425689208, -0.003684858934507397, -0.005962610574399557, -0.008517999605042771, -0.011320877630446886, -0.014322597903401766, -0.017455843271257182, -0.020635985457731158, -0.02376409694285834, -0.026731564940826052, -0.02942606619156916, -0.03173847678223791, -0.033570140610670374, -0.034839828711304775] + [-0.03548970782158693] * 2 + [-0.034839828711304775, -0.033570140610670374, -0.03173847678223791, -0.02942606619156916, -0.026731564940826052, -0.02376409694285834, -0.020635985457731158, -0.017455843271257182, -0.014322597903401766, -0.011320877630446886, -0.008517999605042771, -0.005962610574399557, -0.003684858934507397, -0.0016978434425689208, 0.0],
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
            "samples": [0.0, 0.0016978434425689208, 0.003684858934507397, 0.005962610574399557, 0.008517999605042771, 0.011320877630446886, 0.014322597903401766, 0.017455843271257182, 0.020635985457731158, 0.02376409694285834, 0.026731564940826052, 0.02942606619156916, 0.03173847678223791, 0.033570140610670374, 0.034839828711304775] + [0.03548970782158693] * 2 + [0.034839828711304775, 0.033570140610670374, 0.03173847678223791, 0.02942606619156916, 0.026731564940826052, 0.02376409694285834, 0.020635985457731158, 0.017455843271257182, 0.014322597903401766, 0.011320877630446886, 0.008517999605042771, 0.005962610574399557, 0.003684858934507397, 0.0016978434425689208, 0.0],
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
            "samples": [0.0, 0.0033956868851378417, 0.007369717869014794, 0.011925221148799113, 0.017035999210085542, 0.02264175526089377, 0.028645195806803532, 0.034911686542514364, 0.041271970915462315, 0.04752819388571668, 0.053463129881652104, 0.05885213238313832, 0.06347695356447582, 0.06714028122134075, 0.06967965742260955] + [0.07097941564317387] * 2 + [0.06967965742260955, 0.06714028122134075, 0.06347695356447582, 0.05885213238313832, 0.053463129881652104, 0.04752819388571668, 0.041271970915462315, 0.034911686542514364, 0.028645195806803532, 0.02264175526089377, 0.017035999210085542, 0.011925221148799113, 0.007369717869014794, 0.0033956868851378417, 0.0],
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
            "samples": [0.0, -0.0016978434425689208, -0.003684858934507397, -0.005962610574399557, -0.008517999605042771, -0.011320877630446886, -0.014322597903401766, -0.017455843271257182, -0.020635985457731158, -0.02376409694285834, -0.026731564940826052, -0.02942606619156916, -0.03173847678223791, -0.033570140610670374, -0.034839828711304775] + [-0.03548970782158693] * 2 + [-0.034839828711304775, -0.033570140610670374, -0.03173847678223791, -0.02942606619156916, -0.026731564940826052, -0.02376409694285834, -0.020635985457731158, -0.017455843271257182, -0.014322597903401766, -0.011320877630446886, -0.008517999605042771, -0.005962610574399557, -0.003684858934507397, -0.0016978434425689208, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q4": {
            "sample": 0.218746665,
            "type": "constant",
        },
        "x90_I_wf_q5": {
            "samples": [0.0, 0.002405278210305969, 0.005220216823885479, 0.008447031647066037, 0.012067166107143926, 0.01603790997646642, 0.020290347029819168, 0.02472911130094767, 0.029234312731785807, 0.03366580400238264, 0.037869716999503575, 0.04168692710472298, 0.044962842108170364, 0.04755769919844968, 0.049356424007681754] + [0.050277086080581485] * 2 + [0.049356424007681754, 0.04755769919844968, 0.044962842108170364, 0.04168692710472298, 0.037869716999503575, 0.03366580400238264, 0.029234312731785807, 0.02472911130094767, 0.020290347029819168, 0.01603790997646642, 0.012067166107143926, 0.008447031647066037, 0.005220216823885479, 0.002405278210305969, 0.0],
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
            "samples": [0.0, 0.004810556420611938, 0.010440433647770957, 0.016894063294132074, 0.024134332214287853, 0.03207581995293284, 0.040580694059638336, 0.04945822260189534, 0.058468625463571615, 0.06733160800476529, 0.07573943399900715, 0.08337385420944596, 0.08992568421634073, 0.09511539839689936, 0.09871284801536351] + [0.10055417216116297] * 2 + [0.09871284801536351, 0.09511539839689936, 0.08992568421634073, 0.08337385420944596, 0.07573943399900715, 0.06733160800476529, 0.058468625463571615, 0.04945822260189534, 0.040580694059638336, 0.03207581995293284, 0.024134332214287853, 0.016894063294132074, 0.010440433647770957, 0.004810556420611938, 0.0],
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
            "samples": [0.0, -0.002405278210305969, -0.005220216823885479, -0.008447031647066037, -0.012067166107143926, -0.01603790997646642, -0.020290347029819168, -0.02472911130094767, -0.029234312731785807, -0.03366580400238264, -0.037869716999503575, -0.04168692710472298, -0.044962842108170364, -0.04755769919844968, -0.049356424007681754] + [-0.050277086080581485] * 2 + [-0.049356424007681754, -0.04755769919844968, -0.044962842108170364, -0.04168692710472298, -0.037869716999503575, -0.03366580400238264, -0.029234312731785807, -0.02472911130094767, -0.020290347029819168, -0.01603790997646642, -0.012067166107143926, -0.008447031647066037, -0.005220216823885479, -0.002405278210305969, 0.0],
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
            "samples": [0.0, 0.002405278210305969, 0.005220216823885479, 0.008447031647066037, 0.012067166107143926, 0.01603790997646642, 0.020290347029819168, 0.02472911130094767, 0.029234312731785807, 0.03366580400238264, 0.037869716999503575, 0.04168692710472298, 0.044962842108170364, 0.04755769919844968, 0.049356424007681754] + [0.050277086080581485] * 2 + [0.049356424007681754, 0.04755769919844968, 0.044962842108170364, 0.04168692710472298, 0.037869716999503575, 0.03366580400238264, 0.029234312731785807, 0.02472911130094767, 0.020290347029819168, 0.01603790997646642, 0.012067166107143926, 0.008447031647066037, 0.005220216823885479, 0.002405278210305969, 0.0],
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
            "samples": [0.0, 0.004810556420611938, 0.010440433647770957, 0.016894063294132074, 0.024134332214287853, 0.03207581995293284, 0.040580694059638336, 0.04945822260189534, 0.058468625463571615, 0.06733160800476529, 0.07573943399900715, 0.08337385420944596, 0.08992568421634073, 0.09511539839689936, 0.09871284801536351] + [0.10055417216116297] * 2 + [0.09871284801536351, 0.09511539839689936, 0.08992568421634073, 0.08337385420944596, 0.07573943399900715, 0.06733160800476529, 0.058468625463571615, 0.04945822260189534, 0.040580694059638336, 0.03207581995293284, 0.024134332214287853, 0.016894063294132074, 0.010440433647770957, 0.004810556420611938, 0.0],
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
            "samples": [0.0, -0.002405278210305969, -0.005220216823885479, -0.008447031647066037, -0.012067166107143926, -0.01603790997646642, -0.020290347029819168, -0.02472911130094767, -0.029234312731785807, -0.03366580400238264, -0.037869716999503575, -0.04168692710472298, -0.044962842108170364, -0.04755769919844968, -0.049356424007681754] + [-0.050277086080581485] * 2 + [-0.049356424007681754, -0.04755769919844968, -0.044962842108170364, -0.04168692710472298, -0.037869716999503575, -0.03366580400238264, -0.029234312731785807, -0.02472911130094767, -0.020290347029819168, -0.01603790997646642, -0.012067166107143926, -0.008447031647066037, -0.005220216823885479, -0.002405278210305969, 0.0],
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
            "cosine": [(0.971134279909636, 1800)],
            "sine": [(-0.23853345757858122, 1800)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(0.23853345757858122, 1800)],
            "sine": [(0.971134279909636, 1800)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(-0.23853345757858122, 1800)],
            "sine": [(-0.971134279909636, 1800)],
        },
        "rotated_cosine_weights_q2": {
            "cosine": [(-0.45243470931178276, 1800)],
            "sine": [(0.8917975296052141, 1800)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(-0.8917975296052141, 1800)],
            "sine": [(-0.45243470931178276, 1800)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(0.8917975296052141, 1800)],
            "sine": [(0.45243470931178276, 1800)],
        },
        "rotated_cosine_weights_q3": {
            "cosine": [(0.8754645270000179, 1800)],
            "sine": [(0.4832823832550023, 1800)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(-0.4832823832550023, 1800)],
            "sine": [(0.8754645270000179, 1800)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(0.4832823832550023, 1800)],
            "sine": [(-0.8754645270000179, 1800)],
        },
        "rotated_cosine_weights_q4": {
            "cosine": [(-0.981627183447664, 1800)],
            "sine": [(-0.19080899537654472, 1800)],
        },
        "rotated_sine_weights_q4": {
            "cosine": [(0.19080899537654472, 1800)],
            "sine": [(-0.981627183447664, 1800)],
        },
        "rotated_minus_sine_weights_q4": {
            "cosine": [(-0.19080899537654472, 1800)],
            "sine": [(0.981627183447664, 1800)],
        },
        "rotated_cosine_weights_q5": {
            "cosine": [(-0.9993908270190958, 1800)],
            "sine": [(0.03489949670250114, 1800)],
        },
        "rotated_sine_weights_q5": {
            "cosine": [(-0.03489949670250114, 1800)],
            "sine": [(-0.9993908270190958, 1800)],
        },
        "rotated_minus_sine_weights_q5": {
            "cosine": [(0.03489949670250114, 1800)],
            "sine": [(0.9993908270190958, 1800)],
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
        "octave_octave1_2": [{'intermediate_frequency': 130602000.0, 'lo_frequency': 3200000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]}],
        "octave_octave1_3": [{'intermediate_frequency': 261857000.0, 'lo_frequency': 3200000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]}],
        "octave_octave1_4": [{'intermediate_frequency': 106551000.0, 'lo_frequency': 3960000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]}],
        "octave_octave1_5": [{'intermediate_frequency': 368712000.0, 'lo_frequency': 3960000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]}],
        "octave_octave2_1": [{'intermediate_frequency': 122859000.0, 'lo_frequency': 4600000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]}],
        "octave_octave1_1": [
            {'intermediate_frequency': 163122000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
            {'intermediate_frequency': 126410000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
            {'intermediate_frequency': 49753000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
            {'intermediate_frequency': 218194000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
            {'intermediate_frequency': 28632000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
        ],
    },
}



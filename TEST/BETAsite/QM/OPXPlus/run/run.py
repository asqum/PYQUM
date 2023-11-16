
# Single QUA script generated at 2023-11-10 21:09:15.531837
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
                    "offset": 0.01837158203125,
                },
                "8": {
                    "offset": -0.002716064453125,
                },
                "9": {
                    "offset": 0.0087432861328125,
                },
                "10": {
                    "offset": -0.0157470703125,
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
            "intermediate_frequency": -130785000,
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
            "intermediate_frequency": -261760000,
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
            "intermediate_frequency": -408712000,
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
            "intermediate_frequency": -24179000,
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
            "length": 2000,
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
            "length": 2000,
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
            "length": 2000,
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
            "length": 2000,
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
            "length": 2000,
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
            "samples": [0.0, 0.00040061020275852354, 0.0008694512390706739, 0.0014068921617214193, 0.002009842287761282, 0.002671188031374492, 0.0033794510767312267, 0.00411874778138473, 0.004869109902050376, 0.005607195254850623, 0.006307376394371098, 0.006943150379963105, 0.007488769164570896, 0.00792095460599389, 0.008220540536405484] + [0.008373881059807773] * 2 + [0.008220540536405484, 0.00792095460599389, 0.007488769164570896, 0.006943150379963105, 0.006307376394371098, 0.005607195254850623, 0.004869109902050376, 0.00411874778138473, 0.0033794510767312267, 0.002671188031374492, 0.002009842287761282, 0.0014068921617214193, 0.0008694512390706739, 0.00040061020275852354, 0.0],
        },
        "x90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "x180_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0008012204055170471, 0.0017389024781413478, 0.0028137843234428386, 0.004019684575522564, 0.005342376062748984, 0.0067589021534624535, 0.00823749556276946, 0.009738219804100752, 0.011214390509701246, 0.012614752788742196, 0.01388630075992621, 0.014977538329141792, 0.01584190921198778, 0.01644108107281097] + [0.016747762119615546] * 2 + [0.01644108107281097, 0.01584190921198778, 0.014977538329141792, 0.01388630075992621, 0.012614752788742196, 0.011214390509701246, 0.009738219804100752, 0.00823749556276946, 0.0067589021534624535, 0.005342376062748984, 0.004019684575522564, 0.0028137843234428386, 0.0017389024781413478, 0.0008012204055170471, 0.0],
        },
        "x180_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "minus_x90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, -0.00040061020275852354, -0.0008694512390706739, -0.0014068921617214193, -0.002009842287761282, -0.002671188031374492, -0.0033794510767312267, -0.00411874778138473, -0.004869109902050376, -0.005607195254850623, -0.006307376394371098, -0.006943150379963105, -0.007488769164570896, -0.00792095460599389, -0.008220540536405484] + [-0.008373881059807773] * 2 + [-0.008220540536405484, -0.00792095460599389, -0.007488769164570896, -0.006943150379963105, -0.006307376394371098, -0.005607195254850623, -0.004869109902050376, -0.00411874778138473, -0.0033794510767312267, -0.002671188031374492, -0.002009842287761282, -0.0014068921617214193, -0.0008694512390706739, -0.00040061020275852354, 0.0],
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
            "samples": [0.0, 0.00040061020275852354, 0.0008694512390706739, 0.0014068921617214193, 0.002009842287761282, 0.002671188031374492, 0.0033794510767312267, 0.00411874778138473, 0.004869109902050376, 0.005607195254850623, 0.006307376394371098, 0.006943150379963105, 0.007488769164570896, 0.00792095460599389, 0.008220540536405484] + [0.008373881059807773] * 2 + [0.008220540536405484, 0.00792095460599389, 0.007488769164570896, 0.006943150379963105, 0.006307376394371098, 0.005607195254850623, 0.004869109902050376, 0.00411874778138473, 0.0033794510767312267, 0.002671188031374492, 0.002009842287761282, 0.0014068921617214193, 0.0008694512390706739, 0.00040061020275852354, 0.0],
        },
        "y180_I_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "y180_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, 0.0008012204055170471, 0.0017389024781413478, 0.0028137843234428386, 0.004019684575522564, 0.005342376062748984, 0.0067589021534624535, 0.00823749556276946, 0.009738219804100752, 0.011214390509701246, 0.012614752788742196, 0.01388630075992621, 0.014977538329141792, 0.01584190921198778, 0.01644108107281097] + [0.016747762119615546] * 2 + [0.01644108107281097, 0.01584190921198778, 0.014977538329141792, 0.01388630075992621, 0.012614752788742196, 0.011214390509701246, 0.009738219804100752, 0.00823749556276946, 0.0067589021534624535, 0.005342376062748984, 0.004019684575522564, 0.0028137843234428386, 0.0017389024781413478, 0.0008012204055170471, 0.0],
        },
        "minus_y90_I_wf_q1": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "minus_y90_Q_wf_q1": {
            "type": "arbitrary",
            "samples": [0.0, -0.00040061020275852354, -0.0008694512390706739, -0.0014068921617214193, -0.002009842287761282, -0.002671188031374492, -0.0033794510767312267, -0.00411874778138473, -0.004869109902050376, -0.005607195254850623, -0.006307376394371098, -0.006943150379963105, -0.007488769164570896, -0.00792095460599389, -0.008220540536405484] + [-0.008373881059807773] * 2 + [-0.008220540536405484, -0.00792095460599389, -0.007488769164570896, -0.006943150379963105, -0.006307376394371098, -0.005607195254850623, -0.004869109902050376, -0.00411874778138473, -0.0033794510767312267, -0.002671188031374492, -0.002009842287761282, -0.0014068921617214193, -0.0008694512390706739, -0.00040061020275852354, 0.0],
        },
        "readout_wf_q1": {
            "type": "constant",
            "sample": 0.05273154,
        },
        "x90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.00155635648902151, 0.0033777873566317807, 0.00546572635986626, 0.00780816630462254, 0.01037747116124298, 0.013129048078118287, 0.01600118966531908, 0.018916320002920227, 0.021783755530953477, 0.024503934529090544, 0.026973894008938397, 0.029093603717051407, 0.030772628893114502, 0.03193650965202938] + [0.03253223216978802] * 2 + [0.03193650965202938, 0.030772628893114502, 0.029093603717051407, 0.026973894008938397, 0.024503934529090544, 0.021783755530953477, 0.018916320002920227, 0.01600118966531908, 0.013129048078118287, 0.01037747116124298, 0.00780816630462254, 0.00546572635986626, 0.0033777873566317807, 0.00155635648902151, 0.0],
        },
        "x90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "x180_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.00311271297804302, 0.006755574713263561, 0.01093145271973252, 0.01561633260924508, 0.02075494232248596, 0.026258096156236574, 0.03200237933063816, 0.037832640005840454, 0.043567511061906955, 0.04900786905818109, 0.053947788017876794, 0.058187207434102814, 0.061545257786229005, 0.06387301930405875] + [0.06506446433957604] * 2 + [0.06387301930405875, 0.061545257786229005, 0.058187207434102814, 0.053947788017876794, 0.04900786905818109, 0.043567511061906955, 0.037832640005840454, 0.03200237933063816, 0.026258096156236574, 0.02075494232248596, 0.01561633260924508, 0.01093145271973252, 0.006755574713263561, 0.00311271297804302, 0.0],
        },
        "x180_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "minus_x90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, -0.00155635648902151, -0.0033777873566317807, -0.00546572635986626, -0.00780816630462254, -0.01037747116124298, -0.013129048078118287, -0.01600118966531908, -0.018916320002920227, -0.021783755530953477, -0.024503934529090544, -0.026973894008938397, -0.029093603717051407, -0.030772628893114502, -0.03193650965202938] + [-0.03253223216978802] * 2 + [-0.03193650965202938, -0.030772628893114502, -0.029093603717051407, -0.026973894008938397, -0.024503934529090544, -0.021783755530953477, -0.018916320002920227, -0.01600118966531908, -0.013129048078118287, -0.01037747116124298, -0.00780816630462254, -0.00546572635986626, -0.0033777873566317807, -0.00155635648902151, 0.0],
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
            "samples": [0.0, 0.00155635648902151, 0.0033777873566317807, 0.00546572635986626, 0.00780816630462254, 0.01037747116124298, 0.013129048078118287, 0.01600118966531908, 0.018916320002920227, 0.021783755530953477, 0.024503934529090544, 0.026973894008938397, 0.029093603717051407, 0.030772628893114502, 0.03193650965202938] + [0.03253223216978802] * 2 + [0.03193650965202938, 0.030772628893114502, 0.029093603717051407, 0.026973894008938397, 0.024503934529090544, 0.021783755530953477, 0.018916320002920227, 0.01600118966531908, 0.013129048078118287, 0.01037747116124298, 0.00780816630462254, 0.00546572635986626, 0.0033777873566317807, 0.00155635648902151, 0.0],
        },
        "y180_I_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "y180_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, 0.00311271297804302, 0.006755574713263561, 0.01093145271973252, 0.01561633260924508, 0.02075494232248596, 0.026258096156236574, 0.03200237933063816, 0.037832640005840454, 0.043567511061906955, 0.04900786905818109, 0.053947788017876794, 0.058187207434102814, 0.061545257786229005, 0.06387301930405875] + [0.06506446433957604] * 2 + [0.06387301930405875, 0.061545257786229005, 0.058187207434102814, 0.053947788017876794, 0.04900786905818109, 0.043567511061906955, 0.037832640005840454, 0.03200237933063816, 0.026258096156236574, 0.02075494232248596, 0.01561633260924508, 0.01093145271973252, 0.006755574713263561, 0.00311271297804302, 0.0],
        },
        "minus_y90_I_wf_q2": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "minus_y90_Q_wf_q2": {
            "type": "arbitrary",
            "samples": [0.0, -0.00155635648902151, -0.0033777873566317807, -0.00546572635986626, -0.00780816630462254, -0.01037747116124298, -0.013129048078118287, -0.01600118966531908, -0.018916320002920227, -0.021783755530953477, -0.024503934529090544, -0.026973894008938397, -0.029093603717051407, -0.030772628893114502, -0.03193650965202938] + [-0.03253223216978802] * 2 + [-0.03193650965202938, -0.030772628893114502, -0.029093603717051407, -0.026973894008938397, -0.024503934529090544, -0.021783755530953477, -0.018916320002920227, -0.01600118966531908, -0.013129048078118287, -0.01037747116124298, -0.00780816630462254, -0.00546572635986626, -0.0033777873566317807, -0.00155635648902151, 0.0],
        },
        "readout_wf_q2": {
            "type": "constant",
            "sample": 0.06399,
        },
        "x90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.00044143929506791895, 0.000958063322971923, 0.0015502787493438847, 0.0022146798973111206, 0.00294342818391619, 0.003723875454884459, 0.004538519250526867, 0.005365356219010101, 0.006178665205143168, 0.0069502068846147725, 0.007650777209807981, 0.008252003963381854, 0.008728236558774295, 0.00905835546493924] + [0.0092273240336126] * 2 + [0.00905835546493924, 0.008728236558774295, 0.008252003963381854, 0.007650777209807981, 0.0069502068846147725, 0.006178665205143168, 0.005365356219010101, 0.004538519250526867, 0.003723875454884459, 0.00294342818391619, 0.0022146798973111206, 0.0015502787493438847, 0.000958063322971923, 0.00044143929506791895, 0.0],
        },
        "x90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "x180_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0008828785901358379, 0.001916126645943846, 0.0031005574986877693, 0.004429359794622241, 0.00588685636783238, 0.007447750909768918, 0.009077038501053734, 0.010730712438020202, 0.012357330410286336, 0.013900413769229545, 0.015301554419615962, 0.01650400792676371, 0.01745647311754859, 0.01811671092987848] + [0.0184546480672252] * 2 + [0.01811671092987848, 0.01745647311754859, 0.01650400792676371, 0.015301554419615962, 0.013900413769229545, 0.012357330410286336, 0.010730712438020202, 0.009077038501053734, 0.007447750909768918, 0.00588685636783238, 0.004429359794622241, 0.0031005574986877693, 0.001916126645943846, 0.0008828785901358379, 0.0],
        },
        "x180_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "minus_x90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, -0.00044143929506791895, -0.000958063322971923, -0.0015502787493438847, -0.0022146798973111206, -0.00294342818391619, -0.003723875454884459, -0.004538519250526867, -0.005365356219010101, -0.006178665205143168, -0.0069502068846147725, -0.007650777209807981, -0.008252003963381854, -0.008728236558774295, -0.00905835546493924] + [-0.0092273240336126] * 2 + [-0.00905835546493924, -0.008728236558774295, -0.008252003963381854, -0.007650777209807981, -0.0069502068846147725, -0.006178665205143168, -0.005365356219010101, -0.004538519250526867, -0.003723875454884459, -0.00294342818391619, -0.0022146798973111206, -0.0015502787493438847, -0.000958063322971923, -0.00044143929506791895, 0.0],
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
            "samples": [0.0, 0.00044143929506791895, 0.000958063322971923, 0.0015502787493438847, 0.0022146798973111206, 0.00294342818391619, 0.003723875454884459, 0.004538519250526867, 0.005365356219010101, 0.006178665205143168, 0.0069502068846147725, 0.007650777209807981, 0.008252003963381854, 0.008728236558774295, 0.00905835546493924] + [0.0092273240336126] * 2 + [0.00905835546493924, 0.008728236558774295, 0.008252003963381854, 0.007650777209807981, 0.0069502068846147725, 0.006178665205143168, 0.005365356219010101, 0.004538519250526867, 0.003723875454884459, 0.00294342818391619, 0.0022146798973111206, 0.0015502787493438847, 0.000958063322971923, 0.00044143929506791895, 0.0],
        },
        "y180_I_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "y180_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, 0.0008828785901358379, 0.001916126645943846, 0.0031005574986877693, 0.004429359794622241, 0.00588685636783238, 0.007447750909768918, 0.009077038501053734, 0.010730712438020202, 0.012357330410286336, 0.013900413769229545, 0.015301554419615962, 0.01650400792676371, 0.01745647311754859, 0.01811671092987848] + [0.0184546480672252] * 2 + [0.01811671092987848, 0.01745647311754859, 0.01650400792676371, 0.015301554419615962, 0.013900413769229545, 0.012357330410286336, 0.010730712438020202, 0.009077038501053734, 0.007447750909768918, 0.00588685636783238, 0.004429359794622241, 0.0031005574986877693, 0.001916126645943846, 0.0008828785901358379, 0.0],
        },
        "minus_y90_I_wf_q3": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "minus_y90_Q_wf_q3": {
            "type": "arbitrary",
            "samples": [0.0, -0.00044143929506791895, -0.000958063322971923, -0.0015502787493438847, -0.0022146798973111206, -0.00294342818391619, -0.003723875454884459, -0.004538519250526867, -0.005365356219010101, -0.006178665205143168, -0.0069502068846147725, -0.007650777209807981, -0.008252003963381854, -0.008728236558774295, -0.00905835546493924] + [-0.0092273240336126] * 2 + [-0.00905835546493924, -0.008728236558774295, -0.008252003963381854, -0.007650777209807981, -0.0069502068846147725, -0.006178665205143168, -0.005365356219010101, -0.004538519250526867, -0.003723875454884459, -0.00294342818391619, -0.0022146798973111206, -0.0015502787493438847, -0.000958063322971923, -0.00044143929506791895, 0.0],
        },
        "readout_wf_q3": {
            "type": "constant",
            "sample": 0.0579743325,
        },
        "x90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0023042161006292493, 0.005000879982545753, 0.008092114350970828, 0.011560142321129478, 0.015364048212749346, 0.019437811440330972, 0.023690073010991894, 0.028005980264063715, 0.032251274422450606, 0.0362785524196925, 0.03993537554570101, 0.043073647061608586, 0.045559476543052646, 0.04728262467962791] + [0.04816460347215369] * 2 + [0.04728262467962791, 0.045559476543052646, 0.043073647061608586, 0.03993537554570101, 0.0362785524196925, 0.032251274422450606, 0.028005980264063715, 0.023690073010991894, 0.019437811440330972, 0.015364048212749346, 0.011560142321129478, 0.008092114350970828, 0.005000879982545753, 0.0023042161006292493, 0.0],
        },
        "x90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "x180_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0046084322012584986, 0.010001759965091506, 0.016184228701941656, 0.023120284642258956, 0.03072809642549869, 0.038875622880661945, 0.04738014602198379, 0.05601196052812743, 0.06450254884490121, 0.072557104839385, 0.07987075109140201, 0.08614729412321717, 0.09111895308610529, 0.09456524935925582] + [0.09632920694430738] * 2 + [0.09456524935925582, 0.09111895308610529, 0.08614729412321717, 0.07987075109140201, 0.072557104839385, 0.06450254884490121, 0.05601196052812743, 0.04738014602198379, 0.038875622880661945, 0.03072809642549869, 0.023120284642258956, 0.016184228701941656, 0.010001759965091506, 0.0046084322012584986, 0.0],
        },
        "x180_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "minus_x90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, -0.0023042161006292493, -0.005000879982545753, -0.008092114350970828, -0.011560142321129478, -0.015364048212749346, -0.019437811440330972, -0.023690073010991894, -0.028005980264063715, -0.032251274422450606, -0.0362785524196925, -0.03993537554570101, -0.043073647061608586, -0.045559476543052646, -0.04728262467962791] + [-0.04816460347215369] * 2 + [-0.04728262467962791, -0.045559476543052646, -0.043073647061608586, -0.03993537554570101, -0.0362785524196925, -0.032251274422450606, -0.028005980264063715, -0.023690073010991894, -0.019437811440330972, -0.015364048212749346, -0.011560142321129478, -0.008092114350970828, -0.005000879982545753, -0.0023042161006292493, 0.0],
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
            "samples": [0.0, 0.0023042161006292493, 0.005000879982545753, 0.008092114350970828, 0.011560142321129478, 0.015364048212749346, 0.019437811440330972, 0.023690073010991894, 0.028005980264063715, 0.032251274422450606, 0.0362785524196925, 0.03993537554570101, 0.043073647061608586, 0.045559476543052646, 0.04728262467962791] + [0.04816460347215369] * 2 + [0.04728262467962791, 0.045559476543052646, 0.043073647061608586, 0.03993537554570101, 0.0362785524196925, 0.032251274422450606, 0.028005980264063715, 0.023690073010991894, 0.019437811440330972, 0.015364048212749346, 0.011560142321129478, 0.008092114350970828, 0.005000879982545753, 0.0023042161006292493, 0.0],
        },
        "y180_I_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "y180_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, 0.0046084322012584986, 0.010001759965091506, 0.016184228701941656, 0.023120284642258956, 0.03072809642549869, 0.038875622880661945, 0.04738014602198379, 0.05601196052812743, 0.06450254884490121, 0.072557104839385, 0.07987075109140201, 0.08614729412321717, 0.09111895308610529, 0.09456524935925582] + [0.09632920694430738] * 2 + [0.09456524935925582, 0.09111895308610529, 0.08614729412321717, 0.07987075109140201, 0.072557104839385, 0.06450254884490121, 0.05601196052812743, 0.04738014602198379, 0.038875622880661945, 0.03072809642549869, 0.023120284642258956, 0.016184228701941656, 0.010001759965091506, 0.0046084322012584986, 0.0],
        },
        "minus_y90_I_wf_q4": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "minus_y90_Q_wf_q4": {
            "type": "arbitrary",
            "samples": [0.0, -0.0023042161006292493, -0.005000879982545753, -0.008092114350970828, -0.011560142321129478, -0.015364048212749346, -0.019437811440330972, -0.023690073010991894, -0.028005980264063715, -0.032251274422450606, -0.0362785524196925, -0.03993537554570101, -0.043073647061608586, -0.045559476543052646, -0.04728262467962791] + [-0.04816460347215369] * 2 + [-0.04728262467962791, -0.045559476543052646, -0.043073647061608586, -0.03993537554570101, -0.0362785524196925, -0.032251274422450606, -0.028005980264063715, -0.023690073010991894, -0.019437811440330972, -0.015364048212749346, -0.011560142321129478, -0.008092114350970828, -0.005000879982545753, -0.0023042161006292493, 0.0],
        },
        "readout_wf_q4": {
            "type": "constant",
            "sample": 0.291757965,
        },
        "x90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.0032259025408809486, 0.007001231975564055, 0.011328960091359157, 0.01618419924958126, 0.021509667497849085, 0.02721293601646336, 0.03316610221538865, 0.0392083723696892, 0.045151784191430844, 0.0507899733875695, 0.0559095257639814, 0.06030310588625202, 0.06378326716027369, 0.06619567455147907] + [0.06743044486101515] * 2 + [0.06619567455147907, 0.06378326716027369, 0.06030310588625202, 0.0559095257639814, 0.0507899733875695, 0.045151784191430844, 0.0392083723696892, 0.03316610221538865, 0.02721293601646336, 0.021509667497849085, 0.01618419924958126, 0.011328960091359157, 0.007001231975564055, 0.0032259025408809486, 0.0],
        },
        "x90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "x180_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.006451805081761897, 0.01400246395112811, 0.022657920182718314, 0.03236839849916252, 0.04301933499569817, 0.05442587203292672, 0.0663322044307773, 0.0784167447393784, 0.09030356838286169, 0.101579946775139, 0.1118190515279628, 0.12060621177250404, 0.12756653432054738, 0.13239134910295813] + [0.1348608897220303] * 2 + [0.13239134910295813, 0.12756653432054738, 0.12060621177250404, 0.1118190515279628, 0.101579946775139, 0.09030356838286169, 0.0784167447393784, 0.0663322044307773, 0.05442587203292672, 0.04301933499569817, 0.03236839849916252, 0.022657920182718314, 0.01400246395112811, 0.006451805081761897, 0.0],
        },
        "x180_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0] * 32,
        },
        "minus_x90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, -0.0032259025408809486, -0.007001231975564055, -0.011328960091359157, -0.01618419924958126, -0.021509667497849085, -0.02721293601646336, -0.03316610221538865, -0.0392083723696892, -0.045151784191430844, -0.0507899733875695, -0.0559095257639814, -0.06030310588625202, -0.06378326716027369, -0.06619567455147907] + [-0.06743044486101515] * 2 + [-0.06619567455147907, -0.06378326716027369, -0.06030310588625202, -0.0559095257639814, -0.0507899733875695, -0.045151784191430844, -0.0392083723696892, -0.03316610221538865, -0.02721293601646336, -0.021509667497849085, -0.01618419924958126, -0.011328960091359157, -0.007001231975564055, -0.0032259025408809486, 0.0],
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
            "samples": [0.0, 0.0032259025408809486, 0.007001231975564055, 0.011328960091359157, 0.01618419924958126, 0.021509667497849085, 0.02721293601646336, 0.03316610221538865, 0.0392083723696892, 0.045151784191430844, 0.0507899733875695, 0.0559095257639814, 0.06030310588625202, 0.06378326716027369, 0.06619567455147907] + [0.06743044486101515] * 2 + [0.06619567455147907, 0.06378326716027369, 0.06030310588625202, 0.0559095257639814, 0.0507899733875695, 0.045151784191430844, 0.0392083723696892, 0.03316610221538865, 0.02721293601646336, 0.021509667497849085, 0.01618419924958126, 0.011328960091359157, 0.007001231975564055, 0.0032259025408809486, 0.0],
        },
        "y180_I_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "y180_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, 0.006451805081761897, 0.01400246395112811, 0.022657920182718314, 0.03236839849916252, 0.04301933499569817, 0.05442587203292672, 0.0663322044307773, 0.0784167447393784, 0.09030356838286169, 0.101579946775139, 0.1118190515279628, 0.12060621177250404, 0.12756653432054738, 0.13239134910295813] + [0.1348608897220303] * 2 + [0.13239134910295813, 0.12756653432054738, 0.12060621177250404, 0.1118190515279628, 0.101579946775139, 0.09030356838286169, 0.0784167447393784, 0.0663322044307773, 0.05442587203292672, 0.04301933499569817, 0.03236839849916252, 0.022657920182718314, 0.01400246395112811, 0.006451805081761897, 0.0],
        },
        "minus_y90_I_wf_q5": {
            "type": "arbitrary",
            "samples": [-0.0] * 32,
        },
        "minus_y90_Q_wf_q5": {
            "type": "arbitrary",
            "samples": [0.0, -0.0032259025408809486, -0.007001231975564055, -0.011328960091359157, -0.01618419924958126, -0.021509667497849085, -0.02721293601646336, -0.03316610221538865, -0.0392083723696892, -0.045151784191430844, -0.0507899733875695, -0.0559095257639814, -0.06030310588625202, -0.06378326716027369, -0.06619567455147907] + [-0.06743044486101515] * 2 + [-0.06619567455147907, -0.06378326716027369, -0.06030310588625202, -0.0559095257639814, -0.0507899733875695, -0.045151784191430844, -0.0392083723696892, -0.03316610221538865, -0.02721293601646336, -0.021509667497849085, -0.01618419924958126, -0.011328960091359157, -0.007001231975564055, -0.0032259025408809486, 0.0],
        },
        "readout_wf_q5": {
            "type": "constant",
            "sample": 0.0397908618,
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
            "cosine": [(1.0, 2000)],
            "sine": [(0.0, 2000)],
        },
        "sine_weights": {
            "cosine": [(0.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "minus_sine_weights": {
            "cosine": [(0.0, 2000)],
            "sine": [(-1.0, 2000)],
        },
        "rotated_cosine_weights_q1": {
            "cosine": [(0.14953534344370958, 2000)],
            "sine": [(0.9887563810470058, 2000)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(-0.9887563810470058, 2000)],
            "sine": [(0.14953534344370958, 2000)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(0.9887563810470058, 2000)],
            "sine": [(-0.14953534344370958, 2000)],
        },
        "rotated_cosine_weights_q2": {
            "cosine": [(-0.9291325715340562, 2000)],
            "sine": [(-0.36974675727382916, 2000)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(0.36974675727382916, 2000)],
            "sine": [(-0.9291325715340562, 2000)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(-0.36974675727382916, 2000)],
            "sine": [(0.9291325715340562, 2000)],
        },
        "rotated_cosine_weights_q3": {
            "cosine": [(-0.6279630576493378, 2000)],
            "sine": [(0.7782431485260211, 2000)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(-0.7782431485260211, 2000)],
            "sine": [(-0.6279630576493378, 2000)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(0.7782431485260211, 2000)],
            "sine": [(0.6279630576493378, 2000)],
        },
        "rotated_cosine_weights_q4": {
            "cosine": [(0.656059028990507, 2000)],
            "sine": [(-0.7547095802227722, 2000)],
        },
        "rotated_sine_weights_q4": {
            "cosine": [(0.7547095802227722, 2000)],
            "sine": [(0.656059028990507, 2000)],
        },
        "rotated_minus_sine_weights_q4": {
            "cosine": [(-0.7547095802227722, 2000)],
            "sine": [(-0.656059028990507, 2000)],
        },
        "rotated_cosine_weights_q5": {
            "cosine": [(-0.16504760586067815, 2000)],
            "sine": [(-0.9862856015372313, 2000)],
        },
        "rotated_sine_weights_q5": {
            "cosine": [(0.9862856015372313, 2000)],
            "sine": [(-0.16504760586067815, 2000)],
        },
        "rotated_minus_sine_weights_q5": {
            "cosine": [(-0.9862856015372313, 2000)],
            "sine": [(0.16504760586067815, 2000)],
        },
        "opt_cosine_weights_q1": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_sine_weights_q1": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_minus_sine_weights_q1": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_cosine_weights_q2": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_sine_weights_q2": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_minus_sine_weights_q2": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_cosine_weights_q3": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_sine_weights_q3": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_minus_sine_weights_q3": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_cosine_weights_q4": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_sine_weights_q4": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_minus_sine_weights_q4": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_cosine_weights_q5": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_sine_weights_q5": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_minus_sine_weights_q5": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
    },
    "mixers": {
        "octave_octave1_2": [
            {'intermediate_frequency': -346063000, 'lo_frequency': 3670000000, 'correction': [1.139035176485777, 0.16698597371578217, 0.19680260121822357, 0.9664653651416302]},
            {'intermediate_frequency': -135471000, 'lo_frequency': 3200000000, 'correction': [0.9071802385151386, 0.06404274702072144, 0.0515754371881485, 1.1264725401997566]},
            {'intermediate_frequency': -135196000, 'lo_frequency': 3200000000, 'correction': [0.9105054624378681, 0.06347507238388062, 0.05154538154602051, 1.1212333254516125]},
            {'intermediate_frequency': -130808000, 'lo_frequency': 3200000000, 'correction': [0.9090330041944981, 0.0641556978225708, 0.051899492740631104, 1.1237035803496838]},
            {'intermediate_frequency': -130785000, 'lo_frequency': 3200000000, 'correction': (1, 0, 0, 1)},
        ],
        "octave_octave1_3": [
            {'intermediate_frequency': 471832000, 'lo_frequency': 3670000000, 'correction': [1.0509245730936527, 0.1871345043182373, 0.1878669261932373, 1.0468274168670177]},
            {'intermediate_frequency': -262537000, 'lo_frequency': 3200000000, 'correction': [0.8680114857852459, -0.004036571830511093, -0.002966787666082382, 1.1810052506625652]},
            {'intermediate_frequency': -261338000, 'lo_frequency': 3200000000, 'correction': [0.8681640625, 0.0, 0.0, 1.1806640625]},
            {'intermediate_frequency': -262288000, 'lo_frequency': 3200000000, 'correction': [0.8680580779910088, -0.004612911492586136, -0.0033907778561115265, 1.1809314489364624]},
            {'intermediate_frequency': -261760000, 'lo_frequency': 3200000000, 'correction': (1, 0, 0, 1)},
        ],
        "octave_octave1_4": [{'intermediate_frequency': -146495000, 'lo_frequency': 4000000000, 'correction': [1.39941843226552, -0.06450551748275757, -0.11300128698348999, 0.798842303454876]}],
        "octave_octave1_5": [
            {'intermediate_frequency': -408869000, 'lo_frequency': 4000000000, 'correction': [1.4782978221774101, -0.05286115035414696, -0.10035889968276024, 0.7786506339907646]},
            {'intermediate_frequency': -408712000, 'lo_frequency': 4000000000, 'correction': [1.472061611711979, -0.05293846130371094, -0.09993553161621094, 0.7797894850373268]},
        ],
        "octave_octave2_1": [
            {'intermediate_frequency': -24209000, 'lo_frequency': 4500000000, 'correction': [1.2739626578986645, -0.05181884765625, -0.07916259765625, 0.8339200429618359]},
            {'intermediate_frequency': -24184000, 'lo_frequency': 4500000000, 'correction': [1.2739626578986645, -0.05181884765625, -0.07916259765625, 0.8339200429618359]},
            {'intermediate_frequency': -24196000, 'lo_frequency': 4500000000, 'correction': [1.2739626578986645, -0.05181884765625, -0.07916259765625, 0.8339200429618359]},
            {'intermediate_frequency': -24179000, 'lo_frequency': 4500000000, 'correction': (1, 0, 0, 1)},
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
            {'intermediate_frequency': -163122000, 'lo_frequency': 5900000000, 'correction': [1.0789089314639568, -0.13434219360351562, -0.14752578735351562, 0.9824925884604454]},
            {'intermediate_frequency': -49753000, 'lo_frequency': 5900000000, 'correction': [1.087750818580389, -0.1489931344985962, -0.1642519235610962, 0.9867001883685589]},
            {'intermediate_frequency': 218194000, 'lo_frequency': 5900000000, 'correction': [1.1093690656125546, -0.17780685424804688, -0.19831466674804688, 0.9946486912667751]},
            {'intermediate_frequency': 28632000, 'lo_frequency': 5900000000, 'correction': [1.0886423401534557, -0.1607622355222702, -0.1758531779050827, 0.9952198676764965]},
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
                    "offset": 0.01837158203125,
                    "delay": 0,
                    "shareable": False,
                },
                "8": {
                    "offset": -0.002716064453125,
                    "delay": 0,
                    "shareable": False,
                },
                "9": {
                    "offset": 0.0087432861328125,
                    "delay": 0,
                    "shareable": False,
                },
                "10": {
                    "offset": -0.0157470703125,
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
            "intermediate_frequency": 130785000.0,
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
            "intermediate_frequency": 261760000.0,
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
            "intermediate_frequency": 408712000.0,
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
            "intermediate_frequency": 24179000.0,
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
            "length": 2000,
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
            "length": 2000,
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
            "length": 2000,
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
            "length": 2000,
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
            "length": 2000,
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
            "samples": [0.0, 0.00040061020275852354, 0.0008694512390706739, 0.0014068921617214193, 0.002009842287761282, 0.002671188031374492, 0.0033794510767312267, 0.00411874778138473, 0.004869109902050376, 0.005607195254850623, 0.006307376394371098, 0.006943150379963105, 0.007488769164570896, 0.00792095460599389, 0.008220540536405484] + [0.008373881059807773] * 2 + [0.008220540536405484, 0.00792095460599389, 0.007488769164570896, 0.006943150379963105, 0.006307376394371098, 0.005607195254850623, 0.004869109902050376, 0.00411874778138473, 0.0033794510767312267, 0.002671188031374492, 0.002009842287761282, 0.0014068921617214193, 0.0008694512390706739, 0.00040061020275852354, 0.0],
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
            "samples": [0.0, 0.0008012204055170471, 0.0017389024781413478, 0.0028137843234428386, 0.004019684575522564, 0.005342376062748984, 0.0067589021534624535, 0.00823749556276946, 0.009738219804100752, 0.011214390509701246, 0.012614752788742196, 0.01388630075992621, 0.014977538329141792, 0.01584190921198778, 0.01644108107281097] + [0.016747762119615546] * 2 + [0.01644108107281097, 0.01584190921198778, 0.014977538329141792, 0.01388630075992621, 0.012614752788742196, 0.011214390509701246, 0.009738219804100752, 0.00823749556276946, 0.0067589021534624535, 0.005342376062748984, 0.004019684575522564, 0.0028137843234428386, 0.0017389024781413478, 0.0008012204055170471, 0.0],
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
            "samples": [0.0, -0.00040061020275852354, -0.0008694512390706739, -0.0014068921617214193, -0.002009842287761282, -0.002671188031374492, -0.0033794510767312267, -0.00411874778138473, -0.004869109902050376, -0.005607195254850623, -0.006307376394371098, -0.006943150379963105, -0.007488769164570896, -0.00792095460599389, -0.008220540536405484] + [-0.008373881059807773] * 2 + [-0.008220540536405484, -0.00792095460599389, -0.007488769164570896, -0.006943150379963105, -0.006307376394371098, -0.005607195254850623, -0.004869109902050376, -0.00411874778138473, -0.0033794510767312267, -0.002671188031374492, -0.002009842287761282, -0.0014068921617214193, -0.0008694512390706739, -0.00040061020275852354, 0.0],
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
            "samples": [0.0, 0.00040061020275852354, 0.0008694512390706739, 0.0014068921617214193, 0.002009842287761282, 0.002671188031374492, 0.0033794510767312267, 0.00411874778138473, 0.004869109902050376, 0.005607195254850623, 0.006307376394371098, 0.006943150379963105, 0.007488769164570896, 0.00792095460599389, 0.008220540536405484] + [0.008373881059807773] * 2 + [0.008220540536405484, 0.00792095460599389, 0.007488769164570896, 0.006943150379963105, 0.006307376394371098, 0.005607195254850623, 0.004869109902050376, 0.00411874778138473, 0.0033794510767312267, 0.002671188031374492, 0.002009842287761282, 0.0014068921617214193, 0.0008694512390706739, 0.00040061020275852354, 0.0],
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
            "samples": [0.0, 0.0008012204055170471, 0.0017389024781413478, 0.0028137843234428386, 0.004019684575522564, 0.005342376062748984, 0.0067589021534624535, 0.00823749556276946, 0.009738219804100752, 0.011214390509701246, 0.012614752788742196, 0.01388630075992621, 0.014977538329141792, 0.01584190921198778, 0.01644108107281097] + [0.016747762119615546] * 2 + [0.01644108107281097, 0.01584190921198778, 0.014977538329141792, 0.01388630075992621, 0.012614752788742196, 0.011214390509701246, 0.009738219804100752, 0.00823749556276946, 0.0067589021534624535, 0.005342376062748984, 0.004019684575522564, 0.0028137843234428386, 0.0017389024781413478, 0.0008012204055170471, 0.0],
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
            "samples": [0.0, -0.00040061020275852354, -0.0008694512390706739, -0.0014068921617214193, -0.002009842287761282, -0.002671188031374492, -0.0033794510767312267, -0.00411874778138473, -0.004869109902050376, -0.005607195254850623, -0.006307376394371098, -0.006943150379963105, -0.007488769164570896, -0.00792095460599389, -0.008220540536405484] + [-0.008373881059807773] * 2 + [-0.008220540536405484, -0.00792095460599389, -0.007488769164570896, -0.006943150379963105, -0.006307376394371098, -0.005607195254850623, -0.004869109902050376, -0.00411874778138473, -0.0033794510767312267, -0.002671188031374492, -0.002009842287761282, -0.0014068921617214193, -0.0008694512390706739, -0.00040061020275852354, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q1": {
            "sample": 0.05273154,
            "type": "constant",
        },
        "x90_I_wf_q2": {
            "samples": [0.0, 0.00155635648902151, 0.0033777873566317807, 0.00546572635986626, 0.00780816630462254, 0.01037747116124298, 0.013129048078118287, 0.01600118966531908, 0.018916320002920227, 0.021783755530953477, 0.024503934529090544, 0.026973894008938397, 0.029093603717051407, 0.030772628893114502, 0.03193650965202938] + [0.03253223216978802] * 2 + [0.03193650965202938, 0.030772628893114502, 0.029093603717051407, 0.026973894008938397, 0.024503934529090544, 0.021783755530953477, 0.018916320002920227, 0.01600118966531908, 0.013129048078118287, 0.01037747116124298, 0.00780816630462254, 0.00546572635986626, 0.0033777873566317807, 0.00155635648902151, 0.0],
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
            "samples": [0.0, 0.00311271297804302, 0.006755574713263561, 0.01093145271973252, 0.01561633260924508, 0.02075494232248596, 0.026258096156236574, 0.03200237933063816, 0.037832640005840454, 0.043567511061906955, 0.04900786905818109, 0.053947788017876794, 0.058187207434102814, 0.061545257786229005, 0.06387301930405875] + [0.06506446433957604] * 2 + [0.06387301930405875, 0.061545257786229005, 0.058187207434102814, 0.053947788017876794, 0.04900786905818109, 0.043567511061906955, 0.037832640005840454, 0.03200237933063816, 0.026258096156236574, 0.02075494232248596, 0.01561633260924508, 0.01093145271973252, 0.006755574713263561, 0.00311271297804302, 0.0],
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
            "samples": [0.0, -0.00155635648902151, -0.0033777873566317807, -0.00546572635986626, -0.00780816630462254, -0.01037747116124298, -0.013129048078118287, -0.01600118966531908, -0.018916320002920227, -0.021783755530953477, -0.024503934529090544, -0.026973894008938397, -0.029093603717051407, -0.030772628893114502, -0.03193650965202938] + [-0.03253223216978802] * 2 + [-0.03193650965202938, -0.030772628893114502, -0.029093603717051407, -0.026973894008938397, -0.024503934529090544, -0.021783755530953477, -0.018916320002920227, -0.01600118966531908, -0.013129048078118287, -0.01037747116124298, -0.00780816630462254, -0.00546572635986626, -0.0033777873566317807, -0.00155635648902151, 0.0],
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
            "samples": [0.0, 0.00155635648902151, 0.0033777873566317807, 0.00546572635986626, 0.00780816630462254, 0.01037747116124298, 0.013129048078118287, 0.01600118966531908, 0.018916320002920227, 0.021783755530953477, 0.024503934529090544, 0.026973894008938397, 0.029093603717051407, 0.030772628893114502, 0.03193650965202938] + [0.03253223216978802] * 2 + [0.03193650965202938, 0.030772628893114502, 0.029093603717051407, 0.026973894008938397, 0.024503934529090544, 0.021783755530953477, 0.018916320002920227, 0.01600118966531908, 0.013129048078118287, 0.01037747116124298, 0.00780816630462254, 0.00546572635986626, 0.0033777873566317807, 0.00155635648902151, 0.0],
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
            "samples": [0.0, 0.00311271297804302, 0.006755574713263561, 0.01093145271973252, 0.01561633260924508, 0.02075494232248596, 0.026258096156236574, 0.03200237933063816, 0.037832640005840454, 0.043567511061906955, 0.04900786905818109, 0.053947788017876794, 0.058187207434102814, 0.061545257786229005, 0.06387301930405875] + [0.06506446433957604] * 2 + [0.06387301930405875, 0.061545257786229005, 0.058187207434102814, 0.053947788017876794, 0.04900786905818109, 0.043567511061906955, 0.037832640005840454, 0.03200237933063816, 0.026258096156236574, 0.02075494232248596, 0.01561633260924508, 0.01093145271973252, 0.006755574713263561, 0.00311271297804302, 0.0],
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
            "samples": [0.0, -0.00155635648902151, -0.0033777873566317807, -0.00546572635986626, -0.00780816630462254, -0.01037747116124298, -0.013129048078118287, -0.01600118966531908, -0.018916320002920227, -0.021783755530953477, -0.024503934529090544, -0.026973894008938397, -0.029093603717051407, -0.030772628893114502, -0.03193650965202938] + [-0.03253223216978802] * 2 + [-0.03193650965202938, -0.030772628893114502, -0.029093603717051407, -0.026973894008938397, -0.024503934529090544, -0.021783755530953477, -0.018916320002920227, -0.01600118966531908, -0.013129048078118287, -0.01037747116124298, -0.00780816630462254, -0.00546572635986626, -0.0033777873566317807, -0.00155635648902151, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q2": {
            "sample": 0.06399,
            "type": "constant",
        },
        "x90_I_wf_q3": {
            "samples": [0.0, 0.00044143929506791895, 0.000958063322971923, 0.0015502787493438847, 0.0022146798973111206, 0.00294342818391619, 0.003723875454884459, 0.004538519250526867, 0.005365356219010101, 0.006178665205143168, 0.0069502068846147725, 0.007650777209807981, 0.008252003963381854, 0.008728236558774295, 0.00905835546493924] + [0.0092273240336126] * 2 + [0.00905835546493924, 0.008728236558774295, 0.008252003963381854, 0.007650777209807981, 0.0069502068846147725, 0.006178665205143168, 0.005365356219010101, 0.004538519250526867, 0.003723875454884459, 0.00294342818391619, 0.0022146798973111206, 0.0015502787493438847, 0.000958063322971923, 0.00044143929506791895, 0.0],
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
            "samples": [0.0, 0.0008828785901358379, 0.001916126645943846, 0.0031005574986877693, 0.004429359794622241, 0.00588685636783238, 0.007447750909768918, 0.009077038501053734, 0.010730712438020202, 0.012357330410286336, 0.013900413769229545, 0.015301554419615962, 0.01650400792676371, 0.01745647311754859, 0.01811671092987848] + [0.0184546480672252] * 2 + [0.01811671092987848, 0.01745647311754859, 0.01650400792676371, 0.015301554419615962, 0.013900413769229545, 0.012357330410286336, 0.010730712438020202, 0.009077038501053734, 0.007447750909768918, 0.00588685636783238, 0.004429359794622241, 0.0031005574986877693, 0.001916126645943846, 0.0008828785901358379, 0.0],
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
            "samples": [0.0, -0.00044143929506791895, -0.000958063322971923, -0.0015502787493438847, -0.0022146798973111206, -0.00294342818391619, -0.003723875454884459, -0.004538519250526867, -0.005365356219010101, -0.006178665205143168, -0.0069502068846147725, -0.007650777209807981, -0.008252003963381854, -0.008728236558774295, -0.00905835546493924] + [-0.0092273240336126] * 2 + [-0.00905835546493924, -0.008728236558774295, -0.008252003963381854, -0.007650777209807981, -0.0069502068846147725, -0.006178665205143168, -0.005365356219010101, -0.004538519250526867, -0.003723875454884459, -0.00294342818391619, -0.0022146798973111206, -0.0015502787493438847, -0.000958063322971923, -0.00044143929506791895, 0.0],
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
            "samples": [0.0, 0.00044143929506791895, 0.000958063322971923, 0.0015502787493438847, 0.0022146798973111206, 0.00294342818391619, 0.003723875454884459, 0.004538519250526867, 0.005365356219010101, 0.006178665205143168, 0.0069502068846147725, 0.007650777209807981, 0.008252003963381854, 0.008728236558774295, 0.00905835546493924] + [0.0092273240336126] * 2 + [0.00905835546493924, 0.008728236558774295, 0.008252003963381854, 0.007650777209807981, 0.0069502068846147725, 0.006178665205143168, 0.005365356219010101, 0.004538519250526867, 0.003723875454884459, 0.00294342818391619, 0.0022146798973111206, 0.0015502787493438847, 0.000958063322971923, 0.00044143929506791895, 0.0],
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
            "samples": [0.0, 0.0008828785901358379, 0.001916126645943846, 0.0031005574986877693, 0.004429359794622241, 0.00588685636783238, 0.007447750909768918, 0.009077038501053734, 0.010730712438020202, 0.012357330410286336, 0.013900413769229545, 0.015301554419615962, 0.01650400792676371, 0.01745647311754859, 0.01811671092987848] + [0.0184546480672252] * 2 + [0.01811671092987848, 0.01745647311754859, 0.01650400792676371, 0.015301554419615962, 0.013900413769229545, 0.012357330410286336, 0.010730712438020202, 0.009077038501053734, 0.007447750909768918, 0.00588685636783238, 0.004429359794622241, 0.0031005574986877693, 0.001916126645943846, 0.0008828785901358379, 0.0],
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
            "samples": [0.0, -0.00044143929506791895, -0.000958063322971923, -0.0015502787493438847, -0.0022146798973111206, -0.00294342818391619, -0.003723875454884459, -0.004538519250526867, -0.005365356219010101, -0.006178665205143168, -0.0069502068846147725, -0.007650777209807981, -0.008252003963381854, -0.008728236558774295, -0.00905835546493924] + [-0.0092273240336126] * 2 + [-0.00905835546493924, -0.008728236558774295, -0.008252003963381854, -0.007650777209807981, -0.0069502068846147725, -0.006178665205143168, -0.005365356219010101, -0.004538519250526867, -0.003723875454884459, -0.00294342818391619, -0.0022146798973111206, -0.0015502787493438847, -0.000958063322971923, -0.00044143929506791895, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q3": {
            "sample": 0.0579743325,
            "type": "constant",
        },
        "x90_I_wf_q4": {
            "samples": [0.0, 0.0023042161006292493, 0.005000879982545753, 0.008092114350970828, 0.011560142321129478, 0.015364048212749346, 0.019437811440330972, 0.023690073010991894, 0.028005980264063715, 0.032251274422450606, 0.0362785524196925, 0.03993537554570101, 0.043073647061608586, 0.045559476543052646, 0.04728262467962791] + [0.04816460347215369] * 2 + [0.04728262467962791, 0.045559476543052646, 0.043073647061608586, 0.03993537554570101, 0.0362785524196925, 0.032251274422450606, 0.028005980264063715, 0.023690073010991894, 0.019437811440330972, 0.015364048212749346, 0.011560142321129478, 0.008092114350970828, 0.005000879982545753, 0.0023042161006292493, 0.0],
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
            "samples": [0.0, 0.0046084322012584986, 0.010001759965091506, 0.016184228701941656, 0.023120284642258956, 0.03072809642549869, 0.038875622880661945, 0.04738014602198379, 0.05601196052812743, 0.06450254884490121, 0.072557104839385, 0.07987075109140201, 0.08614729412321717, 0.09111895308610529, 0.09456524935925582] + [0.09632920694430738] * 2 + [0.09456524935925582, 0.09111895308610529, 0.08614729412321717, 0.07987075109140201, 0.072557104839385, 0.06450254884490121, 0.05601196052812743, 0.04738014602198379, 0.038875622880661945, 0.03072809642549869, 0.023120284642258956, 0.016184228701941656, 0.010001759965091506, 0.0046084322012584986, 0.0],
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
            "samples": [0.0, -0.0023042161006292493, -0.005000879982545753, -0.008092114350970828, -0.011560142321129478, -0.015364048212749346, -0.019437811440330972, -0.023690073010991894, -0.028005980264063715, -0.032251274422450606, -0.0362785524196925, -0.03993537554570101, -0.043073647061608586, -0.045559476543052646, -0.04728262467962791] + [-0.04816460347215369] * 2 + [-0.04728262467962791, -0.045559476543052646, -0.043073647061608586, -0.03993537554570101, -0.0362785524196925, -0.032251274422450606, -0.028005980264063715, -0.023690073010991894, -0.019437811440330972, -0.015364048212749346, -0.011560142321129478, -0.008092114350970828, -0.005000879982545753, -0.0023042161006292493, 0.0],
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
            "samples": [0.0, 0.0023042161006292493, 0.005000879982545753, 0.008092114350970828, 0.011560142321129478, 0.015364048212749346, 0.019437811440330972, 0.023690073010991894, 0.028005980264063715, 0.032251274422450606, 0.0362785524196925, 0.03993537554570101, 0.043073647061608586, 0.045559476543052646, 0.04728262467962791] + [0.04816460347215369] * 2 + [0.04728262467962791, 0.045559476543052646, 0.043073647061608586, 0.03993537554570101, 0.0362785524196925, 0.032251274422450606, 0.028005980264063715, 0.023690073010991894, 0.019437811440330972, 0.015364048212749346, 0.011560142321129478, 0.008092114350970828, 0.005000879982545753, 0.0023042161006292493, 0.0],
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
            "samples": [0.0, 0.0046084322012584986, 0.010001759965091506, 0.016184228701941656, 0.023120284642258956, 0.03072809642549869, 0.038875622880661945, 0.04738014602198379, 0.05601196052812743, 0.06450254884490121, 0.072557104839385, 0.07987075109140201, 0.08614729412321717, 0.09111895308610529, 0.09456524935925582] + [0.09632920694430738] * 2 + [0.09456524935925582, 0.09111895308610529, 0.08614729412321717, 0.07987075109140201, 0.072557104839385, 0.06450254884490121, 0.05601196052812743, 0.04738014602198379, 0.038875622880661945, 0.03072809642549869, 0.023120284642258956, 0.016184228701941656, 0.010001759965091506, 0.0046084322012584986, 0.0],
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
            "samples": [0.0, -0.0023042161006292493, -0.005000879982545753, -0.008092114350970828, -0.011560142321129478, -0.015364048212749346, -0.019437811440330972, -0.023690073010991894, -0.028005980264063715, -0.032251274422450606, -0.0362785524196925, -0.03993537554570101, -0.043073647061608586, -0.045559476543052646, -0.04728262467962791] + [-0.04816460347215369] * 2 + [-0.04728262467962791, -0.045559476543052646, -0.043073647061608586, -0.03993537554570101, -0.0362785524196925, -0.032251274422450606, -0.028005980264063715, -0.023690073010991894, -0.019437811440330972, -0.015364048212749346, -0.011560142321129478, -0.008092114350970828, -0.005000879982545753, -0.0023042161006292493, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q4": {
            "sample": 0.291757965,
            "type": "constant",
        },
        "x90_I_wf_q5": {
            "samples": [0.0, 0.0032259025408809486, 0.007001231975564055, 0.011328960091359157, 0.01618419924958126, 0.021509667497849085, 0.02721293601646336, 0.03316610221538865, 0.0392083723696892, 0.045151784191430844, 0.0507899733875695, 0.0559095257639814, 0.06030310588625202, 0.06378326716027369, 0.06619567455147907] + [0.06743044486101515] * 2 + [0.06619567455147907, 0.06378326716027369, 0.06030310588625202, 0.0559095257639814, 0.0507899733875695, 0.045151784191430844, 0.0392083723696892, 0.03316610221538865, 0.02721293601646336, 0.021509667497849085, 0.01618419924958126, 0.011328960091359157, 0.007001231975564055, 0.0032259025408809486, 0.0],
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
            "samples": [0.0, 0.006451805081761897, 0.01400246395112811, 0.022657920182718314, 0.03236839849916252, 0.04301933499569817, 0.05442587203292672, 0.0663322044307773, 0.0784167447393784, 0.09030356838286169, 0.101579946775139, 0.1118190515279628, 0.12060621177250404, 0.12756653432054738, 0.13239134910295813] + [0.1348608897220303] * 2 + [0.13239134910295813, 0.12756653432054738, 0.12060621177250404, 0.1118190515279628, 0.101579946775139, 0.09030356838286169, 0.0784167447393784, 0.0663322044307773, 0.05442587203292672, 0.04301933499569817, 0.03236839849916252, 0.022657920182718314, 0.01400246395112811, 0.006451805081761897, 0.0],
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
            "samples": [0.0, -0.0032259025408809486, -0.007001231975564055, -0.011328960091359157, -0.01618419924958126, -0.021509667497849085, -0.02721293601646336, -0.03316610221538865, -0.0392083723696892, -0.045151784191430844, -0.0507899733875695, -0.0559095257639814, -0.06030310588625202, -0.06378326716027369, -0.06619567455147907] + [-0.06743044486101515] * 2 + [-0.06619567455147907, -0.06378326716027369, -0.06030310588625202, -0.0559095257639814, -0.0507899733875695, -0.045151784191430844, -0.0392083723696892, -0.03316610221538865, -0.02721293601646336, -0.021509667497849085, -0.01618419924958126, -0.011328960091359157, -0.007001231975564055, -0.0032259025408809486, 0.0],
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
            "samples": [0.0, 0.0032259025408809486, 0.007001231975564055, 0.011328960091359157, 0.01618419924958126, 0.021509667497849085, 0.02721293601646336, 0.03316610221538865, 0.0392083723696892, 0.045151784191430844, 0.0507899733875695, 0.0559095257639814, 0.06030310588625202, 0.06378326716027369, 0.06619567455147907] + [0.06743044486101515] * 2 + [0.06619567455147907, 0.06378326716027369, 0.06030310588625202, 0.0559095257639814, 0.0507899733875695, 0.045151784191430844, 0.0392083723696892, 0.03316610221538865, 0.02721293601646336, 0.021509667497849085, 0.01618419924958126, 0.011328960091359157, 0.007001231975564055, 0.0032259025408809486, 0.0],
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
            "samples": [0.0, 0.006451805081761897, 0.01400246395112811, 0.022657920182718314, 0.03236839849916252, 0.04301933499569817, 0.05442587203292672, 0.0663322044307773, 0.0784167447393784, 0.09030356838286169, 0.101579946775139, 0.1118190515279628, 0.12060621177250404, 0.12756653432054738, 0.13239134910295813] + [0.1348608897220303] * 2 + [0.13239134910295813, 0.12756653432054738, 0.12060621177250404, 0.1118190515279628, 0.101579946775139, 0.09030356838286169, 0.0784167447393784, 0.0663322044307773, 0.05442587203292672, 0.04301933499569817, 0.03236839849916252, 0.022657920182718314, 0.01400246395112811, 0.006451805081761897, 0.0],
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
            "samples": [0.0, -0.0032259025408809486, -0.007001231975564055, -0.011328960091359157, -0.01618419924958126, -0.021509667497849085, -0.02721293601646336, -0.03316610221538865, -0.0392083723696892, -0.045151784191430844, -0.0507899733875695, -0.0559095257639814, -0.06030310588625202, -0.06378326716027369, -0.06619567455147907] + [-0.06743044486101515] * 2 + [-0.06619567455147907, -0.06378326716027369, -0.06030310588625202, -0.0559095257639814, -0.0507899733875695, -0.045151784191430844, -0.0392083723696892, -0.03316610221538865, -0.02721293601646336, -0.021509667497849085, -0.01618419924958126, -0.011328960091359157, -0.007001231975564055, -0.0032259025408809486, 0.0],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "readout_wf_q5": {
            "sample": 0.0397908618,
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
            "cosine": [(1.0, 2000)],
            "sine": [(0.0, 2000)],
        },
        "sine_weights": {
            "cosine": [(0.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "minus_sine_weights": {
            "cosine": [(0.0, 2000)],
            "sine": [(-1.0, 2000)],
        },
        "rotated_cosine_weights_q1": {
            "cosine": [(0.14953534344370958, 2000)],
            "sine": [(0.9887563810470058, 2000)],
        },
        "rotated_sine_weights_q1": {
            "cosine": [(-0.9887563810470058, 2000)],
            "sine": [(0.14953534344370958, 2000)],
        },
        "rotated_minus_sine_weights_q1": {
            "cosine": [(0.9887563810470058, 2000)],
            "sine": [(-0.14953534344370958, 2000)],
        },
        "rotated_cosine_weights_q2": {
            "cosine": [(-0.9291325715340562, 2000)],
            "sine": [(-0.36974675727382916, 2000)],
        },
        "rotated_sine_weights_q2": {
            "cosine": [(0.36974675727382916, 2000)],
            "sine": [(-0.9291325715340562, 2000)],
        },
        "rotated_minus_sine_weights_q2": {
            "cosine": [(-0.36974675727382916, 2000)],
            "sine": [(0.9291325715340562, 2000)],
        },
        "rotated_cosine_weights_q3": {
            "cosine": [(-0.6279630576493378, 2000)],
            "sine": [(0.7782431485260211, 2000)],
        },
        "rotated_sine_weights_q3": {
            "cosine": [(-0.7782431485260211, 2000)],
            "sine": [(-0.6279630576493378, 2000)],
        },
        "rotated_minus_sine_weights_q3": {
            "cosine": [(0.7782431485260211, 2000)],
            "sine": [(0.6279630576493378, 2000)],
        },
        "rotated_cosine_weights_q4": {
            "cosine": [(0.656059028990507, 2000)],
            "sine": [(-0.7547095802227722, 2000)],
        },
        "rotated_sine_weights_q4": {
            "cosine": [(0.7547095802227722, 2000)],
            "sine": [(0.656059028990507, 2000)],
        },
        "rotated_minus_sine_weights_q4": {
            "cosine": [(-0.7547095802227722, 2000)],
            "sine": [(-0.656059028990507, 2000)],
        },
        "rotated_cosine_weights_q5": {
            "cosine": [(-0.16504760586067815, 2000)],
            "sine": [(-0.9862856015372313, 2000)],
        },
        "rotated_sine_weights_q5": {
            "cosine": [(0.9862856015372313, 2000)],
            "sine": [(-0.16504760586067815, 2000)],
        },
        "rotated_minus_sine_weights_q5": {
            "cosine": [(-0.9862856015372313, 2000)],
            "sine": [(0.16504760586067815, 2000)],
        },
        "opt_cosine_weights_q1": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_sine_weights_q1": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_minus_sine_weights_q1": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_cosine_weights_q2": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_sine_weights_q2": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_minus_sine_weights_q2": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_cosine_weights_q3": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_sine_weights_q3": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_minus_sine_weights_q3": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_cosine_weights_q4": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_sine_weights_q4": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_minus_sine_weights_q4": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_cosine_weights_q5": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_sine_weights_q5": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
        "opt_minus_sine_weights_q5": {
            "cosine": [(1.0, 2000)],
            "sine": [(1.0, 2000)],
        },
    },
    "mixers": {
        "octave_octave1_2": [
            {'intermediate_frequency': 346063000.0, 'lo_frequency': 3670000000.0, 'correction': [1.139035176485777, 0.16698597371578217, 0.19680260121822357, 0.9664653651416302]},
            {'intermediate_frequency': 135471000.0, 'lo_frequency': 3200000000.0, 'correction': [0.9071802385151386, 0.06404274702072144, 0.0515754371881485, 1.1264725401997566]},
            {'intermediate_frequency': 135196000.0, 'lo_frequency': 3200000000.0, 'correction': [0.9105054624378681, 0.06347507238388062, 0.05154538154602051, 1.1212333254516125]},
            {'intermediate_frequency': 130808000.0, 'lo_frequency': 3200000000.0, 'correction': [0.9090330041944981, 0.0641556978225708, 0.051899492740631104, 1.1237035803496838]},
            {'intermediate_frequency': 130785000.0, 'lo_frequency': 3200000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
        ],
        "octave_octave1_3": [
            {'intermediate_frequency': 471832000.0, 'lo_frequency': 3670000000.0, 'correction': [1.0509245730936527, 0.1871345043182373, 0.1878669261932373, 1.0468274168670177]},
            {'intermediate_frequency': 262537000.0, 'lo_frequency': 3200000000.0, 'correction': [0.8680114857852459, -0.004036571830511093, -0.002966787666082382, 1.1810052506625652]},
            {'intermediate_frequency': 261338000.0, 'lo_frequency': 3200000000.0, 'correction': [0.8681640625, 0.0, 0.0, 1.1806640625]},
            {'intermediate_frequency': 262288000.0, 'lo_frequency': 3200000000.0, 'correction': [0.8680580779910088, -0.004612911492586136, -0.0033907778561115265, 1.1809314489364624]},
            {'intermediate_frequency': 261760000.0, 'lo_frequency': 3200000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
        ],
        "octave_octave1_4": [{'intermediate_frequency': 146495000.0, 'lo_frequency': 4000000000.0, 'correction': [1.39941843226552, -0.06450551748275757, -0.11300128698348999, 0.798842303454876]}],
        "octave_octave1_5": [
            {'intermediate_frequency': 408869000.0, 'lo_frequency': 4000000000.0, 'correction': [1.4782978221774101, -0.05286115035414696, -0.10035889968276024, 0.7786506339907646]},
            {'intermediate_frequency': 408712000.0, 'lo_frequency': 4000000000.0, 'correction': [1.472061611711979, -0.05293846130371094, -0.09993553161621094, 0.7797894850373268]},
        ],
        "octave_octave2_1": [
            {'intermediate_frequency': 24209000.0, 'lo_frequency': 4500000000.0, 'correction': [1.2739626578986645, -0.05181884765625, -0.07916259765625, 0.8339200429618359]},
            {'intermediate_frequency': 24184000.0, 'lo_frequency': 4500000000.0, 'correction': [1.2739626578986645, -0.05181884765625, -0.07916259765625, 0.8339200429618359]},
            {'intermediate_frequency': 24196000.0, 'lo_frequency': 4500000000.0, 'correction': [1.2739626578986645, -0.05181884765625, -0.07916259765625, 0.8339200429618359]},
            {'intermediate_frequency': 24179000.0, 'lo_frequency': 4500000000.0, 'correction': [1.0, 0.0, 0.0, 1.0]},
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
            {'intermediate_frequency': 163122000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0789089314639568, -0.13434219360351562, -0.14752578735351562, 0.9824925884604454]},
            {'intermediate_frequency': 49753000.0, 'lo_frequency': 5900000000.0, 'correction': [1.087750818580389, -0.1489931344985962, -0.1642519235610962, 0.9867001883685589]},
            {'intermediate_frequency': 218194000.0, 'lo_frequency': 5900000000.0, 'correction': [1.1093690656125546, -0.17780685424804688, -0.19831466674804688, 0.9946486912667751]},
            {'intermediate_frequency': 28632000.0, 'lo_frequency': 5900000000.0, 'correction': [1.0886423401534557, -0.1607622355222702, -0.1758531779050827, 0.9952198676764965]},
        ],
    },
}



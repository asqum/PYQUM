from pyqum.instrument.modular import AWG

def squarewave(seg1, seg2):
    s = AWG.InitWithOptions()
    AWG.Abort_Gen(s)
    # Setting Marker:
    AWG.active_marker(s, action=["Set", "1"])
    AWG.active_marker(s)
    AWG.marker_source(s, action=["Set", 10])
    AWG.marker_source(s)
    AWG.marker_delay(s, action=["Set", 2e-7])
    AWG.marker_delay(s)
    AWG.marker_pulse_width(s, action=["Set", 2.5e-7])
    AWG.marker_pulse_width(s)

    # Preparing AWGenerator
    AWG.output_mode_adv(s, action=["Set", 2])
    AWG.output_mode_adv(s)
    AWG.predistortion_enabled(s, action=["Set", False])
    AWG.predistortion_enabled(s)

    # Assigning handles to each different waveform
    # stat = AWG.CreateArbWaveform(s, ([i*0 for i in range(100)] + [i*1 for i in range(seg1)] + [i*0 for i in range(100)]))
    stat = AWG.CreateArbWaveform(s, ([i*1 for i in range(seg1)]))
    h1 = stat[1]
    stat = AWG.CreateArbWaveform(s, ([i*0 for i in range(seg2)]))
    h2 = stat[1]
    # Composing different sequences to each channel
    # Channel 1
    Seq = {}
    Seq[(h1)], Seq[(h2)] = 0, 0 #loopcount
    stat = AWG.CreateArbSequence(s, Seq)
    AWG.arb_sequence_handle(s, RepCap='1', action=["Set", stat[1]])
    AWG.arb_sequence_handle(s, RepCap='1')
    # Channel 2
    Seq = {}
    Seq[str(h1)], Seq[str(h2)] = 1, 1
    stat = AWG.CreateArbSequence(s, Seq)
    AWG.arb_sequence_handle(s, RepCap='2', action=["Set", stat[1]])
    AWG.arb_sequence_handle(s, RepCap='2')
    # Setting Sample Rate
    AWG.arb_sample_rate(s, action=["Set", 1250000000])
    AWG.arb_sample_rate(s)
    # Configure Output (Channels)
    AWG.output_enabled(s, RepCap='1', action=["Set", True])
    AWG.output_enabled(s, RepCap='1')
    AWG.output_enabled(s, RepCap='2', action=["Set", True])
    AWG.output_enabled(s, RepCap='2')
    AWG.OupConfig(s, "1")
    AWG.OupConfig(s, "2")
    AWG.arb_gain(s, RepCap='1', action=["Set", 0.25])
    AWG.arb_gain(s, RepCap='1')
    AWG.arb_gain(s, RepCap='2', action=["Set", 0.25])
    AWG.arb_gain(s, RepCap='2')
    AWG.output_impedance(s, RepCap='1', action=["Set", 50])
    AWG.output_impedance(s, RepCap='1')
    AWG.output_impedance(s, RepCap='2', action=["Set", 50])
    AWG.output_impedance(s, RepCap='2')
    AWG.operation_mode(s, RepCap='1')
    AWG.operation_mode(s, RepCap='1', action=["Set", 0])
    AWG.operation_mode(s, RepCap='2')
    AWG.operation_mode(s, RepCap='2', action=["Set", 0])
    AWG.trigger_source_adv(s, RepCap='1')
    AWG.trigger_source_adv(s, RepCap='1', action=["Set", 0])
    AWG.trigger_source_adv(s, RepCap='2')
    AWG.trigger_source_adv(s, RepCap='2', action=["Set", 0])
    
    AWG.Init_Gen(s)
    AWG.close(s)
    return

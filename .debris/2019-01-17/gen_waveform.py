from pyqum.instrument.modular import AWG
AWG.debug(True)

def squarewave(ch1g, ch1e, ch2g, ch2e):
    s = AWG.InitWithOptions()
    AWG.Clear_ArbMemory(s)
    AWG.Abort_Gen(s)

    # Setting Marker:
    AWG.active_marker(s, action=["Set", "3"])
    AWG.marker_source(s, action=["Set", 7])
    AWG.marker_delay(s, action=["Set", 2e-7])
    AWG.marker_pulse_width(s, action=["Set", 2.5e-7])

    # Preparing AWGenerator
    AWG.output_mode_adv(s, action=["Set", 2])
    AWG.output_mode_adv(s)
    AWG.predistortion_enabled(s, action=["Set", False])
    AWG.predistortion_enabled(s)

    # Setting Sample Rate
    AWG.arb_sample_rate(s, action=["Set", 1250000000])
    AWG.arb_sample_rate(s)

    # Create Waveform
    stat = AWG.CreateArbWaveform(s, ([0]*ch1g + [1]*ch1e))
    ch1 = stat[1]
    stat = AWG.CreateArbWaveform(s, ([0]*ch2g + [1]*ch2e))
    ch2 = stat[1]

    # Composing different sequences to each channel
    # Channel 1
    i = 1
    if i:
        Seq, counts = [ch1], [1] #unique wfm
        stat = AWG.CreateArbSequence(s, Seq, counts)
        AWG.arb_sequence_handle(s, RepCap='1', action=["Set", stat[1]])
        AWG.arb_sequence_handle(s, RepCap='1')
        AWG.output_enabled(s, RepCap='1', action=["Set", True])
        AWG.output_enabled(s, RepCap='1')
        AWG.output_filter_enabled(s, RepCap='1')
        AWG.output_filter_enabled(s, RepCap='1', action=["Set", False])
        AWG.output_filter_bandwidth(s, RepCap='1')
        AWG.output_filter_bandwidth(s, RepCap='1', action=["Set", 0])
        AWG.output_config(s, RepCap='1')
        AWG.output_config(s, RepCap='1', action=["Set", 0])
        AWG.arb_gain(s, RepCap='1', action=["Set", 0.25])
        AWG.arb_gain(s, RepCap='1')
        AWG.output_impedance(s, RepCap='1', action=["Set", 50])
        AWG.output_impedance(s, RepCap='1')
        # Setting pulse mode (Single or Continuous)
        AWG.operation_mode(s, RepCap='1')
        AWG.operation_mode(s, RepCap='1', action=["Set", 0])
        AWG.trigger_source_adv(s, RepCap='1')
        AWG.trigger_source_adv(s, RepCap='1', action=["Set", 0])
        AWG.burst_count(s, RepCap='1', action=["Set", 1000001])

    # Channel 2
    i = 1
    if i:
        Seq, counts = [ch2], [1] #unique wfm
        stat = AWG.CreateArbSequence(s, Seq, counts)
        AWG.arb_sequence_handle(s, RepCap='2', action=["Set", stat[1]])
        AWG.arb_sequence_handle(s, RepCap='2')
        AWG.output_enabled(s, RepCap='2', action=["Set", True])
        AWG.output_enabled(s, RepCap='2')
        AWG.output_filter_enabled(s, RepCap='2')
        AWG.output_filter_enabled(s, RepCap='2', action=["Set", False])
        AWG.output_filter_bandwidth(s, RepCap='2')
        AWG.output_filter_bandwidth(s, RepCap='2', action=["Set", 0])
        AWG.output_config(s, RepCap='2')
        AWG.output_config(s, RepCap='2', action=["Set", 0])
        AWG.arb_gain(s, RepCap='2', action=["Set", 0.25])
        AWG.arb_gain(s, RepCap='2')
        AWG.output_impedance(s, RepCap='2', action=["Set", 50])
        AWG.output_impedance(s, RepCap='2')
        # Setting pulse mode (Single or Continuous)
        AWG.operation_mode(s, RepCap='2')
        AWG.operation_mode(s, RepCap='2', action=["Set", 0])
        AWG.trigger_source_adv(s, RepCap='2')
        AWG.trigger_source_adv(s, RepCap='2', action=["Set", 0])
        AWG.burst_count(s, RepCap='2', action=["Set", 1000001])

    AWG.Init_Gen(s)
    AWG.close(s)
    return


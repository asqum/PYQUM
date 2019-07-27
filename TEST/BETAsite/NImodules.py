# This is a collection of modular VI written by Watson's Lab

from Callout import Call_VI

@Call_VI
def AWG_Seq(initializ):
    pack = dict()
    pack['VIPath'] = "C:\\Labview 2011\\Measure\\Meas PXI.llb\\AWG waveform sequence.vi"
    pack['ParameterNames'] = ["initialize"]
    pack['Parameters'] = [initializ]
    pack['Indicators'] = ["AWG on"]
    return pack

@Call_VI
def VSA_control(switch):
    pack = dict()
    pack['VIPath'] = "C:\\Labview 2011\\Measure\\Meas PXI.llb\\VSA control on-off.vi"
    pack['ParameterNames'] = ["Switch"]
    pack['Parameters'] = [switch]
    pack['Indicators'] = []
    return pack

@Call_VI
def AWG_Gen(waveforms):
    pack = dict()
    pack['VIPath'] = "C:\\Labview 2011\\Measure\\Meas PXI.llb\\AWG Generate waveform.vi"
    pack['ParameterNames'] = ["CH1", "CH2"]
    pack['Parameters'] = waveforms
    pack['Indicators'] = ["ch1(us)"]
    return pack

@Call_VI
def DigitizeIQ(Parameters):
    pack = dict()
    pack['VIPath'] = "C:\\Labview 2011\\Measure\\Meas PXI.llb\\measure VSA one curve no log.vi"
    pack['ParameterNames'] = ['setup cluster IN'] #'Frequency (GHz)', 'Bandwidth (kHz)', 'Power (dBm)', 'Acquisition time (s)' 
    pack['Parameters'] = Parameters
    pack['Indicators'] = ["IQ Curve"]
    return pack

# VSA_control(False) # For Testing

# This is a collection of simple VIs for Agilent Drivers

from QuApp.tools.Callout import Call_VI
# from Callout import Call_VI

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
    pack['Parameters'] = Parameters # variant: [[freq(GHz), Bandwidth(kHz), Power(dBm), Acqtime(s)]]
    pack['Indicators'] = ["IQ Curve"]
    return pack

# Example:
# data = DigitizeIQ([[3, 125000, -30, 2e-5]])
# print(data)
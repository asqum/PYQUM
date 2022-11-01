
import matplotlib.pyplot as plt
from pulse_signal.pulse import Pulse
from pulse_signal.common_Mathfunc import gaussianFunc, DRAGFunc
from pulse_signal.digital_mixer import upConversion_RF

pulse_duration = 30
t0 = 0
freq_IF = -0.0
freq_RF = 4.8

MixerSetting = (1, 90, 0, 0) #IQMixer: tuple = (1, 90, 0, 0)
testPulse = Pulse()

testPulse.duration = pulse_duration
testPulse.carrierFrequency = freq_RF
testPulse.carrierPhase = 0
testPulse.envelopeFunc = DRAGFunc
testPulse.parameters = (1,pulse_duration/4, (pulse_duration+t0)/2, 5 )

WF_envelope = testPulse.generate_envelope( t0, 1 )
time_env = WF_envelope.get_xAxis()
WF_signal = testPulse.generate_signal( t0, 0.001 )
time_sig = WF_signal.get_xAxis()

WF_signal_I, WF_signal_Q, freq_LO = testPulse.generate_IQSignal( t0, 0.001, freq_IF, IQMixer=MixerSetting)

signal_RF = upConversion_RF( WF_signal_I.Y, WF_signal_Q.Y, freq_LO*0.001, IQMixer=MixerSetting)

# Plot setting
fig, ax = plt.subplots(3,1,sharex=True)

# Compare signal and envelope
ax[0].plot( time_sig, WF_signal.Y, label="Target Signal" )
ax[0].plot( WF_envelope.get_xAxis(), abs(WF_envelope.Y), label="ABS envelope" )

ax[0].plot( WF_envelope.get_xAxis(), WF_envelope.Y.real, label="real envelope" )
ax[0].plot( WF_envelope.get_xAxis(), WF_envelope.Y.imag, label="imag envelope" )


ax[0].legend()

# Compare IQ signal and envelope
ax[1].plot( WF_envelope.get_xAxis(), abs(WF_envelope.Y), label="envelope" )
ax[1].plot( WF_signal_I.get_xAxis(), WF_signal_I.Y, label="I" )
ax[1].plot( WF_signal_Q.get_xAxis(), WF_signal_Q.Y, label="Q" )
ax[1].legend()

# Compare Desire sigmal and remixed signal by IQ signal
ax[2].plot( WF_signal_I.get_xAxis(), signal_RF, label="RF Signal" )
ax[2].plot( WF_signal.get_xAxis(), WF_signal.Y, label="Target Signal" )
ax[2].legend()

plt.show()
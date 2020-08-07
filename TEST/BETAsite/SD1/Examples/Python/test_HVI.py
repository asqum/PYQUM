import sys
sys.path.append('C:\Program Files (x86)\Keysight\SD1\Libraries\Python')
#sys.path.append('/opt/keysightSD1/python')

import keysightSD1

# HVI
hvi = keysightSD1.SD_HVI()
hviID = hvi.open('setPhase.HVI')

# MODULE CONSTANTS
PRODUCT = ""
CHASSIS = 1
# change slot number to your value
SLOT = 4

# CREATE AND OPEN MODULE
aou = keysightSD1.SD_AOU()
aouID = aou.openWithSlot(PRODUCT, CHASSIS, SLOT)

if hviID > -1 and aouID > -1:
	wave = keysightSD1.SD_Wave()
	#wave.newFromFile('/var/keysightSD1/Examples/Waveforms/Gaussian.csv')
	# NOTE double "\" after "C:" is required because "\U" starts an unicode sequence
	wave.newFromFile('C:\\Users\Public\Documents\Keysight\SD1\Examples\Waveforms\Gaussian.csv')

	aou.waveformFlush()
	aou.waveformLoad(wave, 0)

	aou.AWGflush(0)
	aou.AWGqueueWaveform(0, 0, keysightSD1.SD_TriggerModes.SWHVITRIG, 0, 0, 1)
	aou.AWGflush(1)
	aou.AWGqueueWaveform(1, 0, keysightSD1.SD_TriggerModes.SWHVITRIG, 0, 0, 1)

	aou.channelWaveShape(0, keysightSD1.SD_Waveshapes.AOU_SINUSOIDAL)
	aou.channelAmplitude(0, 0.2)
	aou.channelFrequency(0, 100000000)

	aou.modulationAmplitudeConfig(0, keysightSD1.SD_ModulationTypes.AOU_MOD_AM, 0.5)

	aou.channelWaveShape(1, keysightSD1.SD_Waveshapes.AOU_SINUSOIDAL)
	aou.channelAmplitude(1, 0.2)
	aou.channelFrequency(1, 100000000)

	aou.modulationAmplitudeConfig(1, keysightSD1.SD_ModulationTypes.AOU_MOD_AM, 0.5)

	aou.AWGstartMultiple(3)
	aou.channelPhaseResetMultiple(3)
	aou.AWGtriggerMultiple(3)

	aou.writeRegisterByNumber(3, 0)

	phase = -90
	aou.writeRegisterByNumber(4, int((2**32) * (phase / 360)))

	hvi.start()

	# exiting...
	aou.close()
	print()
	print("AOU closed")
else:
	print("ERROR")
	print("hviID:", hviID)
	print("aouID:", aouID)

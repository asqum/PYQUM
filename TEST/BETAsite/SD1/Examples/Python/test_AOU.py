import sys
sys.path.append('C:\Program Files (x86)\Keysight\SD1\Libraries\Python')

import keysightSD1

waveform_data_list = [0.01,
0.02,
0.03,
0.04,
0.05,
0.06,
0.07,
0.08,
0.09,
0.1,
0.11,
0.12,
0.13,
0.14,
0.15,
0.16,
0.17,
0.18,
0.19,
0.2,
0.21,
0.22,
0.23,
0.24,
0.25,
0.26,
0.27,
0.28,
0.29,
0.3,
0.31,
0.32,
0.33,
0.34,
0.35,
0.36,
0.37,
0.38,
0.39,
0.4,
0.41,
0.42,
0.43,
0.44,
0.45,
0.46,
0.47,
0.48,
0.49,
0.5,
0.51,
0.52,
0.53,
0.54,
0.55,
0.56,
0.57,
0.58,
0.59,
0.6,
0.61,
0.62,
0.63,
0.64,
0.65,
0.66,
0.67,
0.68,
0.69,
0.7,
0.71,
0.72,
0.73,
0.74,
0.75,
0.76,
0.77,
0.78,
0.79,
0.8,
0.81,
0.82,
0.83,
0.84,
0.85,
0.86,
0.87,
0.88,
0.89,
0.9,
0.91,
0.92,
0.93,
0.94,
0.95,
0.96,
0.97,
0.98,
0.99,
1]

# MODULE CONSTANTS
PRODUCT = ""
CHASSIS = 1
# change slot number to your value
SLOT = 5

CHANNEL = 0

AMPLITUDE = 1.0

# CREATE AND OPEN MODULE
module = keysightSD1.SD_AOU()

moduleID = module.openWithSlot(PRODUCT, CHASSIS, SLOT)

if moduleID < 0:
	print("Module open error:", moduleID)
else:
	print("Module opened:", moduleID)
	print("Module name:", module.getProductName())
	print("slot:", module.getSlot())
	print("Chassis:", module.getChassis())
	print()

	module.channelWaveShape(0, keysightSD1.SD_Waveshapes.AOU_AWG)
	module.channelAmplitude(0, AMPLITUDE)

	# WAVEFORM FROM FILE
	WAVE_NUMBER = 0

	# create, open from file, load to module RAM and queue for execution  
	wave = keysightSD1.SD_Wave()
	# set pat to your file here
	wave.newFromFile("C:/Users/Public/Documents/keysightSD1/Examples/Waveforms/Gaussian.csv")
	module.waveformLoad(wave, 0)
	module.AWGqueueWaveform(CHANNEL, WAVE_NUMBER, 0, 0, 0, 0)

	error = module.AWGstart(0)

	if error < 0:
		print("AWG from file error:", error)
	else:
		print("AWG from file started successfully")

	# WAVEFORM FROM ARRAY/LIST
	# This function is equivalent to create a waveform with new,
	# and then to call waveformLoad, AWGqueueWaveform and AWGstart
	error = module.AWGfromArray(CHANNEL, 0, 0, 0, 0, 0, waveform_data_list)

	if error < 0:
		print("AWG from array error:", error)
	else:
		print("AWG from array started successfully")

	# exiting...
	module.close()
	print()
	print("AOU closed")

import sys
sys.path.append('C:\Program Files (x86)\Keysight\SD1\Libraries\Python')

import keysightSD1
import matplotlib.pyplot as plt
import numpy as np

# MODULE CONSTANTS
PRODUCT = ""
CHASSIS = 1

# change slot numbers to your values
SLOT_IN = 6
SLOT_OUT = 5

NUM_CHANNELS = 3
CHANNEL_TRIG_CONTROL = 3

# CREATE AND OPEN MODULE IN
moduleIn = keysightSD1.SD_AIN()

moduleInID = moduleIn.openWithSlot(PRODUCT, CHASSIS, SLOT_IN)

if moduleInID < 0:
	print("Error opening module IN - error code:", moduleInID)
else:
	print("===== MODULE IN =====")
	print("ID:\t\t", moduleInID)
	print("Product name:\t", moduleIn.getProductName())
	print("Serial number:\t", moduleIn.getSerialNumber())
	print("Chassis:\t", moduleIn.getChassis())
	print("Slot:\t\t", moduleIn.getSlot())

print()

# CREATE AND OPEN MODULE OUT
moduleOut = keysightSD1.SD_AOU()

moduleOutID = moduleOut.openWithSlot(PRODUCT, CHASSIS, SLOT_OUT)

if moduleOutID < 0:
	print("Error opening module OUT - error code:", moduleOutID)
else:
	print("===== MODULE OUT =====")
	print("ID:\t", moduleOutID)
	print("Product name:\t", moduleOut.getProductName())
	print("Serial number:\t", moduleOut.getSerialNumber())
	print("Chassis:\t", moduleOut.getChassis())
	print("slot:\t\t", moduleOut.getSlot())

if moduleInID > -1 and moduleOutID > -1:
	# CONFIGURE TRIGGERS
	TRIGGER_IN = 1
	TRIGGER_NOSYNC = 0

	moduleIn.triggerIOconfig(TRIGGER_IN, TRIGGER_NOSYNC)
	moduleOut.triggerIOconfig(TRIGGER_IN, TRIGGER_NOSYNC)

	# CREATE A WAVEFORM AND LOAD IT INTO MODULE OUT
	wave = keysightSD1.SD_Wave()
	wave.newFromFile("C:/Users/Public/Documents/keysightSD1/Examples/Waveforms/Gaussian.csv")

	WAVE_NUMBER = 0
	WAVE_CYCLES = 10000
	WAVE_PRESCALER = 0

	moduleOut.waveformFlush()
	moduleOut.waveformLoad(wave, WAVE_NUMBER)

	# CONFIGURE CHANNELS 0-2
	NUM_POINTS = 100
	NUM_CYCLES = 10000

	AMPLITUDE = 0.4
	FULL_SCALE = 0.5
	DC_COUPLING = 0
	IMPEDANCE_50 = 1

	DELAY_IN = 250
	DELAY_OUT = 0

	mask = 0

	for c in range(0, NUM_CHANNELS):
		mask |= 1 << c

		# MODULE IN
		moduleIn.channelInputConfig(c, FULL_SCALE, IMPEDANCE_50, DC_COUPLING)
		moduleIn.DAQconfig(c, NUM_POINTS, NUM_CYCLES, DELAY_IN, keysightSD1.SD_TriggerModes.EXTTRIG)
		moduleIn.DAQtriggerExternalConfig(c, keysightSD1.SD_TriggerExternalSources.TRIGGER_EXTERN, keysightSD1.SD_TriggerBehaviors.TRIGGER_RISE)

		# MODULE OUT
		moduleOut.channelAmplitude(c, AMPLITUDE)
		moduleOut.channelWaveShape(c, keysightSD1.SD_Waveshapes.AOU_AWG)

		moduleOut.AWGflush(c)
		moduleOut.AWGqueueWaveform(c, WAVE_NUMBER, keysightSD1.SD_TriggerModes.EXTTRIG_CYCLE, DELAY_OUT, WAVE_CYCLES, WAVE_PRESCALER)
		moduleOut.AWGtriggerExternalConfig(c, keysightSD1.SD_TriggerExternalSources.TRIGGER_EXTERN, keysightSD1.SD_TriggerBehaviors.TRIGGER_RISE)

	# CONFIGURE CHANNEL 3
	AMPLITUDE_C3 = 0.75
	OFFSET_C3 = 0.75
	FREQUENCY_C3 = 50000

	moduleOut.channelAmplitude(CHANNEL_TRIG_CONTROL, AMPLITUDE_C3)
	moduleOut.channelFrequency(CHANNEL_TRIG_CONTROL, FREQUENCY_C3)
	moduleOut.channelOffset(CHANNEL_TRIG_CONTROL, OFFSET_C3)
	moduleOut.channelWaveShape(CHANNEL_TRIG_CONTROL, keysightSD1.SD_Waveshapes.AOU_SQUARE)

	# SET WAVEFORM START
	moduleIn.DAQstartMultiple(mask)
	moduleOut.AWGstartMultiple(mask)

	# READ POINTS
	TOT_POINTS = NUM_POINTS * NUM_CYCLES

	CYCLES_PER_READ = 500
	POINTS_PER_READ = NUM_POINTS * CYCLES_PER_READ

	READ_TIMEOUT = 1000

	numReadPoints = []
	dataPoints = []

	for c in range(0, NUM_CHANNELS):
		numReadPoints.append(0)
		dataPoints.append(np.empty(0, dtype=np.short))

	readDone = False

	print()
	print("Reading data...")

	while readDone == False:
		readDone = True

		for c in range(0, NUM_CHANNELS):
			readPoints = moduleIn.DAQread(c, POINTS_PER_READ, READ_TIMEOUT)

			dataPoints[c] = np.append(dataPoints[c], readPoints)

			numReadPoints[c] += readPoints.size

			readDone = readDone and (numReadPoints[c] >= TOT_POINTS)

	# PLOT
	print()
	print("Generating graph...")

	plt.plot(dataPoints[0], 'r-', dataPoints[1], 'g-', dataPoints[2], 'b-')
	plt.show()

	# RESET AMPLITUDE CHANNEL 3
	moduleOut.channelAmplitude(CHANNEL_TRIG_CONTROL, 0)

	# CLOSE MODULES
	print()
	moduleIn.close()
	print("AIN closed")
	moduleOut.close()
	print("AOU closed")
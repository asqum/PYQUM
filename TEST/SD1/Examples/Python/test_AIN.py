import sys
sys.path.append('C:\Program Files (x86)\Keysight\SD1\Libraries\Python')

import keysightSD1

# MODULE CONSTANTS
PRODUCT = ""
CHASSIS = 1
# change slot number to your value
SLOT = 6

CHANNEL = 0

# CREATE AND OPEN MODULE
module = keysightSD1.SD_AIN()

moduleID = module.openWithSlot(PRODUCT, CHASSIS, SLOT)

if moduleID < 0:
	print("Module open error:", moduleID)
else:
	print("Module opened:", moduleID)
	print("Module name:", module.getProductName())
	print("slot:", module.getSlot())
	print("Chassis:", module.getChassis())
	print()

	# CONFIGURE AND START DAQ
	POINTS_PER_CYCLE = 100
	CYCLES = 500
	TRIGGER_DELAY = 0

	module.DAQconfig(CHANNEL, POINTS_PER_CYCLE, CYCLES, TRIGGER_DELAY, keysightSD1.SD_TriggerModes.SWHVITRIG_CYCLE)
	module.DAQstart(CHANNEL)

	# READ DATA
	TIMEOUT = 1

	dataRead = module.DAQread(CHANNEL, POINTS_PER_CYCLE * CYCLES, TIMEOUT)
	print(dataRead)

	# exiting...
	module.close()
	print()
	print("AIN closed")

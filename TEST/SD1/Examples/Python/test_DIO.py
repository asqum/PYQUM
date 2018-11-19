import sys
sys.path.append('C:\Program Files (x86)\Keysight\SD1\Libraries\Python')

import keysightSD1

# MODULE CONSTANTS
PRODUCT = ""
CHASSIS = 1

# change slot number to your value
SLOT = 3

# CREATE AND OPEN MODULE
module = keysightSD1.SD_DIO()

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
	CYCLES = 1
	TRIGGER_DELAY = 0
	
	module.DAQconfig(CHANNEL, POINTS_PER_CYCLE, CYCLES1, TRIGGER_DELAY, keysightSD1.SD_TriggerModes.AUTOTRIG)
	module.DAQstart(CHANNEL)
	
	# READ DATA
	TIMEOUT = 0

	dataRead = module.DAQread(CHANNEL, POINTS_PER_CYCLE * CYCLES, TIMEOUT)
	print(dataRead)

	# exiting...
	module.close()
	print()
	print("DIO closed")

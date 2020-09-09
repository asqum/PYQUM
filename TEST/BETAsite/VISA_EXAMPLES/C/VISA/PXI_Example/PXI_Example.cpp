////////////////////////////////////////////////////////////////////////////////
// © Keysight Technologies 2016
//
// You have a royalty-free right to use, modify, reproduce and distribute
// the Sample Application Files (and/or any modified version) in any way
// you find useful, provided that you agree that Keysight Technologies has no
// warranty, obligations or liability for any Sample Application Files.
//
////////////////////////////////////////////////////////////////////////////////

#include "stdafx.h"

#include "visa.h"

int main()
{
	
	ViSession resourceManager;
	ViSession session;

	// Change VISA_ADDRESS to a PXI address, e.g. "PXI0::23-0.0::INSTR"	
	ViRsrc VISA_ADDRESS = "Your instrument's VISA address goes here!";

	// Create a connection (session) to the PXI module 
	viOpenDefaultRM(&resourceManager);
	ViStatus error = viOpen(resourceManager, VISA_ADDRESS, VI_NO_LOCK, 0, &session);

	if (error >= VI_SUCCESS)
	{
		ViChar manufacturerName[100];
		ViChar model[100];
		ViInt16 chassis;
		ViInt16 slot;
		ViUInt16 bus;
		ViUInt16 deviceNumber;
		ViUInt16 function;

		viGetAttribute(session, VI_ATTR_MANF_NAME, manufacturerName);
		viGetAttribute(session, VI_ATTR_MODEL_NAME, model);
		viGetAttribute(session, VI_ATTR_PXI_CHASSIS, &chassis);
		viGetAttribute(session, VI_ATTR_SLOT, &slot);
		viGetAttribute(session, VI_ATTR_PXI_BUS_NUM, &bus);
		viGetAttribute(session, VI_ATTR_PXI_DEV_NUM, &deviceNumber);
		viGetAttribute(session, VI_ATTR_PXI_FUNC_NUM, &function);

		printf("Manufacturer: %s\nModel: %s\nChassis: %d\nSlot: %d\nBus-Device.Function: %d-%d.%d\n",
			manufacturerName,
			model,
			chassis,
			slot,
			bus,
			deviceNumber,
			function);

		// Close the connection to the instrument
		viClose(session);

	}
	else
	{
		printf("Couldn't connect to '%s'\n", VISA_ADDRESS);
	}

	// Close the connection to the resource manager
	viClose(resourceManager);

	printf("Press any key to exit...");
	char keyBuffer[100];
	scanf_s("%c", keyBuffer, 100);

	return 0;
}

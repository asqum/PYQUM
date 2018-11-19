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

	// Change VISA_ADDRESS to a serial VISA address, e.g. "ASRL2::INSTR"
	ViRsrc VISA_ADDRESS = "Your instrument's VISA address goes here!";

	// Create a connection (session) to the serial instrument
	viOpenDefaultRM(&resourceManager);
	ViStatus error = viOpen(resourceManager, VISA_ADDRESS, VI_NO_LOCK, 0, &session);

	if (error >= VI_SUCCESS)
	{
		// The first thing you should do with a serial port is enable the Termination Character. Otherwise all of your read's will fail
		viSetAttribute(session, VI_ATTR_TERMCHAR_EN, VI_TRUE);

		// If you've setup the serial port settings in Connection Expert, you can remove this section. 
		// Otherwise, set your connection parameters
		viSetAttribute(session, VI_ATTR_ASRL_BAUD, 9600);
		viSetAttribute(session, VI_ATTR_ASRL_DATA_BITS, 8);
		viSetAttribute(session, VI_ATTR_ASRL_PARITY, VI_ASRL_PAR_NONE);
		viSetAttribute(session, VI_ATTR_ASRL_FLOW_CNTRL, VI_ASRL_FLOW_DTR_DSR);

		// Send the *IDN? and read the response as strings
		viPrintf(session, "*IDN?\n");
		ViChar idnResponse[100];
		viScanf(session, "%t", idnResponse);

		printf("*IDN? returned: %s\n", idnResponse);

		// Close the connection to the instrument
		viClose(session);
	}
	else
	{
		printf("Couldn't connect to '%s'\n", VISA_ADDRESS);
	}

	viClose(resourceManager);

	printf("Press any key to exit...");
	char keyBuffer[100];
	scanf_s("%c", keyBuffer, 100);

	return 0;
}
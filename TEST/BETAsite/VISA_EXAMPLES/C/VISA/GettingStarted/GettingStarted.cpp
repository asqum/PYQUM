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

#include <string>
#include "visa.h"


int main()
{

	// Change this variable to the address of your instrument
	ViRsrc VISA_ADDRESS = "Your instrument's VISA address goes here!";

	// Create a connection (session) to the instrument
	ViSession resourceManager = 0;
	ViSession session = 0;
	ViStatus status = 0;

	status = viOpenDefaultRM(&resourceManager);
	
	if (status < VI_SUCCESS)
	{
		printf("There was a problem opening the default resource manager.\nError code: %d\n", status);
		return 1;
	}

	status = viOpen(resourceManager, VISA_ADDRESS, VI_NO_LOCK, 0, &session);

	if (status < VI_SUCCESS)
	{
		printf("There was a problem opening the connection to the instrument.\nError code: %d\n", status);
		return 1;
	}

	// For Serial and TCP/IP socket connections enable the read Termination Character, or read's will timeout
	ViChar fullAddress[100];
	viGetAttribute(session, VI_ATTR_RSRC_NAME, fullAddress);

	if (strcmp("ASRL", fullAddress) == 0 || strcmp("SOCKET", fullAddress) == 0)
	{
		viSetAttribute(session, VI_ATTR_TERMCHAR_EN, VI_TRUE);
	}

	// Send the *IDN? and read the response as strings
	viPrintf(session, "*IDN?\n");
	ViChar idnResponse[100];
	viScanf(session, "%t", idnResponse);

	printf("*IDN? returned: %s\n", idnResponse);

	// Close the connection to the instrument
	viClose(session);
	viClose(resourceManager);

	printf("Press any key to exit...");
	char keyBuffer[100];
	scanf_s("%c", keyBuffer, 100);

    return 0;
}



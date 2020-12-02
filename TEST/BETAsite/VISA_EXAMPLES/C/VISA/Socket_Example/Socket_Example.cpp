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

	// Change VISA_ADDRESS to a SOCKET address, e.g. "TCPIP::169.254.104.59::5025::SOCKET"
	ViRsrc VISA_ADDRESS = "Your instrument's VISA address goes here!";

	// Create a connection (session) to the TCP/IP socket on the instrument. 	
	viOpenDefaultRM(&resourceManager);
	ViStatus error = viOpen(resourceManager, VISA_ADDRESS, VI_NO_LOCK, 0, &session);

	if (error >= VI_SUCCESS)
	{
		// The first thing you should do with a SOCKET connection is enable the Termination Character. Otherwise all of your read's will fail
		viSetAttribute(session, VI_ATTR_TERMCHAR_EN, VI_TRUE);

		// We can find out details of the connection
		ViChar ipAddress[100];
		ViChar hostname[100];
		ViUInt16 port;
		viGetAttribute(session, VI_ATTR_TCPIP_ADDR, ipAddress);
		viGetAttribute(session, VI_ATTR_TCPIP_HOSTNAME, hostname);
		viGetAttribute(session, VI_ATTR_TCPIP_PORT, &port);

		printf("IP: %s\nHostname: %s\nPort: %d\n",
			ipAddress,
			hostname,
			port);

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


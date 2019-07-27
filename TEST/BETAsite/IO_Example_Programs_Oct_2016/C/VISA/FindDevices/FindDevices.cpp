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

void find(ViString searchString)
{
	ViSession resourceManager;
	ViSession findListSession;
	ViUInt32 foundCount;
	ViChar address[100];

	viOpenDefaultRM(&resourceManager);

	printf("Find with search string \"%s\":\n", searchString);
	viFindRsrc(resourceManager, searchString, &findListSession, &foundCount, address);

	if (foundCount > 0)
	{
		while (foundCount-- > 0)
		{
			printf("\t%s\n", address);

			if (foundCount <= 0)
			{
				viClose(findListSession);
			}
			else
			{
				viFindNext(findListSession, address);
			}
		}
	}
	else
	{
		printf("... didn't find anything!\n");
	}
	
	viClose(resourceManager);
}


int main()
{

	// Finding all devices and interfaces is straightforward
	printf("Find all devices and interfaces:\n");
	find("?*");
	

	// You can specify other device types using different search strings. Here are some common examples:

	// All instruments (no INTFC, BACKPLANE or MEMACC)
	find("?*INSTR");
	// PXI modules
	find("PXI?*INSTR");
	// USB devices
	find("USB?*INSTR");
	// GPIB instruments
	find("GPIB?*");
	// GPIB interfaces
	find("GPIB?*INTFC");
	// GPIB instruments on the GPIB0 interface
	find("GPIB0?*INSTR");
	// LAN instruments
	find("TCPIP?*");
	// SOCKET (::SOCKET) instruments
	find("TCPIP?*SOCKET");
	// VXI-11 (inst) instruments
	find("TCPIP?*inst?*INSTR");
	// HiSLIP (hislip) instruments
	find("TCPIP?*hislip?*INSTR");
	// RS-232 instruments
	find("ASRL?*INSTR");

	printf("Press any key to exit...");
	char keyBuffer[100];
	scanf_s("%c", keyBuffer, 100);

    return 0;
}
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

void errorHandler(ViStatus status, ViSession sessionId)
{
	if (status < VI_SUCCESS)
	{
		printf("An error has occurred!\n");

		// To get more information about the error we can call viStatusDesc
		ViChar errorMessage[256];
		int error = viStatusDesc(sessionId, status, errorMessage);

		if (error >= VI_SUCCESS)
		{
	
			printf("\n\tError code: %d\n\tError description: %s\n",
				status,
				errorMessage);
		}
		else
		{
			printf("\n\tThere was an error getting the description of the original error!\n\tError code: %d\n\tOriginal error code: %d\n",
				error,
				status);
		}
	}
}


int main()
{

	// Change this variable to the address of your instrument
	ViRsrc VISA_ADDRESS = "Your instrument's VISA address goes here!";

	ViSession resourceManager;
	ViSession session;
	viOpenDefaultRM(&resourceManager);

	ViStatus status = 0;
	// Part 1:
	// 
	// Shows the mechanics of how to deal with an error in VISA when it occurs. 
	// To stimulate an error, the code will try to open a connection to an instrument at an invalid address...
	
	// First we'll provide an invalid address and see what error we get 
	status = viOpen(resourceManager, "BAD ADDRESS", VI_NO_LOCK, 0, &session);
	
	if (status < VI_SUCCESS)
	{
		printf("An error has occurred!\n%d\n", status);

		// To get more specific information about the exception, we can check what kind of error it is and add specific error handling code
		// In this example, that is done in the errorHandler method
		errorHandler(status, resourceManager);
	}

	// Part 2:
	// 
	// Stimulate another error by sending an invalid query and trying to read its response. 
	// 
	// Before running this part, don't forget to set your instrument address in the 'VISA_ADDRESS' variable at the top of this method
	status = viOpen(resourceManager, VISA_ADDRESS, VI_NO_LOCK, 0, &session);
	
	// Misspell the *IDN? query as *IND?
	status = viPrintf(session, "*IND?\n");
	
	if (status < VI_SUCCESS)
	{
		printf("You'll never get here, because the *IND? data will get sent to the instrument successfully; it's the instrument that won't like it.\n");
	}

	// Try to read the response (*IND?)
	ViChar idnResponse[100];
	status = viScanf(session, "%t", idnResponse);

	if (status < VI_SUCCESS)
	{
		printf("The scanf call will timeout, because the instrument doesn't know what to do with the command that we sent it.\nError code: %d\n", status);

		// Check the instrument to see if it has any errors in its queue
		ViChar rawError[100];
		int errorCode = -1;
		ViChar errorString[100];

		while (errorCode != 0)
		{
			viPrintf(session, "SYST:ERR?\n");
			viScanf(session, "%t", rawError);
			
			sscanf_s(rawError, "%d, %100[^\n]", &errorCode, errorString, 100);
			printf("Instrument error code: %d, instrument error message: %s\n", errorCode, errorString);
		}
	}

	viClose(session);
	viClose(resourceManager);

	printf("\nPress any key to exit...");
	char keyBuffer[100];
	scanf_s("%c", keyBuffer, 100);

    return 0;
}

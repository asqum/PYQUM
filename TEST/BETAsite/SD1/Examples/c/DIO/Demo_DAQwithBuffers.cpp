#include <stdlib.h>
#include <stdio.h>
// Must include Keysight SD1 programming libraries as global include path. You can use the "KEYSIGHT_SD1_LIBRARY_PATH" system environment variable
#include <include\common\sd_constants.h>
#include <include\c\SD_Module.h>
#include <include\c\SD_DIO.h>

void flushKeys();

int main()
{
	int slot;
	int moduleDIO;
	int nDAQ;
	short *dataBuffer;
	short *readBuffer;
	short *removeBuffer;
	int totalPointsRead = 0;
	int nPointsRead = 0;
	int error = 0;
	int i = 0;

	printf("---- Demo Run DAQ with buffers pool ----\n");
	printf("Enter the Module Slot: ");
	scanf("%d",&slot);
	printf("Enter nDAQ: ");
	scanf("%d",&nDAQ);

	flushKeys();

	// Open module with slot
	moduleDIO = SD_Module_openWithSlot("SD-PXE-DIO",0,slot);						
	
	if(moduleDIO<=0)
	{
		printf("Error opening module\n");
		getchar();
		return 1;
	}

	// Config the Input Bus 0 pins 0 to 15 of Port 0 
	SD_DIO_busConfig(moduleDIO, 1000, 0, 0, 15);

	// Stop DAQ
	SD_DIO_DAQstop(moduleDIO, nDAQ);

	// Flush DAQ
	SD_DIO_DAQflush(moduleDIO, nDAQ);

	// Config DAQ with two cycles of 40 points
	SD_DIO_DAQconfig(moduleDIO, nDAQ, 40, 2, 1, VIHVITRIG);

	// Config DAQ Bufers Pool without Callback
	dataBuffer = (short *)malloc(100*sizeof(short)); 
	SD_DIO_DAQbufferPoolConfig(moduleDIO, nDAQ, dataBuffer, 40, 5000);

	dataBuffer = (short *)malloc(100*sizeof(short)); 
	SD_DIO_DAQbufferAdd(moduleDIO, nDAQ, dataBuffer, 40);  

	printf("Module configuration successfull. Press any key to start the DAQ.");
	getchar();

	// Start DAQ
	SD_DIO_DAQstart(moduleDIO, nDAQ);
	
	printf("DAQ started. Waiting for trigger for fist cycles. Press any key to send a VI/HVI trigger.");
	getchar();

	// Send VI/HVI trigger
	SD_DIO_DAQtrigger(moduleDIO, nDAQ);

	// Waiting for 40 points (first cycle)
	while(SD_DIO_DAQcounterRead(moduleDIO, nDAQ)<40);

	printf("DAQ has acquired %d points.",SD_DIO_DAQcounterRead(moduleDIO, nDAQ));
	getchar();

	printf("Waiting for another trigger for second cycles. Press any key to send a VI/HVI trigger.");
	getchar();

	// Send VI/HVI trigger
	SD_DIO_DAQtrigger(moduleDIO, nDAQ);

	// Waiting for 40 points (second cycle)
	while(SD_DIO_DAQcounterRead(moduleDIO, nDAQ)<80);

	printf("DAQ has acquired %d points. Press any key to continue.",SD_DIO_DAQcounterRead(moduleDIO, nDAQ));;
	getchar();

	// Read data
	while(totalPointsRead<80)
	{
		dataBuffer = SD_DIO_DAQbufferGet(moduleDIO, nDAQ, nPointsRead, error);
		printf("Points Read : %d \n", nPointsRead);
		printf("error : %d \n", error);
		printf("Data Buffer: \n");
		for(i = 0; i<nPointsRead; i++)
			printf("\tData[%d] : %u \n", i, dataBuffer[i]);

		totalPointsRead = totalPointsRead + nPointsRead;
		printf("Total Points read : %d \n", totalPointsRead);
	}

	printf("Press any key to finish.");
	getchar();

	// Free all objects and buffers
	SD_DIO_DAQbufferPoolRelease(moduleDIO, nDAQ);
	while((removeBuffer = SD_DIO_DAQbufferRemove(moduleDIO, nDAQ)) != 0)
		free(removeBuffer);
	SD_Module_close(moduleDIO);

    return 0;
}

void flushKeys()
{
	char ch;
	while ((ch = getchar()) != '\n' && ch != EOF);
}
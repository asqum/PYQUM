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
	short dataBuffer[100];
	int pointsRead = 0;
	int i = 0;

	printf("---- Demo Run DAQ without Buffers ----\n");
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

	// Config DAQ with two cycles of 40 points
	SD_DIO_DAQconfig(moduleDIO, nDAQ, 40, 2, 1, VIHVITRIG); 

	// Flush DAQ
	SD_DIO_DAQflush(moduleDIO, nDAQ);

	printf("Module configuration successfull. Press any key to start the DAQ.");
	getchar();

	// Start DAQ
	SD_DIO_DAQstart(moduleDIO, nDAQ);

	printf("DAQ started. Waiting for first cycle's trigger. Press any key to send a VI/HVI trigger.");
	getchar();

	// Send VI/HVI trigger
	SD_DIO_DAQtrigger(moduleDIO, nDAQ);

	// Waiting for 40 points
	while(SD_DIO_DAQcounterRead(moduleDIO, nDAQ) < 40);

	printf("DAQ has acquired %d points.",SD_DIO_DAQcounterRead(moduleDIO, nDAQ));
	getchar();

	printf("Press any key to send another trigger. Press any key to send a VI/HVI trigger.");
	getchar();

	// Send VI/HVI trigger
	SD_DIO_DAQtrigger(moduleDIO, nDAQ);

	// Waiting for 80 points
	while(SD_DIO_DAQcounterRead(moduleDIO, nDAQ)<80);

	printf("DAQ has acquired %d points.",SD_DIO_DAQcounterRead(moduleDIO, nDAQ));
	getchar();

	// Read data of frist cycle
	pointsRead = SD_DIO_DAQread(moduleDIO, nDAQ, dataBuffer, 40, 0);
	printf("PointsRead : %d \n",pointsRead);
	getchar();

	printf("Data of frist cycle\n");
	for(i = 0; i < 40; i++)
		printf("Data[%d]: %d \n", i, dataBuffer[i]);

	printf("Press any key to continue.");
	getchar();
	
	// Read data of second cycle
	SD_DIO_DAQread(moduleDIO, nDAQ, dataBuffer, 40, 0);

	printf("Data of second cycle\n");
	for(i = 0; i < 40; i++)
		printf("Data[%d]: %d \n", i, dataBuffer[i]);
	getchar();

	// Stop DAQ
	SD_DIO_DAQstop(moduleDIO, nDAQ);

	printf("Press any key to finish.");
	getchar();

	// Free all objects
	SD_Module_close(moduleDIO);

    return 0;
}

void flushKeys()
{
	char ch;
	while ((ch = getchar()) != '\n' && ch != EOF);
}
#include <stdlib.h>
#include <stdio.h>
// Must include Keysight SD1 programming libraries as global include path. You can use the "KEYSIGHT_SD1_LIBRARY_PATH" system environment variable
#include <include\common\sd_constants.h>
#include <include\c\SD_Module.h>
#include <include\c\SD_TDC.h>

void flushKeys();

int main()
{
	int slot;
	int moduleTDC;
	int nDAQ;
	unsigned long long dataBuffer[100];
	int pointsRead = 0;
	int i = 0;

	printf("---- Demo Run DAQ without Buffers ----\n");
	printf("Enter the Module Slot: ");
	scanf("%d",&slot);
	printf("Enter nDAQ: ");
	scanf("%d",&nDAQ);

	flushKeys();

	// Open module with slot
	moduleTDC = SD_Module_openWithSlot("SD-PXE-TDC",0,slot);						
	
	if(moduleTDC<=0)
	{
		printf("Error opening module\n");
		getchar();
		return 1;
	}

	// Config DAQ with two cycles of 16 points
	SD_TDC_DAQconfig(moduleTDC, nDAQ, 16, 2, 1, VIHVITRIG); 

	// Flush DAQ
	SD_TDC_DAQflush(moduleTDC, nDAQ);

	printf("Module configuration successfull. Press any key to start the DAQ.");
	getchar();

	// Start DAQ
	SD_TDC_DAQstart(moduleTDC, nDAQ);

	printf("DAQ started. Waiting for first cycle's trigger. Press any key to send a VI/HVI trigger.");
	getchar();

	// Send VI/HVI trigger
	SD_TDC_DAQtrigger(moduleTDC, nDAQ);

	// Waiting for 16 points
	while(SD_TDC_DAQcounterRead(moduleTDC, nDAQ)<16);

	printf("DAQ has acquired %d points.",SD_TDC_DAQcounterRead(moduleTDC, nDAQ));
	getchar();

	printf("Press any key to send another trigger. Press any key to send a VI/HVI trigger.");
	getchar();

	// Send VI/HVI trigger
	SD_TDC_DAQtrigger(moduleTDC, nDAQ);

	// Waiting for 32 points
	while(SD_TDC_DAQcounterRead(moduleTDC, nDAQ)<32);

	printf("DAQ has acquired %d points.",SD_TDC_DAQcounterRead(moduleTDC, nDAQ));
	getchar();

	// Read data of frist cycle
	pointsRead = SD_TDC_DAQread(moduleTDC, nDAQ, dataBuffer, 16, 0);
	printf("Points read : %d\n", pointsRead);
	getchar();

	printf("Data of frist cycle\n");
	for(i = 0; i<pointsRead; i++)
		printf("Data[%d]: %lld \n", i, dataBuffer[i]);
	getchar();

	// Read data of frist cycle
	pointsRead = SD_TDC_DAQread(moduleTDC, nDAQ, dataBuffer, 16, 0);
	printf("Points read : %d\n", pointsRead);
	getchar();

	printf("Data of second cycle\n");
	for(i = 0; i<pointsRead; i++)
		printf("Data[%d]: %lld \n", i, dataBuffer[i]);
	getchar();

	// Stop DAQ
	SD_TDC_DAQstop(moduleTDC, nDAQ);

	printf("Press any key to finish.");
	getchar();

	// Free all objects
	SD_Module_close(moduleTDC);

    return 0;
}

void flushKeys()
{
	char ch;
	while ((ch = getchar()) != '\n' && ch != EOF);
}
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
	unsigned long long dataPrev=0;
	unsigned long long *dataBuffer;
	unsigned long long *readBuffer;
	unsigned long long *removeBuffer;
	int totalPointsRead = 0;
	int nPointsRead = 0;
	int error = 0;
	int i = 0;

	printf("---- Demo Run DAQ with Buffers ----\n");
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

	// Stop DAQ
	SD_TDC_DAQstop(moduleTDC, nDAQ);

	// Flush DAQ
	SD_TDC_DAQflush(moduleTDC, nDAQ);

	// Config DAQ with two cycles of 16 points
	SD_TDC_DAQconfig(moduleTDC, nDAQ, 16, 2, 1, VIHVITRIG);

	// Config DAQ Buffers Pool with Callback
	dataBuffer = (unsigned long long *)malloc(16*sizeof(unsigned long long)); 
	SD_TDC_DAQbufferPoolConfig(moduleTDC, nDAQ, dataBuffer, 16, 1000);

	// Add other buffer
	dataBuffer = (unsigned long long *)malloc(16*sizeof(unsigned long long)); 
	SD_TDC_DAQbufferAdd(moduleTDC, nDAQ, dataBuffer, 16);  

	printf("Module configuration successfull. Press any key to start the DAQ.");
	getchar();

	// Start DAQ
	SD_TDC_DAQstart(moduleTDC, nDAQ);
	
	printf("DAQ started. Waiting for trigger for first cycles. Press any key to send a VI/HVI trigger.");
	getchar();

	// Send VI/HVI trigger
	SD_TDC_DAQtrigger(moduleTDC, nDAQ);

	// Waiting for 16 points (first cycle)
	while(SD_TDC_DAQcounterRead(moduleTDC, nDAQ)<16);

	printf("DAQ has acquired %d points.",SD_TDC_DAQcounterRead(moduleTDC, nDAQ));
	getchar();

	printf("Waiting for another trigger for second cycles. Press any key to send a VI/HVI trigger.");
	getchar();

	// Send VI/HVI trigger
	SD_TDC_DAQtrigger(moduleTDC, nDAQ);

	// Waiting for 16 points (second cycle)
	while(SD_TDC_DAQcounterRead(moduleTDC, nDAQ)<32);

	printf("DAQ has acquired %d points.",SD_TDC_DAQcounterRead(moduleTDC, nDAQ));;
	getchar();

	// Read data
	while(totalPointsRead<32)
	{
		dataBuffer = SD_TDC_DAQbufferGet(moduleTDC, nDAQ, nPointsRead, error);
		printf("Points Read : %d \n", nPointsRead);
		printf("error : %d \n", error);
		printf("Data Buffer: \n");
		for(i = 0; i<nPointsRead; i++)
		{
			printf("\tData[%d] : %lld ps : difference = %lld ps\n", i+totalPointsRead, dataBuffer[i], dataBuffer[i]-dataPrev);
			dataPrev = dataBuffer[i];
		}

		totalPointsRead = totalPointsRead + nPointsRead;
		printf("Total Points read : %d \n", totalPointsRead);
	}

	printf("Press any key to finish.");
	getchar();

	// Free all objects and buffers
	SD_TDC_DAQbufferPoolRelease(moduleTDC, nDAQ);
	while((removeBuffer = SD_TDC_DAQbufferRemove(moduleTDC, nDAQ)) != 0)
		free(removeBuffer);
	SD_Module_close(moduleTDC);

    return 0;
}

void flushKeys()
{
	char ch;
	while ((ch = getchar()) != '\n' && ch != EOF);
}
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
	int nChannel;
	int rateCount;

	printf("---- Demo Read rateCounter ----\n");
	printf("Enter the Module Slot: ");
	scanf("%d",&slot);
	printf("Enter nChannel: ");
	scanf("%d",&nChannel);

	flushKeys();

	// Open module with slot
	moduleTDC = SD_Module_openWithSlot("SD-PXE-TDC",0,slot);						
	
	if(moduleTDC<=0)
	{
		printf("Error opening module\n");
		getchar();
		return 1;
	}

	// Config channel with 0V of threshold and rising edge
	SD_TDC_thresholdConfig(moduleTDC, nChannel, 0);
	SD_TDC_edgeConfig(moduleTDC, nChannel, TDC_RISING_EDGE);	

	// Set counter rate in 1s
	SD_TDC_rateCounterConfig(moduleTDC, nChannel, 1000000);		// 1s
	rateCount = SD_TDC_rateCounterRead(moduleTDC, nChannel);

	printf(" Rate Couter is : %d Counts/s\n",rateCount);

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
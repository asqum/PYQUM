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
	int nChannel1;
	int nChannel2;
	int rateCount;
	int bufferHistograma[1000];
	int i, maxBin, maxValue;
	long long totalValue;
	double noise;

	printf("---- Demo Histogram ----\n");
	printf("Enter the Module Slot: ");
	scanf("%d",&slot);
	printf("Enter start Channel: ");
	scanf("%d",&nChannel1);
	printf("Enter stop Channel1: ");
	scanf("%d",&nChannel2);

	flushKeys();

	// Open module with slot
	moduleTDC = SD_Module_openWithSlot("SD-PXE-TDC",0,slot);						
	
	if(moduleTDC<=0)
	{
		printf("Error opening module\n");
		getchar();
		return 1;
	}
	
	// Config Histogram with windown size of 160ns and offset 0
	SD_TDC_histogramConfig(moduleTDC, 0, nChannel1, nChannel2, 0, 500, 0); // BinSize = 320ps 
	
	printf("Module configuration successfull. Press any key to start the Histogram.");
	getchar();

	SD_TDC_histogramStart(moduleTDC, 0);

	printf("Press any key to pause.");
	getchar();

	SD_TDC_histogramPause(moduleTDC, 0);

	printf("Press any key to resume.");
	getchar();

	SD_TDC_histogramResume(moduleTDC, 0);

	printf("Press any key to stop.");
	getchar();

	SD_TDC_histogramStop(moduleTDC, 0);

	// Read Histogram data
	SD_TDC_histogramRead(moduleTDC, 0, 0, 500, bufferHistograma);

	SD_TDC_histogramFlush(moduleTDC, 0);

	printf("Histogram data acquired: \n\n");

	maxBin = -1;
	maxValue = -1;
	totalValue = 0;
	// Show Histogram data
	for(i=0;i<500;i++)
	{
		printf(" Bin: %d Time: %.3f ns - Value of bin: %d\n", i, (i*320.0)/1000.0, bufferHistograma[i]);
		if((i % 100)==99)
		{
			printf("\nPress any key to continue.");
			getchar();
		}
		if(bufferHistograma[i] > maxValue)
		{
			maxValue = bufferHistograma[i];
			maxBin = i;
		}
		totalValue += bufferHistograma[i];
	}

	printf("\nMax Bin : %d - Time : %.3f ns\n", maxBin, (maxBin*320.0)/1000.0);
	printf("Max Value : %u\n", maxValue);
	noise = (totalValue - maxValue)/(500.0-1);
	printf("Noise : %.3f\n", noise);
	printf("SNR : %.3f\n", maxValue / noise);

	printf("\nPress any key to finish.");
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
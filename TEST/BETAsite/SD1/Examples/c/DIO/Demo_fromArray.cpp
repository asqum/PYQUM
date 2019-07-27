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
	int nDWG;
	int error = 0;

	printf("---- Demo Run DWG from Array----\n");
	printf("Enter the Module Slot: ");
	scanf("%d",&slot);
	printf("Enter nDWG/nPort: ");
	scanf("%d",&nDWG);

	flushKeys();

	// Open module with slot
	moduleDIO = SD_Module_openWithSlot("SD-PXE-DIO",0,slot);						
	
	if(moduleDIO<=0)
	{
		printf("Error opening module\n");
		getchar();
		return 1;
	}

	// Config the Output Bus selected in pins 0 to 15 of Port selected 
	SD_DIO_busConfig(moduleDIO, 2000 + nDWG, nDWG, 0, 15);

	//Config all pins of both ports as output
	SD_DIO_IOdirectionConfig(moduleDIO, 0xFFFFFFFFFFFFFFFF, DIR_OUT);

	// Erase all waveforms from module memory
    SD_DIO_waveformFlush(moduleDIO);

	printf("Module configuration successfull. Press any key to start the DWG.");
	getchar();

	//Load waveforms from Array with prestaler 1 (100MSPS) and infinite cycles
	int points[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32};
    error = SD_DIO_DWGfromArray(moduleDIO, nDWG, AUTOTRIG, 0, 0, 1, WAVE_DIGITAL, 32, points);
	if (error < 0)
	{
		printf("Error in AWG function");
		exit(1);
	}

	printf("Press any key to stop the DWG.");
	getchar();

    SD_DIO_DWGstop(moduleDIO,nDWG);

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
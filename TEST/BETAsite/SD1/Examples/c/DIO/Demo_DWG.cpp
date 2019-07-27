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

	printf("---- Demo DWG function from file ----\n");
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

	// Config the Output Bus 0 in pins 0 to 15 of Port 0 
	SD_DIO_busConfig(moduleDIO, 2000 + nDWG, nDWG, 0, 15);

	//Config all pins of both ports as output
	SD_DIO_IOdirectionConfig(moduleDIO, 0xFFFFFFFFFFFFFFFF, DIR_OUT);
	
	//Load waveforms from Array with prestaler 1 (100MSPS) and one cycles
	SD_DIO_DWGfromFile(moduleDIO, nDWG, "W:\\Waveforms_Demo\\Alberto\\DigitalTest_32samples.txt", AUTOTRIG, 0, 1, 1);

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
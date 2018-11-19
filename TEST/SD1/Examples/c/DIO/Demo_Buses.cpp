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
	int moduleDIO, nbus; 
	int error, i, dataAux;

	printf("---- Demo Buses ----\n");
	printf("Enter the Module Slot: ");
	scanf("%d",&slot);
	printf("Enter the nBus/nPort: ");
	scanf("%d",&nbus);

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
	SD_DIO_busConfig(moduleDIO, 2000 + nbus, nbus, 0, 15);

	// Config the Input Bus selected in pins 0 to 15 of Port selected 
	SD_DIO_busConfig(moduleDIO, 1000 + nbus, nbus, 1, 15);

	//Config all pins as output
	SD_DIO_IOdirectionConfig(moduleDIO, 0xFFFFFFFFFFFFFFFF, DIR_OUT);

	printf("Module configuration successfull. Press any key to set the trigger.");
	getchar();

	dataAux = 32768;

	while(dataAux > 0)
	{
		error = SD_DIO_busWrite(moduleDIO, 2000 + nbus, dataAux);
		if (error < 0)
			exit(1);
		
		printf("Write data in OutputBus 0\n");

		dataAux = SD_DIO_busRead( moduleDIO, 1000 + nbus, error);
		if (error < 0)
			exit(1);

		printf("Read data in InputBus 0 : %u", dataAux);
		flushKeys();
	}

	// Free all objects
	SD_Module_close(moduleDIO);

    return 0;
}

void flushKeys()
{
	char ch;
	while ((ch = getchar()) != '\n' && ch != EOF);
}
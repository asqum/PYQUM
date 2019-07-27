#include <stdlib.h>
#include <stdio.h>
// Must include Keysight SD1 programming libraries as global include path. You can use the "KEYSIGHT_SD1_LIBRARY_PATH" system environment variable
#include <include\common\sd_constants.h>
#include <include\c\SD_Module.h>
#include <include\c\SD_DIO.h>
#include <include\c\SD_WAVE.h>


void flushKeys();

int main()
{
	int slot;
	int moduleDIO;
	int nChannel;

	printf("---- Demo DWG with strobe out and trigger ----\n");
	printf("Enter the Module Slot: ");
	scanf("%d",&slot);
	printf("Enter nDWG: ");
	scanf("%d",&nChannel);

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
	SD_DIO_busConfig(moduleDIO, 2000, 0, 0, 15);

	// Config the Strobe 0 
	SD_DIO_busSamplingConfig(moduleDIO, 2000, 0, STROBE_ON, STROBE_EDGERISE, 0);

	//Config pins 0 to 15 of Port 0 as output
	SD_DIO_IOdirectionConfig(moduleDIO, 0x000000000000FFFF, DIR_OUT);

	// Create waveforms objects in PC RAM from waveforms files
	int waveId1 = SD_Wave_newFromFile("W:\\Waveforms_Demo\\Alberto\\DigitalTest_32samples.txt");
	int waveId2 = SD_Wave_newFromFile("W:\\Waveforms_Demo\\Alberto\\DigitalTest_48samples.txt");
	int nWave1 = 0;
	int nWave2 = 1;

	if(waveId1<0 || waveId1<0)
	{
		printf("Error opening waveform File\n");
		getchar();

		// Free all objects
		SD_Wave_delete(waveId1);
		SD_Wave_delete(waveId2);
		SD_Module_close(moduleDIO);
		
		return 1;
	}

	// Erase all waveforms from module memory and load waveforms waveId1 and waveId2 in position nWave1 and nWave2
    SD_DIO_waveformFlush(moduleDIO);
    SD_DIO_waveformLoad(moduleDIO,waveId1,nWave1);
    SD_DIO_waveformLoad(moduleDIO,waveId2,nWave2);

	// Flush channel waveform queue
	SD_DIO_DWGflush(moduleDIO,nChannel);

	// Queue waveforms nWave1 and nWave2 in nChannel
    SD_DIO_DWGqueueWaveform(moduleDIO,nChannel,nWave1,AUTOTRIG,0,1,1); 
    SD_DIO_DWGqueueWaveform(moduleDIO,nChannel,nWave2,VIHVITRIG,0,1,1);

	printf("Module configuration successfull. Press any key to start the DWG.");
	getchar();

    SD_DIO_DWGstart(moduleDIO,nChannel);

    printf("DWG started. Press any key to send a VI/HVI trigger.");
	getchar();

	SD_DIO_DWGtrigger(moduleDIO,nChannel);

	printf("Press any key to stop the DWG.");
	getchar();

    SD_DIO_DWGstop(moduleDIO,nChannel);

	printf("DWG Stopped. Press any key to finish.");
	getchar();

	// Free all objects
	SD_Wave_delete(waveId1);
	SD_Wave_delete(waveId2);
	SD_Module_close(moduleDIO);

    return 0;
}

void flushKeys()
{
	char ch;
	while ((ch = getchar()) != '\n' && ch != EOF);
}
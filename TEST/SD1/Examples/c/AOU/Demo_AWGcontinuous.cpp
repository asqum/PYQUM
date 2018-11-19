#include <stdlib.h>
#include <stdio.h>
// Must include Keysight SD1 programming libraries as global include path. You can use the "KEYSIGHT_SD1_LIBRARY_PATH" system environment variable
#include <include\common\sd_constants.h>
#include <include\c\SD_Module.h>
#include <include\c\SD_AOU.h>
#include <include\c\SD_WAVE.h>


void flushKeys();

int main()
{
	int slot;
	int moduleAOU;
	int nChannel;

	printf("---- Demo Run a single waveform continuously ----\n");
	printf("Enter the Module Slot: ");
	scanf("%d",&slot);
	printf("Enter Channel: ");
	scanf("%d",&nChannel);

	flushKeys();

	// Open module with slot
	moduleAOU = SD_Module_openWithSlot("SD-PXE-AOU",0,slot);						
	
	if(moduleAOU<=0)
	{
		printf("Error opening module\n");
		return 1;
	}

	// Create a waveform object in PC RAM from waveform file
	int waveID = SD_Wave_newFromFile("Triangular.csv");
	int nWave = 0;

	if(waveID<0)
	{
		printf("Error opening waveform File\n");
		getchar();

		// Free all objects
		SD_Wave_delete(waveID);
		SD_Module_close(moduleAOU);
		
	}

	// Switch off angle modulation and Amplitude modulation
	SD_AOU_modulationAngleConfig(moduleAOU,nChannel,AOU_MOD_OFF,0);	
	SD_AOU_modulationAmplitudeConfig(moduleAOU,nChannel,AOU_MOD_OFF,0);

	// Erase all waveforms from module memory and load the waveform waveID in position nWave
	SD_AOU_waveformFlush(moduleAOU);
	SD_AOU_waveformLoad(moduleAOU, waveID, nWave);

	// Config amplitude and setup AWG in nChannel
    SD_AOU_channelAmplitude(moduleAOU,nChannel,1.2);					// 1.2 Volts Peak
    SD_AOU_channelWaveShape(moduleAOU,nChannel,AOU_AWG);

	// Flush channel waveform queue
	SD_AOU_AWGflush(moduleAOU,nChannel);

	// Queue waveform nWave in nChannel
	SD_AOU_AWGqueueWaveform(moduleAOU,nChannel,nWave,AUTOTRIG,0,0,0);	// Cycles = 0

	printf("Module configuration successfull. Press any key to start the AWG");
	getchar();

    SD_AOU_AWGstart(moduleAOU,nChannel);

    printf("AWG started. Press any key to pause the AWG.");
	getchar();
 
    SD_AOU_AWGpause(moduleAOU,nChannel);

    printf("AWG paused. Press any key to resume the AWG.");
	getchar();

    SD_AOU_AWGresume(moduleAOU,nChannel);

    printf("AWG resumed. Press any key to stop the AWG.");
	getchar();

    SD_AOU_AWGstop(moduleAOU,nChannel);

    printf("AWG stopped. Press any key to start the AWG.");
	getchar(); 

	SD_AOU_AWGstart(moduleAOU,nChannel);

    printf("AWG started. Press any key to stop the AWG.");
	getchar(); 

	SD_AOU_AWGstop(moduleAOU,nChannel);

	printf("AWG Stopped. Press any key to finish.");
	getchar();

	// Free all objects
	SD_Wave_delete(waveID);
	SD_Module_close(moduleAOU);
		
    return 0;
}

void flushKeys()
{
	char ch;
	while ((ch = getchar()) != '\n' && ch != EOF);
} 
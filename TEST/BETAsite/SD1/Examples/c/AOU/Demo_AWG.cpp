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

	printf("---- Demo Run waveforms ----\n");
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
		getchar();
		return 1;
	}

	// Create waveforms objects in PC RAM from waveforms files
	int waveId1 = SD_Wave_newFromFile("Triangular.csv");
	int waveId2 = SD_Wave_newFromFile("Gaussian.csv");
	int nWave1 = 0;
	int nWave2 = 1;

	if(waveId1<0 || waveId1<0)
	{
		printf("Error opening waveform File\n");
		getchar();

		// Free all objects
		SD_Wave_delete(waveId1);
		SD_Wave_delete(waveId2);
		SD_Module_close(moduleAOU);
		
		return 1;
	}

	// Erase all waveforms from module memory and load waveforms waveId1 and waveId2 in position nWave1 and nWave2
    SD_AOU_waveformFlush(moduleAOU);
    SD_AOU_waveformLoad(moduleAOU,waveId1,nWave1);
    SD_AOU_waveformLoad(moduleAOU,waveId2,nWave2);

	// Turn off nChannel
	SD_AOU_channelWaveShape(moduleAOU,nChannel,AOU_OFF);

	// Switch off angle modulation and Amplitude modulation
	SD_AOU_modulationAngleConfig(moduleAOU,nChannel,AOU_MOD_OFF,0);	
	SD_AOU_modulationAmplitudeConfig(moduleAOU,nChannel,AOU_MOD_OFF,0);		

	// Config amplitude and setup AWG in nChannel
    SD_AOU_channelAmplitude(moduleAOU,nChannel,1.2);			// 1.2 Volts Peak
    SD_AOU_channelWaveShape(moduleAOU,nChannel,AOU_AWG);

	// Flush channel waveform queue
	SD_AOU_AWGflush(moduleAOU,nChannel);

	// Queue waveforms nWave1 and nWave2 in nChannel
    SD_AOU_AWGqueueWaveform(moduleAOU,nChannel,nWave1,AUTOTRIG,0,1,0); 
    SD_AOU_AWGqueueWaveform(moduleAOU,nChannel,nWave2,AUTOTRIG,0,1,0);

	printf("Module configuration successfull. Press any key to start the AWG");
	getchar();

    SD_AOU_AWGstart(moduleAOU,nChannel);

    printf("AWG started. Press any key to stop the AWG.");
	getchar();

    SD_AOU_AWGstop(moduleAOU,nChannel);

	printf("AWG Stopped. Press any key to finish.");
	getchar();

	// Free all objects
	SD_Wave_delete(waveId1);
	SD_Wave_delete(waveId2);
	SD_Module_close(moduleAOU);

    return 0;
}

void flushKeys()
{
	char ch;
	while ((ch = getchar()) != '\n' && ch != EOF);
}
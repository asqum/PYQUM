#include <stdlib.h>
#include <stdio.h>
// Must include Keysight SD1 programming libraries as global include path. You can use the "KEYSIGHT_SD1_LIBRARY_PATH" system environment variable
#include <include\common\sd_constants.h>
#include <include\c\SD_Module.h>
#include <include\c\SD_AOU.h>



void flushKeys();

int main()
{
	int slot;
	int moduleAOU;
	int nChannel;

	printf("---- Demo Run multiples waveforms ----\n");
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

	// Switch off angle modulation and Amplitude modulation
	SD_AOU_modulationAngleConfig(moduleAOU,nChannel,AOU_MOD_OFF,0);	
	SD_AOU_modulationAmplitudeConfig(moduleAOU,nChannel,AOU_MOD_OFF,0);

	// Config amplitude, frequency, phase, offset and shape
    SD_AOU_channelWaveShape(moduleAOU,nChannel,AOU_OFF);
    SD_AOU_channelAmplitude(moduleAOU,nChannel,1.0);				// 1.0 Volts Peak
    SD_AOU_channelFrequency(moduleAOU,nChannel,10E3);				// 10 kHz
    SD_AOU_channelOffset(moduleAOU,nChannel,0.0);					// 0.0 Volts
    SD_AOU_channelPhase(moduleAOU,nChannel,0);						// 0º degrees

	printf("Module configuration successfull. Press any key to start the waveforms.");
	getchar();

    SD_AOU_channelWaveShape(moduleAOU,nChannel,AOU_SINUSOIDAL);

	printf("Waveform started. Press any key to continue.");
	getchar();

    SD_AOU_channelWaveShape(moduleAOU,nChannel,AOU_TRIANGULAR);

    printf("Waveform started. Press any key to continue.");
	getchar();

    SD_AOU_channelWaveShape(moduleAOU,nChannel,AOU_SQUARE);

	printf("Waveform started. Press any key to finish.");
	getchar();

	// Free all objects
	SD_Module_close(moduleAOU);

    return 0;
}

void flushKeys()
{
	char ch;
	while ((ch = getchar()) != '\n' && ch != EOF);
}
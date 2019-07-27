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
	int channelA;
	int channelB; 

	printf("---- Demo Run two waves with different phase ----\n");
	printf("Enter the Module Slot: ");
	scanf("%d",&slot);
	printf("Enter Channel A: ");
	scanf("%d",&channelA);
	printf("Enter Channel B: ");
	scanf("%d",&channelB);

	flushKeys();

	// Open module with slot
	moduleAOU = SD_Module_openWithSlot("SD-PXE-AOU",0,slot);						
		
	if(moduleAOU<=0)
	{
		printf("Error opening module\n");
		return 1;
	}

	// Switch off angle and amplitude modulation
	SD_AOU_modulationAngleConfig(moduleAOU,channelA,AOU_MOD_OFF,0);	
	SD_AOU_modulationAmplitudeConfig(moduleAOU,channelA,AOU_MOD_OFF,0);
	SD_AOU_modulationAngleConfig(moduleAOU,channelB,AOU_MOD_OFF,0);	
	SD_AOU_modulationAmplitudeConfig(moduleAOU,channelB,AOU_MOD_OFF,0);
	
	// Turn off Channels
    SD_AOU_channelWaveShape(moduleAOU,channelA,AOU_OFF);
	SD_AOU_channelWaveShape(moduleAOU,channelB,AOU_OFF);

	// Config amplitude, frequency, phase, offset and shape of channel A
    SD_AOU_channelAmplitude(moduleAOU,channelA,1.0);          // 1.0 Volts Peak
    SD_AOU_channelFrequency(moduleAOU,channelA,10000);        // 10 kHz
    SD_AOU_channelOffset(moduleAOU,channelA,0.0);             // 0 Volts
    SD_AOU_channelPhase(moduleAOU,channelA,0);                // 0º degrees

	// Config amplitude, frequency, phase, offset and shape of channel B
    SD_AOU_channelAmplitude(moduleAOU,channelB,1.0);          // 1.0 Volts Peak
    SD_AOU_channelFrequency(moduleAOU,channelB,10000);        // 10 kHz
    SD_AOU_channelOffset(moduleAOU,channelB,0.0);             // 0 Volts
    SD_AOU_channelPhase(moduleAOU,channelB,0);				  // 0º degrees
 
	// Reset the phase in both channels to synchronize
    SD_AOU_channelPhaseResetMultiple(moduleAOU,(1<<channelA) | (1<<channelB));

	printf("Module configuration successfull. Press any key to start the waveforms.");
	getchar();

	// Turn on Channels
    SD_AOU_channelWaveShape(moduleAOU,channelA,AOU_SINUSOIDAL);
    SD_AOU_channelWaveShape(moduleAOU,channelB,AOU_SINUSOIDAL);

	printf("Waveforms started. Press any key to set 90 degrees phase offset.");
	getchar();
	
	// Config phase in channel B 
	SD_AOU_channelPhase(moduleAOU,channelB,90);				// 90º degrees

	printf("Press any key to change the phase offset to 180 degrees.");
	getchar();

	// Config phase in channel B 
	SD_AOU_channelPhase(moduleAOU,channelB,180);			// 180º degrees

	printf("Press any key to finish.");
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

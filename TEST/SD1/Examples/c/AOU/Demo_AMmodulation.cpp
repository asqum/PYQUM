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

	printf("---- AM modulation ----\n");
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

	// Create a waveform object in PC RAM from waveform file
	int waveID = SD_Wave_newFromFile("Gaussian.csv");
	int nWave = 0; 

	if(waveID<0)
	{
		printf("Error opening waveform File\n");
		getchar();

		// Free all objects
		SD_Wave_delete(waveID);
		SD_Module_close(moduleAOU);
		
		return 1;
	}

	// Erase all waveforms from module memory and load the waveform waveID in position nWave
	SD_AOU_waveformFlush(moduleAOU);
	SD_AOU_waveformLoad(moduleAOU, waveID, nWave);

	// Turn off nChannel
	SD_AOU_channelWaveShape(moduleAOU,nChannel,AOU_OFF);	
 
	// Switch off angle modulation and setup AM modulation
	SD_AOU_modulationAngleConfig(moduleAOU,nChannel,AOU_MOD_OFF,0);	
	SD_AOU_modulationAmplitudeConfig(moduleAOU,nChannel,AOU_MOD_AM,1);		// Deviation Gain = 1

	// Config carrier amplitude, frequency and shape
	SD_AOU_channelAmplitude(moduleAOU,nChannel,0);							// 0 Volts Peak
	SD_AOU_channelFrequency(moduleAOU,nChannel,10E6);	 					// 10 MHz
	SD_AOU_channelWaveShape(moduleAOU,nChannel,AOU_SINUSOIDAL);	
 
	// Flush channel waveform queue
	SD_AOU_AWGflush(moduleAOU,nChannel);

	// Queue waveform nWave in nChannel
	SD_AOU_AWGqueueWaveform(moduleAOU,nChannel,nWave,AUTOTRIG,0,1,1);			

	printf("Module configuration successfull. Press any key to start the AWG");
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
#include <stdlib.h>
#include <stdio.h>
// Must include Keysight SD1 programming libraries as global include path. You can use the "KEYSIGHT_SD1_LIBRARY_PATH" system environment variable
#include <include\common\sd_constants.h>
#include <include\c\SD_Module.h>
#include <include\c\SD_TDC.h>
#include <include\common\SD_Module_DEFS.h>

void flushKeys();
void userCallBack(void* SDobject, int eventNumber, void *buffer, int numData, void *buffer2, int numData2, void *userObject, int status);


struct UserStruct 
{
	int moduleID;
	int nChannel;
	FILE *fp;
};

int main()
{
	int slot;
	int moduleTDC;
	int nDAQ;
	unsigned long long *dataBuffer;
	unsigned long long *removeBuffer;
	int i = 0;
	char fileName[256];

	UserStruct userObject;

	printf("---- Demo DAQ with callback ----\n");
	printf("Enter the Module Slot: ");
	scanf("%d",&slot);
	printf("Enter nDAQ: ");
	scanf("%d",&nDAQ);
	printf("Enter file name: ");
	scanf("%s",fileName);

	flushKeys();

	// Open module with slot
	moduleTDC = SD_Module_openWithSlot("SD-PXE-TDC",0,slot);						
	
	if(moduleTDC<=0)
	{
		printf("Error opening module\n");
		getchar();
		return 1;
	}

	// Stop DAQ
	SD_TDC_DAQstop(moduleTDC, nDAQ);

	// Flush DAQ
	SD_TDC_DAQflush(moduleTDC, nDAQ);

	userObject.moduleID = moduleTDC;
	userObject.nChannel = nDAQ;
	userObject.fp = fopen(fileName, "ab");
	if (userObject.fp == NULL) {
		printf("ERROR : Can't open output file!\n");
	  exit(1);
	}

	// Config DAQ with two cycles of 16 points
	SD_TDC_DAQconfig(moduleTDC, nDAQ, 16, 2, 1, VIHVITRIG); 

	// Config DAQ bufers pool with Callback
	dataBuffer = (unsigned long long *)malloc(16*sizeof(unsigned long long)); 
	SD_TDC_DAQbufferPoolConfig(moduleTDC, nDAQ, dataBuffer, 16, 1000, userCallBack, &userObject);

	// Add other buffer pool
	dataBuffer = (unsigned long long *)malloc(16*sizeof(unsigned long long)); 
	SD_TDC_DAQbufferAdd(moduleTDC, nDAQ, dataBuffer, 16);  

	printf("Module configuration successfull. Press any key to start the DAQ.");
	getchar();

	// Start DAQ
	SD_TDC_DAQstart(moduleTDC, nDAQ);
	
	printf("DAQ started. Waiting for trigger for first cycles. Press any key to send a VI/HVI trigger.");
	getchar();

	// Send VI/HVI trigger
	SD_TDC_DAQtrigger(moduleTDC, nDAQ);

	// Waiting for 16 points (first cycle)
	while(SD_TDC_DAQcounterRead(moduleTDC, nDAQ)<16);

	printf("DAQ has acquired %d points. Press any key to continue.",SD_TDC_DAQcounterRead(moduleTDC, nDAQ));
	getchar();

	printf("Waiting for another trigger for second cycles. Press any key to send a VI/HVI trigger.");
	getchar();

	// Send VI/HVI trigger
	SD_TDC_DAQtrigger(moduleTDC, nDAQ);

	// Waiting for 16 points (second cycle)
	while(SD_TDC_DAQcounterRead(moduleTDC, nDAQ)<32);

	printf("DAQ has acquired %d points.\n",SD_TDC_DAQcounterRead(moduleTDC, nDAQ));
	
	printf("Press any key to finish.");
	getchar();
	
	// Free all objects and buffers
	fclose(userObject.fp);
	SD_TDC_DAQbufferPoolRelease(moduleTDC, nDAQ);
	while((removeBuffer = SD_TDC_DAQbufferRemove(moduleTDC, nDAQ)) != 0)
		free(removeBuffer);
	SD_Module_close(moduleTDC);

    return 0;
}

void flushKeys()
{
	char ch;
	while ((ch = getchar()) != '\n' && ch != EOF);
}

void userCallBack(void* SDobject, int eventNumber, void *buffer, int numDDWdata, void *buffer2, int numData2, void *userObject, int status)
{
    unsigned long long *readBuffer;
	UserStruct *userPtr;
	static unsigned long long dataPrev = 0;

	userPtr = (UserStruct *)userObject;
    readBuffer = (unsigned long long*) buffer;

    printf("\nThe Callback has been called!\n");
    for(int i=0;i<numDDWdata;i++)
    {
        //printf("Data: %u \n", readBuffer[i]);
		fprintf(userPtr->fp, "\tData : %lld ps : difference = %lld ps \r\n", readBuffer[i], readBuffer[i]-dataPrev);
		dataPrev = readBuffer[i];
    }
	printf(" Points written : %d \n",numDDWdata);
	printf(" Total points read : %d \n",SD_TDC_DAQcounterRead(userPtr->moduleID, userPtr->nChannel));
}
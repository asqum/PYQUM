#include <stdlib.h>
#include <stdio.h>
// Must include Keysight SD1 programming libraries as global include path. You can use the "KEYSIGHT_SD1_LIBRARY_PATH" system environment variable
#include <include\common\sd_constants.h>
#include <include\c\SD_Module.h>
#include <include\c\SD_DIO.h>
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
	int moduleDIO;
	int nDAQ;
	short *dataBuffer;
	short *removeBuffer;
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
	moduleDIO = SD_Module_openWithSlot("SD-PXE-DIO",0,slot);						
	
	if(moduleDIO<=0)
	{
		printf("Error opening module\n");
		getchar();
		return 1;
	}

	// Stop DAQ
	SD_DIO_DAQstop(moduleDIO, nDAQ);

	// Flush DAQ
	SD_DIO_DAQflush(moduleDIO, nDAQ);

	userObject.moduleID = moduleDIO;
	userObject.nChannel = nDAQ;
	userObject.fp = fopen(fileName, "ab");
	if (userObject.fp == NULL) {
		printf("ERROR : Can't open output file!\n");
	  exit(1);
	}

	// Config the Input Bus 0 pins 0 to 15 of Port 0 
	SD_DIO_busConfig(moduleDIO, 1000, 0, 0, 15);

	// Config DAQ with two cycles of 40 points
	SD_DIO_DAQconfig(moduleDIO, nDAQ, 40, 2, 1, VIHVITRIG); 

	// Config DAQ bufers pool with Callback
	dataBuffer = (short *)malloc(100*sizeof(short)); 
	SD_DIO_DAQbufferPoolConfig(moduleDIO, nDAQ, dataBuffer, 16, 5000, userCallBack, &userObject);

	// Add other buffer pool
	dataBuffer = (short *)malloc(100*sizeof(short)); 
	SD_DIO_DAQbufferAdd(moduleDIO, nDAQ, dataBuffer, 16);  

	printf("Module configuration successfull. Press any key to start the DAQ.");
	getchar();

	// Start DAQ
	SD_DIO_DAQstart(moduleDIO, nDAQ);
	
	printf("DAQ started. Waiting for trigger for first cycles. Press any key to send a VI/HVI trigger.");
	getchar();

	// Send VI/HVI trigger
	SD_DIO_DAQtrigger(moduleDIO, nDAQ);

	// Waiting for 16 points (first cycle)
	while(SD_DIO_DAQcounterRead(moduleDIO, nDAQ)<16);

	printf("DAQ has acquired %d points. Press any key to continue.",SD_DIO_DAQcounterRead(moduleDIO, nDAQ));
	getchar();

	printf("Waiting for another trigger for second cycles. Press any key to send a VI/HVI trigger.");
	getchar();

	// Send VI/HVI trigger
	SD_DIO_DAQtrigger(moduleDIO, nDAQ);

	// Waiting for 16 points (second cycle)
	while(SD_DIO_DAQcounterRead(moduleDIO, nDAQ)<32);

	printf("DAQ has acquired %d points.",SD_DIO_DAQcounterRead(moduleDIO, nDAQ));
	
	printf("Press any key to finish.");
	getchar();
	
	// Free all objects and buffers
	fclose(userObject.fp);
	SD_DIO_DAQbufferPoolRelease(moduleDIO, nDAQ);
	while((removeBuffer = SD_DIO_DAQbufferRemove(moduleDIO, nDAQ)) != 0)
		free(removeBuffer);
	SD_Module_close(moduleDIO);

    return 0;
}

void flushKeys()
{
	char ch;
	while ((ch = getchar()) != '\n' && ch != EOF);
}

void userCallBack(void* SDobject, int eventNumber, void *buffer, int numDDWdata, void *buffer2, int numData2, void *userObject, int status)
{
    short *readBuffer;
	UserStruct *userPtr;

	userPtr = (UserStruct *)userObject;
    readBuffer = (short*) buffer;

    printf("\nThe Callback has been called!\n");
    for(int i=0;i<numDDWdata*4;i++)
    {
        //printf("Data: %u \n", readBuffer[i]);
		fprintf(userPtr->fp, "Data:\t%u \r\n", readBuffer[i]);
    }
	printf(" Points written : %d \n",numDDWdata *4);
	printf(" Total points read : %d \n",SD_DIO_DAQcounterRead(userPtr->moduleID, userPtr->nChannel));
}
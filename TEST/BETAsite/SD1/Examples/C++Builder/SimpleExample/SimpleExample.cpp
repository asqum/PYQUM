//---------------------------------------------------------------------------

#include <vcl.h>
#pragma hdrstop

#include "SimpleExample.h"
#include "..\..\..\Libraries\include\Cpp_Borland\SignadyneBC.h"

//---------------------------------------------------------------------------
#pragma package(smart_init)
#pragma resource "*.dfm"
TForm1 *Form1;
//---------------------------------------------------------------------------
__fastcall TForm1::TForm1(TComponent* Owner)
	: TForm(Owner)
{
	myModule = 0;
}
//---------------------------------------------------------------------------
void __fastcall TForm1::ButtonOpenClick(TObject *Sender)
{
	UTF8String myStr = this->EditModuleName->Text;

	if(myModule == 0)
	{
		myModule = new(SD_AOU);
		myModule->open(myStr.c_str(),0,this->EditSlot->Text.ToInt());

		if(myModule->isOpen()==true)
		{
			this->EditStatus->Text = "Module Opened";
			this->ButtonOpen->Caption = "Close";
			this->PanelWaveform->Enabled = true;

			// Config amplitude and setup AWG in channels 0
			myModule->channelAmplitude(0, 1.0);				// 1.2 Volts Peak
			myModule->channelWaveShape(0, AOU_AWG);

		}
		else
		{
			this->EditStatus->Text = "Error Openning Module";
			delete myModule;
			myModule = 0;
			this->PanelWaveform->Enabled=false;
		}
	}
	else
	{
		myModule->close();
		delete myModule;
		myModule = 0;
		this->EditStatus->Text = "Module Closed";
		this->ButtonOpen->Caption = "Open";
		this->PanelWaveform->Enabled=false;
	}


}
//---------------------------------------------------------------------------

void __fastcall TForm1::ButtonPlayFileClick(TObject *Sender)
{
	UTF8String fileStr = this->EditFileName->Text;

	if (myModule->AWG(0, fileStr.c_str(), AUTOTRIG, 0, 0, 0) < 0)
	{
		this->EditStatus->Text = "Error loading the waveform file";
		return;
	}
}
//---------------------------------------------------------------------------

void __fastcall TForm1::ButtonStopClick(TObject *Sender)
{
	  myModule->AWGstop(0);
}
//---------------------------------------------------------------------------

void __fastcall TForm1::ButtonPlayArrayClick(TObject *Sender)
{
	double data = 0;
	int nPoints = 1000000;
	double inc = 0.1;
	short* waveformData = new short[nPoints];

	for(int i = 0; i < nPoints; i++)
	{
		waveformData[i] = (short)(data*32767.0);
		data = data + inc;
		if(data > 1)
		{
			data = 2-data;
			inc = -0.1;
		}
		else if (data < -1)
		{
			data = -2 - data;
			inc = 0.1;
		}
	}

	myModule->AWGflush(0);	//Stop AWG and Flush AWG queue

	// Load waveform in module on-board memory
	if (myModule->waveformLoad(WAVE_ANALOG, nPoints,waveformData, 0) < 0)
	{
		this->EditStatus->Text = "Error loading the waveform";
		return;
	}

	// Queue waveform to be played
	if (myModule->AWGqueueWaveform(0, 0, 0, 0, 0, 0) < 0)
	{
		this->EditStatus->Text = "Error queueing loaded waveform";
		return;
	}

	// Start AWG to play queued waveforms
	if (myModule->AWGstart(0) < 0)
	{
		this->EditStatus->Text = "Error running AWG";
		return;
	}

	delete waveformData;

}
//---------------------------------------------------------------------------



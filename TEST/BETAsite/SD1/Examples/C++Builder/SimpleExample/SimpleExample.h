//---------------------------------------------------------------------------

#ifndef SimpleExampleH
#define SimpleExampleH
//---------------------------------------------------------------------------
#include <System.Classes.hpp>
#include <Vcl.Controls.hpp>
#include <Vcl.StdCtrls.hpp>
#include <Vcl.Forms.hpp>
#include <Vcl.ExtCtrls.hpp>
//---------------------------------------------------------------------------

class SD_AOU;

class TForm1 : public TForm
{
__published:	// IDE-managed Components
	TButton *ButtonOpen;
	TEdit *EditModuleName;
	TLabel *Label1;
	TLabel *Label2;
	TEdit *EditSlot;
	TEdit *EditStatus;
	TPanel *PanelWaveform;
	TLabel *Label3;
	TEdit *EditFileName;
	TButton *ButtonPlayFile;
	TButton *ButtonPlayArray;
	TButton *ButtonStop;
	void __fastcall ButtonOpenClick(TObject *Sender);
	void __fastcall ButtonPlayFileClick(TObject *Sender);
	void __fastcall ButtonStopClick(TObject *Sender);
	void __fastcall ButtonPlayArrayClick(TObject *Sender);
private:	// User declarations
	SD_AOU *myModule;
public:		// User declarations
	__fastcall TForm1(TComponent* Owner);
};
//---------------------------------------------------------------------------
extern PACKAGE TForm1 *Form1;
//---------------------------------------------------------------------------
#endif

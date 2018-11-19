object Form1: TForm1
  Left = 0
  Top = 0
  Caption = 'Form1'
  ClientHeight = 107
  ClientWidth = 580
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  OldCreateOrder = False
  PixelsPerInch = 96
  TextHeight = 13
  object Label1: TLabel
    Left = 8
    Top = 21
    Width = 31
    Height = 13
    Caption = 'Name:'
  end
  object Label2: TLabel
    Left = 168
    Top = 21
    Width = 22
    Height = 13
    Caption = 'Slot:'
  end
  object ButtonOpen: TButton
    Left = 239
    Top = 16
    Width = 75
    Height = 25
    Caption = 'Open'
    TabOrder = 0
    OnClick = ButtonOpenClick
  end
  object EditModuleName: TEdit
    Left = 41
    Top = 20
    Width = 121
    Height = 21
    TabOrder = 1
    Text = 'SD-PXE-AOU-H3344'
  end
  object EditSlot: TEdit
    Left = 192
    Top = 20
    Width = 41
    Height = 21
    TabOrder = 2
    Text = '7'
  end
  object EditStatus: TEdit
    Left = 320
    Top = 18
    Width = 251
    Height = 21
    TabOrder = 3
    Text = 'Module Closed'
  end
  object PanelWaveform: TPanel
    Left = 8
    Top = 47
    Width = 564
    Height = 50
    Enabled = False
    TabOrder = 4
    object Label3: TLabel
      Left = 9
      Top = 17
      Width = 50
      Height = 13
      Caption = 'File Name:'
    end
    object EditFileName: TEdit
      Left = 65
      Top = 15
      Width = 249
      Height = 21
      TabOrder = 0
      Text = 'W:\Waveforms_Demo\gaussian.csv'
    end
    object ButtonPlayFile: TButton
      Left = 320
      Top = 11
      Width = 75
      Height = 25
      Caption = 'Play File'
      TabOrder = 1
      OnClick = ButtonPlayFileClick
    end
    object ButtonPlayArray: TButton
      Left = 401
      Top = 11
      Width = 75
      Height = 25
      Caption = 'Play Array'
      TabOrder = 2
      OnClick = ButtonPlayArrayClick
    end
    object ButtonStop: TButton
      Left = 482
      Top = 11
      Width = 75
      Height = 25
      Caption = 'Stop AWG'
      TabOrder = 3
      OnClick = ButtonStopClick
    end
  end
end

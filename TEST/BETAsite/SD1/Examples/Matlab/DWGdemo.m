% Load Visual Studio Library
NET.addAssembly(strcat(getenv('KEYSIGHT_SD1_LIBRARY_PATH'), '\VisualStudio.NET\KeysightSD1.dll'));

slot = 5;
part = 'SD-PXE-DIO';

% Create module object
dio = KeysightSD1.SD_DIO();

if dio.isOpen() % By default module should not be opened.
    disp('Module is alredy opened. Demo will close it.');
    dio.close();
end;

% Open module
if dio.open(part, 1, slot) < 0
    disp(['Error opening module ', part, ', make sure the slot and chassis are correct.']);
    disp('Aborting demo...');
    return;
end;

% Check that module was opened successfully
if dio.isOpen()
    disp(['Module ', part, ' opened in slot ', int2str(slot), '.']);
end;

dio.DWGtriggerExternalConfig(0, KeysightSD1.SD_TriggerExternalSources.TRIGGER_EXTERN, KeysightSD1.SD_TriggerBehaviors.TRIGGER_RISE);

wave = KeysightSD1.SD_Wave('C:/Users/Public/Documents/Keysight/SD1/Examples/Waveforms/DigitalTest_0&1_64samples.csv');
dio.waveformLoad(wave, 0, 0);
dio.DWGqueueWaveform(0,0,KeysightSD1.SD_TriggerModes.EXTTRIG_CYCLE, 0, 0, 0);
dio.DWGstart(0);

dio.close();
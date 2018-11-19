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

dio.busConfig(KeysightSD1.SD_DIO_Bus.DIO_INPUT_BUS0, 0, 0, 15);
dio.DAQtriggerExternalConfig(0, KeysightSD1.SD_TriggerExternalSources.TRIGGER_EXTERN, KeysightSD1.SD_TriggerBehaviors.TRIGGER_RISE);
dio.DAQconfig(0,1000,1,0,KeysightSD1.SD_TriggerModes.EXTTRIG_CYCLE);
dio.DAQstart(0);

%wait, DAQread or whatever that has to be done.

dio.close();
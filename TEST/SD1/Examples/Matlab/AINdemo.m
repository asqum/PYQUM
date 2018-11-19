NET.addAssembly(strcat(getenv('KEYSIGHT_SD1_LIBRARY_PATH'), '\VisualStudio.NET\KeysightSD1.dll'));

slot = 3;
cycles = 1;
points = 2500;
channel = 0;

triggerMode = KeysightSD1.SD_TriggerModes.VIHVITRIG;

prescaler = 0;
fullscale = 3;%in Volt, 0 to peak
coupling = 0;%0=DC, 1=AC

module = KeysightSD1.SD_AIN();

% Open module
if module.open('', 1, slot) < 0
	disp(['Error opening module on slot ' num2str(slot) ', make sure the slot and chassis are correct.']);
	disp('Aborting demo...');
	return;
end;

module.channelInputConfig(channel, fullscale, 1, coupling);
module.DAQconfig(channel, points, cycles, 0, triggerMode);

module.channelPrescalerConfig(channel, prescaler);
module.DAQflush(channel);
module.DAQstart(channel);

disp('Press any key to launch trigger.');
pause;
module.DAQtrigger(channel);
disp('Press any key to read data.');
pause;

data = NET.createArray('System.Int16', points);
readPoints = module.DAQread(channel, data, 1000);

data = int16(data);
plot(data(1:readPoints));

module.close();

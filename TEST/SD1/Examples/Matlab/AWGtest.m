function AWGtest
    % Load Visual Studio Library
    NET.addAssembly(strcat(getenv('KEYSIGHT_SD1_LIBRARY_PATH'), '\VisualStudio.NET\KeysightSD1.dll'));

    slot = 4;
    part = 'SD-PXE-AOU';

    % Create module object
    aou = KeysightSD1.SD_AOU();

    if aou.isOpen() % By default module should not be opened.
        disp('Module is alredy opened. Demo will close it.');
        aou.close();
    end;

    % Open module
    if aou.open(part, 1, slot) < 0
        disp(['Error opening module ', part, ', make sure the slot and chassis are correct.']);
        disp('Aborting demo...');
        return;
    end;

    % Check that module was opened successfully
    if aou.isOpen()
        disp(['Module ', part, ' opened in slot ', int2str(slot), '.']);
    end;

    % Setup AWG channel 0
    aou.waveformFlush(); %Stop all AWGs, Reset Queues and flush waveform memory
    aou.channelAmplitude(0, 1);
    aou.channelWaveShape(0, KeysightSD1.SD_Waveshapes.AOU_AWG);

    disp('Press any key to run AWG channel 0 with an infinite Gaussian waveform loaded from file...');
    pause;

    % Load waveform file
    wave = KeysightSD1.SD_Wave('C:/Users/Public/Documents/Keysight/SD1/Examples/Waveforms/Gaussian.csv');

    if wave.getStatus() < 0
        disp('Error loading waveform file Gaussian.csv, make sure its path is correct.');
        aou.close();
        disp('Aborting demo...');
        return;
    end;

    % Load waveform to module
    if aou.waveformLoad(wave, 0) < 0
        disp('Error loading waveform, make sure wave object and its number are correct.');
        aou.close();
        disp('Aborting demo...');
        return;
    end;
    
    memSize = aou.waveformGetMemorySize(0);
    disp(['Wavefom size = ', int2str(memSize), ' Bytes.']);

    % Queue loaded waveform to AWG 0 queue
    if aou.AWGqueueWaveform(0, 0, 0, 0, 0, 0) < 0
        disp('Error queueing loaded waveform, make sure queue paremeters are correct.');
        aou.close();
        disp('Aborting demo...');
        return;
    end;

    % Run AWG 0
    if aou.AWGstart(0) < 0
        disp('Error running AWG.');
        aou.close();
        disp('Aborting demo...');
        return;
    end;

    disp('Press any key to run AWG channel 0 with an infinite Triangular waveform loaded from array data in one step calling AWG(...) function...');
    pause;

    triangularData = getTriangular();
    % Load and run (in one step) a waveform from arry data
    if aou.AWG(0, 0, 0, 0, 0, KeysightSD1.SD_WaveformTypes.WAVE_ANALOG, triangularData) < 0
        disp('Error loading waveform array, make sure its data and type are correct.');
        aou.close();
        disp('Aborting demo...');
        return;
    end;

    disp('Press any key to run AWG channel 0 with an infinite Exponential waveform loaded from file...');
    pause;

    aou.waveformFlush(); %Stop all AWGs, Reset Queues and flush waveform memory

    % Load waveform file
    wave = KeysightSD1.SD_Wave('C:/Users/Public/Documents/Keysight/SD1/Examples/Waveforms/Exponential.csv');

    if wave.getStatus() < 0
        disp('Error loading waveform file Gaussian.csv, make sure its path is correct.');
        aou.close();
        disp('Aborting demo...');
        return;
    end;

    % Load waveform to module
    if aou.waveformLoad(wave, 0) < 0
        disp('Error loading waveform, make sure wave object and its number are correct.');
        aou.close();
        disp('Aborting demo...');
        return;
    end;
    
    memSize = aou.waveformGetMemorySize(0);
    disp(['Wavefom size = ', int2str(memSize), ' Bytes.']);

    % Queue loaded waveform to AWG 0 queue
    if aou.AWGqueueWaveform(0, 0, 0, 0, 0, 0) < 0
        disp('Error queueing loaded waveform, make sure queue paremeters are correct.');
        aou.close();
        disp('Aborting demo...');
        return;
    end;

    % Run AWG 0
    if aou.AWGstart(0) < 0
        disp('Error running AWG.');
        aou.close();
        disp('Aborting demo...');
        return;
    end;

    disp('Press any key to run AWG channel 0 with an infinite Triangular waveform loaded from int16 array data...');
    pause;

    triangularShort = int16((2^15-1)*triangularData);

    aou.AWGflush(0); %Stop AWG0 and Flush its queue 

    % Load waveform to module
    if aou.waveformLoad(KeysightSD1.SD_WaveformTypes.WAVE_ANALOG, triangularShort, 1) < 0
        disp('Error loading waveform, make sure wave object and its number are correct.');
        aou.close();
        disp('Aborting demo...');
        return;
    end;
    
    memSize = aou.waveformGetMemorySize(1);
    disp(['Wavefom size = ', int2str(memSize), ' Bytes.']);

    % Queue loaded waveform to AWG 0 queue
    if aou.AWGqueueWaveform(0, 1, 0, 0, 0, 0) < 0
        disp('Error queueing loaded waveform, make sure queue paremeters are correct.');
        aou.close();
        disp('Aborting demo...');
        return;
    end;

    % Run AWG 0
    if aou.AWGstart(0) < 0
        disp('Error running AWG.');
        aou.close();
        disp('Aborting demo...');
        return;
    end;
    
    disp('Press any key to reload exponential waveform instead of previous waveform and run it in AWG channel 0...');
    pause;
    
    aou.AWGflush(0); %Stop AWG0 and Flush its queue 

    % Load waveform to module
    if aou.waveformReLoad(wave, 1) < 0
        disp('Error loading waveform, make sure wave object and its number are correct.');
        aou.close();
        disp('Aborting demo...');
        return;
    end;
    
    memSize = aou.waveformGetMemorySize(1);
    disp(['Wavefom size = ', int2str(memSize), ' Bytes.']);

    % Queue loaded waveform to AWG 0 queue
    if aou.AWGqueueWaveform(0, 1, 0, 0, 0, 0) < 0
        disp('Error queueing loaded waveform, make sure queue paremeters are correct.');
        aou.close();
        disp('Aborting demo...');
        return;
    end;

    % Run AWG 0
    if aou.AWGstart(0) < 0
        disp('Error running AWG.');
        aou.close();
        disp('Aborting demo...');
        return;
    end;

    disp('Press any key to close the module and end demo...');
    pause;

    % Stop AWG
    aou.AWGstop(0);

    % Close module
    aou.close();

end

function data = getTriangular()

    data = [0,
    0.04,
    0.08,
    0.12,
    0.16,
    0.2,
    0.24,
    0.28,
    0.32,
    0.36,
    0.4,
    0.44,
    0.48,
    0.52,
    0.56,
    0.6,
    0.64,
    0.68,
    0.72,
    0.76,
    0.8,
    0.84,
    0.88,
    0.92,
    0.96,
    1,
    0.96,
    0.92,
    0.88,
    0.84,
    0.8,
    0.76,
    0.72,
    0.68,
    0.64,
    0.6,
    0.56,
    0.52,
    0.48,
    0.44,
    0.4,
    0.36,
    0.32,
    0.28,
    0.24,
    0.2,
    0.16,
    0.12,
    0.08,
    0.04,
    0,
    -0.04,
    -0.08,
    -0.12,
    -0.16,
    -0.2,
    -0.24,
    -0.28,
    -0.32,
    -0.36,
    -0.4,
    -0.44,
    -0.48,
    -0.52,
    -0.56,
    -0.6,
    -0.64,
    -0.68,
    -0.72,
    -0.76,
    -0.8,
    -0.84,
    -0.88,
    -0.92,
    -0.96,
    -1,
    -0.96,
    -0.92,
    -0.88,
    -0.84,
    -0.8,
    -0.76,
    -0.72,
    -0.68,
    -0.64,
    -0.6,
    -0.56,
    -0.52,
    -0.48,
    -0.44,
    -0.4,
    -0.36,
    -0.32,
    -0.28,
    -0.24,
    -0.2,
    -0.16,
    -0.12,
    -0.08,
    -0.04];
end


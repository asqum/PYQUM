function TDCdemo
    % Load Visual Studio Library
    NET.addAssembly(strcat(getenv('KEYSIGHT_SD1_LIBRARY_PATH'), '\VisualStudio.NET\KeysightSD1.dll'));

    slot = 2;
    part = 'SD-PXE-TDC-H0002';

    % Create module object
    tdc = KeysightSD1.SD_TDC();

    if tdc.isOpen() % By default module should not be opened.
        disp('Module is alredy opened. Demo will close it.');
        tdc.close();
    end;

    % Open module
    if tdc.open(part, 1, slot) < 0
        disp(['Error opening module ', part, ', make sure the slot and chassis are correct.']);
        disp('Aborting demo...');
        return;
    end;

    % Check that module was opened successfully
    if tdc.isOpen()
        disp(['Module ', part, ' opened in slot ', int2str(slot), '.']);
    end;

    dataBuffer = uint64(zeros(1000,1));
    dataBuffer2 = uint64(zeros(1000,1));
    nChannel = 0;
    nChannel2 = 1;
    totalPointsRead = 0;
    nPointsRead = 0;
    points2read = 1000;
    error = 0;
    i = 0;

    % Config DAQ Buffers Pool with Callback
    tdc.DAQbufferPoolConfig(nChannel, dataBuffer, 5000);

    % Add other buffer
    tdc.DAQbufferAdd(nChannel, dataBuffer2);  

    % Stop DAQ
    tdc.DAQstop(nChannel);

    % Flush DAQ
    tdc.DAQflush(nChannel);

    % Config DAQ with 1 cycle of 10000 points
    tdc.DAQconfig(nChannel, points2read, 1, 1, KeysightSD1.SD_TriggerModes.VIHVITRIG);

    display('Module configuration successfull. Press any key to start the DAQ.');
    pause;

    % Start DAQ
    tdc.DAQstart(nChannel);

    display('DAQ started. Waiting for trigger for first cycles. Press any key to send a VI/HVI trigger.');
    pause;

    % Send VI/HVI trigger
    tdc.DAQtrigger(nChannel);

    % Waiting for 1000 points
    while nPointsRead < points2read
        nPointsRead = tdc.DAQcounterRead(nChannel);
    end;

    display(['DAQ has acquired ', int2str(nPointsRead), ' points.']);
    pause;

    % Read data
    nPointsRead = 0;
    while nPointsRead < points2read
        [readBuffer, nPointsRead, error] = tdc.DAQbufferGet(nChannel);
        if nPointsRead < points2read
            display(['Points Read : ', int2str(nPointsRead), '. Expected: ', int2str(points2read)]);
        end;
        if error < 0
            display(['error : ', char(KeysightSD1.SD_Error.getErrorMessage(error))]);
        end;
    end;
    
    plot(readBuffer);

    display('Press any key to release DAQ buffers.');
    pause;

    % Free all  buffers
    tdc.DAQbufferPoolRelease(nChannel);
    nBuffers = 0;
    readBuffer = tdc.DAQbufferRemove(nChannel);
    while ~isempty(readBuffer)
        readBuffer = tdc.DAQbufferRemove(nChannel);
        nBuffers = nBuffers + 1;
    end;
    display(['Removed ', int2str(nBuffers), ' buffers.']);
        
    display('Press any key to finish.');
    pause;
    
    tdc.close();
    
end
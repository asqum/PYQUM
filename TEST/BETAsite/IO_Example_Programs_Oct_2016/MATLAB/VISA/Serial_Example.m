%A an example of setting serial port settings and getting a *IDN? response
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% © Keysight Technologies 2016
%
% You have a royalty-free right to use, modify, reproduce and distribute
% the Sample Application Files (and/or any modified version) in any way
% you find useful, provided that you agree that Keysight Technologies has no
% warranty, obligations or liability for any Sample Application Files.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Change VISA_ADDRESS to a serial VISA address, e.g. 'ASRL2::INSTR'
VISA_ADDRESS = 'Your instruments VISA address goes here!';

try
    % Create a connection (session) to the serial instrument
    session = visa('agilent', VISA_ADDRESS);
	fopen(session);

    % If you've setup the serial port settings in Connection Expert, you can remove this section.
    % Otherwise, set your connection parameters
	session.BaudRate = 57600;
	session.DataBits = 8;
    session.Parity = 'none';
    session.FlowControl = 'software';
    session.Terminator = 10;
    
    % Send the *IDN? and read the response
    fprintf(session,'*IDN?');
    idn = fscanf(session, '%c');
        
    fprintf('*IDN? returned: %s\n', strtrim(idn));

    % Close the connection to the instrument
    fclose(session);
catch ex
    fprintf('An error occurred: %s\n', ex.getReport());
    if (exist('session', 'var'))
        fclose(session);
    end
end

fprintf('Done.\n');

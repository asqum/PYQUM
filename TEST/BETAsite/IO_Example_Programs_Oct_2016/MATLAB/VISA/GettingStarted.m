%A simple example of using VISA to send commands to an instrument
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

    
% Change this variable to the address of your instrument
VISA_ADDRESS = 'Your instruments VISA address goes here!';

try
    % Create a connection (session) to the instrument
    session = visa('agilent', VISA_ADDRESS);
    fopen(session);
catch ex
    fprintf('Couldn''t connect to ''%s''\n%s\n, exiting now...\n', VISA_ADDRESS, getReport(ex));
    return;
end

% Send *IDN? and read the response
fprintf(session, '*IDN?');
idn = fscanf(session, '%c');

fprintf('*IDN? returned: %s\n', strtrim(idn));

% Close the connection to the instrument
fclose(session);

fprintf('Done.\n')

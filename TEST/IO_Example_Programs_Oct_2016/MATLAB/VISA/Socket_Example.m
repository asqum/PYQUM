%Create a connection to an instrument with a TCP/IP socket and send a *IDN?
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


% Change VISA_ADDRESS to a SOCKET address, e.g. 'TCPIP::169.254.104.59::5025::SOCKET'
VISA_ADDRESS = 'Your instruments VISA address goes here!';

try
    % Create a connection (session) to the TCP/IP socket on the instrument.
    session = visa('agilent', VISA_ADDRESS);
    fopen(session);
        
    % Send the *IDN? and read the response
    fprintf(session, '*IDN?');
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

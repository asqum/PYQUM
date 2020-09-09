%An example of how to handle I/O errors in MATLAB
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

 
function ErrorHandling()

	% Change this variable to the address of your instrument
	VISA_ADDRESS = 'Your instruments VISA address goes here!';

	% Part 1:
	%
	% Shows the mechanics of how to deal with an error in MATLAB when it occurs.
	% To stimulate an error, the code will try to open a connection to an instrument at an invalid address...
	%
	% First we'll provide an invalid address and see what error we get

	try
		session = visa('agilent', 'BAD ADDRESS');
	catch ex
		fprintf('VISA ERROR - An error has occurred!\n');

		% To get more specific information about the exception, we can check what kind of error it is and
		% add specific error handling code. In this example, that is done in the exceptionHandler function
		exceptionHandler(ex);
	end
	
	% Part 2:
	%
	% Stimulate another error by sending an invalid query and trying to read its response.
	%
	% Before running this part, don't forget to set your instrument address in the 'VISA_ADDRESS'
	% variable at the top of this function

	session = visa('agilent', VISA_ADDRESS);
	fopen(session);

	% Misspell the *IDN? query as *IND?
	try
		fprintf(session, '*IND?');
	catch ex2
		fprintf('VISA ERROR - You''ll never get here, because the *IND? data will get sent to the instrument successfully, ' + ...
			'it''s the instrument that won''t like it.\n');
	end
	
	% Try to read the response (*IND?)
	try
		idnResponse = fscanf(session, '%c');
        error(lastwarn);
		fprintf('*IDN? returned: %s\n', idnResponse);
	catch ex3
		fprintf('VISA ERROR - The read call will timeout, because the instrument doesn''t know what to do with the command that we sent it.\n');
	end
			  
	% Check the instrument to see if it has any errors in its queue
	rawError = '';
	errorCode = -1;

	while errorCode ~= 0
		fprintf(session, 'SYST:ERR?');
        rawError = fscanf(session, '%c');
		
		errorParts = strsplit(rawError, ',');
		errorCode = str2double(errorParts(1));
		errorMessage = strtrim(char(errorParts(2)));

		fprintf('INSTRUMENT ERROR - Error code: %d, error message: %s\n', errorCode, errorMessage);
	end
	
	% Close the connection to the instrument
	fclose(session);

	fprintf('Done.\n');
end 


function exceptionHandler(exception)
    fprintf('Error information:\n\tIdentifier: %s\n\tMessage: %s\n', ...
		exception.identifier, exception.message);
end

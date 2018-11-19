%An example of how to find devices configured in Keysight Connection Expert
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

 
function FindDevices()

    % Find all devices and interfaces
    find('?*')

    % You can specify other device types using different search strings. 
    % Here are some common examples:

    % All instruments (no INTFC, BACKPLANE or MEMACC)
    find('?*INSTR')
    % PXI modules
    find('PXI?*INSTR')
    % USB devices
    find('USB?*INSTR')
    % GPIB instruments
    find('GPIB?*')
    % GPIB interfaces
    find('GPIB?*INTFC')
    % GPIB instruments on the GPIB0 interface
    find('GPIB0?*INSTR')
    % LAN instruments
    find('TCPIP?*')
    % SOCKET (::SOCKET) instruments
    find('TCPIP?*SOCKET')
    % VXI-11 (inst) instruments
    find('TCPIP?*inst?*INSTR')
    % HiSLIP (hislip) instruments
    find('TCPIP?*hislip?*INSTR')
    % RS-232 instruments
    find('ASRL?*INSTR')

    fprintf('Done.\n');

end 


function [addresses] = find(searchString)
    hwInfo = instrhwinfo('visa', 'agilent');
    constructors = hwInfo.ObjectConstructorName;
    if (size(constructors, 1) > 0)
        expr = ['''(?<string>[^'']+)'''];
        index = 0;
        for constructorI = 1:length(constructors)
            constructorCell = constructors(constructorI);
            constructor = constructorCell{1};
            parts = regexp(constructor, expr, 'names');
            visaAddress = parts(2).string;
            
            % see if it matches searchString
            matlabRegex = strrep(searchString, '?*', '(??.*)');
            startIndex = regexp(visaAddress, matlabRegex, 'ignorecase');
            if length(startIndex) > 0
                if index == 0
                    addressesCell = {visaAddress};
                    index = 1;
                else
                    addressesCell{end+1} = visaAddress;
                end
           end
        end
    else
        addressesCell = {''};
        fprintf('... no devices found.\n');
    end
    if exist('addressesCell', 'var')
        addresses = char(addressesCell);
    else
        addresses = [];
    end
end

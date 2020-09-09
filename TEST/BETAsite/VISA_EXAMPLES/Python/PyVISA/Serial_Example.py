################################################################################
# © Keysight Technologies 2016
#
# You have a royalty-free right to use, modify, reproduce and distribute
# the Sample Application Files (and/or any modified version) in any way
# you find useful, provided that you agree that Keysight Technologies has no
# warranty, obligations or liability for any Sample Application Files.
#
################################################################################

import visa


# Change VISA_ADDRESS to a serial VISA address, e.g. 'ASRL2::INSTR'
VISA_ADDRESS = 'Your instruments VISA address goes here!'

try:
    # Create a connection (session) to the serial instrument
    resourceManager = visa.ResourceManager()
    session = resourceManager.open_resource(VISA_ADDRESS)

    # For Serial and TCP/IP socket connections enable the read Termination Character, or read's will timeout
    if session.resource_name.startswith('ASRL') or session.resource_name.endswith('SOCKET'):
        session.read_termination = '\n'

    # If you've setup the serial port settings in Connection Expert, you can remove this section.
    # Otherwise, set your connection parameters
    session.set_visa_attribute(visa.constants.VI_ATTR_ASRL_BAUD, 9600)
    session.set_visa_attribute(visa.constants.VI_ATTR_ASRL_DATA_BITS, 8)
    session.set_visa_attribute(visa.constants.VI_ATTR_ASRL_PARITY, visa.constants.VI_ASRL_PAR_NONE)
    session.set_visa_attribute(visa.constants.VI_ATTR_ASRL_FLOW_CNTRL, visa.constants.VI_ASRL_FLOW_DTR_DSR)

    # Send the *IDN? and read the response
    session.write('*IDN?')
    idn = session.read()

    print('*IDN? returned: %s' % idn.rstrip('\n'))

    # Close the connection to the instrument
    session.close()
    resourceManager.close()

except visa.Error as ex:
    print('An error occurred: %s' % ex)

print('Done.')

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


# Change VISA_ADDRESS to a SOCKET address, e.g. 'TCPIP::169.254.104.59::5025::SOCKET'
VISA_ADDRESS = 'Your instruments VISA address goes here!'

try:
    # Create a connection (session) to the TCP/IP socket on the instrument.
    resourceManager = visa.ResourceManager()
    session = resourceManager.open_resource(VISA_ADDRESS)

    # For Serial and TCP/IP socket connections enable the read Termination Character, or read's will timeout
    if session.resource_name.startswith('ASRL') or session.resource_name.endswith('SOCKET'):
        session.read_termination = '\n'

    # We can find out details of the connection
    print('IP: %s\nHostname: %s\nPort: %d\n' %
          (session.get_visa_attribute(visa.constants.VI_ATTR_TCPIP_ADDR),
           session.get_visa_attribute(visa.constants.VI_ATTR_TCPIP_HOSTNAME),
           session.get_visa_attribute(visa.constants.VI_ATTR_TCPIP_PORT)))

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

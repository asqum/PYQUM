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
import sys

# Change this variable to the address of your instrument
VISA_ADDRESS = 'Your instruments VISA address goes here!'

try:
    # Create a connection (session) to the instrument
    resourceManager = visa.ResourceManager()
    session = resourceManager.open_resource(VISA_ADDRESS)
except visa.Error as ex:
    print('Couldn\'t connect to \'%s\', exiting now...' % VISA_ADDRESS)
    sys.exit()

# For Serial and TCP/IP socket connections enable the read Termination Character, or read's will timeout
if session.resource_name.startswith('ASRL') or session.resource_name.endswith('SOCKET'):
    session.read_termination = '\n'

# Send *IDN? and read the response
session.write('*IDN?')
idn = session.read()

print('*IDN? returned: %s' % idn.rstrip('\n'))

# Close the connection to the instrument
session.close()
resourceManager.close()

print('Done.')

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

def exceptionHandler(exception):

    print('Error information:\n\tAbbreviation: %s\n\tError code: %s\n\tDescription: %s' % \
          (exception.abbreviation, exception.error_code, exception.description))


# Change this variable to the address of your instrument
VISA_ADDRESS = 'Your instruments VISA address goes here!'

# Part 1:
#
# Shows the mechanics of how to deal with an error in PyVISA when it occurs.
# To stimulate an error, the code will try to open a connection to an instrument at an invalid address...
#
# First we'll provide an invalid address and see what error we get

resourceManager = visa.ResourceManager()

try:
    session = resourceManager.open_resource("BAD ADDRESS")
except visa.VisaIOError as ex:
    print('VISA ERROR - An error has occurred!\n')

    # To get more specific information about the exception, we can check what kind of error it is and
    # add specific error handling code. In this example, that is done in the exceptionHandler function
    exceptionHandler(ex)

# Part 2:
#
# Stimulate another error by sending an invalid query and trying to read its response.
#
# Before running this part, don't forget to set your instrument address in the 'VISA_ADDRESS'
# variable at the top of this script

session = resourceManager.open_resource(VISA_ADDRESS)

# Misspell the *IDN? query as *IND?
try:
    session.write('*IND?')
except visa.VisaIOError as ex2:
    print(
        'VISA ERROR - You\'ll never get here, because the *IND? data will get sent to the instrument successfully, '
        'it\'s the instrument that won\'t like it.')

# Try to read the response (*IND ?)
try:
    idnResponse = session.read()
    print('*IDN? returned: %s\n' % idnResponse)
except visa.VisaIOError as ex3:
    print('VISA ERROR - The read call will timeout, because the instrument doesn\'t'
          ' know what to do with the command that we sent it.')

# Check the instrument to see if it has any errors in its queue
rawError = ''
errorCode = -1

while errorCode != 0:
    session.write('SYST:ERR?')
    rawError = session.read()

    errorParts = rawError.split(',')
    errorCode = int(errorParts[0])
    errorMessage = errorParts[1].rstrip('\n')

    print('INSTRUMENT ERROR - Error code: %d, error message: %s' % (errorCode, errorMessage))

# Close the connection to the instrument
session.close()
resourceManager.close()

print('Done.')

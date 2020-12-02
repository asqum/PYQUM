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


# Change VISA_ADDRESS to a PXI address, e.g. 'PXI0::23-0.0::INSTR'
VISA_ADDRESS = 'visa://qdl-pc/PXI20::14::0::INSTR'

try:
    # Create a connection (session) to the PXI module
    resourceManager = visa.ResourceManager()
    session = resourceManager.open_resource(VISA_ADDRESS)

    print('Manufacturer: %s\nModel: %s\nChassis: %d\nSlot: %d\nBus-Device.Function: %d-%d.%d\n' %
          (session.get_visa_attribute(visa.constants.VI_ATTR_MANF_NAME),
           session.get_visa_attribute(visa.constants.VI_ATTR_MODEL_NAME),
           session.get_visa_attribute(visa.constants.VI_ATTR_PXI_CHASSIS),
           session.get_visa_attribute(visa.constants.VI_ATTR_SLOT),
           session.get_visa_attribute(visa.constants.VI_ATTR_PXI_BUS_NUM),
           session.get_visa_attribute(visa.constants.VI_ATTR_PXI_DEV_NUM),
           session.get_visa_attribute(visa.constants.VI_ATTR_PXI_FUNC_NUM)))

    print(session.get_visa_attribute(visa.constants.VI_ATTR_PXI_FUNC_NUM))
    # Close the connection to the instrument
    session.close()
    resourceManager.close()

except visa.Error as ex:
    print('An error occurred: %s' % ex)

print('Done.')

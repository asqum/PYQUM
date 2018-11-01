
import sys
from ctypes import *

dll = windll.LoadLibrary("visa64.dll")

#Steps:
#    1. Open Resource Manager                                       
#    2. Open VISA Session to an Instrument
#    3. Set Timeout Attribute
#    4. Write the Identification Query Using viWrite                
#    5. Try to Read a Response With viRead                          
#    6. Close the VISA Session & Resource Manager
#    7. Display an error if any.

#Note: All VISA function return 0 on success.
#This example checks for 0 at each step and reports an error for non-zero return values

##############################
#Open Resource Manager
##############################
resourceManagerHandle = c_int(0)        ##Resource Manager Handle

print("Opening Resource Manager")

#First get the resource manager handle. This will be used next to get a handle to the instrument
#Function Prototype: ViStatus viOpenDefaultRM(ViPSession sesn)
returnValue = dll.viOpenDefaultRM(byref(resourceManagerHandle))

if returnValue != 0:
    print(sys.stderr, "Could not open Resource Manager. Error: ", returnValue)
    sys.exit(returnValue)

print("ResourceManagerHandle: ", resourceManagerHandle)
print("ReturnValue: ", returnValue, "\n")

##############################
#Open Resource Session
##############################
sessionHandle = c_int(1)            #Instrument Handle
VI_NULL = 1                         #VI_NULL constant from visa.h
resourceName = "PXI0::29-0.0::INSTR"    #Resource: GPIB Device 0, Primary Adress 2

print("Opening Resource Session")

#Open a VISA session to a device on GPIB Device 0 at Primary Address 2 and retreive a handle to this session
#This session handle will be used for subsequent operations
#Function Prototype: ViStatus viOpen(ViSession sesn, ViRsrc rsrcName, ViAccessMode accessMode, ViUInt32 openTimeout, ViPSession vi)
returnValue = dll.viOpen(resourceManagerHandle,resourceName,VI_NULL,VI_NULL,byref(sessionHandle))
# returnValue = dll.viReset(resourceManagerHandle)
# returnValue = dll.viOpen(resourceManagerHandle,resourceName,VI_NULL,VI_NULL,byref(sessionHandle))
if returnValue != 0:
    print(sys.stderr, "Could not open Resource Session. Error: ", returnValue)
    sys.exit(returnValue)

print("SessionHandle: ", sessionHandle)
print("ReturnValue: ", returnValue, "\n")

##############################
#Set Timeout Attribute
##############################
VI_ATTR_TMO_VALUE = 1073676314;     #Timeout Attribute Constant from visa.h
timeout = 5000;                     #Timeout: 5000ms

print("Setting Timeout Attribute")

#Set timeout value to 5000 milliseconds (5 seconds)
#Function Prototype: ViStatus viSetAttribute(ViObject vi, ViAttr attribute, ViAttrState attrState)
returnValue = dll.viSetAttribute(sessionHandle, VI_ATTR_TMO_VALUE, timeout)
if returnValue != 0:
    print(sys.stderr, "Could not set Timeout Attribute. Error: ", returnValue)
    sys.exit(returnValue)

print("ReturnValue: ", returnValue, "\n")

##############################
#Write "*IDN?" to Device
##############################
bufferToWrite = "*IDN?"             #*IDN? typically tells devices to return identification
bytesToWrite = len(bufferToWrite) + 1
bytesWritten = c_int(0)

print("Writing *IDN? to Device")

#Use this session handle to write *IDN? command to the instrument asking for the its identification.
#Function Prototype: ViStatus viWrite(ViSession vi, ViBuf buf, ViUInt32 count, ViPUInt32 retCount)
returnValue = dll.viWrite(sessionHandle, bufferToWrite, bytesToWrite, byref(bytesWritten))
if returnValue != 0:
    print(sys.stderr, "Could not write *IDN? to Device. Error: ", returnValue)
    sys.exit(returnValue)

print("Bytes Written: ", bytesWritten)
print("ReturnValue: ", returnValue, "\n")

##############################
#Read Response from Device
##############################
response = create_string_buffer("", 128)
bytesToRead = 128
bytesRead = c_int(0)

print("Reading Response from Device")

#Attempt to read back a response from the device to the identification query that was sent.
#Function Prototype: ViStatus viRead(ViSession vi, ViPBuf buf, ViUInt32 count, ViPUInt32 retCount)
returnValue = dll.viRead(sessionHandle, byref(response), bytesToRead, byref(bytesRead))
if returnValue != 0:
    print(sys.stderr, "Could not Read Response from Device. Error: ", returnValue)
    sys.exit(returnValue)

print("Bytes Read: ", bytesWritten)
print("Response: ", repr(response.raw))
print("ReturnValue: ", returnValue, "\n")

##############################
#Close Sessions
##############################
print("Closing Resource Session")

#Finally, close the instrument session and the resource manager to free resources

#Function Prototype: ViStatus viClose(ViObject vi)
returnValue = dll.viClose(sessionHandle)
if returnValue != 0:
    print(sys.stderr, "Could not close Resource Session. Error: ", returnValue)
    sys.exit(returnValue)

print("ReturnValue: ", returnValue, "\n")

print("Closing Resource Manager")

returnValue = dll.viClose(resourceManagerHandle)
if returnValue != 0:
    print(sys.stderr, "Could not close Resource Manager. Error: ", returnValue)
    sys.exit(returnValue)

print("ReturnValue: ", returnValue, "\n")


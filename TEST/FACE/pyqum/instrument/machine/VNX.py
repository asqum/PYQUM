from ctypes import c_int, cdll
from ctypes.util import find_library

# Copy DLL to windows\system32
lib_name = find_library('VNX_atten64.dll') 
vnx = cdll.LoadLibrary(lib_name)
vnx.fnLDA_SetTestMode(0)

DeviceIDArray = c_int * 64
Devices = DeviceIDArray()
print("Number of Devices = %s"%vnx.fnLDA_GetNumDevices())
vnx.fnLDA_GetDevInfo(Devices)
print("Serial Number: %s" %vnx.fnLDA_GetSerialNumber(Devices[0]))
vnx.fnLDA_InitDevice(Devices[0])
vnx.fnLDA_SetWorkingFrequency(Devices[0], 2000)

while True:
    try: Attenuation = float(input("ATT_dB (select 0-63, res: 0.5 OR press enter to exit): ")) # effective attenuation = -10dB - Attenuation-dB (range: -10dB to -73dB, at 6GHz, res: 0.5dB)
    except: break
    vnx.fnLDA_SetAttenuationHR(Devices[0], int(Attenuation * 20))
    print("Attenuation in .05db units = %s" %vnx.fnLDA_GetAttenuationHR(Devices[0]))

vnx.fnLDA_CloseDevice(Devices[0])

from ctypes import *
from ctypes.util import find_library

# dloc = "C:\\Program Files\\IVI Foundation\\IVI\Bin\\AgM9392_64.dll" #64-bit
lib_name = find_library('AgM9392_64.dll') #Python is 64-bit
dll = windll.LoadLibrary(lib_name) 
# Instrument address
VSArs = b'PXI24::12::0::INSTR;PXI24::14::0::INSTR;PXI24::8::0::INSTR;PXI24::9::0::INSTR;PXI29::0::0::INSTR'


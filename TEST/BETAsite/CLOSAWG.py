from ctypes import c_int, c_bool, c_char_p, byref, cdll, c_long, c_char, c_wchar, c_wchar_p, c_byte
from ctypes.util import find_library

# dloc = "C:\\Program Files\\IVI Foundation\\IVI\Bin\\AgM933x_64.dll" #64-bit
lib_name = find_library('AgM933x_64.dll')
dll = cdll.LoadLibrary(lib_name) #Python is 64-bit
AWGrs = b'PXI22::14::0::INSTR'

# Closing session
def run(s=2):
    AGMclose = dll.AgM933x_close
    status = AGMclose(c_long(s)) #session of AWG defaultly set to 2
    print("\nclose:")
    print('status: %s' %(status))
    return status

# run()

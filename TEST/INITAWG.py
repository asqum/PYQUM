from ctypes import c_int, c_bool, c_char_p, byref, cdll, c_long, c_char
from ctypes.util import find_library
from visa import ResourceManager as rm

# dloc = "C:\\Program Files\\IVI Foundation\\IVI\Bin\\AgM933x_64.dll" #64-bit
lib_name = find_library('AgM933x_64.dll')
print(lib_name)
dll = cdll.LoadLibrary(lib_name) #Python is 64-bit

rm = rm()
# A = rm.open_resource("visa://192.168.0.7:3537/PXI20::14::0::INSTR")
AWGrs = b'192.168.0.7:3537/PXI20::14::0::INSTR'

# Initiate session
def run():
    session = c_int()
    AGMinit = dll.AgM933x_InitWithOptions
    AGMinit.restype = c_int
    option = 'Simulate=false, DriverSetup=DDS=false'
    option = bytes(option, 'utf-8')
    status = AGMinit(c_char_p(AWGrs), c_bool(True), c_bool(True), c_char_p(option), byref(session))
    print("\nInitWithOptions:")
    print('status: %s' %(status))
    print('session: %s' %(session.value))
    return status, session.value

run()

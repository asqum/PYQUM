from ctypes import c_int, c_bool, c_char_p, byref, windll
from ctypes.util import find_library

# dloc = "C:\\Program Files\\IVI Foundation\\IVI\Bin\\AgM9392_64.dll" #64-bit
lib_name = find_library('AgM9392_64.dll')
dll = windll.LoadLibrary(lib_name) #Python is 64-bit

address = 'PXI24::12::0::INSTR;PXI24::14::0::INSTR;PXI24::8::0::INSTR;PXI24::9::0::INSTR;PXI29::0::0::INSTR'
VSArs = bytes(address, 'utf-8') # equivalent to b'xxxxxx'
# print(c_wchar_p(VSArs).value)

# def c_string(s):
#     return c_char_p(str(s).encode('utf-8'))

#  Initiate session
session = c_int()
AGM = dll.AgM9392_InitWithOptions
AGM.restype = c_int
status = AGM(c_char_p(VSArs), c_bool(False), c_bool(False), c_char_p(b''), byref(session))
print('status: %s' %(status))
print('session: %s' %(session.value))

AGM9392_ATTR_INSTRUMENT_MODEL = 1050512
answer = c_char_p() # answer value format (use byref)
AGM = dll.AgM9392_GetAttributeViString
AGM.restype = c_int
status = AGM(session, b'', c_int(AGM9392_ATTR_INSTRUMENT_MODEL), c_int(2048), byref(answer))
print('status: %s' %(status))
print('session: %s' %(answer.value))


# Close session
AGMclose = dll.AgM9392_close
stat = AGMclose(session)
print(stat)

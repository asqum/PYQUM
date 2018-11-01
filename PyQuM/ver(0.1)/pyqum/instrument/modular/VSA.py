'''communicating with modular VSA via dll
'''

from ctypes import c_int, c_bool, c_char_p, byref, windll
from ctypes.util import find_library

# dloc = "C:\\Program Files\\IVI Foundation\\IVI\Bin\\AgM9392_64.dll" #64-bit
lib_name = find_library('AgM9392_64.dll')
dll = windll.LoadLibrary(lib_name) #Python is 64-bit

# The name should be consistent with the functions provided in driver's manual
def InitWithOptions(RS, IdQuery=False, Reset=False, OptionsString=''):
    '''[status, session] = InitWithOptions(ResourceName, IdQuery, Reset, OptionsString)
    '''
    Resource = bytes(RS, 'utf-8')
    Option = bytes(OptionsString, 'utf-8')
    session = c_int()
    AGM = dll.AgM9392_InitWithOptions
    AGM.restype = c_int
    status = AGM(c_char_p(Resource), c_bool(IdQuery), c_bool(Reset), c_char_p(Option), byref(session))
    return status, session.value

# from pyqum.instrument.logger import address
# VSArs = address("VSA")
# status, session = InitWithOptions(VSArs)
# print("VSA is initialized: Error=%s, Session#=%s" %(status, session)) #status=0 means no error

def close(session):
    '''status = close(session)
    '''
    AGMclose = dll.AgM9392_close
    status = AGMclose(c_int(session))
    return status

# stat = close(session)
# print("VSA is closed:", stat)
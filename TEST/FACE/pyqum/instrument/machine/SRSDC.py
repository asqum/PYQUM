# Communicating with Benchtop SRS-SX199-DC205 (Latest:2021/04)
from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # module's name e.g. PSG

import socket
from pyqum.instrument.logger import address, set_status, status_code, debug
from numpy import log10, ceil
from time import sleep

# PENDING: Add "available_channels" into the database
available_channels = [1,2]

def Initiate(current=False, which=2, mode='DATABASE'):
    ad = address(mode)
    rs = ad.lookup(mdlname, which) # Instrument's Address
    inst = socket.socket()
    inst.connect((rs.split(':')[0], int(rs.split(':')[1])))
    inst.settimeout(7)
    try:
        inst.send(b'ULOC 1\n')
        inst.send(b'ULOC?\n')
        unlock_state = inst.recv(1024).decode()
        inst.send(b'*IDN?\n')
        model = inst.recv(1024).decode()
        print(Fore.YELLOW + "Unlock %s: %s" %(model, unlock_state))
    except:
        print(Fore.RED + "DC Channel not unlinked properly: go to the previously linked Channel directly")

    return inst

def get_voltage(inst, channel=1):
    '''
    channel: 1-4
    '''
    inst.send(('LINK %s\n' %channel).encode())
    inst.send(b'*OPC?\n')
    inst.recv(1024).decode()
    inst.send(b'VOLT?\n')
    voltage = float(inst.recv(1024).decode())
    inst.send(b'!\n')
    return voltage
def get_range(inst, channel=1):
    '''
    channel: 1-4
    '''
    inst.send(('LINK %s\n' %channel).encode())
    inst.send(b'*OPC?\n')
    inst.recv(1024).decode()
    inst.send(b'RNGE?\n')
    vrange = inst.recv(1024).decode().split('RANGE')[1]
    inst.send(b'!\n')
    return vrange
def get_output(inst, channel=1):
    '''
    channel: 1-4
    '''
    inst.send(('LINK %s\n' %channel).encode())
    inst.send(b'*OPC?\n')
    inst.recv(1024).decode()
    inst.send(b'SOUT?\n')
    state = int(inst.recv(1024).decode())
    inst.send(b'!\n')
    return state
def set_voltage(inst, voltage, channel=1):
    '''
    voltage in V (type: float)
    channel: 1-4
    '''
    # 1. select channel via optic:
    inst.send(('LINK %s\n' %channel).encode())
    inst.send(b'*OPC?\n')
    inst.recv(1024).decode()
    # 1. select range:
    try: range_order = int((ceil(log10(voltage)) + abs(ceil(log10(voltage)))) / 2)
    except(ValueError): range_order = 0 # to accommodate zero-voltage
    if range_order > 2: 
        print(Fore.RED + "voltage setting out of range")
        inst.send(b'!\n')
        return 0
    inst.send(('RNGE %s\n' %(range_order)).encode())
    # 2. set voltage:
    inst.send(('VOLT %s\n' %voltage).encode())
    inst.send(b'*OPC?\n')
    ready = inst.recv(1024).decode()
    inst.send(b'!\n')
    return ready

def sweep(inst, voltage, channel, update_settings={}):
    voltage = round(float(voltage),12)
    if get_output(inst, channel): 
        output(inst, 0, [int(channel)]) # have to turn-off output to move up/down the range!
        set_voltage(inst, voltage, int(channel))
        output(inst, 1, [int(channel)]) # turn back on if initially on
    else:
        set_voltage(inst, voltage, int(channel))
    return

def output(inst, state, channel=available_channels):
    '''
    ***selective output***
    state: 0 (OFF), 1 (ON)
    ALL channel: 1-2 / 1-4 so far
    '''
    for CH in channel:
        inst.send(('LINK %s\n' %CH).encode())
        inst.send(b'*OPC?\n')
        inst.recv(1024).decode()
        inst.send(('SOUT %s\n' %state).encode())
        inst.send(b'*OPC?\n')
        ready = inst.recv(1024).decode()
        inst.send(b'!\n')
    
    return ready

def close(inst, reset=True, which=1):
    if reset: 
        for channel in available_channels: sweep(inst, 0, channel) # return ALL to zero
    try:
        inst.close()
        status = "Success"
        ad = address()
        ad.update_machine(0, "%s_%s"%(mdlname,which))
    except: status = "Error"
    set_status(mdlname, dict(state='disconnected'))
    print(Back.WHITE + Fore.BLACK + "%s-%s's connection Closed" %(mdlname,which))
    return status

# =============================================================================================================================================================
# TEST ZONE:
if __name__ == "__main__":
    from pyqum.instrument.toolbox import cdatasearch, waveform

    v_array = waveform("-0.7 to 0.7 *14").data
    # v_array = [1e-6, 3e-5, 6e-4, 7e-3, 8e-2, 2e-1, 1, 1.5] #, 6, 10, 18, 37, 58, 77, 100, 101, 150, 0]
    # v_array = [6, 10, 18, 37, 58, 77, 100, 101, 150, 0]
    print("Sweeping: %s" %v_array)

    s = Initiate(which=2, mode='TEST') # DR-1: 1, DR-2: 2
    channel = int(input("Channel [1: lower, 2: upper stack] >> ")) # 1: lower, 2: upper stack
    output(s, 1)

    for v in v_array:
        print("\nsweeping %sV:" %v)
        sweep(s, v, channel)
        print("state: %s" %get_output(s, channel))
        print("reading: %sV" %get_voltage(s, channel))
        input("press enter to continue: ")
        
    output(s, 0)    
    close(s, True)



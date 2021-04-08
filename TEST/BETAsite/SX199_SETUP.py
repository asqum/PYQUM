"""SETUP SX199 IP Address for DC205"""

import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

def setup():
    # Open connection
    # print(visa.ResourceManager().list_resources(query='TCP?*'))
    rm = visa.ResourceManager()
    inst = rm.open_resource('GPIB0::6::INSTR')
    # inst = rm.open_resource('TCPIP::192.168.1.44::8888::SOCKET"')
    inst.read_termination = '\n' #omit termination tag from output 
    inst.timeout = 80000000 #set timeout (ms)

    # Unlock Ethernet
    # print(inst.query('ULOC?'))
    inst.write('ULOC 1')
    print(inst.query('ULOC?'))

    # Model
    print(inst.query('*IDN?'))

    # Netmask
    print("Netmask: %s.%s.%s.%s" %(inst.query('NMSK?0'),inst.query('NMSK?1'),inst.query('NMSK?2'),inst.query('NMSK?3')))
    inst.write('NMSK 2, 255')
    print("Netmask: %s.%s.%s.%s" %(inst.query('NMSK?0'),inst.query('NMSK?1'),inst.query('NMSK?2'),inst.query('NMSK?3')))

    # Gateway
    print("Gateway: %s.%s.%s.%s" %(inst.query('GWAY?0'),inst.query('GWAY?1'),inst.query('GWAY?2'),inst.query('GWAY?3')))
    inst.write('GWAY 0, 192; GWAY 1, 168; GWAY 2, 1; GWAY 3, 1;')
    print("Gateway: %s.%s.%s.%s" %(inst.query('GWAY?0'),inst.query('GWAY?1'),inst.query('GWAY?2'),inst.query('GWAY?3')))

    # IP Address
    print("IP Address: %s.%s.%s.%s" %(inst.query('IPAD?0'),inst.query('IPAD?1'),inst.query('IPAD?2'),inst.query('IPAD?3')))
    inst.write('IPAD 0, 192; IPAD 1, 168; IPAD 2, 1; IPAD 3, 44;')
    print("IP Address: %s.%s.%s.%s" %(inst.query('IPAD?0'),inst.query('IPAD?1'),inst.query('IPAD?2'),inst.query('IPAD?3')))

    # Save Parameters
    inst.write('SPAR 0')
    # inst.write('*RST')

    # Close connection
    inst.close()

setup()

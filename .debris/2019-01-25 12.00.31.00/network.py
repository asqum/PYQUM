#!/usr/bin/env python
'''Everything related to Network Configuration & Testing'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

import visa
from time import time, ctime, sleep
from numpy import linspace
import matplotlib.pyplot as plt

def checkallconnections():
    '''Check the availability of all instrument
    '''
    rm = visa.ResourceManager()
    addresses = {}
    # listed (GPIB first):
    addresses["Yoko"] = "GPIB0::2::INSTR"
    # addresses["T01"] = "GPIB0::21::INSTR"
    # addresses["T02"] = "GPIB0::24::INSTR"
    # addresses["T03"] = "GPIB0::5::INSTR"
    addresses['RDS'] = 'TCPIP0::192.168.1.81::INSTR'
    addresses["PSG"] = 'TCPIP0::192.168.1.35::INSTR'
    addresses["ENA"] = 'TCPIP0::192.168.1.85::INSTR'
    addresses['RDG'] = 'TCPIP0::192.168.1.179::INSTR'
    # addresses["PNA"] = "TCPIP0::192.168.0.6::hpib7,16::INSTR"
    # addresses["MXG"] = "TCPIP0::192.168.0.3::INSTR"
    # PXIs
    # addresses["VSA"] = "PXI22::12::0::INSTR;PXI22::14::0::INSTR;PXI22::8::0::INSTR;PXI22::9::0::INSTR;PXI27::0::0::INSTR"
    # addresses["AWG"] = "PXI20::14::0::INSTR"

    

    instr = {}
    for i,ad in addresses.items():
        try:
            instr[i] = rm.open_resource(ad)
            instr[i].read_termination = '\n' #omit termination tag from output 
            instr[i].timeout = 3000 #set timeout
            print(Fore.WHITE + Back.GREEN + "%s is ONLINE!" %i)
            if i in ['Yoko']:
                print(Fore.YELLOW + "OD: %s" %instr[i].query('OD'))
            else:
                print(Fore.YELLOW + "ID: %s" %instr[i].query('*IDN?'))  #inquiring machine identity: "who r u?"
            instr[i].close()
        except:
            pass
            print(Fore.RED + "%s is OFFLINE!" %i)

    return instr

def connectionspeed(instr, typ='query', loop=3000):
    '''Check the speed of instrument's connection
    '''
    if typ.lower() == 'query':
        for k in instr.keys():
            if k == 'Yoko':
                start, speed = time(), []
                for i in range(loop):
                    instr[k].query('OD')
                    duration = time() - start
                    speed.append((i + 1) / duration) # actions per second
                fig, ax = plt.subplots(1, sharex=True, sharey=False)
                ax.set(title="Connection Speed Test for %s"%k, xlabel="count", ylabel='speed(#/s)')
                ax.plot([range(loop)], speed)
                fig.tight_layout()
                plt.show()
            else:
                start, speed = time(), []
                for i in range(loop):
                    instr[k].query('*IDN?')
                    duration = time() - start
                    speed.append((i + 1) / duration) # actions per second
                fig, ax = plt.subplots(1, sharex=True, sharey=False)
                ax.set(title="Connection Speed Test for %s"%k, xlabel="count", ylabel='speed(#/s)')
                ax.plot([range(loop)], speed)
                fig.tight_layout()
                plt.show()

    

instr = checkallconnections()
connectionspeed(instr)





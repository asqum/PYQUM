#!/usr/bin/env python
'''Everything related to Network Configuration & Testing'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

import visa, subprocess, platform
from time import time, ctime, sleep
from contextlib import suppress
from numpy import linspace
import matplotlib.pyplot as plt

# under construction
def scanetwork():
    platinfo = platform.system() #check which OS

    IPlist, active = [], []
    for i in range(10):
        IPlist.append("169.254.0." + str(i))

    if platinfo == "Windows":
        pass
    elif platinfo == "Darwin":
        for ip in IPlist:
            p = subprocess.Popen(["ping", "-c", "1", "-W" "1", ip], stdout=subprocess.PIPE)
            msg = [i for i in p.stdout]
            a = 0
            for msg in msg:
                b = int("ttl" in str(msg))
                a += b
            print("Scanning %s", ip)
            if a == 1:
                active.append(ip)

    print("Active IP:")
    for active in active:
        print(active)
    # under construction

def checkallconnections(closeonexit=False):
    '''Check the availability of all instrument
    '''
    rm = visa.ResourceManager()
    addresses = {}
    # listed (GPIB first):
    # addresses["Yoko"] = "GPIB0::2::INSTR"
    # addresses["T01"] = "GPIB0::21::INSTR"
    # addresses["T02"] = "GPIB0::24::INSTR"
    # addresses["T03"] = "GPIB0::5::INSTR"
    addresses['RDS'] = 'TCPIP0::192.168.1.81::INSTR'
    addresses["PSG"] = 'TCPIP0::192.168.1.35::INSTR'
    addresses["ENA"] = 'TCPIP0::192.168.1.85::INSTR'
    # addresses['RDG'] = 'TCPIP0::192.168.1.179::INSTR'
    # addresses["PNA"] = "TCPIP0::192.168.0.6::hpib7,16::INSTR"
    # addresses["MXG"] = "TCPIP0::192.168.0.3::INSTR"
    # PXIs
    # addresses["VSA"] = "PXI22::12::0::INSTR;PXI22::14::0::INSTR;PXI22::8::0::INSTR;PXI22::9::0::INSTR;PXI27::0::0::INSTR"
    # addresses["AWG"] = "PXI20::14::0::INSTR"

    instr = {}
    for k,ad in addresses.items():
        try:
            instr[k] = rm.open_resource(ad)
            instr[k].read_termination = '\n' #omit termination tag from output 
            instr[k].timeout = 3000 #set timeout
            print(Fore.WHITE + Back.GREEN + "%s is ONLINE!" %k)
            if k in ['Yoko']:
                print(Fore.YELLOW + "OD: %s" %instr[k].query('OD'))
            else:
                print(Fore.YELLOW + "ID: %s" %instr[k].query('*IDN?'))  #inquiring machine identity: "who r u?"
            if closeonexit:
                instr[k].close()
        except:
            pass
            with suppress(KeyError): instr.pop(k)
            print(Fore.RED + "%s is OFFLINE!" %k)
    return instr

def connectionspeed(instr, typ='query', loop=3000):
    '''Check the speed of instrument's connection
    '''
    if typ.lower() == 'query':
        for k in instr.keys():
            if k == 'Yoko':
                start, speed = time(), []
                for i in range(loop):
                    print("Testing %s's connection speed loop#%d" %(k, i+1))
                    instr[k].query('OD')
                    duration = time() - start
                    speed.append((i + 1) / duration) # actions per second
                fig, ax = plt.subplots(1, sharex=True, sharey=False)
                ax.set(title="Connection Speed Test for %s"%k, xlabel="count", ylabel='speed(#/s)')
                ax.plot(range(loop), speed)
                fig.tight_layout()
                plt.show()
            else:
                start, speed = time(), []
                for i in range(loop):
                    print("Testing %s's connection speed loop#%d" %(k, i+1))
                    instr[k].query('*IDN?')
                    duration = time() - start
                    speed.append((i + 1) / duration) # actions per second
                fig, ax = plt.subplots(1, sharex=True, sharey=False)
                ax.set(title="Connection Speed Test for %s"%k, xlabel="count", ylabel='speed(#/s)')
                ax.plot(range(loop), speed)
                fig.tight_layout()
                plt.show()


# instr = checkallconnections()
# print(instr)
# connectionspeed(instr)


scanetwork()
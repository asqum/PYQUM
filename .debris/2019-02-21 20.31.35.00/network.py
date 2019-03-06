#!/usr/bin/env python
'''Everything related to Network Configuration & Testing'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

import visa, subprocess, platform
from time import time, ctime, sleep
from contextlib import suppress
from numpy import linspace
import matplotlib.pyplot as plt

def scanetwork():
    active = []
    platinfo = platform.system() #check which OS
    if platinfo == "Windows":
        counts, timeout = '-n', '-w'
    elif platinfo == "Darwin":
        counts, timeout = '-c', '-W'

    for i in range(256):
        network_prefix = "192.168.1."
        ip = network_prefix + str(i)
        print(Fore.CYAN + "\r%d%% scanned"%(i / 255 * 100) + Fore.GREEN + " [%s instrument(s) FOUND]"%len(active), end='\r', flush=True)
        p = subprocess.Popen(["ping", counts, "1", timeout, "1", ip], stdout=subprocess.PIPE)
        msg = [i for i in p.stdout]
        if "ttl" in str(msg).lower():
            active.append(ip)

    return active

def checkallconnections():
    '''Check the availability of all instrument
    '''
    rm = visa.ResourceManager()
    addresses = {}
    # addresses["Yoko"] = "GPIB0::2::INSTR"
    # addresses["Tes"] = "GPIB0::7::INSTR"
    # addresses["Test"] = "GPIB0::8::INSTR"
    # addresses['RDS'] = 'TCPIP0::192.168.1.81::INSTR'
    addresses["PSGV"] = 'TCPIP0::192.168.1.35::INSTR'
    # addresses["PSGA"] = 'TCPIP0::192.168.1.33::INSTR'
    # addresses["ENA"] = 'TCPIP0::192.168.1.85::INSTR'
    # addresses['RDG'] = 'TCPIP0::192.168.1.179::INSTR'
    # addresses['RDSG'] = 'TCPIP0::192.168.1.25::INSTR'
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
            if k in ['Yoko']:
                ID = instr[k].query('OD')
            else:
                ID = instr[k].query('*IDN?')
            print(Fore.WHITE + Back.GREEN + "%s is ONLINE!" %k)
            print(Fore.YELLOW + "ID: %s" %ID)  #identify each machine
                
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
            print(Fore.CYAN + "Testing %s's connection speed"%k)
            if k == 'Yoko':
                start, speed = time(), []
                for i in range(loop):
                    print("\r%d%%" %(i/(loop-1)*100), end='\r', flush=True)
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
                    print("\r%d%%" %(i/(loop-1)*100), end='\r', flush=True)
                    instr[k].query('*IDN?')
                    duration = time() - start
                    speed.append((i + 1) / duration) # actions per second
                fig, ax = plt.subplots(1, sharex=True, sharey=False)
                ax.set(title="Connection Speed Test for %s"%k, xlabel="count", ylabel='speed(#/s)')
                ax.plot(range(loop), speed)
                fig.tight_layout()
                plt.show()

def closeall(instr):
    for k,v in instr.items():
        print(Fore.BLACK + Back.WHITE + "\rClosing %s"%k, end='\r', flush=True)
        v.close()
        print(Fore.BLACK + Back.WHITE + "\r%s is CLOSED"%k, end='\r', flush=True)
        return


def test():
    # active = scanetwork()
    # print("\nConnected Instruments:")
    # for i, active in enumerate(active):
    #     print(Fore.YELLOW + "%s. %s" %(i+1, active))
    instr = checkallconnections()
    connectionspeed(instr)
    closeall(instr)

    return



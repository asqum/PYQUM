#!/usr/bin/env python
'''Everything related to Network Configuration & Testing'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

import visa, subprocess, platform
from time import time, ctime, sleep
from contextlib import suppress
from numpy import linspace
import matplotlib.pyplot as plt

from pyqum.instrument.logger import address

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

    print("\nConnected Instruments:")
    for i, active in enumerate(active):
        print(Fore.YELLOW + "%s. %s" %(i+1, active))

    return active

def checkallconnections():
    '''Check the availability of all instrument
    '''
    rm = visa.ResourceManager()
    ad = address()
    addresses = {}
    for i in ad.visible():
        addresses[i] = ad.lookup(i)

    instr = {}
    for k,ad in addresses.items():
        try:
            instr[k] = rm.open_resource(ad)
            instr[k].read_termination = '\r\n' #omit termination tag from output 
            instr[k].timeout = 3000 #set timeout
            # check serial interface
            interface = str(instr[k].interface_type).split('.')[1].upper()
            if interface == 'ASRL':
                instr[k].baud_rate, instr[k].data_bits = 57600, 7
                instr[k].parity = visa.constants.Parity(1)
                instr[k].stop_bits = visa.constants.StopBits(10)
            if k in ['Yoko']:
                ID = instr[k].query('OD')
            else:
                ID = instr[k].query('*IDN?')
            print(Fore.WHITE + Back.GREEN + "%s [%s] is ONLINE!" %(k, interface))
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

def initializationspeed():
    # to be filled
    return


def test():
    scanetwork()
    # instr = checkallconnections()
    # connectionspeed(instr)
    # closeall(instr)
    # initializationspeed()
    return

# test()

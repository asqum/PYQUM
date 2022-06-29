"""
THIS is to SETUP IP Address for Model SX199 Optical Interface Controller: (Since 2022/1/12)
0. Before running this script, the following tasks must be prepared:
1. Use the other network card on the PiQuM-Workstation, and connect it to the router that has 10.0.0.xxx environment.
2. Set the bottom-right jumper accordingly such that SX199 has a static IP of 10.0.0.206 (NOTE: follow the instruction beside those jumpers, not the manual!)
3. ping 10.0.0.206 in CMD to check route existence.
4. Install PuTTY and use Telnet to connect using port 8888 along with the aforementioned IP. After starting Telnet, hit ENTER new-line to initialize connection. (Do refer manual for this part)
5. After commands are getting through, we may start to run the codes below:
"""
from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

import socket
from time import sleep

Jumper_ADDR = '10.0.0.206'
Previous_ADDR = '192.168.1.45'

class telnet:
    def __init__(self, Device_IP_Address=Jumper_ADDR, Device_Port=8888):
        # 0. Open connection:
        self.ADDR = (Device_IP_Address, Device_Port)
        self.inst = socket.socket()
        self.inst.connect(self.ADDR)
        self.inst.settimeout(7)
        print(Fore.GREEN + "Connection Initialized.")

    def write(self, command):
        self.inst.send(bytes('%s\n' %command, 'utf-8'))
        return
    def query(self, command):
        BUFSIZ = 1024
        self.inst.send(bytes('%s\n' %command, 'utf-8'))
        return self.inst.recv(BUFSIZ).decode()

    def unlock_controller(self):
        try:
            # 1. Unlock Ethernet:
            self.write('ULOC 1')
            unlock_state = self.query('ULOC?')
            # 2. Check Model:
            model = self.query('*IDN?')
            print(Fore.YELLOW + "Unlock %s: %s" %(model, unlock_state))
            input(Fore.GREEN + "Press ENTER to proceed. ")
        except:
            print(Fore.RED + "Check SX199 physical connection")


def setup(IP_ADDR):
    inst = telnet()
    inst.unlock_controller()

    # 3. Set Netmask:
    print("Netmask: %s.%s.%s.%s" %(inst.query('NMSK?0'),inst.query('NMSK?1'),inst.query('NMSK?2'),inst.query('NMSK?3')))
    inst.write('NMSK 2, 255')
    print("Netmask: %s.%s.%s.%s" %(inst.query('NMSK?0'),inst.query('NMSK?1'),inst.query('NMSK?2'),inst.query('NMSK?3')))

    # 4. Set Gateway:
    print("Gateway: %s.%s.%s.%s" %(inst.query('GWAY?0'),inst.query('GWAY?1'),inst.query('GWAY?2'),inst.query('GWAY?3')))
    inst.write('GWAY 0, 192; GWAY 1, 168; GWAY 2, 1; GWAY 3, 1;')
    print("Gateway: %s.%s.%s.%s" %(inst.query('GWAY?0'),inst.query('GWAY?1'),inst.query('GWAY?2'),inst.query('GWAY?3')))

    # 5. IP Address:
    print("IP Address: %s.%s.%s.%s" %(inst.query('IPAD?0'),inst.query('IPAD?1'),inst.query('IPAD?2'),inst.query('IPAD?3')))
    inst.write('IPAD 0, %s; IPAD 1, %s; IPAD 2, %s; IPAD 3, %s;' %tuple(IP_ADDR.split('.')))
    # print("IP Address: %s.%s.%s.%s" %(inst.query('IPAD?0'),inst.query('IPAD?1'),inst.query('IPAD?2'),inst.query('IPAD?3')))

    # 6. Save Parameters:
    inst.write('SPAR 0')
    # inst.write('*RST')

    # 7. Close connection:
    inst.close()

def test(IP_ADDR):
    inst = telnet(Device_IP_Address=IP_ADDR, Device_Port=8888)
    inst.unlock_controller()


# STEP-1: connect to a router with 10.0.0 network-environment which connected to a different network card, while the jumpers also set to 10.0.0.106 IP
# test('10.0.0.206')

# STEP-2: make sure new IP doesn't have conflicts with others before making changes
# setup('192.168.1.45')  # Chosen-IP: 192.168.1.44,45,46...

# STEP-3: connect back to PiQuM network-environment, with the jumpers set to custom IP
test('192.168.1.45')

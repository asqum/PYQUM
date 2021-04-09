"""SRSDC TEST"""

import socket
from time import sleep

s = socket.socket()
s.connect(("192.168.1.44", 8888))
s.settimeout(7)

try:
    s.send(b'ULOC 1\n')
    s.send(b'ULOC?\n')
    print(s.recv(1024).decode())
    s.send(b'*IDN?\n')
    print(s.recv(1024).decode())
except:
    pass

s.send(b'LINK 1\n')
s.send(b'*OPC?\n')
s.recv(1024).decode()
s.send(b'VOLT 7.3e-5; VOLT?\n')
print(float(s.recv(1024).decode()))
s.send(b'!\n')

s.send(b'LINK 1\n')
s.send(b'*OPC?\n')
s.recv(1024).decode()
s.send(b'VOLT 4.3e-5; VOLT?\n')
print(float(s.recv(1024).decode()))
s.send(b'!\n')

s.send(b'LINK 1\n')
s.send(b'*OPC?\n')
s.recv(1024).decode()
s.send(b'VOLT 4.1e-5; VOLT?\n')
print(float(s.recv(1024).decode()))
s.send(b'!\n')

s.close()
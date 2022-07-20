'''REFERENCES\n
    Temporary code snippets will be put here for easy reference during development
'''

import struct, ast, os

# Truncating and Appending to File's content:
from os import SEEK_END
from random import random as rd
with open('data.star', 'rb+') as star:
    steps = 2
    file_position = star.seek(-steps, SEEK_END)
    print("\nWe are now at position %s after %s step(s) back-seeking in data.star" %(file_position, steps))
    star.truncate()
    star.write(bytes(', ', 'ascii'))
    star.write(bytes('{:.0f}'.format(rd()*100), 'ascii'))
    star.write(bytes(']}', 'ascii'))

# Inserting IEEE-754 data
with open('data.utf', 'rb+') as star:
    steps = 1
    file_position = star.seek(-steps, SEEK_END)
    print("\nWe are now at position %s after %s step(s) back-seeking in data.utf" %(file_position, steps))
    star.truncate()
    star.write(bytes(", 'z':", 'ascii'))
    D = f_dict['z'] # it's a list
    s = struct.pack('>' + 'd'*len(D), *D) # f:32bit, d:64bit each floating-number
    star.write(b'\x05' + s + b'\x06')
    star.write(bytes("}", 'ascii'))

print('After inserted d-64-array, data.utf: ', os.path.getsize('data.utf'), 'bytes (utf-8 encoding)\n')

# *** Read-out the IEEE-754 data-array ***
datastring = ''
with open('data.utf','rb') as bin_file: #use rb to read as binary
    bin_file.seek(0)
    full_read = bin_file.read()
    float_start = full_read.find(b'\x05') #ENQ (Enquiry)
    float_end = full_read.find(b'\x06') #ACK (Acknowledge)
    print("IEEE-data starts from location-%s" %float_start)
    print("and it ends at location-%s\n" %float_end)
    bin_file.seek(0)
    bin_read = bin_file.read(float_start)
    datastring += bin_read.decode('utf-8')
    bin_file.seek(float_start+1) #skip floating-marker-byte \x07 (start)
    z_read = bin_file.read(float_end-float_start-1)
    print("The length of the floating-points: %s" %((float_end-float_start-1)//8))
    unfloat = struct.unpack('>' + 'd'*((float_end-float_start-1)//8), z_read) #unpacking IEEE-754 encoded float-points
    datastring += str(list(unfloat))
    bin_file.seek(float_end+1) #skip floating-marker-byte \x08 (end)
    bin_read = bin_file.read()
    datastring += bin_read.decode('utf-8')
    # print("data-string:\n %s" %datastring)

# Reconstructing byte-data into dictionary
data_reconstructed = ast.literal_eval(datastring)
print('data.utf: David:', data_reconstructed['David'])
ans = data_reconstructed['David'][0] + data_reconstructed['David'][6]
print('1 + 7 = ', ans)
print('data.utf: a list:', data_reconstructed['a list'])
print('data.utf: z[:12]:', data_reconstructed['z'][:12])
print('data.utf: z[2]+z[-1]: %s' %(data_reconstructed['z'][2] + data_reconstructed['z'][-1]))
print('data.utf: x:', data_reconstructed['x'])
print('data.utf: y:', data_reconstructed['y'])


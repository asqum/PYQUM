'''To simulate every measurement process'''

from time import sleep
from numpy import array, append, zeros, prod, floor, inner
from pyqum.instrument.logger import measurement as meas

def cdatadecoder(Order, Structure):
    ''' Order: cdata-location (collective index)\n
        Structure = cdata-structure (how many bases for each hierarchy/level)
                    e.g. [cN#, c(N-1)#, ... , c3#, c2#, c1#], [10, 10, 7, 24, 35, 2]
    '''
    Address, Structure = [], array(Structure)
    Digitmax = len(Structure)
    Structure = append(Structure, [1])
    for i in range(Digitmax):
        Address.append(floor(((Order)%prod(Structure[i:]))/prod(Structure[i+1:])))  
    return Address

def cdataencoder(Address, Structure):
    S = []
    for i in range(len(Structure)):
        S.append(prod(Structure[i+1:]))
    Order = inner(Address, S)
    return Order
        
for i in range(150):
    print("decoding data-%s into c-%s and back into %s" 
    %(i, cdatadecoder(i, [8,10,10,2]), cdataencoder(cdatadecoder(i, [8,10,10,2]), [8,10,10,2])))
    # sleep(0.3)


def test():
    M = meas({'a':'b'}, [100, 100])
    M.log([0,0])

test()
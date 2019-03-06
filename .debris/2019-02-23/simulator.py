'''To simulate every measurement process'''

from time import sleep
from numpy import array, append, zeros, prod, floor, inner
from pyqum.instrument.logger import measurement as meas

def cdatasearch(Order, Structure):
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

def gotocdata(Address, Structure):
    S = []
    for i in range(len(Structure)):
        S.append(prod(Structure[i+1:]))
    Order = inner(Address, S)
    return Order
        
for i in range(150):
    print("decoding data-%s into c-%s and back into %s" 
    %(i, cdatasearch(i, [8,10,10,2]), gotocdata(cdatasearch(i, [8,10,10,2]), [8,10,10,2])))
    # sleep(0.3)


def test():
    M = meas({'a':'b'}, dict(c1=[0,1,2,3,4,5], c2=[0.1,0.2,0.3]))
    M.log([0,0])
    from pyqum.directive.Characterize import TESTC

test()

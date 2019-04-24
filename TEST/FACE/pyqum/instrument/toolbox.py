'''TOOLBOX for all other modules'''

from time import sleep
from numpy import array, append, zeros, prod, floor, inner, linspace

def cdatasearch(Order, Structure):
    ''' Give the address of the data essentially!
        Order: cdata-location (collective index)\n
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
    '''Give the order / entry of the data'''
    S = []
    for i in range(len(Structure)):
        S.append(prod(Structure[i+1:]))
    Order = inner(Address, S)
    return Order

def waveform(command):
    command = command.replace(" ","")
    command = command.split("*")
    C = []
    for c in command:
        C += c.split("to")

    C = [float(x) for x in C] #float all the string elements!
    start, wave = C[0], []
    for target,num in zip(C[1::2],C[2::2]):
        if num == C[-1]:
            wave += list(linspace(start, target, num))
        else:
            wave += list(linspace(start, target, num, endpoint=False))
            start = target
        
    return wave


def test():
    for i in range(150):
        print("decoding data-%s into c-%s and back into %s" 
        %(i, cdatasearch(i, [8,10,10,2]), gotocdata(cdatasearch(i, [8,10,10,2]), [8,10,10,2])))
        # sleep(0.3)
    command = "0 to  10  * 7 to  20 *15 to35*  13"
    print("Waveform of length %s is:\n %s" %(len(waveform(command)), waveform(command)))
    return


# test()

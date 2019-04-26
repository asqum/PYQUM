'''TOOLBOX for all other modules'''

from time import sleep
from numpy import array, append, zeros, prod, floor, inner, linspace, float64

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

class waveform:
    def __init__(self, command):
        self.command = command
        command = command.lower().replace(" ","").split("*")
        C = [j for i in command for j in i.split('to')]
        # rooting out wrong command:
        try:
            C = [float(x) for x in C] #float all the string elements!
            start, self.data, self.count = C[0], [], 0
            change = range(int(len(C[:-1])/2))
            for i,target,num in zip(change,C[1::2],C[2::2]):
                self.count += int(num)
                self.data += list(linspace(start, target, int(num), endpoint=bool(i==change[-1]), dtype=float64))
                start = target
        except:
            print("Invalid command")
            pass


def test():
    # for i in range(150):
    #     print("decoding data-%s into c-%s and back into %s" 
    #     %(i, cdatasearch(i, [8,10,10,2]), gotocdata(cdatasearch(i, [8,10,10,2]), [8,10,10,2])))
        # sleep(0.3)
    command = "0 to  10  * 7 TO  20 *15 to35*  13"
    wave = waveform(command)
    print("Waveform of length %s is:\n %s" %(wave.count, wave.data))
    return


# test()

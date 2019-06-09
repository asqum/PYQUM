'''TOOLBOX for all other modules'''

from time import sleep
from numpy import array, append, zeros, prod, floor, inner, linspace, float64, abs, argmin

def cdatasearch(Order, Structure):
    ''' Give the address of the data essentially!
        Order: cdata-location (collective index)\n
        Structure = cdata-structure (how many bases for each hierarchy/level)
                    e.g. [cN#, c(N-1)#, ... , c3#, c2#, c1#], [10, 10, 7, 24, 35, 2]
        \nNote: 
            Order & Address are index-type(0,1,2...); 
            Structure is count-type(1,2,3...): [slow(high-level) to fast(low-level)]
    '''
    Address, Structure = [], array(Structure)
    Digitmax = len(Structure)
    Structure = append(Structure, [1])
    for i in range(Digitmax):
        dgit = floor(((Order)%prod(Structure[i:]))/prod(Structure[i+1:]))
        Address.append(int(dgit))  
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
        # defaulting to lower case
        self.command = command.lower()
        # get rid of multiple spacings
        while " "*2 in self.command:
            self.command = self.command.replace(" "*2," ")
        # get rid of spacing around keywords
        while " *" in self.command or "* " in self.command:
            self.command = self.command.replace(" *","*")
            self.command = self.command.replace("* ","*")
        while " to" in self.command or "to " in self.command:
            self.command = self.command.replace(" to","to")
            self.command = self.command.replace("to ","to")

        command = self.command.split(" ")
        command = [x for x in command if x is not ""]
        self.data, self.count = [], 0
        for cmd in command:
            self.count += 1
            if "*" in cmd and "to" in cmd:
                C = [j for i in cmd.split("*") for j in i.split('to')]
                # rooting out wrong command:
                try:
                    start = float(C[0])
                    steps = range(int(len(C[:-1])/2))
                    for i,target,num in zip(steps,C[1::2],C[2::2]):
                        self.count += int(num)
                        self.data += list(linspace(start, float(target), int(num), endpoint=False, dtype=float64))
                        # print("data: %s"%self.data)
                        if i==steps[-1]: self.data += [float(target)]
                        else: start = float(target)
                except:
                    print("Invalid command")
                    pass
            else: self.data.append(float(cmd))

def match(List, Value):
    '''matching closest value in a list
    and return the index thereof
    '''
    index = abs(array(List) - Value).argmin()
    return index


def test():
    for i in range(700):
        print("decoding data-%s into c-%s and back into %s" 
        %(i, cdatasearch(i, [8,10,10,2]), gotocdata(cdatasearch(i, [8,10,10,2]), [8,10,10,2])))
        # sleep(0.3)
    command = "1 to 1 * 0"
    # command = "0 1   2   to  10  * 1 TO  20  *1 25 26  to35*  1to 70 *  5 73  75   to80  *5 81 82 to  101*  8"
    # command = "100    12  37              77   81  "
    # command = '1 to 10 *           12 to     25 *    7'
    wave = waveform(command)
    if wave.count == len(wave.data):
        print("Waveform of length %s is:\n %s" %(wave.count, wave.data))

    s = [0,0.5,1,1.5,2,2.5,3,3.5,4,5,6,7,8,10,12,13,15]
    idx = match(s, 7.3)
    print("7.3 is nearest to %s at index %s of s" %(s[idx],idx))

    return


# test()

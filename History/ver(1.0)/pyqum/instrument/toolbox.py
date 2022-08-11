'''TOOLBOX for all other modules'''

import logging
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
    return int(Order)

class waveform:
    '''Guidelines for Command writing:
        1. All characters will be converted to lower case
        2. Use comma separated string to represent string list
    '''
    def __init__(self, command):
        # defaulting to lower case
        self.command = command.lower()

        # special treatment to inner-repeat command:
        self.inner_repeat = 1
        if ' r ' in self.command:
            # inner_repeat: the repeat-counts indicated after the ' r ', determining how every .data's element will be repeated
            # correcting back ("auto-purify") the command-string after having retrieved repeat-count:
            self.command, self.inner_repeat = self.command.split(' r ')
            while " " in self.inner_repeat:
                self.inner_repeat = self.inner_repeat.replace(" ","")
            self.inner_repeat = int(self.inner_repeat)

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
        
        command = self.command.split(" ") + [""]
        # 1. building function generator:
        if command[0].lower() == "fx":
            pass
        # 2. building string list:
        elif ("," in command[0]) or ("," in command[1]):
            # remove all sole-commas from string list command:
            command = [x for x in command if x != ',']
            # remove all attached-commas from string list command:
            command = [i for x in command for i in x.split(',') if i != '']
            self.data = command
            self.count = len(command)
        # 3. building linear numbers
        else:
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

def squarewave(totaltime, ontime, delay, scale=1, dt=0.8, diff=False):
    '''time-unit: ns
        totaltime: total duration (minimum: 1000*0.8ns ~ 1us)
        ontime: +1V duration
        delay: duration before ontime
        scale: -1 to 1 output level
        dt: time-resolution of AWG in ns
        diff: 0V -> -1V if True
    '''
    delaypoints = round(delay / dt)
    onpoints = round(ontime / dt)
    offpoints = round((totaltime - ontime - delay) / dt)
    padding = 8 - (delaypoints + onpoints + offpoints)%8 # so that total-points is the multiples of 8
    if diff: Voff = -scale
    else: Voff = 0
    wave = [Voff] * delaypoints + [scale] * onpoints + [Voff] * (offpoints + padding)
    return wave


def match(List, Value):
    '''matching closest value in a list
    and return the index thereof
    '''
    index = abs(array(List) - Value).argmin()
    return index

# pause logging for some route:
def pauselog():
	log = logging.getLogger('werkzeug')
	log.disabled = True
	return log


def test():
    # for i in range(700):
    #     print("decoding data-%s into c-%s and back into %s" 
    #     %(i, cdatasearch(i, [8,10,10,2]), gotocdata(cdatasearch(i, [8,10,10,2]), [8,10,10,2])))
        # sleep(0.3)
    print("location: %s" %(cdatasearch(8080807, [1,4,101,20002])))
    # converting between addresses with different base structure:
    c_struct = [10, 5, 35, 15]
    c_struct.append(c_struct.pop(c_struct.index(5)))
    C_order_corrected = []
    for a in range(c_struct[0]):
        for b in range(c_struct[1]):
            for c in range(c_struct[2]):
                for d in range(c_struct[3]):
                    C_order_corrected.append(gotocdata([a,d,b,c], [10, 5, 35, 15]))
    print("This much has just stand corrected: %s" %len(C_order_corrected))

    # command = "1 to 1 * 0"
    # command = "0 1   2   to  10  * 1 TO  20  *1 25 26  to35*  1to 70 *  5 73  75   to80  *5 81 82 to  101*  8"
    # command = "100    12  37              77   81  "
    # command = '1 to 10 *           12 to     25 *    7'
    # command = ",s12 ,s21, s22,s11 ,   S22,S12,S21"
    command = "S,"
    # command = "10.0to0.0*1"
    wave = waveform(command)
    if wave.count == len(wave.data):
        print("Waveform of length %s is:\n %s" %(wave.count, wave.data))

    s = [0,0.5,1,1.5,2,2.5,3,3.5,4,5,6,7,8,10,12,13,15]
    idx = match(s, 7.3)
    print("7.3 is nearest to %s at index %s of s" %(s[idx],idx))

    return


# test()


'''For building, extracting, searching....... '''

import logging, collections
from time import sleep
from numpy import array, append, zeros, prod, floor, inner, linspace, float64, abs, argmin, dot, int64, sum, flip, cumprod, matmul, transpose, ones

def flatten(x):
    result = []
    for el in x:
        if isinstance(x, collections.Iterable) and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

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
        dgit = floor(((Order)%prod(Structure[i:],dtype=int64))/prod(Structure[i+1:],dtype=int64))
        Address.append(int(dgit))  
    return Address

def gotocdata(Address, Structure):
    '''Give the Order / Entry of the data
        Address: can be a stack of arrays of parameter-settings to form 2D-matrix
        Structure: an 1D-array of the NUMBER/COUNT of variables for each parameter in the data structure
    '''
    Address = array(Address,dtype=int64)
    Structure = array(Structure,dtype=int64)
    try:
        if Structure.ndim == 1:
            S = flip(cumprod(flip(Structure)))
            S[:-1] , S[-1] = S[1:] , 1
            Order = matmul(Address, S)
        # if Structure.ndim == 2: # Allow 2D-Address (Still PENDING)
        #     S = flip(cumprod(flip(Structure),axis=1))
        #     # print("Address: %s, Structure: %s, S: %s" %(str(Address.shape), str(array(Structure).shape), str(S.shape)))
        #     S[:, :-1] , S[:, -1] = S[:, 1:] , ones(len(S[:, -1]))
        #     Order = matmul(Address, transpose(S)).diagonal().astype(int)
        #     print("Order: %s"%Order)
    except: print("Please Check if the Structure dimension is 1D")
    return Order

class waveform:
    '''Guidelines for Command writing:\n
        1. All characters will be converted to lower case.\n
        2. Use comma separated string to represent string list.\n
        3. Inner-Repeat is ONLY used for CW_SWEEP: MUST use EXACTLY ' r ' (in order to differentiate from r inside word-string).\n
        4. waveform.inner_repeat: the repeat-counts indicated after the ' r ' or '^', determining how every .data's element will be repeated.\n
        NOTE: '^' is equivalent to ' r ' without any spacing restrictions.
    '''
    def __init__(self, command):
        # defaulting to lower case
        command = str(command)
        self.command = command.lower()

        # special treatment to inner-repeat command: (to extract 'inner_repeat' for cwsweep averaging)
        self.inner_repeat = 1
        if ' r ' in self.command:
            self.command, self.inner_repeat = self.command.split(' r ')
            while " " in self.inner_repeat: self.inner_repeat = self.inner_repeat.replace(" ","")
            self.inner_repeat = int(self.inner_repeat)
        if '^' in self.command:
            self.command, self.inner_repeat = self.command.split('^')
            while " " in self.inner_repeat: self.inner_repeat = self.inner_repeat.replace(" ","")
            self.inner_repeat = int(self.inner_repeat)

        # correcting back ("auto-purify") the command-string after having retrieved the repeat-count or not:
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
        # 1. building function generator: (Still PENDING, Refer 'composer')
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
            command = [x for x in command if x != ""]
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

def normalize_dipeak(arr):
    '''unidirectional normalization'''
    arr = array(arr)
    if abs(max(arr)) >= abs(min(arr)): arr = (arr - min(arr)) / (max(arr) - min(arr)) # 0 < x < 1
    elif abs(max(arr)) < abs(min(arr)): arr = (arr - max(arr)) / (max(arr) - min(arr)) # -1 < x < 0
    return arr

# pause logging for some route:
def pauselog():
	log = logging.getLogger('werkzeug')
	log.disabled = True
	return log


def test():
    # for i in range(100):
    #     print("decoding data-%s into c-%s and back into %s" 
    #     %(i, cdatasearch(i, [8,7,10,2]), gotocdata(cdatasearch(i, [8,7,10,2]), [8,7,10,2])))
    #     sleep(2)
    
    # print("location: %s" %(gotocdata([0,8,88,778], [1,100,1000,10000])))
    # print("First check:")
    # print("address: %s" %(cdatasearch(gotocdata([0,79,333,8888,12356], [1,100,1000,10000,1000000]), [1,100,1000,10000,1000000])))
    # print("Second check (List of Addresses):")
    # for x in gotocdata([[0,79,333,5271,12356]]*6 + [[0,79,333,5271,12357]]*1, [1,100,1000,10000,1000000]):
    #     print("address: %s" %(cdatasearch(x, [1,100,1000,10000,1000000])))
    # print("Third check (Array of Addresses):")
    # A = [0,79,333,5271,12356]
    # B = ones([8,1])*array(A)
    # B[:,-1] = range(12300,12308,1)
    # for x in gotocdata(B, [1,100,1000,10000,1000000]):
    #     print("address: %s" %(cdatasearch(x, [1,100,1000,10000,1000000])))
    
    # converting between addresses with different base structure:
    # c_struct = [10, 5, 35, 15]
    # c_struct.append(c_struct.pop(c_struct.index(5)))
    # C_order_corrected = []
    # for a in range(c_struct[0]):
    #     for b in range(c_struct[1]):
    #         for c in range(c_struct[2]):
    #             for d in range(c_struct[3]):
    #                 C_order_corrected.append(gotocdata([a,d,b,c], [10, 5, 35, 15]))
    # print("This much has just stand corrected: %s" %len(C_order_corrected))

    # command = "1 to 1 * 0"
    # command = "0 1   2   to  10  * 1 TO  20  *1 25 26  to35*  1to 70 *  5 73  75   to80  *5 81 82 to  101*  8"
    # command = "100    12  37              77   81  "
    # command = '1 to 10 *           12 to     25 *    7'
    # command = ",s12 ,s21, s22,s11 ,   S22,S12,S21"
    # command = "S,"
    # command = "10.0to0.0*1"
    command = "1e-6 to 5e-6 *4"
    wave = waveform(command)
    if wave.count == len(wave.data):
        print("Waveform of length %s is:\n %s" %(wave.count, wave.data))

    command = "5to12*7   ^100"
    wave = waveform(command)
    print("data %s is repeating %s times" %(wave.data,wave.inner_repeat))

    # s = [0,0.5,1,1.5,2,2.5,3,3.5,4,5,6,7,8,10,12,13,15]
    # idx = match(s, 7.3)
    # print("7.3 is nearest to %s at index %s of s" %(s[idx],idx))

    print(normalize_dipeak([0,0,0,-0.3,-0.3,-0.3,0,0]))

    return


# test()


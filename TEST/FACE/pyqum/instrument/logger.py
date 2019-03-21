'''For logging file'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from pathlib import Path
from os import stat, SEEK_END
from os.path import exists, getsize
from datetime import datetime
from time import time, sleep
from contextlib import suppress
from numpy import prod, mean, rad2deg
import inspect, json, wrapt, struct, geocoder, ast

from pyqum.instrument.toolbox import cdatasearch

__author__ = "Teik-Hui Lee"
__copyright__ = "Copyright 2019, The Pyqum Project"
__credits__ = ["Chii-Dong Chen"]
__license__ = "GPL"
__version__ = "beta3"
__email__ = "teikhui@phys.sinica.edu.tw"
__status__ = "development"

pyfilename = inspect.getfile(inspect.currentframe()) # current pyscript filename (usually with path)
INSTR_PATH = Path(pyfilename).parents[2] / "INSTLOG" # 2 levels up the path
USR_PATH = Path(pyfilename).parents[2] / "USRLOG"

def location():
    place = []
    # approximate radius of earth in km
    eaRth = 6373.0
    # acceptable distance error in km
    toleratekm = 0.00000001
    toleratedeg = rad2deg(toleratekm / eaRth)
    g = geocoder.ip('me')
    gps = g.latlng #[latitude, longitude]
    if mean([abs(i-j) for i,j in zip(gps, [25.0478, 121.532])]) < toleratedeg:
        place.append('AS')
    if mean([abs(i-j) for i,j in zip(gps, [25.0478, 121.532])]) < toleratedeg*10:
        place.append('Taipei')
    
    return place

def clocker(stage, prev=0):
    now = time()
    duration = now - prev
    if int(stage) > 0:
        print(Fore.BLUE + Back.WHITE + "It took {:.5f}s to complete {:d}-th stage\n".format(duration, stage))
    stage += 1
    return stage, now

def status_code(status):
    if status == 0:
        return "Success!"
    else: return "error %s" % status

def output_code(output):
    if output == "1":
        return "ON"
    elif output == "0":
        return "OFF"

def loginstr(instr_name):
    '''[Existence, Assigned Path] = loginstr(Instrument's name)
    '''
    pyqumfile = instr_name + "status.pyqum"
    pqfile = Path(INSTR_PATH) / pyqumfile
    existence = exists(pqfile) and stat(pqfile).st_size > 0
    return existence, pqfile

def get_status(instr_name):
    '''Get Instrument Status from LOG
    '''
    instr_log = loginstr(instr_name)
    if instr_log[0] == False:
        instrument = None # No such Instrument
    else:
        with open(instr_log[1]) as jfile:
            instrument = json.load(jfile) # in json format
    return instrument

def set_status(instr_name, info):
    '''Set Instrument Status for LOG
    * <info> must be a DICT'''
    instrument = get_status(instr_name)
    if instrument is None:
        instrument = {}
    instrument.update(info)
    with open(loginstr(instr_name)[1], 'w') as jfile:
        json.dump(instrument, jfile)

class address:
    '''Use Built-in Params as Default
    Set <reset=False> to directly load from LOG if it contains "address" 
    '''
    def __init__(self):
        self.book = json.load(open(Path(pyfilename).parent / 'address.json'))

    def lookup(self, instr_name, level=0):
        self.instr_name = instr_name
        self.level = level
        try:
            if self.level:
                self.rs = self.book[self.instr_name]["alternative"][self.level-1]
            else: self.rs = self.book[self.instr_name]["resource"]
        except(KeyError): self.rs = None # checking if instrument in database
        return self.rs

    def visible(self):
        self.vis = []
        for k,v in self.book.items():
            if v["visible"]:
                self.vis.append(k)
        return self.vis

    def update_status(self):
        set_status(self.instr_name,dict(address=self.rs))
    
# Debugger settings
def debug(mdlname, state=False):
    debugger = 'debug' + mdlname
    exec('%s %s; %s = %s' %('global', debugger, debugger, 'state'), globals(), locals()) # open global and local both-ways channels!
    if state:
        print(Back.RED + '%s: Debugging Mode' %debugger.replace('debug', ''))
    return eval(debugger)

# SCPI Translator
@wrapt.decorator
def translate_scpi(Name, instance, a, b):
    
    mdlname, bench, SCPIcore, action = Name(*a, **b)
    debugger = 'debug' + mdlname
    SCPIcore = SCPIcore.split(";")
    headers = SCPIcore[0].split(':')
    parakeys, paravalues, getspecific, command = [headers[-1]] + SCPIcore[1:], [], [], []

    if action[0] == 'Get':
        try:
            for i in range(len(parakeys)):
                if len(str(action[i+1])) > 0: #special type of query (e.g. commentstate)
                    getspecific.append(" " + str(action[i+1]))
                else: getspecific.append('')
                command.append(parakeys[i] + "?" + getspecific[i])

            command = ':'.join(headers[:-1] + [";".join(command)])
            paravalues = bench.query(command).split(';')
            #just in case of the presence of query parameters, which is rare
            paravalues = [paravalues[i] + '(' + str(action[i+1]) + ')' for i in range(len(parakeys))]
            paravalues = [x.replace('()', '') for x in paravalues]

            status = "Success"
        except: # get out of the method with just return-value at exception?
            status = "query unsuccessful"
            ans = None

    if action[0] == 'Set':

        for i in range(len(parakeys)):
            if str(action[i+1]) == '':
                paravalues.append("NIL") # allow for arbitrary choosing
            elif ' ' in str(action[i+1]) and not "'" in str(action[i+1]): #set parameters for each header by certain parakey
                actionwords = str(action[i+1]).split(' ')
                oddwords, evenwords, J = actionwords[1::2], actionwords[0::2], []
                # print("Odd: %s; Even: %s"%(oddwords,evenwords))
                for j,h in enumerate(headers):
                    for w,word in enumerate(oddwords):
                        if evenwords[w].upper() in h.upper(): #only need to type part of the header(core)!
                            headers[j] = h.upper() + word
                            J.append(j)
                statement = ','.join([headers[sel] for sel in J])    
                paravalues.append(statement) #will appear in the <ans>
                command.append(parakeys[i])
            else: 
                paravalues.append(str(action[i+1]))
                command.append(parakeys[i] + " " + paravalues[i])

        command = ':'.join(headers[:-1] + [";".join(command)])
        status = str(bench.write(command)[1])[-7:]
        
    # formatting return answer
    ans = dict(zip([a.replace('*','') for a in parakeys], paravalues))

    # Logging answer
    if action[0] == 'Get': # No logging for "Set"
        set_status(mdlname, {Name.__name__ : ans})

    # debugging
    if eval(debugger):
        print(Fore.LIGHTBLUE_EX + "SCPI Header: {%s}" %headers[:-1])
        print(Fore.CYAN + "SCPI Command: {%s}" %command)
        if action[0] == 'Get':
            print(Fore.YELLOW + "%s %s's %s: %s <%s>" %(action[0], mdlname, Name.__name__, ans, status))
        if action[0] == 'Set':
            print(Back.YELLOW + Fore.MAGENTA + "%s %s's %s: %s <%s>" %(action[0], mdlname, Name.__name__ , ans, status))

    return status, ans

class measurement:
    '''Initialize Measurement:\n
        corder: {parameters: [...], instruments: [...], ranges: [...]}\n
    '''
    def __init__(self, mission, task, corder, usr_name='USR', place='Unknown', sample='Sample', comment=''):
        self.mission = mission
        self.task = task
        self.corder = corder
        self.usr_name = usr_name
        self.place = place
        self.sample = sample
        self.comment = comment #to be appended to data after ACK-mark

        # assembly day & moment
        now = datetime.now()
        day = now.strftime("%Y-%m-%d(%a)")
        moment = now.strftime("%H:%M")

        # assembly file-name:
        filename = "%s.pyqum" %task
        self.pqfile = Path(USR_PATH) / self.usr_name / self.sample / mission / day / filename
        
        # assembly the file-header(time, place, mission, task, c-parameters):
        usr_bag = bytes("{'%s': {'place': '%s', 'c-order': %s, 'data': " %(moment, place, corder), 'utf-8')
        usr_bag += b'\x05' + b'\x06' + bytes("}"*2, 'utf-8') # data container

        # check if the file exists and not blank:
        existence = exists(self.pqfile) and stat(self.pqfile).st_size > 0 #The beauty of Python: if first item is false, second item will not be evaluated in AND-statement, thus avoiding errors
        
        # write into file:
        if existence == False:
            self.pqfile.parent.mkdir(parents=True, exist_ok=True) #make directories
            with open(self.pqfile, 'wb') as datapie:
                # Initialize blank file
                datapie.write(usr_bag)
        else:
            with open(self.pqfile, 'rb+') as datapie:
                # Appending moment-log if it's already existed
                datapie.seek(-1, SEEK_END)
                datapie.truncate()
                datapie.write(bytes(", ", 'utf-8') + usr_bag[1:-1] + bytes("}", 'utf-8'))
    
    def log(self, data):
        '''Logging DATA from instruments on the fly
        '''
        data = struct.pack('>' + 'd', data) #f:32bit, d:64bit each floating-number
        try:
            with open(self.pqfile, 'rb+') as datapie:
                datapie.seek(-3, SEEK_END)
                datapie.truncate()
                datapie.write(data + b'\x06' + bytes("}"*2, 'utf-8'))  
        except: print("THE FILE WAS NOT WELL PREPARED. PLS RUN 'measurement' FIRST")              
        return

    def load(self):
        '''Get User's Data from LOG
        '''
        try:
            filesize = stat(self.pqfile).st_size
            with open(self.pqfile, 'rb') as datapie:
                Enq, Ack, datacontainer, buildcontainer = [], [], '', True
                for i in range(filesize):
                    datapie.seek(i)
                    bite = datapie.read(1)
                    if bite == b'\x05':
                        Enq.append(i)
                        buildcontainer = False
                        datacontainer += 'None'
                    elif bite == b'\x06':
                        Ack.append(i)
                        buildcontainer = True
                    else:
                        if buildcontainer:
                            datacontainer += bite.decode('utf-8')
                datacontainer = ast.literal_eval(datacontainer)
            self.datalocation = dict(zip(Enq, Ack)) 
        except:
            print("Measurement not initiated!")
        return datacontainer

    def get(self, entry=1):
        '''select data'''
        try:
            load = self.load()
            selectime = [k for k in load.keys()][entry-1]
            k, v = [k for k in self.datalocation.keys()][entry-1], [v for v in self.datalocation.values()][entry-1]
            with open(self.pqfile, 'rb') as datapie:
                datapie.seek(k+1)
                pie = datapie.read(v-k-1)
                selectedata = list(struct.unpack('>' + 'd'*((v-k-1)//8), pie))
        except: 
            print("out of range!")
        return selectime, selectedata

    def database(self):
        '''reconstructing the database in dictionary format'''
        book = self.load()
        for i,t in enumerate(book.keys()):
            book[t]['data'] = self.get(i+1)[1]
        return book

# C-Parameters Descriptor
def settings(place):
    @wrapt.decorator
    def wrapper(Name, instance, a, b):
        data = Name(*a, **b)
        mission = Path(inspect.stack()[1][1]).name.replace('.py','')
        task = Name.__name__
        Cnames = str(inspect.signature(Name)).replace('(','').replace(')','').split(', ')
        Carrays = list(inspect.getargvalues(inspect.currentframe()).locals['a'])
        Corders = dict(zip(Cnames, Carrays))
        datasize = prod([len(x) for x in Carrays])
        # print(datasize)
        M = measurement(mission, task, Corders, place=place)
        try:
            for x in data:
                # print(Fore.YELLOW + '\r %s' %x, end='\r')
                M.log(x)
                # sleep(0.006)
        except(KeyboardInterrupt): print(Fore.RED + "\nSTOPPED")
        print(M.get(1))
        # print(M.database()['00:50']['c-order'])
        return
    return wrapper


def test():
    L = location()
    print("We are now in %s" %L)
    ad = address()
    print(ad.lookup("YOKO"))
    print(ad.lookup("TEST", 2))
    print(ad.visible())
    return
    
# test()


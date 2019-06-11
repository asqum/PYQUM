'''For logging file'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from pathlib import Path
from os import listdir, stat, SEEK_END
from os.path import exists, getsize, getmtime, join, isdir
from datetime import datetime
from time import time, sleep
from contextlib import suppress
from numpy import prod, mean, rad2deg
import inspect, json, wrapt, struct, geocoder, ast

__author__ = "Teik-Hui Lee"
__copyright__ = "Copyright 2019, The Pyqum Project"
__credits__ = ["Chii-Dong Chen"]
__license__ = "GPL"
__version__ = "beta3"
__email__ = "teikhui@phys.sinica.edu.tw"
__status__ = "development"

pyfilename = inspect.getfile(inspect.currentframe()) # current pyscript filename (usually with path)
MAIN_PATH = Path(pyfilename).parents[6] / "MEGAsync" / "CONFIG"
INSTR_PATH = MAIN_PATH / "INSTLOG" # 2 levels up the path
USR_PATH = MAIN_PATH / "USRLOG"

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
    '''timing algorithm in seconds'''
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
        with open(MAIN_PATH / 'address.json') as ad:
            self.book = json.load(ad)

    def lookup(self, instr_name, level=0):
        '''level: alternative address's index (1,2,3...)'''
        self.instr_name = instr_name
        self.level = level
        try:
            if self.level: #False if 0
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
        1. Assembly Path based on Mission
        2. Checking Database (daylist)
    '''
    def __init__(self, mission, task, usr_name='USR', sample='Sample', comment=''):
        self.mission = mission
        self.task = task
        self.usr_name = usr_name
        self.sample = sample
        self.comment = comment #to be appended to data after ACK-mark

        self.mssnpath = Path(USR_PATH) / usr_name / sample / mission
        self.place = ", ".join(location()) #current location
        
        # FOR Resume / Access operation:
        try:
            daylist = [d for d in listdir(self.mssnpath) if isdir(self.mssnpath / d)]
            daylist.sort(key=lambda x: getmtime(self.mssnpath / x))
            self.daylist = daylist
        except:
            self.daylist = []
            print("database is EMPTY")
            pass

    # only for scripting
    def whichday(self):
        '''This can be replaced by HTML Forms Input'''
        total = len(self.daylist)
        for i,day in enumerate(['new']+self.daylist):
            print("%s. %s" %(i,day))
        while True:
            try:
                k = int(input("Which day would you like to check out (0:new, 1-%s): " %total))
                if k in range(total+1):
                    break
            except(ValueError):
                print("Bad index. Please use numeric!")
        return k-1 #index

    def selectday(self, index, corder={'c':[0,0,0]}):
        '''corder: {parameters: [ranges]}\n'''
        
        # New operation if "new" is selected:
        if index < 0:
            now = datetime.now() #current day & time
            self.day = now.strftime("%Y-%m-%d(%a)")
            self.moment = now.strftime("%H:%M:%f")
            # estimating data size from parameters:
            self.corder = corder
            self.resumepoint = 0
            task_index = 1
            while True:
                self.filename = "%s.pyqum(%s)" %(self.task, task_index)
                self.pqfile = self.mssnpath / self.day / self.filename

                # assembly the file-header(time, place, c-parameters):
                usr_bag = bytes("{'%s': {'place': '%s', 'c-order': %s, 'comment': '%s'}}" %(self.moment, self.place, self.corder, self.comment), 'utf-8')
                usr_bag += b'\x02' + bytes("ACTS", 'utf-8') + b'\x03\x04' # ACTS
                
                # check if the file exists and not blank:
                existence = exists(self.pqfile) and stat(self.pqfile).st_size > 0 #The beauty of Python: if first item is false, second item will not be evaluated in AND-statement, thus avoiding errors
                if existence == False:
                    self.pqfile.parent.mkdir(parents=True, exist_ok=True) #make directories
                    with open(self.pqfile, 'wb') as datapie:
                        # Initialize blank file w/ user bag
                        datapie.write(usr_bag)
                    break
                else:
                    task_index += 1
        # from database:
        else:
            try:
                self.day = self.daylist[index]
                print("Day selected: %s"%self.day)
                self.timelist = [int(t.split('(')[1][:-1]) for t in listdir(self.mssnpath / self.day) if t.split('.')[0] == self.task]
                self.timelist.sort(reverse=False) #ascending order
            except(ValueError): 
                print("index might be out of range")
                pass

    # only for scripting
    def whichmoment(self):
        '''This can be replaced by HTML Forms Input'''
        while True:
            try:
                k = int(input("Which moment would you like to check out (1-%s): " %self.timelist[-1]))
                if k in self.timelist:
                    break
            except(ValueError):
                print("Bad index. Please use numeric!")
        return k

    def selectmoment(self, entry):
        '''select data from time-log'''
        # select file in resume/access mode
        if entry:
            self.filename = "%s.pyqum(%s)" %(self.task, entry)
            self.pqfile = self.mssnpath / self.day / self.filename
            print("moment(file) selected: %s"%self.filename)
        return

    def listime(self):
        '''list all the logged time for each day
            Pre-requisite: selectday
        '''
        startimes = []
        for k in self.timelist:
            self.selectmoment(k)
            with open(self.pqfile, 'rb') as datapie:
                datapie.seek(2)
                bite = datapie.read(5)
                startimes.append(bite.decode('utf-8'))
        self.startimes = startimes
        print("For %s, we have: %s"%(self.day, ', '.join(self.startimes)))
        return

    def accesstructure(self):
        '''Get User-Data's container & location from LOG
            Pre-requisite: pqfile (from selectmoment / selectday)
        '''
        try:
            self.filesize = stat(self.pqfile).st_size
            with open(self.pqfile, 'rb') as datapie:
                i = 0
                while i < (self.filesize):
                    datapie.seek(i)
                    bite = datapie.read(7)
                    if bite == b'\x02' + bytes("ACTS", 'utf-8') + b'\x03\x04': # ACTS
                        self.datalocation = i
                        break
                    else: i += 1
                datapie.seek(0)
                bite = datapie.read(self.datalocation)
                datacontainer = bite.decode('utf-8')
                        
            print("Data locations: %s" %self.datalocation)           
            self.datacontainer = ast.literal_eval(datacontainer) # library w/o the data yet
            self.corder = [x for x in self.datacontainer.values()][0]['c-order']
            self.datasize = prod([x[2]+1 for x in self.corder.values()])
            # print("C-order: %s"%(self.corder))
        except:
            raise
            print("File structure invalid!")
        return

    def loadata(self):
        '''Loading the Data
            Pre-requisite: accesstructure
        '''
        try:
            with open(self.pqfile, 'rb') as datapie:
                datapie.seek(self.datalocation+7)
                pie = datapie.read(self.filesize-self.datalocation-7)
                self.selectedata = list(struct.unpack('>' + 'd'*((self.filesize-self.datalocation-7)//8), pie))
                if len(self.selectedata) == self.datasize:
                    self.data_complete = True
                    print("The Data is COMPLETE")
                else:
                    self.data_complete = False
                    self.resumepoint = len(self.selectedata)
                    print("The Data is NOT COMPLETE")
        except:
            print("\ndata not found")

    def insertdata(self, data):
        '''Logging DATA from instruments on the fly:
            By appending individual data-point to the EOF (defined by SEEK_END)
        '''
        # get data type:
        if type(data) is list:
            data = struct.pack(">" + "d"*len(data), *data)
        else: data = struct.pack('>' + 'd', data) #f:32bit, d:64bit each floating-number
        if not self.data_complete:
            with open(self.pqfile, 'rb+') as datapie:
                datapie.seek(0, SEEK_END) #seek from end
                # datapie.truncate()
                datapie.write(data)
        else: print("THE FILE IS COMPLETE. NO ACTION TAKEN")              
        return

    def buildata(self):
        '''build data into datacontainer'''
        self.datacontainer[next(iter(self.datacontainer))]['data'] = self.selectedata
        return

# Setting up Measurement
def settings():
    @wrapt.decorator
    def wrapper(Name, instance, a, b):
        Generator = Name(*a, **b)
        corders, comment, dayindex, taskentry, buffersize, resumepoint = next(Generator)
        mission = Path(inspect.getfile(Name)).parts[-1].replace('.py','') #Path(inspect.stack()[1][1]).name.replace('.py','')
        task = Name.__name__
        # Get the Arguments from function being wrapped
        # Argnames = str(inspect.signature(Name)).replace('(','').replace(')','').split(', ')
        # Argvalues = list(inspect.getargvalues(inspect.currentframe()).locals['a'])
        M = measurement(mission, task, comment=comment)
        if type(dayindex) is str:
            pass #access-only mode
        elif type(dayindex) is int:
            M.selectday(dayindex, corders)
            M.selectmoment(taskentry)
            M.accesstructure()
            M.loadata()
            # skip insertdata in access-only mode
            try:
                for i,x in enumerate(Generator): #yielding data from measurement-module
                    print(Fore.YELLOW + "\rProgress: %.3f%% [%s]" %((i+1)/(M.datasize-resumepoint)*buffersize*100, x), end='\r', flush=True)
                    M.insertdata(x)
                    sleep(1)
            except(KeyboardInterrupt): print(Fore.RED + "\nSTOPPED")
        
        # Measurement Object/Session:
        return M
    return wrapper

# TEST
def test():
    L = location()
    print("We are now in %s" %L)
    ad = address()
    print(ad.lookup("YOKO"))
    print(ad.lookup("TEST", 2))
    print(ad.visible())
    return
    
# test()


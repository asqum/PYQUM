'''For logging status, address and data'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from pathlib import Path
from os import mkdir, listdir, stat, SEEK_END
from os.path import exists, getsize, getmtime, join, isdir, getctime
from datetime import datetime
from time import time, sleep
from contextlib import suppress
from numpy import prod, mean, rad2deg, array
import inspect, json, wrapt, struct, geocoder, ast
from pandas import DataFrame
from tables import open_file, Filters, Float32Atom, Float64Atom, StringCol, IsDescription

from pyqum.instrument.toolbox import waveform

__author__ = "Teik-Hui Lee"
__copyright__ = "Copyright 2019, The Pyqum Project"
__credits__ = ["Chii-Dong Chen"]
__license__ = "GPL"
__version__ = "beta3"
__email__ = "teikhui@phys.sinica.edu.tw"
__status__ = "development"

pyfilename = inspect.getfile(inspect.currentframe()) # current pyscript filename (usually with path)
MAIN_PATH = Path(pyfilename).parents[7] / "HODOR" / "CONFIG"
INSTR_PATH = MAIN_PATH / "INSTLOG"
USR_PATH = MAIN_PATH / "USRLOG"
PORTAL_PATH = MAIN_PATH / "PORTAL"
ADDRESS_PATH = MAIN_PATH / "Address"
SPECS_PATH = MAIN_PATH / "SPECS"

def location():
    place = []
    # approximate radius of earth in km
    eaRth = 6373.0
    # acceptable distance error in km
    toleratekm = 0.00000001
    toleratedeg = rad2deg(toleratekm / eaRth)
    g = geocoder.ip('me')
    gps = g.latlng #[latitude, longitude]
    try:
        if mean([abs(i-j) for i,j in zip(gps, [25.0478, 121.532])]) < toleratedeg:
            place.append('AS')
        if mean([abs(i-j) for i,j in zip(gps, [25.0478, 121.532])]) < toleratedeg*10:
            place.append('Taipei')
    except: 
        print("Location service may not be available. Please check.")
        pass
    
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

# log, get & set status for both machines & missions (instr = real OR virtual instruments like tasks)
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

# save data in csv for export and be used by clients:
def set_csv(data_dict, filename):
    df = DataFrame(data_dict, columns= [x for x in data_dict.keys()])
    export_csv = df.to_csv(Path(PORTAL_PATH) / filename, index = None, header=True)
    return export_csv

class address:
    '''Use Built-in Params as Default
    Set <reset=False> to directly load from LOG if it contains "address" 
    '''
    def __init__(self):
        with open(ADDRESS_PATH / "address.json") as ad:
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

class specification:
    '''lookup specifications for each instruments
    '''
    def __init__(self):
        with open(SPECS_PATH / "specification.json") as spec:
            self.book = json.load(spec)
    def lookup(self, instr_name, characteristic):
        try: self.limit = self.book[instr_name][characteristic]['limit']
        except(KeyError): self.limit = None
        try: self.range = self.book[instr_name][characteristic]['range']
        except(KeyError): self.range = None
        return
    
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
                paravalues.append("NIL") # allow for arbitrary choosing (turn-off certain parameter(s))
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

# Execution
class measurement:
    '''Initialize Measurement:\n
        1. Assembly Path based on Mission
        2. Checking Database if any (daylist)
        3. Used for sending status to the front-end via JS
    '''
    def __init__(self, mission, task, usr_name='USR', sample='Sample', loopcount=[], loop_dur=[]):
        # Primary parameters (mission & task is auto-detected by OS)
        self.mission, self.task = mission, task
        self.usr_name, self.sample = usr_name, sample
        self.mssnpath = Path(USR_PATH) / usr_name / sample / mission
        self.loopcount, self.loop_dur = loopcount, loop_dur
        #current location
        self.place = ", ".join(location()) 
        
        # FOR Resume / Access operation:
        try:
            daylist = [d for d in listdir(self.mssnpath) if isdir(self.mssnpath / d)]
            print("There are %s days" %len(daylist))
            # filter out non task-specific
            relatedays = []
            for d in daylist:
                task_relevant_time = [t for t in listdir(self.mssnpath / d) if t.split('.')[0] == self.task]
                if task_relevant_time:
                    relatedays.append(d)
            relatedays.sort(key=lambda x: getctime(self.mssnpath / x))
            self.daylist = relatedays
        except:
            self.daylist = []
            print("Mission is EMPTY")
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

    # Secondary parameters
    def selectday(self, index, corder={}, instr=[], datadensity=1, comment='', tag=''):
        '''corder: {parameters: <waveform>}\n'''

        # New operation if "new" is selected:
        if index < 0:
            now = datetime.now() #current day & time
            self.day = now.strftime("%Y-%m-%d(%a)")
            self.moment = now.strftime("%H:%M:%f")
            # estimating data size from parameters:
            self.corder = corder
            self.instr = instr
            self.datadensity = datadensity
            self.comment = comment
            self.tag = tag
        
            task_index = 1
            while True:
                self.filename = "%s.pyqum(%s)" %(self.task, task_index)
                self.pqfile = self.mssnpath / self.day / self.filename

                # assembly the file-header(time, place, c-parameters):
                usr_bag = bytes('{"%s": {"place": "%s", "data-density": %s, "c-order": %s, "instrument": %s, "comment": "%s", "tag": "%s"}}' %(self.moment, self.place, self.datadensity, self.corder, self.instr, self.comment, self.tag), 'utf-8')
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
                self.taskentries = [int(t.split('(')[1][:-1]) for t in listdir(self.mssnpath / self.day) if t.split('.')[0] == self.task]
                self.taskentries.sort(reverse=False) #ascending order
            except(ValueError): 
                print("index might be out of range")
                pass

    # only for scripting
    def whichmoment(self):
        '''This can be replaced by HTML Forms Input'''
        while True:
            try:
                k = int(input("Which moment would you like to check out (1-%s): " %self.taskentries[-1]))
                if k in self.taskentries:
                    break
            except(ValueError):
                print("Bad index. Please use numeric!")
        return k

    def selectmoment(self, entry):
        '''select data from time-log'''
        # select file in resume/access mode (Please avoid -ve because bool(-ve) also returns TRUE)
        if entry:
            self.filename = "%s.pyqum(%s)" %(self.task, entry)
            self.pqfile = self.mssnpath / self.day / self.filename
        return

    def startime(self):
        '''return the started time for selected measurement file
            Pre-requisite: selectday, selectmoment
        '''     
        with open(self.pqfile, 'rb') as datapie:
            datapie.seek(2)
            bite = datapie.read(5)
            startime = bite.decode('utf-8')
        
        print("Measurement started at %s" %(startime))
        return startime

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
                        
            self.writtensize = self.filesize-self.datalocation-7           
            self.datacontainer = ast.literal_eval(datacontainer) # library w/o the data yet
            # Access library keys:
            self.corder = [x for x in self.datacontainer.values()][0]['c-order']
            self.datadensity = [x for x in self.datacontainer.values()][0]['data-density']
            self.comment = [x for x in self.datacontainer.values()][0]['comment']

            # Estimate data size based on version of your data:
            if 'C-Structure'in self.corder:
                self.datasize = int(prod([waveform(self.corder[param]).count * waveform(self.corder[param]).inner_repeat  for param in self.corder['C-Structure']], dtype='uint64')) * 2 #data density of 2 due to IQ
            else:
                self.datasize = prod([waveform(x).count * waveform(x).inner_repeat for x in self.corder.values()]) * self.datadensity

            self.data_progress = float(self.writtensize / (self.datasize*8) * 100)
            self.data_complete = (self.datasize*8==self.writtensize)
            self.data_overflow = (self.datasize*8<self.writtensize)
            Last_Corder = [i for i in self.corder.values()][-1] # for the last key of c-order
            self.data_mismatch = self.writtensize%waveform(Last_Corder).count*waveform(Last_Corder).inner_repeat*8 # counts & inner-repeats
            print(Back.WHITE + Fore.BLACK + "Data starts from %s-byth on the file with size of %sbytes" %(self.datalocation, self.filesize))
            if not self.writtensize%8:
                self.resumepoint = self.writtensize//8
            else:
                self.resumepoint = self.datasize
                print(Back.RED + "SKIP SAVING: REPAIR DATA FIRST!")
            
        except:
            raise
        return

    def loadata(self):
        '''Loading the Data
            Pre-requisite: accesstructure
        '''
        try:
            with open(self.pqfile, 'rb') as datapie:
                datapie.seek(self.datalocation+7)
                pie = datapie.read(self.writtensize)
                self.selectedata = list(struct.unpack('>' + 'd'*((self.writtensize)//8), pie))
        except:
            # raise
            print("\ndata not found")

    def insertdata(self, data):
        '''Logging DATA from instruments on the fly:
            By appending individual data-point to the EOF (defined by SEEK_END)
        '''
        # get data type:
        if type(data) is list:
            data = struct.pack(">" + "d"*len(data), *data)
        else: data = struct.pack('>' + 'd', data) #f:32bit, d:64bit each floating-number
        # inserting data:
        with open(self.pqfile, 'rb+') as datapie:
            datapie.seek(0, SEEK_END) #seek from end
            datapie.write(data)             
        return

    def buildata(self):
        '''build data into datacontainer'''
        self.datacontainer[next(iter(self.datacontainer))]['data'] = self.selectedata
        return

    def repairdata(self):
        '''Pre-requisite: accesstructure
        pending update: repair buffer mismatch'''
        ieee_mismatch = self.writtensize%8
        print("IEEE-754(64bit) mismatch: %sbytes"%ieee_mismatch)
        if ieee_mismatch:
            with open(self.pqfile, 'rb+') as datapie:
                datapie.seek(-ieee_mismatch, SEEK_END) #seek from end
                datapie.truncate()
            return "FILE IS REPAIRED"
        else: return "FILE IS GOOD"

    def resetdata(self,keepdata=0):
        '''Pre-requisite: accesstructure
            keepdata: the amount of data that you wanna save in sample#
            1 sample = 8 bytes
        '''
        with open(self.pqfile, 'rb+') as datapie:
            datapie.truncate(self.datalocation+7+keepdata*8)
        return "FILE IS RESET"
        
    def searchcomment(self, wday, keyword): # still pending
        filelist = []
        filelist += [(self.mssnpath / self.daylist[wday] / t) for t in listdir(self.mssnpath / self.daylist[wday]) if t.split('.')[0] == self.task]
        return filelist

    def mkanalysis(self, entry):
        '''
        prerequisite: selectmoment
        '''
        self.analysisfolder = "%s_analysis(%s)" %(self.task, entry)
        self.analysispath = self.mssnpath / self.day / self.analysisfolder
        try:
            mkdir(self.analysispath)
            status = "Folder <%s> created successfully" %self.analysisfolder
        except(FileExistsError):
            status = "Folder <%s> already existed" %self.analysisfolder
        except: status = "Check the path"
        return status

    def savanalysis(self, adataname, adatarray):
        '''
        prerequisite: accesstructure, mkanalysis
        '''
        m, n = adatarray.shape[0], adatarray.shape[1]
        with open_file(self.analysispath / (self.analysisfolder + ".h5"), 'w') as f:
            filters = Filters(complevel=5, complib='blosc')
            acontainer = f.create_carray(f.root, adataname, Float64Atom(), shape=(m, n), filters=filters)
            acontainer[:,:] = adatarray
            # Create a table in the root directory and append data...
            class About(IsDescription):
                task   = StringCol(len(self.task), pos=1)   # N-character String
                comment   = StringCol(len(self.comment), pos=2)   # N-character String
            tableroot = f.create_table(f.root, 'info', About, "A table at root", Filters(1))
            tableroot.append([(self.task, self.comment)]) # , ("Mediterranean", 11, -1, 11*11, 11**2), ("Adriatic", 12, -2, 12*12, 12**2)])

        return

    def loadanalysis(self, adataname, atype='matrix'):
        '''
        prerequisite: accesstructure, mkanalysis
        return: list
        '''
        with open_file(self.analysispath / (self.analysisfolder + ".h5"), 'r') as f:
            print ("\nContents of the table in root:\n", f.root.info[:])
            data = []
            if atype == 'matrix':
                loaded = eval('f.root.%s' %adataname)
                print ("\nMatrix Data shape: %s,%s" %loaded[:,:].shape)
                for aslice in loaded[:,:]:
                    data.append(aslice)

        return data

    def savenote(self):

        return


# Setting up Measurement (Law-maker)
def settings(datadensity=1):
    '''
    Before dayindex: freely customized by user
    From instr onward: value set is intrinsic to the task
    In-betweens: depends on mode / high interaction with the system
    Here will be executed first!
    '''
    @wrapt.decorator
    def wrapper(Name, instance, a, b):
        Generator = Name(*a, **b)
        usr_name, sample, tag, instr, corder, comment, dayindex, taskentry, testeach = next(Generator)
        mission = Path(inspect.getfile(Name)).parts[-1].replace('.py','') #Path(inspect.stack()[1][1]).name.replace('.py','')
        task = Name.__name__
        # print("task: %s" %task)
        M = measurement(mission, task, usr_name, sample) #M-Initialization
        if type(dayindex) is str:
            pass # Only M-Initialization (everytime when click a task)
        elif type(dayindex) is int:
            if testeach:
                M.loopcount, M.loop_dur = next(Generator)
            else:
                M.selectday(dayindex, corder, instr, datadensity, comment, tag)
                # print(Back.GREEN + "Day selected: %s"%self.day)
                M.selectmoment(taskentry)
                # print(Back.BLUE + "moment(file) selected: %s"%M.filename)
                try:
                    for i,x in enumerate(Generator): #yielding data from measurement-module
                        print('\n' + Fore.GREEN + 'Writing Data loop-%s' %i)
                        M.insertdata(x)
                        # sleep(3) #for debugging purposes
                except(KeyboardInterrupt): print(Fore.RED + "\nSTOPPED")

        # Measurement Object/Session:
        return M
    return wrapper

def lisample(usr):
    samples = [d for d in listdir(USR_PATH / usr) if isdir(USR_PATH / usr / d)]
    return samples

def lismission(usr, sample, mission):
    log = {}
    daylist = [d for d in listdir(USR_PATH / usr / sample / mission) if isdir(USR_PATH / usr / sample / mission /d)]
    return daylist

# TEST
def test():
    L = location()
    print("We are now in %s" %L)
    ad = address()
    print(ad.lookup("YOKO"))
    print(ad.lookup("TEST", 2))
    print(ad.visible())
    print(lisample('abc'))
    print(lismission('abc','Sam','characterize'))

    return
    
# test()


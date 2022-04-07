'''For logging status, address and data'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from pathlib import Path
from os import mkdir, listdir, stat, SEEK_END, walk
from os.path import exists, getsize, getmtime, join, isdir, getctime
from datetime import datetime
from time import time, sleep
from contextlib import suppress
from numpy import prod, mean, rad2deg, array, ndarray, float64
import inspect, json, wrapt, struct, geocoder, ast, socket
import netifaces as nif
from pandas import DataFrame
from tables import open_file, Filters, Float32Atom, Float64Atom, StringCol, IsDescription
from json import loads

# MAT SAVE & LOAD
from scipy.io import savemat, loadmat
# ZIP LOG
from zipfile import ZipFile

from flask import session, g
from pyqum import get_db, close_db
from pyqum.instrument.toolbox import waveform, flatten

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
ANALYSIS_PATH = PORTAL_PATH / "ANALYSIS"
HISTORY_PATH = PORTAL_PATH / "HISTORY"


# Pending: extract MAC from IP?
def mac_for_ip(ip):
    'Returns a list of MACs for interfaces that have given IP, returns None if not found'
    for i in nif.interfaces():
        addrs = nif.ifaddresses(i)
        try:
            if_mac = addrs[nif.AF_LINK][0]['addr']
            if_ip = addrs[nif.AF_INET][0]['addr']
        except(IndexError, KeyError): #ignore ifaces that dont have MAC or IP
            if_mac = if_ip = None
        if if_ip == ip:
            return if_mac
    return None

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

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
    
    details = {'Org':g.org, 'Location': [g.city, g.country], 'Host': g.hostname, 'IP': [get_local_ip(), g.ip], 'Coordinate': [g.lat, g.lng]}
    place.append(str(details))

    return place

def clocker(stage=0, prev=0, agenda="Unkwnown Event"):
    '''timing algorithm in seconds'''
    now = time()
    duration = now - prev
    if int(stage) > 0:
        print(Fore.BLUE + Back.WHITE + "It took {:.5f}s to complete {:s} {:d}-th stage\n".format(duration, agenda, stage))
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
def loginstr(instr_name, label=1):
    '''[Existence, Assigned Path] = loginstr(Instrument's name, Instrument's index/queue)
    '''
    pyqumfile = instr_name + "_" + str(label) + "_status.pyqum"
    pqfile = Path(INSTR_PATH) / pyqumfile
    existence = exists(pqfile) and stat(pqfile).st_size > 0
    return existence, pqfile
def get_status(instr_name, label=1):
    '''Get Instrument Status from LOG
    '''
    try:
        instr_log = loginstr(instr_name, label)
        if instr_log[0] == False:
            instrument = None # No such Instrument
        else:
            with open(instr_log[1]) as jfile:
                instrument = json.load(jfile) # in json format
    except: 
        instrument = {}
        print(Fore.RED + "get_status faced some issues")
    return instrument
def set_status(instr_name, info, label=1):
    '''Set Instrument Status for LOG
    * <info> must be a DICT'''
    instrument = get_status(instr_name, label)
    if instrument is None:
        instrument = {}
    instrument.update(info)
    with open(loginstr(instr_name, label)[1], 'w') as jfile:
        json.dump(instrument, jfile, indent=4)

# save data in csv for export and be used by clients:
def set_csv(data_dict, filename):
    df = DataFrame(data_dict, columns= [x for x in data_dict.keys()])
    export_csv = df.to_csv(Path(PORTAL_PATH) / filename, index = None, header=True)
    return export_csv
# save data in mat for export and be used by clients:
def set_mat(data_dict, filename):
    savemat(Path(PORTAL_PATH) / filename, data_dict)
    return None
def bdr_zip_log(zipname, log_location=Path(r'\\BLUEFORSAS2\dr_bob') / "21-06-06"):
    zipfilename = "bdr[%s].zip"%(zipname)
    with ZipFile(Path(PORTAL_PATH) / zipfilename, 'w') as zipObj:
        for folderName, subfolders, filenames in walk(log_location):
            for filename in filenames:
                filePath = join(folderName, filename) # create complete filepath of file in directory
                status = zipObj.write(filePath) # Add file to zip
    return status

# save JSON into ANALYSIS Folder:
def set_json_measurementinfo(data_dict, filename):
    jsonFilename = filename+".JSON"
    totalPath = ANALYSIS_PATH/jsonFilename
    print( "save file in:", totalPath)
    with open(totalPath, 'w') as outfile:
        json.dump(data_dict, outfile, indent=4)
    return None
def get_json_measurementinfo(filename):
    jsonFilename = filename+".JSON"
    totalPath = ANALYSIS_PATH/jsonFilename
    print( "load file in:", totalPath)
    with open(totalPath, 'r') as f:
        data = json.load(f)
    return data

# save mat into ANALYSIS Folder:
def set_mat_analysis(data_dict, filename):
    matFilename = filename+".mat"
    totalPath = ANALYSIS_PATH/matFilename
    savemat(Path(totalPath), data_dict)
    return None

# save mat into HISTORY Folder:
def set_mat_history(data_dict, samplename, jobid, filename):
    matFilename = filename+".mat"
    totalPath = HISTORY_PATH/Path(samplename)/Path(jobid)/matFilename
    existence = exists(totalPath)# and stat(totalPath).st_size > 0
    if existence == False:
        totalPath.parent.mkdir(parents=True, exist_ok=True) #make directories
    savemat(totalPath, data_dict, format='5', oned_as="column") #made for JS-array
    return None
def get_histories(samplename, jobid):
    sample_job_dir = HISTORY_PATH/Path(samplename)/Path(jobid)
    try: histories = listdir(sample_job_dir)
    except: histories = []
    return histories
def get_mat_history(samplename, jobid, matfilename):
    File_Path = HISTORY_PATH/Path(samplename)/Path(jobid)/matfilename
    matdata = loadmat(File_Path)
    return matdata

class address:
    '''Use DATABASE by DEFAULT, TEST by CHOICE
    '''
    def __init__(self, mode='DATABASE'):
        self.mode = mode
        if self.mode=='DATABASE': pass
        elif self.mode=='TEST':
            with open(ADDRESS_PATH / "address.json") as ad:
                self.book = json.load(ad)
        
    def lookup(self, instr_name, label=1):
        '''Lookup from the database or the book'''
        if self.mode=='DATABASE':
            db = get_db()
            self.rs = db.execute('SELECT m.address FROM machine m WHERE m.codename = ?',('%s_%s'%(instr_name,label),)).fetchone()[0]
            close_db()
        elif self.mode=='TEST':
            try:
                if label>1: self.rs = self.book[instr_name]["alternative"][label-2]
                else: self.rs = self.book[instr_name]["resource"]
            except(KeyError): self.rs = None # checking if instrument in the book
        
        print('resource: %s' %self.rs)
        return self.rs
    
    def update_machine(self,connected,codename):
        ''' 
        Update SQL Database:
        connected: 0 or 1, codename = <instr>-<label/index> 
        '''
        if self.mode=='DATABASE':
            db = get_db()
            db.execute( 'UPDATE machine SET user_id = ?, connected = ? WHERE codename = ?', (session['user_id'], connected, codename,) )
            db.commit()
            close_db()
        elif self.mode=='TEST':
            print(Fore.RED + "REMINDER: MAKE SURE TO CLOSE CONNECTION UPON EXIT AND AVOID CONFLICT WITH ONLINE INSTRUMENTS")
        return
    def macantouch(self,instr_list):
        '''return total connection(s) based on instrument-list given'''
        db = get_db()
        connection = 0
        print(Fore.CYAN + "instr_list: %s" %instr_list)
        for mach in flatten(instr_list):
            connection += int(db.execute('''SELECT connected FROM machine WHERE codename = ?''', (mach,) ).fetchone()['connected'])
        close_db()
        return connection

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

    # Setting extra perimeter(s) like channel, window, S-param etc.
    prime = ''
    if '_' in action[0]: prime = action[0].split('_')[1]
    if headers[0]=='': headers[1] += prime # only the first header has this priviledge in this version # PENDING: more than one perimeter / prime (since it precedes parameter)
    else: headers[0] += prime


    if 'Get' in action[0]:
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

    if 'Set' in action[0]:
        
        for i in range(len(parakeys)):
            if str(action[i+1]) == '':
                paravalues.append("NIL") # allow for arbitrary choosing (turn-off certain parameter(s))
            elif ' ' in str(action[i+1]) and not "'" in str(action[i+1]): #set parameters for each header by certain parakey (very rare)
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
        status = str(bench.write(command)) #PENDING: status code translation
        
    # formatting return answer
    ans = dict(zip([a.replace('*','') for a in parakeys], paravalues))

    # Logging answer
    if 'Get' in action[0]: # No logging for "Set"
        set_status(mdlname, {Name.__name__ : ans})

    # debugging
    if eval(debugger):
        print(Fore.LIGHTBLUE_EX + "SCPI Header: {%s}" %headers[:-1])
        print(Fore.CYAN + "SCPI Command: {%s}" %command)
        if 'Get' in action[0]:
            print(Fore.YELLOW + "%s %s's %s: %s <%s>" %(action[0].split('_')[0], mdlname, Name.__name__, ans, status))
        if 'Set' in action[0]:
            print(Back.YELLOW + Fore.MAGENTA + "%s %s's %s: %s <%s>" %(action[0].split('_')[0], mdlname, Name.__name__ , ans, status))

    return status, ans

# Execution
class measurement:
    '''Initialize Measurement:\n
        1. Assembly Path based on Mission
        2. Checking Database if any (daylist)
        3. Used for sending status to the front-end via JS
    '''
    def __init__(self, mission, task, owner='USR', sample='Sample'):
        # Primary parameters (mission & task is auto-detected by OS)
        self.mission, self.task = mission, task
        self.owner, self.sample = owner, sample
        self.mssnpath = Path(USR_PATH) / owner / sample / mission
        #current location
        self.place = ", ".join(location()) 
        self.status = "M INTIATED"
        # FOR Resume / Access operation:
        try:
            daylist = [d for d in listdir(self.mssnpath) if isdir(self.mssnpath / d)]
            # print("There are %s days" %len(daylist))
            # filter out non-task-related
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
    def selectday(self, index, corder={}, perimeter={}, instr=[], datadensity=1, comment='', tag='', JOBID=None):
        '''corder: {parameters: <waveform>}\n'''

        # New operation if "new" is selected:
        if index == -1:
            now = datetime.now() #current day & time
            self.day = now.strftime("%Y-%m-%d(%a)")
            self.moment = now.strftime("%H:%M:%f")
            # estimating data size from parameters:
            self.corder = corder
            self.perimeter = perimeter
            self.instr = instr
            self.datadensity = datadensity
            self.comment = comment
            self.tag = tag
        
            task_index = 1
            while True:
                self.filename = "%s.pyqum(%s)" %(self.task, task_index)
                self.pqfile = self.mssnpath / self.day / self.filename

                # assembly the file-header(time, place, c-parameters):
                usr_bag = bytes('{"%s": {"place": "%s", "data-density": %s, "c-order": %s, "perimeter": %s, "instrument": %s, "comment": "%s", "tag": "%s"}}' %(self.moment, self.place, self.datadensity, self.corder, self.perimeter, self.instr, self.comment, self.tag), 'utf-8')
                usr_bag += b'\x02' + bytes("ACTS", 'utf-8') + b'\x03\x04' # ACTS
                
                # check if the file exists and not blank:
                existence = exists(self.pqfile) and stat(self.pqfile).st_size > 0 #The beauty of Python: if first item is false, second item will not be evaluated in AND-statement, thus avoiding errors
                if existence == False:
                    self.pqfile.parent.mkdir(parents=True, exist_ok=True) #make directories
                    with open(self.pqfile, 'wb') as datapie:
                        # Initialize blank file w/ user bag
                        datapie.write(usr_bag)

                    # Insert into Queue-list on SQL-Database: (from # 3. in settings)
                    jobstart(self.day, task_index, JOBID)
                    self.status = "JOBID #%s STOPPED" %JOBID # By the time this is output, M has exitted
                    break
                else:
                    task_index += 1

        # LOG-TEMP if "temp" is selected:
        elif index == -3:
            '''PENDING'''
            pass
            
        
        # from database:
        elif index >= 0:
            try:
                self.day = self.daylist[index]
                self.taskentries = [int(t.split('(')[1][:-1]) for t in listdir(self.mssnpath / self.day) if t.split('.')[0] == self.task]
                self.taskentries.sort(reverse=False) #ascending order
            except(ValueError): 
                print("index might be out of range")
                pass
        
        else: print(Fore.RED + "INVALID INDEX (%s) FOR DAY SELECT..." %index)

    # ONLY for scripting
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
            # Access newly added keys after queue-system development:
            try: self.perimeter = [x for x in self.datacontainer.values()][0]['perimeter']
            except(KeyError): self.perimeter = {}

            # Estimate data size based on version of your data:
            if 'C-Structure'in self.corder:
                self.datasize = int(prod([waveform(self.corder[param]).count * waveform(self.corder[param]).inner_repeat  for param in self.corder['C-Structure']], dtype='uint64')) * 2 #data density of 2 due to IQ
            else:
                self.datasize = prod([waveform(x).count * waveform(x).inner_repeat for x in self.corder.values()]) * self.datadensity

            # PENDING: USING JOBID TO EXTRACT TIME RESOLUTION (ns) through Back-door:
            try: print(Fore.YELLOW + "JOBID: %s" %self.perimeter['jobid'])
            except: pass
            # For newer version where seperation between structure & buffer is adopted:
            if 'READOUTYPE' in self.perimeter.keys():
                RJSON = loads(self.perimeter['R-JSON'].replace("'",'"'))
                for k in RJSON.keys(): self.datasize = self.datasize * waveform(str(RJSON[k])).count
                if self.perimeter['READOUTYPE'] == 'one-shot':
                    self.datasize = self.datasize * int(self.perimeter['RECORD-SUM'])
                else:
                    # EXTRACT "TIME_RESOLUTION_NS" IF AVAILABLE: TOTAL_READ_POINTS = RECORD_TIME_NS / TIME_RESOLUTION_NS
                    if 'TIME_RESOLUTION_NS' in self.perimeter.keys(): TIME_RESOLUTION_NS = int(self.perimeter['TIME_RESOLUTION_NS'])
                    else: TIME_RESOLUTION_NS = 1 # backward-compatible with ALZDG's 1GSPS sampling-rate
                    self.datasize = self.datasize * int(self.perimeter['RECORD_TIME_NS']) / TIME_RESOLUTION_NS
                
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
        tStart = time()
        
        try:
            with open(self.pqfile, 'rb') as datapie:
                datapie.seek(self.datalocation+7)
                pie = datapie.read(self.writtensize)
                # self.selectedata = array(struct.unpack('>' + 'd'*((self.writtensize)//8), pie))
                self.selectedata = ndarray(shape=(self.writtensize//8,), dtype=">d", buffer=pie) # speed up with numpy ndarray, with the ability to do indexing in it.
        except:
            # raise
            print("\ndata not found")
        
        print(Back.GREEN + Fore.WHITE + "DATA loaded in %ss" %(time()-tStart))

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
        '''build data into datacontainer (in RAM)'''
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
        
    def searchcomment(self, wday, keyword): # still pending # might prefer SQL to handle this task
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


# Setting up Measurement for MISSION (characterize, manipulate):
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
        owner, sample, tag, instr, corder, comment, dayindex, taskentry, perimeter, queue, renamed_task = next(Generator)
        mission = Path(inspect.getfile(Name)).parts[-1].replace('.py','') #Path(inspect.stack()[1][1]).name.replace('.py','')
        if renamed_task=="": task = Name.__name__
        else: task = renamed_task
        # print("task: %s" %task)
        M = measurement(mission, task, owner, sample) #M-Initialization
        if type(dayindex) is str: # for later access
            pass # ONLY M-INITIALIZATION (everytime when click a task) for the LATTER data access
        elif type(dayindex) is int: # for temp (-3), new (-1), resume (>=0)
            
            if g.user['measurement']:
                # 1. Register or Retrieve JOB(ID):
                if dayindex == -1: # NEW FILE
                    # REQUEUE from previous dropped out JOB => (0 file, 1 job)
                    if 'jobid' in perimeter.keys(): 
                        JOBID = perimeter['jobid']
                        print(Fore.GREEN + "Jobid found in perimeter")
                    # NEW JOB => (0 file, 0 job)
                    else: 
                        JOBID = jobin(task, corder, perimeter, instr, comment, tag)
                        print(Fore.GREEN + "NEW JOB REGISTERED")
                    print(Fore.BLUE + "NEW DAY DETECTED")
                elif dayindex == -3: # TEMP FILE
                    pass
                elif dayindex >= 0: # RESUME from previous stopped File => (1 file, 1 job)
                    day = M.daylist[dayindex]
                    criteria = dict(samplename=sample, task=task, dateday=day, wmoment=taskentry)
                    JOBID = jobsearch(criteria)
                    print(Fore.BLUE + "OLD DAY DETECTED")
                else: print(Fore.RED + "INVALID DAYINDEX: %s" %dayindex)
                perimeter["jobid"] = JOBID # BEWARE: will be reflushed back to the generator, don't know why?

                # 2. Queue-IN and Wait for your turn:
                M.status = qin(queue, JOBID)
                while True:
                    jobsinqueue(queue)
                    # 2.1. Get out in the middle of waiting:
                    if JOBID not in g.jobidlist:
                        M.status = "M-JOB CANCELLED OR NOT QUEUED IN PROPERLY"
                        return M
                    # 2.2. It's your turn AND all relevant instruments are free:
                    elif g.jobidlist.index(JOBID)==0 and not address().macantouch(list(instr.values())):
                        '''All of the following should be fulfilled before taking turn to run:
                            1. ONLY FIRST-IN-LINE get to break the waiting loop
                            2. ALL instruments required are disconnected
                        '''
                        break
                    # 2.3. Keep waiting behind:
                    else:
                        queue_behind = g.jobidlist.index(JOBID) + 1 # "extra +1" just in case of machine still being occupied
                        waiting_interval = 3.17*queue_behind # adjust waiting time based on how far behind in queue
                        sleep(waiting_interval)
                        print(Fore.YELLOW + "JOBID #%s is waiting every %s seconds" %(JOBID,waiting_interval))

                # 3. Start RUNNING / WORKING / MEASUREMENT:
                M.selectday(dayindex, corder, perimeter, instr, datadensity, comment, tag, JOBID)
                perimeter.pop('jobid', None)
                # print(Back.GREEN + "Day selected: %s"%self.day)
                M.selectmoment(taskentry)
                # print(Back.BLUE + "moment(file) selected: %s"%M.filename)
                try:
                    for i,x in enumerate(Generator): #yielding data from measurement-module
                        print('\n' + Fore.GREEN + 'Writing %s Data for Loop-%s' %(task,i))
                        M.insertdata(x)
                        # sleep(3) #for debugging purposes
                except(KeyboardInterrupt): print(Fore.RED + "\nSTOPPED")
                M.status = "M-JOB COMPLETED SUCCESSFULLY"

            else: M.status = "M-JOB REJECTED: PLS CHECK M-CLEARANCE!"

        # Measurement Object/Session:
        return M
    return wrapper

# LISTING
def lisample(usr):
    '''list samples for sample-profile under AUTH'''
    samples = [d for d in listdir(USR_PATH / usr) if isdir(USR_PATH / usr / d)]
    return samples
def lisjob(sample, queue, maxlist=12):
    '''
    list jobs for queue-page under MSSN\n
    job-list should be visible among users to avoid overlapping of measurements!
    '''
    # Provide user's clearances for each Queue (CHAR0, QPC0):
    if g.user['measurement']:
        # Extracting list from SQL-Database:
        Joblist = get_db().execute(
            '''
            SELECT j.id, j.task, j.dateday, j.wmoment, j.startime, j.instrument, j.comment, j.progress, u.username, j.tag, j.note
            FROM user u
            INNER JOIN job j ON j.user_id = u.id
            INNER JOIN sample s ON s.id = j.sample_id
            WHERE j.queue = ? AND s.samplename = ?
            ORDER BY j.id DESC
            ''', (queue, sample)
        ).fetchall()
        close_db()
        Joblist = [dict(x) for x in Joblist]
        Job_count = len(Joblist) # total job(s) done on certain sample
        Joblist = Joblist[:min(maxlist, Job_count)] # limit the number of job listing
        # print("Job list: %s" %Joblist)
        # print("Running %s" %inspect.stack()[0][3]) # current function name
    return Joblist, Job_count
def lisqueue(queue):
    '''
    list queues for queue-page under MSSN
    Update clearance for running the experiment
    '''
    if g.user['measurement']:
        try:
            # Extracting list from SQL-Database: (took-out: "INNER JOIN sample s ON s.id = j.sample_id" since queue-system has to align with sample in order to run experiments)
            db = get_db()
            g.Queue = db.execute(
                '''
                SELECT j.id, j.task, j.startime, u.username, j.instrument, j.comment
                FROM user u
                INNER JOIN %s c ON c.job_id = j.id
                INNER JOIN job j ON j.user_id = u.id
                ORDER BY c.id ASC
                ''' %(queue)
                ).fetchall()
            close_db()
            g.Queue = [dict(x) for x in g.Queue]
        
        except: raise
        # print(Fore.BLACK + Back.WHITE + "Clearance for queue %s: %s"%(queue, session['run_clearance']))
    return
def jobsinqueue(queue):
    if int(g.user['measurement']) > 0:
        db = get_db()
        g.jobidlist = db.execute("SELECT job_id FROM %s ORDER BY id"%queue).fetchall()
        close_db()
        g.jobidlist = [dict(x)['job_id'] for x in g.jobidlist] # use to scheduling tasks in queue
        status = "JOBID-LIST in QUEUE has been extracted"
    else: status = "Measurement clearance was not found"
    return status

# QUEUE
def qin(queue,jobid):
    '''Queue in with a Job'''
    if int(g.user['measurement']) > 0:
        try:
            db = get_db()
            db.execute('INSERT INTO %s (job_id) VALUES (%s)' %(queue,jobid)).lastrowid
            db.commit()
            close_db()
            status = "Queued-in successfully with JOBID #%s" %jobid
        except:
            status = "Error Queueing in with JOBID #%s" %jobid
    else: status = "Measurement clearance was not found"
    return status
def qout(queue,jobid,username):
    '''Queue out without a Job'''
    jobrunner = get_db().execute('SELECT username FROM user u INNER JOIN job j ON j.user_id = u.id WHERE j.id = ?',(jobid,)).fetchone()['username']
    close_db()
    if (int(g.user['measurement']) > 0) and (username==jobrunner):
        try:
            db = get_db()
            db.execute('DELETE FROM %s WHERE job_id = %s' %(queue,jobid))
            db.commit()
            close_db()
            status = "JOBID #%s Queued-out successfully" %jobid
        except:
            # raise
            status = "Error Queueing out with JOBID #%s" %jobid
    else: status = "%s is not allowed to stop %s's job #%s" %(username,jobrunner,jobid)
    return status
def qid(queue,jobid):
    '''Get queue number'''
    try:
        db = get_db()
        id = db.execute('SELECT id FROM %s WHERE job_id = %s' %(queue,jobid)).fetchone()['id']
        close_db()
    except: id = None
    return id
def check_sample_alignment(queue):
    '''
    TO QUEUE-IN, the assigned-sample for that queue-system (by admin) MUST be aligned with the sample chosen (MEAL):
    '''
    try: 
        db = get_db()
        assigned_sample = db.execute( '''SELECT samplename FROM queue WHERE system = ?''', (queue,) ).fetchone()['samplename'] # assigned sample by admin
        close_db()
    except(TypeError): 
        assigned_sample = ''
    session['run_clearance'] = bool( assigned_sample==get_status("MSSN")[session['user_name']]['sample'] and int(g.user['measurement'])>0 )
    return session['run_clearance']
def which_queue_system(sample):
    '''Find out which system is the sample being hooked up to'''
    try:
        db = get_db()
        system = db.execute( '''SELECT system FROM queue WHERE samplename = ?''', (sample,) ).fetchone()['system']
        close_db()
    except(TypeError):
        system = "NULL"
    return system

# JOB
def jobin(task,corder,perimeter,instr,comment,tag):
    '''Register a JOB and get the ID for queue-in later while leaving day and task# blank first'''
    if g.user['measurement']:
        try:
            db = get_db()
            samplename = get_status("MSSN")[session['user_name']]['sample']
            queue = get_status("MSSN")[session['user_name']]['queue']
            sample_id = db.execute('SELECT s.id FROM sample s WHERE s.samplename = ?', (samplename,)).fetchone()[0]
            cursor = db.execute('INSERT INTO job (user_id, sample_id, task, parameter, perimeter, instrument, comment, tag, queue) VALUES (?,?,?,?,?,?,?,?,?)', 
                                        (g.user['id'],sample_id,task,str(corder),str(perimeter),str(instr),comment,tag,queue))
            JOBID = cursor.lastrowid
            db.commit() # to avoid database-lock in the event of pending write-changes
            perimeter['jobid'] = JOBID
            # sleep(0.317)
            db.execute('UPDATE job SET perimeter = ? WHERE id = ?', (str(perimeter),JOBID))
            db.commit()
            close_db()
            print(Fore.GREEN + "Successfully register the data into SQL Database with JOBID: %s" %JOBID)
        except:
            # raise
            JOBID = None 
            print(Fore.RED + Back.WHITE + "Check all database input parameters")
            print(Fore.BLUE + "Please make sure queue's 'check'-constraint inside job's table has already included the new queue!")
    else: JOBID = None
    return JOBID
def jobstart(day,task_index,JOBID):
    '''Start a JOB by logging day and task#'''
    if g.user['measurement']:
        try:
            db = get_db()
            db.execute('UPDATE job SET dateday = ?, wmoment = ? WHERE id = ?', (day,task_index,JOBID))
            db.commit()
            close_db()
            print(Fore.GREEN + "Successfully update JOB#%s with (Day: %s, TASK#: %s)" %(JOBID,day,task_index))
        except:
            print(Fore.RED + Back.WHITE + "INVALID JOBID")
            raise
    else: pass
    return
def jobnote(JOBID, note):
    '''Add NOTE to a JOB after analyzing the data'''
    if g.user['measurement']:
        try:
            db = get_db()
            db.execute('UPDATE job SET note = ? WHERE id = ?', (note,JOBID))
            db.commit()
            close_db()
            print(Fore.GREEN + "User %s has successfully updated JOB#%s with NOTE: %s" %(g.user['username'],JOBID,note))
        except:
            print(Fore.RED + Back.WHITE + "INVALID JOBID")
            raise
    else: pass
    return
def jobsearch(criteria, mode='jobid'):
    '''Search for JOB(s) based on criteria (keywords)
        \nmode <jobid>: get job-id based on criteria
        \nmode <tdmq>: get task, dateday, wmoment & queue based on job-id given as criteria
        \nmode <requeue>: get task, parameter, perimeter, comment & tag based on job-id given as criteria for REQUEUE
        \nmode <note>: get note based on job-id given as criteria
    '''
    db = get_db()
    if mode=='jobid':
        # as single-value
        result = db.execute(
                    '''
                    SELECT j.id 
                    FROM job j 
                    JOIN sample s ON s.id = j.sample_id
                    WHERE s.samplename = ? AND j.task = ? AND j.dateday = ? AND j.wmoment = ?
                    ''', (criteria['samplename'], criteria['task'], criteria['dateday'], criteria['wmoment'])
                ).fetchone()[0]
    elif mode=='tdm':
        # as dictionary
        result = db.execute('SELECT task, dateday, wmoment, queue FROM job WHERE id = ?', (criteria,)).fetchone()
    elif mode=='requeue':
        result = db.execute('SELECT task, parameter, perimeter, comment, tag FROM job WHERE id = ?', (criteria,)).fetchone()
    elif mode=='note':
        result = db.execute('SELECT j.note FROM job j WHERE j.id = ?', (criteria,)).fetchone()[0]
    else: result = None 
    close_db()
    return result
def jobtag(JOBID, tag, mode=0):
    '''
    commit tag to a job.
    mode-0: replace; mode-1: extend;
    '''
    if g.user['measurement']:
        try:
            db = get_db()
            if int(mode): tag = db.execute('SELECT tag FROM job WHERE id = ?', (JOBID,)).fetchone()[0] + tag
            db.execute('UPDATE job SET tag = ? WHERE id = ?', (tag,JOBID))
            db.commit()
            close_db()
            action = ['replace', 'extend']
            print(Fore.GREEN + "User %s has successfully %s JOB#%s with tag: %s" %(g.user['username'],action[mode],JOBID,tag))
        except:
            print(Fore.RED + Back.WHITE + "INVALID JOBID")
            raise
    else: pass
    return
def job_update_perimeter(JOBID, perimeter):
    '''
    Update (Replace) Job's Perimeter.
    '''
    if g.user['measurement']:
        try:
            db = get_db()
            db.execute('UPDATE job SET perimeter = ? WHERE id = ?', (str(perimeter),JOBID))
            db.commit()
            close_db()
            print(Fore.GREEN + "User %s has successfully updated JOB#%s's perimeter as: %s" %(g.user['username'],JOBID,perimeter))
        except:
            print(Fore.RED + Back.WHITE + "INVALID JOBID")
            raise
    else: pass
    return




# TEST
def test():
    L = location()
    print("We are now in %s" %L)
    ad = address()
    print(ad.lookup("YOKO"))
    print(ad.lookup("TEST", 2))
    print(lisample('abc'))
    print(lisjob('Sam','characterize'))

    return
    
# test()


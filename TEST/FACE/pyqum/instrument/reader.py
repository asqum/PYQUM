'''For reading data from different kinds of database'''
from os import path
from datetime import datetime
from operator import itemgetter
from contextlib import suppress
from copy import deepcopy, copy
from sqlite3 import connect, Row, PARSE_DECLTYPES
from json import loads, load, dumps
from pathlib import Path
import sqlite3
from numpy import array

# Getting PATHS:
pyfilename = Path(__file__).resolve() # current pyscript filename (usually with path)
CONFIG_PATH = Path(pyfilename).parents[7] / "HODOR" / "CONFIG"
INSTR_PATH = CONFIG_PATH / "INSTLOG"
DR_SETTINGS = path.join(CONFIG_PATH, 'DR_settings.sqlite')
MIXER_SETTINGS = path.join(CONFIG_PATH, 'MIXER_settings.sqlite')
USREPO_SETTINGS = path.join(CONFIG_PATH, 'USR_repo.sqlite')

# JSON LIBRARY:
def dict_depth(d):
    if isinstance(d, dict):
        return 1 + (max(map(dict_depth, d.values())) if d else 0)
    return 0
def search_value(usrdata, val, prepath=()): # non-destructive # unresolved generator objects
    for k, v in usrdata.items():
        path = prepath + (k,)
        if v == val:
            yield path
        elif hasattr(v, 'items'):
            p = search_value(v, val, path)
            if p is not None:
                yield p
def goto_siblings(usrdata, path): #non-destructive probe
    for key in path[:-1]:
        usrdata = usrdata[key]
    return usrdata
def update_siblings(usrdata, path, item={}): #constructive
    for key in path[:-1]:
        usrdata = usrdata[key]
    usrdata.update(item)
    return usrdata
def searchpop_value(usrdata, val, prepath=()): #destructive
    for k, v in usrdata.items():
        path = prepath + (k,)
        if v == val:
            pop_val = usrdata.pop(k)
            return path, pop_val
        elif hasattr(v, 'items'):
            p = searchpop_value(v, val, path)
            if p is not None:
                return p
def search_allpaths(usrdata, val): # non-destructive
    '''return the paths that contain val
    '''
    result, Paths = "", []
    while result is not None:
        result = searchpop_value(usrdata, val)
        with suppress(TypeError): #bypass type-errors
            Paths.append(list(result[0]))
    # reconstructing
    for p in Paths:
        update_siblings(usrdata, p, {p[-1]: val})
    return Paths
def delete_allkeys(usrdata, keys): # untested
    for key in keys:
        with suppress(KeyError):
            del usrdata[key]
    for v in usrdata.values():
        if hasattr(v, 'items'):
            delete_allkeys(v, keys)
def printTree(tree, depth = 0, parents="", branches=[], treeline='', div=None, idiv=0):
        if not hasattr(tree, 'items'):
            branches.append(parents.split('── '))
            with suppress(IndexError):
                interception = set(branches[-1]) & set(branches[-2])
                if branches[-2][0] in interception:
                    treeline = '── '.join(branches[-2][:len(interception)-1])
                    if idiv/div == 1 or idiv == 1:
                        parents = parents.replace(treeline, ' '*(len(treeline)-1) + '└') 
                    else: parents = parents.replace(treeline, ' '*(len(treeline)-1) + '├')
            note ="" #" branch#%s/%s" %(idiv, div) #for debugging purposes        
            print(parents + str(tree) + note) #printing tree in the process line-by-line
        else:
            idiv=0 # reset when go deeper
            for key, val in tree.items():
                if depth > 0:
                    idiv += 1
                    div = len(tree)
                printTree(val, depth+1, parents+str(key)+"── ", div=div, idiv=idiv)
def search_time(dictpaths, timestamp):
    '''timestamp = Year month day'''
    tstamp0 = [i[0] for i in dictpaths]
    timestamp = datetime.strptime(timestamp, '%Y %m %d')
    tstamplist = [datetime.strptime(i, '%a %b %d %H:%M:%S %Y') for i in tstamp0]
    timedistances = [abs(timestamp - x) for x in tstamplist]
    inearest, nearest = min(enumerate(timedistances), key=itemgetter(1)) #minimize item instead of index
    print(inearest)
    print(nearest)
    selectedP = dictpaths[inearest]
    return nearest, selectedP

# SQLite DATADASE:
# 0. Server port:
def device_port(dev):
    '''retrieve path / port for specific access from DR-specific database'''
    db = connect(DR_SETTINGS, detect_types=PARSE_DECLTYPES, timeout=1000)
    db.row_factory = Row
    dev_port = db.execute('SELECT p.Port FROM PORT p WHERE p.Device = ?', (dev,)).fetchone()[0]
    return dev_port

# 1. BDR address:
def bdr_address(name):
    '''retrieve BDR Specs from DR-specific database'''
    db = connect(DR_SETTINGS, detect_types=PARSE_DECLTYPES, timeout=1000)
    db.row_factory = Row
    bdr_specs = db.execute('SELECT b.LogPath, b.TPath, b.Tname FROM BDR b WHERE b.Name = ?', (name,)).fetchone()
    return array(bdr_specs)
    
# 2. Instrument Allocation:
def inst_order(queue, category='ALL', tabulate=True):
    '''Return list of instruments accordingly'''
    db = connect(DR_SETTINGS, detect_types=PARSE_DECLTYPES, timeout=1000)
    db.row_factory = Row
    if str(category).lower()=='all': 
        inst_list = db.execute("SELECT category, designation FROM %s ORDER BY id ASC"%queue,()).fetchall()
        inst_list = [dict(x) for x in inst_list]
    else: 
         
        inst_list = db.execute("SELECT q.designation FROM %s q WHERE q.category = ? ORDER BY q.id ASC"%queue,(category,)).fetchone()
        if inst_list is None or inst_list[0].replace(' ','')=='': # ABSENT in queue or BLANK space in category
            inst_list = ['DUMMY_1'] # Creating Dummy Instrument for Compatibility reason: for macantouch...
        else: 
            inst_list = inst_list[0]
            
            if tabulate:
                if category=='CH' or category=='ROLE': # virtual-instrument's output: dict

                    # Auto-detect which version:
                    # 1st version: uses rare character to imply wiring-hierarchy: e.g. DAC:I1/Q1,X1/Y1/Z1/P1,Z2>>SG:XY1/XY2,RO1/PA1>>DC:ZPA,ZC
                    if '{' not in inst_list:
                        inst_list = inst_list.replace(' ','') # allow spaces for this version as well
                        inst_list = inst_list.split('>>')
                        inst_list = [{x.split(':')[0]:x.split(':')[1].split(',')} for x in inst_list]
                        inst_list = {instr_type:[instr_chs.split('/') for instr_chs in instr_modules] for instr_config in inst_list for instr_type,instr_modules in instr_config.items()} # {<inst>: <slot-channel> ...}

                    # 2nd version: directly build JSON to save wiring-configuration (for ASQPU): e.g. {"DAC": [["I1", "Q1"], ["X1", "Y1", "Z1", "P1"], ["Z2"]], "SG": [["XY1", "XY2"], ["RO1", "PA1"]], "DC": [["ZPA"], ["ZC"]]}
                    else: inst_list = loads(inst_list)

                else: inst_list = inst_list.split(',') # real-instrument's output: list
            else: 
                inst_list = str(inst_list) # for editting on WIRING-page

    db.close()

    return inst_list
def inst_designate(queue, category, designation):
    '''
    category: instrument-type based on their unique role
    designation: a list of instruments that have been assigned the role
    '''
    db = connect(DR_SETTINGS, detect_types=PARSE_DECLTYPES, timeout=1000)
    db.row_factory = Row
    print(queue, category, designation)
    db.execute("UPDATE %s SET designation = ? WHERE category = ?"%queue, (designation,category,))
    db.commit()
    db.close()
    return

# 3. MACE Execution:
class macer:
    '''
    Based on QPC-Wiring setup, control designated devices according to the MACE-script in R-JSON order 
    Commander in MACE is a Category in QPC-Wiring.
    '''
    def __init__(self, queue=None, commander=None):
        self.commander = commander
        self.queue = queue
        # Initiate database:
        self.db = connect(DR_SETTINGS, detect_types=PARSE_DECLTYPES, timeout=1000)
        self.db.row_factory = Row
        self.experiment_list = [dict(x)["Commander"] for x in self.db.execute('SELECT Commander FROM MACE WHERE Level = "Experiment"').fetchall()] # Check Experiment-list

        # Check Commander's level:
        try:
            self.level = self.db.execute('SELECT m.Level FROM MACE m WHERE m.Commander = ?', (commander,)).fetchone()[0]
            if self.level == "Device": 
                self.device_order = inst_order(queue, self.commander)
            else: 
                self.device_order = []
        except: self.level, self.device_order = None, []

    def get_skills (self):
        '''Extract the Commander's Skills
        '''
        self.PARAMETERS, self.DEFAULT_VALUES = [], []
        try:
            self.commander_attributes = self.db.execute('SELECT m.Skills FROM MACE m WHERE m.Commander = ?', (self.commander,)).fetchone()[0]
            for p in self.commander_attributes.replace(" ","").replace("\n","").split(','):
                self.PARAMETERS.append(p.split('/')[0])
                try: self.DEFAULT_VALUES.append(p.split('/')[1])
                except(IndexError): self.DEFAULT_VALUES += ["{%s}"%p[:4]]
        except: pass

        return

    def initiate_commanders(self):
        '''Initiate all designated Devices in the Commander (Category)'''
        if self.device_order is not None:


            pass

        return

    def execute(self, mace_command):
        '''
        '''
        self.mace = mace_command.replace(" ","").replace("\n","").lower() # get rid of multiple spacings & new-lines and also lower the cases
        PAIRS = self.mace.split(",")
        self.KEYS, self.VALUES = [p.split(':')[0] for p in PAIRS], [p.split(':')[1] for p in PAIRS]

        return

    def close(self):
        self.db.close()

# 4. Mixer-parameters Catalog: (PENDING)
def mixer_order(module, LO_frequency):
    db = connect(MIXER_SETTINGS, detect_types=PARSE_DECLTYPES, timeout=1000)
    db.row_factory = Row
    if str(category).lower()=='all': 
        inst_list = db.execute("SELECT category, designation FROM %s ORDER BY id ASC"%queue,()).fetchall()
        inst_list = [dict(x) for x in inst_list]
    else: 
        inst_list = db.execute("SELECT designation FROM %s WHERE category = ? ORDER BY id ASC"%queue,(category,)).fetchall()
        inst_list = [dict(x)['designation'] for x in inst_list]
    db.close()
    return inst_list
def mixer_designate(queue, category, designation):
    db = connect(MIXER_SETTINGS, detect_types=PARSE_DECLTYPES, timeout=1000)
    db.row_factory = Row
    db.execute("UPDATE %s SET designation = ? WHERE category = ?"%queue, (designation,category,))
    db.commit()
    db.close()
    return

# 5. User-Repositories:
class USR_repo:
    def __init__(self, user):
        '''The management of repositories owned by users'''
        self.user = user
        self.db = connect(USREPO_SETTINGS, detect_types=PARSE_DECLTYPES, timeout=1000) # create file if non-exist
        self.db.row_factory = Row
        return

    def list_users(self):
        '''List all tables' (users') name'''
        SQL_script = f"SELECT name FROM sqlite_master WHERE type='table';"
        self.user_list = [dict(x)['name'] for x in self.db.execute(SQL_script).fetchall()]
        return self.user_list

    def check_user(self):
        '''Create user-table if not exist and list the boxes of that particular user'''
        self.db.execute('''
        CREATE TABLE IF NOT EXISTS %s ( "box" TEXT NOT NULL UNIQUE, "update" TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "content" TEXT NOT NULL, "share_with" TEXT ); ''' %(self.user))
        self.db.commit()
        self.box_list = [dict(x)['box'] for x in self.db.execute("SELECT box FROM %s" %(self.user)).fetchall()]
        return

    def import_from_SCHEME_status(self):
        '''help transition from JSON to SQL-based Database'''
        try:
            with open(Path(INSTR_PATH) / "SCHEME_1_status.pyqum") as jfile: self.imported_SCHEME = load(jfile) # in json format
            for key in self.imported_SCHEME.keys():
                SQL_script = f"INSERT INTO '{self.user}' (box, content) VALUES ('{key}', '{dumps(self.imported_SCHEME[key])}')" # Using different parametrization for dynamic table insertion
                self.db.execute(SQL_script)
                self.db.commit()
        except(sqlite3.IntegrityError): print("This SCHEME has been imported previously")
        return

    def read_user(self, box):
        '''Read user's box-content'''
        SQL_script = f"SELECT content FROM '{self.user}' WHERE box = '{box}'"
        self.content = self.db.execute(SQL_script).fetchone()['content']
        return

    def insert_box(self, box, content):
        '''Insert if box not exist and Update if already exist'''
        if box not in self.box_list: SQL_script = f"INSERT INTO '{self.user}' (box, content) VALUES ('{box}', '{content}')"
        else: SQL_script = f"UPDATE '{self.user}' SET 'update' = CURRENT_TIMESTAMP, content = '{content}' WHERE box = '{box}'"
        self.db.execute(SQL_script)
        self.db.commit()
        return

    def share_box(self):
        '''Share box-content to other user(s)'''
        
        return

    def close(self):
        self.db.close()
        return


def test():
    # DATA-TREE:
    if False:
        Test_DATA = {'A': {'B': {'C': {'D': {'E': 100, 'mind': 'Great'}}}},
        'A1': {'B': {'C': {'D': {'E': 100, 'idol': 'Einstein'}}}},
        'A2': {'B': {'C': {'D': {'E': 100, 'address': 'Mars'}}}},
        'A3': {'B1': 100, 'C1': 200, 'D1': 300, 'E1': {'F1': 100, 'God': 777}},
        'A4': 100, 'AA': {'B2': {'C2': 100, 'D2': 300}},
        'A5': {'B3': {'C3': 100, 'D3': {'E3': 100, 'F3': 200, 'G3': 300}}},
        'A6': {'B5': {'C5': {'D5': {'E5': {'F5': {'G5': 100, 'H24': 'David'}}}}}}, 'alien': 'is good',
        'A7': 100, 'B7': 100, 'C7': {'D7': {'E7': 200, 'F7': 100, 'G7': 300}}}

        print("\nThe depth of Test_DATA is %s" %dict_depth(Test_DATA))

        DATA = deepcopy(Test_DATA)
        for x in [100, 200, 300, 'David', 'is good', 'is']:
            paths = search_allpaths(Test_DATA, x)
            print("\n%s result(s) FOUND for [%s]:" %(len(paths), x))
            for p in paths:
                print("%s. %s" %(1+paths.index(p), p))
        print("After operation: \n%s" %Test_DATA)
        print("Transferred DATA:\n%s" %DATA)

        DATA01 = deepcopy(DATA)
        selectedPath = search_allpaths(DATA, 100)[7]
        sib_dict = goto_siblings(DATA, selectedPath)
        print("The path [%s]'s sib-data:" %selectedPath)
        print(sib_dict)
        
        # try to extract from generator object
        paths = search_value(DATA01, 100)
        print(paths)

        print("Deepcopied DATA with length %s:" %len(DATA01))
        print(DATA01)
        
        printTree(DATA01)

    # SQL Database:
    if False:
        inst_list = inst_order("CHAR0")
        print("inst_list: %s" %inst_list)
        print("CHAR0's DC: %s" %inst_order("CHAR0", 'DC'))
        print("QPC0's DAC: %s" %inst_order("QPC0", 'DAC'))
        print("QPC0's DC: %s" %inst_order("QPC0", 'DC'))
        print("QPC1's DC: %s" %inst_order("QPC1", 'DC'))
        print("QPC0's CH: %s" %inst_order("QPC0", 'CH'))
        print("QPC0's ROLE: %s" %inst_order("QPC0", 'ROLE'))
        print("DAC's Channel-Matrix: %s" %(inst_order("QPC0", 'CH')['DAC']))
        print("QPC1's CH: %s" %inst_order("QPC1", 'CH'))
        print("QPC1's ROLE: %s" %inst_order("QPC1", 'ROLE'))
        # inst_designate("CHAR0","DC","SDAWG_3")
        from pyqum.instrument.toolbox import find_in_list
        DACH_Role = inst_order("QPC0", 'ROLE')['DAC']
        RO_addr = find_in_list(DACH_Role, 'I1')
        XY_addr = find_in_list(DACH_Role, 'X1')
        print("RO_addr: %s, XY_addr: %s" %(RO_addr,XY_addr))

    # MACER
    if True:
        m = macer("QPC0", "SG")
        m.get_skills()
        print("Commander's Level:\n %s (%s)" %(m.level, m.device_order))
        print("Commander's Attributes:\n %s" %m.commander_attributes)
        m.execute("frequency:3e9, power:-10")
        print("Commander's Keys:\n %s" %m.KEYS)
        print("Commander's Values:\n %s" %m.VALUES)
        m.close()

        Exp = macer()
        print(Exp.experiment_list)
        Exp.close()

        Exp = macer(commander="RB")
        print(Exp.experiment_list)
        Exp.get_skills()
        print("Commander's Attributes:\n %s" %Exp.commander_attributes)
        print("Commander's Parameters:\n %s" %Exp.PARAMETERS)
        print("Commander's Defaults:\n %s" %Exp.DEFAULT_VALUES)
        Exp.close()

    # USREPO
    if False:
        repo = USR_repo("abc")
        print("User-list:\n %s" %repo.list_users())
        repo.check_user()
        print("Box-list:\n%s" %repo.box_list)
        repo.import_from_SCHEME_status()
        repo.check_user()
        print("Box-list:\n%s" %repo.box_list)
        repo.read_user("TRANSFER")
        print("HELLO: %s" %loads(repo.content)['R-JSON'])
        repo.insert_box("hola","hello")
        repo.insert_box("T1","HOLA")
        repo.close()

    
    return

if __name__ == "__main__": test()

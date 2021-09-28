'''For reading data from different kinds of database'''
from os import path
from datetime import datetime
from operator import itemgetter
from contextlib import suppress
from copy import deepcopy, copy
from sqlite3 import connect, Row, PARSE_DECLTYPES

from pathlib import Path
pyfilename = Path(__file__).resolve() # current pyscript filename (usually with path)
CONFIG_PATH = Path(pyfilename).parents[7] / "HODOR" / "CONFIG"
DR_SETTINGS = path.join(CONFIG_PATH, 'DR_settings.sqlite')
MIXER_SETTINGS = path.join(CONFIG_PATH, 'MIXER_settings.sqlite')

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
    db = connect(DR_SETTINGS, detect_types=PARSE_DECLTYPES, timeout=1000)
    db.row_factory = Row
    dev_port = db.execute('SELECT p.Port FROM PORT p WHERE p.Device = ?', (dev,)).fetchone()[0]
    return dev_port
    
# 1. Instrument Allocation:
def inst_order(queue, category='ALL', tabulate=True):
    '''Return list of instruments accordingly'''
    db = connect(DR_SETTINGS, detect_types=PARSE_DECLTYPES, timeout=1000)
    db.row_factory = Row
    if str(category).lower()=='all': 
        inst_list = db.execute("SELECT category, designation FROM %s ORDER BY id ASC"%queue,()).fetchall()
        inst_list = [dict(x) for x in inst_list]
    else: 
        try: 
            inst_list = db.execute("SELECT q.designation FROM %s q WHERE q.category = ? ORDER BY q.id ASC"%queue,(category,)).fetchone()[0]
            
            if tabulate:
                if category=='CH' or category=='ROLE': # output: dict
                    inst_list = inst_list.split('>>')
                    inst_list = [{x.split(':')[0]:x.split(':')[1].split(',')} for x in inst_list]
                    inst_list = {k:[x.split('/') for x in v] for d in inst_list for k,v in d.items()}
                else: inst_list = inst_list.split(',') # output: list
            else: 
                inst_list = str(inst_list) # for editting on WIRING-page

        except(TypeError): inst_list = ['DUMMY_1'] # Creating Dummy Instrument for Compatibility reason: for macantouch...
    db.close()

    return inst_list
def inst_designate(queue, category, designation):
    '''
    category: instrument-type based on their unique role
    designation: a list of instruments that have been assigned the role
    '''
    db = connect(DR_SETTINGS, detect_types=PARSE_DECLTYPES, timeout=1000)
    db.row_factory = Row
    db.execute("UPDATE %s SET designation = ? WHERE category = ?"%queue, (designation,category,))
    db.commit()
    db.close()
    return

# 2. Mixer-parameters Catalog: (PENDING)
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


def test():
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
    from json import loads, dumps
    inst_list = inst_order("CHAR0")
    print("inst_list: %s" %inst_list)
    print(inst_order("CHAR0", 'DC'))
    print(inst_order("QPC0", 'DAC'))
    print(inst_order("QPC0", 'DC'))
    print(inst_order("QPC0", 'CH'))
    print(inst_order("QPC0", 'ROLE'))
    print("DAC's Channel-Matrix: %s" %(inst_order("QPC0", 'CH')['DAC']))
    # inst_designate("CHAR0","DC","SDAWG_3")
    from pyqum.instrument.toolbox import find_in_list
    DACH_Role = inst_order("QPC0", 'ROLE')['DAC']
    RO_addr = find_in_list(DACH_Role, 'I1')
    XY_addr = find_in_list(DACH_Role, 'X1')
    print("RO_addr: %s, XY_addr: %s" %(RO_addr,XY_addr))

    
    return


# test()

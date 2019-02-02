'''For reading data'''
from datetime import datetime
from operator import itemgetter
from contextlib import suppress
from copy import deepcopy, copy

def dict_depth(d):
    if isinstance(d, dict):
        return 1 + (max(map(dict_depth, d.values())) if d else 0)
    return 0

# unresolved generator objects
def search_value(usrdata, val, prepath=()): # non-destructive
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

# untested
def delete_allkeys(usrdata, keys):
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
    for x in [100, 200, 300, 'David', 'is good']:
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
    
    return


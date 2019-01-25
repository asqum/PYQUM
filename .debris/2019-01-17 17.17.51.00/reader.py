'''For reading data'''
from datetime import datetime
from operator import itemgetter
from contextlib import suppress

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
    inearest, nearest = min(enumerate(timedistances), key=itemgetter(1))
    selectedP = dictpaths[inearest]
    return nearest, selectedP

def test_reader():

    return

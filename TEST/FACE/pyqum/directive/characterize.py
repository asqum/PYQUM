'''Basic QuBit Characterizations'''

import wrapt, inspect
from pyqum.instrument.logger import settings

@settings('AS')
def TESTC(C1, C2, C3, C4, C5):
    '''Serve as a template for other real tasks to come'''
    data = 0
    for c1 in C1:
        for c2 in C2:
            for c3 in C3:
                for c4 in C4:
                    for c5 in C5:
                        data += 1
                        yield data


TESTC([0,1,2],[0.1,0.2,0.3],[1,3,5],[2,4,6,8,10,12],[100,300])

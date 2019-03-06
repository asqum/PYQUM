'''Basic QuBit Characterizations'''

import wrapt, inspect
from pyqum.instrument.logger import settings

__author__ = "Teik-Hui Lee"
__copyright__ = "Copyright 2019, The Pyqum Project"
__credits__ = ["Chii-Dong Chen", "Yu-Cheng Chang"]
__license__ = "GPL"
__version__ = "beta3"
__email__ = "teikhui@phys.sinica.edu.tw"
__status__ = "development"

@settings('AS')
def TESTC(C1, C2, C3, C4, C5):
    data = []
    for c1 in C1:
        for c2 in C2:
            for c3 in C3:
                for c4 in C4:
                    for c5 in C5:
                        data.append(c1 + c2 + c3 + c4 + c5)
    return data


# TESTC([1],[2],[3],[4],[5])

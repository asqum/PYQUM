# For TESTING of ALL Instruments

from pyqum.instrument.logger import clocker
from pyqum.instrument.benchtop import MXG, DSO, ESG
from pyqum.instrument.modular import AWG, VSA
import inspect, numpy, time

# Testing function's name-string:
def piqom():
    print("(This function's name:", inspect.stack()[0][3], ")")
piqom()

# Testing Help DocStrings
print("The Doc for AWG's active_marker: %s" %AWG.active_marker.__doc__)

# Marking starting point of time:
stage, prev = clocker(0)

# Testing each machine individually
MXG.test(True)
stage, prev = clocker(stage, prev) # Marking certain point of time
AWG.test(True)
stage, prev = clocker(stage, prev)
VSA.test(True)
stage, prev = clocker(stage, prev)
DSO.test(True)
stage, prev = clocker(stage, prev)
ESG.test(True)
stage, prev = clocker(stage, prev)





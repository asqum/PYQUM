# For TESTING of ALL Instruments

from pyqum.instrument.logger import clocker
from pyqum.instrument.benchtop import MXG, DSO, ESG, PNA
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
state = str(input("TEST's Switch Code (MXG-AWG-VSA-DSO-ESG): "))
if state[0] == "1":
    MXG.test(True)
    stage, prev = clocker(stage, prev) # Marking certain point of time
if state[1] == "1":
    AWG.test(True)
    stage, prev = clocker(stage, prev)
if state[2] == "1":
    VSA.test(True)
    stage, prev = clocker(stage, prev)
if state[3] == "1":
    DSO.test(True)
    stage, prev = clocker(stage, prev)
if state[4] == "1":
    ESG.test(True)
    stage, prev = clocker(stage, prev)


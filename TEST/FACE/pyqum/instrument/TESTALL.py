# For TESTING of ALL Instruments

from pyqum.instrument.logger import clocker
from pyqum.instrument.benchtop import ESG
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
ESG.test(True)
stage, prev = clocker(stage, prev) # Marking certain point of time
AWG.test(True)
stage, prev = clocker(stage, prev)
VSA.test(True)
stage, prev = clocker(stage, prev)

# Testing Combo of Modular & Benchtop
m = AWG.InitWithOptions()
AWG.debug(True)
stage, prev = clocker(stage, prev)
b = ESG.Initiate()
ESG.debug(True)
stage, prev = clocker(stage, prev)

fset = numpy.arange(1, 3, 0.2)
for freq in fset:
    ESG.frequency(b, action=['Set', freq])
    ESG.frequency(b)
    time.sleep(0.15)
ESG.close(b)
stage, prev = clocker(stage, prev)

AWG.model(m)
AWG.close(m)
stage, prev = clocker(stage, prev)

m = VSA.InitWithOptions()
m = VSA.InitWithOptions()
VSA.model(m)
VSA.close(m)

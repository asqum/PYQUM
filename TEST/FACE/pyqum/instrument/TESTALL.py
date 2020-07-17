# For TESTING of ALL Modules

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from pyqum.instrument import logger, reader, network, toolbox, analyzer
from pyqum.instrument.benchtop import MXG, DSO, ESG, PNA, ENA, PSGV, PSGA, RDSO, YOKO, GW32, KEIT, DSA8, RSA5, MXA, TKAWG
from pyqum.instrument.modular import AWG, VSA, KMAWG
from pyqum.instrument.serial import LAKE, DC
from pyqum.directive import calibrate as CAL

import inspect, numpy, time

# Testing function's name-string:
def piqom():
    '''Python Instructed Quantum Operation Modules'''
    print(Fore.BLUE + "RUNNING %s" %inspect.stack()[0][3])
piqom()

MDL = ['AWG', 'VSA', 'KMAWG', 'ENA', 'PSGV', 'PSGA', 'RDS', 'MXG', 'DSO', 'YOKO', 'LAKE', 'DC', 'GW32', 'KEIT', 'DSA8', 'RSA5', 'MXA', 'TKAWG', #instruments
        'reader', 'logger', 'network', 'toolbox', 'analyzer', #tools
        'CAL' #calibrations
        ] 
print("These modules are available for test:")
print(Fore.GREEN + str(MDL))
while True:
    selectedmdl = str(input("Pick those you'd like to test with comma between them:\n"))
    selectedmdl = selectedmdl.strip().split(',')
    for i,val in enumerate(selectedmdl):
        val = val.strip()
        if len(val) < 6: #limit up to 5 capital-letters for instruments
            selectedmdl[i] = val.upper()
        else: selectedmdl[i] = val.lower() #tools have to be more than 5 letters in lower-case
    if set(MDL) & set(selectedmdl):
        break

for i in list(set(selectedmdl) - set(MDL)): #pop those not in the list
    selectedmdl.remove(i)
print("The following modules will be tested:")
print(Fore.YELLOW + str(selectedmdl))

# Marking starting point of time:
stage, prev = logger.clocker(0)

# Testing each module individually
for mdl in selectedmdl:
    eval(mdl+".test()")
    stage, prev = logger.clocker(stage, prev) # Marking time


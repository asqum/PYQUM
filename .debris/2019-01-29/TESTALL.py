# For TESTING of ALL Instruments

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from pyqum.instrument.logger import clocker
from pyqum.instrument.benchtop import MXG, DSO, ESG, PNA, ENA, PSG, RDS
from pyqum.instrument.modular import AWG, VSA
import inspect, numpy, time

# Testing function's name-string:
def piqom():
    print(Fore.BLUE + "RUNNING %s" %inspect.stack()[0][3])
piqom()

INSTR = ['AWG', 'VSA', 'ENA', 'PSG', 'RDG', 'RDS', 'MXG', 'DSO']
print("This instrument is available:")
print(Fore.GREEN + str(INSTR))
while True:
    selectedinstrs = str(input(Fore.BLUE + "Pick those you'd like to test with comma between them:\n"))
    selectedinstrs = selectedinstrs.strip().upper().split(',')
    if set(INSTR) & set(selectedinstrs):
        break

for i in list(set(selectedinstrs) - set(INSTR)): #pop those not in the list
    selectedinstrs.remove(i)
print("The following instruments will be tested:")
print(Fore.YELLOW + str(selectedinstrs))

# Marking starting point of time:
stage, prev = clocker(0)

# Testing each machine individually
for instr in selectedinstrs:
    eval(instr+".test(True)")
    stage, prev = clocker(stage, prev) # Marking time

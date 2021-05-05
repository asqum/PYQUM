# SD AWG M3202A
from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # module's name e.g. PSG

from numpy import array, zeros, ceil, empty, float32
from pyqum.instrument.logger import address, set_status
from pyqum.instrument.analyzer import curve

# SD1 Libraries
import sys
sys.path.append('C:\Program Files (x86)\Keysight\SD1\Libraries\Python')
import keysightSD1


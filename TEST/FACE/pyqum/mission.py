# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name







print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this

@ECHO OFF

cmd /K python -c ^
"from IPython import embed; ^
from colorama import init, Fore, Back; ^
init(autoreset=True); ^
from pyqum.instrument.modular import AWG; ^
e, s = AWG.InitWithOptions(); ^
print('AWG initialized', (Fore.RED + '...Error...', Fore.GREEN + '***Success***')[e == 0]); ^
print(Fore.YELLOW + 'Session or s: {}'.format(s)); ^
print(Fore.BLACK + Back.WHITE + 'Starting Interactive Console...\n'); ^
embed();"

PAUSE
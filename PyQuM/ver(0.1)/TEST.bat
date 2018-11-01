@ECHO OFF

cd E:\NCHUQ\PYQUM\PyQuM\ver(0.1)

cmd /K python -c ^
"from IPython import embed; ^
from pyqum.instrument.modular import AWG; ^
print('Starting Interactive Console...\n'); ^
embed();"

PAUSE
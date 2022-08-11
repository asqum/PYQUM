from pyqum.instrument.modular import AWG
from IPython import embed

e, s = AWG.InitWithOptions()

print("AWG initialized")
print(("...Error...","***Success***")[e == 0])
print("Session<s>: {}".format(s))
print("Starting Interactive Console...")

embed()
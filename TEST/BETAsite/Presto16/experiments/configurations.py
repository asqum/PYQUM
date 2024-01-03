from pathlib import Path
import sys, json
print("Absolute Path: " + str(Path().absolute()))
sys.path.append(str(Path().absolute()))

qpu_dir = 'experiments/qpu'
with open(Path().absolute()/qpu_dir/"dr2b.json", 'r') as file: AS_QPU_dr2b = json.load(file)

class QPU:
    def __init__(self, dct):
        for key, value in dct.items():
            setattr(self, key, value)

dr2b = QPU(AS_QPU_dr2b)

print(f"dr2b.q4.readout_freq: {dr2b.q4['readout_freq']}")

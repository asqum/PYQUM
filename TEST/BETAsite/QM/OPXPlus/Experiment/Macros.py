from qm.qua import wait, align, set_dc_offset
from configuration import config

def cz_gate():
    dc0_q1 = config["controllers"]["con1"]["analog_outputs"][7]["offset"]
    set_dc_offset("q1_z", "single", -0.10557)
    wait(189//4, "q1_z")
    align()
    set_dc_offset("q1_z", "single", dc0_q1)
    wait(10) # for flux pulse to relax back completely



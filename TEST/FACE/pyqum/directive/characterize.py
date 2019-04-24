'''Basic QuBit Characterizations'''

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # instrument-module's name e.g. ENA, PSG, YOKO

from flask import request
from numpy import linspace, sin, pi
from pyqum.instrument.benchtop import ENA
from pyqum.instrument.logger import settings
from pyqum.instrument.analyzer import curve

@settings()
def TESTC(C1, C2, C3, C4, C5, comment='', operation="n"):
    '''Serve as a template for other real tasks to come'''
    data = 0
    for c1 in linspace(C1[0],C1[1],C1[2]):
        for c2 in linspace(C2[0],C2[1],C2[2]):
            for c3 in linspace(C3[0],C3[1],C3[2]):
                for c4 in linspace(C4[0],C4[1],C4[2]):
                    for c5 in linspace(C5[0],C5[1],C5[2]):
                        data += 1
                        yield data*1e2

@settings()
def Network_Analyzer(amp, powr, freq, ifb, iq, comment='', operation="a"):
    '''Testing Room Temperature Amplifier
        iq: [0,1,2] <I:0;Q:1> '''
    bench = ENA.Initiate()
    ENA.setrace(bench, Mparam=['S12'], window='D1')
    ENA.dataform(bench, action=['Set', 'REAL32'])
    ENA.sweep(bench, action=['Set', 'ON', freq[2]])
    fstart, fstop = freq[0], freq[1]
    ENA.linfreq(bench, action=['Set', fstart, fstop]) #F-sweep

    # Iteration part
    for ifb in linspace(ifb[0],ifb[1],ifb[2]):
        ENA.ifbw(bench, action=['Set', ifb])
        for p in linspace(powr[0],powr[1],powr[2]):
            ENA.power(bench, action=['Set', p])
            #start sweeping
            stat = ENA.sweep(bench)
            print("Time-taken would be: %s (%spts)" %(stat[1]['TIME'], stat[1]['POINTS']))
            print("Ready: %s" %ENA.measure(bench)[1])
            ENA.autoscal(bench)
            ENA.selectrace(bench, action=['Set', 'para 1 calc 1'])
            data = ENA.sdata(bench)
            for d in data:
                yield d

    ENA.rfports(bench, action=['Set', 'OFF'])
    ENA.close(bench)


def test():
    # Op = "n"
    # C = eval('[1,3000,3000]')
    # M = TESTC([0,0,1], [0.1,0.1,1], [1,1,1], C, [0,1,2], '', Op)
    # if Op.lower() != "n":
    #     M.selectday(M.whichday())
    #     M.selectmoment(1)
    #     M.accesstructure()
    #     M.loadata()
    #     print(M.selectedata[-1])
    #     M.buildata()
    #     print(M.datacontainer)
    Op = "a"
    M = Network_Analyzer([0,0,1], [-70,-50,3], [0.7e9,18e9,251], [10,10,1], [0,1,2], '', Op)
    if Op.lower() != "n":
        M.selectday(M.whichday())
        M.accesstimeline()
        print(M.startimes)
        M.selectmoment(M.whichmoment())
        M.accesstructure()
        M.loadata()
        print(M.selectedata[-1])
        M.buildata()
        print(M.datacontainer)

# test()


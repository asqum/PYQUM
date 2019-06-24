'''Basic QuBit Characterizations'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # instrument-module's name e.g. ENA, PSG, YOKO

from flask import request, session
from numpy import linspace, sin, pi, prod
from pyqum.instrument.benchtop import ENA
from pyqum.instrument.logger import settings, clocker
from pyqum.instrument.analyzer import curve
from pyqum.instrument.toolbox import cdatasearch, gotocdata, waveform

# @settings(session['user_name'], 'Sam')
@settings('ABC', 'Sam')
def TESTC(corder={}, comment='', dayindex='', taskentry=0, resumepoint=0):
    '''Serve as a template for other real tasks to come
        dayindex: {string:access data, -1:new data 0-:manage data}
        C-Order: C1, C2, C3, C4, Var
    '''
    # pushing pre-measurement parameters to settings:
    yield corder, comment, dayindex, taskentry

    # running measurement:
    C1 = waveform(corder['C1'])
    C2 = waveform(corder['C2'])
    C3 = waveform(corder['C3'])
    C4 = waveform(corder['C4'])
    Var = waveform(corder['Var'])
    buffersize = Var.count
    datasize = prod([waveform(x).count for x in corder.values()])
    # adjust check-point so that it is of multiple of buffersize lest some data will never be written:
    # checkpoint = (resumepoint+1)-(resumepoint+1)%buffersize #adjust buffer/data-mismatch but need to offset the M.insertdata as well
    data = []
    for i in range(resumepoint,datasize):
        caddress = cdatasearch(i, [C1.count,C2.count,C3.count,C4.count,Var.count])

        # User-defined M-FLOW here====================================================================================================
        x = C1.data[caddress[0]] + Var.data[caddress[4]]*C2.data[caddress[1]]*sin(pi/2*C3.data[caddress[2]]) + C4.data[caddress[3]]
        x = i + 1 #for debugging
        # ============================================================================================================================

        data.append(x)
        # saving chunck by chunck improves speed a lot!
        if not (i+1)%buffersize or i==datasize-1: #multiples of buffersize / reached the destination
            print(Fore.YELLOW + "\rProgress: %.3f%% [%s]" %((i+1)/datasize*100, data), end='\r', flush=True)
            yield data
            data = []

@settings()
def Network_Analyzer(amp, powr, freq, ifb, iq, comment=''):
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
    points = 70
    C = '1to70*%s'%points
    CORDER = {'C1':'0to0*0', 'C2':'0.1to0.1*0', 'C3':'1to1*0', 'C4':'0to12*3', 'Var':C}
    # access-only mode:
    M = TESTC()
    k = M.whichday()
    if k < 0:
        # Creating New Data:
        stage, prev = clocker(0) # Marking starting point of time
        i = prev
        M = TESTC(CORDER,'', dayindex=k)
        stage, prev = clocker(stage, prev) # Marking time lapsed
        print("Hence this pc can write 1 point for %ss" %((prev - i) / points))
    else:
        M.selectday(k)
        M.listime()
        m = M.whichmoment()
        # reading Data
        M.accesstructure()
        # use this to corrupt data to test repair capability
        # print(Fore.RED + M.resetdata())
        # M.accesstructure()
        print(Fore.CYAN + "Data complete: %s"%M.data_complete)
        print(Fore.CYAN + "Data overflow: %s"%M.data_overflow)
        print(Fore.CYAN + "Data mismatch: %s"%M.data_mismatch)
        print(Fore.MAGENTA + M.repairdata())
        M.accesstructure()
        M.loadata()
        M.buildata()
        print(M.datacontainer)
        # Manage Data
        Ma = TESTC(corder=M.corder, dayindex=k, taskentry=m, resumepoint=M.resumepoint)
        if M.data_complete: 
            print("No action taken")
        else: 
            print(Fore.LIGHTGREEN_EX + "UPDATED:")
            # reading Data
            Ma.accesstructure()
            Ma.loadata()
            Ma.buildata()
            print(Ma.datacontainer)
   

# test()


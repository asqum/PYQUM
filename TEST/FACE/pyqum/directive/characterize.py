'''Basic QuBit Characterizations'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # instrument-module's name e.g. ENA, PSG, YOKO

from flask import request, session
from numpy import linspace, sin, pi, prod, array
from pyqum.instrument.benchtop import ENA
from pyqum.instrument.logger import settings, clocker
from pyqum.instrument.analyzer import curve, IQAP, UnwraPhase
from pyqum.instrument.toolbox import cdatasearch, gotocdata, waveform

# @settings(session['user_name'], 'Sam')
@settings('ABC', 'Sam')
def TESTC(tag="", datadensity=1, instr=[], corder={}, comment='', dayindex='', taskentry=0, resumepoint=0):
    '''Serve as a template for other real tasks to come
        dayindex: {string:access data, -1:new data 0-:manage data}
        C-Order: C1, C2, C3, C4, Var
    '''
    # pushing pre-measurement parameters to settings:
    yield tag, datadensity, instr, corder, comment, dayindex, taskentry

    # User-defined Controlling-PARAMETER(s) ======================================================================================
    C1 = waveform(corder['C1'])
    C2 = waveform(corder['C2'])
    C3 = waveform(corder['C3'])
    C4 = waveform(corder['C4'])
    Var = waveform(corder['Var'])
    # ============================================================================================================================
    buffersize = Var.count
    datasize = prod([waveform(x).count for x in corder.values()])
    data = []
    for i in range(resumepoint,datasize):
        caddress = cdatasearch(i, [C1.count,C2.count,C3.count,C4.count,Var.count])

        # User-defined Measurement-FLOW ==============================================================================================
        x = C1.data[caddress[0]] + Var.data[caddress[4]]*C2.data[caddress[1]]*sin(pi/2*C3.data[caddress[2]]) + C4.data[caddress[3]]
        x = i + 1 #for debugging
        # ============================================================================================================================

        data.append(x)
        # saving chunck by chunck improves speed a lot!
        if not (i+1)%buffersize or i==datasize-1: #multiples of buffersize / reached the destination
            print(Fore.YELLOW + "\rProgress: %.3f%% [%s]" %((i+1)/datasize*100, data), end='\r', flush=True)
            yield data
            data = []

# @settings(session['user_name'], 'Sam')
@settings('ABC', 'Sam')
def F_Response(tag="", corder={}, comment='', dayindex='', taskentry=0, resumepoint=0, instr=['ENA','ENA','ENA'], datadensity=2):
    '''Characterizing 3D-cavity
    C-Order: IF-Bandwidth, Power, Frequency
    '''
    # pushing pre-measurement parameters to settings:
    yield tag, datadensity, instr, corder, comment, dayindex, taskentry

    # User-defined Controlling-PARAMETER(s) ======================================================================================
    Sparam = waveform(corder['S-Parameter'])
    ifb = waveform(corder['IF-Bandwidth'])
    powa = waveform(corder['Power'])
    freq = waveform(corder['Frequency'])
    
    # Buffer setting(s):
    buffersize = freq.count
    
    # Pre-loop settings:
    bench = ENA.Initiate()
    ENA.dataform(bench, action=['Set', 'REAL32'])
    # Freq-sweep-range settings:
    ENA.sweep(bench, action=['Set', 'ON', freq.count])
    fstart, fstop = freq.data[0]*1e9, freq.data[-1]*1e9
    ENA.linfreq(bench, action=['Set', fstart, fstop])

    # User-defined Measurement-FLOW ==============================================================================================
    datasize = prod([waveform(x).count for x in corder.values()])
    for i in range(resumepoint,datasize):

        # Registerring parameter(s)
        caddress = cdatasearch(i, [Sparam.count,ifb.count,powa.count,freq.count])

        # saving chunck by chunck improves speed a lot!
        if not (i+1)%buffersize or i==datasize-1: #multiples of buffersize / reached the destination
            ENA.setrace(bench, Mparam=[Sparam.data[caddress[0]]], window='D1')
            ENA.ifbw(bench, action=['Set', ifb.data[caddress[1]]])
            ENA.power(bench, action=['Set', powa.data[caddress[2]]])
            # start sweeping:
            stat = ENA.sweep(bench)
            print("Time-taken would be: %s (%spts)" %(stat[1]['TIME'], stat[1]['POINTS']))
            print("Operation Complete: %s" %bool(ENA.measure(bench)[1]))
            # adjusting display on ENA:
            ENA.autoscal(bench)
            ENA.selectrace(bench, action=['Set', 'para 1 calc 1'])
            data = ENA.sdata(bench)
            print(Fore.YELLOW + "\rProgress: %.3f%% [%s]" %((i+1)/datasize*100, data), end='\r', flush=True)
            yield data

    ENA.rfports(bench, action=['Set', 'OFF'])
    ENA.close(bench)
    # ============================================================================================================================

def test():
    # points = 3000
    # C = '5to9*%s'%points
    # CORDER = {'S-Parameter':'S12,S21,S22', 'IF-Bandwidth':'1000to2000*1', 'Power':'-9to-7*2', 'Frequency':C}
    # points = 1000
    # C = '0.0003to0.6*%s'%points
    # CORDER = {'S-Parameter':'S21,', 'IF-Bandwidth':'1000', 'Power':'-70', 'Frequency':C}
    points = 4000
    C = '1to10*%s'%points
    CORDER = {'S-Parameter':'S21,', 'IF-Bandwidth':'1000', 'Power':'0', 'Frequency':C}
    # Initialization:
    M = F_Response()
    k = M.whichday()
    if k < 0:
        # Creating New Data:
        stage, prev = clocker(0) # Marking starting point of time
        i = prev
        # Run NEW
        M = F_Response(corder=CORDER, comment='ISO-20-17 attenuation cross', tag='', dayindex=k)
        stage, prev = clocker(stage, prev) # Marking time lapsed
        print("Hence this pc can write 1 point for %ss" %((prev - i) / points))
    else:
        M.selectday(k)
        
        # use this to corrupt data to test repair capability
        # print(Fore.RED + M.resetdata())
        
        # Manage Data
        m = M.whichmoment()
        M.selectmoment(m)
        M.accesstructure()
        print(Fore.CYAN + "Data complete: %s"%M.data_complete)
        print(Fore.CYAN + "Data overflow: %s"%M.data_overflow)
        print(Fore.CYAN + "Data mismatch: %s"%M.data_mismatch)
        print(Fore.MAGENTA + M.repairdata())
        M.loadata()
        M.buildata()
        print(M.datacontainer)

        Ma = F_Response(corder=M.corder, dayindex=k, taskentry=m, resumepoint=M.resumepoint)

        if M.data_complete: 
            print("No action taken")
            # reading Data
            Ma.accesstructure()
            cstructure = [waveform(Ma.corder['S-Parameter']).count,waveform(Ma.corder['IF-Bandwidth']).count,waveform(Ma.corder['Power']).count,waveform(Ma.corder['Frequency']).count*2]
            Ma.loadata()
            X = waveform(C).data
            selected = [Ma.selectedata[gotocdata([0, 0, 0, x], cstructure)] for x in range(waveform(Ma.corder['Frequency']).count*2)]
            yI, yQ, Amp, Pha = IQAP(array(selected))
            print(len(Amp)==len(X))
            curve(X, Amp, 'Freq response S12', 'f(GHz)', 'Amp(dB)')
            curve(X, Pha, 'Freq response S12', 'f(GHz)', 'Pha(rad)')
            curve(X, UnwraPhase(X,Pha), 'Freq response S12', 'f(GHz)', 'Unwrapped-Phase(deg)')

        else: 
            print(Fore.LIGHTGREEN_EX + "UPDATED:")
            # reading Data
            Ma.accesstructure()
            Ma.loadata()
            Ma.buildata()
            print(Ma.datacontainer)
   

# test()


from numpy import sqrt, array, mean, sum, min, max
from sklearn.preprocessing import minmax_scale

from pyqum.instrument.logger import set_status
from pyqum.instrument.toolbox import waveform, gotocdata
from pyqum.instrument.analyzer import curve, IQAParray, UnwraPhase


# 3. Test Square-wave Pulsing
from pyqum.directive.characterize import SQE_Pulse

CStructure = ['Flux-Bias', 
                'XY-Frequency', 'XY-Power', 'RO-Frequency', 'RO-Power',
                'Pulse-Period', 
                'RO-ifLevel', 'RO-Pulse-Delay', 'RO-Pulse-Width', 
                'XY-ifLevel', 'XY-Pulse-Delay', 'XY-Pulse-Width', 
                'LO-Frequency', 'LO-Power', 'ADC-delay', 'Average', 'Sampling-Time']

if True:
    # Access data:
    Logs = SQE_Pulse('abc')
    Logs.selectday(Logs.whichday())
    m = Logs.whichmoment()
    Logs.selectmoment(m)
    print("File selected: %s" %Logs.pqfile)
    Logs.accesstructure()

    print("Loading parameters:\n")
    print(Logs.corder)

    # select from data
    Logs.loadata()
    alldata = Logs.selectedata
    structure = Logs.corder['C-Structure']
    cstructure = [waveform(Logs.corder[param]).count for param in structure][:-1] + [waveform(Logs.corder[structure[-1]]).count * Logs.datadensity]
    print('cstructure: %s' %cstructure)
    timesweep = range(waveform(Logs.corder['Sampling-Time']).count*Logs.datadensity)

    # choosing c-parameters:
    C = dict(xyl='XY-ifLevel', tau='XY-Pulse-Width', xyp='XY-Power', xyf='XY-Frequency', rof='RO-Frequency', flx='Flux-Bias')
    C_option = input("Choose among c-constants: (%s)" %[x for x in C.keys()])
    C_index = input("Enter index 0-%s << "%(waveform(Logs.corder[C[C_option]]).count - 1))
    print("C-parameter <%s> set at {%s}" %(C[C_option],waveform(Logs.corder[C[C_option]]).data[int(C_index)]))

    # choosing x-parameters:
    X = dict(xyl='XY-ifLevel', xyf='XY-Frequency', rof='RO-Frequency', rabi='XY-Pulse-Width', t1='RO-Pulse-Delay', flx='Flux-Bias', xyp='XY-Power')
    X_option = input("Choose among x-parameters: (%s)" %[x for x in X.keys()])
    xdata = waveform(Logs.corder[X[X_option]]).data # x-range
    print('%s is selected as X' %X[X_option])
    
    # write address based on x-parameter picked:
    caddress = '[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,t]' #bare
    # caddress = '[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,t]' #dressed
    # replacing x-variable:
    caddress = caddress[:2*CStructure.index(X[X_option])+1] + 'i' + caddress[2*CStructure.index(X[X_option])+2:]
    # replacing c-constant:
    caddress = caddress[:2*CStructure.index(C[C_option])+1] + C_index + caddress[2*CStructure.index(C[C_option])+2:]
    print("C-Address: %s" %(caddress))

    # Sweep first curve to decide:
    IQdata = array([alldata[gotocdata([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, x], cstructure)] for x in timesweep])
    I, Q, Amp, Pha = IQAParray(IQdata)
    A = [sqrt(i**2+q**2) for (i,q) in zip(I,Q)] # slower iteration
    # select which range you need from the curve:
    curve(range(len(I)), I, 'Pick the start-end point:', '#', 'A(V)')
    curve(range(len(Q)), Q, 'Pick the start-end point:', '#', 'A(V)')
    curve(range(len(A)), A, 'Pick the start-end point:', '#', 'A(V)')
    
    # assemble the analytics
    startpoint = int(input("Reading the measured pulse from: "))
    endpoint = int(input("Reading the measured pulse until: "))
    firstpoint = int(input('Total %s points, plot from: ' %len(xdata)))
    lastpoint = int(input('Total %s points, plot until: ' %len(xdata)))

    # Start post-averaging:
    iA, aphase, aAmp, Asquare, Isquare, Qsquare = [], [], [], [], [], []
    for i in range(firstpoint,lastpoint):
        if not i%10:
            print("\rprocessing %s/%s" %(i,lastpoint), end='\r', flush=True)
        
        # extract IQ:
        IQdata = array([alldata[gotocdata(eval(caddress), cstructure)] for t in timesweep])
        I, Q, Amp, Pha = IQAParray(IQdata)
        A = sqrt(I**2 + Q**2)

        if X_option == 'rabi' or X_option == 't1':
            A2 = A[startpoint:endpoint+1]**2
            Asquare.append(sum(A2))
            I2 = [x**2 for x in I[startpoint:endpoint+1]]
            Isquare.append(sum(I2))
            Q2 = [x**2 for x in Q[startpoint:endpoint+1]]
            Qsquare.append(sum(Q2))
        else:
            aAmp.append(mean(Amp[startpoint:endpoint+1]))
        
        iA.append(mean(A[startpoint:endpoint+1]))
        aphase.append(mean(Pha[startpoint:endpoint+1])) # maybe just the difference between start- & end-point?

    # plotting:
    X = xdata[firstpoint:lastpoint]
    if X_option == 'rabi' or X_option == 't1':
        if input("Press Any-Keys (Enter) to normalize (skip)"):
            curve(X,minmax_scale(array(iA)),'mean V','t(ns)','A(V)','ok')
            curve(X,minmax_scale(array(Asquare)),'Population by V^2dt','t(ns)','P','.k')
            curve(X,minmax_scale(array(Isquare)),'I-Population','t(ns)','<I(V)^2>',':k')
            curve(X,minmax_scale(array(Qsquare)),'Q-Population','t(ns)','<Q(V)^2>',':k')
        else:
            curve(X,iA,'mean V','t(ns)','A(V)','ok')
            curve(X,Asquare,'Population by V^2dt','t(ns)','P','.k')
            curve(X,Isquare,'I-Population','t(ns)','<I(V)^2>',':k')
            curve(X,Qsquare,'Q-Population','t(ns)','<Q(V)^2>',':k')
    else:
        curve(X,array(iA),'','','A(V)',':k')
        curve(X,aAmp,'','','Amp(dBm)')
    curve(X,aphase,'','','Pha(rad)','.k')


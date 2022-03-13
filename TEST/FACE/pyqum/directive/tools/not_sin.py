import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score
from scipy import optimize
from datetime import datetime
import warnings  
warnings.filterwarnings("ignore")  
#---------------define function---------------
def fit_plot(i,ax,coef):return coef[0]*ax*ax+coef[1]*ax+coef[2]

def output_cal(x,valid,ki,fdress,plot):
    #---------------using difference to find upward points---------------
    dif=valid.diff(periods=1, axis=0)['fr']; dif[0] = 0
    last,count = -1,-1
    valid_u, coef_u, poly_u, fit_u, x0_u, r2_u,ax_u, wave,fd = [],[],[],[],[],[],[],[],[]
    for i in valid[(dif>ki)]['index'].keys():
        if last == -1:last = i
        else:
            if len(valid[(valid['fr']>fdress)&(valid['index']>last)&(valid['index']<i)])<3:
                last = i
                pass
            else:
                wave.append(count)
                valid_u.append(valid[(valid['fr']>fdress)&(valid['index']>last-1)&(valid['index']<i)])
                last = i
        count+=1   
    valid_u.append(valid[(valid['fr']>fdress)&(valid['index']>last)&(valid['index']<max(x)*10**6)])
    # print(valid_u)
    wave.append(count)
    for i in range(len(valid_u)):
        coef_u.append(np.polyfit(valid_u[i]['flux'],valid_u[i]['fr'],2))
        poly_u.append(np.poly1d(coef_u[i]))
        fit_u.append(np.polyval(coef_u[i],valid_u[i]['flux']))
        ax_u.append(range(int(valid_u[i]['flux'][valid_u[i]['flux'].keys()[0]])-5,int(valid_u[i]['flux'][valid_u[i]['flux'].keys()[-1]])+5))
        fd.append(min(valid_u[i]['fr']))
        r2_u.append(r2_score(valid_u[i]['fr'], fit_u[i]))
        if coef_u[i][0]!=0:
            x0_u.append(round(-0.5*coef_u[i][1]/coef_u[i][0],2))
        else:
            raise ValueError('Fail to fit.')

    #---------------using Squeeze Theorem find the only one downward function between the minimum points of two upward function---------------
    if len(x0_u)<2 and len(wave)<2:
        raise ValueError('The data does not have enough points to find wavelength. Please add more point')

    wavelength,cavity_range,valid_ca,coef_ca, poly_ca, fit_ca, x0_ca, r2_ca ,fc,ax_ca = [],[],[],[],[],[],[],[],[],[]
    success =-1
    for i in range(len(x0_u)-1):wavelength.append((x0_u[i+1]-x0_u[i])/(wave[i+1]-wave[i]))
    avg_wavelength = np.average(wavelength)
    for i in range(wave[-1]):
        if wave[i] == i:
            cavity_range.append([x0_u[i],x0_u[i]+avg_wavelength])
            success = i
        elif wave[i]!= i:
            if wave[i]== i+1:
                cavity_range.append([x0_u[i]-avg_wavelength,x0_u[i]])
            elif success != -1:
                cavity_range.append([x0_u[success]+(i-success)*avg_wavelength,x0_u[success]+(i-success+1)*avg_wavelength])
            else:
                pass
    # print("cavity_range = ",cavity_range)
    for i in range(len(cavity_range)):
        valid_ca.append(valid[(valid['fr']<np.average(fd)-ki)&(valid['flux']>cavity_range[i][0])&(valid['flux']<cavity_range[i][1])])
        # print(np.average(fd)-ki)
        # print(valid['fr'])
        # print(valid['fr']<np.average(fd)-ki)
        # print(valid_ca[i])
        coef_ca.append(np.polyfit(valid_ca[i]['flux'],valid_ca[i]['fr'],2))
        poly_ca.append(np.poly1d(coef_ca[i]))
        fit_ca.append(np.polyval(coef_ca[i],valid_ca[i]['flux']))
        ax_ca.append(range(int(valid_ca[i]['flux'][valid_ca[i]['flux'].keys()[0]])-5,int(valid_ca[i]['flux'][valid_ca[i]['flux'].keys()[-1]])+5))
        fc.append(max(valid_ca[i]['fr']))
        r2_ca.append(r2_score(valid_ca[i]['fr'], fit_ca[i]))
        if coef_ca[i][0]!=0:
            x0_ca.append(round(-0.5*coef_ca[i][1]/coef_ca[i][0],2))
        else:
            raise ValueError('Fail to fit.')
    #---------------print the conclusion---------------
    print("R2_ERROR :\n\t","{:<18}".format("Avg_Dressed Cavity")," : ","{:.4f}".format(np.average(r2_u)*100),"%\n\t","{:<18}".format("Avg_Cavity")," : ","{:.4f}".format(np.average(r2_ca)*100),"%\n")
    print("{:<11}".format("Avg_fdress")+" : "+ "{:.4f}".format(np.average(fd))+" GHz "+" ; "+"{:<11}".format("Var_fdress")+" : "+ "{:.4f}".format(np.var(fd)*10**6)+" kHz")
    print("{:<11}".format("Avg_fcavity")+" : "+ "{:.4f}".format(np.average(fc))+" GHz "+" ; "+"{:<11}".format("Var_fcavity")+" : "+ "{:.4f}".format(np.var(fc)*10**6)+" kHz\n")
    print("{:^29}".format("Expected")+"|"+"{:^14}".format("Actual")+"\n"+"-"*44)
    print("{:^14}".format("flux(uV/A)")+"|"+"{:^14}".format("freq(GHz)")+"|"+"{:^14}".format("fc(GHz)")+"\n"+"-"*44)
    for i in range(len(valid_u)):
        print("{:^14.2f}".format(x0_u[i])+"|"+"{:^14.4f}".format(poly_u[i](x0_u[i]))+"|"+"{:^14.4f}".format(min(valid_u[i]['fr'])))
    print("-"*44)
    for i in range(len(cavity_range)):
        print("{:^14.2f}".format(x0_ca[i])+"|"+"{:^14.4f}".format(poly_ca[i](x0_ca[i]))+"|"+"{:^14.4f}".format(min(valid_ca[i]['fr'])))
    

    if plot ==1:
        #---------------plot the calculation conclusion---------------
        plt.rcParams["figure.figsize"] = [20,10]
        plt.scatter(valid['flux'],valid['fr'],color='black', marker='o',label='real')
        for i in range(len(valid_u)):
            plt.scatter(valid_u[i]['flux'],valid_u[i]['fr'],color='blue', marker='o',label='real')
            plt.plot(ax_u[i],fit_plot(i,ax_u[i],coef_u[i]),'g',label='curve_fit')
            plt.plot([x0_u[i]]*5,np.linspace(min(valid_u[i]['fr'])-.0125,max(valid_u[i]['fr'])+.0125,5),'r--')
            
        for i in range(len(cavity_range)):
            plt.scatter(valid_ca[i]['flux'],valid_ca[i]['fr'],color='blue', marker='o')
            plt.plot(ax_ca[i],fit_plot(i,ax_ca[i],coef_ca[i]),'g')
            plt.plot([x0_ca[i]]*5,np.linspace(min(valid_ca[i]['fr'])-.0125,max(valid_ca[i]['fr'])+.0125,5),'r--')
            
        title2 = "avg_fc : "+ "{:.4f}".format(np.average(fc)) +" GHz ; avg_r2_score = "+"{:.2f}".format(np.average(r2_ca)*100)+"%"+" ;   " +datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        plt.title(title2)
        plt.xlabel("Flux : uV/A")
        plt.ylabel("Freq : GHz")
        # plt.legend()
        plt.savefig(r'C:\Users\ASQUM\Documents\GitHub\PYQUM\TEST\FACE\pyqum\static\img\fitness.png')
    return float("{:.6f}".format(np.average(fc))),float("{:.6f}".format(np.average(fd))),x0_ca[0]

def fit_sin(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    guess_freq = abs(ff[np.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = np.std(yy) * 2.**0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 2.*np.pi*guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c):  return A * np.sin(w*t + p) + c
    popt, pcov = optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*np.pi)
    fitfunc = lambda t: A * np.sin(w*t + p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": np.max(pcov), "rawres": (guess,popt,pcov)}

def output_cal_sin(valid,plot):
    fc = float("{:.6f}".format(min(valid['fr'])))
    fd = float("{:.6f}".format(max(valid['fr'])))
    offset = valid[(valid['fr']==min(valid['fr']))]['flux'].values[0]
    #https://stackoverflow.com/questions/16716302/how-do-i-fit-a-sine-curve-to-my-data-with-pylab-and-numpy
    res = fit_sin(valid['flux'],valid['fr'])
    print("{:^16}".format("Amplitude")+" = "+ "{:>8.4f}".format(float(res['amp']))+" GHz")
    print("{:^16}".format("Angular freq.")+" = "+ "{:>8.4f}".format(float(res['omega']))+" uV/A")
    print("{:^16}".format("phase")+" = "+ "{:>8.4f}".format(float(res['phase']))+" uV/A")
    print("{:^16}".format("offset")+" = "+ "{:>8.4f}".format(float(res['offset']))+" GHz")
    print("{:^16}".format("Max. Covariance")+" = "+ "{:>8.4f}".format(float(res['maxcov'])))
    x = np.linspace(0,200,200)
    
    if plot ==1:
        #---------------plot the calculation conclusion---------------
        plt.rcParams["figure.figsize"] = [20,10]
        plt.scatter(valid['flux'],valid['fr'],color='black', marker='o',label='real')
        plt.plot(x, res["fitfunc"](x), "r-", label="y fit curve", linewidth=2)
        title2 = "fc : "+ "{:.4f}".format(fc) +" GHz ; max_convariance = "+"{:.4f}".format(float(res['maxcov']))+" ;  " +datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        plt.title(title2)
        plt.xlabel("Flux : uV/A")
        plt.ylabel("Freq : GHz")
        # plt.legend()
        plt.savefig(r'C:\Users\ASQUM\Documents\GitHub\PYQUM\TEST\FACE\pyqum\static\img\fitness.png')
    return float("{:.6f}".format(fc)),float("{:.6f}".format(fd)),offset
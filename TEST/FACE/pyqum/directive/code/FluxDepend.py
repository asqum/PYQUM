from numpy import array, mean, pi, std, argmax, max, sin
from numpy.fft import fft, fftfreq
from scipy.optimize import curve_fit
from pandas import DataFrame
# from scipy.io import loadmat
from pyqum.directive.code.tools.circuit import notch_port
#---------------define function---------------
def flux_load_data(data):
    ''' 
        mat form
        x = Flux-Bias(V/A) ; y = freq(GHz) ;
        I , Q ;
        A = 20*log10(sqrt(I**2 + Q**2)) ;
        P = arctan2(Q, I) # -pi < phase < pi
        
        output  = self.dataframe pandas dataframe
    '''

    #---------------examine the data structure---------------
    # for i in mat.keys():
    #     if i.find('_')==-1:
    #         print(i,' is a ',len(mat[i]),'*',len(mat[i][0]),' matrix')
    # print('x = ',mat['xtitle'][0],'\ny = ',mat['ytitle'][0])

    #---------------prepare data ---------------
    df1=DataFrame()
    fr = []
#     for j in range(len(data)):
#         flux,freq,I,Q,A,P= [],[],[],[],[],[]
#         for i in range(len(mat['y'][0])):
#                 flux.append(mat['x'][0][j]);freq.append(mat['y'][0][i])
#                 I.append(mat['ZZI'][i][j]);Q.append(mat['ZZQ'][i][j])
#         df =DataFrame({"Frequency":freq,"Flux-Bias":flux,"i":I,"q":Q}).sort_values(["Frequency","Flux-Bias"],ascending=True)
#         port1 = notch_port(f_data=df["Frequency"].values,z_data_raw=df["i"]+1j*df["q"])
#         port1.autofit()
#         fr.append(port1.fitresults['fr'])
    for i in data["Flux-Bias"].unique():
        port1 = notch_port(f_data=data[data["Flux-Bias"]==i]["Frequency"].values,z_data_raw=data[data["Flux-Bias"]==i]["I"]+1j*data[data["Flux-Bias"]==i]["Q"])
        port1.autofit()
        fr.append(port1.fitresults['fr'])
    df1.insert(loc=0, column='fr', value = array(fr)*10**3)
    df1.insert(loc=0, column='flux', value = data["Flux-Bias"].unique()*10**6)
    #---------------drop the outward data---------------
    f_min,f_max = min(data["Frequency"].unique())*1000,max(data["Frequency"].unique())*1000
    valid = df1[(df1['fr']>= f_min)&(df1['fr']<= f_max)]
    valid.reset_index(inplace=True)
    valid = valid.drop(labels=['index'], axis="columns")
    return valid

def fit_sin(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt,yy = array(tt),array(yy)
    ff = fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(fft(yy))
    guess_freq = abs(ff[argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp, guess_offset = std(yy) * 2.**0.5, mean(yy)
    guess = array([guess_amp, 2.*pi*guess_freq, 0., guess_offset])
    def sinfunc(t, A, w, p, c):  return A * sin(w*t + p) + c
    popt, pcov = curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*pi)
    fitfunc = lambda t: A * sin(w*t + p) + c
    return {"amp": A, "omega": w, "phase": p,"mean" :c, "offset": max(yy), "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": max(pcov), "rawres": (guess,popt,pcov)}



from pandas import DataFrame
from numpy import array
from numpy import stack, quantile
# import matplotlib.pyplot as plt
# from scipy.io import loadmat  # this is the SciPy module that loads mat-files
from pyqum.directive.code.tools.circuit import notch_port

def loadmat_valid(data):
    ''' 
        mat form
        x = Flux-Bias(V/A) ; y = freq(GHz) ;
        I , Q ;
        A = 20*log10(sqrt(I**2 + Q**2)) ;
        P = arctan2(Q, I) # -pi < phase < pi
        
        output  = self.dataframe pandas dataframe
    '''
#     mat = loadmat(path)
    df1=DataFrame()
    fr = []
    for i in data["Power"].unique():
        port1 = notch_port(f_data=data[data["Power"]==i]["Frequency"].values,z_data_raw=data[data["Power"]==i]["I"]+1j*data[data["Power"]==i]["Q"])
        port1.autofit()
        fr.append(port1.fitresults['fr'])
    df1.insert(loc=0, column='fr', value = array(fr))
    df1.insert(loc=0, column='power', value = data["Power"].unique())
#     for j in range(len(mat['x'][0])):
#         power,freq,I,Q,A,P,df= [],[],[],[],[],[],[]
#         for i in range(len(mat['y'][0])):
#                 power.append(mat['x'][0][j]);freq.append(mat['y'][0][i])
#                 I.append(mat['ZZI'][i][j]);Q.append(mat['ZZQ'][i][j])
#                 # A.append(mat['ZZA'][i][j]);P.append(mat['ZZP'][i][j])
#         # df =DataFrame({"Frequency":freq,"Power":power,"p":P,"a":A,"i":I,"q":Q}).sort_values(["Frequency","Power"],ascending=True)
#         df =DataFrame({"Frequency":freq,"Power":power,"i":I,"q":Q}).sort_values(["Frequency","Power"],ascending=True)
#         port1 = notch_port(f_data=df["Frequency"].values,z_data_raw=df["i"]+1j*df["q"])
#         # port1.plotrawdata()
#         port1.autofit()

#         # port1.plotall()
#         # display(DataFrame([port1.fitresults]).applymap(lambda x: "{0:.2e}".format(x)))
#         df1 = df1.append(DataFrame([port1.fitresults]), ignore_index = True)
#     df1.insert(loc=0, column='power', value=mat['x'][0])

    #---------------drop the outward data---------------
    f_min,f_max = min(data['Frequency']),max(data['Frequency'])
    valid = df1[(df1['fr']>= f_min)&(df1['fr']<= f_max)]
    valid.reset_index(inplace=True)
    power = valid['power']
    fr = valid['fr']*1000
    data = stack((power,fr), axis=1)
    return data

def outlier_detect(data,label):
    error_label = 1
    class0_label ,class1_label = 0,2
    label = class1_label* label
    iteration = 3
    threshold = 1.75
    IQR_end = 0.006
    upquantile,lowquantile=.45,.55
    for i in range(iteration):
        Q1_0 = quantile(data[:,1][label==class0_label],upquantile)
        Q3_0 = quantile(data[:,1][label==class0_label],lowquantile)
        IQR_0 = Q3_0 - Q1_0
        Q1_1 = quantile(data[:,1][label==class1_label],upquantile)
        Q3_1 = quantile(data[:,1][label==class1_label],lowquantile)
        IQR_1 = Q3_1 - Q1_1
        print("IQR :"+"{:.4f}".format(IQR_0)+" ; "+"{:.4f}".format(IQR_1))
        for i in range(len(label)):
            if label[i]==class0_label:
                if IQR_0 <IQR_end:
                    pass
                elif((data[:,1][i] < (Q1_0 - threshold * IQR_0))| (data[:,1][i] > (Q3_0 + threshold * IQR_0))):
                    label[i]=error_label
            if label[i]==class1_label:
                if IQR_1 <IQR_end:
                    pass
                elif((data[:,1][i] < (Q1_1 - threshold * IQR_1))| (data[:,1][i] > (Q3_1 + threshold * IQR_1))):
                    label[i]=error_label
        if (IQR_0<IQR_end)&(IQR_1<IQR_end):
            print('end')
            break
    return label

def cloc(label_new):
    min_0,min_1, min_2 = -1,-1,-1
    error_label = 1
    class0_label ,class1_label = 0,2
    for i in range(len(label_new)):
        if min_0 != -1 | min_1 != -1| min_2 != -1:
            break
        if label_new[i]==error_label:
            if ((min_0 != -1) | (min_1 != -1))&(min_2== -1):
                min_2 = i
        elif label_new[i]==class0_label:
            if min_0 == -1:
                min_0 = i
        elif label_new[i]==class1_label:
            if min_1 == -1:
                min_1 = i
#     print(min_0,min_1,min_2)
    if min_2 != -1:
        if min_0<min_1:
            min_0 = min_2-3
        else:
            min_1 = min_2-3
    else:
        if min_0<min_1:
            min_0 = min_1-4
        else:
            min_1 = min_0-4
    return min_0,min_1


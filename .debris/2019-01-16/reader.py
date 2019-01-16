'''For reading file'''

# Analytics
def IQAP(datas):
    # Slicing datas into IQ-data
    IQdata = datas.reshape(len(datas)/2, 2)
    Idata, Qdata = IQdata[:,0], IQdata[:,1]
    yI, yQ = [float(i) for i in Idata], [float(i) for i in Qdata]
    Amp, Pha = [], []
    for i in zip(yI, yQ):
        Amp.append(20*log10(sqrt(i[0]**2 + i[1]**2)))
        Pha.append(arctan2(i[1], i[0])) # -pi < phase < pi
    return yI, yQ, Amp, Pha
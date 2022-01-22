
# Numpy
# 
from numpy import linspace, arange
# Numpy common math function
from numpy import exp
# Numpy constant
from numpy import pi

class Qubit():
    
    def __init__ (self):

        self.qubitFreq = 0
        self.drivingPower = 0
        self.couplingStrength = 10
        self.anharmonicity = -100 #MHz w12 -w01
def gaussianFunc (t, p):
    # p[0]: amp
    # p[1]: sigma
    # p[2]: peak position
    return p[0] *exp( -( (t-p[2]) /p[1] )**2 /2)
def derivativeGaussianFunc (t, p):
    # p[0]: amp
    # p[1]: sigma
    # p[2]: peak position
    return -p[0] / p[1]**2 *(t-p[2]) *exp( -( (t-p[2]) /p[1] )**2 /2)
class Gate():

    def __init__( self, qubit, startPt, operationPts, timeResolution =1.0):

        # pt = point
        self.startPt = 0
        self.operationPts = 20

        self.timeResolution = 0.5 #ns/sample
        self.pulseInfo = {
            "qubit": qubit,
            "envelope": {
                "shape": 'gaussian',
                "paras": [1,0.25],
            },
            "phase": pi/2 ,
        }

    def cal_controlPulse( self ):

        relativeTime = arange(self.operationPts) *self.timeResolution
        absoluteTime = relativeTime +self.startPt *self.timeResolution

        operationTime = self.operationPts *self.timeResolution
        def get_gaussian():
            centerTime = operationTime /2
            amp = self.pulseInfo["envelope"]["paras"][0]/self.pulseInfo["qubit"].couplingStrength
            sigma = operationTime *self.pulseInfo["envelope"]["paras"][1]
            p = [amp, sigma, centerTime]
            waveform = gaussianFunc(relativeTime, p )+ 0j
            return waveform

        def get_DRAG():
            centerTime = self.operationPts *self.timeResolution /2
            amp = self.pulseInfo["envelope"]["paras"][0]/self.pulseInfo["qubit"].couplingStrength
            sigma = operationTime *self.pulseInfo["envelope"]["paras"][1]

            pGau = [ amp, sigma, centerTime ]

            ampDGau = amp/(self.pulseInfo["qubit"].anharmonicity/1e3)
            pDGau = [ ampDGau, sigma, centerTime ]
            waveform = gaussianFunc(relativeTime, pGau )+ 1j *derivativeGaussianFunc(relativeTime, pDGau)

            return waveform
        pulse = {
            'gaussian': get_gaussian,
            'DRAG': get_DRAG,
        }
        return {"x":absoluteTime,"y":pulse['DRAG']()*exp(1j*self.pulseInfo["phase"])}




if __name__ == "__main__":
    import matplotlib.pyplot as plt
    Q=Qubit()
    print("init")
    A = Gate(Q,0,100)
    print("cal_controlPulse")
    B= A.cal_controlPulse()
        
    plot1 = plt.figure(1)
    plt.plot(B["x"], B["y"].real)
    plt.plot(B["x"], B["y"].imag)
    plot2 = plt.figure(2)
    plt.plot(B["y"].real, B["y"].imag)

    plt.show()






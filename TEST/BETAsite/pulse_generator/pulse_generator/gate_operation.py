# Numpy
# 
from numpy import linspace, arange
# Numpy array
from numpy import array, append
# Numpy common math function
from numpy import exp
# Numpy constant
from numpy import pi

import hardware_information as phyCh

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



#     def set_QubitRegister():
def arbXYGate( p ):
    theta, phi = p
    pulseInfo = {
        "envelope": {
            "shape": 'gaussian',
            "paras": [theta/pi,0.25],
            },
        "phase": phi,
    }
    return pulseInfo
def xGate():
    pulseInfo = {
        "phase": 0,
    }
    return pulseInfo
    
class Operation():
    def __init__( self, functionName):
        self.functionName = functionName
        self.time = 20

class OperationSequence():

    def __init__( self, hardwareInfo):

        self.hardwareInfo = hardwareInfo
        self.operation = []
        self.sequenceTime = 0
        self.sequencePts = 0
        self.waveform = {
            "t0": 0.,
            "dt": 1.,
            "y": array([])
            }
    def set_operation( self, operation ):
        
        self.operation = operation

    
    def cal_pulseSequence( self ):

        allPulse = array([])
        mPulse = MicrowavePulse(hardwareInfo=self.hardwareInfo)
        for i, operation in enumerate(self.operation):
            pulseType = {
                'x': (1,0),
                'y': (1,pi/2),
            } 
            pulseInfo = arbXYGate(pulseType[operation.functionName])
            mPulse.startTime = self.sequenceTime
            mPulse.operationTime = operation.time

            mPulse.pulseInfo.update(pulseInfo)
            newPulse = mPulse.cal_controlPulse()["y"]
            allPulse = append(allPulse, newPulse)

            self.sequencePts += len(newPulse)
        self.sequenceTime = self.sequencePts *self.hardwareInfo.timeResolution

        self.waveform.update({"y":allPulse})
        return self.waveform
    def get_timeAxis( self ):

        return linspace(0 ,self.sequenceTime, self.sequencePts ,endpoint=False)

class MicrowavePulse():

    def __init__( self, startTime=None, operationTime=None, hardwareInfo=None, pulseInfo=None):

        # pt = point
        self.startTime = startTime
        self.operationTime = operationTime
        self.timeResolution = hardwareInfo.timeResolution # ns/sample
        self.operationPts = 0

        self.hardwareInfo = hardwareInfo
        self.pulseInfo = {
            "envelope": {
                "shape": 'gaussian',
                "paras": [1,0.25],
            },
            "phase": 0,
        }
        #self.pulseInfo.update(pulseInfo)

    def cal_controlPulse( self ):
        self.operationPts = int(self.operationTime//self.timeResolution)

        relativeTime = linspace(0,self.operationTime,self.operationPts,endpoint=False)
        absoluteTime = relativeTime +self.startTime

        operationTime = self.operationTime
        def get_gaussian():
            centerTime = operationTime /2
            amp = self.pulseInfo["envelope"]["paras"][0]/self.hardwareInfo.Qubit.couplingStrength
            sigma = operationTime *self.pulseInfo["envelope"]["paras"][1]
            p = [amp, sigma, centerTime]
            waveform = gaussianFunc(relativeTime, p )+ 0j
            return waveform

        def get_DRAG():
            self.hardwareInfo
            centerTime = self.operationPts *self.timeResolution /2
            amp = self.pulseInfo["envelope"]["paras"][0]/self.hardwareInfo.Qubit.couplingStrength
            sigma = operationTime *self.pulseInfo["envelope"]["paras"][1]

            pGau = [ amp, sigma, centerTime ]

            ampDGau = amp/(self.hardwareInfo.Qubit.anharmonicity/1e3)
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
    
    print("register Qubit")
    q1 = phyCh.Qubit()
    print("register IQMixerChannel")
    m1 = phyCh.IQMixerChannel()    
    print("register InputPort")
    p1 = phyCh.InputPort()

    print("register HardwareInfo")
    pch1 = phyCh.HardwareInfo(q1,m1,p1) 

    print("init OS")
    OPS = OperationSequence(pch1)

    print("set new operation")
    op1 = Operation('x')
    op2 = Operation('y')

    print("register operation to sequence")
    OPS.set_operation([op1,op2])

    print("calculate waveform of the sequence")
    B= OPS.cal_pulseSequence()
        
    plot1 = plt.figure(1)
    timeAxis = OPS.get_timeAxis()
    plt.plot(timeAxis, B["y"].real)
    plt.plot(timeAxis, B["y"].imag)
    plot2 = plt.figure(2)
    plt.plot(B["y"].real, B["y"].imag)

    plt.show()



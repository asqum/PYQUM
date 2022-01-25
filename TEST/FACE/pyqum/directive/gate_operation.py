# Numpy
# 
from numpy import linspace, arange
# Numpy common math function
from numpy import exp
# Numpy constant
from numpy import pi

from pyqum.directive.qubit_prop import Qubit

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

# class QuantumCircuit():
#     def __init__( self, qubits, sample=None ):

#         self.qubits = qubits

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
class OperationSequence():

    def __init__( self, qubit, timeResolution =1.0):

        self.qubit = qubit
        self.gate = []
        self.unitGateTime = 20
        self.OperationSequenceTime = 0

    def set_gates( self, gates ):

        for op in gates:
            pulseType = {
                'x': (1,0),
                'y': (1,pi/2),
            } 
            pulseInfo = arbXYGate(pulseType[op])
            sqo = SingleQOperation(self.qubit, self.OperationSequenceTime, self.unitGateTime, pulseInfo)
            self.OperationSequenceTime += self.unitGateTime


class SingleQOperation():

    def __init__( self, qubit, startTime, operationTime, pulseInfo):

        # pt = point
        self.startTime = startTime
        self.operationTime = operationTime

        self.timeResolution = 0.5 #ns/sample
        self.pulseInfo = {
            "qubit": qubit,
            "envelope": {
                "shape": 'gaussian',
                "paras": [1,0.25],
            },
            "phase": 0,
        }
        self.pulseInfo.update(pulseInfo)

    def cal_controlPulse( self ):

        relativeTime = iinspace(0,self.operationTime,endpoint=False)
        absoluteTime = relativeTime +self.startTime

        operationTime = self.operationTime
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
    print("init Q")
    Q = Qubit()

    print("init OS")
    OP = OperationSequence(Q)

    print("set gate")
    OP.set_gates(['x','x'])

    print("cal_controlPulse")
    B= A.cal_controlPulse()
        
    plot1 = plt.figure(1)
    plt.plot(B["x"], B["y"].real)
    plt.plot(B["x"], B["y"].imag)
    plot2 = plt.figure(2)
    plt.plot(B["y"].real, B["y"].imag)

    plt.show()



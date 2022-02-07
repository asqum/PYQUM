# Numpy
# 
from numpy import linspace, arange
# Numpy array
from numpy import array, append, zeros, ones
# Numpy common math function
from numpy import exp, sqrt, arctan2, cos, sin, angle, radians, sign, log
# Numpy constant
from numpy import pi
from pandas import infer_freq

import pulse_generator.hardware_information as phyCh

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
def constFunc (t, p):
    # p[0]: amp
    return p[0]*ones(len(t))


#     def set_QubitRegister():

class Operation():
    def __init__( self, time, functionName):
        self.functionName = functionName
        self.time = time
        self.operationPts = 0 # AWG length
        self.operationStartPt = 0 # Start Index
        self.pulseInfo = {
            "envelope": {
                "shape": 'gaussian',
                "paras": [1,0.25],
            },
            "phase": 0,
        }

    def arbXYGate( self, p ):
        theta, phi = p
        pulseInfo = {
            "envelope": {
                "shape": 'DRAG',
                "paras": [theta/pi,0.25],
                },
            "phase": phi,
        }
        return self.pulseInfo.update(pulseInfo)

    def idle( self, p ):
        pulseInfo = {
            "envelope": {
                "shape": 'const',
                "paras": p,
            },
            "phase": 0,
            }
        return self.pulseInfo.update(pulseInfo)
    def gaussPulse( self, p ):
        amplitude, sfactor = p
        pulseInfo = {
            "envelope": {
                "shape": 'gaussian',
                "paras": [amplitude, 1/sfactor],
            },
            "phase": 0,
            }
        return pulseInfo 
class OperationSequence():

    def __init__( self, sequenceTime, hardwareInfo=phyCh.HardwareInfo ):
        
        self.hardwareInfo = hardwareInfo
        dt = self.hardwareInfo.timeResolution
        self.operation = []
        self.sequenceTime = sequenceTime # ns

        self.sequencePts = int(sequenceTime//dt)
        self.xywaveform = {
            "t0": 0.,
            "dt": dt,
            "data": array([])
            }
        self.iqwaveform = {
            "t0": 0.,
            "dt": dt,
            "data": array([])
            }
    def set_operation( self, operation ):

        dt = self.hardwareInfo.timeResolution
        self.operation = operation
        endPt = int(0)
        for i, op in enumerate(self.operation) :
            operationPts = int(op.time//dt)

            op.operationPts = operationPts
            op.operationStartPt = endPt
            # Reset operation time
            op.time = operationPts*dt
            
            endPt += operationPts

        if endPt < self.sequencePts:
            op = Operation(((self.sequencePts-endPt)*dt),"idle")
            op.idle([0])
            self.operation.append(op)
            print("Operation sequence haven't full")
        elif endPt == self.sequencePts:
            print("Total operations match operation sequence")
        else:
            self.operation = []
            print("Too much operation")
            

    
    def cal_pulseSequence( self ):

        allXYPulse = array([])
        allIQPulse = array([])
        dt = self.hardwareInfo.timeResolution
        mPulse = IFPulse(hardwareInfo=self.hardwareInfo)
        t0 = self.operation[0].time
        for op in self.operation:
            
            mPulse.startTime = op.operationStartPt*dt-t0
            mPulse.operationTime = op.time

            mPulse.pulseInfo.update(op.pulseInfo)
            newPulse = mPulse.generate_envelope()["data"]
            allXYPulse = append(allXYPulse, newPulse)

            newPulse = mPulse.convert_XYtoIQ()["data"]
            allIQPulse = append(allIQPulse, newPulse)

            self.sequencePts += len(newPulse)
            print(len(newPulse))

        self.xywaveform.update({"data":allXYPulse})
        self.iqwaveform.update({"data":allIQPulse})

        return self.xywaveform

def get_timeAxis( waveform ):
    dataPts = len(waveform["data"])
    #print(waveform["t0"], waveform["dt"], dataPts)
    return linspace( waveform["t0"], waveform["t0"]+waveform["dt"]*dataPts, dataPts, endpoint=False)

class IFPulse():

    def __init__( self, startTime=None, operationTime=None, hardwareInfo=None, pulseInfo=None):

        # pt = point 
        self.startTime = startTime
        self.operationTime = operationTime
        self.timeResolution = hardwareInfo.timeResolution # ns/sample
        self.operationPts = 0
        self.hardwareInfo = hardwareInfo
        if pulseInfo == None :
            self.pulseInfo = {
                "envelope": {
                    "shape": 'gaussian',
                    "paras": [1,0.25],
                },
                "phase": 0,
            }
        self.waveform = {
            "t0": startTime,
            "dt": hardwareInfo.timeResolution,
            "data": array([])            
        }
        #self.pulseInfo.update(pulseInfo)

    def generate_envelope( self ):
        self.operationPts = int(self.operationTime//self.timeResolution)
        self.waveform["data"] = zeros( self.operationPts )
        self.waveform["t0"] = self.startTime 
        self.waveform["dt"] = self.timeResolution
        relativeTime = linspace(0,self.operationTime,self.operationPts,endpoint=False)

        operationTime = self.operationTime
        def get_gaussian():
            centerTime = operationTime /2
            amp = self.pulseInfo["envelope"]["paras"][0]/self.hardwareInfo.InputPort.couplingStrength
            sigma = operationTime *self.pulseInfo["envelope"]["paras"][1]
            p = [amp, sigma, centerTime]
            wfData = gaussianFunc( relativeTime, p )+ 0j
            return wfData

        def get_DRAG():
            centerTime = self.operationPts *self.timeResolution /2
            amp = self.pulseInfo["envelope"]["paras"][0] /self.hardwareInfo.InputPort.couplingStrength
            sigma = operationTime *self.pulseInfo["envelope"]["paras"][1]

            pGau = [ amp, sigma, centerTime ]

            ampDGau = amp 
            pDGau = [ ampDGau, sigma, centerTime ]
            wfData = gaussianFunc(relativeTime, pGau )+ -1j/(self.hardwareInfo.Qubit.anharmonicity/1e3) *derivativeGaussianFunc(relativeTime, pDGau)

            return wfData
        def get_const():
            amp = self.pulseInfo["envelope"]["paras"][0]/self.hardwareInfo.InputPort.couplingStrength
            p = [ amp ]

            wfData = constFunc( relativeTime, p )

            return wfData
        pulse = {
            'gaussian': get_gaussian,
            'DRAG': get_DRAG,
            'const': get_const,
        }
        self.waveform["data"]= pulse[self.pulseInfo["envelope"]["shape"]]() *exp(1j*self.pulseInfo["phase"])
        #print(self.waveform)
        return self.waveform
        
    def convert_XYtoIQ( self ):
        
        phaseBalance = self.hardwareInfo.IQMixerChannel.phaseBalance
        ampBalance  = self.hardwareInfo.IQMixerChannel.ampBalance
        (offsetI, offsetQ) = self.hardwareInfo.IQMixerChannel.offset
        XYcontrol = self.waveform["data"]
        absoluteTime = get_timeAxis(self.waveform)
        if_freq = self.hardwareInfo.IQMixerChannel.ifFreq/1e3 # to GHz
        print(if_freq)
        inverse = sign(sin(radians(phaseBalance)))
        #print(phaseBalance, ampBalance, (offsetI, offsetQ), inverse, cos(radians(abs(phaseBalance)-90)))
        A = abs( XYcontrol )
        phi = arctan2( XYcontrol.imag, XYcontrol.real )
        A1 = A / cos(radians(abs(phaseBalance)-90))
        A2 = A1 / ampBalance
        phiQ = -phi+inverse*pi/2.
        sigI = A1 *cos( 2. *pi *if_freq *absoluteTime +phiQ +radians(phaseBalance) +pi) -offsetI
        sigQ = A2 *cos( 2. *pi *if_freq *absoluteTime +phiQ) -offsetQ
        self.waveform["data"] = sigI+ 1j*sigQ
        return self.waveform



if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import scipy.fft as spfft
    print("register Qubit")
    q1 = phyCh.Qubit()
    print("register IQMixerChannel")
    m1 = phyCh.IQMixerChannel()    
    print("register InputPort")
    p1 = phyCh.InputPort()

    print("register HardwareInfo")
    pch1 = phyCh.HardwareInfo(q1,p1,m1) 

    print("init OS")
    OPS = OperationSequence(100,pch1)

    print("set new operation")
    op1 = Operation(20,'x')
    op2 = Operation(20,'y')
    op3 = Operation(20,'i')
    print("register operation to sequence")
    OPS.set_operation([op3, op1])

    print("calculate XY waveform of the sequence")
    xyWf = OPS.cal_pulseSequence()

    print("calculate IQ waveform of the sequence")
    iqWf = OPS.iqwaveform

    plot1 = plt.figure(1)
    timeAxis = get_timeAxis(xyWf)
    plt.plot(timeAxis, xyWf["data"].real)
    plt.plot(timeAxis, xyWf["data"].imag)
    plt.plot(timeAxis, iqWf["data"].real)
    plt.plot(timeAxis, iqWf["data"].imag)
    plot2 = plt.figure(2)
    plt.plot(xyWf["data"].real, xyWf["data"].imag)
    plt.plot(iqWf["data"].real, iqWf["data"].imag)
    plot3 = plt.figure(3)
    fq = q1.qubitFreq
    pmixer = m1.phaseBalance
    fIF = m1.ifFreq/1e3
    # plt.plot(timeAxis, cos(2*pi*fq*timeAxis) )

    # xymix = xyWf["data"].real*cos(2*pi*fq*timeAxis) +xyWf["data"].imag*cos(2*pi*fq*timeAxis +abs(radians(pmixer)) )
    # plt.plot(timeAxis, xymix)
    iqmix = iqWf["data"].real*cos(2*pi*(fq+fIF)*timeAxis) +iqWf["data"].imag*cos(2*pi*(fq+fIF)*timeAxis +radians(pmixer) )
    plt.plot(timeAxis, iqmix)

    data_points = len(timeAxis)
    f_points = data_points//2
    faxis = spfft.fftfreq(data_points,iqWf["dt"])[0:f_points]
    plot4 = plt.figure(4)
    # xyvector = spfft.fft(xymix)[0:f_points]/len(timeAxis)
    # plt.plot(faxis, abs(xyvector))
    iqvector = spfft.fft(iqmix)[0:f_points]/len(timeAxis)
    plt.plot(faxis, 10*log(abs(iqvector)))

    plt.show()



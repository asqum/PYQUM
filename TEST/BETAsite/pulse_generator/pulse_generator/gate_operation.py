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
    def __init__( self, time ):
        # self.functionName = functionName
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
        self.timeResolution = 1.
        self.waveform ={
            "t0": 0.,
            "dt": self.timeResolution,
            "data": array([])            
        }
    def arbXYGate( self, p, shape='DRAG' ):
        theta, phi = p
        pulseInfo = {
            "envelope": {
                "shape": shape,
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

    def purePulse( self, p, shape='gaussian' ):
        pulseInfo = {
            "envelope": {
                "shape": shape,
                "paras": p,
            },
            "phase": 0,
            }
        return self.pulseInfo.update(pulseInfo)

    def generate_envelope( self, dt, startTime, hardwareInfo ):
        self.timeResolution = dt
        self.operationPts = int(self.time//self.timeResolution)
        self.waveform["data"] = zeros( self.operationPts )
        self.waveform["t0"] = startTime
        self.waveform["dt"] = self.timeResolution
        relativeTime = linspace(0,self.time,self.operationPts,endpoint=False)
        
        amp = self.pulseInfo["envelope"]["paras"][0]/hardwareInfo.InputPort.couplingStrength

        def get_gaussian():
            centerTime = self.time /2
            sigma = self.time *self.pulseInfo["envelope"]["paras"][1]
            p = [amp, sigma, centerTime]
            wfData = gaussianFunc( relativeTime, p )+ 0j
            return wfData

        def get_halfGaussian():
            sigma = self.time *self.pulseInfo["envelope"]["paras"][1]
            centerTime = 0
            
            if sigma > 0:
                centerTime = self.time
            p = [amp, sigma, centerTime]
            wfData = gaussianFunc( relativeTime, p )+ 0j
            return wfData

        def get_degaussian():
            centerTime = self.time /2
            sigma = self.time *self.pulseInfo["envelope"]["paras"][1]
            p = [amp, sigma, centerTime]
            wfData = derivativeGaussianFunc( relativeTime, p )+ 0j
            return wfData

        def get_halfDeGaussian():
            sigma = self.time *self.pulseInfo["envelope"]["paras"][1]
            centerTime = 0
            
            if sigma > 0:
                centerTime = self.time
            p = [amp, sigma, centerTime]
            wfData = derivativeGaussianFunc( relativeTime, p )+ 0j
            return wfData

        def get_DRAG():
            centerTime = self.operationPts *self.timeResolution /2
            amp = self.pulseInfo["envelope"]["paras"][0] /hardwareInfo.InputPort.couplingStrength
            sigma = self.time *self.pulseInfo["envelope"]["paras"][1]

            pGau = [ amp, sigma, centerTime ]

            ampDGau = amp 
            pDGau = [ ampDGau, sigma, centerTime ]
            wfData = gaussianFunc(relativeTime, pGau )+ -1j/(hardwareInfo.Qubit.anharmonicity/1e3) *derivativeGaussianFunc(relativeTime, pDGau)

            return wfData
        def get_const():
            amp = self.pulseInfo["envelope"]["paras"][0]/hardwareInfo.InputPort.couplingStrength
            p = [ amp ]

            wfData = constFunc( relativeTime, p )

            return wfData
        pulse = {
            'gaussian': get_gaussian,
            'gaussian_half': get_halfGaussian,
            'degaussian': get_degaussian,
            'degaussian_half': get_halfDeGaussian,
            'gaussian_half': get_halfGaussian,
            'DRAG': get_DRAG,
            'const': get_const,
        }
        self.waveform["data"]= pulse[self.pulseInfo["envelope"]["shape"]]() *exp(1j*self.pulseInfo["phase"])
        #print(self.waveform)
        return self.waveform

    def convert_XYtoIQ( self, hardwareInfo ):
        
        phaseBalance = hardwareInfo.IQMixerChannel.phaseBalance
        ampBalance  = hardwareInfo.IQMixerChannel.ampBalance
        (offsetI, offsetQ) = hardwareInfo.IQMixerChannel.offset
        XYcontrol = self.waveform["data"]
        absoluteTime = get_timeAxis(self.waveform)
        if_freq = hardwareInfo.IQMixerChannel.ifFreq/1e3 # to GHz
        #print(if_freq)
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

class OperationSequence():

    def __init__( self, sequenceTime, hardwareInfo=phyCh.HardwareInfo ):
        
        self.hardwareInfo = hardwareInfo
        dt = self.hardwareInfo.timeResolution
        self.operation = []
        self.sequenceTime = sequenceTime # ns
        self.sequencePts = int(-(sequenceTime//-dt))
        print("sequenceTime",sequenceTime)
        print("sequencePts",self.sequencePts)

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
            operationPts = int(-(op.time//-dt))
            op.operationPts = operationPts
            op.operationStartPt = endPt
            # Reset operation time
            op.time = operationPts*dt

            print("start point",op.operationStartPt)
            print("op point",operationPts)

            endPt += operationPts

        if endPt < self.sequencePts:
            op = Operation(((self.sequencePts-endPt)*dt))
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
        t0 = self.operation[0].time
        for op in self.operation:
            newPulse = op.generate_envelope( dt, t0, self.hardwareInfo )["data"]
            allXYPulse = append(allXYPulse, newPulse)

            newPulse = op.convert_XYtoIQ( self.hardwareInfo )["data"]
            allIQPulse = append(allIQPulse, newPulse)

            self.sequencePts += len(newPulse)
            #print(len(newPulse))

        self.xywaveform.update({"data":allXYPulse})
        self.iqwaveform.update({"data":allIQPulse})

        return self.xywaveform

def get_timeAxis( waveform ):
    dataPts = len(waveform["data"])
    #print(waveform["t0"], waveform["dt"], dataPts)
    return linspace( waveform["t0"], waveform["t0"]+waveform["dt"]*dataPts, dataPts, endpoint=False)




        




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
    op1 = Operation(20)
    op1.arbXYGate([pi,0])
    op2 = Operation(20)
    op2.arbXYGate([pi,pi])
    op3 = Operation(20)
    op3.idle([0])

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



# Numpy Series
# Array
from inspect import Parameter
from xmlrpc.client import boolean
from numpy import array, zeros
# Type
from numpy import ndarray

from typing import List
import sys
sys.path.insert(0, '..')
from utility import math_func, waveform

class Pulse():
    """ Store the necessary information waveform """
    modeList = ["Direct,Mixer"]
    def __init__ ( self ):
        self._carrierFrequency = None
        self._evnelopeFunc = None
        self._duration = None
        self._dt = None
        self._parameters = None
        self._waveform = None

    @property
    def evnelope ( self )->function:
        """ The shape of the pulses"""
        return self._evnelope
    @evnelope.setter
    def evnelope ( self, value:function ):
        if value in self.envelopeList:
            self._evnelope = value
        else:
            raise ValueError(f"{value} not in avalible type {self.envelopeList}")

    @property
    def carrierFrequency ( self )->str:
        """ 
        The carrier frequency of the pulses, unit is as the same as dt. \n
        for DC mode, use 0
        """
        return self._carrierFrequency
    @carrierFrequency.setter
    def carrierFrequency ( self, value:str ):
        if value in self.envelopeList:
            self._carrierFrequency = value
        else:
            raise ValueError(f"{value} not in avalible type {self.envelopeList}")

    @property
    def duration ( self )->float:
        """ The duration of the pulse"""
        return self._duration
    @duration.setter
    def duration ( self, value:float ):
        if value > 0:
            self._duration = value
        else:
            raise ValueError(f"{value} can't be nagtive")

    def calculate_envelopeWaveform ( self, f, dt:float, points:int ):
        self._waveform = zeros( points )

        
        self.waveform["data"]= pulse[self.envelopeType]() *phaseShift
        return self._waveform 
        
    def get_gaussian( self, dt:float ):
        centerTime = self.time /2
        sigma = self.time *self._parameters[1]
        p = [amp, sigma, centerTime]
        wfData = gaussianFunc( relativeTime, p )
        phaseShift = exp(1j*self.pulseInfo["phase"])
        return wfData

    def get_halfGaussian():
        sigma = self.time *self.pulseInfo["envelope"]["paras"][1]
        centerTime = 0
        
        if sigma > 0:
            centerTime = self.time
        p = [amp, sigma, centerTime]
        wfData = gaussianFunc( relativeTime, p )
        return wfData

    def get_degaussian():
        centerTime = self.time /2
        sigma = self.time *self.pulseInfo["envelope"]["paras"][1]
        p = [amp, sigma, centerTime]
        wfData = derivativeGaussianFunc( relativeTime, p )
        return wfData

    def get_halfDeGaussian():
        sigma = self.time *self.pulseInfo["envelope"]["paras"][1]
        centerTime = 0
        
        if sigma > 0:
            centerTime = self.time
        p = [amp, sigma, centerTime]
        wfData = derivativeGaussianFunc( relativeTime, p )
        return wfData

    def get_DRAG():
        centerTime = self.time /2
        amp = self.pulseInfo["envelope"]["paras"][0]
        sigma = self.time *self.pulseInfo["envelope"]["paras"][1]

        pGau = [ amp, sigma, centerTime ]

        ampDGau = amp 
        pDGau = [ ampDGau, sigma, centerTime ]
        #wfData = gaussianFunc(relativeTime, pGau )+ -1j/(hardwareInfo.Qubit.anharmonicity/1e3) *derivativeGaussianFunc(relativeTime, pDGau)
        wfData = gaussianFunc(relativeTime, pGau )+ -1j *derivativeGaussianFunc(relativeTime, pDGau)

        return wfData

    def get_const():
        amp = self.pulseInfo["envelope"]["paras"][0]
        p = [ amp ]

        wfData = constFunc( relativeTime, p )

        return wfData
    def get_linear():
        slope = self.pulseInfo["envelope"]["paras"][0]
        intercept = self.pulseInfo["envelope"]["paras"][1]
        p = [ slope, intercept ]

        wfData = linearFunc( relativeTime, p )

        return wfData
    def get_ringUp():
        flatHieght = self.pulseInfo["envelope"]["paras"][0]
        sigmaRatio = self.pulseInfo["envelope"]["paras"][1]
        edgeLength = self.pulseInfo["envelope"]["paras"][2]

        peakLength = edgeLength*2
        flatLength = self.time -peakLength
        peakMultiplier = self.pulseInfo["envelope"]["paras"][3]
        peakSigma = peakLength *sigmaRatio

        startPos = edgeLength

        ringPeak = flatHieght *(peakMultiplier)
        endPos = startPos +flatLength

        ringGauss = [ ringPeak, peakSigma, startPos ]

        highPowerGauss = gaussianFunc(relativeTime, ringGauss)
        startEdge = [ flatHieght, peakSigma, startPos ]
        gaussUp = where( relativeTime<startPos, gaussianFunc(relativeTime, startEdge),0. )
        endEdge = [ flatHieght, peakSigma, endPos ]
        gaussDn = where( relativeTime>endPos, gaussianFunc(relativeTime, endEdge),0. )
        step = where( (relativeTime>=startPos) & (relativeTime<=endPos), constFunc(relativeTime, [flatHieght]),0. )
        wfData = highPowerGauss +gaussUp +step +gaussDn

        return wfData

class Operation():
    """
    Store the name of the operation and pulses to form it. 
    """

    def __init__ ( self ):
        self._name = None
        self._pulse = []
        self._dt = []
        self._waveform = []

    @property
    def name ( self )->str:
        """ The name of the operation"""
        return self._name
    @name.setter
    def name ( self, value:str ):
        self._name = value

    # @property
    # def pulse ( self )->List[Pulse]:
    #     """ The pulses of the operation"""
    #     return self._pulse
    # @pulse.setter
    # def pulse ( self, value:List[Pulse] ):
    #     self._pulse = value

class OperationLib ():

    def __init__ ( self ):

        self.physicalChannels = [] # All Used channel
        self._operationList = []
        

    def get_OperationsName ( self )->List[str]:    
        nameList = []
        for op in self.operationList:
            nameList.append(op.name)
        return nameList

    def isExist_Operaion ( self, name:str )->bool:
        return name in self.get_OperationsName()
        
    def add_operation ( self, operation:Operation ):
        nameList = self.get_OperationsName()
        if operation.name not in nameList:
            self._operationList.append( operation )

    def create_operation ( self, name:str, physicalCh:list, pulse:List[Pulse] ):
        if len(physicalCh) == len(pulse):
            newOp = Operation()
            newOp.name = name
            newOp.physicalChannels = physicalCh
            newOp.pulse = pulse
        return newOp

    def get_operation ( self, name:str )->Operation:
        """ Get operation by name"""
        nameList = self.get_OperationsName()
        operation_idx = nameList.index(name)
        return self._operationList[operation_idx]



    #def calculate_envelopeWaveform ( self )->ndarray:
## TODO 
# class PurePulse ():
#     def __init__():
#         self._carrier = None
#         self._envelope

# class PulseFuncInfo():


           
def create_Pulse_Gaussian ( carrierFrequency:float, parameters:tuple )->Pulse:
    """ 
    If the carrier frequency of the pulse is 0 
    p0: Pulse length 
    p1: Amplitude 
    p2: s factor ( length = sigma * s factor)
    p3: phase ( optional )
    """
    newPulse = TheoreticPulse()
    newPulse.carrierFrequency = carrierFrequency
    newPulse.shape = "Gau"
    newPulse.parameters = parameters
    return newPulse

def create_Pulse_DerivativeGaussian ( parameters:tuple ):
    """ 
    p0: Pulse length 
    p1: Amplitude 
    p2: s factor ( length = sigma * s factor)
    p3: phase
    """
    newPulse = TheoreticPulse()
    newPulse._envelopeType = "DGau"
    newPulse._parameters = parameters
    return newPulse




    # def set_Parameters ( self, envelopeType:str, parameters:tuple ):
    #     """
    #     Gau, Gau_half, DGau, DGau_half:\n
    #     p0: s factor ( length = sigma * s factor)\n 
    #     const: \n
    #     p0: canstant value \n
    #     linear: \n
    #     p0: slope. p1: intersection.\n
    #     ringup: \n
    #     p0: s factor. p1: Edge width.\n
    #     """
    #     if self._parasNumber[envelopeType] == len(parameters):
    #         self._envelopeType = envelopeType
    #         self._parameters = parameters
    


def create_operation ( name:str, physicalCh:list, pulse:List[Pulse] )->Operation:
    if len(physicalCh) == len(pulse):
        newOp = Operation()
        newOp.name = name
        newOp.physicalChannels = physicalCh
        newOp.pulse = pulse
    return newOp

class OperationSequence():

    def __init__( self, sequencePts, dt ):
        self.dt = dt
        self.operation = []
        self.sequenceTime = sequencePts*dt # ns
        self.sequencePts = sequencePts
        # print("sequenceTime",sequenceTime)
        # print("sequencePts",self.sequencePts)

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
    def set_operation( self, operation:List[Operation]  ):

        self.operation = operation
        endPt = int(0)
        for i, op in enumerate(self.operation) :
            operationPts = op.operationPts
            op.waveform["t0"] = endPt*self.dt
            #print("start point",endPt)
            #print("op point",operationPts)
            endPt += operationPts

        if endPt < self.sequencePts:
            op = PulseBuilder(self.sequencePts-endPt,self.dt)
            op.idle([0])
            self.operation.append(op)
            print("Operation sequence haven't full")
        elif endPt == self.sequencePts:
            print("Total operations match operation sequence")
        else:
            op = PulseBuilder(self.sequencePts,self.dt)
            op.idle([0])
            self.operation = [op]
            print("Too much operation, clean all sequense")
            

    
    def generate_sequenceWaveform( self, mixerInfo=None, firstOperationIdx=None ):

        allXYPulse = array([])
        allIQPulse = array([])
        t0 = 0
        if len(self.operation) == 0 : # For the case with only one operation
            firstOperationIdx = 0
        # Convert XY to IQ language
        for op in self.operation:
            newPulse = op.generate_envelope()["data"]
            allXYPulse = append(allXYPulse, newPulse)

        if firstOperationIdx != None :
            t0 = self.operation[firstOperationIdx].waveform["t0"]
        elif len(self.operation) == 0 :
            t0 = 0
        else:
            try: # Old method to get t0
                t0 = self.dt * where(ceil(abs(allXYPulse))==1)[0][0]
                # print(Back.WHITE + Fore.BLUE + "Pulse starting from %s ns" %pulse_starting_time)
            except(IndexError): 
                t0 = 0

        # Convert XY to IQ language        
        for op in self.operation:
            op.waveform["t0"]-=t0
            newPulse = op.convert_XYtoIQ( mixerInfo )["data"]
            allIQPulse = append(allIQPulse, newPulse)

            #print(len(newPulse))

        self.xywaveform.update({"data":allXYPulse})
        self.iqwaveform.update({"data":allIQPulse})

        return self.iqwaveform



if __name__ == '__main__':
    a = Operation()
    a.name = "x"
    print(type(create_Pulse_Gaussian))
    #print(a.g_qc)
    #print(a.qubit.anharmonicity)
    #print(a.qubit.Ec)

        # pulse = {
        #     'Gau': self.get_gaussian,
        #     'Gau_h': self.get_halfGaussian,
        #     'DGau': self.get_degaussian,
        #     'DGau_h': self.get_halfDeGaussian,
        #     'DRAG': self.get_DRAG,
        #     'const': self.get_const,
        #     'linear': self.get_linear,
        #     'ringup': self.get_ringUp,
        # }
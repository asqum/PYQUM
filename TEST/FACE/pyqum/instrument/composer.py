# Aim to compose a lyric for Qubit

from cProfile import label
from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from copy import copy
from math import trunc, ceil
from numpy import linspace, power, exp, array, zeros, sin, cos, pi, where, ceil, clip, empty, radians, nan, isnan, append, complex128
from pulse_signal.pulse import QAM 
import pulse_signal.common_Mathfunc as cpf

from pulse_signal.pulseScript import give_waveformInfo


# 0106 add 
# give the total time,points consider in AWG limitations
def give_timeInfo(score,dt,clock_multiples):
    order = score.replace(" ","").replace("\n","").lower()
    info = order.split(";")[0].split(",")[0].split('ns=')[1]
    
    totalpoints = int(clock_multiples) *int( -(int( -(float(info.split('/')[0]) //-dt))//-clock_multiples))
    totaltime = totalpoints* dt

    firstOperationIdx = None
    if len(info.split('/'))==2:     # if sequenceSetting is not the form "500/1" ,ex: "500" only
        firstOperationIdx = int(info.split('/')[1])

    return {"OperateFirst":firstOperationIdx,"AWG_times":totaltime,"AWG_points":totalpoints}
    
# give the mixer informations 
def give_mixerInfo(score):
    order = score.replace(" ","").replace("\n","").lower()
    info = order.split(";")[0].split(",")
    try: mixerParams = info[1].split('mhz=')[1] # self.mix_params -> "i/-91/"
    except(IndexError): mixerParams = "z/0/" # No Mixer setting
    # IF Frequency
    ifFreq = float(mixerParams.split("/")[1])
    # mixer modulation
    try: 
        mixerModule = mixerParams.split("/")[2]  # self.mixer_module -> ""
        if mixerModule=='' : mixerModule = "pure" # for the case where mhz=i/37/<empty>
    except(IndexError): 
        mixerModule = "pure" # "pure": "1/0/0" in json-configuration for MIXER
    # If channel
    ifChannel = mixerParams.split("/")[0]
    # modify coef.
    mixerInfo = None
    match ifChannel:
        case "i"|"q":
            try:
                mixerName = mixerModule.split(ifChannel.lower())[0]
                lable_IF = mixerModule.split(ifChannel.lower())[1]
                channel_I = mixerName+'i'+lable_IF
                channel_Q = mixerName+'q'+lable_IF
                from pyqum.instrument.logger import get_status
                amp_I, phase_I, offset_I = [float(x) for x in get_status("MIXER")[channel_I].split("/")]
                amp_Q, phase_Q, offset_Q = [float(x) for x in get_status("MIXER")[channel_Q].split("/")]
                mixerInfo = (amp_I/amp_Q, phase_I-phase_Q, offset_I, offset_Q)
            except:
                mixerInfo = ( 1, 90, 0, 0 )
        case "z":
                mixerInfo = None
        case _:
                mixerInfo = None

    return {"IfFreq":ifFreq,"Module":mixerModule,"IfChannel":ifChannel,"Modifies":mixerInfo}

# give pulse information, width, amplitude, start time and adjFrequency included
def give_pulseInfo(pulseDescribe,dt):
    basicParas={"width":nan,"height":nan,"startTime":nan,"adjFrequency":nan}
    idx = 0   # help to count 
    for p in pulseDescribe.split(',')[1:]:
        if p != '' :
            match idx:
                case 0:
                    basicParas["startTime"] = float(p[1:])
                case 1:
                    basicParas["width"] = float(p[:-1])
                case 2: 
                    basicParas["height"] = float(p) 
                case 3:
                    basicParas["adjFrequency"] = float(p)
        idx += 1

    if isnan(basicParas["adjFrequency"]):
        basicParas["adjFrequency"] = 0
    
    pulsePts = int(-(basicParas["width"]//-dt)) # -(100.0//-0.8) -int-> 125
    basicParas["width"] = pulsePts*dt  # make the pulse width is complete waveform after AWG output
    return basicParas


# specify where the pulse component starts at , return the point
def give_startPoint(starttime,clock_multiples,dt)->str:
    if isnan(starttime):
        StartPoint = ""
    else:
        originStartPoint = -int(starttime // -dt)
        StartPoint = str(int(clock_multiples) *int( -(originStartPoint //-clock_multiples) ))
    return StartPoint



class pulser:
    '''
    Next generation of Pulse Assembly:\n
    All time-units in ns\n
    dt: time-resolution of AWG in ns\n
    clock_multiples: depends on AWG model, waveform must consist of certain multiple of points\n
    score:  SCORES (SCripted ORchestration of Entanglement & Superposition) is a scripted pulse instruction language for running Quantum Algorithm at pulse-level.\n
            analogous to music score, basically a set of syntatical instructions to build the "music": \n
            "ns=<totaltime: pulse-period> , [mhz=<i/q>/<IF>[/<mixer-module>]] (-> mix_params); 
            <shape>/[<param#1>/.../<param#n>], <pulse-width>, <pulse-height>; 
            ... ... "
    music: pulse-sequence output (numpy array)
    NOTE: implement delay as one of the beats for the sake of simplicity, instead of seperated parameter. (Ex: to delay 100ns, write: "flat,100,0")
    '''
    def __init__(self, dt=0.8, clock_multiples=8, 
                score='Gaussup/6,100,1; Flat,100,1; Gaussdn/6,100,1; Pause,300,1; Gaussup/6,100,1; Flat,100,1; Gaussdn/6,100,1;'):
        self.score = score
        self.dt = dt
        self.clock_multiples = clock_multiples

        # save time information into self
        timeInfo = give_timeInfo(self.score,self.dt,self.clock_multiples)  # return dictionary
        self.firstOperationIdx = timeInfo["OperateFirst"]
        self.totalpoints = timeInfo["AWG_points"]
        self.totaltime = timeInfo["AWG_times"]
        self.beatime, self.music, self.timeline = 0, zeros([self.totalpoints]), linspace( 0, self.totaltime, self.totalpoints, endpoint=False)

        # save mixer information into self
        mixerInfo = give_mixerInfo(self.score)  # return dictionary
        self.iffreq = mixerInfo["IfFreq"]

        self.IF_MHz_rotation = self.iffreq

        self.mixer_module = mixerInfo["Module"]
        self.ifChannel = mixerInfo["IfChannel"]
        self.mixerInfo = mixerInfo["Modifies"]

    def relativeIF_compose(self, pulses, modulator):
        '''
        This function is the core of song(). Due to the different relative IF frequency,\n
        there is a different way to compose SSB (Single Sideband).\n
        This function is exactly the determiner.
        '''

        wholeConnectSequence = zeros(self.totalpoints, dtype=complex128)
        Ichannel, Qchannel = [], []
        if len(pulses.keys()) == 1 :   # All the same adjust IF frequency, directly sum all the if frequency
            pulse_components = pulses[list(pulses.keys())[0]]
            _, pulse_signal=modulator.give_RFenvelope_IFfrequency(pulse_components)   # 0107 added: Do first on the pulses with specified start time
            IFfreq = (self.iffreq + float(list(pulses.keys())[0]))/1e3
            wholeConnectSequence += pulse_signal
            # 2. Envelope before IF-Mixing:
            if self.mixerInfo != None:
                signal_i, signal_q, LO_freq = modulator.SSB( IFfreq,leakage_sup=True, envelope_RF=pulse_signal,IQMixer=self.mixerInfo )
                Ichannel.append(signal_i)
                Qchannel.append(signal_q)
        else:        # with adjust IF frequency , all SSB() -> sum -> leakage suppress
            envelopes, connected = {}, {}
            
            if self.mixerInfo != None:
                from pulse_signal.digital_mixer import leakage_suppress
                for IFadj in list(pulses.keys()):   # a relative frequency may contain many pulses
                    if IFadj not in envelopes.keys():
                        envelopes[IFadj] = []  # groups in relative freq  
                    components, pulse_signal = modulator.give_RFIFDict(pulses[IFadj])   # 0107 added: Do first on the pulses with specified start time
                    envelopes[IFadj].append(components)   # pulses envelopes group in relative freq
                    connected[IFadj] = pulse_signal        # whole connected envelope groups in relative freq

                for IFadj in list(connected.keys()):
                    IFfreq = (self.iffreq + float(IFadj))/1e3
                    wholeConnectSequence += connected[IFadj]
                    i, q, LO_freq = modulator.SSB( IFfreq,leakage_sup=False,envelope_RF=connected[IFadj] ,IQMixer=self.mixerInfo )
                    signal_i, signal_q = leakage_suppress( i, q, IQMixer=self.mixerInfo )
                    Ichannel.append(signal_i)
                    Qchannel.append(signal_q)

        return wholeConnectSequence, sum(Ichannel), sum(Qchannel)

    def song(self):
        '''
        compose the song based on the score given:
            ns=<period/length of the song>;
            <pulse-shape>/[<unique factor(s): default (to pulse-library) database) if blank], <pulse-period>, <pulse-height: between -1 & +1>;
            stack a variety of pulse-instruction(s) according to the format illustrated above.
        '''


        pulses = {}
        # 1. Baseband Shaping:
        for beat in self.score.replace(" ","").replace("\n","").lower().split(";")[1:]:
            if beat == '': break # for the last semicolon
            
            # basic para include pulse width and hight
            pulseInfo = give_pulseInfo(beat,self.dt)
            pulsewidth = pulseInfo["width"] # width and height must have value. If not, it will be nan.
            pulseheight = pulseInfo["height"]
            pulseStartPoint = give_startPoint(pulseInfo["startTime"],self.clock_multiples,self.dt) # return string
            pulseAdjFrequency = pulseInfo["adjFrequency"]
            # groups in relative IF frequency
            if str(pulseAdjFrequency) not in pulses.keys():
                pulses[str(pulseAdjFrequency)] = []

            self.beatime += pulsewidth

            # 0105 add. Generate paras a pulse need like width, amplitude, function, phase,...  
            new_pulse = give_waveformInfo(beat,pulsewidth,pulseheight)
            new_pulse.startPoint = pulseStartPoint
            new_pulse.adjFrequency = pulseAdjFrequency
                    
            pulses[str(pulseAdjFrequency)].append(new_pulse)   # group in dict by the relative frequency

        modulator = QAM( self.dt, self.totalpoints ) # 0106 added totalpoints
        wholeConnectEnvelope, Ichannel, Qchannel = self.relativeIF_compose(pulses,modulator)
        
        match self.ifChannel:
            case "i":
                self.envelope = wholeConnectEnvelope.real
                self.music = array(Ichannel)

            case "q":
                self.envelope = wholeConnectEnvelope.imag
                self.music = array(Qchannel)

            case "z": # for z-gate
                self.envelope = abs(wholeConnectEnvelope)
                self.music = abs(wholeConnectEnvelope)
            case _:
                print("Unkown IF channel type.")
                self.envelope = array([])
                self.music = array([])               
        #print("operation number",len(self.operationList))

        # Confine music between -1 and 1:
        self.music = clip(self.music, -1.0, 1.0, out=self.music)

        return self.music


# test
# abc = pulser(dt=0.4, clock_multiples=1, score='NS=10; Flat/,2,0;Gaussup/,4,0.5;gA uss dn/,4,0.5;')
# abc.song()
# print("%sns music:\n%s" %(abc.totaltime, abc.music))
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    xyi = pulser(dt=.5,score='ns=600/1,mhz=I/-80/; GERP/,(100,100),1,0; ',clock_multiples=1)
    xyi.song()
    xyq = pulser(dt=.5,score='ns=600/1,mhz=Q/-80/; GERP/,(100,100),1,0;',clock_multiples=1)
    xyq.song()

    cz = pulser(dt=.5,score='ns=600;Flat/,100,0.5;',clock_multiples=1)
    cz.song()

    roi = pulser(dt=.5,score='ns=600/1,mhz=I/-40/; GAUSSUP/,(370,30),1,0; FLAT/,(400,100),1,0; GAUSSDN/,(500,30),1,0;  ',clock_multiples=1)
    roi.song()
    roq = pulser(dt=.5,score='ns=600/1,mhz=Q/-40/; GAUSSUP/,(370,30),1,0; FLAT/,(400,100),1,0; GAUSSDN/,(500,30),1,0; ',clock_multiples=1)
    roq.song()

    pulsedata = roi.music
    shrinkage = 3
    first_rising_edge, last_falling_edge = where(ceil(abs(pulsedata-pulsedata[-1]))==1)[0][0], where(ceil(abs(pulsedata-pulsedata[-1]))==1)[0][-1]
    print(first_rising_edge, last_falling_edge)
    last_falling_edge = first_rising_edge + int(ceil((last_falling_edge - first_rising_edge)/shrinkage))
    print(first_rising_edge, last_falling_edge)
    
    plot1 = plt.figure(1)
    plt.plot(xyi.timeline, xyi.envelope, label="xyx")
    plt.plot(xyq.timeline, xyq.envelope, label="xyy")
    plt.plot(roi.timeline, roi.envelope, label="rox")
    plt.plot(roq.timeline, roq.envelope, label="roy")

    plt.title("XY envelope")
    plt.legend()
    plot2 = plt.figure(2)
    plt.plot(xyi.timeline, xyi.music, label="xyi")
    plt.plot(xyq.timeline, xyq.music, label="xyq")
    plt.plot(cz.timeline, cz.music, label="z")
    plt.plot(roi.timeline, roi.music, label="roi")
    plt.plot(roq.timeline, roq.music, label="roq")
    plt.title("AWG real output")
    plt.legend()
    plt.show()


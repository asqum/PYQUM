# Aim to compose a lyric for Qubit

from cProfile import label
from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from copy import copy
from math import trunc, ceil
from numpy import linspace, power, exp, array, zeros, sin, cos, pi, where, ceil, clip, empty, radians, nan, isnan, append
from pyqum.instrument.logger import get_status
from pulse_signal.pulse import Pulse
from pulse_signal.pulse import QAM
import pulse_signal.common_Mathfunc as cpf
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
        # Initialize score string type
        self.score = score.replace(" ","").replace("\n","").lower() # get rid of multiple spacings & new-lines and also lower the cases
        
        self.dt = dt
        themeSetting = self.score.split(";")[0].split(",")
        sequenceSetting = themeSetting[0].split('ns=')[1]
        
        # modify user input time
        originTotaltime = float(sequenceSetting.split('/')[0])
        originTotalPoint = int( -(originTotaltime //-dt) )
        # Get first operation
        self.firstOperationIdx = None
        if len(sequenceSetting.split('/'))==2:
            self.firstOperationIdx = int(sequenceSetting.split('/')[1])

        self.totalpoints = int(clock_multiples) *int( -(originTotalPoint //-clock_multiples) )
        self.totaltime = self.totalpoints* dt
        self.beatime, self.music = 0, zeros([self.totalpoints])


        self.timeline = linspace( 0, self.totaltime, self.totalpoints, endpoint=False)
        # mixing module:
        try: self.mix_params = themeSetting[1].split('mhz=')[1]
        except(IndexError): self.mix_params = "z/0/" # No Mixer setting
        
        self.iffreq = float(self.mix_params.split("/")[1]) # pre-loading IF-frequency in MHz
        try: 
            self.mixer_module = self.mix_params.split("/")[2]
            if self.mixer_module=='' : self.mixer_module = "pure" # for the case where mhz=i/37/<empty>
        except(IndexError): 
            self.mixer_module = "pure" # "pure": "1/0/0" in json-configuration for MIXER

        self.IF_MHz_rotation = self.iffreq # uncalibrated pure case, generalised to support baseband case where IF=0
        
        self.ifChannel = self.mix_params.split("/")[0] # Get current IF Channel

        self.mixerInfo = None
        match self.ifChannel:
            case "i"|"q":
                try:
                    mixerName = self.mixer_module.split(self.ifChannel.lower())[0]
                    lable_IF = self.mixer_module.split(self.ifChannel.lower())[1]
                    channel_I = mixerName+'i'+lable_IF
                    channel_Q = mixerName+'q'+lable_IF
                    amp_I, phase_I, offset_I = [float(x) for x in get_status("MIXER")[channel_I].split("/")]
                    amp_Q, phase_Q, offset_Q = [float(x) for x in get_status("MIXER")[channel_Q].split("/")]
                    self.mixerInfo = (amp_I/amp_Q, phase_I-phase_Q, offset_I, offset_Q)
                except:
                    self.mixerInfo = ( 1, 90, 0, 0 )
            case "z":
                    self.mixerInfo = None
            case _:
                    self.mixerInfo = None

    def song(self):
        '''
        compose the song based on the score given:
            ns=<period/length of the song>;
            <pulse-shape>/[<unique factor(s): default (to pulse-library) database) if blank], <pulse-period>, <pulse-height: between -1 & +1>;
            stack a variety of pulse-instruction(s) according to the format illustrated above.
        '''


        pulses = []
        # 1. Baseband Shaping:
        for beat in self.score.split(";")[1:]:
            if beat == '': break # for the last semicolon
            
            # basic para include pulse width and hight
            basicParas=[]
            for p in beat.split(',')[1:]:
                if p == '' :
                    basicParas.append( nan )
                else:
                    basicParas.append( float(p) )            

            pulsewidth = float(basicParas[0])
            pulseheight = float(basicParas[1])


            waveformParas = []
            for p in beat.split(',')[0].split('/')[1:]:
                if p == '':
                    waveformParas.append( nan )
                else:
                    waveformParas.append( float(p) )

            pulsePts = int(-(pulsewidth//-self.dt))
            pulsewidth = pulsePts*self.dt
            self.beatime += pulsewidth
            
            pulseType = beat.split('/')[0]
            match pulseType:
                case "flat":
                    pulse_func = cpf.constFunc
                    func_paras = [pulseheight]
                    carrierPhase = 0
                case "gauss":
                    pulse_func = cpf.gaussianFunc
                    if isnan(waveformParas[0]): sfactor = 4
                    else: sfactor = waveformParas[0]
                    carrierPhase = 0
                    func_paras = [pulseheight, pulsewidth/sfactor, pulsewidth/2]

                case "gaussup":
                    pulse_func = cpf.gaussianFunc
                    if isnan(waveformParas[0]): sfactor = 4
                    else: sfactor = waveformParas[0]
                    carrierPhase = 0
                    func_paras = [pulseheight, pulsewidth*2/sfactor, 0]

                case "gaussdn":
                    pulse_func = cpf.gaussianFunc
                    if isnan(waveformParas[0]): sfactor = 4
                    else: sfactor = waveformParas[0]
                    carrierPhase = 0
                    func_paras = [pulseheight, pulsewidth*2/sfactor, pulsewidth]


                case "drag":
                    pulse_func = cpf.DRAGFunc
                    if len(waveformParas)==1:
                        sfactor = 4
                        dRatio = 0
                        rotAxis = 0
                    else:
                        if isnan(waveformParas[0]): sfactor = 4
                        else: sfactor = waveformParas[0]
                        if isnan(waveformParas[1]): dRatio = 0
                        else: dRatio = waveformParas[1]
                        if isnan(waveformParas[2]): rotAxis = 0
                        else: rotAxis = radians(waveformParas[2])
                    carrierPhase = rotAxis
                    func_paras = [pulseheight, pulsewidth/sfactor, pulsewidth/2, dRatio ]

                case "lin":
                    pulse_func = cpf.linearFunc
                    if isnan(waveformParas[0]): start = 0
                    else: start = waveformParas[0]
                    if isnan(waveformParas[1]): end = 0
                    else: end = waveformParas[1]
                    carrierPhase = 0
                    slope = (start-end)/pulsewidth
                    func_paras = [slope, start]

                case "gerp":
                    pulse_func = cpf.GERPFunc
                    if len(waveformParas)==1:
                        sfactor = 4
                        edgeWidth = 30
                        peakMultiplier = 0
                    else:
                        if isnan(waveformParas[0]): sfactor = 4
                        else: sfactor = waveformParas[0]
                        if isnan(waveformParas[1]): edgeWidth = 30
                        else: edgeWidth = waveformParas[1]
                        if isnan(waveformParas[2]): peakMultiplier = 0
                        else: peakMultiplier = waveformParas[2]

                    func_paras = [pulseheight, pulsewidth, 0, edgeWidth, edgeWidth*2/sfactor]
                case _:
                    pulse_func = cpf.constFunc

            new_pulse = Pulse()
            new_pulse.duration = pulsewidth
            new_pulse.envelopeFunc = pulse_func
            new_pulse.carrierPhase = carrierPhase
            new_pulse.parameters = func_paras
            pulses.append(new_pulse)


        modulator = QAM( self.dt )
        modulator.import_pulseSequence(pulses)

        # Fill remain pts with idle gate
        #remainPts = int( -(self.beatime-self.totaltime) // self.dt)

        remainPts = self.totalpoints -modulator.envelope.shape[-1]

        if remainPts >= 0:
            modulator.envelope = append( modulator.envelope, zeros(remainPts) )
        else:
            print( "Too many pulse.")
            modulator.envelope = zeros(self.totalpoints)
        pulse_signal = modulator.envelope
        # 2. Envelope before IF-Mixing:
        if self.mixerInfo != None:
            signal_i, signal_q = modulator.SSB( self.iffreq/1e3, IQMixer=self.mixerInfo )
        match self.ifChannel:
            case "i":
                self.envelope = pulse_signal.real
                self.music = signal_i

            case "q":
                self.envelope = pulse_signal.imag
                self.music = signal_q

            case "z": # for z-gate
                self.envelope = abs(pulse_signal)
                self.music = abs(pulse_signal)
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
    xyi = pulser(dt=.5,score='ns=500/1,mhz=I/-91/; Flat/,100,0; drag/4/-0.8/0,100,0.5;',clock_multiples=1)
    xyi.song()
    xyq = pulser(dt=.5,score='ns=500/1,mhz=Q/-91/; Flat/,100,0; drag/4/-0.8/0,100,0.5;',clock_multiples=1)
    xyq.song()

    cz = pulser(dt=.5,score='ns=500;Flat/,100,0.5;',clock_multiples=1)
    cz.song()

    roi = pulser(dt=.5,score='ns=500/1,mhz=I/-29/; Flat/,40,0; gerp/,400,0.2;',clock_multiples=1)
    roi.song()
    roq = pulser(dt=.5,score='ns=500/1,mhz=Q/-29/; Flat/,40,0; gerp/,400,0.2;',clock_multiples=1)
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


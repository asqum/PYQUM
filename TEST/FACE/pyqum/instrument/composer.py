# Aim to compose a lyric for Qubit

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from copy import copy
from math import trunc, ceil
from numpy import linspace, power, exp, array, zeros, sin, cos, pi, where, ceil, clip, empty, radians, nan, isnan
from pyqum.instrument.logger import get_status
import pulse_generator.gate_operation as qos
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
        if self.ifChannel == "i" or self.ifChannel == "q":
            self.mixerInfo = qos.IQMixerChannel() 
        # set IQ Mixer calibration parameters into IQMixerChannel object
            try:
                mixerName = self.mixer_module.split(self.ifChannel.lower())[0]
                lable_IF = self.mixer_module.split(self.ifChannel.lower())[1]
                channel_I = mixerName+'i'+lable_IF
                channel_Q = mixerName+'q'+lable_IF
                amp_I, phase_I, offset_I = [float(x) for x in get_status("MIXER")[channel_I].split("/")]
                amp_Q, phase_Q, offset_Q = [float(x) for x in get_status("MIXER")[channel_Q].split("/")]
                self.mixerInfo.ampBalance = amp_I/amp_Q
                self.mixerInfo.phaseBalance = phase_I-phase_Q
                self.mixerInfo.offset = ( offset_I, offset_Q )
            except:
                self.mixerInfo.ampBalance = 1
                self.mixerInfo.phaseBalance = -90
                self.mixerInfo.offset = ( 0, 0 )
            self.mixerInfo.ifFreq = self.iffreq
        elif self.ifChannel == "z":
            self.mixerInfo = None
        #print("register one channel for a Qubit")
 
        self.operationSeq = qos.QubitOperationSequence( originTotalPoint, dt )
        self.operationList = []
    def song(self):
        '''
        compose the song based on the score given:
            ns=<period/length of the song>;
            <pulse-shape>/[<unique factor(s): default (to pulse-library) database) if blank], <pulse-period>, <pulse-height: between -1 & +1>;
            stack a variety of pulse-instruction(s) according to the format illustrated above.
        '''

        # 1. BB Shaping:
        for beat in self.score.split(";")[1:]:
            if beat == '': break # for the last semicolon

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
            op = qos.PulseBuilder(pulsePts,self.dt)
            # Shapes of Tones:
            # 1. Constant Flat Line:
            def get_flat(): 
                op.idle([pulseheight], channel=self.ifChannel)

            # Gaussian
            # 2.0 complete:
            def get_gauss():
                if isnan(waveformParas[0]): sfactor = 4
                else: sfactor = waveformParas[0]
                qosp = [pulseheight, 1/(sfactor)]
                op.purePulse(qosp, channel=self.ifChannel, shape='gaussian')

            # 2.1 raising from zero:
            def get_gaussup():
                if isnan(waveformParas[0]): sfactor = 4
                else: sfactor = waveformParas[0]
                qosp = [pulseheight, 1/(sfactor/2)]
                op.purePulse(qosp, channel=self.ifChannel, shape='gaussian_half')

            # 2.2 falling to zero:
            def get_gaussdn():
                if isnan(waveformParas[0]): sfactor = 4
                else: sfactor = waveformParas[0]
                qosp = [pulseheight, -1/(sfactor/2)]
                op.purePulse(qosp, channel=self.ifChannel, shape='gaussian_half')
            # 3 Derivative Gaussian
            # 3.0
            def get_dgauss():
                if isnan(waveformParas[0]): sfactor = 4
                else: sfactor = waveformParas[0]
                qosp = [pulseheight, -1/(sfactor)]
                op.purePulse(qosp, channel=self.ifChannel, shape='degaussian')
            
            # 3.1 dgauss up
            def get_dgaussup():
                if isnan(waveformParas[0]): sfactor = 4
                else: sfactor = waveformParas[0]
                qosp = [pulseheight, 1/(sfactor/2)]
                op.purePulse(qosp, channel=self.ifChannel, shape='degaussian_half')
            # 3.2 dgauss dn
            def get_dgaussdn():
                if isnan(waveformParas[0]): sfactor = 4
                else: sfactor = waveformParas[0]
                qosp = [pulseheight, -1/(sfactor/2)]
                op.purePulse(qosp, channel=self.ifChannel, shape='degaussian_half')

            # PENDING: BUILD CONNECTORS: require the knowledge of the last height
            def get_drag():
                if len(waveformParas)==1:
                    sfactor = 4
                    dRatio = 1
                    rotAxis = 0
                else:
                    if isnan(waveformParas[0]): sfactor = 4
                    else: sfactor = waveformParas[0]
                    if isnan(waveformParas[1]): dRatio = 1
                    else: dRatio = waveformParas[1]
                    if isnan(waveformParas[2]): rotAxis = 0
                    else: rotAxis = radians(waveformParas[2])
                qosp = [pulseheight, 1/(sfactor), dRatio, rotAxis]
                op.rotXY(qosp, shape='fDRAG')

            # 4. Linear connector: 
            def get_linear():
                if isnan(waveformParas[0]): start = 0
                else: start = waveformParas[0]
                if isnan(waveformParas[1]): end = 0
                else: end = waveformParas[1]
                slope = (start-end)/pulsewidth
                qosp = [slope, start]
                op.purePulse(qosp, channel=self.ifChannel, shape='linear')

            def get_ringup():
                if len(waveformParas)==1:
                    sfactor = 4
                    edgeLength = 30
                    peakMultiplier = 0
                else:
                    if isnan(waveformParas[0]): sfactor = 4
                    else: sfactor = waveformParas[0]
                    if isnan(waveformParas[1]): edgeLength = 30
                    else: edgeLength = waveformParas[1]
                    if isnan(waveformParas[2]): peakMultiplier = 0
                    else: peakMultiplier = waveformParas[2]

                qosp = [pulseheight, 1/(sfactor), edgeLength, peakMultiplier]
                op.purePulse(qosp, channel=self.ifChannel, shape='ringup')
            # 5. Gaussian connector:

            # 6. Sine

            # 7. Cosine

            # 8. Hyperbolic
            #else: print(Fore.RED + "UNRECOGNIZED PULSE-SHAPE. PLEASE CONSULT HELP.")
            pulse = {
                'flat': get_flat,
                'gauss': get_gauss,
                'gaussup': get_gaussup,
                'gaussdn': get_gaussdn,
                'dgauss': get_dgauss,
                'dgaussup': get_dgaussup,
                'dgaussdn': get_dgaussdn,
                'drag': get_drag,
                'lin': get_linear,
                'gestep': get_ringup,
            }
            pulseType = beat.split('/')[0]
            pulse[pulseType]()
            #print(pulseType,paras)
            self.operationList.append(op)

        # Fill remain pts with idle gate
        remainPts = int( -(self.beatime-self.totaltime) // self.dt)
        if remainPts > 0:
            op = qos.PulseBuilder(remainPts,self.dt)
            op.idle([0], channel=self.ifChannel)
            self.operationList.append(op)

        # 2. Envelope before IF-Mixing:
        self.operationSeq.set_operation(self.operationList)
        self.operationSeq.generate_sequenceWaveform(mixerInfo=self.mixerInfo,firstOperationIdx=self.firstOperationIdx)
        self.timeline = qos.get_timeAxis(self.operationSeq.iqwaveform)

        if self.ifChannel == "i":
            self.envelope = abs(self.operationSeq.xywaveform["data"])
            self.music = self.operationSeq.iqwaveform["data"].real

        elif self.ifChannel == "q":
            self.envelope = abs(self.operationSeq.xywaveform["data"])
            self.music = self.operationSeq.iqwaveform["data"].imag
        elif self.ifChannel == "z":
            self.envelope = abs(self.operationSeq.xywaveform["data"])
            self.music = abs(self.operationSeq.iqwaveform["data"])
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
    xyi = pulser(dt=.5,score='ns=500/1,mhz=I/-91/; Flat/,10,0; drag/,30,0.5;',clock_multiples=1)
    xyi.song()
    xyq = pulser(dt=.5,score='ns=500/1,mhz=Q/-91/; Flat/,10,0; drag/,30,0.5;',clock_multiples=1)
    xyq.song()

    cz = pulser(dt=.5,score='ns=500;Flat/,10,0.5;',clock_multiples=1)
    cz.song()

    roi = pulser(dt=.5,score='ns=500/1,mhz=I/-29/; Flat/,40,0; gestep///1,400,0.2;',clock_multiples=1)
    roi.song()
    roq = pulser(dt=.5,score='ns=500/1,mhz=Q/-29/; Flat/,40,0; gestep///1,400,0.2;',clock_multiples=1)
    roq.song()

    plot1 = plt.figure(1)
    plt.plot(xyi.timeline, xyi.envelope)
    plt.plot(xyq.timeline, xyq.envelope)
    plt.title("XY envelope")
    plot2 = plt.figure(2)
    plt.plot(xyi.timeline, xyi.music)
    plt.plot(xyq.timeline, xyq.music)
    plt.plot(cz.timeline, cz.music)
    plt.plot(roi.timeline, roi.music)
    plt.plot(roq.timeline, roq.music)
    plt.title("AWG real output")
    plt.show()


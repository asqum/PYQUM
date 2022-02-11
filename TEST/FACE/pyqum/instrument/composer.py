# Aim to compose a lyric for Qubit

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from copy import copy
from math import trunc, ceil
from numpy import linspace, power, exp, array, zeros, sin, cos, pi, where, ceil, clip, empty, radians, nan, isnan
from pyqum.instrument.logger import get_status
import pulse_generator.hardware_information as phyCh
import pulse_generator.gate_operation as qos
class pulser:
    '''
    Next generation of Pulse Assembly:\n
    All time-units in ns\n
    dt: time-resolution of AWG in ns\n
    clock_multiples: depends on AWG model, waveform must consist of certain multiple of points\n
    score: analogous to music score, basically a set of syntatical instructions to build the "music": \n
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
        except(IndexError): self.mix_params = "i/0" # default: unity = cos(zeros)
        
        self.iffreq = float(self.mix_params.split("/")[1]) # pre-loading IF-frequency in MHz
        try: 
            self.mixer_module = self.mix_params.split("/")[2]
            if self.mixer_module=='' : self.mixer_module = "pure" # for the case where mhz=i/37/<empty>
        except(IndexError): 
            self.mixer_module = "pure" # "pure": "1/0/0" in json-configuration for MIXER

        # if "i" in self.mixer_module.lower(): self.IF_MHz_rotation = float(self.mixer_module.split('i')[1]) # in MHz
        # elif "q" in self.mixer_module.lower(): self.IF_MHz_rotation = float(self.mixer_module.split('q')[1])
        self.IF_MHz_rotation = self.iffreq # uncalibrated pure case, generalised to support baseband case where IF=0
        
        self.ifChannel = self.mix_params.split("/")[0] # Get current IF Channel

        awgInfo = phyCh.AWGChannel()
        awgInfo.timeResolution=dt
        mixerInfo = phyCh.IQMixerChannel()    

        # set IQ Mixer calibration parameters into IQMixerChannel object
        try:
            mixerName = self.mixer_module.split(self.ifChannel.lower())[0]
            lable_IF = self.mixer_module.split(self.ifChannel.lower())[1]
            channel_I = mixerName+'i'+lable_IF
            channel_Q = mixerName+'q'+lable_IF
            amp_I, phase_I, offset_I = [float(x) for x in get_status("MIXER")[channel_I].split("/")]
            amp_Q, phase_Q, offset_Q = [float(x) for x in get_status("MIXER")[channel_Q].split("/")]
            mixerInfo.ampBalance = amp_I/amp_Q
            mixerInfo.phaseBalance = phase_I-phase_Q
            mixerInfo.offset = ( offset_I, offset_Q )
        except:
            mixerInfo.ampBalance = 1
            mixerInfo.phaseBalance = 90
            mixerInfo.offset = ( 0, 0 )
        mixerInfo.ifFreq = self.iffreq
        
        #print("register one channel for a Qubit")
        pch = phyCh.PhysicalChannel( awgInfo, mixerInfo ) 
        #print("init OS")
        self.operationSeq = qos.QubitOperationSequence( originTotalPoint, pch )
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


            paras = []
            for p in beat.split('/')[1].split(','):
                if p == '':
                    paras.append( nan )
                else:
                    paras.append( float(p) )
            pulsewidth = float(paras[1])
            pulseheight = float(paras[2])
            pulsePts = int(-(pulsewidth//-self.dt))
            self.beatime += pulsePts*self.dt
            op = qos.PulseBuilder(pulsePts,self.dt)
            # Shapes of Tones:
            # 1. Constant Flat Line:
            def get_flat(): 
                op.idle([pulseheight], channel=self.ifChannel)

            # Gaussian
            # 2.0 complete:
            def get_gauss():
                if isnan(paras[0]): sfactor = 2
                else: sfactor = paras[0]
                qosp = [pulseheight, 1/(sfactor*2)]
                op.purePulse(qosp, channel=self.ifChannel, shape='gaussian')

            # 2.1 raising from zero:
            def get_gaussup():
                if isnan(paras[0]): sfactor = 2
                else: sfactor = paras[0]
                qosp = [pulseheight, 1/sfactor]
                op.purePulse(qosp, channel=self.ifChannel, shape='gaussian_half')

            # 2.2 falling to zero:
            def get_gaussdn():
                if isnan(paras[0]): sfactor = 2
                else: sfactor = paras[0]
                qosp = [pulseheight, -1/sfactor]
                op.purePulse(qosp, channel=self.ifChannel, shape='gaussian_half')
            # 3 Derivative Gaussian
            # 3.0
            def get_dgauss():
                if isnan(paras[0]): sfactor = 2
                else: sfactor = paras[0]
                qosp = [pulseheight, -1/(sfactor*2)]
                op.purePulse(qosp, channel=self.ifChannel, shape='degaussian')
            
            # 3.1 DRAG up
            def get_dgaussup():
                if isnan(paras[0]): sfactor = 2
                else: sfactor = paras[0]
                qosp = [pulseheight, 1/sfactor]
                op.purePulse(qosp, channel=self.ifChannel, shape='degaussian_half')
            # 3.2 DRAG dn
            def get_dgaussdn():
                if isnan(paras[0]): sfactor = 2
                else: sfactor = paras[0]
                qosp = [pulseheight, -1/sfactor]
                op.purePulse(qosp, channel=self.ifChannel, shape='degaussian_half')

            # PENDING: BUILD CONNECTORS: require the knowledge of the last height
            def get_drag():
                if isnan(paras[0]): sfactor = 2
                else: sfactor = paras[0]
                if isnan(paras[3]): dRatio = 1
                else: dRatio = paras[3]
                if isnan(paras[4]): rotAxis = 0
                else: rotAxis = radians(paras[4])
                qosp = [pulseheight, 1/(sfactor*2), dRatio, rotAxis]
                op.rotXY(qosp, shape='fDRAG')
            # 4. Linear connector: 

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
            }
            pulseType = beat.split('/')[0]
            pulse[pulseType]()
            #print(pulseType,paras)
            self.operationList.append(op)

        # 2. Envelope before IF-Mixing:
        self.operationSeq.set_operation(self.operationList)
        self.operationSeq.generate_sequenceWaveform(firstOperationIdx=self.firstOperationIdx)
        self.timeline = qos.get_timeAxis(self.operationSeq.iqwaveform)

        if self.ifChannel == "i":
            self.envelope = abs(self.operationSeq.xywaveform["data"])
            self.music = self.operationSeq.iqwaveform["data"].real

        elif self.ifChannel == "q":
            self.envelope = abs(self.operationSeq.xywaveform["data"])
            self.music = self.operationSeq.iqwaveform["data"].imag

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
    pr = pulser(dt=.5,score='ns=200/3,mhz=I/-91/; Flat/,50,0; Flat/,20,1; Flat/,5,0; Gauss/,20,1; Flat/,10,0; dGauss/,20,1; Flat/,10,0; drag/,20,1,5,; ',clock_multiples=1)
    pr.song()
    timeAxis = pr.timeline
    envelope = pr.envelope
    music = pr.music

    pr2 = pulser(dt=.5,score='ns=200/3,mhz=Q/-91/; Flat/,50,0; Flat/,20,1; Flat/,5,0; Gauss/,20,1; Flat/,10,0; dGauss/,20,1; Flat/,10,0; drag/,20,1,5,; ',clock_multiples=1)
    pr2.song()
    timeAxis2 = pr2.timeline
    envelope2 = pr2.envelope
    music2 = pr2.music

    plot1 = plt.figure(1)

    plt.plot(timeAxis, envelope)
    plt.plot(timeAxis2, envelope2)
    plot2 = plt.figure(2)
    plt.plot(timeAxis, envelope)
    plt.plot(timeAxis, music)
    plt.title("I")
    plot2 = plt.figure(3)
    plt.plot(timeAxis2, envelope2)
    plt.plot(timeAxis2, music2)
    plt.title("Q")
    plot2 = plt.figure(4)
    plt.plot(timeAxis, music)
    plt.plot(timeAxis2, music2)
    plt.show()


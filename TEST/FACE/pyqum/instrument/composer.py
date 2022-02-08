# Aim to compose a lyric for Qubit

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from copy import copy
from math import trunc, ceil
from numpy import linspace, power, exp, array, zeros, sin, cos, pi, where, ceil, clip, empty, radians
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
        self.dt = dt
        self.score = score.replace(" ","").replace("\n","").lower() # get rid of multiple spacings & new-lines and also lower the cases
        try: self.mix_params = self.score.split(";")[0].split(",")[1].split('mhz=')[1]
        except(IndexError): self.mix_params = "q/0" # default: unity = cos(zeros)
        self.iffreq = float(self.mix_params.split("/")[1]) # pre-loading IF-frequency in MHz
        
        # modify user input time
        originTotaltime = float(self.score.split(";")[0].split(",")[0].split('ns=')[1])
        originTotalPoint = int( -(originTotaltime //-dt) )
        
        self.totalpoints = int(clock_multiples) *int( -(originTotalPoint //-clock_multiples) )
        self.totaltime = self.totalpoints* dt
        print(originTotaltime, self.totaltime)
        self.beatime, self.music = 0, zeros([self.totalpoints])


        self.timeline = linspace( 0, self.totaltime, self.totalpoints)
        # mixing module:
        try: 
            self.mixer_module = self.mix_params.split("/")[2]
            # while ' ' in self.mixer_module: self.mixer_module = self.mixer_module.replace(' ','') # omit spaces (already did from the very beginning.)
            if self.mixer_module=='' : self.mixer_module = "pure" # for the case where mhz=i/37/<empty>
        except(IndexError): 
            self.mixer_module = "pure" # "pure": "1/0/0" in json-configuration for MIXER

        # if "i" in self.mixer_module.lower(): self.IF_MHz_rotation = float(self.mixer_module.split('i')[1]) # in MHz
        # elif "q" in self.mixer_module.lower(): self.IF_MHz_rotation = float(self.mixer_module.split('q')[1])
        self.IF_MHz_rotation = self.iffreq # uncalibrated pure case, generalised to support baseband case where IF=0
        
        ifChannel = self.mix_params.split("/")[0] # Get current IF Channel

        q1 = phyCh.Qubit() # Dump (register Qubit)
        p1 = phyCh.InputPort() # Dump (register InputPort)
        m1 = phyCh.IQMixerChannel() 
        # set IQ Mixer calibration parameters into IQMixerChannel object
        try:
            mixerName = self.mixer_module.split(ifChannel.lower())[0]
            lable_IF = self.mixer_module.split(ifChannel.lower())[1]
            channel_I = mixerName+'i'+lable_IF
            channel_Q = mixerName+'q'+lable_IF
            amp_I, phase_I, offset_I = [float(x) for x in get_status("MIXER")[channel_I].split("/")]
            amp_Q, phase_Q, offset_Q = [float(x) for x in get_status("MIXER")[channel_Q].split("/")]
            m1.ampBalance = amp_I/amp_Q
            m1.phaseBalance = phase_I-phase_Q
            m1.offset = ( offset_I, offset_Q )
        except:
            m1.ampBalance = 1
            m1.phaseBalance = 90
            m1.offset = ( 0, 0 )
        m1.ifFreq = self.iffreq
        
        pch1 = phyCh.HardwareInfo(q1,p1,m1) # requirment of operation sequence
        pch1.timeResolution = dt
        self.operationSeq = qos.OperationSequence( self.totaltime, pch1 )
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

            pulsewidth = float(beat.split(',')[1])
            pulseheight = float(beat.split(',')[2])
            samples = int(pulsewidth//self.dt)
            currentPoint = int(self.beatime//self.dt)
            duration = range(currentPoint, currentPoint +samples)
            self.beatime += pulsewidth
            op = qos.Operation(pulsewidth)
            # Shapes of Tones:
            # 1. Constant Flat Line:
            def get_flat():
                
                op.idle([pulseheight])
                self.operationList.append(op)
                # qos.IFPulse(startTime=None, operationTime=None)
                return qos.constFunc(empty(samples) ,[pulseheight])

            # Gaussian
            # 2.0 complete:
            def get_gauss():
                if beat.split(',')[0].split('/')[1] == '': sfactor = 2
                else: sfactor = float(beat.split(',')[0].split('/')[1])
                timeSegment = linspace(-pulsewidth/2, pulsewidth/2, samples,endpoint=False)
                sigma = pulsewidth /(sfactor*2)
                p = [pulseheight, sigma, 0]
                qosp = [pulseheight, 1/(sfactor*2)]
                op.purePulse(qosp, shape='gaussian')
                self.operationList.append(op)
                return qos.gaussianFunc(timeSegment, p)

            # 2.1 raising from zero:
            def get_gaussup():
                if beat.split(',')[0].split('/')[1] == '': sfactor = 2
                else: sfactor = float(beat.split(',')[0].split('/')[1])
                timeSegment = linspace( -pulsewidth, 0, samples, endpoint=False)
                sigma = pulsewidth /sfactor
                p = [pulseheight, sigma, 0]
                qosp = [pulseheight, 1/sfactor]
                op.purePulse(qosp, shape='gaussian_half')
                self.operationList.append(op)
                return qos.gaussianFunc(timeSegment,p)
            # 2.2 falling to zero:
            def get_gaussdn():
                if beat.split(',')[0].split('/')[1] == '': sfactor = 2
                else: sfactor = float(beat.split(',')[0].split('/')[1])
                timeSegment = linspace( 0, pulsewidth, samples, endpoint=False)
                sigma = pulsewidth /sfactor
                p = [pulseheight, sigma, 0]
                qosp = [pulseheight, -1/sfactor]
                op.purePulse(qosp, shape='gaussian_half')
                self.operationList.append(op)
                return qos.gaussianFunc(timeSegment,p)
            # 3 Derivative Gaussian
            # 3.0
            def get_dgauss():
                if beat.split(',')[0].split('/')[1] == '': sfactor = 2
                else: sfactor = float(beat.split(',')[0].split('/')[1])
                timeSegment = linspace( -pulsewidth/2, pulsewidth/2, samples, endpoint=False)
                sigma = pulsewidth /(sfactor*2)
                p = [pulseheight, sigma, 0]
                qosp = [pulseheight, -1/(sfactor*2)]
                op.purePulse(qosp, shape='degaussian_half')
                self.operationList.append(op)
                return qos.derivativeGaussianFunc(timeSegment,p)
            
            # 3.1 DRAG up
            def get_dgaussup():
                if beat.split(',')[0].split('/')[1] == '': sfactor = 2
                else: sfactor = float(beat.split(',')[0].split('/')[1])
                timeSegment = linspace( -pulsewidth, 0, samples, endpoint=False) 
                sigma = pulsewidth /sfactor
                p = [pulseheight, sigma, 0]
                qosp = [pulseheight, 1/sfactor]
                op.purePulse(qosp, shape='degaussian_half')
                self.operationList.append(op)
                return qos.derivativeGaussianFunc(timeSegment,p)
            # 3.2 DRAG dn
            def get_dgaussdn():
                if beat.split(',')[0].split('/')[1] == '': sfactor = 2
                else: sfactor = float(beat.split(',')[0].split('/')[1])
                timeSegment = linspace(0, pulsewidth, samples, endpoint=False)
                sigma = pulsewidth /sfactor
                p = [pulseheight, sigma, 0]
                qosp = [pulseheight, -1/sfactor]
                op.purePulse(qosp, shape='degaussian')
                self.operationList.append(op)
                return qos.derivativeGaussianFunc(timeSegment,p)
            # PENDING: BUILD CONNECTORS: require the knowledge of the last height
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
            }
            pulseType = beat.split(',')[0].split('/')[0]
            print(pulseType)
            self.music[duration] = pulse[pulseType]()

        # 2. Envelope before IF-Mixing:
        self.envelope = copy(self.music)
        self.operationSeq.set_operation(self.operationList)
        print("operation number",len(self.operationList))
        #self.envelope = copy(self.operationSeq.cal_pulseSequence()["data"].real)
        
        # 3. Offsetting phase to the starting of the pulse (1. to lock readout-phase 2. ?):
        try: 
            pulse_starting_time = self.dt * where(ceil(abs(self.music-self.music[-1]))==1)[0][0]
            #print(pulse_starting_time)
            # print(Back.WHITE + Fore.BLUE + "Pulse starting from %s ns" %pulse_starting_time)
        except(IndexError): 
            pulse_starting_time = 0 # for PURE FLAT LINE!
            # print(Back.WHITE + Fore.RED + "PURE FLAT LINE!")

        # 4. IF Mixing:
        '''
        ns=<Pulse-period>,mhz=<I/Q>/<PENDING: relative-IF>/<Mixer-calibration>; <Pulse-shape>,<Pulse-width>,<Pulse-height>; ...
        <Mixer-calibration> = <Mixer-module> + <i/q> + <IF-correction> (PENDING: + <LO> + <IF-amplitude>)
        <Converted-RF> or <Target-RF> = <LO> + <IF-correction>
        '''
        if self.mix_params.split("/")[0] == 'i': ifphase = 0
        elif self.mix_params.split("/")[0] == 'q': ifphase = 90
        else: print(Fore.RED + "UNRECOGNIZED CW-TYPE. PLEASE CONSULT HELP.")

        try:
            ifamp, phaseBalance, ifoffset = [float(x) for x in get_status("MIXER")[self.mixer_module].split("/")]
        except:
            ifamp, phaseBalance, ifoffset = [1,0,0]
        self.music = self.music * ifamp * cos((self.timeline-pulse_starting_time)*self.iffreq/1e3*2*pi + radians(phaseBalance +ifphase)) +ifoffset

        # Confine music between -1 and 1:
        self.music = clip(self.music, -1.0, 1.0, out=self.music)

        return self.music


# test
# abc = pulser(dt=0.4, clock_multiples=1, score='NS=10; Flat/,2,0;Gaussup/,4,0.5;gA uss dn/,4,0.5;')
# abc.song()
# print("%sns music:\n%s" %(abc.totaltime, abc.music))
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    pr = pulser(dt=1.,score='ns=100,mhz=I/-0/; Flat/,10,0; dGaussup/,20,1; Flat/,10,0; dGauss/,20,; Flat/,10,0; dGaussdn/,20,0; ',clock_multiples=1)
    #print(pr.score)
    IFsignal = pr.song()
    timeAxis = linspace(0,pr.dt*len(IFsignal),len(IFsignal), endpoint=False)
    #print(pr.operationSeq.sequencePts)
    pr.operationSeq.cal_pulseSequence()
    IFsignalNew = pr.operationSeq.iqwaveform["data"].real
    plot1 = plt.figure(1)
    plt.plot(timeAxis, IFsignal)
    #(len(IFsignalNew))
    plt.plot(timeAxis, IFsignalNew)
    plt.show()


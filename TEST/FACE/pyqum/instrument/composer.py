# Aim to compose a lyric for Qubit

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from copy import copy
from math import trunc
from numpy import linspace, power, exp, array, zeros, sin, cos, pi, where, ceil, clip
from pyqum.instrument.logger import get_status

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
        self.totaltime = float(self.score.split(";")[0].split(",")[0].split('ns=')[1])
        try: self.mix_params = self.score.split(";")[0].split(",")[1].split('mhz=')[1]
        except(IndexError): self.mix_params = "q/0" # default: unity = cos(zeros)
        self.iffreq = float(self.mix_params.split("/")[1]) # pre-loading IF-frequency in MHz
        self.totalpoints = int(clock_multiples*trunc(self.totaltime / dt / clock_multiples)) + int(bool((self.totaltime / dt)%clock_multiples))*clock_multiples
        self.beatime, self.music = 0, zeros([self.totalpoints])
        self.timeline = linspace(self.dt, self.totaltime, self.totalpoints)
        # mixing module:
        try: 
            self.mixer_module = self.mix_params.split("/")[2]
            # while ' ' in self.mixer_module: self.mixer_module = self.mixer_module.replace(' ','') # omit spaces (already did from the very beginning.)
            if self.mixer_module=='' : self.mixer_module = "pure" # for the case where mhz=i/37/<empty>
        except(IndexError): 
            self.mixer_module = "pure" # "pure": "1/0/0" in json-configuration for MIXER
        if "i" in self.mixer_module.lower(): self.IF_MHz_rotation = float(self.mixer_module.split('i')[1]) # in MHz
        elif "q" in self.mixer_module.lower(): self.IF_MHz_rotation = float(self.mixer_module.split('q')[1])
        else: self.IF_MHz_rotation = self.iffreq # uncalibrated pure case, generalised to support baseband case where IF=0

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
            self.beatime += pulsewidth
            duration = range(round(self.beatime/self.dt) - round(pulsewidth/self.dt), round(self.beatime/self.dt))

            # Shapes of Tones:
            # 1. Constant Flat Line:
            if beat.split(',')[0].split('/')[0] == 'flat':
                self.music[duration] = pulseheight

            # Gaussian
            # 2.0 complete:
            elif beat.split(',')[0].split('/')[0] == 'gauss':
                if beat.split(',')[0].split('/')[1] == '': sfactor = 6
                else: sfactor = float(beat.split(',')[0].split('/')[1])
                sigma = pulsewidth / sfactor/2
                timeSegment = linspace(self.dt -pulsewidth/2, pulsewidth/2, round(pulsewidth/self.dt))
                self.music[duration] = pulseheight * exp(-(timeSegment/sigma)**2 / 2 )

            # 2.1 raising from zero:
            elif beat.split(',')[0].split('/')[0] == 'gaussup':
                if beat.split(',')[0].split('/')[1] == '': sfactor = 6
                else: sfactor = float(beat.split(',')[0].split('/')[1])
                sigma = pulsewidth / sfactor
                timeSegment = linspace(self.dt, pulsewidth, round(pulsewidth/self.dt)) - pulsewidth
                self.music[duration] = pulseheight * exp(-(timeSegment/sigma)**2/2 )

            # 2.2 falling to zero:
            elif beat.split(',')[0].split('/')[0] == 'gaussdn':
                if beat.split(',')[0].split('/')[1] == '': sfactor = 6
                else: sfactor = float(beat.split(',')[0].split('/')[1])
                sigma = pulsewidth / sfactor
                timeSegment = linspace( self.dt, pulsewidth, round(pulsewidth/self.dt))
                self.music[duration] = pulseheight * exp(-(timeSegment/sigma)**2/2 )

            # PENDING: BUILD CONNECTORS: require the knowledge of the last height

            # 3 Derivative Gaussian
            # 3.0
            elif beat.split(',')[0].split('/')[0] == 'dgauss':
                if beat.split(',')[0].split('/')[1] == '': sfactor = 6
                else: sfactor = float(beat.split(',')[0].split('/')[1])
                sigma = pulsewidth / sfactor/2
                timeSegment = linspace(self.dt -pulsewidth/2, pulsewidth/2, round(pulsewidth/self.dt))
                self.music[duration] = -pulseheight / sigma**2 *timeSegment *exp(-(timeSegment/sigma)**2 / 2 )
            
            # 3.1 DRAG up
            elif beat.split(',')[0].split('/')[0] == 'dgaussup':
                if beat.split(',')[0].split('/')[1] == '': sfactor = 6
                else: sfactor = float(beat.split(',')[0].split('/')[1])
                sigma = pulsewidth / sfactor
                timeSegment = linspace(self.dt, pulsewidth, round(pulsewidth/self.dt)) - pulsewidth
                self.music[duration] = -pulseheight / sigma**2 *timeSegment *exp(-(timeSegment/sigma)**2 / 2 )
            # 3.2 DRAG dn
            elif beat.split(',')[0].split('/')[0] == 'dgaussdn':
                if beat.split(',')[0].split('/')[1] == '': sfactor = 6
                else: sfactor = float(beat.split(',')[0].split('/')[1])
                sigma = pulsewidth / sfactor
                timeSegment = linspace( self.dt, pulsewidth, round(pulsewidth/self.dt))
                self.music[duration] = -pulseheight / sigma**2 *timeSegment *exp(-(timeSegment/sigma)**2 / 2 )
            # 4. Linear connector: 

            # 5. Gaussian connector:

            # 6. Sine

            # 7. Cosine

            # 8. Hyperbolic
            else: print(Fore.RED + "UNRECOGNIZED PULSE-SHAPE. PLEASE CONSULT HELP.")
        
        # 2. Envelope before IF-Mixing:
        self.envelope = copy(self.music)

        # 3. Offsetting phase to the starting of the pulse (1. to lock readout-phase 2. ?):
        try: 
            pulse_starting_time = self.dt * where(ceil(abs(self.music-self.music[-1]))==1)[0][0]
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
        if self.mix_params.split("/")[0] == 'i': iffunction = "sin"
        elif self.mix_params.split("/")[0] == 'q': iffunction = "cos"
        else: print(Fore.RED + "UNRECOGNIZED CW-TYPE. PLEASE CONSULT HELP.")

        ifamp, ifphase, ifoffset = [float(x) for x in get_status("MIXER")[self.mixer_module].split("/")]
        self.music = self.music * ifamp * eval(iffunction + '((self.timeline-pulse_starting_time)*%s/1000*2*pi + %s/180*pi)' %(self.iffreq,ifphase)) + ifoffset

        # Confine music between -1 and 1:
        self.music = clip(self.music, -1.0, 1.0, out=self.music)

        return


# test
# abc = pulser(dt=0.4, clock_multiples=1, score='NS=10; Flat/,2,0;Gaussup/,4,0.5;gA uss dn/,4,0.5;')
# abc.song()
# print("%sns music:\n%s" %(abc.totaltime, abc.music))

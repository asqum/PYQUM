# Aim to compose a lyric for Qubit

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from math import trunc
from numpy import linspace, power, exp, array, zeros, sin, cos, pi, where, ceil
from pyqum.instrument.logger import get_status

class pulser:
    '''
    Next generation of Pulse Assembly:\n
    All time-units in ns\n
    dt: time-resolution of AWG in ns\n
    clock_multiples: depends on AWG model, waveform must consist of certain multiple of points\n
    score: analogous to music score, basically a set of syntatical instructions to build the "music": \n
            "ns=<totaltime>; <shape>/<param#1>/.../<param#n>, pulse-width, pulse-height; ... ..."
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

    def song(self):
        '''
        compose the song based on the score given:
            ns=<period/length of the song>;
            <pulse-shape>/[<unique factor(s): default (to pulse-library) database) if blank], <pulse-period>, <pulse-height: between -1 & +1>;
            stack a variety of pulse-instruction(s) according to the format illustrated above.
        '''
        # BB Shaping:
        for beat in self.score.split(";")[1:]:
            if beat == '': break # for the last semicolon

            pulsewidth = float(beat.split(',')[1])
            pulseheight = float(beat.split(',')[2])
            self.beatime += pulsewidth
            duration = range(round(self.beatime/self.dt) - round(pulsewidth/self.dt), round(self.beatime/self.dt))

            # Shapes of Tones:
            if beat.split(',')[0].split('/')[0] == 'flat':
                self.music[duration] = pulseheight
                
            elif beat.split(',')[0].split('/')[0] == 'gaussup':
                if beat.split(',')[0].split('/')[1] == '': sfactor = 6
                else: sfactor = float(beat.split(',')[0].split('/')[1])
                sigma = pulsewidth / sfactor
                self.music[duration] = pulseheight * exp(-power((linspace(self.dt, pulsewidth, round(pulsewidth/self.dt)) - pulsewidth), 2) / 2 / (sigma**2))

            elif beat.split(',')[0].split('/')[0] == 'gaussdn':
                if beat.split(',')[0].split('/')[1] == '': sfactor = 6
                else: sfactor = float(beat.split(',')[0].split('/')[1])
                sigma = pulsewidth / sfactor
                self.music[duration] = pulseheight * exp(-power((linspace(pulsewidth, self.dt, round(pulsewidth/self.dt)) - pulsewidth), 2) / 2 / (sigma**2))

            else: print(Fore.RED + "UNRECOGNIZED PULSE-SHAPE. PLEASE CONSULT HELP.")

        # Offsetting phase to the rising of the pulse:
        try: 
            pulse_rising_time = self.dt * where(ceil(abs(self.music-self.music[-1]))==1)[0][0]
            # print(Back.WHITE + Fore.BLUE + "Pulse rising from %s ns" %pulse_rising_time)
        except(IndexError): 
            pulse_rising_time = 0 # for PURE FLAT LINE!
            # print(Back.WHITE + Fore.RED + "PURE FLAT LINE!")

        # IF Mixing:
        if self.mix_params.split("/")[0] == 'i': iffunction = "sin"
        elif self.mix_params.split("/")[0] == 'q': iffunction = "cos"
        else: print(Fore.RED + "UNRECOGNIZED CW-TYPE. PLEASE CONSULT HELP.")
        try: mixer_module = self.mix_params.split("/")[2]
        except(IndexError): mixer_module = "ideal"
        ifamp, ifphase, ifoffset = [float(x) for x in get_status("MIXER")[mixer_module].split("/")]
        self.music = self.music * ifamp * eval(iffunction + '((self.timeline-pulse_rising_time)*%s/1000*2*pi + %s/180*pi)' %(self.iffreq,ifphase)) + ifoffset

        return


# test
# abc = pulser(dt=0.4, clock_multiples=1, score='NS=10; Flat/,2,0;Gaussup/,4,0.5;gA uss dn/,4,0.5;')
# abc.song()
# print("%sns music:\n%s" %(abc.totaltime, abc.music))

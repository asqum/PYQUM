# Aim to compose a lyric for Qubit

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from math import trunc
from numpy import linspace, power, exp, array, zeros

class pulser:
    '''
    Next generation of Pulse Assembly:\n
    All time-units in ns\n
    dt: time-resolution of AWG in ns\n
    clock_multiples: depends on AWG model, waveform must consist of certain multiple of points\n
    score: analogous to music score, basically a set of syntatical instructions to build the "music": \n
            "ns=<totaltime>; <shape>/<param#1>/.../<param#n>, pulse-width, pulse-height; ... ..."
    NOTE: implement delay as one of the beats for the sake of simplicity, instead of seperated parameter. (Ex: to delay 100ns, write: "flat,100,0")
    '''
    def __init__(self, dt=0.8, clock_multiples=8, 
                score='Gaussup/6,100,1; Flat,100,1; Gaussdn/6,100,1; Pause,300,1; Gaussup/6,100,1; Flat,100,1; Gaussdn/6,100,1;'):
        self.dt = dt
        self.score = score.replace(" ","").replace("\n","").lower() # get rid of multiple spacings and lower the cases
        self.totaltime = float(self.score.split(";")[0].split('ns=')[1])
        self.totalpoints = int(clock_multiples*trunc(self.totaltime / dt / clock_multiples)) + int(bool((self.totaltime / dt)%clock_multiples))*clock_multiples
        self.beatime, self.music = 0, zeros([self.totalpoints])
        self.timeline = linspace(0, self.totaltime, self.totalpoints)

    def song(self):
        '''
        compose the song based on the score given:
            ns=<period/length of the song>;
            <pulse-shape>/[<unique factor(s): default (to pulse-library) database) if blank], <pulse-period>, <pulse-height: between -1 & +1>;
            stack a variety of pulse-instruction(s) according to the format illustrated above.
        '''
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
                self.music[duration] = pulseheight * exp(-power((linspace(0, pulsewidth, round(pulsewidth/self.dt)) - pulsewidth), 2) / 2 / (sigma**2))

            elif beat.split(',')[0].split('/')[0] == 'gaussdn':
                if beat.split(',')[0].split('/')[1] == '': sfactor = 6
                else: sfactor = float(beat.split(',')[0].split('/')[1])
                sigma = pulsewidth / sfactor
                self.music[duration] = pulseheight * exp(-power((linspace(pulsewidth, 0, round(pulsewidth/self.dt)) - pulsewidth), 2) / 2 / (sigma**2))

            else: print(Fore.RED + "UNRECOGNIZED PULSE. PLEASE CONSULT HELP.")

        return


# test
# abc = pulser(dt=0.4, clock_multiples=1, score='NS=10; Flat/,2,0;Gaussup/,4,0.5;gA uss dn/,4,0.5;')
# abc.song()
# print("%sns music:\n%s" %(abc.totaltime, abc.music))

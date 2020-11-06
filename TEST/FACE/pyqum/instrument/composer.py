# Aim to compose a lyric for Qubit

from numpy import linspace

def squarewave(totaltime, ontime, delay, scale=1, offset=0, dt=0.8, clock_multiples=8, Ramsey_delay=0, Hahn_echo='off', ringup=0):
    '''TO BE DEPRECATED ONCE IT HAS BEEN FULLY REPLACED BY PULSER
    '''
    totalpoints = int(clock_multiples*trunc(totaltime / dt / clock_multiples)) + int(bool((totaltime / dt)%clock_multiples))*clock_multiples # keep total-points to be the multiples of clock_multiples of specific instruments
    delaypoints = round(delay / dt)
    onpoints = round(ontime / dt)

    if Ramsey_delay==0: # normal pulse sequence
        offpoints = totalpoints - delaypoints - onpoints
        wave = [offset]*delaypoints + [scale]*onpoints + [offset]*offpoints
    elif Ramsey_delay>0:
        Ramsey_points = round(Ramsey_delay / dt)
        offpoints = totalpoints - delaypoints - 2*onpoints - Ramsey_points
        wave = [offset]*delaypoints + [scale]*onpoints + [offset]*Ramsey_points + [scale]*onpoints + [offset]*offpoints
    else:
        wave = []
        print("Invalid Ramsey!")

    return wave
# Next generation of Pulse Assembly:
def pulser(totaltime, ontime, delay, scale=1, offset=0, dt=0.8, clock_multiples=8, Ramsey_delay=0, Hahn_echo='off', ringup=0, shape='Gaussian'):
    '''time-unit: ns
        totaltime: total duration (minimum: 1000*0.8ns ~ 1us)
        ontime: +1V duration
        delay: duration before ontime
        scale: -1 to 1 output level in V
        offset: to eliminate LO leakage
        dt: time-resolution of AWG in ns
    '''
    totalpoints = int(clock_multiples*trunc(totaltime / dt / clock_multiples)) + int(bool((totaltime / dt)%clock_multiples))*clock_multiples # keep total-points to be the multiples of clock_multiples of specific instruments
    delaypoints = round(delay / dt)
    onpoints = round(ontime / dt)

    if shape == 'Square':
        pulsing = [scale]*onpoints
    elif shape == 'Gaussian':
        sigma = ontime / 6
        pulsing = list(scale * exp(-power((linspace(0, ontime, onpoints) - ontime/2), 2) / 2 / (sigma**2)))

    if Ramsey_delay==0: # normal pulse sequence
        offpoints = totalpoints - delaypoints - onpoints
        wave = [offset]*delaypoints + pulsing + [offset]*offpoints
    elif Ramsey_delay>0:
        Ramsey_points = round(Ramsey_delay / dt)
        offpoints = totalpoints - delaypoints - 2*onpoints - Ramsey_points
        wave = [offset]*delaypoints + pulsing + [offset]*Ramsey_points + pulsing + [offset]*offpoints
    else:
        wave = []
        print("Invalid Ramsey!")

    return wave
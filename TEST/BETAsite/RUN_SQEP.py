from numpy import sqrt, array, mean, sum, min, max

from pyqum.instrument.logger import set_status
from pyqum.instrument.toolbox import waveform, gotocdata
from pyqum.instrument.analyzer import curve, IQAParray


# 3. Test Square-wave Pulsing
from pyqum.directive.characterize import SQE_Pulse


# Set RUN mode:
set_status("SQE_Pulse", dict(pause=False))

# Assemble C-Structure:
CStructure = ['Flux-Bias', 'XY-Frequency', 'XY-Power', 'RO-Frequency', 'RO-Power',
                'Pulse-Period', 'RO-ifLevel', 'RO-Pulse-Delay', 'RO-Pulse-Width', 'XY-ifLevel', 'XY-Pulse-Delay', 'XY-Pulse-Width', 
                'LO-Frequency', 'LO-Power', 'ADC-delay', 'Average', 'Sampling-Time']

# Sweep RO-frequency:
S_CORDER = {'C-Structure': CStructure,
            'Flux-Bias':'-0.0031', 'XY-Frequency':'4.19', 'XY-Power':'-5', 'RO-Frequency':'4.89 to 4.9 * 100', 'RO-Power':'-20',
            'Pulse-Period':'15994', 'RO-ifLevel':'1', 'RO-Pulse-Delay':'0', 'RO-Pulse-Width':'15994', 'XY-ifLevel':'1', 'XY-Pulse-Delay':'0', 'XY-Pulse-Width':'15994',
            'LO-Frequency':'lockro,', 'LO-Power':'-20', 'ADC-delay':'0', 'Average':'1000', 'Sampling-Time':'2 to 2000 * 999'
            }
S_COMMENT = "Search for dressed cavity frequency at flux=-3.1mA"
S_TAG = 'cavity, spectroscopy'

# Sweep XY-frequency:
X_CORDER = {'C-Structure': CStructure,
            'Flux-Bias':'-0.0031', 'XY-Frequency':'3.7 to 4.5 * 100', 'XY-Power':'0', 'RO-Frequency':'4.893766', 'RO-Power':'-20',
            'Pulse-Period':'15994', 'RO-ifLevel':'1', 'RO-Pulse-Delay':'0', 'RO-Pulse-Width':'15994', 'XY-ifLevel':'1', 'XY-Pulse-Delay':'0', 'XY-Pulse-Width':'15994',
            'LO-Frequency':'lockro,', 'LO-Power':'-20', 'ADC-delay':'0', 'Average':'1000', 'Sampling-Time':'2 to 2000 * 999'
            }
X_COMMENT = "Search for qubit frequency at flux=-3.1mA"
X_TAG = 'two-tone, spectroscopy'

# Test XY-Pulses
TP_CORDER = {'C-Structure': CStructure,
            'Flux-Bias':'0', 'XY-Frequency':'4.128', 'XY-Power':'0', 'RO-Frequency':'opt,', 'RO-Power':'opt,',
            'Pulse-Period':'15994', 'RO-ifLevel':'1', 'RO-Pulse-Delay':'0', 'RO-Pulse-Width':'3000', 'XY-ifLevel':'1', 'XY-Pulse-Delay':'0', 'XY-Pulse-Width':'100 to 1000 * 19',
            'LO-Frequency':'4.128', 'LO-Power':'-10', 'ADC-delay':'0', 'Average':'100', 'Sampling-Time':'2 to 2000 * 999'
            }
TP_COMMENT = "Testing AWG consistency of pulse generation"

# Test Rabi
A_CORDER = {'C-Structure': CStructure,
            'Flux-Bias':'-0.0031', 'XY-Frequency':'4.19', 'XY-Power':'10', 'RO-Frequency':'4.89579', 'RO-Power':'-20',
            'Pulse-Period':'63994', 'RO-ifLevel':'1', 'RO-Pulse-Delay':'lockxypwd+50,', 'RO-Pulse-Width':'1600', 'XY-ifLevel':'1', 'XY-Pulse-Delay':'0', 'XY-Pulse-Width':'0 to 700 * 700',
            'LO-Frequency':'lockro,', 'LO-Power':'-20', 'ADC-delay':'0', 'Average':'10000', 'Sampling-Time':'2 to 3200 * 1599'
            }
A_COMMENT = "Measure Rabi population with time offset and higher xy-power with cavity detuning"
A_TAG = "Rabi"

# Phase sensitive:
T1_CORDER = {'C-Structure': CStructure,
            'Flux-Bias':'-0.0031', 'XY-Frequency':'4.19', 'XY-Power':'10', 'RO-Frequency':'4.93', 'RO-Power':'-20',
            'Pulse-Period':'63994', 'RO-ifLevel':'1', 'RO-Pulse-Delay':'85 to 5000 * 200', 'RO-Pulse-Width':'1600', 'XY-ifLevel':'1', 'XY-Pulse-Delay':'0', 'XY-Pulse-Width':'35',
            'LO-Frequency':'lockro,', 'LO-Power':'-20', 'ADC-delay':'lockropdelay,', 'Average':'10000', 'Sampling-Time':'2 to 3200 * 1599'
            }
T1_COMMENT = "Measure T1 with time offset and higher xy-power with cavity detuning"
T1_TAG = "T1"

# New measurement:
SQE_Pulse('abc', corder=T1_CORDER, comment=T1_COMMENT, tag=T1_TAG, dayindex=-1, testeach=False)

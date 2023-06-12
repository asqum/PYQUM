# Numpy
# Typing
from numpy import ndarray
# Numpy array
from numpy import array, append, zeros, ones, where, linspace
# Numpy common math function
from numpy import exp,sqrt,tanh,cosh
# Numpy constant
from numpy import pi, logical_and
# Scipy
from scipy.special import erf

def sech(x):
    return 1/cosh(x)

# Gaussian Family
def GaussianFamily (x, *p)->ndarray:
    """
    x: array like, shape (n,)\n
    p: parameters\n
        p[0]: amp\n
        p[1]: sigma\n
        p[2]: peak position\n
        p[3]: shift term 
    """
    return p[0] *exp( -( (x-p[2]) /p[1] )**2 /2) + p[3]

def derivativeGaussianFamily (x, *p)->ndarray:
    """
    x: array like, shape (n,)\n
    p: parameters\n
        p[0]: amp\n
        p[1]: sigma\n
        p[2]: peak position\n
    """ 
    if p[1] != 0. :
        return -p[0] / p[1]**2 *(x-p[2]) *exp( -( (x-p[2]) /p[1] )**2 /2)
    else :
        return zeros(len(x))


def ErfShifter(amp_erf,gatetime,sigma)->float:
    if sigma != 0. :
        return amp_erf*exp(-(gatetime**2)/(8*sigma**2))
    else :
        return 0  

def ErfAmplifier(Amp,gatetime,sigma)->float:
    amp = sqrt(2*pi*sigma**2)*erf(gatetime/(sqrt(8)*sigma))-gatetime*exp(-(gatetime**2)/(8*sigma**2))
    if sigma != 0. :
        return Amp*sqrt(2*pi*sigma**2)*erf(gatetime/(sqrt(8)*sigma))/amp
    else :
        return 0 


def gaussianFunc (x, *p)->ndarray:
    """
    x: array like, shape (n,)\n
    p: parameters\n
        p[0]: amp\n
        p[1]: sigma\n
        p[2]: peak position\n
    """
    return p[0] *exp( -( (x-p[2]) /p[1] )**2 /2)

def derivativeGaussianFunc (x, *p)->ndarray:
    """
    return derivative Gaussian
    x: array like, shape (n,) \n
    p: parameters \n
        p[0]: amp \n
        p[1]: sigma \n
        p[2]: peak position \n 
    """

    if p[1] != 0. :
        return -p[0] / p[1]**2 *(x-p[2]) *exp( -( (x-p[2]) /p[1] )**2 /2)
    else :
        return zeros(len(x))


# 1223 append Hermite waveform
# ref: PHYSICAL REVIEW B 68, 224518 (2003)

def HermiteFunc(x, *p)->ndarray:
    """
    x: array like, shape (n,)\n
    p: parameters\n
        p[0]: A (1.67 recommended)\n
        p[1]: alpha (4 recommended)\n
        p[2]: beta (4 recommended)\n
        p[3]: peak position (half gate time recommended)
    """
    if len(x) != 0:
        tg = x[-1]-x[0]
        # given in the reference
        sigma = tg/(2*p[1])

        return (1-p[2]*((x-p[3])/(p[1]*sigma))**2)*p[0]*exp(-(x-p[3])**2/(2*sigma**2))
    else:
        return zeros(len(x))

def derivativeHermiteFunc (x, *p)->ndarray:
    """
    return derivative Hermite
    x: array like, shape (n,) \n
    p: parameters \n
        p[0]: A (1.67 recommended)\n
        p[1]: alpha (4 recommended)\n
        p[2]: beta (4 recommended)\n 
        p[3]: peak position (half gate time recommended)
    """
    if len(x) != 0 :
        tg = x[-1]-x[0]
        # given in the reference
        sigma = tg/(2*p[1])
        return (p[0]*((x-p[3])/(sigma**2))*(-2*p[2]/p[1]**2+(1-p[2]*((x-p[3])/(p[1]*sigma))**2))*exp(-((x-p[3])**2)/(2*sigma**2)))
    else :
        return zeros(len(x))

# 0504 add Tangential
def TangentialFunc(x, *p)->ndarray:
    """
    return tangential function
    x: array like, shape (n,) \n
    p: parameters \n
        p[0]: amp\n
        p[1]: sigma\n
        p[2]: peak position\n
    """
    if len(x) != 0:
        tg = x[-1]-x[0]
        return p[0]*(tanh(x/p[1])-tanh((x-tg)/p[1]))
    else:
        return zeros(len(x))

def derivativeTangentialFunc(x, *p)->ndarray:
    """
    return derivative tangential function
    x: array like, shape (n,) \n
    p: parameters \n
        p[0]: amp\n
        p[1]: sigma\n
        p[2]: peak position\n
    """
    if len(x) != 0:
        tg = x[-1]-x[0]
        return p[0]*(sech(x/p[1])**2-(sech((x-tg)/p[1]))**2)/p[1]
    else:
        return zeros(len(x))




def constFunc (x, *p)->ndarray:
    """
    return constant array
    x: array like, shape (n,) \n
    p[0]: value \n
    """
    return p[0]*ones(len(x))

def rectPulseFunc (x, *p)->ndarray:
    """
    return constant array
    x: array like, shape (n,) \n
    p[0]: amp \n
    p[1]: width \n
    p[2]: start \n
    """
    condition = logical_and(abs(x)>=p[2], abs(x)<=(p[1]+p[2]))

    return where(condition, p[0], 0)

def GERPFunc (x, *p)->ndarray:
    """
    return Gaussian Edge Rectangular Pulse array
    x: array like, shape (n,) \n
    p[0]: amp \n
    p[1]: width \n
    p[2]: start \n
    p[3]: edge width \n
    p[4]: edge sigma \n
    """
    amp = p[0]
    total_width = p[1]
    start_pos = p[2]
    edge_width = p[3]
    peak_width = edge_width*2
    edge_sigma = p[4]

    flat_start = start_pos +edge_width
    flat_width = total_width -peak_width

    flat_end = flat_start +flat_width


    raising_edge_pars = [ amp, edge_sigma, flat_start ]
    gaussUp = where( x<flat_start, gaussianFunc(x, *raising_edge_pars), 0. )
    falling_edge_pars = [ amp, edge_sigma, flat_end ]
    gaussDn = where( x>flat_end, gaussianFunc(x, *falling_edge_pars),0. )

    flat_pars = [ amp, flat_width, flat_start]
    rect_pulse = rectPulseFunc( x, *flat_pars )
    return gaussUp +rect_pulse +gaussDn

def linearFunc (t, *p)->ndarray:
    """
    return constant array
    x: array like, shape (n,) \n
    p[0]: slope \n
    p[1]: intersection \n
    """
    return p[0]*t+p[1]

def DRAGFunc ( t, *p )->ndarray:
    """
    return gaussian -1j*derivative Gaussian\n
    x: array like, shape (n,), the element is complex number \n
    p[0]: amp \n
    p[1]: sigma \n
    p[2]: peak position \n
    p[3]: shift term\n
    p[4]: derivative Gaussian amplitude ratio \n
    """
    gaussParas = (p[0],p[1],p[2],p[3])
    return GaussianFamily( t, *gaussParas ) -1j*p[4]*derivativeGaussianFamily( t, *gaussParas )


# 1223 append DRAG with Hermite wavefor2
def DRAGFunc_Hermite(t, *p )->ndarray:
    """
    return Hermite +1j*derivative Hermite\n
    x: array like, shape (n,), the element is complex number \n
    p[0]: A (1.67 recommended)\n
    p[1]: alpha (4 recommended)\n
    p[2]: beta (4 recommended)\n 
    p[3]: peak position\n
    p[4]: derivative Hermite amplitude ratio \n
    """
    HermiteParas = (p[0],p[1],p[2],p[3])
    return HermiteFunc( t, *HermiteParas ) -1j*p[4]*derivativeHermiteFunc( t, *HermiteParas )

# 0504 add DRAG for tangential
def DRAGFunc_Tangential(t, *p )->ndarray:
    """
    return Tangential +1j*derivative Tangential\n
    x: array like, shape (n,), the element is complex number \n
    p[0]: amp \n
    p[1]: sigma \n
    p[2]: peak position \n
    p[3]: derivative Hermite amplitude ratio \n
    """
    TangParas = (p[0],p[1],p[2],p[3])
    return TangentialFunc( t, *TangParas ) -1j*p[4]*derivativeTangentialFunc( t, *TangParas )


if __name__ == '__main__':
    from numpy import linspace
    import matplotlib.pyplot as plt
    

    x = linspace(0,40,1000)
    p = (1,15,20)
    plt.plot(x,gaussianFunc(x,*p))
    plt.plot(x,derivativeGaussianFunc(x,*p))
    plt.show()


# Numpy
# Typing
from numpy import ndarray
# Numpy array
from numpy import array, append, zeros, ones, where, linspace
# Numpy common math function
from numpy import exp
# Numpy constant
from numpy import pi, logical_and



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
    return gaussian +1j*derivative Gaussian\n
    x: array like, shape (n,), the element is complex number \n
    p[0]: amp \n
    p[1]: sigma \n
    p[2]: peak position \n
    p[3]: derivative Gaussian amplitude ratio \n
    """
    gaussParas = (p[0],p[1],p[2])
    return gaussianFunc( t, *gaussParas )+ 1j*p[3]*derivativeGaussianFunc( t, *gaussParas )

if __name__ == '__main__':
    from numpy import linspace
    import matplotlib.pyplot as plt
    

    x = linspace(0,300,1000)
    p = (1,200,0,30,30/2)
    plt.plot(x,GERPFunc(x,*p))
    plt.show()
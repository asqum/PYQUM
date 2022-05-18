# Numpy
# 
from numpy import linspace, arange
# Numpy array
from numpy import array, append, zeros, ones, where
# Numpy common math function
from numpy import exp, sqrt, arctan2, cos, sin, angle, radians, sign, log, ceil
# Numpy constant
from numpy import pi



def gaussianFunc (t, p):
    """
    p[0]: amp
    p[1]: sigma
    p[2]: peak position
    """

    return p[0] *exp( -( (t-p[2]) /p[1] )**2 /2)
def derivativeGaussianFunc (t, p):
    """
    p[0]: amp
    p[1]: sigma
    p[2]: peak position   
    """

    if p[1] != 0. :
        return -p[0] / p[1]**2 *(t-p[2]) *exp( -( (t-p[2]) /p[1] )**2 /2)
    else :
        return zeros(len(t))
def constFunc (t, p):
    """
    p[0]: amp
    """
    return p[0]*ones(len(t))
def linearFunc (t, p):
    """
    p[0]: slope
    p[1]: intersection
    """
    return p[0]*t+p[1]

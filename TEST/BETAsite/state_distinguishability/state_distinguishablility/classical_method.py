# Numpy
# 
from matplotlib.cbook import flatten
from numpy import linspace, arange, histogram
# Numpy array
from numpy import array, append, mean, sum
# Numpy common math function
from numpy import exp, sqrt, arctan, cos, sin, angle, std
# Numpy constant
from numpy import pi
# Scipy 
from scipy.stats import linregress
from scipy.odr import Model, RealData, ODR

class StateDistinguishability():

    def __init__( self, groundData, otherData ):
        
        self.rawData = {
            "gnd": groundData,
            "other": otherData,
        }
        self.meanPts = mean(otherData, axis=1)
        self.groundPoint = mean(groundData)
        self.ShiftedPts = append(self.meanPts-self.groundPoint,0+0j)

        self.projectedData = {}
        # Histogram
        self.distribution={
            "x":[],
            "count":[],
            "fitted":[]
        }

        self._fitParameters = None
# Vector 
    def get_Vect_projectionline( self ):
        complexVect = sum(self.ShiftedPts)
        return complexVect

# Linear regress method
    def get_Lin_projectionLine( self ):
        res = linregress( self.ShiftedPts.real, self.ShiftedPts.imag )
        return res.slope
# Orthogonal Distance Regression
    def get_ODR_projectionLine( self ):

        linear_model = Model(linear_func)
        mydata = RealData(self.ShiftedPts.real, self.ShiftedPts.imag)
        myodr = ODR(mydata, linear_model, beta0=[self.get_Lin_projectionLine()])
        myoutput = myodr.run()
        myoutput.pprint()
        print(myoutput.beta)            
        return myoutput.beta

    def cal_projectedData( self ):
        
        # Get rotate angle
        angleProjectionLine = arctan(self.get_ODR_projectionLine())
        complexProjectionLine = exp(1j*angleProjectionLine)
        
        for stateType in self.rawData.keys():
            innerProduct = self.rawData[stateType].real*complexProjectionLine.real +self.rawData[stateType].imag *complexProjectionLine.imag
            self.projectedData[stateType]=innerProduct

        return self.projectedData

    def cal_distribution( self ):

        groundDistribution = histogram(self.projectedData["ground"], bins='auto')
        guess = array([ 0.1, midPoint+devData*1.2, devData/2, 0.1, midPoint-devData*1.2, devData/2])
        try:
            popt,pcov=curve_fit( gaussian_func, xAxis, distCount, p0=guess)
            fitSuccess = True
            print("Good fitting", popt)
            self.distribution["fitted"]=gaussian_func(xAxis,popt[0:3])

        distributionData = histogram(self.accData["projected"], bins='auto')
        devData = std(self.accData["projected"])
        xAxis = distributionData[1][1:] +(distributionData[1][1]-distributionData[1][0])/2
        distCount = distributionData[0]/float(len(distributionData[0]))
        midPoint = (xAxis[0]+xAxis[-1])/2

        guess = array([ 0.1, midPoint+devData*1.2, devData/2, 0.1, midPoint-devData*1.2, devData/2])
                                                                                                                            
        self.distribution={
            "x":xAxis,
            "count":distCount,
            "fitted":[],
        }
        try:
            popt,pcov=curve_fit(twoGaussian_func,xAxis, distCount, p0=guess)
            fitSuccess = True
            print("Good fitting", popt)
            self.distribution["fitted"]=gaussian_func(xAxis,popt[0:3])+gaussian_func(xAxis,popt[3:6])
        except:
            fitSuccess = False
            print("Bad fitting")
            self.distribution["fitted"]=gaussian_func(xAxis,guess[0:3])+gaussian_func(xAxis,guess[3:6])


        return self.distribution


# if __name__ == "__main__":
# 	worker_fresp(int(sys.argv[1]),int(sys.argv[2]))
def linear_func(p, x):
   return p*x

def gaussian_func ( x, p):
    # p: amp, mean, sigma
    return p[0]/(p[2]*sqrt(2*pi))*exp( -1./2.*((x-p[1])/p[2])**2 )

def twoGaussian_func (x, *p):
    # p: ex_amp, ex_mean, ex_sigma, g_amp, g_mean, g_sigma
    exPars = (p[0],p[1],p[2])
    if p[1]-p[4]<amin([p[2],p[5]])/10:
        p[4]=p[1]-amin([p[2],p[5]])/10
    gndPars = (p[3],p[4],p[5])
    return gaussian_func(x,exPars)+gaussian_func(x,gndPars)

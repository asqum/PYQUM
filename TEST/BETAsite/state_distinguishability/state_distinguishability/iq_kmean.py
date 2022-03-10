
from cProfile import label
from numpy import array, reshape, mean, transpose
from sklearn.cluster import KMeans



def get_KmeansSklearn( n_clusters, iqComplex )->KMeans:
    data = complex_to_vector(iqComplex, vectorShape="H")
    kmeans = KMeans(n_clusters=n_clusters,tol=1e-4).fit(data)
    return kmeans

def complex_to_vector( complexArray, vectorShape="V" ):
    transArr = array([complexArray.real,complexArray.imag])
    if vectorShape == "V":
        return transArr
    elif "H":
        return transArr.transpose()

def vector_to_complex( vectorArray ):
    vectorArray = vectorArray.transpose()
    complexArray = vectorArray[0]+1j*vectorArray[1]
    return complexArray

def get_projectedIQVector_byTwoPt( projComplex, iqComplex ):
    refPoint = mean(projComplex)
    shiftedIQComplex = iqComplex-refPoint
    relativeProjComplex = projComplex[0]-refPoint
    projectionVector = complex_to_vector(array([relativeProjComplex]),"H")
    shiftedIQVector = complex_to_vector(shiftedIQComplex,"V")
    projectionMatrix = projectionVector.transpose()@projectionVector/abs(relativeProjComplex)**2
    projectedVector = projectionMatrix@shiftedIQVector
    return projectedVector

def get_projectedIQDistance_byTwoPt( projComplex, iqComplex ):
    refPoint = mean(projComplex)
    shiftedIQComplex = iqComplex-refPoint
    relativeProjComplex = projComplex[0]-refPoint
    projectionVector = complex_to_vector(array([relativeProjComplex]),"H")
    shiftedIQVector = complex_to_vector(shiftedIQComplex,"V")
    projectedDistance = projectionVector@shiftedIQVector/abs(relativeProjComplex)
    return projectedDistance[0]

def get_simulationData(measurementPts, excitedProbability, iqPosition, sigma):
    excPts = int(measurementPts*excitedProbability)
    groundProbability = 1-excitedProbability
    groundPts = int(measurementPts*groundProbability)
    gpos=iqPosition[0]
    epos=iqPosition[1]
    g = np.random.normal(gpos.real, sigma, groundPts)+1j*np.random.normal(gpos.imag, sigma, groundPts)
    e = np.random.normal(epos.real, sigma, excPts)+1j*np.random.normal(epos.imag, sigma, excPts)

    iqdata = np.append(g,e)    
    return iqdata

def get_oneShot_kmeanDistance(iqdata):

    km = get_KmeansSklearn(2,iqdata)
    clusterCenter = km.cluster_centers_.transpose()
    clusterCenter = clusterCenter[0]+1j*clusterCenter[1]
    projectedDistance = get_projectedIQDistance_byTwoPt(clusterCenter,iqdata)
    #b = get_projectedIQVector_byTwoPt(clusterCenter,iqdata)
    return projectedDistance

def get_oneshot_plot(iqdata,simIQCenter=None):
    km = get_KmeansSklearn(2,iqdata)
    clusterCenter = vector_to_complex(km.cluster_centers_)
    a = get_projectedIQDistance_byTwoPt(clusterCenter,iqdata)
    plt.figure(1)
    plt.plot( iqdata.real, iqdata.imag, "o", label="Data" )
    plt.plot( clusterCenter.real, clusterCenter.imag, "o", label="KMeans" )
    #if simIQCenter != None:
    simCenter = array(simIQCenter).transpose()
    plt.plot( simCenter.real, simCenter.imag,"ro", label="Simulation" )
    plt.figure(2)
    count, bins, ignored = plt.hist(a, 60, density=True)
    plt.show()
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np


    simCenter = array([0,1])
    measurementPts = 10000
    sigma = 0.2
    get_oneshot_plot(get_simulationData(measurementPts,0.5,simCenter,sigma),simIQCenter=simCenter)
    statisticTest = int(20)
    ProbabilityRange = np.linspace(0.1,0.9,9)
    errorDistanceMean = np.empty(ProbabilityRange.shape[-1])
    errorDistanceSTD = np.empty(ProbabilityRange.shape[-1])
    for i,excitedProbability in enumerate(ProbabilityRange):

        ed = np.empty(statisticTest)
        for j in range(statisticTest):
            km = get_KmeansSklearn(2,get_simulationData(measurementPts,excitedProbability,simCenter,sigma))
            clusterCenter = km.cluster_centers_.transpose()
            clusterCenter = clusterCenter[0]+1j*clusterCenter[1]
            errorDistanceP1 = mean(abs(simCenter.transpose()-clusterCenter))

            clusterCenterP2 = array([clusterCenter[1],clusterCenter[0]])
            errorDistanceP2 = mean(abs(simCenter.transpose()-clusterCenterP2))

            ed[j] = np.min([errorDistanceP1,errorDistanceP2])
        errorDistanceMean[i] = np.mean(ed)
        errorDistanceSTD[i] = np.std(ed)
        #print(simCenter.transpose(),clusterCenter,clusterCenterP2,errorDistance)
    #b = get_projectedIQVector_byTwoPt(clusterCenter,iqdata)

    plt.figure(1)
    plt.errorbar( ProbabilityRange, errorDistanceMean, yerr=errorDistanceSTD, fmt="ro" )

    # plt.plot( clusterCenter.real, clusterCenter.imag, "o", label="KMeans" )
    # simCenter = array(iqPosition).transpose()
    # plt.plot( simCenter[0], simCenter[1],"o", label="Simulation" )
    # #plt.plot( b[0]+mean(clusterCenter).real, b[1]+mean(clusterCenter).imag, "o" )
    # plt.figure(2)
    # count, bins, ignored = plt.hist(a, 60, density=True)
    plt.show()
    
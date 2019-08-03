from multiprocessing import Pool, Queue, Process, Array
from pyqum.instrument.logger import clocker
from pyqum.instrument.analyzer import IQAP
from numpy import array
from pyqum.directive import multiprocessor
from subprocess import Popen, PIPE, STDOUT
from pyqum.instrument.toolbox import cdatasearch, gotocdata

# variables:
A = list(range(10000000*2))

def cube(x):
    return x**3

def f(args):
    # (x,y) = args
    I = A[gotocdata([args[0],0,0,0,2*args[1]],[10000,1,1,1,1000*2])]
    Q = A[gotocdata([args[0],0,0,0,2*args[1]+1],[10000,1,1,1,1000*2])]
    Amp,P = IQAP(I,Q)
    return I, Q, Amp, P
def f_stream(a, b):
    for i in a:
        for j in b:
            yield i, j

def g(a):
    A = list(range(200000000))
    B = [A[gotocdata([x,0,0,0,a],[20000,1,1,1,10000])] for x in range(20000)]
    return B

def collatz_test(n):
    """
    If n is even, return (n/2), else return (3n+1).
    """
    return((n/2) if n%2==0 else (3*n+1))
def chain_length(n):
    """
    Return the length of the collatz chain along
    with the input value `n`.
    """
    if n<=0: return(None)
    cntr, tstint = 0, n
    while tstint!=1:
        cntr+=1
        tstint = collatz_test(tstint)
    return(n, cntr)


def initPool(num):
    print("Initializing pool with ", num,  " processes")

output = Queue()
def square(x, pos, output):
    ans = x**2
    output.put((pos, ans))

def main():
    stage, prev = clocker(0)
    results = [cube(x) for x in range(1,10000)]
    print("Finished processing %s results" %len(results))
    stage, prev = clocker(stage, prev) # Marking time
    # input("Continue?")

    # calling from outside
    multiprocessor.worker_fresp(1000,10000)
    stage, prev = clocker(stage, prev) # Marking time

    # print("Now calling from inside here:")
    # arr  = Array('L', range(1, 10000000))
    # pool = Pool()
    # results = pool.map(f, zip([x//350 for x in range(350000)],[x%350 for x in range(350000)]))
    # IQ = pool.map(f, f_stream(range(10000),range(1000)), 10000) #f_stream(range(1000),range(350)), 35000)
    # pool.close(); pool.join()
    # rI, rQ, rA, rP = [], [], [], []
    # for i,j,k,l in IQ:
    #     rI.append(i); rQ.append(j); rA.append(k); rP.append(l)
    # rI, rQ, rA, rP = array(rI).reshape(10000,1000), array(rQ).reshape(10000,1000), array(rA).reshape(10000,1000), array(rP).reshape(10000,1000)
    # print("Finished processing results of shape %s" %str(rI.shape))
    # stage, prev = clocker(stage, prev) # Marking time
    # input("Continue?")

    # pool = Pool(processes=16)
    # results = pool.map(g, range(1000))
    # pool.close()
    # print("Finished processing results of shape %s" %array(results).shape)
    # stage, prev = clocker(stage, prev) # Marking time
    # input("Continue?")

    # R = []
    # for i in range(10000//600):
    #     processes = [Process(target=square, args=(x, x, output)) for x in range(600)] # max: 600 parallel processes
    #     for p in processes:
    #         p.start()
    #     for p in processes:
    #         p.join()
    #     results = [output.get() for p in processes]
    #     results.sort()
    #     results = [r[1] for r in results]
    #     R += results
    # print("Finished processing %s results" %len(R))
    # stage, prev = clocker(stage, prev) # Marking time

if __name__ == '__main__':
    main()


'''Calibration Suite'''
from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

import copy
from pyqum.instrument.benchtop import RSA5, PSGA, MXA
from pyqum.instrument.modular import AWG
from pyqum.instrument.logger import status_code
from numpy import sin, cos, pi, array, lcm, float64, sum, dot

class IQ_Cal:

    def __init__(self, suppression='LO', IQparams=array([0.,0.,1.,0.,0.]), STEP=array([-0.5,-0.5,0.5,12,12]), ratio=1):
        self.IQparams = IQparams
        self.STEP = STEP
        self.suppression = suppression
        if self.suppression == 'LO':
            self.var = copy.copy(self.IQparams[:2])
            self.step = self.STEP[:2]/(10**(ratio+1))
        elif self.suppression == 'MR':
            self.var = copy.copy(self.IQparams[2:])
            self.step = self.STEP[2:]/(2**(ratio+1))

    def nelder_mead(self, no_improve_thr=10e-6, no_improv_break=10, max_iter=0,
                    alpha=1., gamma=2., rho=-0.5, sigma=0.5, time=0):
        '''
        Pure Python/Numpy implementation of the Nelder-Mead algorithm.
        Reference: https://en.wikipedia.org/wiki/Nelder%E2%80%93Mead_method
        '''
        '''
            @param f (function): function to optimize, must return a scalar score
                and operate over a numpy array of the same dimensions as x_start
            @param x_start (numpy array): initial position
            @param step (float): look-around radius in initial step
            @no_improv_thr,  no_improv_break (float, int): break after no_improv_break iterations with
                an improvement lower than no_improv_thr
            @max_iter (int): always break after this number of iterations.
                Set it to 0 to loop indefinitely.
            @alpha, gamma, rho, sigma (floats): parameters of the algorithm
                (see Wikipedia page for reference)
            return: tuple (best parameter array, best score)
        '''

        index = time%2
        dim = len(self.var)
        "tell AWG to apply DC offset(x) on I & Q"
        AWG_Sinewave(25, self.IQparams)
        "read signal amplitude at LO frequency in and assign it as score"
        MXA.attenuation_mode(mxa, action=['Set','ON'])
        MXA.attenuation(mxa, action=['Set','14dB'])
        power = float((MXA.fpower(mxa, str(5.5 - 0.025*index)+'GHz')).split('dBm')[0]) - index*float((MXA.fpower(mxa, str(5.5 + 0.025*index)+'GHz')).split('dBm')[0])
        prev_best = power
        no_improv = 0
        res = [[self.var, prev_best]]

        for i in range(dim):
            x = copy.copy(self.var)
            x[i] = x[i] + self.step[i]
            # print('applying %s' %x)
            "tell AWG to apply DC offset(x) on I & Q"
            # params(IQparams, index) = x
            if self.suppression == 'LO': self.IQparams[:2] = x
            elif self.suppression == 'MR': self.IQparams[2:] = x
            
            AWG_Sinewave(25, self.IQparams)
            "read signal amplitude at LO frequency in and assign it as score"
            power = float((MXA.fpower(mxa, str(5.5 - 0.025*index)+'GHz')).split('dBm')[0]) - index*float((MXA.fpower(mxa, str(5.5 + 0.025*index)+'GHz')).split('dBm')[0])
            score = power
            res.append([x, score])

        # simplex iter
        iters = 0
        while 1:
            # order
            res.sort(key=lambda x: x[1])
            if self.suppression == 'LO': self.IQparams[:2] = res[0][0]
            elif self.suppression == 'MR': self.IQparams[2:] = res[0][0]
            print(Fore.YELLOW + "\rProgress time#%s: %s" %(time, self.IQparams), end='\r', flush=True)
            best = res[0][1]

            # break after max_iter
            if max_iter and iters >= max_iter:
                return res[0]
            iters += 1

            # break after no_improv_break iterations with no improvement
            # print('...best so far:', best)

            # AWG_Sinewave(25, self.IQparams)
            # if float((RSA5.fpower(rsa, str(5.5)+'GHz')).split('dBm')[0]) < -65. and float((RSA5.fpower(rsa, str(5.475)+'GHz')).split('dBm')[0]) < -65.:
            #     return array([self.IQparams, best, 0.])

            

            if best < prev_best - no_improve_thr or best == prev_best:
                no_improv = 0
                prev_best = best
            else:
                no_improv += 1

            if no_improv >= no_improv_break:
                AWG_Sinewave(25, self.IQparams)
                print("Rest at Optimized IQ Settings: %s" %self.IQparams)
                return array([self.IQparams, best]) # Optimized parameters

            # centroid
            x0 = [0.] * dim
            for tup in res[:-1]:
                for i, c in enumerate(tup[0]):
                    x0[i] += c / (len(res)-1)

            # reflection
            xr = x0 + alpha*(x0 - res[-1][0])
            if self.suppression == 'LO': self.IQparams[:2] = xr
            elif self.suppression == 'MR': self.IQparams[2:] = xr
            "tell AWG to apply DC offset(x) on I & Q"
            AWG_Sinewave(25, self.IQparams)
            "read signal amplitude at LO frequency in and assign it as score"
            power = float((MXA.fpower(mxa, str(5.5 - 0.025*index)+'GHz')).split('dBm')[0]) - index*float((MXA.fpower(mxa, str(5.5 + 0.025*index)+'GHz')).split('dBm')[0])
            # print('Power at 5.475GHz = %s' %float((MXA.fpower(mxa, '5.475GHz')).split('dBm')[0]))
            # print('Power at 5.5GHz = %s' %float((MXA.fpower(mxa, '5.5GHz')).split('dBm')[0]))
            # print('Power at 5.525GHz = %s' %float((MXA.fpower(mxa, '5.525GHz')).split('dBm')[0]))
            # input('hello')
            rscore = power
            if res[0][1] <= rscore < res[-2][1]:
                del res[-1]
                res.append([xr, rscore])
                continue

            # expansion
            if rscore < res[0][1]:
                xe = x0 + gamma*(x0 - res[-1][0])
                if self.suppression == 'LO': self.IQparams[:2] = xe
                elif self.suppression == 'MR': self.IQparams[2:] = xe
                "tell AWG to apply DC offset(x) on I & Q"
                AWG_Sinewave(25, self.IQparams)

                "read signal amplitude at LO frequency in and assign it as score"
                power = float((MXA.fpower(mxa, str(5.5 - 0.025*index)+'GHz')).split('dBm')[0]) - index*float((MXA.fpower(mxa, str(5.5 + 0.025*index)+'GHz')).split('dBm')[0])
                escore = power
                if escore < rscore:
                    del res[-1]
                    res.append([xe, escore])
                    continue
                else:
                    del res[-1]
                    res.append([xr, rscore])
                    continue

            # contraction
            xc = x0 + rho*(x0 - res[-1][0])
            if self.suppression == 'LO': self.IQparams[:2] = xc
            elif self.suppression == 'MR': self.IQparams[2:] = xc
            "tell AWG to apply DC offset(x) on I & Q"
            AWG_Sinewave(25, self.IQparams)

            "read signal amplitude at LO frequency in and assign it as score"
            power = float((MXA.fpower(mxa, str(5.5 - 0.025*index)+'GHz')).split('dBm')[0]) - index*float((MXA.fpower(mxa, str(5.5 + 0.025*index)+'GHz')).split('dBm')[0])
            cscore = power
            if cscore < res[-1][1]:
                del res[-1]
                res.append([xc, cscore])
                continue

            # reduction
            x1 = res[0][0]
            nres = []
            for tup in res:
                redx = x1 + sigma*(tup[0] - x1)
                if self.suppression == 'LO': self.IQparams[:2] = redx
                elif self.suppression == 'MR': self.IQparams[2:] = redx
                "tell AWG to apply DC offset(x) on I & Q"
                AWG_Sinewave(25, self.IQparams)

                "read signal amplitude at LO frequency in and assign it as score"
                power = float((MXA.fpower(mxa, str(5.5 - 0.025*index)+'GHz')).split('dBm')[0]) - index*float((MXA.fpower(mxa, str(5.5 + 0.025*index)+'GHz')).split('dBm')[0])
                score = power
                nres.append([redx, score])
            res = nres
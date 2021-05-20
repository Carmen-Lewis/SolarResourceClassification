# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 16:13:44 2020

@author: Carmen Lewis (carmen@solarXY.org)

Function for calculating the fast Fourier Transform 
and sample standard deviation.
"""

import numpy as np
import scipy.fftpack
from statistics import stdev 

Ts = 60.0               #sampling time or interval
Fs = 1.0/Ts             #sampling rate or frequency
t = np.arange(0,1,Ts)   #time vector
n = 15
k = np.arange(n)
T = n/Fs                #period
frq = k/T               #two-sided frequency range
frq = frq[:int(n/2)]    #one-side frequency range

def fft_sd(D):
    if len(D) == 15:
        #fast fourier transform of 15-minute period
        Y_ghi = scipy.fftpack.fft(D)
        Y_ghi = Y_ghi[:int(n/2)]
        powr = ((abs(Y_ghi))**2)[1:]
        frq2 = frq[1:]
        
        #calculate the first derivative
        dy=np.diff(powr,1)
        dx=np.diff(frq2,1)
        yfirst=dy/dx
        xfirst=0.5*(frq2[:-1]+frq2[1:])
                    
        #calculate the second derivative
        dyfirst=np.diff(yfirst,1)
        dxfirst=np.diff(xfirst,1)
        ysecond=dyfirst/dxfirst
                    
        #Calculate the sample standard deviation 
        #(measure of statistical dispersion)
        SD = stdev(ysecond)/1000**2

    else:
        SD = np.nan

    return SD
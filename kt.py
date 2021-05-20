# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 16:15:56 2020

@author: Carmen Lewis (carmen@solarXY.org)

Function for calculating the clearness index

Liu, B.Y.; Jordan, R.C. "The interrelationship and characteristic distribution 
of direct, diffuse and total solar radiation," Solar Energy vol.4, pp.1–19, 1960. 
G.M. Lohmann, “Irradiance variability quantification and small-scale averaging 
in space and time: A short review,” Atmosphere vol.9, no.264, p.264, 2018. 
doi:10.3390/atmos9070264
"""

import numpy as np
from pvlib.location import Location

def kt(df15):

    #solar zenith angle from degrees to radians
    df15['thetaRad'] = df15['theta'].astype(float).apply(np.deg2rad)
    
    #solar constant
    S = 1367.1
    
    df15['DOY'] = df15.index.dayofyear
    df15['x'] = ((360/365)*(df15['DOY']-81)).astype(float).apply(np.deg2rad)
    
    #calculate the extraterrestrial irradiance
    df15['F0'] = S*(1.00011 + 0.034221*np.cos(df15['x']) + 0.00128*np.sin(df15['x']) \
                  - 0.000719*np.cos(2*df15['x']) + 0.000077*np.sin(2*df15['x']))
    
    #calculate the clearness index
    df15['kt'] = df15['SWD']/(df15['F0']*np.cos(df15['thetaRad']))
    
    #determine overcast periods
    df15.loc[(df15['kt'] > 0) & (df15['kt'] <= 0.35) & (df15['theta'] <= 85), 'Overcast'] = 1

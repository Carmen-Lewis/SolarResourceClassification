# -*- coding: utf-8 -*-
"""
Created on Thu May 20 14:15:48 2021

@author: Carmen Lewis (carmen@solarXY.org)

Plot functions for 15-minute period solar resource classification method 
based on frequency domain theory and the clearness index.
"""

import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
import datetime as dt
from calendar import monthrange

#colour range
cl = ['#9e0142','#d53e4f','#f46d43','#fdae61', '#abdda4', '#66c2a5', '#3288bd', '#5e4fa2']

def ten_day_plot(df, YEAR, month, day_first):
    
    rcParams['figure.figsize'] = 20, 2
    #fig, ax = plt.subplots(1, 1)
    fig, ax = plt.subplots(1, 10, sharey=True)
    
    #calculate number of days in month
    n_day_M = monthrange(YEAR, month)[1]
    
    for i in range(0, 10):
        if(day_first + i > n_day_M):
            month = month + 1
            day_first = 1
            
        df1 = df.loc[(df['DateTime'].dt.month==month) & (df['DateTime'].dt.day==(day_first+i))]
        
        ax[i].set_xlabel(df1['DateTime'].dt.date.values[0])
        ax[i].plot(df1['GHI'], lw=0.8, color='black')
        ax[i].set_xlim(dt.datetime(YEAR, month, (day_first+i), 5, 30, 0), dt.datetime(YEAR, month, (day_first+i), 20, 00, 0))
        
        ax[i].plot(df1['DateTime'], df1['GHI']*df1['Clear'], lw=2.5, color=cl[0], label='Clear')
        ax[i].plot(df1['GHI']*df1['PartiallyClear'], lw=1.5, color=cl[2], label='Partially Clear')
        ax[i].plot(df1['GHI']*df1['PartiallyCloudy'], lw=1.5, color=cl[4], label='Partially Cloudy')
        ax[i].plot(df1['GHI']*df1['Cloudy'], lw=1.5, color=cl[5], label='Cloudy')
        ax[i].plot(df1['GHI']*df1['Overcast'], lw=1.5, color=cl[7], label='Overcast')
        
        ax[i].grid(False)
        ax[i].tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

     
    ax[0].set_ylabel('GHI')
    fig.subplots_adjust(wspace=0, hspace=0)

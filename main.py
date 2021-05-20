# -*- coding: utf-8 -*-
"""
Created on Tue May 18 15:11:36 2021
@author: Carmen Lewis (carmen@solarXY.org)

Main function for 15-minute period solar resource classification method 
based on frequency domain theory and the clearness index.

C. Lewis, J.M. Strauss, A.J. Rix, "A Solar Resource Classification Algorithm 
for Global Horizontal Irradiance Time Series Based on Frequency Domain Analysis,"" 
Journal of Renewable and Sustainable Energy, vol.13, no.3, June 2021. 
doi:10.1063/5.0045032
"""

import fft_sd
import kt

import pandas as pd

from pvlib.location import Location
from pvlib.solarposition import spa_python

import datetime as dt
import sys

import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

#set location parameters
LOCATION = Location(-33.92810059, 18.86540031,'Etc/GMT-2', 119, 'SUN')

YEAR = 2020

def main():
    
    SUN()
    
"""
Classification function for Stellenbosch University (SUN) data from SAURAN
(https://sauran.ac.za/)
"""
def SUN():

    #date format
    dateparse = lambda x: dt.datetime.strptime(x, '%d/%m/%Y %H:%M:%S')
    #read csv
    filepath = 'Data/%s %s.csv' %(LOCATION.name, YEAR)
    try:
        df = pd.read_csv(filepath, skiprows=[0,2,3], parse_dates=['TmStamp'], 
                         index_col='TmStamp', date_parser=dateparse)
    except IOError:
        print('Unable to load', filepath)
        sys.exit()
        
    #set columns names to universal names    
    df['GHI'] = df['SunWM_Avg']     #global horizontal irradiance in W/m^2
    df['P'] = df['BP_mB_Avg']*100   #barometric pressure in Pa
    df['T'] = df['AirTC_Avg']       #temperature in °C
        
    #clean dataset of possible duplicates
    df = df.dropna(subset=['GHI'])
    
    #add missing timestamps to dataframe
    r = pd.date_range(start='%s-01-01 00:00' %YEAR, end='%s-12-31 23:59' %YEAR, freq='min')
    df = df.reindex(r).reset_index().set_index('index')
    df['DateTime'] = df.index
    
    #print(df.head())
    classification(df)

def classification(df):

    #Calculate the solar zenith angle, theta and shift to correct timezone
    df['theta'] = spa_python(df.index, LOCATION.latitude, LOCATION.longitude, \
                    altitude=LOCATION.altitude, pressure=df['P'], \
                    temperature=df['T'], atmos_refract=None).zenith.shift(120)
        
    #Discrete First Difference Filter of GHI
    df['GHI_D'] = df['GHI'].diff()
        
    #Drop minutes where theta > 80
    df['GHI_D'] = df['GHI_D'].loc[df['theta'] <= 80]
    
    #Create a df indexed only for every period
    df15 = df.resample('15min').mean()
    df15['DateTime'] = df15.index
    
    #Retreive the calculated standard deviation (SD) for every period
    df15['SD'] = df['GHI_D'].groupby(pd.Grouper(freq='15Min')).apply(fft_sd.fft_sd)
    
    #Calculate Clearness Index for classification overcast
    kt.kt(df15)
    
    #Set classification thresholds
    df15.loc[(df15['SD'] <= 50) & (df15['Overcast'] != 1), 'Clear'] = 1
    df15.loc[(df15['SD'] > 50) & (df15['SD'] <= 500) & (df15['Overcast'] != 1), 'PartiallyClear'] = 1
    df15.loc[(df15['SD'] > 500) & (df15['SD'] <= 2000) & (df15['Overcast'] != 1), 'PartiallyCloudy'] = 1
    df15.loc[(df15['SD'] > 2000) & (df15['Overcast'] != 1), 'Cloudy'] = 1
    
    #upsampling from 15 minute period df to minute averaged df
    forwardfill_period(df, df15)

    #testPlot(df)
        
def testPlot(df):
    
    plt.plot(df['GHI'])
    plt.plot(df['theta'])

main()
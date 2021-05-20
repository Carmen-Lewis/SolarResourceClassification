# -*- coding: utf-8 -*-
"""
Created on Tue May 18 15:11:36 2021
@author: Carmen Lewis (carmen@solarXY.org)

Main function for 15-minute period solar resource classification method 
based on frequency domain theory and the clearness index.

C. Lewis, J.M. Strauss, A.J. Rix, "A Solar Resource Classification Algorithm 
for Global Horizontal Irradiance Time Series Based on Frequency Domain Analysis," 
Journal of Renewable and Sustainable Energy, vol.13, no.3, June 2021. 
doi:10.1063/5.0045032
"""

import fft_sd
import kt
import plots

import pandas as pd

from pvlib.location import Location
from pvlib.solarposition import spa_python

import datetime as dt
import sys

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

#set location parameters
#LOCATION = Location(-33.92810059, 18.86540031,'Etc/GMT+2', 119, 'SUN')
LOCATION = Location(-30.6667, 23.9930,'Etc/GMT+2', 1287, 'DAA')

#set filepath
#FILEPATH = 'Data/SUN 2020.csv'
FILEPATH = 'Data/DAA_radiation_2020-01.tab'

#set datasource, either BSRN or SAURAN
DATASOURCE = 'BSRN'

#set date for plot
YEAR = 2020
MONTH = 1
DAY_F = 1

def classification():
    
    if(DATASOURCE == 'SAURAN'):
        #date format
        dateparse = lambda x: dt.datetime.strptime(x, '%d/%m/%Y %H:%M:%S')
        #read csv
        try:
            df = pd.read_csv(FILEPATH, skiprows=[0,2,3], parse_dates=['TmStamp'], 
                             index_col='TmStamp', date_parser=dateparse)
            
            #set columns names to universal names 
            df.rename(columns = {'SunWM_Avg':'GHI', 'AirTC_Avg':'T'}, inplace = True) 
            df['P'] = df['BP_mB_Avg']*100   #barometric pressure in Pa

        except IOError:
            print('Unable to load', FILEPATH)
            sys.exit()
    elif(DATASOURCE == 'BSRN'):
        #date format
        dateparse = lambda x: dt.datetime.strptime(x, '%Y-%m-%dT%H:%M')
        #read csv
        try:
            df = pd.read_csv(FILEPATH, skiprows = 31, sep='\t', 
                             parse_dates=['Date/Time'], index_col = 'Date/Time', 
                             date_parser=dateparse).tz_localize(LOCATION.tz).tz_convert('UTC').tz_localize(None)
            
            #set columns names to universal names
            df.rename(columns = {'SWD [W/m**2]':'GHI', 'PoPoPoPo [hPa]':'P', 
                                 'T2 [°C]':'T'}, inplace = True)

        except IOError:
            print('Unable to load', FILEPATH)
            sys.exit()
    else:
        print('Data source %s does not exist' %DATASOURCE)
        sys.exit()

    #clean dataset of possible duplicates
    df = df.dropna(subset=['GHI'])

    #add missing timestamps within range to dataframe
    r = pd.date_range(start='%s' %df.index[0], end='%s' %df.index[-1], freq='min')
    df = df.reindex(r).reset_index().set_index('index')
    df['DateTime'] = df.index

    #Calculate the solar zenith angle, theta and convert series to df
    df1 = spa_python(df.index, LOCATION.latitude, LOCATION.longitude, \
                    altitude=LOCATION.altitude, pressure=df['P'], \
                    temperature=df['T'], atmos_refract=None).zenith.to_frame()
        
    #localize new df to LOCATION timezone, convert to UTC and localize to naive
    df1 = df1.tz_localize(LOCATION.tz).tz_convert('UTC').tz_localize(None)
    #cast new df column to original df
    df['theta'] = df1['zenith']

    #Discrete First Difference Filter of GHI
    df['GHI_D'] = df['GHI'].diff()
        
    #Drop minutes where theta > 85
    df['GHI_D'] = df['GHI_D'].loc[df['theta'] <= 85]
    
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
    df[['Clear', 'PartiallyClear', 'PartiallyCloudy', 'Cloudy', 'Overcast']] = \
        df15[['Clear', 'PartiallyClear', 'PartiallyCloudy', 'Cloudy', 'Overcast']]
    df[['Clear', 'PartiallyClear', 'PartiallyCloudy', 'Cloudy', 'Overcast']] = \
        df[['Clear', 'PartiallyClear', 'PartiallyCloudy', 'Cloudy', 'Overcast']].ffill(limit=14)

    plots.ten_day_plot(df, YEAR, MONTH, DAY_F)
    
if __name__ == "__main__":
    classification()

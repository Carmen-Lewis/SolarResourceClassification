# A Solar Resource Classification Algorithm for Global Horizontal Irradiance Time Series Based on Frequency Domain Analysis 
(DOI: 10.1063/5.0045032) \
A solar resource classification method based on frequency domain theory and the clearness index.

Carmen Lewis, Johann M Strauss, Arnold Johan Rix (Department of Electrical and Electronic Engineering, Stellenbosch University, South Africa)

## Code
This classification method is based on **minute resolution** data. \
May be used for either timezone-naive datasets such as [SAURAN](https://sauran.ac.za/) or timezone-aware datasets such as [BSRN](https://bsrn.awi.de/).

[`main.py`](https://github.com/Carmen-Lewis/SolarResourceClassification/blob/master/main.py): Main function for 15-minute period solar resource classification method.
* Set `LOCATION` parameters (latitude, longitude, timezone, altitude, name) via pvlib.location.Location
* Set `FILEPATH` to .csv directory
* Set `DATASOURCE` to either 'BSRN' or 'SAURAN' to select pre-set date formats for .csv or .tab
* Set `YEAR`, `MONTH`, `DAY_F` for plots

[`fft_sd.py`](https://github.com/Carmen-Lewis/SolarResourceClassification/blob/master/fft_sd.py): Function for calculating the fast Fourier Transform and sample standard deviation.

[`kt.py`](https://github.com/Carmen-Lewis/SolarResourceClassification/blob/master/kt.py): Function for calculating the clearness index.

[`plots.py`](): Plot functions for 15-minute period solar resource classification method.

## Notes
[pvlib](https://github.com/pvlib/pvlib-python) and [pandas](https://pandas.pydata.org/) python libraries are used. Please see library specific links for more information on converting timezones, calculating solar position and general dataframe manipulation.

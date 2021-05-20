# A Solar Resource Classification Algorithm for Global Horizontal Irradiance Time Series Based on Frequency Domain Analysis 
(DOI: 10.1063/5.0045032) \
A solar resource classification method based on frequency domain theory and the clearness index.

Carmen Lewis, Johann M Strauss, Arnold Johan Rix (Department of Electrical and Electronic Engineering, Stellenbosch University, South Africa)

## Code
This classification method is based on **minute resolution** data. \
May be used for either timezone-naive datasets such as [SAURAN](https://sauran.ac.za/) or timezone-aware datasets such as [BSRN](https://bsrn.awi.de/).

[`main.py`](main.py): Main function for 15-minute period solar resource classification method.
* Set `LOCATION` parameters (latitude, longitude, timezone, altitude, name) via pvlib.location.Location
* Set `FILEPATH` to .csv directory
* Set `DATASOURCE` to either 'BSRN' or 'SAURAN' to select pre-set date formats for .csv or .tab
* Set `YEAR`, `MONTH`, `DAY_F` for plots

[`fft_sd.py`](fft_sd.py): Function for calculating the fast Fourier Transform and sample standard deviation.

[`kt.py`](kt.py): Function for calculating the clearness index.

[`plots.py`](plots.py): Plot functions for 15-minute period solar resource classification method.

## Notes
[pvlib](https://github.com/pvlib/pvlib-python) and [pandas](https://pandas.pydata.org/) python libraries are used. Please see library specific links for more information on converting timezones, calculating solar position and general dataframe manipulation.

## Output Examples
### Stellenbosch University, Western Cape, South Africa (SAURAN)
<img src="output_figures/2020-2-1_SUN.png" alt="2020-02-21 Location SUN"/>
<img src="output_figures/2020-6-5_SUN.png" alt="2020-06-05 Location SUN"/>

### De Aar, Northern Cape, South Africa (BSRN)
<img src="output_figures/2020-1-1_DAA.png" alt="2020-01-01 Location SUN"/>
<img src="output_figures/2020-1-15_DAA.png" alt="2020-01-15 Location SUN"/>

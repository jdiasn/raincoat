# -*- coding: utf-8 -*-
#%matplotlib inline

import netCDF4 as nc
from netCDF4 import Dataset
import numpy as np
import math
import pandas as pd

def readPars(year, month, day):
	""" This function reads the parsivel netCDF files and
        extracts the desired variables.
        
        Arguments
        ---------
        year
        month
        day
        
        Returns
        -------
		parsDataFrame_parsZe : DataFrame of the Parsivel Reflectivtiy values 
		tPar				 : unixTime from Parsivel
		timesPar			 : converted unixTime to NormalTime
		log10_NPar			 : original Number concentration per diameter class
		zPar				 : original Reflectivity
		vPar				 : original velocity	
		rainratePar			 : original rainrate
    """

	#Parsivel data path
	parsPath = '/data/obs/site/nya/parsivel/l1'
	
	#join date to get data from right folders
	datePath = ('/').join([year,  month, day])
	
	#join date to get right name for file
	strDate = ('').join([year,month,day])
	
	fileName = 'parsivel_nya_'+strDate+'.nc'
	
	parsFile = ('/').join([parsPath, datePath, fileName])

	#Reading the NetCDF File from Parsivel Data
	parsNC = Dataset(parsFile, 'r')

	zPar_raw = parsNC.variables['Z'][:] 				# dB
	tPar_raw = parsNC.variables['time'][:] 				# seconds since 1/1/1970 00:00:00
	vPar_raw = parsNC.variables['v'][:] 				# m/s
	log10_NPar_raw = parsNC.variables['N'][:]			# log10(m-3 mm-1)
	rainratePar_raw = parsNC.variables['rain_rate'][:] 	# mm/h

	#check for type (as some files contained masked arrays)
	if type(tPar_raw) == np.ma.core.MaskedArray: tPar_raw = tPar_raw.data

	#check for valid time values (values above zero) 
	valid_idx = np.where(tPar_raw > 0)[0]#
	
	#and save only valid indices from other values
	tPar = tPar_raw[valid_idx]
	log10_NPar = log10_NPar_raw[:,valid_idx]
	zPar = zPar_raw[valid_idx]
	vPar = vPar_raw[:,valid_idx]
	rainratePar = rainratePar_raw[valid_idx]

	#convert unix time to normal time
	epoch = pd.datetime(1970, 1, 1)
	timesPar = epoch + pd.to_timedelta(tPar,'s')

	# Create a DataFrame to look at the Data and to prepare for plot
	parsDataFrame_parsZe = pd.DataFrame(data=zPar,columns=['Ze'], index=timesPar)
	
	return parsDataFrame_parsZe, tPar, timesPar, log10_NPar, zPar, vPar, rainratePar
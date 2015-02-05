#!/usr/bin/env python

import pandas as pd

## Reads in our cleaned up and merged footfall data.
all_data = pd.read_csv('cleaned_data.csv')

## This function takes a dataframe and two years and then calculates the
## percentage difference in footfall between those two years.
def year_delta(df, year1, year2):
	gp = df.groupby(['BRCYear', 'LocationName'])['InCount'].mean().reset_index()

	df_yr1 = gp.copy()[gp['BRCYear'] == year1]
	df_yr1.rename(columns={'InCount': str(year1) + '_Mean'}, inplace=True)
	del df_yr1['BRCYear']

	df_yr2 = gp.copy()[gp['BRCYear'] == year2]
	df_yr2.rename(columns={'InCount': str(year2) + '_Mean'}, inplace=True)
	del df_yr2['BRCYear']
	
	df_delta = pd.merge(df_yr1, df_yr2, on='LocationName')
	df_delta[str(year2) + '_' + str(year1) + '_Delta'] = ((df_delta[str(year2) + '_Mean'] - df_delta[str(year1) + '_Mean']) / df_delta[str(year1) + '_Mean']) * 100

	return df_delta

## An example of how the year_delta function works.
print ''
print 'Annual footfall percentage change, 2013 vs. 2012'
print ''

delta_2013_2012 = year_delta(all_data, 2012, 2013)
print delta_2013_2012.sort(columns='2013_2012_Delta', ascending=False)
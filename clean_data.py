#!/usr/bin/env python

import glob
import pandas as pd

## Some of the years have 4 digits, some have only 2 digits. This
## function shortens the 4 digit years to 2 digits.
def fix_year(year):
	if len(year) > 8:
		year = year[:6] + year[-2:]
	return year

## Loads in all of the .csv files with the data in.
footfall_files = glob.glob('new_data/[0-9].csv')

## Reads the first .csv file into a Pandas dataframe, gets the column names
## and stores them for later and adds our first dataframe to a list.
df_1 = pd.read_csv(footfall_files[0])
col_names = df_1.columns.values
df_list = [df_1]

## Reads through the rest of the .csv files, sets the column names to the 
## same subset as the first dataframe and appends them to the list.
for f in footfall_files[1:]:
	df = pd.read_csv(f)
	df = df[col_names]
	df_list.append(df)

## Joins all of the dataframes together.
all_data = pd.concat(df_list, ignore_index=True)

## Strips off spaces from the end of some of the street names.
all_data['LocationName'] = all_data['LocationName'].str.rstrip()

## Shortens the 4 digit years to 2 digits.
all_data['Date'] = all_data['Date'].map(fix_year)

## Creates a new column with the day and month, e.g. 31/01.
all_data['BRCDayMonth'] = all_data['Date'].str[:-3]

## Creates a new column with just the date in the month.
all_data['BRCDayInMonth'] = all_data['Date'].str[:2]

## Writes the cleaned data to a new .csv file.
all_data.to_csv('cleaned_data.csv')
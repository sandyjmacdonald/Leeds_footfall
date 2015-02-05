#!/usr/bin/env python

import glob
import pandas as pd

## Calculates what quarter a given week is in.
def get_quarter(week):
	if week < 14:
		quarter = 1
	elif 13 < week < 27:
		quarter = 2
	elif 26 < week < 40:
		quarter = 3
	elif week > 39:
		quarter = 4
	return quarter

## Reads in the .csv files.
footfall_files = glob.glob('old_data/*.csv')

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

## Renames the columns to be consistent with the newer data.
all_data.rename(columns={'WeekDay': 'Weekday', 
						 'Count': 'InCount', 
						 'WeekNum': 'BRCWeek', 
						 'Month': 'BRCMonthName', 
						 'Year': 'BRCYear'}, 
						 inplace=True)

## Gets the hour into a format consistent with the newer data.
all_data['Hour'] = all_data['Hour'].str[:2].astype(int)

## Adds a new column with the quarter in.
all_data['BRCQuarter'] = all_data['BRCWeek'].map(get_quarter)

## Strips off spaces from the end of some of the street names.
all_data['LocationName'] = all_data['LocationName'].str.rstrip()

## Writes all of the data to a new .csv file.
all_data.to_csv('new_data/7.csv')
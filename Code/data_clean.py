"""Script used to clean raw data file. Combines data/time to a single column,
adds appropriate headers, replaces missing values/cells with zeros with NAN 
so that there is uniformity."""

import pandas as pd
import numpy as np
from datetime import timedelta




# Import csv file with proper datetime format and approriate header
df = pd.read_csv("Raw_Data/TDR_data_2.csv", parse_dates={'datetime': [0, 1]},
                 header = [0, 1, 3])

# Fix datetime so that midnight displays as 0:00 on the following day
df['datetime_zero'] = df['datetime'].str.replace('24:00:00', '0:00')
df['datetime_er'] = pd.to_datetime(df['datetime_zero'], format='%d/%m/%Y %H:%M')
selrow = df['datetime'].str.contains('24:00')
df['datetime_obj'] = df['datetime_er'] + selrow * timedelta(days=1)
df['datetime'] = df['datetime_obj']
df = df.drop(['datetime_zero', 'datetime_er', 'datetime_obj'], axis=1)

# Uniformity in missing values
df = df.replace(['0', '-'], np.nan)

# Export to csv
df.to_csv("Clean_Data/TDR_data_clean.csv", index = False,
                date_format='%Y-%m-%d %H:%M')


"""Plot basic time series, faceted by treatment """

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from dtaidistance import dtw



# Import csv file with proper datetime format
df = pd.read_csv("Clean_Data/Good_Sensors_Only_VWC.csv", parse_dates={'date_time': [0]}, dayfirst = True)

# Edit column header names to enable splitting later on
df.columns = (df.columns.str.replace(' ', '_').str.replace('(', '')
              .str.replace(')', '') .str.replace(',', '').str.replace('\'', '')
              .str.replace('Interface', '').str.replace('Sensor_', ''))

df = df.set_index('date_time')

# We can resample our data using this function (H is for Hour, W is for weekly...)
hourly = df.resample('H').mean()

# Rolling mean?

"""Correlation matrix"""
corr = df.corr()
sns.set(style="white")
# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))
# Generate a custom diverging colormap
cmap = sns.diverging_palette(150, 275, sep=20, as_cmap=True)
# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1.0, center=0.5,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})


"""Dynamic Time Warping"""
#
#series = df.values
#ds = dtw.distance_matrix_fast(series)

"""Plot basic time series, faceted by treatment """

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.pylab as pylab
import seaborn as sns

# Import csv files with proper datetime format
soil_df = pd.read_csv("Clean_Data/Good_Sensors_Only_VWC.csv", parse_dates={'date_time': [0]}, dayfirst = True)
irr_df = pd.read_csv("Clean_Data/Irrigation.csv", parse_dates={'date_time': [0]}, dayfirst = True)
stem_df = pd.read_csv("Clean_Data/SWP_Long.csv", parse_dates={'date_time': [0]}, dayfirst = True) 

# Edit column header names to enable splitting later on
soil_df.columns = (soil_df.columns.str.replace(' ', '_').str.replace('(', '')
                   .str.replace(')', '') .str.replace(',', '').str.replace('\'', '')
                   .str.replace('Interface', '').str.replace('Sensor_', ''))

# Start and finish (needed for x-limits)
start = soil_df.date_time.min()
finish = soil_df.date_time.max()
months = mdates.MonthLocator()

# Melt dataframe to long format. Easier for plotting.
soil_df = pd.melt(soil_df, id_vars = 'date_time')
irr_df = pd.melt(irr_df, id_vars = 'date_time')
stem_df = pd.melt(stem_df, id_vars = 'date_time')


# Multiply SWP values by 100 so that they appear on plot
stem_df['value'] = stem_df['value']*-10

# Remove values that are totally illogical (e.g., more than 100%)
soil_df = soil_df[soil_df.value < 100]

# Separate 'variable' column into components
soil_df['Area'], soil_df['Variable'], soil_df['Sensor'] = soil_df['variable'].str.split('_').str

# Add columns to SWP and Irrigation dataframes so that they match soil data
irr_df['Area'] = irr_df['variable']
irr_df ['Variable'] = 'Irr'
irr_df ['Sensor'] = 4
stem_df['Area'] = stem_df['variable']
stem_df ['Variable'] = 'SWP'
stem_df ['Sensor'] = 5

# Stack dataframes
frames = [soil_df, irr_df, stem_df]
df = pd.concat(frames)


# Create facet plot using seaborn
#sns.set_style("whitegrid")
g = sns.FacetGrid(df, col="Area", hue="Sensor", col_wrap=2, palette="Set1",)
g.map(plt.plot, "date_time", "value", linewidth=0.5) 
g.add_legend() 
g.set_axis_labels("Time", "VWC") 
g.set_titles("Treatment {col_name}") 
g.fig.subplots_adjust(wspace=.05, hspace=.3)
# title
new_title = 'Variable'
g._legend.set_title(new_title)
# replace labels
new_labels = ['Sensor 1', 'Sensor 2', 'Sensor 3', 'Irrigation', 'SWP']
for t, l in zip(g._legend.texts, new_labels): t.set_text(l)

# Adjust axis tiks
for ax in g.axes.flatten():
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=6)
    _ = plt.setp(ax.get_xticklabels(), visible=True)
    ax.grid(True)
    ax.set_xticklabels(ax.get_xticklabels(),rotation=30) 
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
    
    ax.set_xlim(left = start)
    ax.set_ylim(0, 50)
    ax.set_yticks(range(0, 51, 10))
    ax.title.set_position([.5, .5])


    

    
plt.show()
plt.savefig("Output/facet.pdf")


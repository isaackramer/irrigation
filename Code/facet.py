"""Plot basic time series, faceted by treatment """

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.pylab as pylab
import seaborn as sns

# Import csv file with proper datetime format
df = pd.read_csv("Clean_Data/TDR_data_clean_VWC.csv", parse_dates={'date_time': [0]}, dayfirst = True)

# Edit column header names to enable splitting later on
df.columns = (df.columns.str.replace(' ', '_').str.replace('(', '')
              .str.replace(')', '') .str.replace(',', '').str.replace('\'', '')
              .str.replace('Interface', '').str.replace('Sensor_', ''))

# Start and finish (needed for x-limits)
start = df.date_time.min()
finish = df.date_time.max()
months = mdates.MonthLocator()

# Melt dataframe to long format. Easier for plutting.
df = pd.melt(df, id_vars = 'date_time')

# Remove values that are totally illogical (e.g., more than 100%)
df = df[df.value < 100]

# Separate 'variable' column into components
df['Area'], df['Variable'], df['Sensor'] = df['variable'].str.split('_').str


# Create facet plot using seaborn
#sns.set_style("whitegrid")

g = sns.FacetGrid(df, col="Area", hue="Sensor", col_wrap=2, palette="Set1",)
g.map(plt.plot, "date_time", "value", linewidth=0.5) 
g.add_legend() 
g.set_axis_labels("Time", "VWC") 
g.set_titles("Treatment {col_name}") 
g.fig.subplots_adjust(wspace=.05, hspace=.3)

# Adjust axis tiks
for ax in g.axes.flatten():
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=6)
    _ = plt.setp(ax.get_xticklabels(), visible=True)
    ax.set_xticklabels(labels, rotation=30)
    ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
    ax.set_xlim(left = start)
    ax.set_ylim(0, 50)
    ax.set_yticks(range(0, 51, 10))
    ax.title.set_position([.5, .5])


    

    
plt.show()
plt.savefig("Output/facet.pdf")


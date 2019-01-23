import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.pylab as pylab
import seaborn as sns

# Import csv files with proper datetime format
soil_df = pd.read_csv("Clean_Data/Good_Sensors_Only_VWC.csv", parse_dates={'date_time': [0]}, dayfirst = True)
stem_df = pd.read_csv("Clean_Data/SWP_by_Sensor.csv", parse_dates={'date_time': [0]}, dayfirst = True) 


# Edit column header names to enable splitting later on
soil_df.columns = (soil_df.columns.str.replace(' ', '_').str.replace('(', '')
                   .str.replace(')', '') .str.replace(',', '').str.replace('\'', '')
                   .str.replace('Interface', '').str.replace('Sensor_', ''))

# Resample for daily average
soil_df = soil_df.set_index('date_time')
soil_df = soil_df.resample('D').mean()
soil_df['date_time'] = soil_df.index


# Select dates that SWP measurement was done on
myDates = ['2018-05-23', '2018-05-30', '2018-06-06', '2018-06-13',
           '2018-06-20', '2018-06-27', '2018-07-04', '2018-07-11',
           '2018-07-18', '2018-07-25', '2018-07-31']
soil_df = soil_df[soil_df.index.isin(myDates)]

# Melt dataframe to long format. Easier for plotting.
soil_df = pd.melt(soil_df, id_vars = 'date_time', value_name = "SWC")
stem_df = pd.melt(stem_df, id_vars = 'date_time', value_name = "SWP")

# Merge
soil_df['SWP'] = stem_df['SWP']

# Separate 'variable' column into components
soil_df['Area'], soil_df['Variable'], soil_df['Sensor'] = soil_df['variable'].str.split('_').str

# Create facet plot using seaborn
#sns.set_style("whitegrid")
g = sns.FacetGrid(soil_df, col="Area", hue="Sensor", col_wrap=2, palette="Set1",)
g.map(plt.scatter, "SWC", "SWP", linewidth=0.5) 
g.add_legend() 
g.set_axis_labels("SWC", "SWP") 
g.set_titles("Treatment {col_name}") 
g.fig.subplots_adjust(wspace=.05, hspace=.3)

# title
new_title = 'Sensor'
g._legend.set_title(new_title)

# replace labels
new_labels = ['Sensor 1', 'Sensor 2', 'Sensor 3']
for t, l in zip(g._legend.texts, new_labels): t.set_text(l)


plt.show()
plt.savefig("Output/scatter.pdf")

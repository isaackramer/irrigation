import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

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

# Plot all the data together
plt.figure()
plt.scatter(soil_df.SWC, soil_df.SWP, c='r')
plt.xlabel('Soil Water Content (%)')
plt.ylabel('Stem Water Potential (MPa)')
plt.savefig("Output/SWP_scatter_all.pdf")



# Create facet plot using seaborn
sns.set_style("whitegrid")
plt.figure()
g = sns.lmplot(x="SWC", y="SWP", col="Area", hue="Sensor",
               data=soil_df, col_wrap=2, ci=None)
g.set_axis_labels("Soil Water Content (%)", "Stem Water Potential (MPa)").set(xlim=(10, 26), ylim=(-1.5, 0.0)).fig.subplots_adjust(wspace=.02)
g.add_legend() 
plt.savefig("Output/SWP_facet.pdf")
## title
#new_title = 'Sensor'
#g._legend.set_title(new_title)
#
## replace labels
#new_labels = ['Sensor 1', 'Sensor 2', 'Sensor 3']
#for t, l in zip(g._legend.texts, new_labels): t.set_text(l)


# Linear Models by group
def results_summary_to_dataframe(results):
    '''take the result of an statsmodel results table and transforms it into a dataframe'''
    pvals = results.pvalues
    coeff = results.params
    conf_lower = results.conf_int()[0]
    conf_higher = results.conf_int()[1]
    r_squared = results.rsquared

    results_df = pd.DataFrame({"pvals":pvals,
                               "coeff":coeff,
                               "conf_lower":conf_lower,
                               "conf_higher":conf_higher,
                               "r_squared": r_squared
                                })

    #Reordering...
    results_df = results_df[["r_squared","coeff","pvals","conf_lower","conf_higher"]]
    return results_df

def regress(data, yvar, xvars):
    Y = data[yvar]
    X = data[xvars]
    X['intercept'] = 1.
    model = sm.OLS(Y,X)
    results = model.fit()
    return results_summary_to_dataframe(results)

soil_df = soil_df.dropna()

linear_df = soil_df.groupby('variable').apply(regress, 'SWP', ['SWC'])

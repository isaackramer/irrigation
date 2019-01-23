import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import statsmodels.api as sm
from scipy.signal import argrelextrema



# Import csv files with proper datetime format
soil_df = pd.read_csv("Clean_Data/Good_Sensors_Only_VWC.csv", parse_dates={'date_time': [0]}, dayfirst = True)
sensor_df = pd.read_csv("Clean_Data/sensor_meta.csv")

# Edit column header names to enable splitting later on
soil_df.columns = (soil_df.columns.str.replace(' ', '_').str.replace('(', '')
                   .str.replace(')', '') .str.replace(',', '').str.replace('\'', '')
                   .str.replace('Interface', '').str.replace('Sensor_', ''))

# Resample for daily average
soil_df = soil_df.set_index('date_time')
soil_df = soil_df.resample('1H').mean()

# Get column names
columns = list(soil_df)

# Output data frame
deriv_df = pd.DataFrame(columns=columns, index=np.arange(1))

# Loop over column headers
for sensor in columns:
    # New data frame with only data from that sensor
    df = soil_df.filter([sensor], axis=1)
    
    # Find local maxima
    #df['max'] = df[(df.shift(1) < df) & (df.shift(-1) < df)]
    n=60 # number of points to be checked before and after 
    df['max'] = df.iloc[argrelextrema(df.values, np.greater_equal, order=n)[0]][sensor]
    date_time_low = '2018-05-10 00:00:00'
    date_time_high = '2018-07-11 00:00:00'
    date_time_low = datetime.datetime.strptime(date_time_low, '%Y-%m-%d %H:%M:%S')
    date_time_high = datetime.datetime.strptime(date_time_high, '%Y-%m-%d %H:%M:%S')
    df.loc[df.index < date_time_low, 'max'] = np.nan
    df.loc[df.index > date_time_high, 'max'] = np.nan

    # Initiate column for loss rates
    df['loss_rate'] = np.NaN
    
    # Add column for gradients
    gradient = pd.Series(np.gradient(df[sensor]), df.index, name='gradient')
    df['gradient'] = gradient
    
    
    # Create list with index values when there is a local maximum
    max_index = df.index[df['max'] > 0].tolist()
    
    # Plot
#    plt.figure()
#    plt.scatter(df.index, df['max'], c='g')
#    plt.plot(df.index, df[sensor], c='b')
#    plt.title(sensor)

    # Find rate of loss based on two days after irrigation and store in list
    df['rolling_gradient'] = df['gradient'].rolling(72).mean().shift(-72).dropna()
    df = df[df['max']>0]
    loss_rate = df['rolling_gradient'].mean()
    
    # Store average in dataframe
    deriv_df.at[0, sensor] = loss_rate
    

    
# Transpose dataframe
deriv_df = deriv_df.T
deriv_df.columns = ['loss_rate']
deriv_df["loss_rate"] = pd.to_numeric(deriv_df.loss_rate, errors='coerce')

# Add slopes and soil depth to dataframe
ind = np.arange(len(deriv_df)) 
deriv_df['ind'] = ind
deriv_df = deriv_df.set_index('ind')
deriv_df['slope'] = sensor_df['slope']
deriv_df['soil_depth'] = sensor_df['soil_depth']
deriv_df['aspect'] = sensor_df['aspect']

#plt.scatter(deriv_df.slope, deriv_df.loss_rate, c='r')    
    

# Linear model        
        
X = deriv_df[["slope", "soil_depth"]]
y = deriv_df["loss_rate"]
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit()
predictions = model.predict(X) # make the predictions by the model

# Print out the statistics
print(model.summary())

## Plot results
plt.figure()
plt.scatter(deriv_df.slope, deriv_df.loss_rate, c='r')
plt.xlabel('Slope')
plt.ylabel('Loss Rate')
plt.savefig("Output/slope_loss.pdf")

plt.figure()
plt.scatter(deriv_df.soil_depth, deriv_df.loss_rate, c='b')
plt.xlabel('Soil Depth (cm)')
plt.ylabel('Loss Rate')
plt.savefig("Output/soil_depth_loss.pdf")

#
#plt.show()

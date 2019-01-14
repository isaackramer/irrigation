"""Calculate euclidean distances - between rows / columns"""

import pandas as pd
import numpy as np

# Import csv file with proper datetime format
df = pd.read_csv("Clean_Data/TDR_data_clean_VWC.csv", parse_dates={'date_time': [0]}, dayfirst=True)

# Edit column header names to enable splitting later on
df.columns = (df.columns.str.replace(' ', '_').str.replace('(', '')
              .str.replace(')', '').str.replace(',', '').str.replace('\'', '')
              .str.replace('Interface', '').str.replace('Sensor_', ''))
# remove first column
df_no_date = df.drop(df.columns[0], axis=1)

df_columns = df_no_date.values.T  # columns as rows
# some clever trick from SO - euclidean distance between columns (pair-wise)
# NOTE: we ignore here NaN values (i.e, treating them as zeros)
euclidean_matrix = np.nansum((df_columns - df_columns[:, None]) ** 2, axis=2) ** 0.5

euclidean_df = (lambda v, c: pd.DataFrame(v, c, c))(euclidean_matrix, df_no_date.columns)
print("EUCLIDEAN DISTANCES BETWEEN COLUMNS")
print(euclidean_df)

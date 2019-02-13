import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform


# noinspection SpellCheckingInspection
def p_norm(dataframe, p=2):
    """ Returns a data frame containing p-norm distances matrix of the input data frame. If the data contains
        any NaN values, they are interpolated.
        Args:
            dataframe (pandas.core.frame.DataFrame) - a data frame containing the data columns we want to compare
            p (int; optional) - determines which p-norm to use (defaults to 2, and has to be >= 1)
    """
    assert (p >= 1 and p == int(p)), "p has to be an int >= 1"
    # we interpolate the dataframe in order to replace NaN values
    df_interpolated = dataframe.interpolate()
    # We use the transpose values matrix so the columns become row vectors for pdist
    distances_matrix = squareform(pdist(df_interpolated.values.T, metric='minkowski', p=p))
    # Convert into a data frame
    distances_matrix_df = (lambda v, c: pd.DataFrame(v, c, c))(distances_matrix, dataframe.columns)

    return distances_matrix_df


# noinspection SpellCheckingInspection
def matrix_p_norm(dataframe, p=2):
    """ Returns a data frame containing p-norm distances matrix of the input data frame, treated as 3-column matrix.
        If the data contains any NaN values, they are interpolated.
        Args:
            dataframe (pandas.core.frame.DataFrame) - a data frame containing the data columns we want to compare
            p (int; optional) - determines which p-norm to use (defaults to 2, and has to be >= 1)
    """
    assert (p >= 1 and p == int(p)), "p has to be an int >= 1"
    # we interpolate the dataframe in order to replace NaN values
    df_interpolated = dataframe.interpolate()
    num_cols = len(df_interpolated.columns.tolist())
    reshaped_df_values = df_interpolated.values.T.reshape(int(num_cols / 3), -1).T

    # We use the transpose values matrix so the columns become row vectors for pdist
    distances_matrix = squareform(pdist(reshaped_df_values.T, metric='minkowski', p=p))
    _original_cols = dataframe.columns.tolist()
    _new_cols = pd.core.frame.Index(sorted(list(set([title[0] + title[-1] for title in _original_cols]))))
    # Convert into a data frame
    distances_matrix_df = (lambda v, c: pd.DataFrame(v, c, c))(distances_matrix, _new_cols)

    return distances_matrix_df


# Simple example
if __name__ == "__main__":
    # Import csv file with proper datetime format
    df = pd.read_csv("Clean_Data/nan_reduced_VWC.csv", parse_dates={'date_time': [0]}, dayfirst=True)

    # Edit column header names to enable splitting later on
    df.columns = (df.columns.str.replace(' ', '_').str.replace('(', '')
                  .str.replace(')', '').str.replace(',', '').str.replace('\'', '')
                  .str.replace('Interface', '').str.replace('Sensor_', ''))

    # remove first column (date-time)
    df_no_date = df.drop(df.columns[0], axis=1)

    euclidean_dists_df = p_norm(df_no_date)
    plt.figure()
    sns.heatmap(euclidean_dists_df, cmap="hot")
    plt.title("Euclidean distances matrix")
    plt.show()

    L1_dists_df = p_norm(df_no_date, p=1)
    plt.figure()
    sns.heatmap(L1_dists_df, cmap="hot")
    plt.title("L1 distances matrix")
    plt.show()

    df2 = pd.read_csv("Clean_Data/nan_reduced_no_permitivity.csv", parse_dates={'date_time': [0]}, dayfirst=True)

    # Edit column header names to enable splitting later on
    df2.columns = (df2.columns.str.replace(' ', '_').str.replace('(', '')
                  .str.replace(')', '').str.replace(',', '').str.replace('\'', '')
                  .str.replace('Interface', '').str.replace('Sensor_', ''))

    original_cols = df2.columns.tolist()
    new_cols = [original_cols[0]]
    interfaces = [c + '_' for c in "ABCDEFGHI"]
    for interface in interfaces:
        for ind in ['_1', '_2', '_3']:
            for meas in ['VWC', 'Soil_Temperature', 'BulkEC']:
                new_col_title = interface + meas + ind
                if new_col_title in original_cols:
                    new_cols.append(new_col_title)
    df2 = df2[new_cols]
    df2_no_date = df2.drop(df2.columns[0], axis=1)

    euclidean_dists_df2 = matrix_p_norm(df2_no_date)
    plt.figure()
    sns.heatmap(euclidean_dists_df2, cmap="hot")
    plt.title("L1 distances matrix")
    plt.show()



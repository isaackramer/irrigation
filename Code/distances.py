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
    distances_matrix_df = (lambda v, c: pd.DataFrame(v, c, c))(distances_matrix, df_no_date.columns)

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

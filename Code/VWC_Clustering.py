import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import squareform
from sklearn.cluster import KMeans
from pandas import DataFrame
from scipy.cluster.hierarchy import linkage, dendrogram


# noinspection PyPep8Naming
def clustering_demo():
    df = pd.read_pickle('dtw_distances_H_sampling.pkl')
    condensed_distance_matrix = squareform(df.values)
    Z = linkage(condensed_distance_matrix, metric='precomputed')
    dendrogram(Z, orientation='right', labels=df.columns.tolist())
    plt.show()

# read the data from "TDR_data_clean_VWC.csv" file
def read_data():

    soil_df = pd.read_csv("TDR_data_clean_VWC.csv", parse_dates={'date_time': [0]}, dayfirst=True)

    soil_df.columns = (soil_df.columns.str.replace(' ', '_').str.replace('(', '')
                       .str.replace(')', '').str.replace(',', '').str.replace('\'', '')
                       .str.replace('Interface', '').str.replace('Sensor_', ''))

    return soil_df


# plot the k-means clustering between the two columns
def time_series_cluster(data, col1, col2, n_clusters):
    df = DataFrame(data, columns=[col1, col2])

    # Cluster the data
    k_means = KMeans(n_clusters=n_clusters).fit(df)
    centroids = k_means.cluster_centers_
    plt.scatter(df[col1], df[col2], c=k_means.labels_.astype(float), s=50, alpha=0.5)
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
    plt.title('Clusters ' +  col1 +' vs ' + col2)
    plt.xlabel(col1)
    plt.ylabel(col2)
    plt.show()



def main(col1, col2, n):

    soil_df = read_data()
    soil_df = soil_df.fillna(value=0)
    # soil_df['date'] = pd.to_datetime(soil_df['date_time'])
    my_data = soil_df.loc[:, [col1, col2]]
    time_series_cluster(my_data, col1, col2, n)


# This is example of k-means clustering for columns 'A_VWC_1' and 'A_VWC_2' with k = 3
if __name__ == "__main__":
    main('A_VWC_1', 'A_VWC_2', 3)





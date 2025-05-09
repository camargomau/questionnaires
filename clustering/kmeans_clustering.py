from sklearn.cluster import KMeans
import pandas as pd

def kmeans_clustering(data, n_clusters=3):
    """
    Perform KMeans clustering on the given data.

    Args:
        data (pd.DataFrame): The input data for clustering.
        n_clusters (int): The number of clusters to form.

    Returns:
        tuple: A tuple containing the cluster labels and the fitted KMeans model.
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(data)
    return cluster_labels, kmeans

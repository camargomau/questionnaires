from sklearn.cluster import DBSCAN
import pandas as pd

def dbscan_clustering(data, eps=0.5, min_samples=5):
    """
    Perform DBSCAN clustering on the given data.

    Args:
        data (pd.DataFrame): The input data for clustering.
        eps (float): The maximum distance between two samples for them to be considered as in the same neighborhood.
        min_samples (int): The number of samples in a neighborhood for a point to be considered as a core point.

    Returns:
        tuple: A tuple containing the cluster labels and the fitted DBSCAN model.
    """
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    cluster_labels = dbscan.fit_predict(data)
    return cluster_labels, dbscan

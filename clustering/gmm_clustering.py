from sklearn.mixture import GaussianMixture
import pandas as pd

def gmm_clustering(data, n_clusters=3):
    """
    Perform Gaussian Mixture Model clustering on the given data.

    Args:
        data (pd.DataFrame): The input data for clustering.
        n_clusters (int): The number of clusters to form.

    Returns:
        tuple: A tuple containing the cluster labels and the fitted GaussianMixture model.
    """
    gmm = GaussianMixture(n_components=n_clusters, random_state=42)
    cluster_labels = gmm.fit_predict(data)
    return cluster_labels, gmm

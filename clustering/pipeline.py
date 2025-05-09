import pandas as pd
from kmeans_clustering import kmeans_clustering
from dbscan_clustering import dbscan_clustering
from agglomerative_clustering import agglomerative_clustering
from gmm_clustering import gmm_clustering
from visualise import visualise_clusters

def run_clustering_pipeline(data_path):
    """
    Run the clustering pipeline on the given dataset.

    Args:
        data_path (str): Path to the processed data CSV file.
    """
    # Load the processed data
    data = pd.read_csv(data_path)

    # Select relevant features for clustering
	# Numeric features only
    features = data.select_dtypes(include=['float64', 'int64'])

    # Perform KMeans clustering
    kmeans_labels, _ = kmeans_clustering(features)
    visualise_clusters(features, kmeans_labels, title="KMeans Clustering")

    # Perform DBSCAN clustering
    dbscan_labels, _ = dbscan_clustering(features)
    visualise_clusters(features, dbscan_labels, title="DBSCAN Clustering")

    # Perform Agglomerative Clustering
    agglomerative_labels, _ = agglomerative_clustering(features)
    visualise_clusters(features, agglomerative_labels, title="Agglomerative Clustering")

    # Perform Gaussian Mixture Model Clustering
    gmm_labels, _ = gmm_clustering(features)
    visualise_clusters(features, gmm_labels, title="Gaussian Mixture Model Clustering")

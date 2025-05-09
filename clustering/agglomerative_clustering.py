from sklearn.cluster import AgglomerativeClustering
import pandas as pd

def agglomerative_clustering(data, n_clusters=3):
	"""
	Perform Agglomerative Clustering on the given data.

	Args:
		data (pd.DataFrame): The input data for clustering.
		n_clusters (int): The number of clusters to form.

	Returns:
		tuple: A tuple containing the cluster labels and the fitted AgglomerativeClustering model.
	"""
	agglomerative = AgglomerativeClustering(n_clusters=n_clusters)
	cluster_labels = agglomerative.fit_predict(data)
	return cluster_labels, agglomerative

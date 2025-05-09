from clustering.prepare_data import build_master_dataframe, scale_data

from clustering.methods.kmeans import kmeans_clustering
from clustering.methods.dbscan import dbscan_clustering
from clustering.methods.agglomerative import agglomerative_clustering
from clustering.methods.gmm import gmm_clustering

def perform_clustering(data, scaled_data):
	"""
	Run the clustering pipeline on the given dataset.

	Args:
		data (pd.DataFrame): The original non-scaled data as a DataFrame.
		scaled_data (pd.DataFrame): The scaled data as a DataFrame.
	"""

	# Perform KMeans clustering
	kmeans_labels, _ = kmeans_clustering(scaled_data)
	data['KMeans_Cluster'] = kmeans_labels

	# Perform DBSCAN clustering
	dbscan_labels, _ = dbscan_clustering(scaled_data)
	data['DBSCAN_Cluster'] = dbscan_labels

	# Perform Agglomerative Clustering
	agglomerative_labels, _ = agglomerative_clustering(scaled_data)
	data['Agglomerative_Cluster'] = agglomerative_labels

	# Perform Gaussian Mixture Model Clustering
	gmm_labels, _ = gmm_clustering(scaled_data)
	data['GMM_Cluster'] = gmm_labels

	return kmeans_labels, dbscan_labels, agglomerative_labels, gmm_labels

def export_clustering_results(data, output_path="data/export/clustering/clustering_results.csv"):
	"""
	Export the clustering results to a CSV file.

	Args:
		data (pd.DataFrame): The original non-scaled data with cluster labels added.
		output_path (str): The path to save the exported CSV file.
	"""

	data.to_csv(output_path, index=False)
	print(f"Clustering results exported to {output_path}")

if __name__ == "__main__":
	# Build the master dataframe
	data = build_master_dataframe()
	# Scale the data using only numeric features (though the selected features should already be numeric)
	# Exclude "numero de cuenta"
	scaled_data = scale_data(data.drop(columns=['numero de cuenta']).select_dtypes(include=['float64', 'int64']))
	# Perform clustering
	kmeans_labels, dbscan_labels, agglomerative_labels, gmm_labels = perform_clustering(data, scaled_data)
	# Export the clustering results
	export_clustering_results(data)

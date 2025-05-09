import pandas as pd
from sklearn.preprocessing import StandardScaler

from clustering.kmeans_clustering import kmeans_clustering
from clustering.dbscan_clustering import dbscan_clustering
from clustering.agglomerative_clustering import agglomerative_clustering
from clustering.gmm_clustering import gmm_clustering

from clustering.selected_features import selected_features

def build_master_dataframe():
	"""
	Build a master dataframe by selecting relevant columns from multiple questionnaires
	and merging them on the 'numero de cuenta' column.

	Returns:
		pd.DataFrame: The master dataframe containing selected features for clustering.
	"""

	base_path = "data/export/"
	dataframes = []

	# Iterate over the selected features for each questionnaire
	for i, features in enumerate(selected_features):
		# Skip empty lists (no features selected for this questionnaire)
		if features:
			# Construct the file name for the questionnaire
			file_name = f"questionnaire_{i+1}.csv"
			file_path = base_path + file_name

			try:
				df = pd.read_csv(file_path)
				# Handle the specific case for "1 numero de cuenta" (questionnaire 5)
				df.rename(columns={"1 numero de cuenta": "numero de cuenta"}, inplace=True)

				# Select the relevant columns
				selected_df = df[features]
				# Append the selected DataFrame to the list
				dataframes.append(selected_df)
			except FileNotFoundError:
				print(f"Warning: File {file_name} not found. Skipping.")
			except KeyError as e:
				print(f"Warning: Missing columns in {file_name}: {e}. Skipping.")

	# Merge all DataFrames on 'numero de cuenta'
	if dataframes:
		master_df = dataframes[0]
		for df in dataframes[1:]:
			master_df = pd.merge(master_df, df, on="numero de cuenta", how="inner")
	else:
		raise ValueError("No valid dataframes were created. Check your selected_features or input files.")

	return master_df

def scale_data(data):
	"""
	Scale the input data using StandardScaler.

	Args:
		data (pd.DataFrame or np.ndarray): The data to be scaled.

	Returns:
		np.ndarray: The scaled data.
	"""

	scaler = StandardScaler()
	scaled_array = scaler.fit_transform(data)
	return pd.DataFrame(scaled_array, columns=data.columns)

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

def export_clustering_results(data, output_path="data/export/clustering_results.csv"):
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

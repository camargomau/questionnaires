import pandas as pd
from sklearn.preprocessing import StandardScaler

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

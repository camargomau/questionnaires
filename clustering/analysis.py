import pandas as pd
from sklearn.preprocessing import StandardScaler

def generate_cluster_stats(data, cluster_column):
    """
    Generate a dictionary of DataFrames for all supported statistics for a single clustering method.

    Args:
        data (pd.DataFrame): The input data containing features and clustering labels.
        cluster_column (str): The clustering method column name.

    Returns:
        dict: A dictionary where the keys are statistics ('mean', 'median', 'std', 'var', 'range') and the values are DataFrames of the specified statistics.
    """

    data = data.drop(columns=['numero de cuenta'])

    statistics_functions = {
        'mean': lambda grouped, features: grouped[features].mean(),
        'median': lambda grouped, features: grouped[features].median(),
        'std': lambda grouped, features: grouped[features].std(),
        'var': lambda grouped, features: grouped[features].var(),
        'range': lambda grouped, features: grouped[features].max() - grouped[features].min()
    }

    result_statistics = {}

    for statistic, func in statistics_functions.items():
        # Scale data if needed
        if statistic == "mean":
            current_data = data
        else:
            scaler = StandardScaler()
            scaled_array = scaler.fit_transform(data.drop(columns=[cluster_column]))
            current_data = pd.DataFrame(scaled_array, columns=data.drop(columns=[cluster_column]).columns)
            current_data[cluster_column] = data[cluster_column].values  # Add cluster_column back

        # Select only numeric features, excluding the cluster_column
        features = current_data.drop(columns=[cluster_column]).select_dtypes(include=['float64', 'int64']).columns
        grouped = current_data.groupby(cluster_column)
        result_statistics[statistic] = func(grouped, features)

    return result_statistics

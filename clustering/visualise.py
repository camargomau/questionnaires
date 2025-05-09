import matplotlib.pyplot as plt
import pandas as pd

def visualise_clusters(data, cluster_labels, title="Cluster Visualisation"):
    """
    Visualise the clustering results using a scatter plot.

    Args:
        data (pd.DataFrame): The input data for clustering.
        cluster_labels (array-like): The cluster labels for each data point.
        title (str): The title of the plot.
    """
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(data.iloc[:, 0], data.iloc[:, 1], c=cluster_labels, cmap='viridis', s=50)
    plt.colorbar(scatter, label="Cluster")
    plt.title(title)
    plt.xlabel(data.columns[0])
    plt.ylabel(data.columns[1])
    plt.show()

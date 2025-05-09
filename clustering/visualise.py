import seaborn as sns
import matplotlib.pyplot as plt

def visualise_clusters(data, cluster_labels, title="Cluster Visualization"):
    """
    Visualize the clustering results using a scatter plot.

    Args:
        data (pd.DataFrame): The input data for clustering.
        cluster_labels (array-like): The cluster labels for each data point.
        title (str): The title of the plot.
    """

    # Create a DataFrame for visualisation
    visualization_df = data.copy()
    visualization_df['Cluster'] = cluster_labels

    # Use seaborn to create a scatter plot
    plt.figure(figsize=(10, 6))
    scatter = sns.scatterplot(
        x=visualization_df.iloc[:, 0],
        y=visualization_df.iloc[:, 1],
        hue='Cluster',
        palette='viridis',
        data=visualization_df,
        s=50
    )
    scatter.set_title(title)
    scatter.set_xlabel(data.columns[0])
    scatter.set_ylabel(data.columns[1])
    plt.legend(title="Cluster")
    plt.show()

def visualise_all_clusters(data, scaled_data, kmeans_labels, dbscan_labels, agglomerative_labels, gmm_labels):
    """
    Visualize the clustering results for all clustering methods.

    Args:
        data (pd.DataFrame): The original non-scaled data.
        scaled_data (pd.DataFrame): The scaled data used for clustering.
        kmeans_labels (array-like): Cluster labels from KMeans.
        dbscan_labels (array-like): Cluster labels from DBSCAN.
        agglomerative_labels (array-like): Cluster labels from Agglomerative Clustering.
        gmm_labels (array-like): Cluster labels from Gaussian Mixture Model.
    """

    # Visualize KMeans clustering
    visualise_clusters(scaled_data, kmeans_labels, title="KMeans Clustering")

    # Visualize DBSCAN clustering
    visualise_clusters(scaled_data, dbscan_labels, title="DBSCAN Clustering")

    # Visualize Agglomerative Clustering
    visualise_clusters(scaled_data, agglomerative_labels, title="Agglomerative Clustering")

    # Visualize Gaussian Mixture Model Clustering
    visualise_clusters(scaled_data, gmm_labels, title="Gaussian Mixture Model Clustering")

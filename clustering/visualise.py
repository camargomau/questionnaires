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

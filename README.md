# questionnaires

## Overview

This project is designed to process, clean, standardise, cluster, and visualise survey data from multiple Excel files. It was originally used to process responses from specific questionnaires completed by my classmates during my Minería de Datos course.

The project provides tools to:
1. Import, clean, and standardise raw data.
2. Export the processed data to CSV files and optionally upload it to Google BigQuery for further analysis (this is how I worked with this data on Looker Studio).
3. Perform clustering using multiple algorithms (KMeans, DBSCAN, Agglomerative Clustering, and Gaussian Mixture Models).
4. Visualise clustering results interactively in a Jupyter Notebook.

## File Descriptions

### Root Directory

- **`process.py`**
  The main script that orchestrates the data processing workflow. It:
  1. Imports raw data from Excel files.
  2. Cleans and standardises the data.
  3. Exports the processed data to CSV files.
  4. Optionally uploads the data to Google BigQuery if a configuration file is provided.

- **`cluster.py`**
  The main script for clustering. It:
  1. Builds a master dataframe by merging selected features from multiple questionnaires.
  2. Scales the data for clustering.
  3. Performs clustering using KMeans, DBSCAN, Agglomerative Clustering, and Gaussian Mixture Models.
  4. Exports the clustering results to a CSV file.

- **`requirements.txt`**
  Lists the Python packages required to run the project.

### `processing/` Directory

- **`import_data.py`**
  Handles the import of Excel files from the `data/import/xlsx` folder. It reads the files into pandas DataFrames and cleans column names.

- **`clean_data.py`**
  Cleans the imported data by:
  - Removing duplicate rows based on account numbers.
  - Cleaning text fields (e.g., removing accents, punctuation, and normalising whitespace).
  - Dropping unnecessary columns like email addresses.

- **`standardise_data.py`**
  Standardises the data based on predefined question types. It processes numeric, boolean, time, and categorical data to ensure consistency across all datasets.

- **`export_data.py`**
  Exports the processed data:
  - To CSV files in the `data/export` folder.
  - To Google BigQuery, if configured, using the `pandas-gbq` library.

- **`question_types.py`**
  Contains a predefined list of question types for each questionnaire. These types guide the standardisation process. This list corresponds to the questionnaires this project was originally developed for.

### `clustering/` Directory

- **`analysis.ipynb`**
  A Jupyter Notebook for analysing clustering statistics. It:
  - Allows you to specify which statistics to show (mean, median, standard deviation, variance, range).
  - Allows you to select the method whose clusters are to be analysed.

- **`cluster_stats.py`**
  Contains functions to compute various statistics (mean, median, standard deviation, variance, range) for clustering results.

- **`prepare_data.py`**
  Prepares the master dataframe for clustering by merging selected features from multiple questionnaires and scaling the data.

- **`selected_features.py`**
  Contains a list of selected features for each questionnaire. These features are used to build the master dataframe for clustering.

#### `methods/` Subdirectory

- **`kmeans.py`**
  Implements KMeans clustering using scikit-learn.

- **`dbscan.py`**
  Implements DBSCAN clustering using scikit-learn. Includes adjustable parameters for `eps` and `min_samples`.

- **`agglomerative.py`**
  Implements Agglomerative Clustering using scikit-learn.

- **`gmm.py`**
  Implements Gaussian Mixture Model clustering using scikit-learn.

### `visualisation.ipynb`

A Jupyter Notebook for visualising clustering results. It:
- Allows you to specify which features to use for the x and y axes.
- Supports optional convex hull visualisation for clusters.
- Visualises results for all clustering methods (KMeans, DBSCAN, Agglomerative Clustering, and Gaussian Mixture Models).

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Tablero-Analitico
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # on Windows
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Data Workflow

### Processing

Run `python process.py` with the following considerations:

1. **Input Files**:
   Place the raw Excel files in the `data/import/xlsx` folder. The script will automatically detect and process all `.xlsx` files in this directory.

2. **Processing**:
   The script performs the following steps:
   - Cleans and standardises the data.
   - Removes duplicates and unnecessary columns.
   - Applies transformations based on question types.

3. **Output Files**:
   Processed data is exported as CSV files to the `data/export` folder.

### Clustering

Run `python cluster.py` with the following considerations:

1. **Build Master Dataframe**:
   The `cluster.py` script merges selected features from multiple questionnaires into a single dataframe.

2. **Scale Data**:
   The numeric features are scaled using `StandardScaler` to ensure proper clustering.

3. **Clustering Algorithms**:
   The following clustering algorithms are applied:
   - **KMeans**: Groups data into a predefined number of clusters.
   - **DBSCAN**: Identifies clusters based on density, with adjustable `eps` and `min_samples` parameters.
   - **Agglomerative Clustering**: Performs hierarchical clustering.
   - **Gaussian Mixture Models (GMM)**: Fits data to a mixture of Gaussian distributions.

4. **Export Results**:
   The clustering results are exported to `data/export/clustering/clustering_results.csv`. The file includes the original features and cluster labels for each method.

#### Visualisation

1. Open the `visualisation.ipynb` notebook.
2. Load the clustering results from `data/export/clustering/clustering_results.csv`.
3. Use the `visualise_all_clusters()` function to visualise the clusters:
   - Specify the features to use for the x and y axes.
   - Enable or disable convex hull visualisation for clusters.

#### Analysis

1. Open the `analysis.ipynb` notebook.
2. Load the clustering results from `data/export/clustering/clustering_results.csv`.
3. Use the `generate_cluster_stats()` function to explore cluster statistics:
   - Specify the statistics to be shown (mean, median, standard deviation, variance, range).
   - Specify the method whose clusters are to be analysed.

## Google BigQuery Integration

To upload the processed data to Google BigQuery, follow these steps:

1. Create a JSON configuration file with the following structure:
   ```json
   {
       "project_id": "your-google-cloud-project-id",
       "dataset_id": "your-dataset-id",
       "table_names": ["table1", "table2", "table3"]
   }
   ```

2. Run the `process.py` script and pass the configuration file as a command-line argument:
   ```bash
   python process.py path/to/gbq_config.json
   ```

3. The script will validate the configuration and upload the processed data to the specified BigQuery tables.

## Notes

- Ensure your Google Cloud credentials are properly set up before using the BigQuery integration. In my case, I just had to try to upload to BigQuery for the first time and then I was asked to authenticate in my browser.
- The script assumes a specific folder structure for input and output files. Modify the paths in the code if necessary.
- Use the `visualisation.ipynb` and `analysis.ipynb` notebooks for interactive exploration of clustering results and statistics.

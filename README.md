# questionnaires

## Overview

This project is designed to process, clean, and standardise survey data from multiple Excel files. It was originally used to process responses from specific questionnaires completed by my classmates during my Minería de Datos course.

The project provides tools to export the processed data to CSV files and optionally upload it to Google BigQuery for further analysis (this is how I worked with this data on Looker Studio). It handles various data types, including numeric and boloean data, and ensures consistent formatting across all datasets.

## File Descriptions

### Root Directory

- **`questionnaires.py`**
  The main script that orchestrates the data processing workflow. It:
  1. Imports raw data from Excel files.
  2. Cleans and standardises the data.
  3. Exports the processed data to CSV files.
  4. Optionally uploads the data to Google BigQuery if a configuration file is provided.

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

1. **Input Files**:
   Place the raw Excel files in the `data/import/xlsx` folder. The script will automatically detect and process all `.xlsx` files in this directory.

2. **Processing**:
   The script performs the following steps:
   - Cleans and standardises the data.
   - Removes duplicates and unnecessary columns.
   - Applies transformations based on question types.

3. **Output Files**:
   Processed data is exported as CSV files to the `data/export` folder.

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

2. Run the script and pass the configuration file as a command-line argument:
   ```bash
   python questionnaires.py path/to/gbq_config.json
   ```

3. The script will validate the configuration and upload the processed data to the specified BigQuery tables.

## Notes

- Ensure your Google Cloud credentials are properly set up before using the BigQuery integration. In my case, I just had to try to upload to BigQuery for the first time and then I was asked to authenticate in my browser.
- The script assumes a specific folder structure for input and output files. Modify the paths in the code if necessary.

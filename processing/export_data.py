import os
import re
from pandas_gbq import to_gbq

def export_csv(questionnaires, output_folder="data/export"):
    """
    Exports a list of DataFrames to CSV files in the specified output folder.

    Args:
        questionnaires (list): A list of pandas DataFrames to export.
        output_folder (str): The folder where the CSV files will be saved. Defaults to "export".

    Returns:
        list: A list of file paths for the exported CSV files.
    """

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Initialise a list to store the paths of exported files
    exported_files = []

    # Export each DataFrame to a CSV file
    for i, questionnaire in enumerate(questionnaires):
        output_file = os.path.join(output_folder, f"questionnaire_{i + 1}.csv")
        questionnaire.to_csv(output_file, index=False, encoding="utf-8")
        exported_files.append(output_file)

    return exported_files

def export_gbq(questionnaires, project_id, dataset_id, table_names):
    """
    Exports a list of DataFrames to Google BigQuery.

    Args:
        questionnaires (list): A list of pandas DataFrames to export.
        project_id (str): The Google Cloud project ID.
        dataset_id (str): The BigQuery dataset ID.
        table_names (list): A list of table names corresponding to the DataFrames.
    """

    for dataframe, table_name in zip(questionnaires, table_names):
        table_id = f"{dataset_id}.{table_name}"
        to_gbq(dataframe, table_id, project_id=project_id, if_exists="replace")

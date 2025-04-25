import sys
import json

from processing.question_types import question_types

from processing.import_data import import_xlsx
from processing.clean_data import clean_questionnaires
from processing.standardise_data import numeric_standardise_questionnaires
from processing.export_data import export_csv, export_gbq, sanitise_column_names

def load_config(config_file):
    """
    Load configuration from a JSON file.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        dict: Configuration data.
    """

    with open(config_file, "r") as file:
        return json.load(file)

if __name__ == "__main__":
    # Import data from xlsx files
    questionnaires, filenames = import_xlsx()

    # Clean data
    questionnaires_cleaned = clean_questionnaires(questionnaires)

    # Standardise numeric data (percentages, int, float, time, etc.)
    questionnaires_standardised = numeric_standardise_questionnaires(questionnaires_cleaned, question_types)

    # Standardise text data
    # soon

    # Sanitise column names for BigQuery
    questionnaires_standardised = [
        sanitise_column_names(df) for df in questionnaires_standardised
    ]
    # Export processed data to CSV
    exported_files = export_csv(questionnaires_standardised)

    # Check if a configuration file is passed as an argument
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        try:
            config = load_config(config_file)
            project_id = config.get("project_id")
            dataset_id = config.get("dataset_id")
            table_names = config.get("table_names")

            if project_id and dataset_id and table_names:
                # Export data to Google BigQuery
                export_gbq(questionnaires_standardised, project_id, dataset_id, table_names)
                print("Data successfully uploaded to BigQuery.")
            else:
                print("Invalid configuration file. Missing required fields.")
        except Exception as e:
            print(f"Failed to load configuration file: {e}")
    else:
        print("No configuration file provided. Skipping BigQuery upload.")

    print("All files processed and exported successfully.")

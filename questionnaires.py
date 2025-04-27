import sys
import json

from processing.question_types import question_types

from processing.import_data import import_xlsx
from processing.clean_data import clean_questionnaires
from processing.standardise_data import non_text_standardise_questionnaires
from processing.export_data import export_csv, export_gbq

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

def check_gbq_export():
    """
    Check and export data to Google BigQuery if a configuration file is provided.

    This function checks if a configuration file is passed as a command-line argument.
    If provided, it loads the configuration, validates the required fields (project_id,
    dataset_id, and table_names), and attempts to export the processed data to Google BigQuery.
    If any required field is missing or an error occurs during the export, it logs an appropriate
    message. If no configuration file is provided, it skips the BigQuery upload.

    Raises:
        Exception: If an error occurs during the export process.
    """

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
            print(f"Export to Google BigQuery failed: {e}")
    else:
        print("No configuration file provided. Skipping BigQuery upload.")

if __name__ == "__main__":
    # Import data from xlsx files
    questionnaires, filenames = import_xlsx()

    # Clean data
    questionnaires_cleaned = clean_questionnaires(questionnaires)

    # Standardise non-text data (percentages, int, float, time, boolean, etc.)
    questionnaires_standardised = non_text_standardise_questionnaires(questionnaires_cleaned, question_types)
    # Standardise text data
    # soon

    # Export processed data to CSV
    exported_files = export_csv(questionnaires_standardised)
	# If a configuration file is provided, export to Google BigQuery
    check_gbq_export()

    print("All files processed and exported successfully.")

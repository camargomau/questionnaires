import os

def export_csv(questionnaires, output_folder="export"):
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

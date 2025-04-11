import os
import pandas as pd

def import_xlsx(folder="cuestionarios"):
    """
    Imports all .xlsx files from the specified folder, cleans column names,
    and returns a list of DataFrames along with their corresponding filenames.

    Args:
        folder (str): The folder containing the .xlsx files. Defaults to "cuestionarios".

    Returns:
        tuple: A tuple containing:
            - questionnaires (list): A list of pandas DataFrames for each .xlsx file.
            - filenames (list): A list of filenames corresponding to the DataFrames.
    """

    # Get all .xlsx files in the folder
    excel_files = sorted([f for f in os.listdir(folder) if f.endswith('.xlsx')])

    # Initialise lists to store DataFrames and filenames
    questionnaires = []
    filenames = []

    # Process each .xlsx file
    for file in excel_files:
        file_path = os.path.join(folder, file)

        # Read the Excel file into a DataFrame
        file_df = pd.read_excel(file_path)

        # Clean column names by stripping whitespace
        file_df.columns = file_df.columns.str.strip()

        # Append the DataFrame and filename to their respective lists
        questionnaires.append(file_df)
        filenames.append(file)

    return questionnaires, filenames

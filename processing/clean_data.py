import pandas as pd
import re
import string
import unicodedata

def clean_text(text):
    """
    Cleans a given text by:
    - Converting to lowercase
    - Removing accents from characters (e.g., áéíóúñ -> aeioun)
    - Removing non-ASCII characters
    - Removing punctuation except .,:;-–/@
    - Normalising whitespace
    """

    # Convert to lowercase
    text = text.lower()
    # Normalise and remove accents
    text = unicodedata.normalize('NFD', text)
    text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
    # Remove non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    # Remove unwanted punctuation
    text = re.sub(r'[^\w\s.,:;\-–\/@]', '', text)
    # Normalise whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def normalise_column_names(questionnaires):
    """
    Normalises all column names in a list of DataFrames by:
    - Cleaning text using the clean_text function.
    - Removing all punctuation from column names.
    """

    for i, questionnaire in enumerate(questionnaires):
        # Clean and remove punctuation from column names
        questionnaires[i].columns = [
            ''.join(char for char in clean_text(col) if char not in string.punctuation)
            for col in questionnaire.columns
        ]

    return questionnaires

def remove_duplicates(questionnaires):
    """
    Removes duplicate rows based on the account number column within each questionnaire.
    Prioritises earlier responses within the same questionnaire.
    """

    questionnaires_no_dupes = []

    for questionnaire in questionnaires:
        # Normalise column names for dynamic identification
        normalised_columns = {col: clean_text(col) for col in questionnaire.columns}
        account_column = next(
            (original_col for original_col, normalized_col in normalised_columns.items() if "numero de cuenta" in normalized_col),
            None
        )

        if account_column:
            # Ensure account numbers are treated as strings to avoid mismatches
            questionnaire[account_column] = questionnaire[account_column].astype(str)
            # Drop duplicates within the current questionnaire while keeping the first occurrence
            questionnaire = questionnaire[~questionnaire.duplicated(subset=[account_column], keep="first")]

        # Append the deduplicated questionnaire to the result
        questionnaires_no_dupes.append(questionnaire)

    return questionnaires_no_dupes

def clean_questionnaires(questionnaires):
    """
    Cleans a list of questionnaires (DataFrames) by:
    - Removing duplicate rows based on account number
    - Removing the "Dirección de correo electrónico" column if it exists
    - Cleaning text in all columns except those containing "Marca temporal"
    """

    # Normalise column names for each questionnaire
    questionnaires = normalise_column_names(questionnaires)

    # Remove duplicates
    questionnaires = remove_duplicates(questionnaires)

    # Remove email column if it exists
    cleaned_questionnaires = [
        questionnaire.drop(columns=["direccion de correo electronico"], errors="ignore")
        for questionnaire in questionnaires
    ]

    # Clean text in all columns except "Marca temporal"
    for i, questionnaire in enumerate(questionnaires):
        for column in questionnaire.columns:
            if "Marca temporal" in column:
                # Preserve "Marca temporal" columns without modification
                cleaned_questionnaires[i][column] = questionnaire[column]
            else:
                # Clean text in all other columns
                cleaned_questionnaires[i][column] = questionnaire[column].astype(str).apply(clean_text)

    return cleaned_questionnaires

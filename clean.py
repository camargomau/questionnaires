import pandas as pd
import re

def clean_text(text):
    """
    Cleans a given text by:
    - Converting to lowercase
    - Removing non-ASCII characters
    - Removing punctuation except .,:;-–/@
    - Normalising whitespace
    """
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
    text = re.sub(r'[^\w\s.,:;\-–\/@]', '', text)  # Remove unwanted punctuation
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
    return text

def clean_questionnaires(questionnaires):
    """
    Cleans a list of questionnaires (DataFrames) by:
    - Removing the "Dirección de correo electrónico" column if it exists
    - Cleaning text in all columns except those containing "Marca temporal"
    """
    cleaned_questionnaires = [
        questionnaire.drop(columns=["Dirección de correo electrónico"], errors="ignore")
        for questionnaire in questionnaires
    ]

    for i, questionnaire in enumerate(questionnaires):
        for column in questionnaire.columns:
            if "Marca temporal" in column:
                # Preserve "Marca temporal" columns without modification
                cleaned_questionnaires[i][column] = questionnaire[column]
            else:
                # Clean text in all other columns
                cleaned_questionnaires[i][column] = questionnaire[column].astype(str).apply(clean_text)

    return cleaned_questionnaires

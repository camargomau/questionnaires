import pandas as pd
import re
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

from question_types import question_types

from import_data import import_xlsx
from clean_data import clean_questionnaires
from standardise_data import numeric_standardise_questionnaires
from export_data import export_csv

if __name__ == "__main__":
	# Import data from xlsx files
	questionnaires, filenames = import_xlsx()

	# Clean data
	questionnaires_cleaned = clean_questionnaires(questionnaires)

	# Standardise numeric data (percentages, int, float, time, etc.)
	questionnaires_standardised = numeric_standardise_questionnaires(questionnaires_cleaned, question_types)

	# Standardise text data
	# soon

	# Export processed data
	exported_files = export_csv(questionnaires_standardised)

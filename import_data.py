import os
import pandas as pd

def import_xlsx():
	folder = "cuestionarios"

	files = os.listdir(folder)
	excel_files = sorted([f for f in files if f.endswith('.xlsx')])

	# Guardar todos los datos como dataframes, dentro de una lista de dataframes
	questionnaires = []
	# Lista de nombres de archivo como referencia
	filenames = []

	for file in excel_files:
		file_path = os.path.join(folder, file)
		file_df = pd.read_excel(file_path)
		# strip() sobre los nombres de columnas
		file_df.columns = file_df.columns.str.strip()
		questionnaires.append(file_df)
		# Guardar el nombre de archivo como referencia
		filenames.append(os.path.basename(file_path))

	# Guía para saber qué número corresponde a qué archivo
	# for filename in filenames:
	# 	print(f"{filenames.index(filename)} es {filename}")

	return questionnaires, filenames

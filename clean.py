import re

def clean_text(text):
	# Todo a minúsculas
	text = text.lower()
	# Quitar caracteres no ASCII
	text = re.sub(r'[^\x00-\x7F]+', '', text)
	# Quitar signos de puntuación, a excepción de .,:;-–/@
	text = re.sub(r'[^\w\s.,:;\-–\/@]', '', text)
	# Normalizar espacios en blanco
	text = re.sub(r'\s+', ' ', text).strip()

	return text

def clean_questionnaires(questionnaires):
	# Lista de DataFrames donde se almacenarán los datos limpios
	questionnaires_clean = []
	for questionnaire in questionnaires:
		# Copiar el DataFrame questionnaires y eliminar la columna de correo si existe
		new_questionnaire = questionnaire.drop(columns=["Dirección de correo electrónico"], errors="ignore")
		questionnaires_clean.append(new_questionnaire)

	# Aplicar la función de limpieza a cada respuesta en los cuestionarios
	for questionnaire_i, questionnaire in enumerate(questionnaires):
		for column in questionnaire.columns:
			# Saltar las columnas de "Marca temporal"
			if "Marca temporal" not in column:
				questionnaires_clean[questionnaire_i][column] = questionnaire[column].astype(str).apply(clean_text)
			else:
				questionnaires_clean[questionnaire_i][column] = questionnaire[column]

	return questionnaires_clean

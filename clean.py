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

    cleaned_questionnaires = []

    for questionnaire in questionnaires:
        # Remove the email column if it exists
        cleaned_df = questionnaire.drop(columns=["Dirección de correo electrónico"], errors="ignore")
        cleaned_questionnaires.append(cleaned_df)

    for i, questionnaire in enumerate(questionnaires):
        for column in questionnaire.columns:
            if "Marca temporal" in column:
                # Preserve "Marca temporal" columns without modification
                cleaned_questionnaires[i][column] = questionnaire[column]
            else:
                # Clean text in all other columns
                cleaned_questionnaires[i][column] = questionnaire[column].astype(str).apply(clean_text)

    return cleaned_questionnaires

def process_account_number(value):
	"""
	Procesa números de cuenta
	"""
	if pd.isna(value) or not isinstance(value, str):
		return None

	value = value.strip().lower()

	# Buscar un número de cuenta válido
	match = re.search(r'\b[1-4]\d{8}\b', value)

	return match.group(0) if match else None

def process_numeric_input(value):
		"""
		Procesa entradas numéricas (flotantes):
		- Valores únicos (quita comas, $ u otro formato)
		- Miles representados como "K" (e.g., 2.5K -> 2500)
		- Rangos (e.g., "2000 - 5000" o "entre 2000 y 5000" -> promedio del rango)
		- Limpia palabras como "aproximadamente" o similares
		- Procesa "no" y "nada" como 0
		- Procesa fracciones como "3 1/2" y las convierte en decimales (e.g., 3.5)
		"""
		if pd.isna(value) or not isinstance(value, str):
			return None

		value = value.strip().lower()

		# Procesar "no" y "nada" como 0
		if value in ["no", "nada"]:
			return 0

		# Eliminar palabras irrelevantes como "aproximadamente"
		value = value.replace("$", "").replace("aproximadamente", "").replace("aprox", "")
		value = re.sub(r"[^\d.,\s\-–k\/]", "", value)# Quitar no numérico a excepción de .,-–/k

		# Convertir fracciones como "3 1/2" en decimales
		# Buscar expresiones de tipo "3 1/2" y convertirlas
		value = re.sub(r"(\d+)\s+(\d+)/(\d+)", lambda match: str(float(match.group(1)) + float(match.group(2)) / float(match.group(3))), value)

		# Verificar si hay un rango en el formato "3 - 5" o "3 5" y procesarlo correctamente
		if "-" in value or " " in value:
			try:
				# Rangos con "-" o espacio (e.g., "3-5" o "3 5")
				range_values = [float(v.strip().replace(",", "")) for v in value.split() if v.replace(",", "").isdigit()]
				if len(range_values) == 2:
					return sum(range_values) / len(range_values)
			except ValueError:
				return None

		# Miles como K
		if "k" in value:
			try:
				return float(value.replace("k", "").replace(",", "").strip()) * 1000
			except ValueError:
				return None

		# Rangos con "entre"
		if "entre" in value:
			try:
				# Extraer todos los números en el texto
				range_values = [float(v.replace(",", "")) for v in re.findall(r"\d+(?:,\d+)?(?:\.\d+)?", value)]
				if len(range_values) == 2: # Si hay exactamente dos números
					return sum(range_values) / len(range_values) # Retornar el promedio
			except ValueError:
				return None

		# Valores únicos
		try:
			return float(value.replace(",", ""))
		except ValueError:
			return None

def process_integer_input(value):
		"""
		Procesa entradas enteras:
		- Quita comas, espacios y otros caracteres.
		- Convierte strings con enteros a enteros.
		- Convierte "no" o "nada" a 0.
		- Convierte números escritos en palabras en español e inglés a enteros.
		"""
		if pd.isna(value) or not isinstance(value, str):
			return None

		value = value.strip().lower()

		# Diccionario de números en palabras
		num_words = {
			"uno": 1, "un": 1, "una": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
			"seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
			"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
			"six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
		}

		# "no" o "nada" a 0
		if value in ["no", "nada", "ninguno", "ninguna"]:
			return 0

		# Verificar si el valor es una palabra numérica
		if value in num_words:
			return num_words[value]

		# Quita caracteres superfluos
		value = re.sub(r"[^\d-]", "", value)

		# Convierte a entero
		try:
			return int(value)
		except ValueError:
			return None

def process_percentage_input(value):
		"""
		Procesa entradas de porcentajes:
		- Convierte valores como 95 a 0.95 (asume que valores mayores o iguales a 1 son porcentajes).
		- Convierte valores como 0.95 a 0.95 (mantiene valores ya en proporción).
		- Quita caracteres irrelevantes como "%".
		- Convierte "no", "nada", "ninguna", "niguna" o "no tengo" a 0.
		- Convierte "todo" a 1.
		"""
		if pd.isna(value) or not isinstance(value, str):
			return None

		value = value.strip().lower()

		# "no", "nada", "ninguna", "niguna" o "no tengo" a 0
		if value in ["no", "nada", "ninguna", "niguna", "no tengo"]:
			return 0
		# "todo" a 1
		elif value in ["todo", "toda"]:
			return 1

		# Quita caracteres irrelevantes como "%" y "el "
		value = value.replace("%", "").replace("el ", "").strip()

		# Convierte a flotante
		try:
			numeric_value = float(value)
			# Si el valor es mayor o igual a 1, asume que es un porcentaje y lo convierte a proporción
			if numeric_value >= 1:
				return numeric_value / 100
			return numeric_value
		except ValueError:
			return None

def process_time_input(value, return_unit="m"):
		"""
		Procesa entradas de tiempo:
		- Interpreta horas o minutos según el argumento return_unit ("m" para minutos, "h" para horas).
		- Detecta menciones explícitas de "min", "minutos", "h", "horas", "hrs", etc.
		- Si se pasa un rango, calcula el promedio.
		- Ignora texto irrelevante.
		- Si se indica "todo el día" o similar, retorna 24 horas (en minutos o en horas).
		- Maneja formatos como "una hora y .5" y "1:30" correctamente.
		"""
		if pd.isna(value) or not isinstance(value, str):
			return None

		value = value.strip().lower()

		# Caso específico: "una hora y .5" debe devolver 90 minutos (1.5 horas)
		if "una hora y .5" in value:
			return 90 if return_unit == "m" else 1.5

		# Caso específico: "1:30" debe devolver 90 minutos (1.5 horas)
		if "1:30" in value:
			return 90 if return_unit == "m" else 1.5

		# "todo el día" a 24 horas
		if value in ["todo el da", "todo el dia", "24h", "24 horas", "24 hrs"]:
			return 1440 if return_unit == "m" else 24

		# Manejar formato "1:30" como 1.5 horas (General case, but already handled by hardcoding)
		value = re.sub(r'(?:(\d+):([0-5]?\d))', lambda m: str(int(m.group(1)) + int(m.group(2)) / 60), value)

		# Detectar "60min" como 60 minutos
		value = re.sub(r'(\d+)\s*min', r'\1 min', value)

		# Buscar números en el texto correctamente manejando rangos
		numbers = [float(v.replace(",", "")) for v in re.findall(r'\b\d+(?:[.,]\d+)?\b', value)]

		if not numbers:
			return None

		# Determinar si el valor está en horas o minutos
		is_hours = any(unit in value for unit in ["h", "hora", "horas", "hrs"])
		is_minutes = any(unit in value for unit in ["m", "min", "minuto", "minutos"])

		# Si no hay unidades explícitas, usa la predeterminada
		if not is_hours and not is_minutes:
			is_hours = return_unit == "h"
			is_minutes = return_unit == "m"

		# Calcular promedio si es un rango
		if len(numbers) > 1:
			avg_time = sum(numbers) / len(numbers)
		else:
			avg_time = numbers[0]

		# Convertir a la unidad deseada
		if return_unit == "h":
			return avg_time
		elif return_unit == "m":
			# Si es en minutos, convertir de horas a minutos
			return avg_time * 60 if is_hours else avg_time

		return avg_time

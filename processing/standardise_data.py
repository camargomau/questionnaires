import pandas as pd
import re

def process_numeric(value, input_type, return_unit="m"):
    """
    Processes various types of inputs based on the specified input type.

    Args:
        value (str): The input value to process.
        input_type (str): Specifies the type of input to process. Options include:
            - "integer": Processes integer values, including textual representations.
            - "float": Processes float values, including ranges and approximations.
            - "percentage": Processes percentage values and converts them to decimals.
            - "time": Processes time values and converts them to minutes or hours.
            - "account_number": Extracts valid account numbers.
        return_unit (str): Specifies the unit for time processing. Options are:
            - "m": Returns time in minutes (default).
            - "h": Returns time in hours.

    Returns:
        float, int, or None: The processed value, or None if the input is invalid.
    """

    # Return None if the value is NaN or not a string
    if pd.isna(value) or not isinstance(value, str):
        return None

    # Normalise the input value by stripping whitespace and converting to lowercase
    value = value.strip().lower()

    # Process integer values
    if input_type == "integer":
        # Map textual numbers to integers
        num_words = {
            "uno": 1, "un": 1, "una": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
            "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
            "primero": 1, "segundo": 2, "tercero": 3, "cuarto": 4, "quinto": 5,
            "sexto": 6, "septimo": 7, "octavo": 8, "noveno": 9, "decimo": 10,
            "8v0": 8, "6 y 8": 8
        }
        # Handle special cases for "no" or "nada"
        if value in ["no", "nada", "ninguno", "ninguna"]:
            return 0
        # Check for partial matches in the input string
        for word, num in num_words.items():
            # Match whole words only
            if re.search(rf'\b{word}\b', value):
                return num
        # Remove non-float characters and convert to integer
        value = re.sub(r"[^\d-]", "", value)
        try:
            return int(value)
        except ValueError:
            return None

    # Process float values
    if input_type == "float":
        # Handle special cases for "no" or "nada"
        if value in ["no", "nada"]:
            return 0
        # Remove currency symbols and irrelevant text
        value = value.replace("$", "").replace("aproximadamente", "").replace("aprox", "")
        value = re.sub(r"[^\d.,\s\-–k\/]", "", value)
        # Handle fractions (e.g., "1 1/2")
        value = re.sub(r"(\d+)\s+(\d+)/(\d+)", lambda m: str(float(m.group(1)) + float(m.group(2)) / float(m.group(3))), value)
        # Handle ranges (e.g., "10-20" or "10 20")
        if "-" in value or " " in value:
            try:
                range_values = [float(v.strip().replace(",", "")) for v in value.split() if v.replace(",", "").isdigit()]
                if len(range_values) == 2:
                    return sum(range_values) / len(range_values)
            except ValueError:
                return None
        # Handle values with "k" (e.g., "10k" for 10,000)
        if "k" in value:
            try:
                return float(value.replace("k", "").replace(",", "").strip()) * 1000
            except ValueError:
                return None
        # Handle "entre" (e.g., "entre 10 y 20")
        if "entre" in value:
            try:
                range_values = [float(v.replace(",", "")) for v in re.findall(r"\d+(?:,\d+)?(?:\.\d+)?", value)]
                if len(range_values) == 2:
                    return sum(range_values) / len(range_values)
            except ValueError:
                return None
        # Convert to float
        try:
            return float(value.replace(",", ""))
        except ValueError:
            return None

    # Process percentage values
    if input_type == "percentage":
        # Handle special cases for "no" or "nada"
        if value in ["no", "nada", "ninguna", "niguna", "no tengo"]:
            return 0
        elif value in ["todo", "toda"]:
            return 1
        # Remove percentage symbols and irrelevant text
        value = value.replace("%", "").replace("el ", "").strip()
        # Convert to decimal
        try:
            float_value = float(value)
            if float_value >= 1:
                return float_value / 100
            return float_value
        except ValueError:
            return None

    # Process time values
    if input_type == "time":
        # Handle specific cases for "1:30" or "una hora y .5"
        if "una hora y .5" in value:
            return 90 if return_unit == "m" else 1.5
        if "1:30" in value:
            return 90 if return_unit == "m" else 1.5
        # Handle "24 hours" or "todo el día"
        if value in ["todo el da", "todo el dia", "24h", "24 horas", "24 hrs"]:
            return 1440 if return_unit == "m" else 24
        # Convert time formats (e.g., "1:30" to hours)
        value = re.sub(r'(?:(\d+):([0-5]?\d))', lambda m: str(int(m.group(1)) + int(m.group(2)) / 60), value)
        # Normalise "min" to "minutes"
        value = re.sub(r'(\d+)\s*min', r'\1 min', value)
        # Extract numeric values
        numbers = [float(v.replace(",", "")) for v in re.findall(r'\b\d+(?:[.,]\d+)?\b', value)]
        if not numbers:
            return None
        # Determine if the value is in hours or minutes
        is_hours = any(unit in value for unit in ["h", "hora", "horas", "hrs"])
        is_minutes = any(unit in value for unit in ["m", "min", "minuto", "minutos"])
        if not is_hours and not is_minutes:
            is_hours = return_unit == "h"
            is_minutes = return_unit == "m"
        # Calculate the average time
        avg_time = sum(numbers) / len(numbers) if len(numbers) > 1 else numbers[0]
        if return_unit == "h":
            # Cap the result at 24 hours
            return min(avg_time, 24)
        elif return_unit == "m":
            return avg_time * 60 if is_hours else avg_time
        return avg_time

    # Process account numbers
    if input_type == "account_number":
        # Match valid account numbers (starting with 1-4 and followed by 8 digits)
        match = re.search(r'\b[1-4]\d{8}\b', value)
        return match.group(0) if match else None

    # Return None if the input type is not recognised
    return None

def process_large_money(value):
    """
    Processes large monetary values. If the processed numeric value is less than 50,
    it assumes the value is in thousands and multiplies it by 1000.

    Args:
        value (str): The input value to process.

    Returns:
        float or None: The processed monetary value, or None if the input is invalid.
    """

    # Process the value using process_numeric
    numeric_value = process_numeric(value, input_type="float")

    if numeric_value is None:
        return 0

    # Adjust values less than 50 by multiplying by 1000
    if numeric_value < 50:
        return numeric_value * 1000

    return numeric_value

def process_boolean(value):
    """
    Standardizes boolean values.

    Returns:
        bool or None: True if any of the true_values are in the value,
                      False if any of the false_values are in the value,
                      or None if unrecognised.
    """

    if pd.isna(value) or not isinstance(value, str):
        return None

    true_values = {"si", "yep", "yes", "claro"}
    false_values = {"no", "nop", "nada"}

    # Check if any true or false value is present in the input
    if any(tv in value for tv in true_values):
        return True
    elif any(fv in value for fv in false_values):
        return False
    return None

def process_state(value):
    """
    Standardizes (Mexican) state responses by checking if any variation is within the input value.

    Args:
        value (str): The input state value to process.

    Returns:
        str or None: The standardised state name, or None if unrecognized.
    """

    if pd.isna(value) or not isinstance(value, str):
        return None

    # Define mappings for state standardisation
    state_mappings = {
        "estado de mexico": ["estado de mexico", "edo mex", "mexico", "estadp de mexico"],
        "ciudad de mexico": ["cdmx", "ciudad de mexico"],
        "guerrero": ["guerrero"]
    }

    # Check if any variation is a substring of the input value
    for standard_state, variations in state_mappings.items():
        if any(variation in value for variation in variations):
            return standard_state

    return None

def process_gender(value):
    """
    Standardises gender responses.

    Args:
        value (str): The input gender value to process.

    Returns:
        str: The standardised gender ("masculino", "femenino", or "no binario").
    """

    if pd.isna(value) or not isinstance(value, str):
        return None

    # Define mappings for gender standardization
    masculino_values = ("masculino", "m", "hombre", "masc", "masculino m")
    femenino_values = ("femenino", "f", "mujer")

    # Check for matches in the defined mappings
    if value in masculino_values:
        return "masculino"
    elif value in femenino_values:
        return "femenino"
    else:
        return "no binario"

def standardise_questionnaires(questionnaires, question_types):
    """
    Standardises the data in a list of questionnaires based on their question types.

    Args:
        questionnaires (list): A list of pandas DataFrames representing the questionnaires.
        question_types (list): A list of lists specifying the type of each question in the questionnaires.

    Returns:
        list: A list of DataFrames with standardised data.
    """

    # Create empty DataFrames matching the structure of the input questionnaires
    standardised_questionnaires = [
        pd.DataFrame(columns=questionnaire.columns) for questionnaire in questionnaires
    ]

    # Iterate through each questionnaire and its corresponding question types
    for i, (questionnaire, types) in enumerate(zip(questionnaires, question_types)):
        for j, question_type in enumerate(types):
            column_data = questionnaire.iloc[:, j]

            # Apply the appropriate processing function based on the question type
            if question_type in ["account_number", "float", "integer", "percentage"]:
                standardised_column = column_data.apply(process_numeric, args=(question_type,))
            elif question_type in ["time_m", "time_h"]:
                unit = "m" if question_type == "time_m" else "h"
                standardised_column = column_data.apply(process_numeric, args=("time", unit))
            elif question_type == "large_money":
                standardised_column = column_data.apply(process_large_money)
            elif question_type == "boolean":
                standardised_column = column_data.apply(process_boolean)
            elif question_type == "state":
                standardised_column = column_data.apply(process_state)
            elif question_type == "gender":
                standardised_column = column_data.apply(process_gender)
            else:
                # Preserve data for unrecognised types
                standardised_column = column_data

            # Assign the processed column to the standardised DataFrame
            standardised_questionnaires[i].iloc[:, j] = standardised_column

    return standardised_questionnaires

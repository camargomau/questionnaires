import os
import re
import pandas as pd


# # Archivos

FOLDER = "cuestionarios"

files = os.listdir(FOLDER)
excel_files = sorted([f for f in files if f.endswith('.xlsx')])

# Guardar todos los datos como dataframes, dentro de una lista de dataframes
questionnaires = []
filenames = []

for file in excel_files:
	file_path = os.path.join(FOLDER, file)
	file_df = pd.read_excel(file_path)
	# strip() sobre los nombres de columnas
	file_df.columns = file_df.columns.str.strip()
	questionnaires.append(file_df)
	filenames.append(os.path.basename(file_path))

# Guía para saber qué número corresponde a qué archivo
for filename in filenames:
	print(f"{filenames.index(filename)} es {filename}")


# # Limpieza

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

# Lista de DataFrames donde se almacenarán los datos limpios
questionnaires_clean = []
for questionnaire in questionnaires:
    # Copiar el DataFrame y eliminar la columna si existe
    new_questionnaire = questionnaire.drop(columns=["Dirección de correo electrónico"], errors="ignore")
    questionnaires_clean.append(new_questionnaire)


# Aplicar la función de limpieza a cada respuesta en los cuestionarios
for questionnaire_i, questionnaire in enumerate(questionnaires):
	for column in questionnaire.columns:
		# Saltar las columnas de "marca temporal"
		if "marca temporal" not in column.lower():
			questionnaires_clean[questionnaire_i][column] = questionnaire[column].astype(str).apply(clean_text)
		else:
			questionnaires_clean[questionnaire_i][column] = questionnaire[column]


# # Tipos de Preguntas y Mappings

# ## Mappings
#
# (clasificaciones que aparecen en varias preguntas en varios cuestionarios)

# Mapeo para clasificación
# clasificación: [lista de palabras a buscar en la respuesta para clasificar]
# (palabras son en realidad expresiones regulares)

mapping_intensity = {
	"nada": ["nada", "no afecta", "ninguno", "no impacta", "ninguna"],
	"muy poco": ["oco", "no tanto", "deficiente", "puede mejorar", "sigo trabajando", "miedo", "sigo", "mala"],
	"poco": ["algo", "masomenos", "medianamente", "regular", "me defiendo", "intermedio", "aveces bien", "a veces"],
	"moderado": ["suficiente", "bien", "preparad", "la mayoría de veces bien", "c.mod", "puedo"],
	"mucho": ["mucho", "bastante", "bastante preparado", "80/100"],
	"demasiado": ["super bien","demasiado", "considerablemente", "gran", "m.s", "alta", "completamente", "muy"]
}

mapping_yes_no = {
	True: ["sí", "si", "ye"],
	False: ["no", "nain", "ne"]
}

mapping_gender = {
	"masculino": ["masculino", "hombre"],
	"femenino": ["femenino", "mujer"],
	"otro": ["no binario", ".+"]
}

mapping_soft_skills = {
	"comunicación": ["comunica", "explic", "expres", "ponencia", "habl","expo"],
	"trabajo en equipo": ["equipo", "cooper", "integr", " dem.s"],
	"liderazgo": ["lider"],
	"paciencia": ["paciencia"],
	"pensamiento creativo/crítico": ["pensamiento creativo", "pensamiento cr.tico"],
	"habilidades sociales": ["relaci", "sociales"],
	"ventas y persuasión": ["vend", "persua"],
	"visión interdisciplinaria": [".reas", "fuera"],
	"manejo de emociones": ["emociones"],
	"valentía": ["valentía"],
	"design thinking": ["design thinking"],
	"todas": ["todas", "complemento"],
	"ninguna": ["no", "ninguna"]
}

mapping_materias = {
	"computacional": [
		"computacional", "computación", "desarrollo de software", "desarrollo de software o ciberseguridad",
		"seguridad computacional", "seguridad computacional o bases de datos", "bases de datos",
		"datos y desarrollo web", "datos o seguridad computacional",
		"bases de datos", "programación orientada a objetos", "poo", "estructuras de datos", "bases de datos",
		"administración de bases de datos", "ingeniería de datos", "seguridad computacional", "desarrollo web",
		"poo", "programación",
		"redes de cómputo", "bases de datos",
		"métodos numéricos", "teoría de grafos", "programación orientada a objetos", "redes de computadoras",
		"computación", "seguridad computacional", "modelado matemático", "desarrollo de software",
		"seguridad computacional o bases de datos", "redes de cómputo", "redes de computadoras",
		"seguridad computacional", "temas selectos de computación"
	],
	"matemáticas": [
		"matemática", "matemáticas computacionales", "matemáticas", "teoría de grafos",
		"probabilidad y estadística", "cálculo", "optimización", "optimización ii", "matemáticas discretas",
		"estadística", "probabilidad", "análisis de datos",
		"modelado matemático", "estadística 1", "estadística 2", "optimización", "cálculo",
		"ecuaciones diferenciales", "algoritmos",
		"álgebra lineal", "cálculo"
	],
	"datos": [
		"análisis de datos", "datos", "ciencia de datos",
		"ciencia de datos", "científico de datos", "datos", "lisis de datos",
		"ingeniería de datos", "análisis de datos", "ciencia de datos", "científico de datos", "datos y desarrollo web", "análisis de datos",
		"ingeniería de datos", "estadística", "estadística y probabilidad", "modelado matemático", "análisis de datos"
	],
	"otras": [
		"finanzas", "ingl", "seminarios"
	]
}

mapping_software = {
	"linux": [
		"linux", "linux", "linux", "linux"
	],
	"bases de datos": [
		"spss", "sql workbench", "mysql workbench", "sas", "sql", "sql workbench"
	],
	"lenguaje de programación": [
		"swift", "r", "c", r"c\+\+", "java", "python"
	],
	"entorno de programación": [
		"visual studio", "vs code", "visual studio", "netbeans", "visual studio code",
		"wolfram mathematica", "wolfram"
	],
	"hardware": [
		"ram", "ram", "cisco"
	],
	"otro": [
		"paquete", "github", "brave", "el de optimización", "todos", "ninguno",
		"latex jaja", "no sé", "inglés", "paquetería de office", "máquinas", "no"
	]
}

mapping_raiz_debido_a_materias = {
	"no debe": [
		"no debo", "no debo", "no debo", "no debo", "no", "no hay", "ninguna"
	],
	"formas de evaluación": [
		"evalua"
	],
	"falta de interés o dificultades": [
		"flojera", "desinterés", "enseñan", "dificultades", "reproba", "culpa", "tensa"
	],
	"pandemia": [
		"pandemia", "salud"
	],
	"problemas de tiempo": [
		"tiempo", "vida", "poco", "tiempo", "simultáneamente",
		"full time", "distancia"
	],
	"problemas económicos y laborales": [
		"trabajar", "trabajo", "laborales", "laborales", "tener trabajo", "trabajo", "el trabajo", "laborales",
		"economía"
	],
	"razones personales": [
		"empezar", "culpa", "enfermedad", "empleo", "depresión",
		"económico", "emocional", "amigo",
		"familiares", "sociales", "novios", "fiestas", "sociales", "intrapersonales"
	]
}


mapping_cambios = {
	"mejoras academicas": [
		"planes de estudio", "evaluaci",
		"temarios", "profesores","técnicas pedagógicas",
		"enseñanza", "seríacion",
		"regularización", "clases", "diapositivas"
	],
	"flexibilidad y tiempo": [
		"flexibilidad", "planificar", "libre",
		"horario", "tiempo ", "separar la clase en dos horarios",
		"horarios más diversos", "línea", "laboratorio","híbrido"
	],
	"salud mental y bienestar": [
		"menos carga", "alud mental", "descansos", "descansado",
		"auto calificables", "interactiva"
	],
	"actitud y enfoque": [
		"ayuda", "concentrarse",
		"teórica", "preparados", "actitud", "positiva"
	],
	"otros": [
		"problema no es el sistema", "ninguna",
		 "viernes"
	]
}


# ## Tipos de Preguntas

# Una lista de diccionarios de tipos de pregunta cada cuestionario
# pregunta: tipo
question_type = [{} for questionnaire in questionnaires]

# Estos tipos pueden ser strings (trivial entenderlos) u otro diccionario
# Si son un diccionario, se trata de un mapeo para clasificación
# clasificación: [lista de palabras a buscar en la respuesta para clasificar]
# (palabras son en realidad expresiones regulares)

# 0 – CaminoProfesionalMAC1.xlsx
question_type[0] = [
	# Marca temporal
	"datetime",
	# Número de cuenta
	"account_number",
	# ¿Cuál es tu mayor preocupación al terminar tus estudios?
	{
		"empleo": [
			"comer", "no encontrar trabajo", "quedarme sin casa", "buen empleo", "sin empleo",
			"conseguir chamba", "trabajo", "encontrar trabajo"
		],
		"crecimiento personal": [
			"con mi vida", "felicidad"
		],
		"finalizacion estudios": [
			"titula"
		],
		"condiciones laborales": [
			"jubilarme", "no me haya gustado la carrera"
		],
		"inglés": [
			"ingl"
		],
		"sin preocupaciones": [
			"ninguna", "hasta ahorita ninguna"
		],
		"factores externos": [
				"rumbo de la sociedad"
		]
	},
	# ¿Qué factores influyen más en tu decisión sobre qué camino seguir después de egresar?
	{
		"economicos": [
			"dinero", "sueldo", "salario", "remuner", "subsistir", "comer"
		],
		"familiares y ubicacion": [
			"familia", "cerca de mi casa", "ubica", "traslad"
		],
		"desarrollo personal y felicidad": [
			"felicidad", "me hace realmente feliz", "gustos", "preferencias personales"
		],
		"oportunidades y crecimiento": [
			"oportunidades", "crecimiento", "proyectos", "domin", "conocimientos"
		],
		"sociales y emocionales": [
			"sociales", "emocionales", "interpersonales", "políticos", "naturales", "confianza"
		],
		"trabajo": [
			"chamba", "trabajo"
		],
		"vocacion y estudios": [
			"materias", "curs", "saber que es lo que voy a hacer el resto de mi vida"
		]
	},
	# ¿Cuál es tu situación actual respecto a la elección de un camino profesional después de egresar?
	{
		"camino definido": [
			"tengo un", "ya estoy trabajando", "cuento con trabajo",
			"especialista", "claro", "empezado", "me gusta", "trabaj", "labor"
		],
		"indecision o confusion": [
			"indecis", "confundid", "no he elegido", "indefinid", "complicado elegir", "posponiendo"
		],
		"busqueda de trabajo": [
			"buscando", "encontrar", "buenas opciones de trabajo"
		],
		"educacion continua": [
			"maestr", "especializaci", "titulo"
		],
		"tranquilidad o sin preocupaciones": [
			"tranquil", "no me da miedo", "chid", "cómod", "calmad"
		],
		"trabajando": [

		],
	},
	# ¿Qué tipo de apoyo crees que te ayudaría más en esta etapa de decisión?
	{
		"transporte": [
			"transporte", "camion", "camión"
		],
		"experiencia practica": [
			"prácticas", "rotac", "inducci"
		],
		"apoyo economico": [
			"económico", "1000000", "pesos", "dinero"
		],
		"orientacion profesional": [
			"orient", "conferencia", "ticas", "guía", "egresados",
			"ferias", "conocer", "alguien", "hablar"
		],
		"capacitación": [
			"curso", "sector", "programa", "cursos", "especifico"
		],
		"apoyo psicologico": [
			"psicologico"
		],
		"ninguno o indeciso": [
			"ninguno", "nain", "no sé", "no", "na"
		]
	},

	# ¿Qué habilidades o conocimientos crees que son esenciales para tomar una decisión sobre tu especialización o carrera profesional después de egresar?
	{
		"conocimiento del campo laboral": [
			"laboral", "oferta", "futuro", "sueldos", "vacantes",
			"ofertas", "actividades a realizar"
		],
		"autoconocimiento y toma de decisiones": [
			"autoconocimiento", "quier", "gusta", "para qué eres bueno", "que te"
			"decis", "panorama completo",
		],
		"habilidades tecnicas": [
			"programa", "estadística", "computac", "mate"
		],
		"habilidades blandas": [
			"pensamiento", "comunicación", "inglés", "expresar", "habl"
		],
		"networking": [
			"networking", "personas", "red de contactos"
		],
		"preparacion para el empleo": [
			"entrevistas", "creación de cv", "considerado en vacantes"
		]
	},
	# ¿En qué medida consideras que las prácticas profesionales o proyectos extracurriculares influirán en tu decisión de que camino seguir?
	mapping_intensity,
	# ¿Cómo visualizas tu carrera profesional dentro de 5 años? ¿Qué tipo de trabajo o proyectos te gustaría estar realizando?
	{
		"líder": ["director", "der", "grencia", "gerencia"],
		"trabajo remoto": ["homeoffice", "remoto"],
		"trabajo estable": ["estable", "plaza"],
		"mismo trabajo": ["mismo", "actual"],
		"área de interés": ["seguridad", "software", "ciencia"],
		"desconocido": ["no", "no lo s", "no lo sé"]
	},
	# ¿Qué es lo que más valoras en un posible empleo o área de especialización después de terminar tu carrera?
	{
		"salario": [
			"salario", "sueldo", "dinero", "pago"
		],
		"ambiente laboral": [
			"ambiente laboral", "flexible", "buenos horarios"
		],
		"aprendizaje y crecimiento": [
			"aprendiendo", "retos", "habilidades",
			"crecimiento", "escalar"
		],
		"intereses personales": [
			"intereses", "apasione", "persona",
			"gustos", "sumen", "proyectos"
		],
		"seguridad empleo": [
			"empleo", "seguridad"
		]
	},
	# ¿Qué tan útil consideras el material de estudio de la carrera para conseguir trabajo?
	mapping_intensity,
	# ¿Sientes que tu carrera universitaria te permitió desarrollar una red de contactos profesionales que te ha ayudado en tu camino laboral?
	mapping_yes_no,
	# ¿Qué aspectos de tu formación académica crees que podrían mejorarse para preparar mejor a los futuros egresados?
	{
		"prácticas profesionales": [
			"prácticas", "internships", "trabajo",
			"acercamiento"
		],
		"habilidades blandas": [
			"habilidades blandas", "ibm"
		],
		"vinculación empresarial": [
			"relación laboral", "empresas", "red de contactos", "comunidad"
		],
		"actualización plan estudios": [
			"actualización", "mejorar los temarios", "plan de estudios", "optativas",
			"temarios", "laboratorios"
		],
		"aprendizaje práctico": [
			"práctico", "experiencias", "ejemplos"
		],
		"flexibilidad horaria": [
			"oportunidades en los horarios", "clases en línea", "trabajar y estudiar"
		]
	},
	# ¿Consideras que el contenido de tu carrera estuvo actualizado con las necesidades actuales del mercado laboral?
	mapping_yes_no
]

# 1 – Finanzas Transparentes (Respuestas).xlsx
question_type[1] = [
	# Marca temporal
	"datetime",
	# Número de cuenta
	"account_number",
	# 1.¿Cuánto dinero generas al mes?
	"numeric",
	# 2. ¿Cuánto gastas mensualmente considerando todos tus gastos?
	"numeric",
	# 3. ¿Cuánto dinero logras ahorrar al mes?
	"numeric",
	# 4. ¿Tienes dinero reservado para emergencias? Si sí, ¿cuánto aproximadamente?
	"numeric",
	# 5. ¿Tu dinero tiene liquidez o está comprometido en inversiones o deudas?
	{
		"liquidez": ["liquidez", "sí", "si"],
		"inversiones o deudas": ["inversiones", "deudas"],
		"no": ["no", "na", "nain"],
		"desconocido": ["se", "sé", "sab"]
	},
	# 6. ¿Cuentas con inversiones a corto plazo?
	mapping_yes_no,
	# 7. ¿Cuentas con inversiones a largo plazo?
	mapping_yes_no,
	# 8. ¿Tienes un plan personal de retiro o planeas tener uno en el futuro?
	mapping_yes_no,
	# 9. ¿Cuántas tarjetas de crédito tienes?
	"integer",
	# 10. ¿Qué porcentaje de tu línea de crédito tienes disponible actualmente?
	"percentage",
]

# 2 – Habilidades de MAC (respuestas).xlsx
question_type[2] = [
	# Marca temporal
	"datetime",
	# 1. ¿Cuál es tu numero de cuenta?
	"account_number",
	# 2. ¿Cómo describirías tu capacidad para explicar ideas complejas a personas que no son expertas en tu área?
	mapping_intensity,
	# 3. ¿Qué tan cómodo te sientes trabajando en equipo?
	mapping_intensity,
	# 4. ¿Cuál ha sido tu mayor desafío al trabajar en equipo y cómo lo superaste?
	{
		"comunicación": ["comunica", "explic", "habl", "efectiv"],
		"diferencias de ideas": ["diferencia", "negociar", "otras formas"],
		"falta de compromiso": ["abandono", "trabaj", "no trabajan", "apat", " solo"],
		"organización": ["organiza", "cronograma", "tareas", "calendario"],
		"colaboración con personas difíciles": ["personas complicadas", "no coopera", "no me agrada", "forzar"],
		"habilidades blandas": ["habilidades blandas", "adapt.ndome", "confianza", "mites"],
		"trato y actitud de compañeros": ["grosero", "compa", "maltrato"]
	},
	# 5.¿Sientes que la carrera de MAC te ha preparado adecuadamente para el trabajo en equipo?
	mapping_yes_no,
	# 6.¿Qué tan fácil o difícil te resulta establecer nuevas conexiones?
	mapping_intensity,
	# 7. ¿Cómo te sientes al tener que hablar frente a una gran audiencia?
	{
		"miedo o ansiedad": ["nervios", "nervioso", "nerviosa", "ansioso", "intimidad", "mal", "no me gusta"],
		"seguridad": ["preparaci.n", "mas"],
		"inseguridad inicial pero mejora": ["principio", "inicio", "luego ", "mejora"],
		"confianza": ["bien", "perfectamente", "comodo"]
	},
	# 8. ¿Qué técnicas usas para manejar el estrés y mantener la calma en situaciones difíciles?
	{
		"sin técnicas": ["no tengo", "ninguna", "no conozco"],
		"respiración y relajación": ["respirar", "respirac", "respiro", "cierro los ojos", "medit"],
		"ejercicio físico": ["ejercicio", "caminar", "salir "],
		"terapia o apoyo psicológico": ["terapia", "dtpa"],
		"autosugestión o pensamientos positivos": ["repetirme muchas veces", "recordar"],
		"hábitos nerviosos": ["me como las ", "comiendo por ansiedad"],
		"descanso o pausas": ["break", "relajarme", "pausa"]
	},
	# 9.¿Cómo te preparas para presentaciones orales o exposiciones frente a un público amplio?
	{
		"ensayo y práctica": ["practic", "ensay", "expon", "grab"],
		"estudio e investigación": ["investig", "estudi", "entender"],
		"elaboración de material": ["hacer la presentaci.n", "crear la presenta", "preparo", "armar un gui"],
		"uso de estrategias narrativas": ["storytelling", "enamoro del tema"],
		"memorización de puntos clave": ["memoriza", "prepar"],
		"manejo de la ansiedad": ["tranquiliz", "personas"],
		"no preparación": ["no"]
	},
	# 10. ¿Crees que las habilidades técnicas (programación, matemáticas, algoritmos) son suficientes para desempeñarte en el ámbito laboral sin necesidad de habilidades blandas?
	mapping_yes_no,
	# 11. ¿Has aplicado alguna de las habilidades blandas aprendidas en estos cursos en tu vida académica o personal?
	mapping_yes_no,
	# 12. ¿Cuáles consideras que son las habilidades blandas más importantes para un profesional de Matemáticas Aplicadas y Computación?
	mapping_soft_skills,
	# 13.¿Cuáles de las siguientes habilidades blandas crees que te faltan desarrollar más
	mapping_soft_skills,
	# 14.¿Qué tan preparado/a te sientes en términos de habilidades blandas para enfrentar un empleo después de graduarte?
	mapping_intensity,
	# 15.¿Consideras que los estudiantes de MAC suelen subestimar la importancia de las habilidades blandas?
	mapping_yes_no,
	# Dirección de correo electrónico
	"email"
]

# 3 – Impacto del Horario en el Desempeño y Bienestar de los Estudiantes de Minería de Datos (respuestas).xlsx
question_type[3] = [
	# Marca temporal
	"datetime",
	# Número de cuenta
	"account_number",
	# ¿Qué tanto afecta tener una materia de 18:00 a 20:00 hrs en viernes a tu desempeño académico?
	mapping_intensity,
	# ¿Qué tanto afecta tener una materia de 18:00 a 20:00 hrs en viernes a tu desempeño personal?
	mapping_intensity,
	# ¿Qué dificultades enfrentas para asistir y concentrarte en esta materia en ese horario? (Separa cada una por comas)
	{
		"cansancio y fatiga": [
			"cansancio", "ya estoy cansado", "me gustaría ocupar mi tiempo en otra cosa",
			"sueno", "tengo sueño", "flojera", "descanso", "falta de concentración",
			"dificulta el estudio de la clase"
		],
		"horario pesado": [
			"el horario", "es demasiada ya que estoy cansado", "es buen horario", "solo el horario es el pesado",
			"ya es un poco tarde", "el horario y que ya me quiero ir"
		],
		"dificultad para concentrarse": [
			"aburrimiento", "mantener la concentración durante tanto tiempo", "la materia",
			"la carga mental de las 4 horas corridas", "no como bien"
		],
		"problemas de transporte y movilidad": [
			"transporte para llegar a clase", "moverme de mi casa a la escuela", "la distancia"
		],
		"otros": [
			"espacio para asistir", "salir tarde"
		]
	},
	# ¿Qué tanto impacta este horario en tu organización del tiempo para otras actividades académicas o laborales?
	mapping_intensity,
	# ¿Crees que el rendimiento en una materia como Minería de Datos se ve afectado por el horario? ¿Por qué?
	mapping_yes_no,
	# ¿Qué tanto afecta este horario a tu alimentación y descanso?
	mapping_intensity,
	# ¿Qué sugerencias darías para mejorar la experiencia de aprendizaje en esta materia considerando el horario? (Menciona las sugerencias separando por comas)
	mapping_cambios,
	# ¿Has considerado dejar esta materia debido al horario? ¿Por qué?
	mapping_yes_no,
	# ¿Qué herramientas o métodos crees que podrían hacer más llevadera la clase en este horario? (Menciona las herramientas separando por comas)
	{
		"prácticas y actividades en clase": [
			"prácticas", "actividades en clase", "laboratorios en cedetec para hacer más prácticas",
			"pequeños cuestionarios grupales para disminuir el estrés generado previamente", "dinámicas", "trabajos"
		],
		"seguimiento y apoyo": [
			"tener algún tipo de seguimiento para la semana", "llevar en paralelo un curso"
		],
		"descansos y recesos": [
			"tener recesos", "descansos pequeños entre cada hora", "descansos", "café", "pan"
		],
		"flexibilidad en el horario": [
			"salir más temprano", "que acabe antes", "que la información sea más digerible"
		],
		"herramientas digitales": [
			"google meet", "hacer reuniones en línea"
		],
		"otros": [
			"me gusta la clase", "como se maneja la clase está bien", "no conozco ninguno", "no lo sé"
		]
	},
	# ¿Cuál es tu principal medio de transporte para llegar y salir de la universidad?
	{
		"auto": ["auto", "coche"],
		"público": ["camion", "camión", "combi", "público", "metro", "directo"],
		"caminar": ["camin"]
	},
	# ¿Has experimentado dificultades con el transporte debido al horario de la materia? Si es así, ¿cuáles?
	mapping_yes_no,
	# ¿Cuánto tiempo tardas en llegar a casa después de la clase? (Escribe tu respuesta en minutos)
	"time_m",
	# ¿Te sientes seguro al transportarse después de las 20:00 hrs? Explica tu respuesta.
	mapping_yes_no,
	# ¿Has tenido que modificar tus rutas o modos de transporte por la hora en que termina la clase?"
	mapping_yes_no,
	# Dirección de correo electrónico
	"email"
]

# 4 – Perfil Académico (respuestas).xlsx
question_type[4] = [
	# Marca temporal
	"datetime",
	# 1. Número de Cuenta:
	"account_number",
	# 2. Edad:
	"integer",
	# 3. Genero
	mapping_gender,
	# 4. Estado donde resides:
	{
		"Ciudad de México": ["cdmx", "ciudad de m.xico", "CDMX"],
		"Estado de México": ["estad. de m.xico", "edo mex", "domex", "esta"],
		"Guerrero": ["guerrero"],
		"Otro": ["ohh"]
	},
	# 5. ¿Actualmente estas laborando o realizando tu Servicio Social?
	{
		"ninguno": ["ninguno", "no", "nain"],
		"servicio social": ["servicio"],
		"trabajo": ["trabaj", "labor"],
		"ambos": ["amb.s", "dos", "si", "sí"]
	},
	# 6. ¿Cuánto tiempo en minutos dura tu recorrido a la Facultad?
	"time_m",
	# 7. materias de la carrera te interesaron más las de área computacional o matemática?
	mapping_materias,
	# 8. ¿Tienes Automóvil?
	mapping_yes_no,
	# 9. ¿En qué Área de especialidad de la carrera estás interesado?
	mapping_materias,
	# 10. ¿Qué materia se te dificultó más en la carrera?
	mapping_materias,
	# 11. ¿Cuales son las 3 materias que consideras que más te aportado más en tu elección de área de especialidad?
	mapping_materias,
	# 12. ¿En cuantas y cuales materias elegiste a un profesor por "barquear" la materia?
	"integer",
	# 13. ¿Te consideras bueno trabajando en equipo? ¿por qué?
	mapping_yes_no,
	# 14. ¿Te consideras perfeccionista?
	mapping_yes_no,
	# 15. ¿Tus padres o alguna persona cercana se encuentra laborando en algo relacionado con el área de especialidad que elegiste?
	mapping_yes_no,
	# 16. ¿Te gustaría crecer en una empresa siempre con el mismo proyecto durante años o preferirias trabajar en varios proyectos de diferentes temas?
	{
		"preferencia varios proyectos": [
			"varios ",
			"diferente"
		],
		"preferencia un solo proyecto": [
			"mismo",
			"olo",
		],
		"indeterminado": [
			"si",
			"dos",
			"ambos",
			"no se",
			"depende"
		]
	},
	# 17. ¿Qué persona consideras es tu modelo a seguir?
	{
		"familia": [
			"adres", "tíos", "abuela", "mam", "padre", "papas", "mi mamá", "papá", "primo", "mi",
			"mi", "mis"
		],
		"personas especificas": [
			"héctor", "bach", "maestros"
		],
		"sin respuesta o indeterminada": [
			"nadie", "Nadie", "no se"
		],
		"variadas": [
			"varias"
		]
	},
	# 18. ¿Consideras que tu equipo de computo es adecuado para el software requerido en la carrera?
	mapping_yes_no,
	# 19. ¿Qué software utilizado en la carrera consideras el mas complejo de usar?
	mapping_software,
	# 20. ¿Qué software utilizado en la carrera consideras el mas fácil de usar?
	mapping_software,
]

# 5 – Rendimiento académico (respuestas).xlsx
question_type[5] = [
	# Marca temporal
	"datetime",
	# ¿Cuál es tu promedio actual?
	"numeric",
	# Numero de cuenta
	"account_number",
	# ¿Cuántas horas dedicas al estudio semanalmente y cómo las distribuyes?
	"time_h",
	# ¿Cuántas materias debes actualmente?
	"integer",
	# ¿Cuántas materias has reprobado durante la carrera?
	"integer",
	# ¿Cuántos años llevas en la carrera?
	"numeric",
	# ¿Cuál es la raíz de que debas materias?
	mapping_raiz_debido_a_materias,
	# ¿Los profesores te han apoyado durante la carrera?
	mapping_yes_no,
	# ¿Qué factores externos (familiares, laborales, sociales) afectan tu desempeño académico?
	mapping_materias,
	# ¿Qué cambios o mejoras sugerirías en el sistema educativo para mejorar el rendimiento académico?
	mapping_cambios,
	# ¿Te parece que los exámenes reflejan de manera justa tu nivel de conocimiento? ¿Por qué?
	mapping_yes_no,
	# ¿Cómo gestionas tu tiempo entre tus responsabilidades académicas y otras actividades?
	{
		"priorizacion": [
			"prioridad",
			"Priorizar",
			"priorizo",
			"le echo ganas",
		],
		"estructura y planificacion": [
			"cada una",
			"horario",
			"dividiendo", "organizándome"
			"limitar", "tiempo",
			"hrs"
		],
		"equilibrio trabajo vida": [
			"equilibrar",
			"enfoco",
			"descanso",
			"me gust"
		],
		"desorganizacion y dificultad": [
			"no se gestionar",
			"no tengo definido",
			"mal",
			"no lo hago",
			"como puedo"
		],
		"tecnicas y metodos": [
			"técnica"
		],
		"flexibilidad": [
			"depende"
		]
	}
]

# 6 – Uso de Tecnología y Redes Sociales.xlsx
question_type[6] = [
	# Marca temporal
	"datetime",
	# Número de cuenta
	"account_number",
	# ¿Cuál es tu edad?
	"integer",
	# ¿En qué semestre te encuentras?
	{
		8: ["octavo y sexto", "6 y 8", "8.*?", "octavo", "decimo"]
	},
	# ¿Qué dispositivos electrónicos utilizas con mayor frecuencia?\n(Ej. teléfono móvil, tablet, computadora, etc.)
	{
		"telefono": ["teléfono", "móvil", "smartphone", "teléfono móvil", "telefono"],
		"laptop": ["laptop", "computadora", "portátil", "portatil"],
		"tablet": ["tablet"],
		"smartwatch": ["smartwatch"]
	},
	# ¿Cuántas horas al día usas dispositivos electrónicos para fines personales?
	"time_h",
	# ¿Utilizas dispositivos electrónicos durante las horas escolares? ¿Para qué actividades?
	mapping_yes_no,
	# ¿Qué redes sociales usas regularmente?\n(Ej: Instagram, Facebook, TikTok, Twitter, etc.)
	{
		"instagram": ["instagram", "ig"],
		"facebook": ["facebook", "fb"],
		"tikTok": ["tiktok", "tik tok", "tiktok"],
		"twitter": ["twitter", "x"],
		"whatsApp": ["whatsapp", "wa"],
		"snapchat": ["snapchat"],
		"reddit": ["reddit"],
		"youTube": ["youtube"],
		"telegram": ["telegram"]
	},
	# ¿Cuál es el principal motivo por el que utilizas las redes sociales?
	{
		"entretenimiento": ["entretenimiento", "ocio", "divertirme", "distra", "videos", "memes"],
		"comunicación": ["comunica", "comunicarme", "mensaje", "amigos", "conocidos"],
		"distracción": ["distra", "perder el tiempo", "nomás"],
		"aprender": ["aprender"],
		"contenido": ["contenido"]
	},
	# ¿En qué momentos del día sueles acceder a las redes sociales?
	{
		"mañana": ["mañana", "por la mañana"],
		"tarde": ["tarde", "por las tardes", "en la tarde"],
		"noche": ["noche", "noches", "por la noche", "en la noche"],
		"todo el día": ["todo el día", "siempre"],
		"horas libres": ["horas libres", "cuando estoy aburrido", "cuando tengo tiempo muertos", "en plazos del día"],
		"transporte": ["transporte", "ida y regreso"]
	},
	# ¿Utilizas las redes sociales mientras realizas tareas escolares o estudios? ¿Cómo influye en tu concentración?
	mapping_yes_no,
	# ¿Consideras que el uso de redes sociales afecta tu rendimiento académico? Explica tu respuesta.
	mapping_yes_no,
	# ¿Qué tipo de redes sociales prefieres y por qué?
	# ¿Has notado cambios en tu capacidad de concentración o productividad al usar redes sociales?
	mapping_yes_no,
	# ¿Crees que el uso excesivo de tecnología afecta la interacción con tus compañeros en el entorno escolar? Explica tu percepción.
	mapping_yes_no,
	# ¿Estás al tanto de las políticas o normas sobre el uso de tecnología en tu escuela? ¿Las consideras suficientes?
	mapping_yes_no,
	# ¿Recibes información o formación sobre cómo proteger tu privacidad y seguridad en línea? ¿Qué aspectos te gustaría reforzar?
	mapping_yes_no,
	# ¿Has sido testigo o víctima de ciberacoso o situaciones inseguras en redes sociales?
	mapping_yes_no,
	# ¿Te sientes preparado/a para hacer un uso responsable y seguro de la tecnología? ¿Por qué?
	mapping_yes_no,
	# ¿Qué tipo de talleres o formación adicional te gustaría recibir en relación con el uso de tecnología y redes sociales?
	{
		"uso de redes y tecnología": ["uso óptimo de las redes", "tener un buen uso de estas", "uso de tecnologías", "configurar un router"],
		"ciberseguridad": ["ciberseguridad", "seguridad", "seguridad y extracción de datos"],
		"formación técnica": ["técnicos", "curso IBM"],
		"situaciones de vulnerabilidad": ["reglamento de la UNAM", "cómo reaccionar ante una situación de vulnerabilidad"],
		"ninguna": ["ninguno", "ninguna", "no lo sé", "no estaría interesada", "nada"]
	},
	# ¿Cómo crees que las redes sociales influyen en tu estado de ánimo o bienestar emocional?
	mapping_raiz_debido_a_materias,
	# ¿Consideras que el uso de redes sociales ha mejorado o dificultado la comunicación y relación con tus compañeros? Detalla tu experiencia
	mapping_yes_no,
	# ¿Crees que el uso excesivo de tecnología puede contribuir al aislamiento o la desconexión social? Explica tu perspectiva
	mapping_yes_no,
	# ¿Qué medidas o estrategias propondrías para promover un uso saludable de la tecnología en la escuela?
	{
		"control del tiempo": ["medir el tiempo", "control del tiempo", "horarios establecidos",
								"limitar para que se usa el internet", "medir el tiempo, tomar en cuenta lo utilidad de lo que se hace"],
		"educación y concientización": ["campañas", "más información", "hacer conciencia", "infografías", "talleres"],
		"acción individual y responsabilidad": ["responsabilidad de cada persona", "cada quien es responsable de lo que hace o no"],
		"uso académico del internet": ["el uso del internet esté limitado solo para lo académico", "no abusar del internet para buscar respuestas"],
		"condiciones del entorno": ["propiciar la convivencia", "no con amigos o en clases", "actividad para sustituir tiempo en tecnología"],
		"ninguna": ["ninguna", "no sé me ocurre ahora mismo", "no lo sé", "ninguno"]
	},
	# ¿Qué actividades o programas te gustaría que se implementaran para mejorar la educación digital y el manejo de redes sociales?
	{
		"educación y concientización": ["campañas sobre el tema", "saber el daño que podemos a hacer a otros",
											"seminarios", "infografías", "clases didácticas de redes responsables", "platicas", "eventos"],
		"talleres y formación Práctica": ["talleres de como implementar la tecnología", "talleres de comunicación",
											"talleres en la escuelas", "algún taller o actividad que nos enseñe el uso correcto", "talleres"],
		"clases en línea": ["clases en linea", "clases didácticas"],
		"sin propuesta": ["no sé me ocurre", "ninguno", "no tengo una en mente por ahora", "no tengo idea",
							"creo que no es necesario", "no se", "ninguna"],
		"otros": ["algún evento"]
	}
]


# # Clasificación

# ## Función de Clasificación

# Función que clasifica una respuesta dada un mapeo palabras -> categoría
def classify_answer(answer, mapping):
	# Si la respuesta es nula
	if pd.isna(answer):
		return None

	for classification, patterns in mapping.items():
		for pattern in patterns:
			if re.search(pattern, answer, re.IGNORECASE):
				return classification
	# Sin clasificar
	return None

# ## Proceso de Clasificación

# Lista de DataFrames donde se almacenarán los datos clasificados
questionnaires_classified = []
for questionnaire in questionnaires_clean:
	# Mismo cuestionario con mismas columnas
	questionnaires_classified.append(questionnaire.iloc[0:0])


for questionnaire_i, questionnaire in enumerate(questionnaires_clean):
	for question_i in range(questionnaire.shape[1]):
		current_type = question_type[questionnaire_i][question_i]
		column_data = questionnaire.iloc[:, question_i]

		if isinstance(current_type, str):
			classified_column = column_data.tolist()
		# Si el tipo no es un string, es un mapping
		else:
			classified_column = [classify_answer(str(answer), current_type) for answer in column_data]

		questionnaires_classified[questionnaire_i].iloc[:, question_i] = classified_column


# # Procesamiento

# ## Funciones para Procesar

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


# ## Proceso

# Lista de DataFrames donde se almacenarán los datos clasificados
questionnaires_processed = []
for questionnaire in questionnaires_clean:
	# Mismo cuestionario con mismas columnas
	questionnaires_processed.append(questionnaire.iloc[0:0])

for questionnaire_i, questionnaire in enumerate(questionnaires_classified):
	for question_i in range(questionnaire.shape[1]):
		current_type = question_type[questionnaire_i][question_i]
		column_data = questionnaire.iloc[:, question_i]

		if current_type == "account_number":
			classified_column = column_data.apply(process_account_number)
		elif current_type == "numeric":
			classified_column = column_data.apply(process_numeric_input)
		elif current_type == "integer":
			classified_column = column_data.apply(process_integer_input)
		elif current_type == "percentage":
			classified_column = column_data.apply(process_percentage_input)
		elif current_type == "time_m":
			classified_column = column_data.apply(process_time_input, args=("m"))
		elif current_type == "time_h":
			classified_column = column_data.apply(process_time_input, args=("h"))
		else:
			classified_column = [answer for answer in column_data]

		questionnaires_processed[questionnaire_i].iloc[:, question_i] = classified_column


# # Exportación

# ## CSV

output_folder = "export"
os.makedirs(output_folder, exist_ok=True)

for i, questionnaire in enumerate(questionnaires_processed):
	output_file = os.path.join(output_folder, f"questionnaire_{i+1}.csv")
	questionnaire.to_csv(output_file, index=False, encoding="utf-8")
	print(f"Se exportó: {output_file}")

# All of these features correspond to the ones I used in the Looker Studio dashboard
# https://lookerstudio.google.com/reporting/9050576a-ff02-4aea-8a4c-779c70ed658d

selected_features = [[] for _ in range(7)]

# 1 – Finanzas Transparentes (Respuestas).xlsx
selected_features[1] = [
    "numero de cuenta",
    "1 cuanto dinero generas al mes",
    "2 cuanto gastas mensualmente considerando todos tus gastos",
    "3 cuanto dinero logras ahorrar al mes"
]

# 3 – Impacto del Horario en el Desempeño y Bienestar de los Estudiantes de Minería de Datos (respuestas).xlsx
selected_features[3] = [
	"numero de cuenta",
	"cuanto tiempo tardas en llegar a casa despues de la clase escribe tu respuesta en minutos"
	# "te sientes seguro al transportarse despues de las 2000 hrs explica tu respuesta"
]

# 4 – Perfil Académico (respuestas).xlsx
selected_features[4] = [
	"numero de cuenta",
	"2 edad",
	# "3 genero",
	# "4 estado donde resides",
	# "8 tienes automovil"
]

# 5 – Rendimiento académico (respuestas).xlsx
selected_features[5] = [
	"numero de cuenta",
	"cual es tu promedio actual"
]

# 6 – Uso de Tecnología y Redes Sociales.xlsx
selected_features[6] = [
	"numero de cuenta",
	"cual es tu edad",
	"cuantas horas al dia usas dispositivos electronicos para fines personales"
]

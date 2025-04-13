# Question type list of lists
# One list for each questionnaire which contains the type of each question

# 7 questionnaires
question_types = [[] for _ in range(7)]

# 0 – CaminoProfesionalMAC1.xlsx
question_types[0] = [
	# Marca temporal
	"datetime",
	# Número de cuenta
	"account_number",
	# ¿Cuál es tu mayor preocupación al terminar tus estudios?
	"string",
	# ¿Qué factores influyen más en tu decisión sobre qué camino seguir después de egresar?
	"string",
	# ¿Cuál es tu situación actual respecto a la elección de un camino profesional después de egresar?
	"string",
	# ¿Qué tipo de apoyo crees que te ayudaría más en esta etapa de decisión?
	"string",
	# ¿Qué habilidades o conocimientos crees que son esenciales para tomar una decisión sobre tu especialización o carrera profesional después de egresar?
	"string",
	# ¿En qué medida consideras que las prácticas profesionales o proyectos extracurriculares influirán en tu decisión de que camino seguir?
	"string",
	# ¿Cómo visualizas tu carrera profesional dentro de 5 años? ¿Qué tipo de trabajo o proyectos te gustaría estar realizando?
	"string",
	# ¿Qué es lo que más valoras en un posible empleo o área de especialización después de terminar tu carrera?
	"string",
	# ¿Qué tan útil consideras el material de estudio de la carrera para conseguir trabajo?
	"string",
	# ¿Sientes que tu carrera universitaria te permitió desarrollar una red de contactos profesionales que te ha ayudado en tu camino laboral?
	"string",
	# ¿Qué aspectos de tu formación académica crees que podrían mejorarse para preparar mejor a los futuros egresados?
	"string",
	# ¿Consideras que el contenido de tu carrera estuvo actualizado con las necesidades actuales del mercado laboral?
	"string"
]

# 1 – Finanzas Transparentes (Respuestas).xlsx
question_types[1] = [
	# Marca temporal
	"datetime",
	# Número de cuenta
	"account_number",
	# 1.¿Cuánto dinero generas al mes?
	"float",
	# 2. ¿Cuánto gastas mensualmente considerando todos tus gastos?
	"float",
	# 3. ¿Cuánto dinero logras ahorrar al mes?
	"float",
	# 4. ¿Tienes dinero reservado para emergencias? Si sí, ¿cuánto aproximadamente?
	"float",
	# 5. ¿Tu dinero tiene liquidez o está comprometido en inversiones o deudas?
	"string",
	# 6. ¿Cuentas con inversiones a corto plazo?
	"string",
	# 7. ¿Cuentas con inversiones a largo plazo?
	"string",
	# 8. ¿Tienes un plan personal de retiro o planeas tener uno en el futuro?
	"string",
	# 9. ¿Cuántas tarjetas de crédito tienes?
	"integer",
	# 10. ¿Qué porcentaje de tu línea de crédito tienes disponible actualmente?
	"percentage",
]

# 2 – Habilidades de MAC (respuestas).xlsx
question_types[2] = [
	# Marca temporal
	"datetime",
	# 1. ¿Cuál es tu numero de cuenta?
	"account_number",
	# 2. ¿Cómo describirías tu capacidad para explicar ideas complejas a personas que no son expertas en tu área?
	"string",
	# 3. ¿Qué tan cómodo te sientes trabajando en equipo?
	"string",
	# 4. ¿Cuál ha sido tu mayor desafío al trabajar en equipo y cómo lo superaste?
	"string",
	# 5.¿Sientes que la carrera de MAC te ha preparado adecuadamente para el trabajo en equipo?
	"string",
	# 6.¿Qué tan fácil o difícil te resulta establecer nuevas conexiones?
	"string",
	# 7. ¿Cómo te sientes al tener que hablar frente a una gran audiencia?
	"string",
	# 8. ¿Qué técnicas usas para manejar el estrés y mantener la calma en situaciones difíciles?
	"string",
	# 9.¿Cómo te preparas para presentaciones orales o exposiciones frente a un público amplio?
	"string",
	# 10. ¿Crees que las habilidades técnicas (programación, matemáticas, algoritmos) son suficientes para desempeñarte en el ámbito laboral sin necesidad de habilidades blandas?
	"string",
	# 11. ¿Has aplicado alguna de las habilidades blandas aprendidas en estos cursos en tu vida académica o personal?
	"string",
	# 12. ¿Cuáles consideras que son las habilidades blandas más importantes para un profesional de Matemáticas Aplicadas y Computación?
	"string",
	# 13.¿Cuáles de las siguientes habilidades blandas crees que te faltan desarrollar más
	"string",
	# 14.¿Qué tan preparado/a te sientes en términos de habilidades blandas para enfrentar un empleo después de graduarte?
	"string",
	# 15.¿Consideras que los estudiantes de MAC suelen subestimar la importancia de las habilidades blandas?
	"string",
	# Dirección de correo electrónico
	"email"
]

# 3 – Impacto del Horario en el Desempeño y Bienestar de los Estudiantes de Minería de Datos (respuestas).xlsx
question_types[3] = [
	# Marca temporal
	"datetime",
	# Número de cuenta
	"account_number",
	# ¿Qué tanto afecta tener una materia de 18:00 a 20:00 hrs en viernes a tu desempeño académico?
	"string",
	# ¿Qué tanto afecta tener una materia de 18:00 a 20:00 hrs en viernes a tu desempeño personal?
	"string",
	# ¿Qué dificultades enfrentas para asistir y concentrarte en esta materia en ese horario? (Separa cada una por comas)
	"string",
	# ¿Qué tanto impacta este horario en tu organización del tiempo para otras actividades académicas o laborales?
	"string",
	# ¿Crees que el rendimiento en una materia como Minería de Datos se ve afectado por el horario? ¿Por qué?
	"string",
	# ¿Qué tanto afecta este horario a tu alimentación y descanso?
	"string",
	# ¿Qué sugerencias darías para mejorar la experiencia de aprendizaje en esta materia considerando el horario? (Menciona las sugerencias separando por comas)
	"string",
	# ¿Has considerado dejar esta materia debido al horario? ¿Por qué?
	"string",
	# ¿Qué herramientas o métodos crees que podrían hacer más llevadera la clase en este horario? (Menciona las herramientas separando por comas)
	"string",
	# ¿Cuál es tu principal medio de transporte para llegar y salir de la universidad?
	"string",
	# ¿Has experimentado dificultades con el transporte debido al horario de la materia? Si es así, ¿cuáles?
	"string",
	# ¿Cuánto tiempo tardas en llegar a casa después de la clase? (Escribe tu respuesta en minutos)
	"time_m",
	# ¿Te sientes seguro al transportarse después de las 20:00 hrs? Explica tu respuesta.
	"string",
	# ¿Has tenido que modificar tus rutas o modos de transporte por la hora en que termina la clase?"
	"string",
	# Dirección de correo electrónico
	"email"
]

# 4 – Perfil Académico (respuestas).xlsx
question_types[4] = [
	# Marca temporal
	"datetime",
	# 1. Número de Cuenta:
	"account_number",
	# 2. Edad:
	"integer",
	# 3. Genero
	"string",
	# 4. Estado donde resides:
	"string",
	# 5. ¿Actualmente estas laborando o realizando tu Servicio Social?
	"string",
	# 6. ¿Cuánto tiempo en minutos dura tu recorrido a la Facultad?
	"time_m",
	# 7. materias de la carrera te interesaron más las de área computacional o matemática?
	"string",
	# 8. ¿Tienes Automóvil?
	"string",
	# 9. ¿En qué Área de especialidad de la carrera estás interesado?
	"string",
	# 10. ¿Qué materia se te dificultó más en la carrera?
	"string",
	# 11. ¿Cuales son las 3 materias que consideras que más te aportado más en tu elección de área de especialidad?
	"string",
	# 12. ¿En cuantas y cuales materias elegiste a un profesor por "barquear" la materia?
	"integer",
	# 13. ¿Te consideras bueno trabajando en equipo? ¿por qué?
	"string",
	# 14. ¿Te consideras perfeccionista?
	"string",
	# 15. ¿Tus padres o alguna persona cercana se encuentra laborando en algo relacionado con el área de especialidad que elegiste?
	"string",
	# 16. ¿Te gustaría crecer en una empresa siempre con el mismo proyecto durante años o preferirias trabajar en varios proyectos de diferentes temas?
	"string",
	# 17. ¿Qué persona consideras es tu modelo a seguir?
	"string",
	# 18. ¿Consideras que tu equipo de computo es adecuado para el software requerido en la carrera?
	"string",
	# 19. ¿Qué software utilizado en la carrera consideras el mas complejo de usar?
	"string",
	# 20. ¿Qué software utilizado en la carrera consideras el mas fácil de usar?
	"string",
]

# 5 – Rendimiento académico (respuestas).xlsx
question_types[5] = [
	# Marca temporal
	"datetime",
	# ¿Cuál es tu promedio actual?
	"float",
	# Numero de cuenta
	"account_number",
	# ¿Cuántas horas dedicas al estudio semanalmente y cómo las distribuyes?
	"time_h",
	# ¿Cuántas materias debes actualmente?
	"integer",
	# ¿Cuántas materias has reprobado durante la carrera?
	"integer",
	# ¿Cuántos años llevas en la carrera?
	"float",
	# ¿Cuál es la raíz de que debas materias?
	"string",
	# ¿Los profesores te han apoyado durante la carrera?
	"string",
	# ¿Qué factores externos (familiares, laborales, sociales) afectan tu desempeño académico?
	"string",
	# ¿Qué cambios o mejoras sugerirías en el sistema educativo para mejorar el rendimiento académico?
	"string",
	# ¿Te parece que los exámenes reflejan de manera justa tu nivel de conocimiento? ¿Por qué?
	"string",
	# ¿Cómo gestionas tu tiempo entre tus responsabilidades académicas y otras actividades?
	"string"
]

# 6 – Uso de Tecnología y Redes Sociales.xlsx
question_types[6] = [
	# Marca temporal
	"datetime",
	# Número de cuenta
	"account_number",
	# ¿Cuál es tu edad?
	"integer",
	# ¿En qué semestre te encuentras?
	"integer",
	# ¿Qué dispositivos electrónicos utilizas con mayor frecuencia?\n(Ej. teléfono móvil, tablet, computadora, etc.)
	"string",
	# ¿Cuántas horas al día usas dispositivos electrónicos para fines personales?
	"time_h",
	# ¿Utilizas dispositivos electrónicos durante las horas escolares? ¿Para qué actividades?
	"string",
	# ¿Qué redes sociales usas regularmente?\n(Ej: Instagram, Facebook, TikTok, Twitter, etc.)
	"string",
	# ¿Cuál es el principal motivo por el que utilizas las redes sociales?
	"string",
	# ¿En qué momentos del día sueles acceder a las redes sociales?
	"string",
	# ¿Utilizas las redes sociales mientras realizas tareas escolares o estudios? ¿Cómo influye en tu concentración?
	"string",
	# ¿Consideras que el uso de redes sociales afecta tu rendimiento académico? Explica tu respuesta.
	"string",
	# ¿Has notado cambios en tu capacidad de concentración o productividad al usar redes sociales?
	"string",
	# ¿Crees que el uso excesivo de tecnología afecta la interacción con tus compañeros en el entorno escolar? Explica tu percepción.
	"string",
	# ¿Estás al tanto de las políticas o normas sobre el uso de tecnología en tu escuela? ¿Las consideras suficientes?
	"string",
	# ¿Recibes información o formación sobre cómo proteger tu privacidad y seguridad en línea? ¿Qué aspectos te gustaría reforzar?
	"string",
	# ¿Has sido testigo o víctima de ciberacoso o situaciones inseguras en redes sociales?
	"string",
	# ¿Te sientes preparado/a para hacer un uso responsable y seguro de la tecnología? ¿Por qué?
	"string",
	# ¿Qué tipo de talleres o formación adicional te gustaría recibir en relación con el uso de tecnología y redes sociales?
	"string",
	# ¿Cómo crees que las redes sociales influyen en tu estado de ánimo o bienestar emocional?
	"string",
	# ¿Consideras que el uso de redes sociales ha mejorado o dificultado la comunicación y relación con tus compañeros? Detalla tu experiencia
	"string",
	# ¿Crees que el uso excesivo de tecnología puede contribuir al aislamiento o la desconexión social? Explica tu perspectiva
	"string",
	# ¿Qué medidas o estrategias propondrías para promover un uso saludable de la tecnología en la escuela?
	"string",
	# ¿Qué actividades o programas te gustaría que se implementaran para mejorar la educación digital y el manejo de redes sociales?
	"string"
]

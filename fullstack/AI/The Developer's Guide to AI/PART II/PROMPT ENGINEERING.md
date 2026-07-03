## **Dolores de crecimiento en una startup**

La startup con un revuelo ahora sabía lo que tenía que hacer para que el agente de soporte de IA funcionara. El equipo necesitaba conectar al LLM con su conocimiento de soporte.

Y para ello, ¡podrían usar sus correos de soporte! Esos correos contenían soluciones paso a paso. El problema era que estaban enterrados en múltiples cadenas de correos electrónicos de ida y vuelta: largas respuestas llenas de preguntas y respuestas a los clientes. El equipo solo necesitaba limpiar primero la correspondencia.

Ya estaban usando un LLM para transformar sus respuestas apresuradas iniciales a los clientes en respuestas bien redactadas. Enviaban cada primer borrador a ChatGPT, con un prompt que le indicaba "hacer que este correo suene profesional y asegurarse de que las instrucciones sean claras y fáciles de seguir."

Con algunos cambios en el prompt, el equipo podía alimentar sus cadenas de correos de soporte en un LLM para generar respuestas. Como sabían que el LLM podía cometer errores, se asegurarían de tener a un _humano informado_. Un miembro del equipo revisaba los artículos para asegurar su exactitud en caso de que el LLM no tuviera suficiente información, cometiera un error o alucinara una respuesta. Pero eso solo llevó unos minutos, ¡mucho más rápido que crear los propios artículos!

![Clientes por correo electrónico al soporte de los clientes. Un agente humano envía la cadena de correos a un LLM, que devuelve un artículo práctico añadido a una base de conocimiento.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:0642572230333/files/images/annot_page74_1.jpg)

El equipo comenzó a construir una base de conocimiento para las solicitudes de soporte. La llenaron con artículos que documentaban respuestas a preguntas habituales, guías paso a paso y soluciones a problemas recurrentes. Esta biblioteca en crecimiento se convirtió en un tesoro de información práctica, capturando esencialmente su experiencia de apoyo colectiva en un solo lugar.

Una vez completada la base de conocimiento, el equipo podía alimentar este conocimiento de soporte al LLM. Pero no tenían que formar al LLM; Solo tenían que darle la información que necesitaba en el prompt. Crearon una _plantilla de prompt_ que combinaba todos los artículos de la base de conocimiento y la pregunta de un cliente en un solo prompt. Modificaron su llamada API para enviar el nuevo prompt, ¡y voilà! El LLM tenía el contexto necesario para responder a las solicitudes de atención al cliente. De repente, el agente de soporte de IA era bastante inteligente.

No era solo dar respuestas genéricas. Consistía en ofrecer soluciones precisas y específicas para cada contexto, extraídas directamente de sus propios materiales de apoyo. Las respuestas no siempre eran perfectas, y el modelo parecía un poco lento en responder, pero reducía la avalancha de correos de soporte. Podían volver a respirar.

Pero el equipo necesitaba aprender más. Sabían que solo estaban rascando la superficie de las capacidades del LLM. Y, por supuesto, surgieron nuevos problemas.

Las redes sociales estaban llenas de entusiasmo por el producto. Pero los trolls estaban fuera. ¡Comentarios negativos sobre su empresa los publicaban personas que ni siquiera eran clientes reales!

El equipo ya había configurado un panel de control para vigilar las menciones de su producto o empresa. Eran tantos, y su tiempo era limitado. Necesitaban una forma automatizada de identificar las publicaciones negativas para poder dirigir sus respuestas.

Aún más complicado, estas publicaciones no estaban todas en inglés. Algunos estaban en español, francés e incluso chino. Incluso las publicaciones en inglés eran desafiantes porque a veces incluían jerga de la Generación Z como _cringe_, _cheugy_ y _mid_. Quizá podrían usar un modelo de IA preentrenado para esto.

Pero tras unas semanas de uso, el equipo empezó a recibir quejas sobre el agente de soporte de IA. Parecía sufrir amnesia. Cuando un usuario preguntó: "Estoy teniendo problemas con la contraseña. ¿Puedes ayudarme a iniciar sesión?", respondía el agente de soporte de IA. El problema eran las preguntas de seguimiento. Si el usuario respondía entonces con "Actualmente estoy en el trabajo y estoy atascado. ¿Puedes ayudarme con eso o ayudarme a saltarme este bloqueador?", el agente de soporte de IA se quedaría desconcertado. No tenía ni idea de que el usuario intentaba iniciar sesión en el trabajo. No tenía memoria de su _historial de conversación_.

Peor aún, un puñado de preguntas devolvieron respuestas hilarantemente erróneas. El consejo de restablecimiento de contraseña se acompañó de instrucciones rápidas. En ocasiones, el LLM tuvo dificultades para distinguir entre artículos e instrucciones. ¡Algunos artículos incluso estaban siendo ignorados por completo!

El equipo también se dio cuenta de que, en algún momento, no podrían añadir más artículos de apoyo a su plantilla de prompts. Habían experimentado con un prompt muy grande, y la API devolvió 400: Solicitud mala. El tamaño de la solicitud que intentaban enviar superaba el límite.

Luego estaban los cargos por consumo. Vaya, ese primer proyecto de ley les dejó en shock. Normalmente, el equipo veía facturas de unos 1.000 dólares al mes, pero ahora eran casi diez veces mayores. ¿Estaban haciendo algo mal?

Obviamente, el equipo aún tenía mucho que aprender. Necesitaban una mejor comprensión de los estímulos.
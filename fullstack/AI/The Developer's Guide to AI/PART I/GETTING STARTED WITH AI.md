## **El equipo de startups comienza su camino hacia la IA**

Construido sobre noches sin dormir, tarjetas de crédito al límite y pura terquedad, el producto estaba listo—apenas. Pero tenía un subidón increíble. Así que cuando llegó el día de la conferencia tecnológica, el objetivo era sencillo: encontrar _al menos un_ cliente dispuesto a creer. El equipo, exhausto y ansioso, apenas se atrevía a tener esperanzas.

Fue entonces cuando empezó a correr la voz por el pequeño pabellón de exposiciones. Primero un susurro, luego un fuego. Demo tras demo, proveedor tras vendedor, empresa tras empresa cumpliendo, y _les encantó_. La gente hacía cola. Las cartas se intercambiaban de mano. Al final del día, el sueño parecía finalmente al alcance.

Pero el éxito, como resultó, venía acompañado de un giro cruel. El equipo lo llamó el subidón que rompió el banco.

Los contratos que firmaron los proveedores y las empresas incluían condiciones de pago netas de 90 o incluso netas 120. ¿Pero quién prestó atención a los términos? ¡Los contratos estaban en mano! Solo más tarde el equipo comprendió lo que realmente significaba esto: nada de dinero durante tres o cuatro meses. Mientras tanto, las facturas ya _vencían._ Cada tarifa de camarero, cada comida, cada suscripción vaciaba la cuenta bancaria. El oleoducto parecía completo en papel, pero vacío en el banco.

¿Y el problema mayor? El crecimiento trajo una avalancha de solicitudes de atención al cliente. Correos electrónicos interminables repetían las mismas cinco preguntas una y otra vez. Las mismas conversaciones sencillas de apoyo ocurrían cada hora de cada día. El equipo no tenía tiempo para lanzar nuevas funciones ni para crear una estrategia. Un bucle interminable de "¿Cómo hago...?", "¿Puedes ayudarme con..." y "¿Dónde encuentro...?"

Aumentar el número de empleados del equipo estaba fuera de cuestión. Las matemáticas eran brutales. Financiar a una nueva contratación además de los pagos netos de 120 hundiría a la empresa antes de que las facturas se hicieran siquiera la transferencia. Una tarde, mientras el equipo estaba agotado y ahogado en un mar de respuestas de apoyo a medio terminar, un amigo sugirió quedar para tomar un café. En algún momento entre la tercera recarga y los restos fríos de cafeína, el amigo dijo, casi de pasada: "Sabes, si la mayoría de tus preguntas son repetitivas, ¿no podrías entrenarte algo para que te las responda?"

La idea cayó como un rayo. Quizá el problema no era el crecimiento. Quizá el problema era responder a todas las preguntas manualmente, como si aún fuera el primer día. Quizá había otra manera. ¿Y si el equipo usara un agente de soporte de IA?

El equipo ya había visto agentes de soporte con IA en chats de atención al cliente con empresas con las que interactuaban cada día. Los agentes intentaban responder preguntas antes de que un humano interviniera.
![[../assets/Pasted image 20260515054523.png]]

Estos agentes de soporte de IA eran mucho más que una simple FAQ glorificada. Eran inteligentes. Algunos parecían casi humanos en sus respuestas. Otros incluso podrían realizar tareas, como proporcionar una etiqueta de devolución o concertar una cita. Fueron la primera línea de defensa automatizada. Si no podían resolver un problema, un humano siempre podía intervenir.

El equipo sabía que entrenar un modelo de IA estaba fuera de cuestión. La formación requeriría muchos más datos de los que tenían (solo eran una startup) y no tenían experiencia en IA (¡eran desarrolladores, no científicos de datos!). Pero quizá no era necesario entrenar.

Tras investigar un poco, el equipo descubrió que otras empresas estaban utilizando grandes modelos de lenguaje (LLMs) sin formación para construir estos agentes de soporte de IA. Esas empresas llamaban a estos LLMs a través de APIs y usando SDKs. ¡El equipo sabía cómo hacerlo!

Ese mismo día, el equipo de startup ya estaba llamando a la API de OpenAI. El equipo añadió una interfaz de chat en su página de soporte del producto que decía: "¿Necesitas soporte? Para un servicio más rápido, pregunta a nuestro agente de soporte de IA." Funcionó—más o menos.

El LLM podía saludar a los usuarios y redactar respuestas amigables, pero preguntarle algo específico como "Tengo problemas con la contraseña. ¿Me ayudas a iniciar sesión?", y la respuesta fue mucho menos útil. El agente de soporte de IA generaba respuestas genéricas de resolución de problemas o respondía con pasos específicos para un producto del que el equipo ni siquiera había oído hablar.

Llamar al LLM fue fácil y fue genial generando respuestas humanas, pero obviamente no sabía nada del producto del equipo. ¿Cómo usaban esas otras empresas modelos de IA sin formación? El equipo tenía más que aprender.
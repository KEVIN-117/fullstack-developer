![[assets/Pasted image 20260515053831.png]]
¡No necesitas construir modelos de IA para crear algo extraordinario con ellos! Este libro es para desarrolladores como tú. Se basa en una idea simple y poderosa: no somos arquitectos de IA que hablemos en matemáticas. Somos chefs de IA y hablamos código. No necesitamos construir el horno desde cero. Necesitamos las recetas para ensamblar modelos de IA _preentrenados_, APIs y bases de datos para construir algo increíble. Este libro es _esa_ guía de recetas.

Seguirás el camino de un equipo de startup mientras se enfrentan _exactamente_ a los problemas que probablemente estás enfrentando tú en este momento. Su camino comienza con una solución apresurada: usar una llamada API a un modelo de IA para gestionar una avalancha de atención al cliente. Pero, ¿qué ocurre cuando esa primera llamada funciona—más o menos—pero el modelo de IA no sabe nada sobre el producto real?

¿Cuánto más efectivos serían tus sistemas si un modelo de IA tuviera "memoria" de tus _propios_ conocimientos internos y conversaciones? Podrías alimentar a un modelo de IA con todo lo que necesita saber para responder no solo preguntas de soporte, sino también preguntas sobre tu documentación, documentos internos, datos y más. ¿Qué significaría para tu equipo si pudieras evitar el shock de esa primera factura por enviar enormes prompts de API cargados de tokens? Tu equipo podría diseñar prompts que _contengan solo_ el contexto necesario usando una solución más inteligente como la generación aumentada por recuperación (RAG).

¿Y si pudieras resolver el problema de tu bandeja de entrada desbordada? Podrías _enseñar_ a un modelo de IA una habilidad nueva y especializada, como ajustarlo para clasificar _exactamente_ tus tipos de correo: Líder de Ventas, Consulta de Soporte o Spam. ¿Cuánto más valiosos serían tus sistemas si los perfiles de Leads de Ventas pudieran extraerse de forma autónoma del correo electrónico y añadirse a una base de datos? Un modelo de IA podría ayudarte a extraer datos importantes no solo del correo electrónico, sino también de tus documentos, contratos, tickets, registros y más, para desbloquear información que antes estaba atrapada en carpetas y bandejas de entrada saturadas.

Por último, piensa cuál es tu verdadero cuello de botella. ¿Es clasificar el correo o _actuar_ en consecuencia? ¿Cuánto más valioso sería tu equipo si la IA pudiera razonar, planificar y usar herramientas autónomas para gestionar todo un flujo de trabajo, transformándolo de un clasificador de correo en un verdadero colaborador digital?
![[assets/Pasted image 20260515053857.png]]
Este camino es para el ingeniero de software que no tiene ningún deseo de obtener un máster en aprendizaje automático, pero sí tiene un profundo deseo de mantenerse relevante. Es para el manager que sabe que su equipo es capaz de más, si pudiera liberarse de las tareas manuales que agotan su creatividad. Es para el desarrollador junior que ve todo cambiando a su alrededor y está intentando entender toda esta nueva tecnología.

Nuestro trabajo como desarrolladores es entender las herramientas a nuestras puertas para poder resolver problemas reales. Este libro añadirá IA a tu caja de herramientas para que puedas resolver problemas que antes nunca podías. Aprenderás todo lo que _necesites para_ poder pasar de escribir sugerencias a construir agentes.

## **IA generativa y más allá**

El lanzamiento de ChatGPT impulsó la IA a la cultura general, ya que la IA generativa pasó a ser accesible para todos. Después de experimentar con ChatGPT, todos nos quedamos asombrados. Era pura magia. Y independientemente de nuestras habilidades técnicas, todos teníamos las mismas preguntas: ¿Estaba realmente pensando este ordenador? ¿Era alguna inteligencia sobrehumana? ¿Estábamos presenciando el auge de las máquinas?

OpenAI nos hizo creer que la inteligencia artificial general (AGI) estaba en el horizonte. No lo fue, y _probablemente_ aún no lo es. ChatGPT simplemente dio al mundo su primer vistazo a la IA generativa. Ofrecía una interfaz fácil de usar para la verdadera maravilla que se esconde debajo: el gran modelo de lenguaje (LLM).

Los LLMs son un gran punto de partida para nuestro camino en la IA. Estos populares modelos de IA generativa son de propósito general. Están preentrenados para aceptar entradas y generar salidas que todos podemos entender: el lenguaje natural. Todos hemos usado LLMs, y en este libro nos ayudarán a introducir conceptos y herramientas de IA que necesitarás.

A medida que avances en el libro y crezca tu conocimiento conceptual, te presentaremos otros tipos de modelos de IA preentrenados que puedes añadir a tu caja de herramientas. Incluso te mostraremos cómo usar estos modelos para construir sistemas autónomos. Al final del libro, serás un chef de IA consumado listo para crear soluciones reales.

## **Seguridad y privacidad de los datos**

Antes de enviar datos confidenciales a un LLM (o a cualquier modelo de IA), necesitas entender los riesgos. Es importante que las empresas sepan cómo los proveedores de LLM usarán sus datos propietarios.

La política de privacidad de datos de OpenAI para espacios de trabajo personales de ChatGPT establece que las conversaciones de chat pueden usarse para mejorar sus modelos a menos que se opte explícitamente por no participar. La guía de uso de la plataforma también advierte a los usuarios que no compartan información sensible durante cualquier conversación. Samsung aprendió esto por las malas.

_The Economist_ Corea informó de tres incidentes en los que empleados de Samsung Electronics expusieron accidentalmente información sensible a ChatGPT. En un caso, un empleado insertó código fuente confidencial en un chat para depurar errores. Otro empleado compartió código con ChatGPT para solicitar optimización. En un tercer caso, un empleado subió una grabación de una reunión para transcribirla en notas de presentación. Tras descubrir la filtración, Samsung envió una advertencia a sus empleados y restringió el acceso a ChatGPT.

Antes de enviar información confidencial a cualquier LLM alojado externamente, asegúrate de entender sus acuerdos de seguridad y privacidad de datos. Lo discutiremos con más detalle en el [Capítulo 4](https://learning.oreilly.com/library/view/the-developers-guide/0642572230333/xhtml/ch4.xhtml#ch4) para ofrecer algunas orientaciones sobre la seguridad y privacidad de los datos en relación con los LLMs.

## **Elección de Tecnología**

Nuestro objetivo en este libro no es convencerte de ninguna elección tecnológica en particular. Nuestro objetivo es proporcionarte el conocimiento necesario para convertirte en un chef de IA y así construir sistemas increíbles con modelos de IA.

JavaScript es casi universal entre los desarrolladores, lo que lo convierte en el lugar perfecto para empezar. La utilizaremos para explicar muchos conceptos fundamentales de la IA. Si sabes leer o escribir código JavaScript sencillo, tendrás todo lo necesario para empezar.

Luego te iremos introduciendo poco a poco en Python para profundizar en temas avanzados de IA. Python ofrece el ecosistema más maduro para el desarrollo de IA, con un amplio conjunto de librerías y herramientas que lo hacen ideal para demostrar implementaciones complejas.

Los ejemplos utilizan una variedad de modelos de IA preentrenados (por ejemplo, modelos GPT, Llama y Gemini) de varios proveedores (por ejemplo, OpenAI, Meta, Google y Hugging Face). Te daremos consejos sobre cómo elegir un modelo en el camino.

También te presentaremos una variedad de herramientas, librerías y frameworks para ayudarte a explicar la arquitectura y las mejores prácticas. Si decides elegir una de estas tecnologías, ¡genial! Lo importante es que primero entiendas los conceptos. De este modo, sabrás cuándo y por qué una tecnología es la elección adecuada.

> [!NOTE]
> _A lo largo del libro haremos referencia a versiones específicas de modelos, herramientas, bibliotecas y frameworks de IA preentrenados. Elegimos estas versiones a propósito. Las versiones específicas aseguran la precisión en ejemplos de código (como al usar SDKs) y al explicar conceptos fundamentales (como fechas de corte de entrenamiento y tamaños de ventanas contextuales). Si usas una versión diferente o incluso una herramienta, librería, framework o modelo distinto, no te preocupes. Los conceptos y fundamentos siguen siendo los mismos._

---
## **Descargando el código de ejemplo**

El mundo de la IA está cambiando rápidamente. Estamos dedicados a mantener los ejemplos de libros actualizados. Siempre puedes acceder al código más reciente y avanzado desde el repositorio de GitHub _[en https://github.com/jorshali/developers-guide-to-ai](https://github.com/jorshali/developers-guide-to-ai)_.

También hemos añadido (y seguiremos añadiendo) ejemplos más allá de los de este libro. Te animamos a que bifurques el repositorio y experimentes por tu cuenta. Si tienes un ejemplo que crees que merece la pena añadir, ¡háznoslo saber! Nos encantan las solicitudes de tirada.

Mostramos muchos fragmentos de código a lo largo del libro. Ten en cuenta que a menudo solo incluimos fragmentos de código relevantes para un concepto que se está discutiendo. Verás las siguientes convenciones:

- --snip-- Indica código antes o después del fragmento que no se muestra
-  # ... ... Indica código dentro de un fragmento que no se muestra

Para las importaciones de bibliotecas, mostramos solo aquellas que son relevantes para el fragmento de código presentado. Si el fragmento de código es una continuación, podemos excluir una importación de biblioteca indicada anteriormente. Ten en cuenta que si quieres ver un archivo completo, puedes acceder al código completo en el repositorio de GitHub.

También incluimos muchas sentencias de impresión/log en los ejemplos. Imprimir resultados, estructuras de objetos y ejecutar pasos lógicos importantes es una forma extremadamente útil de entender y depurar código. Si un ejemplo no tiene sentido, ¡añade tus propias declaraciones impresas! Te sorprenderá cuánto puede ayudar esto.

Para facilitar la configuración, hemos incluido los archivos de dependencias necesarios: _package.json_ para Node.js y _requirements.txt_ para Python. Cada proyecto también incluye un archivo _README.md_ que explica qué hace el código y cómo hacerlo funcionar.

## **Aviso de retirada de seguridad del Asistente de Codificación de IA**

No podemos escribir un libro de IA para desarrolladores sin mencionar los asistentes de programación de IA. Pueden acelerar tu productividad, pero aún cometen _muchos_ errores. No conducirías un coche sin cinturón de seguridad, ¿verdad? ¡No seas víctima! Abróchate el cinturón por seguridad primero:

- Entiende antes de generar. Nunca dejes que el asistente de IA genere código que no entiendas. Siempre necesitas el conocimiento necesario para saber si el código es correcto.
- Usa el control de versiones. Tu proyecto debería estar bajo control de versiones antes de usar la asistencia de IA. Necesitas la capacidad de hacer retroactivación de cualquier cambio de código que haga.
- Implementa cambios incrementales. Haz que el asistente haga pequeños cambios incrementales que puedan ser fácilmente revisados. Si alguna vez has hecho una revisión de código, sabes lo difícil que es revisar commits grandes.
- Comprométete con frecuencia. Usar el control de versiones no ayuda a menos que commitas tu código antes de que el asistente de IA haga cambios. Esto te da una forma de volver a una versión funcional.
- Diff es tu amigo. Como usas control de versiones y haces commit con frecuencia, puedes ver fácilmente qué ha cambiado la IA con git diff (o insertar tu comando de control de versiones diff).

Estas son realmente buenas prácticas de ingeniería de software que todos deberíamos seguir. Vale, ya estás avisado.

Aquí tienes algunos asistentes de programación de IA populares que puedes probar:

- Claude Code (_[https://claude.com/product/claude-code](https://claude.com/product/claude-code)_)
- GitHub Copilot (_[https://github.com/features/copilot](https://github.com/features/copilot)_)
- Cursor (_[https://www.cursor.com](https://www.cursor.com/)_)
- Windsurf (_[https://windsurf.com](https://windsurf.com/)_)

## **Lo que vamos a cubrir**

Este libro está organizado en cinco partes. [La Parte I](https://learning.oreilly.com/library/view/the-developers-guide/0642572230333/xhtml/part1.xhtml) se centra en el uso de los LLMs tal cual. Esta parte simplemente requiere conocimientos básicos de JavaScript y ganas de aprender. Prepararemos el terreno presentándote a los LLMs a través de un caso de uso con el que todos pueden identificarse: un agente de soporte de IA. Tras una rápida introducción a Python, empezaremos a profundizar más. Los capítulos de esta parte son los siguientes:

- **[Capítulo 1: Comprendiendo los grandes modelos de lenguaje](https://learning.oreilly.com/library/view/the-developers-guide/0642572230333/xhtml/ch1.xhtml#ch1)** Explicaremos qué son los LLMs en términos sencillos, por qué son potentes para automatizar el trabajo del conocimiento, las limitaciones que hay que planificar y las palancas prácticas que los equipos pueden usar para integrar los LLMs de forma fiable en soluciones reales.
- **[Capítulo 2: Creando tu primera aplicación impulsada por LLM](https://learning.oreilly.com/library/view/the-developers-guide/0642572230333/xhtml/ch2.xhtml#ch2)** Tendrás tu primera experiencia programando una solución impulsada por IA mientras construyes una aplicación sencilla de chat real usando JavaScript y un LLM que se ejecuta en tu máquina.
- **[Capítulo 3: Fundamentos de Python para LLMs y APIs](https://learning.oreilly.com/library/view/the-developers-guide/0642572230333/xhtml/ch3.xhtml#ch3)** Te haremos productivo en Python recreando la aplicación en estilo chat mientras introducimos la sintaxis fundamental, los conceptos y las librerías que necesitarás para el resto de ejemplos del libro.

[La Parte II](https://learning.oreilly.com/library/view/the-developers-guide/0642572230333/xhtml/part2.xhtml) es una guía práctica para la ingeniería de prompts. Aprenderás un marco mental y técnicas para crear prompts efectivos. También aprenderás sobre las librerías y frameworks disponibles para integrar LLMs en tus aplicaciones. Ejemplos y código te guiarán durante todo el proceso para que te sientas cómodo instruyendo a los LLMs para que hagan tu voluntad. Los capítulos de esta parte son los siguientes:

- **[Capítulo 4: Fundamentos de la Ingeniería de Prompts](https://learning.oreilly.com/library/view/the-developers-guide/0642572230333/xhtml/ch4.xhtml#ch4)** Explorarás los tipos de problemas reales que resuelven los LLMs, los pilares de un prompt de calidad y las limitaciones que deben gestionarse para mantener las funciones de IA precisas, rápidas y rentables.
- **[Capítulo 5: Técnicas de Ingeniería Prompt](https://learning.oreilly.com/library/view/the-developers-guide/0642572230333/xhtml/ch5.xhtml#ch5)** Aprenderás a obtener resultados más fiables y preparados para el negocio a partir de los LLMs utilizando patrones de prompting probados, técnicas y mejores prácticas.
- **[Capítulo 6: Ingeniería de prompts en código](https://learning.oreilly.com/library/view/the-developers-guide/0642572230333/xhtml/ch6.xhtml#ch6)** Verás cómo convertir esos prompts de calidad en funcionalidades fiables y listas para producción eligiendo las librerías y configuraciones adecuadas de LLM, aplicando patrones de programación probados y gestionando consideraciones del mundo real para que tu primer despliegue sea intencionado y no una apuesta.

[La Parte III](https://learning.oreilly.com/library/view/the-developers-guide/0642572230333/xhtml/part3.xhtml) introduce las bases de datos vectoriales y los problemas reales que resuelven. Aprenderás sobre RAG y usarás todo lo que has aprendido hasta ahora para construir un agente de soporte de IA. A continuación, te presentaremos conceptos avanzados necesarios para construir una solución RAG a nivel de producción. Los capítulos de esta parte son los siguientes:

- **[Capítulo 7: Bases de datos vectoriales en la práctica](https://learning.oreilly.com/library/view/the-developers-guide/0642572230333/xhtml/ch7.xhtml#ch7)** Ampliaremos tu conocimiento sobre modelos de IA preentrenados más allá de los LLMs mostrando cómo las empresas pueden utilizar modelos de incrustación y bases de datos vectoriales para potenciar búsquedas y personalizaciones más inteligentes, como encontrar los productos adecuados o recomendar los siguientes mejores productos.
- **[Capítulo 8: Diseñando un Sistema de Generación Aumentada por Recuperación](https://learning.oreilly.com/library/view/the-developers-guide/0642572230333/xhtml/ch8.xhtml#ch8)** Usarás RAG para transformar un LLM en un experto en tus datos privados, llevándote más allá de respuestas genéricas hacia respuestas precisas y específicas para el negocio que generan una productividad real a partir de tu conocimiento actual.

[La Parte IV](https://learning.oreilly.com/library/view/the-developers-guide/0642572230333/xhtml/part4.xhtml) profundiza en la personalización de modelos de IA preentrenados y LLMs para adaptarlos a necesidades específicas. Aprenderás a afinar un LLM para resolver problemas específicos con un alto grado de precisión. Los capítulos de esta parte son los siguientes:

- **[Capítulo 9: Por qué y cuándo personalizar un modelo](https://learning.oreilly.com/library/view/the-developers-guide/0642572230333/xhtml/ch9.xhtml#ch9)** Exploraremos por qué y cuándo ir más allá de los modelos genéricos preentrenados. Compararemos la eficiencia del ajuste fino con la construcción desde cero e introduciremos las estrategias y métodos clave para especializar la IA en tareas de nicho y del mundo real.
- **[Capítulo 10: Preparación de datos para el ajuste fino](https://learning.oreilly.com/library/view/the-developers-guide/0642572230333/xhtml/ch10.xhtml#ch10)** Verás cómo convertir los datos en un conjunto de datos de alta calidad seleccionando, etiquetando y dividiendo estratégicamente tus datos para afinar tus datos.
- **[Capítulo 11: Ajuste fino de modelos en la práctica](https://learning.oreilly.com/library/view/the-developers-guide/0642572230333/xhtml/ch11.xhtml#ch11)** Cerraremos la brecha entre teoría y código, recorriendo la cadena técnica de extremo a extremo para transformar modelos de propósito general en expertos especializados y afinados.

[La Parte V](https://learning.oreilly.com/library/view/the-developers-guide/0642572230333/xhtml/part5.xhtml) toma el contenido que has aprendido hasta ahora y lo aplica para construir sistemas autónomos con IA agente. Aprenderás a usar los LLMs para entender los objetivos de un usuario y el contexto de un problema. Luego verás cómo los agentes pueden actuar para alcanzar esos objetivos, aprendiendo y adaptándose basándose en nueva información. Los capítulos de esta parte son los siguientes:

- **[Capítulo 12: De flujos de trabajo a agentes autónomos](https://learning.oreilly.com/library/view/the-developers-guide/0642572230333/xhtml/ch12.xhtml#ch12)** Este capítulo marca la transición de una IA reactiva que simplemente "piensa" y "responde" a agentes proactivos y autónomos que "actúan" y "resuelven", llevándonos más allá de simples ventanas de chat y adentrándonos en el mundo de la resolución de problemas orientada a objetivos.
- **[Capítulo 13: Construyendo un agente autónomo](https://learning.oreilly.com/library/view/the-developers-guide/0642572230333/xhtml/ch13.xhtml#ch13)** Darás tus primeros pasos prácticos hacia la creación de agentes de IA, centrándote en un enfoque personalizable basado en código. Luego crearás tu primer agente.
- **[Capítulo 14: Extendiendo agentes con herramientas](https://learning.oreilly.com/library/view/the-developers-guide/0642572230333/xhtml/ch14.xhtml#ch14)** Transicionarás de entender la IA como un "pensador" a construir la IA como un "hacedor" explorando cómo las herramientas y el Protocolo de Contexto del Modelo ayudan a los agentes a alcanzar la verdadera agencia.

¿Qué significaría para tu próximo gran proyecto si tú, o tu equipo, pudierais convertir esa bandeja de entrada caótica de un cementerio de ideas en un motor autónomo de crecimiento? ¡Vamos a descubrirlo juntos al empezar!
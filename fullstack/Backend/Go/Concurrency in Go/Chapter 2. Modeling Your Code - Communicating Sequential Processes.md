# La Diferencia Entre Concurrencia y Paralelismo

El hecho de que la *concurrencia* sea diferente del *paralelismo* a menudo se pasa por alto o se malinterpreta. En las conversaciones entre muchos desarrolladores, los dos términos a menudo se usan indistintamente para significar "algo que se ejecuta al mismo tiempo que otra cosa". A veces usar la palabra "paralelo" en este contexto es correcto, pero generalmente si los desarrolladores están discutiendo sobre código, realmente deberían estar usando la palabra "concurrente".

La razón para diferenciar va mucho más allá de la pedantería. La diferencia entre concurrencia y paralelismo resulta ser una abstracción muy poderosa al modelar tu código, y Go aprovecha al máximo esto. Echemos un vistazo a cómo los dos conceptos son diferentes para que podamos entender el poder de esta abstracción. Comenzaremos con una afirmación muy simple:

> La concurrencia es una propiedad del código; el paralelismo es una propiedad del programa en ejecución.

Esa es una distinción interesante. ¿No solemos pensar en estas dos cosas de la misma manera? Escribimos nuestro código para que se ejecute en paralelo. ¿Verdad?

Bueno, pensemos en eso por un segundo. Si escribo mi código con la intención de que dos fragmentos del programa se ejecuten en paralelo, ¿tengo alguna garantía de que eso sucederá realmente cuando se ejecute el programa? ¿Qué pasa si ejecuto el código en una máquina con un solo núcleo? Algunos de ustedes pueden estar pensando: *Se ejecutará en paralelo*, ¡pero esto no es cierto!

Los fragmentos de nuestro programa pueden *parecer* que se ejecutan en paralelo, pero en realidad se ejecutan de manera secuencial más rápido de lo que es distinguible. El contexto de la CPU cambia para compartir el tiempo entre diferentes programas, y en una granularidad de tiempo lo suficientemente gruesa, las tareas parecen ejecutarse en paralelo. Si ejecutáramos el mismo binario en una máquina con dos núcleos, los fragmentos del programa podrían estar ejecutándose realmente en paralelo.

Esto revela algunas cosas interesantes e importantes. La primera es que no escribimos código paralelo, solo código concurrente que *esperamos* que se ejecute en paralelo. Una vez más, el paralelismo es una propiedad del *tiempo de ejecución* (runtime) de nuestro programa, no del código.

La segunda cosa interesante es que vemos que es posible, tal vez incluso deseable, ignorar si nuestro código concurrente se está ejecutando realmente en paralelo. Esto solo es posible gracias a las capas de abstracción que se encuentran debajo del modelo de nuestro programa: las primitivas de concurrencia, el tiempo de ejecución del programa, el sistema operativo, la plataforma en la que se ejecuta el sistema operativo (en el caso de hipervisores, contenedores y máquinas virtuales), y, en última instancia, las CPUs. Estas abstracciones son las que nos permiten hacer la distinción entre concurrencia y paralelismo, y en última instancia, lo que nos da el poder y la flexibilidad para expresarnos. Volveremos a esto.

La tercera y última cosa interesante es que el paralelismo es una función del tiempo o del contexto. ¿Recuerdas en "Atomicidad" donde discutimos el concepto de contexto? Allí, el contexto se definió como los límites por los cuales una operación se consideraba atómica. Aquí, se define como los límites por los cuales dos o más operaciones podrían considerarse paralelas.

Por ejemplo, si nuestro contexto fuera un espacio de cinco segundos y ejecutáramos dos operaciones que tardaran un segundo cada una en ejecutarse, consideraríamos que las operaciones se han ejecutado en paralelo. Si nuestro contexto fuera de un segundo, consideraríamos que las operaciones se han ejecutado secuencialmente.

Puede que no nos sirva de mucho ir redefiniendo nuestro contexto en términos de fragmentos de tiempo, pero recuerda que el contexto no se limita al tiempo. Podemos definir un contexto como el proceso en el que se ejecuta nuestro programa, el hilo (thread) de su sistema operativo o su máquina. Esto es importante porque el contexto que defines está estrechamente relacionado con el concepto de concurrencia y corrección. Así como las operaciones atómicas pueden considerarse atómicas dependiendo del contexto que definas, las operaciones concurrentes son correctas dependiendo del contexto que definas. Todo es relativo.

Eso es un poco abstracto, así que veamos un ejemplo. Supongamos que el contexto que estamos discutiendo es tu computadora. Dejando de lado la física teórica, podemos esperar razonablemente que un proceso que se ejecuta en mi máquina no afectará la lógica de un proceso en tu máquina. Si ambos iniciamos un proceso de calculadora y comenzamos a realizar algunas operaciones aritméticas simples, los cálculos que realizo no deberían afectar los cálculos que tú realizas.

Es un ejemplo tonto, pero si lo desglosamos, vemos todas las piezas en juego: nuestras máquinas son el contexto, y los procesos son las operaciones concurrentes. En este caso, hemos elegido modelar nuestras operaciones concurrentes pensando en el mundo en términos de computadoras, sistemas operativos y procesos separados. Estas abstracciones nos permiten afirmar con confianza la corrección.

##### ¿Es Realmente un Ejemplo Tonto?

Usar computadoras individuales parece un ejemplo artificial para dejar claro un punto, ¡pero las computadoras personales no siempre fueron tan ubicuas! Hasta fines de la década de 1970, los mainframes eran la norma, y el contexto común que usaban los desarrolladores al pensar en problemas de manera concurrente era el proceso de un programa.

Ahora que muchos desarrolladores trabajan con sistemas distribuidos, ¡está cambiando hacia el otro lado! Ahora estamos comenzando a pensar en términos de hipervisores, contenedores y máquinas virtuales como nuestros contextos concurrentes.

Podemos esperar razonablemente que un proceso en una máquina permanezca inalterado por un proceso en otra máquina (suponiendo que no formen parte del mismo sistema distribuido), pero ¿podemos esperar que dos procesos en la *misma* máquina no afecten la lógica del otro? El proceso `A` podría sobrescribir algunos archivos que el proceso `B` está leyendo, o en un sistema operativo inseguro, el proceso `A` podría incluso corromper la memoria que el proceso `B` está leyendo. Hacerlo intencionalmente es cómo funcionan muchos exploits.

Aún así, a nivel de proceso, las cosas siguen siendo relativamente fáciles de pensar. Si volvemos a nuestro ejemplo de la calculadora, sigue siendo razonable esperar que dos usuarios que ejecutan dos procesos de calculadora en la misma máquina puedan esperar razonablemente que sus operaciones estén lógicamente aisladas entre sí. Afortunadamente, el límite del proceso y el sistema operativo nos ayudan a pensar en estos problemas de manera lógica. Pero podemos ver que el desarrollador comienza a sentirse agobiado por algunas preocupaciones de concurrencia, y este problema solo empeora.

¿Qué pasa si bajamos un nivel más, al límite del hilo (thread) del sistema operativo? Es aquí donde todos los problemas enumerados en la sección "¿Por qué es difícil la concurrencia?" realmente entran en juego: condiciones de carrera, interbloqueos (deadlocks), livelocks e inanición. Si tuviéramos *un* proceso de calculadora en el que todos los usuarios de una máquina tuvieran vistas, sería más difícil hacer bien la lógica concurrente. Tendríamos que empezar a preocuparnos por sincronizar el acceso a la memoria y recuperar los resultados correctos para el usuario correcto.

Lo que sucede es que a medida que comenzamos a descender por la pila de abstracciones, el problema de modelar cosas de manera concurrente se vuelve más difícil de razonar y más importante. A la inversa, nuestras abstracciones se vuelven cada vez más importantes para nosotros. En otras palabras, cuanto más difícil es hacer bien la concurrencia, más importante es tener acceso a primitivas de concurrencia que sean fáciles de componer. Desafortunadamente, la mayoría de la lógica concurrente en nuestra industria se escribe en uno de los niveles más altos de abstracción: hilos del sistema operativo (OS threads).

Antes de que Go se revelara al público, aquí era donde terminaba la cadena de abstracciones para la mayoría de los lenguajes de programación populares. Si querías escribir código concurrente, modelarías tu programa en términos de hilos y sincronizarías el acceso a la memoria entre ellos. Si tenías muchas cosas que modelar concurrentemente y tu máquina no podía manejar tantos hilos, creabas un *pool de hilos* (thread pool) y multiplexabas tus operaciones en el pool de hilos.

Go ha agregado otro eslabón a esa cadena: la *goroutine*. Además, Go ha tomado prestados varios conceptos del trabajo del famoso informático Tony Hoare, y ha introducido nuevas primitivas para que las usemos, a saber, los *canales* (channels).

Si continuamos la línea de razonamiento que hemos estado siguiendo, asumiríamos que la introducción de otro nivel de abstracción debajo de los hilos del sistema operativo traería consigo más dificultades, pero lo interesante es que *no lo hace*. En realidad, hace que las cosas sean *más fáciles*. Esto se debe a que realmente no hemos agregado otra capa de abstracción sobre los hilos del sistema operativo, los hemos suplantado.

Los hilos siguen ahí, por supuesto, pero descubrimos que rara vez tenemos que pensar en nuestro espacio de problemas en términos de hilos del sistema operativo. En su lugar, modelamos cosas en goroutines y canales, y ocasionalmente en memoria compartida. Esto conduce a algunas propiedades interesantes que exploramos en la sección "Cómo te ayuda esto". Pero primero, echemos un vistazo más de cerca a de dónde obtuvo Go muchas de sus ideas: el artículo que es la base de las primitivas de concurrencia de Go: el influyente artículo de Tony Hoare, "Communicating Sequential Processes" (Procesos Secuenciales Comunicantes).

# ¿Qué es CSP?

Cuando se habla de Go, a menudo escucharás a la gente lanzar el acrónimo *CSP*. A menudo en el mismo aliento se elogia como la razón del éxito de Go, o como una panacea para la programación concurrente. Es suficiente para que las personas que no saben qué es CSP comiencen a pensar que la informática había descubierto alguna técnica nueva que mágicamente hace que la programación de programas concurrentes sea tan simple como escribir programas procedimentales. Si bien CSP facilita las cosas y hace que los programas sean más robustos, lamentablemente no es un milagro. Entonces, ¿qué es? ¿Qué tiene a todos tan emocionados?

CSP significa "Communicating Sequential Processes" (Procesos Secuenciales Comunicantes), que es tanto una técnica como el nombre del artículo que la introdujo. En 1978, Charles Antony Richard Hoare publicó el artículo en la Association for Computing Machinery (más popularmente referida como ACM).

En este artículo, Hoare sugiere que la entrada y la salida (input y output) son dos primitivas de programación pasadas por alto, particularmente en el código concurrente. En el momento en que Hoare fue autor de este documento, todavía se estaba investigando cómo estructurar los programas, pero la mayor parte de este esfuerzo se dirigía a técnicas para código secuencial: se debatía el uso de la declaración `goto`, y el paradigma orientado a objetos comenzaba a afianzarse. No se pensaba mucho en las operaciones concurrentes. Hoare se propuso corregir esto, y así nacieron su artículo y CSP.

En el documento de 1978, CSP era solo un lenguaje de programación simple construido únicamente para demostrar el poder de los procesos secuenciales comunicantes; de hecho, incluso dice en el artículo:

> Por lo tanto, los conceptos y notaciones presentados en este artículo no deben ... considerarse adecuados para su uso como lenguaje de programación, ni para programación abstracta ni para programación concreta.

Hoare estaba profundamente preocupado porque las técnicas que presentaba no hicieran nada para avanzar en el estudio de la corrección de los programas, y porque las técnicas pudieran no tener un buen rendimiento en un lenguaje real basado en el suyo propio. En los siguientes seis años, la idea de CSP se refinó en una representación formal de algo llamado *cálculo de procesos* (process calculus) en un esfuerzo por tomar las ideas de los procesos secuenciales comunicantes y comenzar realmente a razonar sobre la corrección del programa. El cálculo de procesos es una forma de modelar matemáticamente sistemas concurrentes y también proporciona leyes algebraicas para realizar transformaciones en estos sistemas con el fin de analizar sus diversas propiedades, p. ej., eficiencia y corrección. Aunque los cálculos de procesos son un tema interesante por derecho propio, están más allá del alcance de este libro. Y dado que el artículo original sobre CSP y el lenguaje que evolucionó de él fueron en gran parte la inspiración para el modelo de concurrencia de Go, nos centraremos en ellos.

Para respaldar su afirmación de que las entradas y salidas debían considerarse primitivas del lenguaje, el lenguaje de programación CSP de Hoare contenía primitivas para modelar correctamente la entrada y salida, o la *comunicación*, entre *procesos* (de ahí proviene el nombre del documento). Hoare aplicó el término *procesos* a cualquier porción de lógica encapsulada que requiriera entrada para ejecutarse y produjera salida que otros procesos consumirían. Hoare probablemente podría haber usado la palabra "función" si no fuera por el debate sobre cómo estructurar programas que ocurría en la comunidad cuando escribió su artículo.

Para la comunicación entre los procesos, Hoare creó *comandos* de entrada y salida: `!` para enviar entrada a un proceso y `?` para leer la salida de un proceso. Cada comando tenía que especificar o bien una variable de salida (en el caso de leer una variable de un proceso), o un destino (en el caso de enviar entrada a un proceso). A veces estos dos se referían a la misma cosa, en cuyo caso se decía que los dos procesos *correspondían* (corresponded). En otras palabras, la salida de un proceso fluiría directamente hacia la entrada de otro proceso. La Tabla 2-1 muestra algunos ejemplos del artículo.

Tabla 2-1. Un extracto de algunos ejemplos del artículo de CSP de Hoare
| Operación | Explicación |
|---|---|
| `cardreader?cardimage` | Desde `cardreader`, lee una tarjeta y asigna su valor (un array de caracteres) a la variable `cardimage`. |
| `lineprinter!lineimage` | Hacia `lineprinter`, envía el valor de `lineimage` para impresión. |
| `X?(x, y)` | Del proceso llamado `X`, ingresa un par de valores y asígnalos a `x` e `y`. |
| `DIV!(3*a+b, 13)` | Al proceso `DIV`, genera los dos valores especificados. |
| `*[c:character; west?c → east!c]` | Lee todos los caracteres emitidos por `west` y envíalos uno por uno a `east`. La repetición termina cuando el proceso `west` termina. |

Las similitudes con los canales (channels) de Go son evidentes. Observa cómo en el último ejemplo la salida de `west` se envió a una variable `c` y la entrada a `east` se recibió de la misma variable. Estos dos procesos corresponden. En el primer artículo de Hoare sobre CSP, los procesos solo podían comunicarse mediante fuentes y destinos con nombre. Él reconoció que esto causaría problemas al incrustar código como biblioteca, ya que los consumidores del código tendrían que conocer los nombres de las entradas y salidas. Casualmente mencionó la posibilidad de registrar lo que él llamó "nombres de puerto" (port names), en los que se podían declarar nombres en la cabecera del comando paralelo, algo que probablemente reconoceríamos como parámetros con nombre y valores de retorno con nombre.

El lenguaje también utilizaba el llamado *comando guardado* (guarded command), que Edgar Dijkstra había introducido en un artículo anterior escrito en 1974, "Comandos guardados, no determinismo y derivación formal de programas". Un comando guardado es simplemente una declaración con un lado izquierdo y otro derecho, divididos por un `→`. El lado izquierdo servía como condicional, o *guardia* para el lado derecho en el sentido de que si el lado izquierdo era falso o, en el caso de un comando, devolvía falso o había terminado, el lado derecho nunca se ejecutaría. Combinar estos con los comandos de I/O de Hoare sentó las bases para los procesos comunicantes de Hoare, y por lo tanto para los canales de Go.

Usando estas primitivas, Hoare recorrió varios ejemplos y demostró cómo un lenguaje con soporte de primera clase para modelar la comunicación hace que resolver problemas sea más simple y fácil de comprender. Algunas de las notaciones que usa son un poco tersas (¡los programadores de perl probablemente no estarían de acuerdo!), pero los problemas que presenta tienen soluciones extraordinariamente claras. Las soluciones similares en Go son un poco más largas, pero también llevan consigo esta claridad.

La historia ha juzgado que la sugerencia de Hoare fue correcta; sin embargo, es interesante notar que antes de que Go fuera lanzado, pocos lenguajes realmente habían incorporado soporte para estas primitivas. La mayoría de los lenguajes populares favorecen el intercambio y la sincronización del acceso a la memoria en lugar del estilo de paso de mensajes de CSP. Hay excepciones, pero desafortunadamente estas están confinadas a lenguajes que no han tenido una adopción generalizada. Go es uno de los primeros lenguajes en incorporar los principios de CSP en su núcleo, y llevar este estilo de programación concurrente a las masas. Su éxito ha llevado a otros lenguajes a intentar agregar también estas primitivas.

La sincronización de acceso a la memoria no es inherentemente mala. Veremos más adelante en el capítulo (en "La Filosofía de Go sobre la Concurrencia") que a veces compartir memoria es apropiado en ciertas situaciones, incluso en Go. Sin embargo, el modelo de memoria compartida *puede* ser difícil de utilizar correctamente, especialmente en programas grandes o complicados. Es por esta razón que la concurrencia se considera uno de los puntos fuertes de Go: se ha construido desde el principio teniendo en cuenta los principios de CSP y, por lo tanto, es fácil de leer, escribir y razonar.

# Cómo te Ayuda Esto

Puede que todo esto te parezca fascinante o no, pero lo más probable es que si estás leyendo este libro tienes problemas que resolver, y te preguntas por qué algo de esto importa. ¿Qué hace Go de manera tan diferente que lo ha diferenciado de otros lenguajes populares en lo que respecta a la concurrencia?

Como discutimos en la sección "La Diferencia Entre Concurrencia y Paralelismo" para modelar problemas concurrentes, es común que los lenguajes terminen su cadena de abstracción al nivel del hilo del sistema operativo (OS thread) y la sincronización del acceso a la memoria. Go toma una ruta diferente y suplementa esto con el concepto de goroutines y canales.

Si tuviéramos que hacer una comparación entre los conceptos de las dos formas de abstraer el código concurrente, probablemente compararíamos la goroutine con un hilo, y un canal con un mutex (estas primitivas solo tienen un parecido superficial, pero es de esperar que la comparación te ayude a orientarte). ¿Qué hacen estas diferentes abstracciones por nosotros?

Las Goroutines nos liberan de tener que pensar en nuestro espacio de problemas en términos de paralelismo y en cambio nos permiten modelar problemas más cerca de su nivel natural de concurrencia. Aunque repasamos la diferencia entre concurrencia y paralelismo, la forma en que esa diferencia afecta a cómo modelamos las soluciones podría no estar clara. Saltemos a un ejemplo.

Supongamos que necesito crear un servidor web que atienda solicitudes en un endpoint. Dejando de lado los frameworks por un momento, en un lenguaje que solo ofrece una abstracción de hilo (thread), probablemente estaría reflexionando sobre las siguientes preguntas:

- ¿Mi lenguaje admite hilos de forma natural, o tendré que elegir una biblioteca?
- ¿Dónde deberían estar mis límites de confinamiento de hilos?
- ¿Qué tan "pesados" son los hilos en este sistema operativo?
- ¿Cómo manejan los hilos de manera diferente los sistemas operativos en los que se ejecutará mi programa?
- Debería crear un pool de workers para limitar la cantidad de hilos que creo. ¿Cómo encuentro el número óptimo?

Todas estas son cosas importantes a considerar, pero ninguna de ellas se refiere directamente al problema que estás tratando de resolver. Te han arrastrado inmediatamente a los tecnicismos de cómo vas a resolver el problema del paralelismo.

Si damos un paso atrás y pensamos en el problema natural, podríamos expresarlo así: los usuarios individuales se conectan a mi endpoint y abren una sesión. La sesión debe atender su solicitud y devolver una respuesta. En Go, podemos representar casi directamente el estado natural de este problema en código: crearíamos una goroutine para cada conexión entrante, atenderíamos la solicitud allí (comunicándonos potencialmente con otras goroutines para obtener datos/servicios), y luego retornaríamos de la función de la goroutine. La forma en que pensamos naturalmente sobre el problema se asigna directamente a la forma natural de codificar las cosas en Go.

Esto se logra mediante una promesa que Go nos hace: que las goroutines son ligeras (lightweight) y normalmente no tendremos que preocuparnos por crear una. Hay momentos apropiados para considerar cuántas goroutines se están ejecutando en tu sistema, pero hacerlo por adelantado es sin duda una optimización prematura. Contrasta esto con los hilos, donde sería prudente considerar tales asuntos por adelantado.

El hecho de que exista un framework disponible para un lenguaje que abstraiga las preocupaciones de paralelismo por ti, ¡no significa que esta forma natural de modelar problemas concurrentes no importe! Alguien tiene que escribir el framework, y tu código se asentará sobre cualquier complejidad con la que haya tenido que lidiar el/los autor/es. El simple hecho de que la complejidad te esté oculta no significa que no esté ahí, y la complejidad engendra errores. En el caso de Go, el lenguaje fue diseñado en torno a la concurrencia, por lo que el lenguaje no es incongruente con las primitivas de concurrencia que proporciona. ¡Esto significa menos fricción y menos errores!

Una asignación más natural al espacio de problemas es un beneficio *enorme*, pero también tiene algunos efectos secundarios beneficiosos. El runtime de Go multiplexa las goroutines en hilos del sistema operativo de forma automática y gestiona su programación (scheduling) por nosotros. Esto significa que se pueden realizar optimizaciones en el tiempo de ejecución sin que tengamos que cambiar cómo hemos modelado nuestro problema; esta es la clásica separación de intereses (separation of concerns). A medida que se logren avances en el paralelismo, el tiempo de ejecución de Go mejorará, al igual que el rendimiento de tu programa, todo de forma gratuita. Mantente atento a las notas de la versión de Go y ocasionalmente verás cosas como:

> En Go 1.5, se ha cambiado el orden en el que se programan las goroutines.

Los autores de Go están haciendo mejoras detrás de escena para que tu programa sea más rápido.

Este desacoplamiento de la concurrencia y el paralelismo tiene otro beneficio: debido a que el runtime de Go gestiona la programación de las goroutines por ti, puede inspeccionar cosas como goroutines bloqueadas esperando I/O y reasignar de forma inteligente los hilos del sistema operativo a las goroutines que no están bloqueadas. Esto también aumenta el rendimiento de tu código. Hablaremos más de lo que hace el runtime de Go por ti en el Capítulo 6.

Otro beneficio más de la asignación más natural entre los espacios de problemas y el código de Go es la probabilidad de que una mayor cantidad del espacio de problemas se modele de forma concurrente. Debido a que los problemas en los que trabajamos como desarrolladores son naturalmente concurrentes en su mayoría, naturalmente escribiremos código concurrente en un nivel de granularidad más fino del que quizás lo haríamos en otros lenguajes; p. ej., si volvemos a nuestro ejemplo de servidor web, ahora tendríamos una goroutine para cada usuario en lugar de conexiones multiplexadas en un pool de hilos. Este nivel de granularidad más fino permite que nuestro programa escale *dinámicamente* cuando se ejecuta hasta la cantidad de paralelismo posible en el host del programa: ¡la ley de Amdahl en acción! Eso es bastante sorprendente.

Y las goroutines son solo una pieza del rompecabezas. Los otros conceptos de CSP, los canales y las declaraciones `select`, también agregan valor.

Los canales, por ejemplo, son inherentemente *componibles* con otros canales. Esto hace que escribir sistemas grandes sea más simple porque puedes coordinar la entrada de múltiples subsistemas componiendo fácilmente la salida junta. Puedes combinar canales de entrada con tiempos de espera (timeouts), cancelaciones o mensajes a otros subsistemas. Coordinar mutexes es una propuesta mucho más difícil.

La declaración `select` es el complemento de los canales de Go y es lo que permite todos los bits difíciles de la composición de canales. Las sentencias `select` te permiten esperar eficientemente por eventos, seleccionar un mensaje de canales competidores de una manera aleatoria uniforme, continuar si no hay mensajes esperando, y más.

Este maravilloso tapiz de primitivas inspiradas en CSP y el tiempo de ejecución que lo respalda son las cosas que impulsan a Go. Pasaremos el resto del libro descubriendo cómo funcionan estas cosas, por qué, y cómo podemos usarlas para escribir un código increíble.

# La Filosofía de Go sobre la Concurrencia

CSP fue y *es* una gran parte de aquello en torno a lo cual se diseñó Go; sin embargo, Go también es compatible con medios más tradicionales de escribir código concurrente a través de la sincronización de acceso a la memoria y las primitivas que siguen esa técnica. Las structs y los métodos en el paquete `sync` y otros paquetes te permiten realizar bloqueos, crear pools de recursos, interrumpir (preempt) goroutines y más.

Esta capacidad de elegir entre las primitivas de CSP y las sincronizaciones de acceso a la memoria es excelente para ti, ya que te da un poco más de control sobre qué estilo de código concurrente eliges escribir para resolver problemas, pero también puede ser un poco confuso. Los recién llegados al lenguaje a menudo tienen la impresión de que el estilo de concurrencia CSP se considera la única forma de escribir código concurrente en Go. Por ejemplo, en la documentación del paquete `sync`, dice:

> El paquete sync proporciona primitivas de sincronización básicas como los bloqueos de exclusión mutua. Aparte de los tipos Once y WaitGroup, la mayoría están destinados para ser utilizados por rutinas de biblioteca de bajo nivel. La sincronización de nivel superior se hace mejor a través de canales y comunicación.

En las preguntas frecuentes del lenguaje (FAQ), dice:

> Con respecto a los mutexes, el paquete sync los implementa, pero esperamos que el estilo de programación de Go anime a las personas a probar técnicas de nivel superior. En particular, considera estructurar tu programa de modo que solo una goroutine a la vez sea responsable de una porción de datos en particular.
>
> No te comuniques compartiendo memoria. En cambio, comparte la memoria comunicándote.

También hay numerosos artículos, conferencias y entrevistas donde varios miembros del equipo central de Go abrazan el estilo CSP sobre primitivas como `sync.Mutex`.

Por lo tanto, es completamente comprensible estar confundido en cuanto a por qué el equipo de Go eligió exponer primitivas de sincronización de acceso a la memoria en absoluto. Lo que puede ser aún más confuso es que verás primitivas de sincronización comúnmente en la naturaleza (out in the wild), verás a personas quejarse del uso excesivo de canales y también escucharás a algunos de los miembros del equipo de Go afirmando que está bien usarlas. Aquí hay una cita de la Wiki de Go sobre el asunto:

> Uno de los lemas de Go es "Comparte memoria comunicándote, no te comuniques compartiendo memoria".
>
> Dicho esto, Go sí proporciona mecanismos de bloqueo tradicionales en el paquete sync. La mayoría de los problemas de bloqueo se pueden resolver usando canales o bloqueos tradicionales.
>
> Entonces, ¿cuál deberías usar?
>
> Usa el que sea más expresivo y/o más simple.

Ese es un buen consejo, y es una pauta que ves a menudo cuando trabajas con Go, pero es un poco vaga. ¿Cómo entendemos qué es más expresivo y/o más simple? ¿Qué criterios podemos usar? Afortunadamente hay algunos indicadores que podemos usar para ayudarnos a hacer lo correcto. Como veremos, la forma en que podemos diferenciarnos principalmente proviene de dónde intentamos administrar nuestra concurrencia: internamente dentro de un ámbito (scope) estrecho o externamente a través de nuestro sistema. La Figura 2-1 enumera estas guías en un árbol de decisión.
![[../../../assets/DecisionTree.png]]
*(Figura 2-1. Árbol de decisión)*

Repasemos estos puntos de decisión uno por uno:

**¿Estás intentando transferir la propiedad de los datos?**

Si tienes un fragmento de código que produce un resultado y quieres compartir ese resultado con otro fragmento de código, lo que realmente estás haciendo es transferir la propiedad (ownership) de esos datos. Si estás familiarizado con el concepto de propiedad de memoria en lenguajes que no admiten la recolección de basura, esta es la misma idea: los datos tienen un propietario, y una forma de hacer que los programas concurrentes sean seguros es garantizar que solo un contexto concurrente tenga la propiedad de los datos a la vez. Los canales nos ayudan a comunicar este concepto al codificar esa intención en el tipo del canal.

Un gran beneficio de hacerlo es que puedes crear canales almacenados en búfer (buffered channels) para implementar una cola en memoria barata y así desacoplar tu productor de tu consumidor. Otro es que al usar canales, implícitamente has hecho que tu código concurrente sea *componible* con otro código concurrente.

**¿Estás intentando proteger el estado interno de un struct?**

Este es un gran candidato para las primitivas de sincronización de acceso a la memoria, y un indicador bastante fuerte de que no deberías usar canales. Al usar las primitivas de sincronización de acceso a la memoria, puedes ocultar el detalle de implementación del bloqueo de tu sección crítica a los invocadores. Aquí hay un pequeño ejemplo de un tipo que es seguro para hilos (thread-safe), pero no expone esa complejidad a quienes lo llaman:

```go
type Counter struct {
    mu    sync.Mutex
    value int
}

func (c *Counter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.value++
}
```

Si recuerdas el concepto de atomicidad, podemos decir que lo que hemos hecho aquí es definir el alcance de la atomicidad para el tipo `Counter`. Las llamadas a `Increment` se pueden considerar atómicas.

Recuerda que la palabra clave aquí es *interno*. Si te encuentras exponiendo bloqueos (locks) más allá de un tipo, esto debería generar una señal de alerta. Trata de mantener los bloqueos restringidos a un ámbito léxico pequeño.

**¿Estás intentando coordinar múltiples piezas de lógica?**

Recuerda que los canales son inherentemente más componibles que las primitivas de sincronización de acceso a la memoria. ¡Tener bloqueos dispersos por todo tu gráfico de objetos suena como una pesadilla, pero se espera y fomenta tener canales en todas partes! Puedo componer canales, pero no puedo componer fácilmente bloqueos o métodos que devuelven valores.

Encontrarás mucho más fácil controlar la complejidad emergente que surge en tu software si utilizas canales debido a la declaración `select` de Go, y a su capacidad para servir como colas y poder pasarse de un lado a otro de forma segura. Si te resulta difícil comprender cómo funciona tu código concurrente, por qué ocurre un interbloqueo (deadlock) o una carrera (race), y estás utilizando primitivas de sync, esto es probablemente un buen indicador de que deberías cambiar a canales.

**¿Es una sección crítica para el rendimiento?**

Esto *no* significa en absoluto: "Quiero que mi programa tenga buen rendimiento, por lo tanto, solo usaré mutexes". Más bien, si tienes una sección de tu programa a la que le has aplicado "profiling", y resulta ser un cuello de botella importante que es órdenes de magnitud más lento que el resto del programa, el uso de primitivas de sincronización de acceso a memoria puede ayudar a que esta sección crítica se desempeñe bien bajo carga. Esto se debe a que los canales *utilizan* la sincronización de acceso a la memoria para operar, por lo tanto, solo pueden ser más lentos. Sin embargo, antes de siquiera considerar esto, una sección crítica para el rendimiento podría estar insinuando que necesitamos reestructurar nuestro programa.

Es de esperar que esto brinde algo de claridad en torno a si utilizar la concurrencia de estilo CSP o la sincronización de acceso a la memoria. Existen otros patrones y prácticas que son útiles en los lenguajes que usan el hilo del sistema operativo (OS thread) como medio para abstraer la concurrencia. Por ejemplo, cosas como los pools de hilos (thread pools) surgen con frecuencia. Debido a que la mayoría de estas abstracciones están dirigidas a las fortalezas y debilidades de los hilos del sistema operativo, una buena regla general al trabajar con Go es descartar estos patrones. Eso no quiere decir que no sean útiles en absoluto, pero los casos de uso están ciertamente mucho más limitados en Go. Limítate a modelar tu espacio de problemas con goroutines, utilízalas para representar las partes concurrentes de tu flujo de trabajo, y no temas ser liberal al iniciarlas. Es mucho más probable que necesites reestructurar tu programa que comenzar a toparte con el límite superior de cuántas goroutines puede soportar tu hardware.

La filosofía de Go sobre la concurrencia se puede resumir así: busca la simplicidad, usa canales cuando sea posible, y trata a las goroutines como un recurso gratuito.
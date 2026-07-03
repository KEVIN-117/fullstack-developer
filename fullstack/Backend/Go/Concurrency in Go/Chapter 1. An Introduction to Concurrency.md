# Capítulo 1: Una Introducción a la Concurrencia

La concurrencia es una palabra interesante porque significa cosas diferentes para diferentes personas en nuestro campo. Además de "concurrencia", es posible que hayas escuchado que se utilizan palabras como "asíncrono", "paralelo" o "multihilo" (threaded). Algunas personas consideran que estas palabras significan lo mismo, y otras personas hacen una clara distinción entre cada una de ellas. Si vamos a pasar el tiempo de todo un libro discutiendo la concurrencia, sería beneficioso dedicar primero un tiempo a discutir a qué nos referimos cuando decimos "concurrencia".

Pasaremos algún tiempo hablando de la filosofía de la concurrencia en el Capítulo 2, pero por ahora adoptemos una definición práctica que servirá como base de nuestra comprensión.

Cuando la mayoría de las personas usan la palabra "concurrente", generalmente se refieren a un proceso que ocurre simultáneamente con uno o más procesos. También suele estar implícito que todos estos procesos están progresando aproximadamente al mismo tiempo. Bajo esta definición, una manera fácil de pensar en esto son las personas. Actualmente estás leyendo esta oración mientras otras en el mundo viven simultáneamente sus vidas. Ellas existen *concurrentemente* a ti.

La concurrencia es un tema amplio en la informática, y de esta definición surgen todo tipo de temas: teoría, enfoques para modelar la concurrencia, corrección lógica, problemas prácticos, ¡incluso física teórica! Tocaremos algunos de los temas auxiliares a lo largo del libro, pero nos ceñiremos principalmente a los problemas prácticos que implican comprender la concurrencia dentro del contexto de Go, específicamente: cómo Go elige modelar la concurrencia, qué problemas surgen de este modelo y cómo podemos componer primitivas dentro de este modelo para resolver problemas.

En este capítulo, daremos un vistazo amplio a algunas de las razones por las que la concurrencia se convirtió en un tema tan importante en la informática, por qué la concurrencia es difícil y merece un estudio cuidadoso, y, lo más importante, la idea de que, a pesar de estos desafíos, Go puede hacer que los programas sean más claros y rápidos utilizando sus primitivas de concurrencia.

Al igual que con la mayoría de los caminos hacia la comprensión, comenzaremos con un poco de historia. Primero veamos cómo la concurrencia se convirtió en un tema tan importante.

## La Ley de Moore, la Escala Web y el Lío en el que Estamos

En 1965, Gordon Moore escribió un documento de tres páginas que describía tanto la consolidación del mercado de la electrónica hacia los circuitos integrados, como la duplicación del número de componentes en un circuito integrado cada año durante al menos una década. En 1975, revisó esta predicción para afirmar que el número de componentes en un circuito integrado se duplicaría cada dos años. Esta predicción se mantuvo más o menos cierta hasta hace poco, alrededor de 2012.

Varias empresas previeron esta desaceleración en el ritmo predicho por la ley de Moore y comenzaron a investigar formas alternativas de aumentar la potencia informática. Como dice el refrán, la necesidad es la madre de la innovación, y fue así como nacieron los procesadores de múltiples núcleos (multicore).

Esto parecía una forma inteligente de resolver los problemas de los límites de la ley de Moore, pero los informáticos pronto se encontraron enfrentando los límites de otra ley: la ley de Amdahl, nombrada en honor al arquitecto informático Gene Amdahl.

La ley de Amdahl describe una manera de modelar las posibles ganancias de rendimiento al implementar la solución a un problema de manera paralela. En pocas palabras, establece que las ganancias están limitadas por la cantidad del programa que debe escribirse de manera secuencial.

Por ejemplo, imagina que estás escribiendo un programa basado principalmente en una interfaz gráfica de usuario (GUI): se le presenta una interfaz a un usuario, este hace clic en algunos botones y suceden cosas. Este tipo de programa está limitado por una porción secuencial muy grande del pipeline: la interacción humana. Sin importar cuántos núcleos pongas a disposición de este programa, siempre estará limitado por la rapidez con la que el usuario pueda interactuar con la interfaz.

Ahora considera un ejemplo diferente: calcular los dígitos de pi. Gracias a una clase de algoritmos llamados algoritmos de espita (spigot algorithms), este problema se denomina *vergonzosamente paralelo* (embarrassingly parallel), lo cual, a pesar de sonar inventado, es un término técnico que significa que puede dividirse fácilmente en tareas paralelas. En este caso, se pueden lograr ganancias significativas poniendo más núcleos a disposición de tu programa, y tu nuevo problema pasa a ser cómo combinar y almacenar los resultados.

La ley de Amdahl nos ayuda a comprender la diferencia entre estos dos problemas y puede ayudarnos a decidir si la paralelización es la forma correcta de abordar las preocupaciones de rendimiento en nuestro sistema.

Para los problemas que son vergonzosamente paralelos, se recomienda que escribas tu aplicación para que pueda *escalar horizontalmente*. Esto significa que puedes tomar instancias de tu programa y ejecutarlas en más CPUs o máquinas, y esto hará que el tiempo de ejecución del sistema mejore. Los problemas vergonzosamente paralelos se ajustan tan bien a este modelo porque es muy fácil estructurar tu programa de tal manera que puedas enviar fragmentos de un problema a diferentes instancias de tu aplicación.

Escalar horizontalmente se volvió mucho más fácil a principios de la década de 2000 cuando un nuevo paradigma comenzó a afianzarse: la *computación en la nube* (cloud computing). Aunque hay indicios de que la frase se usó desde la década de 1970, a principios de la década de 2000 es cuando la idea realmente se arraigó en el espíritu de la época. La computación en la nube implicó un nuevo tipo de escala y un enfoque para las implementaciones de aplicaciones y el escalado horizontal. En lugar de máquinas que curabas cuidadosamente, en las que instalabas software y mantenías, la computación en la nube implicaba el acceso a vastos grupos de recursos que se aprovisionaban en máquinas para cargas de trabajo bajo demanda. Las máquinas se convirtieron en algo casi efímero, y provisto de características específicamente adaptadas a los programas que ejecutarían. Por lo general (pero no siempre), estos grupos de recursos estaban alojados en centros de datos propiedad de otras empresas.

Este cambio alentó un nuevo tipo de pensamiento. De repente, los desarrolladores tenían acceso relativamente económico a enormes cantidades de poder de cómputo que podían usar para resolver problemas grandes. Las soluciones ahora podían abarcar trivialmente muchas máquinas e incluso regiones globales. La computación en la nube hizo posible un conjunto completamente nuevo de soluciones a problemas que antes solo podían resolver los gigantes tecnológicos.

Pero la computación en la nube también presentó muchos desafíos nuevos. Aprovisionar estos recursos, comunicarse entre instancias de máquinas, y agregar y almacenar los resultados se convirtieron en problemas a resolver. Pero entre los más difíciles estaba descubrir cómo modelar el código de manera concurrente. El hecho de que partes de tu solución pudieran estar ejecutándose en máquinas dispares exacerbaba algunos de los problemas comúnmente enfrentados al modelar un problema de manera concurrente. Resolver con éxito estos problemas pronto condujo a una nueva marca para el software: la *escala web* (web scale).

Si el software era a escala web, entre otras cosas, se podía esperar que fuera vergonzosamente paralelo; es decir, normalmente se espera que el software a escala web pueda manejar cientos de miles (o más) de cargas de trabajo simultáneas agregando más instancias de la aplicación. Esto habilitó todo tipo de propiedades como actualizaciones continuas (rolling upgrades), arquitectura elástica escalable horizontalmente y distribución geográfica. También introdujo nuevos niveles de complejidad, tanto en la comprensión como en la tolerancia a fallos.

Y así es en este mundo de múltiples núcleos, computación en la nube, escala web y problemas que pueden o no ser paralelizables, donde nos encontramos los desarrolladores modernos, quizás un poco abrumados. Nos han pasado la proverbial "patata caliente", y se espera que estemos a la altura del desafío de resolver problemas dentro de los confines del hardware que nos han entregado. En 2005, Herb Sutter fue autor de un artículo para *Dr. Dobb's* titulado "El almuerzo gratis se ha acabado: Un giro fundamental hacia la concurrencia en el software". El título es apropiado y el artículo profético. Hacia el final, Sutter afirma: "Necesitamos desesperadamente un modelo de programación de más alto nivel para la concurrencia que el que ofrecen los lenguajes hoy en día".

Para saber por qué Sutter usó un lenguaje tan fuerte, debemos observar por qué es tan difícil hacer bien la concurrencia.

## ¿Por qué es difícil la Concurrencia?

El código concurrente es notoriamente difícil de hacer bien. Por lo general, requiere algunas iteraciones para que funcione como se espera, e incluso entonces no es raro que existan errores en el código durante años antes de que algún cambio en la sincronización o tiempo (mayor utilización del disco, más usuarios conectados al sistema, etc.) provoque que un error no descubierto previamente asome la cabeza. De hecho, para este mismo libro, he hecho que la mayor cantidad posible de personas revisen el código para tratar de mitigar esto.

Afortunadamente, *todos* se encuentran con los mismos problemas cuando trabajan con código concurrente. Debido a esto, los informáticos han podido etiquetar los problemas comunes, lo que nos permite discutir cómo surgen, por qué y cómo resolverlos.

Así que empecemos. A continuación, se detallan algunos de los problemas más comunes que hacen que trabajar con código concurrente sea frustrante e interesante.

### Condiciones de Carrera (Race Conditions)

Una condición de carrera ocurre cuando dos o más operaciones deben ejecutarse en el orden correcto, pero el programa no se ha escrito de manera que se garantice el mantenimiento de ese orden.

La mayoría de las veces, esto aparece en lo que se llama una *carrera de datos* (data race), donde una operación concurrente intenta leer una variable mientras en algún momento indeterminado otra operación concurrente intenta escribir en la misma variable.

Aquí hay un ejemplo básico:

```go
var data int
go func() {
    data++ // 1
}()
if data == 0 {
    fmt.Printf("the value is %v.\n", data)
}
```

En Go, puedes usar la palabra clave `go` para ejecutar una función concurrentemente. Al hacerlo se crea lo que se llama una *goroutine*. Discutiremos esto en detalle en la sección "Goroutines".

Aquí, el bloque dentro de la goroutine (marcado con 1) y la declaración `if` intentan acceder a la variable `data`, pero no hay garantía de en qué orden podría suceder esto. Hay tres posibles resultados al ejecutar este código:

- No se imprime nada. En este caso, la goroutine se ejecutó antes que la declaración `if`.
- Se imprime "the value is 0". En este caso, el `if` y el `Printf` se ejecutaron antes que la goroutine.
- Se imprime "the value is 1". En este caso, la condición `if` se evaluó antes que la goroutine, pero la goroutine se ejecutó antes de la llamada a `fmt.Printf`.

Como puedes ver, solo unas pocas líneas de código incorrecto pueden introducir una tremenda variabilidad en tu programa.

La mayoría de las veces, se introducen carreras de datos porque los desarrolladores están pensando en el problema de forma secuencial. Asumen que debido a que una línea de código está antes que otra, se ejecutará primero. Asumen que la goroutine anterior será programada (scheduled) y ejecutada antes de que se lea la variable `data` en la instrucción `if`.

Cuando escribes código concurrente, tienes que iterar meticulosamente a través de los posibles escenarios. A menos que estés utilizando algunas de las técnicas que cubriremos más adelante en el libro, no tienes garantías de que tu código se ejecutará en el orden en que aparece en el código fuente. A veces me resulta útil imaginar que pasa un largo período de tiempo entre operaciones. Imagina que pasa una hora entre el momento en que se invoca la goroutine y cuando se ejecuta. ¿Cómo se comportaría el resto del programa? ¿Qué pasaría si tomara una hora entre que la goroutine se ejecutara con éxito y que el programa llegara a la declaración `if`? Pensar de esta manera me ayuda porque para una computadora, la escala puede ser diferente, pero los diferenciales de tiempo relativo son más o menos los mismos.

De hecho, algunos desarrolladores caen en la trampa de esparcir "sleeps" (pausas) a lo largo de su código exactamente porque parece resolver sus problemas de concurrencia. Intentemos eso en el programa anterior:

```go
var data int
go func() { data++ }()
time.Sleep(1 * time.Second) // ¡Esto es malo!
if data == 0 {
    fmt.Printf("the value is %v.\n", data)
}
```

¿Hemos resuelto nuestra carrera de datos? No. De hecho, sigue siendo posible que los tres resultados surjan de este programa, solo que cada vez es *más improbable*. Cuanto más durmamos entre invocar nuestra goroutine y verificar el valor de `data`, más cerca estará nuestro programa de lograr la corrección; pero esta probabilidad se acerca asintóticamente a la corrección lógica; nunca será lógicamente correcto.

Además de esto, ahora hemos introducido una ineficiencia en nuestro algoritmo. Ahora tenemos que dormir por un segundo para hacer más probable que no veamos nuestra carrera de datos. Si utilizamos las herramientas correctas, es posible que no tengamos que esperar en absoluto, o la espera podría ser solo de un microsegundo.

La conclusión aquí es que siempre debes apuntar a la corrección lógica. Introducir pausas (`sleep`) en tu código puede ser una forma útil de depurar programas concurrentes, pero no son una solución.

Las condiciones de carrera son uno de los tipos más insidiosos de errores de concurrencia porque es posible que no aparezcan hasta años después de que el código haya sido puesto en producción. Generalmente son precipitadas por un cambio en el entorno en el que se ejecuta el código, o un evento sin precedentes. En estos casos, el código parece comportarse correctamente, pero en realidad, existe una probabilidad muy alta de que las operaciones se ejecuten en orden. Tarde o temprano, el programa tendrá una consecuencia no deseada.

### Atomicidad (Atomicity)

Cuando algo se considera atómico, o que tiene la propiedad de atomicidad, esto significa que dentro del contexto en el que está operando, es indivisible o ininterrumpible.

Entonces, ¿qué significa realmente eso, y por qué es importante saberlo al trabajar con código concurrente?

Lo primero que es muy importante es la palabra "contexto". Algo puede ser atómico en un contexto, pero no en otro. Las operaciones que son atómicas en el contexto de tu proceso pueden no ser atómicas en el contexto del sistema operativo; las operaciones que son atómicas dentro del contexto del sistema operativo pueden no ser atómicas dentro del contexto de tu máquina; y las operaciones que son atómicas en el contexto de tu máquina pueden no ser atómicas en el contexto de tu aplicación. En otras palabras, la atomicidad de una operación puede cambiar dependiendo del alcance definido en ese momento. ¡Este hecho puede jugar tanto a tu favor como en tu contra!

Al pensar en la atomicidad, muy a menudo lo primero que debes hacer es definir el contexto, o alcance, en el que se considerará que la operación es atómica. Todo se deriva de esto.

> **Dato Curioso**
>
> En 2006, la empresa de juegos Blizzard demandó con éxito a MDY Industries por $6,000,000 USD por hacer un programa llamado "Glider", que jugaría automáticamente su juego, World of Warcraft, sin intervención del usuario. Estos tipos de programas se conocen comúnmente como "bots" (abreviatura de robots).
>
> En ese momento, World of Warcraft tenía un programa antitrampas llamado "Warden", que se ejecutaba cada vez que jugabas al juego. Entre otras cosas, Warden escaneaba la memoria de la máquina host y ejecutaba una heurística para buscar programas que parecían usarse para hacer trampa.
>
> ¡Glider evitó con éxito esta verificación aprovechando el concepto de contexto atómico! Warden consideraba escanear la memoria de la máquina como una operación atómica, pero Glider utilizó interrupciones de hardware para esconderse ¡antes de que comenzara este escaneo! El escaneo de la memoria de Warden era atómico en el contexto del proceso, pero no en el contexto del sistema operativo.

Ahora veamos los términos "indivisible" e "ininterrumpible". Estos términos significan que, dentro del contexto que hayas definido, algo que es atómico ocurrirá en su totalidad sin que suceda nada más en ese contexto de forma simultánea. Eso sigue siendo un trabalenguas, así que veamos un ejemplo:

```go
i++
```

Este es probablemente el ejemplo más simple que cualquiera puede inventar, y sin embargo, demuestra fácilmente el concepto de atomicidad. Puede *parecer* atómico, pero un breve análisis revela varias operaciones:

- Recuperar el valor de `i`.
- Incrementar el valor de `i`.
- Almacenar el valor de `i`.

Si bien cada una de estas operaciones por sí sola es atómica, la combinación de las tres puede no serlo, dependiendo de tu contexto. Esto revela una propiedad interesante de las operaciones atómicas: combinarlas no produce necesariamente una operación atómica mayor. Hacer que la operación sea atómica depende del contexto en el que te gustaría que fuera atómica. Si tu contexto es un programa sin procesos concurrentes, entonces este código es atómico dentro de ese contexto. Si tu contexto es una goroutine que no expone `i` a otras goroutines, entonces este código es atómico.

Entonces, ¿por qué nos importa? La atomicidad es importante porque si algo es atómico, implícitamente es seguro dentro de contextos concurrentes. Esto nos permite componer programas lógicamente correctos y, como veremos más adelante, incluso puede servir como una forma de optimizar programas concurrentes.

La mayoría de las declaraciones no son atómicas, y mucho menos las funciones, métodos y programas. Si la atomicidad es la clave para componer programas lógicamente correctos y la mayoría de las declaraciones no son atómicas, ¿cómo reconciliamos estas dos afirmaciones? Profundizaremos más adelante, pero en resumen, podemos forzar la atomicidad empleando varias técnicas. El arte se convierte entonces en determinar qué áreas de tu código deben ser atómicas y en qué nivel de granularidad. Discutimos algunos de estos desafíos en la siguiente sección.

### Sincronización de Acceso a la Memoria

Digamos que tenemos una carrera de datos: dos procesos concurrentes intentan acceder a la misma área de memoria y la forma en que acceden a la memoria no es atómica. Nuestro ejemplo anterior de una carrera de datos simple funcionará bien con algunas modificaciones:

```go
var data int
go func() { data++ }()
if data == 0 {
    fmt.Printf("the value is %v.\n", data)
} else {
    fmt.Printf("the value is %v.\n", data)
}
```

Hemos agregado una cláusula `else` aquí para que, independientemente del valor de `data`, siempre obtengamos algún resultado. Recuerda que, tal como está escrito, existe una carrera de datos y el resultado del programa será completamente no determinista.

De hecho, hay un nombre para una sección de tu programa que necesita acceso exclusivo a un recurso compartido. Esto se llama una *sección crítica* (critical section). En este ejemplo, tenemos tres secciones críticas:

- Nuestra goroutine, que incrementa las variables de `data`.
- Nuestra declaración `if`, que verifica si el valor de `data` es 0.
- Nuestra declaración `fmt.Printf`, que recupera el valor de `data` para el resultado.

Existen varias formas de proteger las secciones críticas de tu programa, y Go tiene algunas ideas mejores sobre cómo lidiar con esto, pero una forma de resolver este problema es sincronizar el acceso a la memoria entre tus secciones críticas. Veamos cómo se ve eso.

El siguiente código no es Go idiomático (y no sugiero que intentes resolver tus problemas de carrera de datos de esta manera), pero demuestra de manera muy simple la sincronización de acceso a la memoria. Si alguno de los tipos, funciones o métodos de este ejemplo te resultan extraños, no pasa nada. Concéntrate en el concepto de sincronizar el acceso a la memoria siguiendo las anotaciones.

```go
var memoryAccess sync.Mutex // 1
var data int
go func() {
    memoryAccess.Lock() // 2
    data++
    memoryAccess.Unlock() // 3
}()

memoryAccess.Lock() // 4
if data == 0 {
    fmt.Printf("the value is 0.\n")
} else {
    fmt.Printf("the value is %v.\n", data)
}
memoryAccess.Unlock() // 5
```

1. Aquí agregamos una variable que permitirá que nuestro código sincronice el acceso a la memoria de la variable `data`. Repasaremos el tipo `sync.Mutex` en detalle en "El paquete sync".
2. Aquí declaramos que, hasta que declaremos lo contrario, nuestra goroutine debe tener acceso exclusivo a esta memoria.
3. Aquí declaramos que la goroutine ha terminado con esta memoria.
4. Aquí declaramos una vez más que las siguientes declaraciones condicionales deben tener acceso exclusivo a la memoria de la variable `data`.
5. Aquí declaramos que hemos terminado una vez más con esta memoria.

En este ejemplo hemos creado una convención para que la sigan los desarrolladores. Cada vez que los desarrolladores deseen acceder a la memoria de la variable `data`, primero deben llamar a `Lock` y, cuando terminen, deben llamar a `Unlock`. El código entre esas dos declaraciones puede entonces asumir que tiene acceso exclusivo a `data`; hemos sincronizado con éxito el acceso a la memoria. También ten en cuenta que si los desarrolladores no siguen esta convención, ¡no tenemos garantía de acceso exclusivo! Volveremos a esta idea en la sección "Confinamiento" (Confinement).

Es posible que hayas notado que, si bien hemos resuelto nuestra carrera de datos, ¡en realidad no hemos resuelto nuestra condición de carrera! El orden de las operaciones en este programa sigue siendo no determinista; simplemente hemos acotado un poco el alcance del no determinismo. En este ejemplo, o la goroutine se ejecutará primero, o ambos bloques, `if` y `else`, lo harán. Todavía no sabemos cuál ocurrirá primero en una ejecución dada de este programa. Más adelante, exploraremos las herramientas para resolver este tipo de problemas de manera adecuada.

A simple vista, esto parece bastante simple: si descubres que tienes secciones críticas, ¡agrega puntos para sincronizar el acceso a la memoria! Fácil, ¿verdad? Bueno... más o menos.

Es cierto que puedes resolver algunos problemas sincronizando el acceso a la memoria, pero como acabamos de ver, no resuelve automáticamente las carreras de datos ni la corrección lógica. Además, también puede crear problemas de mantenimiento y rendimiento.

Ten en cuenta que anteriormente mencionamos que habíamos creado una *convención* para declarar que necesitábamos acceso exclusivo a cierta memoria. Las convenciones son geniales, pero también son fáciles de ignorar, especialmente en la ingeniería de software, donde las demandas del negocio a veces superan a la prudencia. Al sincronizar el acceso a la memoria de esta manera, estás confiando en que todos los demás desarrolladores sigan la misma convención ahora y en el futuro. Es pedir demasiado. Afortunadamente, más adelante en este libro también analizaremos algunas formas en las que podemos ayudar a nuestros colegas a tener más éxito.

Sincronizar el acceso a la memoria de esta manera también tiene ramificaciones en el rendimiento. Guardaremos los detalles para más adelante cuando examinemos el paquete `sync` en la sección "El paquete sync", pero las llamadas a `Lock` que ves pueden hacer que nuestro programa sea *lento*. Cada vez que realizamos una de estas operaciones, nuestro programa se detiene por un período de tiempo. Esto plantea dos preguntas:

- ¿Mis secciones críticas se entran y salen repetidamente?
- ¿Qué tamaño deben tener mis secciones críticas?

Responder a estas dos preguntas en el contexto de tu programa es un arte, y esto se suma a la dificultad de sincronizar el acceso a la memoria.

Sincronizar el acceso a la memoria también comparte algunos problemas con otras técnicas para modelar problemas concurrentes, y las discutiremos en la siguiente sección.

### Interbloqueos (Deadlocks), Livelocks e Inanición (Starvation)

Las secciones anteriores han tratado sobre la corrección del programa en el sentido de que, si estos problemas se manejan correctamente, tu programa nunca dará una respuesta incorrecta. Desafortunadamente, incluso si manejas con éxito estas clases de problemas, hay otra clase de problemas a los que enfrentarse: interbloqueos (deadlocks), livelocks e inanición (starvation). Todos estos problemas tienen que ver con garantizar que tu programa tenga algo útil que hacer en todo momento. Si no se maneja adecuadamente, tu programa podría entrar en un estado en el que dejará de funcionar por completo.

#### Interbloqueo (Deadlock)

Un programa interbloqueado es aquel en el que todos los procesos concurrentes se están esperando mutuamente. En este estado, el programa nunca se recuperará sin intervención externa.

Si eso suena sombrío, ¡es porque lo es! El runtime de Go intenta hacer su parte y detectará algunos interbloqueos (todas las goroutines deben estar bloqueadas o "dormidas"), pero esto no ayuda mucho a prevenir los interbloqueos.

Para ayudar a consolidar qué es un interbloqueo, primero veamos un ejemplo. Nuevamente, es seguro ignorar los tipos, funciones, métodos o paquetes que no conozcas y simplemente seguir las llamadas en el código.

```go
type value struct {
    mu    sync.Mutex
    value int
}

var wg sync.WaitGroup
printSum := func(v1, v2 *value) {
    defer wg.Done()
    v1.mu.Lock()         // 1
    defer v1.mu.Unlock() // 2

    time.Sleep(2 * time.Second) // 3
    v2.mu.Lock()
    defer v2.mu.Unlock()

    fmt.Printf("sum=%v\n", v1.value+v2.value)
}

var a, b value
wg.Add(2)
go printSum(&a, &b)
go printSum(&b, &a)
wg.Wait()
```

1. Aquí intentamos entrar en la sección crítica para el valor entrante.
2. Aquí usamos la declaración `defer` para salir de la sección crítica antes de que regrese `printSum`.
3. Aquí dormimos por un período de tiempo para simular trabajo (y desencadenar un interbloqueo).

Si intentaras ejecutar este código, probablemente verías:

`fatal error: all goroutines are asleep - deadlock!`

¿Por qué? Si miras con cuidado, verás un problema de tiempo en este código. A continuación se muestra una representación gráfica de lo que está sucediendo. Esencialmente, hemos creado dos engranajes que no pueden girar juntos: nuestra primera llamada a `printSum` bloquea `a` y luego intenta bloquear `b`, pero mientras tanto nuestra segunda llamada a `printSum` ha bloqueado `b` y ha intentado bloquear `a`. Ambas goroutines esperan infinitamente la una a la otra.

> **Ironía**
>
> Para mantener este ejemplo simple, uso un `time.Sleep` para activar el interbloqueo. Sin embargo, ¡esto introduce una condición de carrera! ¿Puedes encontrarla?
>
> Un interbloqueo lógicamente "perfecto" requeriría una sincronización correcta.

![[../../../assets/Pasted image 20260518091405.png]]

Parece bastante obvio por qué se está produciendo este interbloqueo cuando lo exponemos de esa manera, pero nos beneficiaríamos de una definición más rigurosa. Resulta que hay algunas condiciones que deben estar presentes para que surjan los interbloqueos, y en 1971, Edgar Coffman enumeró estas condiciones en un artículo. Las condiciones se conocen ahora como las *Condiciones de Coffman* y son la base de las técnicas que ayudan a detectar, prevenir y corregir los interbloqueos.

Las Condiciones de Coffman son las siguientes:

- **Exclusión mutua (Mutual Exclusion)**: Un proceso concurrente posee derechos exclusivos sobre un recurso en un momento dado.
- **Esperar por condición (Wait For Condition)**: Un proceso concurrente debe mantener un recurso simultáneamente y estar esperando un recurso adicional.
- **Sin expropiación (No Preemption)**: Un recurso en poder de un proceso concurrente solo puede ser liberado por ese proceso, por lo que cumple con esta condición.
- **Espera circular (Circular Wait)**: Un proceso concurrente (P1) debe estar esperando a una cadena de otros procesos concurrentes (P2), que a su vez están esperando a (P1), por lo que cumple también con esta condición final.
	![[../../../assets/Pasted image 20260518091308.png]]

Examinemos nuestro programa artificial y determinemos si cumple con las cuatro condiciones:

1. La función `printSum` requiere derechos exclusivos tanto para `a` como para `b`, por lo que cumple con esta condición.
2. Debido a que `printSum` mantiene a `a` o a `b` y está esperando a la otra, cumple con esta condición.
3. No hemos proporcionado ninguna forma de que nuestras goroutines sean interrumpidas (preempted).
4. Nuestra primera invocación de `printSum` está esperando a nuestra segunda invocación, y viceversa.

Sí, definitivamente tenemos un interbloqueo (deadlock) entre manos.

Estas leyes también nos permiten *prevenir* los interbloqueos. Si nos aseguramos de que al menos una de estas condiciones no sea cierta, podemos evitar que ocurran interbloqueos. Desafortunadamente, en la práctica, puede ser difícil razonar sobre estas condiciones y, por lo tanto, difíciles de prevenir. La web está llena de preguntas de desarrolladores como tú y yo que se preguntan por qué un fragmento de código se está interbloqueando. Por lo general, es bastante obvio una vez que alguien lo señala, pero a menudo requiere un par de ojos adicionales. Hablaremos de por qué es esto en la sección "Determinación de la Seguridad de Concurrencia".

#### Livelock

Los livelocks son programas que están realizando operaciones concurrentes activamente, pero estas operaciones no hacen nada para avanzar el estado del programa.

¿Alguna vez has estado caminando por un pasillo hacia otra persona? Ella se mueve hacia un lado para dejarte pasar, pero tú acabas de hacer lo mismo. Así que te mueves hacia el otro lado, pero ella también ha hecho lo mismo. Imagina que esto continúa para siempre, y entenderás los livelocks.

Vamos a escribir algo de código que ayudará a demostrar este escenario. Primero, configuraremos algunas funciones auxiliares que simplificarán el ejemplo. Para tener un ejemplo práctico, el código aquí utiliza varios temas que aún no hemos cubierto. No aconsejo intentar entenderlo en detalle hasta que tengas una comprensión firme del paquete `sync`. En su lugar, recomiendo seguir los comentarios del código para entender los aspectos más destacados, y luego dirigir tu atención al segundo bloque de código, que contiene el corazón del ejemplo.

```go
cadence := sync.NewCond(&sync.Mutex{})
go func() {
    for range time.Tick(1 * time.Millisecond) {
        cadence.Broadcast()
    }
}()

takeStep := func() {
    cadence.L.Lock()
    cadence.Wait()
    cadence.L.Unlock()
}

tryDir := func(dirName string, dir *int32, out *bytes.Buffer) bool {
    fmt.Fprintf(out, " %v", dirName)
    atomic.AddInt32(dir, 1) // 1
    takeStep()              // 2
    if atomic.LoadInt32(dir) == 1 {
        fmt.Fprint(out, ". Success!")
        return true
    }
    takeStep()
    atomic.AddInt32(dir, -1) // 3
    return false
}

var left, right int32
tryLeft := func(out *bytes.Buffer) bool { return tryDir("left", &left, out) }
tryRight := func(out *bytes.Buffer) bool { return tryDir("right", &right, out) }
```

1. Primero, declaramos nuestra intención de movernos en una dirección incrementando esa dirección en uno.
2. Para que el ejemplo demuestre un livelock, cada persona debe moverse a la misma velocidad o cadencia. `takeStep` simula una cadencia constante entre todas las partes.
3. Aquí la persona se da cuenta de que no puede ir en esta dirección y se rinde. Lo indicamos decrementando esa dirección en uno.

```go
walk := func(walking *sync.WaitGroup, name string) {
    var out bytes.Buffer
    defer func() { fmt.Println(out.String()) }()
    defer walking.Done()
    fmt.Fprintf(&out, "%v is trying to scoot:", name)
    for i := 0; i < 5; i++ { // 1
        if tryLeft(&out) || tryRight(&out) { // 2
            return
        }
    }
    fmt.Fprintf(&out, "\n%v tosses her hands up in exasperation!", name)
}

var walking sync.WaitGroup
walking.Add(2)
go walk(&walking, "Alice")
go walk(&walking, "Barbara")
walking.Wait()
```

1. Coloqué un límite artificial en la cantidad de intentos para que este programa terminara. ¡En un programa que tiene un livelock, es posible que no haya tal límite, por lo que es un problema!
2. Primero, la persona intentará dar un paso a la izquierda, y si eso falla, intentará dar un paso a la derecha.

Esto produce la siguiente salida:

```
Alice is trying to scoot: left right left right left right left right left right
Alice tosses her hands up in exasperation!
Barbara is trying to scoot: left right left right left right left right left right
Barbara tosses her hands up in exasperation!
```

Puedes ver que Alice y Barbara continúan estorbándose mutuamente antes de finalmente rendirse.

Este ejemplo demuestra una razón muy común por la que se escriben livelocks: dos o más procesos concurrentes intentando evitar un interbloqueo sin coordinación. Si las personas en el pasillo hubieran acordado entre sí que solo una persona se movería, no habría livelock: una persona se quedaría quieta, la otra se movería al otro lado y continuarían caminando.

En mi opinión, los livelocks son más difíciles de detectar que los interbloqueos simplemente porque puede parecer que el programa está trabajando. Si un programa con livelock se estuviera ejecutando en tu máquina y miraras la utilización de la CPU para determinar si estaba haciendo algo, podrías pensar que sí lo estaba haciendo. Dependiendo del livelock, podría incluso estar emitiendo otras señales que te harían pensar que estaba funcionando. Y, sin embargo, todo el tiempo, tu programa estaría jugando un juego eterno de barajar por el pasillo.

Los livelocks son un subconjunto de un conjunto más grande de problemas llamado *inanición* (starvation). Veremos eso a continuación.

#### Inanición (Starvation)

La inanición es cualquier situación en la que un proceso concurrente no puede obtener todos los recursos que necesita para realizar el trabajo.

Cuando discutimos los livelocks, el recurso del que cada goroutine estaba privada era un candado (lock) compartido. Los livelocks justifican una discusión separada de la inanición porque en un livelock, todos los procesos concurrentes están privados por igual y no se realiza *ningún* trabajo. En términos más generales, la inanición generalmente implica que hay uno o más procesos concurrentes codiciosos que impiden injustamente que uno o más procesos concurrentes realicen el trabajo de la manera más eficiente posible, o tal vez en absoluto.

Aquí hay un ejemplo de un programa con una goroutine codiciosa (greedy) y una goroutine educada (polite):

```go
var wg sync.WaitGroup
var sharedLock sync.Mutex
const runtime = 1 * time.Second

greedyWorker := func() {
    defer wg.Done()
    var count int
    for begin := time.Now(); time.Since(begin) <= runtime; {
        sharedLock.Lock()
        time.Sleep(3 * time.Nanosecond)
        sharedLock.Unlock()
        count++
    }
    fmt.Printf("Greedy worker was able to execute %v work loops\n", count)
}

politeWorker := func() {
    defer wg.Done()
    var count int
    for begin := time.Now(); time.Since(begin) <= runtime; {
        sharedLock.Lock()
        time.Sleep(1 * time.Nanosecond)
        sharedLock.Unlock()

        sharedLock.Lock()
        time.Sleep(1 * time.Nanosecond)
        sharedLock.Unlock()

        sharedLock.Lock()
        time.Sleep(1 * time.Nanosecond)
        sharedLock.Unlock()
        count++
    }
    fmt.Printf("Polite worker was able to execute %v work loops.\n", count)
}

wg.Add(2)
go greedyWorker()
go politeWorker()

wg.Wait()
```

Esto produce:

```
Polite worker was able to execute 289777 work loops.
Greedy worker was able to execute 471287 work loops
```

El trabajador codicioso se aferra al candado compartido durante la totalidad de su ciclo de trabajo, mientras que el trabajador educado intenta bloquear solo cuando lo necesita. Ambos trabajadores hacen la misma cantidad de trabajo simulado (dormir durante tres nanosegundos), pero como puedes ver, en la misma cantidad de tiempo, ¡el trabajador codicioso hizo casi el *doble* del trabajo!

Si asumimos que ambos trabajadores tienen la sección crítica del mismo tamaño, en lugar de concluir que el algoritmo del trabajador codicioso es más eficiente (o que las llamadas a `Lock` y `Unlock` son lentas, que no lo son), concluimos en cambio que el trabajador codicioso ha expandido innecesariamente su retención en el candado compartido más allá de su sección crítica y está impidiendo (a través de la inanición) que la goroutine del trabajador educado realice el trabajo de manera eficiente.

Observa nuestra técnica aquí para identificar la inanición: una métrica. La inanición es un buen argumento para registrar y muestrear métricas. Una de las formas en que puedes detectar y resolver la inanición es registrando cuándo se realiza el trabajo y luego determinando si tu ritmo de trabajo es tan alto como esperas.

> **Encontrar el Equilibrio**
>
> Vale la pena mencionar que el ejemplo de código anterior también puede servir como ejemplo de las ramificaciones de rendimiento de la sincronización de acceso a memoria. Debido a que sincronizar el acceso a la memoria es costoso, podría ser ventajoso ampliar nuestro bloqueo más allá de nuestras secciones críticas. Por otro lado, al hacerlo, como vimos, corremos el riesgo de provocar la inanición de otros procesos concurrentes.
>
> Si utilizas la sincronización de acceso a memoria, tendrás que encontrar un equilibrio entre preferir una sincronización de grano grueso para el rendimiento y una sincronización de grano fino para la equidad. Cuando llegue el momento de ajustar el rendimiento de tu aplicación, para empezar, te recomiendo encarecidamente que limites la sincronización de acceso a la memoria solo a las secciones críticas; si la sincronización se convierte en un problema de rendimiento, siempre puedes ampliar el alcance. Es mucho más difícil ir en la otra dirección.

Así que la inanición puede hacer que tu programa se comporte de manera ineficiente o incorrecta. El ejemplo anterior demuestra una ineficiencia, pero si tienes un proceso concurrente que es tan codicioso como para prevenir *por completo* que otro proceso concurrente realice trabajo, tienes un problema mayor entre manos.

También debemos considerar el caso en que la inanición proviene de fuera del proceso de Go. Ten en cuenta que la inanición también se puede aplicar a la CPU, la memoria, los manejadores de archivos (file handles), las conexiones a bases de datos: cualquier recurso que deba compartirse es un candidato para la inanición.

## Determinación de la Seguridad de Concurrencia

Finalmente, llegamos al aspecto más difícil del desarrollo de código concurrente, lo que subyace a todos los demás problemas: las personas. Detrás de cada línea de código hay al menos una persona.

Como hemos descubierto, el código concurrente es difícil por una miríada de razones. Si eres desarrollador y estás tratando de lidiar con todos estos problemas a medida que introduces nuevas funcionalidades o corriges errores en tu programa, puede ser realmente difícil determinar qué es lo correcto.

Si comienzas con una pizarra en blanco y necesitas construir una forma sensata de modelar tu espacio de problemas y la concurrencia está involucrada, puede ser difícil encontrar el nivel de abstracción adecuado. ¿Cómo expones la concurrencia a quienes llaman a la función? ¿Qué técnicas utilizas para crear una solución que sea fácil de usar y modificar? ¿Cuál es el *nivel* adecuado de concurrencia para este problema? Aunque hay formas de pensar en estos problemas de manera estructurada, sigue siendo un arte.

Como desarrollador que interactúa con código *existente*, no siempre es obvio qué código está utilizando concurrencia y cómo utilizar el código de forma segura. Toma esta firma de función:

```go
// CalculatePi calculates digits of Pi between the begin and end
func CalculatePi(begin, end int64, pi *Pi)
```

Calcular pi con gran precisión es algo que se hace mejor de manera concurrente, pero este ejemplo plantea muchas preguntas:

- ¿Cómo lo hago con esta función?
- ¿Soy responsable de instanciar múltiples invocaciones concurrentes de esta función?
- Parece que todas las instancias de la función van a operar directamente sobre la instancia de `Pi` cuya dirección paso; ¿soy responsable de sincronizar el acceso a esa memoria, o el tipo `Pi` lo maneja por mí?

Una función plantea todas estas preguntas. Imagina un programa de cualquier tamaño moderado, y podrás comenzar a comprender las complejidades que la concurrencia puede plantear.

Los comentarios pueden hacer maravillas aquí. ¿Qué pasaría si la función `CalculatePi` se escribiera en cambio así:

```go
// CalculatePi calculates digits of Pi between the begin and end
// place.
//
// Internally, CalculatePi will create FLOOR((end-begin)/2) concurrent
// instantiations of CalculatePi.
//
// Synchronization over writes to pi are handled internally by the Pi struct.
func CalculatePi(begin, end int64, pi *Pi)
```

Ahora entendemos que podemos llamar a la función sin problemas y no preocuparnos por la concurrencia o la sincronización. Lo que es importante, el comentario cubre estos aspectos:

- ¿Quién es responsable de la concurrencia?
- ¿Cómo se asigna el espacio del problema a las primitivas de concurrencia?
- ¿Quién es responsable de la sincronización?

Al exponer funciones, métodos y variables en espacios de problemas que involucran concurrencia, hazles un favor a tus colegas y a tu futuro yo: peca de lado de los comentarios detallados e intenta cubrir estos tres aspectos.

También considera que tal vez la ambigüedad en esta función sugiere que la hemos modelado mal. Tal vez deberíamos, en cambio, adoptar un enfoque funcional y asegurarnos de que nuestra función no tenga efectos secundarios:

```go
func CalculatePi(begin, end int64) []uint
```

La firma de esta función por sí sola elimina cualquier duda sobre la sincronización, pero aún deja la duda de si se utiliza la concurrencia. Podemos modificar la firma nuevamente para lanzar otra señal de lo que está sucediendo:

```go
func CalculatePi(begin, end int64) <-chan uint
```

Aquí vemos el primer uso de lo que se llama un *canal* (channel). Por razones que exploraremos más adelante en la sección "Canales", esto sugiere que `CalculatePi` al menos tendrá una goroutine y que no deberíamos molestarnos en crear la nuestra propia.

Estas modificaciones luego tienen ramificaciones en el rendimiento que deben tenerse en cuenta, y volvemos al problema de equilibrar la claridad con el rendimiento. La claridad es importante porque queremos hacer que sea lo más probable posible que las personas que trabajen con este código en el futuro hagan lo correcto, y el rendimiento es importante por razones obvias. Ambos no son mutuamente excluyentes, pero son difíciles de mezclar.

Ahora considera estas dificultades en la comunicación e intenta aplicarlas a escala en proyectos del tamaño de un equipo.

Guau, esto es un problema.

La buena noticia es que Go ha logrado avances para facilitar la resolución de estos tipos de problemas. El lenguaje en sí mismo favorece la legibilidad y la simplicidad. La forma en que fomenta el modelado de tu código concurrente fomenta la corrección, la composibilidad y la escalabilidad. De hecho, ¡la forma en que Go maneja la concurrencia realmente puede ayudar a expresar los dominios del problema de forma más clara! Veamos por qué esto es así.

## Simplicidad frente a la Complejidad

Hasta ahora, he pintado un panorama bastante sombrío. La concurrencia es sin duda un área difícil en la informática, pero quiero dejarte con esperanza: estos problemas no son intratables, y con las primitivas de concurrencia de Go, puedes expresar tus algoritmos concurrentes de manera más segura y clara. Las dificultades de tiempo de ejecución y comunicación que hemos discutido de ninguna manera están resueltas por Go, pero se han hecho significativamente más fáciles. En el próximo capítulo, descubriremos la raíz de cómo se ha logrado este progreso. Aquí, pasaremos un poco de tiempo explorando la idea de que las primitivas de concurrencia de Go realmente pueden facilitar el modelado de dominios de problemas y expresar algoritmos con mayor claridad.

El entorno de ejecución (runtime) de Go hace la mayor parte del trabajo pesado y proporciona la base para la mayoría de las comodidades de concurrencia de Go. Guardaremos la discusión sobre cómo funciona todo para el Capítulo 6, pero aquí discutiremos cómo estas cosas te facilitan la vida.

Primero hablemos del recolector de basura (garbage collector) de baja latencia y concurrente de Go. A menudo hay debate entre los desarrolladores sobre si los recolectores de basura son algo bueno de tener en un lenguaje. Los detractores sugieren que los recolectores de basura impiden el trabajo en cualquier dominio del problema que requiera un rendimiento en tiempo real o un perfil de rendimiento determinista: que simplemente detener toda la actividad en un programa para limpiar la basura no es aceptable. Si bien esto tiene algún mérito, el excelente trabajo que se ha realizado en el recolector de basura de Go ha reducido drásticamente la audiencia que necesita preocuparse por las minucias de cómo funciona la recolección de basura de Go. A partir de Go 1.8, ¡las pausas de la recolección de basura generalmente duran entre 10 y 100 microsegundos!

¿Cómo te ayuda esto? La gestión de la memoria puede ser otro dominio de problema difícil en la informática, y cuando se combina con la concurrencia, puede volverse extraordinariamente difícil escribir un código correcto. Si estás en la mayoría de los desarrolladores que no necesitan preocuparse por pausas tan pequeñas como 10 microsegundos, Go te ha facilitado mucho el uso de la concurrencia en tu programa al no obligarte a administrar la memoria, y mucho menos a través de procesos concurrentes.

El runtime de Go también maneja automáticamente la multiplexación de operaciones concurrentes en subprocesos (threads) del sistema operativo. Eso es un trabalenguas, y veremos exactamente qué significa eso en la sección "Goroutines". Con el propósito de entender cómo te ayuda esto, todo lo que necesitas saber es que te permite asignar problemas concurrentes directamente en constructos concurrentes en lugar de lidiar con los detalles de iniciar y administrar hilos, y de mapear la lógica de manera uniforme en los hilos disponibles.

Por ejemplo, supongamos que escribes un servidor web y te gustaría que cada conexión aceptada se maneje concurrentemente con todas las demás conexiones. En algunos lenguajes, antes de que tu servidor web comience a aceptar conexiones, probablemente tendrías que crear una colección de hilos, comúnmente llamada *pool de hilos* (thread pool), y luego asignar las conexiones entrantes a los hilos. Luego, dentro de cada hilo que hayas creado, tendrías que iterar sobre todas las conexiones en ese hilo para asegurarte de que todas reciban algo de tiempo de CPU. Además, tendrías que escribir la lógica de manejo de tu conexión para que sea pausable y se comparta equitativamente con las demás conexiones.

¡Uf! Por el contrario, en Go escribirías una función y luego antepondrías su invocación con la palabra clave `go`. ¡El runtime maneja todo lo demás que hemos discutido de forma automática! Cuando pasas por el proceso de diseñar tu programa, ¿bajo qué modelo crees que es más probable que optes por la concurrencia? ¿Cuál crees que es más probable que resulte correcto?

Las primitivas de concurrencia de Go también facilitan la composición de problemas más grandes. Como veremos en la sección "Canales", la primitiva de *canal* (channel) de Go proporciona una forma componible y segura en un entorno concurrente para comunicarse entre procesos concurrentes.

He pasado por alto la mayor parte de los detalles sobre cómo funcionan estas cosas, pero quería darte una idea de cómo Go te invita a utilizar la concurrencia en tu programa para ayudarte a resolver tus problemas de una manera clara y con buen rendimiento. En el próximo capítulo discutiremos la filosofía de la concurrencia y por qué Go acertó en tantas cosas. Si estás ansioso por adentrarte en algo de código, es posible que desees pasar al Capítulo 3.
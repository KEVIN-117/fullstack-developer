# Capítulo 6: Goroutines y el Entorno de Ejecución de Go

Cuando trabajas en Go, ¡es divertido sumergirse directamente en el uso de la concurrencia porque el lenguaje lo hace muy fácil! Muy raramente he necesitado entender cómo el entorno de ejecución (runtime) une todo bajo el capó. Aun así, ha habido momentos en los que esta información ha sido útil, y todas las cosas discutidas en el Capítulo 2 son posibles gracias al runtime, por lo que vale la pena tomarse un momento para echar un vistazo a cómo funciona. ¡Tiene el beneficio adicional de ser interesante!

De todas las cosas que el runtime de Go hace por ti, generar y gestionar goroutines es probablemente la más beneficiosa para ti y tu software. Google, la empresa que dio a luz a Go, tiene una historia de poner a trabajar teorías de la informática y artículos de investigación (white papers), por lo que no es de extrañar que Go contenga varias ideas del mundo académico. Lo que es sorprendente es la cantidad de sofisticación que hay detrás de cada goroutine. Go ha hecho un trabajo maravilloso al utilizar algunas ideas potentes que hacen que tu programa sea más eficiente, pero abstrayendo estos detalles y presentando una fachada muy simple para que los desarrolladores trabajen con ella.

## Robo de Trabajo (Work Stealing)

Como discutimos en las secciones "Cómo te ayuda esto" y "Goroutines", Go se encargará de multiplexar las goroutines en hilos (threads) del sistema operativo por ti. El algoritmo que utiliza para ello se conoce como estrategia de *robo de trabajo* (work stealing). ¿Qué significa esto?

Primero, veamos una estrategia ingenua para compartir el trabajo entre muchos procesadores, algo llamado *planificación justa* (fair scheduling). En un esfuerzo por asegurar que todos los procesadores se utilicen por igual, podríamos distribuir uniformemente la carga entre todos los procesadores disponibles. Imagina que hay `n` procesadores y `x` tareas a realizar. En la estrategia de planificación justa, cada procesador recibiría `x/n` tareas:

![[../../../assets/Pasted image 20260518150621.png]]
*(Imagen omitida: Tareas distribuidas uniformemente)*

Lamentablemente, este enfoque plantea problemas. Si recuerdas la sección "Goroutines", Go modela la concurrencia utilizando un modelo fork-join. En un paradigma fork-join, es probable que las tareas dependan unas de otras, y resulta que dividirlas ingenuamente entre los procesadores probablemente causará que uno de los procesadores esté infrautilizado. No solo eso, sino que también puede llevar a una mala localidad de caché (cache locality), ya que las tareas que requieren los mismos datos se programan en otros procesadores. Veamos un ejemplo de por qué.

Considera un programa sencillo que da como resultado la distribución de trabajo descrita anteriormente. ¿Qué pasaría si la tarea dos tardara más en completarse que las tareas uno y tres combinadas?

| Tiempo | P1 | P2 |
|---|---|---|
| | T1 | T2 |
| n+a | T3 | T2 |
| n+a+b | (inactivo) | T4 |

Sea cual sea la duración del tiempo entre `a` y `b`, el procesador uno estará inactivo.

¿Qué ocurre si hay interdependencias entre las tareas, si una tarea asignada a un procesador requiere el resultado de una tarea asignada a otro procesador? Por ejemplo, ¿qué pasaría si la tarea uno dependiera de la tarea cuatro?

| Tiempo | P1 | P2 |
|---|---|---|
| | T1 | T2 |
| n+a | (bloqueado) | T2 |
| n+a+b | (bloqueado) | T4 |
| n+a+b+c | T1 | (inactivo) |
| n+a+b+c+d | T3 | (inactivo) |

En este escenario, el procesador uno está completamente inactivo mientras se calculan las tareas dos y cuatro. Mientras el procesador uno estaba bloqueado en la tarea uno, y el procesador dos estaba ocupado con la tarea dos, el procesador uno podría haber estado trabajando en la tarea cuatro para desbloquearse a sí mismo.

Bien, esto suena como problemas básicos de equilibrio de carga que tal vez una cola FIFO pueda ayudar a resolver, así que intentémoslo: las tareas de trabajo se programan en la cola, y nuestros procesadores desencolan tareas a medida que tienen capacidad, o se bloquean en las uniones (joins). Este es el primer tipo de algoritmo de robo de trabajo que veremos. ¿Resuelve esto el problema?
![[../../../assets/Pasted image 20260518150639.png]]
*(Imagen omitida: Cola centralizada)*

La respuesta es *quizás*. Es mejor que simplemente dividir las tareas entre los procesadores porque resuelve el problema de los procesadores infrautilizados, pero ahora hemos introducido una estructura de datos centralizada que todos los procesadores deben utilizar. Como se discutió en "Sincronización de acceso a la memoria", sabemos que entrar y salir continuamente de secciones críticas es extremadamente costoso. No solo eso, sino que nuestros problemas de localidad de caché no han hecho más que agravarse: ahora vamos a cargar la cola centralizada en la caché de cada procesador cada vez que quiera encolar o desencolar una tarea. Aun así, para operaciones de grano grueso, este puede ser un enfoque válido. Sin embargo, las goroutines no suelen ser de grano grueso, por lo que una cola centralizada probablemente no sea una gran elección para nuestro algoritmo de programación de trabajo.

El siguiente salto que podríamos dar es descentralizar las colas de trabajo. Podríamos dar a cada procesador su propio hilo y una cola de dos extremos, o *deque*, como esto:
![[../../../assets/Pasted image 20260518150647.png]]
*(Imagen omitida: Colas distribuidas por procesador)*

Bien, hemos solucionado nuestro problema con una estructura de datos central bajo alta contención, pero ¿qué pasa con los problemas de localidad de caché y utilización del procesador? Y sobre ese tema, si el trabajo comienza en P1, y todas las tareas bifurcadas (forked) se colocan en la cola de P1, ¿cómo llega el trabajo a P2? ¿Y no tenemos un problema con el cambio de contexto ahora que las tareas se mueven entre colas? Repasemos las reglas de cómo funciona un algoritmo de robo de trabajo con colas distribuidas.

Como recordatorio, recuerda que Go sigue un modelo fork-join para la concurrencia. Los forks son cuando se inician las goroutines, y los puntos de unión (join points) son cuando dos o más goroutines se sincronizan a través de canales o tipos en el paquete `sync`. El algoritmo de robo de trabajo sigue unas cuantas reglas básicas. Dado un hilo de ejecución:

1. En un punto de bifurcación (fork point), añadir tareas al final (tail) del deque asociado al hilo.
2. Si el hilo está inactivo, robar trabajo de la cabeza (head) del deque asociado a algún otro hilo aleatorio.
3. En un punto de unión (join point) que aún no puede realizarse (es decir, la goroutine con la que está sincronizada aún no ha terminado), sacar (pop) trabajo del final del propio deque del hilo.
4. Si el deque del hilo está vacío, entonces:
    - Detenerse en una unión (stall).
    - Robar trabajo de la cabeza de un deque asociado a un hilo aleatorio.

Esto es un poco abstracto, así que veamos algo de código real y veamos este algoritmo en acción. Toma el siguiente programa, que calcula la secuencia de Fibonacci de forma recursiva:

```go
var fib func(n int) <-chan int
fib = func(n int) <-chan int {
    result := make(chan int)
    go func() {
        defer close(result)
        if n <= 2 {
            result <- 1
            return
        }
        result <- <-fib(n-1) + <-fib(n-2)
    }()
    return result
}

func main() {
    fmt.Printf("fib(4) = %v\n", <-fib(4))
}
```

Veamos cómo funcionaría esta versión de un algoritmo de robo de trabajo en este programa Go. Digamos que este programa se está ejecutando en una máquina hipotética con dos procesadores de un solo núcleo. Generaremos un hilo del SO en cada procesador, T1 para el procesador uno, y T2 para el procesador dos. A medida que avancemos en este ejemplo, iré saltando de T1 a T2 en un esfuerzo por proporcionar cierta estructura. En realidad, nada de esto es determinista.

Así que nuestro programa comienza. Inicialmente, solo tenemos una goroutine, la *goroutine principal* (main goroutine), y supondremos que está programada en el procesador uno:

| Pila de llamadas T1 | Deque de trabajo T1 | Pila de llamadas T2 | Deque de trabajo T2 |
|---|---|---|---|
| (main goroutine) | | | |

A continuación, llegamos a la llamada a `fib(4)`. Esta goroutine se programará y se colocará en el final del deque de trabajo de T1, y la goroutine padre continuará procesando:

| Pila de llamadas T1 | Deque de trabajo T1 | Pila de llamadas T2 | Deque de trabajo T2 |
|---|---|---|---|
| (main goroutine) | `fib(4)` | | |

En este punto, dependiendo del tiempo, ocurrirá una de dos cosas: T1 o T2 robarán la goroutine que aloja la llamada a `fib(4)`. Para este ejemplo, para ilustrar más claramente el algoritmo, supondremos que T1 gana el robo; sin embargo, es importante notar que cualquiera de los dos hilos podría ganar.

| Pila de llamadas T1 | Deque de trabajo T1 | Pila de llamadas T2 | Deque de trabajo T2 |
|---|---|---|---|
| (main) (punto unión no realizado) | | | |
| `fib(4)` | | | |

`fib(4)` se ejecuta en T1 y —debido a que el orden de las operaciones para la suma es de izquierda a derecha— pone `fib(3)` y luego `fib(2)` en el final de su deque:

| Pila de llamadas T1 | Deque de trabajo T1 | Pila de llamadas T2 | Deque de trabajo T2 |
|---|---|---|---|
| (main) (punto unión no realizado) | `fib(3)` | | |
| `fib(4)` | `fib(2)` | | |

En este punto, T2 sigue inactivo, por lo que extrae `fib(3)` de la cabeza del deque de T1. Fíjate que `fib(2)` —lo último que `fib(4)` puso en la cola y, por tanto, lo primero que T1 probablemente necesitará calcular— permanece en T1. Discutiremos por qué esto es importante más adelante.

| Pila de llamadas T1 | Deque de trabajo T1 | Pila de llamadas T2 | Deque de trabajo T2 |
|---|---|---|---|
| (main) (punto unión no realizado) | `fib(2)` | `fib(3)` | |
| `fib(4)` | | | |

Mientras tanto, T1 llega a un punto en el que no puede seguir trabajando en `fib(4)` porque está esperando los canales devueltos por `fib(3)` y `fib(2)`. Este es el *punto de unión no realizado* en el paso tres de nuestro algoritmo. Debido a esto, saca trabajo del final de su propia cola, aquí `fib(2)`:

| Pila de llamadas T1 | Deque de trabajo T1 | Pila de llamadas T2 | Deque de trabajo T2 |
|---|---|---|---|
| (main) (punto unión no realizado) | | `fib(3)` | |
| `fib(4)` (punto unión no realizado) | | | |
| `fib(2)` | | | |

Aquí se vuelve un poco confuso. Debido a que no estamos utilizando el retroceso (backtracking) en nuestro algoritmo recursivo, vamos a programar otra goroutine para calcular `fib(2)`. Esta es una goroutine nueva y separada de la que se acaba de programar en T1. La que se acaba de programar en T1 formaba parte de la llamada a `fib(4)` (es decir, 4-2); la nueva goroutine forma parte de la llamada a `fib(3)` (es decir, 3-1). Aquí están las goroutines recién programadas de la llamada a `fib(3)`:

| Pila de llamadas T1 | Deque de trabajo T1 | Pila de llamadas T2 | Deque de trabajo T2 |
|---|---|---|---|
| (main) (punto unión no realizado) | | `fib(3)` | `fib(2)` |
| `fib(4)` (punto unión no realizado) | | | `fib(1)` |
| `fib(2)` | | | |

A continuación, T1 alcanza el caso base de nuestro algoritmo recursivo de Fibonacci (`n <= 2`) y devuelve 1:

| Pila de llamadas T1 | Deque de trabajo T1 | Pila de llamadas T2 | Deque de trabajo T2 |
|---|---|---|---|
| (main) (punto unión no realizado) | | `fib(3)` | `fib(2)` |
| `fib(4)` (punto unión no realizado) | | | `fib(1)` |
| (devuelve 1) | | | |

Entonces T2 llega a un punto de unión no realizado y saca trabajo del final de su deque:

| Pila de llamadas T1 | Deque de trabajo T1 | Pila de llamadas T2 | Deque de trabajo T2 |
|---|---|---|---|
| (main) (punto unión no realizado) | | `fib(3)` (punto unión no realizado) | `fib(2)` |
| `fib(4)` (punto unión no realizado) | | `fib(1)` | |
| (devuelve 1) | | | |

Ahora T1 vuelve a estar inactivo, por lo que roba trabajo de la cabeza del deque de trabajo de T2:

| Pila de llamadas T1 | Deque de trabajo T1 | Pila de llamadas T2 | Deque de trabajo T2 |
|---|---|---|---|
| (main) (punto unión no realizado) | | `fib(3)` (punto unión no realizado) | |
| `fib(4)` (punto unión no realizado) | | `fib(1)` | |
| `fib(2)` | | | |

T2 vuelve a alcanzar el caso base (`n <= 2`) y devuelve 1:

| Pila de llamadas T1 | Deque de trabajo T1 | Pila de llamadas T2 | Deque de trabajo T2 |
|---|---|---|---|
| (main) (punto unión no realizado) | | `fib(3)` (punto unión no realizado) | |
| `fib(4)` (punto unión no realizado) | | (devuelve 1) | |
| `fib(2)` | | | |

A continuación, T1 también alcanza el caso base y devuelve 1:

| Pila de llamadas T1 | Deque de trabajo T1 | Pila de llamadas T2 | Deque de trabajo T2 |
|---|---|---|---|
| (main) (punto unión no realizado) | | `fib(3)` (punto unión no realizado) | |
| `fib(4)` (punto unión no realizado) | | (devuelve 1) | |
| (devuelve 1) | | | |

La llamada de T2 a `fib(3)` tiene ahora dos *puntos de unión realizados*; es decir, las llamadas a `fib(2)` y `fib(1)` han devuelto resultados en sus canales, y las dos goroutines generadas se han unido de nuevo a su goroutine padre, la que aloja la llamada a `fib(3)`. Realiza su suma (1+1=2) y devuelve el resultado en su canal:

| Pila de llamadas T1 | Deque de trabajo T1 | Pila de llamadas T2 | Deque de trabajo T2 |
|---|---|---|---|
| (main) (punto unión no realizado) | | (devuelve 2) | |
| `fib(4)` (punto unión no realizado) | | | |

A continuación sucede lo mismo: la goroutine que aloja la llamada a `fib(4)` tenía dos puntos de unión no realizados: `fib(3)` y `fib(2)`. Acabamos de completar la unión para `fib(3)` en el paso anterior, y la unión para `fib(2)` se completó como la última tarea que T2 finalizó. Una vez más, se realiza la suma (2+1=3) y el resultado se devuelve en el canal de `fib(4)`:

| Pila de llamadas T1 | Deque de trabajo T1 | Pila de llamadas T2 | Deque de trabajo T2 |
|---|---|---|---|
| (main) (punto unión no realizado) | | | |
| (devuelve 3) | | | |

En este punto, hemos realizado el punto de unión en la goroutine principal (`<-fib(4)`), y la goroutine principal puede continuar. Lo hace imprimiendo el resultado:

| Pila de llamadas T1 | Deque de trabajo T1 | Pila de llamadas T2 | Deque de trabajo T2 |
|---|---|---|---|
| (imprime 3) | | | |

Ahora, examinemos algunas propiedades interesantes de este algoritmo. Recuerda que un hilo de ejecución tanto pone (push) como (cuando es necesario) saca (pop) del final de su deque de trabajo. El trabajo que se encuentra en el final de su deque tiene un par de propiedades interesantes:

**Es el trabajo que más probablemente se necesite para completar la unión (join) del padre.**
Completar las uniones más rápidamente significa que nuestro programa es probable que rinda mejor, y también que mantenga menos cosas en memoria.

**Es el trabajo que más probablemente siga en la caché de nuestro procesador.**
Puesto que es el trabajo en el que el hilo estuvo trabajando por última vez antes de su trabajo actual, es probable que esta información permanezca en la caché de la CPU en la que se está ejecutando el hilo. Esto significa menos fallos de caché (cache misses).

En general, programar el trabajo de esta manera tiene muchos beneficios de rendimiento implícitos.

## ¿Robar Tareas o Continuaciones?

Una cosa que hemos pasado por alto es la cuestión de qué trabajo estamos encolando y robando. Bajo un paradigma fork-join, hay dos opciones: tareas y continuaciones. Para asegurarnos de que tienes una comprensión clara de qué son las tareas y las continuaciones en Go, miremos nuestro programa Fibonacci una vez más:

```go
func fib(n int) <-chan int {
    result := make(chan int)
    go func() { // 1
        // ...
    }()
    return result // 2
}
```

1. En Go, las goroutines son **tareas**.
2. Todo lo que sigue a la llamada de una goroutine es la **continuación**.

En nuestro recorrido anterior de un algoritmo de robo de trabajo de cola distribuida, estábamos encolando tareas, o goroutines. Puesto que una goroutine aloja funciones que encapsulan perfectamente un cuerpo de trabajo, esta es una forma natural de pensar en las cosas; sin embargo, no es así como funciona realmente el algoritmo de robo de trabajo de Go. El algoritmo de robo de trabajo de Go encola y roba continuaciones.

Entonces, ¿por qué es esto importante? ¿Qué nos aporta encolar y robar continuaciones que no nos aporte encolar y robar tareas? Para empezar a responder a esta pregunta, fijémonos en nuestros puntos de unión.

Bajo nuestro algoritmo, cuando un hilo de ejecución llega a un punto de unión no realizado, el hilo debe pausar la ejecución e ir a pescar una tarea para robar. Esto se denomina una *unión con estancamiento* (stalling join) porque se está estancando en la unión mientras busca trabajo que hacer. Tanto los algoritmos de robo de tareas como los de robo de continuaciones tienen uniones con estancamiento, pero hay una diferencia significativa en la frecuencia con la que se producen los estancamientos.

Considera esto: al crear una goroutine, es muy probable que tu programa quiera que se ejecute la función de esa goroutine. También es razonablemente probable que la continuación de esa goroutine quiera unirse en algún momento con esa goroutine. Y no es raro que la continuación intente una unión antes de que la goroutine haya terminado de completarse. Dados estos axiomas, al programar una goroutine, tiene sentido empezar a trabajar en ella inmediatamente.

Ahora piensa de nuevo en las propiedades de un hilo que pone y saca trabajo de/hacia el final de su deque, y de otros hilos que sacan trabajo de la cabeza. Si ponemos la continuación en el final del deque, es menos probable que sea robada por otro hilo que esté sacando cosas de la cabeza del deque y, por lo tanto, es muy probable que podamos volver a recogerla cuando hayamos terminado de ejecutar nuestra goroutine, evitando así un estancamiento. Esto también hace que la tarea bifurcada (forked) se parezca mucho a una llamada a función: el hilo salta a ejecutar la goroutine y luego vuelve a la continuación después de haber terminado.

Al final, el robo de continuaciones se considera teóricamente superior al robo de tareas y, por lo tanto, es mejor encolar la continuación y no la goroutine. Como puedes ver en la siguiente tabla, el robo de continuaciones tiene varios beneficios:

| | Continuación | Hijo (Tarea) |
|---|---|---|
| Tamaño de la cola | Acotado | No acotado |
| Orden de ejecución | Serial | Fuera de orden |
| Punto de unión | Sin estancamiento | Con estancamiento |

Entonces, ¿por qué no todos los algoritmos de robo de trabajo implementan el robo de continuaciones? Bueno, el robo de continuaciones suele requerir el apoyo del compilador. Por suerte, Go tiene su propio compilador, y el robo de continuaciones es como se implementa el algoritmo de robo de trabajo de Go. Los lenguajes que no tienen este lujo suelen implementar el robo de tareas, o del llamado "hijo", como una biblioteca.

Aunque este modelo se acerca más al algoritmo de Go, sigue sin representar toda la imagen. Go realiza optimizaciones adicionales. Antes de analizarlas, preparemos el terreno empezando a utilizar la nomenclatura del planificador de Go tal y como aparece en el código fuente.

El planificador de Go tiene tres conceptos principales:

**G**
Una goroutine.

**M**
Un hilo del SO (también referenciado como *machine* en el código fuente).

**P**
Un contexto (también referenciado como *processor* en el código fuente).

En nuestra discusión sobre el robo de trabajo, *M* es equivalente a *T*, y *P* es equivalente al deque de trabajo (cambiar `GOMAXPROCS` cambia cuántos de estos se asignan). La *G* es una goroutine, pero ten en cuenta que representa el *estado* actual de una goroutine, sobre todo su contador de programa (PC). Esto permite que una G represente una continuación para que Go pueda realizar el robo de continuaciones.

En el runtime de Go, se inician las M, que luego alojan a las P, que a su vez programan y alojan a las G:
![[../../../assets/Pasted image 20260518150733.png]]
*(Imagen omitida: M -> P -> G)*

Personalmente, me resulta difícil seguir el análisis de cómo funciona este algoritmo cuando solo se utiliza esta notación, así que utilizaré sus nombres completos en este análisis. Muy bien, ahora que tenemos claros nuestros términos, ¡echemos un vistazo a cómo funciona el planificador de Go!

Como hemos mencionado, el ajuste `GOMAXPROCS` controla cuántos contextos están disponibles para que los utilice el runtime. El ajuste por defecto es que haya un contexto por cada CPU lógica en la máquina anfitriona. A diferencia de los contextos, puede haber más o menos hilos del SO que núcleos para ayudar al runtime de Go a gestionar cosas como la recolección de basura y las goroutines. Menciono esto porque hay una garantía muy importante en el runtime: siempre habrá al menos suficientes hilos del SO disponibles para encargarse de alojar cada contexto. Esto permite al runtime realizar una optimización importante. El runtime también contiene un pool de hilos para los hilos que no se están utilizando en ese momento. ¡Hablemos ahora de esas optimizaciones!

Considera qué pasaría si alguna de las goroutines se bloqueara por entrada/salida o por realizar una llamada al sistema fuera del runtime de Go. El hilo del SO que aloja la goroutine también se bloquearía y sería incapaz de progresar o de alojar cualquier otra goroutine. Lógicamente, esto está bien, pero desde una perspectiva de rendimiento, Go podría hacer más para mantener los procesadores de la máquina tan activos como fuera posible.

Lo que hace Go en esta situación es disociar el contexto del hilo del SO para que el contexto pueda entregarse a otro hilo del SO no bloqueado. Esto permite que el contexto programe más goroutines, lo que permite al runtime mantener activas las CPUs de la máquina anfitriona. La goroutine bloqueada permanece asociada al hilo bloqueado.

Cuando la goroutine finalmente se desbloquea, el hilo del SO anfitrión intenta recuperar un contexto de uno de los otros hilos del SO para poder seguir ejecutando la goroutine anteriormente bloqueada. Sin embargo, a veces esto no siempre es posible. En este caso, el hilo colocará su goroutine en un *contexto global*, el hilo se irá a dormir y se pondrá en el pool de hilos del runtime para su uso futuro (por ejemplo, si una goroutine vuelve a bloquearse).

El contexto global que acabamos de mencionar no encaja en nuestras discusiones anteriores sobre algoritmos abstractos de robo de trabajo. Es un detalle de implementación que viene impuesto por la forma en que Go optimiza la utilización de la CPU. Para garantizar que las goroutines situadas en el contexto global no permanezcan allí perpetuamente, se añaden unos cuantos pasos adicionales al algoritmo de robo de trabajo. Periódicamente, un contexto comprobará el contexto global para ver si hay alguna goroutine allí, y cuando la cola de un contexto esté vacía, comprobará primero el contexto global en busca de trabajo que robar antes de comprobar los contextos de otros hilos del SO.

Además de la entrada/salida y las llamadas al sistema, Go también permite que las goroutines sean interrumpidas (preempted) durante cualquier llamada a función. Esto funciona en tándem con la filosofía de Go de preferir tareas concurrentes de grano muy fino, asegurando que el runtime pueda programar el trabajo de forma eficiente. Una excepción notable que el equipo ha estado tratando de resolver son las goroutines que no realizan entrada/salida, llamadas al sistema o llamadas a funciones. Actualmente, este tipo de goroutines no son interrumpibles y pueden causar problemas significativos como largas esperas de GC, o incluso interbloqueos. Afortunadamente, desde una perspectiva anecdótica, se trata de una ocurrencia ínfima.

## Presentando todo esto al Desarrollador

Ahora que entiendes cómo funcionan las goroutines bajo el capó, vamos a retirarnos una vez más y reiterar cómo los desarrolladores interactúan con todo esto: la palabra clave `go`. ¡Eso es todo!

Coloca la palabra `go` antes de una función o cierre, y habrás programado automáticamente una tarea que se ejecutará de la forma más eficiente para la máquina en la que se esté ejecutando. Como desarrolladores, seguimos pensando en las primitivas con las que estamos familiarizados: funciones. No tenemos que entender una nueva forma de hacer las cosas, estructuras de datos complicadas o algoritmos de planificación.

Escalabilidad, eficiencia y simplicidad. *Esto* es lo que hace que las goroutines sean tan intrigantes.

## Conclusión

Ya hemos recorrido todo el panorama de la concurrencia en Go: desde los primeros principios hasta el uso básico, pasando por los patrones y cómo hace las cosas el entorno de ejecución. Espero sinceramente que este libro te haya dado una buena comprensión de la concurrencia en Go y te ayude a completar todos tus gloriosos "hacks". ¡Gracias!

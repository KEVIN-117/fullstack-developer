# Capítulo 3: Bloques de Construcción de Concurrencia en Go

En este capítulo, discutiremos el rico tapiz de características de Go que respaldan su historia de concurrencia. Al final de este capítulo, deberías tener una buena comprensión de la sintaxis, las funciones y los paquetes disponibles para ti, y su funcionalidad.

## Goroutines

Las goroutines son una de las unidades de organización más básicas en un programa Go, por lo que es importante que entendamos qué son y cómo funcionan. De hecho, todo programa Go tiene al menos una goroutine: la *goroutine principal* (main goroutine), que se crea y se inicia automáticamente cuando comienza el proceso. En casi cualquier programa, es probable que tarde o temprano recurras a una goroutine para que te ayude a resolver tus problemas. Entonces, ¿qué son?

En pocas palabras, una goroutine es una función que se ejecuta de forma concurrente (recuerda: ¡no necesariamente en paralelo!) junto con otro código. Puedes iniciar una simplemente colocando la palabra clave `go` antes de una función:

```go
func main() {
    go sayHello()
    // continúa ejecutando el resto de la función...
}

func sayHello() {
    fmt.Println("hello")
}
```

¡Las funciones anónimas también funcionan! Aquí hay un ejemplo que hace lo mismo que el ejemplo anterior; sin embargo, en lugar de crear una goroutine a partir de una función, creamos una goroutine a partir de una función anónima:

```go
go func() {
    fmt.Println("hello")
}() // 1
```

1. Ten en cuenta que debemos invocar la función anónima de inmediato para usar la palabra clave `go`.

Alternativamente, puedes asignar la función a una variable y llamar a la función anónima de esta manera:

```go
sayHello := func() {
    fmt.Println("hello")
}
go sayHello()
```

¡Qué genial es esto! ¡Podemos crear un bloque de lógica concurrente con una función y una sola palabra clave! Lo creas o no, eso es todo lo que necesitas saber para iniciar goroutines. Hay mucho que decir con respecto a cómo usarlas adecuadamente, sincronizarlas y organizarlas, pero esto es realmente todo lo que necesitas saber para comenzar a utilizarlas. El resto de este capítulo profundiza en qué *son* las goroutines y cómo funcionan. Si solo estás interesado en escribir un código que funcione correctamente con goroutines, puedes considerar saltar a la siguiente sección.

Así que veamos qué sucede detrás de escena aquí: ¿cómo funcionan realmente las goroutines? ¿Son hilos del sistema operativo (OS threads)? ¿Hilos verdes (green threads)? ¿Cuántos podemos crear?

Las goroutines son exclusivas de Go (aunque algunos otros lenguajes tienen una primitiva de concurrencia similar). No son hilos del SO, y no son exactamente hilos verdes (hilos administrados por el tiempo de ejecución de un lenguaje); son un nivel superior de abstracción conocido como *corutinas* (coroutines). Las corrutinas son simplemente subrutinas concurrentes (funciones, cierres o métodos en Go) que *no son expropiables* (nonpreemptive), es decir, no se pueden interrumpir. En cambio, las corrutinas tienen múltiples puntos a través de los cuales permiten la suspensión o el reingreso.

Lo que hace que las goroutines sean exclusivas de Go es su profunda integración con el entorno de ejecución (runtime) de Go. Las goroutines no definen sus propios puntos de suspensión o reingreso; el runtime de Go observa el comportamiento en tiempo de ejecución de las goroutines y las suspende automáticamente cuando se bloquean y luego las reanuda cuando se desbloquean. En cierto modo, esto las hace expropiables, pero solo en los puntos en los que la goroutine se ha bloqueado. Es una asociación elegante entre el runtime y la lógica de una goroutine. Por lo tanto, las goroutines se pueden considerar una clase especial de corrutina.

Las corrutinas, y por tanto las goroutines, son construcciones implícitamente concurrentes, pero la concurrencia no es una propiedad *de* una corrutina: algo debe alojar varias corrutinas simultáneamente y darle a cada una la oportunidad de ejecutarse; de lo contrario, ¡no serían concurrentes! Ten en cuenta que esto no implica que las corrutinas sean implícitamente paralelas. Ciertamente es posible tener varias corrutinas ejecutándose secuencialmente para dar la ilusión de paralelismo, y de hecho esto sucede todo el tiempo en Go.

El mecanismo de Go para alojar goroutines es una implementación de lo que se llama un *planificador M:N* (M:N scheduler), lo que significa que asigna `M` hilos verdes a `N` hilos del sistema operativo. Las goroutines luego se programan en los hilos verdes. Cuando tenemos más goroutines que hilos verdes disponibles, el planificador maneja la distribución de las goroutines a través de los hilos disponibles y se asegura de que cuando estas goroutines se bloqueen, se puedan ejecutar otras goroutines. Discutiremos cómo funciona todo esto en el Capítulo 6, pero aquí cubriremos cómo Go modela la concurrencia.

Go sigue un modelo de concurrencia llamado modelo *fork-join*. La palabra *fork* se refiere al hecho de que, en cualquier punto del programa, se puede separar una rama *hija* (child) de ejecución para que se ejecute al mismo tiempo que su *padre* (parent). La palabra *join* se refiere al hecho de que, en algún momento en el futuro, estas ramas de ejecución concurrentes se unirán nuevamente. El lugar donde el hijo se reincorpora al padre se llama *punto de unión* (join point). Aquí hay una representación gráfica para ayudarte a imaginarlo:

![[../../../assets/Fork-JoinModel.png]]

La declaración `go` es cómo Go realiza un fork, y los hilos de ejecución bifurcados son las goroutines. Volvamos a nuestro ejemplo simple de goroutine:

```go
sayHello := func() {
    fmt.Println("hello")
}
go sayHello()
// continúa ejecutando el resto de la función...
```

Aquí, la función `sayHello` se ejecutará en su propia goroutine, mientras que el resto del programa continúa ejecutándose. En este ejemplo, no hay un punto de unión (join point). La goroutine que ejecuta `sayHello` simplemente saldrá en algún momento indeterminado en el futuro, y el resto del programa ya habrá continuado su ejecución.

Sin embargo, hay un problema con este ejemplo: tal como está escrito, es indeterminado si la función `sayHello` se ejecutará alguna vez. La goroutine será *creada* y programada con el tiempo de ejecución de Go para ejecutarse, pero es posible que en realidad no tenga la oportunidad de ejecutarse antes de que salga la goroutine principal.

De hecho, debido a que omitimos el resto de la función principal por simplicidad, cuando ejecutamos este pequeño ejemplo, es casi seguro que el programa terminará de ejecutarse antes de que se inicie la goroutine que aloja la llamada a `sayHello`. Como resultado, no verás la palabra "hello" impresa en `stdout`. Podrías poner un `time.Sleep` después de crear la goroutine, pero recuerda que esto no crea realmente un punto de unión, solo una condición de carrera. Si recuerdas el Capítulo 1, aumentas la probabilidad de que la goroutine se ejecute antes de salir, pero no lo garantizas. Los puntos de unión son lo que garantiza la corrección de nuestro programa y elimina la condición de carrera.

Para crear un punto de unión, debes sincronizar la goroutine principal y la goroutine `sayHello`. Esto se puede hacer de varias maneras, pero usaré una de la que hablaremos en "El paquete sync": `sync.WaitGroup`. En este momento no es importante comprender cómo este ejemplo crea un punto de unión, solo que crea uno entre las dos goroutines. Aquí hay una versión correcta de nuestro ejemplo:

```go
var wg sync.WaitGroup
sayHello := func() {
    defer wg.Done()
    fmt.Println("hello")
}
wg.Add(1)
go sayHello()
wg.Wait() // 1
```

1. Este es el punto de unión.

Esto produce:

```
hello
```

Este ejemplo bloqueará determinísticamente la goroutine principal hasta que finalice la goroutine que aloja la función `sayHello`. Aprenderás cómo funciona `sync.WaitGroup` en "El paquete sync", pero para que nuestros ejemplos sean correctos, comenzaré a usarlo para crear puntos de unión.

Hemos estado usando muchas funciones anónimas en nuestros ejemplos para crear ejemplos rápidos de goroutines. Cambiemos nuestra atención a los cierres (closures). Los cierres se cierran alrededor del ámbito léxico en el que se crean, capturando así variables. Si ejecutas un cierre en una goroutine, ¿el cierre opera sobre una copia de estas variables o sobre las referencias originales? Hagamos una prueba y veamos:

```go
var wg sync.WaitGroup
salutation := "hello"
wg.Add(1)
go func() {
    defer wg.Done()
    salutation = "welcome" // 1
}()
wg.Wait()
fmt.Println(salutation)
```

1. Aquí vemos a la goroutine modificando el valor de la variable `salutation`.

¿Cuál crees que será el valor de `salutation`: "hello" o "welcome"? Vamos a ejecutarlo y averiguarlo:

```
welcome
```

¡Interesante! Resulta que las goroutines se ejecutan dentro del mismo espacio de direcciones en el que se crearon, por lo que nuestro programa imprime la palabra "welcome". Intentemos con otro ejemplo. ¿Qué crees que generará este programa?

```go
var wg sync.WaitGroup
for _, salutation := range []string{"hello", "greetings", "good day"} {
    wg.Add(1)
    go func() {
        defer wg.Done()
        fmt.Println(salutation) // 1
    }()
}
wg.Wait()
```

1. Aquí hacemos referencia a la variable del bucle `salutation` creada al iterar sobre un slice de cadenas.

La respuesta es más complicada de lo que la mayoría de la gente espera, y es una de las pocas cosas sorprendentes en Go. La mayoría de las personas piensa intuitivamente que esto imprimirá las palabras "hello", "greetings" y "good day" en algún orden no determinista, pero mira lo que hace:

```
good day
good day
good day
```

¡Eso es un poco sorprendente! Averigüemos qué está pasando aquí. En este ejemplo, la goroutine está ejecutando un cierre que se ha cerrado sobre la variable de iteración `salutation`, que tiene un tipo de `string`. A medida que nuestro bucle itera, a `salutation` se le asigna el siguiente valor de cadena en el literal de slice. Debido a que las goroutines que se programan pueden ejecutarse en cualquier momento en el futuro, es indeterminado qué valores se imprimirán desde dentro de la goroutine. En mi máquina, hay una alta probabilidad de que el bucle salga antes de que comiencen las goroutines. Esto significa que la variable `salutation` queda fuera de alcance. ¿Qué pasa entonces? ¿Pueden las goroutines seguir haciendo referencia a algo que ha quedado fuera de alcance? ¿No accederán las goroutines a memoria que potencialmente ha sido recolectada por el recolector de basura?

Esta es una nota al margen interesante sobre cómo Go administra la memoria. El runtime de Go es lo suficientemente observador como para saber que todavía se mantiene una referencia a la variable `salutation`, y por lo tanto transferirá la memoria al montón (heap) para que las goroutines puedan seguir accediendo a ella.

Por lo general, en mi máquina, el bucle finaliza antes de que ninguna goroutine comience a ejecutarse, por lo que `salutation` se transfiere al montón manteniendo una referencia al último valor en mi slice de cadenas, "good day". Y así, por lo general, veo "good day" impreso tres veces. La forma correcta de escribir este bucle es pasar una copia de `salutation` al cierre para que cuando se ejecute la goroutine, esté operando con los datos de su iteración del bucle:

```go
var wg sync.WaitGroup
for _, salutation := range []string{"hello", "greetings", "good day"} {
    wg.Add(1)
    go func(salutation string) { // 1
        defer wg.Done()
        fmt.Println(salutation)
    }(salutation) // 2
}
wg.Wait()
```

1. Aquí declaramos un parámetro, como cualquier otra función. Sombreamos la variable original `salutation` para hacer más evidente lo que está sucediendo.
2. Aquí pasamos la variable de la iteración actual al cierre. Se hace una copia de la estructura de la cadena, lo que garantiza que cuando se ejecute la goroutine, nos referiremos a la cadena correcta.

Y como vemos, obtenemos el resultado correcto:

```
good day
hello
greetings
```

Este ejemplo se comporta como esperaríamos y es solo un poco más detallado (verbose).

Debido a que las goroutines operan dentro del mismo espacio de direcciones que las demás y simplemente alojan funciones, utilizar goroutines es una extensión natural a la escritura de código no concurrente. El compilador de Go se encarga muy bien de anclar (pin) variables en la memoria para que las goroutines no accedan accidentalmente a la memoria liberada, lo que permite a los desarrolladores centrarse en su espacio de problemas en lugar de en la administración de la memoria; sin embargo, no es un cheque en blanco.

Dado que varias goroutines pueden operar contra el mismo espacio de direcciones, todavía tenemos que preocuparnos por la sincronización. Como hemos discutido, podemos optar por sincronizar el acceso a la memoria compartida a la que acceden las goroutines, o podemos usar primitivas de CSP para compartir memoria mediante la comunicación. Discutiremos estas técnicas más adelante en el capítulo en "Canales" y "El Paquete sync".

Otro beneficio de las goroutines es que son extraordinariamente ligeras. Aquí hay un extracto de las preguntas frecuentes (FAQ) de Go:

> A una goroutine recién creada se le asignan unos pocos kilobytes, que casi siempre es suficiente. Cuando no lo es, el tiempo de ejecución (runtime) aumenta (y reduce) automáticamente la memoria para almacenar la pila, lo que permite que muchas goroutines vivan en una cantidad modesta de memoria. La sobrecarga de la CPU promedia aproximadamente tres instrucciones baratas por llamada a función. Es práctico crear cientos de miles de goroutines en el mismo espacio de direcciones. Si las goroutines fueran solo hilos (threads), los recursos del sistema se agotarían en un número mucho menor.

Unos pocos kilobytes por goroutine; ¡eso no está nada mal! Intentemos verificar eso por nosotros mismos. Pero antes de hacerlo, tenemos que cubrir una cosa interesante sobre las goroutines: el recolector de basura (garbage collector) no hace nada para recolectar las goroutines que han sido abandonadas de alguna manera. Si escribo lo siguiente:

```go
go func() {
    // <operación que se bloqueará para siempre>
}()
// Haz un poco de trabajo
```

La goroutine aquí permanecerá hasta que el proceso salga. Discutiremos cómo abordar esto en el Capítulo 4 en la sección "Prevención de fugas de Goroutine". Usaremos esto para nuestra ventaja en el próximo ejemplo para medir realmente el tamaño de una goroutine.

En el siguiente ejemplo, combinamos el hecho de que el recolector de basura no recolecta goroutines con la capacidad del runtime de auto-inspeccionarse (introspect) y medir la cantidad de memoria asignada antes y después de la creación de la goroutine:

```go
memConsumed := func() uint64 {
    runtime.GC()
    var s runtime.MemStats
    runtime.ReadMemStats(&s)
    return s.Sys
}

var c <-chan interface{}
var wg sync.WaitGroup
noop := func() { wg.Done(); <-c } // 1

const numGoroutines = 1e4 // 2
wg.Add(numGoroutines)
before := memConsumed() // 3
for i := numGoroutines; i > 0; i-- {
    go noop()
}
wg.Wait()
after := memConsumed() // 4
fmt.Printf("%.3fkb", float64(after-before)/numGoroutines/1000)
```

1. Requerimos una goroutine que nunca salga para poder mantener varias de ellas en la memoria para su medición. No te preocupes por cómo lo logramos en este momento; solo debes saber que esta goroutine no saldrá hasta que el proceso haya terminado.
2. Aquí definimos la cantidad de goroutines que se crearán. Usaremos la ley de los grandes números para acercarnos asintóticamente al tamaño de una goroutine.
3. Aquí medimos la cantidad de memoria consumida antes de crear nuestras goroutines.
4. Y aquí medimos la cantidad de memoria consumida después de crear nuestras goroutines.

Y aquí está el resultado:

```
2.817kb
```

¡Parece que la documentación es correcta! Estas son solo goroutines vacías que no hacen nada, pero aun así nos da una idea de la cantidad de goroutines que probablemente podamos crear. La Tabla 3-1 da algunas estimaciones aproximadas de cuántas goroutines probablemente podrías crear con una CPU de 64 bits sin usar espacio de intercambio (swap).

Tabla 3-1. Análisis del número aproximado de goroutines posibles dentro de una memoria dada

| Memoria (GB) | Goroutines (#/100,000) | Orden de magnitud |
|---|---|---|
| 2^0 | 3.718 | 3 |
| 2^1 | 7.436 | 3 |
| 2^2 | 14.873 | 6 |
| 2^3 | 29.746 | 6 |
| 2^4 | 59.492 | 6 |
| 2^5 | 118.983 | 6 |
| 2^6 | 237.967 | 6 |
| 2^7 | 475.934 | 6 |
| 2^8 | 951.867 | 6 |
| 2^9 | 1903.735 | 9 |

¡Esos números son bastante grandes! En mi computadora portátil tengo 8 GB de RAM, lo que significa que en teoría puedo activar *millones* de goroutines sin requerir intercambio. Por supuesto, esto ignora otras cosas que se ejecutan en mi computadora y el contenido real de las goroutines, ¡pero este cálculo rápido demuestra cuán livianas son las goroutines!

Algo que podría desanimarnos es el *cambio de contexto* (context switching), que es cuando algo que aloja un proceso concurrente debe guardar su estado para cambiar a ejecutar un proceso concurrente diferente. Si tenemos demasiados procesos concurrentes, podemos pasar todo nuestro tiempo de CPU haciendo cambios de contexto entre ellos y nunca realizar un trabajo real. A nivel del SO, con subprocesos (threads), esto puede ser bastante costoso. El hilo del sistema operativo debe guardar cosas como valores de registro, tablas de búsqueda y mapas de memoria para poder cambiar de nuevo al hilo actual cuando sea el momento con éxito. Luego tiene que cargar la misma información para el hilo entrante.

El cambio de contexto en el software es comparativamente mucho, mucho más barato. Bajo un programador definido por software (software-defined scheduler), el runtime puede ser más selectivo en lo que se persiste para su recuperación, cómo se persiste y cuándo debe ocurrir la persistencia. Echemos un vistazo al rendimiento relativo del cambio de contexto en mi computadora portátil entre hilos del sistema operativo y goroutines. Primero, utilizaremos la suite de evaluación comparativa integrada de Linux para medir cuánto tiempo se tarda en enviar un mensaje entre dos subprocesos en el mismo núcleo:

```bash
taskset -c 0 perf bench sched pipe -T
```

Esto produce:

```
# Running 'sched/pipe' benchmark:
# Executed 1000000 pipe operations between two threads

     Total time: 2.935 [sec]

       2.935784 usecs/op
         340624 ops/sec
```

Este benchmark en realidad mide el tiempo que lleva enviar *y* recibir un mensaje en un hilo, por lo que tomaremos el resultado y lo dividiremos entre dos. Eso nos da 1.467 μs por cambio de contexto. Eso no parece estar mal, pero reservemos nuestro juicio hasta que examinemos los cambios de contexto entre las goroutines.

Construiremos un benchmark similar usando Go. He usado algunas cosas que aún no hemos discutido, así que si algo es confuso, solo sigue los comentarios y concéntrate en el resultado. El siguiente ejemplo creará dos goroutines y enviará un mensaje entre ellas:

```go
func BenchmarkContextSwitch(b *testing.B) {
    var wg sync.WaitGroup
    begin := make(chan struct{})
    c := make(chan struct{})

    var token struct{}
    sender := func() {
        defer wg.Done()
        <-begin // 1
        for i := 0; i < b.N; i++ {
            c <- token // 2
        }
    }
    receiver := func() {
        defer wg.Done()
        <-begin // 1
        for i := 0; i < b.N; i++ {
            <-c // 3
        }
    }

    wg.Add(2)
    go sender()
    go receiver()
    b.StartTimer() // 4
    close(begin)   // 5
    wg.Wait()
}
```

1. Aquí esperamos hasta que se nos diga que comencemos. No queremos que el costo de configurar y comenzar cada goroutine influya en la medición del cambio de contexto.
2. Aquí enviamos mensajes a la goroutine del receptor. Un `struct{}{}` se denomina *struct vacío* y no ocupa memoria; por lo tanto, solo estamos midiendo el tiempo que lleva señalar un mensaje.
3. Aquí recibimos un mensaje pero no hacemos nada con él.
4. Aquí comenzamos el temporizador de rendimiento.
5. Aquí le decimos a las dos goroutines que comiencen.

Ejecutamos el benchmark especificando que solo queremos utilizar una CPU para que sea una prueba similar a la prueba comparativa de Linux. Echemos un vistazo a los resultados:

```bash
go test -bench=. -cpu=1 \
src/gos-concurrency-building-blocks/goroutines/fig-ctx-switch_test.go
```

| | | | |
|---|---|---|---|
| BenchmarkContextSwitch | 5000000 | 225 | ns/op |
| PASS | | | |
| ok | command-line-arguments | 1.393s | |

225 ns por cambio de contexto, ¡guau! Eso es 0.225 μs, o un 92% más rápido que un cambio de contexto del sistema operativo en mi máquina, que si recuerdas tardó 1.467 μs. Es difícil hacer afirmaciones sobre cuántas goroutines causarán demasiado cambio de contexto, pero podemos decir cómodamente que el límite superior probablemente no sea ningún tipo de barrera para el uso de goroutines.

Habiendo leído esta sección, ahora deberías entender cómo iniciar goroutines y un poco sobre cómo funcionan. También deberías estar seguro de que puedes crear de forma segura una goroutine en cualquier momento que sientas que el espacio de problemas lo justifica. Como discutimos en la sección "La Diferencia Entre Concurrencia y Paralelismo", cuantas más goroutines crees, y si tu espacio de problemas no está limitado por un segmento concurrente según la ley de Amdahl, más se escalará tu programa con múltiples procesadores. La creación de goroutines es muy barata, por lo que solo debes discutir su costo si has demostrado que son la causa raíz de un problema de rendimiento.

## El Paquete sync

El paquete `sync` contiene las primitivas de concurrencia que son más útiles para la sincronización de acceso a memoria de bajo nivel. Si has trabajado en lenguajes que manejan la concurrencia principalmente a través de la sincronización de acceso a la memoria, es probable que estos tipos ya te resulten familiares. La diferencia entre estos lenguajes y Go es que Go ha construido un nuevo conjunto de primitivas de concurrencia sobre las primitivas de sincronización de acceso a memoria para proporcionarte un conjunto ampliado de elementos con los que trabajar. Como comentamos en "La Filosofía de Go sobre la Concurrencia", estas operaciones tienen su utilidad, principalmente en ámbitos pequeños, como una `struct`. Dependerá de ti decidir cuándo es apropiada la sincronización de acceso a la memoria. Dicho esto, comencemos a echar un vistazo a las diversas primitivas que expone el paquete `sync`.

### WaitGroup

`WaitGroup` es una excelente manera de esperar a que se complete un conjunto de operaciones concurrentes cuando no te importa el resultado de la operación concurrente o tienes otros medios de recopilar sus resultados. Si ninguna de esas condiciones es cierta, sugiero que uses canales y una declaración `select` en su lugar. `WaitGroup` es tan útil que lo presento primero para poder usarlo en secciones posteriores. Aquí hay un ejemplo básico del uso de un `WaitGroup` para esperar a que finalicen las goroutines:

```go
var wg sync.WaitGroup

wg.Add(1) // 1
go func() {
    defer wg.Done() // 2
    fmt.Println("1st goroutine sleeping...")
    time.Sleep(1 * time.Second)
}()

wg.Add(1) // 1
go func() {
    defer wg.Done() // 2
    fmt.Println("2nd goroutine sleeping...")
    time.Sleep(2 * time.Second)
}()

wg.Wait() // 3
fmt.Println("All goroutines complete.")
```

1. Aquí llamamos a `Add` con un argumento de 1 para indicar que está comenzando una goroutine.
2. Aquí llamamos a `Done` usando la palabra clave `defer` para asegurar que antes de salir del cierre de la goroutine, indicamos al `WaitGroup` que hemos salido.
3. Aquí llamamos a `Wait`, que bloqueará la goroutine principal hasta que todas las goroutines hayan indicado que salieron.

Esto produce:

```
2nd goroutine sleeping...
1st goroutine sleeping...
All goroutines complete.
```

Puedes pensar en un `WaitGroup` como un contador concurrente seguro: las llamadas a `Add` incrementan el contador por el número entero pasado, y las llamadas a `Done` decrementan el contador en uno. Las llamadas a `Wait` se bloquean hasta que el contador llega a cero.

Observa que las llamadas a `Add` se realizan fuera de las goroutines a las que ayudan a rastrear. Si no hiciéramos esto, habríamos introducido una condición de carrera, porque recuerda en "Goroutines" que no tenemos garantías de cuándo se programarán las goroutines; podríamos llegar a la llamada a `Wait` antes de que comience cualquiera de las goroutines. Si las llamadas a `Add` se hubieran colocado dentro de los cierres de las goroutines, la llamada a `Wait` podría haber regresado sin bloquearse en absoluto porque las llamadas a `Add` no se habrían llevado a cabo.

Es costumbre acoplar las llamadas a `Add` lo más cerca posible de las goroutines que están ayudando a rastrear, pero a veces encontrarás que se llama a `Add` para rastrear un grupo de goroutines todas a la vez. Suelo hacer esto antes de los bucles `for` como este:

```go
hello := func(wg *sync.WaitGroup, id int) {
    defer wg.Done()
    fmt.Printf("Hello from %v!\n", id)
}

const numGreeters = 5
var wg sync.WaitGroup
wg.Add(numGreeters)
for i := 0; i < numGreeters; i++ {
    go hello(&wg, i+1)
}
wg.Wait()
```

Esto produce:

```
Hello from 5!
Hello from 4!
Hello from 3!
Hello from 2!
Hello from 1!
```

### Mutex y RWMutex

Si ya estás familiarizado con los lenguajes que manejan la concurrencia a través de la sincronización del acceso a la memoria, entonces probablemente reconocerás de inmediato `Mutex`. Si no te cuentas entre ese grupo, no te preocupes, `Mutex` es muy fácil de entender. *Mutex* significa "exclusión mutua" y es una forma de proteger las secciones críticas de tu programa. Si recuerdas del Capítulo 1, una sección crítica es un área de tu programa que requiere acceso exclusivo a un recurso compartido. Un `Mutex` proporciona una forma segura frente a la concurrencia de expresar el acceso exclusivo a estos recursos compartidos. Para tomar prestado un "Go-ismo", mientras que los canales comparten la memoria comunicándose, un `Mutex` comparte la memoria creando una convención que los desarrolladores deben seguir para sincronizar el acceso a la memoria. Eres responsable de coordinar el acceso a esta memoria protegiendo el acceso a ella con un mutex. Aquí hay un ejemplo simple de dos goroutines que intentan incrementar y disminuir un valor común; utilizan un `Mutex` para sincronizar el acceso:

```go
var count int
var lock sync.Mutex

increment := func() {
    lock.Lock() // 1
    defer lock.Unlock() // 2
    count++
    fmt.Printf("Incrementing: %d\n", count)
}

decrement := func() {
    lock.Lock() // 1
    defer lock.Unlock() // 2
    count--
    fmt.Printf("Decrementing: %d\n", count)
}

// ... Incrementar y decrementar de manera concurrente (código simplificado)
var wg sync.WaitGroup
for i := 0; i <= 5; i++ {
    wg.Add(1)
    go func() {
        defer wg.Done()
        increment()
    }()
}

for i := 0; i <= 5; i++ {
    wg.Add(1)
    go func() {
        defer wg.Done()
        decrement()
    }()
}
wg.Wait()
fmt.Println("Arithmetic complete.")
```

1. Aquí solicitamos el uso exclusivo de la sección crítica, en este caso la variable `count`, protegida por un `Mutex`, `lock`.
2. Aquí indicamos que hemos terminado con la sección crítica que `lock` está protegiendo.

Esto produce:

```
Decrementing: -1
Incrementing: 0
Decrementing: -1
Incrementing: 0
Decrementing: -1
Decrementing: -2
Decrementing: -3
Incrementing: -2
Decrementing: -3
Incrementing: -2
Incrementing: -1
Incrementing: 0
Arithmetic complete.
```

Notarás que siempre llamamos a `Unlock` dentro de una instrucción `defer`. Este es un modismo muy común cuando se utiliza un `Mutex` para asegurar que la llamada siempre suceda, incluso al hacer `panic`. Si no lo haces, probablemente harás que tu programa se interbloquee (deadlock).

Las secciones críticas se denominan así porque reflejan un cuello de botella en tu programa. Es algo costoso entrar y salir de una sección crítica, y por lo general la gente intenta minimizar el tiempo que se pasa en las secciones críticas.

Una estrategia para hacerlo es reducir la sección transversal (cross-section) de la sección crítica. Puede haber memoria que deba compartirse entre varios procesos concurrentes, pero quizás no todos estos procesos leerán *y* escribirán en esta memoria. Si este es el caso, puedes aprovechar un tipo diferente de mutex: `sync.RWMutex`.

El `sync.RWMutex` es conceptualmente lo mismo que un `Mutex`: protege el acceso a la memoria; sin embargo, `RWMutex` te da un poco más de control sobre la memoria. Puedes solicitar un bloqueo de lectura, en cuyo caso se te otorgará acceso a menos que se mantenga el bloqueo para la escritura. Esto significa que un número arbitrario de lectores puede mantener un bloqueo de lectura siempre que no haya otra cosa que mantenga un bloqueo de escritor. Aquí hay un ejemplo que demuestra un productor que es menos activo que los numerosos consumidores que crea el código:

```go
producer := func(wg *sync.WaitGroup, l sync.Locker) { // 1
    defer wg.Done()
    for i := 5; i > 0; i-- {
        l.Lock()
        l.Unlock()
        time.Sleep(1 * time.Second) // 2
    }
}

observer := func(wg *sync.WaitGroup, l sync.Locker) {
    defer wg.Done()
    l.Lock()
    defer l.Unlock()
}
// ... Benchmark code ...
```

1. El segundo parámetro de la función `producer` es del tipo `sync.Locker`. Esta interfaz tiene dos métodos, `Lock` y `Unlock`, que satisfacen los tipos `Mutex` y `RWMutex`.
2. Aquí hacemos que el productor duerma durante un segundo para hacerlo menos activo que las goroutines del `observer`.

Esto produce:

```
Readers  RWMutex       Mutex
1        38.343µs      15.854µs
2        21.86µs       13.2µs
4        31.01µs       31.358µs
8        63.835µs      24.584µs
16       52.451µs      78.153µs
32       75.569µs      69.492µs
64       141.708µs     163.43µs
128      176.35µs      157.143µs
256      234.808µs     237.182µs
512      262.186µs     434.625µs
1024     459.349µs     850.601µs
2048     840.753µs     1.663279ms
4096     1.683672ms    2.42148ms
8192     2.167814ms    4.13665ms
16384    4.973842ms    8.197173ms
32768    9.236067ms    16.247469ms
65536    16.767161ms   30.948295ms
131072   71.457282ms   62.203475ms
262144   158.76261ms   119.634601ms
524288   303.865661ms  231.072729ms
```

Puedes ver en este ejemplo en particular que reducir la sección transversal de nuestra sección crítica en realidad solo comienza a dar sus frutos alrededor de 213 lectores. Esto variará dependiendo de lo que esté haciendo tu sección crítica, pero por lo general es aconsejable usar `RWMutex` en lugar de `Mutex` cuando tenga sentido lógico.

### Cond

El comentario para el tipo `Cond` realmente hace un gran trabajo al describir su propósito:

> ...un punto de encuentro para goroutines que esperan o anuncian la ocurrencia de un evento.

En esa definición, un "evento" es cualquier señal arbitraria entre dos o más goroutines que no contiene otra información que no sea el hecho de que ha ocurrido. Muy a menudo querrás esperar a una de estas señales antes de continuar la ejecución en una goroutine. Si quisiéramos ver cómo lograr esto sin el tipo `Cond`, un enfoque ingenuo para hacerlo es usar un bucle infinito:

```go
for conditionTrue() == false {
}
```

Sin embargo, esto consumiría todos los ciclos de un núcleo. Para arreglar eso, podríamos introducir un `time.Sleep`:

```go
for conditionTrue() == false {
    time.Sleep(1 * time.Millisecond)
}
```

Esto es mejor, pero sigue siendo ineficiente y tienes que averiguar cuánto tiempo dormir: demasiado, y degradas artificialmente el rendimiento; demasiado corto, y consumes innecesariamente demasiado tiempo de CPU. Sería mejor si hubiera algún tipo de forma para que una goroutine durmiera de manera eficiente hasta que se le indicara que se despertara y verificara su condición. Esto es exactamente lo que el tipo `Cond` hace por nosotros. Usando un `Cond`, podríamos escribir los ejemplos anteriores así:

```go
c := sync.NewCond(&sync.Mutex{}) // 1
c.L.Lock()                       // 2
for conditionTrue() == false {
    c.Wait()                     // 3
}
c.L.Unlock()                     // 4
```

1. Aquí instanciamos un nuevo `Cond`. La función `NewCond` toma un tipo que satisface la interfaz `sync.Locker`. Esto es lo que permite que el tipo `Cond` facilite la coordinación con otras goroutines de forma segura.
2. Aquí bloqueamos el `Locker` para esta condición. Esto es necesario porque la llamada a `Wait` llama automáticamente a `Unlock` en el `Locker` cuando se ingresa.
3. Aquí esperamos a ser notificados de que la condición ha ocurrido. Esta es una llamada bloqueante y la goroutine se suspenderá.
4. Aquí desbloqueamos el `Locker` para esta condición. Esto es necesario porque cuando sale la llamada a `Wait`, llama a `Lock` en el `Locker` para la condición.

Este enfoque es *mucho* más eficiente. Ten en cuenta que la llamada a `Wait` no solo bloquea, sino que *suspende* la goroutine actual, lo que permite que otras goroutines se ejecuten en el hilo del sistema operativo. Algunas otras cosas suceden cuando llamas a `Wait`: al entrar a `Wait`, se llama a `Unlock` en el `Locker` de la variable `Cond`, y al salir de `Wait`, se llama a `Lock` en el `Locker` de la variable `Cond`. En mi opinión, esto requiere un poco de tiempo para acostumbrarse; es efectivamente un efecto secundario oculto del método. Parece que estamos reteniendo este candado todo el tiempo mientras esperamos a que ocurra la condición, pero en realidad ese no es el caso. Cuando estés escaneando código, solo tendrás que estar atento a este patrón.

Ampliemos este ejemplo y mostremos ambos lados de la ecuación: una goroutine que espera una señal y una goroutine que envía señales. Digamos que tenemos una cola de longitud fija de 2 y 10 elementos que queremos colocar en la cola. Queremos encolar los elementos tan pronto como haya espacio, por lo que queremos ser notificados tan pronto como haya espacio en la cola. Intentemos usar un `Cond` para gestionar esta coordinación:

```go
c := sync.NewCond(&sync.Mutex{}) // 1
queue := make([]interface{}, 0, 10) // 2

removeFromQueue := func(delay time.Duration) {
    time.Sleep(delay)
    c.L.Lock()        // 8
    queue = queue[1:] // 9
    fmt.Println("Removed from queue")
    c.L.Unlock()      // 10
    c.Signal()        // 11
}

for i := 0; i < 10; i++ {
    c.L.Lock() // 3
    for len(queue) == 2 { // 4
        c.Wait() // 5
    }
    fmt.Println("Adding to queue")
    queue = append(queue, struct{}{})
    go removeFromQueue(1 * time.Second) // 6
    c.L.Unlock() // 7
}
```

1. Primero, creamos nuestra condición utilizando un `sync.Mutex` estándar como `Locker`.
2. A continuación, creamos una rebanada (slice) con una longitud de cero. Como sabemos que eventualmente agregaremos 10 elementos, lo instanciamos con una capacidad de 10.
3. Entramos a la sección crítica de la condición llamando a `Lock` en el `Locker` de la condición.
4. Aquí comprobamos la longitud de la cola en un bucle. Esto es importante porque una señal sobre la condición no significa necesariamente que haya ocurrido lo que estabas esperando, solo que *algo* ha ocurrido.
5. Llamamos a `Wait`, lo que suspenderá a la goroutine principal hasta que se envíe una señal en la condición.
6. Aquí creamos una nueva goroutine que desencolará un elemento después de un segundo.
7. Aquí salimos de la sección crítica de la condición ya que hemos puesto en cola correctamente un elemento.
8. Una vez más, ingresamos a la sección crítica de la condición para poder modificar datos pertinentes a la condición.
9. Aquí simulamos desencolar un elemento reasignando el encabezado del slice al segundo elemento.
10. Aquí salimos de la sección crítica de la condición ya que hemos desencolado un elemento con éxito.
11. Aquí le informamos a una goroutine que espera sobre la condición que algo ha ocurrido.

Esto produce:

```
Adding to queue
Adding to queue
Removed from queue
Adding to queue
Removed from queue
Adding to queue
Removed from queue
Adding to queue
Removed from queue
Adding to queue
Removed from queue
Adding to queue
Removed from queue
Adding to queue
Removed from queue
Adding to queue
Removed from queue
Adding to queue
```

Como puedes ver, el programa agrega con éxito los 10 elementos a la cola (y sale antes de tener la oportunidad de desencolar los dos últimos elementos). También siempre espera hasta que al menos un elemento se desencole antes de encolar otro.

También tenemos un nuevo método en este ejemplo, `Signal`. Este es uno de los dos métodos que proporciona el tipo `Cond` para notificar a las goroutines bloqueadas en una llamada a `Wait` que se ha activado la condición. El otro es un método llamado `Broadcast`. Internamente, el entorno de ejecución mantiene una lista FIFO de goroutines en espera de ser señalizadas; `Signal` encuentra a la goroutine que ha estado esperando más tiempo y lo notifica, mientras que `Broadcast` envía una señal a *todas* las goroutines que están esperando. Podría decirse que `Broadcast` es el más interesante de los dos métodos, ya que proporciona una forma de comunicarse con múltiples goroutines a la vez. Podemos reproducir trivialmente `Signal` con canales (como veremos en la sección "Canales"), pero reproducir el comportamiento de llamadas repetidas a `Broadcast` sería más difícil. Además, el tipo `Cond` es mucho más eficaz que utilizar canales.

Para tener una idea de cómo es usar `Broadcast`, imaginemos que estamos creando una aplicación de interfaz gráfica (GUI) con un botón en ella. Queremos registrar un número arbitrario de funciones que se ejecutarán cuando se haga clic en ese botón. Un `Cond` es perfecto para esto porque podemos usar su método `Broadcast` para notificar a todos los manejadores (handlers) registrados. Veamos cómo se vería eso:

```go
type Button struct { // 1
    Clicked *sync.Cond
}
button := Button{Clicked: sync.NewCond(&sync.Mutex{})}

subscribe := func(c *sync.Cond, fn func()) { // 2
    var goroutineRunning sync.WaitGroup
    goroutineRunning.Add(1)
    go func() {
        goroutineRunning.Done()
        c.L.Lock()
        defer c.L.Unlock()
        c.Wait()
        fn()
    }()
    goroutineRunning.Wait()
}

var clickRegistered sync.WaitGroup // 4
clickRegistered.Add(3)

subscribe(button.Clicked, func() { // 5
    fmt.Println("Maximizing window.")
    clickRegistered.Done()
})
subscribe(button.Clicked, func() { // 6
    fmt.Println("Displaying annoying dialog box!")
    clickRegistered.Done()
})
subscribe(button.Clicked, func() {
    fmt.Println("Mouse clicked.")
    clickRegistered.Done()
})

button.Clicked.Broadcast() // 3, 7
clickRegistered.Wait()
```

1. Definimos un tipo `Button` que contiene una condición, `Clicked`.
2. Aquí definimos una función de conveniencia que nos permitirá registrar funciones para manejar señales de una condición. Cada manejador se ejecuta en su propia goroutine, y `subscribe` no saldrá hasta que se confirme que la goroutine se está ejecutando.
3. (Se usa `Broadcast` más abajo) Aquí configuramos un manejador para cuando se levanta el botón del mouse. A su vez llama a `Broadcast` sobre el `Cond` `Clicked` para que todos los manejadores sepan que se ha hecho clic en el botón del mouse (una implementación más robusta comprobaría primero que se hubiera presionado).
4. Aquí creamos un `WaitGroup`. Esto se hace solo para garantizar que nuestro programa no salga antes de que se realicen nuestras escrituras en `stdout`.
5. Aquí registramos un manejador que simula maximizar la ventana del botón cuando se hace clic en el botón.
6. Aquí registramos un manejador que simula mostrar un cuadro de diálogo cuando se hace clic con el mouse.
7. A continuación, simulamos que un usuario levanta el botón del mouse después de haber hecho clic en el botón de la aplicación.

Esto produce:

```
Mouse clicked.
Maximizing window.
Displaying annoying dialog box!
```

Puedes ver que con una sola llamada a `Broadcast` sobre el `Cond` de `Clicked`, se ejecutan los tres manejadores. Si no fuera por el `WaitGroup` de `clickRegistered`, podríamos llamar a `button.Clicked.Broadcast()` múltiples veces, y cada vez se invocarían los tres manejadores. Esto es algo que los canales no pueden hacer fácilmente y, por lo tanto, es una de las razones principales para utilizar el tipo `Cond`.

Como ocurre con la mayoría de las otras cosas en el paquete `sync`, el uso de `Cond` funciona mejor cuando se restringe a un alcance reducido o se expone a un alcance más amplio a través de un tipo que lo encapsula.

### Once

¿Qué crees que imprimirá este código?

```go
var count int
increment := func() {
    count++
}

var once sync.Once
var wg sync.WaitGroup
wg.Add(100)
for i := 0; i < 100; i++ {
    go func() {
        defer wg.Done()
        once.Do(increment)
    }()
}
wg.Wait()
fmt.Printf("Count is %d\n", count)
```

Es tentador decir que el resultado será `Count is 100`, pero estoy seguro de que has notado la variable `sync.Once`, y que de alguna manera estamos envolviendo la llamada al incremento dentro del método `Do` de `once`. De hecho, este código imprimirá lo siguiente:

```
Count is 1
```

Como lo indica el nombre, `sync.Once` es un tipo que utiliza algunas primitivas `sync` internamente para asegurar que solo una llamada a `Do` invoca alguna vez a la función pasada, incluso en diferentes goroutines. Esto es ciertamente porque envolvemos la llamada a `increment` en un método `sync.Once.Do()`.

Puede parecer que la capacidad de llamar a una función exactamente una vez es algo extraño de encapsular y poner en el paquete estándar, pero resulta que la necesidad de este patrón surge con bastante frecuencia. Solo por diversión, revisemos la biblioteca estándar de Go y veamos con qué frecuencia el propio Go utiliza esta primitiva. Aquí hay un comando `grep` que realizará la búsqueda:

```bash
grep -ir sync.Once $(go env GOROOT)/src | wc -l
```

Esto produce:

```
70
```

Hay algunas cosas a tener en cuenta sobre la utilización de `sync.Once`. Echemos un vistazo a otro ejemplo; ¿qué crees que imprimirá?

```go
var count int
increment := func() { count++ }
decrement := func() { count-- }

var once sync.Once
once.Do(increment)
once.Do(decrement)

fmt.Printf("Count: %d\n", count)
```

Esto produce:

```
Count: 1
```

¿Es sorprendente que la salida muestre `1` y no `0`? Esto se debe a que `sync.Once` solo cuenta la cantidad de veces que se llama a `Do`, no la cantidad de veces que se llama a las funciones únicas que se pasan a `Do`. De esta manera, las copias de `sync.Once` están estrechamente unidas a las funciones con las que deben ser llamadas; una vez más, vemos cómo el uso de los tipos dentro del paquete `sync` funciona mejor dentro de un alcance estrecho. Recomiendo que formalices este acoplamiento envolviendo cualquier uso de `sync.Once` en un pequeño bloque léxico: ya sea una función pequeña o envolviendo ambos en un tipo. ¿Qué tal este ejemplo? ¿Qué crees que sucederá?

```go
var onceA, onceB sync.Once
var initB func()
initA := func() { onceB.Do(initB) } // 1
initB = func() { onceA.Do(initA) } // 2
onceA.Do(initA)
```

1. Esta llamada no puede continuar hasta que regrese la llamada en (2).
2. Esta llamada no puede continuar hasta que regrese la llamada en (1).

Este programa se interbloqueará (deadlock) porque la llamada a `Do` en (1) no continuará hasta que salga la llamada a `Do` en (2), un ejemplo clásico de interbloqueo. Para algunos, esto puede ser un poco contradictorio, ya que parece que estamos usando `sync.Once` de la forma prevista para protegernos contra una inicialización múltiple, pero lo único que garantiza `sync.Once` es que tus funciones solo se llamarán una vez. A veces, esto se hace bloqueando por completo (deadlocking) el programa y exponiendo la falla en tu lógica, en este caso, una referencia circular.

### Pool

`Pool` es una implementación segura ante concurrencia del patrón de diseño de grupo de objetos (object pool pattern). Una explicación completa del patrón de pool de objetos se deja mejor para la literatura sobre patrones de diseño; sin embargo, dado que `Pool` reside en el paquete `sync`, analizaremos brevemente por qué podría interesarte utilizarlo.

A un alto nivel, el patrón del pool es una forma de crear y poner a disposición una cantidad fija, o un grupo, de cosas para usar. Se usa comúnmente para restringir la creación de cosas que son costosas (por ejemplo, conexiones a bases de datos) de modo que solo se cree una cantidad fija de ellas, pero una cantidad indeterminada de operaciones aún puede solicitar acceso a estas cosas. En el caso de `sync.Pool` de Go, este tipo de datos puede ser usado de manera segura por múltiples goroutines.

La interfaz principal de `Pool` es su método `Get`. Cuando se lo llama, `Get` primero verificará si hay instancias disponibles dentro del pool para devolver al invocador, y si no, llamará a su variable miembro `New` para crear una nueva. Cuando terminan, los invocadores llaman a `Put` para colocar la instancia con la que estaban trabajando en el grupo para que la utilicen otros procesos. Aquí hay un ejemplo simple para demostrar:

```go
myPool := &sync.Pool{
    New: func() interface{} {
        fmt.Println("Creating new instance.")
        return struct{}{}
    },
}

myPool.Get() // 1
instance := myPool.Get() // 1
myPool.Put(instance) // 2
myPool.Get() // 3
```

1. Aquí llamamos a `Get` en el pool. Estas llamadas invocarán la función `New` definida en el pool ya que aún no se han instanciado instancias.
2. Aquí volvemos a poner en el pool una instancia que se recuperó previamente. Esto aumenta el número disponible de instancias a uno.
3. Cuando se ejecuta esta llamada, reutilizaremos la instancia previamente asignada y la volveremos a colocar en el pool. La función `New` no será invocada.

Como podemos ver, solo vemos dos llamadas a la función `New`:

```
Creating new instance.
Creating new instance.
```

Entonces, ¿por qué usar un pool y no solo instanciar objetos a medida que avanzas? Go tiene un recolector de basura, por lo que los objetos instanciados se limpiarán automáticamente. ¿Cuál es el punto? Considera este ejemplo:

```go
var numCalcsCreated int
calcPool := &sync.Pool{
    New: func() interface{} {
        numCalcsCreated += 1
        mem := make([]byte, 1024)
        return &mem // 1
    },
}

// Inicia el pool con 4KB de memoria
calcPool.Put(calcPool.New())
calcPool.Put(calcPool.New())
calcPool.Put(calcPool.New())
calcPool.Put(calcPool.New())

const numWorkers = 1024 * 1024
var wg sync.WaitGroup
wg.Add(numWorkers)
for i := 0; i < numWorkers; i++ {
    go func() {
        defer wg.Done()
        mem := calcPool.Get().(*[]byte) // 2
        defer calcPool.Put(mem)

        // Asume que estamos haciendo algo interesante con la memoria aquí
    }()
}
wg.Wait()
fmt.Printf("%d calculators were created.", numCalcsCreated)
```

1. Observa que estamos almacenando la *dirección* del slice de bytes.
2. Y aquí estamos afirmando que el tipo es un puntero a un slice de bytes.

Esto produce:

```
8 calculators were created.
```

Si hubiera ejecutado este ejemplo sin un `sync.Pool`, aunque los resultados no son deterministas, en el peor de los casos podría haber estado intentando asignar un gigabyte de memoria, pero como ves en el resultado, solo he asignado 4 KB.

Otra situación común donde un `Pool` es útil es para calentar una caché de objetos pre-asignados para operaciones que deben ejecutarse lo más rápido posible. En este caso, en lugar de tratar de proteger la memoria de la máquina host limitando la cantidad de objetos creados, estamos tratando de proteger el tiempo de los consumidores cargando por adelantado (front-loading) el tiempo que lleva obtener una referencia a otro objeto. Esto es muy común cuando se escriben servidores de red de alto rendimiento que intentan responder a las solicitudes lo más rápido posible. Echemos un vistazo a un escenario de este tipo.

Primero, creemos una función que simule la creación de una conexión a un servicio. Haremos que esta conexión tome mucho tiempo:

```go
func connectToService() interface{} {
    time.Sleep(1 * time.Second)
    return struct{}{}
}
```

A continuación, veamos qué tan eficiente sería un servicio de red si para cada solicitud iniciáramos una nueva conexión con el servicio. Escribiremos un manejador de red (network handler) que abre una conexión a otro servicio por cada conexión que el manejador de red acepte. Para hacer que la evaluación comparativa sea sencilla, solo permitiremos una conexión a la vez:

```go
func startNetworkDaemon() *sync.WaitGroup {
    var wg sync.WaitGroup
    wg.Add(1)
    go func() {
        server, err := net.Listen("tcp", "localhost:8080")
        if err != nil {
            log.Fatalf("cannot listen: %v", err)
        }
        defer server.Close()
        wg.Done()

        for {
            conn, err := server.Accept()
            if err != nil {
                log.Printf("cannot accept connection: %v", err)
                continue
            }
            connectToService()
            fmt.Fprintln(conn, "")
            conn.Close()
        }
    }()
    return &wg
}
```

Ahora vamos a realizar un benchmark de esto:

```go
func BenchmarkNetworkRequest(b *testing.B) {
    daemonStarted := startNetworkDaemon()
    daemonStarted.Wait()

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        conn, err := net.Dial("tcp", "localhost:8080")
        if err != nil {
            b.Fatalf("cannot dial host: %v", err)
        }
        if _, err := ioutil.ReadAll(conn); err != nil {
            b.Fatalf("cannot read: %v", err)
        }
        conn.Close()
    }
}
```

```bash
go test -bench=. src/gos-concurrency-building-blocks/sync/pool/fig-pool-network-daemon_test.go
```

Esto produce:

| | | | |
|---|---|---|---|
| BenchmarkNetworkRequest-8 | 10 | 1000385643 | ns/op |
| PASS | | | |
| ok | command-line-arguments | 11.008s | |

Parece que tarda aproximadamente 1E9 ns/op. Esto parece razonable en cuanto al rendimiento, pero veamos si podemos mejorarlo usando un `sync.Pool` para alojar conexiones a nuestro servicio ficticio:

```go
func warmupServiceConnCache() *sync.Pool {
    p := &sync.Pool{
        New: connectToService,
    }
    for i := 0; i < 10; i++ {
        p.Put(p.New())
    }
    return p
}

func startNetworkDaemon() *sync.WaitGroup {
    var wg sync.WaitGroup
    wg.Add(1)
    go func() {
        connPool := warmupServiceConnCache()

        server, err := net.Listen("tcp", "localhost:8080")
        if err != nil {
            log.Fatalf("cannot listen: %v", err)
        }
        defer server.Close()
        wg.Done()

        for {
            conn, err := server.Accept()
            if err != nil {
                log.Printf("cannot accept connection: %v", err)
                continue
            }
            svcConn := connPool.Get()
            fmt.Fprintln(conn, "")
            connPool.Put(svcConn)
            conn.Close()
        }
    }()
    return &wg
}
```

Y si evaluamos esto con un benchmark, así:

```bash
go test -bench=. src/gos-concurrency-building-blocks/sync/pool/fig-pool-network-daemon-cached_test.go
```

Obtenemos:

| | | | |
|---|---|---|---|
| BenchmarkNetworkRequest-8 | 5000 | 2904307 | ns/op |
| PASS | | | |
| ok | command-line-arguments | 32.647s | |

2.9E6 ns/op: ¡tres órdenes de magnitud más rápido! Puedes ver cómo utilizar este patrón al trabajar con cosas que son costosas de crear puede mejorar drásticamente el tiempo de respuesta.

Como hemos visto, el patrón de diseño de pool de objetos se usa mejor cuando tienes procesos concurrentes que requieren objetos, pero se deshacen de ellos muy rápidamente después de la creación, o cuando la construcción de estos objetos podría afectar negativamente a la memoria.

Sin embargo, hay una cosa de la que debes cuidarte al determinar si debes o no utilizar un `Pool`: si el código que utiliza el `Pool` requiere cosas que no son más o menos homogéneas, puedes pasar más tiempo convirtiendo lo que has recuperado del `Pool` de lo que te habría llevado instanciarlo en primer lugar. Por ejemplo, si tu programa requiere slices de longitud variable y aleatoria, un `Pool` no te ayudará mucho. La probabilidad de que recibas un slice con la longitud que necesitas es baja.

Así que al trabajar con un `Pool`, solo recuerda los siguientes puntos:

- Al instanciar un `sync.Pool`, asígnale una variable miembro `New` que sea thread-safe (segura en entornos de hilos) al llamarse.
- Cuando recibes una instancia de `Get`, no hagas suposiciones con respecto al estado del objeto que recibes de vuelta.
- Asegúrate de llamar a `Put` cuando hayas terminado con el objeto que sacaste del pool. De lo contrario, el `Pool` es inútil. Por lo general, esto se hace con `defer`.
- Los objetos en el pool deben ser de constitución más o menos uniforme.

## Canales (Channels)

Los canales son una de las primitivas de sincronización en Go derivadas de CSP de Hoare. Aunque pueden usarse para sincronizar el acceso a la memoria, se usan mejor para comunicar información entre goroutines. Como discutimos en "La Filosofía de Go sobre la Concurrencia", los canales son extremadamente útiles en programas de cualquier tamaño debido a su capacidad de ser compuestos en conjunto. Después de presentar el canal en esta sección, exploraremos esa composición en la siguiente sección, "La declaración select".

Como un río, un canal sirve como conducto para un flujo de información; los valores pueden pasar a lo largo del canal y luego leerse más adelante en el flujo (downstream). Por esta razón, usualmente termino mis nombres de variables `chan` con la palabra "Stream". Cuando uses canales, pasarás un valor a una variable `chan` y, luego, en otra parte de tu programa, lo leerás del canal. Las partes dispares de tu programa no requieren conocimiento la una de la otra, solo una referencia al mismo lugar en la memoria donde reside el canal. Esto se puede hacer pasando referencias de canales por tu programa.

Crear un canal es muy simple. Aquí hay un ejemplo que expande la creación de un canal en su declaración y posterior creación para que puedas ver cómo se ven ambos. Al igual que con otros valores en Go, puedes crear canales en un solo paso con el operador `:=`, pero necesitarás declarar canales a menudo, por lo que es útil ver los dos divididos en pasos individuales:

```go
var dataStream chan interface{} // 1
dataStream = make(chan interface{}) // 2
```

1. Aquí declaramos un canal. Decimos que es "de tipo" `interface{}` ya que el tipo que hemos declarado es la interfaz vacía.
2. Aquí creamos la instancia del canal utilizando la función integrada `make`.

Este ejemplo define un canal, `dataStream`, en el que se puede escribir o leer cualquier valor (porque usamos la interfaz vacía). Los canales también se pueden declarar para admitir solo un flujo unidireccional de datos; es decir, puedes definir un canal que solo admita enviar o recibir información. Explicaré por qué esto es importante más adelante en esta sección.

Para declarar un canal unidireccional, simplemente incluirás el operador `<-`. Para declarar e instanciar un canal que solo se puede leer, coloca el operador `<-` en el lado izquierdo, de esta manera:

```go
var dataStream <-chan interface{}
dataStream = make(<-chan interface{})
```

Y para declarar y crear un canal que solo puede enviar, colocas el operador `<-` en el lado derecho, así:

```go
var dataStream chan<- interface{}
dataStream = make(chan<- interface{})
```

No ves canales unidireccionales instanciados muy a menudo, pero a menudo los verás usados como parámetros de función y tipos de retorno, lo cual es muy útil, como veremos. Esto es posible porque Go convertirá implícitamente canales bidireccionales en canales unidireccionales cuando sea necesario. Aquí hay un ejemplo:

```go
var receiveChan <-chan interface{}
var sendChan chan<- interface{}
dataStream := make(chan interface{})

// Valid statements:
receiveChan = dataStream
sendChan = dataStream
```

Ten en cuenta que los canales están tipados (son strictly typed). En este ejemplo, creamos una variable `chan interface{}`, lo que significa que podemos colocar cualquier tipo de dato en ella, pero también podemos darle un tipo más estricto para limitar el tipo de dato que podría transmitirse a lo largo de ella. Aquí hay un ejemplo de un canal para enteros; también voy a cambiar a la forma más canónica de instanciar canales por brevedad ahora que hemos pasado la introducción:

```go
intStream := make(chan int)
```

Para usar canales, una vez más haremos uso del operador `<-`. El envío se realiza colocando el operador `<-` a la derecha de un canal, y la recepción se realiza colocando el operador `<-` a la izquierda del canal. Otra forma de pensar en esto es que los datos fluyen hacia la variable en la dirección en la que apunta la flecha. Echemos un vistazo a un ejemplo simple:

```go
stringStream := make(chan string)
go func() {
    stringStream <- "Hello channels!" // 1
}()
fmt.Println(<-stringStream) // 2
```

1. Aquí pasamos un literal de cadena (string) al canal `stringStream`.
2. Aquí leemos el literal de cadena del canal y lo imprimimos en `stdout`.

Esto produce:

```
Hello channels!
```

Bastante simple, ¿verdad? Todo lo que necesitas es una variable de canal y puedes pasarle datos y leer datos de ella; sin embargo, es un error intentar escribir un valor en un canal de solo lectura, y un error leer un valor de un canal de solo escritura. Si intentamos compilar el siguiente ejemplo, el compilador de Go nos hará saber que estamos haciendo algo ilegal:

```go
writeStream := make(chan<- interface{})
readStream := make(<-chan interface{})

<-writeStream
readStream <- struct{}{}
```

Esto arrojará el error:

```
invalid operation: <-writeStream (receive from send-only type chan<- interface {})
invalid operation: readStream <- struct {} literal (send to receive-only type <-chan interface {})
```

Esto es parte del sistema de tipos de Go que nos permite tener seguridad de tipos incluso cuando tratamos con primitivas de concurrencia. Como veremos más adelante en esta sección, esta es una forma poderosa de hacer declaraciones sobre nuestra API y crear programas lógicos y componibles que son fáciles de razonar.

Recuerda que al principio del capítulo destacamos el hecho de que solo porque una goroutine estuviera programada, no había garantía de que se ejecutaría antes de que terminara el proceso; sin embargo, el ejemplo anterior está completo y es correcto sin código omitido. Te estarás preguntando por qué la goroutine anónima termina antes que la goroutine principal; ¿acabo de tener suerte cuando ejecuté esto? Tomemos una breve digresión para explorar esto.

Este ejemplo funciona porque se dice que los canales en Go son *bloqueantes* (blocking). Esto significa que cualquier goroutine que intente escribir en un canal que esté lleno esperará hasta que el canal se haya vaciado, y cualquier goroutine que intente leer de un canal que esté vacío esperará hasta que se coloque al menos un elemento en él. En este ejemplo, nuestro `fmt.Println` contiene una extracción del canal `stringStream` y se quedará allí hasta que se coloque un valor en el canal. Del mismo modo, la goroutine anónima intenta colocar un literal de cadena en el `stringStream`, por lo que la goroutine no saldrá hasta que la escritura sea exitosa. Por lo tanto, la goroutine principal y la goroutine anónima se bloquean de manera determinista.

Esto puede causar interbloqueos (deadlocks) si no estructuras tu programa correctamente. Echa un vistazo al siguiente ejemplo, que introduce un condicional sin sentido para evitar que la goroutine anónima coloque un valor en el canal:

```go
stringStream := make(chan string)
go func() {
    if 0 != 1 { // 1
        return
    }
    stringStream <- "Hello channels!"
}()
fmt.Println(<-stringStream)
```

1. Aquí nos aseguramos de que el canal `stringStream` nunca obtenga un valor puesto en él.

Esto hará que entre en pánico con:

```
fatal error: all goroutines are asleep - deadlock!

goroutine 1 [chan receive]:
main.main()
    /tmp/babel-23079IVB/go-src-230795Jc.go:15 +0x97
exit status 2
```

La goroutine principal está esperando a que se coloque un valor en el canal `stringStream`, y debido a nuestro condicional, esto nunca sucederá. Cuando la goroutine anónima sale, Go detecta correctamente que todas las goroutines están dormidas e informa de un interbloqueo. Más adelante en esta sección, explicaré cómo estructurar nuestros programas como un primer paso para evitar interbloqueos como este, y en el próximo capítulo cómo prevenirlos por completo. Mientras tanto, volvamos a hablar sobre la lectura de los canales.

La forma receptora del operador `<-` también puede devolver opcionalmente dos valores, como este:

```go
stringStream := make(chan string)
go func() {
    stringStream <- "Hello channels!"
}()
salutation, ok := <-stringStream // 1
fmt.Printf("(%v): %v", ok, salutation)
```

1. Aquí recibimos tanto una cadena, `salutation`, como un valor booleano, `ok`.

Esto producirá:

```
(true): Hello channels!
```

¡Muy curioso! ¿Qué significa el booleano? El segundo valor de retorno es una forma en que una operación de lectura indica si la lectura fuera del canal fue un valor generado por una escritura en otra parte del proceso, o un valor por defecto generado a partir de un canal cerrado. Espera un segundo; un canal cerrado, ¿qué es eso?

En los programas, es muy útil poder indicar que no se enviarán más valores por un canal. Esto ayuda a los procesos "downstream" a saber cuándo continuar, salir, reabrir las comunicaciones en un canal nuevo o diferente, etc. Podríamos lograr esto con un valor centinela especial para cada tipo, pero esto duplicaría el esfuerzo de todos los desarrolladores y realmente es una función del canal y no del tipo de datos, por lo que cerrar un canal es como un centinela universal que dice: "Oye, upstream no va a escribir más valores, haz lo que quieras". Para cerrar un canal, usamos la palabra clave `close`, de esta manera:

```go
valueStream := make(chan interface{})
close(valueStream)
```

Curiosamente, también podemos leer desde un canal cerrado. Toma este ejemplo:

```go
intStream := make(chan int)
close(intStream)
integer, ok := <- intStream // 1
fmt.Printf("(%v): %v", ok, integer)
```

1. Aquí leemos de un flujo (stream) cerrado.

Esto producirá:

```
(false): 0
```

Ten en cuenta que nunca colocamos nada en este canal; lo cerramos de inmediato. Aún así pudimos realizar una operación de lectura y, de hecho, podríamos seguir realizando lecturas en este canal indefinidamente a pesar de que el canal permanezca cerrado. Esto es para permitir el soporte de múltiples lecturas aguas abajo (downstream) desde un único escritor aguas arriba (upstream) en el canal (en el Capítulo 4 veremos que este es un escenario común). El segundo valor devuelto —aquí almacenado en la variable `ok`— es `false`, indicando que el valor que recibimos es el valor por defecto para `int`, es decir, `0`, y no un valor colocado en el flujo.

Esto abre algunos patrones nuevos para nosotros. El primero es *recorrer* (ranging) sobre un canal. La palabra clave `range` —usada en conjunción con la declaración `for`— soporta canales como argumentos, y automáticamente interrumpirá (break) el bucle cuando se cierre un canal. Esto permite una iteración concisa sobre los valores en un canal. Echemos un vistazo a un ejemplo:

```go
intStream := make(chan int)
go func() {
    defer close(intStream) // 1
    for i := 1; i <= 5; i++ {
        intStream <- i
    }
}()

for integer := range intStream { // 2
    fmt.Printf("%v ", integer)
}
```

1. Aquí nos aseguramos de que el canal esté cerrado antes de que salgamos de la goroutine. Este es un patrón muy común.
2. Aquí iteramos sobre `intStream`.

Como puedes ver, se imprimen todos los valores y luego el programa se cierra:

```
1 2 3 4 5
```

Observa cómo el bucle no necesita un criterio de salida, y el `range` no devuelve el segundo valor booleano. Los detalles de cómo manejar un canal cerrado se administran por ti para mantener el bucle conciso.

Cerrar un canal también es una de las formas en que puedes enviar señales a varias goroutines simultáneamente. Si tienes `n` goroutines esperando en un solo canal, en lugar de escribir `n` veces en el canal para desbloquear cada goroutine, simplemente puedes cerrar el canal. Dado que un canal cerrado se puede leer un número infinito de veces, no importa cuántas goroutines lo estén esperando, y cerrar el canal es más barato y más rápido que realizar `n` escrituras. Aquí hay un ejemplo de desbloqueo de múltiples goroutines a la vez:

```go
begin := make(chan interface{})
var wg sync.WaitGroup
for i := 0; i < 5; i++ {
    wg.Add(1)
    go func(i int) {
        defer wg.Done()
        <-begin // 1
        fmt.Printf("%v has begun\n", i)
    }(i)
}

fmt.Println("Unblocking goroutines...")
close(begin) // 2
wg.Wait()
```

1. Aquí la goroutine espera hasta que se le dice que puede continuar.
2. Aquí cerramos el canal, desbloqueando así a todas las goroutines simultáneamente.

Puedes ver que ninguna de las goroutines comienza a ejecutarse hasta que cerramos el canal `begin`:

```
Unblocking goroutines...
4 has begun
2 has begun
3 has begun
0 has begun
1 has begun
```

Recuerda que en "El Paquete sync" discutimos el uso del tipo `sync.Cond` para realizar el mismo comportamiento. Ciertamente puedes usar eso, pero como hemos discutido, los canales son componibles, por lo que esta es mi forma favorita de desbloquear varias goroutines al mismo tiempo.

También podemos crear *canales con buffer* (buffered channels), que son canales a los que se les da una *capacidad* cuando se instancian. Esto significa que incluso si no se realizan lecturas en el canal, una goroutine aún puede realizar `n` escrituras, donde `n` es la capacidad del canal con buffer. A continuación te indicamos cómo declarar e instanciar uno:

```go
var dataStream chan interface{}
dataStream = make(chan interface{}, 4) // 1
```

1. Aquí creamos un canal en buffer con una capacidad de cuatro. Esto significa que podemos colocar cuatro cosas en el canal, independientemente de si se están leyendo.

Una vez más, he desglosado la creación de instancias en dos líneas para que puedas ver que la declaración de un canal con búfer no es diferente a la de uno sin búfer (unbuffered). Esto es algo interesante porque significa que la goroutine que crea una instancia de un canal controla si tiene o no almacenamiento en buffer. Esto sugiere que la creación de un canal probablemente debería estar estrechamente ligada a las goroutines que realizarán escrituras en él para que podamos razonar sobre su comportamiento y rendimiento con mayor facilidad. Volveremos a esto más adelante en esta sección.

Los canales sin búfer (unbuffered) también se definen en términos de canales en búfer: un canal sin búfer es simplemente un canal en búfer creado con una capacidad de 0. Aquí hay un ejemplo de dos canales que tienen una funcionalidad equivalente:

```go
a := make(chan int)
b := make(chan int, 0)
```

Ambos canales son canales de `int` con una capacidad de cero. ¿Recuerdas que cuando hablamos del bloqueo, dijimos que las escrituras en un canal se bloquean si el canal está lleno y las lecturas de un canal se bloquean si el canal está vacío? "Lleno" y "vacío" son funciones de la capacidad, o el tamaño del búfer. Un canal sin búfer tiene una capacidad de cero y, por lo tanto, ya está lleno antes de cualquier escritura. Un canal en búfer sin receptores y una capacidad de cuatro estaría lleno después de cuatro escrituras y se bloquearía en la quinta escritura ya que no tiene ningún otro lugar donde colocar el quinto elemento. Al igual que los canales sin búfer, los canales en búfer siguen siendo bloqueantes; las condiciones previas para que el canal esté vacío o lleno son simplemente diferentes. De esta manera, los canales en búfer son una cola FIFO en memoria sobre la cual se comunican los procesos concurrentes.

Para ayudar a entender esto, ilustremos lo que está sucediendo en nuestro ejemplo de un canal con un búfer de capacidad de cuatro. Primero, vamos a inicializarlo:

```go
c := make(chan rune, 4)
```

Lógicamente, esto crea un canal con un búfer que tiene cuatro espacios, así:
![[../../../assets/Pasted image 20260518090819.png]]

Ahora, vamos a escribir en el canal:

```go
c <- 'A'
```

Cuando este canal no tiene lectores, la runa `A` se colocará en la primera ranura del búfer del canal, así:

![[../../../assets/Pasted image 20260518090829.png]]

Cada escritura posterior en el canal en búfer (nuevamente, asumiendo que no hay lectores) llenaría los espacios restantes en el canal en búfer, así:

```go
c <- 'B'
c <- 'C'
c <- 'D'
```
![[../../../assets/Pasted image 20260518090948.png]]

Después de cuatro escrituras, nuestro canal en búfer con capacidad de cuatro está lleno. ¿Qué pasa si intentamos escribir en el canal nuevamente?

```go
c <- 'E'
```
![[../../../assets/Pasted image 20260518091000.png]]

¡La goroutine que realiza esta escritura está bloqueada! La goroutine permanecerá bloqueada hasta que alguna goroutine que realice una lectura haga espacio en el búfer. Veamos cómo se ve eso:

```go
<-c
```
![[../../../assets/Pasted image 20260518091013.png]]

Como puedes ver, la lectura recibe la primera runa que se colocó en el canal, `A`, la escritura que estaba bloqueada se desbloquea y la `E` se coloca al final del búfer.

También cabe mencionar que si un canal en búfer está vacío y tiene un receptor, se omitirá el búfer y el valor se pasará directamente del remitente al receptor. En la práctica, esto sucede de forma transparente, pero vale la pena saberlo para comprender el perfil de rendimiento de los canales en búfer.

Los canales en búfer pueden ser útiles en ciertas situaciones, pero debes crearlos con cuidado. Como veremos en el próximo capítulo, los canales en búfer pueden convertirse fácilmente en una optimización prematura y también ocultar interbloqueos al hacer que sea menos probable que sucedan. Esto suena como algo bueno, pero supongo que preferirías encontrar un punto muerto (deadlock) mientras escribes el código por primera vez, y no en medio de la noche cuando tu sistema de producción se cae.

Examinemos otro ejemplo de código más completo que usa canales con búfer solo para que puedas tener una mejor idea de cómo es trabajar con ellos:

```go
var stdoutBuff bytes.Buffer // 1
defer stdoutBuff.WriteTo(os.Stdout) // 2

intStream := make(chan int, 4) // 3
go func() {
    defer close(intStream)
    defer fmt.Fprintln(&stdoutBuff, "Producer Done.")
    for i := 0; i < 5; i++ {
        fmt.Fprintf(&stdoutBuff, "Sending: %d\n", i)
        intStream <- i
    }
}()

for integer := range intStream {
    fmt.Fprintf(&stdoutBuff, "Received %v.\n", integer)
}
```

1. Aquí creamos un búfer en memoria para ayudar a mitigar la naturaleza no determinista de la salida. No nos da ninguna garantía, pero es un poco más rápido que escribir en `stdout` directamente.
2. Aquí nos aseguramos de que el búfer se escriba en `stdout` antes de que se cierre el proceso.
3. Aquí creamos un canal con buffer con una capacidad de cuatro (nota: en el original dice "one", pero el código `make(chan int, 4)` muestra 4).

En este ejemplo, el orden en el que la salida se escribe a `stdout` no es determinista, pero aun así puedes tener una idea aproximada de cómo está funcionando la goroutine anónima. Si observas la salida, puedes ver cómo nuestra goroutine anónima es capaz de colocar todos sus cinco resultados en el `intStream` y salir antes de que la goroutine principal saque siquiera un resultado:

```
Sending: 0
Sending: 1
Sending: 2
Sending: 3
Sending: 4
Producer Done.
Received 0.
Received 1.
Received 2.
Received 3.
Received 4.
```

Este es un ejemplo de una optimización que puede ser útil en las condiciones adecuadas: si una goroutine que realiza escrituras en un canal tiene conocimiento de cuántas escrituras realizará, puede ser útil crear un canal en búfer cuya capacidad sea el número de escrituras que se realizarán, y luego hacer esas escrituras tan rápido como sea posible. Hay, por supuesto, advertencias, y las cubriremos en el próximo capítulo.

Hemos discutido canales sin buffer, canales con buffer, canales bidireccionales y canales unidireccionales. El único aspecto de los canales que no hemos cubierto es el valor predeterminado para los canales: `nil`. ¿Cómo interactúan los programas con un canal `nil`? Primero, intentemos leer desde un canal `nil`:

```go
var dataStream chan interface{}
<-dataStream
```

Esto entra en pánico con:

```
  fatal error: all goroutines are asleep - deadlock!

  goroutine 1 [chan receive (nil chan)]:
  main.main()
      /tmp/babel-23079IVB/go-src-23079O4q.go:9 +0x3f
  exit status 2
```

¡Un punto muerto (deadlock)! Esto indica que leer de un canal `nil` bloqueará (aunque no necesariamente creará un interbloqueo fatal si hay otras corriendo) un programa. ¿Qué hay de las escrituras?

```go
var dataStream chan interface{}
dataStream <- struct{}{}
```

Esto produce:

```
  fatal error: all goroutines are asleep - deadlock!

  goroutine 1 [chan send (nil chan)]:
  main.main()
      /tmp/babel-23079IVB/go-src-23079dnD.go:9 +0x77
  exit status 2
```

Parece que las escrituras a un canal `nil` también se bloquearán. Eso solo deja una operación, `close`. ¿Qué pasa si intentamos cerrar un canal `nil`?

```go
var dataStream chan interface{}
close(dataStream)
```

Esto produce:

```
  panic: close of nil channel

  goroutine 1 [running]:
  panic(0x45b0c0, 0xc42000a160)
      /usr/local/lib/go/src/runtime/panic.go:500 +0x1a1
  main.main()
      /tmp/babel-23079IVB/go-src-230794uu.go:9 +0x2a
  exit status 2
```

¡Huy! Este es probablemente el peor resultado de todas las operaciones realizadas en un canal `nil`: un panic (pánico). Asegúrate de que los canales con los que estás trabajando siempre se inicialicen primero.

Hemos repasado muchas reglas sobre cómo interactuar con los canales. Ahora que comprendes el cómo y el por qué de realizar operaciones en canales, vamos a crear una referencia útil sobre cuál es el comportamiento definido para trabajar con canales. La Tabla 3-2 enumera las operaciones en los canales y qué sucederá dados los posibles estados del canal.

Tabla 3-2. Resultado de las operaciones del canal dado el estado de un canal

| Operación | Estado del canal | Resultado |
|---|---|---|
| Lectura (Read) | `nil` | Bloquea (Block) |
| | Abierto y no vacío | Valor |
| | Abierto y vacío | Bloquea (Block) |
| | Cerrado | `<valor por defecto>`, false |
| | Solo Escritura | Error de compilación |
| Escritura (Write) | `nil` | Bloquea (Block) |
| | Abierto y lleno | Bloquea (Block) |
| | Abierto y no lleno | Escribe el Valor |
| | Cerrado | **panic** |
| | Solo Recepción | Error de compilación |
| `close` | `nil` | **panic** |
| | Abierto y no vacío | Cierra el Canal; las lecturas tienen éxito hasta que se drena el canal, luego las lecturas producen el valor por defecto |
| | Abierto y vacío | Cierra el Canal; las lecturas producen el valor por defecto |
| | Cerrado | **panic** |
| | Solo Recepción | Error de compilación |

Si examinamos esta tabla, vemos algunas áreas que podrían generar problemas. ¡Tenemos tres operaciones que pueden hacer que una goroutine se bloquee, y tres operaciones que pueden hacer que tu programa entre en `panic`! A primera vista, parece que los canales pueden ser peligrosos de utilizar, pero después de examinar la motivación de estos resultados y enmarcar el uso de los canales, se vuelve menos aterrador y comienza a tener mucho sentido. Echemos un vistazo a cómo podemos organizar los diferentes tipos de canales para comenzar a construir algo sólido y estable.

Lo primero que debemos hacer para ubicar a los canales en el contexto correcto es asignar la *propiedad* (ownership) del canal. Definiré la propiedad como la goroutine que instancia, escribe y cierra un canal. Al igual que la memoria en lenguajes sin recolección de basura, es importante aclarar qué goroutine posee un canal para poder razonar de manera lógica sobre nuestros programas. Las declaraciones de canales unidireccionales son la herramienta que nos permitirá distinguir entre las goroutines que poseen canales y las que solo los utilizan: los propietarios del canal tienen una vista de acceso de escritura hacia el canal (`chan` o `chan<-`), y los utilizadores del canal solo tienen una vista de solo lectura en el canal (`<-chan`). Una vez que hacemos esta distinción entre propietarios de canales y no propietarios, los resultados de la tabla anterior se deducen de forma natural, y podemos comenzar a asignar responsabilidades a las goroutines que poseen canales y a las que no.

Comencemos con los propietarios de canales (channel owners). La goroutine que posee un canal debe:

1. Instanciar el canal.
2. Realizar escrituras o pasar la propiedad a otra goroutine.
3. Cerrar el canal.
4. Encapsular las tres cosas anteriores de esta lista y exponerlas a través de un canal lector (reader channel).

Al asignar estas responsabilidades a los dueños del canal, suceden varias cosas:

- Debido a que somos nosotros quienes inicializamos el canal, eliminamos el riesgo de interbloqueo al escribir en un canal `nil`.
- Debido a que somos nosotros los que inicializamos el canal, eliminamos el riesgo de que haya `panic` al cerrar un canal `nil`.
- Debido a que somos nosotros quienes decidimos cuándo se cierra el canal, eliminamos el riesgo de tener un `panic` al escribir en un canal cerrado.
- Debido a que somos nosotros quienes decidimos cuándo se cierra el canal, eliminamos el riesgo de caer en `panic` cerrando un canal más de una vez.
- Utilizamos el verificador de tipos (type checker) en tiempo de compilación para prevenir escrituras inadecuadas en nuestro canal.

Ahora veamos aquellas operaciones bloqueantes que pueden ocurrir durante la lectura. Como consumidor de un canal, solo tengo que preocuparme de dos cosas:

- Saber cuando se cierra un canal.
- Manejar responsablemente los bloqueos por cualquier motivo.

Para abordar el primer punto, simplemente examinamos el segundo valor de retorno de la operación de lectura, como se discutió anteriormente. El segundo punto es mucho más difícil de definir porque depende de tu algoritmo: es posible que desees agotar el tiempo de espera (timeout), es posible que desees dejar de leer cuando alguien te lo indique, o simplemente te contentes con bloquearte durante la vida útil del proceso. Lo importante es que, como consumidor, debes manejar el hecho de que las lecturas pueden y serán bloqueantes. Examinaremos las formas de lograr cualquier objetivo de un lector de canales en el próximo capítulo.

Por ahora, veamos un ejemplo para ayudar a aclarar estos conceptos. Creemos una goroutine que claramente posea un canal, y un consumidor que maneje claramente el bloqueo y el cierre de un canal:

```go
chanOwner := func() <-chan int {
    resultStream := make(chan int, 5) // 1
    go func() { // 2
        defer close(resultStream) // 3
        for i := 0; i <= 5; i++ {
            resultStream <- i
        }
    }()
    return resultStream // 4
}

resultStream := chanOwner()
for result := range resultStream { // 5
    fmt.Printf("Received: %d\n", result)
}
fmt.Println("Done receiving!")
```

1. Aquí instanciamos un canal con búfer. Como sabemos que produciremos seis resultados, creamos un canal con búfer de cinco para que la goroutine pueda completarse lo más rápido posible.
2. Aquí iniciamos una goroutine anónima que realiza escrituras en `resultStream`. Ten en cuenta que hemos invertido la forma en que creamos goroutines. Ahora está encapsulada dentro de la función circundante.
3. Aquí nos aseguramos de que `resultStream` se cierre una vez que hayamos terminado con él. Como dueños del canal, esta es nuestra responsabilidad.
4. Aquí devolvemos el canal. Dado que el valor de retorno se declara como un canal de solo lectura, `resultStream` se convertirá implícitamente en de solo lectura para los consumidores.
5. Aquí recorremos (range) a través del `resultStream`. Como consumidores, solo nos preocupan los canales cerrados y los bloqueos.

Esto produce:

```
Received: 0
Received: 1
Received: 2
Received: 3
Received: 4
Received: 5
Done receiving!
```

Observa cómo el ciclo de vida del canal `resultStream` está encapsulado dentro de la función `chanOwner`. Queda muy claro que las escrituras no se producirán en un canal nil o cerrado, y que el cierre siempre se realizará una vez. Esto elimina una gran franja de riesgo de nuestro programa. Te animo encarecidamente a que hagas lo posible en tus programas para mantener el alcance de la propiedad de tus canales reducido, para que estas cosas sigan siendo obvias. Si tienes un canal como variable miembro de una estructura con numerosos métodos en ella, pronto dejará de estar claro cómo se comportará el canal.

La función del consumidor solo tiene acceso a un canal de lectura y, por lo tanto, solo necesita saber cómo debe manejar las lecturas bloqueantes y los cierres de canales. En este pequeño ejemplo, hemos adoptado la postura de que está perfectamente bien bloquear la vida del programa hasta que se cierre el canal.

Si diseñas tu código siguiendo este principio, será mucho más fácil razonar sobre tu sistema y es mucho más probable que funcione como esperas. No puedo prometer que nunca introducirás interbloqueos o pánicos (panics), pero cuando lo hagas, creo que encontrarás que el alcance de la propiedad de tu canal se ha vuelto demasiado grande, o que la propiedad no está clara.

Los canales fueron una de las cosas que me atrajeron de Go en primer lugar. Combinado con la simplicidad de las goroutines y los cierres, era obvio para mí lo fácil que sería escribir un código limpio, correcto y concurrente. En muchos sentidos, los canales son el pegamento que une las goroutines. Este capítulo debería haberte dado una buena descripción general de qué son los canales y cómo usarlos. La verdadera diversión comienza cuando comenzamos a componer canales para formar patrones de diseño de concurrencia de orden superior. Llegaremos a eso en el próximo capítulo.

## La Declaración select

La declaración `select` es el pegamento que une los canales; es cómo somos capaces de componer canales juntos en un programa para formar abstracciones más grandes. Si los canales son el pegamento que une a las goroutines, ¿qué dice eso sobre la declaración `select`? No es una exageración decir que las declaraciones `select` son una de las cosas más cruciales en un programa de Go con concurrencia. Puedes encontrar declaraciones `select` que unen canales a nivel local, dentro de una sola función o tipo, y también a nivel global, en la intersección de dos o más componentes de un sistema. Además de unir componentes, en estas uniones críticas de tu programa, las declaraciones `select` pueden ayudar a unir los canales de manera segura con conceptos como cancelaciones, tiempos de espera (timeouts), esperas y valores por defecto.

Por el contrario, si las declaraciones `select` son la *lingua franca* de tu programa y tratan exclusivamente con canales, ¿cómo crees que deberían coordinarse los componentes de tu programa entre sí? Examinaremos esta pregunta específicamente en el Capítulo 5 (pista: prefiere usar canales).

Entonces, ¿qué son estas poderosas sentencias `select`? ¿Cómo las usamos y cómo funcionan? Comencemos por simplemente plantear una. Aquí hay un ejemplo muy simple:

```go
var c1, c2 <-chan interface{}
var c3 chan<- interface{}
select {
case <- c1:
    // Hacer algo
case <- c2:
    // Hacer otra cosa
case c3<- struct{}{}:
    // Hacer aún otra cosa más
}
```

Se parece un poco a un bloque `switch`, ¿no es así? Al igual que un bloque `switch`, un bloque `select` abarca una serie de sentencias `case` que protegen una serie de sentencias; sin embargo, ahí es donde terminan las similitudes. A diferencia de los bloques `switch`, las declaraciones `case` en un bloque `select` no se prueban secuencialmente, y la ejecución no "caerá" (fall through) automáticamente si no se cumple ninguno de los criterios.

En cambio, todas las lecturas y escrituras del canal se consideran simultáneamente para ver si alguna de ellas está lista: canales poblados o cerrados en el caso de las lecturas, y canales que no están al límite de su capacidad en el caso de las escrituras. Si ninguno de los canales está listo, la instrucción `select` completa se bloquea. Luego, cuando uno de los canales está listo, esa operación continuará y se ejecutarán sus sentencias correspondientes. Veamos un ejemplo rápido:

```go
start := time.Now()
c := make(chan interface{})
go func() {
    time.Sleep(5 * time.Second)
    close(c) // 1
}()

fmt.Println("Blocking on read...")
select {
case <-c: // 2
    fmt.Printf("Unblocked %v later.\n", time.Since(start))
}
```

1. Aquí cerramos el canal después de esperar cinco segundos.
2. Aquí intentamos leer en el canal. Ten en cuenta que tal como está escrito este código, no requerimos una declaración `select` —simplemente podríamos escribir `<-c`— pero expandiremos este ejemplo.

Esto produce:

```
Blocking on read...
Unblocked 5.000170047s later.
```

Como puedes ver, solo nos desbloqueamos aproximadamente cinco segundos después de ingresar al bloque `select`. Esta es una forma simple y eficiente de bloquearnos mientras esperamos a que suceda algo, pero si reflexionamos por un momento podemos formularnos algunas preguntas:

- ¿Qué sucede cuando varios canales tienen algo que leer?
- ¿Qué sucede si nunca hay canales que estén listos?
- ¿Qué pasa si queremos hacer algo pero no hay canales listos actualmente?

La primera pregunta de varios canales que están listos simultáneamente parece interesante. ¡Vamos a intentarlo y ver qué pasa!

```go
c1 := make(chan interface{})
close(c1)
c2 := make(chan interface{})
close(c2)

var c1Count, c2Count int
for i := 1; i < 1000; i++ {
    select {
    case <-c1:
        c1Count++
    case <-c2:
        c2Count++
    }
}

fmt.Printf("c1Count: %d\nc2Count: %d\n", c1Count, c2Count)
```

Esto produce:

```
c1Count: 505
c2Count: 496
```

Como puedes ver, en mil iteraciones, aproximadamente la mitad de las veces la instrucción `select` leyó de `c1`, y aproximadamente la mitad de las veces leyó de `c2`. Eso parece interesante, y tal vez un poco demasiada coincidencia. ¡De hecho, lo es! El runtime de Go realizará una selección pseudoaleatoria y uniforme sobre el conjunto de sentencias case. Esto solo significa que de tu conjunto de declaraciones de caso, cada uno tiene las mismas posibilidades de ser seleccionado que todos los demás.

Esto puede parecer poco importante al principio, pero el razonamiento detrás de ello es increíblemente interesante. Primero, hagamos una declaración bastante obvia: el entorno de ejecución de Go no puede saber nada sobre la intención de tu declaración `select`; es decir, no puede inferir tu espacio de problemas ni el motivo por el cual colocaste un grupo de canales juntos en una instrucción `select`. Debido a esto, lo mejor que el runtime de Go puede esperar hacer es funcionar bien en el caso promedio. Una buena forma de hacerlo es introducir una variable aleatoria en la ecuación, en este caso, de qué canal seleccionar. Al sopesar la posibilidad de que cada canal se utilice por igual, todos los programas Go que utilizan la declaración `select` funcionarán bien en el caso promedio.

¿Qué pasa con la segunda pregunta: qué sucede si nunca hay canales listos? Si no hay nada útil que puedas hacer cuando todos los canales están bloqueados, pero tampoco puedes bloquear para siempre, es posible que desees agotar el tiempo (time out). El paquete `time` de Go proporciona una forma elegante de hacer esto con canales que encajan muy bien dentro del paradigma de las sentencias `select`. Aquí hay un ejemplo usando uno:

```go
var c <-chan int
select {
case <-c: // 1
case <-time.After(1 * time.Second):
    fmt.Println("Timed out.")
}
```

1. Esta declaración case nunca se desbloqueará porque estamos leyendo de un canal `nil`.

Esto produce:

```
Timed out.
```

La función `time.After` recibe un argumento de tipo `time.Duration` y devuelve un canal que enviará la hora actual después de la duración que le proporciones. Esto ofrece una forma concisa de agotar el tiempo de espera en declaraciones `select`. Revisaremos este patrón en el Capítulo 4, donde analizaremos una solución más sólida a este problema.

Esto nos deja la pregunta restante: ¿qué sucede cuando ningún canal está listo y necesitamos hacer algo mientras tanto? Al igual que las sentencias `case`, la sentencia `select` también permite una cláusula `default` en caso de que desees hacer algo si todos los canales frente a los que estás realizando el `select` se están bloqueando. Aquí hay un ejemplo:

```go
start := time.Now()
var c1, c2 <-chan int
select {
case <-c1:
case <-c2:
default:
    fmt.Printf("In default after %v\n", time.Since(start))
}
```

Esto produce:

```
In default after 1.421µs
```

Puedes ver que ejecutó la declaración `default` casi instantáneamente. Esto te permite salir de un bloque `select` sin bloquearte. Usualmente, verás una cláusula `default` usada junto con un bucle `for-select`. Esto le permite a una goroutine progresar en el trabajo mientras espera que otra goroutine informe un resultado. Aquí hay un ejemplo de eso:

```go
done := make(chan interface{})
go func() {
    time.Sleep(5 * time.Second)
    close(done)
}()

workCounter := 0
loop:
for {
    select {
    case <-done:
        break loop
    default:
    }

    // Simula trabajo
    workCounter++
    time.Sleep(1 * time.Second)
}

fmt.Printf("Achieved %v cycles of work before signalled to stop.\n", workCounter)
```

Esto produce:

```
Achieved 5 cycles of work before signalled to stop.
```

En este caso, tenemos un bucle que está haciendo algún tipo de trabajo y de vez en cuando verifica si debería detenerse.

Por último, hay un caso especial para sentencias `select` vacías: sentencias `select` sin cláusulas `case`. Se ven así:

```go
select {}
```

Esta instrucción simplemente se bloqueará para siempre.

En el Capítulo 6, analizaremos más a fondo cómo funciona la sentencia `select`. Desde una perspectiva de nivel superior, debería ser evidente cómo puede ayudarte a componer varios conceptos y subsistemas juntos de forma segura y eficiente.

## La Palanca GOMAXPROCS

En el paquete `runtime`, hay una función llamada `GOMAXPROCS`. En mi opinión, el nombre es engañoso: a menudo se piensa que esta función se relaciona con la cantidad de procesadores lógicos en la máquina anfitriona (host) —y, indirectamente, lo hace— pero en realidad esta función controla la cantidad de hilos (threads) del sistema operativo que alojarán a las llamadas "colas de trabajo" (work queues). Para obtener más información sobre qué es esta función y cómo funciona, consulta el Capítulo 6.

Antes de Go 1.5, `GOMAXPROCS` siempre se establecía en uno, y normalmente encontrarías este fragmento en la mayoría de los programas Go:

```go
runtime.GOMAXPROCS(runtime.NumCPU())
```

Casi universalmente, los desarrolladores quieren aprovechar todos los núcleos de la máquina en la que se ejecuta su proceso. Debido a esto, en versiones posteriores de Go, ahora se ajusta automáticamente a la cantidad de CPU lógicas en la máquina host.

Entonces, ¿por qué querrías modificar este valor? La mayoría de las veces no querrás hacerlo. El algoritmo de programación (scheduling) de Go es lo suficientemente bueno en la mayoría de las situaciones que aumentar o disminuir la cantidad de colas y subprocesos de trabajadores probablemente hará más daño que bien, pero todavía hay algunas situaciones en las que cambiar este valor puede ser útil.

Por ejemplo, trabajé en un proyecto que tenía un conjunto de pruebas plagado de condiciones de carrera. Como sea que haya sucedido, el equipo tenía un puñado de paquetes que tenían pruebas que a veces fallaban. La infraestructura en la que ejecutábamos nuestras pruebas solo tenía cuatro CPU lógicas, y por lo tanto, en un momento dado teníamos cuatro goroutines ejecutándose simultáneamente. Al aumentar `GOMAXPROCS` más allá de la cantidad de CPU lógicas que teníamos, pudimos desencadenar las condiciones de carrera con mucha más frecuencia y así hacer que se corrigieran más rápido.

Otros pueden encontrar mediante experimentación que sus programas funcionan mejor con una determinada cantidad de hilos y colas de trabajo, pero pido cautela. Si estás exprimiendo al máximo el rendimiento ajustando esto, asegúrate de hacerlo después de cada commit, cuando utilices hardware diferente y cuando uses versiones diferentes de Go. Modificar este valor acerca tu programa más al "metal" en el que se ejecuta, pero a costa de la abstracción y la estabilidad del rendimiento a largo plazo.

## Conclusión

En este capítulo, hemos cubierto todas las primitivas de concurrencia básicas que Go pone a tu disposición. Si has leído y entendido esto, ¡felicitaciones! Estás en el buen camino para escribir programas con buen rendimiento, legibles y lógicamente correctos. Sabes cuándo es apropiado buscar las primitivas de sincronización de acceso a la memoria en el paquete `sync` y cuándo es más apropiado "compartir memoria mediante la comunicación" mediante el uso de canales y la instrucción `select`.

Todo lo que queda por entender a la hora de escribir código Go concurrente es cómo combinar estas primitivas en formas estructuradas que puedan escalar y sean fáciles de comprender. En la segunda mitad del libro, analizaremos cómo hacer precisamente eso. El próximo capítulo trata sobre cómo combinar estas primitivas utilizando patrones que la comunidad ha descubierto.
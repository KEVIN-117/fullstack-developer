# Capítulo 5: Concurrencia a Escala

Ahora que has aprendido algunos patrones comunes para utilizar la concurrencia dentro de Go, dirijamos nuestra atención a la composición de estos patrones en una serie de prácticas que te permitirán escribir sistemas grandes y componibles que escalen.

En este capítulo, discutiremos formas de escalar las operaciones concurrentes dentro de un solo proceso, y también comenzaremos a ver cómo entra en juego la concurrencia cuando se trata de más de un proceso.

## Propagación de Errores

Con el código concurrente, y especialmente con los sistemas distribuidos, es fácil que algo salga mal en tu sistema y difícil entender por qué sucedió. Puedes ahorrarte a ti mismo, a tu equipo y a tus usuarios mucho dolor considerando cuidadosamente cómo se propagan los problemas a través de tu sistema y cómo terminan representándose ante el usuario. En la sección "Manejo de Errores", discutimos *cómo* propagar errores desde las goroutines, pero no dedicamos tiempo a discutir qué aspecto deberían tener esos errores, o cómo deberían fluir a través de un sistema grande y complejo. Dediquemos un tiempo aquí a discutir una filosofía de propagación de errores. Lo que sigue es un marco de trabajo opinado para el manejo de errores en sistemas concurrentes.

Muchos desarrolladores cometen el error de pensar en la propagación de errores como algo secundario, u "otro", al flujo de su sistema. Se presta una atención cuidadosa a cómo fluyen los datos a través del sistema, pero los errores son algo que se tolera y se transporta por la pila de llamadas sin pensarlo mucho, y finalmente se vuelca frente al usuario. Go intentó corregir esta mala práctica obligando a los usuarios a manejar los errores en cada marco de la pila de llamadas, pero sigue siendo común ver que los errores se tratan como ciudadanos de segunda clase en el flujo de control del sistema. Con solo un poco de previsión y una sobrecarga mínima, puedes hacer que el manejo de errores sea un activo para tu sistema y un deleite para tus usuarios.

Primero examinemos qué son los errores. ¿Cuándo ocurren y qué beneficio proporcionan?

Los errores indican que tu sistema ha entrado en un estado en el que no puede cumplir una operación que un usuario solicitó de forma explícita o implícita. Por eso, necesita transmitir algunas piezas críticas de información:

**Qué sucedió.**
Esta es la parte del error que contiene información sobre lo ocurrido, por ejemplo, "disco lleno", "socket cerrado" o "credenciales expiradas". Es probable que esta información sea generada implícitamente por lo que sea que generó los errores, aunque probablemente puedas decorarla con algún contexto que ayude al usuario.

**Cuándo y dónde ocurrió.**
Los errores siempre deben contener un trazado de la pila (stack trace) completo, comenzando por cómo se inició la llamada y terminando por dónde se instanció el error. El trazado de la pila *no* debe estar contenido en el mensaje de error (más sobre esto en un momento), sino que debe ser fácilmente accesible cuando se maneje el error en la pila superior.
Además, el error debe contener información relativa al contexto en el que se ejecuta. Por ejemplo, en un sistema distribuido, debería tener alguna forma de identificar en qué máquina se produjo el error. Más adelante, cuando intentes comprender qué ha sucedido en tu sistema, esta información será inestimable.
Además, el error debe contener la hora de la máquina en la que se instanció el error, en UTC.

**Un mensaje amigable para el usuario.**
El mensaje que se muestra al usuario debe estar personalizado para adaptarse a tu sistema y a sus usuarios. Solo debe contener información abreviada y relevante de los dos puntos anteriores. Un mensaje amigable está centrado en el ser humano, da alguna indicación de si el problema es transitorio y debería tener aproximadamente una línea de texto.

**Cómo puede obtener el usuario más información.**
En algún momento, es probable que alguien quiera saber, en detalle, qué ocurrió cuando se produjo el error. Los errores que se presentan a los usuarios deben proporcionar un ID que pueda cotejarse con un log (registro) correspondiente que muestre la información completa del error: la hora en que se produjo el error (no la hora en que se registró el error), el trazado de la pila... todo lo que hayas introducido en el error cuando se creó. También puede ser útil incluir un hash del trazado de la pila para ayudar a agregar problemas similares en los rastreadores de bugs.

Por defecto, ningún error contendrá toda esta información sin tu intervención. Por lo tanto, podrías adoptar la postura de que cualquier error que se propague al usuario *sin* esta información es un error y, por tanto, un bug. Esto nos lleva a un marco general que podemos utilizar para pensar en los errores. Es posible situar todos los errores en una de dos categorías:

- Bugs
- Casos de borde conocidos (ej., conexiones de red rotas, fallos en la escritura en disco, etc.)

Los bugs son errores que no has personalizado para tu sistema, o errores "puros" (raw): tus casos de borde conocidos. A veces esto es intencionado; puede que no te importe dejar que los errores de los casos de borde lleguen a tus usuarios mientras sacas adelante las primeras iteraciones de tu sistema. A veces ocurre por accidente. Pero si estás de acuerdo con el enfoque que he planteado, los errores puros son siempre bugs. Esta distinción resultará útil a la hora de determinar cómo propagar los errores, cómo crece tu sistema con el tiempo y qué mostrar finalmente al usuario.

Imagina un sistema grande con múltiples módulos:
![[../../../assets/Pasted image 20260518105521.png]]

*(Imagen: Componente de bajo nivel -> Componente intermediario -> Usuario)*

Supongamos que se produce un error en el "Componente de bajo nivel" y hemos creado allí un error bien formado para pasarlo a la parte superior de la pila. Dentro del contexto del "Componente de bajo nivel", este error podría considerarse bien formado, pero dentro del contexto de nuestro sistema, puede que no lo sea. Adoptemos la postura de que, en los límites de cada componente, todos los errores entrantes deben envolverse en un error bien formado para el componente en el que se encuentra nuestro código. Por ejemplo, si estuviéramos en el "Componente intermediario" y estuviéramos llamando a código del "Componente de bajo nivel", que podría dar error, podríamos tener esto:

```go
func (c IntermediaryComponent) DoWork() error {
    err := c.lowLevelComponent.DoWork()
    if err != nil {
        if _, ok := err.(WellFormedError); ok { // 1
            return err
        }
        return wrapError(err, "intermediary component failed") // 2
    }
    return nil
}
```

1. Aquí comprobamos que recibimos un error bien formado. Si no es así, simplemente transportamos el error mal formado por la pila para indicar un bug.
2. Aquí utilizamos una hipotética llamada a función para envolver el error entrante con información pertinente para nuestro módulo, y para darle un nuevo tipo. Ten en cuenta que envolver el error puede implicar *ocultar* algunos detalles de bajo nivel que pueden no ser importantes para el usuario dentro de este contexto.

Los detalles de bajo nivel de dónde se produjo la raíz del error (ej., qué goroutine, máquina, trazado de la pila, etc.) se siguen rellenando cuando se instancia inicialmente el error, pero nuestra arquitectura dicta que en los límites de los módulos convertimos el error al tipo de error de nuestro módulo, rellenando potencialmente la información pertinente. Ahora, cualquier error que escape de *nuestro* módulo sin el tipo de error de nuestro módulo puede considerarse mal formado, y un bug. Ten en cuenta que solo es necesario envolver los errores de esta manera en tus *propios* límites de módulo (funciones/métodos públicos) o cuando tu código pueda añadir un contexto valioso. Normalmente, esto evita la necesidad de envolver los errores en la mayor parte del código.

Adoptar esta postura permite que nuestro sistema crezca de forma muy orgánica. Podemos estar seguros de que los errores entrantes están bien formados y, a nuestra vez, podemos asegurarnos de que estamos pensando en cómo escapan los errores de nuestro módulo. La corrección de los errores se convierte en una propiedad emergente de nuestro sistema. También concedemos la perfección desde el principio manejando explícitamente los errores mal formados y, al hacerlo, nos hemos dotado de un marco para tomar los errores y corregirlos a lo largo del tiempo. Los errores mal formados se delimitan claramente tanto por el tipo como, como veremos, por lo que se presenta al usuario.

Como establecimos, todos los errores deben registrarse con tanta información como esté disponible. Pero al mostrar los errores a los usuarios, es aquí donde entra en juego la distinción entre bugs y casos de borde conocidos.

Cuando nuestro código de cara al usuario recibe un error bien formado, podemos estar seguros de que en todos los niveles de nuestro código se tuvo cuidado de elaborar el mensaje de error, y simplemente podemos registrarlo e imprimirlo para que el usuario lo vea. La confianza que obtenemos al ver un error con el tipo correcto no se puede subestimar.

Cuando los errores mal formados, o bugs, se propagan hasta el usuario, también debemos registrar el error, pero mostrar un mensaje amigable al usuario indicando que ha ocurrido algo inesperado. Si admitimos el reporte automático de errores en nuestro sistema, el error debería reportarse como un bug. Si no lo hacemos, podríamos sugerir al usuario que presente un informe de bug. Ten en cuenta que el error mal formado puede contener en realidad información útil, pero no podemos garantizarlo y, por tanto —ya que la única garantía que tenemos es que el error no está personalizado— debemos mostrar sin ambages un mensaje centrado en el ser humano sobre lo sucedido.

Recuerda que en cualquiera de los dos casos, con errores bien o mal formados, habremos incluido un ID de registro en el mensaje para dar al usuario algo a lo que remitirse si desea más información. Así, incluso si los bugs contuvieran información útil, el usuario curioso sigue teniendo medios para investigar.

Echemos un vistazo a un ejemplo completo. Este ejemplo no será extremadamente robusto (ej., el tipo de error es quizás simplista) y la pila de llamadas es lineal, lo que ofusca el hecho de que solo es necesario envolver los errores en los límites de los módulos. Además, es difícil representar funciones en diferentes paquetes en un libro, por lo que estaremos fingiendo.

Primero, vamos a crear un tipo de error que pueda contener todos los aspectos de un error bien formado que hemos discutido:

```go
type MyError struct {
    Inner      error // 1
    Message    string
    StackTrace string // 2
    Misc       map[string]interface{} // 3
}

func (m MyError) Error() string {
    return m.Message
}

func wrapError(err error, messagef string, msgArgs ...interface{}) MyError {
    return MyError{
        Inner:      err,
        Message:    fmt.Sprintf(messagef, msgArgs...),
        StackTrace: string(debug.Stack()),
        Misc:       make(map[string]interface{}),
    }
}
```

1. Aquí almacenamos el error que estamos envolviendo. Siempre queremos poder volver al error de nivel más bajo en caso de que necesitemos investigar lo que ocurrió.
2. Esta línea de código toma nota del trazado de la pila cuando se creó el error.
3. Aquí creamos un cajón de sastre para almacenar información diversa. Aquí es donde podríamos almacenar el ID concurrente, un hash del trazado de la pila u otra información contextual que pueda ayudar a diagnosticar el error.

A continuación, vamos a crear un módulo, `lowlevel`:

```go
// Módulo "lowlevel"
type LowLevelErr struct {
    error
}

func isGloballyExec(path string) (bool, error) {
    info, err := os.Stat(path)
    if err != nil {
        return false, LowLevelErr{(wrapError(err, err.Error()))} // 1
    }
    return info.Mode().Perm()&0100 != 0, nil
}
```

1. Aquí envolvemos el error puro de llamar a `os.Stat` con un error personalizado. En este caso estamos conformes con el mensaje que sale de este error, por lo que no lo enmascararemos.

A continuación, vamos a crear otro módulo, `intermediate`, que llama a funciones del paquete `lowlevel`:

```go
// Módulo "intermediate"
type IntermediateErr struct {
    error
}

func runJob(id string) error {
    const jobBinPath = "/bad/job/binary"
    isExecutable, err := isGloballyExec(jobBinPath)
    if err != nil {
        return err // 1
    }
    if isExecutable == false {
        return wrapError(nil, "job binary is not executable")
    }
    return nil
}
```

1. Aquí estamos pasando errores del módulo `lowlevel`. Debido a nuestra decisión arquitectónica de considerar los errores pasados desde otros módulos sin envolverlos en nuestro propio tipo como bugs, esto nos causará problemas más adelante.

Por último, vamos a crear una función `main` de nivel superior que llame a las funciones del paquete `intermediate`. Esta es la parte de nuestro programa que ve el usuario:

```go
func main() {
    log.SetFlags(log.Ltime | log.LUTC)
    err := runJob("1")
    if err != nil {
        msg := "There was an unexpected issue; please report this as a bug."
        if _, ok := err.(IntermediateErr); ok { // 1
            msg = err.Error()
        }
        log.Printf("[logID: 1]: %v", err) // 3
        fmt.Printf("[%v] %v\n", 1, msg) // 2
    }
}
```

1. Aquí comprobamos si el error es del tipo esperado. Si lo es, sabemos que es un error bien elaborado y simplemente podemos pasar su mensaje al usuario.
2. En esta línea vinculamos el registro y el mensaje de error con un ID de `1`. Podríamos hacer fácilmente que este aumentara monótonamente, o utilizar un GUID para asegurar un ID único.
3. Aquí registramos el error completo por si alguien necesita profundizar en lo sucedido.

Cuando ejecutamos esto, obtenemos un mensaje de registro que contiene el stack trace y los detalles internos, pero un mensaje a `stdout` que dice:

```
[1] There was an unexpected issue; please report this as a bug.
```

Podemos ver que en algún punto del camino de este error, no se manejó correctamente, y como no podemos estar seguros de que el mensaje de error sea apto para el consumo humano, imprimimos un error simple indicando que ocurrió algo inesperado. Si miramos hacia atrás a nuestro módulo `intermediate`, recordamos por qué: no envolvimos los errores del módulo `lowlevel`. Corrijamos eso y veamos qué sucede:

```go
// Módulo "intermediate" actualizado
func runJob(id string) error {
    const jobBinPath = "/bad/job/binary"
    isExecutable, err := isGloballyExec(jobBinPath)
    if err != nil {
        return IntermediateErr{wrapError(err, "cannot run job %q: requisite binaries not available", id)} // 1
    }
    // ...
}
```

1. Ahora estamos personalizando el error con un mensaje elaborado. En este caso, queremos ofuscar los detalles de bajo nivel de por qué el trabajo no se está ejecutando porque sentimos que no es información importante para los consumidores de nuestro módulo.

Ahora, cuando ejecutamos el código actualizado, nuestro mensaje de error es exactamente lo que queremos que vean los usuarios:

```
[1] cannot run job "1": requisite binaries not available
```

Existen paquetes de errores que son compatibles con este enfoque (recomiendo `github.com/pkg/errors`), pero dependerá de ti implementar esta técnica utilizando el paquete de errores que decidas usar. La buena noticia es que esta técnica es orgánica; puedes examinar tu manejo de errores de nivel superior y delimitar entre bugs y errores bien elaborados, y luego asegurar progresivamente que todos los errores que crees se consideren bien elaborados.

## Tiempos de Espera y Cancelación

Cuando se trabaja con código concurrente, los tiempos de espera (timeouts) y las cancelaciones van a aparecer con frecuencia. Como veremos en esta sección, entre otras cosas, los tiempos de espera son cruciales para crear un sistema con un comportamiento que puedas entender. La cancelación es una respuesta natural a un tiempo de espera. También exploraremos otras razones por las que un proceso concurrente podría ser cancelado.

¿Cuáles son las razones por las que podríamos querer que nuestros procesos concurrentes admitan tiempos de espera? He aquí algunas:

**Saturación del sistema**
Como discutimos en la sección "Colas", si nuestro sistema está saturado (es decir, si su capacidad para procesar peticiones está al límite), es posible que queramos que las peticiones en los bordes de nuestro sistema agoten el tiempo de espera en lugar de tardar mucho tiempo en atenderlas. El camino que tomes depende de tu espacio de problemas, pero aquí hay algunas directrices generales sobre cuándo agotar el tiempo de espera:
- Si es poco probable que la petición se repita cuando se agote el tiempo de espera.
- Si no tienes recursos para almacenar las peticiones (ej., memoria para colas en memoria, espacio en disco para colas persistentes).
- Si la necesidad de la petición, o los datos que envía, se volverán obsoletos.

**Datos obsoletos**
A veces los datos tienen una ventana dentro de la cual deben procesarse antes de que haya datos más relevantes disponibles, o la necesidad de procesar los datos haya expirado. Si un proceso concurrente tarda más en procesar los datos que esta ventana, querríamos agotar el tiempo de espera y cancelar el proceso concurrente. Por ejemplo, si nuestro proceso concurrente está desencolando una petición después de una larga espera, la petición o sus datos podrían haber quedado obsoletos durante el proceso de encolado.
Si esta ventana se conoce de antemano, tendría sentido pasar a nuestro proceso concurrente un `context.Context` creado con `context.WithDeadline` o `context.WithTimeout`. Si no se conoce de antemano, querríamos que el padre del proceso concurrente fuera capaz de cancelar el proceso concurrente cuando la necesidad de la petición ya no esté presente. `context.WithCancel` es perfecto para este propósito.

**Intento de prevenir interbloqueos**
En un sistema grande —especialmente en sistemas distribuidos— a veces puede ser difícil comprender la forma en que los datos pueden fluir, o qué casos extremos pueden aparecer. No es descabellado, e incluso se recomienda, poner tiempos de espera en *todas* tus operaciones concurrentes para garantizar que tu sistema no se interbloquee (deadlock). El periodo de tiempo de espera no tiene por qué estar cerca del tiempo real que se tarda en realizar la operación concurrente. El propósito del periodo de tiempo de espera es solo prevenir el interbloqueo y, por tanto, solo necesita ser lo suficientemente corto para que un sistema interbloqueado se desbloquee en una cantidad de tiempo razonable para tu caso de uso.
Recuerda que intentar evitar un interbloqueo estableciendo un tiempo de espera puede transformar potencialmente tu problema de un sistema que se interbloquea a un sistema que tiene un *livelock*. Sin embargo, en sistemas grandes, debido a que hay más partes móviles, hay una mayor probabilidad de que tu sistema experimente un perfil de tiempo diferente al de cuando se interbloqueó por última vez. Por lo tanto, es preferible arriesgarse a un livelock y solucionarlo cuando el tiempo lo permita, que a que se produzca un interbloqueo y tener un sistema recuperable solo mediante reinicio.

Ahora que tenemos una idea de cuándo utilizar los tiempos de espera, dirijamos nuestra atención a las causas de la cancelación y a cómo construir un proceso concurrente para manejar la cancelación con elegancia. Hay varias razones por las que un proceso concurrente podría cancelarse:

- **Tiempos de espera (Timeouts):** Un tiempo de espera es una cancelación implícita.
- **Intervención del usuario:** Para una buena experiencia de usuario, suele ser aconsejable iniciar procesos de larga duración de forma concurrente y luego informar del estado al usuario en un intervalo de sondeo, o permitir a los usuarios consultar el estado como consideren oportuno. Cuando hay operaciones concurrentes de cara al usuario, a veces también es necesario permitir que los usuarios cancelen la operación que han iniciado.
- **Cancelación del padre:** Por el mismo motivo, si cualquier tipo de padre de una operación concurrente —humano o de otro tipo— se detiene, como hijo de ese padre, seremos cancelados.
- **Peticiones replicadas:** Podemos desear enviar datos a múltiples procesos concurrentes en un intento de obtener una respuesta más rápida de uno de ellos. Cuando el primero regrese, querríamos cancelar el resto de los procesos.

Sin embargo, la pregunta "por qué" no es ni mucho menos tan difícil o interesante como la pregunta de "cómo". En el Capítulo 4 exploramos dos formas de cancelar procesos concurrentes: un canal `done` y el tipo `context.Context`. Pero esa es la parte fácil; aquí queremos explorar preguntas más complejas: cuando se cancela un proceso concurrente, ¿qué significa eso para el algoritmo que se estaba ejecutando y sus consumidores posteriores? Al escribir código concurrente que puede terminarse en cualquier momento, ¿qué cosas hay que tener en cuenta?

Para responder a esas preguntas, lo primero que tenemos que explorar es la capacidad de interrupción (preemptability) de un proceso concurrente. Toma el siguiente código y supón que se está ejecutando en su propia goroutine:

```go
var valueStream <-chan interface{}
for {
    select {
    case <-done:
        return
    case v := <-valueStream:
        result := reallyLongCalculation(v)
        select {
        case <-done:
            return
        case resultStream <- result:
        }
    }
}
```

Hemos acoplado diligentemente la lectura de `valueStream` y la escritura en `resultStream` con una comprobación contra el canal `done` para ver si la goroutine ha sido cancelada, pero seguimos teniendo un problema. `reallyLongCalculation` no parece ser interrumpible y, por el nombre, ¡parece que podría llevar mucho tiempo! Esto significa que si algo intenta cancelar esta goroutine mientras `reallyLongCalculation` se está ejecutando, podría pasar mucho tiempo antes de que reconozcamos la cancelación y nos detengamos. Intentemos hacer que `reallyLongCalculation` sea interrumpible:

```go
reallyLongCalculation := func(done <-chan interface{}, v interface{}) interface{} {
    intermediateResult := longCalculation(v)
    select {
    case <-done:
        return nil
    default:
    }
    // ...
    return finalResult
}
```

Hemos hecho algunos progresos: `reallyLongCalculation` es ahora interrumpible, pero podemos ver que solo hemos reducido el problema a la mitad: solo podemos interrumpir `reallyLongCalculation` entre llamadas a otras llamadas a funciones, aparentemente de larga duración. Para solucionar esto, tenemos que hacer que `longCalculation` sea también interrumpible.

Si llevamos este razonamiento a su conclusión lógica, vemos que debemos hacer dos cosas: definir el periodo dentro del cual nuestro proceso concurrente es interrumpible y garantizar que cualquier funcionalidad que lleve más tiempo que este periodo sea ella misma interrumpible. Una forma sencilla de hacerlo es dividir las piezas de tu goroutine en piezas más pequeñas. Debes aspirar a que todas las operaciones atómicas *no interrumpibles* se completen en menos tiempo que el periodo que hayas considerado aceptable.

Hay otro problema que acecha aquí también: si nuestra goroutine resulta que modifica el estado compartido (ej., una base de datos, un archivo, una estructura de datos en memoria), ¿qué ocurre cuando se cancela la goroutine? ¿Intenta tu goroutine deshacer el trabajo intermediario que ha hecho? ¿De cuánto tiempo dispone para hacer este trabajo? Algo le ha dicho a la goroutine que debe detenerse, por lo que la goroutine no debería tardar mucho en revertir su trabajo, ¿verdad?

Es difícil dar consejos generales sobre cómo manejar este problema porque la naturaleza de tu algoritmo dictará mucho de cómo manejas esta situación; sin embargo, si mantienes tus modificaciones a cualquier estado compartido dentro de un ámbito estrecho, y/o te aseguras de que esas modificaciones se deshacen fácilmente, normalmente puedes manejar las cancelaciones bastante bien. Si es posible, construye los resultados intermedios en memoria y luego modifica el estado lo más rápido posible.

Otro problema del que debes preocuparte es el de los mensajes duplicados. Supongamos que tienes un pipeline con tres etapas: una etapa generadora, la etapa A y la etapa B. La etapa generadora monitoriza la etapa A llevando la cuenta de cuánto tiempo ha pasado desde la última vez que leyó de su canal, e inicia una nueva instancia, A2, si la instancia actual deja de funcionar. Si eso ocurriera, es posible que la etapa B reciba mensajes duplicados.

![[../../../assets/Pasted image 20260518105610.png]]
*(Figura 5-1: Ejemplo de cómo podría producirse un mensaje duplicado)*

Hay algunas formas de evitar el envío de mensajes duplicados. La más sencilla (y el método que recomiendo) es hacer que sea extremadamente improbable que una goroutine padre envíe una señal de cancelación después de que una goroutine hija ya haya informado de un resultado. Esto requiere una comunicación bidireccional entre las etapas, y cubriremos esto en detalle en la sección "Latidos" (Heartbeats). Otros enfoques son:

- **Aceptar el primer o el último resultado informado:** Si tu algoritmo lo permite, o tu proceso concurrente es idempotente, puedes simplemente permitir la posibilidad de mensajes duplicados en tus procesos posteriores y elegir si aceptas el primer o el último mensaje que recibas.
- **Sondear la goroutine padre para obtener permiso:** Puedes utilizar la comunicación bidireccional con tu padre para solicitar explícitamente permiso para enviar tu mensaje.

![[../../../assets/Pasted image 20260518105654.png]]

Al diseñar tus procesos concurrentes, asegúrate de tener en cuenta los tiempos de espera y la cancelación. Como muchos otros temas en ingeniería de software, descuidar los tiempos de espera y la cancelación desde el principio e intentar introducirlos después es un poco como intentar añadir huevos a un pastel después de haberlo horneado.

## Latidos (Heartbeats)

Los latidos (heartbeats) son una forma de que los procesos concurrentes señalen vida a partes externas. Reciben su nombre de la anatomía humana, donde un latido significa vida para un observador. Los latidos existen desde antes de Go y siguen siendo útiles en él.

Hay un par de razones diferentes por las que los latidos son interesantes para el código concurrente. Nos permiten conocer mejor nuestro sistema y pueden hacer que las pruebas del sistema sean deterministas cuando de otro modo no lo serían.

Hay dos tipos diferentes de latidos que discutiremos en esta sección:
- Latidos que ocurren en un intervalo de tiempo.
- Latidos que ocurren al principio de una unidad de trabajo.

Los latidos que ocurren en un intervalo de tiempo son útiles para el código concurrente que puede estar esperando a que ocurra algo más para procesar una unidad de trabajo. Como no sabes cuándo puede llegar ese trabajo, tu goroutine puede estar sentada un rato esperando a que ocurra algo. Un latido es una forma de señalar a sus oyentes que todo va bien y que el silencio es esperado.

El siguiente código demuestra una goroutine que expone un latido:

```go
doWork := func(
    done <-chan interface{},
    pulseInterval time.Duration,
) (<-chan interface{}, <-chan time.Time) {
    heartbeat := make(chan interface{}) // 1
    results := make(chan time.Time)
    go func() {
        defer close(heartbeat)
        defer close(results)

        pulse := time.NewTicker(pulseInterval) // 2
        workGen := time.NewTicker(pulseInterval * 2) // 3

        sendPulse := func() {
            select {
            case heartbeat <- struct{}{}:
            default: // 4
            }
        }

        sendResult := func(r time.Time) {
            for {
                select {
                case <-done:
                    return
                case <-pulse.C: // 5
                    sendPulse()
                case results <- r:
                    return
                }
            }
        }

        for {
            select {
            case <-done:
                return
            case <-pulse.C: // 5
                sendPulse()
            case r := <-workGen.C:
                sendResult(r)
            }
        }
    }()
    return heartbeat, results
}
```

1. Aquí configuramos un canal para enviar latidos. Lo devolvemos fuera de `doWork`.
2. Aquí configuramos el latido para que pulse en el `pulseInterval` que se nos dio. Cada `pulseInterval` habrá algo que leer en este canal.
3. Esto es solo otro ticker utilizado para simular la llegada de trabajo. Elegimos una duración mayor que el `pulseInterval` para que podamos ver algunos latidos saliendo de la goroutine.
4. Ten en cuenta que incluimos una cláusula `default`. Debemos protegernos siempre contra el hecho de que nadie esté escuchando nuestro latido. Los resultados emitidos por la goroutine son críticos, pero los pulsos no lo son.
5. Al igual que con los canales `done`, siempre que realices un envío o una recepción, también debes incluir un caso para el pulso del latido.

Nota que como podríamos estar enviando múltiples pulsos mientras esperamos la entrada, o múltiples pulsos mientras esperamos para enviar resultados, todas las sentencias `select` necesitan estar dentro de bucles `for`. Todo parece correcto hasta ahora; ¿cómo utilizamos esta función y consumimos los eventos que emite? Echemos un vistazo:

```go
done := make(chan interface{})
time.AfterFunc(10*time.Second, func() { close(done) }) // 1

const timeout = 2 * time.Second // 2
heartbeat, results := doWork(done, timeout/2) // 3

for {
    select {
    case _, ok := <-heartbeat: // 4
        if ok == false {
            return
        }
        fmt.Println("pulse")
    case r, ok := <-results: // 5
        if ok == false {
            return
        }
        fmt.Printf("results %v\n", r.Second())
    case <-time.After(timeout): // 6
        fmt.Println("worker goroutine is not healthy!")
        return
    }
}
```

1. Configuramos el canal `done` estándar y lo cerramos después de 10 segundos. Esto le da tiempo a nuestra goroutine para hacer algo de trabajo.
2. Aquí establecemos nuestro periodo de tiempo de espera. Lo usaremos para acoplar nuestro intervalo de latidos a nuestro tiempo de espera.
3. Pasamos `timeout/2` aquí. Esto le da a nuestro latido un tic extra para responder para que nuestro tiempo de espera no sea demasiado sensible.
4. Aquí seleccionamos sobre el latido. Cuando no hay resultados, al menos tenemos garantizado un mensaje del canal `heartbeat` cada `timeout/2`. Si no lo recibimos, sabemos que algo va mal con la propia goroutine.
5. Aquí seleccionamos del canal de resultados; nada fuera de lo común.
6. Aquí agotamos el tiempo de espera si no hemos recibido ni un latido ni un nuevo resultado.

Al ejecutar este código, verás que recibimos unos dos pulsos por resultado, tal y como pretendíamos.

En un sistema que funciona correctamente, los latidos no son tan interesantes. Podríamos utilizarlos para recopilar estadísticas sobre el tiempo de inactividad, pero la utilidad de los latidos basados en intervalos brilla realmente cuando tu goroutine no se comporta como se esperaba. Los latidos nos permiten detectar de forma determinista si una goroutine está sana o no, evitando interbloqueos sin depender de tiempos de espera largos y arbitrarios.

## Peticiones Replicadas

Para algunas aplicaciones, recibir una respuesta lo más rápido posible es la máxima prioridad. Por ejemplo, tal vez la aplicación esté atendiendo la petición HTTP de un usuario, o recuperando un blob de datos replicados. En estos casos puedes hacer un compromiso: puedes replicar la petición a múltiples manejadores (ya sean goroutines, procesos o servidores), y uno de ellos regresará más rápido que los demás; entonces puedes devolver inmediatamente el resultado. La desventaja es que tendrás que utilizar recursos para mantener múltiples copias de los manejadores en ejecución.

Si esta replicación se hace en memoria, puede que no sea tan costosa, pero si replicar los manejadores requiere replicar procesos, servidores o incluso centros de datos, esto puede resultar bastante caro. La decisión que tendrás que tomar es si el coste compensa el beneficio.

Veamos cómo puedes replicar peticiones dentro de un solo proceso. Utilizaremos múltiples goroutines para que sirvan de manejadores de peticiones, y las goroutines dormirán durante una cantidad aleatoria de tiempo entre uno y seis nanosegundos para simular la carga. Esto nos dará manejadores que devuelven un resultado en varios momentos y nos permitirá ver cómo esto puede conducir a resultados más rápidos.

```go
doWork := func(
    done <-chan interface{},
    id int,
    wg *sync.WaitGroup,
    result chan<- int,
) {
    started := time.Now()
    defer wg.Done()

    // Simula carga aleatoria
    simulationTime := time.Duration(1+rand.Intn(5)) * time.Second
    select {
    case <-done:
    case <-time.After(simulationTime):
    }

    select {
    case <-done:
    case result <- id:
    }

    took := time.Since(started)
    // Muestra cuánto tiempo habría tardado si no hubiéramos cancelado
    if took < simulationTime {
        took = simulationTime
    }
    fmt.Printf("%v took %v\n", id, took)
}

done := make(chan interface{})
result := make(chan int)

var wg sync.WaitGroup
wg.Add(10)
for i := 0; i < 10; i++ { // 1
    go doWork(done, i, &wg, result)
}

firstReturned := <-result // 2
close(done) // 3
wg.Wait()

fmt.Printf("Received an answer from #%v\n", firstReturned)
```

1. Aquí iniciamos 10 manejadores para encargarse de nuestras peticiones.
2. Esta línea toma el primer valor devuelto por el grupo de manejadores.
3. Aquí cancelamos todos los manejadores restantes. Esto asegura que no sigan haciendo trabajo innecesario.

Este ejemplo muestra que el primer manejador en responder gana y el resto son cancelados para liberar recursos. Aunque puede ser costoso de configurar y mantener, si la velocidad es tu objetivo, esta es una técnica valiosa. Además, esto proporciona naturalmente tolerancia a fallos y escalabilidad.

## Limitación de Tasa (Rate Limiting)

Si alguna vez has trabajado con la API de un servicio, es probable que hayas tenido que lidiar con la limitación de tasa (rate limiting), que restringe el número de veces que se accede a algún tipo de recurso a un número finito por unidad de tiempo. El recurso puede ser cualquier cosa: conexiones API, lecturas/escrituras en disco, paquetes de red, errores.

Las limitaciones de tasa permiten razonar sobre el rendimiento y la estabilidad de tu sistema evitando que se salga de los límites que ya has investigado. En Go, la mayoría de las limitaciones de tasa se realizan utilizando un algoritmo llamado *token bucket* (cubo de tokens).

Imagina un cubo que contiene fichas o "tokens". Cada vez que necesites acceder a un recurso, debes sacar un token del cubo. Si no hay tokens, la petición se deniega o se bloquea hasta que haya uno. El cubo tiene una profundidad `d` (capacidad máxima) y se rellena a una tasa `r` (tokens por unidad de tiempo).

Utilizaremos el paquete `golang.org/x/time/rate` para nuestros ejemplos.

```go
func Open() *APIConnection {
    return &APIConnection{
        rateLimiter: rate.NewLimiter(rate.Every(1*time.Second), 1), // 1
    }
}

type APIConnection struct {
    rateLimiter *rate.Limiter
}

func (a *APIConnection) ReadFile(ctx context.Context) error {
    if err := a.rateLimiter.Wait(ctx); err != nil { // 2
        return err
    }
    // Fingir que leemos un archivo
    fmt.Printf("ReadFile\n")
    return nil
}
```

1. Aquí establecemos el límite de tasa para todas las conexiones de la API a un evento por segundo.
2. Aquí esperamos a que el limitador de tasa tenga suficientes tokens de acceso para completar nuestra petición.

En producción, a menudo querremos establecer múltiples niveles de límites: controles de grano fino para limitar las peticiones por segundo, y controles de grano grueso para limitar las peticiones por minuto, hora o día. Para ello podemos crear un `MultiLimiter`:

```go
type MultiLimiter struct {
    limiters []RateLimiter
}

func (l *MultiLimiter) Wait(ctx context.Context) error {
    for _, l := range l.limiters {
        if err := l.Wait(ctx); err != nil {
            return err
        }
    }
    return nil
}
```

Esta técnica nos permite componer limitadores lógicos en grupos que tengan sentido para cada llamada, protegiendo tanto nuestro sistema como el de nuestros clientes.

## Curación de Goroutines no Saludables

En procesos de larga duración, como los demonios (daemons), es muy común tener un conjunto de goroutines de larga vida que pueden quedarse bloqueadas en un mal estado del que no pueden recuperarse sin ayuda externa. En estos casos, puede ser útil crear un mecanismo que asegure que tus goroutines permanezcan sanas y las reinicie si dejan de estarlo. Nos referiremos a este proceso como "curación" (healing).

Para curar goroutines, utilizaremos nuestro patrón de latidos para comprobar la vitalidad de la goroutine que estamos monitorizando. Llamaremos a la lógica que monitoriza la salud de una goroutine un *steward* (mayordomo), y a la goroutine que monitoriza un *ward* (protegido).

```go
type startGoroutineFn func(
    done <-chan interface{},
    pulseInterval time.Duration,
) (heartbeat <-chan interface{}) // 1

newSteward := func(
    timeout time.Duration,
    startGoroutine startGoroutineFn,
) startGoroutineFn { // 2
    return func(
        done <-chan interface{},
        pulseInterval time.Duration,
    ) (<-chan interface{}) {
        heartbeat := make(chan interface{})
        go func() {
            defer close(heartbeat)

            var wardDone chan interface{}
            var wardHeartbeat <-chan interface{}
            startWard := func() { // 3
                wardDone = make(chan interface{}) // 4
                wardHeartbeat = startGoroutine(or(wardDone, done), pulseInterval) // 5
            }

            startWard()
            pulse := time.NewTicker(pulseInterval)
            defer pulse.Stop()

            for {
                select {
                case <-pulse.C: // 6
                    select {
                    case heartbeat <- struct{}{}:
                    default:
                    }
                case <-wardHeartbeat: // 7
                    continue
                case <-time.After(timeout): // 8
                    fmt.Println("steward: ward unhealthy; restarting")
                    close(wardDone)
                    startWard()
                case <-done:
                    return
                }
            }
        }()
        return heartbeat
    }
}
```

El uso de este patrón puede ayudar a garantizar que tus goroutines de larga duración se mantengan en funcionamiento y sanas, reiniciándolas automáticamente si fallan o se bloquean.

## Resumen

En este capítulo, hemos cubierto algunas formas de mantener tus sistemas estables y comprensibles a medida que los dominios de los problemas que abordan requieren sistemas más grandes que quizás sean distribuidos. Este capítulo también ha demostrado cómo las primitivas de concurrencia de Go escalan a medida que creas abstracciones de orden superior. Sin el beneficio de un lenguaje diseñado en torno a la concurrencia, estos patrones serían probablemente mucho más engorrosos y mucho menos robustos.

En el capítulo final, vamos a explorar las entrañas de parte del runtime de Go para ayudarte a desarrollar un conocimiento profundo de cómo funcionan las cosas. También exploraremos algunas herramientas útiles que facilitarán el trabajo de desarrollar y depurar software en Go.
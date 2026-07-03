Ya sea que uses Kafka como cola, bus de mensajes o plataforma de almacenamiento de datos, siempre lo usarás creando un productor que escriba datos para Kafka, un consumidor que lea datos de Kafka, o una aplicación que cumpla ambos roles.

Por ejemplo, en un sistema de procesamiento de transacciones con tarjeta de crédito, habrá una aplicación cliente, quizás una tienda online, responsable de enviar cada transacción a Kafka inmediatamente después de realizar un pago. Otra aplicación es responsable de comprobar inmediatamente esta transacción con un motor de reglas y determinar si la transacción es aprobada o denegada. La respuesta de aprobación/denegación puede entonces escribirse de nuevo en Kafka, y la respuesta puede propagarse de vuelta a la tienda online donde se inició la transacción. Una tercera aplicación puede leer tanto las transacciones como el estado de aprobación de Kafka y almacenarlas en una base de datos donde los analistas pueden revisar posteriormente las decisiones y quizás mejorar el motor de reglas.

Apache Kafka incluye APIs de cliente integradas que los desarrolladores pueden usar al desarrollar aplicaciones que interactúan con Kafka.

En este capítulo aprenderemos a usar el productor Kafka, comenzando con una visión general de su diseño y componentes. Mostraremos cómo crear objetos `ProducerRecord`, cómo enviar registros a Kafka y cómo gestionar los errores que Kafka pueda devolver. A continuación, revisaremos las opciones de configuración más importantes que se usan para controlar el comportamiento del productor. Concluiremos con un análisis más profundo de cómo usar diferentes métodos de particionamiento y serializadores, y cómo escribir tus propios serializadores y particionadores.`KafkaProducer`

En [el capítulo 4](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch04.html#reading_data_from_kafka), analizaremos el cliente consumidor de Kafka y la lectura de datos de Kafka.

# Clientes de terceros

Además de los clientes integrados, Kafka cuenta con un protocolo de cable binario. Esto significa que es posible que las aplicaciones lean mensajes de Kafka o escriban mensajes en Kafka simplemente enviando las secuencias correctas de bytes al puerto de red de Kafka. Existen múltiples clientes que implementan el protocolo wire de Kafka en diferentes lenguajes de programación, ofreciendo formas sencillas de usar Kafka no solo en aplicaciones Java, sino también en lenguajes como C++, Python, Go y muchos más. Esos clientes no forman parte del proyecto Apache Kafka, pero en la [wiki](https://oreil.ly/9SbJr) del proyecto se mantiene una lista de clientes no Java. El protocolo de cable y los clientes externos están fuera del alcance del capítulo.

# Resumen del productor

Hay muchas razones por las que una aplicación puede necesitar escribir mensajes a Kafka: grabar actividades del usuario para auditoría o análisis, registrar métricas, almacenar mensajes de registro, registrar información de electrodomésticos inteligentes, comunicarse de forma asíncrona con otras aplicaciones, almacenar información en búfer antes de escribir en una base de datos y mucho más.

Esos diversos casos de uso también implican requisitos distintos: ¿es cada mensaje crítico o podemos tolerar la pérdida de mensajes? ¿Estamos de acuerdo con duplicar mensajes accidentalmente? ¿Hay algún requisito estricto de latencia o rendimiento que debamos soportar?

En el ejemplo de procesamiento de transacciones con tarjeta de crédito que presentamos antes, podemos ver que es fundamental no perder ni duplicar ningún mensaje. La latencia debe ser baja, pero se pueden tolerar latencias de hasta 500 ms y el rendimiento debe ser muy alto; esperamos procesar hasta un millón de mensajes por segundo.

Otro caso de uso podría ser almacenar información de clics de una página web. En ese caso, se puede tolerar cierta pérdida de mensajes o algunos duplicados; La latencia puede ser alta siempre que no afecte a la experiencia del usuario. En otras palabras, no nos importa si el mensaje tarda unos segundos en llegar a Kafka, siempre que la siguiente página cargue inmediatamente después de que el usuario haga clic en un enlace. El rendimiento dependerá del nivel de actividad que preveamos en nuestra web.

Los diferentes requisitos influirán en la forma en que usas la API de productor para escribir mensajes a Kafka y en la configuración que uses.

Aunque la API del productor es muy sencilla, hay algo más que ocurre bajo el capó del productor cuando enviamos datos. La [Figura 3-1](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch03.html#fig-1-overview) muestra los pasos principales implicados en el envío de datos a Kafka.
![[../../../assets/Pasted image 20260522214216.png]]
Figura 3-1. Visión general de alto nivel de los componentes productores de Kafka

Empezamos a producir mensajes para Kafka creando un , que debe incluir el tema al que queremos enviar el registro y un valor. Opcionalmente, también podemos especificar una clave, una partición, una marca de tiempo y/o una colección de cabeceras. Una vez que enviemos el , lo primero que hará el productor es serializar los objetos clave y valor en arrays de bytes para que puedan enviarse por la red.`ProducerRecord``ProducerRecord`

Después, si no especificamos explícitamente una partición, los datos se envían a un particionador. El particionista elegirá una partición por nosotros, normalmente en función de la clave. Una vez seleccionada una partición, el productor sabe a qué tema y partición irá el disco. Luego añade el registro a un lote de registros que también se enviarán al mismo tema y partición. Un hilo separado es responsable de enviar esos lotes de registros a los corredores Kafka correspondientes.`ProducerRecord`

Cuando el intermediario recibe los mensajes, responde con una respuesta. Si los mensajes se escribieron correctamente en Kafka, devolverá un objeto con el tema, la partición y el desplazamiento del registro dentro de la partición. Si el intermediario no escribió los mensajes, devolverá un error. Cuando el productor recibe un error, puede intentar enviar el mensaje varias veces más antes de rendirse y devolver un error.`RecordMetadata`

# Construyendo un productor kafka

El primer paso para escribir mensajes a Kafka es crear un objeto productor con las propiedades que quieres pasar al productor. Un productor de Kafka tiene tres propiedades obligatorias:

- `bootstrap.servers`

	Lista de pares de brokers que el productor usará para establecer la conexión inicial con el clúster de Kafka. Esta lista no tiene por qué incluir a todos los intermediarios, ya que el productor obtendrá más información tras la conexión inicial. Pero se recomienda incluir al menos dos, para que en caso de que uno de los brokers se caigan, el productor pueda seguir conectándose al clúster.`host:port`

- `key.serializer`

	Nombre de una clase que se usará para serializar las claves de los registros que produciremos a Kafka. Los brokers Kafka esperan arrays de bytes como claves y valores de los mensajes. Sin embargo, la interfaz productora permite, usando tipos parametrizados, enviar cualquier objeto Java como clave y valor. Esto da lugar a un código muy legible, pero también significa que el productor debe saber cómo convertir estos objetos en arrays de bytes. debe asignarse al nombre de una clase que implemente la interfaz. El productor usará esta clase para serializar el objeto clave en un array de bytes. El paquete cliente Kafka incluye (que no hace mucho), , , y mucho más, así que si usas tipos comunes, no es necesario implementar tus propios serializadores. Se requiere configurar incluso si solo tienes intención de enviar valores, pero puedes usar el tipo para la clave y el .`key.serializer``org.apache.kafka.common.serialization.Serializer``ByteArraySerializer``String​Serial⁠izer``IntegerSerializer``key.serializer``Void``VoidSerializer`

- `value.serializer`

	Nombre de una clase que se usará para serializar los valores de los registros que produciremos en Kafka. De la misma manera que se asigna el nombre de una clase que serializará el objeto clave mensaje a un array de bytes, se asigna a una clase que serializará el objeto valor mensaje.`key.serializer``value.serializer`

El siguiente fragmento de código muestra cómo crear un nuevo productor estableciendo solo los parámetros obligatorios y usando los valores predeterminados para todo lo demás:

```java
Properties kafkaProps = new Properties(); // 1
kafkaProps.put("bootstrap.servers", "broker1:9092,broker2:9092");

kafkaProps.put("key.serializer",
    "org.apache.kafka.common.serialization.StringSerializer"); // 2
kafkaProps.put("value.serializer",
    "org.apache.kafka.common.serialization.StringSerializer");

producer = new KafkaProducer<String, String>(kafkaProps); // 3
```

1. Empezamos con un objeto.`Properties`
2. Como planeamos usar cadenas para la clave y el valor del mensaje, usamos el archivo integrado .`StringSerializer`
3. Aquí creamos un nuevo productor estableciendo los tipos de clave y valor apropiados y pasando el objeto.`Properties`

Con una interfaz tan sencilla, está claro que la mayor parte del control sobre el comportamiento del productor se realiza estableciendo las propiedades de configuración correctas. La documentación de Apache Kafka cubre todas las [opciones de configuración](http://bit.ly/2sMu1c8), y repasaremos las más importantes más adelante en este capítulo.

Una vez que instanciamos a un productor, es hora de empezar a enviar mensajes. Existen tres métodos principales para enviar mensajes:

Disparar y olvidar

Enviamos un mensaje al servidor y realmente no nos importa si llega con éxito o no. La mayoría de las veces, llega con éxito, ya que Kafka está muy disponible y el productor intentará enviar mensajes automáticamente. Sin embargo, en caso de errores no reutilizables o tiempo de espera, los mensajes se perderán y la aplicación no recibirá ninguna información ni excepción al respecto.

Envío síncrono

Técnicamente, Kafka Producer siempre es asincrónico: enviamos un mensaje y el método devuelve un objeto. Sin embargo, solíamos esperar a ver si había tenido éxito o no antes de enviar el siguiente disco.`send()``Future``get()``Future``send()`

Envío asincrónico

Llamamos al método con una función de callback, que se activa cuando recibe una respuesta del broker Kafka.`send()`

En los ejemplos que sigue, veremos cómo enviar mensajes usando estos métodos y cómo manejar los diferentes tipos de errores que pueden ocurrir.

Aunque todos los ejemplos de este capítulo son monohilos, un objeto productor puede ser utilizado por múltiples hilos para enviar mensajes.

# Enviar un mensaje a Kafka

La forma más sencilla de enviar un mensaje es la siguiente:
```java
ProducerRecord<String, String> record =
    new ProducerRecord<>("CustomerCountry", "Precision Products",
        "France"); // 1
try {
    producer.send(record); // 2
} catch (Exception e) {
    e.printStackTrace(); // 3
}
```

  
1. [El productor acepta objetos, así que empezamos creando uno. `ProducerRecord` tiene varios constructores, de los que hablaremos más adelante. Aquí usamos uno que requiere el nombre del tema al que enviamos los datos, que siempre es una cadena, y la clave y el valor que enviamos a Kafka, que en este caso también son cadenas. Los tipos de la clave y el valor deben coincidir con nuestros y objetos.`ProducerRecord``key serializer``value serializer`](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch03.html#co_kafka_producers__writing__span_class__keep_together__messages_to_kafka__span__CO2-1)
2. [Usamos el método de objeto productor para enviar el archivo . Como hemos visto en el diagrama de arquitectura productor en [la Figura 3-1](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch03.html#fig-1-overview), el mensaje se colocará en un búfer y se enviará al broker en un hilo separado. El método devuelve un [objeto `Java Future`](http://bit.ly/2rG7Cg6) con , pero como simplemente ignoramos el valor devuelto, no tenemos forma de saber si el mensaje se envió correctamente o no. Este método de envío de mensajes puede usarse cuando es aceptable dejar un mensaje en silencio. Esto no suele ocurrir en aplicaciones de producción.`send()``ProducerRecord``send()``RecordMetadata`](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch03.html#co_kafka_producers__writing__span_class__keep_together__messages_to_kafka__span__CO2-2)
3. [Aunque ignoramos los errores que pueden ocurrir al enviar mensajes a los brokers de Kafka o en los propios brokers, aún podemos obtener una excepción si el productor encontró errores antes de enviar el mensaje a Kafka. Estos pueden ser, por ejemplo, una `SerializationException` cuando no se serializa el mensaje, un o si el búfer está lleno, o una `InterruptionException` si el hilo emisor fue interrumpido.`Buffer​ExhaustedException``TimeoutException`](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch03.html#co_kafka_producers__writing__span_class__keep_together__messages_to_kafka__span__CO2-3)
## Enviar un mensaje de forma síncrona

Enviar un mensaje de forma sincrónica es sencillo pero aún permite al productor detectar excepciones cuando Kafka responde a la solicitud de producción con un error, o cuando se agotan los intentos de envío. El principal compromiso es el rendimiento. Dependiendo de lo ocupado que esté el clúster Kafka, los brokers pueden tardar entre 2 ms y unos segundos en responder a las solicitudes de producción. Si envías mensajes de forma simultánea, el hilo de envío pasará ese tiempo esperando y sin hacer nada más, ni siquiera enviando mensajes adicionales. Esto conduce a un rendimiento muy pobre y, como resultado, los envíos síncronos normalmente no se usan en aplicaciones de producción (pero son muy comunes en ejemplos de código).

La forma más sencilla de enviar un mensaje de forma síncrona es la siguiente:

```java
ProducerRecord<String, String> record =
    new ProducerRecord<>("CustomerCountry", "Precision Products", "France");
try {
    producer.send(record).get(); // 1
} catch (Exception e) {
    e.printStackTrace(); // 2
}
```

1. [Aquí estamos acostumbrados a esperar una respuesta de Kafka. Este método generará una excepción si el registro no se envía correctamente a Kafka. Si no hubo errores, obtendremos un objeto que podemos usar para recuperar el desplazamiento en el que se escribió el mensaje y otros metadatos.`Future.get()``RecordMetadata`](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch03.html#co_kafka_producers__writing__span_class__keep_together__messages_to_kafka__span__CO3-1)

2. [Si hubo errores antes o durante el envío del registro a Kafka, encontraremos una excepción. En este caso, simplemente imprimimos cualquier excepción que encontremos.](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch03.html#co_kafka_producers__writing__span_class__keep_together__messages_to_kafka__span__CO3-2)

`KafkaProducer` tiene dos tipos de errores. Los errores _retentables_ son aquellos que pueden resolverse enviando el mensaje de nuevo. Por ejemplo, un error de conexión puede resolverse porque la conexión puede restablecerse. Un error de "no líder para partición" puede resolverse cuando se elige un nuevo líder para la partición y se actualizan los metadatos del cliente. se puede configurar para reintentar esos errores automáticamente, de modo que el código de la aplicación solo recibirá excepciones reintentables cuando se agotara el número de intentos y el error no se resolvió. Algunos errores no se resolverán intentándolo de nuevo—por ejemplo, "Tamaño del mensaje demasiado grande." En esos casos, no intentará reintentarlo y devolverá la excepción inmediatamente.`KafkaProducer``KafkaProducer`
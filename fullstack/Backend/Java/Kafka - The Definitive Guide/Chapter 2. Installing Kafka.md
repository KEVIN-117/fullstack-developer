Este capítulo describe cómo empezar con el broker Apache Kafka, incluyendo cómo configurar Apache ZooKeeper, que es utilizado por Kafka para almacenar metadatos para los brokers. El capítulo también cubrirá opciones básicas de configuración para despliegues de Kafka, así como algunas sugerencias para seleccionar el hardware correcto para ejecutar los brokers. Por último, explicamos cómo instalar varios brokers Kafka como parte de un solo clúster y cosas que debes saber al usar Kafka en un entorno de producción.

# Configuración del entorno

Antes de usar Apache Kafka, tu entorno debe estar configurado con algunos requisitos previos para asegurar que funcione correctamente. Las siguientes secciones te guiarán durante ese proceso.

## Elección de un sistema operativo

Apache Kafka es una aplicación Java y puede ejecutarse en muchos sistemas operativos. Aunque Kafka puede ejecutarse en muchos sistemas operativos, incluyendo Windows, macOS, Linux y otros, Linux es el sistema recomendado para el uso general. Los pasos de instalación en este capítulo se centrarán en configurar y usar Kafka en un entorno Linux. Para información sobre la instalación de Kafka en Windows y macOS, consulte [el Apéndice A](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/app01.html#appendix_installing_other_os).

## Instalación de Java

Antes de instalar ZooKeeper o Kafka, necesitarás un entorno Java configurado y funcionando. Kafka y ZooKeeper funcionan bien con todas las implementaciones de Java basadas en OpenJDK, incluido Oracle JDK. Las últimas versiones de Kafka soportan tanto Java 8 como Java 11. La versión exacta instalada puede ser la que proporciona tu sistema operativo o una descargada directamente de la web, por ejemplo, [la web de Oracle para la versión de Oracle](https://www.oracle.com/java). Aunque ZooKeeper y Kafka funcionarán con una edición de Java en tiempo de ejecución, se recomienda al desarrollar herramientas y aplicaciones contar con el Java Development Kit (JDK) completo. Se recomienda instalar la última versión de parche de tu entorno Java, ya que las versiones anteriores pueden tener vulnerabilidades de seguridad. Los pasos de instalación asumirán que has instalado JDK versión 11 actualización 10 desplegada en _/usr/java/jdk-11.0.10_.

## Instalación de ZooKeeper

Apache Kafka utiliza Apache ZooKeeper para almacenar metadatos sobre el clúster Kafka, así como detalles de clientes de consumidor, como se muestra en [la Figura 2-1](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch02.html#fig-1-kafkazk). ZooKeeper es un servicio centralizado para mantener la información de configuración, nombrar, proporcionar sincronización distribuida y proporcionar servicios de grupo. Este libro no entrará en detalles extensos sobre ZooKeeper, pero limitará las explicaciones solo a lo necesario para operar Kafka. Aunque es posible ejecutar un servidor ZooKeeper usando scripts contenidos en la distribución Kafka, es trivial instalar una versión completa de ZooKeeper desde la distribución.

![[../../../assets/Pasted image 20260522213609.png]]
Figura 2-1. Kafka y ZooKeeper

Kafka ha sido probado extensamente con la versión estable 3.5 de ZooKeeper y se actualiza regularmente para incluir la última versión. En este libro, utilizaremos ZooKeeper 3.5.9, que se puede descargar desde la [web de ZooKeeper](https://oreil.ly/iMZjR).

### Servidor independiente

ZooKeeper viene con un archivo de configuración de ejemplo base que funcionará bien para la mayoría de los casos de uso en _/usr/local/zookeeper/config/zoo_sample.cfg_. Sin embargo, en este libro crearemos manualmente el nuestro con algunos ajustes básicos para fines de demostración. El siguiente ejemplo instala ZooKeeper con una configuración básica en _/usr/local/zookeeper_, almacenando sus datos en _/var/lib/zookeeper_:

```
# tar -zxf apache-zookeeper-3.5.9-bin.tar.gz
# mv apache-zookeeper-3.5.9-bin /usr/local/zookeeper
# mkdir -p /var/lib/zookeeper
# cp > /usr/local/zookeeper/conf/zoo.cfg << EOF
> tickTime=2000
> dataDir=/var/lib/zookeeper
> clientPort=2181
> EOF
# export JAVA_HOME=/usr/java/jdk-11.0.10
# /usr/local/zookeeper/bin/zkServer.sh start
JMX enabled by default
Using config: /usr/local/zookeeper/bin/../conf/zoo.cfg
Starting zookeeper ... STARTED
#
```

Ahora puedes validar que ZooKeeper está funcionando correctamente en modo independiente conectándote al puerto cliente y enviando el comando de cuatro letras. Esto devolverá información básica de ZooKeeper desde el servidor en ejecución:`srvr`

```
# telnet localhost 2181
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
srvr
Zookeeper version: 3.5.9-83df9301aa5c2a5d284a9940177808c01bc35cef, built on 01/06/2021 19:49 GMT
Latency min/avg/max: 0/0/0
Received: 1
Sent: 0
Connections: 1
Outstanding: 0
Zxid: 0x0
Mode: standalone
Node count: 5
Connection closed by foreign host.
#
```

### Conjunto ZooKeeper

ZooKeeper está diseñado para funcionar como un conjunto, llamado _conjunto_, para garantizar una alta disponibilidad. Debido al algoritmo de balanceo utilizado, se recomienda que los conjuntos contengan un número impar de servidores (por ejemplo, 3, 5, etc.), ya que la mayoría de los miembros del conjunto (un _quórum_) deben estar trabajando para que ZooKeeper pueda responder a las solicitudes. Esto significa que en un conjunto de tres nodos, puedes ejecutar con un nodo faltante. Con un conjunto de cinco nodos, puedes ejecutar con dos nodos faltando.

# Dimensionando tu conjunto de ZooKeeper

Considera ejecutar ZooKeeper en un conjunto de cinco nodos. Para hacer cambios de configuración en el conjunto, incluyendo cambiar un nodo, tendrás que recargar los nodos uno a uno. Si tu conjunto no puede tolerar que más de un nodo esté caído, realizar trabajos de mantenimiento supone un riesgo adicional. Tampoco se recomienda ejecutar más de siete nodos, ya que el rendimiento puede empezar a degradarse debido a la naturaleza del protocolo de consenso.

Además, si consideras que cinco o siete nodos no soportan la carga debido a demasiadas conexiones de clientes, considera añadir nodos observadores adicionales para ayudar a equilibrar el tráfico de solo lectura.

Para configurar servidores ZooKeeper en conjunto, deben tener una configuración común que liste todos los servidores, y cada servidor necesita un archivo _myid_ en el directorio de datos que especifique el número ID del servidor. Si los nombres de host de los servidores en el conjunto son , , y , el archivo de configuración podría verse así:`zoo1.example.com``zoo2.example.com``zoo3.example.com`

```
tickTime=2000
dataDir=/var/lib/zookeeper
clientPort=2181
initLimit=20
syncLimit=5
server.1=zoo1.example.com:2888:3888
server.2=zoo2.example.com:2888:3888
server.3=zoo3.example.com:2888:3888
```

En esta configuración, es la cantidad de tiempo que permite a los seguidores conectar con un líder. El valor limita cuánto tiempo pueden estar los seguidores desincronizados con el líder. Ambos valores son un número de unidades, lo que hace que 20 × 2.000 ms, o 40 segundos. La configuración también lista cada servidor del conjunto. Los servidores se especifican en el formato , con los siguientes parámetros:`initLimit``syncLimit``tickTime``init​Li⁠mit``_server.X=hostname:peerPort:leaderPort_`

- `X`

	El número de ID del servidor. Esto debe ser un entero, pero no tiene que ser basado en ceros ni secuencial.

- `hostname`

	El nombre de host o la dirección IP del servidor.

- `peerPort`

	El puerto TCP sobre el que los servidores del conjunto se comunican entre sí.

- `leaderPort`

	El puerto TCP sobre el que se realiza la elección de líderes.

Los clientes solo necesitan poder conectarse al conjunto a través del , pero los miembros del conjunto deben poder comunicarse entre sí a través de los tres puertos.`_clientPort_`

Además del archivo de configuración compartido, cada servidor debe tener un archivo en el directorio _dataDir_ con el nombre _myid_. Este archivo debe contener el número ID del servidor, que debe coincidir con el archivo de configuración. Una vez completados estos pasos, los servidores se iniciarán y se comunicarán entre sí en conjunto.

# Probando el conjunto ZooKeeper en una sola máquina

Es posible probar y ejecutar un conjunto ZooKeeper en una sola máquina especificando todos los nombres de host en la configuración como y con puertos únicos especificados para y para cada instancia. Además, sería necesario crear un _zoo.cfg_ separado para cada instancia con un _dataDir_ único y definido para cada instancia. Esto puede ser útil solo para pruebas, pero _no_ se recomienda para sistemas de producción.`localhost``_peerPort_``_leaderPort_``_clientPort_`

# Instalación de un corredor Kafka

Una vez configurados Java y ZooKeeper, estarás listo para instalar Apache Kafka. La versión actual se puede descargar desde la [web de Kafka](https://oreil.ly/xLopS). En el momento de la edición, esa versión es la 2.8.0 y funciona bajo la versión 2.13.0 de Scala. Los ejemplos de estos capítulos se muestran usando la versión 2.7.0.

El siguiente ejemplo instala Kafka en _/usr/local/kafka_, configurado para usar el servidor ZooKeeper iniciado previamente y para almacenar los segmentos del registro de mensajes almacenados en _/tmp/kafka-logs_:

```
# tar -zxf kafka_2.13-2.7.0.tgz
# mv kafka_2.13-2.7.0 /usr/local/kafka
# mkdir /tmp/kafka-logs
# export JAVA_HOME=/usr/java/jdk-11.0.10
# /usr/local/kafka/bin/kafka-server-start.sh -daemon
/usr/local/kafka/config/server.properties
#
```

Una vez que el broker Kafka está activo, podemos verificar que está funcionando realizando algunas operaciones sencillas contra el clúster: crear un tema de prueba, producir algunos mensajes y consumir los mismos mensajes.

Crea y verifica un tema:

```
# /usr/local/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create
--replication-factor 1 --partitions 1 --topic test
Created topic "test".
# /usr/local/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092
--describe --topic test
Topic:test    PartitionCount:1    ReplicationFactor:1    Configs:
    Topic: test    Partition: 0    Leader: 0    Replicas: 0    Isr: 0
#
```

Produce mensajes para un tema de prueba (usa Ctrl-C para detener al productor en cualquier momento):

```
# /usr/local/kafka/bin/kafka-console-producer.sh --bootstrap-server
localhost:9092 --topic test
Test Message 1
Test Message 2
^C
#
```

Consume mensajes de un tema de prueba:

```
# /usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server
localhost:9092 --topic test --from-beginning
Test Message 1
Test Message 2
^C
Processed a total of 2 messages
#
```

# Cancelación de las conexiones ZooKeeper en las utilidades CLI de Kafka

Si conoces versiones antiguas de las utilidades Kafka, puede que estés acostumbrado a usar una cadena de conexión. Esto ha sido obsoleto en casi todos los casos. La mejor práctica actual es usar la opción más nueva y conectarse directamente al broker de Kafka. Si estás ejecutando en un clúster, puedes proporcionar el host:port de cualquier broker dentro del clúster.`--zookeeper``--bootstrap-server`

# Configuración del Broker

La configuración de ejemplo proporcionada con la distribución Kafka es suficiente para ejecutar un servidor independiente como prueba de concepto, pero probablemente no será suficiente para instalaciones grandes. Existen numerosas opciones de configuración para Kafka que controlan todos los aspectos de la configuración y la afinación. Sin embargo, la mayoría de las opciones pueden quedarse en los ajustes por defecto, ya que tratan aspectos de ajuste del broker Kafka que no serán aplicables hasta que tengas un caso de uso específico que requiera ajustar estos ajustes.

## Parámetros del corredor general

Hay varios parámetros de configuración del broker que deben revisarse al desplegar Kafka para cualquier entorno que no sea un broker independiente en un solo servidor. Estos parámetros se refieren a la configuración básica del broker, y la mayoría deben modificarse para funcionar correctamente en un clúster con otros brokers.

### broker.id

Todo broker de Kafka debe tener un identificador entero, que se establece usando la configuración. Por defecto, este entero se establece en , pero puede ser cualquier valor. Es esencial que el entero sea único para cada broker dentro de un único clúster Kafka. La selección de este número es técnicamente arbitraria y puede moverse entre corredores si es necesario para tareas de mantenimiento. Sin embargo, se recomienda encarecidamente establecer este valor a algo intrínseco al host para que, al realizar el mantenimiento, no sea complicado asignar números de ID del broker a los hosts. Por ejemplo, si tus nombres de host contienen un número único (como , , etc.), entonces y serían buenas opciones para los valores, respectivamente.`broker.id``0``host1.example.com``host2.example.com``1``2``broker.id`

### oyentes

Las versiones antiguas de Kafka usaban una configuración sencilla. Esto aún puede usarse como respaldo para configuraciones simples, pero es una configuración obsoleta. El archivo de configuración de ejemplo inicia Kafka con un oyente en el puerto TCP 9092. La nueva configuración es una lista separada por comas de URIs en la que escuchamos junto con los nombres de los oyentes. Si el nombre del oyente no es un protocolo de seguridad común, entonces también debe configurarse otro `oyente de configuración, security.protocol.map`. Un oyente se define como . Un ejemplo de configuración legal es . Especificar el nombre de host como se vinculará a todas las interfaces. Dejar el nombre del host vacío lo vinculará a la interfaz predeterminada. Ten en cuenta que si eliges un puerto inferior a 1024, Kafka debe empezar como raíz. Ejecutar Kafka como root no es una configuración recomendada.`port``listeners``_<protocol>://<hostname>:<port>_``listener``PLAINTEXT://localhost:9092,SSL://:9091``0.0.0.0`

### zookeeper.connect

La ubicación del ZooKeeper utilizado para almacenar los metadatos del broker se establece usando el parámetro de configuración. La configuración de ejemplo utiliza un ZooKeeper que se ejecuta en el puerto 2181 del host local, que se especifica como . El formato de este parámetro es una lista de cadenas separadas por punto y coma, que incluyen:`zookeeper.connect``localhost:2181``hostname:port/path`

- `hostname`

	El nombre de host o dirección IP del servidor ZooKeeper.

- `port`

	El número de puerto del cliente para el servidor.

- `/path`

	Una ruta opcional de ZooKeeper para usar como entorno chroot para el clúster Kafka. Si se omite, se utiliza el camino raíz.

Si se especifica una ruta chroot (una ruta designada para actuar como directorio raíz para una aplicación dada) y no existe, será creada por el broker al iniciar.

# ¿Por qué usar un camino de Chroot?

Generalmente se considera buena práctica usar una ruta chroot para el clúster de Kafka. Esto permite compartir el conjunto ZooKeeper con otras aplicaciones, incluidos otros clústeres de Kafka, sin conflicto. También es mejor especificar múltiples servidores ZooKeeper (que forman parte del mismo conjunto) en esta configuración. Esto permite que el broker Kafka se conecte con otro miembro del conjunto ZooKeeper en caso de fallo del servidor.

### log.dirs

Kafka persiste todos los mensajes en disco, y estos segmentos de registro se almacenan en el directorio especificado en la configuración. Para varios directorios, la configuración es preferible. Si este valor no está fijado, volverá a ser . es una lista separada por comas de caminos en el sistema local. Si se especifica más de un camino, el intermediario almacenará las particiones en ellas de forma "menos utilizada", almacenando los segmentos logarítmicos de una partición dentro del mismo camino. Ten en cuenta que el broker colocará una nueva partición en el camino que tenga el menor número de particiones almacenadas actualmente, no la menor cantidad de espacio en disco utilizado, por lo que no está garantizada una distribución uniforme de los datos entre múltiples directorios.`log.dir``log.dirs``log.dir``log.dirs`

### num.recovery.threads.per.data.dir

Kafka utiliza un conjunto configurable de hilos para manejar segmentos de log. Actualmente, se utiliza este pool de hilos:

- Al iniciar normalmente, para abrir los segmentos logarítmicos de cada partición
    
- Al iniciar tras un fallo, comprobar y truncar los segmentos logarítmicos de cada partición
    
- Al apagarse, cerrar limpiamente los segmentos de tronco
    

Por defecto, solo se utiliza un hilo por directorio de registro. Como estos hilos solo se usan durante el arranque y el apagado, es razonable establecer un mayor número de hilos para paralelizar las operaciones. Específicamente, cuando se recupera de un paro poco limpio, esto puede suponer la diferencia de varias horas al reiniciar un bróker con un gran número de particiones. Al establecer este parámetro, recuerda que el número configurado es por directorio de registro especificado con . Esto significa que si está configurado en 8 y hay 3 rutas especificadas en `log.dirs`, esto equivale a un total de 24 hilos.`log.dirs``num.​recov⁠ery.threads.per.data.dir`

### auto.create.topics.enable

La configuración predeterminada de Kafka especifica que el corredor debe crear automáticamente un tema bajo las siguientes circunstancias:

- Cuando un productor empieza a escribir mensajes sobre el tema
    
- Cuando un consumidor empieza a leer mensajes del tema
    
- Cuando algún cliente solicita metadatos para el tema
    

En muchas situaciones, esto puede ser un comportamiento indeseable, especialmente porque no hay forma de validar la existencia de un tema mediante el protocolo Kafka sin provocar que se cree. Si gestionas la creación de temas explícitamente, ya sea manualmente o a través de un sistema de provisionamiento, puedes establecer la configuración como .`auto.create.topics.enable``false`

### auto.leader.rebalance.enable

Para asegurar que un clúster Kafka no se desequilibre al tener todo el liderazgo de los temas en un solo broker, esta configuración puede especificarse para garantizar que el liderazgo esté equilibrado tanto como sea posible. Permite un hilo de fondo que comprueba la distribución de particiones a intervalos regulares (este intervalo se puede configurar mediante ). Si el desequilibrio de liderazgo supera otra configuración, , entonces se inicia un reequilibrio de líderes preferidos para las particiones.`leader.​imbal⁠ance.check.interval.seconds``leader.imbalance.per.broker.percentage`

### delete.topic.enable

Dependiendo de tu entorno y de las directrices de retención de datos, puede que quieras bloquear un clúster para evitar eliminaciones arbitrarias de temas. Desactivar la eliminación de temas se puede establecer esta bandera en .`false`

## Temas predeterminados

La configuración del servidor Kafka especifica muchas configuraciones predeterminadas para los temas que se crean. Varios de estos parámetros, incluyendo el recuento de particiones y la retención de mensajes, pueden establecerse por tema utilizando las herramientas administrativas (tratadas en [el Capítulo 12](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch12.html#administering_kafka)). Los valores predeterminados en la configuración del servidor deben establecerse en valores base apropiados para la mayoría de los temas del clúster.

# Uso de anulaciones por tema

En versiones anteriores de Kafka, era posible especificar sobreescrituras por tema para estas configuraciones en la configuración del broker usando los parámetros `log.retention.hours.per.topic`, , y . Estos parámetros ya no son compatibles y las anulaciones deben especificarse usando las herramientas administrativas.`log.reten⁠tion.​bytes.per.topic``log.segment.bytes.per.topic`

### num.particiones

El parámetro determina cuántas particiones se crea un nuevo tema, principalmente cuando la creación automática de temas está habilitada (que es la configuración predeterminada). Este parámetro se asigna por defecto a una partición. Ten en cuenta que el número de particiones para un tema solo puede aumentarse, nunca disminuir. Esto significa que si un tema necesita tener menos particiones que , habrá que tener cuidado de crear manualmente el tema (discutido en [el capítulo 12](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch12.html#administering_kafka)).`num.partitions``num.partitions`

Como se describe en [el Capítulo 1](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch01.html#meet_kafka), las particiones son la forma en que se escala un tema dentro de un clúster Kafka, lo que hace importante usar conteos de particiones que equilibren la carga de mensajes en todo el clúster a medida que se añaden intermediarios. Muchos usuarios tienen el recuento de particiones de un tema igual o múltiplo del número de brokers en el clúster. Esto permite que las particiones se distribuyan uniformemente entre los brokers, lo que repartirá la carga de mensajes de manera equitativa. Por ejemplo, un tema con 10 particiones operando en un clúster Kafka con 10 hosts y liderazgo equilibrado entre los 10 hosts tendrá un rendimiento óptimo. Sin embargo, esto no es un requisito, ya que también puedes equilibrar la carga de mensajes de otras formas, como tener varios temas.

##### Cómo elegir el número de particiones

Hay varios factores a tener en cuenta al elegir el número de particiones:

- ¿Cuál es el rendimiento que esperas lograr para el tema? Por ejemplo, ¿esperas escribir a 100 KBps o 1 GBps?
    
- ¿Cuál es el rendimiento máximo que esperas alcanzar al consumir desde una sola partición? Una partición siempre será consumida completamente por un solo consumidor (incluso cuando no se usan grupos de consumidores, el consumidor debe leer todos los mensajes de la partición). Si sabes que tu consumidor más lento escribe los datos en una base de datos y esta base nunca gestiona más de 50 MBps de cada hilo que escribe, entonces sabes que estás limitado a 50 MBps de rendimiento al consumir desde una partición.
    
- Puedes hacer el mismo ejercicio para estimar el rendimiento máximo por productor para una sola partición, pero dado que los productores suelen ser mucho más rápidos que los consumidores, normalmente es seguro saltarse esto.
    
- Si envías mensajes a particiones basadas en claves, añadir particiones más adelante puede ser muy complicado, así que calcula el rendimiento basándote en tu uso futuro esperado, no en el uso actual.
    
- Considera el número de particiones que colocarás en cada broker y el espacio en disco y ancho de banda de red disponibles por intermediario.
    
- Evita sobreestimar, ya que cada partición utiliza memoria y otros recursos en el broker y aumentará el tiempo para las actualizaciones de metadatos y transferencias de liderazgo.
    
- ¿Vas a reflejar datos? Puede que también tengas que considerar el rendimiento de tu configuración de espejado. Las grandes particiones pueden convertirse en un cuello de botella en muchas configuraciones de espejo.
    
- Si usas servicios en la nube, ¿tienes limitaciones de IOPS (operaciones de entrada/salida por segundo) en tus máquinas virtuales o discos? Puede haber límites estrictos en el número de IOPS permitidos dependiendo de tu servicio en la nube y la configuración de la máquina virtual que te harán cumplir cuotas. Tener demasiadas particiones puede tener el efecto secundario de aumentar la cantidad de IOPS debido al paralelismo involucrado.
    

Con todo esto en mente, está claro que quieres muchas particiones, pero no demasiadas. Si tienes alguna estimación sobre el rendimiento objetivo del tema y el rendimiento esperado de los consumidores, puedes dividir el rendimiento objetivo entre el rendimiento esperado del consumidor y derivar el número de particiones de esta manera. Así que si queremos poder escribir y leer 1 GBps de un tema, y sabemos que cada consumidor solo puede procesar 50 MBps, entonces sabemos que necesitamos al menos 20 particiones. De este modo, podemos tener 20 consumidores leyendo el tema y alcanzar 1 GBps.

Si no tienes esta información detallada, nuestra experiencia sugiere que limitar el tamaño de la partición del disco a menos de 6 GB por día de retención suele dar resultados satisfactorios. Empezar poco a poco y expandirse según sea necesario es más fácil que empezar demasiado grande.

### factor.replicación.por defecto

Si se habilita la creación automática de tópicos, esta configuración establece cuál debe ser el factor de replicación para nuevos temas. La estrategia de replicación puede variar según la durabilidad o disponibilidad deseada de un clúster y se tratará más en capítulos posteriores. A continuación se presenta una breve recomendación si ejecutas Kafka en un clúster que evitará cortes por factores ajenos a las capacidades internas de Kafka, como fallos de hardware.

Se recomienda encarecidamente establecer el factor de replicación al menos 1 por encima del ajuste. Para configuraciones más resistentes a fallos, si tienes clústeres lo suficientemente grandes y suficiente hardware, puede ser preferible poner tu factor de replicación en 2 por encima de (abreviado como RF++). RF++ permitirá un mantenimiento más sencillo y evitará cortes. La razón detrás de esta recomendación es permitir que ocurra simultáneamente una interrupción planificada dentro del conjunto réplica y una interrupción no planificada. Para un clúster típico, esto significaría que tendrías un mínimo de tres réplicas de cada partición. Un ejemplo de esto es si hay una caída del switch de red, fallo en el disco u otro problema no planificado durante un despliegue o actualización continua de Kafka o del sistema operativo subyacente, puedes estar seguro de que aún habrá una réplica adicional disponible. Esto se tratará más en [el capítulo 7](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch07.html#reliable_data_delivery).`min.insync.replicas``min.insync.replicas`

### log.retention.ms

La configuración más común para cuánto tiempo Kafka retendrá los mensajes es por tiempo. El valor por defecto se especifica en el archivo de configuración usando el parámetro, y se establece en 168 horas, o una semana. Sin embargo, hay otros dos parámetros permitidos, y . Los tres controlan el mismo objetivo (el tiempo tras el cual los mensajes pueden ser eliminados), pero el parámetro recomendado es , ya que el tamaño de unidad menor tendrá prioridad si se especifican más de uno. Esto asegurará que el conjunto de valores para sea siempre el que se utilize. Si se especifican más de uno, el tamaño de unidad más pequeño tendrá prioridad.`log.retention.hours``log.retention.minutes``log.retention.ms``log.retention.ms``log.retention.ms`

# Retención por tiempo y tiempos de última modificación

La retención por tiempo se realiza examinando el último tiempo modificado (mtime) en cada archivo de segmento de registro en disco. Bajo operaciones normales de clúster, este es el momento en que se cerró el segmento de registro y representa la marca de tiempo del último mensaje del archivo. Sin embargo, al usar herramientas administrativas para mover particiones entre intermediarios, este tiempo no es preciso y resultará en una retención excesiva de dichas particiones. Para más información sobre esto, véase [el capítulo 12](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch12.html#administering_kafka) sobre los movimientos de partición.

### log.retention.bytes

Otra forma de caducar mensajes es basándose en el número total de bytes de mensajes retenidos. Este valor se establece usando el parámetro, y se aplica por partición. Esto significa que si tienes un tema con 8 particiones y está configurado en 1 GB, la cantidad de datos retenidos para el tema será como máximo 8 GB. Ten en cuenta que toda la retención se realiza para particiones individuales, no para el tema. Esto significa que si se amplía el número de particiones de un tema, la retención también aumentará si se utiliza. Establecer el valor en –1 permitirá una retención infinita.`log.retention.bytes``log.retention.bytes``log.retention.bytes`

# Configuración de la retención por tamaño y tiempo

Si has especificado un valor para ambos y (u otro parámetro para la retención por tiempo), los mensajes pueden eliminarse cuando se cumpla cualquiera de los criterios. Por ejemplo, si está configurado en 864000000 (1 día) y en 1000000000 (1 GB), es posible que se eliminen mensajes con menos de 1 día si el volumen total de mensajes a lo largo del día es mayor a 1 GB. Por el contrario, si el volumen es inferior a 1 GB, los mensajes pueden eliminarse tras 1 día incluso si el tamaño total de la partición es inferior a 1 GB. Se recomienda, para simplificar, elegir la retención basada en tamaño o en tiempo—y no ambos—para evitar sorpresas y pérdidas no deseadas de datos, pero ambos pueden usarse para configuraciones más avanzadas.`log.retention.bytes``log.retention.ms``log.retention.ms``log.​reten⁠tion.bytes`

### log.segment.bytes

Las configuraciones de retención de registros mencionadas anteriormente funcionan sobre segmentos de registro, no sobre mensajes individuales. A medida que se producen mensajes al intermediario Kafka, se añaden al segmento de registro actual para la partición. Una vez que el segmento logarítrico ha alcanzado el tamaño especificado por el parámetro, que por defecto es 1 GB, el segmento logarítmic se cierra y se abre uno nuevo. Una vez que se ha cerrado un segmento de log, puede considerarse como caducidad. Un tamaño de segmento de registro más pequeño significa que los archivos deben cerrarse y asignarse con más frecuencia, lo que reduce la eficiencia general de las escrituras en disco.`log.segment.bytes`

Ajustar el tamaño de los segmentos de tronco puede ser importante si los temas tienen una baja tasa de producción. Por ejemplo, si un tema recibe solo 100 megabytes diarios de mensajes y está configurado por defecto, tardará 10 días en llenar un segmento. Como los mensajes no pueden expirar hasta que se cierre el segmento de registro, si se establece en 604800000 (1 semana), en realidad habrá hasta 17 días de mensajes retenidos hasta que expire el segmento cerrado. Esto se debe a que, una vez que el segmento de registro se cierra con los 10 días actuales de mensajes, ese segmento debe conservarse durante 7 días antes de expirar según la política de tiempo (ya que el segmento no puede eliminarse hasta que el último mensaje del segmento pueda expirar).`log.segment.bytes``log.retention.ms`

# Recuperación de desplazamientos por marca temporal

El tamaño del segmento logarítmico también afecta al comportamiento de captar desplazamientos por marca temporal. Al solicitar desplazamientos para una partición en una marca de tiempo específica, Kafka encuentra el archivo de segmento de registro que se estaba escribiendo en ese momento. Lo hace utilizando la hora de creación y última modificación del archivo, y buscando un archivo que se haya creado antes de la marca de tiempo especificada y que haya sido modificado por última vez después de la marca de tiempo. El desplazamiento al inicio de ese segmento de registro (que también es el nombre del archivo) se devuelve en la respuesta.

### log.roll.ms

Otra forma de controlar cuándo se cierran los segmentos logarítmicos es usando el parámetro, que especifica el tiempo tras el cual debe cerrarse un segmento logarítmico. Como con los parámetros y y no son propiedades mutuamente excluyentes. Kafka cerrará un segmento logarítmico ya sea cuando se alcance el límite de tamaño o cuando se alcance el límite de tiempo, lo que ocurra primero. Por defecto, no hay una opción para , lo que solo permite cerrar segmentos logarítmicos por tamaño.`log.roll.ms``log.retention.bytes``log.retention.ms``log.segment.bytes``log.roll.ms``log.roll.ms`

# Rendimiento del disco al usar segmentos basados en el tiempo

Al utilizar un límite de segmentos logarítmicos basado en tiempo, es importante considerar el impacto en el rendimiento del disco cuando se cierran varios segmentos logarítmicos simultáneamente. Esto puede ocurrir cuando hay muchas particiones que nunca alcanzan el límite de tamaño para segmentos logarítmicos, ya que el reloj del límite de tiempo comenzará cuando el broker inicia y siempre se ejecutará al mismo tiempo para estas particiones de bajo volumen.

### min.insync.replicas

Al configurar tu clúster para la durabilidad de los datos, poner en 2 asegura que al menos dos réplicas estén al día y "sincronizadas" con el productor. Esto se usa junto con configurar la configuración del productor para que intercepte "todas" las peticiones. Esto asegurará que al menos dos réplicas (líder y una otra) reconozcan una escritura para que tenga éxito. Esto puede evitar la pérdida de datos en situaciones donde el líder ackya una escritura, luego sufre un fallo y el liderazgo se transfiere a una réplica que no tiene una escritura exitosa. Sin estos ajustes duraderos, el productor pensaría que se produjo con éxito y el(los) mensaje(s) caerían al suelo y se perderían. Sin embargo, configurar para mayor durabilidad tiene el efecto secundario de ser menos eficiente debido a la sobrecarga adicional, por lo que no se recomienda clústeres con alto rendimiento que toleran pérdida ocasional de mensajes para cambiar esta configuración desde el valor por defecto de 1. Consulta [el capítulo 7](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch07.html#reliable_data_delivery) para más información.`min.insync.replicas`

### message.max.bytes

El broker Kafka limita el tamaño máximo de un mensaje que puede producirse, configurado por el parámetro, que por defecto es 1000000, o 1 MB. Un productor que intente enviar un mensaje mayor que este recibirá un error del broker, y el mensaje no será aceptado. Como ocurre con todos los tamaños de byte especificados en el broker, esta configuración se encarga del tamaño comprimido del mensaje, lo que significa que los productores pueden enviar mensajes mucho mayores que este valor sin comprimir, siempre que se compriman por debajo del tamaño configurado.`message.max.bytes``message.max.bytes`

Hay impactos notables en el rendimiento al aumentar el tamaño permitido del mensaje. Los mensajes más grandes significarán que los hilos intermediarios que se encargan del procesamiento de conexiones y solicitudes de red trabajarán más tiempo en cada solicitud. Los mensajes más grandes también aumentan el tamaño de las escrituras en disco, lo que afectará al rendimiento de E/S. Otras soluciones de almacenamiento, como almacenes blob y/o almacenamiento por niveles, pueden ser otro método para abordar problemas de escritura en discos grandes, pero no se tratarán en este capítulo.

# Coordinación de configuraciones de tamaño de mensaje

El tamaño del mensaje configurado en el broker Kafka debe coordinarse con la configuración de los clientes consumidores. Si este valor es menor que , entonces los consumidores que se encuentran con mensajes más grandes no podrán acceder a esos mensajes, lo que resultará en una situación en la que el consumidor se queda atascado y no podrá continuar. La misma regla se aplica a la configuración `de replica.fetch.max.bytes` en los brokers cuando están configurados en un clúster.`fetch.message.max.bytes``message.max.bytes`

# Selección de hardware

Seleccionar una configuración de hardware adecuada para un corredor Kafka puede ser más arte que ciencia. Kafka en sí no tiene un requisito estricto sobre una configuración de hardware específica y funcionará sin problemas en la mayoría de los sistemas. Sin embargo, una vez que el rendimiento se convierte en una preocupación, existen varios factores que pueden contribuir a los cuellos de botella generales en el rendimiento: el rendimiento y la capacidad del disco, la memoria, la red y la CPU. Al escalar Kafka en gran tamaño, también puede haber restricciones en el número de particiones que un solo intermediario puede manejar debido a la cantidad de metadatos que necesitan actualizarse. Una vez que hayas determinado qué tipos de rendimiento son los más críticos para tu entorno, puedes seleccionar una configuración de hardware optimizada adecuada a tu presupuesto.

## Rendimiento de disco

El rendimiento de los clientes productores estará más directamente influenciado por el rendimiento del disco broker que se utiliza para almacenar segmentos de log. Los mensajes Kafka deben ser almacenados localmente cuando se producen, y la mayoría de los clientes esperarán hasta que al menos un intermediario haya confirmado que los mensajes han sido comprometidos antes de considerar el envío exitoso. Esto significa que escrituras más rápidas en disco resultarán en menor latencia.

La decisión obvia en cuanto al rendimiento del disco es si usar discos duros giratorios tradicionales (HDD) o discos de estado sólido (SSD). Los SSD tienen tiempos de búsqueda y acceso drásticamente más bajos y ofrecen el mejor rendimiento. Los HDD, en cambio, son más económicos y proporcionan más capacidad por unidad. También puedes mejorar el rendimiento de los discos duros usando más en un broker, ya sea teniendo varios directorios de datos o configurando los discos en una configuración RAID (array redundante de discos independientes). Otros factores, como la tecnología específica de la unidad (por ejemplo, almacenamiento conectado en serie o ATA serie), así como la calidad del controlador de unidad, afectarán al rendimiento. En general, las observaciones muestran que los discos duros suelen ser más útiles para clústeres con necesidades de almacenamiento muy elevadas pero no se acceden tan a menudo, mientras que los SSD son mejores opciones si hay un número muy grande de conexiones cliente.

## Capacidad del disco

La capacidad es la otra cara de la discusión sobre el almacenamiento. La cantidad de capacidad del disco necesaria está determinada por cuántos mensajes deben retenerse en cada momento. Si se espera que el broker reciba 1 TB de tráfico cada día, con 7 días de retención, entonces necesitará un mínimo de 7 TB de almacenamiento utilizable para segmentos de registro. También deberías tener en cuenta al menos un 10% de sobrecarga para otros archivos, además de cualquier buffer que quieras mantener para fluctuaciones de tráfico o crecimiento a lo largo del tiempo.

La capacidad de almacenamiento es uno de los factores a considerar al dimensionar un clúster Kafka y decidir cuándo expandirlo. El tráfico total de un clúster puede equilibrarse entre el clúster teniendo múltiples particiones por tema, lo que permitirá que brokers adicionales aumenten la capacidad disponible si la densidad en un solo broker no es suficiente. La decisión sobre cuánta capacidad de disco se necesita también estará informada por la estrategia de replicación elegida para el clúster (que se discute con más detalle en [el Capítulo 7](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch07.html#reliable_data_delivery)).

## Memoria

El modo normal de funcionamiento para un consumidor Kafka es leer desde el final de las particiones, donde el consumidor queda al día y queda muy poco o nada por detrás de los productores. En esta situación, los mensajes que el consumidor está leyendo se almacenan óptimamente en la caché de páginas del sistema, lo que resulta en lecturas más rápidas que si el broker tiene que releer los mensajes del disco. Por lo tanto, disponer de más memoria para la caché de página mejorará el rendimiento de los clientes de consumo.

Kafka en sí no necesita mucha memoria heap configurada para la Máquina Virtual Java (JVM). Incluso un broker que gestiona 150.000 mensajes por segundo y una tasa de datos de 200 megabits por segundo puede funcionar con un heap de 5 GB. El resto de la memoria del sistema será utilizada por la caché de páginas y beneficiará a Kafka al permitir que el sistema almacene en caché los segmentos de registro en uso. Esta es la razón principal por la que no se recomienda colocar Kafka en un sistema con ninguna otra aplicación significativa, ya que tendría que compartir el uso de la caché de páginas. Esto disminuirá el rendimiento del consumidor para Kafka.

## Networking

El rendimiento de red disponible especificará la cantidad máxima de tráfico que Kafka puede manejar. Esto puede ser un factor determinante, combinado con el almacenamiento en disco, para el tamaño del clúster. Esto se complica por el desequilibrio inherente entre el uso de red entrante y saliente que se crea por el soporte de Kafka para múltiples consumidores. Un productor puede escribir 1 MB por segundo para un tema dado, pero puede haber cualquier número de consumidores que creen un multiplicador en el uso de la red saliente. Otras operaciones, como la replicación de clústeres (tratada en [el Capítulo 7](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch07.html#reliable_data_delivery)) y el espejado (discutido en [el Capítulo 10](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch10.html#cross_cluster_mirroring)), también aumentarán los requisitos. Si la interfaz de red se satura, no es raro que la replicación del clúster se retrase, lo que puede dejar al clúster en un estado vulnerable. Para evitar que la red sea un factor regulador importante, se recomienda utilizar al menos tarjetas de red (NIC) de 10 Gb. Las máquinas antiguas con tarjetas de 1 Gb se saturan fácilmente y no se recomiendan.

## CPU

La potencia de procesamiento no es tan importante como el disco y la memoria hasta que empieces a escalar Kafka a gran escala, pero afectará en cierta medida al rendimiento general del broker. Idealmente, los clientes deberían comprimir los mensajes para optimizar el uso de la red y del disco. Sin embargo, el broker Kafka debe descomprimir todos los lotes de mensajes para validar los mensajes individuales y asignar desplazamientos. Luego necesita recomprimir el lote del mensaje para almacenarlo en disco. De ahí proviene la mayor parte de la necesidad de potencia de procesamiento de Kafka. Sin embargo, este no debería ser el factor principal a la hora de seleccionar el hardware, a menos que los clústeres se hagan muy grandes, con cientos de nodos y millones de particiones en un solo clúster. En ese momento, seleccionar CPUs más eficientes puede ayudar a reducir el tamaño de los clústeres.`checksum`

# Kafka en la Nube

En los últimos años, una instalación más común de Kafka es en entornos de computación en la nube, como Microsoft Azure, AWS de Amazon o Google Cloud Platform. Hay muchas opciones para configurar Kafka en la nube y gestionarlo por ti a través de proveedores como Confluent o incluso a través del propio Kafka de Azure en HDInsight, pero los siguientes van algunos consejos sencillos si planeas gestionar manualmente tus propios clústeres Kafka. En la mayoría de entornos en la nube, tienes una selección de muchas instancias de cómputo, cada una con una combinación diferente de CPU, memoria, IOPS y disco. Las distintas características de rendimiento de Kafka deben priorizarse para poder seleccionar la configuración correcta de instancias a utilizar.

## Microsoft Azure

En Azure, puedes gestionar los discos por separado de la máquina virtual (VM), por lo que decidir tus necesidades de almacenamiento no tiene por qué estar relacionado con el tipo de VM seleccionado. Dicho esto, un buen punto de partida para tomar decisiones es la cantidad de retención de datos requerida, seguida del rendimiento que requieren los productores. Si es necesaria una latencia muy baja, podrían ser necesarias instancias optimizadas para E/S que utilicen almacenamiento SSD premium. De lo contrario, las opciones de almacenamiento gestionado (como los Azure Managed Disks o Azure Blob Storage) podrían ser suficientes.

En términos reales, la experiencia en Azure muestra que los tipos de instancias son una buena opción para clústeres pequeños y son lo suficientemente eficientes para la mayoría de los casos de uso. Para adaptarse a las necesidades de hardware y CPU de alto rendimiento, las instancias tienen un buen rendimiento que puede escalar para clústeres más grandes. Se recomienda construir tu clúster en un conjunto de disponibilidad de Azure y balancear las particiones entre dominios de fallos de cálculo de Azure para asegurar la disponibilidad. Una vez que tengas una máquina virtual elegida, puede venir decidir los tipos de almacenamiento. Se recomienda encarecidamente utilizar Azure Managed Disks en lugar de discos efímeros. Si se mueve una VM, corres el riesgo de perder todos los datos de tu broker Kafka. Los discos gestionados HDD son relativamente económicos, pero no cuentan con SLA claramente definidos por Microsoft en cuanto a disponibilidad. Los SSD premium o configuraciones Ultra SSD son mucho más caros, pero mucho más rápidos y están bien soportados con un 99,99% de SLA de Microsoft. Alternativamente, usar Microsoft Blob Storage es una opción si no eres tan sensible a la latencia.`Standard D16s v3``D64s v4`

## Amazon Web Services

En AWS, si se necesita una latencia muy baja, pueden ser necesarias instancias optimizadas para E/S que tengan almacenamiento local en SSD. De lo contrario, el almacenamiento efímero (como la tienda Amazon Elastic Block) podría ser suficiente.

Una opción común en AWS son los tipos de instancia de o. Esto permitirá períodos de retención más largos, pero el rendimiento al disco será menor porque está en almacenamiento elástico por bloques. La instancia tendrá un rendimiento mucho mejor con discos SSD locales, pero esos discos limitarán la cantidad de datos que se pueden conservar. Para lo mejor de ambos mundos, puede ser necesario pasar a los tipos de instancia o o, pero son significativamente más caros.`m4``r3``m4``r3``i2``d2`

# Configuración de clústeres de Kafka

Un solo broker Kafka funciona bien para trabajos de desarrollo local o para un sistema de prueba de concepto, pero hay beneficios significativos en tener múltiples brokers configurados como un clúster, como se muestra en [la Figura 2-2](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch02.html#fig-2-cluster). El mayor beneficio es la posibilidad de escalar la carga entre varios servidores. Un segundo lugar cercano es el uso de la replicación para evitar la pérdida de datos debido a fallos individuales del sistema. La replicación también permitirá realizar trabajos de mantenimiento en Kafka o en los sistemas subyacentes, manteniendo la disponibilidad para los clientes. Esta sección se centra en los pasos para configurar un clúster básico de Kafka. El [capítulo 7](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch07.html#reliable_data_delivery) contiene más información sobre la replicación de datos y la durabilidad.

![[../../../assets/Pasted image 20260522213911.png]]
Figura 2-2. Un simple cúmulo de Kafka

## ¿Cuántos corredores?

El tamaño adecuado para un cúmulo de Kafka está determinado por varios factores. Normalmente, el tamaño de tu clúster estará limitado a las siguientes áreas clave:

- Capacidad del disco
    
- Capacidad de réplica por intermediario
    
- Capacidad de la CPU
    
- Capacidad de la red
    

El primer factor a considerar es cuánta capacidad de disco se requiere para retener mensajes y cuánto almacenamiento hay disponible en un único intermediario. Si el clúster debe conservar 10 TB de datos y un solo broker puede almacenar 2 TB, entonces el tamaño mínimo del clúster es de 5 brokers. Además, aumentar el factor de replicación incrementará los requisitos de almacenamiento al menos un 100%, dependiendo del ajuste del factor de replicación elegido (véase [el Capítulo 7](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch07.html#reliable_data_delivery)). En este caso, las réplicas se refieren al número de brokers diferentes a los que se copia una sola partición. Esto significa que este mismo clúster, configurado con una replicación de 2, ahora necesita contener al menos 10 brokers.

El otro factor a considerar es la capacidad del clúster para gestionar solicitudes. Esto puede manifestarse en los otros tres cuellos de botella mencionados anteriormente.

Si tienes un clúster Kafka de 10 brokers pero más de 1 millón de réplicas (es decir, 500.000 particiones con un factor de replicación de 2) en tu clúster, cada broker está asumiendo aproximadamente 100.000 réplicas en un escenario equilibrado. Esto puede provocar cuellos de botella en las colas de productos frescos, consumidores y controladores. En el pasado, las recomendaciones oficiales han sido no tener más de 4.000 réplicas de partición por intermediario y no más de 200.000 réplicas de partición por clúster. Sin embargo, los avances en la eficiencia de los clústeres han permitido a Kafka escalar mucho más. Actualmente, en un entorno bien configurado, se recomienda no tener más de 14.000 réplicas de partición por broker ni 1 millón de _réplicas_ por clúster.

Como se mencionó anteriormente en este capítulo, la CPU normalmente no es un cuello de botella importante en la mayoría de los casos de uso, pero puede serlo si hay una cantidad excesiva de conexiones y solicitudes de clientes en un broker. Vigilar el uso general de CPU en función de cuántos clientes y grupos de consumidores únicos existen, y ampliar para cubrir esas necesidades, puede ayudar a garantizar un mejor rendimiento global en grandes clústeres. Hablando de la capacidad de red, es importante tener en cuenta la capacidad de las interfaces de red y si pueden gestionar el tráfico cliente si hay múltiples consumidores de datos o si el tráfico no es consistente durante el periodo de retención de los datos (por ejemplo, ráfagas de tráfico durante las horas punta). Si la interfaz de red de un solo broker se utiliza al 80% de su capacidad en el pico, y hay dos consumidores de esos datos, los consumidores no podrán seguir el ritmo del tráfico pico a menos que haya dos brokers. Si se utiliza replicación en el clúster, este es un consumidor adicional de los datos que debe tenerse en cuenta. También puede que quieras escalar a más brokers en un clúster para gestionar las preocupaciones de rendimiento causadas por un menor rendimiento de disco o memoria del sistema disponible.

## Configuración del Broker

Solo hay dos requisitos en la configuración del broker para permitir que varios brokers Kafka se unan a un solo clúster. La primera es que todos los corredores deben tener la misma configuración para el parámetro. Esto especifica el conjunto y la ruta de ZooKeeper donde el clúster almacena los metadatos. El segundo requisito es que todos los brokers del clúster tengan un valor único para el parámetro. Si dos brokers intentan unirse al mismo clúster con el mismo , el segundo broker registrará un error y no podrá iniciarse. Existen otros parámetros de configuración utilizados al ejecutar un clúster—específicamente, parámetros que controlan la replicación, que se abordan en capítulos posteriores.`zookeeper.connect``broker.id``broker.id`

## Ajuste del sistema operativo

Aunque la mayoría de las distribuciones Linux tienen una configuración lista para los parámetros de ajuste del kernel que funcionará bastante bien para la mayoría de aplicaciones, hay algunos cambios que se pueden hacer para un broker Kafka que mejorarán el rendimiento. Estos giran principalmente en torno a la memoria virtual y los subsistemas de red, así como preocupaciones específicas sobre el punto de montaje del disco utilizado para almacenar segmentos de registro. Estos parámetros suelen configurarse en el archivo _/etc/sysctl.conf_, pero deberías consultar la documentación de tu distribución Linux para detalles específicos sobre cómo ajustar la configuración del kernel.

### Memoria virtual

En general, el sistema de memoria virtual de Linux se ajusta automáticamente a la carga de trabajo del sistema. Podemos hacer algunos ajustes en cómo se gestiona el espacio de swap, así como en páginas de memoria sucias, para ajustarlas a la carga de trabajo de Kafka.

Como en la mayoría de las aplicaciones, especialmente aquellas donde el rendimiento es un problema, es mejor evitar el intercambio a (casi) toda costa. El coste que implica cambiar páginas de memoria a disco se reflejará en un impacto notable en todos los aspectos del rendimiento en Kafka. Además, Kafka hace un uso intensivo de la caché de páginas del sistema, y si el sistema de máquinas virtuales cambia a disco, no se asigna suficiente memoria a la caché de páginas.

Una forma de evitar el intercambio es simplemente no configurar ningún espacio de swap. Tener swap no es un requisito, pero sí proporciona una red de seguridad si ocurre algo catastrófico en el sistema. Tener swap puede evitar que el sistema operativo cancele abruptamente un proceso debido a una condición de falta de memoria. Por esta razón, la recomendación es establecer el parámetro en un valor muy bajo, como 1. El parámetro es un porcentaje de la probabilidad de que el subsistema de la VM use espacio de intercambio en lugar de eliminar páginas de la caché de páginas. Es preferible reducir la cantidad de memoria disponible para la caché de páginas en lugar de utilizar cualquier cantidad de memoria de swap.`vm.swappiness`

# ¿Por qué no poner la inmutabilidad a cero?

Antes, la recomendación siempre era ponerlo en 0. Este valor solía significar "no intercambiar a menos que haya una condición de falta de memoria." Sin embargo, el significado de este valor cambió a partir de la versión 3.5-rc1 del núcleo de Linux, y ese cambio fue trasladado a muchas distribuciones, incluidos los kernels de Red Hat Enterprise Linux, a partir de la versión 2.6.32-303. Esto cambió el significado del valor 0 a "nunca intercambiar bajo ninguna circunstancia". Por eso ahora se recomienda un valor de 1.`vm.swappiness`

También hay una ventaja en ajustar cómo el kernel maneja las páginas sucias que deben ser enjuagadas al disco. Kafka depende del rendimiento de la E/S de disco para proporcionar buenos tiempos de respuesta a los productores. Esta es también la razón por la que los segmentos de registro suelen colocarse en un disco rápido, ya sea un disco individual con un tiempo de respuesta rápido (por ejemplo, un SSD) o un subsistema de disco con una cantidad significativa de NVRAM para caché (por ejemplo, RAID). El resultado es que se puede reducir el número de páginas sucias permitidas, antes de que el proceso de ensabotado en segundo plano comience a escribirlas en disco. Hazlo poniendo el valor por debajo del valor por defecto de 10. El valor es un porcentaje de la cantidad total de memoria del sistema, y fijar este valor en 5 es apropiado en muchas situaciones. Sin embargo, esta configuración no debería estar a cero, ya que haría que el kernel vaciara continuamente las páginas, eliminando así la capacidad del núcleo para almacenar en búfer las escrituras de disco frente a picos temporales en el rendimiento del dispositivo subyacente.`vm.dirty_background_ratio`

El número total de páginas sucias permitidas antes de que el kernel obligue a operaciones síncronas a vaciarlas al disco también puede incrementarse cambiando el valor de a por encima del valor por defecto de 20 (también un porcentaje de la memoria total del sistema). Hay un amplio rango de valores posibles para esta configuración, pero entre 60 y 80 es un número razonable. Esta configuración introduce un pequeño riesgo, tanto en cuanto a la cantidad de actividad del disco no vaciado como en la posibilidad de largas pausas de E/S si se forzan los enjuagues síncronos. Si se elige una configuración superior para , se recomienda encarecidamente que se utilice replicación en el clúster Kafka para evitar fallos del sistema.`vm.dirty_ratio``vm.dirty_ratio`

Al elegir valores para estos parámetros, es recomendable revisar el número de páginas sucias a lo largo del tiempo mientras el clúster de Kafka se ejecuta bajo carga, ya sea en producción o simulada. El número actual de páginas sucias se puede determinar comprobando el archivo _/proc/vmstat_:

```
# cat /proc/vmstat | egrep "dirty|writeback"
nr_dirty 21845
nr_writeback 0
nr_writeback_temp 0
nr_dirty_threshold 32715981
nr_dirty_background_threshold 2726331
#
```

Kafka utiliza descriptores de archivo para segmentos de registro y conexiones abiertas. Si un broker tiene muchas particiones, entonces necesita al _menos (number_of_partitions)_ × _(partition_size/segment_size)_ para rastrear todos los segmentos logarítmicos además del número de conexiones que hace. Por ello, se recomienda actualizar a un número muy grande basándose en el cálculo anterior. Dependiendo del entorno, cambiar este valor a 400.000 o 600.000 ha sido generalmente exitoso. También se recomienda poner en 0. Establecer el valor por defecto de 0 indica que el núcleo determina la cantidad de memoria libre de una aplicación. Si la propiedad se establece en un valor distinto de cero, podría llevar al sistema operativo a absorber demasiada memoria, privando de memoria para que Kafka funcione de forma óptima. Esto es común en aplicaciones con altas tasas de ingestión.`vm.max_map_count``vm.overcommit_memory`

### Disco

Más allá de seleccionar el hardware del dispositivo de disco, así como la configuración del RAID si se utiliza, la elección del sistema de archivos para este disco puede tener el siguiente mayor impacto en el rendimiento. Existen muchos sistemas de archivos diferentes disponibles, pero las opciones más comunes para sistemas de archivos locales son Ext4 (cuarto sistema de archivos extendido) o Extents File System (XFS). XFS se ha convertido en el sistema de archivos predeterminado para muchas distribuciones de Linux, y esto es por una buena razón: supera a Ext4 en la mayoría de las cargas de trabajo con un ajuste mínimo necesario. Ext4 puede funcionar bien pero requiere usar parámetros de ajuste considerados menos seguros. Esto incluye establecer el intervalo de compromiso a un tiempo mayor que el predeterminado de cinco para forzar descargas menos frecuentes. Ext4 también introdujo la asignación tardía de bloques, lo que conlleva una mayor probabilidad de pérdida de datos y corrupción del sistema de archivos en caso de fallo del sistema. El sistema de archivos XFS también utiliza un algoritmo de asignación retardada, pero generalmente es más seguro que el que utiliza Ext4. XFS también ofrece mejor rendimiento para la carga de trabajo de Kafka sin requerir ajuste más allá del ajuste automático realizado por el sistema de archivos. También es más eficiente al agrupar escrituras en disco, lo que se combina para ofrecer un mejor rendimiento global de E/S.

Independientemente del sistema de archivos elegido para el montaje que contiene los segmentos de log, es recomendable establecer la opción de montaje para el punto de montaje. Los metadatos del archivo contienen tres marcas de tiempo: hora de creación (), hora de última modificación () y última hora de acceso (). Por defecto, se actualiza cada vez que se lee un archivo. Esto genera un gran número de escrituras en disco. El atributo generalmente se considera de poca utilidad, a menos que una aplicación necesite saber si un archivo ha sido accedido desde la última modificación (en cuyo caso se puede usar la opción). Kafka no lo usa en absoluto, así que desactivarlo es seguro. Configurar en la montura evitará que estas actualizaciones de marca de tiempo ocurran, pero no afectará al manejo adecuado de los atributos de and. Usar esta opción también puede ayudar a mejorar la eficiencia de Kafka cuando hay escrituras de disco más grandes.`noatime``ctime``mtime``atime``atime``atime``relatime``atime``noatime``ctime``mtime``largeio`

### Networking

Ajustar la configuración predeterminada de la pila de red Linux es común en cualquier aplicación que genere una gran cantidad de tráfico de red, ya que el núcleo no está ajustado por defecto para transferencias de datos grandes y de alta velocidad. De hecho, los cambios recomendados para Kafka son los mismos que los recomendados para la mayoría de servidores web y otras aplicaciones de red. El primer ajuste consiste en cambiar la cantidad predeterminada y máxima de memoria asignada para los búferes de envío y recepción de cada socket. Esto aumentará significativamente el rendimiento para transferencias grandes. Los parámetros relevantes para el tamaño predeterminado del búfer de envío y recepción por socket son y , y una configuración razonable para estos parámetros es 131072, o 128 KiB. Los parámetros para los tamaños máximos de los búferes de envío y recepción son y , y una configuración razonable es 2097152, o 2 MiB. Ten en cuenta que el tamaño máximo no indica que cada socket tenga tanto espacio de buffer asignado; Solo permite hasta ese límite si es necesario.`net.core.wmem_default``net.core.rmem_default``net.core.wmem_max``net.core.rmem_max`

Además de la configuración de los sockets, los tamaños de búfer de envío y recepción para los sockets TCP deben establecerse por separado usando los parámetros y. Estos se establecen usando tres enteros separados por espacio que especifican los tamaños mínimo, por defecto y máximo, respectivamente. El tamaño máximo no puede ser mayor que los valores especificados para todos los zócalos que usen y . Un ejemplo de configuración para cada uno de estos parámetros es "4096 65536 2048000", que es un mínimo de 4 KiB, 64 KiB de valor por defecto y un búfer máximo de 2 MiB. Según la carga real de trabajo de tus brokers Kafka, puede que quieras aumentar los tamaños máximos para permitir un mayor buffering de las conexiones de red.`net.ipv4.tcp_wmem``net.ipv4.tcp_rmem``net.core.wmem_max``net.core.rmem_max`

Hay varios otros parámetros de ajuste de red que son útiles para establecer. Habilitar la escalada de ventanas TCP configurando a 1 permitirá a los clientes transferir datos de forma más eficiente y permitir que esos datos se almacenen en búfer en el lado del broker. Aumentar el valor de por encima del valor por defecto de 1024 permitirá aceptar un mayor número de conexiones simultáneas. Aumentar el valor de a mayor que el valor por defecto de 1000 puede ayudar con ráfagas de tráfico de red, especialmente al usar velocidades de conexión multigigabit, permitiendo que se pongan más paquetes en cola para que el núcleo los procese.`net.ipv4.tcp_window_scaling``net.ipv4.tcp_max_syn_backlog``net.core.netdev_max_backlog`

# Preocupaciones de producción

Una vez que estés listo para trasladar tu entorno Kafka de las pruebas a tus operaciones de producción, hay algunas cosas más que considerar que te ayudarán a configurar un servicio de mensajería fiable.

## Opciones de recolector de basura

Ajustar las opciones de recogida de basura en Java para una aplicación siempre ha sido un arte, requiriendo información detallada sobre cómo la aplicación utiliza la memoria y una cantidad significativa de observación y prueba y error. Por suerte, esto ha cambiado con Java 7 y la introducción del recolector de basura primero (G1GC). Aunque inicialmente se consideró inestable el G1GC, experimentó una mejora notable en JDK8 y JDK11. Ahora se recomienda que Kafka use G1GC como recolector de basura por defecto. G1GC está diseñado para ajustarse automáticamente a diferentes cargas de trabajo y proporcionar tiempos de pausa consistentes para la recogida de basura a lo largo de la vida útil de la aplicación. También maneja grandes tamaños de montones con facilidad al segmentar el montón en zonas más pequeñas y no acumular en todo el montón en cada pausa.

G1GC hace todo esto con una configuración mínima en funcionamiento normal. Existen dos opciones de configuración para G1GC que se utilizan para ajustar su rendimiento:

- `MaxGCPauseMillis`

	Esta opción especifica el tiempo de pausa preferido para cada ciclo de recogida de basura. No es un máximo fijo: G1GC puede y superará este tiempo si es necesario. Este valor por defecto es de 200 milisegundos. Esto significa que G1GC intentará programar la frecuencia de los ciclos del recolector de basura, así como el número de zonas recogidas en cada ciclo, de modo que cada ciclo dure aproximadamente 200 ms.

- `InitiatingHeapOccupancyPercent`

	Esta opción especifica el porcentaje del montón total que puede estar en uso antes de que G1GC inicie un ciclo de recogida. El valor por defecto es 45. Esto significa que G1GC no iniciará un ciclo de recogida hasta después de que el 45% del montón esté en uso. Esto incluye tanto el uso de la nueva (Edén) como la antigua, en total.

El broker Kafka es bastante eficiente utilizando la memoria heap y creando objetos basura, por lo que es posible reducir estas opciones. Las opciones de ajuste del recogedor de basura proporcionadas en esta sección se han comprobado adecuadas para un servidor con 64 GB de memoria, ejecutando Kafka en un montón de 5 GB. Para , este broker puede configurarse con un valor de 20 ms. El valor de se establece en 35, lo que hace que la recogida de basura se ejecute ligeramente antes que con el valor por defecto.`MaxGCPauseMillis``InitiatingHeap​Occu⁠pancyPercent`

Kafka se lanzó originalmente antes de que el coleccionista G1GC estuviera disponible y se considerara estable. Por lo tanto, Kafka utiliza por defecto la recogida de basura concurrente mark and sweep para asegurar la compatibilidad con todas las JVM. La nueva mejor práctica es usar G1GC para cualquier cosa de Java 1.8 y posteriores. El cambio es fácil de hacer mediante variables de entorno. Usando el comando anterior en el capítulo, modifícalo de la siguiente manera:`start`

```
# export KAFKA_JVM_PERFORMANCE_OPTS="-server -Xmx6g -Xms6g
-XX:MetaspaceSize=96m -XX:+UseG1GC
-XX:MaxGCPauseMillis=20 -XX:InitiatingHeapOccupancyPercent=35
-XX:G1HeapRegionSize=16M -XX:MinMetaspaceFreeRatio=50
-XX:MaxMetaspaceFreeRatio=80 -XX:+ExplicitGCInvokesConcurrent"
# /usr/local/kafka/bin/kafka-server-start.sh -daemon
/usr/local/kafka/config/server.properties
#
```

## Distribución del Centro de Datos

Para entornos de pruebas y desarrollo, la ubicación física de los brokers Kafka dentro de un centro de datos no es tan preocupante, ya que el impacto no es tan severo si el clúster está parcial o completamente indisponible durante cortos periodos de tiempo. Sin embargo, al atender tráfico de producción, el tiempo de inactividad suele significar pérdida de dinero, ya sea por la pérdida de servicios para los usuarios o la pérdida de telemetría sobre lo que los usuarios están haciendo. Es entonces cuando se vuelve fundamental configurar la replicación dentro del clúster Kafka ([véase el Capítulo 7](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch07.html#reliable_data_delivery)), que es también cuando es importante considerar la ubicación física de los brokers en sus racks dentro del centro de datos. Un entorno de centro de datos que tenga un concepto de zonas de fallo es preferible. Si no se aborda antes de desplegar Kafka, puede ser necesario un mantenimiento costoso para mover servidores.

Kafka puede asignar nuevas particiones a los brokers de forma consciente del rack, asegurándose de que las réplicas de una sola partición no compartan rack. Para ello, la configuración de cada broker debe estar correctamente configurada. Esta configuración también puede configurarse en el dominio de fallos en entornos de nube por razones similares. Sin embargo, esto solo se aplica a particiones recién creadas. El clúster Kafka no monitoriza particiones que ya no son conscientes del rack (por ejemplo, como resultado de una reasignación de particiones), ni corrige automáticamente esta situación. Se recomienda utilizar herramientas que mantengan el cuadro de instrumentos correctamente equilibrados para mantener la conciencia del portaequipajes, como el control de crucero (véase [el Apéndice B](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/app02.html#appendix_3rd_party_tools)). Configurarlo correctamente ayudará a asegurar una conciencia continua del rack a lo largo del tiempo.`broker.rack`

En general, la mejor práctica es tener cada broker Kafka instalado en un clúster en un rack diferente, o al menos no compartir puntos únicos de fallo para servicios de infraestructura como la energía y la red. Esto normalmente significa al menos desplegar los servidores que ejecutarán brokers con conexiones de alimentación dual (a dos circuitos diferentes) y switches de red dual (con una interfaz conectada en los propios servidores para hacer la conmutación por error sin interrupciones). Incluso con conexiones dobles, hay una ventaja en tener intermediarios en racks completamente separados. De vez en cuando, puede ser necesario realizar mantenimiento físico en un rack o mueble que requiera estar desconectado (como mover servidores o recablear conexiones de alimentación).

## Colocación de aplicaciones en ZooKeeper

Kafka utiliza ZooKeeper para almacenar información de metadatos sobre los brokers, temas y particiones. Las escrituras en ZooKeeper solo se realizan en cambios en la membresía de los grupos de consumidores o en cambios en el propio clúster Kafka. Esta cantidad de tráfico es generalmente mínima y no justifica el uso de un conjunto dedicado de ZooKeeper para un único clúster Kafka. De hecho, muchos despliegues usan un único conjunto ZooKeeper para múltiples clústeres Kafka (usando una ruta chroot ZooKeeper para cada clúster, como se ha descrito anteriormente en este capítulo).

# Kafka Consumidores, Herramientas, ZooKeeper y Tú

Con el tiempo, la dependencia de ZooKeeper va disminuyendo. En la versión 2.8.0, Kafka introduce una visión en acceso anticipado de un Kafka completamente sin ZooKeeper, pero aún no está listo para producción. Sin embargo, todavía podemos ver esta reducción de dependencia de ZooKeeper en las versiones previas a esto. Por ejemplo, en versiones anteriores de Kafka, los consumidores (además de los brokers) utilizaban ZooKeeper para almacenar directamente información sobre la composición del grupo de consumidores y los temas que consumía, y para comprometer periódicamente los desplazamientos de cada partición consumida (para permitir la conmutación por error entre los consumidores del grupo). Con la versión 0.9.0.0, se modificó la interfaz de consumidor, permitiendo gestionarla directamente con los brokers Kafka. En cada versión 2.x de Kafka, vemos pasos adicionales para eliminar ZooKeeper de otros caminos obligatorios de Kafka. Las herramientas de administración ahora se conectan directamente al clúster y han eliminado la necesidad de conectarse directamente a ZooKeeper para operaciones como creación de temas, cambios dinámicos de configuración, etc. Por ello, muchas de las herramientas de línea de comandos que antes usaban las banderas `--zookeeper` se han actualizado para usar esta opción. Las opciones aún pueden usarse, pero han sido obsoletas y se eliminarán en el futuro cuando Kafka ya no tenga que conectarse a ZooKeeper para crear, gestionar o consumir a partir de temas.`--bootstrap-server``--zookeeper`

Sin embargo, existe una preocupación tanto por parte de los consumidores como de ZooKeeper bajo ciertas configuraciones. Aunque el uso de ZooKeeper para estos fines está obsoleto, los consumidores tienen la opción configurable de usar ZooKeeper o Kafka para hacer compromisos de compensación, y también pueden configurar el intervalo entre commmits. Si el consumidor utiliza ZooKeeper para los desplazamientos, cada consumidor realizará una escritura de ZooKeeper en cada intervalo para cada partición que consume. Un intervalo razonable para los commits de offset es de 1 minuto, ya que es el periodo durante el cual un grupo de consumidores leerá mensajes duplicados en caso de fallo del consumidor. Estos commits pueden suponer una cantidad significativa de tráfico de ZooKeeper, especialmente en un grupo con muchos consumidores, y deberán tenerse en cuenta. Puede ser necesario usar un intervalo de compromiso más largo si el conjunto ZooKeeper no puede manejar el tráfico. Sin embargo, se recomienda que los consumidores que usen las últimas librerías Kafka utilicen Kafka para comprometer los desplazamientos, eliminando así la dependencia de ZooKeeper.

Fuera de usar un solo conjunto para múltiples clústeres de Kafka, no se recomienda compartir el conjunto con otras aplicaciones, si es posible evitarlo. Kafka es sensible a la latencia y los tiempos muertos de ZooKeeper, y una interrupción en la comunicación con el conjunto hará que los intermediarios se comporten de forma impredecible. Esto puede hacer que varios brokers se desconecten al mismo tiempo si pierden conexiones a ZooKeeper, lo que resultará en particiones offline. También pone estrés en el controlador del clúster, que puede aparecer como errores sutiles mucho después de que la interrupción haya pasado, como al intentar realizar un apagado controlado de un intermediario. Otras aplicaciones que puedan poner presión sobre el conjunto ZooKeeper, ya sea por uso intensivo o por operaciones inadecuadas, deberían segregarse en su propio conjunto.

# Resumen

En este capítulo aprendimos cómo poner en marcha a Apache Kafka. También cubrimos cómo elegir el hardware adecuado para tus brokers y preocupaciones específicas sobre cómo configurarlo en un entorno de producción. Ahora que tienes un clúster Kafka, repasaremos los conceptos básicos de las aplicaciones cliente Kafka. Los dos siguientes capítulos cubrirán cómo crear clientes tanto para producir mensajes para Kafka ([Capítulo 3](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch03.html#writing_messages_to_kafka)) como para consumir esos mensajes de nuevo ([Capítulo 4](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch04.html#reading_data_from_kafka)).
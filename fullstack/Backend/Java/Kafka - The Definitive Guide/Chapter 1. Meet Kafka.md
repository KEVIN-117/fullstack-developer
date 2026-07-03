Toda empresa funciona con datos. Absorbemos información, la analizamos, la manipulamos y creamos más como resultado. Cada aplicación crea datos, ya sean mensajes de registro, métricas, actividad del usuario, mensajes salientes o cualquier otra cosa. Cada byte de datos tiene una historia que contar, algo importante que informará lo siguiente que hay que hacer. Para saber qué es, necesitamos obtener los datos desde donde se crean hasta donde pueden analizarse. Vemos esto todos los días en sitios web como Amazon, donde nuestros clics en artículos que nos interesan se convierten en recomendaciones que nos muestran poco después.

Cuanto antes lo hagamos, más ágiles y responsivas serán nuestras organizaciones. Cuanto menos esfuerzo dediquemos a mover datos, más podremos centrarnos en el negocio principal que tenemos entre manos. Por eso la pipeline es un componente crítico en la empresa basada en datos. La forma en que movemos los datos se vuelve casi tan importante como los propios datos.

> Cada vez que los científicos no están de acuerdo, es porque no tenemos datos suficientes. Entonces podemos ponernos de acuerdo sobre qué tipo de datos obtener; Obtenemos los datos; Y los datos resuelven el problema. O yo tengo razón, o tú tienes razón, o los dos estamos equivocados. Y seguimos adelante.
> 
> Neil deGrasse Tyson

# Publicar/Suscribir mensajes

Antes de hablar de los detalles de Apache Kafka, es importante que entendamos el concepto de mensajería de publicación/suscripción y por qué es un componente crítico de las aplicaciones basadas en datos. _La mensajería publicar/suscribirse (publicación/sub)_ es un patrón caracterizado por el remitente (publicador) de un dato (mensaje) que no lo dirige específicamente a un destinatario. En su lugar, el editor clasifica el mensaje de alguna manera, y ese receptor (suscriptor) se suscribe para recibir ciertas clases de mensajes. Los sistemas pub/subs suelen tener un broker, un punto central donde se publican los mensajes, para facilitar este patrón.

## Cómo empieza

Muchos casos de uso para publicar/suscribirse empiezan de la misma manera: con una cola de mensajes sencilla o un canal de comunicación entre procesos. Por ejemplo, creas una aplicación que necesita enviar información de monitorización a algún lugar, así que abres una conexión directa de tu aplicación a una app que muestra tus métricas en un panel de control, y envías métricas a través de esa conexión, como se ve en [la Figura 1-1](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch01.html#fig-1-singleconn).

![[../../../assets/Pasted image 20260522213231.png]]
Figura 1-1. Una única editorial de métricas directas

Esta es una solución sencilla a un problema sencillo que funciona cuando empiezas a monitorizar. En poco tiempo, decides que quieres analizar tus métricas a largo plazo, y eso no funciona bien en el panel de control. Inicias un nuevo servicio que puede recibir métricas, almacenarlas y analizarlas. Para soportar esto, modificas tu aplicación para que escriba métricas en ambos sistemas. A estas alturas tienes tres aplicaciones más que generan métricas, y todas hacen las mismas conexiones con estos dos servicios. Tu compañero cree que sería buena idea hacer encuestas activas de los servicios para alertas también, así que añades un servidor en cada una de las aplicaciones para proporcionar métricas a petición. Con el tiempo, hay más aplicaciones que usan esos servidores para obtener métricas individuales y usarlas para diversos fines. Esta arquitectura puede parecerse mucho [a la Figura 1-2](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch01.html#fig-2-multiconn), con conexiones aún más difíciles de rastrear.

![[../../../assets/Pasted image 20260522213251.png]]
Figuras 1-2. Muchas métricas publican publicaciones, usando conexiones directas

La deuda técnica acumulada aquí es evidente, así que decides devolverla en parte. Configuras una única aplicación que recibe métricas de todas las aplicaciones existentes y proporcionas un servidor para consultar esas métricas para cualquier sistema que las necesite. Esto reduce la complejidad de la arquitectura a algo similar a [la de las figuras 1-3](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch01.html#fig-3-single-pubsub). ¡Enhorabuena, has creado un sistema de mensajería para publicar/suscribirse!

![kdg2 0103](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492043072/files/assets/kdg2_0103.png)

###### Figuras 1-3. Un sistema de publicación/suscripción por métricas

## Sistemas de colas individuales

Al mismo tiempo que tú llevas librando esta guerra con las métricas, uno de tus compañeros ha estado haciendo un trabajo similar con mensajes de registro. Otra ha sido trabajar en el seguimiento del comportamiento de los usuarios en la web frontend y proporcionar esa información a desarrolladores que trabajan en aprendizaje automático, así como en crear algunos informes para la dirección. Todos habéis seguido un camino similar de construir sistemas que desacoplen a los editores de la información de los suscriptores a esa información. Las [figuras 1-4](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch01.html#fig-4-multi-pubsub) muestran dicha infraestructura, con tres sistemas pub/subs separados.

![[../../../assets/Pasted image 20260522213307.png]]
Figuras 1-4. Múltiples sistemas de publicación/suscripción

Esto es sin duda mucho mejor que utilizar conexiones punto a punto (como en [las Figuras 1-2](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch01.html#fig-2-multiconn)), pero hay mucha duplicación. Tu empresa mantiene múltiples sistemas para poner en cola los datos, cada uno con sus propios fallos y limitaciones individuales. También sabes que pronto habrá más casos de uso para la mensajería. Lo que te gustaría es tener un sistema centralizado único que permita publicar tipos genéricos de datos, que crecerán a medida que tu negocio crezca.

# Entra Kafka

Apache Kafka fue desarrollado como un sistema de mensajería de publicación/suscripción diseñado para resolver este problema. A menudo se describe como un "registro de commit distribuido" o, más recientemente, como una "plataforma de streaming distributiva". Un registro de commit de sistema de archivos o base de datos está diseñado para proporcionar un registro duradero de todas las transacciones para que puedan reproducirse y construir consistentemente el estado de un sistema. De manera similar, los datos dentro de Kafka se almacenan de forma duradera, en orden, y pueden leerse de forma determinista. Además, los datos pueden distribuirse dentro del sistema para proporcionar protecciones adicionales frente a fallos, así como oportunidades significativas para escalar el rendimiento.

## Mensajes y lotes

La unidad de datos dentro de Kafka se llama _mensaje_. Si te acercas a Kafka desde un entorno de base de datos, puedes pensar en esto como una _fila_ o un _registro_. Un mensaje es simplemente un array de bytes en lo que respecta a Kafka, por lo que los datos contenidos en él no tienen un formato o significado específico para Kafka. Un mensaje puede tener un metadato opcional, que se denomina _clave_. La clave también es un array de bytes y, como el mensaje, no tiene un significado específico para Kafka. Las claves se utilizan cuando se van a escribir mensajes en particiones de manera más controlada. El esquema más sencillo de este tipo es generar un hash consistente de la clave y luego seleccionar el número de partición para ese mensaje tomando el resultado del hash módulo el número total de particiones en el tema. Esto garantiza que los mensajes con la misma clave siempre se escriban en la misma partición (siempre que el conteo de particiones no cambie).

Para mayor eficiencia, los mensajes se escriben en Kafka en lotes. Un _lote_ es simplemente una colección de mensajes, todos los cuales se producen para el mismo tema y partición. Un viaje individual de ida y vuelta a través de la red para cada mensaje resultaría en una sobrecarga excesiva, y recopilar los mensajes en un lote reduce esto. Por supuesto, esto es un equilibrio entre latencia y rendimiento: cuanto mayores son los lotes, más mensajes se pueden manejar por unidad de tiempo, pero más tarda un mensaje individual en propagarse. Los lotes también suelen estar comprimidos, proporcionando una transferencia y almacenamiento de datos más eficientes a costa de cierta potencia de procesamiento. Tanto las claves como los lotes se discuten con más detalle en [el Capítulo 3](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch03.html#writing_messages_to_kafka).

## Esquemas

Aunque los mensajes son arrays de bytes opacos respecto a Kafka en sí, se recomienda imponer una estructura o esquema adicional al contenido del mensaje para que pueda entenderse fácilmente. Existen muchas opciones disponibles para _el esquema_ de mensajes, dependiendo de las necesidades individuales de tu aplicación. Sistemas simplistas, como JavaScript Object Notation (JSON) y Extensible Markup Language (XML), son fáciles de usar y legibles por humanos. Sin embargo, carecen de características como un manejo robusto de tipos y compatibilidad entre versiones de esquema. Muchos desarrolladores de Kafka prefieren el uso de Apache Avro, que es un framework de serialización desarrollado originalmente para Hadoop. Avro proporciona un formato compacto de serialización, esquemas separados de las cargas útiles de mensajes y que no requieren que se genere código al cambiar, y una fuerte tipificación de datos y evolución de esquemas, con compatibilidad tanto hacia atrás como hacia adelante.

Un formato de datos coherente es importante en Kafka, ya que permite desacoplar la escritura y la lectura de mensajes. Cuando estas tareas están estrechamente acopladas, las aplicaciones que suscriben mensajes deben actualizarse para manejar el nuevo formato de datos, en paralelo con el formato antiguo. Solo entonces se pueden actualizar las aplicaciones que publican los mensajes para utilizar el nuevo formato. Al usar esquemas bien definidos y almacenarlos en un repositorio común, los mensajes en Kafka pueden entenderse sin coordinación. Los esquemas y la serialización se tratan con más detalle en [el Capítulo 3](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch03.html#writing_messages_to_kafka).

## Temas y particiones

Los mensajes en kafka se clasifican por _temas_. Las analogías más cercanas para un tema son una tabla de base de datos o una carpeta en un sistema de archivos. Los temas también se descomponen en varias _particiones_. Volviendo a la descripción de "log de confirmación", una partición es un solo log. Los mensajes se escriben en ella solo en forma de añadir y se leen en orden de principio a fin. Ten en cuenta que, como un tema suele tener varias particiones, no hay garantía de que el orden de los mensajes se distribuya en todo el tema, solo dentro de una sola partición. Las [figuras 1-5](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch01.html#fig-5-partitions) muestran un tema con cuatro particiones, con escrituras añadidas al final de cada una. Las particiones también son la forma en que Kafka proporciona redundancia y escalabilidad. Cada partición puede alojarse en un servidor diferente, lo que significa que un solo tema puede escalarse horizontalmente entre varios servidores para ofrecer un rendimiento muy superior a la capacidad de un solo servidor. Además, se pueden replicar particiones, de modo que diferentes servidores almacenarán una copia de la misma partición en caso de que uno falle.

![[../../../assets/Pasted image 20260522213320.png]]
Figuras 1-5. Representación de un tema con múltiples particiones

El _término flujo_ se utiliza a menudo al hablar de datos dentro de sistemas como Kafka. La mayoría de las veces, un flujo se considera un único tema de datos, independientemente del número de particiones. Esto representa un único flujo de datos que pasa de los productores a los consumidores. Esta forma de referirse a los mensajes es más común cuando se habla de procesamiento de flujos, que es cuando los frameworks —algunos de los cuales son Kafka Streams, Apache Samza y Storm— operan sobre los mensajes en tiempo real. Este método de operación puede compararse con la forma en que los frameworks offline, concretamente Hadoop, están diseñados para trabajar con datos masivos en un momento posterior. En [el Capítulo 14](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch14.html#stream_processing) se ofrece una visión general del procesamiento de corrientes.

## Productores y consumidores

Los clientes Kafka son usuarios del sistema, y existen dos tipos básicos: productores y consumidores. También existen APIs avanzadas para clientes: Kafka Connect API para integración de datos y Kafka Streams para el procesamiento de flujos. Los clientes avanzados utilizan productores y consumidores como bloques de construcción y proporcionan funcionalidad de mayor nivel encima.

_Los productores_ crean nuevos mensajes. En otros sistemas de publicación/suscripción, estos pueden llamarse _editores_ o _escritores_. Se producirá un mensaje sobre un tema específico. Por defecto, el productor equilibrará los mensajes en todas las particiones de un tema de manera equitativa. En algunos casos, el productor dirigirá mensajes a particiones específicas. Esto normalmente se hace usando la clave de mensaje y un particionador que genera un hash de la clave y la mapea a una partición específica. Esto garantiza que todos los mensajes producidos con una clave determinada se escriban en la misma partición. El productor también podría usar un particionador personalizado que siga otras reglas de negocio para mapear mensajes a particiones. Los productores se explican con más detalle en [el capítulo 3](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch03.html#writing_messages_to_kafka).

_Los consumidores_ leen los mensajes. En otros sistemas de publicación/suscripción, estos clientes pueden llamarse _suscriptores_ o _lectores_. El consumidor se suscribe a uno o más temas y lee los mensajes en el orden en que se produjeron en cada partición. El consumidor lleva un registro de los mensajes que ya ha consumido controlando el desplazamiento de los mensajes. El _desplazamiento_ —un valor entero que aumenta continuamente— es otro metadato que Kafka añade a cada mensaje a medida que se produce. Cada mensaje en una partición dada tiene un desplazamiento único, y el siguiente mensaje tiene un desplazamiento mayor (aunque no necesariamente monótonamente mayor). Almacenando el siguiente desplazamiento posible para cada partición, normalmente en Kafka, un consumidor puede detenerse y reiniciar sin perder su lugar.

Los consumidores trabajan como parte de un _grupo de consumidores_, que consiste en uno o más consumidores que colaboran para consumir un tema. El grupo asegura que cada partición sea consumida solo por un miembro. En [las Figuras 1-6](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch01.html#fig-6-consumer), hay tres consumidores en un mismo grupo que consumen un tema. Dos de los consumidores trabajan desde una partición cada uno, mientras que el tercero trabaja desde dos particiones. La asignación de un consumidor a una partición suele llamarse _propiedad_ de la partición por parte del consumidor.

De este modo, los consumidores pueden escalar horizontalmente para consumir temas con un gran número de mensajes. Además, si falla un solo consumidor, los miembros restantes del grupo reasignarán las particiones que se están consumiendo para reemplazar al miembro que falta. Los consumidores y los grupos de consumidores se discuten con más detalle en [el Capítulo 4](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch04.html#reading_data_from_kafka).

![[../../../assets/Pasted image 20260522213331.png]]
Figuras 1-6. Un grupo de consumidores leyendo un tema

## Corredores y clústeres

Un único servidor Kafka se llama _broker_. El broker recibe mensajes de los productores, les asigna desplazamientos y escribe los mensajes en el almacenamiento en disco. También da servicio a los consumidores, respondiendo a solicitudes de obtención de particiones y con los mensajes que han sido publicados. Dependiendo del hardware específico y sus características de rendimiento, un solo broker puede manejar fácilmente miles de particiones y millones de mensajes por segundo.

Los corredores Kafka están diseñados para operar como parte de un _clúster._ Dentro de un clúster de brokers, uno de los brokers también funcionará como _controlador_ del clúster (elegido automáticamente entre los miembros activos del clúster). El controlador es responsable de las operaciones administrativas, incluyendo la asignación de particiones a los corredores y la supervisión de fallos de los corredores. Una partición es propiedad de un único intermediario en el clúster, y ese intermediario se denomina _líder_ de la partición. Se asigna una partición replicada (como se ve en [las Figuras 1-7](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch01.html#fig-7-replication)) a intermediarios adicionales, _llamados seguidores_ de la partición. La replicación proporciona redundancia de los mensajes en la partición, de modo que uno de los seguidores puede asumir el liderazgo si hay un fallo del intermediario. Todos los productores deben conectarse al líder para publicar mensajes, pero los consumidores pueden buscar el líder o uno de los seguidores. Las operaciones de clúster, incluida la replicación de particiones, se tratan en detalle en [el Capítulo 7](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch07.html#reliable_data_delivery).

![[../../../assets/Pasted image 20260522213341.png]]
Figuras 1-7. Replicación de particiones en un clúster

Una característica clave de Apache Kafka es la _retención_, que es el almacenamiento duradero de mensajes durante un periodo de tiempo. Los brokers Kafka están configurados con una configuración predeterminada de retención para los temas, ya sea reteniendo mensajes durante un periodo de tiempo (por ejemplo, 7 días) o hasta que la partición alcance cierto tamaño en bytes (por ejemplo, 1 GB). Una vez alcanzados estos límites, los mensajes caducan y se eliminan. De este modo, la configuración de retención define una cantidad mínima de datos disponibles en cualquier momento. Los temas individuales también pueden configurarse con sus propios ajustes de retención para que los mensajes se almacenen solo mientras sean útiles. Por ejemplo, un tema de seguimiento puede mantenerse durante varios días, mientras que las métricas de aplicación pueden conservarse solo unas pocas horas. Los temas también pueden configurarse como _log-compacted_, lo que significa que Kafka solo conservará el último mensaje producido con una clave específica. Esto puede ser útil para datos tipo changelog, donde solo la última actualización resulta interesante.

## Múltiples clústeres

A medida que crecen los despliegues de Kafka, a menudo es ventajoso contar con múltiples clústeres. Hay varias razones por las que esto puede ser útil:

- Segregación de tipos de datos
    
- Aislamiento para requisitos de seguridad
    
- Múltiples centros de datos (recuperación ante desastres)
    

Al trabajar con múltiples centros de datos en particular, a menudo se requiere que los mensajes se copien entre ellos. De este modo, las aplicaciones online pueden acceder a la actividad de los usuarios en ambos sitios. Por ejemplo, si un usuario cambia información pública en su perfil, ese cambio deberá ser visible independientemente del centro de datos en el que se muestren los resultados de búsqueda. O bien, los datos de monitorización pueden recopilarse de muchos sitios en un único lugar central donde se alojan los sistemas de análisis y alerta. Los mecanismos de replicación dentro de los clústeres de Kafka están diseñados únicamente para funcionar dentro de un solo clúster, no entre múltiples clústeres.

El proyecto Kafka incluye una herramienta llamada _MirrorMaker_, utilizada para replicar datos a otros clústeres. En esencia, MirrorMaker es simplemente un consumidor y productor Kafka, vinculados por una cola. Los mensajes se consumen desde un grupo de Kafka y se producen a otro. La [Figura 1-8](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch01.html#fig-8-tiers) muestra un ejemplo de una arquitectura que utiliza MirrorMaker, agregando mensajes de dos clústeres locales en un clúster agregado y luego copiando ese clúster a otros centros de datos. La naturaleza sencilla de la aplicación oculta su capacidad para crear sofisticadas canalizaciones de datos, que se detallarán más en [el capítulo 9](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch09.html#building_data_pipelines).

![[../../../assets/Pasted image 20260522213353.png]]
Figuras 1-8. Arquitectura de múltiples centros de datos

# ¿Por qué Kafka?

Hay muchas opciones para sistemas de mensajería de publicación/suscripción, así que ¿qué hace que Apache Kafka sea una buena opción?

## Múltiples productores

Kafka es capaz de gestionar sin problemas a múltiples productores, ya sea que esos clientes utilicen muchos temas o el mismo tema. Esto hace que el sistema sea ideal para agregar datos de muchos sistemas frontend y hacerlos consistentes. Por ejemplo, un sitio que sirve contenido a los usuarios a través de varios microservicios puede tener un único tema para las vistas de página en el que todos los servicios pueden escribir usando un formato común. Las aplicaciones de consumo pueden entonces recibir un único flujo de vistas de página para todas las aplicaciones del sitio sin tener que coordinar el consumo de varios temas, uno para cada aplicación.

## Múltiples consumidores

Además de tener varios productores, Kafka está diseñado para que varios consumidores puedan leer cualquier secuencia de mensajes sin interferir entre ellos. Esto contrasta con muchos sistemas de cola, donde una vez que un mensaje es consumido por un cliente, no está disponible para ningún otro. Varios consumidores de Kafka pueden elegir operar como parte de un grupo y compartir un stream, asegurando que todo el grupo procese un mensaje dado solo una vez.

## Retención basada en disco

Kafka no solo puede gestionar a varios consumidores, sino que la retención duradera de mensajes significa que los consumidores no siempre necesitan trabajar en tiempo real. Los mensajes se escriben en disco y se almacenan con reglas de retención configurables. Estas opciones pueden seleccionarse por tema, permitiendo que diferentes flujos de mensajes tengan distintos niveles de retención según las necesidades del consumidor. La retención duradera significa que si un consumidor se atrasa, ya sea por procesamiento lento o por un aumento de tráfico, no hay peligro de perder datos. También significa que el mantenimiento puede realizarse en los consumidores, desconectando las aplicaciones durante un corto periodo de tiempo, sin preocuparse de que los mensajes se respalden en el productor o se pierdan. Se puede detener a los consumidores y los mensajes se mantendrán en Kafka. Esto les permite reiniciar y retomar los mensajes procesados donde lo dejaron sin pérdida de datos.

## Escalable

La escalabilidad flexible de Kafka facilita el manejo de cualquier cantidad de datos. Los usuarios pueden empezar con un solo broker como prueba de concepto, ampliarse a un pequeño clúster de desarrollo de tres brokers y pasar a la producción con un clúster mayor de decenas o incluso cientos de brokers que crece con el tiempo a medida que los datos crecen. Las expansiones pueden realizarse mientras el clúster está en línea, sin afectar la disponibilidad del sistema en su conjunto. Esto también significa que un grupo de varios corredores puede gestionar el fallo de un corredor individual y seguir atendiendo a los clientes. Los clústeres que necesitan tolerar más fallos simultáneos pueden configurarse con factores de replicación más altos. La replicación se discute con más detalle en [el capítulo 7](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch07.html#reliable_data_delivery).

## Alto rendimiento

Todas estas características se combinan para hacer de Apache Kafka un sistema de mensajería de publicación/suscripción con un rendimiento excelente bajo alta carga. Productores, consumidores y brokers pueden escalarse para manejar flujos de mensajes muy grandes con facilidad. Esto puede hacerse sin perder una latencia de mensaje de un segundo desde la producción hasta la disponibilidad para los consumidores.

## Características de la plataforma

El proyecto principal de Apache Kafka también ha añadido algunas funciones de plataforma de streaming que pueden facilitar mucho a los desarrolladores realizar tipos de trabajo habituales. Aunque no son plataformas completas, que normalmente incluyen un entorno de ejecución estructurado como YARN, estas características se presentan en forma de APIs y bibliotecas que proporcionan una base sólida sobre la que construir y flexibilidad sobre dónde pueden ejecutarse. Kafka Connect ayuda en la tarea de extraer datos de un sistema de datos fuente y enviarlos a Kafka, o extraer datos de Kafka y enviarlos a un sistema de datos de sumidero. Kafka Streams proporciona una biblioteca para desarrollar fácilmente aplicaciones de procesamiento de flujos que sean escalables y tolerantes a fallos. Connect se discute en [el capítulo 9](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch09.html#building_data_pipelines), mientras que Streams se detalla en [el capítulo 14](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch14.html#stream_processing).

# El ecosistema de datos

Muchas aplicaciones participan en los entornos que construimos para el procesamiento de datos. Hemos definido entradas en forma de aplicaciones que crean datos o los introducen de alguna manera en el sistema. Hemos definido resultados en forma de métricas, informes y otros productos de datos. Creamos bucles, con algunos componentes leyendo datos del sistema, transformándolos usando datos de otras fuentes y luego reintroduciéndolos en la infraestructura de datos para usarlos en otros lugares. Esto se hace para numerosos tipos de datos, cada uno con cualidades únicas de contenido, tamaño y uso.

Apache Kafka proporciona el sistema circulatorio para el ecosistema de datos, como se muestra en [las Figuras 1-9](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch01.html#fig-9-ecosystem). Transporta mensajes entre los distintos miembros de la infraestructura, proporcionando una interfaz consistente para todos los clientes. Cuando se combina con un sistema que proporciona esquemas de mensajes, los productores y consumidores ya no requieren un acoplamiento estrecho ni conexiones directas de ningún tipo. Los componentes pueden añadirse y eliminarse a medida que se crean y disuelven los casos de negocio, y los productores no tienen que preocuparse por quién utiliza los datos ni por el número de aplicaciones que consumen.

![[../../../assets/Pasted image 20260522213408.png]]
Figuras 1-9. Un ecosistema de big data

## Casos de uso

### Seguimiento de actividad

El caso de uso original de Kafka, tal y como fue diseñado en LinkedIn, es el seguimiento de la actividad de los usuarios. Los usuarios de un sitio web interactúan con aplicaciones frontend, que generan mensajes sobre las acciones que el usuario está realizando. Esto puede ser información pasiva, como vistas de página y seguimiento de clics, o acciones más complejas, como información que un usuario añade a su perfil. Los mensajes se publican en uno o más temas, que luego son absorbidos por las aplicaciones en el backend. Estas aplicaciones pueden estar generando informes, alimentando sistemas de aprendizaje automático, actualizando resultados de búsqueda o realizando otras operaciones necesarias para ofrecer una experiencia de usuario enriquecida.

### Mensajería

Kafka también se utiliza para mensajería, donde las aplicaciones necesitan enviar notificaciones (como correos electrónicos) a los usuarios. Estas aplicaciones pueden generar mensajes sin necesidad de preocuparse por el formato o por cómo se enviarán realmente los mensajes. Una sola aplicación puede entonces leer todos los mensajes a enviar y gestionarlos de forma consistente, incluyendo:

- Formatear los mensajes (también conocido como _decoración_) usando un aspecto y sensación comunes
    
- Recopilar múltiples mensajes en una sola notificación para enviar
    
- Aplicar las preferencias del usuario sobre cómo quiere recibir mensajes
    

Utilizar una sola aplicación para esto evita la necesidad de duplicar funcionalidades en múltiples aplicaciones, además de permitir operaciones como la agregación que de otro modo no serían posibles.

### Métricas y registro

Kafka también es ideal para recopilar métricas y registros de aplicaciones y sistemas. Este es un caso de uso en el que destaca la capacidad de tener múltiples aplicaciones produciendo el mismo tipo de mensaje. Las aplicaciones publican métricas de forma regular sobre un tema de Kafka, y esas métricas pueden ser consumidas por los sistemas para monitorización y alertas. También pueden usarse en un sistema offline como Hadoop para realizar análisis a largo plazo, como proyecciones de crecimiento. Los mensajes de registro pueden publicarse de la misma manera y pueden ser enrutados a sistemas dedicados de búsqueda de registros como Elasticsearch o a aplicaciones de análisis de seguridad. Otro beneficio añadido de Kafka es que cuando el sistema de destino necesita cambiar (por ejemplo, es hora de actualizar el sistema de almacenamiento de registros), no es necesario modificar las aplicaciones frontales ni los medios de agregación.

### Registro de confirmación

Dado que Kafka se basa en el concepto de registro de commit, los cambios en la base de datos pueden publicarse en Kafka, y las aplicaciones pueden monitorizar fácilmente este flujo para recibir actualizaciones en vivo a medida que ocurran. Este flujo de registro de cambios también puede usarse para replicar actualizaciones de bases de datos en un sistema remoto, o para consolidar cambios de múltiples aplicaciones en una única vista de base de datos. La retención duradera es útil aquí para proporcionar un buffer para el registro de cambios, lo que significa que puede reproducirse en caso de fallo de las aplicaciones que lo consumen. Alternativamente, los temas log-compactados pueden usarse para proporcionar una retención más prolongada al conservar solo un cambio por clave.

### Procesamiento de flujos

Otra área que ofrece numerosos tipos de aplicaciones es el procesamiento de flujos. Aunque casi todo el uso de Kafka puede considerarse como procesamiento de flujos, el término se utiliza típicamente para referirse a aplicaciones que ofrecen funcionalidades similares para mapear/reducir el procesamiento en Hadoop. Hadoop suele basarse en la agregación de datos durante un largo periodo de tiempo, ya sea horas o días. El procesamiento de flujo opera sobre datos en tiempo real, tan rápido como se producen los mensajes. Los frameworks de flujo permiten a los usuarios escribir pequeñas aplicaciones para operar sobre mensajes Kafka, realizando tareas como contar métricas, particionar mensajes para un procesamiento eficiente por parte de otras aplicaciones o transformar mensajes utilizando datos de múltiples fuentes. El procesamiento de flujos se trata en [el Capítulo 14](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/ch14.html#stream_processing).

# El origen de Kafka

Kafka se creó para abordar el problema de la cadena de datos en LinkedIn. Fue diseñado para proporcionar un sistema de mensajería de alto rendimiento capaz de manejar muchos tipos de datos y proporcionar datos limpios y estructurados sobre la actividad del usuario y las métricas del sistema en tiempo real.

> Los datos realmente impulsan todo lo que hacemos.
> 
> Jeff Weiner, ex CEO de LinkedIn

## El problema de LinkedIn

Similar al ejemplo descrito al principio de este capítulo, LinkedIn tenía un sistema para recopilar métricas de sistemas y aplicaciones que utilizaba recolectores personalizados y herramientas de código abierto para almacenar y presentar datos internamente. Además de métricas tradicionales, como el uso de la CPU y el rendimiento de las aplicaciones, existía una sofisticada función de rastreo de solicitudes que utilizaba el sistema de monitorización y podía ofrecer una introspección sobre cómo una solicitud de un solo usuario se propagaba a través de aplicaciones internas. Sin embargo, el sistema de monitorización presentaba muchos fallos. Esto incluía la recogida de métricas basadas en encuestas, grandes intervalos entre métricas y la ausencia de la capacidad de los propietarios de la aplicación para gestionar sus propias métricas. El sistema era de alta sensibilidad, requiriendo intervención humana para la mayoría de tareas sencillas, e inconsistente, con nombres de métricas diferentes para la misma medición entre distintos sistemas.

Al mismo tiempo, se creó un sistema para rastrear la información de actividad de los usuarios. Este era un servicio HTTP al que los servidores frontales se conectaban periódicamente y publicaban un lote de mensajes (en formato XML) en el servicio HTTP. Estos lotes se trasladaron luego a plataformas de procesamiento offline, donde se analizaban y recopilaban los archivos. Este sistema tenía muchos fallos. El formato XML era inconsistente y analizarlo era computacionalmente costoso. Cambiar el tipo de actividad del usuario que se rastreaba requirió una cantidad significativa de trabajo coordinado entre los frontends y el procesamiento offline. Aun así, el sistema se estropeaba constantemente debido a los cambios de esquema. El seguimiento se basaba en lotes horarios, por lo que no podía usarse en tiempo real.

La monitorización y el seguimiento de la actividad del usuario no podían usar el mismo servicio de backend. El servicio de monitorización era demasiado torpe, el formato de datos no estaba orientado al seguimiento de actividades, y el modelo de sondeo para monitorización no era compatible con el modelo push para el seguimiento. Al mismo tiempo, el servicio de seguimiento era demasiado frágil para usarlo en métricas, y el procesamiento orientado a lotes no era el modelo adecuado para la monitorización y alertas en tiempo real. Sin embargo, los datos de monitorización y seguimiento compartían muchas características, y la correlación de la información (como cómo ciertos tipos de actividad de usuarios afectaban al rendimiento de la aplicación) era muy deseable. Una disminución en ciertos tipos de actividad del usuario podía indicar problemas con la aplicación que la atendía, pero horas de retraso en el procesamiento de lotes de actividad significaban una respuesta lenta a este tipo de problemas.

Al principio, se investigaron a fondo las soluciones de código abierto ya existentes para encontrar un nuevo sistema que proporcionara acceso en tiempo real a los datos y se ampliara para gestionar la cantidad de tráfico de mensajes necesario. Los sistemas prototipo se configuraron usando ActiveMQ, pero en ese momento no podía manejar la escala. También era una solución frágil para la forma en que LinkedIn necesitaba usarla, descubriendo muchos fallos en ActiveMQ que hacían que los brokers se detuvieran. Estas pausas harían copias de seguridad de las conexiones con los clientes e interferirían con la capacidad de las aplicaciones para atender solicitudes a los usuarios. Se tomó la decisión de avanzar con una infraestructura personalizada para la cadena de datos.

## El nacimiento de Kafka

El equipo de desarrollo de LinkedIn estuvo dirigido por Jay Kreps, ingeniero principal de software que anteriormente fue responsable del desarrollo y la publicación de código abierto de Voldemort, un sistema distribuido de almacenamiento de clave-valor. El equipo inicial también incluía a Neha Narkhede y, más tarde, a Jun Rao. Juntos, se propusieron crear un sistema de mensajería que pudiera satisfacer las necesidades tanto de los sistemas de monitorización como de seguimiento, y escalar para el futuro. Los objetivos principales eran:

- Desacoplar productores y consumidores mediante un modelo push-pull
    
- Proporcionar persistencia para los datos de los mensajes dentro del sistema de mensajería para permitir múltiples consumidores
    
- Optimizar para un alto rendimiento de mensajes
    
- Permitir que la escalada horizontal del sistema crezca a medida que los flujos de datos crecían
    

El resultado fue un sistema de mensajería publicación/suscripción que tenía una interfaz típica de los sistemas de mensajería pero una capa de almacenamiento más parecida a un sistema de agregación de logs. Combinado con la adopción de Apache Avro para la serialización de mensajes, Kafka fue eficaz para gestionar tanto métricas como seguimiento de la actividad del usuario a una escala de miles de millones de mensajes al día. La escalabilidad de Kafka ha ayudado a que el uso de LinkedIn crezca en más de siete billones de mensajes producidos (a febrero de 2020) y más de cinco petabytes de datos consumidos diariamente.

## Código abierto

Kafka fue lanzado como un proyecto de código abierto en GitHub a finales de 2010. A medida que empezó a ganar atención en la comunidad de código abierto, fue propuesto y aceptado como proyecto incubador de la Apache Software Foundation en julio de 2011. Apache Kafka se graduó de la incubadora en octubre de 2012. Desde entonces, se ha trabajado continuamente en ello y ha encontrado una comunidad sólida de colaboradores y committers fuera de LinkedIn. Kafka se utiliza ahora en algunas de las mayores cadenas de datos del mundo, incluyendo las de Netflix, Uber y muchas otras empresas.

La adopción generalizada de Kafka ha creado también un ecosistema saludable alrededor del proyecto central. Existen grupos activos de encuentro en decenas de países de todo el mundo, que ofrecen debate local y apoyo al procesamiento de flujos. También existen numerosos proyectos de código abierto relacionados con Apache Kafka. LinkedIn sigue manteniendo varios, incluyendo Cruise Control, Kafka Monitor y Burrow. Además de sus ofertas comerciales, Confluent ha lanzado proyectos como ksqlDB, un registro de esquemas y un proxy REST bajo una licencia comunitaria (que no es estrictamente de código abierto, ya que incluye restricciones de uso). Varios de los proyectos más populares se enumeran en [el Apéndice B](https://learning.oreilly.com/library/view/kafka-the-definitive/9781492043072/app02.html#appendix_3rd_party_tools).

## Compromiso comercial

En otoño de 2014, Jay Kreps, Neha Narkhede y Jun Rao dejaron LinkedIn para fundar Confluent, una empresa centrada en ofrecer desarrollo, soporte empresarial y formación para Apache Kafka. También se unieron a otras empresas (como Heroku) para ofrecer servicios en la nube de Kafka. Confluent, a través de una colaboración con Google, ofrece clústeres Kafka gestionados en Google Cloud Platform, así como servicios similares en Amazon Web Services y Azure. Otra de las principales iniciativas de Confluent es organizar la serie de conferencias de la Cumbre Kafka. Iniciada en 2016, con conferencias anuales en Estados Unidos y Londres, la Cumbre Kafka ofrece un lugar para que la comunidad se reúna a escala global y comparta conocimientos sobre Apache Kafka y proyectos relacionados.

## El nombre

La gente suele preguntar cómo se llamó Kafka y si significa algo específico sobre la propia aplicación. Jay Kreps ofreció la siguiente perspectiva:

> Pensé que, dado que Kafka era un sistema optimizado para escribir, usar el nombre de un escritor tendría sentido. Había hecho muchas clases de literatura en la universidad y me gustaba Franz Kafka. Además, el nombre sonaba bien para un proyecto de código abierto.
> 
> Así que básicamente no hay mucha relación.

# Empezando con Kafka

Ahora que sabemos todo sobre Kafka y su historia, podemos montarlo y construir nuestra propia cadena de datos. En el próximo capítulo, exploraremos la instalación y configuración de Kafka. También hablaremos sobre la selección del hardware adecuado para ejecutar Kafka y algunas cosas a tener en cuenta al pasar a operaciones de producción.
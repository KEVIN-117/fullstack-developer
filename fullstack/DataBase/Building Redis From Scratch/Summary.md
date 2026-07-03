[Redis](https://redis.io/docs/latest/develop/get-started/data-store/) es un almacén de estructuras de datos en memoria que se utiliza a menudo como base de datos, caché, intermediario de mensajes y motor de streaming. En este desafío construiremos nuestro propio servidor Redis capaz de servir comandos básicos, leer archivos RDB y más.

A lo largo del camino, aprenderemos sobre servidores TCP, el Protocolo Redis y más.

## ¿Qué es exactamente lo que construiremos?

Empezarás implementando los bloques básicos de cada servidor Redis:

- Vinculación a un puerto TCP y escucha conexiones
- Responder a comandos básicos como `PING` y `ECHO`
- Análisis del Protocolo Redis (RESP) a partir de solicitudes del cliente
- Gestionar varios clientes simultáneamente
- Implementando los comandos `SET` and `GET` para almacenar y recuperar datos.

En esta etapa, tu Redis ya se sentirá real y podrás interactuar con el oficial .`redis-cli`

A medida que avances, implementarás funciones avanzadas como:

- Replicación de Redis
- Persistencia RDB
- Transacciones atómicas
- … y más

Al final, tendrás un repositorio de GitHub para presumir.
## ¿Qué es exactamente lo que voy a aprenderemos?
En las primeras 7 etapas, aprenderemos:
- Cómo un servidor `TCP` se enlaza a un puerto y acepta conexiones 
- Qué es el protocolo Redis (`RESP`) y cómo analizar/codificar mensajes 
- Cómo gestionar múltiples clientes simultáneamente 
- Cómo implementar comandos como `PING`, `ECHO`, `SET` y `GET` 
- Cómo administrar un almacén de clave-valor con caducidad automática de claves
En las etapas avanzadas, descubrirás nuevas ideas de programación, como la sincronización maestro-réplica, las transacciones atómicas y estructuras de datos especializadas como conjuntos ordenados e índices geoespaciales.

A medida que tu código se vuelva más complejo, te verás obligado a estructurarlo y refactorizarlo, para evitar regresiones y facilitar la adición de nuevas funcionalidades.

## ¿Por qué deberíamos de construir un proyecto así?

Crear tu propio Redis combina programación de redes, computación concurrente y diseño de sistemas. Si te has dedicado principalmente al desarrollo de sitios web o aplicaciones, este proyecto te permitirá comprender con mayor profundidad cómo funcionan el almacenamiento en caché y los sistemas distribuidos.

También estarás construyendo una pieza fundamental de la infraestructura de la que dependen las aplicaciones, como la línea de tiempo de Twitter y la caché integrada de Uber.

Más allá de la profundidad técnica, comprender una herramienta que millones de desarrolladores utilizan a diario tiene una satisfacción única. Al finalizar, te convertirás en un desarrollador más seguro y con mayor proyección.
## ¿Cuáles son los requisitos para este reto?

Debes sentirte cómodo escribiendo código en cualquier lenguaje y utilizando Git. No se requiere experiencia previa con bases de datos ni programación de redes.

La mayoría de los estudiantes van adquiriendo los conceptos necesarios (por ejemplo, servidores TCP) a medida que avanzan.

Lo más importante es la curiosidad y la perseverancia. Desarrollarás tu intuición explorando, depurando y descubriendo soluciones por ti mismo.

Si bien haremos que empezar sea extremadamente sencillo, no esperes que sea un tutorial paso a paso.


# Stages

## Core Commands

- [Bind to a port](https://app.codecrafters.io/courses/redis/introduction)
- [Respond to PING](https://app.codecrafters.io/courses/redis/stages/rg2)
- [Respond to multiple PINGs](https://app.codecrafters.io/courses/redis/stages/wy1)
- [Handle concurrent clients](https://app.codecrafters.io/courses/redis/stages/zu2)
- [Implement the ECHO command](https://app.codecrafters.io/courses/redis/stages/qq0)
- [Implement the SET & GET commands](https://app.codecrafters.io/courses/redis/stages/la7)
- [Expiry](https://app.codecrafters.io/courses/redis/stages/yz1)

## Lists

- [Create a list](https://app.codecrafters.io/courses/redis/stages/mh6)
- [Append an element](https://app.codecrafters.io/courses/redis/stages/tn7)
- [Append multiple elements](https://app.codecrafters.io/courses/redis/stages/lx4)
- [List elements (positive indexes)](https://app.codecrafters.io/courses/redis/stages/sf6)
- [List elements (negative indexes)](https://app.codecrafters.io/courses/redis/stages/ri1)
- [Prepend elements](https://app.codecrafters.io/courses/redis/stages/gu5)
- [Query list length](https://app.codecrafters.io/courses/redis/stages/fv6)
- [Remove an element](https://app.codecrafters.io/courses/redis/stages/ef1)
- [Remove multiple elements](https://app.codecrafters.io/courses/redis/stages/jp1)
- [Blocking retrieval](https://app.codecrafters.io/courses/redis/stages/ec3)
- [Blocking retrieval with timeout](https://app.codecrafters.io/courses/redis/stages/xj7)

## Streams

- [The TYPE command](https://app.codecrafters.io/courses/redis/stages/cc3)
- [Create a stream](https://app.codecrafters.io/courses/redis/stages/cf6)
- [Validating entry IDs](https://app.codecrafters.io/courses/redis/stages/hq8)
- [Partially auto-generated IDs](https://app.codecrafters.io/courses/redis/stages/yh3)
- [Fully auto-generated IDs](https://app.codecrafters.io/courses/redis/stages/xu6)
- [Query entries from stream](https://app.codecrafters.io/courses/redis/stages/zx1)
- [Query with -](https://app.codecrafters.io/courses/redis/stages/yp1)
- [Query with +](https://app.codecrafters.io/courses/redis/stages/fs1)
- [Query single stream using XREAD](https://app.codecrafters.io/courses/redis/stages/um0)
- [Query multiple streams using XREAD](https://app.codecrafters.io/courses/redis/stages/ru9)
- [Blocking reads](https://app.codecrafters.io/courses/redis/stages/bs1)
- [Blocking reads without timeout](https://app.codecrafters.io/courses/redis/stages/hw1)
- [Blocking reads using $](https://app.codecrafters.io/courses/redis/stages/xu1)

## Transactions

- [The INCR command (1/3) - Easy](https://app.codecrafters.io/courses/redis/stages/si4)
- [The INCR command (2/3) - Easy](https://app.codecrafters.io/courses/redis/stages/lz8)
- [The INCR command (3/3) - Easy](https://app.codecrafters.io/courses/redis/stages/mk1)
- [The MULTI command - Easy](https://app.codecrafters.io/courses/redis/stages/pn0)
- [The EXEC command - Easy](https://app.codecrafters.io/courses/redis/stages/lo4)
- [Empty transaction - Hard](https://app.codecrafters.io/courses/redis/stages/we1)
- [Queueing commands - Medium](https://app.codecrafters.io/courses/redis/stages/rs9)
- [Executing a transaction - Hard](https://app.codecrafters.io/courses/redis/stages/fy6)
- [The DISCARD command - Easy](https://app.codecrafters.io/courses/redis/stages/rl9)
- [Failures within transactions - Medium](https://app.codecrafters.io/courses/redis/stages/sg9)
- [Multiple transactions - Medium](https://app.codecrafters.io/courses/redis/stages/jf8)

## Optimistic Locking

- [The WATCH command - Easy](https://app.codecrafters.io/courses/redis/stages/jb7)
- [WATCH inside transaction - Easy](https://app.codecrafters.io/courses/redis/stages/jq9)
- [Tracking key modifications - Medium](https://app.codecrafters.io/courses/redis/stages/mh8)
- [Watching multiple keys - Medium](https://app.codecrafters.io/courses/redis/stages/fp0)
- [Watching missing keys - Easy](https://app.codecrafters.io/courses/redis/stages/uo9)
- [The UNWATCH command - Easy](https://app.codecrafters.io/courses/redis/stages/bn1)
- [Unwatch on EXEC - Easy](https://app.codecrafters.io/courses/redis/stages/fn4)
- [Unwatch on DISCARD - Easy](https://app.codecrafters.io/courses/redis/stages/hq1)

## Replication

- [Configure listening port - Easy](https://app.codecrafters.io/courses/redis/stages/bw1)
- [The INFO command - Easy](https://app.codecrafters.io/courses/redis/stages/ye5)
- [The INFO command on a replica - Medium](https://app.codecrafters.io/courses/redis/stages/hc6)
- [Initial replication ID and offset - Easy](https://app.codecrafters.io/courses/redis/stages/xc1)
- [Send handshake (1/3) - Easy](https://app.codecrafters.io/courses/redis/stages/gl7)
- [Send handshake (2/3) - Easy](https://app.codecrafters.io/courses/redis/stages/eh4)
- [Send handshake (3/3) - Medium](https://app.codecrafters.io/courses/redis/stages/ju6)
- [Receive handshake (1/2) - Easy](https://app.codecrafters.io/courses/redis/stages/fj0)
- [Receive handshake (2/2) - Easy](https://app.codecrafters.io/courses/redis/stages/vm3)
- [Empty RDB transfer - Easy](https://app.codecrafters.io/courses/redis/stages/cf8)
- [Single-replica propagation - Medium](https://app.codecrafters.io/courses/redis/stages/zn8)
- [Multi-replica propagation - Hard](https://app.codecrafters.io/courses/redis/stages/hd5)
- [Command processing - Hard](https://app.codecrafters.io/courses/redis/stages/yg4)
- [ACKs with no commands - Easy](https://app.codecrafters.io/courses/redis/stages/xv6)
- [ACKs with commands - Medium](https://app.codecrafters.io/courses/redis/stages/yd3)
- [WAIT with no replicas - Medium](https://app.codecrafters.io/courses/redis/stages/my8)
- [WAIT with no commands - Medium](https://app.codecrafters.io/courses/redis/stages/tu8)
- [WAIT with multiple commands - Hard](https://app.codecrafters.io/courses/redis/stages/na2)

## RDB Persistence

- [RDB file config - Easy](https://app.codecrafters.io/courses/redis/stages/zg5)
- [Read a key - Medium](https://app.codecrafters.io/courses/redis/stages/jz6)
- [Read a string value - Medium](https://app.codecrafters.io/courses/redis/stages/gc6)
- [Read multiple keys - Medium](https://app.codecrafters.io/courses/redis/stages/jw4)
- [Read multiple string values - Medium](https://app.codecrafters.io/courses/redis/stages/dq3)
- [Read value with expiry - Medium](https://app.codecrafters.io/courses/redis/stages/sm4)

## AOF Persistence

- [Default AOF options - Easy](https://app.codecrafters.io/courses/redis/stages/uj3)
- [AOF options from flags - Easy](https://app.codecrafters.io/courses/redis/stages/vd9)
- [Create append-only directory - Easy](https://app.codecrafters.io/courses/redis/stages/fm0)
- [Create append-only file - Easy](https://app.codecrafters.io/courses/redis/stages/dw4)
- [Create manifest file - Easy](https://app.codecrafters.io/courses/redis/stages/pb9)
- [Write a single command - Hard](https://app.codecrafters.io/courses/redis/stages/dc8)
- [Write multiple commands - Medium](https://app.codecrafters.io/courses/redis/stages/fi1)
- [Filter write commands - Easy](https://app.codecrafters.io/courses/redis/stages/ep6)
- [Replay a single command - Hard](https://app.codecrafters.io/courses/redis/stages/xz2)
- [Replay multiple commands - Medium](https://app.codecrafters.io/courses/redis/stages/kn2)

## Pub/Sub

- [Subscribe to a channel - Easy](https://app.codecrafters.io/courses/redis/stages/mx3)
- [Subscribe to multiple channels - Easy](https://app.codecrafters.io/courses/redis/stages/zc8)
- [Enter subscribed mode - Medium](https://app.codecrafters.io/courses/redis/stages/aw8)
- [PING in subscribed mode - Easy](https://app.codecrafters.io/courses/redis/stages/lf1)
- [Publish a message - Easy](https://app.codecrafters.io/courses/redis/stages/hf2)
- [Deliver messages - Hard](https://app.codecrafters.io/courses/redis/stages/dn4)
- [Unsubscribe - Medium](https://app.codecrafters.io/courses/redis/stages/ze9)

## Sorted Sets

- [Create a sorted set - Easy](https://app.codecrafters.io/courses/redis/stages/ct1)
- [Add members - Medium](https://app.codecrafters.io/courses/redis/stages/hf1)
- [Retrieve member rank - Medium](https://app.codecrafters.io/courses/redis/stages/lg6)
- [List sorted set members - Easy](https://app.codecrafters.io/courses/redis/stages/ic1)
- [ZRANGE with negative indexes - Easy](https://app.codecrafters.io/courses/redis/stages/bj4)
- [Count sorted set members - Easy](https://app.codecrafters.io/courses/redis/stages/kn4)
- [Retrieve member score - Medium](https://app.codecrafters.io/courses/redis/stages/gd7)
- [Remove a member - Easy](https://app.codecrafters.io/courses/redis/stages/sq7)

## Geospatial Commands

- [Respond to GEOADD - Easy](https://app.codecrafters.io/courses/redis/stages/zt4)
- [Validate coordinates - Easy](https://app.codecrafters.io/courses/redis/stages/ck3)
- [Store a location - Medium](https://app.codecrafters.io/courses/redis/stages/tn5)
- [Calculate location score - Hard](https://app.codecrafters.io/courses/redis/stages/cr3)
- [Respond to GEOPOS - Easy](https://app.codecrafters.io/courses/redis/stages/xg4)
- [Decode coordinates - Hard](https://app.codecrafters.io/courses/redis/stages/hb5)
- [Calculate distance - Medium](https://app.codecrafters.io/courses/redis/stages/ek6)
- [Search within radius - Easy](https://app.codecrafters.io/courses/redis/stages/rm9)

## Authentication

- [Respond to ACL WHOAMI - Easy](https://app.codecrafters.io/courses/redis/stages/jn4)
- [Respond to ACL GETUSER - Easy](https://app.codecrafters.io/courses/redis/stages/gx8)
- [The nopass flag - Easy](https://app.codecrafters.io/courses/redis/stages/ql6)
- [The passwords property - Easy](https://app.codecrafters.io/courses/redis/stages/pl7)
- [Setting default user password - Medium](https://app.codecrafters.io/courses/redis/stages/uv9)
- [The AUTH command - Medium](https://app.codecrafters.io/courses/redis/stages/hz3)
- [Enforce authentication - Medium](https://app.codecrafters.io/courses/redis/stages/nm2)
- [Authenticate using AUTH - Medium](https://app.codecrafters.io/courses/redis/stages/ws7)
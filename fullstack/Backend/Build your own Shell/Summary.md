Un intérprete de comandos es el programa que interpreta lo que escribes en la terminal. Lee tus comandos, ejecuta programas e imprime su resultado. Algunos ejemplos populares son Bash y ZSH.
En este desafío, construirás tu propia carcasa desde cero.
Tu intérprete de comandos ejecutará un REPL, analizará comandos, creará procesos y mucho más.

## ¿Qué voy a construir exactamente?
Comenzarás implementando los bloques de construcción principales de cualquier shell:

- Leer y analizar la entrada del usuario
- Comandos integrados (built-in) como `pwd` y `cd`
- Iniciar programas externos

En esta etapa, tu shell ya se sentirá utilizable. Podrás escribir comandos, ver su salida y navegar dentro de tu sistema de archivos.

A medida que progreses, implementarás funciones avanzadas como:

- Tuberías (pipes) y redirección
- Historial de comandos
- Autocompletado
- … y más

Al final, tendrás un repositorio de GitHub para presumir.

## ¿Qué voy a aprender exactamente?

En las primeras 10 etapas, aprenderás:

- Cómo un shell lee, analiza y ejecuta comandos (¡no es magia!)
- Qué es un REPL y cómo funciona internamente
- Cómo se ejecutan los comandos incorporados como `echo`, frente a los externos (como `cursor`)
- Qué significa `$PATH` y su papel en la identificación de archivos ejecutables
- Cómo la ejecución de comandos requiere la creación de procesos del sistema operativo y sus salidas

En las etapas avanzadas, descubrirás nuevas ideas de programación, como el análisis de sintaxis complejas y la gestión de procesos.

A medida que tu código se vuelva más complejo, te verás obligado a estructurarlo y refactorizarlo, para evitar regresiones y facilitar la adición de nuevas funciones.

## ¿Por qué debería construir un proyecto así?
Crear tu propio intérprete de comandos combina diseño de sistemas, práctica avanzada de programación y conocimientos informáticos prácticos (conector + sistema operativo). Si hasta ahora solo has trabajado con código web o de aplicaciones, tendrás la oportunidad de comprender mejor cómo tu ordenador ejecuta el software.
Más allá de la profundidad técnica, comprender una herramienta que se usa a diario tiene una satisfacción única. Te convertirás en un desarrollador más seguro y con mayor capacidad para generar interés.

## ¿Cuáles son los requisitos previos para este desafío?

Debes sentirte cómodo escribiendo código en cualquier lenguaje y utilizando Git. No se requiere experiencia previa con shells ni sistemas operativos.

La mayoría de los estudiantes van adquiriendo los conceptos necesarios (por ejemplo, los procesos) a medida que avanzan.

Lo más importante es la curiosidad y la perseverancia. Desarrollarás tu intuición explorando, depurando y descubriendo soluciones por ti mismo.

Aunque haremos que sea extremadamente sencillo comenzar, no esperes que esto sea un tutorial paso a paso.

# Etapas

## Conceptos Básicos
*   [Imprimir un prompt](https://app.codecrafters.io/courses/shell/introduction)
*   [Manejar comandos inválidos](https://app.codecrafters.io/courses/shell/stages/cz2)
*   [Implementar un REPL](https://app.codecrafters.io/courses/shell/stages/ff0)
*   [Implementar exit](https://app.codecrafters.io/courses/shell/stages/pn5)
*   [Implementar echo](https://app.codecrafters.io/courses/shell/stages/iz3) 
*   [Implementar type](https://app.codecrafters.io/courses/shell/stages/ez5)
*   [Localizar archivos ejecutables](https://app.codecrafters.io/courses/shell/stages/mg5)
*   [Ejecutar un programa](https://app.codecrafters.io/courses/shell/stages/ip1)

## Navegación
*   [El comando integrado pwd](https://app.codecrafters.io/courses/shell/stages/ei0)
*   [El comando integrado cd: Rutas absolutas](https://app.codecrafters.io/courses/shell/stages/ra6)
*   [El comando integrado cd: Rutas relativas](https://app.codecrafters.io/courses/shell/stages/gq9)
*   [El comando integrado cd: Directorio personal](https://app.codecrafters.io/courses/shell/stages/gp4)

## Uso de Comillas (Quoting)
*   [Comillas simples](https://app.codecrafters.io/courses/shell/stages/ni6)
*   [Comillas dobles](https://app.codecrafters.io/courses/shell/stages/tg6)
*   [Barra invertida fuera de comillas](https://app.codecrafters.io/courses/shell/stages/yt5)
*   [Barra invertida dentro de comillas simples](https://app.codecrafters.io/courses/shell/stages/le5)
*   [Barra invertida dentro de comillas dobles](https://app.codecrafters.io/courses/shell/stages/gu3)
*   [Ejecutar un ejecutable entrecomillado](https://app.codecrafters.io/courses/shell/stages/qj0)

## Redirección
*   [Redirigir stdout](https://app.codecrafters.io/courses/shell/stages/jv1)
*   [Redirigir stderr](https://app.codecrafters.io/courses/shell/stages/vz4)
*   [Adjuntar stdout](https://app.codecrafters.io/courses/shell/stages/el9)
*   [Adjuntar stderr](https://app.codecrafters.io/courses/shell/stages/un3)

## Autocompletado de Comandos
*   [Autocompletar comandos integrados](https://app.codecrafters.io/courses/shell/stages/qp2)
*   [Autocompletar con argumentos](https://app.codecrafters.io/courses/shell/stages/gm9)
*   [Autocompletados faltantes](https://app.codecrafters.io/courses/shell/stages/qm8)
*   [Autocompletar ejecutables](https://app.codecrafters.io/courses/shell/stages/gy5)
*   [Múltiples autocompletados](https://app.codecrafters.io/courses/shell/stages/wh6)
*   [Autocompletados parciales](https://app.codecrafters.io/courses/shell/stages/wt6)

## Autocompletado de Nombres de Archivos
*   [Autocompletar archivos](https://app.codecrafters.io/courses/shell/stages/zv2)
*   [Autocompletar archivos anidados](https://app.codecrafters.io/courses/shell/stages/ue6)
*   [Autocompletar directorios](https://app.codecrafters.io/courses/shell/stages/lc6)
*   [Autocompletados faltantes](https://app.codecrafters.io/courses/shell/stages/vs5)
*   [Múltiples coincidencias](https://app.codecrafters.io/courses/shell/stages/no5)
*   [Autocompletados parciales](https://app.codecrafters.io/courses/shell/stages/jp8)
*   [Autocompletado de múltiples argumentos](https://app.codecrafters.io/courses/shell/stages/bf8)

## Autocompletado Programable
*   [Registrar el comando integrado complete](https://app.codecrafters.io/courses/shell/stages/ne7)
*   [Imprimir especificaciones faltantes](https://app.codecrafters.io/courses/shell/stages/oi7)
*   [Mostrar especificaciones registradas](https://app.codecrafters.io/courses/shell/stages/wl6)
*   [Autocompletado simple](https://app.codecrafters.io/courses/shell/stages/pm5)
*   [Manejar la ausencia de autocompletados](https://app.codecrafters.io/courses/shell/stages/qf1)
*   [Pasar argumentos de línea de comandos](https://app.codecrafters.io/courses/shell/stages/zi0)
*   [Pasar variables de entorno](https://app.codecrafters.io/courses/shell/stages/nr7)
*   [Múltiples candidatos para completar](https://app.codecrafters.io/courses/shell/stages/ep2)
*   [Prefijo común más largo](https://app.codecrafters.io/courses/shell/stages/xz3)
*   [Anular el registro de un autocompletado](https://app.codecrafters.io/courses/shell/stages/tz2)

## Trabajos en Segundo Plano (Background Jobs)
*   [El comando integrado jobs](https://app.codecrafters.io/courses/shell/stages/af3)
*   [Iniciar trabajos en segundo plano](https://app.codecrafters.io/courses/shell/stages/at7)
*   [Imprimir la salida de trabajos en segundo plano](https://app.codecrafters.io/courses/shell/stages/si2)
*   [Listar un solo trabajo](https://app.codecrafters.io/courses/shell/stages/jd6)
*   [Listar múltiples trabajos](https://app.codecrafters.io/courses/shell/stages/dk5)
*   [Finalizar (reap) un trabajo](https://app.codecrafters.io/courses/shell/stages/ma9)
*   [Finalizar múltiples trabajos](https://app.codecrafters.io/courses/shell/stages/rq2)
*   [Finalizar antes del siguiente prompt](https://app.codecrafters.io/courses/shell/stages/bv8)
*   [Reciclar números de trabajo](https://app.codecrafters.io/courses/shell/stages/fy4)

## Tuberías (Pipelines)
*   [Tubería de dos comandos](https://app.codecrafters.io/courses/shell/stages/br6)
*   [Tuberías con comandos integrados](https://app.codecrafters.io/courses/shell/stages/ny9)
*   [Tuberías de múltiples comandos](https://app.codecrafters.io/courses/shell/stages/xk3)

## Historial
*   [El comando integrado history](https://app.codecrafters.io/courses/shell/stages/bq4)
*   [Listar el historial](https://app.codecrafters.io/courses/shell/stages/yf5)
*   [Limitar las entradas del historial](https://app.codecrafters.io/courses/shell/stages/ag6)
*   [Navegación con la flecha arriba](https://app.codecrafters.io/courses/shell/stages/rh7)
*   [Navegación con la flecha abajo](https://app.codecrafters.io/courses/shell/stages/vq0)
*   [Ejecutar comandos desde el historial](https://app.codecrafters.io/courses/shell/stages/dm2)

## Persistencia del Historial
*   [Leer historial desde un archivo](https://app.codecrafters.io/courses/shell/stages/za2)
*   [Escribir historial en un archivo](https://app.codecrafters.io/courses/shell/stages/in3)
*   [Adjuntar historial a un archivo](https://app.codecrafters.io/courses/shell/stages/sx3)
*   [Leer historial al iniciar](https://app.codecrafters.io/courses/shell/stages/zp4)
*   [Escribir historial al salir](https://app.codecrafters.io/courses/shell/stages/kz7)
*   [Adjuntar historial al salir](https://app.codecrafters.io/courses/shell/stages/jv2)

## Expansión de Parámetros
*   [El comando integrado declare](https://app.codecrafters.io/courses/shell/stages/ji0)
*   [Imprimir variables no definidas](https://app.codecrafters.io/courses/shell/stages/oa2)
*   [Almacenar variables de shell](https://app.codecrafters.io/courses/shell/stages/kv5)
*   [Validar nombres de variables](https://app.codecrafters.io/courses/shell/stages/db8)
*   [Expandir variables](https://app.codecrafters.io/courses/shell/stages/ge9)
*   [Expansión con llaves](https://app.codecrafters.io/courses/shell/stages/br2)
*   [Expandir variables vacías](https://app.codecrafters.io/courses/shell/stages/my0)
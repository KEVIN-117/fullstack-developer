# Historia de la IA moderna y sus aplicaciones
## Introducción a la inteligencia artificial y al aprendizaje automático

La Inteligencia Artificial es una rama de la informática que se ocupa de la simulación del comportamiento inteligente en los ordenadores. Las máquinas imitan funciones cognitivas como el aprendizaje y la resolución de problemas.

El aprendizaje automático es el estudio de programas que no se programan explícitamente, sino que estos algoritmos aprenden patrones a partir de datos.

El aprendizaje profundo es un subconjunto del aprendizaje automático en el que las redes neuronales multicapa aprenden a partir de grandes cantidades de datos.

## Historia de la IA

La IA ha experimentado ciclos de inviernos de IA y auges de IA.

Las soluciones de la IA incluyen el reconocimiento del habla, la visión por ordenador, el diagnóstico médico asistido y la robótica, entre otras.

## La IA moderna

Los factores que han contribuido al estado actual del aprendizaje automático son: conjuntos de datos más grandes, ordenadores más rápidos, paquetes de código abierto y una amplia gama de arquitecturas de redes neuronales.

## Flujo de trabajo del aprendizaje automático

El flujo de trabajo del aprendizaje automático consiste en

- Planteamiento del problema
    
- Recogida de datos
    
- Exploración y preprocesamiento de datos
    
- Modelado
    
- Validación
    
- Toma de decisiones y despliegue
    

Este es un resumen de la taxonomía común de los datos en los paquetes de código abierto para el aprendizaje automático:

- objetivo: categoría o valor que se intenta predecir
    
- características: variables explicativas utilizadas para la predicción
    
- ejemplo: una observación o un único punto dentro de los datos
    
- etiqueta: el valor del objetivo para un único punto de datos

---
# Recuperación y Limpieza de datos 

## Recuperación de datos de archivos CSV y JSON
Esta sección del curso se centra en cómo recuperar datos desde diferentes fuentes para análisis y aprendizaje automático.

Lectura de archivos CSV
- Los archivos CSV contienen datos separados por comas y pueden ser leídos fácilmente con la función `pd.read_csv` de la biblioteca Pandas en Python.
- Se pueden usar argumentos para manejar diferentes separadores, definir encabezados, nombrar columnas y especificar valores nulos.

Lectura de archivos JSON
- Los archivos JSON almacenan datos en un formato estructurado similar a diccionarios de Python, común en bases de datos `NoSQL` y `APIs`.
- Para leer JSON en Pandas se usa `read_json`, con varios argumentos para adaptarse a diferentes estructuras de datos JSON.

Consideraciones prácticas
- Es importante conocer las opciones y argumentos de las funciones para manejar correctamente los datos según su formato y estructura.
- También se mencionan brevemente las funciones para escribir datos en formato JSON desde un `DataFrame` de Pandas.
## Recuperación de datos de DB, API y la nube

Esta lección se centra en cómo trabajar con diferentes tipos de bases de datos y fuentes de datos para extraer información útil en Python.
Bases de datos SQL
- SQL (`Structured Query Language`) se usa para bases de datos relacionales con esquemas fijos, como `Microsoft SQL Server`, `Postgres`, `MySQL`, entre otros.
- En Python, se puede conectar a estas bases usando librerías específicas (ej. `sqlite3`, `SQLAlchemy`, `Psycopg2`) y extraer datos con consultas SQL que luego se convierten en `DataFrames` de Pandas.

Bases de datos NoSQL
- NoSQL incluye bases de datos no relacionales que almacenan datos en formatos más flexibles, comúnmente JSON.
- Ejemplos incluyen bases de documentos (`MongoDB`), bases de grafos (para análisis de redes) y bases de columnas anchas.
- Para `MongoDB`, se usa la librería `pymongo` para conectar, consultar colecciones y convertir los resultados en `DataFrames` de Pandas.

Acceso a datos vía `APIs` y en la nube
- Muchas fuentes de datos ofrecen `APIs` para acceder a datos en tiempo real, como Twitter o Amazon.
- También se pueden cargar `datasets` desde `URLs` directamente en Pandas usando funciones como `read_csv`.
- Se mencionan posibles problemas comunes al importar datos y la importancia de manejar correctamente los formatos y argumentos en las funciones.

## Limpieza de datos

La importancia de limpiar los datos para el aprendizaje automático

Importancia de la limpieza de datos
- Los modelos de machine learning solo son tan buenos como la calidad de los datos que reciben; datos sucios pueden llevar a resultados poco confiables ("garbage-in, garbage-out").
- Observaciones incorrectas o mal etiquetadas pueden distorsionar la relación entre características y etiquetas, afectando la precisión del modelo.

Problemas comunes con los datos
- Falta de datos relevantes puede impedir el éxito del modelo, mientras que exceso de datos dispersos genera problemas de ingeniería de datos.
- Datos duplicados, errores tipográficos, datos faltantes, valores atípicos y problemas de integración de múltiples fuentes pueden complicar el análisis y modelado.

Manejo de datos duplicados
- Es importante evaluar si los duplicados son reales o errores; por ejemplo, duplicados exactos en imágenes no aportan valor, pero observaciones idénticas en mediciones pueden ser válidas.
- Se recomienda revisar y filtrar cuidadosamente los datos para identificar duplicados sin perder información útil para el análisis posterior.
### Manejo de valores perdidos y valores atípicos

Manejo de valores faltantes

- Los modelos no aceptan valores en blanco, por lo que se debe decidir cómo tratarlos: eliminar filas o columnas, imputar valores o enmascarar los datos faltantes.
- Eliminar filas es rápido pero puede perder información o sesgar el conjunto; imputar valores mantiene datos pero añade incertidumbre; enmascarar trata los faltantes como una categoría que puede tener significado.

Detección y manejo de valores atípicos

- Los valores atípicos son observaciones que difieren significativamente del resto y pueden distorsionar modelos si no se manejan adecuadamente.
- Algunos atípicos pueden contener información valiosa, por lo que no siempre deben eliminarse sin análisis.

Herramientas y métodos para identificar valores atípicos

- Se pueden usar gráficos como histogramas, diagramas de caja y análisis de residuos para detectar atípicos.
- Matemáticamente, se calcula el rango intercuartílico (IQR) y se definen límites para identificar valores fuera de rango como atípicos, usando percentiles 25 y 75 y multiplicando el IQR por 1.5 para establecer umbrales.

### Manejo de valores perdidos y valores atípicos mediante residuos

Concepto de residuos y detección de valores atípicos
- Los residuos son la diferencia entre el valor real y el valor predicho por un modelo, representando fallos del modelo.
- Para detectar valores atípicos se pueden usar residuos estandarizados, residuos eliminados y residuos estudiados, que ajustan los residuos según el rango y la influencia de cada observación.

Manejo de valores atípicos
- Se pueden eliminar los valores atípicos, aunque esto puede implicar perder datos importantes.
- Otra opción es asignar un valor diferente al atípico o transformar la columna (por ejemplo, con una transformación logarítmica) para reducir su impacto.

Alternativas para tratar valores atípicos
- Predecir el valor atípico usando observaciones similares o regresión, aunque esto requiere más trabajo y puede perder información valiosa.
- Mantener el valor atípico y usar modelos resistentes a estos, que se abordarán en cursos posteriores.

Resumen general

- La limpieza de datos es crucial para que los algoritmos aprendan correctamente.
- Se deben identificar y manejar datos duplicados, faltantes y valores atípicos para construir modelos sólidos.
- La próxima lección abordará el análisis exploratorio de datos como siguiente paso en el flujo de trabajo de Machine Learning.

## Resumen
## Recuperación de datos

Puede recuperar datos de múltiples fuentes:

- Bases de datos SQL
    
- Bases de datos NoSQL
    
- APIs
    
- Fuentes de datos en la nube
    

Los dos formatos más comunes para archivos planos de datos delimitados son separados por comas (csv) y separados por tabulaciones (tsv). También es posible utilizar caracteres especiales como separadores.

SQL representa un conjunto de bases de datos relacionales con esquemas fijos.

## Lectura de archivos de bases de datos

Los pasos para leer en un archivo de base de datos utilizando la biblioteca sqlite son:

- crear una variable path que haga referencia a la ruta de acceso a la base de datos
    
- crear una variable de conexión que haga referencia a la conexión con la base de datos
    
- crear una variable de consulta que contenga la consulta SQL que lee la tabla de datos de la base de datos
    
- crear una variable observations para asignar las funciones read_sql del paquete pandas
    
- crear una variable tables para leer los datos de la tabla sqlite_master
    

Los archivos JSON son una forma estándar de almacenar datos en todas las plataformas. Su estructura es similar a la de los diccionarios de Python.

Las bases de datos NoSQL no son relacionales y varían más en su estructura. La mayoría de las bases de datos NoSQL almacenan datos en formato JSON.

## Limpieza de datos

La limpieza de datos es importante porque los datos desordenados conducirán a resultados poco fiables. Algunos problemas comunes que hacen que los datos sean desordenados son: datos duplicados o innecesarios, datos incoherentes y errores tipográficos, datos que faltan, valores atípicos y problemas con la fuente de datos.

Se pueden identificar los datos duplicados o innecesarios.

Las políticas habituales para tratar los datos que faltan son: eliminar una fila con columnas que faltan, imputar los datos que faltan y enmascarar los datos creando una categoría para los valores que faltan.

Los métodos comunes para encontrar valores atípicos son: a través de gráficos, estadísticas o residuos.

Las políticas habituales para tratar los valores atípicos son: eliminar los valores atípicos, imputarlos, utilizar una transformación de variables o utilizar un modelo resistente a los valores atípicos.